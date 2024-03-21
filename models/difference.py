from dataclasses import dataclass


@dataclass
class Difference:
    field: str
    actual: str
    expected: str
