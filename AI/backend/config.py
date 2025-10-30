"""Configuration settings for Plan My Trip API"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Data file path
DATA_FILE = BASE_DIR / "data" / "chiang_rai_featured.csv"

# API Settings
API_TITLE = "Plan My Trip API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "REST API for planning trips in Chiang Rai with Carbon Footprint calculation"

# Distance settings
EARTH_RADIUS_KM = 6371

# Carbon calculation constants
TRANSPORT_CARBON_PER_KM = 0.12  # kg CO2/km for car

# Theme definitions
THEMES = [
    {
        "id": "naturalist",
        "name": "Naturalist",
        "name_th": "ธรรมชาติ",
        "subtitle": "Nature Sightseeing",
        "icon": "🌲",
        "keywords": ["จุดชมวิว", "น้ำตก", "ถ้ำ", "สวนชา"],
        "carbon_level": "low",
        "description": "เที่ยวชมธรรมชาติ ลดคาร์บอน"
    },
    {
        "id": "conservative",
        "name": "Conservative",
        "name_th": "วัฒนธรรม",
        "subtitle": "Customs & Culture",
        "icon": "↗",
        "keywords": ["งานหัตถกรรม", "ของที่ระลึกท้องถิ่น", "ของฝากชุมชน"],
        "carbon_level": "low",
        "description": "เที่ยวชมวัฒนธรรมท้องถิ่น"
    },
    {
        "id": "photogenic",
        "name": "Photogenic",
        "name_th": "ถ่ายรูป",
        "subtitle": "Photo Trip",
        "icon": "📷",
        "keywords": ["จุดชมวิว", "สวนชา", "ฟาร์ม"],
        "carbon_level": "low",
        "description": "สถานที่สวยงามเหมาะถ่ายรูป"
    },
    {
        "id": "cafeist",
        "name": "Cafe'ist",
        "name_th": "คาเฟ่",
        "subtitle": "Community Cafe",
        "icon": "☕",
        "keywords": ["สวนชา", "ฟาร์ม"],
        "carbon_level": "low",
        "description": "คาเฟ่ชุมชน บรรยากาศดี"
    },
    {
        "id": "mood",
        "name": "Based on My Mood",
        "name_th": "ตามอารมณ์",
        "subtitle": "Mood-based",
        "icon": "😊",
        "keywords": [],
        "carbon_level": "medium",
        "description": "เลือกสถานที่ตามอารมณ์"
    },
    {
        "id": "weather",
        "name": "Based on Weather",
        "name_th": "ตามสภาพอากาศ",
        "subtitle": "Weather-based",
        "icon": "☀️",
        "keywords": [],
        "carbon_level": "medium",
        "description": "แนะนำตามสภาพอากาศ"
    }
]

# Scoring weights
SCORING_WEIGHTS = {
    "tourism_score": 0.30,
    "rating": 0.20,
    "carbon": 0.25,
    "popularity": 0.15,
    "distance": 0.10
}

# Eco score weights
ECO_SCORE_WEIGHTS = {
    "carbon": 4.0,
    "tourism": 3.0,
    "rating": 2.0,
    "efficiency": 1.0
}
