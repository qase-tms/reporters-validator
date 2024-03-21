import certifi
from qaseio import TestStepResult
from qaseio.api.cases_api import CasesApi
from qaseio.api_client import ApiClient
from qaseio.configuration import Configuration
from qaseio.api.results_api import ResultsApi

from models.result import Result, Attachment, Step
from models.testcase import TestCase, TestCaseStep


class QaseClient:
    def __init__(self, token: str):
        configuration = Configuration()
        configuration.api_key['TokenAuth'] = token
        configuration.host = 'https://api.qase.io/v1'
        configuration.ssl_ca_cert = certifi.where()

        self.__client = ApiClient(configuration)

    def get_result_hashes(self, project_code: str, run_id: str) -> list[str]:
        api = ResultsApi(self.__client)
        results = api.get_results(project_code, run=run_id, limit=50)
        return [result.hash for result in results.result.entities]

    def get_result(self, project_code: str, hash: str) -> Result:
        api = ResultsApi(self.__client)
        result = api.get_result(project_code, hash).result
        return Result(case_id=result.case_id, comment=result.comment, stack_trace=result.stacktrace,
                      status=result.status,
                      attachments=self.__convert_attachments(result.attachments),
                      result_steps=self.__convert_steps(result.steps))

    def get_test_case(self, project_code: str, case_id: str) -> TestCase:
        api = CasesApi(self.__client)
        case = api.get_case(project_code, case_id).result
        return TestCase(title=case.title, description=case.description, preconditions=case.preconditions,
                        postconditions=case.postconditions, severity=case.severity, priority=case.priority,
                        layer=case.layer, tags=self.__convert_tags(case.tags), status=case.status,
                        steps=self.__convert_testcase_steps(case.steps))

    def __convert_steps(self, steps: list[TestStepResult]) -> list[Step]:
        result = []
        if steps is None:
            return result

        for step in steps:
            result.append(Step(status=step.status,
                               attachments=self.__convert_attachments(step.attachments),
                               steps=self.__convert_children_steps(step.steps)))
        return result

    def __convert_children_steps(self, steps: list[dict]) -> list[Step]:
        result = []
        if steps is None:
            return result

        for step in steps:
            result.append(Step(status=step['status'],
                               attachments=self.__convert_attachments(step['attachments']),
                               steps=[]))
        return result

    @staticmethod
    def __convert_attachments(attachments: list) -> list[Attachment]:
        result = []
        if attachments is None:
            return result

        for attach in attachments:
            result.append(Attachment(size=attach.size, mime=attach.mime, file_name=attach.filename))
        return result

    @staticmethod
    def __convert_tags(tags: list) -> list[str]:
        result = []
        if tags is None:
            return result

        for tag in tags:
            result.append(tag)
        return result

    def __convert_testcase_steps(self, steps: list) -> list[TestCaseStep]:
        result = []
        if steps is None:
            return result

        for step in steps:
            result.append(TestCaseStep(action=step.action, steps=self.__convert_children_testcase_steps(step.steps)))
        return result

    def __convert_children_testcase_steps(self, steps: list[dict]) -> list[TestCaseStep]:
        result = []
        if steps is None:
            return result

        for step in steps:
            result.append(
                TestCaseStep(action=step['action'], steps=self.__convert_children_testcase_steps(step['steps'])))
        return result
