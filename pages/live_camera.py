import streamlit as st
import cv2
import time
import numpy as np
from utils.detector import load_model, run_detection, bgr_to_rgb, class_distribution
from utils.session import init_session, add_to_history


def show():
    init_session()
    st.title("🎥 Live Camera Detection")
    st.markdown("Real-time YOLOv8 detection from your webcam. Use the controls below to start and stop the feed.")

    with st.spinner("Loading YOLOv8 model…"):
        model, err = load_model(st.session_state.get("model_size", "yolov8s"))
    if err:
        st.error(f"Model load failed: {err}")
        return

    with st.sidebar:
        st.markdown("### Camera settings")
        conf  = st.slider("Confidence", 0.1, 0.95, st.session_state.get("conf_threshold", 0.50), 0.05)
        cam_id = st.number_input("Camera index", 0, 5, 0, 1)
        max_fps = st.slider("Target FPS", 1, 30, 10)
        st.session_state["conf_threshold"] = conf

    col1, col2 = st.columns([1, 1])
    start_btn = col1.button("▶ Start camera", use_container_width=True, type="primary")
    stop_btn  = col2.button("⏹ Stop",         use_container_width=True)

    if stop_btn:
        st.session_state["cam_running"] = False

    if start_btn:
        st.session_state["cam_running"] = True

    if not st.session_state.get("cam_running", False):
        st.markdown("""
        <div style="border:2px dashed #333;border-radius:12px;padding:4rem;text-align:center;color:#555;margin-top:1rem;">
            <div style="font-size:3rem;">📹</div>
            <p style="margin:0.5rem 0 0;">Click <b>Start camera</b> to begin live detection</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Live feed ────────────────────────────────────────────────────────────
    st.markdown("---")
    feed_col, stats_col = st.columns([3, 2])

    frame_placeholder = feed_col.empty()
    stats_placeholder = stats_col.empty()

    cap = cv2.VideoCapture(cam_id)
    if not cap.isOpened():
        st.error(f"Could not open camera {cam_id}. Make sure your webcam is connected and not in use by another app.")
        st.session_state["cam_running"] = False
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    frame_delay = 1.0 / max_fps
    total_frames = 0
    total_detections = 0
    fps_start = time.time()
    fps_display = 0.0

    st.session_state["cam_running"] = True

    try:
        while st.session_state.get("cam_running", False):
            t0 = time.time()
            ret, frame = cap.read()
            if not ret:
                st.warning("Lost camera feed.")
                break

            annotated, detections, inf_ms = run_detection(
                frame, model,
                conf_threshold=conf,
                iou_threshold=st.session_state.get("iou_threshold", 0.4)
            )

            total_frames += 1
            total_detections += len(detections)

            elapsed_total = time.time() - fps_start
            fps_display = round(total_frames / elapsed_total, 1) if elapsed_total > 0 else 0

            cv2.putText(annotated, f"FPS: {fps_display}", (10, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(annotated, f"Objects: {len(detections)}", (10, 55),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            frame_placeholder.image(bgr_to_rgb(annotated), channels="RGB", use_container_width=True)

            add_to_history(f"camera_frame_{total_frames}", detections, inf_ms, source="camera")

            dist = class_distribution(detections)
            stats_md = f"""
**Frame #{total_frames}** · {inf_ms} ms inference

| Metric | Value |
|--------|-------|
| FPS | {fps_display} |
| Objects this frame | {len(detections)} |
| Total objects seen | {total_detections} |

**This frame:**
"""
            if dist:
                for cls, cnt in list(dist.items())[:6]:
                    stats_md += f"\n- **{cls}** × {cnt}"
            else:
                stats_md += "\n*No detections*"

            stats_placeholder.markdown(stats_md)

            elapsed = time.time() - t0
            sleep_time = frame_delay - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    finally:
        cap.release()
        st.session_state["cam_running"] = False
        st.success(f"Camera stopped. Processed {total_frames} frames, detected {total_detections} objects total.")
