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
"""Validate ESR integration across interfaces, obligations, graph, and report."""

from __future__ import annotations

import json

from agentic_common import ROOT, clean_text, fail, load_json_object, rel
from discovery_marathon_common import LATEST_HTML, LATEST_TIMELINE_HTML


POLICY = ROOT / "docs/research-methods/equational-symbolic-reasoning.md"
SCHEMA = ROOT / "agentic/spec/finite_algebra_interface_packet.schema.json"
FINITE = ROOT / "agentic/reports/finite_algebra_interfaces/latest.json"
OBLIGATIONS = ROOT / "agentic/reports/analytic_estimate_obligations/latest.json"
GRAPH = ROOT / "agentic/state/qualitative_mechanistic_graphs/yang-mills-existence-and-mass-gap-target.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def embedded_payload(path):
    html = path.read_text(encoding="utf-8")
    raw = html.split('<script id="marathon-data" type="application/json">', 1)[1].split("</script>", 1)[0]
    import html as html_lib

    return json.loads(html_lib.unescape(raw))


def main() -> int:
    for path in [LATEST_HTML, LATEST_TIMELINE_HTML]:
        require(path.exists(), f"missing {rel(path)}")
    target_id = clean_text(embedded_payload(LATEST_HTML).get("report", {}).get("target_id"))
    if target_id != "yang-mills-existence-and-mass-gap-target":
        print(f"skipped equational symbolic integration for active target {target_id}")
        return 0
    for path in [POLICY, SCHEMA, FINITE, OBLIGATIONS, GRAPH]:
        require(path.exists(), f"missing {rel(path)}")
    json.loads(SCHEMA.read_text(encoding="utf-8"))
    policy = POLICY.read_text(encoding="utf-8").lower()
    for marker in ["exact determinant expansion", "quotient holonomy", "excluded tasks", "lean", "out of scope"]:
        require(marker in policy, f"{rel(POLICY)} missing `{marker}`")
    finite = load_json_object(FINITE)
    obligations = load_json_object(OBLIGATIONS)
    graph = load_json_object(GRAPH)
    packet = finite["packets"][0]
    text = clean_text(packet).lower()
    for marker in ["det(q)", "rho12", "phi", "holonomy", "coboundary", "rephasing", "not lean checked", "not theorem-prover output"]:
        require(marker in text, f"{rel(FINITE)} missing `{marker}`")
    require(198 <= min(int(c.split("-")[-1]) for c in packet["source_cycle_ids"] if c.startswith("cycle-")) <= 205, f"{rel(FINITE)} is not grounded in cycle 198-205 window")
    require(len(packet["side_conditions"]) >= 5, f"{rel(FINITE)} needs side-condition ledger")
    require(len(packet["falsifier_templates"]) >= 4, f"{rel(FINITE)} needs falsifier shapes")
    require(not any("lean checked" in clean_text(identity).lower() for identity in packet["exact_identities"]), f"{rel(FINITE)} identities must not claim Lean checking")
    obligation_text = clean_text(obligations).lower()
    for marker in ["finite_interface_dependency", "boundary_ope_estimate", "contact_control", "phase_coboundary_control", "observable_density"]:
        require(marker in obligation_text, f"{rel(OBLIGATIONS)} missing `{marker}`")
    graph_text = clean_text(graph).lower()
    for marker in ["equational_interface", "side_condition_ledger", "falsifier_shape"]:
        require(marker in graph_text, f"{rel(GRAPH)} missing `{marker}`")
    for html_path in [LATEST_HTML, LATEST_TIMELINE_HTML]:
        payload = embedded_payload(html_path)
        layer = payload.get("parsimonious_probe_layer", {})
        require(layer.get("finite_algebra_interfaces"), f"{rel(html_path)} missing finite_algebra_interfaces in payload")
        require("PMP Probes" in html_path.read_text(encoding="utf-8"), f"{rel(html_path)} missing PMP/ESR tab")
    print("validated equational symbolic integration")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
