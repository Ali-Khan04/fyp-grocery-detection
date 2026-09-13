# Grocery Item Detection Benchmark: YOLOv8n vs YOLO11n

Object detection and edge-deployment comparison of YOLOv8n and YOLO11n for an autonomous retail robot.

The project evaluates both models using Pakistani grocery products and compares:

- Detection accuracy
- Precision and recall
- Validation performance
- Held-out test performance
- Negative/background rejection
- Model complexity
- Raspberry Pi 5 inference latency
- Raspberry Pi 5 FPS
- PyTorch vs NCNN deployment performance

The final deployment target is a **Raspberry Pi 5 with 8 GB RAM**.

---

## Installation

Python 3.12+ is recommended.

### 1. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment.

#### Windows - Git Bash

```bash
source .venv/Scripts/activate
```

#### Windows - PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

#### Linux / Raspberry Pi

```bash
source .venv/bin/activate
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

The project uses a hardware-neutral `requirements.txt` so that the repository can run on CPU-only machines, NVIDIA GPU systems, and Raspberry Pi.

Recommended `requirements.txt`:

```txt
ultralytics==8.4.147
PyYAML>=6.0
matplotlib>=3.8
```

Ultralytics installs its required dependencies, including PyTorch, OpenCV, NumPy, Pillow, and related packages.

---

### Optional NVIDIA GPU Acceleration

The project can run entirely on CPU.

For systems with an NVIDIA GPU, install a CUDA-enabled version of PyTorch compatible with the installed NVIDIA driver and operating system.

After installing the appropriate CUDA-enabled PyTorch build, verify GPU availability:

```bash
python -c "import torch; print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

Example output:

```text
CUDA: True
GPU: NVIDIA GeForce RTX 4060
```

Training can then use:

```text
device=0
```

For CPU-only systems use:

```text
device=cpu
```

Example GPU training:

```bash
yolo detect train model=yolo11n.pt data=filtered_dataset/data.yaml epochs=100 imgsz=640 batch=16 device=0
```

Example CPU training:

```bash
yolo detect train model=yolo11n.pt data=filtered_dataset/data.yaml epochs=100 imgsz=640 batch=16 device=cpu
```

CPU training is supported but significantly slower.

---

### Raspberry Pi 5

On Raspberry Pi OS / Ubuntu:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The Raspberry Pi uses CPU inference.

For final deployment, the trained models are exported to **NCNN**, which provides significantly better ARM CPU performance than native PyTorch inference.

---

## Development Hardware

Training was performed locally using:

| Component | Configuration |
|---|---|
| GPU | NVIDIA GeForce RTX 4060 8 GB |
| Training Framework | Ultralytics |
| PyTorch | 2.14.0 |
| CUDA Runtime | CUDA 13.0 |
| Training Image Size | 640 x 640 |

Edge deployment benchmarking was performed on:

| Component | Configuration |
|---|---|
| Device | Raspberry Pi 5 |
| RAM | 8 GB |
| Inference Device | CPU |
| Optimized Backend | NCNN |

---

# Dataset

The original dataset was obtained from Roboflow Universe.

## Original Grocery Dataset

The source dataset contains approximately:

- 14,137 annotated images
- 25 grocery-product classes
- YOLO object-detection annotations

For the FYP-2 experiment, the dataset was filtered to three Pakistani grocery products.

| Class ID | Product |
|---:|---|
| 0 | LU Candi Biscuit |
| 1 | LU Prince Biscuit |
| 2 | Peek Freans Sooper Biscuit |

---

## Initial Filtered Dataset

| Split | Images |
|---|---:|
| Training | 1,139 |
| Validation | 334 |
| Testing | 153 |
| Total | 1,626 |

The exact same train, validation, and test splits were used for YOLOv8n and YOLO11n.

---

# Training Configuration

Both models were trained using identical settings.

| Parameter | Value |
|---|---|
| Epochs | 100 |
| Image Size | 640 x 640 |
| Batch Size | 16 |
| Random Seed | 42 |
| GPU | NVIDIA GeForce RTX 4060 |
| Task | Object Detection |
| Framework | Ultralytics |

Initial models:

- YOLOv8n
- YOLO11n

Both experiments started from the official pretrained model weights.

This means the models were **fine-tuned using transfer learning**, rather than trained completely from scratch.

---

# Accuracy, Validation and Testing

These terms represent different parts of the machine-learning evaluation process.

## Training

Training is where the model learns.

The model updates its internal weights using the:

```text
1,139 training images
```

---

## Validation

Validation evaluates the model while training is taking place.

The validation images are **not used to update model weights**.

They are used to:

- monitor generalization
- evaluate performance after epochs
- compare checkpoints
- select the best model

The validation set contained:

```text
334 images
```

Ultralytics automatically performs validation during training.

