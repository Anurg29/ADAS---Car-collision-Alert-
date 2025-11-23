from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from backend.camera import VideoCamera
from backend.routers import alerts, chat, users, captures
import uvicorn

app = FastAPI(title="ADAS Backend API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(alerts.router, tags=["alerts"])
app.include_router(chat.router, prefix="/api", tags=["ai-chat"])
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(captures.router, tags=["captures"])

# Global Camera Instance
camera = None

def get_camera():
    global camera
    if camera is None:
        try:
            print("🎥 Initializing camera system...")
            camera = VideoCamera()
            print("✅ Camera system ready!")
        except Exception as e:
            print(f"❌ Camera initialization failed: {str(e)}")
            # Do not crash the server, just return None so we can try again later
            camera = None
    return camera

def gen_frames(camera):
    if camera is None:
        print("Camera is None, cannot generate frames")
        return
    
    try:
        while True:
            frame = camera.get_frame()
            if frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                print("No frame received from camera")
                break
    except Exception as e:
        print(f"Error in gen_frames: {e}")

@app.get("/video_feed")
def video_feed():
    cam = get_camera()
    if cam is None:
        return Response(content="Camera not available", status_code=503)
    
    return StreamingResponse(gen_frames(cam),
                             media_type='multipart/x-mixed-replace; boundary=frame')

@app.get("/camera/status")
def camera_status():
    cam = get_camera()
    return {
        "camera_initialized": cam is not None,
        "camera_open": cam.cap.isOpened() if cam else False
    }

@app.get("/")
def read_root():
    return {"status": "ADAS Backend Running", "endpoints": ["/video_feed", "/alerts", "/camera/status"]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
