
from pathlib import Path
from collections import Counter

DATASET = Path(
    "FYP-Pakistani-Buiscuits.v1-best_dataset_v1_443images_original_noaugmentation.yolov8"
)

label_dir = DATASET / "train" / "labels"

counts = Counter()
invalid_files = []

for file in label_dir.glob("*.txt"):
    for line_number, line in enumerate(file.read_text().splitlines(), 1):
        parts = line.split()

        if not parts:
            continue

        try:
            values = [float(value) for value in parts]

            if len(values) == 5:
                counts["Bounding boxes"] += 1

            elif len(values) >= 7 and len(values) % 2 == 1:
                counts["Segmentation polygons"] += 1

            else:
                counts["Invalid annotations"] += 1
                invalid_files.append(file.name)

        except ValueError:
            counts["Invalid annotations"] += 1
            invalid_files.append(file.name)

print("Annotation Summary")
print("------------------")

print("Total label files:", len(list(label_dir.glob("*.txt"))))

for name, count in counts.items():
    print(f"{name}: {count}")

print("\nInvalid files:")

for name in sorted(set(invalid_files)):
    print(name)
