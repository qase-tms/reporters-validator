from models.difference import Difference
from models.result import Attachment, Step, Result
from models.testcase import TestCase, TestCaseStep
from models.testcase_info import TestCaseInfo


class Comparer:

    def compare_testcase_info(self, actual: TestCaseInfo, excepted: TestCaseInfo) -> list[Difference]:
        return (self.__compare_testcase(actual.case, excepted.case)
                + self.__compare_results(actual.result, excepted.result))

    def __compare_testcase(self, actual: TestCase, excepted: TestCase) -> list[Difference]:
        differences = []
        if actual.title != excepted.title:
            differences.append(
                Difference(field="title", actual=actual.title, expected=excepted.title))

        if actual.description != excepted.description:
            differences.append(
                Difference(field="description", actual=actual.description, expected=excepted.description))

        if actual.preconditions != excepted.preconditions:
            differences.append(
                Difference(field="preconditions", actual=actual.preconditions, expected=excepted.preconditions))

        if actual.postconditions != excepted.postconditions:
            differences.append(
                Difference(field="postconditions", actual=actual.postconditions, expected=excepted.postconditions))

        if actual.severity != excepted.severity:
            differences.append(
                Difference(field="severity", actual=actual.severity, expected=excepted.severity))

        if actual.priority != excepted.priority:
            differences.append(
                Difference(field="priority", actual=actual.priority, expected=excepted.priority))

        if actual.layer != excepted.layer:
            differences.append(
                Difference(field="layer", actual=actual.layer, expected=excepted.layer))

        if actual.tags != excepted.tags:
            differences.append(
                Difference(field="tags", actual=actual.tags, expected=excepted.tags))

        if actual.status != excepted.status:
            differences.append(
                Difference(field="status", actual=actual.status, expected=excepted.status))

        diffs = self.__compare_testcase_steps(actual.steps, excepted.steps)
        differences.extend(diffs)

        return differences

    def __compare_testcase_steps(self, actual: list[TestCaseStep], excepted: list[TestCaseStep]) -> list[Difference]:
        differences = []
        if len(actual) != len(excepted):
            differences.append(Difference(field="Step count", actual=len(actual), expected=len(excepted)))
            return differences

        for i in range(len(actual)):
            if actual[i].action != excepted[i].action:
                differences.append(
                    Difference(field=f"Step {i}: action", actual=actual[i].action, expected=excepted[i].action))

            diffs = self.__compare_testcase_steps(actual[i].steps, excepted[i].steps)
            differences.extend(diffs)

        return differences

    @staticmethod
    def __compare_attachments(actual: list[Attachment], excepted: list[Attachment]) -> list[Difference]:
        differences = []
        if len(actual) != len(excepted):
            differences.append(Difference(field="Attachment count", actual=len(actual), expected=len(excepted)))
            return differences

        for i in range(len(actual)):
            if actual[i].size != excepted[i].size:
                differences.append(
                    Difference(field=f"Attachment {i}: size", actual=actual[i].size, expected=excepted[i].size))

            if actual[i].file_name != excepted[i].file_name:
                differences.append(
                    Difference(field=f"Attachment {i}: file_name", actual=actual[i].file_name,
                               expected=excepted[i].file_name))

            if actual[i].mime != excepted[i].mime:
                differences.append(
                    Difference(field=f"Attachment {i}: mime", actual=actual[i].mime, expected=excepted[i].mime))

        return differences

    def __compare_steps(self, actual: list[Step], excepted: list[Step]) -> list[Difference]:
        differences = []

        if actual is None or excepted is None:
            differences.append(Difference(field="Step count", actual=actual, expected=excepted))
            return differences

        if len(actual) != len(excepted):
            differences.append(Difference(field="Step count", actual=len(actual), expected=len(excepted)))
            return differences

        for i in range(len(actual)):
            if actual[i].status != excepted[i].status:
                differences.append(
                    Difference(field="status", actual=actual[i].status, expected=excepted[i].status))

            diffs_a = self.__compare_attachments(actual[i].attachments, excepted[i].attachments)
            differences.extend(diffs_a)

            diffs_s = self.__compare_steps(actual[i].steps, excepted[i].steps)
            differences.extend(diffs_s)

        return differences

    def __compare_results(self, actual: Result, excepted: Result) -> list[Difference]:
        differences = []

        if actual.case_id != excepted.case_id:
            differences.append(
                Difference(field="case_id", actual=actual.case_id, expected=excepted.case_id))

        if actual.comment != excepted.comment:
            differences.append(
                Difference(field="comment", actual=actual.comment, expected=excepted.comment))

        if actual.stack_trace != excepted.stack_trace:
            differences.append(
                Difference(field="stack_trace", actual=actual.stack_trace,
                           expected=excepted.stack_trace))

        if actual.status != excepted.status:
            differences.append(
                Difference(field="status", actual=actual.status, expected=excepted.status))

        diffs_a = self.__compare_attachments(actual.attachments, excepted.attachments)
        differences.extend(diffs_a)

        diffs_s = self.__compare_steps(actual.result_steps, excepted.result_steps)
        differences.extend(diffs_s)

        return differences
