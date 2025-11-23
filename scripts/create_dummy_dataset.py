import os
import random
from pathlib import Path

from PIL import Image, ImageDraw


DATASET_ROOT = Path(__file__).resolve().parent.parent / "dataset"
IMAGE_SIZE = (640, 512)  # width, height
CLASSES = [
    "person",
    "bike",
    "car",
    "motor",
    "bus",
    "train",
    "truck",
    "scooter",
    "other_vehicle",
]
SPLITS = {"train": 12, "val": 4}
MAX_OBJECTS_PER_IMAGE = 4
MIN_RECT_SIZE = 40
MAX_RECT_SIZE = 200


def ensure_dirs():
    for split in SPLITS:
        for sub in ("images", "labels"):
            path = DATASET_ROOT / sub / split
            path.mkdir(parents=True, exist_ok=True)


def random_bbox():
    width = random.randint(MIN_RECT_SIZE, MAX_RECT_SIZE)
    height = random.randint(MIN_RECT_SIZE, MAX_RECT_SIZE)
    max_x = IMAGE_SIZE[0] - width - 1
    max_y = IMAGE_SIZE[1] - height - 1
    x_min = random.randint(0, max_x)
    y_min = random.randint(0, max_y)
    x_max = x_min + width
    y_max = y_min + height
    return x_min, y_min, x_max, y_max


def to_yolo_format(x_min, y_min, x_max, y_max):
    img_w, img_h = IMAGE_SIZE
    x_center = ((x_min + x_max) / 2) / img_w
    y_center = ((y_min + y_max) / 2) / img_h
    width = (x_max - x_min) / img_w
    height = (y_max - y_min) / img_h
    return x_center, y_center, width, height


def draw_sample(image_path, label_path):
    img = Image.new("RGB", (IMAGE_SIZE[0], IMAGE_SIZE[1]), color=(20, 20, 20))
    draw = ImageDraw.Draw(img)
    n_objects = random.randint(1, MAX_OBJECTS_PER_IMAGE)
    label_lines = []
    for _ in range(n_objects):
        class_id = random.randint(0, len(CLASSES) - 1)
        x_min, y_min, x_max, y_max = random_bbox()
        color = tuple(random.randint(64, 255) for _ in range(3))
        draw.rectangle([x_min, y_min, x_max, y_max], outline=color, width=3)
        draw.text((x_min + 2, y_min + 2), CLASSES[class_id][:3], fill=color)
        x_center, y_center, width, height = to_yolo_format(x_min, y_min, x_max, y_max)
        label_lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

    img.save(image_path)
    with open(label_path, "w", encoding="utf-8") as f:
        f.write("\n".join(label_lines))


def main():
    ensure_dirs()
    for split, count in SPLITS.items():
        for idx in range(count):
            image_path = DATASET_ROOT / "images" / split / f"{split}_{idx:03d}.jpg"
            label_path = DATASET_ROOT / "labels" / split / f"{split}_{idx:03d}.txt"
            draw_sample(image_path, label_path)
    print(f"Created dummy dataset at {DATASET_ROOT}")


if __name__ == "__main__":
    random.seed(42)
    main()

