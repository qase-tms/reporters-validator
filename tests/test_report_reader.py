import pytest
from pathlib import Path

from reporters_validator.report_reader import read_report

FIXTURES = Path(__file__).parent / "fixtures"


def test_read_report_returns_run_and_results():
    report = read_report(FIXTURES / "valid_report")
    assert report.run is not None
    assert len(report.results) == 2


def test_read_report_run_fields():
    report = read_report(FIXTURES / "valid_report")
    assert report.run["title"] == "Test Run"
    assert report.run["stats"]["total"] == 2
    assert report.run["stats"]["passed"] == 1


def test_read_report_results_are_dicts():
    report = read_report(FIXTURES / "valid_report")
    signatures = {r["signature"] for r in report.results}
    assert signatures == {"MyTests.PassingTest", "MyTests.FailingTest"}


def test_read_report_missing_dir():
    with pytest.raises(FileNotFoundError):
        read_report(Path("/nonexistent"))


def test_read_report_missing_run_json():
    with pytest.raises(FileNotFoundError):
        read_report(FIXTURES)  # fixtures dir has no run.json
