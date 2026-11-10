#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Synthesize a paper-style analysis and expert hypothesis recommendations from final KB artifacts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import logging
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

_log = logging.getLogger(__name__)

import yaml

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from contracts import validate_bridges
from contracts import validate_coherence_report
from contracts import validate_conjecture_report
from contracts import validate_connection_analysis
from contracts import validate_entrypoints
from contracts import validate_pathways
from contracts import validate_phyp
from contracts import validate_proof_sketch_report
from contracts import validate_strategy_report
from kb_context import canonical_artifacts_dir
from kb_context import resolve_kb_reference
from reasoning_log import ReasoningLogger
from statement_text import load_statement_index
from statement_text import statement_excerpt


HYP_KIND_NOVELTY: dict[str, float] = {
    "definition-introduction": 0.95,
    "representation-shift": 0.92,
    "intermediate-invariant": 0.90,
    "barrier-escape-principle": 0.93,
    "analogy-transfer": 0.84,
    "normal-form-reduction": 0.82,
    "bridge-link": 0.78,
    "intervention-focus": 0.58,
}

# Generative scoring policy tuned for "high-upside but testable" expert recommendations.
GEN_FUNC_WEIGHTS: dict[str, float] = {
    "support_signal": 0.21,
    "coherence_signal": 0.14,
    "explanatory_signal": 0.14,
    "structural_leverage": 0.16,
    "strategy_leverage": 0.12,
    "anti_barrier_alignment": 0.08,
    "testability": 0.07,
    "novelty_signal": 0.08,
    "revision_priority": 0.05,
}

GEN_RISK_WEIGHTS: dict[str, float] = {
    "refutation_risk": 0.45,
    "negative_coherence_risk": 0.22,
    "barrier_pressure_risk": 0.18,
    "uncertainty_risk": 0.15,
}

BRIDGE_FUNC_WEIGHTS: dict[str, float] = {
    "bridge_signal": 0.16,
    "conjecture_priority": 0.12,
    "sketch_score": 0.14,
    "hypothesis_support": 0.10,
    "mathematical_specificity": 0.18,
    "evidence_signal": 0.14,
    "falsifiability_signal": 0.08,
    "sketch_operationalization": 0.05,
    "search_novelty_signal": 0.03,
}

def _safe_float(value: Any, default: float = 0.0) -> float:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Defensive conversion/parsing to keep scoring and reporting robust.
    Contribution: Reduces runtime ambiguity and prevents malformed artifacts from destabilizing the workflow.
    """

    try:
        return float(value)
    except (TypeError, ValueError):
        _log.warning("_safe_float: could not convert %r to float; using default %s", value, default)
        return default


def _clamp01(value: float) -> float:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Score-domain normalization helper.
    Contribution: Keeps all component metrics within a comparable [0,1] range for transparent weighted scoring.
    """

    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return value


def _load_json(path: Path) -> dict[str, Any]:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Provides clean, typed inputs so downstream reasoning steps remain auditable.
    """

    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _load_yaml(path: Path) -> dict[str, Any]:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Enables robust ingestion of hypothesis inventories when JSON reports are absent or partial.
    """

    if not path.exists():
        return {}
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _load_optional_validated_json(path: Path, validator: Any, warnings: list[str], name: str) -> dict[str, Any]:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Soft validation wrapper for optional upstream artifacts.
    Contribution: Preserves pipeline robustness by using validated payloads when available while surfacing schema drift as warnings.
    """

    payload = _load_json(path)
    if not payload:
        warnings.append(f"missing:{name}:{path}")
        return {}
    try:
        return validator(payload, name=name)
    except Exception as exc:
        warnings.append(f"invalid:{name}:{path}:{exc}")
        return {}


def _statement_index_from_kb(kb_path: Path) -> dict[str, dict[str, Any]]:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Deterministic recovery of typed KB statements for narrative rendering.
    Contribution: Lets paper output cite statement previews and phases directly from the source KB.
    """

    return load_statement_index(kb_path)


def _normalize_map(values: dict[str, float]) -> dict[str, float]:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Normalization of sparse score maps into a stable range.
    Contribution: Prevents one artifact family from dominating the generative function solely by scale.
    """

    if not values:
        return {}
    max_v = max(values.values())
    if max_v <= 1e-9:
        return {k: 0.0 for k in values}
    return {k: _clamp01(v / max_v) for k, v in values.items()}


def _hypothesis_eval_index(hyp_eval: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Construction of derived lookups from hypothesis-evaluation outputs.
    Contribution: Aligns each hypothesis with measured support/refute/confidence signals for expert ranking.
    """

    out: dict[str, dict[str, Any]] = {}
    rows = hyp_eval.get("results", []) if isinstance(hyp_eval.get("results"), list) else []
    for row in rows:
        if not isinstance(row, dict):
            continue
        hid = str(row.get("hypothesis_id", "")).strip()
        if hid:
            out[hid] = row
    return out


