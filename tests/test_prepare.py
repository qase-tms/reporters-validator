import json
import yaml
import pytest
from pathlib import Path
from click.testing import CliRunner

from reporters_validator.cli import main
from reporters_validator.prepare import generate_expected

FIXTURES = Path(__file__).parent / "fixtures"


def test_generate_expected_from_report():
    data = generate_expected(FIXTURES / "valid_report")
    assert "run" in data
    assert data["run"]["stats"]["total"] == 2
    assert len(data["results"]) == 2


def test_generate_expected_results_have_key_fields():
    data = generate_expected(FIXTURES / "valid_report")
    for result in data["results"]:
        assert "signature" in result or "title" in result
        assert "status" in result


def test_generate_expected_excludes_dynamic_fields():
    data = generate_expected(FIXTURES / "valid_report")
    for result in data["results"]:
        assert "id" not in result
        assert "start_time" not in result.get("execution", {})
        assert "end_time" not in result.get("execution", {})
        assert "duration" not in result.get("execution", {})


def test_prepare_cli_writes_yaml(tmp_path):
    output_file = tmp_path / "out.yaml"
    runner = CliRunner()
    result = runner.invoke(main, [
        "prepare",
        "--report-dir", str(FIXTURES / "valid_report"),
        "--output", str(output_file),
    ])
    assert result.exit_code == 0
    assert output_file.exists()

    with open(output_file) as f:
        data = yaml.safe_load(f)
    assert "results" in data
    assert len(data["results"]) == 2
