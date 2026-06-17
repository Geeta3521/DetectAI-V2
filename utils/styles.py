import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp {background-color: #0f1117;}

    section[data-testid="stSidebar"] {
        background-color: #1a1d27;
        border-right: 1px solid #2d2d3d;
    }

    .metric-card {
        background: #1e2130;
        border: 1px solid #2d2d3d;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        text-align: center;
    }
    .metric-card .label {
        font-size: 0.75rem;
        color: #888;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-card .value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #fff;
    }
    .metric-card .unit {
        font-size: 0.75rem;
        color: #888;
    }

    .det-row {
        background: #1e2130;
        border: 1px solid #2d2d3d;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        margin-bottom: 0.4rem;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
    }
    .badge-blue  { background:#1a3a5c; color:#5eb0f5; }
    .badge-green { background:#1a3a2a; color:#4cd98a; }
    .badge-amber { background:#3a2a10; color:#f5a623; }
    .badge-red   { background:#3a1a1a; color:#f56060; }

    .section-header {
        font-size: 1rem;
        font-weight: 600;
        color: #e0e0e0;
        margin: 1.2rem 0 0.6rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid #2d2d3d;
    }

    .info-box {
        background: #1a2535;
        border: 1px solid #1e4a7a;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        font-size: 0.85rem;
        color: #90b8e0;
        margin: 0.5rem 0;
    }

    div[data-testid="stButton"] > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }

    .stProgress > div > div {
        background: linear-gradient(90deg, #4f8ef7, #7c5af7);
    }
    </style>
    """, unsafe_allow_html=True)
