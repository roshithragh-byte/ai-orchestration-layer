from dataclasses import dataclass, field, asdict
from typing import Any

@dataclass
class Scenario:
    id: str
    category: str
    title: str
    objective: str
    acceptance_criteria: list[str]
    difficulty: str
    benchmark_version: str

@dataclass
class CaseResult:
    scenario_id: str
    status: str
    correctness: int
    completeness: int
    validity: int
    proof: int
    latency_ms: int
    cost_usd: float
    attempts: int = 1
    recoveries: int = 0
    human_interventions: int = 0
    notes: str = ""

    @property
    def quality_points(self) -> int:
        return self.correctness + self.completeness + self.validity + self.proof

@dataclass
class BenchmarkRun:
    schema_version: str
    benchmark_version: str
    run_id: str
    mode: str
    timestamp: str
    model: str
    provider: str
    scenarios: list[CaseResult]
    metadata: dict[str, Any] = field(default_factory=dict)

    def aggregate(self) -> dict[str, Any]:
        n = len(self.scenarios)
        if not n:
            return {}
        quality = sum(x.quality_points for x in self.scenarios) / (16*n)
        success = sum(x.status == "passed" for x in self.scenarios) / n
        completeness = sum(x.completeness for x in self.scenarios) / (4*n)
        validity = sum(x.validity for x in self.scenarios) / (4*n)
        proof = sum(x.proof for x in self.scenarios) / (4*n)
        return {
            "cases": n,
            "success_rate": success,
            "quality_score": quality,
            "completeness_score": completeness,
            "validity_score": validity,
            "proof_score": proof,
            "median_latency_ms": sorted(x.latency_ms for x in self.scenarios)[n//2],
            "total_latency_ms": sum(x.latency_ms for x in self.scenarios),
            "total_cost_usd": sum(x.cost_usd for x in self.scenarios),
            "recovery_rate": (
                sum(x.recoveries > 0 and x.status == "passed" for x in self.scenarios)
                / max(1, sum(x.recoveries > 0 or x.status == "failed" for x in self.scenarios))
            ),
            "human_intervention_rate": sum(x.human_interventions > 0 for x in self.scenarios) / n,
        }

def case_to_dict(c: CaseResult) -> dict[str, Any]:
    return asdict(c)
