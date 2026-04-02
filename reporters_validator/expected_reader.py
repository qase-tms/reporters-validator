import yaml
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ExpectedData:
    run: dict | None = None
    results: list[dict] = field(default_factory=list)


def read_expected(expected_path: Path) -> ExpectedData:
    """Read expected results from a YAML file."""
    expected_path = Path(expected_path)
    if not expected_path.is_file():
        raise FileNotFoundError(f"Expected file not found: {expected_path}")

    with open(expected_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return ExpectedData(
        run=data.get("run"),
        results=data.get("results", []),
    )
