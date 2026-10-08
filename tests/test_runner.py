from orch_bench.corpus import load_scenarios
from orch_bench.runner import run

def test_baseline_runner_produces_all_cases():
    scenarios = load_scenarios("benchmark/scenarios.json")
    result = run(scenarios, "baseline")
    assert result.mode == "baseline"
    assert len(result.scenarios) == 30
    assert result.aggregate()["cases"] == 30

def test_orchestrated_fixture_is_distinct_from_baseline():
    scenarios = load_scenarios("benchmark/scenarios.json")
    baseline = run(scenarios, "baseline")
    orchestrated = run(scenarios, "orchestrated")
    assert orchestrated.aggregate()["quality_score"] >= baseline.aggregate()["quality_score"]
    assert orchestrated.aggregate()["recovery_rate"] >= baseline.aggregate()["recovery_rate"]
