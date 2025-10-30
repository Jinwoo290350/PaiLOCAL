"""Carbon footprint calculator service"""
import pandas as pd
from typing import List, Tuple
from config import TRANSPORT_CARBON_PER_KM


class CarbonCalculator:
    """Calculate carbon footprint for trips"""

    @staticmethod
    def calculate_transport_carbon(distance_km: float) -> float:
        """
        Calculate carbon emissions from transportation.

        Args:
            distance_km: Distance traveled in kilometers

        Returns:
            Carbon emissions in kg CO2
        """
        return round(distance_km * TRANSPORT_CARBON_PER_KM, 2)

    @staticmethod
    def calculate_place_carbon(
        place_row: pd.Series,
        distance_from_prev_km: float
    ) -> float:
        """
        Calculate total carbon for visiting a place.

        Args:
            place_row: DataFrame row for the place
            distance_from_prev_km: Distance traveled to reach this place

        Returns:
            Total carbon in kg CO2
        """
        # Transport carbon
        transport_carbon = CarbonCalculator.calculate_transport_carbon(
            distance_from_prev_km
        )

        # Activity carbon (from pre-calculated features in CSV)
        activity_carbon = place_row.get('activity_carbon_score', 0) * 0.5

        # Visitor carbon factor (from CSV)
        visitor_carbon = place_row.get('visitor_carbon_factor', 0)

        total_carbon = transport_carbon + activity_carbon + visitor_carbon

        return round(total_carbon, 2)

    @staticmethod
    def calculate_trip_carbon(
        places: List[Tuple[pd.Series, float]]
    ) -> float:
        """
        Calculate total carbon for entire trip.

        Args:
            places: List of (place_row, distance_from_prev) tuples

        Returns:
            Total carbon in kg CO2
        """
        total_carbon = 0.0

        for place_row, distance_from_prev in places:
            place_carbon = CarbonCalculator.calculate_place_carbon(
                place_row,
                distance_from_prev
            )
            total_carbon += place_carbon

        return round(total_carbon, 2)

    @staticmethod
    def calculate_eco_score(
        total_carbon_kg: float,
        avg_tourism_score: float,
        avg_rating: float,
        route_efficiency: float
    ) -> float:
        """
        Calculate eco-friendliness score (0-10 scale).

        Args:
            total_carbon_kg: Total carbon emissions
            avg_tourism_score: Average tourism score (0-1)
            avg_rating: Average rating (0-5)
            route_efficiency: Route efficiency score (0-1)

        Returns:
            Eco score (0-10)
        """
        # Normalize carbon (assuming typical trip: 5-20 kg CO2)
        normalized_carbon = min(total_carbon_kg / 20.0, 1.0)

        # Calculate score
        eco_score = (
            (1 - normalized_carbon) * 4 +  # 0-4 points (lower carbon = higher score)
            avg_tourism_score * 3 +          # 0-3 points
            (avg_rating / 5) * 2 +           # 0-2 points
            route_efficiency * 1             # 0-1 points
        )

        # Scale to 0-10
        eco_score = (eco_score / 10) * 10

        return round(max(0, min(10, eco_score)), 1)

    @staticmethod
    def calculate_carbon_reduction_percent(
        total_carbon_kg: float,
        baseline_carbon_kg: float = 15.0
    ) -> float:
        """
        Calculate carbon reduction percentage compared to baseline.

        Args:
            total_carbon_kg: Actual carbon emissions
            baseline_carbon_kg: Baseline/average carbon emissions (default: 15 kg)

        Returns:
            Reduction percentage (0-100)
        """
        if baseline_carbon_kg <= 0:
            return 0.0

        reduction = ((baseline_carbon_kg - total_carbon_kg) / baseline_carbon_kg) * 100

        return round(max(0, min(100, reduction)), 1)

    @staticmethod
    def get_carbon_level(carbon_kg: float) -> str:
        """
        Get carbon level category.

        Args:
            carbon_kg: Carbon emissions in kg

        Returns:
            Category: 'low', 'medium', or 'high'
        """
        if carbon_kg < 5:
            return "low"
        elif carbon_kg < 12:
            return "medium"
        else:
            return "high"
