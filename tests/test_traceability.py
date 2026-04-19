import unittest

from app.models import Requirement, TestCase
from app.traceability import build_traceability_matrix, coverage_summary, orphan_requirements, orphan_test_cases


def sample():
    requirements = [
        Requirement(id="SYS-001", level="system", title="Hierarchy", statement="Support parent-child links"),
        Requirement(id="SWE-001", level="software", title="Export", statement="Export matrix"),
    ]
    test_cases = [
        TestCase(id="TC-001", title="Hierarchy", steps=["a"], expected_result="ok", linked_requirement_ids=["SYS-001"]),
    ]
    return requirements, test_cases


class TraceabilityTests(unittest.TestCase):
    def test_coverage_summary(self):
        reqs, tests = sample()
        matrix = build_traceability_matrix(reqs, tests)
        summary = coverage_summary(matrix)
        self.assertEqual(summary["total"], 2)
        self.assertEqual(summary["covered"], 1)

    def test_orphan_detection(self):
        reqs, tests = sample()
        self.assertEqual(orphan_requirements(reqs, tests), ["SWE-001"])
        self.assertEqual(orphan_test_cases(reqs, tests), [])
