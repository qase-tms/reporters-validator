import pytest
from pathlib import Path
from click.testing import CliRunner

from reporters_validator.cli import main

FIXTURES = Path(__file__).parent / "fixtures"


def test_validate_full_passes():
    runner = CliRunner()
    result = runner.invoke(main, [
        "validate",
        "--report-dir", str(FIXTURES / "valid_report"),
        "--schema-dir", str(FIXTURES / "schemas"),
        "--expected", str(FIXTURES / "expected" / "simple.yaml"),
    ])
    assert result.exit_code == 0


def test_validate_schema_only_passes():
    runner = CliRunner()
    result = runner.invoke(main, [
        "validate",
        "--report-dir", str(FIXTURES / "valid_report"),
        "--schema-dir", str(FIXTURES / "schemas"),
        "--schema-only",
    ])
    assert result.exit_code == 0


def test_validate_schema_failure_exits_1(tmp_path):
    run_json = tmp_path / "run.json"
    run_json.write_text('{"title": 123}')
    results_dir = tmp_path / "results"
    results_dir.mkdir()

    runner = CliRunner()
    result = runner.invoke(main, [
        "validate",
        "--report-dir", str(tmp_path),
        "--schema-dir", str(FIXTURES / "schemas"),
        "--schema-only",
    ])
    assert result.exit_code == 1
    assert "schema" in result.output.lower()


def test_validate_requires_expected_or_schema_only():
    """Without --expected or --schema-only, should fail."""
    runner = CliRunner()
    result = runner.invoke(main, [
        "validate",
        "--report-dir", str(FIXTURES / "valid_report"),
        "--schema-dir", str(FIXTURES / "schemas"),
    ])
    assert result.exit_code == 2
