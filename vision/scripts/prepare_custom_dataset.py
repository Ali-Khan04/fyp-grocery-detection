
from pathlib import Path
from collections import Counter, defaultdict
import hashlib
import math
import random
import shutil
import yaml

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
VISION_DIR = PROJECT_ROOT / 'vision'
DATASETS_DIR = VISION_DIR / 'datasets'
MODELS_DIR = VISION_DIR / 'models'
EVALUATION_DIR = VISION_DIR / 'evaluation'
ROOT = VISION_DIR

# Original Roboflow dataset
SOURCE = DATASETS_DIR / "FYP-Pakistani-Buiscuits.v1-best_dataset_v1_443images_original_noaugmentation.yolov8"

# New prepared dataset
OUTPUT = DATASETS_DIR / "custom_biscuit_dataset"

# Separate real-world test dataset
TEST = DATASETS_DIR / "grocery-real-world-test.yolov8"

CLASSES = ["Candi", "Prince", "Sooper"]

VAL_RATIO = 0.15
SEED = 42

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

source_images = SOURCE / "train" / "images"
source_labels = SOURCE / "train" / "labels"


# Convert YOLO segmentation polygons into bounding boxes
def convert_label(line):
    parts = line.split()

    class_id = int(parts[0])
    values = [float(v) for v in parts[1:]]

    if class_id not in range(len(CLASSES)):
        raise ValueError(f"Invalid class ID: {class_id}")

    # Normal YOLO bounding box
    if len(values) == 4:
        x, y, w, h = values

    # Segmentation polygon
    elif len(values) >= 6 and len(values) % 2 == 0:
        xs = values[::2]
        ys = values[1::2]

        x_min = min(xs)
        x_max = max(xs)
        y_min = min(ys)
        y_max = max(ys)

        x = (x_min + x_max) / 2
        y = (y_min + y_max) / 2
        w = x_max - x_min
        h = y_max - y_min

    else:
        raise ValueError("Invalid YOLO annotation format")

    # Validate normalized coordinates
    if not all(0 <= v <= 1 for v in [x, y, w, h]):
        raise ValueError("Coordinates must be between 0 and 1")

    if w <= 0 or h <= 0:
        raise ValueError("Bounding box must have positive size")

    if x - w / 2 < -1e-6 or x + w / 2 > 1 + 1e-6:
        raise ValueError("Bounding box exceeds image width")

    if y - h / 2 < -1e-6 or y + h / 2 > 1 + 1e-6:
        raise ValueError("Bounding box exceeds image height")

    return f"{class_id} {x:.10f} {y:.10f} {w:.10f} {h:.10f}"


# Calculate image hash for duplicate checking
def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


# Check folders
if not source_images.exists() or not source_labels.exists():
    raise FileNotFoundError("Source dataset folders not found")

if OUTPUT.exists():
    raise FileExistsError(
        "custom_biscuit_dataset already exists. "
        "Check it before deleting or replacing it."
    )


# Find images
images = sorted(
    p for p in source_images.iterdir()
    if p.suffix.lower() in IMAGE_EXTENSIONS
)

print(f"Source images: {len(images)}")

groups = defaultdict(list)
polygon_count = 0
box_count = 0

# Validate and convert all annotations in memory
for image in images:
    label = source_labels / f"{image.stem}.txt"

    if not label.exists():
        raise FileNotFoundError(f"Missing label: {image.name}")

    converted_lines = []

    for line in label.read_text().splitlines():
        if not line.strip():
            continue

        try:
            converted = convert_label(line)
        except (ValueError, IndexError) as error:
            raise ValueError(
                f"Problem in {label.name}: {error}"
            ) from error

        converted_lines.append(converted)

        if len(line.split()) == 5:
            box_count += 1
        else:
            polygon_count += 1

    # Keep identical images in the same split
    groups[file_hash(image)].append(
        (image, label, converted_lines)
    )

print(f"Bounding boxes: {box_count}")
print(f"Polygons converted: {polygon_count}")


# Check for duplicate images in independent test set
test_images = [
    p for p in TEST.rglob("*")
    if p.is_file()
    and p.parent.name == "images"
    and p.suffix.lower() in IMAGE_EXTENSIONS
]

test_hashes = {file_hash(p) for p in test_images}

overlaps = set(groups.keys()) & test_hashes

print(f"Independent test images found: {len(test_images)}")
print(f"Exact test overlaps: {len(overlaps)}")

if overlaps:
    raise ValueError(
        "Some training images also exist in the test dataset!"
    )


# Split into training and validation
image_groups = list(groups.values())

random.Random(SEED).shuffle(image_groups)

target_val = math.ceil(len(images) * VAL_RATIO)

train = []
valid = []

for group in image_groups:
    if len(valid) < target_val:
        valid.extend(group)
    else:
        train.extend(group)


# Copy images and converted labels
for split_name, pairs in [
    ("train", train),
    ("valid", valid)
]:
    image_dir = OUTPUT / split_name / "images"
    label_dir = OUTPUT / split_name / "labels"

    image_dir.mkdir(parents=True, exist_ok=True)
    label_dir.mkdir(parents=True, exist_ok=True)

    for image, label, converted_lines in pairs:
        shutil.copy2(image, image_dir / image.name)

        (label_dir / label.name).write_text(
            "\n".join(converted_lines) +
            ("\n" if converted_lines else "")
        )


# Generate data.yaml
data = {
    "path": OUTPUT.resolve().as_posix(),
    "train": "train/images",
    "val": "valid/images",
    "nc": 3,
    "names": CLASSES
}

with open(OUTPUT / "data.yaml", "w") as f:
    yaml.safe_dump(data, f, sort_keys=False)


# Count images containing each class
def class_counts(pairs):
    counts = Counter()

    for image, label, converted_lines in pairs:
        class_ids = {
            int(line.split()[0])
            for line in converted_lines
        }

        counts.update(class_ids)

    return counts


train_counts = class_counts(train)
valid_counts = class_counts(valid)


# Final summary
print("\nDataset prepared successfully!")

print(f"Training images: {len(train)}")
print(f"Validation images: {len(valid)}")
print(f"Total images: {len(train) + len(valid)}")

print("\nClass distribution:")

for class_id, name in enumerate(CLASSES):
    print(
        f"{name}: "
        f"Train={train_counts[class_id]}, "
        f"Valid={valid_counts[class_id]}"
    )

    if train_counts[class_id] == 0 or valid_counts[class_id] == 0:
        print(f"WARNING: {name} is missing from a split!")

print(f"\nSaved to: {OUTPUT}")
