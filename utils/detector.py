import numpy as np
import cv2
import time
from pathlib import Path
import streamlit as st

COLORS = [
    (86, 180, 233), (230, 159, 0), (0, 158, 115), (213, 94, 0),
    (0, 114, 178), (204, 121, 167), (240, 228, 66), (0, 202, 255),
    (255, 105, 180), (0, 255, 127), (255, 165, 0), (138, 43, 226),
]

@st.cache_resource(show_spinner=False)
def load_model(model_size="yolov8s"):
    """Load YOLOv8 model (cached so it only loads once)."""
    try:
        from ultralytics import YOLO
        model = YOLO(f"{model_size}.pt")
        return model, None
    except ImportError:
        return None, "ultralytics not installed. Run: pip install ultralytics"
    except Exception as e:
        return None, str(e)


def run_detection(image_bgr: np.ndarray, model, conf_threshold=0.5, iou_threshold=0.4):
    """
    Run YOLOv8 inference on a BGR image.
    Returns (annotated_image, results_list, inference_ms)
    results_list: list of dicts with keys: class_name, confidence, bbox (x1,y1,x2,y2)
    """
    start = time.perf_counter()

    results = model.predict(
        source=image_bgr,
        conf=conf_threshold,
        iou=iou_threshold,
        verbose=False
    )

    elapsed_ms = (time.perf_counter() - start) * 1000
    annotated = image_bgr.copy()
    detections = []

    for result in results:
        boxes = result.boxes
        names = result.names

        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            cls_name = names[cls_id]

            color = COLORS[cls_id % len(COLORS)]

            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)

            label = f"{cls_name} {conf:.0%}"
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)
            cv2.rectangle(annotated, (x1, y1 - th - 8), (x1 + tw + 6, y1), color, -1)
            cv2.putText(annotated, label, (x1 + 3, y1 - 4),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 1, cv2.LINE_AA)

            detections.append({
                "class_name": cls_name,
                "confidence": round(conf * 100, 1),
                "bbox": (x1, y1, x2, y2),
                "class_id": cls_id,
                "color": color,
            })

    return annotated, detections, round(elapsed_ms, 1)


def bgr_to_rgb(img: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def bytes_to_bgr(file_bytes: bytes) -> np.ndarray:
    arr = np.frombuffer(file_bytes, np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)


def detections_to_csv(detections: list) -> str:
    import io, csv
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["class_name", "confidence", "x1", "y1", "x2", "y2"])
    writer.writeheader()
    for d in detections:
        x1, y1, x2, y2 = d["bbox"]
        writer.writerow({
            "class_name": d["class_name"],
            "confidence": d["confidence"],
            "x1": x1, "y1": y1, "x2": x2, "y2": y2,
        })
    return output.getvalue()


def detections_to_yolo_txt(detections: list, img_w: int, img_h: int) -> str:
    lines = []
    for d in detections:
        x1, y1, x2, y2 = d["bbox"]
        cx = ((x1 + x2) / 2) / img_w
        cy = ((y1 + y2) / 2) / img_h
        w  = (x2 - x1) / img_w
        h  = (y2 - y1) / img_h
        lines.append(f"{d['class_id']} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}")
    return "\n".join(lines)


def class_distribution(detections: list) -> dict:
    dist = {}
    for d in detections:
        dist[d["class_name"]] = dist.get(d["class_name"], 0) + 1
    return dict(sorted(dist.items(), key=lambda x: x[1], reverse=True))
