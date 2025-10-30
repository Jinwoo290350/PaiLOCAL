# 🌱 Plan My Trip API - Chiang Rai

REST API for planning low-carbon trips in Chiang Rai with intelligent route optimization and carbon footprint calculation.

## ✨ Features

- **Theme-Based Planning**: Plan trips based on themes (Naturalist, Conservative, Photogenic, Cafeist, etc.)
- **Place-Based Planning**: Find similar places based on a specific location
- **Route Optimization**: Greedy Nearest Neighbor algorithm for efficient routes
- **Carbon Footprint**: Calculate and display CO2 emissions for each trip
- **Eco Score**: Rate trips on environmental friendliness (0-10 scale)
- **Rule-Based Scoring**: No ML models needed - simple, fast, and transparent

## 🏗️ Architecture

```
AI/
├── backend/               # FastAPI Backend
│   ├── app.py            # Main FastAPI application
│   ├── config.py         # Configuration & theme definitions
│   ├── requirements.txt  # Python dependencies
│   │
│   ├── api/              # API endpoints
│   │   └── routes.py     # POST /api/plan-trip, GET /api/themes, etc.
│   │
│   ├── services/         # Business logic
│   │   ├── trip_planner.py       # Main trip planning logic
│   │   ├── route_optimizer.py   # Route optimization (Greedy NN)
│   │   └── carbon_calculator.py # Carbon footprint calculation
│   │
│   ├── models/           # Pydantic schemas
│   │   └── schemas.py    # Request/response models
│   │
│   ├── utils/            # Utilities
│   │   ├── data_loader.py # CSV data loader
│   │   └── geo_utils.py   # Haversine distance calculation
│   │
│   └── data/             # Data files
│       └── chiang_rai_featured.csv
│
└── frontend/             # Simple Web UI
    ├── index.html        # Main page
    ├── style.css         # Styling
    └── app.js            # JavaScript logic
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip

### Installation

1. **Navigate to backend folder**
```bash
cd AI/backend
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the API

**Start the server:**
```bash
source venv/bin/activate  # Activate venv first (On Windows: venv\Scripts\activate)
python app.py
```

The API will be available at `http://localhost:8000`

**API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Running the Frontend

1. **Open the frontend in a browser:**
```bash
cd AI/frontend
open index.html  # macOS
# or
start index.html  # Windows
# or just double-click index.html
```

2. The frontend will connect to `http://localhost:8000`

## 📡 API Endpoints

### 1. Plan Trip
**POST** `/api/plan-trip`

Plan a trip based on theme or place name.

**Request Body:**
```json
{
  "start_lat": 19.9105,
  "start_lng": 99.8406,
  "mode": "theme",
  "value": "naturalist",
  "num_stops": 5,
  "max_distance_km": 50
}
```

**Modes:**
- `"theme"`: Plan by theme (value = theme ID)
- `"place_name"`: Plan by place similarity (value = place name)

**Response:**
```json
{
  "trip_id": "trip_abc123",
  "start_location": { "lat": 19.9105, "lng": 99.8406 },
  "mode": "theme",
  "theme": "naturalist",
  "summary": {
    "total_stops": 5,
    "total_distance_km": 45.3,
    "estimated_time_hours": 1.13,
    "total_carbon_kg": 5.44,
    "eco_score": 8.5,
    "carbon_reduction_percent": 63.7
  },
  "route": [
    {
      "stop_number": 1,
      "place_id": "ChIJxxx",
      "name": "ภูชี้ฟ้า",
      "keyword": "จุดชมวิว",
      "lat": 19.95,
      "lng": 99.88,
      "distance_from_prev_km": 8.5,
      "rating": 4.8,
      "carbon_kg": 1.02,
      "photos": ["photo_url_1", "photo_url_2"],
      ...
    }
  ]
}
```

### 2. Get Themes
**GET** `/api/themes`

Get list of available themes.

**Response:**
```json
{
  "themes": [
    {
      "id": "naturalist",
      "name": "Naturalist",
      "name_th": "ธรรมชาติ",
      "icon": "🌲",
      "keywords": ["จุดชมวิว", "น้ำตก", "ถ้ำ", "สวนชา"],
      "description": "เที่ยวชมธรรมชาติ ลดคาร์บอน"
    }
  ]
}
```

### 3. Search Places
**GET** `/api/places/search?query={text}&limit=10`

Search places by name.

**Query Parameters:**
- `query` (required): Search text
- `limit` (optional): Max results (default: 10)
- `start_lat` (optional): Reference latitude for distance
- `start_lng` (optional): Reference longitude for distance

**Response:**
```json
{
  "results": [
    {
      "place_id": "ChIJxxx",
      "name": "วัดพระแก้ว",
      "keyword": "จุดชมวิว",
      "lat": 19.91,
      "lng": 99.84,
      "rating": 4.7,
      "distance_km": 2.3
    }
  ]
}
```

## 🧠 How It Works

### 1. Theme-Based Planning

1. Filter places by theme keywords (e.g., "naturalist" → จุดชมวิว, น้ำตก, ถ้ำ)
2. Calculate weighted score for each place:
   ```
   score = tourism_score × 0.30 +
           rating × 0.20 +
           carbon_score × 0.25 +
           popularity × 0.15 +
           distance × 0.10
   ```
