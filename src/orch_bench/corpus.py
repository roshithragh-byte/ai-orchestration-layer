import json
from pathlib import Path
from .models import Scenario

def load_scenarios(path: str | Path) -> list[Scenario]:
    path = Path(path)
    if path.is_file():
        data = json.loads(path.read_text())
        return [Scenario(**item) for item in data]
    return [Scenario(**json.loads(f.read_text())) for f in sorted(path.glob("*.json"))]

def select_scenarios(
    scenarios: list[Scenario],
    ids: list[str] | None = None,
    categories: list[str] | None = None,
) -> list[Scenario]:
    if ids:
        wanted = set(ids)
        return [s for s in scenarios if s.id in wanted]
    if categories:
        wanted = set(categories)
        return [s for s in scenarios if s.category in wanted]
    return scenarios