def _coherence_index(coherence: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Construction of derived lookups from coherence outputs.
    Contribution: Injects global-theory-fit and explanatory-unification diagnostics into recommendation decisions.
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


def _entrypoint_statement_scores(entrypoints: dict[str, Any]) -> dict[str, float]:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Extraction of statement-level leverage from entrypoint rankings.
    Contribution: Encodes where interventions are likely to maximize downstream inferential impact.
    """

    out: dict[str, float] = {}
    rows = entrypoints.get("ranked_entrypoints", []) if isinstance(entrypoints.get("ranked_entrypoints"), list) else []
    for row in rows:
        if not isinstance(row, dict):
            continue
        sid = str(row.get("statement_id", "")).strip()
        if not sid:
            continue
        out[sid] = max(out.get(sid, 0.0), _safe_float(row.get("entry_score", 0.0)))
    return out


def _intervention_statement_scores(analysis: dict[str, Any]) -> dict[str, float]:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Extraction of statement-level leverage from connector interventions.
    Contribution: Integrates graph-central intervention pressure into hypothesis prioritization.
    """

    out: dict[str, float] = {}
    rows = analysis.get("top_interventions", []) if isinstance(analysis.get("top_interventions"), list) else []
    for row in rows:
        if not isinstance(row, dict):
            continue
        sid = str(row.get("statement_id", "")).strip()
        if not sid:
            continue
        out[sid] = max(out.get(sid, 0.0), _safe_float(row.get("score", 0.0)))
    return out


def _pathway_signals(pathways: dict[str, Any]) -> tuple[dict[str, float], dict[str, float]]:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Construction of hypothesis and statement participation maps from pathway synthesis.
    Contribution: Rewards hypotheses that repeatedly appear in high-scoring operational proof pathways.
    """

    hyp_weight: dict[str, float] = defaultdict(float)
    stmt_weight: dict[str, float] = defaultdict(float)
    rows = pathways.get("pathways", []) if isinstance(pathways.get("pathways"), list) else []
    for row in rows:
        if not isinstance(row, dict):
            continue
        pscore = _clamp01(_safe_float(row.get("pathway_score", 0.0)))
        weight = 0.35 + 0.65 * pscore
        entry_sid = str(row.get("entry_statement_id", "")).strip()
        if entry_sid:
            stmt_weight[entry_sid] += weight
        for hrow in row.get("supporting_hypotheses", []) if isinstance(row.get("supporting_hypotheses"), list) else []:
            if not isinstance(hrow, dict):
                continue
            hid = str(hrow.get("id", "")).strip()
            if hid:
                hyp_weight[hid] += weight
        for lrow in row.get("supporting_links", []) if isinstance(row.get("supporting_links"), list) else []:
            if not isinstance(lrow, dict):
                continue
            sid_from = str(lrow.get("from_id", "")).strip()
            sid_to = str(lrow.get("to_id", "")).strip()
            if sid_from:
                stmt_weight[sid_from] += 0.5 * weight
            if sid_to:
                stmt_weight[sid_to] += 0.5 * weight
    return dict(hyp_weight), dict(stmt_weight)


def _strategy_signals(
    strategies: dict[str, Any], proof_sketches: dict[str, Any]
) -> tuple[dict[str, float], dict[str, float], dict[str, list[str]], dict[str, float]]:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Construction of hypothesis-level leverage from strategy and sketch artifacts.
    Contribution: Captures whether a hypothesis already activates multiple viable strategy regimes.
    """

    hyp_counts: dict[str, float] = defaultdict(float)
    hyp_fertility_values: dict[str, list[float]] = defaultdict(list)
    hyp_strategy_ids: dict[str, list[str]] = defaultdict(list)
    strategy_sketch_counts: dict[str, float] = defaultdict(float)

    for row in proof_sketches.get("proof_sketches", []) if isinstance(proof_sketches.get("proof_sketches"), list) else []:
        if not isinstance(row, dict):
            continue
        sid = str(row.get("strategy_id", "")).strip()
        if sid:
            strategy_sketch_counts[sid] += 1.0

    for row in strategies.get("strategies", []) if isinstance(strategies.get("strategies"), list) else []:
        if not isinstance(row, dict):
            continue
        strategy_id = str(row.get("strategy_id", "")).strip()
        strategy_score = _clamp01(_safe_float(row.get("strategy_score", 0.0)))
        fertility = _clamp01(_safe_float(row.get("concept_fertility", 0.0)))
        sketch_presence = _clamp01(strategy_sketch_counts.get(strategy_id, 0.0))
        boost = 0.20 * sketch_presence
        hids = row.get("hypothesis_ids", []) if isinstance(row.get("hypothesis_ids"), list) else []
        for hid_raw in hids:
            hid = str(hid_raw).strip()
            if not hid:
                continue
            hyp_counts[hid] += strategy_score + boost
            hyp_fertility_values[hid].append(fertility)
            if strategy_id:
                hyp_strategy_ids[hid].append(strategy_id)

    hyp_fertility_avg: dict[str, float] = {}
    for hid, values in hyp_fertility_values.items():
        if values:
            hyp_fertility_avg[hid] = _clamp01(sum(values) / len(values))
        else:
            hyp_fertility_avg[hid] = 0.0
    return dict(hyp_counts), hyp_fertility_avg, dict(hyp_strategy_ids), dict(strategy_sketch_counts)


def _revision_targets(revision: dict[str, Any]) -> set[str]:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Extraction of structured targets from ontology-revision outputs.
    Contribution: Prioritizes hypotheses whose adjacent statements are explicitly marked as bottlenecks for next-round progress.
    """

    targets: set[str] = set()
    for key in ("priority_program", "revision_actions"):
        rows = revision.get(key, []) if isinstance(revision.get(key), list) else []
        for row in rows:
            if not isinstance(row, dict):
                continue
            tids = row.get("target_statement_ids", []) if isinstance(row.get("target_statement_ids"), list) else []
            for sid in tids:
                sid_s = str(sid).strip()
                if sid_s:
                    targets.add(sid_s)
    return targets


def _hardness_signals(hardness: dict[str, Any]) -> tuple[set[str], float]:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Aggregation of anti-barrier and pressure signals from hardness diagnostics.
    Contribution: Connects hypothesis ranking to epistemological constraints instead of local hypothesis quality only.
    """

    families: set[str] = set()
    rows = hardness.get("anti_barrier_programs", []) if isinstance(hardness.get("anti_barrier_programs"), list) else []
    for row in rows:
        if not isinstance(row, dict):
            continue
        fam = str(row.get("barrier_family", "")).strip().lower()
        if fam:
            families.add(fam)

    pressure = 0.0
    pressure_rows = hardness.get("essential_elements", []) if isinstance(hardness.get("essential_elements"), list) else []
    if pressure_rows:
        total = 0.0
        for row in pressure_rows:
            if not isinstance(row, dict):
                continue
            name = str(row.get("name", "")).strip().lower()
            score = _clamp01(_safe_float(row.get("score", 0.0)))
            sev = str(row.get("severity", "")).strip().lower()
            sev_bonus = 1.0 if sev == "high" else 0.75 if sev == "moderate" else 0.6
            barrier_bonus = 1.0 if "barrier" in name else 0.75
            total += score * sev_bonus * barrier_bonus
        pressure = _clamp01(total / max(1, len(pressure_rows)))
    return families, pressure


def _extract_barrier_scope(hyp: dict[str, Any], hyp_eval_row: dict[str, Any]) -> str:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Typed extraction of inferential barrier scope for a hypothesis.
    Contribution: Aligns hypothesis-level risk and anti-barrier opportunity estimation.
    """

    c_eval = hyp_eval_row.get("inferential_commitment", {})
    if isinstance(c_eval, dict):
        scope = str(c_eval.get("barrier_scope", "")).strip().lower()
        if scope:
            return scope
    c_hyp = hyp.get("inferential_commitment", {})
    if isinstance(c_hyp, dict):
        scope = str(c_hyp.get("barrier_scope", "")).strip().lower()
        if scope:
            return scope
    metrics = hyp.get("metrics", {})
    if isinstance(metrics, dict):
        scope = str(metrics.get("barrier_scope", "")).strip().lower()
        if scope:
            return scope
    return "none"


def _testability_score(hyp: dict[str, Any]) -> float:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Estimation of how operationally testable a hypothesis is.
    Contribution: Avoids recommending conceptually attractive but experimentally intractable hypotheses.
    """

    protocol = hyp.get("validation_protocol", [])
    if not isinstance(protocol, list):
        protocol = []
    n_steps = len([str(step).strip() for step in protocol if str(step).strip()])
    falsifier = str(hyp.get("falsifier", "")).strip()
    has_falsifier = 1.0 if falsifier else 0.0
    step_strength = _clamp01(n_steps / 4.0)
    has_protocol = 1.0 if n_steps > 0 else 0.0
    return _clamp01(0.45 * has_protocol + 0.35 * step_strength + 0.20 * has_falsifier)


def _kind_novelty(kind: str) -> float:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Prior over hypothesis-type novelty.
    Contribution: Increases selection pressure toward concept-discovery hypotheses when evidence supports them.
    """

    return _clamp01(HYP_KIND_NOVELTY.get(kind.strip().lower(), 0.62))


def _recommendation_tier(score: float, risk: float, min_score: float) -> str:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Typed policy mapping numeric hypothesis quality to expert-facing recommendation bands.
    Contribution: Produces interpretable recommendation classes for downstream human prioritization.
    """

    if score >= 0.72 and risk <= 0.35:
        return "Tier-1: Immediate Expert Focus"
    if score >= 0.60:
        return "Tier-2: High-Upside Program"
    if score >= min_score:
        return "Tier-3: Exploratory Candidate"
    return "Hold"


def _statement_preview(statement_index: dict[str, dict[str, Any]], sid: str, limit: int = 220) -> str:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Compact semantic projection of statement content for reporting.
    Contribution: Gives experts quick context on target/support statements without forcing KB navigation.
    """

    stmt = statement_index.get(sid, {})
    if not isinstance(stmt, dict):
        return ""
    return statement_excerpt(stmt, limit=limit)


def _merge_statement_delta(*candidates: Any) -> dict[str, Any]:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Merge helper for bridge-level statement deltas propagated across stages.
    Contribution: Preserves the most specific route diagnosis available when assembling the final paper.
    """

    merged: dict[str, Any] = {}
    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue
        for key, value in candidate.items():
            if isinstance(value, str):
                if value.strip():
                    merged[key] = value
            elif value:
                merged[key] = value
    return merged


def _is_placeholder_text(value: Any) -> bool:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Detection of underspecified mathematical placeholders.
    Contribution: Prevents bridge scores from mistaking scaffold labels for theorem-relevant mathematical content.
    """

    text = str(value or "").strip().lower()
    if not text:
        return True
    placeholder_tokens = (
        "unspecified",
        "underspecified",
        "untyped",
        "not yet typed",
        "support-to-target interface",
        "statement-conclusion",
        "bridge object",
        "route not yet typed",
    )
    return any(token in text for token in placeholder_tokens)


def _mathematical_specificity(
    *,
    abstraction_label: str,
    carrier_kind: str,
    typing_status: str,
    statement_delta: dict[str, Any],
    missing_route_lemma: str,
    proof_obligations: list[str],
    candidate_lemmas: list[str],
) -> float:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Estimate of how theorem-shaped and mathematically inspectable a route currently is.
    Contribution: Separates content specificity from mere scaffold completeness.
    """

    typed_signal = 1.0 if str(typing_status).strip().lower() == "typed" else 0.25
    object_signal = 0.0 if _is_placeholder_text(abstraction_label) else 1.0
    carrier_signal = 0.0 if _is_placeholder_text(carrier_kind) else (1.0 if len(str(carrier_kind).strip()) >= 18 else 0.7)
    source_focus = str(statement_delta.get("source_claim_focus", "")).strip()
    target_focus = str(statement_delta.get("target_claim_focus", "")).strip()
    theorem_binding = 0.0
    if source_focus and not _is_placeholder_text(source_focus):
        theorem_binding += 0.4
    if target_focus and not _is_placeholder_text(target_focus):
        theorem_binding += 0.4
    if str(statement_delta.get("route_synopsis", "")).strip():
        theorem_binding += 0.2
    theorem_binding = _clamp01(theorem_binding)
    lemma_signal = 0.0 if _is_placeholder_text(missing_route_lemma) else 1.0
    obligation_signal = min(1.0, len([item for item in proof_obligations if not _is_placeholder_text(item)]) / 3.0)
    lemma_chain_signal = min(1.0, len([item for item in candidate_lemmas if not _is_placeholder_text(item)]) / 3.0)
    return _clamp01(
        0.18 * typed_signal
        + 0.18 * object_signal
        + 0.16 * carrier_signal
        + 0.20 * theorem_binding
        + 0.16 * lemma_signal
        + 0.06 * obligation_signal
        + 0.06 * lemma_chain_signal
    )


def _bridge_evidence_signal(
    *,
    evidence_count: int,
    linked_hypothesis_rows: list[dict[str, Any]],
) -> float:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Estimate of how much bridge support comes from actual evidence rather than internal coherence only.
    Contribution: Penalizes runs with no external/adversarial evidence while still distinguishing among internally stronger routes.
    """

    empirical_signal = min(1.0, max(0, int(evidence_count)) / 4.0)
    if not linked_hypothesis_rows:
        internal_signal = 0.0
    else:
        supported = sum(1 for row in linked_hypothesis_rows if str(row.get("eval_verdict", "")).strip() == "supported")
        inconclusive = sum(1 for row in linked_hypothesis_rows if str(row.get("eval_verdict", "")).strip() == "inconclusive")
        total = max(1, len(linked_hypothesis_rows))
        internal_signal = _clamp01(0.75 * (supported / total) + 0.25 * (1.0 - inconclusive / total))
    return _clamp01(0.75 * empirical_signal + 0.25 * internal_signal)


def _falsifiability_signal(*, counterfactual: dict[str, Any], abort_conditions: list[str], failure_diagnosis: str) -> float:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Estimate of how explicitly the route exposes ways to fail.
    Contribution: Rewards bridges that are inspectable under adversarial probing, not only constructive narration.
    """

    counterfactual_signal = 1.0 if isinstance(counterfactual, dict) and counterfactual else 0.0
    abort_signal = min(1.0, len([item for item in abort_conditions if str(item).strip()]) / 2.0)
    failure_signal = 0.0 if _is_placeholder_text(failure_diagnosis) else 1.0
    return _clamp01(0.45 * counterfactual_signal + 0.30 * abort_signal + 0.25 * failure_signal)


def _hypothesis_payload_to_row(
    hyp: dict[str, Any],
    hyp_eval_row: dict[str, Any],
    coh_row: dict[str, Any],
    entry_scores: dict[str, float],
    intervention_scores: dict[str, float],
    pathway_hyp_scores: dict[str, float],
    pathway_stmt_scores: dict[str, float],
    strategy_hyp_scores: dict[str, float],
    strategy_hyp_fertility: dict[str, float],
    strategy_ids_by_hyp: dict[str, list[str]],
    revision_targets: set[str],
    anti_barrier_families: set[str],
    global_barrier_pressure: float,
) -> dict[str, Any]:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Main generative scoring transform from hypothesis payload to expert-prioritization row.
    Contribution: Produces auditable, factorized recommendation scores with explicit risk accounting.
    """

    hid = str(hyp.get("id", "")).strip()
    kind = str(hyp.get("kind", "")).strip().lower()
    priority = _clamp01(_safe_float(hyp.get("priority", 0.0)))

    target_id = str(
        hyp_eval_row.get("target_statement_id")
        or hyp.get("target_statement_id")
        or ""
    ).strip()
    support_id = str(
        hyp_eval_row.get("support_statement_id")
        or hyp.get("support_statement_id")
        or ""
    ).strip()

    support_signal = _clamp01(
        _safe_float(hyp_eval_row.get("support_score", 0.35 + 0.50 * priority))
    )
    refute_signal = _clamp01(
        _safe_float(hyp_eval_row.get("refute_score", 0.15))
    )
    confidence = _clamp01(
        _safe_float(hyp_eval_row.get("confidence", 0.40 + 0.40 * priority))
    )

    coherence_delta = _safe_float(
        coh_row.get("coherence_delta_global"),
        _safe_float(
            (hyp_eval_row.get("signals", {}) if isinstance(hyp_eval_row.get("signals"), dict) else {}).get(
                "coherence_delta_global", 0.0
            ),
            0.0,
        ),
    )
    explanatory_signal = _clamp01(
        _safe_float(
            coh_row.get("explanatory_power_local"),
            _safe_float(
                (hyp_eval_row.get("signals", {}) if isinstance(hyp_eval_row.get("signals"), dict) else {}).get(
                    "explanatory_power_local", 0.0
                ),
                0.0,
            ),
        )
    )
    coherence_signal = _clamp01(0.5 + coherence_delta / 0.20)
    negative_coherence_risk = _clamp01((-coherence_delta) / 0.20)

    entry_signal = max(entry_scores.get(target_id, 0.0), entry_scores.get(support_id, 0.0))
    intervention_signal = max(intervention_scores.get(target_id, 0.0), intervention_scores.get(support_id, 0.0))
    pathway_signal = max(
        pathway_hyp_scores.get(hid, 0.0),
        pathway_stmt_scores.get(target_id, 0.0),
        pathway_stmt_scores.get(support_id, 0.0),
    )
    structural_leverage = _clamp01(0.45 * entry_signal + 0.35 * intervention_signal + 0.20 * pathway_signal)

    strategy_leverage = _clamp01(strategy_hyp_scores.get(hid, 0.0))
    fertility = _clamp01(strategy_hyp_fertility.get(hid, 0.0))
    novelty_signal = _clamp01(0.60 * fertility + 0.40 * _kind_novelty(kind))

    barrier_scope = _extract_barrier_scope(hyp, hyp_eval_row)
    if barrier_scope and barrier_scope != "none" and barrier_scope in anti_barrier_families:
        anti_barrier_alignment = 1.0
    elif barrier_scope and barrier_scope != "none" and anti_barrier_families:
        anti_barrier_alignment = 0.45
    elif barrier_scope in {"none", "", "untyped-barrier"}:
        anti_barrier_alignment = 0.60
    else:
        anti_barrier_alignment = 0.40
    barrier_pressure_risk = _clamp01(global_barrier_pressure * (1.0 if barrier_scope not in {"", "none"} else 0.5))

    testability = _testability_score(hyp)
    revision_priority = 1.0 if (target_id in revision_targets or support_id in revision_targets) else 0.0
    uncertainty_risk = _clamp01(1.0 - confidence)

    potential_raw = (
        GEN_FUNC_WEIGHTS["support_signal"] * support_signal
        + GEN_FUNC_WEIGHTS["coherence_signal"] * coherence_signal
        + GEN_FUNC_WEIGHTS["explanatory_signal"] * explanatory_signal
        + GEN_FUNC_WEIGHTS["structural_leverage"] * structural_leverage
        + GEN_FUNC_WEIGHTS["strategy_leverage"] * strategy_leverage
        + GEN_FUNC_WEIGHTS["anti_barrier_alignment"] * anti_barrier_alignment
        + GEN_FUNC_WEIGHTS["testability"] * testability
        + GEN_FUNC_WEIGHTS["novelty_signal"] * novelty_signal
    )
    risk_raw = (
        GEN_RISK_WEIGHTS["refutation_risk"] * refute_signal
        + GEN_RISK_WEIGHTS["negative_coherence_risk"] * negative_coherence_risk
        + GEN_RISK_WEIGHTS["barrier_pressure_risk"] * barrier_pressure_risk
        + GEN_RISK_WEIGHTS["uncertainty_risk"] * uncertainty_risk
    )
    final_score = _clamp01(potential_raw * (1.0 - 0.55 * risk_raw) + GEN_FUNC_WEIGHTS["revision_priority"] * revision_priority)

    eval_verdict = str(hyp_eval_row.get("verdict", "unscored")).strip().lower()
    eval_action = str(hyp_eval_row.get("recommended_action", "")).strip()
    strategy_ids = strategy_ids_by_hyp.get(hid, [])

    justifications = [
        (
            f"Evidence balance: support={support_signal:.3f}, refute={refute_signal:.3f}, "
            f"confidence={confidence:.3f}."
        ),
        (
            f"Global-theory effect: coherence_delta={coherence_delta:+.4f}, "
            f"coherence_signal={coherence_signal:.3f}, explanatory_signal={explanatory_signal:.3f}."
        ),
        (
            f"Structural leverage: entry={entry_signal:.3f}, intervention={intervention_signal:.3f}, "
            f"pathway={pathway_signal:.3f}, combined={structural_leverage:.3f}."
        ),
        (
            f"Strategy leverage: linked_strategies={len(strategy_ids)}, strategy_signal={strategy_leverage:.3f}, "
            f"concept_fertility={fertility:.3f}."
        ),
        (
            f"Barrier/readiness: barrier_scope={barrier_scope or 'none'}, anti_barrier_alignment={anti_barrier_alignment:.3f}, "
            f"testability={testability:.3f}, revision_priority={revision_priority:.3f}."
        ),
        (
            f"Risk decomposition: refutation={refute_signal:.3f}, negative_coherence={negative_coherence_risk:.3f}, "
            f"barrier_pressure={barrier_pressure_risk:.3f}, uncertainty={uncertainty_risk:.3f}; aggregated_risk={risk_raw:.3f}."
        ),
    ]

    recommended_actions: list[str] = []
    if target_id and support_id:
        recommended_actions.append(
            f"Run focused deduction test on `{support_id} -> {target_id}` under the current inferential commitment."
        )
    if barrier_scope not in {"", "none"}:
        recommended_actions.append(
            f"Execute anti-barrier probe for scope `{barrier_scope}` and test whether the bridge survives representation shift."
        )
    if isinstance(hyp.get("validation_protocol"), list):
        for step in hyp.get("validation_protocol", [])[:2]:
            step_text = str(step).strip()
            if step_text:
                recommended_actions.append(step_text)
    if eval_action:
        recommended_actions.append(f"Follow evaluator action: {eval_action}.")

    return {
        "hypothesis_id": hid,
        "kind": kind,
        "target_statement_id": target_id,
        "support_statement_id": support_id,
        "status": str(hyp.get("status", "")).strip() or str(hyp_eval_row.get("next_status", "")).strip(),
        "eval_verdict": eval_verdict or "unscored",
        "tier": "",
        "scores": {
            "final": final_score,
            "potential_raw": potential_raw,
            "risk_raw": risk_raw,
            "support_signal": support_signal,
            "refute_signal": refute_signal,
            "confidence": confidence,
            "coherence_signal": coherence_signal,
            "coherence_delta_global": coherence_delta,
            "negative_coherence_risk": negative_coherence_risk,
            "explanatory_signal": explanatory_signal,
            "structural_leverage": structural_leverage,
            "entry_signal": entry_signal,
            "intervention_signal": intervention_signal,
            "pathway_signal": pathway_signal,
            "strategy_leverage": strategy_leverage,
            "fertility": fertility,
            "novelty_signal": novelty_signal,
            "anti_barrier_alignment": anti_barrier_alignment,
            "barrier_pressure_risk": barrier_pressure_risk,
            "testability": testability,
            "revision_priority": revision_priority,
            "uncertainty_risk": uncertainty_risk,
        },
        "barrier_scope": barrier_scope,
        "linked_strategy_ids": strategy_ids,
        "justification": justifications,
        "expert_actions": recommended_actions[:6],
        "hypothesis_informal": str(hyp.get("informal", "")).strip(),
        "hypothesis_latex": str(hyp.get("hypothesis_latex", "")).strip(),
    }


def _bridge_lookup(bridges: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Construction of a bridge-program lookup for bridge-first reporting.
    Contribution: Makes conceptual bridge commitments directly reusable in the final expert narrative.
    """

    out: dict[str, dict[str, Any]] = {}
    for row in bridges.get("bridge_programs", []) if isinstance(bridges.get("bridge_programs"), list) else []:
        if not isinstance(row, dict):
            continue
        bridge_id = str(row.get("bridge_id", "")).strip()
        if bridge_id:
            out[bridge_id] = row
    return out


def _conjectures_by_bridge(conjectures: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Grouping conjectures by bridge program.
    Contribution: Aligns missing-object hypotheses with the bridge programs they are meant to complete.
    """

    out: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in conjectures.get("abstraction_conjectures", []) if isinstance(conjectures.get("abstraction_conjectures"), list) else []:
        if not isinstance(row, dict):
            continue
        bridge_id = str(row.get("bridge_id", "")).strip()
        if bridge_id:
            out[bridge_id].append(row)
    return out


def _sketches_by_bridge(proof_sketches: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Grouping proof sketches by bridge program.
    Contribution: Lets the final report explain each bridge together with its most relevant proof architecture.
    """

    out: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in proof_sketches.get("proof_sketches", []) if isinstance(proof_sketches.get("proof_sketches"), list) else []:
        if not isinstance(row, dict):
            continue
        bridge_id = str(row.get("bridge_id", "")).strip()
        if bridge_id:
            out[bridge_id].append(row)
    return out


def _proof_readiness(sketch: dict[str, Any]) -> float:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Estimation of how operationally mature a proof sketch is.
    Contribution: Rewards bridges whose associated sketches already expose obligations, lemmas, and decision points.
    """

    obligations = len(sketch.get("proof_obligations", [])) if isinstance(sketch.get("proof_obligations"), list) else 0
    lemmas = len(sketch.get("candidate_lemmas", [])) if isinstance(sketch.get("candidate_lemmas"), list) else 0
    steps = len(sketch.get("proof_outline_steps", [])) if isinstance(sketch.get("proof_outline_steps"), list) else 0
    counterfactual = 1.0 if isinstance(sketch.get("counterfactual_test"), dict) and sketch.get("counterfactual_test") else 0.0
    abort_conditions = 1.0 if isinstance(sketch.get("abort_conditions"), list) and sketch.get("abort_conditions") else 0.0
    return _clamp01(
        0.25 * min(1.0, obligations / 4.0)
        + 0.20 * min(1.0, lemmas / 3.0)
        + 0.20 * min(1.0, steps / 4.0)
        + 0.20 * counterfactual
        + 0.15 * abort_conditions
    )


def _bridge_hypothesis_support(linked_hypothesis_rows: list[dict[str, Any]]) -> float:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Verdict-aware aggregation of linked hypothesis support.
    Contribution: Prevents one highly scored row from dominating the bridge score when the surrounding evidence is mixed or inconclusive.
    """

    if not linked_hypothesis_rows:
        return 0.0
    weighted_scores: list[float] = []
    verdict_weights = {
        "supported": 1.0,
        "inconclusive": 0.65,
        "unscored": 0.55,
        "unknown": 0.50,
        "refuted": 0.0,
    }
    for row in linked_hypothesis_rows:
        verdict = str(row.get("eval_verdict", "")).strip().lower() or "unknown"
        verdict_weight = verdict_weights.get(verdict, 0.50)
        base_score = _safe_float((row.get("scores", {}) if isinstance(row.get("scores"), dict) else {}).get("final", 0.0))
        weighted_scores.append(verdict_weight * base_score)
    return _clamp01(sum(weighted_scores) / max(1, len(weighted_scores)))


def _bridge_priority_row(
    bridge: dict[str, Any],
    conjectures: list[dict[str, Any]],
    sketches: list[dict[str, Any]],
    hypothesis_rows_by_id: dict[str, dict[str, Any]],
    statement_index: dict[str, dict[str, Any]],
    evidence_count: int,
) -> dict[str, Any]:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Main transform from bridge/conjecture/sketch artifacts into an expert-facing conceptual bridge row.
    Contribution: Produces a bridge-first explanation layer that links conceptual gaps to concrete proof architectures.
    """

    bridge_id = str(bridge.get("bridge_id", "")).strip()
    raw_bridge_score = _clamp01(_safe_float(bridge.get("bridge_score", 0.0)))
    bridge_score = _clamp01(_safe_float(bridge.get("effective_bridge_score", raw_bridge_score)))
    best_conjecture = max(conjectures, key=lambda item: _safe_float(item.get("priority", 0.0))) if conjectures else {}
    best_sketch = max(sketches, key=lambda item: _safe_float(item.get("sketch_score", 0.0))) if sketches else {}
    conjecture_priority = _clamp01(_safe_float(best_conjecture.get("priority", 0.0)))
    sketch_score = _clamp01(_safe_float(best_sketch.get("sketch_score", 0.0)))
    sketch_operationalization = _proof_readiness(best_sketch) if best_sketch else 0.0

    linked_hypothesis_ids: list[str] = []
    inferential_commitment = bridge.get("inferential_commitment", {}) if isinstance(bridge.get("inferential_commitment"), dict) else {}
    hid = str(inferential_commitment.get("hypothesis_id", "")).strip()
    if hid:
        linked_hypothesis_ids.append(hid)
    for hyp_id in best_sketch.get("hypothesis_ids", []) if isinstance(best_sketch.get("hypothesis_ids"), list) else []:
        hyp_s = str(hyp_id).strip()
        if hyp_s and hyp_s not in linked_hypothesis_ids:
            linked_hypothesis_ids.append(hyp_s)
    linked_hypothesis_rows = [hypothesis_rows_by_id[h] for h in linked_hypothesis_ids if h in hypothesis_rows_by_id]
    hypothesis_support = _bridge_hypothesis_support(linked_hypothesis_rows)

    barrier_scope = (
        str(best_sketch.get("barrier_scope", "")).strip()
        or str(best_conjecture.get("barrier_scope", "")).strip()
        or str(inferential_commitment.get("barrier_scope", "")).strip()
        or "none"
    )
    barrier_penalty = 0.15 if barrier_scope not in {"", "none"} else 0.0

    source_id = str(bridge.get("from_id", "") or best_sketch.get("source_statement_id", "")).strip()
    target_id = str(bridge.get("to_id", "") or best_sketch.get("target_statement_id", "")).strip()
    source_preview = _statement_preview(statement_index, source_id)
    target_preview = _statement_preview(statement_index, target_id)
    source_excerpt = _statement_preview(statement_index, source_id, limit=420)
    target_excerpt = _statement_preview(statement_index, target_id, limit=420)
    gap_axes = []
    gap_target = str(best_conjecture.get("gap_target", "")).strip()
    if gap_target:
        gap_axes.extend(part.strip() for part in gap_target.split(",") if part.strip())
    abstraction_label = str(best_conjecture.get("abstraction_label", "")).strip()
    abstraction_type = str(best_conjecture.get("abstraction_type", "")).strip()
    mathematical_role = str(best_conjecture.get("mathematical_object_role", "")).strip()
    support_antecedent = str(
        best_sketch.get("support_antecedent_schema", "")
        or best_conjecture.get("support_antecedent_schema", "")
        or inferential_commitment.get("support_antecedent_schema", "")
    ).strip()
    target_consequence = str(
        best_sketch.get("target_consequence_schema", "")
        or best_conjecture.get("target_consequence_schema", "")
        or inferential_commitment.get("target_consequence_schema", "")
    ).strip()
    preserved_invariant = str(
        best_sketch.get("preserved_invariant", "")
        or best_conjecture.get("preserved_invariant", "")
        or inferential_commitment.get("preserved_invariant", "")
    ).strip()
    proof_family = str(best_sketch.get("proof_strategy_family", "")).strip()
    family_rationale = str(best_sketch.get("family_rationale", "")).strip()
    proof_outline = [
        str(item.get("objective", "")).strip()
        for item in best_sketch.get("proof_outline_steps", [])
        if isinstance(item, dict) and str(item.get("objective", "")).strip()
    ][:4]
    proof_obligations = [
        str(item.get("requirement", "")).strip()
        for item in best_sketch.get("proof_obligations", [])
        if isinstance(item, dict) and str(item.get("requirement", "")).strip()
    ][:5]
    candidate_lemmas = [
        str(item.get("statement", "")).strip()
        for item in best_sketch.get("candidate_lemmas", [])
        if isinstance(item, dict) and str(item.get("statement", "")).strip()
    ][:4]
    counterfactual = best_sketch.get("counterfactual_test", {}) if isinstance(best_sketch.get("counterfactual_test"), dict) else {}
    mathematical_argument = best_sketch.get("mathematical_argument", {}) if isinstance(best_sketch.get("mathematical_argument"), dict) else {}
    mathematical_spec = best_conjecture.get("mathematical_specification", {}) if isinstance(best_conjecture.get("mathematical_specification"), dict) else {}
    statement_delta = _merge_statement_delta(
        bridge.get("statement_delta", {}) if isinstance(bridge.get("statement_delta"), dict) else {},
        best_conjecture.get("statement_delta", {}) if isinstance(best_conjecture.get("statement_delta"), dict) else {},
        best_sketch.get("statement_delta", {}) if isinstance(best_sketch.get("statement_delta"), dict) else {},
        mathematical_argument.get("statement_delta", {}) if isinstance(mathematical_argument.get("statement_delta"), dict) else {},
        mathematical_spec.get("statement_delta", {}) if isinstance(mathematical_spec.get("statement_delta"), dict) else {},
    )
    negative_route = ""
    if counterfactual:
        negative_route = " ".join(
            part
            for part in (
                str(counterfactual.get("intervention", "")).strip(),
                str(counterfactual.get("expected_bridge_effect", "")).strip(),
                str(counterfactual.get("diagnostic_value", "")).strip(),
            )
            if part
        )
    abort_conditions = [
        str(item).strip()
        for item in best_sketch.get("abort_conditions", [])
        if str(item).strip()
    ][:3]
    bridge_definition = str(mathematical_argument.get("bridge_definition", "") or mathematical_spec.get("definition_template", "")).strip()
    conditional_proposition = str(mathematical_argument.get("proposition", "") or mathematical_spec.get("conditional_claim", "")).strip()
    carrier_kind = str(
        best_sketch.get("carrier_kind", "")
        or best_conjecture.get("carrier_kind", "")
        or mathematical_argument.get("carrier_kind", "")
        or mathematical_spec.get("carrier_kind", "")
    ).strip()
    typing_status = str(
        best_sketch.get("typing_status", "")
        or best_conjecture.get("typing_status", "")
        or mathematical_argument.get("typing_status", "")
        or mathematical_spec.get("typing_status", "")
    ).strip()
    route_synopsis = str(statement_delta.get("route_synopsis", "")).strip()
    model_shift = str(statement_delta.get("model_shift", "")).strip()
    threshold_shift = str(statement_delta.get("threshold_shift", "")).strip()
    consequence_shift = str(statement_delta.get("consequence_shift", "")).strip()
    missing_route_lemma = str(
        statement_delta.get("missing_witness_or_transport", "")
        or mathematical_spec.get("missing_route_lemma", "")
    ).strip()
    failure_diagnosis = str(
        mathematical_spec.get("obstruction_template", "")
        or mathematical_argument.get("failure_mode", "")
    ).strip()
    mathematical_assumptions = [
        str(item).strip()
        for item in (
            mathematical_argument.get("assumptions", [])
            if isinstance(mathematical_argument.get("assumptions"), list)
            else mathematical_spec.get("assumptions", [])
            if isinstance(mathematical_spec.get("assumptions"), list)
            else []
        )
        if str(item).strip()
    ][:4]
    mathematical_specificity = _mathematical_specificity(
        abstraction_label=abstraction_label,
        carrier_kind=carrier_kind,
        typing_status=typing_status or str(statement_delta.get("typing_status", "")).strip(),
        statement_delta=statement_delta,
        missing_route_lemma=missing_route_lemma,
        proof_obligations=proof_obligations,
        candidate_lemmas=candidate_lemmas,
    )
    evidence_signal = _bridge_evidence_signal(
        evidence_count=evidence_count,
        linked_hypothesis_rows=linked_hypothesis_rows,
    )
    falsifiability_signal = _falsifiability_signal(
        counterfactual=counterfactual,
        abort_conditions=abort_conditions,
        failure_diagnosis=failure_diagnosis,
    )
    bridge_signals = bridge.get("signals", {}) if isinstance(bridge.get("signals"), dict) else {}
    search_novelty_signal = _clamp01(_safe_float(bridge_signals.get("novelty_signal", 1.0), 1.0))

    justifications = [
        route_synopsis
        or (
            f"The bridge transports `{support_antecedent or 'support antecedent'}` toward "
            f"`{target_consequence or 'target consequence'}` while preserving "
            f"`{preserved_invariant or 'the selected invariant'}`."
        ),
        " / ".join(part for part in [f"model shift: {model_shift}" if model_shift else "", f"threshold shift: {threshold_shift}" if threshold_shift else "", f"consequence shift: {consequence_shift}" if consequence_shift else ""] if part),
        (
            f"The conjectured object `{abstraction_label or 'unnamed abstraction'}` is treated as "
            f"a `{abstraction_type or 'bridge abstraction'}` with carrier `{carrier_kind or 'bridge carrier'}`, playing the role `{mathematical_role or 'bridge object'}`."
        ),
        (
            f"The route-specific missing lemma is: {missing_route_lemma or 'not yet isolated'}; "
            f"the chosen proof family `{proof_family or 'untyped family'}` is used because "
            f"{family_rationale or 'it supplies the most concrete source-to-target transport mechanism currently available'}"
        ),
    ]
    priority = _clamp01(
        BRIDGE_FUNC_WEIGHTS["bridge_signal"] * bridge_score
        + BRIDGE_FUNC_WEIGHTS["conjecture_priority"] * conjecture_priority
        + BRIDGE_FUNC_WEIGHTS["sketch_score"] * sketch_score
        + BRIDGE_FUNC_WEIGHTS["hypothesis_support"] * hypothesis_support
        + BRIDGE_FUNC_WEIGHTS["mathematical_specificity"] * mathematical_specificity
        + BRIDGE_FUNC_WEIGHTS["evidence_signal"] * evidence_signal
        + BRIDGE_FUNC_WEIGHTS["falsifiability_signal"] * falsifiability_signal
        + BRIDGE_FUNC_WEIGHTS["sketch_operationalization"] * sketch_operationalization
        + BRIDGE_FUNC_WEIGHTS["search_novelty_signal"] * search_novelty_signal
        - barrier_penalty
    )
    if bridge_score or conjecture_priority or sketch_score:
        justifications.append(
            (
                f"Bridge priority is supported by effective_bridge_score={bridge_score:.3f}, raw_bridge_score={raw_bridge_score:.3f}, "
                f"conjecture_priority={conjecture_priority:.3f}, sketch_score={sketch_score:.3f}, "
                f"hypothesis_support={hypothesis_support:.3f}, mathematical_specificity={mathematical_specificity:.3f}, "
                f"evidence_signal={evidence_signal:.3f}, falsifiability_signal={falsifiability_signal:.3f}, "
                f"sketch_operationalization={sketch_operationalization:.3f}, search_novelty_signal={search_novelty_signal:.3f}."
            )
        )
    if negative_route or abort_conditions:
        justifications.append(
            "The sketch is not only constructive: it also exposes a negative route or abort logic that can falsify the bridge rather than merely postponing judgment."
        )
    justifications = [item for item in justifications if str(item).strip()]

    expert_actions = []
    if missing_route_lemma:
        expert_actions.append(f"Discharge the route-specific lemma: {missing_route_lemma}")
    elif proof_obligations:
        expert_actions.append(f"Discharge the first obligation: {proof_obligations[0]}")
    if candidate_lemmas:
        expert_actions.append(f"Stabilize the main bridge lemma: {candidate_lemmas[0]}")
    if negative_route:
        expert_actions.append(f"Run the designated counterfactual probe: {negative_route}")
    elif abort_conditions:
        expert_actions.append(f"Track the main abort condition: {abort_conditions[0]}")

    return {
        "bridge_id": bridge_id,
        "bridge_type": str(bridge.get("bridge_type", "")).strip(),
        "source_statement_id": source_id,
        "target_statement_id": target_id,
        "source_preview": source_preview,
        "target_preview": target_preview,
        "source_excerpt": source_excerpt,
        "target_excerpt": target_excerpt,
        "priority": priority,
        "signals": {
            "bridge_signal": bridge_score,
            "raw_bridge_score": raw_bridge_score,
            "conjecture_priority": conjecture_priority,
            "sketch_score": sketch_score,
            "hypothesis_support": hypothesis_support,
            "mathematical_specificity": mathematical_specificity,
            "evidence_signal": evidence_signal,
            "falsifiability_signal": falsifiability_signal,
            "sketch_operationalization": sketch_operationalization,
            "proof_readiness": sketch_operationalization,
            "search_novelty_signal": search_novelty_signal,
            "barrier_penalty": barrier_penalty,
        },
        "support_antecedent_schema": support_antecedent,
        "target_consequence_schema": target_consequence,
        "preserved_invariant": preserved_invariant,
        "gap_axes": gap_axes,
        "abstraction_label": abstraction_label,
        "abstraction_type": abstraction_type,
        "mathematical_object_role": mathematical_role,
        "proof_strategy_family": proof_family,
        "family_rationale": family_rationale,
        "proof_outline": proof_outline,
        "proof_obligations": proof_obligations,
        "candidate_lemmas": candidate_lemmas,
        "bridge_definition": bridge_definition,
        "conditional_proposition": conditional_proposition,
        "mathematical_assumptions": mathematical_assumptions,
        "carrier_kind": carrier_kind,
        "typing_status": typing_status,
        "statement_delta": statement_delta,
        "route_synopsis": route_synopsis,
        "missing_route_lemma": missing_route_lemma,
        "failure_diagnosis": failure_diagnosis,
        "negative_route": negative_route,
        "abort_conditions": abort_conditions,
        "linked_hypothesis_ids": linked_hypothesis_ids,
        "linked_hypothesis_rows": [
            {
                "hypothesis_id": row.get("hypothesis_id", ""),
                "score": _safe_float(row.get("scores", {}).get("final", 0.0)),
                "tier": row.get("tier", ""),
                "kind": row.get("kind", ""),
            }
            for row in linked_hypothesis_rows
        ],
        "justification": justifications,
        "expert_actions": expert_actions[:4],
    }


def _bridge_portfolio(
    bridges: dict[str, Any],
    conjectures: dict[str, Any],
    proof_sketches: dict[str, Any],
    hypothesis_rows: list[dict[str, Any]],
    statement_index: dict[str, dict[str, Any]],
    evidence_count: int,
    top_k: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Composition of bridge-plan, abstraction, and sketch artifacts into a bridge-first portfolio.
    Contribution: Gives the final expert report a primary conceptual object of analysis beyond ranked hypotheses.
    """

    hypothesis_rows_by_id = {
        str(row.get("hypothesis_id", "")).strip(): row
        for row in hypothesis_rows
        if isinstance(row, dict) and str(row.get("hypothesis_id", "")).strip()
    }
    conjecture_map = _conjectures_by_bridge(conjectures)
    sketch_map = _sketches_by_bridge(proof_sketches)
    rows: list[dict[str, Any]] = []
    for bridge in bridges.get("bridge_programs", []) if isinstance(bridges.get("bridge_programs"), list) else []:
        if not isinstance(bridge, dict):
            continue
        rows.append(
            _bridge_priority_row(
                bridge=bridge,
                conjectures=conjecture_map.get(str(bridge.get("bridge_id", "")).strip(), []),
                sketches=sketch_map.get(str(bridge.get("bridge_id", "")).strip(), []),
                hypothesis_rows_by_id=hypothesis_rows_by_id,
                statement_index=statement_index,
                evidence_count=evidence_count,
            )
        )
    rows.sort(key=lambda item: _safe_float(item.get("priority", 0.0)), reverse=True)
    return rows, rows[: max(1, top_k)]


def _latex_escape(value: str) -> str:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Rendering helper for TeX artifact safety.
    Contribution: Ensures generated TeX compiles reliably even with symbol-heavy statement identifiers.
    """

    text = str(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text


def _render_markdown(
    kb_ref: str,
    rows: list[dict[str, Any]],
    top_rows: list[dict[str, Any]],
    bridge_rows: list[dict[str, Any]],
    top_bridge_rows: list[dict[str, Any]],
    statement_index: dict[str, dict[str, Any]],
    generated_utc: str,
    warnings: list[str],
) -> str:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Human-readable rendering of the final scientific argument and recommendation portfolio.
    Contribution: Converts raw inferential diagnostics into an expert-facing paper narrative.
    """
    top_ids = [row.get("hypothesis_id", "") for row in top_rows[:3] if row.get("hypothesis_id")]
    top_bridge_ids = [row.get("bridge_id", "") for row in top_bridge_rows[:3] if row.get("bridge_id")]
    abstract = (
        f"This paper-style synthesis aggregates final reasoning artifacts for `{kb_ref}` and applies a transparent "
        "generative bridge-and-hypothesis selection model to explain the main conceptual bridges, the proof sketches behind them, "
        "and the hypotheses that currently best support them. "
        f"The leading bridges are {', '.join(top_bridge_ids) if top_bridge_ids else 'not yet available'}, "
        f"and the top hypotheses are {', '.join(top_ids) if top_ids else 'not yet available'}."
    )

    lines: list[str] = []
    lines.append(f"# Expert Hypothesis Recommendation Paper: `{kb_ref}`")
    lines.append("")
    lines.append(f"- Generated (UTC): {generated_utc}")
    lines.append(f"- Hypotheses scored: {len(rows)}")
    lines.append(f"- Bridges synthesized: {len(bridge_rows)}")
    lines.append(f"- Main bridges highlighted: {len(top_bridge_rows)}")
    lines.append(f"- Recommended for experts: {len(top_rows)}")
    lines.append("")
    lines.append("## Abstract")
    lines.append("")
    lines.append(abstract)
    lines.append("")
    lines.append("## 1. Problem Context")
    lines.append("")
    lines.append(
        "The objective is to transform end-to-end inferential outputs into an expert-facing research agenda that does not only rank hypotheses locally, "
        "but explains why each recommendation has high expected epistemic payoff."
    )
    lines.append("")
    lines.append("## 2. Generative Recommendation Function")
    lines.append("")
    lines.append(
        "For each hypothesis `h`, we compute `Potential(h)` and `Risk(h)`, then derive a final recommendation score:"
    )
    lines.append("")
    lines.append("```math")
    lines.append("Potential(h) = 0.21 S + 0.14 C + 0.14 E + 0.16 L + 0.12 G + 0.08 A + 0.07 T + 0.08 N")
    lines.append("```")
    lines.append("")
    lines.append("```math")
    lines.append("Risk(h) = 0.45 R + 0.22 C^- + 0.18 B + 0.15 U")
    lines.append("```")
    lines.append("")
    lines.append("```math")
    lines.append("Score(h) = clip(Potential(h) * (1 - 0.55 Risk(h)) + 0.05 V, 0, 1)")
    lines.append("```")
    lines.append("")
    lines.append("Where:")
    lines.append("- `S`: support signal from hypothesis evaluation.")
    lines.append("- `C`: positive coherence contribution.")
    lines.append("- `E`: local explanatory power.")
    lines.append("- `L`: structural leverage across entrypoints/interventions/pathways.")
    lines.append("- `G`: strategy leverage from strategy/sketch artifacts.")
    lines.append("- `A`: anti-barrier alignment.")
    lines.append("- `T`: testability (validation protocol + falsifier clarity).")
    lines.append("- `N`: novelty/fertility signal.")
    lines.append("- `R`, `C^-`, `B`, `U`: refutation, negative coherence, barrier pressure, uncertainty.")
    lines.append("- `V`: revision-priority bonus when a hypothesis touches revision-loop targets.")
    lines.append("")
    lines.append(
        "For bridge-first interpretation, we synthesize a conceptual bridge priority from effective bridge strength, conjecture maturity, sketch strength, verdict-aware linked hypothesis support, mathematical specificity, evidential pressure, falsifiability, sketch operationalization, and search-space novelty:"
    )
    lines.append("")
    lines.append("```math")
    lines.append("BridgePriority(b) = 0.16 B + 0.12 C_b + 0.14 P_b + 0.10 H_b + 0.18 M_b + 0.14 E_b + 0.08 F_b + 0.05 O_b + 0.03 N_b - \\mathrm{BarrierPenalty}(b)")
    lines.append("```")
    lines.append("")
    lines.append("Where `B` is effective bridge-program strength, `C_b` is conjecture maturity, `P_b` is proof-sketch strength, `H_b` is verdict-aware linked hypothesis support, `M_b` is mathematical specificity, `E_b` is evidence signal, `F_b` is falsifiability, `O_b` is sketch operationalization, and `N_b` is search-space novelty.")
    lines.append("")
    lines.append("## 3. Main Conceptual Bridges")
    lines.append("")
    lines.append("| Rank | Bridge | Type | Priority | Consequence | Invariant | Proof family |")
    lines.append("|---|---|---|---:|---|---|---|")
    for idx, row in enumerate(top_bridge_rows, start=1):
        lines.append(
            "| "
            f"{idx} | {row.get('bridge_id', '')} | {row.get('bridge_type', '')} | "
            f"{_safe_float(row.get('priority', 0.0)):.4f} | {row.get('target_consequence_schema', '')} | "
            f"{row.get('preserved_invariant', '')} | {row.get('proof_strategy_family', '') or 'n/a'} |"
        )
    if not top_bridge_rows:
        lines.append("| - | - | - | - | - | - | - |")
    lines.append("")
    lines.append("## 4. Bridge-First Proof Sketch Interpretation")
    lines.append("")
    if not top_bridge_rows:
        lines.append("No bridge had enough combined bridge/conjecture/sketch support to justify an expert-facing conceptual synthesis.")
    for idx, row in enumerate(top_bridge_rows, start=1):
        lines.append(f"### {idx}. `{row.get('bridge_id', '')}`")
        lines.append("")
        lines.append(row.get("route_synopsis", "") or (
            f"This bridge is treated as a `{row.get('bridge_type', '')}` connecting "
            f"`{row.get('support_antecedent_schema', '') or 'support antecedent'}` to "
            f"`{row.get('target_consequence_schema', '') or 'target consequence'}`."
        ))
        lines.append("")
        lines.append(f"- Priority: {_safe_float(row.get('priority', 0.0)):.4f}")
        lines.append(f"- Source statement: `{row.get('source_statement_id', '') or 'n/a'}`")
        if row.get("source_excerpt"):
            lines.append(f"  source theorem: {row.get('source_excerpt', '')}")
        lines.append(f"- Target statement: `{row.get('target_statement_id', '') or 'n/a'}`")
        if row.get("target_excerpt"):
            lines.append(f"  target theorem: {row.get('target_excerpt', '')}")
        lines.append(f"- Candidate bridge object: `{row.get('abstraction_label', '') or 'n/a'}`")
        lines.append(f"- Abstraction type: `{row.get('abstraction_type', '') or 'n/a'}`")
        lines.append(f"- Carrier kind: `{row.get('carrier_kind', '') or 'n/a'}`")
        lines.append(f"- Typing status: `{row.get('typing_status', '') or 'n/a'}`")
        lines.append(f"- Mathematical role: `{row.get('mathematical_object_role', '') or 'n/a'}`")
        lines.append(f"- Preserved invariant: `{row.get('preserved_invariant', '') or 'n/a'}`")
        statement_delta = row.get("statement_delta", {}) if isinstance(row.get("statement_delta"), dict) else {}
        if statement_delta:
            lines.append("- Mathematical delta:")
            lines.append(f"  - model shift: {statement_delta.get('model_shift', '')}")
            lines.append(f"  - threshold shift: {statement_delta.get('threshold_shift', '')}")
            lines.append(f"  - consequence shift: {statement_delta.get('consequence_shift', '')}")
            lines.append(f"  - missing route lemma: {row.get('missing_route_lemma', '')}")
        if row.get("bridge_definition"):
            lines.append(f"- Bridge definition: {row.get('bridge_definition', '')}")
        if row.get("conditional_proposition"):
            lines.append(f"- Conditional proposition: {row.get('conditional_proposition', '')}")
        if row.get("mathematical_assumptions"):
            lines.append("- Mathematical assumptions:")
            for item in row.get("mathematical_assumptions", [])[:4]:
                lines.append(f"  - {item}")
        if row.get("gap_axes"):
            lines.append(f"- Dominant gap axes: {', '.join(row.get('gap_axes', []))}")
        lines.append(f"- Chosen proof family: `{row.get('proof_strategy_family', '') or 'n/a'}`")
        if row.get("family_rationale"):
            lines.append(f"- Why that family fits: {row.get('family_rationale', '')}")
        lines.append("- Why this bridge matters:")
        for reason in row.get("justification", []):
            lines.append(f"  - {reason}")
        lines.append("- Main proof obligations:")
        for obligation in row.get("proof_obligations", [])[:4]:
            lines.append(f"  - {obligation}")
        if not row.get("proof_obligations"):
            lines.append("  - none exposed yet")
        lines.append("- Main proof-sketch steps:")
        for step in row.get("proof_outline", [])[:4]:
            lines.append(f"  - {step}")
        if not row.get("proof_outline"):
            lines.append("  - none exposed yet")
        lines.append("- Candidate lemmas:")
        for lemma in row.get("candidate_lemmas", [])[:3]:
            lines.append(f"  - {lemma}")
        if not row.get("candidate_lemmas"):
            lines.append("  - none exposed yet")
        if row.get("failure_diagnosis"):
            lines.append(f"- Failure diagnosis: {row.get('failure_diagnosis', '')}")
        lines.append("- Negative route or failure logic:")
        if row.get("negative_route"):
            lines.append(f"  - {row.get('negative_route', '')}")
        for item in row.get("abort_conditions", [])[:2]:
            lines.append(f"  - {item}")
        if not row.get("negative_route") and not row.get("abort_conditions"):
            lines.append("  - no explicit falsification route surfaced yet")
        lines.append("- Linked supporting hypotheses:")
        for hyp in row.get("linked_hypothesis_rows", [])[:4]:
            if not isinstance(hyp, dict):
                continue
            lines.append(
                f"  - {hyp.get('hypothesis_id', '')} | kind={hyp.get('kind', '')} | "
                f"tier={hyp.get('tier', '')} | score={_safe_float(hyp.get('score', 0.0)):.4f}"
            )
        if not row.get("linked_hypothesis_rows"):
            lines.append("  - no linked hypothesis evidence surfaced")
        lines.append("- Expert actions:")
        for action in row.get("expert_actions", []):
            lines.append(f"  - {action}")
        if not row.get("expert_actions"):
            lines.append("  - no concrete action surfaced")
        lines.append("")
    lines.append("## 5. Top Expert Recommendations")
    lines.append("")
    lines.append("| Rank | Hypothesis | Tier | Score | Potential | Risk | Verdict |")
    lines.append("|---|---|---|---:|---:|---:|---|")
    for idx, row in enumerate(top_rows, start=1):
        scores = row.get("scores", {})
        lines.append(
            "| "
            f"{idx} | {row.get('hypothesis_id', '')} | {row.get('tier', '')} | "
            f"{_safe_float(scores.get('final')):.4f} | {_safe_float(scores.get('potential_raw')):.4f} | "
            f"{_safe_float(scores.get('risk_raw')):.4f} | {row.get('eval_verdict', 'unscored')} |"
        )
    if not top_rows:
        lines.append("| - | - | - | - | - | - | - |")
    lines.append("")
    lines.append("## 6. Detailed Justification Per Recommendation")
    lines.append("")
    if not top_rows:
        lines.append("No hypothesis met the recommendation threshold in this run.")
    for idx, row in enumerate(top_rows, start=1):
        target_id = str(row.get("target_statement_id", "")).strip()
        support_id = str(row.get("support_statement_id", "")).strip()
        target_preview = _statement_preview(statement_index, target_id)
        support_preview = _statement_preview(statement_index, support_id)
        lines.append(f"### {idx}. `{row.get('hypothesis_id', '')}`")
        lines.append("")
        lines.append(f"- Tier: {row.get('tier', '')}")
        lines.append(f"- Kind: `{row.get('kind', '')}`")
        lines.append(f"- Target statement: `{target_id or 'n/a'}`")
        if target_preview:
            lines.append(f"  target preview: {target_preview}")
        lines.append(f"- Support statement: `{support_id or 'n/a'}`")
        if support_preview:
            lines.append(f"  support preview: {support_preview}")
        lines.append("- Why this is high-potential:")
        for reason in row.get("justification", []):
            lines.append(f"  - {reason}")
        lines.append("- Recommended expert actions:")
        for action in row.get("expert_actions", []):
            lines.append(f"  - {action}")
        lines.append("")
    lines.append("## 7. Methodological Interpretation")
    lines.append("")
    lines.append(
        "The report is bridge-first rather than hypothesis-only: it asks which conceptual interfaces are missing, which mathematical objects would close them, "
        "which proof families make those objects actionable, and which negative routes would reveal that the bridge is ill-posed. "
        "Hypotheses remain important, but only insofar as they support or destabilize those bridge objects."
    )
    lines.append("")
    lines.append("## 8. Limitations")
    lines.append("")
    lines.append(
        "This report depends on currently available bridge, conjecture, and proof-sketch artifacts. "
        "If bridge-plan or sketch artifacts are sparse, the conceptual bridge narrative should be read as a disciplined research proposal rather than a settled mathematical diagnosis."
    )
    lines.append("")
    lines.append("## 9. Provenance")
    lines.append("")
    lines.append(
        "This report is generated from typed artifacts (`connection-analysis`, `entrypoints`, `pathways`, `coherence`, "
        "`bridge-plan`, `concept-gap-abstractions`, `hypothesis-evaluation`, `hypothesis-loop`, `revision-loop`, `hardness`, "
        "`strategies`, `proof-sketches`, and `phyp`)."
    )
    if warnings:
        lines.append("")
        lines.append("Warnings:")
        for warning in warnings:
            lines.append(f"- {warning}")
    lines.append("")
    return "\n".join(lines).strip() + "\n"


def _render_tex(
    kb_ref: str,
    top_bridge_rows: list[dict[str, Any]],
    top_rows: list[dict[str, Any]],
    generated_utc: str,
) -> str:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: TeX rendering for publication-oriented export.
    Contribution: Provides a direct paper-ready artifact without requiring additional conversion tooling.
    """

    lines: list[str] = []
    lines.append(r"\documentclass[11pt]{article}")
    lines.append(r"\usepackage[a4paper,margin=1in]{geometry}")
    lines.append(r"\usepackage{booktabs}")
    lines.append(r"\usepackage{longtable}")
    lines.append(r"\usepackage{hyperref}")
    lines.append(r"\title{Expert Hypothesis Recommendation Paper: " + _latex_escape(kb_ref) + "}")
    lines.append(r"\date{" + _latex_escape(generated_utc) + r"}")
    lines.append(r"\begin{document}")
    lines.append(r"\maketitle")
    lines.append(r"\section*{Abstract}")
    lines.append(
        _latex_escape(
            "This paper ranks hypotheses using a generative potential function that balances support, coherence, "
            "explanatory value, structural leverage, strategy leverage, anti-barrier fit, and testability."
        )
    )
    lines.append(r"\section*{Generative Function}")
    lines.append(r"\[")
    lines.append(r"Potential(h) = 0.21S + 0.14C + 0.14E + 0.16L + 0.12G + 0.08A + 0.07T + 0.08N")
    lines.append(r"\]")
    lines.append(r"\[")
    lines.append(r"Risk(h) = 0.45R + 0.22C^- + 0.18B + 0.15U")
    lines.append(r"\]")
    lines.append(r"\[")
    lines.append(r"Score(h) = \mathrm{clip}(Potential(h) \cdot (1 - 0.55 Risk(h)) + 0.05V, 0, 1)")
    lines.append(r"\]")
    lines.append(r"\section*{Main Conceptual Bridges}")
    lines.append(r"\begin{longtable}{p{0.18\linewidth}p{0.17\linewidth}p{0.13\linewidth}p{0.20\linewidth}p{0.20\linewidth}}")
    lines.append(r"\toprule")
    lines.append(r"Bridge & Type & Priority & Consequence & Proof Family \\")
    lines.append(r"\midrule")
    lines.append(r"\endhead")
    if top_bridge_rows:
        for row in top_bridge_rows:
            lines.append(
                f"{_latex_escape(str(row.get('bridge_id', '')))} & "
                f"{_latex_escape(str(row.get('bridge_type', '')))} & "
                f"{_safe_float(row.get('priority', 0.0)):.4f} & "
                f"{_latex_escape(str(row.get('target_consequence_schema', '')))} & "
                f"{_latex_escape(str(row.get('proof_strategy_family', 'n/a')))} \\\\"
            )
    else:
        lines.append(r"No bridge recommendation & -- & -- & -- & -- \\")
    lines.append(r"\bottomrule")
    lines.append(r"\end{longtable}")
    lines.append(r"\section*{Bridge-First Sketch Rationale}")
    if not top_bridge_rows:
        lines.append(_latex_escape("No bridge had enough support to justify a bridge-first proof-sketch synthesis."))
    for idx, row in enumerate(top_bridge_rows, start=1):
        statement_delta = row.get("statement_delta", {}) if isinstance(row.get("statement_delta"), dict) else {}
        lines.append(r"\subsection*{" + _latex_escape(f"{idx}. {row.get('bridge_id', '')}") + "}")
        if str(row.get("route_synopsis", "")).strip():
            lines.append(_latex_escape(str(row.get("route_synopsis", "")).strip()))
        lines.append(r"\begin{itemize}")
        lines.append(r"\item " + _latex_escape(f"Type: {row.get('bridge_type', '')}"))
        lines.append(r"\item " + _latex_escape(f"Abstraction: {row.get('abstraction_label', '')}"))
        lines.append(r"\item " + _latex_escape(f"Carrier: {row.get('carrier_kind', '')}"))
        lines.append(r"\item " + _latex_escape(f"Typing status: {row.get('typing_status', '')}"))
        lines.append(r"\item " + _latex_escape(f"Invariant: {row.get('preserved_invariant', '')}"))
        lines.append(r"\item " + _latex_escape(f"Consequence: {row.get('target_consequence_schema', '')}"))
        lines.append(r"\item " + _latex_escape(f"Proof family: {row.get('proof_strategy_family', '')}"))
        for reason in row.get("justification", [])[:5]:
            lines.append(r"\item " + _latex_escape(reason))
        lines.append(r"\end{itemize}")
        lines.append(r"\paragraph{Source Theorem}")
        lines.append(_latex_escape(str(row.get("source_excerpt", "")).strip() or "Source theorem excerpt unavailable."))
        lines.append(r"\paragraph{Target Theorem}")
        lines.append(_latex_escape(str(row.get("target_excerpt", "")).strip() or "Target theorem excerpt unavailable."))
        lines.append(r"\paragraph{Mathematical Delta}")
        lines.append(r"\begin{itemize}")
        lines.append(r"\item " + _latex_escape(f"Model shift: {statement_delta.get('model_shift', '') or 'not typed'}"))
        lines.append(r"\item " + _latex_escape(f"Threshold shift: {statement_delta.get('threshold_shift', '') or 'not typed'}"))
        lines.append(r"\item " + _latex_escape(f"Consequence shift: {statement_delta.get('consequence_shift', '') or 'not typed'}"))
        lines.append(r"\item " + _latex_escape(f"Missing route lemma: {row.get('missing_route_lemma', '') or 'not isolated'}"))
        lines.append(r"\end{itemize}")
        lines.append(r"\paragraph{Candidate Bridge Object}")
        lines.append(_latex_escape(str(row.get("bridge_definition", "")).strip() or "No bridge definition surfaced yet."))
        if row.get("mathematical_assumptions"):
            lines.append(r"\paragraph{Admissibility Conditions}")
            lines.append(r"\begin{itemize}")
            for item in row.get("mathematical_assumptions", [])[:4]:
                lines.append(r"\item " + _latex_escape(str(item)))
            lines.append(r"\end{itemize}")
        lines.append(r"\paragraph{Lemma Chain}")
        lines.append(r"\begin{itemize}")
        for item in row.get("candidate_lemmas", [])[:4]:
            lines.append(r"\item " + _latex_escape(str(item)))
        if not row.get("candidate_lemmas"):
            lines.append(r"\item " + _latex_escape("No explicit candidate lemmas surfaced yet."))
        lines.append(r"\end{itemize}")
        lines.append(r"\paragraph{Proof obligations}")
        lines.append(r"\begin{itemize}")
        for item in row.get("proof_obligations", [])[:4]:
            lines.append(r"\item " + _latex_escape(str(item)))
        if not row.get("proof_obligations"):
            lines.append(r"\item " + _latex_escape("No explicit obligations surfaced yet."))
        lines.append(r"\end{itemize}")
        lines.append(r"\paragraph{Failure Diagnosis}")
        lines.append(
            _latex_escape(
                str(row.get("failure_diagnosis", "")).strip()
                or "No explicit failure diagnosis surfaced yet."
            )
        )
        lines.append(r"\paragraph{Negative route}")
        lines.append(
            _latex_escape(
                str(row.get("negative_route", "")).strip()
                or (row.get("abort_conditions", [None])[0] if row.get("abort_conditions") else "No explicit negative route surfaced yet.")
            )
        )
    lines.append(r"\section*{Top Recommendations}")
    lines.append(r"\begin{longtable}{p{0.28\linewidth}p{0.20\linewidth}p{0.13\linewidth}p{0.13\linewidth}p{0.13\linewidth}}")
    lines.append(r"\toprule")
    lines.append(r"Hypothesis & Tier & Score & Potential & Risk \\")
    lines.append(r"\midrule")
    lines.append(r"\endhead")
    if top_rows:
        for row in top_rows:
            scores = row.get("scores", {})
            lines.append(
                f"{_latex_escape(str(row.get('hypothesis_id', '')))} & "
                f"{_latex_escape(str(row.get('tier', '')))} & "
                f"{_safe_float(scores.get('final')):.4f} & "
                f"{_safe_float(scores.get('potential_raw')):.4f} & "
                f"{_safe_float(scores.get('risk_raw')):.4f} \\\\"
            )
    else:
        lines.append(r"No recommendation & -- & -- & -- & -- \\")
    lines.append(r"\bottomrule")
    lines.append(r"\end{longtable}")
    lines.append(r"\section*{Detailed Justification}")
    if not top_rows:
        lines.append(_latex_escape("No hypothesis met the recommendation threshold in this run."))
    for idx, row in enumerate(top_rows, start=1):
        lines.append(r"\subsection*{" + _latex_escape(f"{idx}. {row.get('hypothesis_id', '')}") + "}")
        lines.append(r"\begin{itemize}")
        lines.append(r"\item " + _latex_escape(f"Tier: {row.get('tier', '')}"))
        lines.append(r"\item " + _latex_escape(f"Kind: {row.get('kind', '')}"))
        lines.append(r"\item " + _latex_escape(f"Target: {row.get('target_statement_id', 'n/a')}"))
        lines.append(r"\item " + _latex_escape(f"Support: {row.get('support_statement_id', 'n/a')}"))
        for reason in row.get("justification", []):
            lines.append(r"\item " + _latex_escape(reason))
        lines.append(r"\end{itemize}")
        lines.append(r"\paragraph{Recommended Expert Actions}")
        lines.append(r"\begin{itemize}")
        for action in row.get("expert_actions", []):
            lines.append(r"\item " + _latex_escape(action))
        lines.append(r"\end{itemize}")
    lines.append(r"\end{document}")
    return "\n".join(lines) + "\n"


def _build_report(
    kb_ref: str,
    phyp: dict[str, Any],
    hypothesis_eval: dict[str, Any],
    coherence: dict[str, Any],
    analysis: dict[str, Any],
    entrypoints: dict[str, Any],
    pathways: dict[str, Any],
    bridges: dict[str, Any],
    conjectures: dict[str, Any],
    hardness: dict[str, Any],
    revision: dict[str, Any],
    strategies: dict[str, Any],
    proof_sketches: dict[str, Any],
    statement_index: dict[str, dict[str, Any]],
    top_k: int,
    min_score: float,
    warnings: list[str],
) -> dict[str, Any]:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: Main stage-level composition across all final analysis artifacts.
    Contribution: Produces a single integrated, expert-facing recommendation object and paper payload.
    """

    hyp_eval_idx = _hypothesis_eval_index(hypothesis_eval)
    coh_idx = _coherence_index(coherence)
    hypothesis_eval_meta = hypothesis_eval.get("metadata", {}) if isinstance(hypothesis_eval.get("metadata"), dict) else {}
    evidence_count = max(0, int(hypothesis_eval_meta.get("evidence_count", 0) or 0))

    entry_scores = _normalize_map(_entrypoint_statement_scores(entrypoints))
    intervention_scores = _normalize_map(_intervention_statement_scores(analysis))
    pathway_hyp_raw, pathway_stmt_raw = _pathway_signals(pathways)
    pathway_hyp_scores = _normalize_map(pathway_hyp_raw)
    pathway_stmt_scores = _normalize_map(pathway_stmt_raw)
    strategy_hyp_raw, strategy_hyp_fertility, strategy_ids_by_hyp, _ = _strategy_signals(strategies, proof_sketches)
    strategy_hyp_scores = _normalize_map(strategy_hyp_raw)
    revision_targets = _revision_targets(revision)
    anti_barrier_families, global_barrier_pressure = _hardness_signals(hardness)

    rows: list[dict[str, Any]] = []
    for hyp in phyp.get("hypotheses", []) if isinstance(phyp.get("hypotheses"), list) else []:
        if not isinstance(hyp, dict):
            continue
        hid = str(hyp.get("id", "")).strip()
        if not hid:
            continue
        row = _hypothesis_payload_to_row(
            hyp=hyp,
            hyp_eval_row=hyp_eval_idx.get(hid, {}),
            coh_row=coh_idx.get(hid, {}),
            entry_scores=entry_scores,
            intervention_scores=intervention_scores,
            pathway_hyp_scores=pathway_hyp_scores,
            pathway_stmt_scores=pathway_stmt_scores,
            strategy_hyp_scores=strategy_hyp_scores,
            strategy_hyp_fertility=strategy_hyp_fertility,
            strategy_ids_by_hyp=strategy_ids_by_hyp,
            revision_targets=revision_targets,
            anti_barrier_families=anti_barrier_families,
            global_barrier_pressure=global_barrier_pressure,
        )
        row["tier"] = _recommendation_tier(
            score=_safe_float(row.get("scores", {}).get("final", 0.0)),
            risk=_safe_float(row.get("scores", {}).get("risk_raw", 0.0)),
            min_score=min_score,
        )
        rows.append(row)

    rows.sort(key=lambda item: _safe_float(item.get("scores", {}).get("final", 0.0)), reverse=True)
    top_rows = [row for row in rows if _safe_float(row.get("scores", {}).get("final", 0.0)) >= min_score][: max(1, top_k)]
    bridge_rows, top_bridge_rows = _bridge_portfolio(
        bridges=bridges,
        conjectures=conjectures,
        proof_sketches=proof_sketches,
        hypothesis_rows=rows,
        statement_index=statement_index,
        evidence_count=evidence_count,
        top_k=max(1, min(top_k, 6)),
    )

    generated_utc = dt.datetime.now(dt.UTC).isoformat()
    markdown = _render_markdown(
        kb_ref=kb_ref,
        rows=rows,
        top_rows=top_rows,
        bridge_rows=bridge_rows,
        top_bridge_rows=top_bridge_rows,
        statement_index=statement_index,
        generated_utc=generated_utc,
        warnings=warnings,
    )
    tex = _render_tex(kb_ref=kb_ref, top_bridge_rows=top_bridge_rows, top_rows=top_rows, generated_utc=generated_utc)

    return {
        "metadata": {
            "kb_ref": kb_ref,
            "generated_utc": generated_utc,
            "hypothesis_count": len(rows),
            "recommended_count": len(top_rows),
            "bridge_count": len(bridge_rows),
            "recommended_bridge_count": len(top_bridge_rows),
            "top_k": top_k,
            "min_score": min_score,
            "warnings": warnings,
        },
        "generative_function": {
            "name": "expert_hypothesis_potential_function",
            "description": (
                "Transparent weighted scoring model combining support, coherence, explanatory power, structural leverage, "
                "strategy leverage, anti-barrier alignment, testability, novelty, and revision pressure; "
                "with explicit risk penalties."
            ),
            "potential_weights": GEN_FUNC_WEIGHTS,
            "risk_weights": GEN_RISK_WEIGHTS,
            "formula": {
                "potential": "0.21*S + 0.14*C + 0.14*E + 0.16*L + 0.12*G + 0.08*A + 0.07*T + 0.08*N",
                "risk": "0.45*R + 0.22*C_neg + 0.18*B + 0.15*U",
                "final": "clip(Potential*(1 - 0.55*Risk) + 0.05*V, 0, 1)",
            },
            "signal_glossary": {
                "S": "support signal",
                "C": "positive coherence signal",
                "E": "explanatory signal",
                "L": "structural leverage",
                "G": "strategy leverage",
                "A": "anti-barrier alignment",
                "T": "testability",
                "N": "novelty signal",
                "R": "refutation risk",
                "C_neg": "negative coherence risk",
                "B": "barrier pressure risk",
                "U": "uncertainty risk",
                "V": "revision-priority bonus",
            },
        },
        "bridge_selection_function": {
            "name": "expert_bridge_priority_function",
            "description": (
                "Bridge-first prioritization model combining effective bridge-program strength, conjecture maturity, proof-sketch quality, "
                "verdict-aware linked hypothesis support, mathematical specificity, evidence pressure, falsifiability, sketch operationalization, "
                "and search-space novelty."
            ),
            "weights": BRIDGE_FUNC_WEIGHTS,
            "formula": "0.16*B + 0.12*C_b + 0.14*P_b + 0.10*H_b + 0.18*M_b + 0.14*E_b + 0.08*F_b + 0.05*O_b + 0.03*N_b - BarrierPenalty(b)",
            "signal_glossary": {
                "B": "effective bridge-program strength",
                "C_b": "conjecture maturity",
                "P_b": "proof-sketch strength",
                "H_b": "verdict-aware linked hypothesis support",
                "M_b": "mathematical specificity",
                "E_b": "evidence signal",
                "F_b": "falsifiability signal",
                "O_b": "sketch operationalization",
                "N_b": "search-space novelty",
            },
        },
        "bridge_portfolio": bridge_rows,
        "recommended_bridges": top_bridge_rows,
        "hypothesis_scores": rows,
        "recommended_hypotheses": top_rows,
        "paper_markdown": markdown,
        "paper_tex": tex,
    }


def main() -> int:
    """
    Relevance: Operates within the expert paper synthesis layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds parsing, computation, and artifact emission into a reproducible script execution.
    """

    logger = ReasoningLogger("kb-expert-paper-generator")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--kb", required=True, help="Path to KB markdown file.")
    ap.add_argument(
        "--kb-ref",
        default="",
        help="Optional canonical KB reference (must match front matter kb_id when present).",
    )
    ap.add_argument(
        "--artifacts-dir",
        default="",
        help="Optional explicit artifacts directory. Must match canonical artifacts/<kb-ref>.",
    )
    ap.add_argument(
        "--phyp",
        default="",
        help="Optional path to phyp YAML. Defaults to phyp/<kb-ref>.proof-hypotheses.yaml.",
    )
    ap.add_argument("--top-k", type=int, default=8, help="Maximum number of expert recommendations.")
    ap.add_argument(
        "--min-score",
        type=float,
        default=0.52,
        help="Minimum final score threshold for recommendation inclusion.",
    )
    ap.add_argument(
        "--output-json",
        default="",
        help="Output JSON path (default: artifacts/<kb-ref>/expert-hypothesis-paper.json).",
    )
    ap.add_argument(
        "--output-md",
        default="",
        help="Output Markdown path (default: artifacts/<kb-ref>/expert-hypothesis-paper.md).",
    )
    ap.add_argument(
        "--output-tex",
        default="",
        help="Output TeX path (default: artifacts/<kb-ref>/expert-hypothesis-paper.tex).",
    )
    args = ap.parse_args()

    repo = Path(__file__).resolve().parents[4]
    kb = Path(args.kb)
    if not kb.exists():
        log_path = logger.finalize("error", summary=f"KB not found: {kb}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] KB not found: {kb}")

    try:
        kb_ctx = resolve_kb_reference(kb, explicit_kb_ref=args.kb_ref)
    except ValueError as exc:
        log_path = logger.finalize("error", summary=str(exc))
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] {exc}")
    kb_ref = str(kb_ctx.get("kb_ref", "")).strip()
    if not kb_ref:
        log_path = logger.finalize("error", summary="Unable to resolve KB reference.")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit("[ERROR] Unable to resolve KB reference.")

    expected_artifacts_dir = canonical_artifacts_dir(repo, kb_ref)
    if args.artifacts_dir:
        requested = Path(args.artifacts_dir)
        if not requested.is_absolute():
            requested = (repo / requested).resolve()
        if requested != expected_artifacts_dir:
            log_path = logger.finalize(
                "error",
                summary=(
                    "Non-canonical artifacts directory rejected. "
                    f"expected={expected_artifacts_dir} requested={requested}"
                ),
            )
            print(f"[LOG] {log_path}", file=sys.stderr)
            raise SystemExit(
                "[ERROR] artifacts are associated with the reference KB name. "
                f"Use canonical path: {expected_artifacts_dir}"
            )
    artifacts_dir = expected_artifacts_dir
    phyp_path = Path(args.phyp) if args.phyp else repo / "phyp" / f"{kb_ref}.proof-hypotheses.yaml"

    output_json = Path(args.output_json) if args.output_json else artifacts_dir / "expert-hypothesis-paper.json"
    output_md = Path(args.output_md) if args.output_md else artifacts_dir / "expert-hypothesis-paper.md"
    output_tex = Path(args.output_tex) if args.output_tex else artifacts_dir / "expert-hypothesis-paper.tex"

    logger.step(
        "Parsed expert-paper arguments",
        "\n".join(
            [
                f"kb={kb}",
                f"kb_ref={kb_ref}",
                f"artifacts_dir={artifacts_dir}",
                f"phyp={phyp_path}",
                f"top_k={max(1, args.top_k)}",
                f"min_score={_clamp01(args.min_score)}",
                f"output_json={output_json}",
                f"output_md={output_md}",
                f"output_tex={output_tex}",
            ]
        ),
    )

    if not phyp_path.exists():
        log_path = logger.finalize("error", summary=f"Missing required phyp file: {phyp_path}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Missing required phyp file: {phyp_path}")

    warnings: list[str] = []

    phyp_payload = _load_yaml(phyp_path)
    try:
        phyp = validate_phyp(phyp_payload, name="phyp")
    except Exception as exc:
        log_path = logger.finalize("error", summary=f"Invalid phyp payload: {exc}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Invalid phyp payload: {exc}")

    analysis = _load_optional_validated_json(
        artifacts_dir / "connection-analysis.json",
        validate_connection_analysis,
        warnings,
        "analysis",
    )
    entrypoints = _load_optional_validated_json(
        artifacts_dir / "entrypoints.json",
        validate_entrypoints,
        warnings,
        "entrypoints",
    )
    pathways = _load_optional_validated_json(
        artifacts_dir / "entrypoint-pathways.json",
        validate_pathways,
        warnings,
        "pathways",
    )
    coherence = _load_optional_validated_json(
        artifacts_dir / "coherence-report.json",
        validate_coherence_report,
        warnings,
        "coherence",
    )
    bridges = _load_optional_validated_json(
        artifacts_dir / "bridge-plan.json",
        validate_bridges,
        warnings,
        "bridges",
    )
    conjectures = _load_optional_validated_json(
        artifacts_dir / "concept-gap-abstractions.json",
        validate_conjecture_report,
        warnings,
        "conjectures",
    )
    strategies = _load_optional_validated_json(
        artifacts_dir / "proof-strategies.json",
        validate_strategy_report,
        warnings,
        "strategies",
    )
    proof_sketches = _load_optional_validated_json(
        artifacts_dir / "proof-sketches.json",
        validate_proof_sketch_report,
        warnings,
        "proof_sketches",
    )
    hardness = _load_json(artifacts_dir / "epistemic-hardness.json")
    hypothesis_eval = _load_json(artifacts_dir / "hypothesis-evaluation.json")
    hypothesis_loop = _load_json(artifacts_dir / "hypothesis-refutation-loop.json")
    revision = _load_json(artifacts_dir / "revision-loop.json")
    dynamics = _load_json(artifacts_dir / "reasoning-dynamics.json")
    statement_index = _statement_index_from_kb(kb)

    logger.step(
        "Loaded expert-paper inputs",
        "\n".join(
            [
                f"hypotheses={len(phyp.get('hypotheses', []))}",
                f"analysis_loaded={bool(analysis)}",
                f"entrypoints_loaded={bool(entrypoints)}",
                f"pathways_loaded={bool(pathways)}",
                f"coherence_loaded={bool(coherence)}",
                f"bridges_loaded={bool(bridges)}",
                f"conjectures_loaded={bool(conjectures)}",
                f"strategies_loaded={bool(strategies)}",
                f"proof_sketches_loaded={bool(proof_sketches)}",
                f"hypothesis_eval_loaded={bool(hypothesis_eval)}",
                f"hypothesis_loop_loaded={bool(hypothesis_loop)}",
                f"revision_loaded={bool(revision)}",
                f"hardness_loaded={bool(hardness)}",
                f"dynamics_loaded={bool(dynamics)}",
                f"warnings={len(warnings)}",
            ]
        ),
    )

    report = _build_report(
        kb_ref=kb_ref,
        phyp=phyp,
        hypothesis_eval=hypothesis_eval,
        coherence=coherence,
        analysis=analysis,
        entrypoints=entrypoints,
        pathways=pathways,
        bridges=bridges,
        conjectures=conjectures,
        hardness=hardness,
        revision=revision,
        strategies=strategies,
        proof_sketches=proof_sketches,
        statement_index=statement_index,
        top_k=max(1, args.top_k),
        min_score=_clamp01(args.min_score),
        warnings=warnings,
    )

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_tex.parent.mkdir(parents=True, exist_ok=True)

    output_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
    output_md.write_text(str(report.get("paper_markdown", "")), encoding="utf-8")
    output_tex.write_text(str(report.get("paper_tex", "")), encoding="utf-8")

    logger.add_output("expert_paper_json", output_json)
    logger.add_output("expert_paper_md", output_md)
    logger.add_output("expert_paper_tex", output_tex)
    logger.step(
        "Built expert recommendations",
        "\n".join(
            [
                f"bridge_recommended_count={len(report.get('recommended_bridges', []))}",
                f"recommended_count={len(report.get('recommended_hypotheses', []))}",
                "generative_function=expert_hypothesis_potential_function",
                "bridge_selection_function=expert_bridge_priority_function",
            ]
        ),
    )

    log_path = logger.finalize(
        "success",
        summary=(
            f"Generated expert paper with {len(report.get('recommended_bridges', []))} "
            f"main bridges and {len(report.get('recommended_hypotheses', []))} recommended hypotheses."
        ),
    )
    print(f"[OK] Wrote JSON: {output_json}")
    print(f"[OK] Wrote Markdown paper: {output_md}")
    print(f"[OK] Wrote LaTeX paper: {output_tex}")
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
