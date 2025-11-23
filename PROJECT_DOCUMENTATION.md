# ADAS Object Detection System - Complete Project Documentation

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [File Structure & Dependencies](#file-structure--dependencies)
4. [Core Components](#core-components)
5. [Data Flow](#data-flow)
6. [Database Schema](#database-schema)
7. [API Reference](#api-reference)
8. [Setup & Deployment](#setup--deployment)

---

## 🎯 Project Overview

### Purpose
An Advanced Driver Assistance System (ADAS) that uses YOLOv5 AI model to detect vehicles and pedestrians in real-time, estimate their distance, and provide proximity alerts when objects come within 50 meters.

### Key Features
- ✅ Real-time object detection using YOLOv5
- ✅ Distance estimation using monocular vision
- ✅ Proximity alerts (visual & database logging)
- ✅ Web dashboard with live video feed
- ✅ MySQL database for alert history
- ✅ Image capture and storage (file + BLOB)

### Technology Stack
- **AI/ML**: YOLOv5 (PyTorch)
- **Backend**: FastAPI, Python 3.14
- **Frontend**: React (Vite), Vanilla CSS
- **Database**: MySQL 
- **Computer Vision**: OpenCV
- **Real-time**: MJPEG streaming

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE                            │
│              (Browser @ localhost:5173)                      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  React Frontend (Vite)                                  │ │
│  │  - Live Video Display                                   │ │
│  │  - Alert Dashboard                                      │ │
│  │  - Real-time Stats                                      │ │
│  └────────────────┬───────────────────────┬────────────────┘ │
└───────────────────┼───────────────────────┼──────────────────┘
                    │                       │
                    │ HTTP/WS               │ HTTP GET
                    │                       │
┌───────────────────▼───────────────────────▼──────────────────┐
│              FASTAPI BACKEND SERVER                          │
│              (localhost:8000)                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  main.py - FastAPI Application                        │   │
│  │  ├─ /video_feed → MJPEG Stream                       │   │
│  │  ├─ /alerts → JSON API                               │   │
│  │  └─ /alerts/{id}/image → BLOB Images                 │   │
│  └────┬─────────────────────────────────────┬────────────┘   │
│       │                                     │                │
│  ┌────▼──────────────┐             ┌───────▼──────────────┐ │
│  │  camera.py        │             │  routers/alerts.py   │ │
│  │  VideoCamera Class│             │  Database Queries    │ │
│  └────┬──────────────┘             └───────┬──────────────┘ │
└───────┼──────────────────────────────────────┼──────────────┘
        │                                     │
        │ cv2.VideoCapture()                  │ mysql.connector
        │ YOLO Inference                      │
┌───────▼─────────────────┐          ┌────────▼──────────────┐
│   CAMERA HARDWARE       │          │   MySQL DATABASE      │
│   (Webcam/USB Camera)   │          │   'car' database      │
│                         │          │   'alerts' table      │
└─────────────────────────┘          └───────────────────────┘
        │                                     ▲
        │ Raw Video Frames                    │
        │                                     │
┌───────▼────────────────────────────────────┴──────────────┐
│              YOLO v5 MODEL                                 │
│   (yolov5_official + trained weights)                      │
│   - Object Detection                                       │
│   - Bounding Box Coordinates                               │
│   - Class Labels & Confidence                              │
└────────────────────────────────────────────────────────────┘
```

---

## 📂 File Structure & Dependencies

### Directory Tree

```
YOLO-Object-Detection-and-Classification-for-ADAS/
│
├── 🔧 Configuration & Setup
│   ├── requirements.txt          → Python dependencies
│   ├── db_setup.py                → Database initialization
│   ├── run_web.sh                 → Startup script (both servers)
│   └── verify_setup.py            → Environment checker
│
├── 🎯 Core Application Files
│   ├── run_live_camera.py         → Standalone desktop app
│   └── PROJECT_REPORT.md          → Technical documentation
│
├── 🌐 Backend (FastAPI)
│   ├── backend/
│   │   ├── main.py                → FastAPI app entry point
│   │   ├── camera.py              → Video processing & YOLO
│   │   └── routers/
│   │       └── alerts.py          → API endpoints
│
├── 💻 Frontend (React)
│   ├── frontend/
│   │   ├── package.json           → NPM dependencies
│   │   ├── vite.config.js         → Build configuration
│   │   ├── index.html             → HTML entry point
│   │   └── src/
│   │       ├── main.jsx           → React entry point
│   │       ├── App.jsx            → Main dashboard component
│   │       └── App.css            → Styling (dark theme)
│
├── 🤖 AI Model
│   ├── yolov5_official/           → YOLOv5 source code
│   └── yolov5/runs/train/.../best_fixed.pt → Trained weights
│
├── 💾 Data Storage
│   ├── captured_alerts/           → Alert images (auto-created)
│   └── dataset/                   → Training data
│
└── 📊 Outputs
    └── live_detection_output.mp4  → Recorded video (optional)
```

---

## 🔧 Core Components

### 1. **Backend: main.py**

**Location**: `backend/main.py`

**Purpose**: FastAPI application server that coordinates video streaming and API endpoints.

**Key Functions**:
```python
get_camera()          # Singleton camera instance
gen_frames(camera)    # Generator for MJPEG stream
video_feed()          # Endpoint: GET /video_feed
camera_status()       # Endpoint: GET /camera/status
read_root()           # Endpoint: GET /
```

**Dependencies**:
- ← Imports `VideoCamera` from `camera.py`
- ← Imports alert router from `routers/alerts.py`
- → Serves to React frontend
- ↔ CORS middleware for cross-origin requests

**Data Flow**:
```
Browser Request → FastAPI → get_camera() → VideoCamera.get_frame()
→ JPEG bytes → gen_frames() → StreamingResponse → Browser
```

---

### 2. **Backend: camera.py**

**Location**: `backend/camera.py`

**Purpose**: Core video processing with YOLO inference and alert logic.

**Key Class**: `VideoCamera`

**Initialization Flow**:
```
1. Load YOLOv5 model (DetectMultiBackend)
2. Open camera (cv2.VideoCapture)
3. Connect to MySQL database
4. Create alerts directory
```

**Key Methods**:
```python
__init__()                    # Initialize camera, model, DB
get_frame()                   # Capture → Detect → Annotate → Return JPEG
estimate_distance(bbox_width) # Calculate distance from bounding box
connect_db()                  # MySQL connection
```

**Dependencies**:
- ← `cv2` (OpenCV) for camera capture
- ← `torch` + YOLOv5 for object detection
- ← `mysql.connector` for database
- → Streams frames to `main.py`

**Alert Logic Flow**:
```
Frame → YOLO Detection → Extract BBox → Calculate Distance
→ IF distance < 50m:
    ├─ Draw WARNING on frame
    ├─ Save image to captured_alerts/
    └─ INSERT into MySQL (with BLOB)
```

---

### 3. **Backend: routers/alerts.py**

**Location**: `backend/routers/alerts.py`

**Purpose**: REST API endpoints for fetching alert data.

**Endpoints**:
```python
GET /alerts/?limit=10           # Fetch recent alerts (JSON)
GET /alerts/{id}/image          # Fetch alert image (JPEG blob)
```

**Database Connection**:
- Uses **connection pooling** for performance
- Pool size: 5 connections
- Auto-reconnect on failure

**Dependencies**:
- ← MySQL database ('car'.alerts table)
- → Serves JSON/images to React frontend

**Response Format** (`GET /alerts`):
```json
[
  {
    "id": 13,
    "timestamp": "2025-11-23T00:26:00",
    "object_class": "car",
    "confidence": 0.92,
    "distance": 6.3,
    "image_path": "captured_alerts/alert_1763837574_6.3m.jpg"
  }
]
```

---

### 4. **Frontend: App.jsx**

**Location**: `frontend/src/App.jsx`

**Purpose**: Main React dashboard component.

**State Management**:
```javascript
alerts        // Array of alert objects
isConnected   // Backend connection status
stats         // {totalAlerts, activeWarnings}
```

**Key Features**:
1. **Live Video Feed**: `<img src="http://localhost:8000/video_feed" />`
2. **Alert Polling**: `setInterval(fetchAlerts, 2000)` - polls every 2 seconds
3. **Dynamic Stats**: Real-time count of warnings

**API Calls**:
```javascript
axios.get('http://localhost:8000/alerts?limit=10')  // Fetch alerts
// Images loaded via: http://localhost:8000/alerts/{id}/image
```

**UI Sections**:
- 📊 Header (logo, title, status)
- 📈 Stats Bar (total alerts, active warnings)
- 🎥 Video Feed Section
- 🚨 Alerts Panel (scrollable list)

---

### 5. **Frontend: App.css**

**Location**: `frontend/src/App.css`

**Purpose**: Premium dark-themed styling with animations.

**Design System**:
```css
--bg-primary: #0f172a      /* Dark blue */
--accent-cyan: #06b6d4      /* Cyan highlights */
--accent-red: #ef4444       /* Alert color */
--text-primary: #f1f5f9     /* Light text */
```

**Key Features**:
- 🎨 Glassmorphism effects (`backdrop-filter: blur(10px)`)
- ✨ Pulse animations for status indicators
- 🌊 Smooth transitions and hover effects
- 📱 Responsive grid layout

---

### 6. **Database: db_setup.py**

**Location**: `db_setup.py`

**Purpose**: Initialize MySQL database and tables.

**Creates**:
```sql
DATABASE: car

TABLE: alerts
  ├─ id (INT, PRIMARY KEY, AUTO_INCREMENT)
  ├─ timestamp (DATETIME)
  ├─ object_class (VARCHAR(50))
  ├─ confidence (FLOAT)
  ├─ distance (FLOAT)
  ├─ image_path (VARCHAR(255))
  └─ image_data (LONGBLOB)          ← Binary image data
```

**Execution**:
```bash
python3 db_setup.py
```

**Error Handling**:
- Creates database if doesn't exist
- Drops and recreates table (to update schema)
- Connection validation

---

### 7. **Standalone: run_live_camera.py**

**Location**: `run_live_camera.py`

**Purpose**: Desktop application (no web interface).

**Features**:
- Opens live camera in OpenCV window
- Real-time YOLO detection
- Distance estimation & alerts
- Database logging
- Video recording (optional)

**Keyboard Controls**:
- `q`: Quit
- `s`: Save current frame
- `p`: Pause/Resume

**Usage**:
```bash
python run_live_camera.py --save-video --output demo.mp4
```

---

## 🔄 Data Flow

### Complete Request-Response Cycle

#### **1. User Opens Dashboard**
```
1. Browser → http://localhost:5173
2. Vite dev server → Serves index.html
3. React loads → App.jsx mounts
4. useEffect triggers → fetchAlerts()
5. axios.get('http://localhost:8000/alerts')
6. FastAPI routes to alerts.py
7. MySQL query → SELECT * FROM alerts ORDER BY id DESC LIMIT 10
8. JSON response → Browser updates state
9. Alert images load → http://localhost:8000/alerts/{id}/image
```

#### **2. Video Stream Initialization**
```
1. <img src="http://localhost:8000/video_feed"> loads
2. FastAPI receives GET /video_feed
3. main.py calls get_camera()
4. VideoCamera.__init__() executes:
   ├─ Loads YOLOv5 model
   ├─ Opens cv2.VideoCapture(0)
   └─ Connects to MySQL
5. gen_frames() generator starts
6. Loop:
   ├─ camera.get_frame() → Captures frame
   ├─ YOLO inference → Detections
   ├─ Draw bounding boxes
   ├─ Check distance → Alert if < 50m
   ├─ Encode to JPEG
   └─ Yield MJPEG frame
7. StreamingResponse → Browser displays
```

#### **3. Alert Triggered**
```
1. YOLO detects car with bbox width = 400px
2. estimate_distance(400) → 4.5 meters
3. IF 4.5 < 50:
   ├─ cv2.putText("WARNING: PROXIMITY ALERT")
   ├─ Save: captured_alerts/alert_1763837574_4.5m.jpg
   ├─ cv2.imencode() → JPEG bytes
   └─ INSERT INTO alerts (..., image_data = bytes)
4. Next frontend poll (2 sec) →  fetch shows new alert
```

---

## 💾 Database Schema

### Table: `alerts`

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `id` | INT (PK) | Unique alert ID | 13 |
| `timestamp` | DATETIME | When alert occurred | 2025-11-23 00:26:00 |
| `object_class` | VARCHAR(50) | Type of object | "car", "truck", "person" |
| `confidence` | FLOAT | Model confidence | 0.92 (92%) |
| `distance` | FLOAT | Estimated distance (m) | 6.3 |
| `image_path` | VARCHAR(255) | File path | captured_alerts/alert_*.jpg |
| `image_data` | LONGBLOB | Binary image | \xFF\xD8\xFF... |

### Query Examples

```sql
-- Get 10 most recent alerts
SELECT * FROM car.alerts ORDER BY id DESC LIMIT 10;

-- Get all critical alerts (< 30m)
SELECT * FROM car.alerts WHERE distance < 30;

-- Get alerts for a specific date
SELECT * FROM car.alerts 
WHERE DATE(timestamp) = '2025-11-23';

-- Get image size
SELECT id, LENGTH(image_data) as size_bytes 
FROM car.alerts;
```

---

## 🔌 API Reference

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Root
```http
GET /
```
**Response**:
```json
{
  "status": "ADAS Backend Running",
  "endpoints": ["/video_feed", "/alerts", "/camera/status"]
}
```

---

#### 2. Video Feed
```http
GET /video_feed
```
**Response**: `multipart/x-mixed-replace` (MJPEG stream)

**Usage in HTML**:
```html
<img src="http://localhost:8000/video_feed">
```

---

#### 3. Get Alerts
```http
GET /alerts?limit=10
```
**Parameters**:
- `limit` (optional, default=10): Number of alerts to fetch

**Response**:
```json
[
  {
    "id": 13,
    "timestamp": "2025-11-23T00:26:00",
    "object_class": "car",
    "confidence": 0.92,
    "distance": 6.3,
    "image_path": "captured_alerts/alert_1763837574_6.3m.jpg"
  }
]
```

---

#### 4. Get Alert Image
```http
GET /alerts/{alert_id}/image
```
**Response**: `image/jpeg` (BLOB data)

**Example**:
```
http://localhost:8000/alerts/13/image
```

---

#### 5. Camera Status
```http
GET /camera/status
```
**Response**:
```json
{
  "camera_initialized": true,
  "camera_open": true
}
```

---

## 🚀 Setup & Deployment

### Prerequisites
```bash
- Python 3.14+
- MySQL 8.0+
- Node.js 18+
- Webcam/Camera
```

### Installation

#### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
pip install fastapi uvicorn mysql-connector-python
```

#### 2. Setup Database
```bash
python3 db_setup.py
# Enter MySQL credentials when prompted (root / Anurag*29)
```

#### 3. Install Frontend Dependencies
```bash
cd frontend
npm install
cd ..
```

### Running the Application

#### Option A: All-in-One Script
```bash
./run_web.sh
```

#### Option B: Manual (Separate Terminals)

**Terminal 1 - Backend**:
```bash
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

#### Option C: Desktop App Only
```bash
python run_live_camera.py
```

### Access Points
- **Dashboard**: http://localhost:5173
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Auto-generated)

---

## 🔧 Configuration

### Distance Calibration
Edit `backend/camera.py`:
```python
self.FOCAL_LENGTH = 1000  # Increase if distances underestimated
self.KNOWN_WIDTH = 1.8    # Average car width in meters
```

### Alert Threshold
```python
if dist < 50.0:  # Change threshold here (meters)
    # Alert logic
```

### MySQL Credentials
Edit `backend/routers/alerts.py` and `backend/camera.py`:
```python
db_config = {
    'user': 'root',
    'password': 'YOUR_PASSWORD',
    'host': 'localhost',
    'database': 'car'
}
```

---

## 📊 Performance Metrics

### Typical Performance
- **FPS**: 13-15 frames per second
- **Inference Time**: ~70ms per frame (CPU)
- **Alert Response**: < 100ms
- **Database Insert**: ~50ms

### Optimization Tips
1. Use GPU for YOLO inference (10x speedup)
2. Reduce image size (640x640 → 416x416)
3. Lower confidence threshold for faster detection
4. Use database connection pooling (already implemented)

---

## 🐛 Troubleshooting

### Camera Not Opening
```python
# Check camera permissions in System Settings
# Try different camera ID:
cap = cv2.VideoCapture(1)  # Instead of 0
```

### Database Connection Failed
```bash
# Check MySQL is running:
mysql.server start

# Test connection:
mysql -u root -p
```

### Port Already in Use
```bash
# Kill existing process:
lsof -ti:8000 | xargs kill
lsof -ti:5173 | xargs kill
```

---

## 📝 Future Enhancements

1. **Multi-Camera Support**: Handle multiple camera feeds
2. **GPU Acceleration**: CUDA support for faster inference
3. **WebSocket**: Replace polling with real-time updates
4. **User Authentication**: Login system for multi-user access
5. **Cloud Storage**: AWS S3 for alert images
6. **Mobile App**: React Native companion app
7. **Advanced Analytics**: Detection heatmaps, trends

---

## 📄 License & Credits

- **YOLOv5**: Ultralytics (GPL-3.0)
- **FastAPI**: Sebastián Ramírez (MIT)
- **React**: Meta (MIT)
- **Project**: Custom Implementation for ADAS

---

**Document Version**: 1.0  
**Last Updated**: November 23, 2025  
**Author**: AI Assistant + Anurag Dinesh Rokade
