"""Trip planner service with theme-based and place-name-based recommendation"""
import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
import uuid
from config import THEMES, SCORING_WEIGHTS
from utils import get_data_loader, haversine_distance, calculate_distances_vectorized, estimate_travel_time
from services.route_optimizer import RouteOptimizer
from services.carbon_calculator import CarbonCalculator
from services.trip_narrator import TripNarrator


class TripPlanner:
    """Plan trips using rule-based recommendation"""

    def __init__(self):
        self.data_loader = get_data_loader()
        self.route_optimizer = RouteOptimizer()
        self.carbon_calculator = CarbonCalculator()
        self.trip_narrator = TripNarrator()

    def plan_trip(
        self,
        start_lat: float,
        start_lng: float,
        mode: str,
        value: str,
        num_stops: int,
        max_distance_km: float
    ) -> Dict:
        """
        Plan a trip based on mode (theme or place_name).

        Args:
            start_lat: Starting latitude
            start_lng: Starting longitude
            mode: "theme" or "place_name"
            value: Theme name or place name
            num_stops: Number of stops
            max_distance_km: Maximum distance radius

        Returns:
            Trip plan dictionary
        """
        if mode == "theme":
            return self._plan_trip_by_theme(
                start_lat, start_lng, value, num_stops, max_distance_km
            )
        elif mode == "place_name":
            return self._plan_trip_by_place_name(
                start_lat, start_lng, value, num_stops, max_distance_km
            )
        else:
            raise ValueError(f"Invalid mode: {mode}")

    def _plan_trip_by_theme(
        self,
        start_lat: float,
        start_lng: float,
        theme_id: str,
        num_stops: int,
        max_distance_km: float
    ) -> Dict:
        """Plan trip based on theme"""
        # Get theme info
        theme = self._get_theme(theme_id)
        if not theme:
            raise ValueError(f"Theme not found: {theme_id}")

        # Get all places data
        df = self.data_loader.get_data()

        # Filter by distance
        df = self._filter_by_distance(df, start_lat, start_lng, max_distance_km)

        # Filter by theme keywords
        if theme['keywords']:
            df = df[df['keyword'].isin(theme['keywords'])]

        if len(df) == 0:
            raise ValueError("No places found matching criteria")

        # Calculate scores
        df = self._calculate_scores(df, start_lat, start_lng)

        # Select top N places
        selected_places = df.nlargest(min(num_stops, len(df)), 'final_score')

        # Optimize route
        route = self._build_optimized_route(
            start_lat, start_lng, selected_places
        )

        # Build response
        trip_id = f"trip_{uuid.uuid4().hex[:8]}"
        return self._build_trip_response(
            trip_id, start_lat, start_lng, mode="theme",
            theme=theme_id, route=route
        )

    def _plan_trip_by_place_name(
        self,
        start_lat: float,
        start_lng: float,
        place_name: str,
        num_stops: int,
        max_distance_km: float
    ) -> Dict:
        """Plan trip based on a specific place name"""
        # Find the target place
        search_results = self.data_loader.search_by_name(place_name, limit=1)

        if len(search_results) == 0:
            raise ValueError(f"Place not found: {place_name}")

        target_place = search_results.iloc[0]

        # Get all places data
        df = self.data_loader.get_data()

        # Exclude the target place itself
        df = df[df['place_id'] != target_place['place_id']]

        # Filter by distance from START point (not from target place)
        df = self._filter_by_distance(df, start_lat, start_lng, max_distance_km)

        if len(df) == 0:
            raise ValueError("No similar places found")

        # Find similar places
        df = self._find_similar_places(df, target_place)

        # Select top N places
        selected_places = df.nlargest(min(num_stops, len(df)), 'similarity_score')

        # Optimize route
        route = self._build_optimized_route(
            start_lat, start_lng, selected_places
        )

        # Build response
        trip_id = f"trip_{uuid.uuid4().hex[:8]}"
        return self._build_trip_response(
            trip_id, start_lat, start_lng, mode="place_name",
            place_name=target_place['name'], route=route
        )

    def _filter_by_distance(
        self,
        df: pd.DataFrame,
        center_lat: float,
        center_lng: float,
        max_distance_km: float
    ) -> pd.DataFrame:
        """Filter places by distance"""
        distances = calculate_distances_vectorized(
            center_lat, center_lng,
            df['lat'].values, df['lng'].values
        )
        df = df.copy()
        df['distance_from_center'] = distances
        return df[df['distance_from_center'] <= max_distance_km]

    def _calculate_scores(
        self,
        df: pd.DataFrame,
        start_lat: float,
        start_lng: float
    ) -> pd.DataFrame:
        """Calculate weighted scores for places"""
        df = df.copy()

        # Normalize features
        df['rating_normalized'] = df['rating'] / 5.0
        df['popularity_normalized'] = self._normalize_column(df['popularity_score'])
        df['tourism_normalized'] = self._normalize_column(df['tourism_score'])

        # Carbon score (lower carbon = higher score)
        df['carbon_normalized'] = 1 - self._normalize_column(
            df['estimated_transport_carbon_kg']
        )

        # Distance score (closer = higher score)
        df['distance_normalized'] = 1 - self._normalize_column(
            df['distance_from_center']
        )

        # Calculate final weighted score
        df['final_score'] = (
            df['tourism_normalized'] * SCORING_WEIGHTS['tourism_score'] +
            df['rating_normalized'] * SCORING_WEIGHTS['rating'] +
            df['carbon_normalized'] * SCORING_WEIGHTS['carbon'] +
            df['popularity_normalized'] * SCORING_WEIGHTS['popularity'] +
            df['distance_normalized'] * SCORING_WEIGHTS['distance']
        )

        return df

    def _find_similar_places(
        self,
        df: pd.DataFrame,
        target_place: pd.Series
    ) -> pd.DataFrame:
        """Find places similar to target place"""
        df = df.copy()

        # Same or similar keyword
        df['keyword_match'] = (df['keyword'] == target_place['keyword']).astype(float)

        # Similar tourism score
        df['tourism_similarity'] = 1 - np.abs(
            df['tourism_score'] - target_place['tourism_score']
        )

        # Similar rating
        df['rating_similarity'] = 1 - np.abs(
            df['rating'] - target_place['rating']
        ) / 5.0

        # Calculate overall similarity
        df['similarity_score'] = (
            df['keyword_match'] * 0.40 +
            df['tourism_similarity'] * 0.30 +
            df['rating_similarity'] * 0.30
        )

        return df

    def _build_optimized_route(
        self,
        start_lat: float,
        start_lng: float,
        places_df: pd.DataFrame
    ) -> List[Dict]:
        """Build optimized route with all place details"""
        # Optimize route order
        optimized_route = self.route_optimizer.optimize_route(
            start_lat, start_lng, places_df
        )

        route = []
        for stop_number, (idx, dist_from_prev, dist_from_start) in enumerate(optimized_route, 1):
            place = places_df.loc[idx]

            # Calculate carbon for this place
            carbon_kg = self.carbon_calculator.calculate_place_carbon(
                place, dist_from_prev
            )

            # Get photos
            photos = self._get_place_photos(place)

            # Build place dict
            place_dict = {
                "stop_number": stop_number,
                "place_id": str(place['place_id']),
                "name": str(place['name']),
                "keyword": str(place['keyword']),
                "address": str(place['address']),
                "lat": float(place['lat']),
                "lng": float(place['lng']),
                "distance_from_prev_km": float(dist_from_prev),
                "distance_from_start_km": float(dist_from_start),
                "rating": float(place['rating']),
                "user_ratings_total": int(place['user_ratings_total']),
                "tourism_score": float(place['tourism_score']),
                "carbon_kg": float(carbon_kg),
                "photos": photos,
                "has_phone": bool(place['has_phone']),
                "phone": str(place['phone']) if place['has_phone'] else None,
                "has_website": bool(place['has_website']),
                "website": str(place['website']) if place['has_website'] else None,
                "review_summary": str(place['review_summary']) if place['review_summary'] else None
            }

            route.append(place_dict)

        return route

    def _build_trip_response(
        self,
        trip_id: str,
        start_lat: float,
        start_lng: float,
        mode: str,
        route: List[Dict],
        theme: Optional[str] = None,
        place_name: Optional[str] = None
    ) -> Dict:
        """Build complete trip response"""
        if not route:
            raise ValueError("No route generated")

        # Calculate summary
        total_stops = len(route)
        total_distance_km = route[-1]['distance_from_start_km']
        estimated_time_hours = estimate_travel_time(total_distance_km)
        total_carbon_kg = sum(place['carbon_kg'] for place in route)

        # Calculate eco score
        avg_tourism_score = np.mean([place['tourism_score'] for place in route])
        avg_rating = np.mean([place['rating'] for place in route])
        route_efficiency = self.route_optimizer.calculate_route_efficiency(
            total_distance_km, total_stops
        )

        eco_score = self.carbon_calculator.calculate_eco_score(
            total_carbon_kg, avg_tourism_score, avg_rating, route_efficiency
        )

        carbon_reduction_percent = self.carbon_calculator.calculate_carbon_reduction_percent(
            total_carbon_kg
        )

        # Generate narrative summary
        narrative = self.trip_narrator.generate_trip_summary(
            places=route,
            start_location={"lat": start_lat, "lng": start_lng},
            total_distance=total_distance_km,
            total_carbon=total_carbon_kg,
            eco_score=eco_score,
            theme=theme
        )

        # Generate compact summary
        compact_summary = self.trip_narrator.generate_compact_summary(
            places=route,
            total_distance=total_distance_km,
            total_carbon=total_carbon_kg,
            eco_score=eco_score
        )

        # Generate route directions
        directions = self.trip_narrator.generate_route_directions(route)

        # Build response
        response = {
            "trip_id": trip_id,
            "start_location": {
                "lat": start_lat,
                "lng": start_lng
            },
            "mode": mode,
            "summary": {
                "total_stops": total_stops,
                "total_distance_km": round(total_distance_km, 2),
                "estimated_time_hours": round(estimated_time_hours, 2),
                "total_carbon_kg": round(total_carbon_kg, 2),
                "eco_score": round(eco_score, 1),
                "carbon_reduction_percent": round(carbon_reduction_percent, 1),
                "narrative": narrative,
                "compact": compact_summary,
                "directions": directions
            },
            "route": route
        }

        if theme:
            response['theme'] = theme
        if place_name:
            response['place_name'] = place_name

        return response

    def _get_place_photos(self, place: pd.Series) -> List[str]:
        """Get list of photo URLs for a place"""
        photos = []
        for col in ['photo_1', 'photo_2', 'photo_3']:
            if col in place.index:
                photo = place[col]
                if pd.notna(photo) and str(photo).strip() != '':
                    photos.append(str(photo))
        return photos

    def _get_theme(self, theme_id: str) -> Optional[Dict]:
        """Get theme by ID"""
        for theme in THEMES:
            if theme['id'] == theme_id:
                return theme
        return None

    @staticmethod
    def _normalize_column(series: pd.Series) -> pd.Series:
        """Normalize a series to 0-1 range"""
        min_val = series.min()
        max_val = series.max()

        if max_val == min_val:
            return pd.Series([0.5] * len(series), index=series.index)

        return (series - min_val) / (max_val - min_val)
