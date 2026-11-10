#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Conjecture abstraction types that could close concept gaps between bridge endpoints."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from contracts import validate_bridges
from contracts import validate_connection_analysis
from contracts import validate_entrypoints
from contracts import validate_pathways
from contracts import validate_phyp
from reasoning_log import ReasoningLogger
from statement_text import humanize_schema_label
from statement_text import normalize_math_text

PROFILE_KEYS = (
    "core_problems",
    "claim_signatures",
    "model_signatures",
    "reduction_signatures",
    "antecedent_signatures",
    "consequence_signatures",
    "complexity_classes",
    "barrier_signals",
)

GENERIC_SIGNATURES = {
    "unconditional",
    "statement-conclusion",
    "support interface",
    "support",
    "potential support",
    "semantic object",
    "complexity measure",
    "witness complexity",
}


def _safe_float(value: Any, default: float = 0.0) -> float:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Defensive conversion/parsing to keep scoring and reporting robust.
    Contribution: Reduces runtime ambiguity and prevents malformed artifacts from destabilizing the workflow.
    """

    try:
        return float(value)
    except (TypeError, ValueError):
        return default



def _as_str_list(value: Any) -> list[str]:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Extraction of normalized symbolic labels from structured artifacts.
    Contribution: Keeps abstraction conjecture generation attached to typed processed outputs rather than raw lexical scans.
    """

    if not isinstance(value, list):
        return []
    out: list[str] = []
    seen: set[str] = set()
    for item in value:
        text = str(item).strip()
        if text and text not in seen:
            seen.add(text)
            out.append(text)
    return out



def _as_profile(value: Any) -> dict[str, Any]:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Ensures later gap analysis operates on typed connector profiles rather than arbitrary payloads.
    """

    return value if isinstance(value, dict) else {}



def _term_map(profile: dict[str, Any]) -> dict[str, list[str]]:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Construction of derived graph/model structures used by later stages.
    Contribution: Converts heterogeneous connector profile fields into a stable mathematical-signature map for gap diagnosis.
    """

    return {key: _as_str_list(profile.get(key)) for key in PROFILE_KEYS}



def _flatten_term_map(term_map: dict[str, list[str]]) -> list[str]:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Produces a single ordered signature surface used for ranking and reporting conjectured abstractions.
    """

    out: list[str] = []
    seen: set[str] = set()
    for key in PROFILE_KEYS:
        for item in term_map.get(key, []):
            if item not in seen:
                seen.add(item)
                out.append(item)
    return out



def _shared_missing(from_terms: dict[str, list[str]], to_terms: dict[str, list[str]]) -> tuple[list[str], list[str], list[str]]:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Extraction of overlap signals across paired statement profiles.
    Contribution: Makes concept gaps explicit by separating shared signatures from one-sided commitments.
    """

    from_flat = _flatten_term_map(from_terms)
    to_flat = _flatten_term_map(to_terms)
    shared = [item for item in from_flat if item in set(to_flat)]
    missing_from_source = [item for item in to_flat if item not in set(from_flat)]
    missing_from_target = [item for item in from_flat if item not in set(to_flat)]
    return shared, missing_from_source, missing_from_target



def _contains_any(values: list[str], needles: tuple[str, ...]) -> bool:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Lightweight semantic feature computation for graph reasoning heuristics.
    Contribution: Uses structured signature vocabulary to trigger domain-specific abstraction families without inspecting raw KB prose.
    """

    lowered = [value.lower() for value in values]
    return any(any(needle in value for needle in needles) for value in lowered)



def _is_generic_invariant(text: str) -> bool:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Typed classification used to guide scoring and prioritization.
    Contribution: Detects when a bridge still lacks a mathematically discriminating invariant and needs a conjectured abstraction.
    """

    normalized = str(text).strip().lower()
    if not normalized:
        return True
    if normalized in GENERIC_SIGNATURES:
        return True
    return normalized.endswith("interface") or normalized.endswith("object") or normalized.endswith("measure")



def _specificity(term: str) -> int:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Typed prioritization of concept labels by inferential specificity.
    Contribution: Keeps conjectures anchored on theorem-level mathematical signatures instead of broad topical buckets.
    """

    text = str(term).strip().lower()
    if not text:
        return 0
    score = 1
    if text in GENERIC_SIGNATURES:
        score -= 1
    if any(token in text for token in ("implies", "collapse", "separation", "not-in", "lower-bound", "complete")):
        score += 2
    if any(token in text for token in ("mcsp", "pit", "ips", "acc0", "ac0", "frege", "permanent", "nexp", "gap-", "p/poly")):
        score += 2
    if any(token in text for token in ("mass-gap", "wightman", "osterwalder", "schwinger", "continuum-limit", "reflection-positivity", "transfer-matrix")):
        score += 2
    if len(text) > 24:
        score += 1
    if text.count("-") >= 3 and " " not in text:
        score -= 3
    return max(0, score)



def _pick_anchor_term(*groups: list[str]) -> str:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Selection/retrieval of the most relevant candidates for reasoning.
    Contribution: Chooses a representative mathematical anchor so conjectured abstractions remain interpretable and task-specific.
    """

    items: list[str] = []
    seen: set[str] = set()
    for group in groups:
        for item in group:
            raw = str(item).strip()
            if not raw:
                continue
            text = normalize_math_text(raw) if any(token in raw for token in ("\\", "Qtext", "Rightarrow", "mathcal", "mathbb", "emph")) else humanize_schema_label(raw)
            text = text.strip()
            if text and text not in seen:
                seen.add(text)
                items.append(text)
    items.sort(key=lambda item: (_specificity(item), len(item)), reverse=True)
    return items[0] if items else "bridge"



