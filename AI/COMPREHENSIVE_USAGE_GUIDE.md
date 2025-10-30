# 📘 Plan My Trip - Comprehensive Usage Guide

## สารบัญ (Table of Contents)

1. [ภาพรวมระบบ (System Overview)](#ภาพรวมระบบ-system-overview)
2. [สถาปัตยกรรม (Architecture)](#สถาปัตยกรรม-architecture)
3. [วิธีการใช้งาน (How to Use)](#วิธีการใช้งาน-how-to-use)
4. [รายละเอียดส่วนประกอบ (Components Details)](#รายละเอียดสวนประกอบ-components-details)
5. [ข้อดีข้อเสีย (Pros and Cons)](#ขอดขอเสย-pros-and-cons)
6. [การ Deploy (Deployment)](#การ-deploy-deployment)
7. [Troubleshooting](#troubleshooting)

---

## ภาพรวมระบบ (System Overview)

### ระบบนี้คืออะไร?

**Plan My Trip** เป็น AI-powered Trip Planning System สำหรับจังหวัดเชียงราย ที่ช่วย:
- **วางแผนเส้นทางท่องเที่ยว** โดยอัตโนมัติจาก Theme หรือชื่อสถานที่
- **ค้นหาสถานที่ด้วยรูปภาพ** (Image Search) เพื่อหาสถานที่คล้ายกัน
- **คำนวณ Carbon Footprint** และให้ Eco Score
- **เพิ่มประสิทธิภาพเส้นทาง** ด้วยอัลกอริทึม 2-opt

### เทคโนโลยีหลัก

**Backend:**
- FastAPI (Python 3.13)
- Pandas (Data manipulation)
- Rule-based scoring (ไม่ใช้ ML models)
- In-memory data storage

**Frontend:**
- Vanilla JavaScript + HTML5 + CSS3
- Leaflet.js (Interactive maps)
- Responsive design

**Data Source:**
- CSV file: `chiang_rai_featured.csv` (1,055 places)
- 12 keyword categories (ฟาร์ม, โฮมสเตย์, จุดชมวิว, etc.)
- Photos stored in Google Drive

---

## สถาปัตยกรรม (Architecture)

### Directory Structure

```
AI/
├── backend/
│   ├── app.py                    # Main FastAPI app
│   ├── config.py                 # Configuration & themes
│   ├── requirements.txt          # Python dependencies
│   ├── start.sh / start.bat      # Startup scripts
│   ├── api/
│   │   ├── routes.py            # API endpoints
│   │   └── schemas.py           # Pydantic models
│   ├── services/
│   │   ├── trip_planner.py      # Core trip planning logic
│   │   ├── route_optimizer.py   # Route optimization (2-opt)
│   │   ├── carbon_calculator.py # Carbon & eco score
│   │   ├── data_loader.py       # CSV data loader
│   │   └── image_similarity.py  # Image search
│   └── utils/
│       ├── geo_utils.py         # Haversine distance
│       └── photo_utils.py       # Google Drive photo handling
├── frontend/
│   ├── index.html               # Theme search page
│   ├── image-search.html        # Image search page
│   ├── app.js                   # Theme search JS
│   ├── image-search.js          # Image search JS
│   └── style.css                # Shared styles
├── data/
│   └── chiang_rai_featured.csv  # Places data (1,055 rows)
└── docs/
    ├── README.md
    ├── QUICKSTART.md
    ├── IMAGE_SEARCH_README.md
    └── COMPREHENSIVE_USAGE_GUIDE.md (this file)
```

### Data Flow

```
User Input → Frontend → FastAPI Backend → Services → Data Processing → Response
                                              ↓
                                         DataFrame
                                      (In-Memory CSV)
```

---

## วิธีการใช้งาน (How to Use)

### 1. Setup & Installation

#### Step 1: Clone & Navigate
```bash
cd /path/to/PaiLOCAL/AI/backend
```

#### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# หรือ
venv\Scripts\activate     # Windows
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**ข้อควรระวัง:** ต้องใช้ Python 3.13+ และ pandas>=2.2.0

#### Step 4: Start Server
```bash
# ใช้ startup script (แนะนำ)
./start.sh              # macOS/Linux
start.bat               # Windows

# หรือ manual
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

เปิด browser ไปที่:
- API Docs: http://localhost:8000/docs
- Theme Search: `file:///path/to/AI/frontend/index.html`
- Image Search: `file:///path/to/AI/frontend/image-search.html`

---

### 2. ใช้งาน Theme Search (index.html)

#### ขั้นตอน:

1. **เลือก Mode:**
   - **Theme-based**: เลือก 1 ใน 6 themes (Naturalist, Conservative, Photogenic, Cafeist, Mood, Weather)
   - **Place Name-based**: พิมพ์ชื่อสถานที่ (เช่น "สิงห์ปาร์ค", "ดอยแม่สลอง")

2. **กำหนดจุดเริ่มต้น:**
   - Latitude: เช่น 19.9105 (เชียงรายเมือง)
   - Longitude: เช่น 99.8406

3. **ตั้งค่าพารามิเตอร์:**
   - Number of Stops: จำนวนสถานที่ (1-20)
   - Max Distance: ระยะทางสูงสุด (km)

4. **คลิก "Plan My Trip"**

5. **ผลลัพธ์:**
   - แผนที่แสดงเส้นทาง (Leaflet.js)
   - รายละเอียดแต่ละสถานที่:
     - ชื่อ, Keyword, Rating
     - ระยะทางจากจุดก่อนหน้า
     - ระยะทางสะสมจากจุดเริ่มต้น
     - Carbon footprint
     - รูปภาพ 1-3 รูป
   - สรุปทริป: Total distance, Carbon, Eco Score

---

### 3. ใช้งาน Image Search (image-search.html)

#### ขั้นตอน:

1. **Upload รูปภาพ:**
   - Drag & Drop รูปลงใน Upload Zone
   - หรือคลิกเพื่อเลือกไฟล์
   - รองรับ: JPG, PNG, WebP

2. **ดู Preview** และคลิก **"🔍 Find Similar Places"**

3. **ผลลัพธ์ที่ได้:**
   - Top 5 สถานที่ที่คล้ายกัน
   - แต่ละสถานที่แสดง:
     - รูปภาพ thumbnail
     - ชื่อ, Keyword
     - Rating & Reviews
     - **Similarity Score** (% ความคล้าย)

4. **เลือกสถานที่:**
   - คลิกที่สถานที่เพื่อเลือก/ยกเลิก
   - สถานที่ที่เลือกจะมี highlight สีฟ้า
   - **Selected Places Summary** จะแสดงรายการที่เลือก (1-5)

5. **วางแผนทริป:**
   - กำหนดจุดเริ่มต้น (Lat/Lng)
   - คลิก **"Plan Trip with Selected Places"**
   - ระบบจะวางแผนเส้นทางที่เหมาะสมที่สุด

---

## รายละเอียดส่วนประกอบ (Components Details)

### Backend Services

#### 1. TripPlanner (services/trip_planner.py)

**หน้าที่:** วางแผนทริปจาก Theme หรือ Place Name

**เอาไปทำไง:**
```python
from services.trip_planner import TripPlanner

planner = TripPlanner(dataframe)
result = planner.plan_trip(
    start_lat=19.9105,
    start_lng=99.8406,
    mode="theme",          # หรือ "place_name"
    value="naturalist",    # theme name หรือ place name
    num_stops=5,
    max_distance_km=100
)
```

**ทำงานอย่างไร:**
1. **Filter places** ตาม mode (theme keywords หรือ name similarity)
2. **Score places** ด้วย rule-based formula:
   ```
   score = (tourism_score × 0.30) +
           (rating × 0.20) +
           (carbon_score × 0.25) +
           (popularity × 0.15) +
           (distance_score × 0.10)
   ```
3. **Select top-N places** ตามคะแนน
4. **Optimize route** ด้วย RouteOptimizer
5. **Calculate carbon & eco score**

**ข้อดี:**
- Fast (ไม่ต้อง train model)
- Transparent (เห็นการคำนวณชัดเจน)
- Customizable (แก้ weight ได้ง่าย)

**ข้อเสีย:**
- ไม่ได้ "เรียนรู้" จากพฤติกรรมผู้ใช้
- Scoring formula ต้องปรับ manual
- ไม่สามารถ capture complex patterns

---

#### 2. RouteOptimizer (services/route_optimizer.py)

**หน้าที่:** เพิ่มประสิทธิภาพเส้นทางให้ระยะทางสั้นที่สุด

**เอาไปทำไง:**
```python
from services.route_optimizer import RouteOptimizer

route = RouteOptimizer.optimize_route(
    start_lat=19.9105,
    start_lng=99.8406,
    places_df=selected_places
)
# Returns: [(index, dist_from_prev, dist_from_start), ...]
```

**อัลกอริทึม:**
1. **Greedy Nearest Neighbor:**
   - เริ่มจากจุดเริ่มต้น
   - เลือกสถานที่ใกล้ที่สุดที่ยังไม่ได้เยี่ยมชม
   - ทำซ้ำจนเยี่ยมชมทั้งหมด

2. **2-opt Improvement:**
   - ลอง reverse segments ของเส้นทาง
   - ถ้าระยะทางลดลง → ใช้เส้นทางใหม่
   - ทำซ้ำจนไม่สามารถปรับปรุงได้

**ตัวอย่าง:**
```
Initial: A → B → D → C → E (distance: 120 km)
                ↓
         A → B → C → D → E (distance: 95 km)  ✅ Better!
```

**ข้อดี:**
- ลด zig-zag patterns อย่างมาก
- Fast (O(n²) per iteration)
- ใช้ได้ดีกับ 5-20 สถานที่

**ข้อเสีย:**
- ไม่ใช่ optimal solution (TSP is NP-hard)
- สำหรับ >50 สถานที่ อาจช้า
- ไม่ consider เวลาเปิด-ปิด, traffic

**ทางเลือกอื่น:**
- Genetic Algorithm (ดีกว่า แต่ช้ากว่า)
- Simulated Annealing
- Christofides Algorithm
- Google OR-Tools

---

#### 3. CarbonCalculator (services/carbon_calculator.py)

**หน้าที่:** คำนวณ Carbon Footprint และ Eco Score

**เอาไปทำไง:**
```python
from services.carbon_calculator import CarbonCalculator

carbon = CarbonCalculator.calculate_place_carbon(place_row, distance_km)
# Returns: float (kg CO2)

eco_score = CarbonCalculator.calculate_eco_score(
    total_carbon=45.5,
    avg_tourism_score=8.2,
    avg_rating=4.5,
    route_efficiency=0.85
)
# Returns: float (0-10)
```

**สูตรคำนวณ Carbon:**
```python
transport_carbon = distance_km × 0.12  # kg CO2/km (car)
activity_carbon = activity_carbon_score × 0.5
visitor_carbon = visitor_carbon_factor
total = transport_carbon + activity_carbon + visitor_carbon
```

**สูตรคำนวณ Eco Score (0-10):**
```python
carbon_score = max(0, 10 - (total_carbon / 10))
tourism_score_normalized = avg_tourism_score
rating_score = avg_rating × 2
efficiency_score = route_efficiency × 10

eco_score = (carbon_score × 0.35 +
             tourism_score_normalized × 0.25 +
             rating_score × 0.25 +
             efficiency_score × 0.15)
```

**ข้อดี:**
- Simple และเข้าใจง่าย
- ส่งเสริม eco-friendly tourism
- Adjustable weights

**ข้อเสีย:**
- Carbon factors เป็น estimated values
- ไม่ consider ประเภทยานพาหนะ
- Activity carbon เป็น rough estimate

**การปรับปรุง:**
- ให้ user เลือกประเภทรถ (car, EV, bike)
- ดึงข้อมูล real-time carbon data
- เพิ่ม offset options

---

#### 4. ImageSimilaritySearch (services/image_similarity.py)

**หน้าที่:** ค้นหาสถานที่ที่คล้ายกับรูปที่ upload

**เอาไปทำไง:**
```python
from services.image_similarity import ImageSimilaritySearch

search = ImageSimilaritySearch()
results = search.search_similar_places(
    image_bytes=uploaded_image,
    top_k=5
)
# Returns: DataFrame with similarity scores
```

**Current Implementation (Simple):**
- Extract color histogram จากรูป
- Score places based on:
  - Tourism score
  - Rating
  - Popularity
  - Random factor (for demo)
- Return top-K results

**ข้อดี:**
- ไม่ต้องใช้ ML model
- Fast
- No GPU required

**ข้อเสีย:**
- **ความแม่นยำต่ำมาก**
- ไม่ได้ดูเนื้อหาในรูปจริงๆ
- เป็น mock implementation

---

**Production Implementation (Recommended):**

```python
# Install: pip install transformers torch

from transformers import CLIPProcessor, CLIPModel
import torch

# Load model
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Extract image embedding
image = Image.open(image_path)
inputs = processor(images=image, return_tensors="pt")
image_features = model.get_image_features(**inputs)

# Compare with pre-computed place embeddings
similarities = torch.cosine_similarity(image_features, place_embeddings)
top_k_indices = similarities.topk(k=5)
```

**CLIP Approach ข้อดี:**
- ความแม่นยำสูงมาก (state-of-the-art)
- เข้าใจเนื้อหาในรูป (mountains, temples, farms)
- Pre-trained บนข้อมูล billions of images

**CLIP Approach ข้อเสีย:**
- ต้องใช้ ML infrastructure
- ต้องมี GPU (หรือช้ามาก)
- ต้อง pre-compute embeddings สำหรับทุกรูปใน database
- Model size ~600MB

---

#### 5. PhotoUtils (utils/photo_utils.py)

**หน้าที่:** จัดการ photo URLs จาก Google Drive

**เอาไปทำไง:**
```python
from utils.photo_utils import get_place_photos

photos = get_place_photos(place_row, use_placeholders=True)
# Returns: ["url1", "url2", "url3"] หรือ placeholders
```

**Current Implementation:**
- Check ถ้า photo column มีค่า
- Check ถ้าเป็น full URL → ใช้ได้เลย
- ถ้าเป็น filename → Return placeholder พร้อม keyword
- Placeholder format: `https://via.placeholder.com/400x300/667eea/ffffff?text={keyword}`

**ข้อดี:**
- ไม่มีรูปแตก (broken images)
- Professional appearance
- Shows keyword (user รู้ว่าเป็นประเภทอะไร)

**ข้อเสีย:**
- ไม่ใช่รูปจริง
- User experience ไม่ดีเท่ารูปจริง

---

**Production Implementation:**

**Step 1: Setup Google Drive API**
```bash
pip install google-api-python-client google-auth
```

**Step 2: Get Service Account Credentials**
1. ไปที่ Google Cloud Console
2. Create Service Account
3. Download JSON key file
4. Share Google Drive folder กับ service account email

**Step 3: Create Photo Mapping**
```python
from googleapiclient.discovery import build
from google.oauth2 import service_account
import json

# Authenticate
credentials = service_account.Credentials.from_service_account_file(
    'service-account-key.json',
    scopes=['https://www.googleapis.com/auth/drive.readonly']
)

service = build('drive', 'v3', credentials=credentials)

# List files in folder
folder_id = "1RWlpDybqGllqeIIKuNOTNkwvcgpcnf7X"
results = service.files().list(
    q=f"'{folder_id}' in parents",
    fields="files(id, name)"
).execute()

# Create mapping
file_mapping = {
    file['name']: file['id']
    for file in results.get('files', [])
}

# Save to JSON
with open('photo_mapping.json', 'w') as f:
    json.dump(file_mapping, f)
```

**Step 4: Update photo_utils.py**
```python
import json

# Load mapping
with open('photo_mapping.json') as f:
    PHOTO_MAPPING = json.load(f)

def get_photo_url_from_filename(filename):
    if filename in PHOTO_MAPPING:
        file_id = PHOTO_MAPPING[filename]
        return f"https://drive.google.com/uc?export=view&id={file_id}"
    return None
```

**Google Drive API ข้อดี:**
- ใช้รูปจริงจาก Drive
- Centralized storage
- Easy to update photos

**Google Drive API ข้อเสีย:**
- ต้อง setup credentials
- Requires API calls (quota limits)
- Slower กว่า CDN

**ทางเลือกอื่น:**
- **Cloudinary**: Image optimization + CDN
- **AWS S3 + CloudFront**: Scalable, fast
- **Firebase Storage**: Easy integration
- **Imgur API**: Free tier available

---

### Frontend Components

#### 1. Theme Search (index.html + app.js)

**หน้าที่:** UI สำหรับ theme-based และ place-name-based trip planning

**Features:**
- Mode selection (theme/place name)
- Input validation
- Interactive map (Leaflet.js)
- Photo display (1-3 photos per place)
- Route visualization
- Trip summary

**Key Functions:**

```javascript
// Plan trip
async function planTrip() {
    const response = await fetch('http://localhost:8000/api/plan-trip', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(tripData)
    });
    const result = await response.json();
    displayResults(result);
}

// Display map
function displayMap(places) {
    const map = L.map('map').setView([startLat, startLng], 10);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

    // Add markers & route
    places.forEach((place, idx) => {
        L.marker([place.lat, place.lng])
            .bindPopup(`${idx + 1}. ${place.name}`)
            .addTo(map);
    });
}
```

---

#### 2. Image Search (image-search.html + image-search.js)

**หน้าที่:** Upload image และค้นหาสถานที่คล้ายกัน

**Features:**
- Drag & Drop file upload
- Image preview
- Similar places display
- **Selected places summary** (แสดง 1-5 ที่เลือก)
- Multi-selection
- Trip planning from selected places

**Key Functions:**

```javascript
// Upload & search
async function searchSimilarPlaces() {
    const formData = new FormData();
    formData.append('image', selectedFile);
    formData.append('top_k', 5);

    const response = await fetch('http://localhost:8000/api/image-search', {
        method: 'POST',
        body: formData
    });
    const result = await response.json();
    displaySimilarPlaces(result.results);
}

// Update selected summary
function updateSelectedSummary() {
    const summaryDiv = document.getElementById('selected-summary');
    if (selectedPlaces.size === 0) {
        summaryDiv.style.display = 'none';
        return;
    }

    summaryDiv.style.display = 'block';
    const selectedArray = Array.from(selectedPlaces).sort((a, b) => a - b);
    const listHTML = selectedArray.map((index, order) => {
        const place = similarPlacesData[index];
        return `<div>${order + 1}. ${place.name} (${place.keyword})</div>`;
    }).join('');

    document.getElementById('selected-list').innerHTML = listHTML;
}
```

---

## ข้อดีข้อเสีย (Pros and Cons)

### Rule-Based vs ML Approach

| Aspect | Rule-Based (Current) | ML-Based |
|--------|---------------------|----------|
| **Development Time** | 🟢 Fast (1-2 days) | 🔴 Slow (weeks-months) |
| **Accuracy** | 🟡 Good (70-80%) | 🟢 Better (85-95%) |
| **Explainability** | 🟢 Transparent | 🔴 Black box |
| **Maintenance** | 🟢 Easy | 🟡 Requires retraining |
| **Infrastructure** | 🟢 Simple (CPU only) | 🔴 Complex (GPU, training pipeline) |
| **Customization** | 🟢 Easy (edit weights) | 🔴 Hard (retrain model) |
| **Scalability** | 🟢 Linear | 🟡 Requires optimization |
| **Data Requirements** | 🟢 Works with 1K rows | 🔴 Needs 10K+ labeled data |

**สรุป:** Rule-based approach เหมาะสำหรับ MVP และ dataset ขนาดเล็ก-กลาง

---

### In-Memory vs Database

| Aspect | In-Memory (Current) | Database |
|--------|---------------------|----------|
| **Speed** | 🟢 Very Fast (< 10ms) | 🟡 Fast (10-50ms) |
| **Scalability** | 🔴 Limited (< 10K rows) | 🟢 Unlimited |
| **Data Updates** | 🔴 Requires restart | 🟢 Real-time |
| **Complexity** | 🟢 Simple | 🟡 Moderate |
| **Concurrency** | 🟡 Read-only safe | 🟢 ACID transactions |
| **Memory Usage** | 🔴 High (all data in RAM) | 🟢 Efficient |
| **Deployment** | 🟢 Single file | 🟡 Separate service |

**สรุป:** In-memory เหมาะสำหรับ read-heavy, static data. ถ้า data มีการเปลี่ยนแปลงบ่อย → ใช้ Database

---

### 2-opt vs Other TSP Algorithms

| Algorithm | Time Complexity | Quality | Use Case |
|-----------|----------------|---------|----------|
| **Greedy NN** | O(n²) | 🟡 Fair | Quick & dirty |
| **2-opt** (Current) | O(n²) per iteration | 🟢 Good | 5-50 places |
| **3-opt** | O(n³) per iteration | 🟢 Better | 10-30 places |
| **Genetic Algorithm** | O(n² × generations) | 🟢 Very Good | 20-100 places |
| **Christofides** | O(n³) | 🟢 Guaranteed 1.5× optimal | Academic/research |
| **Exact (Branch & Bound)** | O(n!) | 🟢 Optimal | < 20 places only |
| **Google OR-Tools** | Depends | 🟢 Excellent | Production |

**สรุป:** 2-opt เป็น sweet spot ระหว่างความเร็วและคุณภาพ

---

### Placeholder vs Real Photos

| Aspect | Placeholder (Current) | Google Drive API | CDN (S3/Cloudinary) |
|--------|---------------------|------------------|---------------------|
| **Setup Time** | 🟢 0 minutes | 🟡 1-2 hours | 🟡 30 minutes |
| **Cost** | 🟢 Free | 🟢 Free (quota) | 🔴 Paid |
| **Speed** | 🟢 Fast | 🟡 Medium | 🟢 Very Fast |
| **Image Quality** | 🔴 Generic | 🟢 Real | 🟢 Optimized |
| **Maintenance** | 🟢 Zero | 🟡 Medium | 🟢 Low |
| **UX** | 🟡 Acceptable for demo | 🟢 Good | 🟢 Excellent |

**สรุป:** Placeholder สำหรับ demo/MVP, production ควรใช้ CDN

---

### Color Histogram vs CLIP Embeddings

| Aspect | Color Histogram (Current) | CLIP Embeddings |
|--------|--------------------------|-----------------|
| **Accuracy** | 🔴 Poor (30-40%) | 🟢 Excellent (85-95%) |
| **Setup** | 🟢 Easy | 🔴 Complex |
| **Speed** | 🟢 Fast (< 100ms) | 🟡 Medium (500ms without GPU) |
| **Requirements** | 🟢 CPU only | 🔴 GPU recommended |
| **Model Size** | 🟢 0 MB | 🔴 ~600 MB |
| **Understanding** | 🔴 Colors only | 🟢 Semantic content |
| **Cost** | 🟢 Free | 🟡 Cloud GPU costs |

**ตัวอย่าง:**
- **Color Histogram**: รูปฟ้าสีฟ้า = ทุกรูปที่มีฟ้าสีฟ้า (ไม่ดูว่ามีภูเขาหรือวัด)
- **CLIP**: รูปวัด = หาวัดอื่นๆ (เข้าใจ semantic meaning)

**สรุป:** CLIP เหมาะสำหรับ production, Color Histogram สำหรับ demo เท่านั้น

---

## การ Deploy (Deployment)

### 1. Local Development

```bash
# Already covered in "How to Use"
cd AI/backend
source venv/bin/activate
./start.sh
```

---

### 2. Production Deployment Options

#### Option A: Traditional VPS (DigitalOcean, Linode, etc.)

**ข้อดี:**
- Full control
- Simple deployment
- Predictable costs

**Steps:**
```bash
# 1. Setup server
ssh user@your-server-ip

# 2. Install dependencies
sudo apt update
sudo apt install python3.13 python3.13-venv nginx

# 3. Clone repo
git clone <your-repo>
cd AI/backend

# 4. Setup venv & install
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Run with systemd
sudo nano /etc/systemd/system/tripplanner.service
```

**tripplanner.service:**
```ini
[Unit]
Description=Plan My Trip API
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/AI/backend
ExecStart=/path/to/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 6. Enable & start
sudo systemctl enable tripplanner
sudo systemctl start tripplanner

# 7. Setup Nginx reverse proxy
sudo nano /etc/nginx/sites-available/tripplanner
```

**Nginx config:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# 8. Enable site & restart Nginx
sudo ln -s /etc/nginx/sites-available/tripplanner /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

---

#### Option B: Docker

**ข้อดี:**
- Consistent environment
- Easy scaling
- Better for CI/CD

**Dockerfile:**
```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Run
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  api:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - PYTHONUNBUFFERED=1
    restart: always

  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./frontend:/usr/share/nginx/html
    restart: always
```

**Deploy:**
```bash
docker-compose up -d
```

---

#### Option C: Cloud Platforms

##### 1. Heroku
```bash
# Procfile
web: uvicorn app:app --host 0.0.0.0 --port $PORT

# Deploy
heroku create your-app-name
git push heroku main
```

**ข้อดี:** Easy deployment
**ข้อเสีย:** Expensive for production

---

##### 2. AWS Elastic Beanstalk
```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.13 trip-planner

# Create environment
eb create trip-planner-env

# Deploy
eb deploy
```

**ข้อดี:** Auto-scaling, managed
**ข้อเสีย:** More complex

---

##### 3. Google Cloud Run (Recommended for small-medium traffic)

**ข้อดี:**
- Serverless (pay per request)
- Auto-scaling
- Easy deployment

**Steps:**
```bash
# 1. Install gcloud CLI
# 2. Build container
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/trip-planner

# 3. Deploy
gcloud run deploy trip-planner \
  --image gcr.io/YOUR_PROJECT_ID/trip-planner \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated
```

**Cost Estimate:**
- 0-1M requests: ~$0
- 1-10M requests: ~$50-200/month

---

### 3. Database Migration (Optional)

**เมื่อไหร่ต้อง migrate:**
- Data > 10K rows
- Frequent updates
- Multiple concurrent writes
- Need data versioning

**Recommended: PostgreSQL**

```bash
# Install
pip install sqlalchemy psycopg2-binary

# Update data_loader.py
from sqlalchemy import create_engine
import pandas as pd

class DataLoader:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)

    def get_data(self):
        return pd.read_sql("SELECT * FROM places", self.engine)
```

---

### 4. Monitoring & Logging

#### Add Logging to app.py:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

#### Production Monitoring Tools:
- **Sentry**: Error tracking
- **Prometheus + Grafana**: Metrics
- **ELK Stack**: Log aggregation

---

## Troubleshooting

### Common Issues

#### 1. ModuleNotFoundError
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
# Check if venv is activated
which python  # Should show venv path

# Reinstall
pip install -r requirements.txt
```

---

#### 2. Port Already in Use
```
ERROR: [Errno 48] Address already in use
```

**Solution:**
```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn app:app --port 8001
```

---

#### 3. CORS Error
```
Access to fetch blocked by CORS policy
```

**Solution:** Already configured in [app.py:23-30](AI/backend/app.py#L23-L30)
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
```

---

#### 4. CSV File Not Found
```
FileNotFoundError: chiang_rai_featured.csv
```

**Solution:**
```bash
# Check path
ls AI/data/chiang_rai_featured.csv

# Update DATA_FILE in app.py if needed
DATA_FILE = "../data/chiang_rai_featured.csv"
```

---

#### 5. Pandas Compatibility Issue
```
ImportError: cannot import name '_maybe_promote'
```

**Solution:**
```bash
# Update pandas
pip install --upgrade pandas>=2.2.0
```

---

#### 6. Photos Not Showing
**Symptoms:** Placeholder images instead of real photos

**Cause:** CSV contains filenames, not URLs

**Solution Options:**

**Option 1: Use placeholders (current)**
- Already implemented
- Good for demo

**Option 2: Setup Google Drive API**
- Follow instructions in [photo_utils.py:84-145](AI/backend/utils/photo_utils.py#L84-L145)

**Option 3: Move photos to CDN**
```bash
# Upload to Cloudinary
for file in photos/*; do
    curl -X POST https://api.cloudinary.com/v1_1/YOUR_CLOUD/upload \
      -F "file=@$file" \
      -F "upload_preset=YOUR_PRESET"
done
```

---

#### 7. Image Search Returns Random Results
**Cause:** Current implementation uses color histogram (mock)

**Solution:** Implement CLIP embeddings (see [Components Details - ImageSimilaritySearch](#4-imagesimilaritysearch-servicesimage_similaritypy))

---

#### 8. Route Still Inefficient
**Possible causes:**
- Not enough iterations (default: 100)
- Dataset characteristics

**Solution:**
```python
# Increase max_iterations in route_optimizer.py:95
def _two_opt_improvement(..., max_iterations=200):  # Default was 100
```

---

## Performance Optimization Tips

### 1. Caching

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def calculate_distance(lat1, lng1, lat2, lng2):
    return haversine_distance(lat1, lng1, lat2, lng2)
```

---

### 2. Pre-compute Place Embeddings (for Image Search)

```python
# One-time script
import pickle
from services.image_similarity import ImageSimilaritySearch

search = ImageSimilaritySearch()
embeddings = {}

for idx, row in df.iterrows():
    if row['photo_1']:
        embeddings[row['place_id']] = search.extract_embedding(row['photo_1'])

with open('place_embeddings.pkl', 'wb') as f:
    pickle.dump(embeddings, f)
```

---

### 3. Use uvloop (Faster async)

```bash
pip install uvloop
```

```python
# In app.py
import uvloop
uvloop.install()
```

---

## Next Steps

### Immediate (Demo → MVP)
1. ✅ Fix route optimization (Done)
2. ✅ Add selected places summary (Done)
3. ⬜ Setup Google Drive photo mapping
4. ⬜ Deploy to cloud (Cloud Run recommended)
5. ⬜ Add error handling & logging

### Short-term (MVP → Production)
1. ⬜ Implement CLIP for image search
2. ⬜ Add user authentication
3. ⬜ Migrate to PostgreSQL
4. ⬜ Add caching (Redis)
5. ⬜ Setup monitoring (Sentry)

### Long-term (Production → Scale)
1. ⬜ ML-based personalized recommendations
2. ⬜ Multi-day trip planning
3. ⬜ Real-time traffic integration
4. ⬜ Mobile app (Flutter/React Native)
5. ⬜ Social features (share trips, reviews)

---

## Summary

| Component | What It Does | When to Use | Production Ready? |
|-----------|--------------|-------------|-------------------|
| **TripPlanner** | วางแผนทริปด้วย rule-based scoring | Theme/place-based planning | 🟢 Yes (MVP) |
| **RouteOptimizer** | เพิ่มประสิทธิภาพเส้นทาง (2-opt) | 5-50 สถานที่ | 🟢 Yes |
| **CarbonCalculator** | คำนวณ carbon & eco score | ทุกทริป | 🟡 Need real data |
| **ImageSimilarity** | ค้นหาสถานที่จากรูป | Image search feature | 🔴 Need CLIP |
| **PhotoUtils** | จัดการ photo URLs | Photo display | 🟡 Need Google Drive API |
| **In-Memory Storage** | เก็บข้อมูลใน RAM | < 10K rows, read-heavy | 🟢 Yes (small scale) |
| **Placeholder Images** | แสดงรูป generic | Demo/development | 🟡 MVP only |

---

## Contact & Support

- **GitHub Issues**: [Report bugs](https://github.com/your-repo/issues)
- **Documentation**: [README.md](README.md), [QUICKSTART.md](QUICKSTART.md)
- **API Docs**: http://localhost:8000/docs (when running)

---

**เอกสารนี้สร้างเมื่อ:** 2025-10-30
**Version:** 1.0
**สถานะ:** Production-Ready for MVP, Need Enhancements for Scale

