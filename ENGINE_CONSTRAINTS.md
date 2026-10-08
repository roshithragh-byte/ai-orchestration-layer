# Engine Constraints v0.1

These are provisional constraints. They become binding only after a real baseline/treatment run.

1. **Model-independent control plane.** Planner, scheduler, validator, recovery and state management must not depend on a specific LLM vendor.
2. **Typed task outputs.** Downstream tasks consume validated artifacts, not arbitrary conversational context.
3. **Validation is completion.** A task cannot become COMPLETED merely because an executor returned successfully.
4. **Explicit failure.** No silent catch-and-continue behavior that converts failure into success.
5. **Observable recovery.** Retries, fallback executors, recovery tasks and replans are recorded as execution events.
6. **Adaptive decomposition.** Support DIRECT, LINEAR and DAG execution modes; measure decomposition overhead.
7. **First-class benchmarkability.** Every workflow run exposes enough metadata to compare quality, cost, latency and recovery.
8. **Deterministic checks first.** Prefer schema validation, tests, counts and calculations over LLM judges where possible.
9. **Cost and latency are product constraints.**
10. **Failure-heavy workloads are mandatory.** The adversarial tier remains in every release benchmark.

## Decision gate

Do not introduce Redis, Kafka, Temporal, Kubernetes, or a visual workflow builder until benchmark evidence shows a concrete need.
