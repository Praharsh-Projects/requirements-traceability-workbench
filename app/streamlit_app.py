import streamlit as st

from app.models import Requirement, TestCase
from app.store import load_requirements, load_test_cases, persist, seed_if_empty
from app.traceability import (
    build_requirement_table,
    build_test_table,
    build_traceability_matrix,
    coverage_summary,
    orphan_requirements,
    orphan_test_cases,
)


SEED = {
    "requirements": [
        {
            "id": "SYS-001",
            "level": "system",
            "title": "Requirements hierarchy",
            "statement": "The system shall support a hierarchical requirements model with parent-child relationships.",
            "parent_id": None,
            "rationale": "Keeps system and software requirements structured.",
            "status": "Approved",
            "linked_tests": ["TC-001"],
        },
        {
            "id": "SWE-001",
            "level": "software",
            "title": "Requirement versioning",
            "statement": "The system shall retain version history for each requirement update.",
            "parent_id": "SYS-001",
            "rationale": "Supports review and traceability.",
            "status": "Reviewed",
            "linked_tests": ["TC-002"],
        },
        {
            "id": "SWE-002",
            "level": "software",
            "title": "Traceability matrix export",
            "statement": "The system shall export a requirements-to-test traceability matrix.",
            "parent_id": "SYS-001",
            "rationale": "Used for verification planning.",
            "status": "Draft",
            "linked_tests": ["TC-003"],
        },
    ],
    "test_cases": [
        {
            "id": "TC-001",
            "title": "Create hierarchy",
            "steps": ["Create a system requirement", "Add a child software requirement"],
            "expected_result": "The child requirement is linked to the parent.",
            "linked_requirement_ids": ["SYS-001"],
            "priority": "High",
            "status": "Pass",
        },
        {
            "id": "TC-002",
            "title": "Retain version history",
            "steps": ["Update requirement text", "Check version log"],
            "expected_result": "A previous version is preserved.",
            "linked_requirement_ids": ["SWE-001"],
            "priority": "High",
            "status": "Pass",
        },
        {
            "id": "TC-003",
            "title": "Export trace matrix",
            "steps": ["Open matrix view", "Export report"],
            "expected_result": "A traceability matrix is generated.",
            "linked_requirement_ids": ["SWE-002"],
            "priority": "Medium",
            "status": "Pass",
        },
    ],
}


st.set_page_config(page_title="Requirements Traceability Workbench", layout="wide")
st.title("Requirements Traceability Workbench")
st.caption("Structured requirements hierarchy, traceability, and verification coverage.")

seed_if_empty(SEED)
requirements = load_requirements()
test_cases = load_test_cases()
matrix = build_traceability_matrix(requirements, test_cases)
summary = coverage_summary(matrix)

metric1, metric2, metric3, metric4 = st.columns(4)
metric1.metric("Requirements", len(requirements))
metric2.metric("Test cases", len(test_cases))
metric3.metric("Covered", summary["covered"])
metric4.metric("Coverage", f"{summary['coverage_pct']}%")

left, right = st.columns(2)
with left:
    st.subheader("Requirements")
    st.dataframe(build_requirement_table(requirements), use_container_width=True, hide_index=True)

with right:
    st.subheader("Test cases")
    st.dataframe(build_test_table(test_cases), use_container_width=True, hide_index=True)

st.subheader("Traceability matrix")
st.dataframe(matrix, use_container_width=True, hide_index=True)

st.subheader("Gap analysis")
gap_left, gap_right = st.columns(2)
with gap_left:
    st.write("Orphan requirements:", orphan_requirements(requirements, test_cases))
with gap_right:
    st.write("Orphan test cases:", orphan_test_cases(requirements, test_cases))

st.subheader("Add a requirement")
with st.form("add_requirement"):
    rid = st.text_input("Requirement ID", value="SWE-003")
    level = st.selectbox("Level", ["system", "software"])
    title = st.text_input("Title", value="New requirement")
    statement = st.text_area("Statement", value="The system shall...")
    parent_id = st.text_input("Parent ID", value="SYS-001")
    rationale = st.text_area("Rationale", value="Added for traceability.")
    status = st.selectbox("Status", ["Draft", "Reviewed", "Approved"])
    submitted = st.form_submit_button("Save requirement")
    if submitted:
        requirements.append(
            Requirement(
                id=rid,
                level=level,
                title=title,
                statement=statement,
                parent_id=parent_id or None,
                rationale=rationale,
                status=status,
            )
        )
        persist(requirements, test_cases)
        st.success("Requirement saved. Refresh the page to see the updated matrix.")

st.markdown(
    """
    ### Notes
    - The project is intentionally simple and readable.
    - It demonstrates the same ideas as a structured requirements tool: hierarchy, versioning, traceability, and verification coverage.
    - It is not a production requirements management platform.
    """
)
