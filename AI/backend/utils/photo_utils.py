"""Utility functions for handling photo URLs from local storage"""
import pandas as pd
from pathlib import Path
from typing import List, Optional
import logging
import urllib.parse

logger = logging.getLogger(__name__)

# Local photos directory (relative to project root)
PHOTOS_DIR = Path(__file__).parent.parent.parent / "data" / "photos"


def check_photo_exists(filename: str) -> bool:
    """
    Check if photo file exists in local directory.

    Args:
        filename: Photo filename (e.g., "เวียงชัย_PK_FARM_Wiang_Chi_0.jpg")

    Returns:
        True if file exists, False otherwise
    """
    if not filename or pd.isna(filename):
        return False

    photo_path = PHOTOS_DIR / str(filename).strip()
    return photo_path.exists()


def get_photo_url_from_filename(filename: str) -> Optional[str]:
    """
    Convert filename to photo URL (local file path).

    Args:
        filename: Photo filename from CSV

    Returns:
        URL path to photo, or None if not found
    """
    if not filename or pd.isna(filename) or str(filename).strip() == '':
        return None

    filename = str(filename).strip()

    # Check if already a full URL
    if filename.startswith('http://') or filename.startswith('https://'):
        return filename

    # Check if file exists locally
    if check_photo_exists(filename):
        # URL encode filename for proper handling
        encoded_filename = urllib.parse.quote(filename)
        # Return relative URL path (will be served by FastAPI static files)
        return f"/static/photos/{encoded_filename}"

    # File not found
    return None


def get_place_photos(place_row: pd.Series, use_placeholders: bool = True, max_photos: int = 3) -> List[str]:
    """
    Extract photo URLs from place data.

    Args:
        place_row: DataFrame row with photo_1, photo_2, photo_3 columns
        use_placeholders: Whether to use placeholders when photos not available
        max_photos: Maximum number of photos to return (default 3)

    Returns:
        List of photo URLs
    """
    photos = []

    for i, col in enumerate(['photo_1', 'photo_2', 'photo_3']):
        if i >= max_photos:
            break

        if col not in place_row.index:
            continue

        filename = place_row[col]

        # Skip if no filename
        if not filename or pd.isna(filename):
            continue

        # Try to get photo URL
        photo_url = get_photo_url_from_filename(filename)

        if photo_url:
            photos.append(photo_url)
        elif use_placeholders:
            # Use placeholder with keyword
            keyword = place_row.get('keyword', 'Place')
            keyword_encoded = urllib.parse.quote(str(keyword))

            # Use different colors for different photo numbers
            colors = {
                0: '667eea',  # Purple-blue
                1: '764ba2',  # Purple
                2: '5b86e5',  # Blue
            }
            bg_color = colors.get(i, '667eea')

            placeholder_url = f"https://via.placeholder.com/400x300/{bg_color}/ffffff?text={keyword_encoded}"
            photos.append(placeholder_url)

    # If no photos at all, add one placeholder
    if len(photos) == 0 and use_placeholders:
        keyword = place_row.get('keyword', 'Place')
        text_encoded = urllib.parse.quote(str(keyword))
        placeholder_url = f"https://via.placeholder.com/400x300/667eea/ffffff?text={text_encoded}"
        photos.append(placeholder_url)

    return photos


def get_photos_stats() -> dict:
    """Get statistics about available photos"""
    if not PHOTOS_DIR.exists():
        return {
            "photos_dir": str(PHOTOS_DIR),
            "exists": False,
            "total_files": 0,
            "status": "directory_not_found"
        }

    # Count image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
    photo_files = [
        f for f in PHOTOS_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in image_extensions
    ]

    return {
        "photos_dir": str(PHOTOS_DIR),
        "exists": True,
        "total_files": len(photo_files),
        "status": "ready"
    }


# Initialize and log photo directory status
def init_photos():
    """Initialize photo system and log status"""
    stats = get_photos_stats()

    if stats['exists']:
        logger.info(f"✅ Photos directory found: {stats['photos_dir']}")
        logger.info(f"   Total photos: {stats['total_files']}")
    else:
        logger.warning(f"⚠️  Photos directory not found: {stats['photos_dir']}")
        logger.warning("   Using placeholder images")

    return stats
