#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Generate structured proof sketches for prioritized conjectured bridge concepts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from contracts import validate_bridges
from contracts import validate_coherence_report
from contracts import validate_conjecture_report
from contracts import validate_phyp
from contracts import validate_proof_sketch_report
from contracts import validate_strategy_report
from negative_route_heuristic import build_negative_route_heuristic
from reasoning_log import ReasoningLogger
from statement_text import load_statement_index
from statement_text import statement_excerpt


STRATEGY_FAMILY_CATALOG: dict[str, str] = {
    "invariant-lift-through-intermediate-object": (
        "Introduce a conjectured intermediate object or invariant, prove that the source regime induces it, "
        "then force the target consequence through that invariant."
    ),
    "spectral-calculus-realization": (
        "Use spectral theorem or functional calculus data to realize the hidden bridge object, then exponentiate or reconstruct the target dynamics from that representation."
    ),
    "generator-recovery-from-unitary-orbits": (
        "Recover the infinitesimal generator from strongly continuous orbit data, prove the required domain and closure properties, then identify the target operator."
    ),
    "domain-core-self-adjointness": (
        "Build a dense core on which the hidden operator is well-defined, prove symmetry or closure there, and upgrade the core data to self-adjointness."
    ),
    "measure-construction-from-positive-functional": (
        "Recover the hidden measure object from positivity on the function space, then prove that the resulting set function is regular and uniquely represents the target functional."
    ),
    "regularity-via-compact-open-approximation": (
        "Use compact-open approximation, Urysohn-type separation, and regularity reconstruction to turn topological control into a unique representing measure."
    ),
    "integration-duality-decomposition": (
        "Express the target functional through integration against a regular measure, then extend to signed or complex duality using Jordan decomposition or total variation control."
    ),
    "affine-averaging-to-fixed-point": (
        "Use affine orbit averages inside the compact convex set, extract a limiting witness by compactness, and prove that the limit is a fixed point for the single map."
    ),
    "invariant-fixed-point-subset-reduction": (
        "Construct the fixed-point subset of one map, prove it is nonempty compact convex and preserved by commuting maps, then recurse on the reduced invariant subset."
    ),
    "finite-intersection-compactness-lift": (
        "Show every finite commuting subfamily has a common fixed point, package these as nonempty compact sets, and use finite intersection plus compactness to obtain a point fixed by the whole family."
    ),
    "surrogate-reduction-transfer": (
        "Define a surrogate object or promise problem, reduce the source statement into it, and transfer the required "
        "consequence through the surrogate interface."
    ),
    "barrier-escape-reencoding": (
        "Re-encode the conjectured bridge concept in a representation that preserves the intended invariant while "
        "sidestepping the currently dominant barrier family."
    ),
    "contradiction-via-collapse-or-separation": (
        "Assume the conjectured bridge fails or the target consequence does not hold, then derive a forbidden collapse "
        "or contradiction with a known separation profile."
    ),
    "bootstrapped-derandomization-transfer": (
        "Use a derandomization or pseudorandomness-style object as the bridge, then bootstrap it into a lower-bound or separation consequence."
    ),
    "case-split-regime-transfer": (
        "Partition the argument by regime, model, or threshold case, prove each branch against the same bridge concept, and reassemble the target consequence."
    ),
}

_TOKEN_RE = re.compile(r"[a-z0-9]+")
def _safe_float(value: Any, default: float = 0.0) -> float:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: Defensive conversion/parsing to keep scoring and reporting robust.
    Contribution: Reduces runtime ambiguity and prevents malformed artifacts from destabilizing the workflow.
    """

    try:
        return float(value)
    except (TypeError, ValueError):
        return default



def _load_kb_statements(kb_path: Path | None) -> dict[str, dict[str, Any]]:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: Deterministic recovery of typed KB statements for narrative rendering.
    Contribution: Lets the paper-style argument cite the actual mathematical source statement rather than internal IDs only.
    """

    return load_statement_index(kb_path)



def _as_list(value: Any) -> list[Any]:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: Defensive normalization of artifact fields into list form.
    Contribution: Keeps later proof-sketch assembly deterministic even when optional fields are missing.
    """

    return value if isinstance(value, list) else []


def _statement_body(statement: dict[str, Any]) -> str:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: Rendering stored KB statements into compact mathematical prose.
    Contribution: Surfaces the theorem family that the proof sketch is trying to realize.
    """

    return statement_excerpt(statement, limit=420)


