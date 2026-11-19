# 5-Minute Live Interview Demo Script — PhysicsVeto

## 0:00–0:45 | The Hook & Product Thesis
- Open **Overview** (`app/Home.py`).
- State the thesis: *"AI surrogates make simulation 100–1000× faster. Physics decides whether you can trust the answer."*[cite: 4]

## 0:45–2:15 | Speed & Accuracy (Simulate & Compare)
- Switch to **Simulate & Compare**.
- Run the 2D acoustic wave solver alongside the FNO surrogate on a synthetic velocity model[cite: 3].
- Scrub through wavefield propagation frames and discuss CPU vs. GPU scaling thresholds honestly.

## 2:15–3:45 | The Core Differentiator ("Try to break it")
- Switch to **Physics Veto**.
- Show an in-distribution **ACCEPT** verdict[cite: 5].
- Click **"💥 Try to break it"** to inject an extreme high-contrast velocity anomaly and unphysical wavefield artifacts.
- Watch the Trust Score drop and the **VETO** fire, highlighting the per-cell PDE residual heatmap[cite: 5].

## 3:45–5:00 | Business Case & NVIDIA Scaling Story
- Switch to **ROI & Business Case**.
- Show how the **measured veto rate is subtracted** from gross savings[cite: 5].
- Close with the **Scaling on the NVIDIA Stack** architecture (PhysicsNeMo + CuPy + Omniverse)[cite: 3].