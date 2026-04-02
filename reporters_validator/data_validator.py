from dataclasses import dataclass
from pathlib import Path

from reporters_validator.report_reader import read_report
from reporters_validator.expected_reader import read_expected
from reporters_validator.matcher import match_results


@dataclass
class DataValidationError:
    result_signature: str
    field: str
    expected: str
    actual: str
    message: str = ""

    def __str__(self):
        if self.message:
            return f"[{self.result_signature}] {self.message}"
        return f"[{self.result_signature}] {self.field}: expected {self.expected!r}, got {self.actual!r}"


def validate_data(report_dir: Path, expected_path: Path) -> list[DataValidationError]:
    """Validate report data against expected values using partial matching."""
    report = read_report(report_dir)
    expected = read_expected(expected_path)
    errors: list[DataValidationError] = []

    # Validate run-level fields
    if expected.run:
        errors.extend(_compare_dict(report.run, expected.run, prefix="run", signature="run"))

    # Validate results
    if expected.results:
        matches = match_results(report.results, expected.results)
        for match in matches:
            sig = match.expected.get("signature") or match.expected.get("title") or "unknown"

            if match.actual is None:
                errors.append(DataValidationError(
                    result_signature=sig, field="", expected="", actual="",
                    message=f"Result not found in actual report: {sig}",
                ))
                continue

            # "status" shorthand maps to execution.status
            exp = dict(match.expected)
            if "status" in exp and "execution" not in exp:
                exp.setdefault("execution", {})["status"] = exp.pop("status")
            elif "status" in exp and "execution" in exp:
                exp["execution"].setdefault("status", exp.pop("status"))
                if "status" in exp:
                    del exp["status"]

            # Remove matcher keys from comparison
            for key in ("signature", "title"):
                exp.pop(key, None)

            errors.extend(_compare_dict(match.actual, exp, prefix="", signature=sig))

    return errors


def _compare_dict(actual: dict, expected: dict, prefix: str, signature: str) -> list[DataValidationError]:
    """Recursively compare actual dict against expected dict (partial matching)."""
    errors: list[DataValidationError] = []

    for key, exp_value in expected.items():
        field_path = f"{prefix}.{key}" if prefix else key
        act_value = actual.get(key)

        if isinstance(exp_value, dict) and isinstance(act_value, dict):
            errors.extend(_compare_dict(act_value, exp_value, field_path, signature))
        elif isinstance(exp_value, list) and isinstance(act_value, list):
            errors.extend(_compare_list(act_value, exp_value, field_path, signature))
        elif isinstance(exp_value, dict) and act_value is None:
            errors.append(DataValidationError(
                result_signature=signature, field=field_path,
                expected=str(exp_value), actual="None",
                message=f"Expected object at {field_path}, got None",
            ))
        elif exp_value != act_value:
            errors.append(DataValidationError(
                result_signature=signature, field=field_path,
                expected=str(exp_value), actual=str(act_value),
            ))

    return errors


def _compare_list(actual: list, expected: list, prefix: str, signature: str) -> list[DataValidationError]:
    """Compare lists element by element (order matters for steps, suites)."""
    errors: list[DataValidationError] = []

    if len(actual) < len(expected):
        errors.append(DataValidationError(
            result_signature=signature, field=f"{prefix}.length",
            expected=str(len(expected)), actual=str(len(actual)),
        ))
        return errors

    for i, exp_item in enumerate(expected):
        field_path = f"{prefix}[{i}]"
        if i >= len(actual):
            break
        act_item = actual[i]

        if isinstance(exp_item, dict) and isinstance(act_item, dict):
            errors.extend(_compare_dict(act_item, exp_item, field_path, signature))
        elif exp_item != act_item:
            errors.append(DataValidationError(
                result_signature=signature, field=field_path,
                expected=str(exp_item), actual=str(act_item),
            ))

    return errors
