
from pathlib import Path
from multiprocessing import freeze_support
import csv

from ultralytics import YOLO

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
VISION_DIR = PROJECT_ROOT / 'vision'
DATASETS_DIR = VISION_DIR / 'datasets'
MODELS_DIR = VISION_DIR / 'models'
EVALUATION_DIR = VISION_DIR / 'evaluation'
ROOT = VISION_DIR

# Independent real-world test dataset
DATASET = DATASETS_DIR / "grocery-real-world-test.yolov8" / "data.yaml"

# All four trained models
MODELS = {
    "yolov8n_before": MODELS_DIR / "new-models/yolov8n_negatives.pt",

    "yolo11n_before": MODELS_DIR / "new-models/yolo11n_negatives.pt",

    "yolov8n_after": EVALUATION_DIR / "runs/detect/results/yolov8n_custom_finetune-3/weights/best.pt",

    "yolo11n_after": EVALUATION_DIR / "runs/detect/results/yolo11n_custom_finetune/weights/best.pt"
}

# Evaluation settings
IMAGE_SIZE = 640
BATCH = 16
DEVICE = 0

# Results folder
OUTPUT = ROOT / "results" / "real_world_comparison"

CLASSES = ["Candi", "Prince", "Sooper"]


def main():

    if not DATASET.exists():
        raise FileNotFoundError(f"Dataset not found: {DATASET}")

    for name, weights in MODELS.items():
        if not weights.exists():
            raise FileNotFoundError(f"Model not found: {weights}")

    OUTPUT.mkdir(parents=True, exist_ok=True)

    results = []

    for name, weights in MODELS.items():

        print(f"\nEvaluating: {name}")

        # Load model
        model = YOLO(str(weights))

        # Evaluate on the same 60 test images
        metrics = model.val(
            data=str(DATASET),
            split="test",
            imgsz=IMAGE_SIZE,
            batch=BATCH,
            device=DEVICE,
            workers=0,
            conf=0.001,
            iou=0.7,
            plots=True,
            project=str(OUTPUT),
            name=name,
            exist_ok=True
        )

        # Extract metrics
        precision = metrics.box.mp
        recall = metrics.box.mr
        map50 = metrics.box.map50
        map5095 = metrics.box.map

        # Save overall results
        results.append({
            "Model": name,
            "Precision": round(precision, 4),
            "Recall": round(recall, 4),
            "mAP50": round(map50, 4),
            "mAP50-95": round(map5095, 4)
        })

        print(f"\n{name} results:")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"mAP50: {map50:.4f}")
        print(f"mAP50-95: {map5095:.4f}")

        # Per-class results
        print("\nPer-class mAP50-95:")

        for class_id, class_name in enumerate(CLASSES):
            print(
                f"{class_name}: "
                f"{metrics.box.maps[class_id]:.4f}"
            )

    # Save comparison as CSV
    csv_path = OUTPUT / "comparison.csv"

    with open(csv_path, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "Model",
                "Precision",
                "Recall",
                "mAP50",
                "mAP50-95"
            ]
        )

        writer.writeheader()
        writer.writerows(results)

    # Display final comparison
    print("\n========== FINAL COMPARISON ==========")

    for result in results:
        print(
            f"{result['Model']}: "
            f"P={result['Precision']}, "
            f"R={result['Recall']}, "
            f"mAP50={result['mAP50']}, "
            f"mAP50-95={result['mAP50-95']}"
        )

    print(f"\nComparison saved to: {csv_path}")


if __name__ == "__main__":
    freeze_support()
    main()
