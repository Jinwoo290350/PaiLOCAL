"""
Trip Narrator Service
Generates human-readable trip summaries and route narratives using LLM.
"""

import logging
from typing import List, Dict, Any
import pandas as pd

logger = logging.getLogger(__name__)


class TripNarrator:
    """Generates narrative descriptions of trips"""

    def __init__(self):
        """Initialize trip narrator"""
        pass

    def generate_trip_summary(
        self,
        places: List[Dict],
        start_location: Dict[str, float],
        total_distance: float,
        total_carbon: float,
        eco_score: float,
        theme: str = None
    ) -> str:
        """
        Generate a narrative summary of the trip.

        Args:
            places: List of place dictionaries
            start_location: Dict with 'lat' and 'lng'
            total_distance: Total distance in km
            total_carbon: Total carbon in kg CO2
            eco_score: Eco score (0-10)
            theme: Theme used for planning (if any)

        Returns:
            Human-readable trip summary
        """
        if not places:
            return "No places found for this trip."

        # Count keywords
        keywords = {}
        for place in places:
            keyword = place.get('keyword', 'สถานที่')
            keywords[keyword] = keywords.get(keyword, 0) + 1

        keyword_summary = ", ".join([f"{k} {v} แห่ง" for k, v in keywords.items()])

        # Build narrative
        narrative = []

        # Opening
        if theme:
            narrative.append(f"🌟 **ทริป {theme}** ที่จะพาคุณเที่ยว {len(places)} สถานที่")
        else:
            narrative.append(f"🌟 **ทริปของคุณ** ประกอบด้วย {len(places)} สถานที่")

        # Place types
        narrative.append(f"   รวม {keyword_summary}")
        narrative.append("")

        # Route description
        narrative.append("📍 **เส้นทางการเดินทาง:**")

        for i, place in enumerate(places, 1):
            name = place['name']
            keyword = place.get('keyword', 'สถานที่')
            dist_from_prev = place.get('distance_from_prev_km', 0)
            dist_from_start = place.get('distance_from_start_km', 0)
            rating = place.get('rating', 0)
            carbon = place.get('carbon_footprint_kg', 0)

            # Format rating
            stars = "⭐" * int(rating) if rating else "•"

            if i == 1:
                narrative.append(f"   **{i}. {name}** ({keyword}) - {stars} {rating}/5")
                narrative.append(f"      ระยะทางจากจุดเริ่มต้น: {dist_from_start:.1f} km")
            else:
                narrative.append(f"   **{i}. {name}** ({keyword}) - {stars} {rating}/5")
                narrative.append(f"      ↓ ระยะทาง {dist_from_prev:.1f} km | คาร์บอน {carbon:.2f} kg CO2")

        narrative.append("")

        # Summary stats
        narrative.append("📊 **สรุปทริป:**")
        narrative.append(f"   • ระยะทางรวม: **{total_distance:.1f} km**")
        narrative.append(f"   • คาร์บอนฟุตพริ้นท์: **{total_carbon:.1f} kg CO2**")
        narrative.append(f"   • Eco Score: **{eco_score:.1f}/10** {self._get_eco_rating(eco_score)}")

        # Eco recommendation
        if eco_score >= 7:
            narrative.append("")
            narrative.append("✅ **ทริปนี้เป็นมิตรกับสิ่งแวดล้อม!** คาร์บอนต่ำและเส้นทางมีประสิทธิภาพ")
        elif eco_score >= 5:
            narrative.append("")
            narrative.append("⚠️  **ทริปนี้ใช้คาร์บอนปานกลาง** ลองเลือกสถานที่ใกล้กันมากขึ้นเพื่อลดคาร์บอน")
        else:
            narrative.append("")
            narrative.append("🔴 **ทริปนี้ใช้คาร์บอนสูง** แนะนำให้ลดจำนวนสถานที่หรือเลือกที่ใกล้กันมากขึ้น")

        return "\n".join(narrative)

    def generate_route_directions(self, places: List[Dict]) -> List[str]:
        """
        Generate step-by-step route directions.

        Args:
            places: List of place dictionaries

        Returns:
            List of direction strings
        """
        directions = []

        for i, place in enumerate(places, 1):
            name = place['name']
            dist_from_prev = place.get('distance_from_prev_km', 0)

            if i == 1:
                directions.append(f"🚗 เริ่มต้นที่ **{name}**")
            else:
                direction = self._calculate_direction(
                    places[i-2]['lat'],
                    places[i-2]['lng'],
                    place['lat'],
                    place['lng']
                )
                directions.append(f"🚗 มุ่งหน้า{direction} {dist_from_prev:.1f} km ไปยัง **{name}**")

        return directions

    def _calculate_direction(self, lat1: float, lng1: float, lat2: float, lng2: float) -> str:
        """Calculate cardinal direction between two points"""
        dlat = lat2 - lat1
        dlng = lng2 - lng1

        # Determine primary direction
        if abs(dlat) > abs(dlng):
            primary = "ทิศเหนือ" if dlat > 0 else "ทิศใต้"
        else:
            primary = "ทิศตะวันออก" if dlng > 0 else "ทิศตะวันตก"

        # Determine secondary direction
        if abs(dlat) > 0.01 and abs(dlng) > 0.01:
            if dlat > 0:
                secondary = "เหนือ" if dlng > 0 else "ตะวันออก" if dlng > 0 else "ตะวันตก"
            else:
                secondary = "ใต้"

            # Combine
            if dlat > 0 and dlng > 0:
                return "ทิศตะวันออกเหนือ"
            elif dlat > 0 and dlng < 0:
                return "ทิศตะวันตกเหนือ"
            elif dlat < 0 and dlng > 0:
                return "ทิศตะวันออกใต้"
            else:
                return "ทิศตะวันตกใต้"

        return primary

    def _get_eco_rating(self, eco_score: float) -> str:
        """Get emoji rating for eco score"""
        if eco_score >= 8:
            return "🌟🌟🌟"
        elif eco_score >= 6:
            return "🌟🌟"
        elif eco_score >= 4:
            return "🌟"
        else:
            return "💨"

    def generate_compact_summary(
        self,
        places: List[Dict],
        total_distance: float,
        total_carbon: float,
        eco_score: float
    ) -> str:
        """
        Generate a compact one-line summary.

        Args:
            places: List of place dictionaries
            total_distance: Total distance in km
            total_carbon: Total carbon in kg CO2
            eco_score: Eco score (0-10)

        Returns:
            Compact summary string
        """
        if not places:
            return "ไม่พบสถานที่"

        # Get unique keywords
        keywords = list(set([p.get('keyword', 'สถานที่') for p in places]))
        keyword_str = keywords[0] if len(keywords) == 1 else f"{len(keywords)} ประเภท"

        return f"เที่ยว {len(places)} แห่ง ({keyword_str}) • {total_distance:.0f} km • {total_carbon:.0f} kg CO2 • Eco {eco_score:.1f}/10"