The best-performing checkpoint is saved as:

```text
best.pt
```

---

## Testing

Testing is the final evaluation performed after training has finished.

The test images are held out from training and are used to measure final model performance.

The original test set contained:

```text
153 images
```

---

# Detection Metrics

Object detection does not normally use a single classification-style accuracy value.

Instead, the main metrics are:

- Precision
- Recall
- mAP@0.50
- mAP@0.50:0.95

All values range approximately from:

```text
0.0 to 1.0
```

and can be converted to percentages.

For example:

```text
0.998 = 99.8%
```

---

## Precision

Precision measures how often a detection made by the model is correct.

High precision means the model produces few false detections.

Example:

```text
Precision = 0.998
```

corresponds to approximately:

```text
99.8%
```

---

## Recall

Recall measures how many actual target objects present in the dataset were successfully detected.

Example:

```text
Recall = 1.000
```

corresponds to:

```text
100%
```

---

## mAP@0.50

mAP@0.50 evaluates object detection using an Intersection over Union threshold of 0.50.

It measures both:

- correct object classification
- correct bounding-box localization

A prediction is considered sufficiently localized when its overlap with the ground-truth box reaches the required IoU threshold.

---

## mAP@0.50:0.95

mAP@0.50:0.95 is a stricter metric.

Performance is evaluated across multiple IoU thresholds:

```text
0.50
0.55
0.60
0.65
0.70
0.75
0.80
0.85
0.90
0.95
```

The results are averaged.

For this project, **mAP@0.50:0.95 is treated as the primary overall detection-performance metric**.

---

# Initial Validation Results

## YOLOv8n

| Metric | Result |
|---|---:|
| Precision | 0.999 |
| Recall | 1.000 |
| mAP@0.50 | 0.995 |
| mAP@0.50:0.95 | 0.898 |

Per-class mAP@0.50:0.95:

| Class | Result |
|---|---:|
| Candi | 0.903 |
| Prince | 0.851 |
| Sooper | 0.939 |

---

## YOLO11n

| Metric | Result |
|---|---:|
| Precision | 0.999 |
| Recall | 1.000 |
| mAP@0.50 | 0.995 |
| mAP@0.50:0.95 | 0.895 |

Per-class mAP@0.50:0.95:

| Class | Result |
|---|---:|
| Candi | 0.896 |
| Prince | 0.858 |
| Sooper | 0.932 |

---

# Initial Held-Out Test Results

The original held-out test set contained:

```text
153 images
```

## Overall Results

| Metric | YOLOv8n | YOLO11n |
|---|---:|---:|
| Precision | 0.998 | 0.998 |
| Recall | 1.000 | 1.000 |
| mAP@0.50 | 0.995 | 0.995 |
| mAP@0.50:0.95 | **0.899** | 0.890 |

## Per-Class mAP@0.50:0.95

| Class | YOLOv8n | YOLO11n |
|---|---:|---:|
| Candi | **0.891** | 0.872 |
| Prince | **0.851** | 0.849 |
| Sooper | **0.955** | 0.948 |

YOLOv8n achieved slightly higher initial test accuracy.

---

# Model Complexity

| Parameter | YOLOv8n | YOLO11n |
|---|---:|---:|
| Parameters | 3,006,233 | **2,582,737** |
| GFLOPs | 8.1 | **6.4** |

YOLO11n is smaller in both parameter count and computational complexity.

---

# Initial Raspberry Pi 5 PyTorch Benchmark

Both original `.pt` models were benchmarked on the same 153 images.

| Metric | YOLOv8n | YOLO11n |
|---|---:|---:|
| Average Inference | **530.88 ms** | 556.41 ms |
| Inference FPS | **1.88** | 1.80 |
| End-to-End FPS | **1.84** | 1.76 |
| Total Time | **83.16 s** | 86.89 s |

Native PyTorch inference was relatively slow on the Raspberry Pi CPU.

---

# Initial Raspberry Pi 5 NCNN Benchmark

Both models were exported to NCNN.

| Metric | YOLOv8n NCNN | YOLO11n NCNN |
|---|---:|---:|
| Preprocess | 9.73 ms | **9.39 ms** |
| Inference | 194.41 ms | **112.75 ms** |
| Postprocess | 1.94 ms | **1.64 ms** |
| Pipeline Latency | 206.09 ms | **123.77 ms** |
| Inference FPS | 5.14 | **8.87** |
| End-to-End FPS | 4.81 | **7.96** |
| Total Time | 31.82 s | **19.21 s** |

NCNN produced a major performance improvement over native PyTorch inference.

---

# Negative / Background Sample Experiment

Live-camera testing revealed occasional false-positive detections on non-target objects.

Examples included:

- people
- faces
- hands
- doors
- windows
- unrelated grocery items
- other objects in the environment

