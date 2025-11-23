# 🚀 Quick Start Guide - YOLO ADAS Object Detection

## ✅ Setup Complete!

All dependencies are installed and the project is ready to run.

---

## 🎯 Three Ways to Run

### 1️⃣ **Interactive Menu (Easiest)**

```bash
/usr/local/bin/python3 launcher.py
```

Then choose:
- **Option 1** - Run inference on validation images
- **Option 2** - Live camera detection
- **Option 3** - Live camera with video recording

---

### 2️⃣ **Direct Commands**

**Run inference on images:**
```bash
/usr/local/bin/python3 run_complete_inference.py
```

**Live camera detection:**
```bash
/usr/local/bin/python3 run_live_camera.py
```

**Camera with recording:**
```bash
/usr/local/bin/python3 run_live_camera.py --save-video --output my_video.mp4
```

---

### 3️⃣ **Verify Setup**

```bash
/usr/local/bin/python3 verify_setup.py
```

This checks all dependencies and files are in place.

---

## 📊 What You'll Get

### Image Inference:
- ✓ Annotated images in `final_inference_results/`
- ✓ Detailed report in `final_runtime_report.txt`
- ✓ Performance metrics (FPS, inference time, detections)

### Live Camera:
- ✓ Real-time object detection window
- ✓ FPS counter and inference time
- ✓ Bounding boxes with labels
- ✓ Interactive controls (q=quit, s=save, p=pause)
- ✓ Optional video recording

---

## 🎮 Camera Controls

When camera window is open:
- **`q`** - Quit and close
- **`s`** - Save current frame
- **`p`** - Pause/Resume

---

## 🎯 Detected Objects

The model detects 9 ADAS-relevant classes:
1. person
2. bike
3. car
4. motor (motorcycle)
5. bus
6. train
7. truck
8. scooter
9. other_vehicle

---

## ⚡ Performance

**On your Mac (CPU):**
- Inference time: ~20ms per image
- FPS (camera): 20-30 fps
- Model size: 3.7 MB
- Parameters: 1.77M

---

## 📝 Example Session

```bash
# 1. Verify everything is ready
/usr/local/bin/python3 verify_setup.py

# 2. Run inference on validation images
/usr/local/bin/python3 run_complete_inference.py

# 3. Try live camera (press 'q' to exit)
/usr/local/bin/python3 run_live_camera.py

# 4. View results
cat final_runtime_report.txt
open final_inference_results/
```

---

## 🔧 Troubleshooting

**If camera doesn't open:**
1. Check System Settings → Privacy & Security → Camera
2. Try different camera ID: `--camera 1` or `--camera 2`
3. Make sure no other app is using the camera

**If "Module not found" error:**
- Always use `/usr/local/bin/python3` (not just `python` or `python3`)
- This ensures the correct Python with packages is used

**If low detection rate:**
- Model was trained on thermal images (not RGB)
- For best results, use a thermal camera or retrain on RGB images
- Adjust confidence threshold: `--conf-thres 0.15` for more detections

---

## 📚 Documentation

- **Live Camera Guide:** `LIVE_CAMERA_GUIDE.md`
- **Project Summary:** `PROJECT_SUMMARY.md`
- **README:** `README.md`

---

## 🎉 You're Ready!

**Start with the launcher:**
```bash
/usr/local/bin/python3 launcher.py
```

**Or jump straight to camera:**
```bash
/usr/local/bin/python3 run_live_camera.py
```

Happy detecting! 🚗📹
