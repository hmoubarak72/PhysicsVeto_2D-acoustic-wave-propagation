# PhysicsVeto — Solution Brief
**Verified AI Physics Surrogates for Subsurface & CAE Simulation**

### The Challenge
AI surrogates accelerate physics simulation by orders of magnitude at production scale, yet engineering teams cannot deploy black-box models where physical accuracy is non-negotiable.

### The PhysicsVeto Solution
PhysicsVeto pairs Fourier Neural Operators (FNO) with an inline physics verification engine:
1. **Verify with Physics:** Computes PDE residuals, boundary mismatch, energy drift, and OOD distance on every run[cite: 5].
2. **Smart Routing:** Routes low-confidence predictions back to the reference numerical solver[cite: 4, 5].
3. **Quantify Net ROI:** Explicitly subtracts vetoed fallback runs from annual HPC savings[cite: 5].