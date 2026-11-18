
from pathlib import Path
import hashlib
import shutil
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VISION_DIR = PROJECT_ROOT / 'vision'
DATASETS_DIR = VISION_DIR / 'datasets'
MODELS_DIR = VISION_DIR / 'models'
EVALUATION_DIR = VISION_DIR / 'evaluation'
ROOT = VISION_DIR

# Already prepared custom biscuit dataset
POSITIVE = DATASETS_DIR / "custom_biscuit_dataset"

# Existing dataset containing negative images
NEGATIVE = DATASETS_DIR / "filtered_dataset_with_negatives"

# Our difficult real-world evaluation dataset
TEST = DATASETS_DIR / "grocery-real-world-test.yolov8"

# New dataset
OUTPUT = DATASETS_DIR / "custom_biscuit_with_negatives"

CLASSES = ["Candi", "Prince", "Sooper"]
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def get_images(folder):
    return sorted(
        p for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in EXTENSIONS
    )


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def get_label(image, dataset, split):
    label = dataset / split / "labels" / f"{image.stem}.txt"

    if not label.exists():
        raise FileNotFoundError(f"Missing label: {image.name}")

    return label


def copy_pair(image, label, split):
    images_out = OUTPUT / split / "images"
    labels_out = OUTPUT / split / "labels"

    images_out.mkdir(parents=True, exist_ok=True)
    labels_out.mkdir(parents=True, exist_ok=True)

    destination = images_out / image.name

    if destination.exists():
        raise FileExistsError(f"Duplicate filename: {image.name}")

    shutil.copy2(image, destination)
    shutil.copy2(label, labels_out / label.name)


def main():
    if OUTPUT.exists():
        raise FileExistsError(
            "custom_biscuit_with_negatives already exists. "
            "Check it before rerunning."
        )

    # Find our original positive images
    train_images = get_images(POSITIVE / "train" / "images")
    valid_images = get_images(POSITIVE / "valid" / "images")

    # Find independent real-world test images
    test_images = [
        p for p in TEST.rglob("*")
        if p.is_file()
        and p.parent.name == "images"
        and p.suffix.lower() in EXTENSIONS
    ]

    train_hashes = {file_hash(p) for p in train_images}
    valid_hashes = {file_hash(p) for p in valid_images}
    test_hashes = {file_hash(p) for p in test_images}

    # Check for dataset leakage
    if train_hashes & valid_hashes:
        raise ValueError("Training and validation images overlap!")

    if (train_hashes | valid_hashes) & test_hashes:
        raise ValueError("Images overlap with the real-world test set!")

    # Copy custom positive training images
    for image in train_images:
        label = get_label(image, POSITIVE, "train")
        copy_pair(image, label, "train")

    # Keep the original validation split unchanged
    for image in valid_images:
        label = get_label(image, POSITIVE, "valid")
        copy_pair(image, label, "valid")

    print(f"Positive training images: {len(train_images)}")
    print(f"Positive validation images: {len(valid_images)}")

    # Load negative/background images
    negative_images = get_images(NEGATIVE / "train" / "images")

    grocery_added = 0
    person_added = 0
    skipped = 0

    used_hashes = train_hashes | valid_hashes | test_hashes

    for image in negative_images:

        # Only include explicitly added negative images
        if image.stem.startswith("grocery_negative_"):
            category = "grocery"

        elif image.stem.startswith("person_negative_"):
            category = "person"

        else:
            continue

        label = get_label(image, NEGATIVE, "train")

        # Negative images must have empty labels
        if label.read_text().strip():
            raise ValueError(
                f"Negative image has nonempty labels: {image.name}"
            )

        image_hash = file_hash(image)

        # Prevent exact duplicate images across splits
        if image_hash in used_hashes:
            skipped += 1
            print(f"Skipping duplicate: {image.name}")
            continue

        copy_pair(image, label, "train")
        used_hashes.add(image_hash)

        if category == "grocery":
            grocery_added += 1
        else:
            person_added += 1

    # Generate Ultralytics data.yaml
    data = {
        "path": OUTPUT.resolve().as_posix(),
        "train": "train/images",
        "val": "valid/images",
        "nc": 3,
        "names": CLASSES
    }

    with open(OUTPUT / "data.yaml", "w") as f:
        yaml.safe_dump(data, f, sort_keys=False)

    # Final summary
    print("\n===== NEW DATASET SUMMARY =====")
    print(f"Positive training images: {len(train_images)}")
    print(f"Grocery negatives: {grocery_added}")
    print(f"Person/background negatives: {person_added}")
    print(f"Duplicates skipped: {skipped}")

    total_train = (
        len(train_images) + grocery_added + person_added
    )

    print(f"\nTotal training images: {total_train}")
    print(f"Validation images: {len(valid_images)}")
    print(f"Independent real-world test images: {len(test_images)}")
    print(f"\nSaved to: {OUTPUT}")


if __name__ == "__main__":
    main()
