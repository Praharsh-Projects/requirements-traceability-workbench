from __future__ import annotations

from .models import Requirement, TestCase


def build_requirement_table(requirements: list[Requirement]) -> list[dict]:
    return [r.to_dict() for r in requirements]


def build_test_table(test_cases: list[TestCase]) -> list[dict]:
    return [t.to_dict() for t in test_cases]


def build_traceability_matrix(requirements: list[Requirement], test_cases: list[TestCase]) -> list[dict]:
    rows: list[dict] = []
    for req in requirements:
        linked = [case.id for case in test_cases if req.id in case.linked_requirement_ids]
        rows.append(
            {
                "requirement_id": req.id,
                "level": req.level,
                "title": req.title,
                "status": req.status,
                "linked_tests": ", ".join(linked) if linked else "",
                "coverage_status": "Covered" if linked else "Uncovered",
            }
        )
    return rows


def coverage_summary(matrix: list[dict]) -> dict:
    if not matrix:
        return {"total": 0, "covered": 0, "coverage_pct": 0.0}
    total = len(matrix)
    covered = sum(1 for row in matrix if row["coverage_status"] == "Covered")
    return {
        "total": total,
        "covered": covered,
        "coverage_pct": round((covered / total) * 100, 1),
    }


def orphan_requirements(requirements: list[Requirement], test_cases: list[TestCase]) -> list[str]:
    linked = {req_id for case in test_cases for req_id in case.linked_requirement_ids}
    return [req.id for req in requirements if req.id not in linked]


def orphan_test_cases(requirements: list[Requirement], test_cases: list[TestCase]) -> list[str]:
    valid = {req.id for req in requirements}
    return [case.id for case in test_cases if not set(case.linked_requirement_ids).intersection(valid)]
