# YOLO Object Detection for ADAS - Complete Project Run Report

## Execution Date: November 21, 2025

---

## PROJECT OVERVIEW

This project implements YOLOv5-based object detection for Advanced Driver Assistance Systems (ADAS) using thermal imaging. The complete workflow includes data preprocessing, model training (already completed), and inference on validation data.

---

## SYSTEM ENVIRONMENT

**Hardware & OS:**
- Platform: macOS 26.1 (ARM64 - Apple Silicon)
- CPU: Apple Silicon (M-series)
- GPU: Not available (CPU-only inference)

**Software:**
- Python: 3.14.0
- PyTorch: 2.9.1
- CUDA: Not available (CPU mode)
- YOLOv5: Latest (cloned from ultralytics/yolov5)

**Dependencies Installed:**
- torch, torchvision, opencv-python, numpy, pandas
- matplotlib, seaborn, tensorboard
- jupyter, notebook, ipykernel, ipywidgets
- ultralytics, gitpython, dill
- All requirements from requirements.txt (✓ installed successfully)

---

## DATASET

**Structure:**
- Training images: 12 samples in `dataset/images/train/`
- Validation images: 4 samples in `dataset/images/val/`
- Labels: YOLO format (.txt files) in `dataset/labels/train/` and `dataset/labels/val/`

**Classes (10 total):**
1. person
2. bike
3. car
4. motor
5. bus
6. train
7. truck
8. scooter
9. other_vehicle
10. background

**Image specifications:**
- Format: JPG (thermal images)
- Resolution: 640x512 pixels
- Source: FLIR ADAS Dataset

---

## MODEL DETAILS

**Architecture:** YOLOv5n (Nano variant)
- Layers: 157
- Parameters: 1,771,342
- GFLOPs: 4.2
- Input size: 640x640

**Training Configuration:**
- Epochs: 10
- Batch size: 16
- Image size: 640
- Device: GPU (training was done previously)
- Weights location: `yolov5/runs/train/exp_model-n_img-640/weights/`
  - best.pt (3.7 MB)
  - last.pt (3.7 MB)

**Model Loading:**
- Original weights had WindowsPath serialization issue
- Fixed using custom pathlib patching script (`fix_weights.py`)
- Created `best_fixed.pt` for cross-platform compatibility
- Load time: 0.108s (CPU)

---

## INFERENCE RESULTS

**Performance Metrics:**
- Total validation images processed: 4
- Total detections: 1
- Average inference time: **19.55 ms per image**
- Total inference time: 0.078s
- Confidence threshold: 0.25
- IOU threshold: 0.45

**Per-Image Results:**

| Image       | Detections | Inference Time | Details |
|------------|-----------|----------------|---------|
| val_000.jpg | 0         | 22.98 ms       | No objects detected |
| val_001.jpg | 1         | 18.14 ms       | car (conf: 0.501) |
| val_002.jpg | 0         | 18.38 ms       | No objects detected |
| val_003.jpg | 0         | 18.68 ms       | No objects detected |

**Detection Summary:**
- Cars detected: 1
- Average confidence: 0.501
- Detection rate: 25% (1 out of 4 images)

---

## OUTPUT FILES

**Created/Modified Files:**

1. **requirements.txt** - Python package dependencies
2. **fix_weights.py** - Script to fix WindowsPath serialization issues
3. **run_yolo_inference.py** - Initial inference runner (with fallbacks)
4. **run_complete_inference.py** - Final complete inference script
5. **run_live_camera.py** - Real-time camera detection script ⭐ NEW
6. **runtime_report.txt** - Initial runtime data
7. **final_runtime_report.txt** - Detailed inference results
8. **PROJECT_SUMMARY.md** - This comprehensive report
9. **LIVE_CAMERA_GUIDE.md** - Live camera usage guide ⭐ NEW

**Directories Created:**