def _route_delta(
    conjecture: dict[str, Any],
    bridge: dict[str, Any],
    kb_statements: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: Consolidation of the bridge/conjecture statement delta with optional theorem excerpts.
    Contribution: Gives obligations and lemmas a route-specific mathematical payload rather than only schema labels.
    """

    delta: dict[str, Any] = {}
    if isinstance(bridge.get("statement_delta"), dict):
        delta.update(bridge.get("statement_delta", {}))
    if isinstance(conjecture.get("statement_delta"), dict):
        delta.update(conjecture.get("statement_delta", {}))
    source_id = str(bridge.get("from_id", "")).strip()
    target_id = str(bridge.get("to_id", "")).strip()
    kb_statements = kb_statements or {}
    source_excerpt = _statement_body(kb_statements.get(source_id, {})) if source_id else ""
    target_excerpt = _statement_body(kb_statements.get(target_id, {})) if target_id else ""
    if source_excerpt:
        delta.setdefault("source_theorem_excerpt", source_excerpt)
    if target_excerpt:
        delta.setdefault("target_theorem_excerpt", target_excerpt)
    return delta


def _token_set(*values: Any) -> set[str]:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: Lightweight tokenization over already-structured artifact fields.
    Contribution: Supports deterministic matching between conjectures and strategies without scanning raw KB prose.
    """

    tokens: set[str] = set()
    for value in values:
        if isinstance(value, list):
            parts = [str(item) for item in value]
        else:
            parts = [str(value)]
        for part in parts:
            for token in _TOKEN_RE.findall(part.lower()):
                if len(token) >= 3:
                    tokens.add(token)
    return tokens



def _coherence_index(coherence: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: Construction of a hypothesis-level coherence lookup.
    Contribution: Lets proof sketches prefer conjectures whose supporting hypotheses are less globally damaging.
    """

    out: dict[str, dict[str, Any]] = {}
    rows = coherence.get("hypothesis_coherence", []) if isinstance(coherence.get("hypothesis_coherence"), list) else []
    for row in rows:
        if not isinstance(row, dict):
            continue
        hid = str(row.get("hypothesis_id", "")).strip()
        if hid:
            out[hid] = row
    return out



def _bridge_lookup(bridges: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: Construction of derived lookups from bridge-plan outputs.
    Contribution: Aligns each conjecture with the inferential commitment that its proof sketch must realize.
    """

    out: dict[str, dict[str, Any]] = {}
    for row in bridges.get("bridge_programs", []) if isinstance(bridges.get("bridge_programs"), list) else []:
        if not isinstance(row, dict):
            continue
        bridge_id = str(row.get("bridge_id", "")).strip()
        if bridge_id:
            out[bridge_id] = row
    return out



def _strategy_lookup(strategies: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: Construction of derived lookups from strategy outputs.
    Contribution: Makes strategy-level anchor, phase, and bridge selections directly reusable during proof-sketch selection.
    """

    out: dict[str, dict[str, Any]] = {}
    for row in strategies.get("strategies", []) if isinstance(strategies.get("strategies"), list) else []:
        if not isinstance(row, dict):
            continue
        sid = str(row.get("strategy_id", "")).strip()
        if sid:
            out[sid] = row
    return out



def _hypothesis_lookup(phyp: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: Construction of hypothesis lookups from the proof-hypothesis artifact.
    Contribution: Carries explicit support statements and kinds into proof obligations and lemma suggestions.
    """

    out: dict[str, dict[str, Any]] = {}
    for row in phyp.get("hypotheses", []) if isinstance(phyp.get("hypotheses"), list) else []:
        if not isinstance(row, dict):
            continue
        hid = str(row.get("id", "")).strip()
        if hid:
            out[hid] = row
    return out



def _strategy_family(conjecture: dict[str, Any], strategy: dict[str, Any], bridge: dict[str, Any]) -> str:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: Typed classification of proof-sketch regimes.
    Contribution: Chooses the proof architecture that best matches the conjecture's inferential burden and barrier profile.
    """

    abstraction_type = str(conjecture.get("abstraction_type", "")).strip().lower()
    gap_target = str(conjecture.get("gap_target", "")).strip().lower()
    consequence = str(conjecture.get("target_consequence_schema", "")).strip().lower()
    antecedent = str(bridge.get("inferential_commitment", {}).get("support_antecedent_schema", "")).strip().lower()
    barrier = str(conjecture.get("barrier_scope") or bridge.get("inferential_commitment", {}).get("barrier_scope", "")).strip().lower()
    phase = str(strategy.get("phase", "")).strip().lower()
    blob = " ".join(
        [
            abstraction_type,
            gap_target,
            consequence,
            antecedent,
            phase,
            str(conjecture.get("abstraction_label", "")),
            str(conjecture.get("preserved_invariant", "")),
            str(conjecture.get("mathematical_object_role", "")),
            str(bridge.get("bridge_type", "")),
        ]
    ).lower()

    if any(token in blob for token in ("spectral theorem", "functional calculus", "projection-valued measure", "spectral-functional-calculus", "spectral-calculus")):
        return "spectral-calculus-realization"
    if any(token in blob for token in ("stone", "unitary group", "strongly-continuous-unitary-group", "unitary-generator", "self-adjoint generator")):
        return "generator-recovery-from-unitary-orbits"
    if any(
        token in blob
        for token in (
            "finite-intersection-property",
            "common-fixed-point-for-finite-commuting-family",
            "common-fixed-point-for-commuting-family",
            "finite-intersection-property-implies-common-fixed-point",
        )
    ):
        return "finite-intersection-compactness-lift"
    if any(token in blob for token in ("cesaro-averaging", "affine averaging", "single-affine-map-fixed-point", "affine-orbit-averages-in-compact-convex-set")):
        return "affine-averaging-to-fixed-point"
    if any(
        token in blob
        for token in (
            "markov-kakutani",
            "common fixed point",
            "invariant-fixed-point-subset",
            "fixed-point-subset-bridge",
            "single-map-fixed-point-implies-invariant-fixed-point-subset",
            "commutativity-implies-fixed-point-subset-invariance",
            "commuting-affine-family",
            "compact-convex",
        )
    ):
        return "invariant-fixed-point-subset-reduction"
    if any(token in blob for token in ("self-adjoint", "selfadjoint", "skew-adjoint", "dense core", "core", "symmetry", "domain")):
        return "domain-core-self-adjointness"
    if any(token in blob for token in ("positive-functional-implies-regular-measure", "riesz-markov-kakutani", "regular-borel-measure-representation", "positive linear functional", "regular borel measure")):
        return "measure-construction-from-positive-functional"
    if any(token in blob for token in ("function-separation-implies-measure-uniqueness", "compact-open-approximation", "inner regular", "outer regular", "urysohn")):
        return "regularity-via-compact-open-approximation"
    if any(token in blob for token in ("integration-defines-positive-functional", "signed-regular-measure-duality", "c0-dual-implies-signed-regular-measure", "total variation")):
        return "integration-duality-decomposition"
    if barrier and barrier != "none":
        return "barrier-escape-reencoding"
    if any(token in abstraction_type for token in ("surrogate", "promise", "reduction")) or "transfer-mechanism-gap" in gap_target:
        return "surrogate-reduction-transfer"
    if any(token in antecedent for token in ("pit", "derandom", "prg", "bpp", "random")):
        return "bootstrapped-derandomization-transfer"
    if "collapse" in consequence or ("separation" in consequence and any(token in phase for token in ("barrier", "meta"))):
        return "contradiction-via-collapse-or-separation"
    if any(token in abstraction_type for token in ("intermediate", "invariant", "certificate", "measure")) or "missing-intermediate-abstraction" in gap_target:
        return "invariant-lift-through-intermediate-object"
    if "model-mismatch" in gap_target or "regime" in gap_target or any(token in phase for token in ("nonuniform", "proof", "algebraic")):
        return "case-split-regime-transfer"
    return "invariant-lift-through-intermediate-object"



def _match_score(conjecture: dict[str, Any], strategy: dict[str, Any], bridge: dict[str, Any], coherence_index: dict[str, dict[str, Any]]) -> float:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: Selection/retrieval scoring over conjecture-strategy pairs.
    Contribution: Prioritizes proof sketches that are simultaneously strong, aligned, and less coherence-damaging.
    """

    priority = _safe_float(conjecture.get("priority", 0.0))
    strategy_score = _safe_float(strategy.get("strategy_score", 0.0))
    definitional = _safe_float(conjecture.get("definitional_completeness", 0.0))
    counterfactual = _safe_float(conjecture.get("counterfactual_sharpness", 0.0))

    bridge_id = str(conjecture.get("bridge_id", "")).strip()
    bridge_bonus = 0.15 if bridge_id and bridge_id in {str(x).strip() for x in _as_list(strategy.get("bridge_ids"))} else 0.0

    conj_tokens = _token_set(
        conjecture.get("abstraction_label", ""),
        conjecture.get("abstraction_type", ""),
        conjecture.get("gap_target", ""),
        conjecture.get("target_consequence_schema", ""),
        conjecture.get("preserved_invariant", ""),
        conjecture.get("mathematical_object_role", ""),
    )
    strat_tokens = _token_set(
        strategy.get("phase", ""),
        strategy.get("name", ""),
        strategy.get("anchor_concepts", []),
        strategy.get("bridge_concepts", []),
        strategy.get("abstraction_concepts", []),
        strategy.get("definitional_focus", []),
    )
    overlap = len(conj_tokens & strat_tokens) / max(1, len(conj_tokens | strat_tokens))

    coherence_rows = [coherence_index.get(str(hid).strip(), {}) for hid in _as_list(strategy.get("hypothesis_ids"))]
    if coherence_rows:
        coherence_avg = sum(_safe_float(row.get("coherence_delta_global", 0.0)) for row in coherence_rows if isinstance(row, dict)) / len(coherence_rows)
    else:
        coherence_avg = 0.0
    coherence_bonus = max(-0.08, min(0.08, coherence_avg))

    family = _strategy_family(conjecture, strategy, bridge)
    family_bonus = 0.04 if family == "invariant-lift-through-intermediate-object" and "intermediate" in str(conjecture.get("abstraction_type", "")).lower() else 0.0

    return max(
        0.0,
        min(
            1.0,
            0.38 * priority
            + 0.28 * strategy_score
            + 0.12 * definitional
            + 0.10 * counterfactual
            + 0.12 * overlap
            + bridge_bonus
            + coherence_bonus
            + family_bonus,
        ),
    )


def _obligation_claim(
    *,
    attribute: str,
    kind: str,
    label: str,
    carrier_kind: str,
    source_id: str,
    target_id: str,
    antecedent: str,
    consequence: str,
    invariant: str,
    barrier_scope: str,
    route_delta: dict[str, Any],
) -> str:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: Translation of definitional attributes into theorem-shaped obligations.
    Contribution: Makes proof obligations inspectable as mathematical claims instead of pipeline reminders.
    """

    kind = kind.strip()
    source_focus = str(route_delta.get("source_claim_focus", "")).strip() or antecedent
    target_focus = str(route_delta.get("target_claim_focus", "")).strip() or consequence
    model_shift = str(route_delta.get("model_shift", "")).strip() or f"`{source_id}` -> `{target_id}`"
    threshold_shift = str(route_delta.get("threshold_shift", "")).strip() or "threshold shift not yet typed"
    missing_lemma = str(route_delta.get("missing_witness_or_transport", "")).strip()
    if kind == "antecedent-realization":
        return (
            f"Prove the source-to-object claim: the source-side content `{source_focus}` available at `{source_id}` "
            f"can be organized into `{label}` as a {carrier_kind}."
        )
    if kind == "invariant-preservation":
        return (
            f"Prove the transport claim: every admissible realization of `{label}` preserves `{invariant}` "
            f"while crossing the route {model_shift}."
        )
    if kind == "consequence-forcing":
        return (
            f"Prove the payoff claim: once `{label}` carries the route data from `{source_focus}` toward `{target_focus}`, it forces `{consequence}` at `{target_id}`."
        )
    if kind == "model-alignment":
        return (
            f"Exhibit the model-alignment claim: `{label}` gives a faithful translation across {model_shift}."
        )
    if kind == "transfer-law":
        return (
            f"Construct the transfer-law claim: an explicit reduction or transport map sends `{source_focus}` into `{label}` "
            f"without losing the route to `{consequence}`."
        )
    if kind == "barrier-evasion":
        return (
            f"Prove the barrier-evasion claim: the realization of `{label}` stays outside barrier scope `{barrier_scope}` "
            "while preserving the intended source-to-target content."
        )
    if kind == "explicit-object-witness":
        return f"Define the witness claim: give an explicit {carrier_kind} realization of `{label}` rather than a role-description only."
    if kind == "operationalizability" and missing_lemma:
        return f"Discharge the route lemma: {missing_lemma}"
    if kind == "promise-control":
        return f"Make the threshold control explicit: `{label}` must realize the shift {threshold_shift} in a mathematically checkable way."
    return f"Prove the bridge claim: `{label}` satisfies `{attribute}` on the route from `{source_focus}` to `{target_focus}`."


def _proof_obligations(
    conjecture: dict[str, Any],
    bridge: dict[str, Any],
    strategy: dict[str, Any],
    kb_statements: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, str]]:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: Construction of theorem-family-specific proof obligations.
    Contribution: Turns a broad sketch into a concrete checklist of claims that must be discharged.
    """

    obligations: list[dict[str, str]] = []
    definitional = conjecture.get("definitional_profile", {}) if isinstance(conjecture.get("definitional_profile"), dict) else {}
    necessary = definitional.get("necessary_attributes", []) if isinstance(definitional.get("necessary_attributes"), list) else []
    label = str(conjecture.get("abstraction_label", "candidate bridge object")).strip() or "candidate bridge object"
    carrier_kind = str(conjecture.get("carrier_kind", "")).strip() or "bridge carrier"
    source_id = str(bridge.get("from_id", "")).strip() or "source statement"
    target_id = str(bridge.get("to_id", "")).strip() or "target statement"
    antecedent = str(conjecture.get("support_antecedent_schema") or bridge.get("inferential_commitment", {}).get("support_antecedent_schema", "source-side theorem schema")).strip()
    consequence = str(conjecture.get("target_consequence_schema") or bridge.get("inferential_commitment", {}).get("target_consequence_schema", "statement-conclusion")).strip()
    invariant = str(conjecture.get("preserved_invariant") or bridge.get("inferential_commitment", {}).get("preserved_invariant", "support-to-target interface")).strip()
    barrier_scope = str(conjecture.get("barrier_scope") or bridge.get("inferential_commitment", {}).get("barrier_scope", "none")).strip() or "none"
    route_delta = _route_delta(conjecture, bridge, kb_statements=kb_statements)
    for idx, attr in enumerate(necessary[:4], start=1):
        if not isinstance(attr, dict):
            continue
        requirement = _obligation_claim(
            attribute=str(attr.get("attribute", "")).strip(),
            kind=str(attr.get("kind", "")).strip(),
            label=label,
            carrier_kind=carrier_kind,
            source_id=source_id,
            target_id=target_id,
            antecedent=antecedent,
            consequence=consequence,
            invariant=invariant,
            barrier_scope=barrier_scope,
            route_delta=route_delta,
        )
        obligations.append(
            {
                "obligation_id": f"obl.{idx:02d}",
                "kind": str(attr.get("kind", "")).strip() or "definitional-claim",
                "requirement": requirement,
                "claim_template": requirement,
                "why_it_matters": str(
                    attr.get("why_it_matters")
                    or attr.get("rationale")
                    or "Definitional commitment for the bridge concept."
                ).strip(),
                "derived_from": f"{conjecture.get('conjecture_id', '')}:definitional-profile",
            }
        )
    obligations.extend(
        [
            {
                "obligation_id": f"obl.{len(obligations)+1:02d}",
                "kind": "transport-claim",
                "requirement": f"Show that every admissible realization of `{label}` preserves `{invariant}` across {route_delta.get('model_shift', f'`{source_id}` -> `{target_id}`')}.",
                "claim_template": f"Every admissible realization of `{label}` preserves `{invariant}` across {route_delta.get('model_shift', f'`{source_id}` -> `{target_id}`')}.",
                "why_it_matters": "Without invariant preservation, the bridge concept does not carry the relevant mathematical structure.",
                "derived_from": f"{bridge.get('bridge_id', '')}:inferential-commitment",
            },
            {
                "obligation_id": f"obl.{len(obligations)+2:02d}",
                "kind": "payoff-claim",
                "requirement": f"Prove that any admissible realization of `{label}` forces `{consequence}` once the route-specific lemma `{route_delta.get('missing_witness_or_transport', 'target payoff')}` is discharged.",
                "claim_template": f"If `{label}` is realized and the route-specific lemma is discharged, then `{consequence}` follows.",
                "why_it_matters": "This is the theorem-family payoff that justifies introducing the bridge concept.",
                "derived_from": f"{bridge.get('bridge_id', '')}:target-consequence",
            },
        ]
    )
    if barrier_scope and barrier_scope != "none":
        obligations.append(
            {
                "obligation_id": f"obl.{len(obligations)+1:02d}",
                "kind": "barrier-check",
                "requirement": f"Demonstrate that the realization of `{label}` avoids the `{barrier_scope}` barrier or explain precisely why the barrier does not apply in this encoding.",
                "claim_template": f"The bridge realization for `{label}` stays outside barrier scope `{barrier_scope}`.",
                "why_it_matters": "A bridge that triggers a known barrier without explanation is not a credible proof route.",
                "derived_from": f"{bridge.get('bridge_id', '')}:barrier-scope",
            }
        )
    if str(strategy.get("phase", "")).strip():
        obligations.append(
            {
                "obligation_id": f"obl.{len(obligations)+1:02d}",
                "kind": "regime-faithfulness",
                "requirement": f"Keep the argument faithful to the `{strategy.get('phase', '')}` regime while linking `{source_id}` to `{target_id}`.",
                "claim_template": f"The proof route remains inside the `{strategy.get('phase', '')}` regime while deriving `{consequence}`.",
                "why_it_matters": "Prevents the sketch from drifting into a different regime than the selected strategy anchor.",
                "derived_from": f"{strategy.get('strategy_id', '')}:phase",
            }
        )
    return obligations



def _candidate_lemmas(
    conjecture: dict[str, Any],
    bridge: dict[str, Any],
    family: str,
    kb_statements: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, str]]:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: Construction of candidate intermediate lemmas implied by the sketch architecture.
    Contribution: Gives the user and later agents explicit local proof targets instead of only a prose plan.
    """

    bridge_id = str(bridge.get("bridge_id", "bridge")).strip() or "bridge"
    label = str(conjecture.get("abstraction_label", "candidate bridge object")).strip() or "candidate bridge object"
    source_id = str(bridge.get("from_id", "")).strip() or "source statement"
    target_id = str(bridge.get("to_id", "")).strip() or "target statement"
    invariant = str(conjecture.get("preserved_invariant") or bridge.get("inferential_commitment", {}).get("preserved_invariant", "support-to-target interface")).strip()
    consequence = str(conjecture.get("target_consequence_schema") or bridge.get("inferential_commitment", {}).get("target_consequence_schema", "statement-conclusion")).strip()
    antecedent = str(conjecture.get("support_antecedent_schema") or bridge.get("inferential_commitment", {}).get("support_antecedent_schema", "source-side theorem schema")).strip()
    carrier_kind = str(conjecture.get("carrier_kind", "")).strip() or "bridge carrier"
    route_delta = _route_delta(conjecture, bridge, kb_statements=kb_statements)
    source_focus = str(route_delta.get("source_claim_focus", "")).strip() or antecedent
    target_focus = str(route_delta.get("target_claim_focus", "")).strip() or consequence
    model_shift = str(route_delta.get("model_shift", "")).strip() or f"`{source_id}` -> `{target_id}`"
    missing_lemma = str(route_delta.get("missing_witness_or_transport", "")).strip()
    definitional = conjecture.get("definitional_profile", {}) if isinstance(conjecture.get("definitional_profile"), dict) else {}
    sufficient_sets = definitional.get("sufficient_attribute_sets", []) if isinstance(definitional.get("sufficient_attribute_sets"), list) else []
    first_attrs: list[str] = []
    if sufficient_sets and isinstance(sufficient_sets[0], dict):
        first_attrs = [str(x).strip() for x in _as_list(sufficient_sets[0].get("attributes")) if str(x).strip()][:3]
    attr_clause = "; ".join(first_attrs) if first_attrs else f"the admissibility conditions of `{label}`"
    lemmas = [
        {
            "lemma_id": f"{bridge_id}.lemma.01",
            "statement": (
                f"Source-to-object lemma: the source-side content `{source_focus}` at `{source_id}` yields a realization of `{label}` "
                f"as a {carrier_kind}, satisfying {attr_clause}."
            ),
            "role": "Pins down the bridge concept before it is used in the proof.",
        },
        {
            "lemma_id": f"{bridge_id}.lemma.02",
            "statement": (
                f"Transport lemma: every admissible realization of `{label}` preserves `{invariant}` "
                f"while crossing {model_shift}."
            ),
            "role": "Transfers the source-side structure into the bridge object.",
        },
        {
            "lemma_id": f"{bridge_id}.lemma.03",
            "statement": (
                f"Payoff lemma: if `{label}` is realized, carries `{invariant}`, and discharges the route-specific step from `{source_focus}` to `{target_focus}`, then `{consequence}` holds at `{target_id}`."
            ),
            "role": "Converts the bridge object into the target theorem-family consequence.",
        },
    ]
    if family == "surrogate-reduction-transfer":
        lemmas.append(
            {
                "lemma_id": f"{bridge_id}.lemma.04",
                "statement": (
                    f"Reduction lemma: the source-side content `{source_focus}` reduces to the surrogate object encoded by `{label}` "
                    f"without weakening the path to `{consequence}`."
                ),
                "role": "Makes the transfer route explicit instead of only analogical.",
            }
        )
    if family == "spectral-calculus-realization":
        lemmas.append(
            {
                "lemma_id": f"{bridge_id}.lemma.04",
                "statement": f"Spectral lemma: the self-adjoint or spectral data attached to `{label}` yields a strongly continuous unitary representation.",
                "role": "Turns spectral information into the concrete dynamical object needed for the theorem.",
            }
        )
    if family == "generator-recovery-from-unitary-orbits":
        lemmas.append(
            {
                "lemma_id": f"{bridge_id}.lemma.04",
                "statement": f"Generator lemma: differentiable orbit data for `{label}` determines the hidden infinitesimal generator uniquely.",
                "role": "Makes the Stone-style recovery of the generator explicit.",
            }
        )
    if family == "domain-core-self-adjointness":
        lemmas.append(
            {
                "lemma_id": f"{bridge_id}.lemma.04",
                "statement": f"Core lemma: a dense core for `{label}` is sufficient to upgrade symmetry/closure into the self-adjointness needed for the bridge payoff.",
                "role": "Localizes the hard operator-theoretic step.",
            }
        )
    if family == "measure-construction-from-positive-functional":
        lemmas.append(
            {
                "lemma_id": f"{bridge_id}.lemma.04",
                "statement": f"Measure-construction lemma: positivity data for `{label}` determines a countably additive regular Borel measure.",
                "role": "Makes the hidden measure object explicit rather than inferred rhetorically.",
            }
        )
    if family == "regularity-via-compact-open-approximation":
        lemmas.append(
            {
                "lemma_id": f"{bridge_id}.lemma.04",
                "statement": f"Regularity lemma: compact-open approximation for `{label}` yields inner/outer regularity and uniqueness of the representing measure.",
                "role": "Localizes the topological regularity step behind the theorem.",
            }
        )
    if family == "integration-duality-decomposition":
        lemmas.append(
            {
                "lemma_id": f"{bridge_id}.lemma.04",
                "statement": f"Duality lemma: `{label}` admits an integration or signed-measure decomposition realizing the target dual functional statement.",
                "role": "Turns the bridge into an explicit duality mechanism instead of a generic representation claim.",
            }
        )
    if family == "affine-averaging-to-fixed-point":
        lemmas.append(
            {
                "lemma_id": f"{bridge_id}.lemma.04",
                "statement": f"Averaging lemma: the affine averaging kernel encoded by `{label}` produces a genuine fixed-point witness rather than only approximate orbit averages.",
                "role": "Localizes the single-map fixed-point extraction step.",
            }
        )
    if family == "invariant-fixed-point-subset-reduction":
        lemmas.append(
            {
                "lemma_id": f"{bridge_id}.lemma.04",
                "statement": f"Invariant-subset lemma: `{label}` yields a nonempty compact convex fixed-point subset preserved by the commuting family.",
                "role": "Makes the hidden bridge object explicit for the family-level reduction.",
            }
        )
    if family == "finite-intersection-compactness-lift":
        lemmas.append(
            {
                "lemma_id": f"{bridge_id}.lemma.04",
                "statement": f"Compactness lift lemma: finite common fixed-point data encoded by `{label}` extends to the whole family through finite intersection and compactness.",
                "role": "Turns finite-stage control into the full Markov-Kakutani payoff.",
            }
        )
    if family == "barrier-escape-reencoding":
        lemmas.append(
            {
                "lemma_id": f"{bridge_id}.lemma.04",
                "statement": f"Encoding lemma: `{label}` admits a representation that avoids the active barrier while preserving `{invariant}`.",
                "role": "Prevents the sketch from immediately collapsing under a known barrier.",
            }
        )
    elif missing_lemma:
        lemmas.append(
            {
                "lemma_id": f"{bridge_id}.lemma.04",
                "statement": f"Route lemma: {missing_lemma}",
                "role": "Names the theorem-pair-specific step that distinguishes this route from a generic bridge template.",
            }
        )
    if family == "contradiction-via-collapse-or-separation":
        lemmas.append(
            {
                "lemma_id": f"{bridge_id}.lemma.04",
                "statement": f"Contradiction lemma: negating the bridge payoff forces a forbidden collapse or contradicts an accepted separation profile.",
                "role": "Turns the sketch into a contradiction-based route rather than a direct transfer only.",
            }
        )
    return lemmas



def _outline_steps(
    conjecture: dict[str, Any],
    bridge: dict[str, Any],
    strategy: dict[str, Any],
    family: str,
    kb_statements: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: Construction of ordered proof programs.
    Contribution: Converts conjectural bridge concepts into a sequence of proof actions with explicit expected outputs.
    """

    conjecture_id = str(conjecture.get("conjecture_id", "")).strip()
    bridge_id = str(bridge.get("bridge_id", "")).strip()
    strategy_id = str(strategy.get("strategy_id", "")).strip()
    label = str(conjecture.get("abstraction_label", "candidate bridge object")).strip() or "candidate bridge object"
    carrier_kind = str(conjecture.get("carrier_kind", "")).strip() or "bridge carrier"
    consequence = str(conjecture.get("target_consequence_schema") or bridge.get("inferential_commitment", {}).get("target_consequence_schema", "statement-conclusion")).strip()
    invariant = str(conjecture.get("preserved_invariant") or bridge.get("inferential_commitment", {}).get("preserved_invariant", "support-to-target interface")).strip()
    route_delta = _route_delta(conjecture, bridge, kb_statements=kb_statements)
    source_focus = str(route_delta.get("source_claim_focus", "")).strip() or str(bridge.get("inferential_commitment", {}).get("support_antecedent_schema", "source theorem")).strip()
    target_focus = str(route_delta.get("target_claim_focus", "")).strip() or consequence
    model_shift = str(route_delta.get("model_shift", "")).strip() or f"`{bridge.get('from_id', '')}` -> `{bridge.get('to_id', '')}`"
    missing_lemma = str(route_delta.get("missing_witness_or_transport", "")).strip()
    steps: list[dict[str, Any]] = [
        {
            "step_id": "step.01",
            "objective": f"Define `{label}` as a {carrier_kind} with the necessary attributes extracted in `{conjecture_id}`.",
            "uses": [conjecture_id, bridge_id, strategy_id],
            "expected_output": "A typed bridge object with explicit carrier, admissibility conditions, and theorem-family commitments.",
        },
        {
            "step_id": "step.02",
            "objective": f"Show that the source-side content `{source_focus}` induces `{invariant}` inside `{label}`.",
            "uses": [bridge_id, strategy_id],
            "expected_output": "An invariant-preservation lemma for the conjectured object.",
        },
    ]
    if family == "surrogate-reduction-transfer":
        steps.append(
            {
                "step_id": "step.03",
                "objective": f"Construct the surrogate reduction into `{label}` and verify that it preserves the needed route from `{source_focus}` to `{target_focus}`.",
                "uses": [bridge_id, strategy_id],
                "expected_output": "A reduction lemma exposing the transfer mechanism.",
            }
        )
    elif family == "spectral-calculus-realization":
        steps.append(
            {
                "step_id": "step.03",
                "objective": "Assemble the spectral theorem or functional-calculus representation needed to exponentiate the hidden operator.",
                "uses": [conjecture_id, bridge_id, strategy_id],
                "expected_output": "A spectral representation lemma yielding a strongly continuous unitary family.",
            }
        )
    elif family == "generator-recovery-from-unitary-orbits":
        steps.append(
            {
                "step_id": "step.03",
                "objective": "Recover the infinitesimal generator from unitary-orbit data and verify uniqueness at the operator level.",
                "uses": [conjecture_id, bridge_id, strategy_id],
                "expected_output": "A generator-recovery lemma with explicit domain and closure commitments.",
            }
        )
    elif family == "domain-core-self-adjointness":
        steps.append(
            {
                "step_id": "step.03",
                "objective": "Construct a dense core and upgrade local symmetry or closure information into self-adjointness.",
                "uses": [conjecture_id, bridge_id, strategy_id],
                "expected_output": "A core argument that turns the hidden operator into a self-adjoint bridge object.",
            }
        )
    elif family == "measure-construction-from-positive-functional":
        steps.append(
            {
                "step_id": "step.03",
                "objective": "Construct the representing measure from positivity on the function space and prove countable additivity.",
                "uses": [conjecture_id, bridge_id, strategy_id],
                "expected_output": "A measure-construction lemma producing the hidden regular Borel measure.",
            }
        )
    elif family == "regularity-via-compact-open-approximation":
        steps.append(
            {
                "step_id": "step.03",
                "objective": "Use compact-open approximation and topological separation to prove regularity and uniqueness of the representing measure.",
                "uses": [conjecture_id, bridge_id, strategy_id],
                "expected_output": "A regularity/uniqueness lemma making the representation theorem fully typed.",
            }
        )
    elif family == "integration-duality-decomposition":
        steps.append(
            {
                "step_id": "step.03",
                "objective": "Express the bridge object through integration and extend it to the signed or dual setting via decomposition.",
                "uses": [conjecture_id, bridge_id, strategy_id],
                "expected_output": "An integration-duality lemma or signed-measure normal form.",
            }
        )
    elif family == "affine-averaging-to-fixed-point":
        steps.append(
            {
                "step_id": "step.03",
                "objective": "Construct the affine averaging sequence or kernel and prove that compactness upgrades it to a genuine fixed-point witness for one map.",
                "uses": [conjecture_id, bridge_id, strategy_id],
                "expected_output": "A single-map fixed-point lemma derived from affine averaging.",
            }
        )
    elif family == "invariant-fixed-point-subset-reduction":
        steps.append(
            {
                "step_id": "step.03",
                "objective": "Show that the fixed-point subset is nonempty compact convex and preserved by the rest of the commuting family.",
                "uses": [conjecture_id, bridge_id, strategy_id],
                "expected_output": "An invariant fixed-point subset reduction lemma.",
            }
        )
    elif family == "finite-intersection-compactness-lift":
        steps.append(
            {
                "step_id": "step.03",
                "objective": "Lift finite commuting-subfamily fixed-point data through the finite intersection property and compactness.",
                "uses": [conjecture_id, bridge_id, strategy_id],
                "expected_output": "A compactness lift from finite common fixed points to the whole family.",
            }
        )
    elif family == "barrier-escape-reencoding":
        steps.append(
            {
                "step_id": "step.03",
                "objective": "Re-express the bridge concept in a representation that blocks the dominant barrier from firing.",
                "uses": [conjecture_id, bridge_id],
                "expected_output": "A barrier-aware encoding lemma or a clear failure diagnosis.",
            }
        )
    elif family == "contradiction-via-collapse-or-separation":
        steps.append(
            {
                "step_id": "step.03",
                "objective": f"Assume `{consequence}` fails and derive a forbidden collapse or contradiction with the selected strategy regime.",
                "uses": [bridge_id, strategy_id],
                "expected_output": "A contradiction branch that justifies the bridge payoff.",
            }
        )
    elif family == "bootstrapped-derandomization-transfer":
        steps.append(
            {
                "step_id": "step.03",
                "objective": "Bootstrap the derandomization-style object into a hardness or lower-bound signal.",
                "uses": [bridge_id, strategy_id],
                "expected_output": "A transfer lemma from the randomized object to the target lower-bound regime.",
            }
        )
    elif family == "case-split-regime-transfer":
        steps.append(
            {
                "step_id": "step.03",
                "objective": "Split the argument by model/regime and prove that each branch still realizes the same bridge concept.",
                "uses": [bridge_id, strategy_id],
                "expected_output": "A case partition that prevents regime mismatch from invalidating the sketch.",
            }
        )
    else:
        steps.append(
            {
                "step_id": "step.03",
                "objective": missing_lemma or f"Introduce the intermediate object `{label}` as the minimal structure needed to carry `{invariant}` to `{consequence}` across {model_shift}.",
                "uses": [conjecture_id, bridge_id],
                "expected_output": "A bridge lemma linking the intermediate object to the target payoff.",
            }
        )
    steps.append(
        {
            "step_id": f"step.{len(steps)+1:02d}",
            "objective": f"Use the realized bridge object to force `{consequence}`.",
            "uses": [conjecture_id, bridge_id, strategy_id],
            "expected_output": "A payoff theorem candidate or a sharply localized remaining obstruction.",
        }
    )
    return steps



def _barrier_checkpoints(conjecture: dict[str, Any], bridge: dict[str, Any], hardness: dict[str, Any]) -> list[dict[str, str]]:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: Construction of barrier-aware checkpoints inside the proof plan.
    Contribution: Makes barrier reasoning operational rather than leaving it as ambient commentary.
    """

    barrier_scope = str(conjecture.get("barrier_scope") or bridge.get("inferential_commitment", {}).get("barrier_scope", "none")).strip() or "none"
    if barrier_scope == "none":
        return [
            {
                "checkpoint": "barrier.01",
                "condition": "Verify that no named barrier is already attached to the bridge commitment.",
                "response": "If a hidden barrier appears, reclassify the sketch family before continuing.",
            }
        ]
    anti = hardness.get("anti_barrier_programs", []) if isinstance(hardness.get("anti_barrier_programs"), list) else []
    anti_text = "; ".join(
        ", ".join(str(x) for x in _as_list(row.get("minimal_conceptual_changes"))[:2])
        for row in anti
        if isinstance(row, dict) and str(row.get("barrier_family", "")).strip() == barrier_scope
    )
    response = f"Use anti-barrier change set: {anti_text}" if anti_text else "Re-encode the bridge object or abort the route if the barrier remains active."
    return [
        {
            "checkpoint": "barrier.01",
            "condition": f"Check whether `{barrier_scope}` blocks the proposed bridge object or proof tactic.",
            "response": response,
        }
    ]



def _abort_conditions(
    conjecture: dict[str, Any],
    bridge: dict[str, Any],
    kb_statements: dict[str, dict[str, Any]] | None = None,
) -> list[str]:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: Construction of explicit negative stopping conditions.
    Contribution: Keeps proof sketches falsifiable and prevents indefinite escalation of weak routes.
    """

    conditions: list[str] = []
    route_delta = _route_delta(conjecture, bridge, kb_statements=kb_statements)
    label = str(conjecture.get("abstraction_label", "bridge object")).strip() or "bridge object"
    carrier_kind = str(conjecture.get("carrier_kind", "")).strip() or "bridge carrier"
    counterfactuals = conjecture.get("counterfactual_probes", []) if isinstance(conjecture.get("counterfactual_probes"), list) else []
    if counterfactuals:
        probe = counterfactuals[0] if isinstance(counterfactuals[0], dict) else {}
        conditions.append(
            f"Abort if the negative-route intervention does not expose the expected failure: {probe.get('intervention', '')} => {probe.get('expected_bridge_effect', '')}."
        )
    barrier_scope = str(conjecture.get("barrier_scope") or bridge.get("inferential_commitment", {}).get("barrier_scope", "none")).strip()
    if barrier_scope and barrier_scope != "none":
        conditions.append(f"Abort if the sketch still falls inside the `{barrier_scope}` barrier after re-encoding attempts.")
    conditions.append(f"Abort if `{label}` cannot be defined as a {carrier_kind} on the current theorem pair.")
    if str(route_delta.get("missing_witness_or_transport", "")).strip():
        conditions.append(f"Abort if the route-specific lemma fails: {route_delta.get('missing_witness_or_transport', '')}")
    conditions.append("Abort if the payoff lemma does not improve over the existing bridge consequence or only restates known dependencies.")
    return conditions


def _negative_reasoning_program(
    conjecture: dict[str, Any],
    bridge: dict[str, Any],
    strategy: dict[str, Any],
    family: str,
    counterfactual: dict[str, Any],
    kb_statements: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: Structured negative and impossibility-side proof program attached to a sketch.
    Contribution: Turns contradiction, barrier, and non-realization reasoning into inspectable proof objects rather than loose commentary.
    """

    label = str(conjecture.get("abstraction_label", "bridge object")).strip() or "bridge object"
    barrier_scope = str(conjecture.get("barrier_scope") or bridge.get("inferential_commitment", {}).get("barrier_scope", "none")).strip() or "none"
    route_delta = _route_delta(conjecture, bridge, kb_statements=kb_statements)
    source_focus = str(route_delta.get("source_claim_focus", "")).strip() or str(
        bridge.get("inferential_commitment", {}).get("support_antecedent_schema", "source theorem")
    ).strip()
    target_focus = str(route_delta.get("target_claim_focus", "")).strip() or str(
        conjecture.get("target_consequence_schema") or bridge.get("inferential_commitment", {}).get("target_consequence_schema", "target consequence")
    ).strip()
    invariant = str(conjecture.get("preserved_invariant") or bridge.get("inferential_commitment", {}).get("preserved_invariant", "route invariant")).strip()
    missing_lemma = str(route_delta.get("missing_witness_or_transport", "")).strip()
    intervention = str(counterfactual.get("intervention", "")).strip()
    expected_effect = str(counterfactual.get("expected_bridge_effect", "")).strip()
    diagnostic_value = str(counterfactual.get("diagnostic_value", "")).strip()

    mode = "obstruction"
    negated_claim = f"Assume the route from `{source_focus}` to `{target_focus}` does not go through `{label}`."
    contradiction_target = f"Show that no admissible realization of `{label}` can preserve `{invariant}` strongly enough to force `{target_focus}`."
    forbidden_outcome = f"`{label}` becomes only topical overlap rather than a theorem-level bridge."
    impossibility_claim = (
        f"No admissible realization of `{label}` can simultaneously absorb `{source_focus}`, preserve `{invariant}`, "
        f"and force `{target_focus}` on the current theorem pair."
    )

    if family == "contradiction-via-collapse-or-separation":
        mode = "contradiction"
        negated_claim = f"Assume `{target_focus}` fails even if `{label}` is admissible."
        contradiction_target = "Derive a forbidden collapse or a contradiction with the accepted separation profile."
        forbidden_outcome = "A collapse or contradiction appears in the ambient complexity landscape."
        impossibility_claim = (
            f"If negating `{target_focus}` forces a forbidden collapse, then any admissible route through `{label}` yields `{target_focus}`."
        )
    elif barrier_scope != "none":
        mode = "barrier-impossibility"
        negated_claim = f"Assume every realization of `{label}` remains trapped inside the barrier `{barrier_scope}`."
        contradiction_target = f"Show that the route cannot escape the barrier family `{barrier_scope}` while preserving `{invariant}`."
        forbidden_outcome = f"Any realization of `{label}` collapses back into the known barrier `{barrier_scope}`."
        impossibility_claim = (
            f"Every admissible realization of `{label}` inside the current encoding remains blocked by barrier `{barrier_scope}` and therefore cannot force `{target_focus}`."
        )
    elif any(token in label.lower() for token in ("obstruction", "witness", "certificate")):
        mode = "non-realization"
        negated_claim = f"Assume `{label}` cannot be realized as a mathematically usable carrier for `{source_focus}`."
        contradiction_target = f"Localize the failure to carrier realization, witness preservation, or payoff forcing for `{target_focus}`."
        forbidden_outcome = f"`{label}` exists only as a role-description and never becomes a usable mathematical object."
        impossibility_claim = (
            f"No admissible carrier realizing `{label}` currently supports the full bundle source `{source_focus}` + invariant `{invariant}` + payoff `{target_focus}`."
        )
    elif "transport" in missing_lemma.lower() or "transfer" in missing_lemma.lower():
        mode = "transport-obstruction"
        negated_claim = f"Assume the transport from `{source_focus}` to `{target_focus}` loses `{invariant}`."
        contradiction_target = "Expose the first transport law whose failure makes the route impossible in the current regime."
        forbidden_outcome = f"The invariant `{invariant}` cannot survive the required model or representation shift."
        impossibility_claim = (
            f"No transport map currently known can carry `{source_focus}` to `{target_focus}` while preserving `{invariant}`."
        )

    heuristic = build_negative_route_heuristic(
        candidate_object=label,
        source_focus=source_focus,
        target_focus=target_focus,
        invariant=invariant,
        negative_route=intervention or contradiction_target,
        failure_diagnosis=forbidden_outcome,
        barrier_scope=barrier_scope,
        missing_route_lemma=missing_lemma,
        carrier_kind=str(conjecture.get("carrier_kind", "")).strip(),
    )

    return {
        "negative_mode": mode,
        "negated_claim": negated_claim,
        "contradiction_target": contradiction_target,
        "forbidden_outcome": forbidden_outcome,
        "impossibility_claim_template": impossibility_claim,
        "barrier_scope": barrier_scope,
        "designated_negative_route": intervention or contradiction_target,
        "expected_effect": expected_effect,
        "diagnostic_value": diagnostic_value or "Negative reasoning should either sharpen the bridge object or produce a usable impossibility theorem.",
        "preferred_when": (
            "Prefer the negative route when the carrier remains schematic, the transport law is missing, or a barrier theorem would compress the search space more than another constructive variant."
        ),
        "missing_negative_lemma": missing_lemma or contradiction_target,
        "heuristic": heuristic,
    }


def _mathematical_argument(
    conjecture: dict[str, Any],
    bridge: dict[str, Any],
    strategy: dict[str, Any],
    obligations: list[dict[str, Any]],
    lemmas: list[dict[str, Any]],
    counterfactual: dict[str, Any],
    kb_statements: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: Condensed mathematical interface for expert inspection of a proof sketch.
    Contribution: Packages the bridge definition, assumptions, proposition, and failure mode into a theorem-shaped record.
    """

    label = str(conjecture.get("abstraction_label", "candidate bridge object")).strip() or "candidate bridge object"
    abstraction_type = str(conjecture.get("abstraction_type", "bridge object")).strip() or "bridge object"
    carrier_kind = str(conjecture.get("carrier_kind", "")).strip() or "bridge carrier"
    typing_status = str(conjecture.get("typing_status", "")).strip() or "typed"
    role = str(conjecture.get("mathematical_object_role", "")).strip()
    source_id = str(bridge.get("from_id", "")).strip() or "source statement"
    target_id = str(bridge.get("to_id", "")).strip() or "target statement"
    antecedent = str(conjecture.get("support_antecedent_schema") or bridge.get("inferential_commitment", {}).get("support_antecedent_schema", "source-side theorem schema")).strip()
    consequence = str(conjecture.get("target_consequence_schema") or bridge.get("inferential_commitment", {}).get("target_consequence_schema", "statement-conclusion")).strip()
    invariant = str(conjecture.get("preserved_invariant") or bridge.get("inferential_commitment", {}).get("preserved_invariant", "support-to-target interface")).strip()
    barrier_scope = str(conjecture.get("barrier_scope") or bridge.get("inferential_commitment", {}).get("barrier_scope", "none")).strip() or "none"
    route_delta = _route_delta(conjecture, bridge, kb_statements=kb_statements)
    source_focus = str(route_delta.get("source_claim_focus", "")).strip() or antecedent
    target_focus = str(route_delta.get("target_claim_focus", "")).strip() or consequence
    model_shift = str(route_delta.get("model_shift", "")).strip() or f"`{source_id}` -> `{target_id}`"
    threshold_shift = str(route_delta.get("threshold_shift", "")).strip() or "threshold shift not yet typed"
    missing_lemma = str(route_delta.get("missing_witness_or_transport", "")).strip()
    definitional = conjecture.get("definitional_profile", {}) if isinstance(conjecture.get("definitional_profile"), dict) else {}
    sufficient_sets = definitional.get("sufficient_attribute_sets", []) if isinstance(definitional.get("sufficient_attribute_sets"), list) else []
    bridge_definition = (
        f"Treat `{label}` as a `{abstraction_type}` attached to the route `{source_id}` -> `{target_id}` and typed as a {carrier_kind}"
        + (f", playing the role of `{role}`" if role else "")
        + f", carrying the source-side content `{source_focus}` across {model_shift} toward `{target_focus}` while preserving `{invariant}`."
    )
    if sufficient_sets and isinstance(sufficient_sets[0], dict):
        attrs = [str(x).strip() for x in _as_list(sufficient_sets[0].get("attributes")) if str(x).strip()]
        if attrs:
            bridge_definition += " Minimal admissibility conditions: " + "; ".join(attrs[:4]) + "."
    assumptions = [
        f"The source-side content `{source_focus}` is available at `{source_id}`.",
        f"There exists an admissible realization of `{label}` as a {carrier_kind}.",
        f"The realization preserves `{invariant}` across {model_shift}.",
    ]
    if barrier_scope != "none":
        assumptions.append(f"The construction avoids barrier scope `{barrier_scope}`.")
    proposition = (
        f"If these assumptions hold and the route-specific lemma `{missing_lemma or 'bridge payoff lemma'}` is discharged, "
        f"then `{consequence}` follows at `{target_id}`."
    )
    failure_mode = " ".join(
        part
        for part in (
            str(counterfactual.get("intervention", "")).strip(),
            str(counterfactual.get("expected_bridge_effect", "")).strip(),
            str(counterfactual.get("diagnostic_value", "")).strip(),
        )
        if part
    ) or (
        f"Failure occurs if `{label}` never becomes a typed {carrier_kind} or if the route from `{source_focus}` to `{target_focus}` remains unproved."
    )
    inspection_points = [
        f"Where is the carrier of `{label}` defined, and how does it realize the {carrier_kind}?",
        f"Which lemma first proves preservation of `{invariant}` across {model_shift}?",
        f"Which lemma first converts the route shift {threshold_shift} into `{consequence}`?",
    ]
    return {
        "bridge_definition": bridge_definition,
        "assumptions": assumptions,
        "proposition": proposition,
        "conclusion": consequence,
        "carrier_kind": carrier_kind,
        "typing_status": typing_status,
        "statement_delta": route_delta,
        "source_theorem_excerpt": str(route_delta.get("source_theorem_excerpt", "")).strip(),
        "target_theorem_excerpt": str(route_delta.get("target_theorem_excerpt", "")).strip(),
        "lemma_chain": [str(item.get("statement", "")).strip() for item in lemmas[:4] if isinstance(item, dict) and str(item.get("statement", "")).strip()],
        "obligation_claims": [str(item.get("claim_template", item.get("requirement", ""))).strip() for item in obligations[:6] if isinstance(item, dict)],
        "failure_mode": failure_mode,
        "inspection_points": inspection_points,
        "strategy_regime": str(strategy.get("phase", "")).strip(),
    }


def _reason_for_family(family: str) -> str:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: Rendering internal classifications into concise analyst-facing rationale.
    Contribution: Makes the chosen proof regime interpretable and auditable.
    """

    return STRATEGY_FAMILY_CATALOG.get(family, "Selected because it best matches the conjecture's current inferential profile.")



def _build(
    conjectures: dict[str, Any],
    strategies: dict[str, Any],
    bridges: dict[str, Any],
    phyp: dict[str, Any],
    analysis: dict[str, Any],
    coherence: dict[str, Any],
    hardness: dict[str, Any],
    top_k: int,
    kb_statements: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: Construction of the stage-level proof-sketch artifact.
    Contribution: Aligns conjectures, strategies, bridges, and hypotheses into explicit proof-outline programs.
    """

    bridge_by_id = _bridge_lookup(bridges)
    strategy_rows = [row for row in _as_list(strategies.get("strategies")) if isinstance(row, dict)]
    hypothesis_by_id = _hypothesis_lookup(phyp)
    coherence_by_hyp = _coherence_index(coherence)

    candidates: list[dict[str, Any]] = []
    for conj in _as_list(conjectures.get("abstraction_conjectures")):
        if not isinstance(conj, dict):
            continue
        bridge_id = str(conj.get("bridge_id", "")).strip()
        bridge = bridge_by_id.get(bridge_id, {})
        if strategy_rows:
            relevant = [
                row for row in strategy_rows
                if bridge_id and bridge_id in {str(x).strip() for x in _as_list(row.get("bridge_ids"))}
            ]
            relevant = relevant or strategy_rows[: min(4, len(strategy_rows))]
        else:
            relevant = []
        for strat in relevant:
            score = _match_score(conj, strat, bridge, coherence_by_hyp)
            candidates.append(
                {
                    "conjecture": conj,
                    "strategy": strat,
                    "bridge": bridge,
                    "score": score,
                }
            )

    candidates.sort(key=lambda row: row["score"], reverse=True)
    selected = candidates[: max(1, top_k)]

    proof_sketches: list[dict[str, Any]] = []
    family_counter: Counter[str] = Counter()
    for idx, item in enumerate(selected, start=1):
        conjecture = item["conjecture"]
        strategy = item["strategy"]
        bridge = item["bridge"]
        family = _strategy_family(conjecture, strategy, bridge)
        family_counter[family] += 1
        definitional = conjecture.get("definitional_profile", {}) if isinstance(conjecture.get("definitional_profile"), dict) else {}
        necessary = [
            str(attr.get("attribute", "")).strip()
            for attr in _as_list(definitional.get("necessary_attributes"))
            if isinstance(attr, dict) and str(attr.get("attribute", "")).strip()
        ]
        sufficient_sets = []
        for row in _as_list(definitional.get("sufficient_attribute_sets"))[:3]:
            if not isinstance(row, dict):
                continue
            sufficient_sets.append(
                {
                    "label": str(row.get("label", "")).strip() or "unnamed set",
                    "attributes": [str(x).strip() for x in _as_list(row.get("attributes")) if str(x).strip()],
                }
            )
        hypothesis_ids = [
            str(hid).strip()
            for hid in _as_list(strategy.get("hypothesis_ids"))
            if str(hid).strip() in hypothesis_by_id
        ][:6]
        counterfactuals = [row for row in _as_list(conjecture.get("counterfactual_probes")) if isinstance(row, dict)]
        counterfactual = counterfactuals[0] if counterfactuals else {}
        obligations = _proof_obligations(conjecture, bridge, strategy, kb_statements=kb_statements)
        lemmas = _candidate_lemmas(conjecture, bridge, family, kb_statements=kb_statements)
        outline_steps = _outline_steps(conjecture, bridge, strategy, family, kb_statements=kb_statements)
        route_delta = _route_delta(conjecture, bridge, kb_statements=kb_statements)
        negative_program = _negative_reasoning_program(
            conjecture,
            bridge,
            strategy,
            family,
            counterfactual,
            kb_statements=kb_statements,
        )
        sketch = {
            "sketch_id": f"psk.{idx:03d}",
            "title": f"{str(conjecture.get('abstraction_label', 'Bridge concept')).strip() or 'Bridge concept'} via {str(strategy.get('strategy_id', '')).strip()}",
            "conjecture_id": str(conjecture.get("conjecture_id", "")).strip(),
            "strategy_id": str(strategy.get("strategy_id", "")).strip(),
            "strategy_name": str(strategy.get("name", "")).strip(),
            "bridge_id": str(bridge.get("bridge_id", conjecture.get("bridge_id", ""))).strip(),
            "source_statement_id": str(bridge.get("from_id", "")).strip(),
            "target_statement_id": str(bridge.get("to_id", "")).strip(),
            "anchor_statement_id": str(strategy.get("anchor_statement_id", "")).strip(),
            "anchor_phase": str(strategy.get("phase", "")).strip(),
            "proof_strategy_family": family,
            "family_rationale": _reason_for_family(family),
            "sketch_score": round(item["score"], 4),
            "abstraction_type": str(conjecture.get("abstraction_type", "")).strip(),
            "conjectured_object": str(conjecture.get("abstraction_label", "")).strip(),
            "carrier_kind": str(conjecture.get("carrier_kind", "")).strip(),
            "typing_status": str(conjecture.get("typing_status", "")).strip(),
            "target_consequence_schema": str(conjecture.get("target_consequence_schema") or bridge.get("inferential_commitment", {}).get("target_consequence_schema", "")).strip(),
            "support_antecedent_schema": str(bridge.get("inferential_commitment", {}).get("support_antecedent_schema", "")).strip(),
            "preserved_invariant": str(conjecture.get("preserved_invariant") or bridge.get("inferential_commitment", {}).get("preserved_invariant", "")).strip(),
            "barrier_scope": str(conjecture.get("barrier_scope") or bridge.get("inferential_commitment", {}).get("barrier_scope", "none")).strip() or "none",
            "statement_delta": route_delta,
            "definitional_commitments": necessary,
            "sufficient_attribute_sets": sufficient_sets,
            "counterfactual_test": {
                "intervention": str(counterfactual.get("intervention", "")).strip(),
                "expected_bridge_effect": str(counterfactual.get("expected_bridge_effect", "")).strip(),
                "diagnostic_value": str(counterfactual.get("diagnostic_value", "")).strip(),
            },
            "negative_reasoning_program": negative_program,
            "hypothesis_ids": hypothesis_ids,
            "proof_obligations": obligations,
            "candidate_lemmas": lemmas,
            "proof_outline_steps": outline_steps,
            "mathematical_argument": _mathematical_argument(
                conjecture,
                bridge,
                strategy,
                obligations,
                lemmas,
                counterfactual,
                kb_statements=kb_statements,
            ),
            "barrier_checkpoints": _barrier_checkpoints(conjecture, bridge, hardness),
            "abort_conditions": _abort_conditions(conjecture, bridge, kb_statements=kb_statements),
            "success_signal": (
                "A theorem-family-specific payoff lemma is isolated and survives the designated counterfactual probe."
            ),
        }
        proof_sketches.append(sketch)

    report = {
        "metadata": {
            "input_conjectures": len(_as_list(conjectures.get("abstraction_conjectures"))),
            "input_strategies": len(strategy_rows),
            "input_bridges": len(_as_list(bridges.get("bridge_programs"))),
            "input_hypotheses": len(_as_list(phyp.get("hypotheses"))),
            "input_analysis_rows": len(_as_list(analysis.get("connection_candidates"))),
            "input_coherence_signals": len(coherence_by_hyp),
            "sketch_count": len(proof_sketches),
            "selection_policy": "top conjecture-strategy alignment with coherence-aware bridge matching",
            "strategy_family_catalog": STRATEGY_FAMILY_CATALOG,
            "family_distribution": dict(sorted(family_counter.items())),
        },
        "proof_sketches": proof_sketches,
        "recommended_execution_order": [row["sketch_id"] for row in proof_sketches],
    }
    return validate_proof_sketch_report(report, name="proof_sketches")



def _to_markdown(report: dict[str, Any]) -> str:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: Rendering internal outputs into human-readable artifacts.
    Contribution: Makes proof-sketch programs inspectable without reading raw JSON.
    """

    lines: list[str] = []
    meta = report.get("metadata", {}) if isinstance(report.get("metadata"), dict) else {}
    lines.append("# Proof Sketches")
    lines.append("")
    lines.append("## Stats")
    lines.append("")
    lines.append(f"- Proof sketches: {meta.get('sketch_count', 0)}")
    lines.append(f"- Conjectures used: {meta.get('input_conjectures', 0)}")
    lines.append(f"- Strategies used: {meta.get('input_strategies', 0)}")
    lines.append(f"- Bridges used: {meta.get('input_bridges', 0)}")
    lines.append(f"- Hypotheses used: {meta.get('input_hypotheses', 0)}")
    if isinstance(meta.get("family_distribution"), dict) and meta.get("family_distribution"):
        lines.append(
            "- Strategy families: "
            + ", ".join(f"{k}={v}" for k, v in meta.get("family_distribution", {}).items())
        )
    lines.append("")

    lines.append("## Strategy Families")
    lines.append("")
    for name, desc in STRATEGY_FAMILY_CATALOG.items():
        lines.append(f"- `{name}`: {desc}")
    lines.append("")

    lines.append("## Sketches")
    lines.append("")
    lines.append("| sketch_id | conjecture_id | strategy_id | family | score | target |")
    lines.append("|---|---|---|---|---|---|")
    for row in _as_list(report.get("proof_sketches")):
        if not isinstance(row, dict):
            continue
        lines.append(
            f"| {row.get('sketch_id', '')} | {row.get('conjecture_id', '')} | {row.get('strategy_id', '')} | {row.get('proof_strategy_family', '')} | {row.get('sketch_score', 0.0)} | {row.get('target_consequence_schema', '')} |"
        )
    lines.append("")

    for row in _as_list(report.get("proof_sketches")):
        if not isinstance(row, dict):
            continue
        lines.append(f"### {row.get('sketch_id', '')} - {row.get('title', '')}")
        lines.append(f"- Conjecture: {row.get('conjecture_id', '')}")
        lines.append(f"- Strategy: {row.get('strategy_id', '')} ({row.get('strategy_name', '')})")
        lines.append(f"- Bridge: {row.get('bridge_id', '')}")
        lines.append(f"- Family: {row.get('proof_strategy_family', '')}")
        lines.append(f"- Score: {row.get('sketch_score', 0.0)}")
        lines.append(f"- Target consequence: {row.get('target_consequence_schema', '')}")
        lines.append(f"- Antecedent: {row.get('support_antecedent_schema', '') or 'unconditional'}")
        lines.append(f"- Invariant: {row.get('preserved_invariant', '')}")
        lines.append(f"- Carrier kind: {row.get('carrier_kind', '') or 'bridge carrier'}")
        lines.append(f"- Typing status: {row.get('typing_status', '') or 'typed'}")
        lines.append(f"- Barrier scope: {row.get('barrier_scope', '')}")
        lines.append(f"- Family rationale: {row.get('family_rationale', '')}")
        mathematical_argument = row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}
        if mathematical_argument:
            lines.append(f"- Bridge definition: {mathematical_argument.get('bridge_definition', '')}")
            lines.append(f"- Conditional proposition: {mathematical_argument.get('proposition', '')}")
            delta = mathematical_argument.get("statement_delta", {}) if isinstance(mathematical_argument.get("statement_delta"), dict) else {}
            if delta:
                lines.append(f"- Route synopsis: {delta.get('route_synopsis', '')}")
                lines.append(f"- Model shift: {delta.get('model_shift', '')}")
                lines.append(f"- Threshold shift: {delta.get('threshold_shift', '')}")
                lines.append(f"- Consequence shift: {delta.get('consequence_shift', '')}")
                lines.append(f"- Missing route lemma: {delta.get('missing_witness_or_transport', '')}")
            assumptions = mathematical_argument.get("assumptions", []) if isinstance(mathematical_argument.get("assumptions"), list) else []
            if assumptions:
                lines.append("- Mathematical assumptions:")
                for item in assumptions[:4]:
                    lines.append(f"  - {item}")
        if _as_list(row.get("definitional_commitments")):
            lines.append("- Definitional commitments: " + ", ".join(str(x) for x in _as_list(row.get("definitional_commitments"))[:4]))
        counterfactual = row.get("counterfactual_test", {}) if isinstance(row.get("counterfactual_test"), dict) else {}
        if counterfactual:
            lines.append(
                f"- Counterfactual test: {counterfactual.get('intervention', '')} => {counterfactual.get('expected_bridge_effect', '')}"
            )
        negative_program = row.get("negative_reasoning_program", {}) if isinstance(row.get("negative_reasoning_program"), dict) else {}
        if negative_program:
            lines.append(f"- Negative mode: {negative_program.get('negative_mode', '')}")
            lines.append(f"- Negated claim: {negative_program.get('negated_claim', '')}")
            lines.append(f"- Contradiction target: {negative_program.get('contradiction_target', '')}")
            lines.append(f"- Impossibility claim template: {negative_program.get('impossibility_claim_template', '')}")
            heuristic = negative_program.get("heuristic", {}) if isinstance(negative_program.get("heuristic"), dict) else {}
            if heuristic:
                lines.append(f"- Negative-route heuristic: {heuristic.get('decision', '')} | principle={heuristic.get('epistemic_principle', '')}")
        lines.append("- Proof obligations:")
        for obligation in _as_list(row.get("proof_obligations")):
            if not isinstance(obligation, dict):
                continue
            lines.append(
                f"  - {obligation.get('obligation_id', '')}: {obligation.get('requirement', '')}"
            )
        lines.append("- Candidate lemmas:")
        for lemma in _as_list(row.get("candidate_lemmas")):
            if not isinstance(lemma, dict):
                continue
            lines.append(
                f"  - {lemma.get('lemma_id', '')}: {lemma.get('statement', '')}"
            )
        if mathematical_argument:
            lemma_chain = mathematical_argument.get("lemma_chain", []) if isinstance(mathematical_argument.get("lemma_chain"), list) else []
            if lemma_chain:
                lines.append("- Lemma chain summary:")
                for item in lemma_chain[:4]:
                    lines.append(f"  - {item}")
        lines.append("- Proof outline:")
        for step in _as_list(row.get("proof_outline_steps")):
            if not isinstance(step, dict):
                continue
            lines.append(
                f"  - {step.get('step_id', '')}: {step.get('objective', '')} -> {step.get('expected_output', '')}"
            )
        lines.append("- Barrier checkpoints:")
        for checkpoint in _as_list(row.get("barrier_checkpoints")):
            if not isinstance(checkpoint, dict):
                continue
            lines.append(
                f"  - {checkpoint.get('checkpoint', '')}: {checkpoint.get('condition', '')} / {checkpoint.get('response', '')}"
            )
        lines.append("- Abort conditions:")
        for condition in _as_list(row.get("abort_conditions")):
            lines.append(f"  - {condition}")
        if mathematical_argument and mathematical_argument.get("failure_mode"):
            lines.append(f"- Failure mode: {mathematical_argument.get('failure_mode', '')}")
        lines.append(f"- Success signal: {row.get('success_signal', '')}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _theorem_heading(sketch: dict[str, Any]) -> str:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: Translation of sketch metadata into a paper-like theorem heading.
    Contribution: Gives the rendered argument a mathematically meaningful entry point tied to the selected pathway.
    """

    consequence = str(sketch.get("target_consequence_schema", "")).strip() or "target consequence"
    family = str(sketch.get("proof_strategy_family", "")).strip() or "proof route"
    return f"Conditional {consequence} via {family}"


def _paper_style_argument(report: dict[str, Any], kb_statements: dict[str, dict[str, Any]] | None = None) -> str:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: Translation of the strongest final pathway into a paper-style mathematical argument.
    Contribution: Produces a readable conditional argument with proposition, lemmas, and proof so the final route can be inspected like a research note.
    """

    kb_statements = kb_statements or {}
    sketches = [row for row in _as_list(report.get("proof_sketches")) if isinstance(row, dict)]
    if not sketches:
        return "# Paper-Style Argument\n\nNo proof sketch is available.\n"

    sketch = sketches[0]
    source_id = str(sketch.get("source_statement_id", "")).strip() or str(sketch.get("anchor_statement_id", "")).strip()
    target_id = str(sketch.get("target_statement_id", "")).strip()
    source_statement = kb_statements.get(source_id, {})
    target_statement = kb_statements.get(target_id, {})
    source_text = _statement_body(source_statement)
    target_text = _statement_body(target_statement)

    theorem_title = _theorem_heading(sketch)
    obj = str(sketch.get("conjectured_object", "")).strip() or "bridge object"
    carrier_kind = str(sketch.get("carrier_kind", "")).strip() or "bridge carrier"
    typing_status = str(sketch.get("typing_status", "")).strip() or "typed"
    antecedent = str(sketch.get("support_antecedent_schema", "")).strip() or "unconditional source theorem"
    consequence = str(sketch.get("target_consequence_schema", "")).strip() or "target consequence"
    invariant = str(sketch.get("preserved_invariant", "")).strip() or "transport invariant"
    family = str(sketch.get("proof_strategy_family", "")).strip() or "proof route"
    strategy_name = str(sketch.get("strategy_name", "")).strip() or str(sketch.get("strategy_id", "")).strip()
    bridge = str(sketch.get("bridge_id", "")).strip()
    conjecture = str(sketch.get("conjecture_id", "")).strip()
    obligations = [row for row in _as_list(sketch.get("proof_obligations")) if isinstance(row, dict)]
    lemmas = [row for row in _as_list(sketch.get("candidate_lemmas")) if isinstance(row, dict)]
    suff_sets = [row for row in _as_list(sketch.get("sufficient_attribute_sets")) if isinstance(row, dict)]
    counterfactual = sketch.get("counterfactual_test", {}) if isinstance(sketch.get("counterfactual_test"), dict) else {}
    mathematical_argument = sketch.get("mathematical_argument", {}) if isinstance(sketch.get("mathematical_argument"), dict) else {}
    route_delta = (
        mathematical_argument.get("statement_delta", {})
        if isinstance(mathematical_argument.get("statement_delta"), dict)
        else sketch.get("statement_delta", {})
        if isinstance(sketch.get("statement_delta"), dict)
        else {}
    )
    source_focus = str(route_delta.get("source_claim_focus", "")).strip() or antecedent
    target_focus = str(route_delta.get("target_claim_focus", "")).strip() or consequence
    model_shift = str(route_delta.get("model_shift", "")).strip() or f"`{source_id}` -> `{target_id}`"
    threshold_shift = str(route_delta.get("threshold_shift", "")).strip() or "threshold shift not yet typed"
    consequence_shift = str(route_delta.get("consequence_shift", "")).strip() or f"derive `{consequence}`"
    missing_lemma = str(route_delta.get("missing_witness_or_transport", "")).strip() or "route-specific lemma not yet isolated"
    failure_mode = str(mathematical_argument.get("failure_mode", "")).strip()

    lines: list[str] = []
    lines.append("# Paper-Style Argument")
    lines.append("")
    lines.append("## Route")
    lines.append("")
    lines.append(f"- Selected sketch: `{sketch.get('sketch_id', '')}`")
    lines.append(f"- Strategy: `{sketch.get('strategy_id', '')}` ({strategy_name})")
    lines.append(f"- Bridge: `{bridge}`")
    lines.append(f"- Conjecture: `{conjecture}`")
    lines.append(f"- Strategy family: `{family}`")
    lines.append(f"- Target consequence: `{consequence}`")
    lines.append(f"- Antecedent schema: `{antecedent}`")
    lines.append(f"- Preserved invariant: `{invariant}`")
    lines.append(f"- Carrier kind: `{carrier_kind}`")
    lines.append(f"- Typing status: `{typing_status}`")
    lines.append("")

    lines.append("## Mathematical Context")
    lines.append("")
    if source_id:
        lines.append(f"Source theorem (`{source_id}`):")
        lines.append("")
        lines.append(f"> {source_text or 'Source statement text unavailable in the current KB snapshot.'}")
        lines.append("")
    if target_id:
        lines.append(f"Target theorem (`{target_id}`):")
        lines.append("")
        lines.append(f"> {target_text or 'Target statement text unavailable in the current KB snapshot.'}")
        lines.append("")
    lines.append(
        f"The selected route interprets the theorem pair as a transport from `{source_focus}` to `{target_focus}` through the invariant `{invariant}`."
    )
    lines.append("")

    lines.append("## Mathematical Delta")
    lines.append("")
    lines.append(f"- Model shift: {model_shift}")
    lines.append(f"- Threshold shift: {threshold_shift}")
    lines.append(f"- Consequence shift: {consequence_shift}")
    lines.append(f"- Missing route lemma: {missing_lemma}")
    lines.append("")

    lines.append("## Candidate Bridge Object")
    lines.append("")
    lines.append(
        f"Let $\\mathcal{{B}}$ denote the conjectured bridge object called `{obj}`. "
        f"It is intended to encode the minimal mathematical structure needed to carry `{source_focus}` from `{source_id}` "
        f"to `{target_focus}` at `{target_id}` while preserving `{invariant}`."
    )
    if mathematical_argument.get("bridge_definition"):
        lines.append("")
        lines.append(mathematical_argument.get("bridge_definition", ""))
    lines.append("")
    if suff_sets:
        first = suff_sets[0]
        attrs = [str(x).strip() for x in _as_list(first.get("attributes")) if str(x).strip()]
        if attrs:
            lines.append(
                f"We take the attribute set `{first.get('label', 'core set')}` as the minimal working specification of $\\mathcal{{B}}$:"
            )
            lines.append("")
            for idx, attr in enumerate(attrs, start=1):
                lines.append(f"{idx}. {attr}")
            lines.append("")

    lines.append("## Admissibility Conditions")
    lines.append("")
    assumptions = mathematical_argument.get("assumptions", []) if isinstance(mathematical_argument.get("assumptions"), list) else []
    if assumptions:
        lines.append("Minimal admissibility conditions:")
        lines.append("")
        for idx, item in enumerate(assumptions, start=1):
            lines.append(f"{idx}. {item}")
        lines.append("")
    else:
        lines.append("Assume there exists a realization of $\\mathcal{B}$ satisfying the needed transport conditions.")
        lines.append("")
    lines.append(f"## Proposition ({theorem_title})")
    lines.append("")
    lines.append(mathematical_argument.get("proposition", f"If $\\mathcal{{B}}$ is realized and preserves `{invariant}`, then `{consequence}` follows."))
    lines.append("")

    lines.append("## Lemma Chain")
    lines.append("")
    lemma_titles = ["Source-to-object lemma", "Transport lemma", "Payoff lemma"]
    for idx, lemma in enumerate(lemmas[:4], start=1):
        title = lemma_titles[idx - 1] if idx - 1 < len(lemma_titles) else f"Route lemma {idx}"
        lines.append(f"### Lemma {idx} ({title})")
        lines.append("")
        lines.append(str(lemma.get("statement", "")).strip() or "Statement unavailable.")
        lines.append("")
        if idx == 1:
            lines.append(f"This lemma isolates the point at which the source theorem content `{source_focus}` yields an explicit realization of the bridge object.")
        elif idx == 2:
            lines.append(
                f"This lemma is the transport step: it prevents the route from collapsing into topical similarity by forcing preservation of `{invariant}`."
            )
        elif idx == 3:
            lines.append(
                f"This lemma is the payoff step: the bridge is only allowed to claim the theorem-family consequence `{consequence}` here."
            )
        else:
            lines.append(
                f"This additional lemma localizes the theorem-pair-specific obstruction `{missing_lemma}`."
            )
        lines.append("")

    lines.append("## Proof")
    lines.append("")
    lines.append(f"Work in the `{strategy_name}` regime.")
    lines.append(
        f"The source theorem at `{source_id}` supplies the route content `{source_focus}`. By the source-to-object lemma, that content yields an admissible realization of the bridge object $\\mathcal{{B}}$ on the route from `{source_id}` to `{target_id}`."
    )
    lines.append(
        f"By the transport lemma, this realization preserves `{invariant}` in exactly the form needed to cross {model_shift}."
    )
    lines.append(
        f"The route-specific step `{missing_lemma}` is then the only remaining nonformal insertion. Once discharged, the payoff lemma converts the realized bridge object, together with the transported invariant, into the target consequence `{consequence}`."
    )
    lines.append(
        f"This matches the target theorem at `{target_id}`: {target_text or 'Target statement text unavailable in the current KB snapshot.'}"
    )
    lines.append(f"Therefore `{consequence}` follows conditionally on the stated bridge lemmas. $\\square$")
    lines.append("")

    lines.append("## Remaining Obligations")
    lines.append("")
    if obligations:
        lines.append("The present framework has not solved the problem; it has isolated the obligations that a real proof would still have to discharge:")
        lines.append("")
        for obligation in obligations[:7]:
            lines.append(
                f"- `{obligation.get('obligation_id', '')}`: {obligation.get('requirement', '')} "
                f"({obligation.get('why_it_matters', '')})"
            )
        lines.append("")
    else:
        lines.append("No explicit proof obligations were recorded.")
        lines.append("")

    lines.append("## Failure Diagnosis")
    lines.append("")
    if failure_mode:
        lines.append(failure_mode)
        lines.append("")
    else:
        lines.append("No explicit failure diagnosis was recorded.")
        lines.append("")

    lines.append("## Counterfactual Check")
    lines.append("")
    if counterfactual:
        lines.append(
            f"If one performs the intervention `{counterfactual.get('intervention', '')}`, the expected effect is `{counterfactual.get('expected_bridge_effect', '')}`."
        )
        lines.append(
            "This is the structural necessity test for the bridge concept: if the route survives the intervention unchanged, then the proposed object was not mathematically essential."
        )
        if mathematical_argument.get("failure_mode"):
            lines.append("")
            lines.append(f"Failure mode summary: {mathematical_argument.get('failure_mode', '')}")
    else:
        lines.append("No counterfactual probe was recorded for the selected sketch.")
    lines.append("")

    lines.append("## Provenance")
    lines.append("")
    lines.append(f"- sketch_id: `{sketch.get('sketch_id', '')}`")
    lines.append(f"- conjecture_id: `{conjecture}`")
    lines.append(f"- strategy_id: `{sketch.get('strategy_id', '')}`")
    lines.append(f"- bridge_id: `{bridge}`")
    lines.append(f"- anchor_statement_id: `{source_id}`")
    lines.append(f"- target_statement_id: `{target_id}`")
    lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    """
    Relevance: Operates within the proof-sketch synthesis layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds parsing, sketch synthesis, and artifact emission into a reproducible execution path.
    """

    logger = ReasoningLogger("kb-proof-sketcher")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--conjectures", required=True)
    ap.add_argument("--strategies", required=True)
    ap.add_argument("--bridges", required=True)
    ap.add_argument("--phyp", required=True)
    ap.add_argument("--analysis")
    ap.add_argument("--coherence-report")
    ap.add_argument("--hardness")
    ap.add_argument("--kb", help="Optional KB markdown path used for paper-style argument rendering.")
    ap.add_argument("--top-k", type=int, default=6)
    ap.add_argument("--output-json")
    ap.add_argument("--output-md")
    ap.add_argument("--output-paper-md")
    args = ap.parse_args()

    logger.step(
        "Parsed proof-sketcher arguments",
        "\n".join(
            [
                f"conjectures={args.conjectures}",
                f"strategies={args.strategies}",
                f"bridges={args.bridges}",
                f"phyp={args.phyp}",
                f"analysis={args.analysis or ''}",
                f"coherence_report={args.coherence_report or ''}",
                f"hardness={args.hardness or ''}",
                f"kb={args.kb or ''}",
                f"top_k={args.top_k}",
                f"output_json={args.output_json or ''}",
                f"output_md={args.output_md or ''}",
                f"output_paper_md={args.output_paper_md or ''}",
            ]
        ),
    )

    conjectures_path = Path(args.conjectures)
    strategies_path = Path(args.strategies)
    bridges_path = Path(args.bridges)
    phyp_path = Path(args.phyp)
    analysis_path = Path(args.analysis) if args.analysis else None
    coherence_path = Path(args.coherence_report) if args.coherence_report else None
    hardness_path = Path(args.hardness) if args.hardness else None
    kb_path = Path(args.kb) if args.kb else None

    for path in [conjectures_path, strategies_path, bridges_path, phyp_path]:
        if not path.exists():
            log_path = logger.finalize("error", summary=f"Missing input: {path}")
            print(f"[LOG] {log_path}", file=sys.stderr)
            raise SystemExit(f"[ERROR] Missing input: {path}")
    for path in [analysis_path, coherence_path, hardness_path, kb_path]:
        if path and not path.exists():
            log_path = logger.finalize("error", summary=f"Missing input: {path}")
            print(f"[LOG] {log_path}", file=sys.stderr)
            raise SystemExit(f"[ERROR] Missing input: {path}")

    try:
        conjectures = validate_conjecture_report(json.loads(conjectures_path.read_text(encoding="utf-8")), name="conjectures")
        strategies = validate_strategy_report(json.loads(strategies_path.read_text(encoding="utf-8")), name="strategies")
        bridges = validate_bridges(json.loads(bridges_path.read_text(encoding="utf-8")), name="bridges")
        phyp = validate_phyp(yaml.safe_load(phyp_path.read_text(encoding="utf-8")), name="phyp")
        analysis = json.loads(analysis_path.read_text(encoding="utf-8")) if analysis_path else {}
        coherence = (
            validate_coherence_report(json.loads(coherence_path.read_text(encoding="utf-8")), name="coherence")
            if coherence_path
            else {}
        )
        hardness = json.loads(hardness_path.read_text(encoding="utf-8")) if hardness_path else {}
        kb_statements = _load_kb_statements(kb_path)

        report = _build(
            conjectures=conjectures,
            strategies=strategies,
            bridges=bridges,
            phyp=phyp,
            analysis=analysis if isinstance(analysis, dict) else {},
            coherence=coherence,
            hardness=hardness if isinstance(hardness, dict) else {},
            top_k=max(1, args.top_k),
            kb_statements=kb_statements,
        )
        sketches = report.get("proof_sketches", []) if isinstance(report.get("proof_sketches"), list) else []
        logger.step(
            "Proof sketch trace",
            "\n".join(
                [
                    "top_sketches="
                    + "; ".join(
                        f"{str(row.get('sketch_id', '')).strip()}:{str(row.get('conjecture_id', '')).strip()}:{str(row.get('proof_strategy_family', '')).strip()}:{float(row.get('sketch_score', 0.0) or 0.0):.4f}"
                        for row in sketches[:6]
                        if isinstance(row, dict) and str(row.get("sketch_id", "")).strip()
                    ),
                    "top_propositions="
                    + "; ".join(
                        f"{str(row.get('sketch_id', '')).strip()}:{str((row.get('mathematical_argument', {}) if isinstance(row.get('mathematical_argument'), dict) else {}).get('proposition', '')).strip()}"
                        for row in sketches[:4]
                        if isinstance(row, dict)
                        and str(row.get("sketch_id", "")).strip()
                        and str((row.get("mathematical_argument", {}) if isinstance(row.get("mathematical_argument"), dict) else {}).get("proposition", "")).strip()
                    ),
                    "families="
                    + json.dumps(report.get("metadata", {}).get("family_distribution", {}), ensure_ascii=False),
                ]
            ),
        )

        if args.output_json:
            out = Path(args.output_json)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"[OK] Wrote JSON: {out}")
            logger.add_output("proof_sketches_json", out)
        if args.output_md:
            out = Path(args.output_md)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(_to_markdown(report), encoding="utf-8")
            print(f"[OK] Wrote Markdown: {out}")
            logger.add_output("proof_sketches_md", out)
        if args.output_paper_md:
            out = Path(args.output_paper_md)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(_paper_style_argument(report, kb_statements=kb_statements), encoding="utf-8")
            print(f"[OK] Wrote Paper-Style Argument: {out}")
            logger.add_output("paper_style_argument_md", out)
            top = sketches[0] if sketches else {}
            logger.step(
                "Paper-style argument trace",
                "\n".join(
                    [
                        f"top_sketch={top.get('sketch_id', '') if isinstance(top, dict) else ''}",
                        f"target={top.get('target_consequence_schema', '') if isinstance(top, dict) else ''}",
                        f"antecedent={top.get('support_antecedent_schema', '') if isinstance(top, dict) else ''}",
                        f"invariant={top.get('preserved_invariant', '') if isinstance(top, dict) else ''}",
                        "proposition="
                        + str(
                            (top.get("mathematical_argument", {}) if isinstance(top.get("mathematical_argument"), dict) else {}).get(
                                "proposition", ""
                            )
                        ).strip(),
                    ]
                ),
            )

        print(f"[OK] Proof sketches: {len(sketches)}")
        if sketches:
            top = sketches[0]
            logger.step(
                "Selected top proof sketch",
                "\n".join(
                    [
                        f"sketch_id={top.get('sketch_id', '')}",
                        f"conjecture_id={top.get('conjecture_id', '')}",
                        f"family={top.get('proof_strategy_family', '')}",
                        f"score={top.get('sketch_score', 0.0)}",
                        "proposition="
                        + str(
                            (top.get("mathematical_argument", {}) if isinstance(top.get("mathematical_argument"), dict) else {}).get(
                                "proposition", ""
                            )
                        ).strip(),
                    ]
                ),
            )
        log_path = logger.finalize("success", summary=f"Generated {len(sketches)} proof sketches.")
        print(f"[LOG] {log_path}")
        return 0
    except Exception as exc:
        log_path = logger.finalize("error", summary=f"Proof sketch generation failed: {exc}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
