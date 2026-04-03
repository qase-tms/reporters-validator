import json
from dataclasses import dataclass
from pathlib import Path

import jsonschema

from reporters_validator.report_reader import read_report
from reporters_validator.schema_loader import load_schema


@dataclass
class SchemaValidationError:
    file: str
    path: str
    message: str

    def __str__(self):
        return f"{self.file}: {self.path} — {self.message}"


def validate_schema(report_dir: Path, schema_dir: Path) -> list[SchemaValidationError]:
    """Validate report JSON files against YAML schemas. Returns list of errors (empty = valid)."""
    report_dir = Path(report_dir)
    schema_dir = Path(schema_dir)
    errors = []

    report = read_report(report_dir)

    # Validate run.json
    run_schema = load_schema(schema_dir / "root.yaml")
    errors.extend(_validate_json(report.run, run_schema, "run.json"))

    # Validate each result
    result_schema = load_schema(schema_dir / "result.yaml")
    results_dir = report_dir / "results"
    if results_dir.is_dir():
        for result_file in sorted(results_dir.glob("*.json")):
            with open(result_file, "r", encoding="utf-8-sig") as f:
                result_data = json.load(f)
            errors.extend(_validate_json(result_data, result_schema, f"results/{result_file.name}"))

    return errors


def _validate_json(data: dict, schema: dict, filename: str) -> list[SchemaValidationError]:
    """Validate a single JSON object against a JSON Schema."""
    errors = []
    validator = jsonschema.Draft7Validator(schema)
    for error in validator.iter_errors(data):
        path = "$." + ".".join(str(p) for p in error.absolute_path) if error.absolute_path else "$"
        errors.append(SchemaValidationError(
            file=filename,
            path=path,
            message=error.message,
        ))
    return errors
