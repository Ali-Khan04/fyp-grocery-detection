
from pathlib import Path
from multiprocessing import freeze_support
from ultralytics import YOLO

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
VISION_DIR = PROJECT_ROOT / 'vision'
DATASETS_DIR = VISION_DIR / 'datasets'
MODELS_DIR = VISION_DIR / 'models'
EVALUATION_DIR = VISION_DIR / 'evaluation'
ROOT = VISION_DIR

# Dataset containing biscuits + negative images
DATASET = DATASETS_DIR / "custom_biscuit_with_negatives" / "data.yaml"

# Previously fine-tuned models
MODELS = {
    "yolov8n": EVALUATION_DIR / "runs/detect/results/yolov8n_custom_finetune-3/weights/best.pt",

    "yolo11n": EVALUATION_DIR / "runs/detect/results/yolo11n_custom_finetune/weights/best.pt"
}

# Training settings
EPOCHS = 50
BATCH = 16
IMAGE_SIZE = 640
DEVICE = 0
SEED = 42

# Results folder
RESULTS = EVALUATION_DIR / "runs/detect/results"


def main():

    if not DATASET.exists():
        raise FileNotFoundError(f"Dataset not found: {DATASET}")

    for name, weights in MODELS.items():

        if not weights.exists():
            raise FileNotFoundError(f"Model not found: {weights}")

        print(f"\nStarting fine-tuning: {name}")
        print(f"Starting weights: {weights.name}")

        # Load previously fine-tuned model
        model = YOLO(str(weights))

        # Fine-tune using biscuits + negative images
        model.train(
            data=str(DATASET),
            epochs=EPOCHS,
            imgsz=IMAGE_SIZE,
            batch=BATCH,
            device=DEVICE,
            seed=SEED,
            deterministic=True,
            patience=15,
            optimizer="AdamW",
            lr0=0.0003,
            workers=2,
            plots=True,
            project=str(RESULTS),
            name=f"{name}_custom_with_negatives",
            exist_ok=False
        )

        print(f"\n{name} fine-tuning completed!")
        print(f"Results saved in: {model.trainer.save_dir}")

    print("\nBoth models finished fine-tuning!")


# Required for Windows multiprocessing
if __name__ == "__main__":
    freeze_support()
    main()
