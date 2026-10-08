import argparse
import json
from pathlib import Path
from .corpus import load_scenarios, select_scenarios
from .runner import run
from .compare import compare

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "benchmark/scenarios.json"
BASELINES = ROOT / "benchmark/baselines"
RUNS = ROOT / "benchmark/runs"

def save_run(run_obj, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": run_obj.schema_version,
        "benchmark_version": run_obj.benchmark_version,
        "run_id": run_obj.run_id,
        "mode": run_obj.mode,
        "timestamp": run_obj.timestamp,
        "model": run_obj.model,
        "provider": run_obj.provider,
        "metadata": run_obj.metadata,
        "aggregate": run_obj.aggregate(),
        "scenarios": [vars(x) for x in run_obj.scenarios],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")

def load_run(path):
    from .models import BenchmarkRun, CaseResult
    data = json.loads(Path(path).read_text())
    return BenchmarkRun(
        schema_version=data["schema_version"],
        benchmark_version=data["benchmark_version"],
        run_id=data["run_id"],
        mode=data["mode"],
        timestamp=data["timestamp"],
        model=data["model"],
        provider=data["provider"],
        scenarios=[CaseResult(**{k: v for k, v in x.items() if k != "quality_points"}) for x in data["scenarios"]],
        metadata=data.get("metadata", {}),
    )

def main():
    p = argparse.ArgumentParser(prog="orch-bench")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("baseline", "run"):
        sp = sub.add_parser(name)
        sp.add_argument("--ids", nargs="*")
        sp.add_argument("--categories", nargs="*")
        sp.add_argument("--provider", default="mock")
        sp.add_argument("--model", default="fixture-v0.1")
        sp.add_argument("--out")
    cp = sub.add_parser("compare")
    cp.add_argument("baseline")
    cp.add_argument("current")
    args = p.parse_args()

    if args.cmd in ("baseline", "run"):
        scenarios = select_scenarios(load_scenarios(CORPUS), args.ids, args.categories)
        mode = "baseline" if args.cmd == "baseline" else "orchestrated"
        result = run(scenarios, mode, args.provider, args.model)
        out = Path(args.out) if args.out else (BASELINES if mode == "baseline" else RUNS) / f"{result.run_id}.json"
        save_run(result, out)
        print(json.dumps({
            "run_id": result.run_id,
            "mode": mode,
            "cases": len(scenarios),
            "aggregate": result.aggregate(),
            "output": str(out),
        }, indent=2))
    else:
        result = compare(load_run(args.baseline), load_run(args.current))
        print(json.dumps(result, indent=2))
        raise SystemExit(0 if result["pass"] else 1)

if __name__ == "__main__":
    main()