3. Select top N places by score
4. Optimize route using Greedy Nearest Neighbor
5. Calculate carbon footprint

### 2. Place-Name-Based Planning

1. Find target place by name
2. Calculate similarity to other places:
   ```
   similarity = keyword_match × 0.40 +
                tourism_similarity × 0.30 +
                rating_similarity × 0.30
   ```
3. Select top N similar places
4. Optimize route
5. Calculate carbon footprint

### 3. Route Optimization

**Greedy Nearest Neighbor Algorithm:**
1. Start at starting location
2. Find nearest unvisited place
3. Move to that place
4. Repeat until all places visited

### 4. Carbon Calculation

```
place_carbon = transport_carbon + activity_carbon + visitor_carbon

transport_carbon = distance_km × 0.12 kg CO2/km
activity_carbon = activity_carbon_score × 0.5 (from CSV)
visitor_carbon = visitor_carbon_factor (from CSV)
```

### 5. Eco Score

```
eco_score = (1 - carbon_normalized) × 4 +
            avg_tourism_score × 3 +
            avg_rating/5 × 2 +
            route_efficiency × 1

Scale: 0-10 (higher = more eco-friendly)
```

## 🧪 Testing

Run the test suite:
```bash
cd AI/backend
python test_api.py
```

**Example Tests:**
- Health check
- Get themes
- Search places
- Plan trip by theme
- Plan trip by place name

## 📊 Available Themes

| Theme | Icon | Keywords | Description |
|-------|------|----------|-------------|
| Naturalist | 🌲 | จุดชมวิว, น้ำตก, ถ้ำ, สวนชา | Nature sightseeing |
| Conservative | ↗ | งานหัตถกรรม, ของที่ระลึกท้องถิ่น | Culture & customs |
| Photogenic | 📷 | จุดชมวิว, สวนชา, ฟาร์ม | Photo-worthy spots |
| Cafeist | ☕ | สวนชา, ฟาร์ม | Community cafes |
| Mood | 😊 | - | Mood-based (flexible) |
| Weather | ☀️ | - | Weather-based (flexible) |

## 🛠️ Tech Stack

**Backend:**
- FastAPI 0.104.1
- Pandas 2.1.3 (in-memory data)
- NumPy 1.26.2 (calculations)
- Pydantic 2.5.0 (validation)
- Uvicorn 0.24.0 (ASGI server)

**Frontend:**
- HTML5 + CSS3
- Vanilla JavaScript
- Leaflet.js (maps)

**Key Design Decisions:**
- ✅ In-memory data (no database) for speed
- ✅ Rule-based scoring (no ML models)
- ✅ Simple greedy algorithm (not complex TSP)
- ✅ Pre-calculated carbon features (fast lookup)

## 📝 Example Usage

### Theme-Based Trip
```bash
curl -X POST http://localhost:8000/api/plan-trip \
  -H "Content-Type: application/json" \
  -d '{
    "start_lat": 19.9105,
    "start_lng": 99.8406,
    "mode": "theme",
    "value": "naturalist",
    "num_stops": 5,
    "max_distance_km": 50
  }'
```

### Place-Name-Based Trip
```bash
curl -X POST http://localhost:8000/api/plan-trip \
  -H "Content-Type: application/json" \
  -d '{
    "start_lat": 19.9105,
    "start_lng": 99.8406,
    "mode": "place_name",
    "value": "ภูชี้ฟ้า",
    "num_stops": 4,
    "max_distance_km": 30
  }'
```

## 🎯 Key Features Checklist

- ✅ POST /api/plan-trip (theme & place_name modes)
- ✅ GET /api/themes
- ✅ GET /api/places/search
- ✅ Rule-based recommendation (weighted scoring)
- ✅ Route optimization (Greedy NN)
- ✅ Carbon calculation (pre-calculated features)
- ✅ Eco score (0-10 scale)
- ✅ Photo handling (1-3 photos per place)
- ✅ Distance calculation (Haversine)
- ✅ CORS enabled
- ✅ Input validation
- ✅ Error handling
- ✅ Simple web demo with map
- ✅ Test suite

## 🌍 Data

**Dataset:** `chiang_rai_featured.csv`
- 1,230 places in Chiang Rai
- 12 keyword categories
- Pre-calculated features:
  - Tourism score
  - Carbon scores
  - Popularity metrics
  - Reviews & ratings

## 🔧 Configuration

Edit `backend/config.py` to customize:
- Scoring weights
- Carbon calculation constants
- Theme definitions
- API settings

## 📖 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🐛 Troubleshooting

**Server won't start:**
- Check if port 8000 is available
- Install all dependencies: `pip install -r requirements.txt`

**CSV file not found:**
- Ensure `chiang_rai_featured.csv` is in `backend/data/`
- Check file path in `config.py`

**Frontend can't connect:**
- Make sure backend is running on http://localhost:8000
- Check CORS settings in `app.py`

## 📄 License

This project is for educational purposes.

## 👥 Contributing

This is a demo project for the PaiLOCAL platform.

---

Made with 💚 for sustainable tourism in Chiang Rai
