# 🚀 DetectAI V2 – Real-Time Object Detection & Analytics Platform

DetectAI V2 is a modern computer vision application built using **YOLOv8**, **Streamlit**, and **OpenCV**. The platform enables real-time object detection on images and live webcam feeds while providing analytics, object statistics, and export functionality.

## 📌 Features

### 🖼️ Image Detection

* Upload single or multiple images
* Detect objects using YOLOv8
* Bounding box visualization
* Confidence score display
* Previous/Next image navigation
* Export results as CSV

### 📹 Live Camera Detection

* Real-time webcam object detection
* Live object counting
* FPS monitoring
* Session-based detection history

### 📊 Analytics Dashboard

* Top detected object classes
* Confidence distribution analysis
* Detection history tracking
* Export analytics reports

### ⚙️ Model Configuration

* Support for YOLOv8n / YOLOv8s / YOLOv8m / YOLOv8l / YOLOv8x
* Adjustable confidence threshold
* Adjustable IoU threshold
* COCO dataset class support (80 classes)

---

## 🛠️ Tech Stack

* Python
* YOLOv8 (Ultralytics)
* Streamlit
* OpenCV
* NumPy
* Pandas
* Plotly

---

## 📂 Project Structure

```text
detectai_v2/
│
├── app.py
├── requirements.txt
├── render.yaml
│
├── pages/
│   ├── image_detection.py
│   ├── live_camera.py
│   ├── analytics.py
│   └── model_config.py
│
├── utils/
│   └── detector.py
│
└── exports/
```

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/geeta3521/DetectAI-V2.git
cd DetectAI-V2
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

## 🎯 Supported Object Classes

The model supports detection of 80 COCO dataset classes including:

* Person
* Car
* Bus
* Truck
* Bicycle
* Dog
* Cat
* Chair
* Laptop
* Mobile Phone

and many more.

---

## 📈 Future Enhancements

* Video Upload Detection
* Object Tracking (DeepSORT/ByteTrack)
* AI-Powered Detection Reports
* Cloud Deployment
* Multi-Camera Support
* Custom Model Training

---

## 👩‍💻 Author

**Geeta A N**

GitHub: https://github.com/geeta3521

LinkedIn: https://linkedin.com/in/geeta-nemgouda/

---


