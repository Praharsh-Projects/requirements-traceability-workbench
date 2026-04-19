from __future__ import annotations

import json
from pathlib import Path

from .models import Requirement, TestCase


STORE_PATH = Path("data/store.json")


def _default_payload() -> dict:
    return {"requirements": [], "test_cases": []}


def load_store() -> dict:
    if not STORE_PATH.exists():
        return _default_payload()
    return json.loads(STORE_PATH.read_text(encoding="utf-8"))


def save_store(payload: dict) -> None:
    STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STORE_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_requirements() -> list[Requirement]:
    payload = load_store()
    return [Requirement(**item) for item in payload.get("requirements", [])]


def load_test_cases() -> list[TestCase]:
    payload = load_store()
    return [TestCase(**item) for item in payload.get("test_cases", [])]


def persist(requirements: list[Requirement], test_cases: list[TestCase]) -> None:
    payload = {
        "requirements": [req.to_dict() for req in requirements],
        "test_cases": [case.to_dict() for case in test_cases],
    }
    save_store(payload)


def seed_if_empty(seed_payload: dict) -> None:
    if not STORE_PATH.exists():
        save_store(seed_payload)
