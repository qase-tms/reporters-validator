import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Report:
    run: dict
    results: list[dict] = field(default_factory=list)


def read_report(report_dir: Path) -> Report:
    """Read run.json and all results/*.json from a report directory."""
    report_dir = Path(report_dir)
    if not report_dir.is_dir():
        raise FileNotFoundError(f"Report directory not found: {report_dir}")

    run_path = report_dir / "run.json"
    if not run_path.is_file():
        raise FileNotFoundError(f"run.json not found in {report_dir}")

    with open(run_path, "r", encoding="utf-8") as f:
        run_data = json.load(f)

    results = []
    results_dir = report_dir / "results"
    if results_dir.is_dir():
        for result_file in sorted(results_dir.glob("*.json")):
            with open(result_file, "r", encoding="utf-8") as f:
                results.append(json.load(f))

    return Report(run=run_data, results=results)
