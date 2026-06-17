import streamlit as st

st.set_page_config(
    page_title="DetectAI v2.0",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

from utils.styles import inject_css
inject_css()

st.sidebar.markdown("""
<div style="text-align:center; padding: 1rem 0 0.5rem;">
    <div style="font-size:2rem;">🎯</div>
    <h2 style="margin:0; font-size:1.3rem;">DetectAI v2.0</h2>
    <p style="margin:0; font-size:0.75rem; color:#888;">Powered by YOLOv8</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["📷  Image Detection", "🎥  Live Camera", "📊  Analytics Dashboard", "⚙️  Model Config"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-size:0.75rem; color:#888; padding: 0.5rem 0;">
    <b>Model:</b> YOLOv8s<br>
    <b>Dataset:</b> COCO (80 classes)<br>
    <b>Input:</b> 640×640
</div>
""", unsafe_allow_html=True)

if "📷" in page:
    from pages.image_detection import show
    show()
elif "🎥" in page:
    from pages.live_camera import show
    show()
elif "📊" in page:
    from pages.analytics import show
    show()
elif "⚙️" in page:
    from pages.model_config import show
    show()
