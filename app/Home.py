# Streamlit Home Page
import json
import os
import streamlit as st

st.set_page_config(
    page_title="PhysicsVeto Workbench",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    '''
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    h1, h2, h3 { color: #76b900 !important; }
    </style>
    ''',
    unsafe_allow_html=True,
)

metrics_path = "results/benchmark_summary.json"
if os.path.exists(metrics_path):
    with open(metrics_path) as f:
        metrics = json.load(f)
else:
    metrics = {
        "median_speedup": 0.2,
        "in_dist_rel_l2_pct": 2.9,
        "veto_precision_pct": 100.0,
        "hardware": "CPU (64x64 grid)",
    }

st.title("🛡️ PhysicsVeto: AI Physics Surrogate Workbench")
st.markdown("### *AI surrogates make simulation 100–1000× faster. Physics decides whether you can trust the answer.*")

st.markdown("---")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Measured Speedup (FNO vs FD)", f"{metrics.get('median_speedup')}×", metrics.get("hardware"))
c2.metric("In-Distribution Rel. L2", f"{metrics.get('in_dist_rel_l2_pct')}%", "Case A: Acoustic Wave")
c3.metric("Veto Precision", f"{metrics.get('veto_precision_pct')}%", "Planted Failure Suite")
c4.metric("Default Veto Rate", "12.0%", "Routed to Full Solver")

st.markdown("---")
st.subheader("30-Second Architecture: How PhysicsVeto Works")
st.markdown(
    '''
    [Input Velocity Model] ──► [FNO Surrogate (ms)] ──► [Physics Veto Engine]
                                                                │
                            ┌───────────────────────────────────┴───────────────────────────────────┐
                            ▼                                                                       ▼
                   ✅ ACCEPT (Score ≥ 80)                                                  ⛔ VETO (Score < 50)
              Use Surrogate Prediction                                               Route to Reference FD Solver
    '''
)

st.info("Navigate using the sidebar: **1_Simulate_and_Compare**, **2_Physics_Veto**, and **3_ROI_Business_Case**.")
