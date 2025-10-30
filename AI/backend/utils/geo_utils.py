"""Geographic utilities for distance calculation"""
import math
import numpy as np
from typing import Tuple
from config import EARTH_RADIUS_KM


def haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth
    using the Haversine formula.

    Args:
        lat1: Latitude of first point
        lng1: Longitude of first point
        lat2: Latitude of second point
        lng2: Longitude of second point

    Returns:
        Distance in kilometers
    """
    # Convert decimal degrees to radians
    lat1_rad = math.radians(lat1)
    lng1_rad = math.radians(lng1)
    lat2_rad = math.radians(lat2)
    lng2_rad = math.radians(lng2)

    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad

    a = (
        math.sin(dlat / 2) ** 2 +
        math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))

    # Distance in kilometers
    distance = EARTH_RADIUS_KM * c

    return round(distance, 2)


def calculate_distances_vectorized(
    start_lat: float,
    start_lng: float,
    lats: np.ndarray,
    lngs: np.ndarray
) -> np.ndarray:
    """
    Calculate distances from a start point to multiple points using vectorized operations.

    Args:
        start_lat: Starting latitude
        start_lng: Starting longitude
        lats: Array of latitudes
        lngs: Array of longitudes

    Returns:
        Array of distances in kilometers
    """
    # Convert to radians
    start_lat_rad = math.radians(start_lat)
    start_lng_rad = math.radians(start_lng)
    lats_rad = np.radians(lats)
    lngs_rad = np.radians(lngs)

    # Haversine formula (vectorized)
    dlat = lats_rad - start_lat_rad
    dlng = lngs_rad - start_lng_rad

    a = (
        np.sin(dlat / 2) ** 2 +
        np.cos(start_lat_rad) * np.cos(lats_rad) * np.sin(dlng / 2) ** 2
    )
    c = 2 * np.arcsin(np.sqrt(a))

    distances = EARTH_RADIUS_KM * c

    return np.round(distances, 2)


def calculate_total_route_distance(coordinates: list) -> float:
    """
    Calculate total distance for a route with multiple waypoints.

    Args:
        coordinates: List of (lat, lng) tuples

    Returns:
        Total distance in kilometers
    """
    if len(coordinates) < 2:
        return 0.0

    total_distance = 0.0
    for i in range(len(coordinates) - 1):
        lat1, lng1 = coordinates[i]
        lat2, lng2 = coordinates[i + 1]
        total_distance += haversine_distance(lat1, lng1, lat2, lng2)

    return round(total_distance, 2)


def estimate_travel_time(distance_km: float, avg_speed_kmh: float = 40) -> float:
    """
    Estimate travel time based on distance and average speed.

    Args:
        distance_km: Distance in kilometers
        avg_speed_kmh: Average speed in km/h (default: 40 km/h for local roads)

    Returns:
        Time in hours
    """
    if distance_km <= 0:
        return 0.0

    time_hours = distance_km / avg_speed_kmh
    return round(time_hours, 2)


def is_within_radius(
    center_lat: float,
    center_lng: float,
    point_lat: float,
    point_lng: float,
    radius_km: float
) -> bool:
    """
    Check if a point is within a given radius from a center point.

    Args:
        center_lat: Center latitude
        center_lng: Center longitude
        point_lat: Point latitude
        point_lng: Point longitude
        radius_km: Radius in kilometers

    Returns:
        True if point is within radius, False otherwise
    """
    distance = haversine_distance(center_lat, center_lng, point_lat, point_lng)
    return distance <= radius_km
