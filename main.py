from client import QaseClient
from comparer import Comparer
from config import ConfigManager, Config
from getter import QaseGetter
import json

from models.difference import Difference
from models.testcase_info import object_decoder, TestCaseInfo


def get_config():
    cm = ConfigManager()
    return cm.get_config()


def get_qase_client(cfg: Config) -> QaseGetter:
    api_client = QaseClient(cfg.token)
    return QaseGetter(api_client)


def write_json_to_file(data: dict[str, TestCaseInfo], file_path: str):
    json_string = json.dumps(data, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    with open(file_path, 'w') as f:
        f.write(json_string)


def read_json_from_file(file_path: str) -> dict[str, TestCaseInfo]:
    with open(file_path, 'r') as file:
        data = file.read()
    return json.loads(data, object_hook=object_decoder)


def compare_testcase_info(comparer: Comparer, results: dict[str, TestCaseInfo],
                          expected_results: dict[str, TestCaseInfo]):
    keys = expected_results.keys()
    differences = {}
    for key in keys:
        if key not in results:
            differences[key] = Difference(field="Key not found", actual="None", expected="None")
            continue
        diffs = comparer.compare_testcase_info(results[key], expected_results[key])
        if len(diffs) != 0:
            differences[key] = diffs
    return differences


config = get_config()
qase = get_qase_client(config)
results = qase.get_results(config.project_code, config.testrun_id)

if config.mode == "prepare":
    write_json_to_file(results, config.output)
    exit(0)

expected_results = read_json_from_file(config.input)

comparer = Comparer()
diffs = compare_testcase_info(comparer, results, expected_results)

if len(diffs) != 0:
    print(json.dumps(diffs, default=lambda o: o.__dict__, sort_keys=True, indent=4))
    exit(1)
