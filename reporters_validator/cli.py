import click


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
    click.echo("validate: not implemented yet")


@main.command()
@click.option("--report-dir", required=True, type=click.Path(exists=True), help="Path to report directory")
@click.option("--output", required=True, type=click.Path(), help="Output path for expected YAML file")
def prepare(report_dir, output):
    """Generate expected YAML file from an existing report."""
    click.echo("prepare: not implemented yet")
