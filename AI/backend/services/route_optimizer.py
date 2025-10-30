"""Route optimizer service using improved algorithms"""
import pandas as pd
import numpy as np
from typing import List, Tuple
from utils.geo_utils import haversine_distance


class RouteOptimizer:
    """Optimize route using Nearest Neighbor + 2-opt improvement"""

    @staticmethod
    def optimize_route(
        start_lat: float,
        start_lng: float,
        places_df: pd.DataFrame
    ) -> List[Tuple[int, float, float]]:
        """
        Optimize route using Nearest Neighbor + 2-opt improvement.

        Args:
            start_lat: Starting latitude
            start_lng: Starting longitude
            places_df: DataFrame of places to visit

        Returns:
            List of (index, distance_from_prev, distance_from_start) tuples in optimized order
        """
        if len(places_df) == 0:
            return []

        # Step 1: Get initial route using Nearest Neighbor
        initial_route = RouteOptimizer._nearest_neighbor(
            start_lat, start_lng, places_df
        )

        # Step 2: Improve route using 2-opt
        improved_route = RouteOptimizer._two_opt_improvement(
            start_lat, start_lng, places_df, initial_route
        )

        return improved_route

    @staticmethod
    def _nearest_neighbor(
        start_lat: float,
        start_lng: float,
        places_df: pd.DataFrame
    ) -> List[int]:
        """
        Greedy Nearest Neighbor algorithm - returns list of indices.

        Args:
            start_lat: Starting latitude
            start_lng: Starting longitude
            places_df: DataFrame of places

        Returns:
            List of place indices in visit order
        """
        unvisited = set(places_df.index)
        route = []
        current_lat = start_lat
        current_lng = start_lng

        while unvisited:
            nearest_idx = None
            nearest_dist = float('inf')

            for idx in unvisited:
                place = places_df.loc[idx]
                dist = haversine_distance(
                    current_lat, current_lng,
                    place['lat'], place['lng']
                )

                if dist < nearest_dist:
                    nearest_dist = dist
                    nearest_idx = idx

            if nearest_idx is not None:
                route.append(nearest_idx)
                place = places_df.loc[nearest_idx]
                current_lat = place['lat']
                current_lng = place['lng']
                unvisited.remove(nearest_idx)

        return route

    @staticmethod
    def _two_opt_improvement(
        start_lat: float,
        start_lng: float,
        places_df: pd.DataFrame,
        route: List[int],
        max_iterations: int = 100
    ) -> List[Tuple[int, float, float]]:
        """
        Improve route using 2-opt algorithm.

        2-opt works by removing two edges and reconnecting them in a different way
        to see if it reduces total distance.

        Args:
            start_lat: Starting latitude
            start_lng: Starting longitude
            places_df: DataFrame of places
            route: Initial route (list of indices)
            max_iterations: Maximum number of improvement iterations

        Returns:
            Optimized route with (index, dist_from_prev, dist_from_start) tuples
        """
        if len(route) < 3:
            # Too small for 2-opt, just return as-is
            return RouteOptimizer._calculate_route_details(
                start_lat, start_lng, places_df, route
            )

        improved = True
        iterations = 0

        while improved and iterations < max_iterations:
            improved = False
            iterations += 1

            for i in range(len(route) - 1):
                for j in range(i + 2, len(route)):
                    # Calculate current distance
                    current_dist = RouteOptimizer._calculate_segment_distance(
                        start_lat, start_lng, places_df, route, i, j
                    )

                    # Reverse segment and calculate new distance
                    new_route = route[:i+1] + route[i+1:j+1][::-1] + route[j+1:]
                    new_dist = RouteOptimizer._calculate_segment_distance(
                        start_lat, start_lng, places_df, new_route, i, j
                    )

                    # If improvement found, apply it
                    if new_dist < current_dist:
                        route = new_route
                        improved = True
                        break

                if improved:
                    break

        return RouteOptimizer._calculate_route_details(
            start_lat, start_lng, places_df, route
        )

    @staticmethod
    def _calculate_segment_distance(
        start_lat: float,
        start_lng: float,
        places_df: pd.DataFrame,
        route: List[int],
        i: int,
        j: int
    ) -> float:
        """Calculate distance for a segment of the route."""
        # Get coordinates
        if i == 0:
            lat1, lng1 = start_lat, start_lng
        else:
            place1 = places_df.loc[route[i-1]]
            lat1, lng1 = place1['lat'], place1['lng']

        place2 = places_df.loc[route[i]]
        lat2, lng2 = place2['lat'], place2['lng']

        place3 = places_df.loc[route[j]]
        lat3, lng3 = place3['lat'], place3['lng']

        if j + 1 < len(route):
            place4 = places_df.loc[route[j+1]]
            lat4, lng4 = place4['lat'], place4['lng']
        else:
            return haversine_distance(lat1, lng1, lat2, lng2) + \
                   haversine_distance(lat2, lng2, lat3, lng3)

        # Calculate: (prev -> i) + (j -> next)
        dist = haversine_distance(lat1, lng1, lat2, lng2) + \
               haversine_distance(lat3, lng3, lat4, lng4)

        return dist

    @staticmethod
    def _calculate_route_details(
        start_lat: float,
        start_lng: float,
        places_df: pd.DataFrame,
        route: List[int]
    ) -> List[Tuple[int, float, float]]:
        """
        Calculate detailed route information.

        Args:
            start_lat: Starting latitude
            start_lng: Starting longitude
            places_df: DataFrame of places
            route: List of place indices

        Returns:
            List of (index, distance_from_prev, distance_from_start) tuples
        """
        result = []
        current_lat = start_lat
        current_lng = start_lng
        total_distance = 0.0

        for idx in route:
            place = places_df.loc[idx]
            dist = haversine_distance(
                current_lat, current_lng,
                place['lat'], place['lng']
            )

            total_distance += dist
            result.append((idx, dist, total_distance))

            current_lat = place['lat']
            current_lng = place['lng']

        return result

    @staticmethod
    def calculate_route_efficiency(
        optimized_distance: float,
        total_places: int
    ) -> float:
        """
        Calculate route efficiency score (0-1).

        Args:
            optimized_distance: Total optimized distance
            total_places: Number of places

        Returns:
            Efficiency score (0-1, higher is better)
        """
        if total_places <= 1:
            return 1.0

        # Expected average distance per place (rough estimate)
        avg_expected_distance_per_place = 10  # km

        expected_distance = total_places * avg_expected_distance_per_place
        actual_distance = optimized_distance

        # Calculate efficiency (lower actual vs expected = higher efficiency)
        if expected_distance == 0:
            return 1.0

        efficiency = max(0, 1 - (actual_distance / (expected_distance * 1.5)))

        return round(min(1.0, efficiency), 2)

    @staticmethod
    def get_route_summary(route: List[Tuple[int, float, float]]) -> dict:
        """
        Get summary statistics for the route.

        Args:
            route: List of (index, distance_from_prev, distance_from_start) tuples

        Returns:
            Dictionary with route statistics
        """
        if not route:
            return {
                "total_stops": 0,
                "total_distance_km": 0.0,
                "avg_distance_per_stop_km": 0.0
            }

        total_stops = len(route)
        total_distance = route[-1][2]  # Last element's distance_from_start
        avg_distance = total_distance / total_stops if total_stops > 0 else 0

        return {
            "total_stops": total_stops,
            "total_distance_km": round(total_distance, 2),
            "avg_distance_per_stop_km": round(avg_distance, 2)
        }
