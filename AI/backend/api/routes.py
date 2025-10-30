"""API routes for Plan My Trip"""
from fastapi import APIRouter, HTTPException, Query, UploadFile, File
from typing import Optional, List
from pydantic import BaseModel
from models import (
    TripRequest,
    TripResponse,
    ThemesResponse,
    Theme,
    SearchResponse,
    SearchPlace
)
from services import TripPlanner
from services.image_similarity import ImageSimilaritySearch
from services.trip_narrator import TripNarrator
from utils import get_data_loader, haversine_distance
from config import THEMES
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/api/plan-trip", response_model=TripResponse)
async def plan_trip(request: TripRequest):
    """
    Plan a trip based on theme or place name.

    Args:
        request: Trip request with start location, mode, and preferences

    Returns:
        Trip plan with optimized route and carbon footprint
    """
    try:
        planner = TripPlanner()

        trip = planner.plan_trip(
            start_lat=request.start_lat,
            start_lng=request.start_lng,
            mode=request.mode,
            value=request.value,
            num_stops=request.num_stops,
            max_distance_km=request.max_distance_km
        )

        return trip

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error planning trip: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/api/themes", response_model=ThemesResponse)
async def get_themes():
    """
    Get list of available themes.

    Returns:
        List of themes with details
    """
    try:
        themes_list = [Theme(**theme) for theme in THEMES]
        return ThemesResponse(themes=themes_list)

    except Exception as e:
        logger.error(f"Error getting themes: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/api/places/search", response_model=SearchResponse)
async def search_places(
    query: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(10, ge=1, le=50, description="Maximum results"),
    start_lat: Optional[float] = Query(None, ge=-90, le=90, description="Reference latitude for distance"),
    start_lng: Optional[float] = Query(None, ge=-180, le=180, description="Reference longitude for distance")
):
    """
    Search places by name.

    Args:
        query: Search query string
        limit: Maximum number of results
        start_lat: Optional reference latitude for distance calculation
        start_lng: Optional reference longitude for distance calculation

    Returns:
        List of matching places
    """
    try:
        data_loader = get_data_loader()
        results_df = data_loader.search_by_name(query, limit)

        results = []
        for _, place in results_df.iterrows():
            # Calculate distance if start coordinates provided
            distance_km = 0.0
            if start_lat is not None and start_lng is not None:
                distance_km = haversine_distance(
                    start_lat, start_lng,
                    place['lat'], place['lng']
                )

            search_place = SearchPlace(
                place_id=str(place['place_id']),
                name=str(place['name']),
                keyword=str(place['keyword']),
                lat=float(place['lat']),
                lng=float(place['lng']),
                rating=float(place['rating']),
                distance_km=float(distance_km)
            )
            results.append(search_place)

        return SearchResponse(results=results)

    except Exception as e:
        logger.error(f"Error searching places: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/api/image-search")
async def image_search(
    image: UploadFile = File(...),
    top_k: int = Query(5, ge=1, le=20, description="Number of results")
):
    """
    Search for similar places using image upload.

    Args:
        image: Uploaded image file
        top_k: Number of similar places to return

    Returns:
        List of similar places with similarity scores
    """
    try:
        # Validate image file
        if not image.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="File must be an image (JPEG, PNG, WebP)"
            )

        # Read image bytes
        image_bytes = await image.read()

        # Perform similarity search
        similarity_search = ImageSimilaritySearch()
        results = similarity_search.search_similar_places(
            image_bytes=image_bytes,
            top_k=top_k
        )

        return {"results": results}

    except ValueError as e:
        logger.error(f"Validation error in image search: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in image search: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


class PlanTripFromPlacesRequest(BaseModel):
    """Request model for planning trip from specific places"""
    start_lat: float
    start_lng: float
    place_ids: List[str]


@router.post("/api/plan-trip-from-places", response_model=TripResponse)
async def plan_trip_from_places(request: PlanTripFromPlacesRequest):
    """
    Plan a trip from a list of specific place IDs.

    Args:
        request: Request with start location and place IDs

    Returns:
        Optimized trip plan
    """
    try:
        data_loader = get_data_loader()
        df = data_loader.get_data()

        # Filter places by IDs
        places_df = df[df['place_id'].isin(request.place_ids)]

        if len(places_df) == 0:
            raise ValueError("No valid places found with provided IDs")

        # Use trip planner to optimize route
        planner = TripPlanner()

        # Build route using existing route building logic
        route = planner._build_optimized_route(
            request.start_lat,
            request.start_lng,
            places_df
        )

        # Build response
        import uuid
        trip_id = f"trip_{uuid.uuid4().hex[:8]}"
        trip_response = planner._build_trip_response(
            trip_id=trip_id,
            start_lat=request.start_lat,
            start_lng=request.start_lng,
            mode="image_search",
            route=route
        )

        return trip_response

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error planning trip from places: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "Plan My Trip API"}
