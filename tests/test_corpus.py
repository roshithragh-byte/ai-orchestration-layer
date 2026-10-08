from orch_bench.corpus import load_scenarios, select_scenarios

def test_corpus_contains_exactly_30_unique_scenarios():
    scenarios = load_scenarios("benchmark/scenarios.json")
    assert len(scenarios) == 30
    assert len({s.id for s in scenarios}) == 30

def test_corpus_has_five_scenarios_per_category():
    scenarios = load_scenarios("benchmark/scenarios.json")
    counts = {}
    for s in scenarios:
        counts[s.category] = counts.get(s.category, 0) + 1
    assert counts == {"research": 5, "software": 10, "data": 5, "planning": 5, "adversarial": 5}

def test_select_by_id_is_deterministic():
    scenarios = load_scenarios("benchmark/scenarios.json")
    selected = select_scenarios(scenarios, ids=["A03", "R01"])
    assert [s.id for s in selected] == ["A03", "R01"]
