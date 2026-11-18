from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VISION_DIR = PROJECT_ROOT / 'vision'
DATASETS_DIR = VISION_DIR / 'datasets'
MODELS_DIR = VISION_DIR / 'models'
EVALUATION_DIR = VISION_DIR / 'evaluation'
import shutil
import yaml

# Original dataset
SOURCE = DATASETS_DIR / "dataset" / "Grocery Dataset.v4-raw-images.yolov8"

# New filtered dataset for our 3 target classes
OUTPUT = DATASETS_DIR / "filtered_dataset"

# old class ID -> new class ID
CLASS_MAP = {
    9: 0,    # Candi
    11: 1,   # Prince
    17: 2    # Sooper
}

SPLITS = ["train", "valid", "test"]

for split in SPLITS:

    src_images = SOURCE / split / "images"
    src_labels = SOURCE / split / "labels"

    out_images = OUTPUT / split / "images"
    out_labels = OUTPUT / split / "labels"

    out_images.mkdir(parents=True, exist_ok=True)
    out_labels.mkdir(parents=True, exist_ok=True)

    kept_images = 0

    for label_file in src_labels.glob("*.txt"):

        new_labels = []

        with open(label_file, "r") as f:
            lines = f.readlines()

        for line in lines:

            parts = line.strip().split()

            if not parts:
                continue

            old_class = int(parts[0])

            if old_class in CLASS_MAP:

                new_class = CLASS_MAP[old_class]

                parts[0] = str(new_class)

                new_labels.append(" ".join(parts))

        # Only keep images containing one of our 3 products
        if new_labels:

            # Find matching image
            image_file = None

            for ext in [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]:
                candidate = src_images / (label_file.stem + ext)

                if candidate.exists():
                    image_file = candidate
                    break

            if image_file:

                shutil.copy2(
                    image_file,
                    out_images / image_file.name
                )

                with open(out_labels / label_file.name, "w") as f:
                    f.write("\n".join(new_labels))

                kept_images += 1

    print(f"{split}: {kept_images} images")

# Create new data.yaml
data = {
    "train": "train/images",
    "val": "valid/images",
    "test": "test/images",
    "nc": 3,
    "names": [
        "LU Candi Biscuit 60gm",
        "LU Prince Biscuit 55.2gm",
        "Peek Freans Sooper Biscuit 13.2gm"
    ]
}

with open(OUTPUT / "data.yaml", "w") as f:
    yaml.dump(data, f, sort_keys=False)

print("\nDone!")
print("Filtered dataset created in: filtered_dataset/")