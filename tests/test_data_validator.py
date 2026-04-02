import pytest
from pathlib import Path

from reporters_validator.data_validator import validate_data, DataValidationError

FIXTURES = Path(__file__).parent / "fixtures"


def test_validate_matching_data_passes():
    errors = validate_data(
        FIXTURES / "valid_report",
        FIXTURES / "expected" / "simple.yaml",
    )
    assert errors == []


def test_validate_wrong_status(tmp_path):
    """Expected says passed but actual says failed."""
    _write_minimal_report(tmp_path, results=[
        {"id": "1", "title": "T", "signature": "A.Test", "execution": {"status": "failed"},
         "fields": {}, "attachments": [], "steps": [], "params": {}, "param_groups": [],
         "relations": {"suite": {"data": []}}, "muted": False},
    ])
    _write_expected(tmp_path, results=[
        {"signature": "A.Test", "status": "passed"},
    ])

    errors = validate_data(tmp_path / "report", tmp_path / "expected.yaml")
    assert len(errors) == 1
    assert errors[0].field == "execution.status"
    assert errors[0].expected == "passed"
    assert errors[0].actual == "failed"


def test_validate_missing_field(tmp_path):
    """Expected has field that doesn't exist in actual."""
    _write_minimal_report(tmp_path, results=[
        {"id": "1", "title": "T", "signature": "A.Test", "execution": {"status": "passed"},
         "fields": {}, "attachments": [], "steps": [], "params": {}, "param_groups": [],
         "relations": {"suite": {"data": []}}, "muted": False},
    ])
    _write_expected(tmp_path, results=[
        {"signature": "A.Test", "fields": {"severity": "critical"}},
    ])

    errors = validate_data(tmp_path / "report", tmp_path / "expected.yaml")
    assert len(errors) == 1
    assert "severity" in errors[0].field


def test_validate_missing_actual_result(tmp_path):
    """Expected result not found in actual."""
    _write_minimal_report(tmp_path, results=[])
    _write_expected(tmp_path, results=[
        {"signature": "A.Missing", "status": "passed"},
    ])

    errors = validate_data(tmp_path / "report", tmp_path / "expected.yaml")
    assert len(errors) == 1
    assert "not found" in errors[0].message.lower()


def test_validate_run_stats(tmp_path):
    """Run stats mismatch."""
    _write_minimal_report(tmp_path, stats={"total": 5, "passed": 3, "failed": 2, "skipped": 0, "blocked": 0, "invalid": 0, "muted": 0})
    _write_expected(tmp_path, run={"stats": {"total": 10}})

    errors = validate_data(tmp_path / "report", tmp_path / "expected.yaml")
    assert len(errors) == 1
    assert errors[0].field == "run.stats.total"


def test_validate_steps(tmp_path):
    """Step status mismatch."""
    _write_minimal_report(tmp_path, results=[
        {"id": "1", "title": "T", "signature": "A.Test", "execution": {"status": "passed"},
         "fields": {}, "attachments": [], "params": {}, "param_groups": [],
         "steps": [{"id": "s1", "step_type": "text", "data": {"action": "click"},
                     "execution": {"status": "passed"}, "steps": []}],
         "relations": {"suite": {"data": []}}, "muted": False},
    ])
    _write_expected(tmp_path, results=[
        {"signature": "A.Test", "steps": [{"data": {"action": "click"}, "execution": {"status": "failed"}}]},
    ])

    errors = validate_data(tmp_path / "report", tmp_path / "expected.yaml")
    assert len(errors) == 1
    assert "steps[0]" in errors[0].field


def test_validate_partial_match_ignores_unspecified(tmp_path):
    """Fields not in expected are not checked."""
    _write_minimal_report(tmp_path, results=[
        {"id": "1", "title": "Different title", "signature": "A.Test", "execution": {"status": "passed"},
         "fields": {"extra": "value"}, "attachments": [], "steps": [], "params": {}, "param_groups": [],
         "relations": {"suite": {"data": []}}, "muted": False},
    ])
    _write_expected(tmp_path, results=[
        {"signature": "A.Test", "status": "passed"},
    ])

    errors = validate_data(tmp_path / "report", tmp_path / "expected.yaml")
    assert errors == []


# --- Helpers ---

def _write_minimal_report(base: Path, results=None, stats=None):
    import json
    report_dir = base / "report"
    report_dir.mkdir(exist_ok=True)
    if stats is None:
        stats = {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "blocked": 0, "invalid": 0, "muted": 0}
    run = {
        "title": "Test",
        "execution": {"start_time": 0, "end_time": 0, "duration": 0, "cumulative_duration": 0},
        "stats": stats,
        "results": [],
    }
    (report_dir / "run.json").write_text(json.dumps(run))
    results_dir = report_dir / "results"
    results_dir.mkdir(exist_ok=True)
    if results:
        for i, r in enumerate(results):
            (results_dir / f"r{i}.json").write_text(json.dumps(r))


def _write_expected(base: Path, results=None, run=None):
    import yaml
    data = {}
    if run:
        data["run"] = run
    if results:
        data["results"] = results
    (base / "expected.yaml").write_text(yaml.dump(data))
