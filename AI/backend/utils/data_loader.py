"""Data loader utility for loading CSV data into memory"""
import pandas as pd
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class DataLoader:
    """Load and manage CSV data in memory"""

    def __init__(self, csv_path: Path):
        self.csv_path = csv_path
        self.df: Optional[pd.DataFrame] = None

    def load(self) -> pd.DataFrame:
        """Load CSV file into pandas DataFrame"""
        try:
            logger.info(f"Loading data from {self.csv_path}")
            self.df = pd.read_csv(self.csv_path)

            # Clean and prepare data
            self._clean_data()

            logger.info(f"Loaded {len(self.df)} places from CSV")
            return self.df

        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            raise

    def _clean_data(self):
        """Clean and prepare the DataFrame"""
        if self.df is None:
            return

        # Fill missing values
        self.df['keyword'] = self.df['keyword'].fillna('')
        self.df['phone'] = self.df['phone'].fillna('')
        self.df['website'] = self.df['website'].fillna('')
        self.df['review_summary'] = self.df['review_summary'].fillna('')
        self.df['photo_1'] = self.df['photo_1'].fillna('')
        self.df['photo_2'] = self.df['photo_2'].fillna('')
        self.df['photo_3'] = self.df['photo_3'].fillna('')

        # Ensure numeric columns
        numeric_cols = [
            'lat', 'lng', 'rating', 'user_ratings_total',
            'tourism_score', 'popularity_score',
            'estimated_transport_carbon_kg', 'activity_carbon_score',
            'visitor_carbon_factor'
        ]

        for col in numeric_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)

        # Create boolean flags
        self.df['has_phone'] = self.df['phone'].astype(str).str.strip() != ''
        self.df['has_website'] = self.df['website'].astype(str).str.strip() != ''

        logger.info("Data cleaned and prepared")

    def get_data(self) -> pd.DataFrame:
        """Get the loaded DataFrame"""
        if self.df is None:
            raise ValueError("Data not loaded. Call load() first.")
        return self.df

    def search_by_name(self, query: str, limit: int = 10) -> pd.DataFrame:
        """Search places by name"""
        if self.df is None:
            raise ValueError("Data not loaded")

        query_lower = query.lower().strip()
        mask = self.df['name'].str.lower().str.contains(query_lower, na=False)
        return self.df[mask].head(limit)

    def filter_by_keywords(self, keywords: list) -> pd.DataFrame:
        """Filter places by keywords"""
        if self.df is None:
            raise ValueError("Data not loaded")

        if not keywords:
            return self.df

        mask = self.df['keyword'].isin(keywords)
        return self.df[mask]

    def get_place_by_id(self, place_id: str) -> Optional[pd.Series]:
        """Get a single place by place_id"""
        if self.df is None:
            raise ValueError("Data not loaded")

        result = self.df[self.df['place_id'] == place_id]
        if len(result) > 0:
            return result.iloc[0]
        return None


# Global data loader instance
_data_loader: Optional[DataLoader] = None


def init_data_loader(csv_path: Path) -> DataLoader:
    """Initialize the global data loader"""
    global _data_loader
    _data_loader = DataLoader(csv_path)
    _data_loader.load()
    return _data_loader


def get_data_loader() -> DataLoader:
    """Get the global data loader instance"""
    if _data_loader is None:
        raise ValueError("DataLoader not initialized. Call init_data_loader() first.")
    return _data_loader
