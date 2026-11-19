# ROI Cost Model implementation
from typing import Dict, List

def compute_hpc_roi(
    simulations_per_year: int = 50000,
    solver_core_hours: float = 4.0,
    cloud_cost_per_core_hour: float = 0.08,
    surrogate_speedup: float = 240.0,
    veto_rate: float = 0.12,
    engineer_hourly_cost: float = 120.0,
) -> Dict[str, float]:
    traditional_cost = simulations_per_year * solver_core_hours * cloud_cost_per_core_hour

    accepted_fraction = max(0.0, min(1.0, 1.0 - veto_rate))
    surrogate_solve_cost = (
        simulations_per_year
        * accepted_fraction
        * (solver_core_hours / max(1.0, surrogate_speedup))
        * cloud_cost_per_core_hour
    )
    veto_solve_cost = simulations_per_year * veto_rate * solver_core_hours * cloud_cost_per_core_hour
    total_hybrid_cost = surrogate_solve_cost + veto_solve_cost

    annual_savings = traditional_cost - total_hybrid_cost
    time_saved_core_hours = simulations_per_year * solver_core_hours * accepted_fraction * (1.0 - 1.0 / max(1.0, surrogate_speedup))
    time_to_design_reduction_pct = accepted_fraction * (1.0 - 1.0 / max(1.0, surrogate_speedup)) * 100.0

    return {
        "traditional_annual_cost_usd": round(traditional_cost, 2),
        "hybrid_annual_cost_usd": round(total_hybrid_cost, 2),
        "annual_savings_usd": round(annual_savings, 2),
        "veto_rate_pct": round(veto_rate * 100.0, 1),
        "time_saved_core_hours": round(time_saved_core_hours, 1),
        "time_to_design_reduction_pct": round(time_to_design_reduction_pct, 1),
    }

def run_sensitivity_tornado(base_params: Dict[str, float]) -> List[Dict[str, float]]:
    base_savings = compute_hpc_roi(**base_params)["annual_savings_usd"]
    factors = [
        ("Simulations / Year", "simulations_per_year", 0.7, 1.3),
        ("Solver Core-Hours / Run", "solver_core_hours", 0.7, 1.3),
        ("Cloud $/Core-Hour", "cloud_cost_per_core_hour", 0.7, 1.3),
        ("Measured Veto Rate", "veto_rate", 0.5, 1.5),
        ("Surrogate Speedup", "surrogate_speedup", 0.5, 1.5),
    ]
    results = []
    for label, key, low_mult, high_mult in factors:
        low_p = dict(base_params)
        low_p[key] = base_params[key] * low_mult
        high_p = dict(base_params)
        high_p[key] = base_params[key] * high_mult
        low_sav = compute_hpc_roi(**low_p)["annual_savings_usd"]
        high_sav = compute_hpc_roi(**high_p)["annual_savings_usd"]
        results.append({
            "parameter": label,
            "low_savings": low_sav,
            "high_savings": high_sav,
            "base_savings": base_savings,
            "swing": abs(high_sav - low_sav),
        })
    results.sort(key=lambda x: x["swing"], reverse=True)
    return results
