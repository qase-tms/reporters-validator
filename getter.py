from client import QaseClient
from models.testcase_info import TestCaseInfo


class QaseGetter:
    def __init__(self, client: QaseClient):
        self.__api_client = client

    def get_results(self, project_code: str, run_id: str) -> dict[str, TestCaseInfo]:
        hashes = self.__api_client.get_result_hashes(project_code, run_id)

        results = {}
        for hash in hashes:
            result = self.__api_client.get_result(project_code, hash)
            case = self.__api_client.get_test_case(project_code, result.case_id)

            results[str(result.case_id)] = TestCaseInfo(case=case, result=result)

        return results
