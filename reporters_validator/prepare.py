import yaml
from pathlib import Path

from reporters_validator.report_reader import read_report

# Fields that change every run and should not be in expected files
_DYNAMIC_RESULT_KEYS = {"id"}
_DYNAMIC_EXECUTION_KEYS = {"start_time", "end_time", "duration", "thread"}


def generate_expected(report_dir: Path) -> dict:
    """Generate expected data from an existing report for bootstrapping."""
    report = read_report(report_dir)

    expected_results = []
    for result in report.results:
        expected_result = _strip_dynamic(result)
        expected_results.append(expected_result)

    return {
        "run": {
            "stats": report.run.get("stats", {}),
        },
        "results": expected_results,
    }


def write_expected(data: dict, output_path: Path) -> None:
    """Write expected data to a YAML file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def _strip_dynamic(result: dict) -> dict:
    """Remove dynamic fields from a result dict."""
    out = {}
    for key, value in result.items():
        if key in _DYNAMIC_RESULT_KEYS:
            continue
        if key == "execution" and isinstance(value, dict):
            stripped_exec = {k: v for k, v in value.items() if k not in _DYNAMIC_EXECUTION_KEYS}
            if stripped_exec:
                out[key] = stripped_exec
            # Promote status to top level for readability
            if "status" in value:
                out["status"] = value["status"]
            continue
        out[key] = value
    return out
