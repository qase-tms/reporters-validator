from dataclasses import dataclass

from models.result import Result
from models.testcase import TestCase


@dataclass
class TestCaseInfo:
    case: TestCase
    result: Result

    @staticmethod
    def from_json(json: dict) -> 'TestCaseInfo':
        case = TestCase.from_json(json["case"])
        result = Result.from_json(json["result"])
        return TestCaseInfo(case=case, result=result)


def object_decoder(obj):
    if 'case' in obj and 'result' in obj:
        return TestCaseInfo.from_json(obj)
    return obj
