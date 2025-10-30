"""Pydantic models for API request/response schemas"""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class TripRequest(BaseModel):
    """Request model for planning a trip"""
    start_lat: float = Field(..., ge=-90, le=90, description="Starting latitude")
    start_lng: float = Field(..., ge=-180, le=180, description="Starting longitude")
    mode: Literal["theme", "place_name"] = Field(..., description="Mode: theme or place_name")
    value: str = Field(..., description="Theme name or place name")
    num_stops: int = Field(5, ge=1, le=20, description="Number of stops")
    max_distance_km: float = Field(50, gt=0, description="Maximum distance in km")


class Place(BaseModel):
    """Model for a single place in the trip"""
    stop_number: int
    place_id: str
    name: str
    keyword: str
    address: str
    lat: float
    lng: float
    distance_from_prev_km: float
    distance_from_start_km: float
    rating: float
    user_ratings_total: int
    tourism_score: float
    carbon_kg: float
    photos: List[str]
    has_phone: bool
    phone: Optional[str]
    has_website: bool
    website: Optional[str]
    review_summary: Optional[str]


class TripSummary(BaseModel):
    """Summary statistics for the trip"""
    total_stops: int
    total_distance_km: float
    estimated_time_hours: float
    total_carbon_kg: float
    eco_score: float
    carbon_reduction_percent: float


class TripResponse(BaseModel):
    """Response model for trip planning"""
    trip_id: str
    start_location: dict
    mode: str
    theme: Optional[str] = None
    place_name: Optional[str] = None
    summary: TripSummary
    route: List[Place]


class Theme(BaseModel):
    """Model for a theme"""
    id: str
    name: str
    name_th: str
    subtitle: str
    icon: str
    keywords: List[str]
    carbon_level: str
    description: str


class ThemesResponse(BaseModel):
    """Response model for themes list"""
    themes: List[Theme]


class SearchPlace(BaseModel):
    """Model for search result place"""
    place_id: str
    name: str
    keyword: str
    lat: float
    lng: float
    rating: float
    distance_km: float


class SearchResponse(BaseModel):
    """Response model for place search"""
    results: List[SearchPlace]
