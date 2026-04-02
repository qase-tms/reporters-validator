import pytest
from pathlib import Path

from reporters_validator.expected_reader import read_expected, ExpectedData

FIXTURES = Path(__file__).parent / "fixtures"


def test_read_expected_returns_expected_data():
    data = read_expected(FIXTURES / "expected" / "simple.yaml")
    assert isinstance(data, ExpectedData)


def test_read_expected_run_stats():
    data = read_expected(FIXTURES / "expected" / "simple.yaml")
    assert data.run["stats"]["total"] == 2
    assert data.run["stats"]["passed"] == 1


def test_read_expected_results_count():
    data = read_expected(FIXTURES / "expected" / "simple.yaml")
    assert len(data.results) == 2


def test_read_expected_result_fields():
    data = read_expected(FIXTURES / "expected" / "simple.yaml")
    passing = next(r for r in data.results if r["signature"] == "MyTests.PassingTest")
    assert passing["status"] == "passed"


def test_read_expected_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_expected(Path("/nonexistent.yaml"))


def test_read_expected_no_run_section():
    """Expected file with only results section is valid."""
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write("results:\n  - signature: test\n    status: passed\n")
        f.flush()
        data = read_expected(Path(f.name))
        assert data.run is None
        assert len(data.results) == 1
