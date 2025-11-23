
"""
Real-time YOLO Object Detection with Live Camera Feed
Runs inference on webcam/camera input with your custom trained ADAS model
"""
import sys
import os
import time
import pathlib
from pathlib import Path

# Monkey-patch pathlib BEFORE any imports that might use it
class WindowsPath(pathlib.PurePosixPath):
    pass
pathlib.WindowsPath = WindowsPath

# Now import torch and other modules
import torch
import cv2
import cv2
import numpy as np
import mysql.connector
from datetime import datetime

# Add yolov5_official to path
sys.path.insert(0, 'yolov5_official')

from models.common import DetectMultiBackend
from utils.general import (check_img_size, non_max_suppression, scale_boxes)
from utils.plots import Annotator, colors
from utils.torch_utils import select_device

class LiveYOLODetector:
    def __init__(self, weights='yolov5/runs/train/exp_model-n_img-640/weights/best_fixed.pt', 
                 conf_thres=0.25, iou_thres=0.45, img_size=640):
        """
        Initialize live YOLO detector
        
        Args:
            weights: Path to model weights
            conf_thres: Confidence threshold for detections
            iou_thres: IOU threshold for NMS
            img_size: Input image size
        """
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.img_size = img_size
        
        # Load model
        print("Loading YOLO model...")
        self.device = select_device('')
        self.model = DetectMultiBackend(weights, device=self.device, dnn=False, data=None, fp16=False)
        self.stride, self.names, self.pt = self.model.stride, self.model.names, self.model.pt
        self.imgsz = check_img_size(img_size, s=self.stride)
        print(f"✓ Model loaded on {self.device}")
        print(f"✓ Classes: {', '.join(self.names.values() if isinstance(self.names, dict) else self.names)}")
        
        # Warm up model
        print("Warming up model...")
        self.model.warmup(imgsz=(1, 3, self.imgsz, self.imgsz))
        print("✓ Ready for inference\n")
        
        # Stats
        self.fps = 0
        self.frame_count = 0
        self.total_detections = 0
        self.start_time = time.time()
        
        # Alert system
        self.last_alert_time = 0
        self.alert_cooldown = 3.0  # Seconds between captures
        self.alert_dir = Path("captured_alerts")
        self.alert_dir.mkdir(exist_ok=True)
        
        # Distance constants (Approximate)
        # Focal length depends on camera field of view. 
        # Assuming a standard webcam with ~60 deg FOV and 640 width -> ~600-800 focal length.
        # We'll use 1000 as a starting point for calibration.
        self.FOCAL_LENGTH = 1000 
        self.KNOWN_WIDTH = 1.8  # Average car width in meters
        
        # Database Connection
        self.db_config = {
            'user': 'root',
            'password': 'Anurag*29',
            'host': 'localhost',
            'database': 'car'
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
    
    def preprocess(self, img):
        """Preprocess image for model input"""
        # Resize and pad
        img_resized = cv2.resize(img, (self.imgsz, self.imgsz))
        
        # Convert to tensor
        img_tensor = img_resized.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        img_tensor = np.ascontiguousarray(img_tensor)
        img_tensor = torch.from_numpy(img_tensor).to(self.device)
        img_tensor = img_tensor.half() if self.model.fp16 else img_tensor.float()
        img_tensor /= 255.0
        
        if len(img_tensor.shape) == 3:
            img_tensor = img_tensor[None]
        
        return img_tensor
    
    def estimate_distance(self, bbox_width_px):
        """
        Estimate distance to object based on bounding box width
        Distance = (Known_Width * Focal_Length) / Pixel_Width
        """
        if bbox_width_px <= 0: return 999.0
        return (self.KNOWN_WIDTH * self.FOCAL_LENGTH) / bbox_width_px
    
    def detect(self, frame):
        """
        Run detection on a single frame
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            Annotated frame with bounding boxes
        """
        original_frame = frame.copy()
        h, w = frame.shape[:2]
        
        # Preprocess
        img_tensor = self.preprocess(frame)
        
        # Inference
        t0 = time.time()
        pred = self.model(img_tensor, augment=False, visualize=False)
        inference_time = time.time() - t0
        
        # NMS
        pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, None, False, max_det=1000)
        
        # Process detections
        det = pred[0]
        detections = []
        
        if len(det):
            # Rescale boxes from img_size to original image size
            det[:, :4] = scale_boxes(img_tensor.shape[2:], det[:, :4], original_frame.shape).round()
            
            # Draw boxes
            annotator = Annotator(original_frame, line_width=2, example=str(self.names))
            
            for *xyxy, conf, cls in reversed(det):
                c = int(cls)
                label = f'{self.names[c]} {conf:.2f}'
                annotator.box_label(xyxy, label, color=colors(c, True))
                
                detections.append({
                    'class': self.names[c],
                    'confidence': float(conf),
                    'bbox': [int(x) for x in xyxy]
                })
                
                # --- Distance & Alert Logic ---
                # Only process for 'car' or 'truck' or 'bus' if your model has those classes
                # For now, we'll assume all detections are relevant vehicles or check class name
                if self.names[c] in ['car', 'truck', 'bus', 'vehicle']: 
                    bbox_w = xyxy[2] - xyxy[0]
                    dist = self.estimate_distance(float(bbox_w))
                    
                    # Add distance label
                    dist_label = f"{dist:.1f}m"
                    annotator.box_label([xyxy[0], xyxy[1]-20, xyxy[2], xyxy[1]], dist_label, color=(0, 255, 255)) # Yellow for distance
                    
                    if dist < 50.0:
                        # Visual Alert
                        cv2.putText(original_frame, "WARNING: VEHICLE PROXIMITY ALERT!", (50, 100), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                        
                        # Capture Alert Image
                        current_time = time.time()
                        if current_time - self.last_alert_time > self.alert_cooldown:
                            img_name = f"alert_{int(current_time)}_{dist:.1f}m.jpg"
                            save_path = self.alert_dir / img_name
                            cv2.imwrite(str(save_path), original_frame)
                            print(f"!!! ALERT: Vehicle at {dist:.1f}m. Image saved to {save_path}")
                            self.last_alert_time = current_time
                            
                            # Log to Database
                            if self.cnx and self.cnx.is_connected():
                                try:
                                    # Encode image to blob
                                    _, img_encoded = cv2.imencode('.jpg', original_frame)
                                    img_bytes = img_encoded.tobytes()
                                    
                                    add_alert = ("INSERT INTO alerts "
                                                 "(timestamp, object_class, confidence, distance, image_path, image_data) "
                                                 "VALUES (%s, %s, %s, %s, %s, %s)")
                                    alert_data = (datetime.now(), self.names[c], float(conf), dist, str(save_path), img_bytes)
                                    self.cursor.execute(add_alert, alert_data)
                                    self.cnx.commit()
                                    print("✓ Alert logged to database (with image data)")
                                except mysql.connector.Error as err:
                                    print(f"⚠ Error logging to DB: {err}")
            
            original_frame = annotator.result()
        
        # Update stats
        self.frame_count += 1
        self.total_detections += len(detections)
        elapsed = time.time() - self.start_time
        self.fps = self.frame_count / elapsed if elapsed > 0 else 0
        
        # Add info overlay
        info_text = [
            f"FPS: {self.fps:.1f}",
            f"Inference: {inference_time*1000:.1f}ms",
            f"Detections: {len(detections)}",
            f"Total Frames: {self.frame_count}"
        ]
        
        y_offset = 30
        for text in info_text:
            cv2.putText(original_frame, text, (10, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            y_offset += 30
        
        return original_frame, detections
    
    def run_camera(self, camera_id=0, save_video=False, output_path='live_detection_output.mp4'):
        """
        Run live detection on camera feed
        
        Args:
            camera_id: Camera device ID (0 for default webcam)
            save_video: Whether to save the output video
            output_path: Path to save output video
        """
        print(f"Opening camera (ID: {camera_id})...")
        cap = cv2.VideoCapture(camera_id)
        
        if not cap.isOpened():
            print(f"✗ Error: Could not open camera {camera_id}")
            print("\nTroubleshooting:")
            print("  1. Check if camera is connected")
            print("  2. Try different camera_id (0, 1, 2, etc.)")
            print("  3. Check camera permissions in System Settings")
            return
        
        # Get camera properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps_cam = int(cap.get(cv2.CAP_PROP_FPS))
        
        print(f"✓ Camera opened successfully")
        print(f"  Resolution: {width}x{height}")
        print(f"  Camera FPS: {fps_cam}")
        
        # Video writer
        video_writer = None
        if save_video:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(output_path, fourcc, 20.0, (width, height))
            print(f"✓ Saving video to: {output_path}")
        
        print("\n" + "="*60)
        print("LIVE DETECTION STARTED")
        print("="*60)
        print("Press 'q' to quit")
        print("Press 's' to save current frame")
        print("Press 'p' to pause/resume")
        print("="*60 + "\n")
        
        paused = False
        frame_num = 0
        
        try:
            while True:
                if not paused:
                    ret, frame = cap.read()
                    if not ret:
                        print("✗ Error: Could not read frame from camera")
                        break
                    
                    # Run detection
                    annotated_frame, detections = self.detect(frame)
                    
                    # Save frame if requested
                    if save_video and video_writer is not None:
                        video_writer.write(annotated_frame)
                    
                    # Display
                    cv2.imshow('YOLO Live Detection - ADAS', annotated_frame)
                    
                    # Print detections
                    if detections:
                        det_str = ", ".join([f"{d['class']}:{d['confidence']:.2f}" for d in detections])
                        print(f"Frame {frame_num:04d}: {det_str}")
                    
                    frame_num += 1
                else:
                    # Show paused frame
                    cv2.imshow('YOLO Live Detection - ADAS', annotated_frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    print("\n✓ Quitting...")
                    break
                elif key == ord('s'):
                    # Save current frame
                    save_path = f"captured_frame_{int(time.time())}.jpg"
                    cv2.imwrite(save_path, annotated_frame)
                    print(f"✓ Frame saved to: {save_path}")
                elif key == ord('p'):
                    paused = not paused
                    status = "PAUSED" if paused else "RESUMED"
                    print(f"✓ {status}")
        
        except KeyboardInterrupt:
            print("\n✓ Interrupted by user")
        
        finally:
            # Cleanup
            cap.release()
            if video_writer is not None:
                video_writer.release()
            if video_writer is not None:
                video_writer.release()
            cv2.destroyAllWindows()
            
            # Close DB connection
            if self.cnx and self.cnx.is_connected():
                self.cursor.close()
                self.cnx.close()
                print("✓ Database connection closed")
            
            # Print statistics
            print("\n" + "="*60)
            print("LIVE DETECTION STATISTICS")
            print("="*60)
            print(f"Total frames processed: {self.frame_count}")
            print(f"Total detections: {self.total_detections}")
            print(f"Average FPS: {self.fps:.2f}")
            print(f"Total time: {time.time() - self.start_time:.2f}s")
            if save_video:
                print(f"Video saved to: {output_path}")
            print("="*60)

def main():
    """Main function to run live camera detection"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Real-time YOLO Object Detection with Camera')
    parser.add_argument('--weights', type=str, 
                       default='yolov5/runs/train/exp_model-n_img-640/weights/best_fixed.pt',
                       help='Path to model weights')
    parser.add_argument('--camera', type=int, default=0, 
                       help='Camera device ID (0 for default webcam)')
    parser.add_argument('--conf-thres', type=float, default=0.25, 
                       help='Confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, 
                       help='IOU threshold for NMS')
    parser.add_argument('--img-size', type=int, default=640, 
                       help='Inference image size')
    parser.add_argument('--save-video', action='store_true', 
                       help='Save output video')
    parser.add_argument('--output', type=str, default='live_detection_output.mp4',
                       help='Output video path')
    
    args = parser.parse_args()
    
    # Initialize detector
    detector = LiveYOLODetector(
        weights=args.weights,
        conf_thres=args.conf_thres,
        iou_thres=args.iou_thres,
        img_size=args.img_size
    )
    
    # Run live detection
    detector.run_camera(
        camera_id=args.camera,
        save_video=args.save_video,
        output_path=args.output
    )

if __name__ == '__main__':
    main()