def _analysis_lookup(analysis: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Construction of derived graph/model structures used by later stages.
    Contribution: Aligns bridge-plan rows with the richer connector profiles needed for concept-gap diagnostics.
    """

    out: dict[tuple[str, str], dict[str, Any]] = {}
    for row in analysis.get("connection_candidates", []) if isinstance(analysis.get("connection_candidates"), list) else []:
        if not isinstance(row, dict):
            continue
        src = str(row.get("from_id", "")).strip()
        dst = str(row.get("to_id", "")).strip()
        if src and dst:
            out[(src, dst)] = row
    return out



def _pathway_support(pathways: dict[str, Any]) -> dict[tuple[str, str], int]:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Construction of derived graph/model structures used by later stages.
    Contribution: Measures how much current pathway planning already operationalizes a bridge, which helps distinguish conceptual from execution gaps.
    """

    out: dict[tuple[str, str], int] = defaultdict(int)
    for row in pathways.get("pathways", []) if isinstance(pathways.get("pathways"), list) else []:
        if not isinstance(row, dict):
            continue
        for link in row.get("supporting_links", []) if isinstance(row.get("supporting_links"), list) else []:
            if not isinstance(link, dict):
                continue
            src = str(link.get("from_id", "")).strip()
            dst = str(link.get("to_id", "")).strip()
            if src and dst:
                out[(src, dst)] += 1
    return out



def _pair_hypotheses(phyp: dict[str, Any]) -> dict[tuple[str, str], list[dict[str, Any]]]:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Construction of derived graph/model structures used by later stages.
    Contribution: Connects bridge-level gap analysis to existing hypothesis kinds so conjectures can reuse prior conceptual commitments.
    """

    out: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in phyp.get("hypotheses", []) if isinstance(phyp.get("hypotheses"), list) else []:
        if not isinstance(row, dict):
            continue
        src = str(row.get("support_statement_id", "")).strip()
        dst = str(row.get("target_statement_id", "")).strip()
        if src and dst:
            out[(src, dst)].append(row)
    return out



def _hardness_pressure(hardness: dict[str, Any]) -> list[str]:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Imports problem-level difficulty signals so abstraction conjectures target genuine epistemic bottlenecks.
    """

    out: list[str] = []
    for row in hardness.get("essential_elements", []) if isinstance(hardness.get("essential_elements"), list) else []:
        if not isinstance(row, dict):
            continue
        name = str(row.get("name", "")).strip()
        diagnosis = str(row.get("diagnosis", "")).strip()
        if name:
            out.append(name)
        if diagnosis:
            out.append(diagnosis)
    return out



def _gap_axes(
    bridge: dict[str, Any],
    candidate: dict[str, Any],
    pathway_count: int,
    pair_hypotheses: list[dict[str, Any]],
    hardness: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[str], list[str], list[str]]:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Construction of derived graph/model structures used by later stages.
    Contribution: Diagnoses where a bridge fails mathematically by exposing model, implication, barrier, reduction, and invariant mismatches.
    """

    from_profile = _as_profile(candidate.get("from_profile"))
    to_profile = _as_profile(candidate.get("to_profile"))
    from_terms = _term_map(from_profile)
    to_terms = _term_map(to_profile)
    shared_terms, missing_from_source, missing_from_target = _shared_missing(from_terms, to_terms)
    bridge_type = str(bridge.get("bridge_type", "")).strip().lower()
    commitment = bridge.get("inferential_commitment", {}) if isinstance(bridge.get("inferential_commitment"), dict) else {}
    antecedent = str(commitment.get("support_antecedent_schema", "")).strip()
    consequence = str(commitment.get("target_consequence_schema", "")).strip()
    invariant = str(commitment.get("preserved_invariant", "")).strip()
    barrier = str(commitment.get("barrier_scope", "none")).strip().lower() or "none"
    invariant_basis = _as_str_list(commitment.get("invariant_basis"))
    hardness_terms = [item.lower() for item in _hardness_pressure(hardness)]

    axes: list[dict[str, Any]] = []
    shared_models = [item for item in from_terms.get("model_signatures", []) if item in set(to_terms.get("model_signatures", []))]
    if from_terms.get("model_signatures") and to_terms.get("model_signatures") and not shared_models:
        axes.append(
            {
                "axis": "model-mismatch",
                "severity": 0.82,
                "detail": (
                    "Source model signatures "
                    + ", ".join(from_terms.get("model_signatures", [])[:3])
                    + " do not align with target model signatures "
                    + ", ".join(to_terms.get("model_signatures", [])[:3])
                    + "."
                ),
            }
        )
    elif bool(from_terms.get("model_signatures")) ^ bool(to_terms.get("model_signatures")):
        axes.append(
            {
                "axis": "model-underspecification",
                "severity": 0.48,
                "detail": "One side of the bridge lacks an explicit model signature, so transfer obligations are underspecified.",
            }
        )

    shared_claims = [item for item in from_terms.get("claim_signatures", []) if item in set(to_terms.get("claim_signatures", []))]
    shared_consequences = [item for item in from_terms.get("consequence_signatures", []) if item in set(to_terms.get("consequence_signatures", []))]
    if antecedent and antecedent != "unconditional" and consequence and consequence != "statement-conclusion" and antecedent != consequence:
        severity = 0.74 if not shared_claims and not shared_consequences else 0.58
        axes.append(
            {
                "axis": "implication-lift",
                "severity": severity,
                "detail": f"The bridge must lift antecedent `{antecedent}` into target consequence `{consequence}`.",
            }
        )

    if _is_generic_invariant(invariant) or len(invariant_basis) < 3:
        axes.append(
            {
                "axis": "missing-intermediate-abstraction",
                "severity": 0.78 if _is_generic_invariant(invariant) else 0.52,
                "detail": (
                    f"Current preserved invariant `{invariant or 'unspecified'}` is too weakly typed to certify the bridge."
                ),
            }
        )

    reduction_terms = from_terms.get("reduction_signatures", []) + to_terms.get("reduction_signatures", [])
    if not reduction_terms or not any(item in set(from_terms.get("reduction_signatures", [])) for item in to_terms.get("reduction_signatures", [])):
        if "lifting" in bridge_type or "transfer" in bridge_type or _contains_any(shared_terms + missing_from_source + missing_from_target, ("reduction", "complete", "lifting", "local")):
            axes.append(
                {
                    "axis": "transfer-mechanism-gap",
                    "severity": 0.63,
                    "detail": "No shared reduction or transfer mechanism currently explains how the bridge should transport the relevant consequence.",
                }
            )

    if barrier != "none":
        axes.append(
            {
                "axis": "barrier-pressure",
                "severity": 0.84,
                "detail": f"The conjectured move is exposed to barrier scope `{barrier}` and needs a barrier-evading abstraction.",
            }
        )
    elif any("barrier" in item or "oracle" in item or "dependency structure" in item for item in hardness_terms):
        axes.append(
            {
                "axis": "epistemic-pressure",
                "severity": 0.41,
                "detail": "Problem-level hardness diagnostics indicate that current conceptual wiring is sparse or obstructed.",
            }
        )

    if from_terms.get("core_problems") and to_terms.get("core_problems"):
        shared_problems = [item for item in from_terms.get("core_problems", []) if item in set(to_terms.get("core_problems", []))]
        if not shared_problems:
            axes.append(
                {
                    "axis": "problem-regime-gap",
                    "severity": 0.57,
                    "detail": (
                        "The source and target are anchored in different core problem signatures: "
                        + ", ".join(from_terms.get("core_problems", [])[:2])
                        + " vs "
                        + ", ".join(to_terms.get("core_problems", [])[:2])
                        + "."
                    ),
                }
            )

    if pathway_count == 0 and len(pair_hypotheses) <= 1:
        axes.append(
            {
                "axis": "operationalization-gap",
                "severity": 0.36,
                "detail": "Current pathways and paired hypotheses do not yet operationalize this bridge as a usable proof move.",
            }
        )

    axes.sort(key=lambda row: _safe_float(row.get("severity"), 0.0), reverse=True)
    return axes, shared_terms, missing_from_source, missing_from_target



def _gap_score(axes: list[dict[str, Any]]) -> float:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Quantitative preference for concept gaps that promise high leverage if repaired.
    Contribution: Prioritizes abstraction work where a single conceptual innovation could unlock a strong bridge.
    """

    if not axes:
        return 0.0
    severities = [_safe_float(row.get("severity"), 0.0) for row in axes]
    mean_score = sum(severities) / len(severities)
    peak_score = max(severities)
    breadth = min(1.0, len(severities) / 4.0)
    return min(1.0, 0.45 * peak_score + 0.35 * mean_score + 0.20 * breadth)



def _context_domain(context: dict[str, Any]) -> str:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Domain routing over typed bridge and model signals.
    Contribution: Prevents overloaded mathematical tokens such as `generator` from being interpreted using the wrong discovery regime.
    """

    blob = " ".join(
        [
            str(context.get("bridge_type", "")),
            str(context.get("target_consequence_schema", "")),
            str(context.get("preserved_invariant", "")),
            *[str(item) for item in context.get("terms", [])],
            *[str(item) for item in context.get("model_terms", [])],
        ]
    ).lower()
    if any(token in blob for token in ("yang-mills", "mass-gap", "wightman", "osterwalder", "reflection-positivity", "continuum-limit")):
        return "mathematical-physics"
    if any(
        token in blob
        for token in (
            "markov-kakutani-common-fixed-point",
            "common-fixed-point",
            "compact-convex-set",
            "commuting-affine-family",
            "invariant-fixed-point-subset",
            "cesaro-averaging",
            "finite-intersection-property",
            "continuous-affine-self-map-on-compact-convex-set",
        )
    ):
        return "functional-analysis-convex-fixed-point"
    if any(
        token in blob
        for token in (
            "riesz-markov-kakutani",
            "riesz representation",
            "regular-borel-measure",
            "regular borel measure",
            "radon measure",
            "positive-linear-functional",
            "positive linear functional",
            "compactly-supported-continuous-functions",
            "vanishing-at-infinity-function-space",
            "signed-regular-measure-duality",
            "function-separation-implies-measure-uniqueness",
            "c0-dual-implies-signed-regular-measure",
        )
    ):
        return "functional-analysis-measure-representation"
    if any(
        token in blob
        for token in (
            "stone",
            "unitary-group",
            "unitary group",
            "self-adjoint",
            "selfadjoint",
            "skew-adjoint",
            "skewadjoint",
            "spectral theorem",
            "spectral-functional-calculus",
            "functional calculus",
            "hilbert",
            "c0-semigroup",
            "c_0-semigroup",
            "hille-yosida",
            "lumer-phillips",
            "resolvent",
            "yosida",
        )
    ):
        return "functional-analysis-semigroup"
    if any(token in blob for token in ("mcsp", "pit", "nexp", "acc0", "p/poly", "frege", "proof complexity", "pseudorandom")):
        return "computational-complexity"
    return "generic-mathematics"


def _template_scores(context: dict[str, Any]) -> dict[str, float]:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Selection/retrieval of the most relevant candidates for reasoning.
    Contribution: Maps typed mathematical gaps to candidate abstraction families that can plausibly repair them.
    """

    scores = {
        "intermediate-complexity-measure": 0.0,
        "surrogate-promise-problem": 0.0,
        "normal-form-translation": 0.0,
        "algebraic-certificate": 0.0,
        "pseudorandom-object": 0.0,
        "reduction-gadget-family": 0.0,
        "communication-lifting-gadget": 0.0,
        "proof-potential-measure": 0.0,
        "barrier-escaping-representation": 0.0,
        "canonical-obstruction-family": 0.0,
        "continuum-limit-construction": 0.0,
        "os-reconstruction-interface": 0.0,
        "mass-gap-witness-transfer": 0.0,
        "spectral-measure-interface": 0.0,
        "functional-calculus-normal-form": 0.0,
        "self-adjoint-generator-core": 0.0,
        "invariant-fixed-point-core": 0.0,
        "affine-averaging-kernel": 0.0,
        "finite-intersection-lift": 0.0,
        "measure-functional-interface": 0.0,
        "regular-borel-envelope": 0.0,
        "signed-measure-normal-form": 0.0,
    }

    terms = [str(item).strip().lower() for item in context.get("terms", [])]
    bridge_type = str(context.get("bridge_type", "")).lower()
    gap_axes = set(context.get("gap_axes", []))
    conceptual_kinds = set(context.get("conceptual_kinds", []))
    consequence = str(context.get("target_consequence_schema", "")).lower()
    domain = _context_domain(context)

    if "missing-intermediate-abstraction" in gap_axes:
        scores["intermediate-complexity-measure"] += 0.55
        scores["proof-potential-measure"] += 0.20
    if "model-mismatch" in gap_axes or "model-underspecification" in gap_axes:
        scores["normal-form-translation"] += 0.50
        scores["barrier-escaping-representation"] += 0.10
    if "transfer-mechanism-gap" in gap_axes:
        scores["reduction-gadget-family"] += 0.50
        scores["communication-lifting-gadget"] += 0.15
    if "barrier-pressure" in gap_axes:
        scores["barrier-escaping-representation"] += 0.90
        scores["canonical-obstruction-family"] += 0.15
    if "problem-regime-gap" in gap_axes:
        scores["surrogate-promise-problem"] += 0.35
        scores["normal-form-translation"] += 0.15
    if "continuum-limit" in bridge_type or _contains_any(terms, ("continuum-limit", "cutoff-removal", "ultraviolet-control", "renormalization-group", "lattice")):
        scores["continuum-limit-construction"] += 0.85
        scores["barrier-escaping-representation"] += 0.20
    if "os-reconstruction" in bridge_type or _contains_any(terms, ("wightman", "osterwalder", "schwinger", "reflection-positivity", "analytic continuation", "reconstruction")):
        scores["os-reconstruction-interface"] += 0.80
        scores["normal-form-translation"] += 0.15
    if "mass-gap" in bridge_type or (
        _contains_any(terms, ("mass-gap", "positive-mass-gap", "spectral-gap", "correlator-decay", "exponential-correlation-decay"))
        and _contains_any(terms, ("transfer-matrix", "hamiltonian", "reflection-positivity", "schwinger"))
    ):
        scores["mass-gap-witness-transfer"] += 0.85
        scores["proof-potential-measure"] += 0.10

    if domain == "functional-analysis-semigroup":
        if "missing-intermediate-abstraction" in gap_axes:
            scores["self-adjoint-generator-core"] += 0.55
        if "model-mismatch" in gap_axes or "model-underspecification" in gap_axes:
            scores["functional-calculus-normal-form"] += 0.50
        if "transfer-mechanism-gap" in gap_axes:
            scores["spectral-measure-interface"] += 0.45
        if any(token in bridge_type for token in ("stone", "self-adjoint", "unitary-generator")) or _contains_any(
            terms,
            (
                "stone-unitary-group-correspondence",
                "unique-self-adjoint-generator",
                "unitary-group-implies-self-adjoint-generator",
                "self-adjoint-generator-characterization",
                "strongly-continuous-unitary-group",
            ),
        ):
            scores["self-adjoint-generator-core"] += 0.80
        if any(token in bridge_type for token in ("spectral-calculus",)) or _contains_any(
            terms,
            (
                "spectral theorem",
                "spectral-functional-calculus",
                "functional calculus",
                "projection-valued measure",
                "unitary-group-via-functional-calculus",
            ),
        ):
            scores["spectral-measure-interface"] += 0.75
            scores["functional-calculus-normal-form"] += 0.70
        if _contains_any(terms, ("orbit-differentiability-control", "generator-definition", "differentiable-unitary-orbit-at-zero")):
            scores["self-adjoint-generator-core"] += 0.30
        if "barrier-pressure" in gap_axes and _contains_any(terms, ("spectral", "domain", "functional calculus", "self-adjoint")):
            scores["functional-calculus-normal-form"] += 0.15

    if domain == "functional-analysis-convex-fixed-point":
        if "missing-intermediate-abstraction" in gap_axes:
            scores["invariant-fixed-point-core"] += 0.55
            scores["affine-averaging-kernel"] += 0.25
        if "transfer-mechanism-gap" in gap_axes:
            scores["finite-intersection-lift"] += 0.50
            scores["invariant-fixed-point-core"] += 0.20
        if "model-mismatch" in gap_axes or "model-underspecification" in gap_axes:
            scores["invariant-fixed-point-core"] += 0.35
            scores["affine-averaging-kernel"] += 0.30
        if any(token in bridge_type for token in ("fixed-point-subset", "commuting-invariance")) or _contains_any(
            terms,
            (
                "invariant-fixed-point-subset",
                "single-map-fixed-point-implies-invariant-fixed-point-subset",
                "nonempty-compact-convex-fixed-point-subset",
                "commutativity-implies-fixed-point-subset-invariance",
            ),
        ):
            scores["invariant-fixed-point-core"] += 0.85
        if any(token in bridge_type for token in ("affine-averaging",)) or _contains_any(
            terms,
            (
                "cesaro-averaging",
                "affine-averaging-implies-single-map-fixed-point",
                "affine-orbit-averages-in-compact-convex-set",
                "single-affine-map-fixed-point",
            ),
        ):
            scores["affine-averaging-kernel"] += 0.80
            scores["invariant-fixed-point-core"] += 0.20
        if any(token in bridge_type for token in ("finite-intersection",)) or _contains_any(
            terms,
            (
                "finite-intersection-property",
                "finite-intersection-property-implies-common-fixed-point",
                "common-fixed-point-for-finite-commuting-family",
                "common-fixed-point-for-commuting-family",
            ),
        ):
            scores["finite-intersection-lift"] += 0.85
        if "barrier-pressure" in gap_axes and _contains_any(terms, ("fixed-point subset", "commuting", "compactness", "finite intersection")):
            scores["invariant-fixed-point-core"] += 0.10
            scores["finite-intersection-lift"] += 0.10

    if domain == "functional-analysis-measure-representation":
        if "missing-intermediate-abstraction" in gap_axes:
            scores["measure-functional-interface"] += 0.50
            scores["regular-borel-envelope"] += 0.35
        if "model-mismatch" in gap_axes or "model-underspecification" in gap_axes:
            scores["regular-borel-envelope"] += 0.45
        if "transfer-mechanism-gap" in gap_axes:
            scores["measure-functional-interface"] += 0.45
            scores["signed-measure-normal-form"] += 0.20
        if any(token in bridge_type for token in ("measure-representation", "regularity-reconstruction")) or _contains_any(
            terms,
            (
                "riesz-markov-kakutani-correspondence",
                "positive-functional-implies-regular-measure",
                "regular-borel-measure-representation",
                "regular-borel-measure-model",
                "positive-linear-functional-on-cc-space",
            ),
        ):
            scores["measure-functional-interface"] += 0.80
            scores["regular-borel-envelope"] += 0.55
        if any(token in bridge_type for token in ("integration-duality",)) or _contains_any(
            terms,
            (
                "regular-measure-implies-positive-functional",
                "integration-defines-positive-functional",
                "signed-regular-measure-duality",
                "c0-dual-implies-signed-regular-measure",
                "total-variation-equals-dual-norm",
            ),
        ):
            scores["signed-measure-normal-form"] += 0.80
            scores["measure-functional-interface"] += 0.25
        if _contains_any(
            terms,
            ("inner regular", "outer regular", "compact-open-approximation", "topological-regularity-reconstruction", "urysohn"),
        ):
            scores["regular-borel-envelope"] += 0.70
        if "barrier-pressure" in gap_axes and _contains_any(terms, ("regularity", "measure", "compact support", "radon")):
            scores["regular-borel-envelope"] += 0.15

    if "magnification" in bridge_type or any(token in terms for token in ("mcsp", "meta-complexity", "gap-mcsp", "hardness-magnification")):
        scores["intermediate-complexity-measure"] += 0.45
        scores["surrogate-promise-problem"] += 0.50
        scores["canonical-obstruction-family"] += 0.20
    if any(token in terms for token in ("pit", "derandom", "prg", "hitting-set", "identity-testing", "pseudorandom generator")):
        scores["pseudorandom-object"] += 0.65
        scores["algebraic-certificate"] += 0.20
    if any(token in terms for token in ("ips", "frege", "resolution", "taut", "proof")):
        scores["proof-potential-measure"] += 0.60
        scores["algebraic-certificate"] += 0.35
    if any(token in terms for token in ("communication", "lifting", "gadget")) or "lifting" in bridge_type:
        scores["communication-lifting-gadget"] += 0.70
        scores["reduction-gadget-family"] += 0.25
    if any(token in terms for token in ("permanent", "arithmetic", "algebraic", "polynomial")):
        scores["algebraic-certificate"] += 0.45
    if any(token in consequence for token in ("lower-bound", "separation", "collapse", "not-in", "not-equal")):
        scores["canonical-obstruction-family"] += 0.35
        scores["intermediate-complexity-measure"] += 0.15

    if "definition-introduction" in conceptual_kinds or "representation-shift" in conceptual_kinds:
        scores["normal-form-translation"] += 0.35
    if "intermediate-invariant" in conceptual_kinds:
        scores["intermediate-complexity-measure"] += 0.35
    if "barrier-escape-principle" in conceptual_kinds:
        scores["barrier-escaping-representation"] += 0.35
    if "normal-form-reduction" in conceptual_kinds:
        scores["normal-form-translation"] += 0.20
        scores["reduction-gadget-family"] += 0.20
    if "analogy-transfer" in conceptual_kinds:
        scores["reduction-gadget-family"] += 0.15

    return {key: min(1.0, value) for key, value in scores.items()}


def _preferred_domain_family(context: dict[str, Any]) -> str:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Deterministic preference for explicit domain families when the bridge type already names one.
    Contribution: Prevents Yang-Mills-specific conjecture families from being crowded out by earlier generic templates with similar scores.
    """

    bridge_type = str(context.get("bridge_type", "")).lower()
    terms = [str(item).strip().lower() for item in context.get("terms", [])]
    consequence = str(context.get("target_consequence_schema", "")).strip().lower()
    invariant = str(context.get("preserved_invariant", "")).strip().lower()
    domain = _context_domain(context)
    if "stone" in bridge_type or "self-adjoint" in bridge_type or "unitary-generator" in bridge_type:
        return "self-adjoint-generator-core"
    if "fixed-point-subset" in bridge_type or "commuting-invariance" in bridge_type:
        return "invariant-fixed-point-core"
    if "affine-averaging" in bridge_type:
        return "affine-averaging-kernel"
    if "finite-intersection" in bridge_type or "family-fixed-point" in bridge_type:
        return "finite-intersection-lift"
    if "spectral-calculus" in bridge_type:
        return "spectral-measure-interface"
    if "regularity-reconstruction" in bridge_type:
        return "regular-borel-envelope"
    if "measure-representation" in bridge_type:
        return "measure-functional-interface"
    if "integration-duality" in bridge_type:
        return "signed-measure-normal-form"
    if "os-reconstruction" in bridge_type:
        return "os-reconstruction-interface"
    if "mass-gap" in bridge_type:
        return "mass-gap-witness-transfer"
    if "continuum-limit" in bridge_type:
        return "continuum-limit-construction"
    if domain == "functional-analysis-convex-fixed-point":
        if _contains_any(terms, ("cesaro-averaging", "affine-averaging-implies-single-map-fixed-point", "single-affine-map-fixed-point")):
            return "affine-averaging-kernel"
        if _contains_any(
            terms,
            (
                "finite-intersection-property",
                "finite-intersection-property-implies-common-fixed-point",
                "common-fixed-point-for-finite-commuting-family",
                "finite-commuting-affine-subfamily",
            ),
        ) and "invariant-fixed-point-subset" not in " ".join(terms):
            return "finite-intersection-lift"
        if _contains_any(
            terms,
            (
                "invariant-fixed-point-subset",
                "single-map-fixed-point-implies-invariant-fixed-point-subset",
                "commutativity-implies-fixed-point-subset-invariance",
            ),
        ) or "fixed-point subset" in invariant or "common-fixed-point" in consequence:
            return "invariant-fixed-point-core"
    if domain == "functional-analysis-semigroup":
        if _contains_any(terms, ("spectral theorem", "spectral-functional-calculus", "projection-valued measure", "functional calculus")):
            return "spectral-measure-interface"
        return "self-adjoint-generator-core"
    if domain == "functional-analysis-measure-representation":
        if _contains_any(
            terms,
            ("inner regular", "outer regular", "compact-open-approximation", "urysohn", "regular-borel-measure"),
        ):
            return "regular-borel-envelope"
        if _contains_any(terms, ("signed-regular-measure-duality", "c0-dual-implies-signed-regular-measure", "total variation")):
            return "signed-measure-normal-form"
        return "measure-functional-interface"
    return ""

def _statement_delta_context(context: dict[str, Any]) -> dict[str, Any]:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Access to the bridge-level statement delta contract.
    Contribution: Lets abstraction conjectures reuse the concrete source-to-target shift already diagnosed upstream.
    """

    return context.get("statement_delta", {}) if isinstance(context.get("statement_delta"), dict) else {}


def _typed_object_profile(family: str, context: dict[str, Any]) -> dict[str, str]:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Typed naming of the candidate bridge object and its carrier class.
    Contribution: Prevents abstraction conjectures from degrading into generic placeholder nouns.
    """

    delta = _statement_delta_context(context)
    anchor = (
        str(delta.get("source_problem_family", "")).strip()
        or _pick_anchor_term(
            context.get("shared_terms", []),
            context.get("missing_from_source", []),
            context.get("missing_from_target", []),
            context.get("invariant_basis", []),
        )
        or "bridge"
    )
    anchor_lower = anchor.lower()
    source_model = str(delta.get("source_model", "")).strip()
    target_model = str(delta.get("target_model", "")).strip()
    threshold_shift = str(delta.get("threshold_shift", "")).strip().lower()
    bridge_type = str(context.get("bridge_type", "")).strip().lower()

    computational_profiles = {
        "intermediate-complexity-measure": (
            "threshold-sensitive MCSP witness family" if "mcsp" in anchor_lower and "near-threshold" in threshold_shift else
            "MCSP witness family" if "mcsp" in anchor_lower else
            f"{anchor} witness family",
            "family of instances equipped with a monotone witness measure",
        ),
        "surrogate-promise-problem": (
            "Gap-MCSP promise problem" if "mcsp" in anchor_lower else f"{anchor} promise-gap problem",
            "promise problem with an explicit yes/no gap and transfer reduction",
        ),
        "normal-form-translation": (
            f"{anchor} transport normal form",
            "translation map between the source and target encodings",
        ),
        "algebraic-certificate": (
            f"{anchor} certificate family",
            "checkable certificate map or algebraic witness relation",
        ),
        "pseudorandom-object": (
            f"{anchor} hitting-set family",
            "seeded generator or hitting-set family",
        ),
        "reduction-gadget-family": (
            f"{anchor} reduction gadget family",
            "family of reductions preserving the route witness structure",
        ),
        "communication-lifting-gadget": (
            f"{anchor} lifting gadget",
            "combinatorial gadget map for lifting lower-bound witnesses",
        ),
        "proof-potential-measure": (
            f"{anchor} proof progress measure",
            "monotone potential function over proofs or certificates",
        ),
        "barrier-escaping-representation": (
            f"{anchor} barrier-avoiding encoding",
            "re-encoding map designed to stay outside the active barrier",
        ),
        "canonical-obstruction-family": (
            f"{anchor} obstruction family",
            "family of hard instances or obstructions forcing the target payoff",
        ),
    }
    if family in computational_profiles:
        label, carrier = computational_profiles[family]
        return {"label": label, "carrier_kind": carrier, "typing_status": "typed"}

    typed_profiles = {
        "continuum-limit-construction": (
            f"{anchor} continuum-limit construction",
            "regulated family together with a cutoff-stable limiting object",
        ),
        "os-reconstruction-interface": (
            f"{anchor} OS reconstruction interface",
            "Euclidean-to-Wightman reconstruction interface",
        ),
        "mass-gap-witness-transfer": (
            f"{anchor} mass-gap witness transfer",
            "spectral or decay witness transporting Euclidean control into a mass-gap certificate",
        ),
        "spectral-measure-interface": (
            f"{anchor} spectral-measure interface",
            "projection-valued measure or equivalent spectral interface",
        ),
        "functional-calculus-normal-form": (
            f"{anchor} functional-calculus normal form",
            "functional-calculus representation making the bridge operator explicit",
        ),
        "self-adjoint-generator-core": (
            f"{anchor} self-adjoint generator core",
            "dense domain or core carrying the hidden generator",
        ),
        "invariant-fixed-point-core": (
            f"{anchor} invariant fixed-point subset core",
            "nonempty compact convex invariant subset",
        ),
        "affine-averaging-kernel": (
            f"{anchor} affine averaging kernel",
            "averaging operator or compactness witness for fixed-point extraction",
        ),
        "finite-intersection-lift": (
            f"{anchor} finite-intersection lift",
            "finite-family compactness package for lifting local witnesses to the full family",
        ),
        "measure-functional-interface": (
            f"{anchor} measure-functional interface",
            "interface pairing positive functionals with representing measures",
        ),
        "regular-borel-envelope": (
            f"{anchor} regular-Borel envelope",
            "regularity envelope controlling inner and outer approximation",
        ),
        "signed-measure-normal-form": (
            f"{anchor} signed-measure normal form",
            "signed-measure decomposition or duality normal form",
        ),
    }
    if family in typed_profiles:
        label, carrier = typed_profiles[family]
        return {"label": label, "carrier_kind": carrier, "typing_status": "typed"}
    if anchor and anchor != "bridge":
        return {
            "label": f"{anchor} bridge witness",
            "carrier_kind": f"explicit witness family or transport map from {source_model or 'source'} to {target_model or 'target'}",
            "typing_status": "typed" if bridge_type else "underspecified",
        }
    return {
        "label": f"underspecified {family.replace('-', ' ')} for {context.get('bridge_id', 'bridge')}",
        "carrier_kind": "carrier not yet typed",
        "typing_status": "underspecified",
    }


def _family_label(family: str, context: dict[str, Any]) -> str:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Rendering internal outputs into human-readable artifacts.
    Contribution: Names the proposed abstraction in mathematically meaningful terms tied to the current bridge commitments.
    """

    return _typed_object_profile(family, context).get("label", "bridge abstraction")



def _family_role(family: str, context: dict[str, Any]) -> str:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Rendering internal outputs into human-readable artifacts.
    Contribution: Explains why a conjectured mathematical object would matter for closing a specific bridge gap.
    """

    invariant = str(context.get("preserved_invariant", "support-target interface") or "support-target interface")
    antecedent = str(context.get("support_antecedent_schema", "unconditional") or "unconditional")
    consequence = str(context.get("target_consequence_schema", "statement-conclusion") or "statement-conclusion")
    barrier = str(context.get("barrier_scope", "none") or "none")
    delta = _statement_delta_context(context)
    carrier_kind = _typed_object_profile(family, context).get("carrier_kind", "bridge carrier")
    source_focus = str(delta.get("source_claim_focus", "")).strip() or antecedent
    target_focus = str(delta.get("target_claim_focus", "")).strip() or consequence
    model_shift = str(delta.get("model_shift", "")).strip()
    threshold_shift = str(delta.get("threshold_shift", "")).strip()

    roles = {
        "intermediate-complexity-measure": (
            f"An explicit {carrier_kind} that records enough of `{source_focus}` to test whether the route can reach `{consequence}` while preserving `{invariant}`."
        ),
        "surrogate-promise-problem": (
            f"A {carrier_kind} whose threshold behavior makes the shift {threshold_shift or '`source` -> `target`'} mathematically testable."
        ),
        "normal-form-translation": (
            f"A {carrier_kind} that transports `{invariant}` across the model shift {model_shift or 'source -> target'} without weakening the payoff `{consequence}`."
        ),
        "algebraic-certificate": (
            f"A {carrier_kind} that turns the missing step from `{source_focus}` to `{target_focus}` into a verifiable certificate condition."
        ),
        "pseudorandom-object": (
            f"A {carrier_kind} that converts the current hardness signal into a concrete derandomization or lower-bound interface."
        ),
        "reduction-gadget-family": (
            f"A {carrier_kind} that preserves `{invariant}` while carrying the route from `{source_focus}` into `{consequence}`."
        ),
        "communication-lifting-gadget": (
            f"A {carrier_kind} that lifts a witness from the source regime into the target communication or circuit setting."
        ),
        "proof-potential-measure": (
            f"A {carrier_kind} witnessing whether the move from `{source_focus}` toward `{consequence}` is structurally achievable."
        ),
        "barrier-escaping-representation": (
            f"A {carrier_kind} designed to expose `{invariant}` without re-entering barrier scope `{barrier}`."
        ),
        "canonical-obstruction-family": (
            f"A {carrier_kind} whose existence would force `{consequence}` rather than merely suggest it."
        ),
        "continuum-limit-construction": (
            f"A cutoff-stable construction that keeps `{invariant}` visible while transporting the bridge into a genuine continuum object supporting `{consequence}`."
        ),
        "os-reconstruction-interface": (
            f"A reconstruction interface that turns OS/reflection-positivity data into a Wightman-side realization while preserving `{invariant}`."
        ),
        "mass-gap-witness-transfer": (
            f"A transfer object that converts decay, transfer-matrix, or spectral information into a positive mass-gap witness forcing `{consequence}`."
        ),
        "spectral-measure-interface": (
            f"A spectral-measure or functional-calculus interface that turns self-adjoint data into unitary dynamics while preserving `{invariant}`."
        ),
        "functional-calculus-normal-form": (
            f"A normal form for exponentiating self-adjoint operators so the bridge to `{consequence}` becomes a typed functional-calculus obligation."
        ),
        "self-adjoint-generator-core": (
            f"A dense-domain or symmetry core that is strong enough to recover the self-adjoint generator hidden behind the current bridge toward `{consequence}`."
        ),
        "invariant-fixed-point-core": (
            f"A nonempty compact convex fixed-point subset object that makes `{invariant}` explicit enough to reduce the family theorem toward `{consequence}`."
        ),
        "affine-averaging-kernel": (
            f"An averaging kernel that turns affine orbit data into a genuine fixed-point witness while preserving `{invariant}`."
        ),
        "finite-intersection-lift": (
            f"A compactness-and-finite-intersection mechanism that lifts finite-family fixed-point data into the family-level consequence `{consequence}`."
        ),
        "measure-functional-interface": (
            f"An interface object that makes the passage between positive linear functionals and representing measures explicit while preserving `{invariant}`."
        ),
        "regular-borel-envelope": (
            f"A regularity envelope that reconstructs inner/outer regular measure control from the topological side without losing `{invariant}`."
        ),
        "signed-measure-normal-form": (
            f"A signed-measure or variation normal form that turns the current bridge into an explicit duality statement toward `{consequence}`."
        ),
    }
    return roles.get(family, "A bridge abstraction that would make the missing mathematical move explicit and testable.")



def _construction_template(family: str, context: dict[str, Any]) -> list[str]:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Rendering internal outputs into human-readable artifacts.
    Contribution: Turns an abstract conjecture into a concrete research program for the next reasoning loop.
    """

    invariant = str(context.get("preserved_invariant", "support-target interface") or "support-target interface")
    bridge_id = str(context.get("bridge_id", "bridge") or "bridge")
    shared = ", ".join(context.get("shared_terms", [])[:3]) or "current shared signatures"

    templates = {
        "intermediate-complexity-measure": [
            f"Define a candidate measure that refines `{invariant}` on the shared signature set: {shared}.",
            f"Show how the measure changes along the support-to-target move in `{bridge_id}`.",
            "Retain only variants that distinguish the target regime from nearby weaker models.",
        ],
        "surrogate-promise-problem": [
            "Specify a promise version whose threshold behaviour mirrors the desired target separation.",
            f"Prove that lower bounds or hardness on the surrogate preserve `{invariant}`.",
            "Test whether magnification or transfer theorems become cleaner when phrased through the surrogate.",
        ],
        "normal-form-translation": [
            "Design a canonical encoding shared by the source and target model signatures.",
            f"Verify that `{invariant}` is preserved by the translation.",
            "Check whether existing deductions become theorem-schema matches after re-expression.",
        ],
        "algebraic-certificate": [
            "Define a certificate whose validity can be checked in the relevant algebraic regime.",
            "Show how certificate existence/nonexistence corresponds to the desired lower bound or consequence.",
            "Test the certificate on the strongest existing theorem families in the KB.",
        ],
        "pseudorandom-object": [
            "Construct a candidate hitting-set, generator, or seed family matched to the target regime.",
            "Relate its success/failure to the current hardness or identity-testing statement.",
            "Use the object to convert a semantic gap into a proof obligation over explicit instances.",
        ],
        "reduction-gadget-family": [
            "Specify a local gadget that transports instances while preserving the target invariant.",
            "Track what structural information is lost or amplified under the gadget.",
            "Retain only gadgets that preserve the target consequence class, not just the statement surface.",
        ],
        "communication-lifting-gadget": [
            "Choose a base function or witness family to lift.",
            "Design a gadget composition that preserves the targeted lower-bound witness.",
            "Check whether known lifting theorems or counterexamples constrain the gadget class.",
        ],
        "proof-potential-measure": [
            "Define a monotone or subadditive quantity over proofs/certificates in the target system.",
            "Show how the measure would certify the missing step if it crossed a threshold.",
            "Compare the measure against existing lower-bound and simulation results in the KB.",
        ],
        "barrier-escaping-representation": [
            "Re-encode the target objects so the critical structure is not expressible in the blocked barrier regime.",
            f"Check that `{invariant}` remains observable after the representation change.",
            "Run coherence and bridge validation on the re-encoded statements before promoting the move.",
        ],
        "canonical-obstruction-family": [
            "Define an explicit hard family or obstruction parameterized by the target regime.",
            "Show that any weak realization of the family already forces the intended separation or collapse consequence.",
            "Use the family to generate intermediate lemmas and failure certificates.",
        ],
        "continuum-limit-construction": [
            "Specify the regulated or lattice family together with the candidate limiting object.",
            f"Show that `{invariant}` remains uniformly controlled across scales and survives cutoff removal.",
            "Test whether OS/Wightman admissibility and positivity survive the limit rather than appearing only formally.",
        ],
        "os-reconstruction-interface": [
            "Package the OS axioms, reflection positivity, and continuity inputs into a single reconstruction interface.",
            f"Verify that `{invariant}` is preserved under analytic continuation and reconstruction.",
            "Check whether the interface yields a genuine Wightman/Hamiltonian object that can feed downstream mass-gap arguments.",
        ],
        "mass-gap-witness-transfer": [
            "Define an object that records how correlator decay, transfer-matrix gap, or spectral positivity is transported.",
            f"Show that the object preserves `{invariant}` while turning decay information into a positive mass-gap witness.",
            "Test the construction against existing lattice, OS, and Hamiltonian statements in the KB.",
        ],
        "spectral-measure-interface": [
            "Package the spectral theorem data into a projection-valued measure or equivalent functional-calculus interface.",
            f"Show that `{invariant}` survives when exponentiating the self-adjoint object into unitary time evolution.",
            "Test whether the interface yields a strongly continuous one-parameter unitary group rather than a formal exponential only.",
        ],
        "functional-calculus-normal-form": [
            "Re-express the bridge through a canonical functional-calculus normal form.",
            f"Verify that the normal form preserves `{invariant}` while making the target consequence `{context.get('target_consequence_schema', 'statement-conclusion')}` explicit.",
            "Check whether continuity, domain, and group-law obligations become theorem-schema matches after the re-expression.",
        ],
        "self-adjoint-generator-core": [
            "Define the minimal dense domain or core on which the hidden infinitesimal operator is well-defined.",
            f"Show that the core preserves `{invariant}` and is strong enough to force self-adjointness or an equivalent closure property.",
            "Test whether the core upgrades unitary-orbit information into a unique generator statement rather than a heuristic derivative.",
        ],
        "invariant-fixed-point-core": [
            "Define the fixed-point subset object attached to a single affine map and specify why it remains nonempty, compact, and convex.",
            f"Show that the object preserves `{invariant}` while reducing the bridge toward `{context.get('target_consequence_schema', 'statement-conclusion')}`.",
            "Test whether the subset is genuinely preserved by the commuting family rather than merely containing one accidental fixed point.",
        ],
        "affine-averaging-kernel": [
            "Define the affine averaging operator or orbit-average kernel that stays inside the compact convex set.",
            f"Show that the averaging kernel preserves `{invariant}` while converting approximate fixed points into a genuine fixed-point witness.",
            "Retain only kernels that expose an actual single-map fixed-point mechanism rather than a generic compactness argument.",
        ],
        "finite-intersection-lift": [
            "Specify the family of invariant fixed-point subsets associated with finite commuting subfamilies.",
            f"Show that `{invariant}` survives the finite-intersection and compactness lift to the full family consequence.",
            "Keep only lifts that make the common fixed-point conclusion theorem-testable on current bridge candidates.",
        ],
        "measure-functional-interface": [
            "Define an interface that pairs compactly supported or vanishing-at-infinity test functions with a candidate measure object.",
            f"Show that the interface preserves `{invariant}` while transporting positivity into a genuine representation statement.",
            "Test whether the interface yields uniqueness and countable additivity rather than only a formal linear pairing.",
        ],
        "regular-borel-envelope": [
            "Specify how compact sets and open neighborhoods generate a candidate regularity envelope for the measure object.",
            f"Show that `{invariant}` survives inner/outer approximation through this envelope.",
            "Retain only envelopes that make regularity and uniqueness theorem-testable on existing bridge candidates.",
        ],
        "signed-measure-normal-form": [
            "Define the signed or complex measure normal form associated with the current dual functional statement.",
            f"Verify that the normal form preserves `{invariant}` while making total variation or Jordan decomposition explicit.",
            "Test whether the normal form sharpens the C_0-dual consequence instead of merely renaming the functional.",
        ],
    }
    return templates.get(family, ["Define the abstraction.", "State its preservation law.", "Test it against the current bridge obligations."])



def _validation_questions(family: str, context: dict[str, Any]) -> list[str]:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Rendering internal outputs into human-readable artifacts.
    Contribution: Supplies explicit falsification criteria so conjectured abstractions enter the framework as disciplined proof hypotheses.
    """

    invariant = str(context.get("preserved_invariant", "support-target interface") or "support-target interface")
    consequence = str(context.get("target_consequence_schema", "statement-conclusion") or "statement-conclusion")

    return [
        f"Does the proposed abstraction make `{invariant}` more discriminating than the current bridge commitment?",
        f"If the abstraction existed, would it reduce the missing proof step to a theorem-family obligation toward `{consequence}`?",
        "Can the abstraction be tested on at least one existing bridge or pathway without inventing new unsupported assumptions?",
    ]


def _regime_descriptor(context: dict[str, Any], side: str) -> str:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Compact mathematical descriptor for the source or target regime of a bridge conjecture.
    Contribution: Lets experts inspect which ambient problem/model setting the conjectured object is supposed to inhabit.
    """

    prefix = "source" if side == "source" else "target"
    statement_id = str(context.get(f"{prefix}_statement_id", "")).strip()
    problems = [str(item).strip() for item in context.get(f"{prefix}_core_problems", []) if str(item).strip()]
    models = [str(item).strip() for item in context.get(f"{prefix}_model_terms", []) if str(item).strip()]
    delta = _statement_delta_context(context)
    focus_key = "source_claim_focus" if prefix == "source" else "target_claim_focus"
    claims: list[str] = []
    focus = str(delta.get(focus_key, "")).strip()
    if focus:
        claims.append(focus)
    for item in context.get(f"{prefix}_claim_terms", []):
        text = humanize_schema_label(item)
        if text and text not in claims:
            claims.append(text)
    parts: list[str] = []
    if problems:
        parts.append("problems " + ", ".join(problems[:2]))
    if models:
        parts.append("models " + ", ".join(models[:2]))
    if claims:
        parts.append("claims " + ", ".join(claims[:2]))
    if not parts:
        parts.append("untyped regime")
    summary = "; ".join(parts)
    return f"{statement_id} ({summary})" if statement_id else summary


def _attribute_record(attribute: str, kind: str, rationale: str, derived_from: list[str]) -> dict[str, Any]:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Rendering structured definitional constraints for candidate bridge abstractions.
    Contribution: Encodes each required attribute with provenance so the framework can explain why a conjectured bridge concept is mathematically necessary.
    """

    return {
        "attribute": attribute,
        "kind": kind,
        "rationale": rationale,
        "why_it_matters": rationale,
        "derived_from": [str(item).strip() for item in derived_from if str(item).strip()][:6],
    }


def _counterfactual_intervention(
    attribute: dict[str, Any],
    context: dict[str, Any],
    family: str,
    carrier_kind: str,
) -> str:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Route-specific construction of a falsifying intervention.
    Contribution: Keeps counterfactual probes tied to the theorem pair rather than to generic attribute deletion.
    """

    kind = str(attribute.get("kind", "")).strip()
    delta = _statement_delta_context(context)
    source_focus = str(delta.get("source_claim_focus", "")).strip() or str(context.get("support_antecedent_schema", "")).strip()
    target_focus = str(delta.get("target_claim_focus", "")).strip() or str(context.get("target_consequence_schema", "")).strip()
    model_shift = str(delta.get("model_shift", "")).strip()
    threshold_shift = str(delta.get("threshold_shift", "")).strip()
    invariant = str(context.get("preserved_invariant", "")).strip()
    barrier = str(context.get("barrier_scope", "none") or "none").strip()
    label = _family_label(family, context)

    interventions = {
        "antecedent-realization": (
            f"Allow `{label}` to ignore the source-side content `{source_focus}` and only preserve topical overlap."
        ),
        "consequence-forcing": (
            f"Weaken `{label}` so that it no longer forces the target-side payoff `{target_focus}`."
        ),
        "invariant-preservation": (
            f"Permit the route from `{source_focus}` to `{target_focus}` to proceed without preserving `{invariant}`."
        ),
        "model-alignment": (
            f"Remove the explicit transport map needed to cross the model shift {model_shift or 'source -> target'}."
        ),
        "transfer-law": (
            f"Replace the route-specific transport mechanism for `{label}` by a nonconstructive existence claim only."
        ),
        "explicit-object-witness": (
            f"Replace the typed carrier of `{label}` by an untyped role description instead of an explicit {carrier_kind}."
        ),
        "barrier-evasion": (
            f"Force `{label}` to stay inside barrier scope `{barrier}` instead of using a barrier-avoiding encoding."
        ),
        "promise-control": (
            f"Collapse the promise or threshold distinction in {threshold_shift or 'the route threshold shift'}."
        ),
        "operationalizability": (
            f"Treat `{label}` as schematic and do not realize it on the current theorem pair."
        ),
    }
    return interventions.get(
        kind,
        f"Replace the theorem-pair-specific content of `{label}` by generic overlap between `{source_focus}` and `{target_focus}`.",
    )


def _necessary_attributes(family: str, context: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Definitional reasoning over what must hold for a bridge-filling concept to be mathematically admissible.
    Contribution: Recovers the necessary attributes that any adequate bridging concept must satisfy before it can support a proof pathway.
    """

    attributes: list[dict[str, Any]] = []
    seen: set[str] = set()
    gap_axes = set(context.get("gap_axes", []))
    antecedent = str(context.get("support_antecedent_schema", "")).strip()
    consequence = str(context.get("target_consequence_schema", "")).strip()
    invariant = str(context.get("preserved_invariant", "")).strip()
    barrier = str(context.get("barrier_scope", "none") or "none").strip()
    delta = _statement_delta_context(context)
    source_focus = str(delta.get("source_claim_focus", "")).strip() or antecedent
    target_focus = str(delta.get("target_claim_focus", "")).strip() or consequence
    carrier_kind = _typed_object_profile(family, context).get("carrier_kind", "bridge carrier")
    model_terms = [str(item).strip() for item in context.get("model_terms", []) if str(item).strip()]
    anchor = _pick_anchor_term(
        context.get("shared_terms", []),
        context.get("missing_from_source", []),
        context.get("missing_from_target", []),
        context.get("invariant_basis", []),
    )

    def add(attribute: str, kind: str, rationale: str, derived_from: list[str]) -> None:
        """
        Relevance: Local helper for definitional attribute synthesis inside one conjectured abstraction family.
        Concept: Canonicalization of attribute evidence into a deduplicated definitional profile.
        Contribution: Ensures the necessary-attribute layer stays compact, typed, and reusable in downstream counterfactual and proof-sketch reasoning.
        """
        key = f"{kind}:{attribute}".strip().lower()
        if not attribute.strip() or key in seen:
            return
        seen.add(key)
        attributes.append(_attribute_record(attribute, kind, rationale, derived_from))

    if antecedent and antecedent != "unconditional":
        add(
            f"admits source-side witness data for `{source_focus}`",
            "antecedent-realization",
            "The bridge object must absorb the actual source-side mathematical content rather than merely name the antecedent.",
            [antecedent, source_focus],
        )
    if consequence and consequence != "statement-conclusion":
        add(
            f"forces the target-side payoff `{consequence}`",
            "consequence-forcing",
            "A bridging concept is not sufficient unless it materially contributes to the target theorem-family payoff.",
            [consequence, target_focus],
        )
    if invariant:
        add(
            f"preserves the route invariant `{invariant}`",
            "invariant-preservation",
            "The bridge must keep the core mathematical quantity or structure stable across the source-target move.",
            [invariant, *context.get("invariant_basis", [])],
        )
    if "model-mismatch" in gap_axes or "model-underspecification" in gap_axes:
        model_text = ", ".join(model_terms[:2]) if model_terms else "source and target regimes"
        add(
            f"aligns the model shift ({model_text}) with an explicit transport map",
            "model-alignment",
            "The abstraction must live in both regimes or provide a faithful translation between them.",
            model_terms,
        )
    if "transfer-mechanism-gap" in gap_axes:
        add(
            "provides an explicit transfer law or reduction mechanism on the route",
            "transfer-law",
            "Without a transport rule, the bridge remains a topical analogy rather than a proof move.",
            context.get("shared_terms", []) + context.get("missing_from_source", []) + context.get("missing_from_target", []),
        )
    if "missing-intermediate-abstraction" in gap_axes:
        add(
            f"specifies a typed carrier ({carrier_kind}) rather than a role-description only",
            "explicit-object-witness",
            "The abstraction must be concrete enough to witness the bridge and to be re-used in downstream deductions.",
            [anchor, *context.get("missing_from_source", []), *context.get("missing_from_target", [])],
        )
    if barrier and barrier != "none":
        add(
            f"evades barrier scope `{barrier}`",
            "barrier-evasion",
            "The abstraction must avoid collapsing back into the known blocked proof regime.",
            [barrier],
        )
    if str(family).strip() == "surrogate-promise-problem":
        add(
            "admits a threshold or promise formulation with controllable hardness regime",
            "promise-control",
            "A surrogate problem only helps if its promise structure sharpens the weak-to-strong transfer.",
            context.get("missing_from_source", []) + context.get("missing_from_target", []),
        )
    if str(family).strip() == "continuum-limit-construction":
        add(
            "provides a cutoff-stable limiting object",
            "limit-construction",
            "A continuum-limit abstraction must specify the object that survives cutoff removal, not just the existence of approximants.",
            model_terms + context.get("missing_from_target", []),
        )
        add(
            "retains positivity and admissibility across the limit",
            "positivity-control",
            "The limiting construction must preserve the positivity or admissibility conditions required for reconstruction and spectral arguments.",
            context.get("shared_terms", []) + context.get("missing_from_source", []),
        )
    if str(family).strip() == "os-reconstruction-interface":
        add(
            "encodes reflection positivity and OS admissibility",
            "os-admissibility",
            "The bridge concept must carry the precise Euclidean axioms needed for reconstruction.",
            context.get("shared_terms", []) + context.get("missing_from_source", []),
        )
        add(
            "supports analytic continuation or reconstruction into Wightman data",
            "reconstruction-law",
            "An OS bridge is not sufficient unless it produces a genuine Wightman-side realization.",
            context.get("missing_from_target", []) + model_terms,
        )
    if str(family).strip() == "mass-gap-witness-transfer":
        add(
            "converts decay or transfer-matrix control into a mass-gap witness",
            "spectral-transfer",
            "The bridge must explain how Euclidean or lattice control becomes a positive mass-gap statement.",
            context.get("shared_terms", []) + context.get("missing_from_target", []),
        )
        add(
            "controls positivity of the transferred spectral object",
            "spectral-positivity",
            "Without spectral positivity, the witness does not certify a genuine Hamiltonian mass gap.",
            context.get("shared_terms", []) + model_terms,
        )
    if str(family).strip() in {"algebraic-certificate", "proof-potential-measure"}:
        add(
            "supports a verifiable certificate or monotone progress criterion",
            "verifiability",
            "Proof-directed abstractions must expose a checkable criterion for success or failure.",
            [anchor, consequence],
        )
    add(
        "admits a concrete realization on the current source-target theorem pair",
        "operationalizability",
        "The abstraction should be realizable on the current theorem pair, not only in an abstract future theory.",
        [str(context.get("bridge_id", "")).strip(), *context.get("shared_terms", [])],
    )
    return attributes


def _sufficient_attribute_sets(
    family: str,
    context: dict[str, Any],
    necessary_attributes: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Definitional reasoning over attribute bundles that would be enough to render a bridge conjecture testable.
    Contribution: Identifies sufficient attribute sets so the framework can move from vague abstraction ideas to concrete bridge criteria.
    """

    by_kind = {str(row.get("kind", "")).strip(): str(row.get("attribute", "")).strip() for row in necessary_attributes if isinstance(row, dict)}
    sufficient_sets: list[dict[str, Any]] = []

    def add_set(label: str, kinds: list[str], why: str) -> None:
        """
        Relevance: Local helper for sufficient-set synthesis within conjecture mode.
        Concept: Assembly of higher-level attribute bundles that jointly define a viable bridge abstraction.
        Contribution: Turns isolated necessary properties into concrete enough packages for evaluation, proof planning, and revision.
        """
        attrs = [by_kind[k] for k in kinds if by_kind.get(k)]
        if len(attrs) < 2:
            return
        sufficient_sets.append(
            {
                "set_id": f"suff.{len(sufficient_sets) + 1}",
                "label": label,
                "attributes": attrs,
                "why_sufficient": why,
            }
        )

    add_set(
        "transport set",
        ["antecedent-realization", "invariant-preservation", "model-alignment", "transfer-law", "consequence-forcing"],
        "Together these attributes define a bridge object that can transport the source theorem schema into the target regime without losing the relevant invariant.",
    )
    add_set(
        "witness set",
        ["explicit-object-witness", "invariant-preservation", "consequence-forcing", "operationalizability"],
        "This bundle is enough to turn the abstraction into a concrete witness family that can be checked against existing bridge and pathway artifacts.",
    )
    if by_kind.get("barrier-evasion"):
        add_set(
            "barrier-evasion set",
            ["barrier-evasion", "invariant-preservation", "consequence-forcing", "operationalizability"],
            "If these hold together, the bridge concept should escape the blocked regime while still forcing the intended consequence.",
        )
    if str(family).strip() == "surrogate-promise-problem":
        add_set(
            "promise-threshold set",
            ["promise-control", "antecedent-realization", "invariant-preservation", "consequence-forcing"],
            "A surrogate problem becomes sufficient when its promise regime both mirrors the antecedent hardness and forces the target consequence.",
        )
    if str(family).strip() == "continuum-limit-construction":
        add_set(
            "continuum-control set",
            ["limit-construction", "positivity-control", "invariant-preservation", "consequence-forcing"],
            "A continuum-limit construction is sufficient when it produces a cutoff-stable limit object that keeps the relevant positivity and invariant structure intact.",
        )
    if str(family).strip() == "os-reconstruction-interface":
        add_set(
            "reconstruction set",
            ["os-admissibility", "reconstruction-law", "invariant-preservation", "consequence-forcing"],
            "An OS-reconstruction interface is sufficient when it packages the Euclidean axioms tightly enough to force a Wightman-side realization.",
        )
    if str(family).strip() == "mass-gap-witness-transfer":
        add_set(
            "mass-gap witness set",
            ["spectral-transfer", "spectral-positivity", "invariant-preservation", "consequence-forcing"],
            "A mass-gap transfer abstraction is sufficient when it turns decay or transfer-matrix control into a positive mass-gap witness.",
        )
    if str(family).strip() in {"algebraic-certificate", "proof-potential-measure"}:
        add_set(
            "certificate set",
            ["verifiability", "invariant-preservation", "consequence-forcing", "operationalizability"],
            "A certificate-like bridge concept is sufficient when it provides a checkable criterion tied to the invariant and target consequence.",
        )

    if not sufficient_sets:
        core = [str(row.get("attribute", "")).strip() for row in necessary_attributes[:3] if str(row.get("attribute", "")).strip()]
        if core:
            sufficient_sets.append(
                {
                    "set_id": "suff.1",
                    "label": "minimal core set",
                    "attributes": core,
                    "why_sufficient": "This is the smallest currently recoverable attribute bundle that would make the conjectured bridge concept mathematically testable.",
                }
            )
    return sufficient_sets[:3]


def _definitional_profile(family: str, context: dict[str, Any]) -> dict[str, Any]:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Definitional reasoning that states what an adequate bridging concept must be.
    Contribution: Packages necessary and sufficient attributes into a reusable definition-like profile for bridge concepts.
    """

    necessary_attributes = _necessary_attributes(family, context)
    sufficient_sets = _sufficient_attribute_sets(family, context, necessary_attributes)
    antecedent = str(context.get("support_antecedent_schema", "") or "unconditional").strip()
    consequence = str(context.get("target_consequence_schema", "") or "statement-conclusion").strip()
    invariant = str(context.get("preserved_invariant", "") or "support-target interface").strip()
    barrier = str(context.get("barrier_scope", "none") or "none").strip()
    object_profile = _typed_object_profile(family, context)
    label = object_profile.get("label", "bridge object")
    carrier_kind = object_profile.get("carrier_kind", "bridge carrier")
    definition = (
        f"An adequate `{family}` bridge concept for `{context.get('bridge_id', '')}` is a `{carrier_kind}` named `{label}` "
        f"that absorbs `{antecedent}`, preserves `{invariant}`, and is strong enough to force `{consequence}`"
        + (f" while evading barrier scope `{barrier}`." if barrier != "none" else ".")
    )
    return {
        "object_label": label,
        "carrier_kind": carrier_kind,
        "typing_status": object_profile.get("typing_status", "typed"),
        "bridging_concept_definition": definition,
        "necessary_attributes": necessary_attributes,
        "sufficient_attribute_sets": sufficient_sets,
        "excluded_as_superficial": [
            "shared lexical overlap without invariant preservation",
            "same topical regime without a transfer law",
            "consequence mention without an object witness or certificate",
        ],
    }


def _mathematical_specification(
    family: str,
    context: dict[str, Any],
    definitional_profile: dict[str, Any],
) -> dict[str, Any]:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Theorem-shaped content contract for a conjectured bridge object.
    Contribution: Makes each abstraction inspectable as a mathematical proposal rather than a family label only.
    """

    source_regime = _regime_descriptor(context, "source")
    target_regime = _regime_descriptor(context, "target")
    antecedent = str(context.get("support_antecedent_schema", "") or "source-side theorem schema").strip()
    consequence = str(context.get("target_consequence_schema", "") or "target consequence").strip()
    invariant = str(context.get("preserved_invariant", "") or "bridge interface").strip()
    object_profile = _typed_object_profile(family, context)
    label = object_profile.get("label", _family_label(family, context))
    carrier_kind = object_profile.get("carrier_kind", "bridge carrier")
    object_sort = _family_role(family, context)
    definition_template = str(definitional_profile.get("bridging_concept_definition", "")).strip()
    barrier = str(context.get("barrier_scope", "none") or "none").strip()
    delta = _statement_delta_context(context)
    source_focus = str(delta.get("source_claim_focus", "")).strip() or antecedent
    target_focus = str(delta.get("target_claim_focus", "")).strip() or consequence
    model_shift = str(delta.get("model_shift", "")).strip() or "source -> target"
    threshold_shift = str(delta.get("threshold_shift", "")).strip() or "threshold not yet typed"
    consequence_shift = str(delta.get("consequence_shift", "")).strip() or f"force `{consequence}`"
    missing_lemma = str(delta.get("missing_witness_or_transport", "")).strip()
    assumptions = [
        f"The source-side content `{source_focus}` is available in {source_regime}.",
        f"There exists a `{label}` object, typed as a {carrier_kind}.",
        f"The object preserves `{invariant}` across the source-to-target move {model_shift}.",
    ]
    if barrier != "none":
        assumptions.append(f"The construction avoids or neutralizes barrier scope `{barrier}`.")
    proof_obligation_templates = [
        f"Source-to-object claim: build `{label}` from the source theorem content `{source_focus}` available in {source_regime}.",
        f"Transport claim: prove that `{label}` preserves `{invariant}` across the route {model_shift}.",
        f"Payoff claim: show that `{label}` upgrades {threshold_shift} and thereby {consequence_shift} in {target_regime}.",
    ]
    if "transfer-mechanism-gap" in set(context.get("gap_axes", [])):
        proof_obligation_templates.append(
            f"Transfer-law claim: exhibit the reduction or transport mechanism that carries `{source_focus}` into `{label}`."
        )
    if barrier != "none":
        obstruction_template = f"Failure mode: the object re-enters barrier scope `{barrier}` before the payoff lemma can be established."
    else:
        obstruction_template = (
            f"Failure mode: `{label}` never becomes more than topical overlap because the route-specific lemma remains missing. "
            + (missing_lemma if missing_lemma else f"The gap from `{source_focus}` to `{target_focus}` stays unproved.")
        )
    inspection_focus = [
        f"Specify the mathematical carrier and admissibility conditions of `{label}` as a {carrier_kind}.",
        f"Locate where `{invariant}` lives and how it is measured inside the conjectured object while crossing {model_shift}.",
        f"State the first theorem-family lemma that turns `{label}` from `{source_focus}` into `{target_focus}`.",
    ]
    return {
        "source_regime": source_regime,
        "target_regime": target_regime,
        "statement_delta": delta,
        "carrier_kind": carrier_kind,
        "typing_status": object_profile.get("typing_status", "typed"),
        "object_sort": object_sort,
        "definition_template": definition_template,
        "assumptions": assumptions,
        "conditional_claim": f"If such a `{label}` object exists and discharges the route-specific lemma from `{source_focus}` to `{target_focus}`, then `{consequence}` should follow in {target_regime}.",
        "proof_obligation_templates": proof_obligation_templates,
        "obstruction_template": obstruction_template,
        "missing_route_lemma": missing_lemma,
        "inspection_focus": inspection_focus,
    }


def _counterfactual_probes(
    family: str,
    context: dict[str, Any],
    definitional_profile: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Counterfactual reasoning over how bridge quality changes when candidate attributes are removed, added, or weakened.
    Contribution: Gives the workflow explicit tests for whether a conjectured bridging concept is genuinely explanatory or merely decorative.
    """

    necessary = definitional_profile.get("necessary_attributes", []) if isinstance(definitional_profile.get("necessary_attributes"), list) else []
    sufficient_sets = (
        definitional_profile.get("sufficient_attribute_sets", [])
        if isinstance(definitional_profile.get("sufficient_attribute_sets"), list)
        else []
    )
    probes: list[dict[str, Any]] = []
    gap_axes = list(context.get("gap_axes", []))
    delta = _statement_delta_context(context)
    source_focus = str(delta.get("source_claim_focus", "")).strip() or str(context.get("support_antecedent_schema", "")).strip()
    target_focus = str(delta.get("target_claim_focus", "")).strip() or str(context.get("target_consequence_schema", "")).strip()
    missing_lemma = str(delta.get("missing_witness_or_transport", "")).strip()
    carrier_kind = _typed_object_profile(family, context).get("carrier_kind", "bridge carrier")
    top_attribute = necessary[0] if necessary else {}
    if isinstance(top_attribute, dict) and str(top_attribute.get("attribute", "")).strip():
        diagnostic_value = str(top_attribute.get("why_it_matters", "") or top_attribute.get("rationale", "")).strip()
        probes.append(
            {
                "probe_id": "cf.1",
                "intervention": _counterfactual_intervention(top_attribute, context, family, carrier_kind),
                "expected_bridge_effect": "bridge-degrades-or-fails",
                "targeted_axis": gap_axes[0] if gap_axes else "bridge under-specification",
                "diagnostic_use": diagnostic_value
                or "Tests whether the leading theorem-pair commitment is genuinely necessary rather than descriptive.",
                "diagnostic_value": diagnostic_value
                or "Tests whether the leading theorem-pair commitment is genuinely necessary rather than descriptive.",
            }
        )

    if sufficient_sets:
        suff = sufficient_sets[0] if isinstance(sufficient_sets[0], dict) else {}
        attrs = suff.get("attributes", []) if isinstance(suff.get("attributes"), list) else []
        probes.append(
            {
                "probe_id": "cf.2",
                "intervention": (
                    f"Assume the typed carrier exists as a {carrier_kind} and fully realizes the working bundle "
                    + ", ".join(str(x) for x in attrs[:4])
                    + (
                        f"; then ask whether the route-specific lemma `{missing_lemma}` reduces to a concrete lemma chain."
                        if missing_lemma
                        else f"; then ask whether the route from `{source_focus}` to `{target_focus}` becomes theorem-level."
                    )
                ),
                "expected_bridge_effect": "bridge-becomes-testable",
                "targeted_axis": gap_axes[0] if gap_axes else "bridge under-specification",
                "diagnostic_use": "Tests whether the proposed sufficient bundle really collapses the current concept gap into a concrete proof obligation.",
                "diagnostic_value": "Tests whether the proposed sufficient bundle really collapses the current concept gap into a concrete proof obligation.",
            }
        )

    if str(context.get("barrier_scope", "none") or "none") != "none":
        probes.append(
            {
                "probe_id": f"cf.{len(probes) + 1}",
                "intervention": f"Replace the abstraction with one that stays inside barrier scope `{context.get('barrier_scope', 'none')}`.",
                "expected_bridge_effect": "bridge-blocked-by-known-barrier",
                "targeted_axis": "barrier-pressure",
                "diagnostic_use": "Checks that the bridge concept is not merely restating a blocked proof style under a new name.",
                "diagnostic_value": "Checks that the bridge concept is not merely restating a blocked proof style under a new name.",
            }
        )
    else:
        probes.append(
            {
                "probe_id": f"cf.{len(probes) + 1}",
                "intervention": (
                    f"Keep only shared vocabulary between `{source_focus}` and `{target_focus}` and discard the typed carrier "
                    f"`{_family_label(family, context)}`."
                ),
                "expected_bridge_effect": "bridge-reduces-to-superficial-similarity",
                "targeted_axis": gap_axes[0] if gap_axes else "bridge under-specification",
                "diagnostic_use": "Separates genuine bridge concepts from superficial analogies.",
                "diagnostic_value": "Separates genuine bridge concepts from superficial analogies.",
            }
        )
    return probes[:3]


def _definitional_completeness(definitional_profile: dict[str, Any]) -> float:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Quantitative estimate of how well a conjectured abstraction has been definitionally characterized.
    Contribution: Rewards conjectures that specify their bridge concept tightly enough to be acted on.
    """

    necessary = (
        definitional_profile.get("necessary_attributes", [])
        if isinstance(definitional_profile.get("necessary_attributes"), list)
        else []
    )
    sufficient = (
        definitional_profile.get("sufficient_attribute_sets", [])
        if isinstance(definitional_profile.get("sufficient_attribute_sets"), list)
        else []
    )
    return min(1.0, 0.60 * min(1.0, len(necessary) / 5.0) + 0.40 * min(1.0, len(sufficient) / 2.0))


def _counterfactual_sharpness(counterfactuals: list[dict[str, Any]]) -> float:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Quantitative estimate of how discriminative the counterfactual probes are.
    Contribution: Rewards conjectures whose failure and success modes are clear enough to guide the next reasoning round.
    """

    effects = {
        str(row.get("expected_bridge_effect", "")).strip()
        for row in counterfactuals
        if isinstance(row, dict) and str(row.get("expected_bridge_effect", "")).strip()
    }
    if not effects:
        return 0.0
    return min(1.0, 0.50 * min(1.0, len(counterfactuals) / 3.0) + 0.50 * min(1.0, len(effects) / 3.0))



def _conjecture_rows(
    bridges: dict[str, Any],
    analysis_lookup: dict[tuple[str, str], dict[str, Any]],
    pathways: dict[str, Any],
    phyp_pairs: dict[tuple[str, str], list[dict[str, Any]]],
    hardness: dict[str, Any],
    max_conjectures_per_bridge: int,
) -> dict[str, Any]:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Primary callable implementing a stage-level behavior.
    Contribution: Builds the stage's main output by turning bridge-local concept gaps into ranked abstraction conjectures.
    """

    gap_clusters: list[dict[str, Any]] = []
    abstraction_conjectures: list[dict[str, Any]] = []
    pathway_index = _pathway_support(pathways)
    counter = 1

    bridge_rows = bridges.get("bridge_programs", []) if isinstance(bridges.get("bridge_programs"), list) else []
    for bridge in bridge_rows:
        if not isinstance(bridge, dict):
            continue
        src = str(bridge.get("from_id", "")).strip()
        dst = str(bridge.get("to_id", "")).strip()
        if not src or not dst:
            continue
        candidate = analysis_lookup.get((src, dst), {})
        pair_rows = phyp_pairs.get((src, dst), [])
        pathway_count = pathway_index.get((src, dst), 0)
        axes, shared_terms, missing_from_source, missing_from_target = _gap_axes(
            bridge=bridge,
            candidate=candidate,
            pathway_count=pathway_count,
            pair_hypotheses=pair_rows,
            hardness=hardness,
        )
        gap_score = _gap_score(axes)
        commitment = bridge.get("inferential_commitment", {}) if isinstance(bridge.get("inferential_commitment"), dict) else {}
        from_profile = _as_profile(candidate.get("from_profile"))
        to_profile = _as_profile(candidate.get("to_profile"))
        model_terms = _as_str_list(from_profile.get("model_signatures")) + [
            item for item in _as_str_list(to_profile.get("model_signatures")) if item not in set(_as_str_list(from_profile.get("model_signatures")))
        ]
        conceptual_kinds = [
            str(row.get("kind", "")).strip()
            for row in pair_rows
            if isinstance(row, dict) and str(row.get("kind", "")).strip()
        ]
        terms = [
            *shared_terms,
            *missing_from_source,
            *missing_from_target,
            *_as_str_list(bridge.get("concept_evidence")),
            *_as_str_list(bridge.get("evidence_terms")),
            *_as_str_list(commitment.get("invariant_basis")),
        ]
        context = {
            "bridge_id": str(bridge.get("bridge_id", "")).strip(),
            "source_statement_id": src,
            "target_statement_id": dst,
            "bridge_type": str(bridge.get("bridge_type", "")).strip(),
            "statement_delta": bridge.get("statement_delta", {}) if isinstance(bridge.get("statement_delta"), dict) else {},
            "support_antecedent_schema": str(commitment.get("support_antecedent_schema", "")).strip(),
            "target_consequence_schema": str(commitment.get("target_consequence_schema", "")).strip(),
            "preserved_invariant": str(commitment.get("preserved_invariant", "")).strip(),
            "barrier_scope": str(commitment.get("barrier_scope", "none")).strip() or "none",
            "invariant_basis": _as_str_list(commitment.get("invariant_basis")),
            "source_core_problems": _as_str_list(from_profile.get("core_problems")),
            "target_core_problems": _as_str_list(to_profile.get("core_problems")),
            "source_model_terms": _as_str_list(from_profile.get("model_signatures")),
            "target_model_terms": _as_str_list(to_profile.get("model_signatures")),
            "source_claim_terms": _as_str_list(from_profile.get("claim_signatures")) + _as_str_list(from_profile.get("consequence_signatures")),
            "target_claim_terms": _as_str_list(to_profile.get("claim_signatures")) + _as_str_list(to_profile.get("consequence_signatures")),
            "gap_axes": [str(row.get("axis", "")).strip() for row in axes],
            "shared_terms": shared_terms,
            "missing_from_source": missing_from_source,
            "missing_from_target": missing_from_target,
            "terms": terms,
            "model_terms": model_terms,
            "conceptual_kinds": conceptual_kinds,
        }
        template_scores = _template_scores(context)
        ranked_templates = sorted(template_scores.items(), key=lambda item: item[1], reverse=True)
        selected_templates = [(family, score) for family, score in ranked_templates if score >= 0.35][: max(1, max_conjectures_per_bridge)]
        if not selected_templates and ranked_templates:
            selected_templates = ranked_templates[:1]
        preferred_family = _preferred_domain_family(context)
        if preferred_family:
            preferred_score = _safe_float(template_scores.get(preferred_family), 0.0)
            if preferred_score > 0.0 and preferred_family not in {family for family, _ in selected_templates}:
                selected_templates = [(preferred_family, preferred_score)] + selected_templates[: max(0, max_conjectures_per_bridge - 1)]
            selected_templates = sorted(
                selected_templates,
                key=lambda item: (item[0] != preferred_family, -_safe_float(item[1], 0.0), item[0]),
            )
        delta = _statement_delta_context(context)
        anchor_term = _pick_anchor_term(
            [
                str(delta.get("source_claim_focus", "")).strip(),
                str(delta.get("target_claim_focus", "")).strip(),
            ],
            shared_terms,
            missing_from_source,
            missing_from_target,
            _as_str_list(commitment.get("invariant_basis")),
        )

        gap_clusters.append(
            {
                "bridge_id": context["bridge_id"],
                "from_id": src,
                "to_id": dst,
                "bridge_type": context["bridge_type"],
                "bridge_score": round(_safe_float(bridge.get("bridge_score"), 0.0), 4),
                "gap_score": round(gap_score, 4),
                "gap_axes": axes,
                "shared_terms": shared_terms[:8],
                "missing_from_source": missing_from_source[:8],
                "missing_from_target": missing_from_target[:8],
                "pathway_support": pathway_count,
                "paired_hypothesis_kinds": conceptual_kinds[:8],
                "inferential_commitment": commitment,
                "recommended_abstraction_families": [family for family, _ in selected_templates],
            }
        )

        bridge_score = _safe_float(bridge.get("bridge_score"), 0.0)
        for family, family_score in selected_templates:
            definitional_profile = _definitional_profile(family, context)
            mathematical_specification = _mathematical_specification(family, context, definitional_profile)
            counterfactuals = _counterfactual_probes(family, context, definitional_profile)
            definitional_score = _definitional_completeness(definitional_profile)
            counterfactual_score = _counterfactual_sharpness(counterfactuals)
            novelty_signal = min(1.0, 0.45 * gap_score + 0.55 * family_score)
            feasibility_signal = min(
                1.0,
                0.40 * min(1.0, len(_as_str_list(commitment.get("invariant_basis"))) / 5.0)
                + 0.25 * min(1.0, pathway_count / 2.0)
                + 0.20 * min(1.0, len(pair_rows) / 3.0)
                + 0.15 * bridge_score,
            )
            priority_adjustment = 0.0
            if preferred_family and family == preferred_family:
                # Domain-native bridge objects should outrank generic barrier-evasion proposals when both are viable.
                priority_adjustment += 0.06
            if preferred_family and family == "barrier-escaping-representation":
                priority_adjustment -= 0.04
            priority = min(
                1.0,
                0.35 * bridge_score
                + 0.28 * gap_score
                + 0.12 * family_score
                + 0.10 * feasibility_signal
                + 0.10 * definitional_score
                + 0.05 * counterfactual_score,
            )
            priority = max(0.0, min(1.0, priority + priority_adjustment))
            object_profile = _typed_object_profile(family, context)
            abstraction_conjectures.append(
                {
                    "conjecture_id": f"conj.{counter:03d}",
                    "bridge_id": context["bridge_id"],
                    "from_id": src,
                    "to_id": dst,
                    "bridge_type": context["bridge_type"],
                    "gap_score": round(gap_score, 4),
                    "abstraction_type": family,
                    "abstraction_label": object_profile.get("label", _family_label(family, context)),
                    "carrier_kind": object_profile.get("carrier_kind", "bridge carrier"),
                    "typing_status": object_profile.get("typing_status", "typed"),
                    "mathematical_object_role": _family_role(family, context),
                    "gap_target": ", ".join(context["gap_axes"][:3]) or "bridge under-specification",
                    "support_antecedent_schema": context["support_antecedent_schema"] or "unconditional",
                    "target_consequence_schema": context["target_consequence_schema"] or "statement-conclusion",
                    "preserved_invariant": context["preserved_invariant"] or "support-target interface",
                    "barrier_scope": context["barrier_scope"] or "none",
                    "statement_delta": context.get("statement_delta", {}),
                    "anchor_concepts": [anchor_term] if anchor_term else [],
                    "shared_terms": shared_terms[:6],
                    "missing_from_source": missing_from_source[:6],
                    "missing_from_target": missing_from_target[:6],
                    "construction_template": _construction_template(family, context),
                    "validation_questions": _validation_questions(family, context),
                    "definitional_profile": definitional_profile,
                    "mathematical_specification": mathematical_specification,
                    "counterfactual_probes": counterfactuals,
                    "novelty_signal": round(novelty_signal, 4),
                    "feasibility_signal": round(feasibility_signal, 4),
                    "definitional_completeness": round(definitional_score, 4),
                    "counterfactual_sharpness": round(counterfactual_score, 4),
                    "priority": round(priority, 4),
                }
            )
            counter += 1

    gap_clusters.sort(key=lambda row: (_safe_float(row.get("gap_score"), 0.0), _safe_float(row.get("bridge_score"), 0.0)), reverse=True)
    abstraction_conjectures.sort(key=lambda row: _safe_float(row.get("priority"), 0.0), reverse=True)
    return {
        "gap_clusters": gap_clusters,
        "abstraction_conjectures": abstraction_conjectures,
    }



def _build(
    analysis: dict[str, Any],
    entrypoints: dict[str, Any],
    pathways: dict[str, Any],
    bridges: dict[str, Any],
    phyp: dict[str, Any],
    hardness: dict[str, Any],
    top_bridges: int,
    max_conjectures_per_bridge: int,
) -> dict[str, Any]:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Primary callable implementing a stage-level behavior.
    Contribution: Binds gap diagnosis and abstraction-family ranking into a reproducible conjecture artifact.
    """

    trimmed_bridges = {
        "bridge_programs": [
            row for row in (bridges.get("bridge_programs", []) if isinstance(bridges.get("bridge_programs"), list) else [])[: max(1, top_bridges)]
            if isinstance(row, dict)
        ]
    }
    rows = _conjecture_rows(
        bridges=trimmed_bridges,
        analysis_lookup=_analysis_lookup(analysis),
        pathways=pathways,
        phyp_pairs=_pair_hypotheses(phyp),
        hardness=hardness,
        max_conjectures_per_bridge=max(1, max_conjectures_per_bridge),
    )
    return {
        "metadata": {
            "input_connection_candidates": len(analysis.get("connection_candidates", []) if isinstance(analysis.get("connection_candidates"), list) else []),
            "input_entrypoints": len(entrypoints.get("ranked_entrypoints", []) if isinstance(entrypoints.get("ranked_entrypoints"), list) else []),
            "input_pathways": len(pathways.get("pathways", []) if isinstance(pathways.get("pathways"), list) else []),
            "input_bridges": len(trimmed_bridges.get("bridge_programs", [])),
            "input_hypotheses": len(phyp.get("hypotheses", []) if isinstance(phyp.get("hypotheses"), list) else []),
            "input_hardness_elements": len(hardness.get("essential_elements", []) if isinstance(hardness.get("essential_elements"), list) else []),
            "gap_cluster_count": len(rows["gap_clusters"]),
            "abstraction_conjecture_count": len(rows["abstraction_conjectures"]),
            "selection_policy": "bridge leverage + concept-gap severity + abstraction-family fit + definitional/counterfactual sharpness",
            "inference_mode": "conjecture",
        },
        "gap_clusters": rows["gap_clusters"],
        "abstraction_conjectures": rows["abstraction_conjectures"],
        "recommended_run_order": [row.get("conjecture_id", "") for row in rows["abstraction_conjectures"][:12] if str(row.get("conjecture_id", "")).strip()],
    }



def _to_markdown(report: dict[str, Any]) -> str:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: Rendering internal outputs into human-readable artifacts.
    Contribution: Makes the concept-gap analysis and abstraction conjectures readable to mathematicians inspecting the run.
    """

    meta = report.get("metadata", {}) if isinstance(report.get("metadata"), dict) else {}
    gap_clusters = report.get("gap_clusters", []) if isinstance(report.get("gap_clusters"), list) else []
    conjectures = report.get("abstraction_conjectures", []) if isinstance(report.get("abstraction_conjectures"), list) else []

    lines: list[str] = []
    lines.append("# Concept-Gap Abstraction Conjectures")
    lines.append("")
    lines.append("This report identifies where current bridge programs are mathematically under-specified and which abstraction types could close those gaps.")
    lines.append("")
    lines.append("## Stats")
    lines.append("")
    lines.append(f"- Inference mode: {meta.get('inference_mode', 'conjecture')}")
    lines.append(f"- Bridges inspected: {meta.get('input_bridges', 0)}")
    lines.append(f"- Gap clusters: {meta.get('gap_cluster_count', 0)}")
    lines.append(f"- Abstraction conjectures: {meta.get('abstraction_conjecture_count', 0)}")
    lines.append(f"- Selection policy: {meta.get('selection_policy', '')}")
    lines.append("")

    lines.append("## Gap Diagnostics")
    lines.append("")
    lines.append("| bridge | type | gap_score | dominant axes | shared terms |")
    lines.append("|---|---|---|---|---|")
    for row in gap_clusters[:12]:
        axes = ", ".join(str(item.get("axis", "")) for item in row.get("gap_axes", [])[:3] if isinstance(item, dict))
        shared = ", ".join(str(item) for item in row.get("shared_terms", [])[:3])
        lines.append(
            f"| {row.get('bridge_id', '')} | {row.get('bridge_type', '')} | {row.get('gap_score', 0.0)} | {axes or 'none'} | {shared or 'none'} |"
        )
    lines.append("")

    for row in gap_clusters[:8]:
        lines.append(f"### {row.get('bridge_id', '')} - {row.get('bridge_type', '')}")
        lines.append(f"- Bridge: `{row.get('from_id', '')}` -> `{row.get('to_id', '')}`")
        lines.append(f"- Gap score: {row.get('gap_score', 0.0)}")
        if row.get("gap_axes"):
            lines.append("- Gap axes:")
            for axis in row.get("gap_axes", [])[:5]:
                if not isinstance(axis, dict):
                    continue
                lines.append(
                    f"  - {axis.get('axis', '')} ({axis.get('severity', 0.0)}): {axis.get('detail', '')}"
                )
        if row.get("shared_terms"):
            lines.append(f"- Shared typed terms: {', '.join(row.get('shared_terms', [])[:8])}")
        if row.get("missing_from_source"):
            lines.append(f"- Missing from source: {', '.join(row.get('missing_from_source', [])[:8])}")
        if row.get("missing_from_target"):
            lines.append(f"- Missing from target: {', '.join(row.get('missing_from_target', [])[:8])}")
        if row.get("recommended_abstraction_families"):
            lines.append(
                f"- Candidate abstraction families: {', '.join(row.get('recommended_abstraction_families', [])[:5])}"
            )
        lines.append("")

    lines.append("## Abstraction Conjectures")
    lines.append("")
    for row in conjectures[:16]:
        lines.append(f"### {row.get('conjecture_id', '')} - {row.get('abstraction_label', '')}")
        lines.append(f"- Bridge: {row.get('bridge_id', '')} (`{row.get('from_id', '')}` -> `{row.get('to_id', '')}`)")
        lines.append(f"- Abstraction type: {row.get('abstraction_type', '')}")
        lines.append(f"- Carrier kind: {row.get('carrier_kind', '')}")
        lines.append(f"- Typing status: {row.get('typing_status', '')}")
        lines.append(f"- Priority: {row.get('priority', 0.0)}")
        lines.append(f"- Gap target: {row.get('gap_target', '')}")
        lines.append(f"- Role: {row.get('mathematical_object_role', '')}")
        lines.append(
            f"- Commitments: antecedent={row.get('support_antecedent_schema', '')}; consequence={row.get('target_consequence_schema', '')}; invariant={row.get('preserved_invariant', '')}; barrier={row.get('barrier_scope', '')}"
        )
        lines.append(
            f"- Definitional completeness: {row.get('definitional_completeness', 0.0)}; counterfactual sharpness: {row.get('counterfactual_sharpness', 0.0)}"
        )
        if row.get("shared_terms"):
            lines.append(f"- Shared terms: {', '.join(row.get('shared_terms', [])[:6])}")
        if row.get("missing_from_source"):
            lines.append(f"- Missing from source: {', '.join(row.get('missing_from_source', [])[:6])}")
        if row.get("missing_from_target"):
            lines.append(f"- Missing from target: {', '.join(row.get('missing_from_target', [])[:6])}")
        definitional = row.get("definitional_profile", {}) if isinstance(row.get("definitional_profile"), dict) else {}
        mathematical_spec = row.get("mathematical_specification", {}) if isinstance(row.get("mathematical_specification"), dict) else {}
        necessary = definitional.get("necessary_attributes", []) if isinstance(definitional.get("necessary_attributes"), list) else []
        sufficient = definitional.get("sufficient_attribute_sets", []) if isinstance(definitional.get("sufficient_attribute_sets"), list) else []
        if definitional.get("bridging_concept_definition"):
            lines.append(f"- Definition: {definitional.get('bridging_concept_definition', '')}")
        if mathematical_spec:
            lines.append(f"- Source regime: {mathematical_spec.get('source_regime', '')}")
            lines.append(f"- Target regime: {mathematical_spec.get('target_regime', '')}")
            delta = mathematical_spec.get("statement_delta", {}) if isinstance(mathematical_spec.get("statement_delta"), dict) else {}
            if delta:
                lines.append(f"- Route synopsis: {delta.get('route_synopsis', '')}")
                lines.append(f"- Model shift: {delta.get('model_shift', '')}")
                lines.append(f"- Threshold shift: {delta.get('threshold_shift', '')}")
                lines.append(f"- Consequence shift: {delta.get('consequence_shift', '')}")
                lines.append(f"- Missing route lemma: {delta.get('missing_witness_or_transport', '')}")
            lines.append(f"- Object sort: {mathematical_spec.get('object_sort', '')}")
            lines.append(f"- Conditional claim: {mathematical_spec.get('conditional_claim', '')}")
            assumptions = mathematical_spec.get("assumptions", []) if isinstance(mathematical_spec.get("assumptions"), list) else []
            if assumptions:
                lines.append("- Assumptions:")
                for item in assumptions[:4]:
                    lines.append(f"  - {item}")
            proof_templates = mathematical_spec.get("proof_obligation_templates", []) if isinstance(mathematical_spec.get("proof_obligation_templates"), list) else []
            if proof_templates:
                lines.append("- Theorem-shaped proof obligations:")
                for item in proof_templates[:4]:
                    lines.append(f"  - {item}")
            if mathematical_spec.get("obstruction_template"):
                lines.append(f"- Obstruction template: {mathematical_spec.get('obstruction_template', '')}")
        if necessary:
            lines.append("- Necessary attributes:")
            for attr in necessary[:5]:
                if not isinstance(attr, dict):
                    continue
                lines.append(f"  - {attr.get('attribute', '')}: {attr.get('rationale', '')}")
        if sufficient:
            lines.append("- Sufficient attribute sets:")
            for item in sufficient[:3]:
                if not isinstance(item, dict):
                    continue
                attrs = item.get("attributes", []) if isinstance(item.get("attributes"), list) else []
                lines.append(f"  - {item.get('label', '')}: {', '.join(str(x) for x in attrs[:5])}")
        counterfactuals = row.get("counterfactual_probes", []) if isinstance(row.get("counterfactual_probes"), list) else []
        if counterfactuals:
            lines.append("- Counterfactual probes:")
            for probe in counterfactuals[:3]:
                if not isinstance(probe, dict):
                    continue
                lines.append(
                    f"  - {probe.get('intervention', '')} => {probe.get('expected_bridge_effect', '')} ({probe.get('diagnostic_use', '')})"
                )
        lines.append("- Construction template:")
        for step in row.get("construction_template", [])[:4]:
            lines.append(f"  - {step}")
        lines.append("- Validation questions:")
        for question in row.get("validation_questions", [])[:4]:
            lines.append(f"  - {question}")
        lines.append("")

    lines.append("## Recommended Run Order")
    lines.append("")
    for idx, item in enumerate(report.get("recommended_run_order", [])[:12], start=1):
        lines.append(f"{idx}. `{item}`")
    lines.append("")
    return "\n".join(lines)



def main() -> int:
    """
    Relevance: Operates within the conjecture-mode abstraction synthesis layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds parsing, computation, and artifact emission into a reproducible script execution.
    """

    logger = ReasoningLogger("kb-gap-abstraction-conjecturer")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--analysis", required=True)
    ap.add_argument("--entrypoints", required=True)
    ap.add_argument("--pathways", required=True)
    ap.add_argument("--bridges", required=True)
    ap.add_argument("--phyp", required=True)
    ap.add_argument("--hardness")
    ap.add_argument("--top-bridges", type=int, default=12)
    ap.add_argument("--max-conjectures-per-bridge", type=int, default=3)
    ap.add_argument("--output-json")
    ap.add_argument("--output-md")
    args = ap.parse_args()
    logger.step(
        "Parsed gap-abstraction-conjecturer arguments",
        "\n".join(
            [
                f"analysis={args.analysis}",
                f"entrypoints={args.entrypoints}",
                f"pathways={args.pathways}",
                f"bridges={args.bridges}",
                f"phyp={args.phyp}",
                f"hardness={args.hardness or ''}",
                f"top_bridges={args.top_bridges}",
                f"max_conjectures_per_bridge={args.max_conjectures_per_bridge}",
                f"output_json={args.output_json or ''}",
                f"output_md={args.output_md or ''}",
            ]
        ),
    )

    analysis_path = Path(args.analysis)
    entrypoints_path = Path(args.entrypoints)
    pathways_path = Path(args.pathways)
    bridges_path = Path(args.bridges)
    phyp_path = Path(args.phyp)
    hardness_path = Path(args.hardness) if args.hardness else None

    for path in [analysis_path, entrypoints_path, pathways_path, bridges_path, phyp_path]:
        if not path.exists():
            log_path = logger.finalize("error", summary=f"Missing input: {path}")
            print(f"[LOG] {log_path}", file=sys.stderr)
            raise SystemExit(f"[ERROR] Missing input: {path}")
    if hardness_path and not hardness_path.exists():
        log_path = logger.finalize("error", summary=f"Missing input: {hardness_path}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Missing input: {hardness_path}")

    try:
        analysis = validate_connection_analysis(json.loads(analysis_path.read_text(encoding="utf-8")), name="analysis")
        entrypoints = validate_entrypoints(json.loads(entrypoints_path.read_text(encoding="utf-8")), name="entrypoints")
        pathways = validate_pathways(json.loads(pathways_path.read_text(encoding="utf-8")), name="pathways")
        bridges = validate_bridges(json.loads(bridges_path.read_text(encoding="utf-8")), name="bridges")
        phyp = validate_phyp(yaml.safe_load(phyp_path.read_text(encoding="utf-8")), name="phyp")
        hardness = json.loads(hardness_path.read_text(encoding="utf-8")) if hardness_path else {}
        if not isinstance(hardness, dict):
            hardness = {}

        report = _build(
            analysis=analysis,
            entrypoints=entrypoints,
            pathways=pathways,
            bridges=bridges,
            phyp=phyp,
            hardness=hardness,
            top_bridges=max(1, args.top_bridges),
            max_conjectures_per_bridge=max(1, args.max_conjectures_per_bridge),
        )
        gap_clusters = report.get("gap_clusters", []) if isinstance(report.get("gap_clusters"), list) else []
        conjectures = report.get("abstraction_conjectures", []) if isinstance(report.get("abstraction_conjectures"), list) else []
        logger.step(
            "Concept gap trace",
            "\n".join(
                [
                    "top_gap_clusters="
                    + "; ".join(
                        f"{row.get('bridge_id', '')}:{row.get('gap_score', 0.0):.4f}:[{', '.join(str(axis.get('axis', '')) for axis in row.get('gap_axes', [])[:2] if isinstance(axis, dict))}]"
                        for row in gap_clusters[:6]
                        if isinstance(row, dict)
                    ),
                "top_abstractions="
                + "; ".join(
                    f"{row.get('conjecture_id', '')}:{row.get('abstraction_type', '')}:{row.get('priority', 0.0):.4f}:{row.get('abstraction_label', '')}"
                    for row in conjectures[:6]
                    if isinstance(row, dict)
                ),
                "top_conditional_claims="
                + "; ".join(
                    f"{row.get('conjecture_id', '')}:{str((row.get('mathematical_specification', {}) if isinstance(row.get('mathematical_specification'), dict) else {}).get('conditional_claim', '')).strip()}"
                    for row in conjectures[:4]
                    if isinstance(row, dict)
                    and str((row.get('mathematical_specification', {}) if isinstance(row.get('mathematical_specification'), dict) else {}).get("conditional_claim", "")).strip()
                ),
            ]
        ),
    )

        if args.output_json:
            out_json = Path(args.output_json)
            out_json.parent.mkdir(parents=True, exist_ok=True)
            out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"[OK] Wrote JSON: {out_json}")
            logger.add_output("gap_abstraction_conjectures_json", out_json)

        markdown = _to_markdown(report)
        if args.output_md:
            out_md = Path(args.output_md)
            out_md.parent.mkdir(parents=True, exist_ok=True)
            out_md.write_text(markdown, encoding="utf-8")
            print(f"[OK] Wrote Markdown: {out_md}")
            logger.add_output("gap_abstraction_conjectures_md", out_md)

        if conjectures:
            top = conjectures[0]
            logger.step(
                "Selected top abstraction conjecture",
                "\n".join(
                    [
                        f"conjecture_id={top.get('conjecture_id', '')}",
                        f"abstraction_type={top.get('abstraction_type', '')}",
                        f"priority={top.get('priority', 0.0)}",
                        f"label={top.get('abstraction_label', '')}",
                        "conditional_claim="
                        + str(
                            (top.get("mathematical_specification", {}) if isinstance(top.get("mathematical_specification"), dict) else {}).get(
                                "conditional_claim", ""
                            )
                        ).strip(),
                    ]
                ),
            )

        log_path = logger.finalize(
            "success",
            summary=f"Generated {len(conjectures)} abstraction conjectures across {len(gap_clusters)} bridge gaps.",
        )
        print(f"[LOG] {log_path}")
        return 0
    except Exception as exc:
        log_path = logger.finalize("error", summary=f"Gap-abstraction conjecture stage failed: {exc}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
