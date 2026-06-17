import streamlit as st
from datetime import datetime


def init_session():
    """Initialize all session state keys."""
    defaults = {
        "history": [],          # list of detection run dicts
        "model_size": "yolov8s",
        "conf_threshold": 0.50,
        "iou_threshold": 0.40,
        "input_size": 640,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def add_to_history(filename: str, detections: list, inference_ms: float, source: str = "image"):
    """Append a detection run to session history."""
    if "history" not in st.session_state:
        st.session_state["history"] = []

    st.session_state["history"].append({
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "filename": filename,
        "count": len(detections),
        "avg_conf": round(sum(d["confidence"] for d in detections) / len(detections), 1) if detections else 0,
        "inference_ms": inference_ms,
        "detections": detections,
        "source": source,
    })


def get_history():
    return st.session_state.get("history", [])


def clear_history():
    st.session_state["history"] = []


def get_all_detections():
    """Flatten all detections from history into one list."""
    all_det = []
    for run in get_history():
        all_det.extend(run["detections"])
    return all_det
