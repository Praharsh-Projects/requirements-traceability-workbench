from dataclasses import dataclass, field, asdict
from typing import Literal


RequirementLevel = Literal["system", "software"]
RequirementStatus = Literal["Draft", "Reviewed", "Approved"]
TestStatus = Literal["Not Run", "Pass", "Fail"]


@dataclass
class Requirement:
    id: str
    level: RequirementLevel
    title: str
    statement: str
    parent_id: str | None = None
    rationale: str = ""
    status: RequirementStatus = "Draft"
    linked_tests: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class TestCase:
    id: str
    title: str
    steps: list[str]
    expected_result: str
    linked_requirement_ids: list[str] = field(default_factory=list)
    priority: str = "Medium"
    status: TestStatus = "Not Run"

    def to_dict(self) -> dict:
        return asdict(self)
