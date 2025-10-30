"""Image similarity search service (Simple implementation without ML models)"""
import base64
from io import BytesIO
from PIL import Image
import numpy as np
from typing import List, Tuple
import pandas as pd
from utils import get_data_loader


class ImageSimilaritySearch:
    """
    Simple image similarity search based on color histograms.
    NOTE: This is a simplified implementation. For production, you would use:
    - CLIP embeddings
    - Vision transformers
    - Or other deep learning models
    """

    def __init__(self):
        self.data_loader = get_data_loader()

    def extract_color_histogram(self, image_bytes: bytes) -> np.ndarray:
        """
        Extract color histogram from image as a simple feature vector.

        Args:
            image_bytes: Image file bytes

        Returns:
            Feature vector (numpy array)
        """
        try:
            # Open image
            image = Image.open(BytesIO(image_bytes))

            # Convert to RGB
            image = image.convert('RGB')

            # Resize to standard size
            image = image.resize((256, 256))

            # Calculate color histogram (RGB channels)
            histogram = []
            for channel in range(3):
                channel_data = np.array(image)[:, :, channel]
                hist, _ = np.histogram(channel_data, bins=32, range=(0, 256))
                histogram.extend(hist)

            # Normalize
            histogram = np.array(histogram, dtype=np.float32)
            histogram = histogram / (histogram.sum() + 1e-10)

            return histogram

        except Exception as e:
            raise ValueError(f"Failed to process image: {e}")

    def calculate_similarity(
        self,
        query_features: np.ndarray,
        place_features: np.ndarray
    ) -> float:
        """
        Calculate similarity between two feature vectors using cosine similarity.

        Args:
            query_features: Query image features
            place_features: Place image features

        Returns:
            Similarity score (0-1)
        """
        # Cosine similarity
        dot_product = np.dot(query_features, place_features)
        norm_a = np.linalg.norm(query_features)
        norm_b = np.linalg.norm(place_features)

        if norm_a == 0 or norm_b == 0:
            return 0.0

        similarity = dot_product / (norm_a * norm_b)

        # Convert to 0-1 range
        similarity = (similarity + 1) / 2

        return float(similarity)

    def search_similar_places(
        self,
        image_bytes: bytes,
        top_k: int = 5,
        keyword_filter: str = None
    ) -> List[dict]:
        """
        Search for places with similar images.

        NOTE: This is a MOCK implementation using random scoring
        based on keyword matching and place features.

        For production, you would:
        1. Extract image features using CLIP or other vision models
        2. Compare with pre-computed embeddings of place images
        3. Return top-K most similar places

        Args:
            image_bytes: Uploaded image bytes
            top_k: Number of results to return
            keyword_filter: Optional keyword filter

        Returns:
            List of similar places with similarity scores
        """
        try:
            # Extract query features (simplified)
            query_features = self.extract_color_histogram(image_bytes)

            # Get all places
            df = self.data_loader.get_data()

            # Filter by keyword if provided
            if keyword_filter:
                df = df[df['keyword'] == keyword_filter]

            # Filter places that have photos
            df = df[
                (df['photo_1'].notna()) & (df['photo_1'] != '')
            ].copy()

            if len(df) == 0:
                return []

            # MOCK: Calculate pseudo-similarity based on place features
            # In production, you would compare actual image embeddings
            df['similarity'] = self._calculate_mock_similarity(df)

            # Sort by similarity
            df = df.nlargest(top_k, 'similarity')

            # Build results
            results = []
            for _, place in df.iterrows():
                # Get photos
                photos = []
                for col in ['photo_1', 'photo_2', 'photo_3']:
                    if pd.notna(place[col]) and str(place[col]).strip() != '':
                        photos.append(str(place[col]))

                result = {
                    "place_id": str(place['place_id']),
                    "name": str(place['name']),
                    "keyword": str(place['keyword']),
                    "lat": float(place['lat']),
                    "lng": float(place['lng']),
                    "rating": float(place['rating']),
                    "user_ratings_total": int(place['user_ratings_total']),
                    "tourism_score": float(place['tourism_score']),
                    "similarity": float(place['similarity']),
                    "photos": photos,
                    "address": str(place['address'])
                }
                results.append(result)

            return results

        except Exception as e:
            raise ValueError(f"Error in image similarity search: {e}")

    def _calculate_mock_similarity(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate mock similarity scores based on place features.

        In production, this would be replaced with actual image similarity.
        """
        # Use weighted combination of existing features as proxy
        scores = (
            df['tourism_score'] * 0.40 +
            (df['rating'] / 5.0) * 0.30 +
            (df['popularity_score'] / df['popularity_score'].max()) * 0.20 +
            np.random.rand(len(df)) * 0.10  # Add some randomness
        )

        # Normalize to 0-1 range
        scores = (scores - scores.min()) / (scores.max() - scores.min() + 1e-10)

        # Scale to 0.6-0.95 range (realistic similarity scores)
        scores = 0.6 + scores * 0.35

        return scores
