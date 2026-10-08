from .models import BenchmarkRun

def pct_delta(before: float, after: float) -> float | None:
    if before == 0:
        return None
    return (after - before) / before

def compare(baseline: BenchmarkRun, current: BenchmarkRun) -> dict:
    b, c = baseline.aggregate(), current.aggregate()
    metrics = {}
    for key in [
        "success_rate", "completeness_score", "quality_score", "validity_score",
        "proof_score", "recovery_rate", "human_intervention_rate",
        "median_latency_ms", "total_cost_usd",
    ]:
        metrics[key] = {
            "baseline": b.get(key),
            "current": c.get(key),
            "delta": (
                c.get(key) - b.get(key)
                if b.get(key) is not None and c.get(key) is not None
                else None
            ),
            "pct_delta": (
                pct_delta(b.get(key, 0), c.get(key, 0))
                if b.get(key) is not None and c.get(key) is not None
                else None
            ),
        }
    gates = {
        "reliability": metrics["success_rate"]["delta"] is not None and metrics["success_rate"]["delta"] >= 0.20,
        "completeness": metrics["completeness_score"]["delta"] is not None and metrics["completeness_score"]["delta"] >= 0.15,
        "cost": metrics["total_cost_usd"]["pct_delta"] is not None and metrics["total_cost_usd"]["pct_delta"] <= 1.0,
        "latency": metrics["median_latency_ms"]["pct_delta"] is not None and metrics["median_latency_ms"]["pct_delta"] <= 2.0,
    }
    return {"metrics": metrics, "gates": gates, "pass": all(gates.values())}
