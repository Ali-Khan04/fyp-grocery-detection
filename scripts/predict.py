from ultralytics import YOLO
import matplotlib.pyplot as plt
from pathlib import Path

# Load trained YOLOv8n model
model = YOLO("runs/detect/results/yolov8n/weights/best.pt")

# Cleaner class names
model.model.names = {
    0: "Candi",
    1: "Prince",
    2: "Sooper"
}

# Run prediction on all images inside unlabeled
results = model.predict(
    source="unlabeled",
    imgsz=640,
    conf=0.25,
    device=0,
    save=False,
    save_txt=False,
)

# Display predictions one-by-one
for result in results:

    # YOLO returns annotated image in BGR
    annotated_image = result.plot()

    # Convert BGR -> RGB for matplotlib
    annotated_image = annotated_image[:, :, ::-1]

    plt.figure(figsize=(10, 7))
    plt.imshow(annotated_image)
    plt.axis("off")

    # Show image filename as title
    plt.title(Path(result.path).name)

    plt.tight_layout()
    plt.show()