# Gaussian Random Field generator for Case A
import numpy as np
from scipy.ndimage import gaussian_filter

def generate_gaussian_random_field(
    nx: int = 64,
    ny: int = 64,
    scale: float = 8.0,
    v_min: float = 2000.0,
    v_max: float = 4500.0,
    seed: int | None = None,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    noise = rng.standard_normal((nx, ny))
    smoothed = gaussian_filter(noise, sigma=scale)
    v_field = v_min + (v_max - v_min) * (smoothed - smoothed.min()) / (smoothed.max() - smoothed.min() + 1e-8)
    return v_field.astype(np.float32)