These false positives commonly appeared at significantly lower confidence than genuine biscuit detections.

The original filtered dataset contained substantial background information inside product images, but very few images where **none of the target classes were present**.

To improve background rejection, explicit negative samples were added.

---

## Negative Grocery Samples

The original 25-class grocery dataset was reused.

Images containing none of the three target classes were selected.

Target classes excluded from negative selection:

```text
Candi
Prince
Sooper
```

A total of:

```text
300 non-target grocery images
```

were added.

Each negative image was assigned an **empty YOLO label file**, indicating that none of the target objects were present.

These images included other grocery categories such as:

- drinks
- chips
- tea
- soap
- shampoo
- toothpaste
- other non-target products

---

## Person and Retail Background Samples

An additional:

```text
87 person / retail-background images
```

were added.

These included examples containing:

- people
- faces
- hands
- doors
- windows
- retail environments
- shelves
- non-target packaged products

These images also used empty YOLO labels.

The objective was not to detect people.

Instead, the desired model behavior was:

```text
Candi  -> detect
Prince -> detect
Sooper -> detect

Person -> background
Face   -> background
Hand   -> background
Other groceries -> background
Random objects  -> background
```

---

# Negative-Enhanced Training Dataset

The new training set contained:

| Category | Images |
|---|---:|
| Original target-product training images | 1,139 |
| Non-target grocery negatives | 300 |
| Person/background negatives | 87 |
| **Total training images** | **1,526** |

The original validation and test sets were retained.

Both YOLOv8n and YOLO11n were retrained starting from their original pretrained weights.

This produced:

```text
yolov8n_negatives
yolo11n_negatives
```

The previous trained models were preserved as experimental baselines.

---

# Final Mixed Evaluation Dataset

The original test set contained target products but no dedicated background-only images.

A new mixed evaluation dataset was therefore created.

It contained:

| Type | Images |
|---|---:|
| Target-product test images | 153 |
| Unseen negative/background images | 100 |
| **Total** | **253** |

The 100 negative images were selected from the original Roboflow test split and contained none of:

```text
Candi
Prince
Sooper
```

Their label files were empty.

This allows the evaluation to measure both:

1. whether the models correctly detect the target products
2. whether the models correctly ignore non-target objects

---

# Final Mixed Evaluation Results

## Overall Comparison

| Metric | YOLOv8n + Negatives | YOLO11n + Negatives |
|---|---:|---:|
| Precision | 0.998 | 0.998 |
| Recall | 1.000 | 1.000 |
| mAP@0.50 | 0.995 | 0.995 |
| mAP@0.50:0.95 | **0.892** | **0.892** |

Both models achieved essentially identical overall detection performance on the final mixed evaluation set.

---

## Per-Class mAP@0.50:0.95

| Class | YOLOv8n | YOLO11n |
|---|---:|---:|
| Candi | **0.887** | 0.879 |
| Prince | 0.845 | **0.848** |
| Sooper | 0.945 | **0.950** |

YOLOv8n performed slightly better on Candi.

YOLO11n performed slightly better on Prince and Sooper.

Overall performance remained effectively tied.

---

# Effect of Negative Samples

Qualitative live-camera testing showed a substantial reduction in false-positive detections after negative/background samples were introduced.

The models became better at ignoring:

- faces
- hands
- people
- unrelated objects
- non-target groceries

while retaining strong detection confidence for genuine target products.

The negative-sample experiment therefore improved the practical behavior of the detector without significantly reducing its target-product detection performance.

---

# Final Raspberry Pi 5 PyTorch Benchmark

The negative-trained models were benchmarked again using the same 153 test images.

| Metric | YOLOv8n PyTorch | YOLO11n PyTorch |
|---|---:|---:|
| Preprocess | 9.34 ms | **9.02 ms** |
| Inference | **546.67 ms** | 564.61 ms |
| Postprocess | 1.24 ms | 1.25 ms |
| Pipeline Latency | **557.25 ms** | 574.88 ms |
| Inference FPS | **1.83** | 1.77 |
| End-to-End FPS | **1.79** | 1.73 |
| Total Time | **85.52 s** | 88.23 s |

Native PyTorch inference remained too slow for ideal real-time edge deployment.

---

# Final Raspberry Pi 5 NCNN Benchmark

The negative-trained models were exported to NCNN and benchmarked again.

| Metric | YOLOv8n NCNN | YOLO11n NCNN |
|---|---:|---:|
| Preprocess | **7.93 ms** | 7.98 ms |
| Inference | 160.02 ms | **154.66 ms** |
| Postprocess | 1.41 ms | 1.41 ms |
| Pipeline Latency | 169.36 ms | **164.06 ms** |
| Inference FPS | 6.25 | **6.47** |
| End-to-End FPS | 5.84 | **6.03** |
| Total Time | 26.18 s | **25.36 s** |

