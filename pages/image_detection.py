import streamlit as st
import cv2
from utils.detector import (
    load_model, run_detection, bgr_to_rgb,
    bytes_to_bgr, detections_to_csv, detections_to_yolo_txt, class_distribution
)
from utils.session import init_session, add_to_history


def show():
    init_session()
    st.title("📷 Image Detection")
    st.markdown("Upload one or multiple images — YOLOv8 will detect objects, draw bounding boxes, and give you full export options.")

    # ── Model load ──────────────────────────────────────────────────────────
    with st.spinner("Loading YOLOv8 model…"):
        model, err = load_model(st.session_state.get("model_size", "yolov8s"))
    if err:
        st.error(f"Model load failed: {err}")
        st.info("Install dependencies: `pip install ultralytics opencv-python`")
        return

    # ── Sidebar controls ────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### Detection settings")
        conf  = st.slider("Confidence threshold", 0.1, 0.95,
                          st.session_state.get("conf_threshold", 0.50), 0.05)
        iou   = st.slider("NMS IoU threshold",    0.1, 0.95,
                          st.session_state.get("iou_threshold",  0.40), 0.05)
        st.session_state["conf_threshold"] = conf
        st.session_state["iou_threshold"]  = iou

    # ── Upload ───────────────────────────────────────────────────────────────
    uploaded = st.file_uploader(
        "Drop images here",
        type=["jpg", "jpeg", "png", "webp", "bmp"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if not uploaded:
        st.markdown("""
        <div style="border:2px dashed #333; border-radius:12px; padding:3rem; text-align:center; color:#666; margin-top:1rem;">
            <div style="font-size:3rem;">📂</div>
            <p style="margin:0.5rem 0 0;">Drag & drop images here, or click <b>Browse files</b> above</p>
            <p style="font-size:0.8rem; margin-top:0.3rem;">JPG · PNG · WEBP · BMP</p>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Navigation when multiple files ───────────────────────────────────────
    if len(uploaded) > 1:
        col_nav1, col_nav2, col_nav3 = st.columns([1, 3, 1])
        if "img_idx" not in st.session_state:
            st.session_state["img_idx"] = 0
        idx = st.session_state["img_idx"]
        with col_nav1:
            if st.button("◀ Prev") and idx > 0:
                st.session_state["img_idx"] -= 1
                st.rerun()
        with col_nav2:
            st.markdown(
                f"<p style='text-align:center; color:#aaa; margin:0.5rem 0;'>"
                f"Image {idx+1} of {len(uploaded)}</p>",
                unsafe_allow_html=True
            )
        with col_nav3:
            if st.button("Next ▶") and idx < len(uploaded) - 1:
                st.session_state["img_idx"] += 1
                st.rerun()
        file = uploaded[st.session_state["img_idx"]]
    else:
        file = uploaded[0]

    # ── Run detection ────────────────────────────────────────────────────────
    image_bgr = bytes_to_bgr(file.read())
    h, w = image_bgr.shape[:2]

    with st.spinner("Running YOLOv8 inference…"):
        annotated_bgr, detections, ms = run_detection(image_bgr, model, conf, iou)

    add_to_history(file.name, detections, ms, source="image")

    # ── Layout: image left, results right ───────────────────────────────────
    col_img, col_res = st.columns([3, 2])

    with col_img:
        st.image(bgr_to_rgb(annotated_bgr), caption=file.name, use_container_width=True)

    with col_res:
        # Metric cards
        m1, m2, m3 = st.columns(3)
        m1.metric("Objects", len(detections))
        m2.metric("Avg conf", f"{sum(d['confidence'] for d in detections)/len(detections):.0f}%" if detections else "—")
        m3.metric("Time", f"{ms} ms")

        st.markdown("---")
        st.markdown("**Detected objects**")

        if not detections:
            st.info("No objects detected above the confidence threshold.")
        else:
            for d in detections:
                conf_val = d["confidence"]
                badge_cls = "badge-blue" if conf_val >= 80 else "badge-green" if conf_val >= 65 else "badge-amber"
                st.markdown(
                    f"""<div class="det-row">
                        <span style="font-size:1.1rem">🔍</span>
                        <div style="flex:1">
                            <b style="color:#e0e0e0">{d['class_name']}</b>
                        </div>
                        <span class="badge {badge_cls}">{conf_val}%</span>
                    </div>""",
                    unsafe_allow_html=True
                )

            # Class distribution bar chart
            st.markdown("---")
            st.markdown("**Class breakdown**")
            dist = class_distribution(detections)
            max_count = max(dist.values())
            for cls, cnt in dist.items():
                pct = int(cnt / max_count * 100)
                st.markdown(
                    f"""<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                        <span style="width:80px;font-size:0.8rem;color:#aaa;text-align:right">{cls}</span>
                        <div style="flex:1;background:#2d2d3d;border-radius:4px;height:8px;overflow:hidden">
                            <div style="width:{pct}%;height:100%;background:#4f8ef7;border-radius:4px"></div>
                        </div>
                        <span style="font-size:0.8rem;color:#aaa;width:16px">{cnt}</span>
                    </div>""",
                    unsafe_allow_html=True
                )

    # ── Export section ───────────────────────────────────────────────────────
    if detections:
        st.markdown("---")
        st.markdown("### 📤 Export results")
        ec1, ec2, ec3 = st.columns(3)

        csv_data = detections_to_csv(detections)
        ec1.download_button(
            "⬇️ Download CSV",
            data=csv_data,
            file_name=f"{file.name.rsplit('.',1)[0]}_detections.csv",
            mime="text/csv",
            use_container_width=True,
        )

        yolo_txt = detections_to_yolo_txt(detections, w, h)
        ec2.download_button(
            "⬇️ YOLO annotations (.txt)",
            data=yolo_txt,
            file_name=f"{file.name.rsplit('.',1)[0]}.txt",
            mime="text/plain",
            use_container_width=True,
        )

        _, ann_encoded = cv2.imencode(".jpg", annotated_bgr)
        ec3.download_button(
            "⬇️ Annotated image",
            data=ann_encoded.tobytes(),
            file_name=f"{file.name.rsplit('.',1)[0]}_annotated.jpg",
            mime="image/jpeg",
            use_container_width=True,
        )
