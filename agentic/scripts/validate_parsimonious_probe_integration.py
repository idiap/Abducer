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
"""Validate end-to-end parsimonious probe integration."""

from __future__ import annotations

import json

from agentic_common import ROOT, clean_text, fail, load_json_object, rel


POLICY = ROOT / "docs/research-methods/parsimonious-probe-policy.md"
SCHEMA = ROOT / "agentic/spec/parsimonious_probe_decision.schema.json"
SYMBOLIC = ROOT / "agentic/reports/symbolic_matrix_probe/latest.json"
OBLIGATIONS = ROOT / "agentic/reports/analytic_estimate_obligations/latest.json"
NUMERIC = ROOT / "agentic/reports/bounded_numeric_probe/latest.json"
GRAPH = ROOT / "agentic/state/qualitative_mechanistic_graphs/yang-mills-existence-and-mass-gap-target.json"
SUBWORKFLOW = ROOT / "agentic/reports/subworkflow_integration/latest.json"
TASK_REGISTRY = ROOT / "registry/tasks/discovery-marathon/task_registry.json"


def require_file(path) -> None:
    if not path.exists():
        fail(f"missing {rel(path)}")


def main() -> int:
    for path in [POLICY, SCHEMA, SYMBOLIC, OBLIGATIONS, GRAPH, SUBWORKFLOW, TASK_REGISTRY]:
        require_file(path)
    json.loads(SCHEMA.read_text(encoding="utf-8"))
    policy_text = POLICY.read_text(encoding="utf-8").lower()
    for marker in ["exact symbolic derivation first", "bounded numeric probes third", "not part of the proof-control loop"]:
        if marker not in policy_text:
            fail(f"{rel(POLICY)} missing `{marker}`")
    if "qutip" not in policy_text or "not selected" not in policy_text:
        fail(f"{rel(POLICY)} must explicitly exclude QuTiP for the current PMP foundation")
    symbolic = load_json_object(SYMBOLIC)
    obligations = load_json_object(OBLIGATIONS)
    graph = load_json_object(GRAPH)
    subworkflow = load_json_object(SUBWORKFLOW)
    registry = load_json_object(TASK_REGISTRY)
    if symbolic.get("status") != "symbolic_formula":
        fail(f"{rel(SYMBOLIC)} must remain symbolic_formula")
    if symbolic.get("probe_decision", {}).get("decision") != "derive_symbolically":
        fail(f"{rel(SYMBOLIC)} must choose symbolic derivation first")
    if len(obligations.get("obligations", [])) < 5:
        fail(f"{rel(OBLIGATIONS)} needs analytic obligations")
    queue = obligations.get("next_experiment_queue_items", [])
    if not queue or queue[0].get("epistemic_status") != "analytic_obligation":
        fail(f"{rel(OBLIGATIONS)} queue must start with analytic obligations")
    graph_text = clean_text(graph).lower()
    for marker in ["symbolic_formula", "analytic_obligation", "finite matrix", "holonomy"]:
        if marker not in graph_text:
            fail(f"{rel(GRAPH)} missing PMP graph marker `{marker}`")
    sub_text = clean_text(subworkflow).lower()
    for marker in ["parsimonious", "symbolic-before-numeric", "bounded numeric"]:
        if marker not in sub_text:
            fail(f"{rel(SUBWORKFLOW)} missing PMP integration marker `{marker}`")
    registry_text = clean_text(registry)
    for artifact in [
        "agentic/spec/parsimonious_probe_decision.schema.json",
        "agentic/scripts/build_symbolic_matrix_probe.py",
        "agentic/scripts/validate_parsimonious_probe_integration.py",
        "agentic/reports/analytic_estimate_obligations/latest.json",
    ]:
        if artifact not in registry_text:
            fail(f"{rel(TASK_REGISTRY)} missing {artifact}")
    if NUMERIC.exists():
        numeric = load_json_object(NUMERIC)
        if numeric.get("status") not in {"calibration_only", "validated_probe", "falsifier_candidate"}:
            fail(f"{rel(NUMERIC)} numeric status is not proof-safe")
    print("validated parsimonious probe integration")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
