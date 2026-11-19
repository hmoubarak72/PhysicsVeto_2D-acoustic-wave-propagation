# 2D Acoustic Wave Solver with Absorbing Boundaries and CFL Check
import numpy as np
from typing import Tuple

class AcousticWaveSolver:
    def __init__(self, nx: int = 64, ny: int = 64, dx: float = 10.0, dy: float = 10.0, cfl: float = 0.4):
        self.nx = nx
        self.ny = ny
        self.dx = dx
        self.dy = dy
        self.cfl = cfl

    def check_cfl(self, velocity_model: np.ndarray, dt: float) -> bool:
        max_vel = float(np.max(velocity_model))
        min_dh = min(self.dx, self.dy)
        dt_max = self.cfl * min_dh / (max_vel + 1e-8)
        if dt > dt_max:
            raise ValueError(f"CFL violation: dt={dt} exceeds stability limit {dt_max:.5f}")
        return True

    def solve(self, velocity_model: np.ndarray, source_loc: Tuple[int, int], wavelet: np.ndarray, dt: float = 0.0005) -> np.ndarray:
        nt = len(wavelet)
        self.check_cfl(velocity_model, dt)

        p_prev = np.zeros((self.nx, self.ny), dtype=np.float32)
        p_curr = np.zeros((self.nx, self.ny), dtype=np.float32)
        p_next = np.zeros((self.nx, self.ny), dtype=np.float32)

        wavefield_history = np.zeros((nt, self.nx, self.ny), dtype=np.float32)
        dx2 = self.dx ** 2
        dy2 = self.dy ** 2
        sx, sy = source_loc

        sponge_width = 8
        damping = np.zeros((self.nx, self.ny), dtype=np.float32)
        for i in range(self.nx):
            for j in range(self.ny):
                dist_edge = min(i, j, self.nx - 1 - i, self.ny - 1 - j)
                if dist_edge < sponge_width:
                    factor = (float(sponge_width - dist_edge) / sponge_width) ** 2
                    damping[i, j] = 0.05 * factor

        v2_dt2 = (velocity_model ** 2) * (dt ** 2)

        for n in range(nt):
            laplacian = np.zeros_like(p_curr)
            laplacian[1:-1, 1:-1] = (
                (p_curr[2:, 1:-1] - 2 * p_curr[1:-1, 1:-1] + p_curr[:-2, 1:-1]) / dx2 +
                (p_curr[1:-1, 2:] - 2 * p_curr[1:-1, 1:-1] + p_curr[1:-1, :-2]) / dy2
            )

            p_next[1:-1, 1:-1] = (
                2.0 * p_curr[1:-1, 1:-1] - p_prev[1:-1, 1:-1] +
                v2_dt2[1:-1, 1:-1] * laplacian[1:-1, 1:-1]
            )

            p_next[sx, sy] += wavelet[n] * v2_dt2[sx, sy]
            p_next *= (1.0 - damping)

            p_prev[:, :] = p_curr
            p_curr[:, :] = p_next
            wavefield_history[n] = p_curr

        return wavefield_history
