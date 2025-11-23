


import cv2
import time
import pathlib
import torch
import numpy as np
import mysql.connector
from datetime import datetime
from pathlib import Path
import sys
import os

# Monkey-patch pathlib BEFORE any imports that might use it
# On macOS/Linux, map WindowsPath to PosixPath (not PurePosixPath)
if not hasattr(pathlib, 'WindowsPath'):
    pathlib.WindowsPath = pathlib.PosixPath

# CRITICAL: Also add to __main__ for torch.load compatibility
import __main__
if not hasattr(__main__, 'WindowsPath'):
    __main__.WindowsPath = pathlib.PosixPath

# Add parent directory to path to find yolov5_official
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../yolov5_official')))

from models.common import DetectMultiBackend
from utils.general import (check_img_size, non_max_suppression, scale_boxes)
from utils.plots import Annotator, colors
from utils.torch_utils import select_device

class VideoCamera:
    def __init__(self, weights='yolov5/runs/train/exp_model-n_img-640/weights/best_fixed.pt'):
        self.weights = weights
        self.conf_thres = 0.25
        self.iou_thres = 0.45
        self.img_size = 640
        
        # Load model
        self.device = select_device('')
        self.model = DetectMultiBackend(self.weights, device=self.device, dnn=False, data=None, fp16=False)
        self.stride, self.names, self.pt = self.model.stride, self.model.names, self.model.pt
        self.imgsz = check_img_size(self.img_size, s=self.stride)
        self.model.warmup(imgsz=(1, 3, self.imgsz, self.imgsz))
        
        # Camera
        print("Attempting to open camera...")
        self.cap = cv2.VideoCapture(0)
        
        # CRITICAL: Validate camera opened successfully
        if not self.cap.isOpened():
            print("❌ Error: Could not open video device 0. Trying device 1...")
            self.cap = cv2.VideoCapture(1)
            if not self.cap.isOpened():
                raise RuntimeError("Could not open any video camera. Please check permissions.")
        
        print(f"✓ Camera opened successfully: {self.cap.getBackendName()}")
        
        # Alert System
        self.last_alert_time = 0
        self.alert_cooldown = 3.0
        self.alert_dir = Path("captured_alerts")
        self.alert_dir.mkdir(exist_ok=True)
        
        # Distance Constants
        self.FOCAL_LENGTH = 1000 
        self.KNOWN_WIDTH = 1.8
        
        # Database
        self.db_config = {
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', 'Anurag*29'),
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'database': os.getenv('DB_NAME', 'car'),
            'connection_timeout': 5
        }
        self.cnx = None
        self.cursor = None
        self.connect_db()

    def connect_db(self):
        try:
            self.cnx = mysql.connector.connect(**self.db_config)
            self.cursor = self.cnx.cursor()
            print("✓ Connected to MySQL database")
        except mysql.connector.Error as err:
            print(f"⚠ Warning: Could not connect to database: {err}")
            self.cnx = None

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()
        if self.cnx and self.cnx.is_connected():
            self.cursor.close()
            self.cnx.close()

    def estimate_distance(self, bbox_width_px):
        if bbox_width_px <= 0: return 999.0
        return (self.KNOWN_WIDTH * self.FOCAL_LENGTH) / bbox_width_px

    def get_frame(self):
        success, frame = self.cap.read()
        if not success:
            return None

        original_frame = frame.copy()
        
        # Preprocess
        img = cv2.resize(frame, (self.imgsz, self.imgsz))
        img = img.transpose((2, 0, 1))[::-1]
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(self.device)
        img = img.half() if self.model.fp16 else img.float()
        img /= 255.0
        if len(img.shape) == 3:
            img = img[None]

        # Inference
        pred = self.model(img, augment=False, visualize=False)
        pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, None, False, max_det=1000)
        
        # Process
        det = pred[0]
        if len(det):
            det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], original_frame.shape).round()
            annotator = Annotator(original_frame, line_width=2, example=str(self.names))
            
            for *xyxy, conf, cls in reversed(det):
                c = int(cls)
                label = f'{self.names[c]} {conf:.2f}'
                annotator.box_label(xyxy, label, color=colors(c, True))
                
                # Alert Logic
                if self.names[c] in ['car', 'truck', 'bus', 'vehicle']:
                    bbox_w = xyxy[2] - xyxy[0]
                    dist = self.estimate_distance(float(bbox_w))
                    
                    dist_label = f"{dist:.1f}m"
                    annotator.box_label([xyxy[0], xyxy[1]-20, xyxy[2], xyxy[1]], dist_label, color=(0, 255, 255))
                    
                    if dist < 50.0:
                        cv2.putText(original_frame, "WARNING: PROXIMITY ALERT!", (50, 100), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                        
                        current_time = time.time()
                        if current_time - self.last_alert_time > self.alert_cooldown:
                            self.last_alert_time = current_time
                            
                            # Save and Log
                            img_name = f"alert_{int(current_time)}_{dist:.1f}m.jpg"
                            save_path = self.alert_dir / img_name
                            cv2.imwrite(str(save_path), original_frame)
                            
                            if self.cnx and self.cnx.is_connected():
                                try:
                                    _, img_encoded = cv2.imencode('.jpg', original_frame)
                                    img_bytes = img_encoded.tobytes()
                                    add_alert = ("INSERT INTO alerts "
                                                 "(timestamp, object_class, confidence, distance, image_path, image_data) "
                                                 "VALUES (%s, %s, %s, %s, %s, %s)")
                                    alert_data = (datetime.now(), self.names[c], float(conf), dist, str(save_path), img_bytes)
                                    self.cursor.execute(add_alert, alert_data)
                                    self.cnx.commit()
                                except mysql.connector.Error as err:
                                    print(f"DB Error: {err}")

            original_frame = annotator.result()

        ret, jpeg = cv2.imencode('.jpg', original_frame)
        return jpeg.tobytes()
