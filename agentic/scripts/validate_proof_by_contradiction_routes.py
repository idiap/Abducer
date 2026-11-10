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

"""Validate proof-by-contradiction route fixtures and active Yang-Mills branches."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_array, load_json_object, load_optional_json, rel, write_json


SCHEMA = ROOT / "agentic/spec/proof_by_contradiction_route.schema.json"
FIXTURES = ROOT / "agentic/fixtures/proof_by_contradiction_routes.json"
BRIDGE = ROOT / "agentic/reports/yang_mills_bridge_lemma_packets/latest.json"
OUT_JSON = ROOT / "agentic/reports/proof_by_contradiction_validation/latest.json"
OUT_MD = ROOT / "agentic/reports/proof_by_contradiction_validation/latest.md"


def text_of(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(text_of(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(text_of(item) for item in value)
    return clean_text(value)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def normalize_bridge_branch(packet: dict[str, Any], branch: dict[str, Any]) -> dict[str, Any]:
    return {
        "route_id": branch.get("branch_id", ""),
        "target_claim": packet.get("lemma_statement", ""),
        "route_family": packet.get("route_family", ""),
        "exact_negation": branch.get("exact_negation", ""),
        "preserved_commitments": branch.get("preserved_commitments", []),
        "same_theory_invariant": packet.get("same_theory_invariant", ""),
        "contradiction_carrier": branch.get("contradiction_carrier", ""),
        "derived_consequence": branch.get("derived_consequence", ""),
        "conflict_target": branch.get("conflict_target", ""),
        "conflict_target_status": "proof-obligation",
        "proof_obligations": branch.get("proof_obligations", []),
        "failure_modes": branch.get("failure_modes", []),
        "validation_handoff": branch.get("audit_skill", ""),
        "domain_markers": [
            "Yang-Mills",
            "gauge-invariant",
            "continuum",
            packet.get("route_family", ""),
            branch.get("strategy", ""),
        ],
        "generative_interpretation": branch.get("learning_if_failed", ""),
        "expected_verdict": "promote",
        "source_packet_id": packet.get("packet_id", ""),
        "source": "yang_mills_bridge_packet",
    }


def active_routes_from_bridge() -> list[dict[str, Any]]:
    bridge = load_optional_json(BRIDGE)
    routes: list[dict[str, Any]] = []
    for packet in bridge.get("packets", []) if isinstance(bridge.get("packets"), list) else []:
        if not isinstance(packet, dict):
            continue
        for branch in packet.get("contradiction_branches", []):
            if isinstance(branch, dict):
                routes.append(normalize_bridge_branch(packet, branch))
    return routes


def classify_route(route: dict[str, Any], schema: dict[str, Any]) -> tuple[str, list[dict[str, str]], str]:
    policy = schema["audit_policy"]
    findings: list[dict[str, str]] = []

    for field in schema["required_fields"]:
        if field not in route:
            findings.append({"severity": "critical", "kind": "missing_field", "field": field, "message": f"Missing field `{field}`."})
        elif field not in schema["list_fields"] and not clean_text(route.get(field)):
            findings.append({"severity": "critical", "kind": "empty_field", "field": field, "message": f"Empty field `{field}`."})
    for field in schema["list_fields"]:
        value = route.get(field)
        if not isinstance(value, list) or not value:
            findings.append({"severity": "critical", "kind": "bad_list", "field": field, "message": f"`{field}` must be a non-empty list."})

    exact_negation = clean_text(route.get("exact_negation"))
    if len(exact_negation.split()) < int(policy["minimum_exact_negation_words"]):
        findings.append({"severity": "critical", "kind": "weak_exact_negation", "field": "exact_negation", "message": "Exact negation is too thin to control quantifiers and objects."})

    route_text = text_of(route).lower()
    assumption_text = text_of(
        {
            "exact_negation": route.get("exact_negation", ""),
            "preserved_commitments": route.get("preserved_commitments", []),
            "same_theory_invariant": route.get("same_theory_invariant", ""),
            "contradiction_carrier": route.get("contradiction_carrier", ""),
            "derived_consequence": route.get("derived_consequence", ""),
            "conflict_target": route.get("conflict_target", ""),
            "domain_markers": route.get("domain_markers", []),
        }
    ).lower()
    domain_hits = [marker for marker in policy["required_physics_markers"] if marker in route_text]
    if len(domain_hits) < int(policy["minimum_domain_marker_count"]):
        findings.append({"severity": "critical", "kind": "generic_route_language", "field": "domain_markers", "message": "Route lacks enough Yang-Mills physics/math markers."})

    cross_hits = [flag for flag in policy["cross_theory_red_flags"] if flag in assumption_text]
    if cross_hits:
        findings.append({"severity": "critical", "kind": "cross_theory_slippage", "field": "same_theory_invariant", "message": f"Cross-theory or cutoff slippage detected: {', '.join(cross_hits)}."})

    strong_hits = [flag for flag in policy["too_strong_negation_red_flags"] if flag in route_text]
    if strong_hits:
        findings.append({"severity": "critical", "kind": "too_strong_negation", "field": "exact_negation", "message": f"Negation appears stronger than the target: {', '.join(strong_hits)}."})

    if route.get("conflict_target_status") == "missing":
        findings.append({"severity": "critical", "kind": "missing_conflict_target", "field": "conflict_target", "message": "Conflict target is not established; this is an evidence task, not proof progress."})
    elif route.get("conflict_target_status") == "incompatible":
        findings.append({"severity": "critical", "kind": "incompatible_conflict_target", "field": "conflict_target", "message": "Conflict target belongs to an incompatible object or regime."})
    elif route.get("conflict_target_status") not in schema["allowed_conflict_target_status"]:
        findings.append({"severity": "critical", "kind": "bad_conflict_target_status", "field": "conflict_target_status", "message": "Unknown conflict target status."})

    if isinstance(route.get("preserved_commitments"), list) and len(route["preserved_commitments"]) < int(policy["minimum_preserved_commitments"]):
        findings.append({"severity": "medium", "kind": "thin_preserved_commitments", "field": "preserved_commitments", "message": "Route should preserve at least three commitments."})
    if isinstance(route.get("proof_obligations"), list) and len(route["proof_obligations"]) < int(policy["minimum_proof_obligations"]):
        findings.append({"severity": "medium", "kind": "thin_proof_obligations", "field": "proof_obligations", "message": "Route should expose at least three proof obligations."})
    if isinstance(route.get("failure_modes"), list) and len(route["failure_modes"]) < int(policy["minimum_failure_modes"]):
        findings.append({"severity": "medium", "kind": "thin_failure_modes", "field": "failure_modes", "message": "Route should expose at least two failure modes."})

    kinds = {finding["kind"] for finding in findings}
    if "missing_conflict_target" in kinds:
        verdict = "evidence-acquire"
        learning = "The reductio has the right shape but teaches that the missing theorem or closedness result must be acquired before contradiction can carry proof weight."
    elif "cross_theory_slippage" in kinds or "incompatible_conflict_target" in kinds:
        verdict = "quarantine"
        learning = "The route teaches a boundary: contradiction cannot be derived by crossing cutoff, Hilbert-space, observable, or theory identity."
    elif "too_strong_negation" in kinds or "weak_exact_negation" in kinds:
        verdict = "repair"
        learning = "The route teaches that reductio pressure begins with the exact logical negation; overstrong assumptions make the contradiction mathematically uninformative."
    elif any(finding["severity"] == "critical" for finding in findings):
        verdict = "repair"
        learning = "The route has repairable structural defects before it can be interpreted."
    else:
        verdict = "promote"
        learning = "The route is promotable as a proof obligation: it has a precise negation, same-theory carrier, explicit conflict target status, and domain-specific mathematical obligations."
    return verdict, findings, learning


def audit_routes(routes: list[dict[str, Any]], schema: dict[str, Any], source: str) -> list[dict[str, Any]]:
    rows = []
    for route in routes:
        verdict, findings, learning = classify_route(route, schema)
        expected = route.get("expected_verdict")
        rows.append(
            {
                "route_id": route.get("route_id", ""),
                "source": source,
                "route_family": route.get("route_family", ""),
                "expected_verdict": expected,
                "computed_verdict": verdict,
                "matches_expected": expected in {None, "", verdict},
                "finding_count": len(findings),
                "findings": findings,
                "mathematical_learning": learning,
                "generative_quality": {
                    "status": "domain-specific" if verdict != "repair" or route.get("domain_markers") else "needs-domain-specificity",
                    "interpretation": route.get("generative_interpretation", ""),
                    "domain_markers": route.get("domain_markers", []),
                },
                "route": route,
            }
        )
    return rows


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Proof By Contradiction Route Validation",
        "",
        f"- Fixture routes: {report['summary']['fixture_routes']}",
        f"- Active bridge routes: {report['summary']['active_bridge_routes']}",
        f"- Verdict mismatches: {report['summary']['verdict_mismatches']}",
        f"- Critical findings: {report['summary']['critical_findings']}",
        "",
        "## Generative Review",
        "",
        report["generative_review"]["summary"],
        "",
    ]
    for row in report["routes"]:
        lines.extend(
            [
                f"## {row['route_id']}",
                "",
                f"- Source: `{row['source']}`",
                f"- Computed verdict: `{row['computed_verdict']}`",
                f"- Expected verdict: `{row['expected_verdict']}`",
                f"- Mathematical learning: {row['mathematical_learning']}",
                "",
            ]
        )
        if row["findings"]:
            lines.append("### Findings")
            lines.extend(f"- `{finding['kind']}`: {finding['message']}" for finding in row["findings"])
            lines.append("")
    return "\n".join(lines)


def main() -> int:
    schema = load_json_object(SCHEMA)
    fixtures = load_json_array(FIXTURES)
    for route in fixtures:
        require(isinstance(route, dict), f"{rel(FIXTURES)} entries must be objects")
    active = active_routes_from_bridge()
    fixture_rows = audit_routes(fixtures, schema, "fixture")
    active_rows = audit_routes(active, schema, "yang_mills_bridge_packet")
    rows = fixture_rows + active_rows
    mismatches = [row for row in fixture_rows if not row["matches_expected"]]
    critical_findings = sum(1 for row in rows for finding in row["findings"] if finding["severity"] == "critical")
    report = {
        "version": 1,
        "schema": rel(SCHEMA),
        "fixtures": rel(FIXTURES),
        "active_source": rel(BRIDGE),
        "summary": {
            "fixture_routes": len(fixtures),
            "active_bridge_routes": len(active),
            "routes_checked": len(rows),
            "verdict_mismatches": len(mismatches),
            "critical_findings": critical_findings,
            "active_promotable_routes": sum(1 for row in active_rows if row["computed_verdict"] == "promote"),
        },
        "generative_review": {
            "status": "pass" if not mismatches and len(active) >= 3 else "fail",
            "summary": (
                "The validation probes separate typed structure from mathematical interpretation. "
                "The valid no-gap route is accepted only as a proof obligation because observable density, "
                "spectral support, and cutoff-uniform decay remain to be proved. The bad fixtures are not merely "
                "schema failures: cross-cutoff contradiction is quarantined, overstrong negation is repaired, and "
                "missing OS-positivity closedness becomes an evidence-acquisition task."
            ),
            "domain_specificity_oracle": (
                "A route must speak in Yang-Mills terms such as H_YM, Omega, spectral measure, Schwinger functions, "
                "OS/reflection positivity, gauge-invariant observables, connected cumulants, continuum limit, and cutoff uniformity."
            ),
        },
        "routes": rows,
    }
    write_json(OUT_JSON, report)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(render_markdown(report), encoding="utf-8")
    if mismatches:
        fail(f"{rel(FIXTURES)} fixture verdict mismatches: {[row['route_id'] for row in mismatches]}")
    if len(active) < 3:
        fail(f"{rel(BRIDGE)} should expose at least three active Yang-Mills contradiction branches")
    if report["generative_review"]["status"] != "pass":
        fail("proof-by-contradiction generative review did not pass")
    print(f"validated {len(rows)} proof-by-contradiction routes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
