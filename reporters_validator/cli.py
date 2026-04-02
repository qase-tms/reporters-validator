import sys

import click

from reporters_validator.schema_validator import validate_schema
from reporters_validator.data_validator import validate_data
from reporters_validator.diff_reporter import format_errors


@click.group()
def main():
    """Qase reporters validator — offline integration testing tool."""
    pass


@main.command()
@click.option("--report-dir", required=True, type=click.Path(exists=True), help="Path to report directory (contains run.json + results/)")
@click.option("--schema-dir", required=True, type=click.Path(exists=True), help="Path to YAML schema directory")
@click.option("--expected", type=click.Path(exists=True), help="Path to expected results YAML file")
@click.option("--schema-only", is_flag=True, default=False, help="Only validate schema, skip data validation")
def validate(report_dir, schema_dir, expected, schema_only):
    """Validate a report against schema and expected data."""
    from pathlib import Path

    report_dir = Path(report_dir)
    schema_dir = Path(schema_dir)

    if not schema_only and not expected:
        click.echo("Error: --expected is required unless --schema-only is used.", err=True)
        sys.exit(2)

    # Schema validation
    schema_errors = validate_schema(report_dir, schema_dir)

    # Data validation
    data_errors = []
    if not schema_only and expected:
        data_errors = validate_data(report_dir, Path(expected))

    # Report
    if schema_errors or data_errors:
        output = format_errors(schema_errors, data_errors)
        click.echo(output)
        sys.exit(1)

    click.echo("All validations passed.")


@main.command()
@click.option("--report-dir", required=True, type=click.Path(exists=True), help="Path to report directory")
@click.option("--output", required=True, type=click.Path(), help="Output path for expected YAML file")
def prepare(report_dir, output):
    """Generate expected YAML file from an existing report."""
    from pathlib import Path
    from reporters_validator.prepare import generate_expected, write_expected

    data = generate_expected(Path(report_dir))
    write_expected(data, Path(output))
    click.echo(f"Expected file written to: {output}")
