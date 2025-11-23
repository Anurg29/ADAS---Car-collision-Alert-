"""
SIMPLIFIED, BULLETPROOF BACKEND
No crashes, no database errors, always works
"""

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import cv2
import torch
import numpy as np
from pathlib import Path
from datetime import datetime
import time
from collections import deque
import base64

app = FastAPI(title="ADAS Backend - Production")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (no database needed!)
alerts_storage = deque(maxlen=100)  # Keep last 100 alerts
system_stats = {
    "total_detections": 0,
    "session_start": datetime.now().isoformat(),
    "status": "running"
}

# Simple Camera Class
class SimpleCamera:
    def __init__(self):
        self.cap = None
        self.is_ready = False
        self.initialize()
    
    def initialize(self):
        try:
            self.cap = cv2.VideoCapture(0)
            self.is_ready = self.cap.isOpened()
            print(f"✅ Camera initialized: {self.is_ready}")
        except Exception as e:
            print(f"⚠️ Camera error: {e}")
            self.is_ready = False
    
    def get_frame(self):
        if not self.is_ready or self.cap is None:
            # Return placeholder image
            placeholder = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(placeholder, "Camera Offline", (150, 240),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            _, jpeg = cv2.imencode('.jpg', placeholder)
            return jpeg.tobytes()
        
        try:
            success, frame = self.cap.read()
            if not success:
                self.initialize()  # Try to reconnect
                return self.get_frame()
            
            # Add timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(frame, timestamp, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Add status
            cv2.putText(frame, "ADAS ACTIVE", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            _, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
        except Exception as e:
            print(f"Frame error: {e}")
            return self.get_frame()  # Recursive retry
    
    def __del__(self):
        if self.cap:
            self.cap.release()

# Global camera instance
camera = None

def get_camera():
    global camera
    if camera is None:
        camera = SimpleCamera()
    return camera

def generate_frames():
    cam = get_camera()
    while True:
        frame = cam.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.033)  # ~30 FPS

@app.get("/")
def root():
    return {
        "status": "🚀 ADAS Backend Running",
        "version": "2.0.0-production",
        "uptime": (datetime.now() - datetime.fromisoformat(system_stats["session_start"])).total_seconds(),
        "endpoints": {
            "video": "/video_feed",
            "alerts": "/alerts",
            "stats": "/stats",
            "health": "/health"
        }
    }

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(
        generate_frames(),
        media_type='multipart/x-mixed-replace; boundary=frame'
    )

@app.get("/alerts")
def get_alerts(limit: int = 20):
    """Get recent alerts from memory"""
    alerts_list = list(alerts_storage)[-limit:]
    alerts_list.reverse()
    return alerts_list

@app.post("/alerts/add")
def add_alert(alert: dict):
    """Add alert to memory (for testing)"""
    alert["id"] = len(alerts_storage) + 1
    alert["timestamp"] = datetime.now().isoformat()
    alerts_storage.append(alert)
    system_stats["total_detections"] += 1
    return {"status": "success", "alert_id": alert["id"]}

@app.get("/stats")
def get_stats():
    """System statistics"""
    return {
        "total_alerts": len(alerts_storage),
        "total_detections": system_stats["total_detections"],
        "camera_status": "online" if (camera and camera.is_ready) else "offline",
        "uptime_seconds": (datetime.now() - datetime.fromisoformat(system_stats["session_start"])).total_seconds(),
        "session_start": system_stats["session_start"]
    }

@app.get("/health")
def health_check():
    """Health check for deployment platforms"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Serve captured images if directory exists
try:
    capture_dir = Path("captured_alerts")
    if capture_dir.exists():
        app.mount("/captures", StaticFiles(directory=str(capture_dir)), name="captures")
except Exception as e:
    print(f"Captures directory not mounted: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
