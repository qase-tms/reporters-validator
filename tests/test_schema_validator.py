import pytest
from pathlib import Path

from reporters_validator.schema_validator import validate_schema, SchemaValidationError

FIXTURES = Path(__file__).parent / "fixtures"
SCHEMAS = FIXTURES / "schemas"
REPORT = FIXTURES / "valid_report"


def test_validate_valid_report_passes():
    errors = validate_schema(REPORT, SCHEMAS)
    assert errors == []


def test_validate_returns_errors_for_invalid_run(tmp_path):
    # run.json with wrong type for title
    run_json = tmp_path / "run.json"
    run_json.write_text('{"title": 123}')
    results_dir = tmp_path / "results"
    results_dir.mkdir()

    errors = validate_schema(tmp_path, SCHEMAS)
    assert len(errors) > 0
    assert any("run.json" in e.file for e in errors)


def test_validate_returns_errors_for_invalid_result(tmp_path):
    import json

    run_json = tmp_path / "run.json"
    run_json.write_text(json.dumps({
        "title": "Run",
        "execution": {"start_time": 0, "end_time": 0, "duration": 0, "cumulative_duration": 0},
        "stats": {"total": 1, "passed": 1, "failed": 0, "skipped": 0, "blocked": 0, "invalid": 0, "muted": 0},
        "results": [{"id": "a", "title": "t", "status": "passed", "duration": 0}]
    }))

    results_dir = tmp_path / "results"
    results_dir.mkdir()
    result_file = results_dir / "bad.json"
    # id must be string, here it's a number
    result_file.write_text('{"id": 123, "title": "t", "muted": false}')

    errors = validate_schema(tmp_path, SCHEMAS)
    assert len(errors) > 0
    assert any("bad.json" in e.file for e in errors)


def test_schema_validation_error_has_message():
    err = SchemaValidationError(file="run.json", path="$.title", message="123 is not of type 'string'")
    assert "run.json" in str(err)
    assert "title" in str(err)
