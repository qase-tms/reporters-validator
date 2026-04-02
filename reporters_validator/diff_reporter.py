from reporters_validator.schema_validator import SchemaValidationError
from reporters_validator.data_validator import DataValidationError


def format_errors(
    schema_errors: list[SchemaValidationError],
    data_errors: list[DataValidationError],
) -> str:
    """Format validation errors as a human-readable report."""
    if not schema_errors and not data_errors:
        return ""

    lines: list[str] = []

    if schema_errors:
        lines.append("Schema validation errors:")
        lines.append("")
        for err in schema_errors:
            lines.append(f"  FAIL {err.file}: {err.path}")
            lines.append(f"    {err.message}")
        lines.append("")

    if data_errors:
        lines.append("Data validation errors:")
        lines.append("")
        for err in data_errors:
            lines.append(f"  FAIL [{err.result_signature}]")
            if err.message:
                lines.append(f"    {err.message}")
            else:
                lines.append(f"    {err.field}: expected {err.expected!r}, got {err.actual!r}")
        lines.append("")

    total = len(schema_errors) + len(data_errors)
    lines.append(f"Total: {total} error(s)")

    return "\n".join(lines)
