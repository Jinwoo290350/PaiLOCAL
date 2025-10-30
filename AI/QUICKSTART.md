# 🚀 Quick Start Guide - Plan My Trip API

## ภาพรวม (Overview)

**Plan My Trip** เป็นระบบวางแผนท่องเที่ยวอัจฉริยะสำหรับจังหวัดเชียงราย ที่มี:
- ✅ **Theme Search**: วางแผนทริปจาก 6 themes (Naturalist, Conservative, Photogenic, etc.)
- ✅ **Image Search**: อัพโหลดรูปเพื่อค้นหาสถานที่คล้ายกัน
- ✅ **Route Optimization**: ใช้อัลกอริทึม 2-opt เพิ่มประสิทธิภาพเส้นทาง
- ✅ **Trip Narrative**: สร้างคำอธิบายเส้นทางภาษาไทยอัตโนมัติ
- ✅ **Carbon Tracking**: คำนวณ carbon footprint และ eco score
- ✅ **Production Ready**: พร้อม deploy (with placeholders for photos)

---

## 🏃 เริ่มใช้งาน 3 ขั้นตอน

### 1. Setup Environment

```bash
# Navigate to backend
cd AI/backend

# Create virtual environment (Python 3.13+)
python3 -m venv venv

# Activate venv
source venv/bin/activate  # macOS/Linux
# หรือ
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

**✅ Expected Output:**
```
Successfully installed fastapi-0.120.2 pandas-2.3.3 uvicorn-0.38.0 ...
```

---

### 2. Start Server

```bash
# Option A: Using startup script (recommended)
./start.sh              # macOS/Linux
start.bat               # Windows

# Option B: Manual
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**✅ Server Running:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
INFO:     Successfully loaded 1055 places into memory
```

---

### 3. Open Demo Pages

**Theme Search:**
```
file:///path/to/AI/frontend/index.html
```

**Image Search:**
```
file:///path/to/AI/frontend/image-search.html
```

**API Documentation:**
```
http://localhost:8000/docs
```

---

## 📋 ทดสอบระบบ

### Test 1: Theme Search (index.html)

1. เปิด `frontend/index.html` ใน browser
2. กรอกข้อมูล:
   - **Starting Location**: 19.9105, 99.8406 (Central Chiang Rai)
   - **Plan By**: Theme
   - **Select Theme**: Naturalist
   - **Number of Stops**: 5
   - **Max Distance**: 50 km
3. คลิก **"Plan My Trip"**

**✅ ผลลัพธ์ที่ต้องได้:**
- แผนที่แสดงเส้นทาง
- **Trip Narrative** (คำอธิบายเส้นทางภาษาไทย):
  ```
  🌟 ทริป Naturalist ที่จะพาคุณเที่ยว 5 สถานที่
     รวม ฟาร์ม 3 แห่ง, จุดชมวิว 2 แห่ง

  📍 เส้นทางการเดินทาง:
     1. PK.FARM Wiang Chi (ฟาร์ม) - ⭐⭐⭐⭐⭐ 5.0/5
        ระยะทางจากจุดเริ่มต้น: 9.6 km
     2. JC ORGANIC FARM (ฟาร์ม) - ⭐⭐⭐⭐⭐ 5.0/5
        ↓ ระยะทาง 3.2 km | คาร์บอน 0.45 kg CO2
     ...

  📊 สรุปทริป:
     • ระยะทางรวม: 45.3 km
     • คาร์บอนฟุตพริ้นท์: 5.8 kg CO2
     • Eco Score: 8.5/10 🌟🌟🌟

  ✅ ทริปนี้เป็นมิตรกับสิ่งแวดล้อม!
  ```
- รายละเอียดแต่ละสถานที่พร้อมรูปภาพ (placeholder)
- Total distance, carbon, eco score

---

### Test 2: Image Search (image-search.html)

1. เปิด `frontend/image-search.html`
2. อัพโหลดรูปภาพ (drag & drop หรือคลิก)
3. คลิก **"🔍 Find Similar Places"**
4. ระบบจะแสดง Top 5 สถานที่ที่คล้ายกัน
5. เลือกสถานที่ที่ต้องการ (1-5 แห่ง)
6. **Selected Places Summary** จะแสดงรายการที่เลือก
7. กรอก Starting Location: 19.9105, 99.8406
8. คลิก **"Plan Trip with Selected Places"**

**✅ ผลลัพธ์ที่ต้องได้:**
- Similar places พร้อม similarity scores
- Selected summary แสดงชื่อสถานที่ที่เลือก
- Trip narrative พร้อมเส้นทางที่เหมาะสม
- แผนที่แสดงเส้นทาง

---

### Test 3: API (Postman/curl)

```bash
# Test theme-based trip planning
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

**✅ Response:**
```json
{
  "trip_id": "trip_abc123",
  "start_location": {"lat": 19.9105, "lng": 99.8406},
  "mode": "theme",
  "theme": "naturalist",
  "summary": {
    "total_stops": 5,
    "total_distance_km": 45.3,
    "estimated_time_hours": 2.5,
    "total_carbon_kg": 5.8,
    "eco_score": 8.5,
    "carbon_reduction_percent": 15.2,
    "narrative": "🌟 ทริป Naturalist...",
    "compact": "เที่ยว 5 แห่ง (ฟาร์ม) • 45 km • 6 kg CO2 • Eco 8.5/10",
    "directions": [
      "🚗 เริ่มต้นที่ PK.FARM Wiang Chi",
      "🚗 มุ่งหน้าทิศเหนือ 3.2 km ไปยัง JC ORGANIC FARM",
      ...
    ]
  },
  "route": [...]
}
```

---

## 🎯 Key Features

### 1. Trip Narrative (NEW!)

ระบบสร้างคำอธิบายเส้นทางภาษาไทยอัตโนมัติ:
- ไม่ใช้ LLM API (ไม่มีค่าใช้จ่าย)
- Template-based generation (fast)
- เหมาะสำหรับ production

### 2. Route Optimization (Upgraded!)

ใช้อัลกอริทึม **2-opt** ลดระยะทาง 10-30%

### 3. Photo System

ใช้ placeholder images (keyword-based) - พร้อมใช้ทันที!

### 4. Unified Starting Location

ทั้ง 2 demo ใช้จุดเริ่มต้น: **19.9105, 99.8406** (Central Chiang Rai)

---

## 📚 Next Steps

- [COMPREHENSIVE_USAGE_GUIDE.md](COMPREHENSIVE_USAGE_GUIDE.md) - Full documentation
- [README.md](README.md) - API reference

---

**Built with ❤️ for sustainable tourism in Chiang Rai**
