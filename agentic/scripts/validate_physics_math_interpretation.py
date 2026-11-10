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

"""Validate active physics/math interpretation of the Yang-Mills routes."""

from __future__ import annotations

from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel


REPORT = ROOT / "agentic/reports/physics_math_interpretation/latest.json"
CURRENT_TARGET = ROOT / "agentic/state/current_target.json"
YANG_MILLS_TARGET = "yang-mills-existence-and-mass-gap-target"
FORBIDDEN_SCORE_FIELDS = {"score", "specificity_score", "target_relevance_score", "quality_score"}

REQUIRED_COMMON_MARKERS = [
    "yang-mills",
    "schwinger",
    "os",
    "hamiltonian",
    "gap",
    "continuum",
]

ROUTE_REQUIRED_MARKERS = {
    "Balaban RG continuum-control route": [
        "balaban",
        "effective action",
        "cutoff",
        "os-positive",
        "nontrivial",
        "mass-gap",
    ],
    "Euclidean correlator-decay to spectral-gap route": [
        "correlator",
        "reflection positivity",
        "transfer matrix",
        "os reconstruction",
        "hamiltonian",
        "spectral gap",
        "uniform",
    ],
}


def flatten_text(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(flatten_text(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(flatten_text(item) for item in value)
    return clean_text(value).lower()


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def validate_no_scores(value: Any, path: str = "report") -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            if key in FORBIDDEN_SCORE_FIELDS:
                fail(f"{rel(REPORT)} {path}.{key} uses score-like validation in the interpretation artifact")
            validate_no_scores(nested, f"{path}.{key}")
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            validate_no_scores(nested, f"{path}[{index}]")


def validate_interpretation(item: dict[str, Any], index: int) -> None:
    subject = f"interpretation {index} ({item.get('candidate_id', 'unknown')})"
    required_fields = [
        "candidate_id",
        "route_family",
        "route_thesis",
        "mathematical_objects",
        "mechanism_chain",
        "physical_meaning",
        "load_bearing_bridge",
        "conceptual_bottleneck",
        "false_positive_controls",
        "next_lemma_questions",
        "content_verdict",
        "why_not_a_proof",
    ]
    for field in required_fields:
        require(field in item, f"{rel(REPORT)} {subject} missing `{field}`")
    require(len(item["mathematical_objects"]) >= 3, f"{rel(REPORT)} {subject} needs at least three mathematical objects")
    require(len(item["mechanism_chain"]) >= 5, f"{rel(REPORT)} {subject} needs a five-step mechanism chain")
    require(len(item["false_positive_controls"]) >= 3, f"{rel(REPORT)} {subject} needs false-positive controls")
    require(len(item["next_lemma_questions"]) >= 3, f"{rel(REPORT)} {subject} needs next lemma questions")
    text = flatten_text(item)
    for marker in REQUIRED_COMMON_MARKERS:
        require(marker in text, f"{rel(REPORT)} {subject} lacks common physics/math marker `{marker}`")
    family = item["route_family"]
    for marker in ROUTE_REQUIRED_MARKERS.get(family, []):
        require(marker in text, f"{rel(REPORT)} {subject} lacks route-specific marker `{marker}`")
    require("not proof" in text or "not a proof" in text, f"{rel(REPORT)} {subject} must state the non-proof boundary")
    require("reject" in text or "do not" in text, f"{rel(REPORT)} {subject} must actively reject false positives")
    require("score" not in text, f"{rel(REPORT)} {subject} should not justify itself by a score")


def main() -> int:
    report = load_json_object(REPORT)
    current = load_json_object(CURRENT_TARGET)
    require(report.get("target_id") == current.get("target_id"), f"{rel(REPORT)} target does not match active target")
    require(report.get("target_id") == YANG_MILLS_TARGET, f"{rel(REPORT)} is not a Yang-Mills interpretation report")
    require(report.get("interpretation_mode") == "active physics/math route interpretation", f"{rel(REPORT)} has wrong interpretation mode")
    validate_no_scores(report)
    interpretations = report.get("interpretations", [])
    require(isinstance(interpretations, list) and len(interpretations) >= 2, f"{rel(REPORT)} needs at least two active route interpretations")
    families = {item.get("route_family") for item in interpretations if isinstance(item, dict)}
    require("Balaban RG continuum-control route" in families, f"{rel(REPORT)} missing Balaban RG interpretation")
    require("Euclidean correlator-decay to spectral-gap route" in families, f"{rel(REPORT)} missing correlator-decay/spectral-gap interpretation")
    for index, item in enumerate(interpretations, start=1):
        require(isinstance(item, dict), f"{rel(REPORT)} interpretation {index} must be an object")
        validate_interpretation(item, index)
    synthesis = report.get("cross_route_synthesis", {})
    require(isinstance(synthesis, dict), f"{rel(REPORT)} cross_route_synthesis must be an object")
    synthesis_text = flatten_text(synthesis)
    for marker in ["same limiting yang-mills theory", "rg", "correlator", "spectral", "os"]:
        require(marker in synthesis_text, f"{rel(REPORT)} cross-route synthesis lacks `{marker}`")
    print(f"validated physics/math interpretation for {report['target_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
