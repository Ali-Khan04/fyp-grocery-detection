import argparse
import cv2
import json
import math
from pathlib import Path
from ultralytics import YOLO

SCRIPT_DIR = Path(__file__).resolve().parent
VISION_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = VISION_DIR.parent

DEFAULT_MODEL = (
    VISION_DIR / "evaluation/runs/detect/runs/detect/results/"
    "yolo26n_custom_with_negatives/weights/best.pt"
)
CALIBRATION_PATH = SCRIPT_DIR / "slot_calibration.json"
OUTPUT_PATH = VISION_DIR / "evaluation/results/slot_detection_result.jpg"

parser = argparse.ArgumentParser()
parser.add_argument("image", help="Path to shelf image")
parser.add_argument("--model", default=str(DEFAULT_MODEL))
parser.add_argument("--confidence", type=float, default=0.25)
parser.add_argument("--max-distance", type=float, default=180)
args = parser.parse_args()

MODEL_PATH = Path(args.model)
IMAGE_PATH = Path(args.image).resolve()

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

if not CALIBRATION_PATH.exists():
    raise FileNotFoundError(f"Calibration not found: {CALIBRATION_PATH}")

with CALIBRATION_PATH.open() as file:
    calibration = json.load(file)

SLOT_CENTERS = {
    int(name.split("_")[1]): (data["x"], data["y"])
    for name, data in calibration["slots"].items()
}

model = YOLO(str(MODEL_PATH))
image = cv2.imread(str(IMAGE_PATH))

if image is None:
    raise FileNotFoundError(f"Could not load image: {IMAGE_PATH}")

height, width = image.shape[:2]

if (width, height) != (
    calibration["image_width"], calibration["image_height"]
):
    raise ValueError(
        f"Image is {width}x{height}, but calibration is "
        f"{calibration['image_width']}x{calibration['image_height']}. "
        "Use an image with the calibrated resolution or recalibrate."
    )

display = image.copy()
results = model.predict(
    source=image,
    imgsz=640,
    conf=args.confidence,
    verbose=False
)

detections = []
occupied_slots = {}

for result in results:
    for box in result.boxes:
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        confidence = float(box.conf[0])

        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        distances = {
            slot: math.dist((center_x, center_y), center)
            for slot, center in SLOT_CENTERS.items()
        }

        nearest_slot = min(distances, key=distances.get)
        nearest_distance = distances[nearest_slot]

        if nearest_distance > args.max_distance:
            slot = None
            status = "Outside slot"
        else:
            slot = nearest_slot
            status = "Assigned"

        detections.append({
            "class": class_name,
            "slot": slot,
            "confidence": round(confidence, 2),
            "center": [center_x, center_y],
            "distance": round(nearest_distance, 1),
            "status": status
        })

        if slot is not None:
            occupied_slots.setdefault(slot, []).append(class_name)

        cv2.rectangle(display, (x1, y1), (x2, y2), (0, 255, 0), 2)

        label = f"{class_name} {confidence:.2f}"
        label += f" | Slot {slot}" if slot is not None else " | Unassigned"

        cv2.putText(
            display, label, (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2
        )
        cv2.circle(display, (center_x, center_y), 5, (0, 0, 255), -1)

for slot, (x, y) in SLOT_CENTERS.items():
    cv2.circle(display, (x, y), 9, (255, 0, 0), 2)
    cv2.putText(
        display, f"Slot {slot}", (x + 10, y - 12),
        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2
    )

print("\nSLOT ASSIGNMENTS")
for slot in SLOT_CENTERS:
    products = occupied_slots.get(slot, [])
    if not products:
        print(f"Slot {slot}: EMPTY")
    elif len(products) == 1:
        print(f"Slot {slot}: {products[0]}")
    else:
        print(f"Slot {slot}: CONFLICT - {products}")

print("\nDETECTIONS")
print(json.dumps(detections, indent=4))

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
cv2.imwrite(str(OUTPUT_PATH), display)
print(f"\nSaved: {OUTPUT_PATH}")

cv2.imshow("YOLO Slot Detection", display)
cv2.waitKey(0)
cv2.destroyAllWindows()
