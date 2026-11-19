# Physics Veto Engine implementation
import numpy as np
from typing import Dict, Any

class PhysicsVetoEngine:
    def __init__(
        self,
        pde_tolerance: float = 0.05,
        energy_tolerance: float = 0.10,
        ood_threshold: float = 1.5,
        accept_min: float = 80.0,
        review_min: float = 50.0,
    ):
        self.pde_tolerance = pde_tolerance
        self.energy_tolerance = energy_tolerance
        self.ood_threshold = ood_threshold
        self.accept_min = accept_min
        self.review_min = review_min

    def compute_residual_map(self, pred_field: np.ndarray, v_model: np.ndarray, dx: float = 10.0, dy: float = 10.0) -> np.ndarray:
        laplacian = np.zeros_like(pred_field, dtype=np.float32)
        laplacian[1:-1, 1:-1] = (
            (pred_field[2:, 1:-1] - 2 * pred_field[1:-1, 1:-1] + pred_field[:-2, 1:-1]) / (dx ** 2) +
            (pred_field[1:-1, 2:] - 2 * pred_field[1:-1, 1:-1] + pred_field[1:-1, :-2]) / (dy ** 2)
        )
        norm_factor = np.max(np.abs(pred_field)) + 1e-8
        residual_map = np.abs(laplacian * (dx ** 2)) / norm_factor
        return residual_map

    def compute_boundary_error(self, pred_field: np.ndarray) -> float:
        edge_vals = np.concatenate([
            pred_field[0, :], pred_field[-1, :], pred_field[:, 0], pred_field[:, -1]
        ])
        interior_rms = float(np.sqrt(np.mean(pred_field[8:-8, 8:-8] ** 2)) + 1e-8)
        edge_rms = float(np.sqrt(np.mean(edge_vals ** 2)))
        return edge_rms / interior_rms

    def check_energy_conservation(self, pred_field: np.ndarray, expected_energy: float) -> float:
        total_energy = float(np.sum(pred_field ** 2))
        return abs(total_energy - expected_energy) / (expected_energy + 1e-8)

    def compute_ood_score(self, input_velocity: np.ndarray) -> float:
        mean_v = float(np.mean(input_velocity))
        std_v = float(np.std(input_velocity))
        expected_mean, expected_std = 3250.0, 550.0
        distance = abs(mean_v - expected_mean) / expected_std + abs(std_v - expected_std) / expected_std
        return float(distance)

    def evaluate(
        self,
        pred_field: np.ndarray,
        input_velocity: np.ndarray,
        expected_energy: float | None = None,
    ) -> Dict[str, Any]:
        residual_map = self.compute_residual_map(pred_field, input_velocity)
        pde_res = float(np.sqrt(np.mean(residual_map ** 2)))
        bc_err = self.compute_boundary_error(pred_field)
        if expected_energy is None:
            expected_energy = float(np.sum(pred_field ** 2))
        energy_err = self.check_energy_conservation(pred_field, expected_energy)
        ood_score = self.compute_ood_score(input_velocity)

        penalty = (
            max(0.0, (pde_res - 0.02) * 350.0)
            + max(0.0, (bc_err - 0.15) * 120.0)
            + (energy_err * 80.0)
            + max(0.0, (ood_score - self.ood_threshold) * 35.0)
        )
        trust_score = max(0.0, min(100.0, 100.0 - penalty))

        reasons = []
        if pde_res > self.pde_tolerance:
            reasons.append(f"High PDE residual ({pde_res:.4f} > {self.pde_tolerance})")
        if bc_err > 0.35:
            reasons.append(f"Boundary reflection mismatch ({bc_err:.2f})")
        if energy_err > self.energy_tolerance:
            reasons.append(f"Energy conservation drift ({energy_err:.1%})")
        if ood_score > self.ood_threshold:
            reasons.append(f"Out-of-distribution velocity contrast (OOD={ood_score:.2f})")

        if trust_score >= self.accept_min and not reasons:
            verdict = "ACCEPT"
        elif trust_score >= self.review_min:
            verdict = "REVIEW"
        else:
            verdict = "VETO"

        return {
            "trust_score": round(trust_score, 1),
            "verdict": verdict,
            "pde_residual": round(pde_res, 4),
            "boundary_error": round(bc_err, 4),
            "energy_error": round(energy_err, 4),
            "ood_score": round(ood_score, 2),
            "reasons": reasons if reasons else ["All physics checks passed within tolerance."],
            "residual_map": residual_map,
        }
