import argparse
import cv2
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

parser = argparse.ArgumentParser()
parser.add_argument("image", help="Path to shelf image")
args = parser.parse_args()

IMAGE_PATH = Path(args.image).resolve()
OUTPUT_PATH = SCRIPT_DIR / "slot_calibration.json"

SLOT_NAMES = ["Slot 1", "Slot 2", "Slot 3"]
points = []

image = cv2.imread(str(IMAGE_PATH))

if image is None:
    raise FileNotFoundError(f"Could not load image: {IMAGE_PATH}")

height, width = image.shape[:2]
print(f"Image dimensions: {width}x{height}")


def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 3:
            points.append((x, y))
            print(f"{SLOT_NAMES[len(points)-1]}: ({x}, {y})")
        else:
            print("All slots selected. Press R to reset.")


cv2.namedWindow("Shelf Slot Calibration", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("Shelf Slot Calibration", mouse_callback)

while True:
    display = image.copy()

    for i, point in enumerate(points):
        cv2.circle(display, point, 7, (0, 255, 0), -1)
        cv2.putText(
            display, SLOT_NAMES[i],
            (point[0] + 12, point[1] - 12),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
        )

    cv2.putText(
        display,
        "Click Slot 1 -> Slot 2 -> Slot 3 | R: Reset | Q: Save",
        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2
    )

    cv2.imshow("Shelf Slot Calibration", display)
    key = cv2.waitKey(0) & 0xFF

    if key == ord("r"):
        points.clear()
        print("Selections reset.")
    elif key == ord("q"):
        break

cv2.destroyAllWindows()

if len(points) == 3:
    calibration = {
        "image_width": width,
        "image_height": height,
        "slots": {
            f"slot_{i+1}": {"x": p[0], "y": p[1]}
            for i, p in enumerate(points)
        }
    }

    OUTPUT_PATH.write_text(json.dumps(calibration, indent=4))
    print(f"Calibration saved to: {OUTPUT_PATH}")
else:
    print("Calibration cancelled. Three points are required.")
