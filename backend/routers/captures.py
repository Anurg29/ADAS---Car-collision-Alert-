from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import FileResponse
from pathlib import Path
from typing import List
from pydantic import BaseModel
from datetime import datetime
import os

router = APIRouter(prefix="/captures", tags=["captures"])

CAPTURE_DIR = Path("captured_alerts")

class CaptureFile(BaseModel):
    filename: str
    timestamp: int
    distance: str
    filesize: int
    url: str

@router.get("/", response_model=List[CaptureFile])
def get_recent_captures(limit: int = 20):
    """Get list of recent captured alert images"""
    try:
        if not CAPTURE_DIR.exists():
            return []
        
        files= []
        for file in CAPTURE_DIR.glob("alert_*.jpg"):
            # Parse filename: alert_1763879533_13.1m.jpg
            parts = file.stem.split('_')
            if len(parts) >= 3:
                timestamp = int(parts[1])
                distance = parts[2]
                
                files.append({
                    "filename": file.name,
                    "timestamp": timestamp,
                    "distance": distance,
                    "filesize": file.stat().st_size,
                    "url": f"/captures/image/{file.name}"
                })
        
        # Sort by timestamp (newest first)
        files.sort(key=lambda x: x['timestamp'], reverse=True)
        return files[:limit]
        
    except Exception as e:
        print(f"Error listing captures: {e}")
        return []

@router.get("/image/{filename}")
def get_capture_image(filename: str):
    """Get a specific captured image"""
    file_path = CAPTURE_DIR / filename
    
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(file_path, media_type="image/jpeg")

@router.get("/stats")
def get_capture_stats():
    """Get statistics about captures"""
    try:
        if not CAPTURE_DIR.exists():
            return {"total": 0, "today": 0}
        
        files = list(CAPTURE_DIR.glob("alert_*.jpg"))
        total = len(files)
        
        # Count today's captures
        today_start = datetime.now().replace(hour=0, minute=0, second=0).timestamp()
        today_count = sum(1 for f in files if f.stat().st_mtime > today_start)
        
        return {
            "total": total,
            "today": today_count,
            "latest": max((f.stat().st_mtime for f in files), default=0) if files else 0
        }
    except Exception as e:
        return {"total": 0, "today": 0, "error": str(e)}
