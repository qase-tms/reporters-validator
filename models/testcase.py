from dataclasses import dataclass


@dataclass
class TestCaseStep:
    action: str
    steps: list['TestCaseStep']

    @staticmethod
    def from_json(json: dict) -> 'TestCaseStep':
        steps = []
        if json["steps"]:
            for step in json["steps"]:
                steps.append(TestCaseStep.from_json(step))

        return TestCaseStep(action=json["action"], steps=steps)


@dataclass
class TestCase:
    title: str
    description: str
    preconditions: str
    postconditions: str
    severity: int
    priority: int
    layer: int
    tags: list[str]
    status: int
    steps: list[TestCaseStep]

    @staticmethod
    def from_json(json: dict) -> 'TestCase':
        steps = []
        if json["steps"]:
            for step in json["steps"]:
                steps.append(TestCaseStep.from_json(step))

        return TestCase(title=json["title"], description=json["description"], preconditions=json["preconditions"],
                        postconditions=json["postconditions"], severity=json["severity"], priority=json["priority"],
                        layer=json["layer"], tags=json["tags"], status=json["status"], steps=steps)
