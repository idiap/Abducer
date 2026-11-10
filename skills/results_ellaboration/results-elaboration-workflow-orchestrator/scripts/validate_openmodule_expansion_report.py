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
"""Validate an open-module result-elaboration report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    path = args.report.expanduser().resolve()
    data = json.loads(path.read_text(encoding="utf-8"))
    require(data.get("schema") == "abducer.results_elaboration.openmodule.v1", "unexpected schema")
    context = data.get("context", {})
    require("Finite-cutoff SU(2)" in context.get("bounded_contribution", ""), "missing Route A bounded contribution")
    require(len(context.get("explicit_non_claims", [])) >= 4, "missing explicit non-claims")
    modules = data.get("source_structure", {}).get("open_modules", [])
    require(len(modules) >= 8, "expected at least eight open modules")
    module_ids = {module.get("module_id") for module in modules}
    for required in ["G1", "G2", "G3", "G4", "E1", "E2", "M1", "M2"]:
        require(required in module_ids, f"missing open module {required}")
    todos = data.get("todos", [])
    require(len(todos) >= len(modules) + 2, "missing deterministic or module TODOs")
    for todo in todos:
        tid = todo.get("todo_id", "<unknown>")
        for field in [
            "mathematical_object",
            "subtasks",
            "deterministic_regime",
            "generative_regime",
            "critical_self_refinement",
            "expected_artifact",
            "acceptance_criterion",
            "paper_insertion_target",
            "validation_handoff",
            "stop_or_quarantine_condition",
        ]:
            require(todo.get(field), f"{tid} missing {field}")
        require(len(todo.get("subtasks", [])) >= 4, f"{tid} needs concrete subtasks")
        require(len(todo.get("deterministic_regime", [])) >= 2, f"{tid} needs deterministic regime")
        require(len(todo.get("generative_regime", [])) >= 1, f"{tid} needs generative regime")
        require(len(todo.get("critical_self_refinement", [])) >= 2, f"{tid} needs self-refinement prompts")
    workflow = data.get("workflow", {})
    require(workflow.get("independent_from_discovery") is True, "workflow must be independent from discovery")
    sequence = workflow.get("skill_sequence", [])
    require("results-open-module-decomposer" in sequence, "missing open-module skill")
    require("results-critical-self-refiner" in sequence, "missing critical self-refiner skill")
    review = data.get("todo_review", {})
    require(review.get("limitations_found"), "missing limitation review")
    require(review.get("repairs_applied"), "missing repair review")
    print(f"validated {len(modules)} open modules and {len(todos)} TODOs in {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
