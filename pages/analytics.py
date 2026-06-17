import streamlit as st
import pandas as pd
from collections import Counter
from utils.session import init_session, get_history, get_all_detections, clear_history


def show():
    init_session()
    st.title("📊 Analytics Dashboard")
    st.markdown("Aggregated stats across all detection runs this session.")

    history = get_history()

    if not history:
        st.markdown("""
        <div style="border:2px dashed #333;border-radius:12px;padding:3rem;text-align:center;color:#555;margin-top:1rem;">
            <div style="font-size:3rem;">📈</div>
            <p style="margin:0.5rem 0 0;">No detection runs yet. Go to <b>Image Detection</b> or <b>Live Camera</b> to get started.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    all_det = get_all_detections()
    total_objects = len(all_det)
    avg_conf = round(sum(d["confidence"] for d in all_det) / total_objects, 1) if all_det else 0
    avg_ms   = round(sum(r["inference_ms"] for r in history) / len(history), 1)

    # ── Summary metrics ──────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total runs",    len(history))
    c2.metric("Total objects", total_objects)
    c3.metric("Avg confidence", f"{avg_conf}%")
    c4.metric("Avg inference",  f"{avg_ms} ms")

    st.markdown("---")

    # ── Class distribution ────────────────────────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### Most detected classes")
        class_counts = Counter(d["class_name"] for d in all_det)
        top_classes = class_counts.most_common(10)

        if top_classes:
            df_classes = pd.DataFrame(top_classes, columns=["Class", "Count"])
            st.bar_chart(df_classes.set_index("Class"), use_container_width=True)

            st.markdown("**Top 10 table**")
            st.dataframe(df_classes, use_container_width=True, hide_index=True)

    with col_right:
        st.markdown("### Confidence distribution")
        if all_det:
            conf_bins = {"<60%": 0, "60-70%": 0, "70-80%": 0, "80-90%": 0, "≥90%": 0}
            for d in all_det:
                c = d["confidence"]
                if c < 60:   conf_bins["<60%"] += 1
                elif c < 70: conf_bins["60-70%"] += 1
                elif c < 80: conf_bins["70-80%"] += 1
                elif c < 90: conf_bins["80-90%"] += 1
                else:        conf_bins["≥90%"] += 1

            df_conf = pd.DataFrame(
                list(conf_bins.items()), columns=["Range", "Count"]
            )
            st.bar_chart(df_conf.set_index("Range"), use_container_width=True)

    st.markdown("---")

    # ── Per-run history table ─────────────────────────────────────────────────
    st.markdown("### Detection run history")

    df_hist = pd.DataFrame([{
        "Time":       r["timestamp"],
        "File":       r["filename"],
        "Source":     r["source"],
        "Objects":    r["count"],
        "Avg conf %": r["avg_conf"],
        "Time (ms)":  r["inference_ms"],
    } for r in history])

    st.dataframe(df_hist, use_container_width=True, hide_index=True)

    # ── Export all ────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### Export all data")

    ex1, ex2, ex3 = st.columns(3)

    all_det_flat = []
    for r in history:
        for d in r["detections"]:
            x1, y1, x2, y2 = d["bbox"]
            all_det_flat.append({
                "timestamp": r["timestamp"],
                "filename":  r["filename"],
                "source":    r["source"],
                "class":     d["class_name"],
                "confidence": d["confidence"],
                "x1": x1, "y1": y1, "x2": x2, "y2": y2,
            })

    if all_det_flat:
        df_export = pd.DataFrame(all_det_flat)
        ex1.download_button(
            "⬇️ All detections CSV",
            data=df_export.to_csv(index=False),
            file_name="all_detections.csv",
            mime="text/csv",
            use_container_width=True,
        )
        ex2.download_button(
            "⬇️ Run history CSV",
            data=df_hist.to_csv(index=False),
            file_name="run_history.csv",
            mime="text/csv",
            use_container_width=True,
        )
        class_csv = pd.DataFrame(top_classes, columns=["Class","Count"]).to_csv(index=False)
        ex3.download_button(
            "⬇️ Class summary CSV",
            data=class_csv,
            file_name="class_summary.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown("---")
    if st.button("🗑 Clear session history", type="secondary"):
        clear_history()
        st.rerun()