1. **yolov5_official/** - Cloned official YOLOv5 repository
2. **inference_outputs/** - Initial test outputs
3. **final_inference_results/** - Final annotated validation images
   - val_000.jpg (annotated)
   - val_001.jpg (annotated with car detection)
   - val_002.jpg (annotated)
   - val_003.jpg (annotated)

---

## CHALLENGES RESOLVED

1. **Missing requirements.txt**
   - Created comprehensive requirements file with all dependencies
   - Successfully installed all packages

2. **WindowsPath Compatibility Issue**
   - Problem: Model weights contained Windows-specific path serialization
   - Solution: Created pathlib monkey-patch in fix_weights.py
   - Result: Successfully loaded and converted weights to macOS-compatible format

3. **YOLOv5 Hub Configuration Missing**
   - Problem: Local yolov5 folder lacked hubconf.py
   - Solution: Cloned official ultralytics/yolov5 repository
   - Result: Proper model loading infrastructure

4. **Missing Dependencies (dill, gitpython)**
   - Problem: YOLOv5 required additional packages
   - Solution: Installed gitpython and dill
   - Result: Full YOLOv5 functionality

5. **torch.load Security Changes (PyTorch 2.6+)**
   - Problem: New weights_only=True default blocked custom model classes
   - Solution: Used weights_only=False with proper sys.path configuration
   - Result: Successful model checkpoint loading

---

## PERFORMANCE ANALYSIS

**Inference Speed:**
- CPU-only inference: ~19.55ms per image
- Throughput: ~51 images per second
- Model is lightweight and efficient for real-time ADAS applications

**Detection Quality:**
- Low detection rate (25%) on validation set suggests:
  - Limited training data (only 10 epochs, small dataset)
  - Possible overfitting or underfitting
  - Thermal images may require more training

**Recommendations for Improvement:**
1. Increase training epochs (suggested: 100-300)
2. Expand training dataset (current: 12 images → target: 1000+)
3. Use data augmentation
4. Fine-tune confidence thresholds per class
5. Consider GPU training for faster iterations
6. Implement class balancing if needed

---

## HOW TO RUN THE PROJECT

### Setup:
```bash
# Install dependencies
pip install -r requirements.txt

# Fix weights (if needed)
python fix_weights.py
```

### Run Inference on Validation Images:
```bash
# Complete inference with metrics
python run_complete_inference.py
```

### Run Live Camera Detection:
```bash
# Basic live detection with webcam
python run_live_camera.py

# With video recording
python run_live_camera.py --save-video

# Custom camera (USB camera, etc.)
python run_live_camera.py --camera 1

# All options
python run_live_camera.py --camera 0 --conf-thres 0.25 --save-video --output my_video.mp4
```

**Camera Controls:**
- Press `q` to quit
- Press `s` to save current frame
- Press `p` to pause/resume

See `LIVE_CAMERA_GUIDE.md` for detailed instructions.

### View Results:
- Annotated images: `final_inference_results/`
- Detailed report: `final_runtime_report.txt`
- Project summary: `PROJECT_SUMMARY.md`
- Live camera guide: `LIVE_CAMERA_GUIDE.md`

---

## NEXT STEPS

1. **Enhance Dataset:**
   - Add more thermal images (target: 1000+ per split)
   - Balance classes (especially underrepresented: motor, bus, train)
   - Add data augmentation

2. **Improve Training:**
   - Train for more epochs (100-300)
   - Use GPU for faster training
   - Implement learning rate scheduling
   - Try larger YOLOv5 variants (s, m, l, x)

3. **Optimize Model:**
   - Hyperparameter tuning
   - Class-specific confidence thresholds
   - Test-time augmentation (TTA)
   - Model ensemble

4. **Live Camera Integration:** ✅ DONE
   - ✓ Real-time camera detection implemented
   - ✓ Interactive controls (pause, save, quit)
   - ✓ FPS and performance metrics display
   - ✓ Video recording capability
   - Next: Add multi-camera support

5. **Deployment:**
   - Convert to ONNX for cross-platform deployment
   - Optimize for edge devices
   - Add object tracking for video streams
   - Implement alert system for ADAS applications

---

## FILES & DIRECTORIES STRUCTURE

```
YOLO-Object-Detection-and-Classification-for-ADAS/
├── dataset/
│   ├── data.yaml
│   ├── images/
│   │   ├── train/ (12 images)
│   │   └── val/ (4 images)
│   └── labels/
│       ├── train/ (12 labels)
│       └── val/ (4 labels)
├── yolov5/
│   ├── runs/train/exp_model-n_img-640/
│   │   └── weights/
│   │       ├── best.pt (3.7 MB)
│   │       ├── best_fixed.pt (3.7 MB)
│   │       └── last.pt (3.7 MB)
│   └── yolov5n.pt
├── yolov5_official/ (cloned repo)
├── final_inference_results/ (annotated outputs)
├── requirements.txt
├── fix_weights.py
├── run_complete_inference.py
├── run_live_camera.py ⭐ NEW
├── final_runtime_report.txt
├── PROJECT_SUMMARY.md (this file)
└── LIVE_CAMERA_GUIDE.md ⭐ NEW
```

---

## CONCLUSION

✓ **Project successfully executed end-to-end**
✓ **All dependencies installed and configured**
✓ **Model weights fixed and loaded successfully**
✓ **Inference completed on validation set**
✓ **Runtime metrics collected and documented**
✓ **Output visualizations generated**

The YOLO object detection system is operational and ready for further development. The low detection rate indicates the model needs more training data and epochs to achieve production-level performance for ADAS applications.

---

**Report Generated:** November 21, 2025
**Execution Time:** ~5 minutes (including setup and inference)
**Status:** ✓ Complete Success
