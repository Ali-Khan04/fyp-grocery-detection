from pathlib import Path
import shutil
import random



# our main dataset with 3 target classes
POSITIVE_DATASET = Path("filtered_dataset")

# Original 25-class Roboflow dataset
ORIGINAL_DATASET = Path(
    "dataset/Grocery Dataset.v4-raw-images.yolov8"
)

# New evaluation dataset
OUTPUT = Path("final_evaluation")

# Original class IDs
TARGET_CLASSES = {
    9,   # Candi
    11,  # Prince
    17   # Sooper
}

NEGATIVE_COUNT = 100

random.seed(42)


# Remove any old version if it exists
if OUTPUT.exists():
    shutil.rmtree(OUTPUT)

test_images_out = OUTPUT / "test" / "images"
test_labels_out = OUTPUT / "test" / "labels"

test_images_out.mkdir(parents=True)
test_labels_out.mkdir(parents=True)



# step 1: Copy existing 153 positive test images

positive_images = POSITIVE_DATASET / "test" / "images"
positive_labels = POSITIVE_DATASET / "test" / "labels"

positive_count = 0

for image in positive_images.iterdir():

    if image.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
        continue

    label = positive_labels / f"{image.stem}.txt"

    shutil.copy2(
        image,
        test_images_out / image.name
    )

    shutil.copy2(
        label,
        test_labels_out / label.name
    )

    positive_count += 1


print(f"Copied {positive_count} target-product test images.")


# step 2: Find unseen negative images
# from ORIGINAL TEST split

original_test_images = ORIGINAL_DATASET / "test" / "images"
original_test_labels = ORIGINAL_DATASET / "test" / "labels"

negative_candidates = []


for label_file in original_test_labels.glob("*.txt"):

    contains_target = False

    with open(label_file, "r") as f:

        for line in f:

            parts = line.strip().split()

            if not parts:
                continue

            class_id = int(parts[0])

            if class_id in TARGET_CLASSES:
                contains_target = True
                break


    # Image contains NONE of Candi / Prince / Sooper
    if not contains_target:

        for ext in [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]:

            image_file = (
                original_test_images /
                f"{label_file.stem}{ext}"
            )

            if image_file.exists():
                negative_candidates.append(image_file)
                break


print(
    f"Found {len(negative_candidates)} "
    f"unseen negative candidates."
)


# Select 100 negatives
random.shuffle(negative_candidates)

selected_negatives = negative_candidates[:NEGATIVE_COUNT]


for index, image in enumerate(selected_negatives):

    stem = f"negative_test_{index:04d}"

    new_image = (
        test_images_out /
        f"{stem}{image.suffix.lower()}"
    )

    new_label = (
        test_labels_out /
        f"{stem}.txt"
    )

    shutil.copy2(
        image,
        new_image
    )

    # Empty label 
    new_label.touch()


print(
    f"Added {len(selected_negatives)} "
    f"unseen negative test images."
)


# Create data.yaml
yaml_content = """test: test/images

nc: 3

names:
  0: Candi
  1: Prince
  2: Sooper
"""

with open(OUTPUT / "data.yaml", "w") as f:
    f.write(yaml_content)


print("\nFinal evaluation dataset created.")
print(f"Positive images: {positive_count}")
print(f"Negative images: {len(selected_negatives)}")
print(
    f"Total images: "
    f"{positive_count + len(selected_negatives)}"
)