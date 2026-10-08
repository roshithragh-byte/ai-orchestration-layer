# Benchmark Protocol v0.1

## Baseline

Run the same 30 scenarios through the simplest credible single-agent implementation.

Capture benchmark version, scenario version, model/provider, prompt version, commit, timestamp, latency, cost, output, and evaluator scores.

## Treatment

Run the exact same scenario set through the orchestrator. Only the execution strategy should change. Keep model/provider constant whenever possible.

## Minimum experiment

- 30 scenarios
- 3 independent runs per condition
- identical model/provider configuration
- fixed scenario corpus
- deterministic evaluators wherever possible

Do not compare one baseline run against one treatment run and call the result conclusive.

## Primary gates

- Reliability: +20 percentage points target
- Completeness: +15 percentage points target
- Recovery: materially better on A01-A05
- Cost: <= 2x baseline
- Median latency: <= 3x baseline

These are product gates, not statistical significance claims. Once real data exists, add confidence intervals and variance reporting.
