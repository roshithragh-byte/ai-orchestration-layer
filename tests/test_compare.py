from orch_bench.corpus import load_scenarios
from orch_bench.runner import run
from orch_bench.compare import compare

def test_compare_reports_gate_results():
    scenarios = load_scenarios("benchmark/scenarios.json")
    baseline = run(scenarios, "baseline")
    current = run(scenarios, "orchestrated")
    result = compare(baseline, current)
    assert set(result["gates"]) == {"reliability", "completeness", "cost", "latency"}
    assert all(isinstance(v, bool) for v in result["gates"].values())
