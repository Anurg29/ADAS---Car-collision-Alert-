# 📁 Output Files Guide

## Where Your Results Are Stored

### 🖼️ Image Inference Outputs

**Location:** `./final_inference_results/`

**What's inside:**
- `val_000.jpg` - Annotated validation image 1
- `val_001.jpg` - Annotated validation image 2 (with car detection!)
- `val_002.jpg` - Annotated validation image 3
- `val_003.jpg` - Annotated validation image 4

**How to view:**
```bash
# Open in Finder
open final_inference_results/

# Or view a specific image
open final_inference_results/val_001.jpg
```

---

### 📊 Inference Report

**Location:** `./final_runtime_report.txt`

**What's inside:**
- Environment details (Python, PyTorch version)
- Model information
- Performance metrics (FPS, inference time)
- Per-image detection results with confidence scores

**How to view:**
```bash
cat final_runtime_report.txt

# Or open in text editor
open final_runtime_report.txt
```

---

### 📹 Live Camera Outputs

#### Captured Frames (when you press 's')

**Location:** `./captured_frame_<timestamp>.jpg`

**Example:** `./captured_frame_1732208345.jpg`

**How to capture:**
1. Run: `./run.sh camera`
2. Press `s` key during detection
3. Frame saved to current directory

**How to view:**
```bash
# List all captured frames
ls -lh captured_frame_*.jpg

# Open most recent
open $(ls -t captured_frame_*.jpg | head -1)
```

#### Recorded Videos (with --save-video)

**Default location:** `./live_detection_output.mp4`

**Custom location:** Whatever you specify with `--output`

**How to record:**
```bash
# Default output
./run.sh record

# Custom output name
/usr/local/bin/python3 run_live_camera.py --save-video --output my_demo.mp4
```

**How to view:**
```bash
# Play video
open live_detection_output.mp4

# Or specific video
open my_demo.mp4
```

---

### 🎯 Model Weights

**Location:** `./yolov5/runs/train/exp_model-n_img-640/weights/`

**Files:**
- `best.pt` - Original best model (3.7 MB) - has Windows path issue
- `best_fixed.pt` - Fixed for macOS (3.7 MB) ✓ **CURRENTLY USED**
- `last.pt` - Last training checkpoint (3.7 MB)

**Path used by scripts:**
```python
weights = 'yolov5/runs/train/exp_model-n_img-640/weights/best_fixed.pt'
```

---

### 📈 Training Metrics

**Location:** `./yolov5/runs/train/exp_model-n_img-640/`

**Files:**
- `results.csv` - Training metrics over epochs
- `hyp.yaml` - Hyperparameters used
- `opt.yaml` - Training options
- Tensorboard event files

**How to view:**
```bash
# View CSV metrics
open yolov5/runs/train/exp_model-n_img-640/results.csv

# Or with cat
cat yolov5/runs/train/exp_model-n_img-640/results.csv
```

---

## Quick Commands

```bash
# View all image results
open final_inference_results/

# Read inference report
cat final_runtime_report.txt

# List captured frames
ls -lh captured_frame_*.jpg

# List recorded videos
ls -lh *.mp4

# View training results
cat yolov5/runs/train/exp_model-n_img-640/results.csv
```

---

## File Sizes Reference

- **Annotated images:** ~7-14 KB each
- **Model weights:** 3.7 MB each
- **Reports:** ~1 KB
- **Captured frames:** ~50-200 KB each (depends on content)
- **Recorded videos:** ~1-5 MB per minute (depends on resolution)

---

## Need Help?

- **Image inference:** See `QUICKSTART.md`
- **Live camera:** See `LIVE_CAMERA_GUIDE.md`
- **Project overview:** See `PROJECT_SUMMARY.md`

