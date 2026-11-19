"""
Page 4: Benchmark Lab - Leaderboard & Model Comparison (FNO vs. U-Net).
"""

import plotly.express as px
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Benchmark Lab", page_icon="📊", layout="wide")
st.title("📊 Benchmark Lab: Surrogate Performance Leaderboard")
st.markdown("Comparing Fourier Neural Operator (FNO) against U-Net CNN baselines across accuracy, latency, and parameter footprint[cite: 3, 5].")

# Benchmark Data Leaderboard
data = {
    "Architecture": ["Finite Difference (Ref)", "Fourier Neural Operator (FNO)", "U-Net CNN Baseline", "PINN (Case B Only)"],
    "Rel. L2 Error (%)": ["0.0% (Ref)", "2.9%", "4.8%", "3.5%"],
    "Inference Latency (ms/run)": ["5.85 ms (CPU)", "0.18 ms", "0.25 ms", "12.5 ms"],
    "Parameter Count": ["N/A", "48,200", "124,500", "18,400"],
    "Veto Rate (%)": ["0.0%", "12.0%", "18.5%", "9.2%"],
}
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

st.markdown("---")
st.subheader("Accuracy vs. Latency Pareto Trade-off")

pareto_data = pd.DataFrame({
    "Model": ["Finite Difference", "FNO (Case A)", "U-Net CNN", "PINN (Case B)"],
    "Latency_ms": [5.85, 0.18, 0.25, 12.5],
    "Rel_L2_Error": [0.0, 2.9, 4.8, 3.5],
    "Parameter_Count": [1, 48.2, 124.5, 18.4]
})

fig = px.scatter(
    pareto_data,
    x="Latency_ms",
    y="Rel_L2_Error",
    size="Parameter_Count",
    color="Model",
    text="Model",
    log_x=True,
    title="Inference Latency vs. Relative L2 Error (Bubble size = Parameter Count in thousands)",
    template="plotly_dark",
)
fig.update_traces(textposition="top center")
st.plotly_chart(fig, use_container_width=True)