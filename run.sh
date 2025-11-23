#!/bin/bash
# Quick run script for YOLO ADAS project
# Usage: ./run.sh [option]

PYTHON="/usr/local/bin/python3"

case "$1" in
    "menu"|"")
        echo "🚀 Starting interactive menu..."
        $PYTHON launcher.py
        ;;
    "inference"|"images")
        echo "📸 Running inference on validation images..."
        $PYTHON run_complete_inference.py
        ;;
    "camera"|"live")
        echo "📹 Starting live camera detection..."
        echo "Press 'q' in the camera window to quit"
        $PYTHON run_live_camera.py
        ;;
    "record")
        echo "🎬 Starting camera with recording..."
        $PYTHON run_live_camera.py --save-video
        ;;
    "verify"|"check")
        echo "🔍 Verifying setup..."
        $PYTHON verify_setup.py
        ;;
    "help"|"-h"|"--help")
        cat << 'EOF'

🚗 YOLO ADAS - Quick Run Script

Usage: ./run.sh [option]

Options:
  (none)       Start interactive menu (default)
  menu         Start interactive menu
  inference    Run inference on validation images
  camera       Start live camera detection
  record       Start camera with video recording
  verify       Verify setup and dependencies
  help         Show this help message

Examples:
  ./run.sh              # Interactive menu
  ./run.sh camera       # Live camera
  ./run.sh inference    # Process images
  ./run.sh verify       # Check setup

EOF
        ;;
    *)
        echo "❌ Unknown option: $1"
        echo "Run './run.sh help' for usage information"
        exit 1
        ;;
esac
