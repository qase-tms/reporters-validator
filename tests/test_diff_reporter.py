from reporters_validator.diff_reporter import format_errors
from reporters_validator.schema_validator import SchemaValidationError
from reporters_validator.data_validator import DataValidationError


def test_format_empty_errors():
    output = format_errors([], [])
    assert output == ""


def test_format_schema_errors():
    errors = [
        SchemaValidationError(file="run.json", path="$.title", message="123 is not of type 'string'"),
    ]
    output = format_errors(schema_errors=errors, data_errors=[])
    assert "run.json" in output
    assert "title" in output
    assert "string" in output


def test_format_data_errors():
    errors = [
        DataValidationError(
            result_signature="A.Test", field="execution.status",
            expected="passed", actual="failed",
        ),
    ]
    output = format_errors(schema_errors=[], data_errors=errors)
    assert "A.Test" in output
    assert "passed" in output
    assert "failed" in output


def test_format_mixed_errors():
    schema_errors = [
        SchemaValidationError(file="run.json", path="$", message="bad"),
    ]
    data_errors = [
        DataValidationError(result_signature="X", field="f", expected="a", actual="b"),
    ]
    output = format_errors(schema_errors, data_errors)
    assert "schema" in output.lower()
    assert "data" in output.lower()
