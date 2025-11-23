# File Organization Guide

This document explains where everything is and why.

## 📂 Directory Structure

### `/backend` - FastAPI Server
All Python backend code for the web application.
- `main.py` - FastAPI app
- `camera.py` - Video processing
- `routers/alerts.py` - API endpoints

### `/frontend` - React Dashboard
All React/JavaScript frontend code.
- `src/App.jsx` - Main component
- `src/App.css` - Styling
- `package.json` - Dependencies

### `/docs` - Documentation
Additional guides and documentation files.
- `QUICKSTART.md` - Fast setup guide
- `LIVE_CAMERA_GUIDE.md` - Desktop app usage
- `OUTPUT_GUIDE.md` - Understanding outputs

### `/archive` - Old Files
Development files, experiments, and deprecated code.
- Jupyter notebooks
- Old scripts
- Test files

### `/outputs` - Generated Files
Program output files (auto-generated).
- Video recordings
- Screenshots
- Reports

### `/captured_alerts` - Alert Images
Auto-generated alert snapshots (created by the app).

### `/dataset` - Training Data
YOLO training images and labels.

### `/yolov5_official` - YOLOv5 Source
Official YOLOv5 framework code.

### `/yolov5` - Trained Model
Your trained YOLOv5 weights.

---

## 📄 Root Files

### Essential Files (Don't Delete!)
- `README.md` - Main project guide
- `PROJECT_DOCUMENTATION.md` - Complete reference
- `PROJECT_REPORT.md` - Technical summary
- `run_web.sh` - Startup script
- `run_live_camera.py` - Desktop app
- `db_setup.py` - Database setup
- `requirements.txt` - Python dependencies

### Auto-Generated (Safe to Delete)
- `outputs/*` - Test outputs
- `captured_alerts/*` - Old alerts
- `.venv/` - Virtual environment (can regenerate)
- `node_modules/` - Node packages (can regenerate)

---

## 🗑️ What Can I Delete?

### Safe to Delete:
- `/archive` - Old development files
- `/outputs` - Test outputs
- `/captured_alerts/*` - Old alert images
- `live_detection_output.mp4` - Recorded video

### Keep These:
- All Python files in root
- `/backend` and `/frontend` folders
- `/yolov5` and `/yolov5_official`
- `/dataset` (if you want to retrain)
- Documentation files

---

## 🔄 Regenerating Deleted Items

### Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Node Modules
```bash
cd frontend
npm install
```

### Database
```bash
python3 db_setup.py
```

---

## 📊 File Size Guide

Large files (you might want to backup/remove):
- `/yolov5_official/` - ~500MB (YOLOv5 source)
- `/dataset/` - Varies (training images)
- `yolov5n.pt` - ~4MB (pretrained weights)
- `.venv/` - ~1GB (Python packages)
- `node_modules/` - ~200MB (Node packages)
- Video outputs - ~20MB each

---

## 🧹 Cleanup Commands

### Delete all outputs
```bash
rm -rf outputs/*
rm -rf captured_alerts/*
```

### Clean Python cache
```bash
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

### Clean Node
```bash
cd frontend && rm -rf node_modules
```

---

**Tip**: Before deleting, check if files are needed for training or testing!
