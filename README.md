# 🎯 DetectAI v2.0 — YOLOv8 Object Detection Web App

A modern upgrade of a YOLOv4+Tkinter project, rebuilt with YOLOv8 and Streamlit for 2025/26 placements.

## Features

| Feature | Description |
|---------|-------------|
| 📷 Image Detection | Upload single or multiple images, get annotated results |
| 🎥 Live Camera | Real-time webcam detection with FPS overlay |
| 📊 Analytics | Session-wide dashboard — class distribution, confidence charts |
| ⬇️ Export | CSV, YOLO .txt annotations, annotated JPEG |
| ⚙️ Model Config | Switch between yolov8n/s/m/l/x, tune conf & IoU thresholds |

## Quick Start

```bash
# 1. Clone / download this folder
cd detectai_v2

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app opens at **http://localhost:8501**

YOLOv8 weights (yolov8s.pt, ~22 MB) download automatically on first run.

## Project Structure

```
detectai_v2/
├── app.py                   # Entry point — sidebar nav
├── requirements.txt
├── README.md
├── pages/
│   ├── image_detection.py   # Upload & detect page
│   ├── live_camera.py       # Webcam detection page
│   ├── analytics.py         # Session analytics dashboard
│   └── model_config.py      # Model & threshold settings
└── utils/
    ├── detector.py          # YOLOv8 inference engine
    ├── session.py           # Session state / history manager
    └── styles.py            # CSS injection
```

## Deployment (free)

### Render
1. Push to GitHub
2. New Web Service → connect repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

### Railway
Same as above — Railway auto-detects Streamlit.

### Streamlit Community Cloud (easiest)
1. Push to GitHub
2. Go to share.streamlit.io → Deploy → point to `app.py`
3. Free, automatic HTTPS, custom subdomain

## Resume Line

> Built and deployed DetectAI v2.0 — a real-time object detection web app using YOLOv8 + Streamlit with CSV/annotation export, class analytics dashboard, and live webcam detection. Deployed on [Render/Railway]. [your-live-url]

## Tech Stack

- **Model**: YOLOv8 (Ultralytics) — COCO 80 classes
- **Frontend**: Streamlit
- **CV**: OpenCV
- **Data**: Pandas, NumPy
- **Export**: CSV, YOLO .txt, JPEG
