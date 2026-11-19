"""
Page 5: Go-to-Market Studio & Product Requirements Document (PRD).
"""

import streamlit as st

st.set_page_config(page_title="GTM Studio & PRD", page_icon="🎯", layout="wide")
st.title("🎯 Go-to-Market Studio & Product Roadmap")

tab1, tab2 = st.tabs(["GTM Solution Brief & Personas", "Product PRD & Roadmap"])

with tab1:
    st.subheader("Target Vertical: Energy & Subsurface (Seismic Imaging / FWI)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Customer Persona")
        st.markdown("""
        * **Title:** Simulation Lead / CAE Manager / VP of Subsurface HPC.
        * **Pain Points:** 
          1. HPC cluster congestion and multi-million dollar annual cloud bills.
          2. Zero trust in black-box deep learning surrogates for out-of-distribution geological models.
        * **Key Objection:** *"How do I know the surrogate won't fail silently on a new reservoir model?"*
        """)
    with col2:
        st.markdown("### Value Proposition & Physics Veto Defense")
        st.markdown("""
        * **Value Proposition:** Accelerate design sweeps 100–1000× while guaranteeing physical validity[cite: 4].
        * **Objection Handling:** Answered via the **Physics Veto Engine**, which audits PDE residuals, energy bounds, and OOD Mahalanobis distance on every prediction[cite: 5].
        """)

    st.markdown("---")
    st.download_button(
        label="📥 Download One-Page Solution Brief (Markdown)",
        data="# PhysicsVeto Solution Brief\nVerified AI Physics Surrogates for HPC CAE.\n- 240x speedup\n- Automated Physics Veto Gate",
        file_name="PhysicsVeto_Solution_Brief.md",
        mime="text/markdown",
    )

with tab2:
    st.subheader("Product Requirements Document (PRD)")
    st.markdown("""
    * **Problem:** Enterprise simulation teams cannot adopt AI surrogates due to lack of verification[cite: 4].
    * **Users:** CAE engineers, HPC administrators, subsurface geophysicists.
    * **Success Metrics:** Veto precision > 95%[cite: 5], page load < 3 seconds[cite: 6], time-to-first-surrogate < 5 minutes.
    * **Now / Next / Later Roadmap:**
      * **Now:** Case A (Acoustic Wave) + Veto Engine + Streamlit App + ROI Calculator[cite: 2, 3, 5].
      * **Next:** Case B (Thermal Conduction / Poisson) + PINN integration[cite: 3].
      * **Later:** Case C (Darcy Flow) + NVIDIA PhysicsNeMo multi-GPU distributed training backend[cite: 3].
    """)