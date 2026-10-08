import hashlib
import time
import uuid
from datetime import datetime, timezone
from .models import BenchmarkRun, CaseResult, Scenario

def _stable_score(sid: str, mode: str) -> tuple[int, int, int, int]:
    seed = int(hashlib.sha256(f"{sid}:{mode}".encode()).hexdigest()[:8], 16)
    base = 2 + seed % 3
    if mode == "baseline":
        return base, max(1, base - 1), max(1, base - 1), max(1, base - 1)
    return min(4, base + 1), min(4, base + 1), min(4, base + 1), min(4, base + 1)

def run_scenario(
    s: Scenario,
    mode: str,
    provider: str = "mock",
    model: str = "fixture-v0.1",
) -> CaseResult:
    start = time.perf_counter()
    c, comp, val, proof = _stable_score(s.id, mode)
    if s.category == "adversarial" and mode == "baseline":
        c = max(1, c - 1)
        val = max(1, val - 1)
    recoveries = 1 if s.category == "adversarial" and mode == "orchestrated" else 0
    latency = int((time.perf_counter() - start) * 1000) + (50 if mode == "baseline" else 120)
    cost = 0.01 if mode == "baseline" else 0.018
    return CaseResult(
        scenario_id=s.id,
        status="passed" if c >= 2 and comp >= 2 and val >= 2 else "failed",
        correctness=c,
        completeness=comp,
        validity=val,
        proof=proof,
        latency_ms=latency,
        cost_usd=cost,
        recoveries=recoveries,
        notes="synthetic fixture; replace with real model adapter" if provider == "mock" else "",
    )

def run(
    scenarios: list[Scenario],
    mode: str,
    provider: str = "mock",
    model: str = "fixture-v0.1",
) -> BenchmarkRun:
    now = datetime.now(timezone.utc).isoformat()
    results = [run_scenario(s, mode, provider, model) for s in scenarios]
    return BenchmarkRun(
        schema_version="0.1.0",
        benchmark_version="0.1.0",
        run_id=f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}",
        mode=mode,
        timestamp=now,
        model=model,
        provider=provider,
        scenarios=results,
        metadata={"synthetic": provider == "mock"},
    )
