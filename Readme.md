# Qase Reporters Validator

Offline integration testing tool for Qase reporters. Validates local JSON reports
(generated in `mode=report`) against YAML schemas and expected data files.

## Installation

```bash
pip install git+https://github.com/qase-tms/reporters-validator.git
```

## Usage

### Validate

Full validation (schema + data):

```bash
reporters-validator validate \
  --report-dir ./build/qase-report \
  --schema-dir ./specs/report/schemas \
  --expected ./expected/my-tests.yaml
```

Schema-only validation:

```bash
reporters-validator validate \
  --report-dir ./build/qase-report \
  --schema-dir ./specs/report/schemas \
  --schema-only
```

### Prepare

Generate an expected file from an existing report:

```bash
reporters-validator prepare \
  --report-dir ./build/qase-report \
  --output ./expected/my-tests.yaml
```

Then review and edit the generated file — remove fields you don't want to check
and adjust expected values.

### Exit Codes

- `0` — all validations passed
- `1` — validation failures
- `2` — invalid arguments

## CI Integration

```yaml
steps:
  - uses: actions/setup-python@v5
    with:
      python-version: '3.12'

  - name: Install validator
    run: pip install git+https://github.com/qase-tms/reporters-validator.git

  - name: Run tests in report mode
    run: QASE_MODE=report dotnet test  # or pytest, jest, etc.

  - name: Validate report
    run: |
      reporters-validator validate \
        --report-dir ./build/qase-report \
        --schema-dir ./specs/report/schemas \
        --expected ./expected/my-tests.yaml
```

## Expected File Format

```yaml
run:
  stats:
    total: 5
    passed: 3
    failed: 2

results:
  - signature: "MyTests.PassingTest"
    status: "passed"
    relations:
      suite:
        data:
          - title: "MyTests"

  - signature: "MyTests.FailingTest"
    status: "failed"
    fields:
      severity: "critical"
```

Only specified fields are checked (partial matching). Dynamic fields
(id, timestamps, duration) are ignored unless explicitly included.

## Development

```bash
git clone git@github.com:qase-tms/reporters-validator.git
cd reporters-validator
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -v
```
