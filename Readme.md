# Qase reporter's validator

This validator is used to validate the Qase reporter's functionality. It compares the expected results of the reporter
with the results of the Qase API.

## Installation

Run the following command to install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

This tools has the following mode:

- `validate` - validates the reporter's results with the Qase API
- `prepare` - prepares the expected results for the reporter

### Validate

To validate the reporter's results with the Qase API, run the following command:

```bash
python main.py --mode validate --project-code <project_code> --token <token> --testrun-id <testrun_id> --input <input_file>
```

Where:

- `project-code` - the code of the project in Qase
- `token` - the token to access the Qase API
- `testrun-id` - the id of the test run in Qase
- `input` - the file with the excepted results

### Prepare

To prepare the expected results for the reporter, run the following command:

```bash
python main.py --mode prepare --project-code <project_code> --token <token> --testrun-id <testrun_id> --output <output_file>
```

Where:

- `project-code` - the code of the project in Qase
- `token` - the token to access the Qase API
- `testrun-id` - the id of the test run in Qase
- `output` - the file to save the expected results
