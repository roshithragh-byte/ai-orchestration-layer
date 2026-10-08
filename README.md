# AI Orchestration Benchmark v0.1

Benchmark-first orchestration research workspace.

This repository separates the benchmark corpus, single-agent baseline, orchestrated treatment, evaluation, and regression comparison. The default `mock` provider is a deterministic harness fixture only; it is **not evidence that orchestration improves real model performance**.

## gstack-derived patterns

The harness adapts useful benchmark/eval patterns from gstack: explicit baselines, timestamped run artifacts, machine-readable results, reference comparisons, regression thresholds, selective execution, historical preservation, and deterministic local tests.

Reference: https://github.com/garrytan/gstack/tree/main/scripts

## Run

```bash
python -m pytest -q
PYTHONPATH=src python -m orch_bench.cli baseline
PYTHONPATH=src python -m orch_bench.cli run
```

Compare two runs:

```bash
PYTHONPATH=src python -m orch_bench.cli compare benchmark/baselines/<baseline>.json benchmark/runs/<run>.json
```

Selective execution:

```bash
PYTHONPATH=src python -m orch_bench.cli baseline --categories research software
PYTHONPATH=src python -m orch_bench.cli run --ids A01 A02 A03 A04 A05
```

## Research rule

The first real provider adapter should record model/provider, prompt version, latency, token counts where available, tool calls, final answer, structured artifacts, evaluator scores, and failures/retries.

Do not use synthetic fixture results for product conclusions.
