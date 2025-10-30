"""Main FastAPI application for Plan My Trip API"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path
import logging
import sys

from config import API_TITLE, API_VERSION, API_DESCRIPTION, DATA_FILE
from utils import init_data_loader
from utils.photo_utils import init_photos
from api import router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    logger.info("Starting Plan My Trip API...")

    try:
        # Load data into memory
        logger.info(f"Loading data from {DATA_FILE}")
        data_loader = init_data_loader(DATA_FILE)
        df = data_loader.get_data()
        logger.info(f"Successfully loaded {len(df)} places into memory")

        # Initialize photo system
        init_photos()

    except Exception as e:
        logger.error(f"Failed to load data: {e}")
        raise

    logger.info("Plan My Trip API started successfully!")

    yield

    # Shutdown
    logger.info("Shutting down Plan My Trip API...")


# Create FastAPI app
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": API_TITLE,
        "version": API_VERSION,
        "description": API_DESCRIPTION,
        "endpoints": {
            "plan_trip": "POST /api/plan-trip",
            "get_themes": "GET /api/themes",
            "search_places": "GET /api/places/search",
            "health": "GET /health",
            "docs": "GET /docs"
        }
    }


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting uvicorn server...")
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