The final NCNN models achieved very similar Raspberry Pi performance.

YOLO11n retained a small speed advantage.

---

# PyTorch vs NCNN

## YOLOv8n

| Backend | Inference | Inference FPS |
|---|---:|---:|
| PyTorch | 546.67 ms | 1.83 |
| NCNN | **160.02 ms** | **6.25** |

## YOLO11n

| Backend | Inference | Inference FPS |
|---|---:|---:|
| PyTorch | 564.61 ms | 1.77 |
| NCNN | **154.66 ms** | **6.47** |

NCNN substantially improved Raspberry Pi inference performance for both models.

---

# Final Engineering Comparison

| Category | YOLOv8n | YOLO11n |
|---|---:|---:|
| Precision | 99.8% | 99.8% |
| Recall | 100% | 100% |
| mAP@0.50 | 99.5% | 99.5% |
| mAP@0.50:0.95 | **89.2%** | **89.2%** |
| Parameters | 3.01 M | **2.58 M** |
| GFLOPs | 8.1 | **6.4** |
| Pi 5 NCNN Inference | 160.02 ms | **154.66 ms** |
| Pi 5 NCNN Inference FPS | 6.25 | **6.47** |
| Pi 5 NCNN End-to-End FPS | 5.84 | **6.03** |

The two models currently provide essentially equal quantitative detection accuracy.

YOLO11n is computationally smaller and slightly faster under the final NCNN benchmark.

YOLOv8n showed strong practical live-camera behavior during qualitative testing.

---

# Live Camera Inference

Example YOLOv8n NCNN command on Raspberry Pi:

```bash
yolo detect predict \
model="new-ncnn-models/yolov8n_negatives_ncnn_model" \
source=0 \
imgsz=640 \
conf=0.25 \
show=True
```

YOLO11n:

```bash
yolo detect predict \
model="new-ncnn-models/yolo11n_negatives_ncnn_model" \
source=0 \
imgsz=640 \
conf=0.25 \
show=True
```

If the USB camera is not index `0`, use:

```text
source=1
```

or the appropriate camera index.

---

# NCNN Export

YOLOv8n:

```bash
yolo export \
model="runs/detect/results/yolov8n_negatives/weights/best.pt" \
format=ncnn \
imgsz=640
```

YOLO11n:

```bash
yolo export \
model="runs/detect/results/yolo11n_negatives/weights/best.pt" \
format=ncnn \
imgsz=640
```

---

# Repository Structure

Generated datasets, model weights, benchmark output, virtual environments, and archives are excluded from Git.

The repository primarily contains the reproducible processing and evaluation pipeline.

```text
fyp-grocery-detection/
|
├── scripts/
│   ├── filter_dataset.py
│   ├── add_negatives.py
│   ├── create_final_evaluation.py
│   └── predict.py
|
├── requirements.txt
├── README.md
└── .gitignore
```

Large generated files such as:

```text
dataset/
filtered_dataset/
filtered_dataset_with_negatives/
final_evaluation/
runs/
results/
*.pt
*_ncnn_model/
```

are excluded from normal Git history.

---

# Evaluation Summary

| Evaluation Requirement | Status |
|---|---|
| Model training | Completed |
| Validation | Completed |
| Held-out testing | Completed |
| Precision measurement | Completed |
| Recall measurement | Completed |
| mAP@0.50 | Completed |
| mAP@0.50:0.95 | Completed |
| Per-class evaluation | Completed |
| Background/negative evaluation | Completed |
| Live-camera inference | Completed |
| Raspberry Pi 5 deployment | Completed |
| PyTorch benchmark | Completed |
| NCNN benchmark | Completed |
| YOLOv8n vs YOLO11n comparison | Completed |

---

# Engineering Conclusion

Both YOLOv8n and YOLO11n successfully learned the three target Pakistani grocery products.

The final mixed evaluation included:

```text
153 target-product images
100 negative/background images
253 total images
```

Both negative-trained models achieved:

```text
Precision        = 99.8%
Recall           = 100%
mAP@0.50         = 99.5%
mAP@0.50:0.95    = 89.2%
```

The explicit addition of negative grocery and person/background samples substantially improved live-camera rejection of non-target objects.

On the Raspberry Pi 5, NCNN significantly outperformed native PyTorch inference.

Final NCNN performance:

```text
YOLOv8n:
6.25 inference FPS
5.84 end-to-end FPS

YOLO11n:
6.47 inference FPS
6.03 end-to-end FPS
```

YOLO11n provides the smaller architecture and slightly higher Raspberry Pi inference throughput, while YOLOv8n demonstrated strong practical detection behavior during live-camera testing.

The final deployment decision can therefore be based on the required trade-off between practical detection robustness and computational efficiency.
