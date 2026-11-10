#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Validate a result-elaboration report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


FORBIDDEN_HOOK_TERMS = [
    "run_discovery_marathon",
    "discovery marathon jobs",
    "branch schedulers",
    "target active pointers",
    "long-horizon discovery queues",
]

GENERIC_ACCEPTANCE_CRITERIA = {
    "The marker can be removed and replaced by final paper text without weakening the theorem statement or hiding proof debt.",
    "All coefficient formulas include definitions, assumptions, validity regime, and explicit remainder or bound.",
}


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    report_path = args.report.expanduser().resolve()
    data = json.loads(report_path.read_text(encoding="utf-8"))
    require(data.get("schema") == "abducer.results_elaboration.v1", "unexpected schema")
    context = data.get("context", {})
    require(context.get("title"), "missing title")
    require(context.get("bounded_contribution"), "missing bounded contribution")
    require(len(context.get("explicit_non_claims", [])) >= 3, "missing explicit non-claims")
    structure = data.get("source_structure", {})
    slots = structure.get("slots", [])
    todos = data.get("todos", [])
    require(len(slots) >= 6, "expected at least six result expansion slots")
    slot_labels = {slot.get("label") for slot in slots}
    todo_markers = {todo.get("source_marker") for todo in todos}
    missing = sorted(label for label in slot_labels if label not in todo_markers)
    require(not missing, f"slots without TODOs: {missing}")
    workflow = data.get("workflow", {})
    require(workflow.get("independent_from_discovery") is True, "workflow must be independent from discovery")
    hooks = workflow.get("local_hooks", [])
    require(len(hooks) >= 5, "missing local hook coverage")
    forbidden = " ".join(workflow.get("forbidden_couplings", [])).lower()
    for term in FORBIDDEN_HOOK_TERMS[1:]:
        require(term in forbidden, f"forbidden coupling not stated: {term}")
    for todo in todos:
        require(todo.get("target_section"), f"{todo.get('todo_id')} missing target section")
        require(todo.get("mathematical_object"), f"{todo.get('todo_id')} missing mathematical object")
        require("depends_on" in todo, f"{todo.get('todo_id')} missing dependency field")
        require(todo.get("required_inputs"), f"{todo.get('todo_id')} missing required inputs")
        require(len(todo.get("subtasks", [])) >= 3, f"{todo.get('todo_id')} needs at least three concrete subtasks")
        require(todo.get("action"), f"{todo.get('todo_id')} missing action")
        require(todo.get("expected_artifact"), f"{todo.get('todo_id')} missing expected artifact")
        require(todo.get("acceptance_criterion"), f"{todo.get('todo_id')} missing acceptance criterion")
        require(
            todo.get("acceptance_criterion") not in GENERIC_ACCEPTANCE_CRITERIA,
            f"{todo.get('todo_id')} has generic acceptance criterion",
        )
        require(todo.get("limitation_addressed"), f"{todo.get('todo_id')} missing limitation addressed")
        require(todo.get("paper_insertion_target"), f"{todo.get('todo_id')} missing paper insertion target")
        require(todo.get("validation_handoff"), f"{todo.get('todo_id')} missing validation handoff")
        require(todo.get("stop_or_quarantine_condition"), f"{todo.get('todo_id')} missing stop/quarantine condition")
        require(
            "marker cannot be discharged" not in todo.get("stop_or_quarantine_condition", ""),
            f"{todo.get('todo_id')} has generic stop/quarantine condition",
        )
        require(todo.get("recommended_skills"), f"{todo.get('todo_id')} missing skill handoff")
        require(todo.get("narrative_consequence"), f"{todo.get('todo_id')} missing narrative consequence")
    review = data.get("todo_review", {})
    require(len(review.get("limitations_found", [])) >= 2, "missing TODO limitation review")
    require(len(review.get("repairs_applied", [])) >= 2, "missing TODO repair summary")
    narrative = data.get("narrative_integration", {})
    require(len(narrative.get("spine", [])) >= 3, "missing narrative spine")
    print(f"validated {len(slots)} slots and {len(todos)} TODOs in {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
