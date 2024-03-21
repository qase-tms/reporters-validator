from dataclasses import dataclass


@dataclass
class Attachment:
    size: int
    file_name: str
    mime: str

    @staticmethod
    def from_json(json: dict) -> 'Attachment':
        return Attachment(size=json["size"], file_name=json["file_name"], mime=json["mime"])


@dataclass
class Step:
    status: int
    attachments: list[Attachment]
    steps: list['Step']

    @staticmethod
    def from_json(json: dict) -> 'Step':
        attachments = []
        if json["attachments"]:
            for attachment in json["attachments"]:
                attachments.append(Attachment.from_json(attachment))

        steps = []
        if json["steps"]:
            for step in json["steps"]:
                steps.append(Step.from_json(step))

        return Step(status=json["status"], attachments=attachments, steps=steps)


@dataclass
class Result:
    case_id: str
    comment: str
    stack_trace: str
    status: str
    attachments: list[Attachment]
    result_steps: list[Step]

    @staticmethod
    def from_json(json: dict) -> 'Result':
        attachments = []
        if json["attachments"]:
            for attachment in json["attachments"]:
                attachments.append(Attachment.from_json(attachment))

        result_steps = []
        if json["result_steps"]:
            for step in json["result_steps"]:
                result_steps.append(Step.from_json(step))

        return Result(case_id=json["case_id"], comment=json["comment"], stack_trace=json["stack_trace"],
                      status=json["status"], attachments=attachments, result_steps=result_steps)
