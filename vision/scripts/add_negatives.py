from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
VISION_DIR = PROJECT_ROOT / 'vision'
DATASETS_DIR = VISION_DIR / 'datasets'
MODELS_DIR = VISION_DIR / 'models'
EVALUATION_DIR = VISION_DIR / 'evaluation'
import shutil
import random


# our main dataset with 3 target classes
BASE_DATASET = DATASETS_DIR / "filtered_dataset"

# Original roboflow dataset with 25 classes
ORIGINAL_DATASET = Path(
    DATASETS_DIR / "dataset" / "Grocery Dataset.v4-raw-images.yolov8"
)

# negative images dataset of people and backgrounds
PERSON_NEGATIVES = Path(str(DATASETS_DIR / "person_nagtaive_background" / "images"))

# New improved dataset
OUTPUT = DATASETS_DIR / "filtered_dataset_with_negatives"

TARGET_CLASSES = {
    9,   # Candi
    11,  # Prince
    17   # Sooper
}
random.seed(42)

if OUTPUT.exists():
    shutil.rmtree(OUTPUT)

shutil.copytree(BASE_DATASET, OUTPUT)

print("Copied existing filtered dataset.")



#helper function to find image with its label file in the original dataset
def find_image(folder, stem):

    for ext in [
        ".jpg",
        ".jpeg",
        ".png",
        ".JPG",
        ".JPEG",
        ".PNG"
    ]:

        image = folder / f"{stem}{ext}"

        if image.exists():
            return image

    return None


# Add non-target grocery negatives


source_images = ORIGINAL_DATASET / "train" / "images"
source_labels = ORIGINAL_DATASET / "train" / "labels"

output_images = OUTPUT / "train" / "images"
output_labels = OUTPUT / "train" / "labels"

grocery_negatives = []


for label_file in source_labels.glob("*.txt"):

    contains_target = False

    with open(label_file, "r") as file:

        for line in file:

            parts = line.strip().split()

            if not parts:
                continue

            class_id = int(parts[0])

            if class_id in TARGET_CLASSES:
                contains_target = True
                break


    # Keep only images containing none of our target biscuits
    if not contains_target:

        image = find_image(
            source_images,
            label_file.stem
        )

        if image:
            grocery_negatives.append(image)


random.shuffle(grocery_negatives)

selected_grocery = grocery_negatives[:300]


for index, image in enumerate(selected_grocery):

    stem = f"grocery_negative_{index:04d}"

    destination_image = (
        output_images / f"{stem}{image.suffix.lower()}"
    )

    destination_label = (
        output_labels / f"{stem}.txt"
    )

    shutil.copy2(
        image,
        destination_image
    )

    # Empty YOLO label
    destination_label.touch()


print(
    f"Added {len(selected_grocery)} "
    f"non-target grocery images."
)


# Add all person/background negatives

person_images = [
    path
    for path in PERSON_NEGATIVES.iterdir()
    if path.suffix.lower()
    in [".jpg", ".jpeg", ".png"]
]


for index, image in enumerate(person_images):

    stem = f"person_negative_{index:04d}"

    destination_image = (
        output_images / f"{stem}{image.suffix.lower()}"
    )

    destination_label = (
        output_labels / f"{stem}.txt"
    )

    shutil.copy2(
        image,
        destination_image
    )

    # Empty label:
    # no Candi / Prince / Sooper present
    destination_label.touch()


print(
    f"Added {len(person_images)} "
    f"person/background negatives."
)



# Summary
original_train_count = len(
    list((BASE_DATASET / "train" / "images").iterdir())
)

new_train_count = len(
    list((OUTPUT / "train" / "images").iterdir())
)


print("\nDone!")

print(f"Original training images: {original_train_count}")

print(
    f"Grocery negatives added: "
    f"{len(selected_grocery)}"
)

print(
    f"Person negatives added: "
    f"{len(person_images)}"
)

print(f"New training total: {new_train_count}")

print(
    "\nNew dataset created at:"
    "\nfiltered_dataset_with_negatives/"
)