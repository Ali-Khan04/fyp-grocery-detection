
from pathlib import Path
import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
VISION_DIR = PROJECT_ROOT / 'vision'
DATASETS_DIR = VISION_DIR / 'datasets'
MODELS_DIR = VISION_DIR / 'models'
EVALUATION_DIR = VISION_DIR / 'evaluation'
ROOT = VISION_DIR

# Our 60 difficult test images
IMAGE_DIR = ROOT / "grocery-real-world-test.yolov8/train/images"

# Previous and newly fine-tuned models
MODEL_PATHS = {
    "YOLOv8n - Before": MODELS_DIR / "new-models/yolov8n_negatives.pt",

    "YOLOv8n - After": EVALUATION_DIR / "runs/detect/results/yolov8n_custom_finetune-3/weights/best.pt",

    "YOLO11n - Before": MODELS_DIR / "new-models/yolo11n_negatives.pt",

    "YOLO11n - After": EVALUATION_DIR / "runs/detect/results/yolo11n_custom_finetune/weights/best.pt"
}

CONF = 0.25
IMAGE_SIZE = 640

# Load models
models = {}

for name, path in MODEL_PATHS.items():
    print(f"Loading {name}...")
    models[name] = YOLO(str(path))

# Get all test images
extensions = {".jpg", ".jpeg", ".png", ".webp"}

images = sorted([
    p for p in IMAGE_DIR.iterdir()
    if p.suffix.lower() in extensions
])

if not images:
    raise FileNotFoundError("No test images found!")

print(f"\nFound {len(images)} test images")

# Current image index
index = 0

# Create Matplotlib window
fig, axes = plt.subplots(2, 2, figsize=(16, 9))
axes = axes.flatten()


def show_image():
    global index

    image_path = images[index]

    print(f"\nShowing {index + 1}/{len(images)}: {image_path.name}")

    for ax, (name, model) in zip(axes, models.items()):

        # Run prediction
        result = model.predict(
            source=str(image_path),
            imgsz=IMAGE_SIZE,
            conf=CONF,
            device=0,
            verbose=False
        )[0]

        # Draw bounding boxes
        predicted_image = result.plot()

        # Convert BGR to RGB
        predicted_image = cv2.cvtColor(
            predicted_image,
            cv2.COLOR_BGR2RGB
        )

        ax.clear()
        ax.imshow(predicted_image)
        ax.set_title(
            f"{name} | Detections: {len(result.boxes)}",
            fontsize=12
        )
        ax.axis("off")

    fig.suptitle(
        f"Real-World Test {index + 1}/{len(images)}\n"
        f"{image_path.name}",
        fontsize=14
    )

    fig.tight_layout(rect=[0, 0.04, 1, 0.94])
    fig.canvas.draw_idle()


# Keyboard controls
def on_key(event):
    global index

    if event.key == "right":
        index = (index + 1) % len(images)
        show_image()

    elif event.key == "left":
        index = (index - 1) % len(images)
        show_image()

    elif event.key in ["q", "escape"]:
        plt.close(fig)


fig.canvas.mpl_connect("key_press_event", on_key)

fig.text(
    0.5, 0.015,
    "Right Arrow: Next  |  Left Arrow: Previous  |  Q: Quit",
    ha="center",
    fontsize=11
)

# Display first image
show_image()

# Open Matplotlib window
plt.show()
