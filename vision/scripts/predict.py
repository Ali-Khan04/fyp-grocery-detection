from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VISION_DIR = PROJECT_ROOT / 'vision'
DATASETS_DIR = VISION_DIR / 'datasets'
MODELS_DIR = VISION_DIR / 'models'
EVALUATION_DIR = VISION_DIR / 'evaluation'
import random

import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO


# --------------------------------------------------
# Paths
# --------------------------------------------------

IMAGE_DIR = DATASETS_DIR / "grocery-real-world-test.yolov8" / "train" / "images"

YOLOV8_MODEL = str(MODELS_DIR / "new-models/yolov8n_negatives.pt")
YOLO11_MODEL = str(MODELS_DIR / "new-models/yolo11n_negatives.pt")


# --------------------------------------------------
# Load models
# --------------------------------------------------

print("Loading models...")

yolov8 = YOLO(YOLOV8_MODEL)
yolo11 = YOLO(YOLO11_MODEL)


# Use clean class names for display
class_names = {
    0: "Candi",
    1: "Prince",
    2: "Sooper",
}

yolov8.model.names = class_names
yolo11.model.names = class_names


# --------------------------------------------------
# Find images
# --------------------------------------------------

extensions = {".jpg", ".jpeg", ".png", ".webp"}

images = [
    image
    for image in IMAGE_DIR.iterdir()
    if image.is_file() and image.suffix.lower() in extensions
]

if not images:
    raise FileNotFoundError(f"No images found in {IMAGE_DIR}")


# Randomly select 10 difficult images
selected_images = random.sample(images, k=min(10, len(images)))

print(f"Showing {len(selected_images)} random difficult images...")


# --------------------------------------------------
# Predict and display
# --------------------------------------------------

for image_path in selected_images:

    result_v8 = yolov8.predict(
        source=str(image_path),
        imgsz=640,
        conf=0.25,
        verbose=False
    )[0]

    result_v11 = yolo11.predict(
        source=str(image_path),
        imgsz=640,
        conf=0.25,
        verbose=False
    )[0]


    # Ultralytics plot() returns BGR image
    image_v8 = result_v8.plot()
    image_v11 = result_v11.plot()

    # Convert BGR -> RGB for matplotlib
    image_v8 = cv2.cvtColor(image_v8, cv2.COLOR_BGR2RGB)
    image_v11 = cv2.cvtColor(image_v11, cv2.COLOR_BGR2RGB)


    # --------------------------------------------------
    # Display side-by-side
    # --------------------------------------------------

    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    axes[0].imshow(image_v8)
    axes[0].set_title("YOLOv8n")
    axes[0].axis("off")

    axes[1].imshow(image_v11)
    axes[1].set_title("YOLO11n")
    axes[1].axis("off")

    fig.suptitle(
        f"Difficult Real-World Test: {image_path.name}",
        fontsize=14
    )

    plt.tight_layout()
    plt.show()
    plt.close()