# ADAS Project Report: Object Detection & Alert System

## 1. Project Overview
This project is an **Advanced Driver Assistance System (ADAS)** prototype designed to detect vehicles and pedestrians in real-time using a camera feed. It uses the **YOLOv5** object detection model to identify objects and adds a custom layer of logic to estimate distance and trigger proximity alerts.

### Key Features
- **Real-time Object Detection**: Identifies cars, trucks, buses, and pedestrians.
- **Distance Estimation**: Calculates the approximate distance of detected vehicles using monocular vision techniques (bounding box width).
- **Proximity Alert**: Triggers a visual warning and captures an image when a vehicle is within **50 meters**.
- **Data Logging**: Stores alert details (timestamp, object type, distance, confidence) and the full alert image into a **MySQL database**.

---

## 2. System Architecture & File Interactions

The project consists of a main execution script, a database setup utility, and the core YOLOv5 inference engine.

### Core Files

#### 1. `run_live_camera.py` (The Main Controller)
This is the heart of the application. It orchestrates the entire flow:
- **Initialization**:
    - Loads the YOLOv5 model from `yolov5_official`.
    - Connects to the MySQL database (`car`).
    - Sets up the camera feed.
- **Processing Loop**:
    - Captures frames from the camera.
    - Sends frames to the YOLO model for detection.
    - Receives bounding boxes and class labels.
    - **Distance Logic**: Calculates distance based on the width of the bounding box.
    - **Alert Logic**: Checks if `distance < 50m`. If yes:
        - Draws a warning on the screen.
        - Saves the image to `captured_alerts/`.
        - Inserts a record (with image BLOB) into the MySQL database.
- **Output**: Displays the annotated video feed and saves it to `live_detection_output.mp4` if requested.

#### 2. `db_setup.py` (Database Utility)
This script is responsible for the infrastructure:
- **Database Creation**: Connects to MySQL and creates the `car` database if it doesn't exist.
- **Table Management**: Defines the schema for the `alerts` table.
- **Schema Updates**: If run, it will drop and recreate the table to ensure the schema (including the `LONGBLOB` column for images) is correct.

#### 3. `yolov5_official/` (Inference Engine)
This directory contains the standard YOLOv5 library code.
- `run_live_camera.py` imports modules from here (e.g., `models.common`, `utils.general`) to handle the complex deep learning inference tasks.
- It provides the `DetectMultiBackend` class used to load the `.pt` weights file.

#### 4. `requirements.txt`
Lists all Python dependencies required to run the project, including `torch`, `opencv-python`, and `mysql-connector-python`.

---

## 3. Data Flow

1.  **Input**: Webcam captures a raw frame.
2.  **Inference**: Frame -> `yolov5_official` -> Detections (Bounding Boxes).
3.  **Logic**:
    - `run_live_camera.py` calculates `Distance = (Known_Width * Focal_Length) / Pixel_Width`.
4.  **Decision**:
    - **IF** Distance < 50m:
        - **Action A**: Overlay "WARNING" text on frame.
        - **Action B**: Save frame to disk (`captured_alerts/`).
        - **Action C**: Encode frame to bytes -> Send INSERT query to MySQL (`car.alerts`).
5.  **Output**: Annotated frame is shown to the user.

## 4. Database Schema
**Database Name**: `car`
**Table**: `alerts`

| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | INT (PK) | Unique ID for the alert |
| `timestamp` | DATETIME | Time of the alert |
| `object_class` | VARCHAR | Type of object (e.g., 'car') |
| `confidence` | FLOAT | Detection confidence (0.0 - 1.0) |
| `distance` | FLOAT | Estimated distance in meters |
| `image_path` | VARCHAR | Local path to the saved image |
| `image_data` | LONGBLOB | Binary data of the captured image |

---

## 5. How to Run
1.  **Setup Database**: `python db_setup.py`
2.  **Run System**: `python run_live_camera.py`
