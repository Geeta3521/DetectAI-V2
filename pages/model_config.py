import streamlit as st
from utils.session import init_session


MODEL_INFO = {
    "yolov8n": {"params": "3.2M",  "mAP": "37.3", "speed": "⚡⚡⚡ Fastest", "use": "Edge / real-time on CPU"},
    "yolov8s": {"params": "11.2M", "mAP": "44.9", "speed": "⚡⚡  Fast",    "use": "Balanced — good default"},
    "yolov8m": {"params": "25.9M", "mAP": "50.2", "speed": "⚡   Medium",   "use": "Better accuracy, needs GPU"},
    "yolov8l": {"params": "43.7M", "mAP": "52.9", "speed": "🐢  Slow",     "use": "High accuracy, GPU required"},
    "yolov8x": {"params": "68.2M", "mAP": "53.9", "speed": "🐢🐢 Slowest", "use": "Max accuracy, strong GPU"},
}


def show():
    init_session()
    st.title("⚙️ Model Configuration")
    st.markdown("Tune the YOLOv8 model and detection parameters. Changes apply immediately on the next run.")

    st.markdown("### Model size")
    st.markdown("Larger models are more accurate but slower. **yolov8s** is the recommended starting point.")

    current = st.session_state.get("model_size", "yolov8s")
    cols = st.columns(len(MODEL_INFO))

    for i, (name, info) in enumerate(MODEL_INFO.items()):
        with cols[i]:
            selected = name == current
            border = "2px solid #4f8ef7" if selected else "1px solid #2d2d3d"
            bg     = "#1a2a45"           if selected else "#1e2130"
            st.markdown(f"""
            <div style="background:{bg};border:{border};border-radius:10px;padding:0.8rem;text-align:center;margin-bottom:0.5rem;">
                <div style="font-weight:700;font-size:0.9rem;color:#e0e0e0">{name}</div>
                <div style="font-size:0.7rem;color:#888;margin:4px 0">{info['params']} params</div>
                <div style="font-size:0.75rem;color:#aaa">{info['speed']}</div>
                <div style="font-size:0.7rem;color:#5eb0f5;margin-top:4px">mAP {info['mAP']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Select", key=f"sel_{name}", use_container_width=True,
                         type="primary" if selected else "secondary"):
                st.session_state["model_size"] = name
                st.rerun()

    chosen = st.session_state.get("model_size", "yolov8s")
    st.markdown(f"""
    <div class="info-box">
        ✅ Active model: <b>{chosen}</b> — {MODEL_INFO[chosen]['use']}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Detection thresholds")

    col1, col2 = st.columns(2)
    with col1:
        conf = st.slider(
            "Confidence threshold",
            0.05, 0.95,
            st.session_state.get("conf_threshold", 0.50), 0.05,
            help="Minimum confidence score for a detection to be kept. Higher = fewer but more certain detections."
        )
        st.session_state["conf_threshold"] = conf
        st.caption(f"Current: **{conf:.0%}** — {'strict (may miss objects)' if conf > 0.7 else 'balanced' if conf >= 0.4 else 'permissive (more false positives)'}")

    with col2:
        iou = st.slider(
            "NMS IoU threshold",
            0.1, 0.95,
            st.session_state.get("iou_threshold", 0.40), 0.05,
            help="Controls how aggressively overlapping boxes are suppressed. Lower = more aggressive merging."
        )
        st.session_state["iou_threshold"] = iou
        st.caption(f"Current: **{iou:.0%}** — {'loose (may have duplicates)' if iou > 0.6 else 'balanced' if iou >= 0.35 else 'aggressive merging'}")

    st.markdown("---")
    st.markdown("### COCO classes (80 total)")
    st.markdown("YOLOv8 trained on COCO can detect all of these out of the box:")

    coco_classes = [
        "person","bicycle","car","motorcycle","airplane","bus","train","truck","boat",
        "traffic light","fire hydrant","stop sign","parking meter","bench","bird","cat",
        "dog","horse","sheep","cow","elephant","bear","zebra","giraffe","backpack",
        "umbrella","handbag","tie","suitcase","frisbee","skis","snowboard","sports ball",
        "kite","baseball bat","baseball glove","skateboard","surfboard","tennis racket",
        "bottle","wine glass","cup","fork","knife","spoon","bowl","banana","apple",
        "sandwich","orange","broccoli","carrot","hot dog","pizza","donut","cake","chair",
        "couch","potted plant","bed","dining table","toilet","tv","laptop","mouse",
        "remote","keyboard","cell phone","microwave","oven","toaster","sink","refrigerator",
        "book","clock","vase","scissors","teddy bear","hair drier","toothbrush"
    ]

    cols_per_row = 6
    rows = [coco_classes[i:i+cols_per_row] for i in range(0, len(coco_classes), cols_per_row)]
    for row in rows:
        rcols = st.columns(cols_per_row)
        for j, cls in enumerate(row):
            rcols[j].markdown(
                f"<span style='font-size:0.75rem;background:#1e2130;border:1px solid #2d2d3d;"
                f"border-radius:5px;padding:2px 6px;display:inline-block;color:#aaa'>{cls}</span>",
                unsafe_allow_html=True
            )

    st.markdown("---")
    st.markdown("### About this app")
    st.markdown("""
    **DetectAI v2.0** is an upgraded reimagination of a YOLOv4+Tkinter desktop app, rebuilt with:

    | Component | Old (v1) | New (v2) |
    |-----------|----------|----------|
    | Model | YOLOv4 | **YOLOv8** |
    | Frontend | Tkinter | **Streamlit** |
    | Export | None | **CSV, YOLO .txt, annotated image** |
    | Analytics | None | **Full dashboard** |
    | Deployment | Local only | **Cloud-ready** |
    | Camera | Basic | **FPS-controlled, stats overlay** |

    Built with Python 3.10+, Ultralytics, OpenCV, Streamlit, Pandas.
    """)
