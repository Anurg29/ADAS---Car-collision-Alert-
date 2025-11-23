# 📹 Live Camera Detection Guide

## Quick Start

### Basic Usage (Default Webcam):
```bash
python run_live_camera.py
```

### With Video Recording:
```bash
python run_live_camera.py --save-video
```

### Custom Camera (e.g., external USB camera):
```bash
python run_live_camera.py --camera 1
```

### All Options:
```bash
python run_live_camera.py \
    --weights yolov5/runs/train/exp_model-n_img-640/weights/best_fixed.pt \
    --camera 0 \
    --conf-thres 0.25 \
    --iou-thres 0.45 \
    --img-size 640 \
    --save-video \
    --output my_detection_video.mp4
```

## 🎮 Controls

While the camera window is active:

- **`q`** - Quit and close camera
- **`s`** - Save current frame as image
- **`p`** - Pause/Resume detection

## 📊 On-Screen Display

The live feed shows:
- **FPS** - Frames per second
- **Inference time** - Processing time per frame (in ms)
- **Detections** - Number of objects detected in current frame
- **Total Frames** - Total frames processed
- **Bounding boxes** - Around detected objects with class labels and confidence scores

## 🔧 Command-Line Options

| Option | Default | Description |
|--------|---------|-------------|
| `--weights` | `yolov5/.../best_fixed.pt` | Path to model weights |
| `--camera` | `0` | Camera device ID (0=built-in, 1=USB, etc.) |
| `--conf-thres` | `0.25` | Confidence threshold (0.0-1.0) |
| `--iou-thres` | `0.45` | IOU threshold for NMS |
| `--img-size` | `640` | Input image size |
| `--save-video` | `False` | Save output video |
| `--output` | `live_detection_output.mp4` | Output video filename |

## 🎯 Detection Classes

The model detects 9 ADAS-relevant objects:
1. person
2. bike
3. car
4. motor
5. bus
6. train
7. truck
8. scooter
9. other_vehicle

## 💡 Tips

1. **Better Performance:**
   - Lower `--conf-thres` (e.g., 0.15) to detect more objects
   - Lower `--img-size` (e.g., 416) for faster FPS on CPU

2. **More Accurate:**
   - Raise `--conf-thres` (e.g., 0.4) to reduce false positives
   - Ensure good lighting for better detections

3. **Multiple Cameras:**
   - Try `--camera 0`, `--camera 1`, etc. to find your camera
   - On macOS, check System Settings → Privacy & Security → Camera

4. **Troubleshooting:**
   - If camera doesn't open, check permissions
   - Try different camera IDs (0, 1, 2)
   - Make sure no other app is using the camera

## 📈 Performance Expectations

**On CPU (Apple Silicon/M-series):**
- FPS: 20-30 (depending on detections)
- Inference time: ~20-50ms per frame

**On GPU:**
- FPS: 60-100+
- Inference time: ~5-15ms per frame

## 🎬 Example Workflows

### 1. Quick Test:
```bash
python run_live_camera.py
# Press 'q' when done
```

### 2. Record a Demo:
```bash
python run_live_camera.py --save-video --output demo.mp4
# Record for a few minutes, press 'q' to save
```

### 3. Low Latency Mode (Faster FPS):
```bash
python run_live_camera.py --img-size 416 --conf-thres 0.3
```

### 4. High Accuracy Mode:
```bash
python run_live_camera.py --conf-thres 0.4 --img-size 640
```

## 📸 Captured Frames

When you press `s`, frames are saved as:
- `captured_frame_<timestamp>.jpg`

Example: `captured_frame_1700612345.jpg`

## ⚠️ Notes

- The model was trained on **thermal images**, so results on regular RGB camera may vary
- For best results with regular cameras, consider re-training on RGB images
- First-time run may be slower due to model warmup

---

**Enjoy real-time object detection!** 🚗🚴‍♂️🚶‍♂️
