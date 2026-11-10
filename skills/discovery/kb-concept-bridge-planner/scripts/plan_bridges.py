# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""Systematically plan bridges between essential concepts from intermediate artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from reasoning_log import ReasoningLogger
from contracts import validate_connection_analysis
from contracts import validate_coherence_report
from contracts import validate_entrypoints
from contracts import validate_pathways
from contracts import validate_phyp
from search_space_tree import build_route_dimensions
from search_space_tree import compute_revisit_signal
from search_space_tree import load_search_space_state
from search_space_tree import route_content_fingerprint
from search_space_tree import route_signature
from statement_text import humanize_schema_label
from statement_text import load_statement_index
from statement_text import statement_excerpt
from statement_text import statement_focus

ID_RE = re.compile(r"`(st\.[A-Za-z0-9._-]+)`")


def _phase_map(concept_path: Path) -> dict[str, str]:
    """
    Relevance: Operates within the concept bridge planning layer.
    Concept: Typed classification used to guide scoring and prioritization.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    current = "Unspecified"
    out: dict[str, str] = {}
    for line in concept_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            current = line.replace("## ", "", 1).strip()
            continue
        for sid in ID_RE.findall(line):
            out[sid] = current
    return out


def _bridge_type(
    from_id: str,
    to_id: str,
    from_phase: str,
    to_phase: str,
    from_bridge_roles: list[str] | None = None,
    to_bridge_roles: list[str] | None = None,
) -> str:
    """
    Relevance: Operates within the concept bridge planning layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    roles = {str(role).strip().lower() for role in (from_bridge_roles or []) + (to_bridge_roles or []) if str(role).strip()}
    if any(role.startswith("transfer-matrix-to-gap") for role in roles):
        return "transfer-matrix-to-gap bridge"
    if any(role.startswith("correlator-decay-to-gap") for role in roles):
        return "correlator-decay-to-gap bridge"
    if any(role.startswith("os-to-wightman-to-gap") for role in roles):
        return "OS-to-Wightman-to-gap bridge"
    if any(role.startswith("os-reconstruction") or role.startswith("os-to-wightman") for role in roles):
        return "OS-reconstruction bridge"
    if any(role.startswith("continuum-limit") for role in roles):
        return "continuum-limit bridge"

    blob = " ".join([from_id.lower(), to_id.lower(), from_phase.lower(), to_phase.lower()])
    if any(token in blob for token in ("os-to-wightman", "wightman-to-gap")):
        return "OS-to-Wightman-to-gap bridge"
    if any(token in blob for token in ("osterwalder", "schrader", "os-", "wightman", "reflection-positivity", "reconstruction")):
        return "OS-reconstruction bridge"
    if any(token in blob for token in ("transfer-matrix", "reflection-positive-transfer")):
        return "transfer-matrix-to-gap bridge"
    if any(token in blob for token in ("correlator-decay", "exponential decay", "schwinger-function-decay")):
        return "correlator-decay-to-gap bridge"
    if any(token in blob for token in ("mass-gap", "transfer-matrix", "correlator-decay", "spectral-gap", "hamiltonian")):
        return "mass-gap transfer bridge"
    if any(token in blob for token in ("continuum-limit", "cutoff-removal", "ultraviolet", "renormalization-group", "lattice")):
        return "continuum-limit bridge"
    if "barrier" in blob:
        return "barrier-aware transfer bridge"
    if "magnification" in blob or "meta-complexity" in blob or "mcsp" in blob:
        return "magnification bridge"
    if "pit" in blob or "derandom" in blob or "pseudorandom" in blob:
        return "randomness-hardness bridge"
    if "proof" in blob or "frege" in blob or "resolution" in blob or "ips" in blob:
        return "proof-complexity bridge"
    if "communication" in blob or "lifting" in blob:
        return "lifting bridge"
    return "structural support bridge"


def _tier(score: float) -> str:
    """
    Relevance: Operates within the concept bridge planning layer.
    Concept: Typed classification used to guide scoring and prioritization.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if score >= 0.60:
        return "A"
    if score >= 0.45:
        return "B"
    return "C"


def _commitment_score(row: dict[str, Any]) -> float:
    """
    Relevance: Operates within the concept bridge planning layer.
    Concept: Quantitative preference for bridge programs that carry explicit inferential commitments.
    Contribution: Biases planning toward theorem-level bridges instead of generic associative links.
    """

    score = 0.0
    antecedent = str(row.get("support_antecedent_schema", "")).strip()
    consequence = str(row.get("target_consequence_schema", "")).strip()
    invariant = str(row.get("preserved_invariant", "")).strip()
    barrier = str(row.get("barrier_scope", "")).strip().lower()
    basis = row.get("invariant_basis", [])
    if antecedent and antecedent != "unconditional":
        score += 0.25
    if consequence and consequence != "statement-conclusion":
        score += 0.25
    if invariant:
        score += 0.25
    if barrier and barrier != "none":
        score += 0.15
    if isinstance(basis, list) and any(str(x).strip() for x in basis):
        score += 0.10
    return min(1.0, score)


def _as_str_list(value: Any, limit: int = 6) -> list[str]:
    """
    Relevance: Operates within the concept bridge planning layer.
    Concept: Lightweight normalization of typed profile fields into ordered symbolic lists.
    Contribution: Keeps mathematical-program rendering attached to profile content rather than raw payload shapes.
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
        if len(out) >= max(1, limit):
            break
    return out


def _regime_summary(
    statement_id: str,
    phase: str,
    profile: dict[str, Any],
    *,
    claim_focus: str = "",
) -> str:
    """
    Relevance: Operates within the concept bridge planning layer.
    Concept: Compact mathematical description of the source or target regime attached to a bridge endpoint.
    Contribution: Gives experts an inspectable statement of where the bridge is supposed to live.
    """

    problems = _as_str_list(profile.get("core_problems"))
    models = _as_str_list(profile.get("model_signatures"))
    raw_claims = _as_str_list(profile.get("claim_signatures")) or _as_str_list(profile.get("consequence_signatures"))
    claims: list[str] = []
    if str(claim_focus).strip():
        claims.append(str(claim_focus).strip())
    for claim in raw_claims:
        humanized = humanize_schema_label(claim)
        if humanized and humanized not in claims:
            claims.append(humanized)
    parts: list[str] = []
    if phase and phase != "Unspecified":
        parts.append(phase)
    if problems:
        parts.append("problems " + ", ".join(problems[:2]))
    if models:
        parts.append("models " + ", ".join(models[:2]))
    if claims:
        parts.append("claims " + ", ".join(claims[:2]))
    if not parts:
        parts.append("untyped mathematical regime")
    summary = "; ".join(parts)
    return f"{statement_id} ({summary})" if statement_id else summary


def _primary_signature(profile: dict[str, Any], *keys: str) -> str:
    """
    Relevance: Operates within the concept bridge planning layer.
    Concept: Selection of the most informative typed signature from a statement profile.
    Contribution: Keeps statement-delta summaries anchored on concrete theorem content rather than arbitrary field order.
    """

    for key in keys:
        values = _as_str_list(profile.get(key))
        if values:
            return values[0]
    return ""


def _threshold_signal(*values: Any) -> str:
    """
    Relevance: Operates within the concept bridge planning layer.
    Concept: Lightweight detection of threshold/strength regimes from typed signatures.
    Contribution: Makes source-to-target strengthening explicit in bridge summaries without requiring full theorem parsing.
    """

    blob = " ".join(str(value) for value in values if str(value).strip()).lower()
    if any(token in blob for token in ("not-in", "separation", "collapse", "major-separation")):
        return "major separation consequence"
    if "exponential" in blob:
        return "exponential lower bound"
    if "superpolynomial" in blob:
        return "superpolynomial lower bound"
    if any(token in blob for token in ("near-threshold", "barely", "superlinear", "n^1", "n^{1", "slightly beyond")):
        return "near-threshold lower bound"
    if "lower-bound" in blob:
        return "generic lower-bound regime"
    return "threshold regime not yet typed"


def _typed_object_expectation(
    bridge_type: str,
    *,
    anchor: str,
    source_problem: str,
    target_problem: str,
    source_threshold: str,
    target_threshold: str,
) -> tuple[str, str]:
    """
    Relevance: Operates within the concept bridge planning layer.
    Concept: Typed prediction of the missing bridge object family required by a route.
    Contribution: Prevents downstream stages from falling back to untyped placeholder nouns when the route already suggests an object class.
    """

    bridge_text = str(bridge_type).strip().lower()
    focus = anchor or source_problem or target_problem or "bridge"
    focus_lower = focus.lower()
    if "magnification" in bridge_text:
        if "mcsp" in focus_lower:
            if "near-threshold" in " ".join((source_threshold, target_threshold)).lower():
                return "threshold-sensitive MCSP instance family", "typed"
            return "MCSP witness family", "typed"
        return "hardness-magnification witness family", "typed"
    if "randomness-hardness" in bridge_text:
        return "hitting-set or pseudorandom-generator family", "typed"
    if "proof-complexity" in bridge_text:
        return "proof certificate family or monotone proof measure", "typed"
    if "lifting" in bridge_text:
        return "lifting gadget or communication map", "typed"
    if any(token in bridge_text for token in ("transfer", "support", "structural")):
        return "witness-preserving transport map", "typed"
    if focus and focus != "bridge":
        return f"{focus} witness family or transport map", "typed"
    return "underspecified bridge witness", "underspecified"


def _statement_delta(
    *,
    src: str,
    dst: str,
    from_profile: dict[str, Any],
    to_profile: dict[str, Any],
    bridge_type: str,
    commitment: dict[str, Any],
    concept_evidence: list[str],
    evidence_terms: list[str],
    source_statement: dict[str, Any] | None = None,
    target_statement: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Relevance: Operates within the concept bridge planning layer.
    Concept: Explicit contract describing the mathematical shift from source statement to target statement.
    Contribution: Gives downstream stages a content-first description of what new object or lemma must be inserted on the route.
    """

    source_problem = _primary_signature(from_profile, "core_problems")
    target_problem = _primary_signature(to_profile, "core_problems")
    source_model = _primary_signature(from_profile, "model_signatures")
    target_model = _primary_signature(to_profile, "model_signatures")
    source_schema = (
        _primary_signature(from_profile, "claim_signatures", "consequence_signatures", "antecedent_signatures")
        or str(commitment.get("support_antecedent_schema", "")).strip()
    )
    target_schema = (
        _primary_signature(to_profile, "consequence_signatures", "claim_signatures")
        or str(commitment.get("target_consequence_schema", "")).strip()
    )
    antecedent = str(commitment.get("support_antecedent_schema", "")).strip() or source_schema or "source-side theorem schema"
    consequence = str(commitment.get("target_consequence_schema", "")).strip() or target_schema or "target consequence"
    source_claim = statement_focus(source_statement or {}, fallback=source_schema, role="source") or source_schema
    target_claim = statement_focus(target_statement or {}, fallback=target_schema, role="target") or target_schema
    source_excerpt = statement_excerpt(source_statement or {}, limit=360)
    target_excerpt = statement_excerpt(target_statement or {}, limit=360)
    invariant = str(commitment.get("preserved_invariant", "")).strip() or "bridge interface"
    anchor = _primary_signature(
        {
            "focus": [
                source_claim,
                target_claim,
                *(_as_str_list(from_profile.get("core_problems"))),
                *(_as_str_list(to_profile.get("core_problems"))),
                *(_as_str_list(commitment.get("invariant_basis"))),
                *[str(item).strip() for item in concept_evidence if str(item).strip()],
                *[str(item).strip() for item in evidence_terms if str(item).strip()],
            ]
        },
        "focus",
    )
    source_threshold = _threshold_signal(
        antecedent,
        source_claim,
        *(_as_str_list(from_profile.get("claim_signatures"))),
        *(_as_str_list(from_profile.get("consequence_signatures"))),
        *evidence_terms,
        *concept_evidence,
    )
    target_threshold = _threshold_signal(
        consequence,
        target_claim,
        *(_as_str_list(to_profile.get("claim_signatures"))),
        *(_as_str_list(to_profile.get("consequence_signatures"))),
        *evidence_terms,
        *concept_evidence,
    )
    typed_object, typing_status = _typed_object_expectation(
        bridge_type,
        anchor=anchor,
        source_problem=source_problem,
        target_problem=target_problem,
        source_threshold=source_threshold,
        target_threshold=target_threshold,
    )
    if source_model and target_model and source_model != target_model:
        model_shift = f"{source_model} -> {target_model}"
    elif source_model or target_model:
        model_shift = source_model or target_model
    else:
        model_shift = "model shift not yet typed"
    if source_threshold != target_threshold:
        threshold_shift = f"{source_threshold} -> {target_threshold}"
    else:
        threshold_shift = source_threshold
    consequence_shift = (
        f"upgrade `{source_claim or antecedent}` into `{target_claim or consequence}`"
        if (source_claim or antecedent) and (target_claim or consequence) and (source_claim or antecedent) != (target_claim or consequence)
        else f"stabilize the payoff `{target_claim or consequence}`"
    )
    if source_model and target_model and source_model != target_model:
        missing_lemma = (
            f"Prove that a {typed_object} preserves `{invariant}` while transporting the route from the {source_model} regime "
            f"to the {target_model} regime strongly enough to derive `{target_claim or consequence}`."
        )
    elif source_threshold != target_threshold:
        missing_lemma = (
            f"Prove that a {typed_object} upgrades the route from {source_threshold} to {target_threshold} "
            f"without losing `{invariant}`."
        )
    else:
        missing_lemma = (
            f"Prove that a {typed_object} turns `{source_claim or antecedent}` into `{target_claim or consequence}` while preserving `{invariant}`."
        )
    route_synopsis = (
        f"Move from `{src}`"
        + (f" on problem `{source_problem}`" if source_problem else "")
        + (f" in model `{source_model}`" if source_model else "")
        + f" using `{source_claim or antecedent}` toward `{dst}`"
        + (f" on problem `{target_problem}`" if target_problem and target_problem != source_problem else "")
        + (f" in model `{target_model}`" if target_model else "")
        + f" to obtain `{target_claim or consequence}`."
    )
    return {
        "source_problem_family": source_problem or "unspecified",
        "target_problem_family": target_problem or "unspecified",
        "source_model": source_model or "unspecified",
        "target_model": target_model or "unspecified",
        "source_claim_focus": source_claim or antecedent or "source theorem content not yet typed",
        "target_claim_focus": target_claim or consequence or "target theorem content not yet typed",
        "source_theorem_excerpt": source_excerpt,
        "target_theorem_excerpt": target_excerpt,
        "model_shift": model_shift,
        "threshold_shift": threshold_shift,
        "consequence_shift": consequence_shift,
        "typed_object_expectation": typed_object,
        "typing_status": typing_status,
        "missing_witness_or_transport": missing_lemma,
        "route_synopsis": route_synopsis,
    }


def _mathematical_program(
    *,
    src: str,
    dst: str,
    src_phase: str,
    dst_phase: str,
    from_profile: dict[str, Any],
    to_profile: dict[str, Any],
    bridge_type: str,
    commitment: dict[str, Any],
    concept_evidence: list[str],
    evidence_terms: list[str],
    statement_delta: dict[str, Any],
) -> dict[str, Any]:
    """
    Relevance: Operates within the concept bridge planning layer.
    Concept: Expert-facing theorem-level description of what the bridge is trying to establish.
    Contribution: Turns a ranked bridge candidate into inspectable mathematical content instead of an execution protocol alone.
    """

    antecedent = str(commitment.get("support_antecedent_schema", "")).strip() or "source-side theorem schema"
    consequence = str(commitment.get("target_consequence_schema", "")).strip() or "target consequence"
    invariant = str(commitment.get("preserved_invariant", "")).strip() or "bridge interface"
    barrier = str(commitment.get("barrier_scope", "")).strip() or "none"
    invariant_basis = _as_str_list(commitment.get("invariant_basis"))
    source_regime = _regime_summary(
        src,
        src_phase,
        from_profile,
        claim_focus=str(statement_delta.get("source_claim_focus", "")).strip(),
    )
    target_regime = _regime_summary(
        dst,
        dst_phase,
        to_profile,
        claim_focus=str(statement_delta.get("target_claim_focus", "")).strip(),
    )
    object_focus = _as_str_list([*concept_evidence, *evidence_terms, *invariant_basis], limit=5)
    focus_text = ", ".join(object_focus[:3]) if object_focus else bridge_type
    typed_object = str(statement_delta.get("typed_object_expectation", "")).strip() or f"{bridge_type} object"
    missing_lemma = str(statement_delta.get("missing_witness_or_transport", "")).strip()
    bridge_question = (
        f"What explicit {typed_object} built around {focus_text} "
        f"carries `{antecedent}` from {source_regime} into `{consequence}` at {target_regime} while preserving `{invariant}`?"
    )
    theorem_template = (
        f"If one constructs a theorem-relevant {bridge_type} object on the route `{src}` -> `{dst}` "
        f"that realizes `{antecedent}` and preserves `{invariant}`, then `{consequence}` should follow."
    )
    obstruction = (
        f"Any candidate must avoid or neutralize barrier scope `{barrier}`."
        if barrier != "none"
        else "No named barrier is attached yet, so failure should be explained in terms of missing transport, typing, or payoff."
    )
    inspection_checklist = [
        f"State the source-side assumption precisely in the regime {source_regime}.",
        f"Specify the mathematical carrier of the expected object `{typed_object}` and how `{invariant}` is represented inside it.",
        missing_lemma or f"Identify the first theorem-family lemma turning the bridge object into `{consequence}` at {target_regime}.",
        obstruction,
    ]
    return {
        "source_regime": source_regime,
        "target_regime": target_regime,
        "source_assumption": f"Assume `{antecedent}` on the source side anchored at `{src}`.",
        "target_payoff": f"Derive `{consequence}` on the target side anchored at `{dst}`.",
        "bridge_question": bridge_question,
        "invariant_transport": f"Show that the bridge preserves `{invariant}`" + (f" with basis {', '.join(invariant_basis[:4])}." if invariant_basis else "."),
        "obstruction_pressure": obstruction,
        "theorem_template": theorem_template,
        "typed_object_expectation": typed_object,
        "missing_witness_or_transport": missing_lemma,
        "inspection_checklist": inspection_checklist,
    }


def _build(
    analysis: dict[str, Any],
    entrypoints: dict[str, Any],
    pathways: dict[str, Any],
    phyp: dict[str, Any],
    coherence: dict[str, Any],
    phase_of: dict[str, str],
    top_k: int,
    kb_statements: dict[str, dict[str, Any]] | None = None,
    search_space_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Relevance: Operates within the concept bridge planning layer.
    Concept: Construction of derived graph/model structures used by later stages.
    Contribution: Creates the structural substrate that enables cross-stage scoring and interpretation.
    """

    kb_statements = kb_statements or {}
    state_branches = (
        search_space_state.get("branches", {})
        if isinstance(search_space_state, dict) and isinstance(search_space_state.get("branches"), dict)
        else {}
    )

    ep_score = {
        str(x.get("statement_id", "")).strip(): float(x.get("entry_score", 0.0) or 0.0)
        for x in entrypoints.get("ranked_entrypoints", [])
        if isinstance(x, dict)
    }

    pathway_anchor_score = {
        str(p.get("entry_statement_id", "")).strip(): float(p.get("pathway_score", 0.0) or 0.0)
        for p in pathways.get("pathways", [])
        if isinstance(p, dict)
    }

    hyp_pair = defaultdict(float)
    hyp_coherence_pair = defaultdict(float)
    hyp_expl_pair = defaultdict(float)
    hyp_commitment_pair: dict[tuple[str, str], dict[str, Any]] = {}
    coh_index: dict[str, dict[str, Any]] = {}
    if isinstance(coherence.get("hypothesis_coherence_index"), dict):
        for hid, row in coherence.get("hypothesis_coherence_index", {}).items():
            if isinstance(row, dict):
                coh_index[str(hid).strip()] = row
    elif isinstance(coherence.get("hypothesis_coherence"), list):
        for row in coherence.get("hypothesis_coherence", []):
            if not isinstance(row, dict):
                continue
            hid = str(row.get("hypothesis_id", "")).strip()
            if hid:
                coh_index[hid] = row

    for h in phyp.get("hypotheses", []):
        if not isinstance(h, dict):
            continue
        hid = str(h.get("id", "")).strip()
        target = str(h.get("target_statement_id", "")).strip()
        support = str(h.get("support_statement_id", "")).strip()
        pr = float(h.get("priority", 0.0) or 0.0)
        coh_row = coh_index.get(hid, {})
        coh_delta = max(0.0, float(coh_row.get("coherence_delta_global", 0.0) or 0.0))
        expl = max(0.0, float(coh_row.get("explanatory_power_local", 0.0) or 0.0))
        if target and support:
            hyp_pair[(support, target)] = max(hyp_pair[(support, target)], pr)
            hyp_pair[(target, support)] = max(hyp_pair[(target, support)], pr * 0.9)
            hyp_coherence_pair[(support, target)] = max(hyp_coherence_pair[(support, target)], coh_delta)
            hyp_expl_pair[(support, target)] = max(hyp_expl_pair[(support, target)], expl)
            current = hyp_commitment_pair.get((support, target))
            if current is None or pr >= float(current.get("_priority", -1.0) or -1.0):
                hyp_commitment_pair[(support, target)] = {
                    "_priority": pr,
                    "hypothesis_id": hid,
                    "hypothesis_kind": str(h.get("kind", "")).strip(),
                    "support_antecedent_schema": str(h.get("support_antecedent_schema", "")).strip(),
                    "target_consequence_schema": str(h.get("target_consequence_schema", "")).strip(),
                    "preserved_invariant": str(h.get("preserved_invariant", "")).strip(),
                    "barrier_scope": str(h.get("barrier_scope", "")).strip(),
                    "invariant_basis": [str(x).strip() for x in h.get("invariant_basis", []) if str(x).strip()]
                    if isinstance(h.get("invariant_basis"), list)
                    else [],
                }

    programs = []
    for idx, c in enumerate(analysis.get("connection_candidates", []), start=1):
        if not isinstance(c, dict):
            continue
        src = str(c.get("from_id", "")).strip()
        dst = str(c.get("to_id", "")).strip()
        if not src or not dst:
            continue

        a_score = float(c.get("score", 0.0) or 0.0)
        e_score = max(ep_score.get(src, 0.0), ep_score.get(dst, 0.0))
        p_score = max(pathway_anchor_score.get(src, 0.0), pathway_anchor_score.get(dst, 0.0))
        h_score = hyp_pair.get((src, dst), 0.0)
        expl_score = max(float(c.get("semantic_score", 0.0) or 0.0), hyp_expl_pair.get((src, dst), 0.0))
        coh_score = hyp_coherence_pair.get((src, dst), 0.0)
        concept_score = float(c.get("concept_alignment", 0.0) or 0.0)
        commitment = hyp_commitment_pair.get((src, dst), {})
        commitment_signal = _commitment_score(commitment)
        from_profile = c.get("from_profile", {}) if isinstance(c.get("from_profile"), dict) else {}
        to_profile = c.get("to_profile", {}) if isinstance(c.get("to_profile"), dict) else {}

        bridge_score = (
            0.28 * a_score
            + 0.18 * e_score
            + 0.08 * p_score
            + 0.08 * h_score
            + 0.14 * expl_score
            + 0.10 * coh_score
            + 0.08 * concept_score
            + 0.06 * commitment_signal
        )

        src_phase = str(from_profile.get("statement_phase", "")).strip() or phase_of.get(src, "Unspecified")
        dst_phase = str(to_profile.get("statement_phase", "")).strip() or phase_of.get(dst, "Unspecified")
        src_roles = [str(role).strip() for role in from_profile.get("bridge_roles", [])] if isinstance(from_profile.get("bridge_roles"), list) else []
        dst_roles = [str(role).strip() for role in to_profile.get("bridge_roles", [])] if isinstance(to_profile.get("bridge_roles"), list) else []
        btype = _bridge_type(src, dst, src_phase, dst_phase, src_roles, dst_roles)
        statement_delta = _statement_delta(
            src=src,
            dst=dst,
            from_profile=from_profile,
            to_profile=to_profile,
            bridge_type=btype,
            commitment=commitment,
            concept_evidence=[str(t) for t in c.get("concept_evidence", [])][:6],
            evidence_terms=[str(t) for t in c.get("evidence_terms", [])][:6],
            source_statement=kb_statements.get(src, {}),
            target_statement=kb_statements.get(dst, {}),
        )
        mathematical_program = _mathematical_program(
            src=src,
            dst=dst,
            src_phase=src_phase,
            dst_phase=dst_phase,
            from_profile=from_profile,
            to_profile=to_profile,
            bridge_type=btype,
            commitment=commitment,
            concept_evidence=[str(t) for t in c.get("concept_evidence", [])][:6],
            evidence_terms=[str(t) for t in c.get("evidence_terms", [])][:6],
            statement_delta=statement_delta,
        )
        route_dimensions = build_route_dimensions(
            source_statement_id=src,
            target_statement_id=dst,
            bridge_type=btype,
            statement_delta=statement_delta,
            inferential_commitment=commitment,
        )
        route_sig = route_signature(route_dimensions)
        content_fingerprint = route_content_fingerprint(
            route_signature_value=route_sig,
            statement_delta=statement_delta,
            bridge_object_label=str(statement_delta.get("typed_object_expectation", "")).strip(),
        )
        revisit = compute_revisit_signal(state_branches.get(route_sig), content_fingerprint)
        effective_bridge_score = round(bridge_score * float(revisit.get("score_multiplier", 1.0) or 1.0), 4)

        programs.append(
            {
                "bridge_id": f"bridge.{idx:03d}",
                "from_id": src,
                "to_id": dst,
                "from_phase": src_phase,
                "to_phase": dst_phase,
                "from_bridge_roles": src_roles[:6],
                "to_bridge_roles": dst_roles[:6],
                "bridge_type": btype,
                "bridge_score": round(bridge_score, 4),
                "effective_bridge_score": effective_bridge_score,
                "tier": _tier(bridge_score),
                "search_space_state": {
                    "route_signature": route_sig,
                    "content_fingerprint": content_fingerprint,
                    "revisit_status": str(revisit.get("revisit_status", "")).strip(),
                    "prior_outcome": str(revisit.get("prior_outcome", "")).strip(),
                    "visit_count": int(revisit.get("visit_count", 0) or 0),
                    "last_seen_run_id": str(revisit.get("last_seen_run_id", "")).strip(),
                },
                "evidence_terms": [str(t) for t in c.get("evidence_terms", [])][:6],
                "concept_evidence": [str(t) for t in c.get("concept_evidence", [])][:6],
                "inferential_commitment": {
                    "hypothesis_id": str(commitment.get("hypothesis_id", "")).strip(),
                    "hypothesis_kind": str(commitment.get("hypothesis_kind", "")).strip(),
                    "support_antecedent_schema": str(commitment.get("support_antecedent_schema", "")).strip(),
                    "target_consequence_schema": str(commitment.get("target_consequence_schema", "")).strip(),
                    "preserved_invariant": str(commitment.get("preserved_invariant", "")).strip(),
                    "barrier_scope": str(commitment.get("barrier_scope", "")).strip() or "none",
                    "invariant_basis": [str(x) for x in commitment.get("invariant_basis", [])][:6]
                    if isinstance(commitment.get("invariant_basis"), list)
                    else [],
                },
                "statement_delta": statement_delta,
                "mathematical_program": mathematical_program,
                "signals": {
                    "analysis_score": round(a_score, 4),
                    "entrypoint_signal": round(e_score, 4),
                    "pathway_signal": round(p_score, 4),
                    "hypothesis_signal": round(h_score, 4),
                    "explanatory_signal": round(expl_score, 4),
                    "coherence_signal": round(coh_score, 4),
                    "concept_signal": round(concept_score, 4),
                    "commitment_signal": round(commitment_signal, 4),
                    "novelty_signal": float(revisit.get("novelty_signal", 1.0) or 1.0),
                    "revisit_penalty": float(revisit.get("revisit_penalty", 0.0) or 0.0),
                },
                "protocol": [
                    f"Instantiate tentative dependency {dst} depends_on {src} in a scratch KB branch.",
                    (
                        "State antecedent `{}` and target consequence `{}` explicitly before testing."
                    ).format(
                        str(commitment.get("support_antecedent_schema", "")).strip() or "unconditional",
                        str(commitment.get("target_consequence_schema", "")).strip() or "statement-conclusion",
                    ),
                    (
                        "Track preserved invariant `{}` and barrier scope `{}` while testing the bridge."
                    ).format(
                        str(commitment.get("preserved_invariant", "")).strip() or "support-to-target interface",
                        str(commitment.get("barrier_scope", "")).strip() or "none",
                    ),
                    f"Run kb-deduce with target {dst} and classify entailment status.",
                    f"Run kb-abduce on {dst}; keep the bridge only if residual missing-premise count decreases.",
                    "Run coherence-eval and retain bridge only if coherence_delta_global is non-negative.",
                ],
            }
        )

    programs.sort(key=lambda x: (x.get("effective_bridge_score", x["bridge_score"]), x["bridge_score"]), reverse=True)
    programs = programs[: max(1, top_k)]

    axis_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for p in programs:
        axis = f"{p['from_phase']} -> {p['to_phase']}"
        axis_groups[axis].append(p)

    axes = []
    for axis, items in sorted(axis_groups.items(), key=lambda kv: max(i["bridge_score"] for i in kv[1]), reverse=True):
        axes.append(
            {
                "axis": axis,
                "count": len(items),
                "top_bridges": [
                    {"bridge_id": b["bridge_id"], "from_id": b["from_id"], "to_id": b["to_id"], "score": b["bridge_score"]}
                    for b in items[:3]
                ],
            }
        )

    return {
            "metadata": {
                "candidate_count": len(analysis.get("connection_candidates", [])),
                "bridge_program_count": len(programs),
                "axes_count": len(axes),
                "scoring": (
                "0.28*analysis + 0.18*entrypoint + 0.08*pathway + 0.08*hypothesis + "
                "0.14*explanatory + 0.10*coherence + 0.08*concept + 0.06*commitment"
                ),
                "recommended_order_adjustment": "effective_bridge_score = bridge_score * search-space novelty multiplier",
            },
        "bridge_programs": programs,
        "bridge_axes": axes,
        "recommended_run_order": [b["bridge_id"] for b in programs[:6]],
    }


def _to_markdown(report: dict[str, Any]) -> str:
    """
    Relevance: Operates within the concept bridge planning layer.
    Concept: Rendering internal outputs into human-readable artifacts.
    Contribution: Improves interpretability by exposing machine results in analyst-friendly form.
    """

    lines = []
    lines.append("# Essential Concept Bridge Plan")
    lines.append("")
    meta = report.get("metadata", {})
    lines.append("## Stats")
    lines.append("")
    lines.append(f"- Input connection candidates: {meta.get('candidate_count', 0)}")
    lines.append(f"- Bridge programs: {meta.get('bridge_program_count', 0)}")
    lines.append(f"- Concept axes: {meta.get('axes_count', 0)}")
    lines.append("")

    lines.append("## Top Bridge Programs")
    lines.append("")
    lines.append("| bridge_id | from_id | to_id | type | tier | score | effective | novelty | expl | coh | concept_evidence |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for b in report.get("bridge_programs", []):
        signals = b.get("signals", {}) if isinstance(b.get("signals"), dict) else {}
        lines.append(
            f"| {b['bridge_id']} | {b['from_id']} | {b['to_id']} | {b['bridge_type']} | {b['tier']} | {b['bridge_score']} | {b.get('effective_bridge_score', b['bridge_score'])} | {signals.get('novelty_signal', 1.0)} | {signals.get('explanatory_signal', 0.0)} | {signals.get('coherence_signal', 0.0)} | {', '.join(b.get('concept_evidence', [])[:4])} |"
        )
    lines.append("")

    lines.append("## Mathematical Commitments")
    lines.append("")
    for b in report.get("bridge_programs", [])[:10]:
        commit = b.get("inferential_commitment", {}) if isinstance(b.get("inferential_commitment"), dict) else {}
        mathematical_program = b.get("mathematical_program", {}) if isinstance(b.get("mathematical_program"), dict) else {}
        lines.append(f"### {b['bridge_id']} ({b['from_id']} -> {b['to_id']})")
        lines.append(
            f"- Antecedent schema: {commit.get('support_antecedent_schema', '') or 'unconditional'}"
        )
        lines.append(
            f"- Target consequence: {commit.get('target_consequence_schema', '') or 'statement-conclusion'}"
        )
        lines.append(
            f"- Preserved invariant: {commit.get('preserved_invariant', '') or 'support-to-target interface'}"
        )
        lines.append(f"- Barrier scope: {commit.get('barrier_scope', '') or 'none'}")
        basis = commit.get("invariant_basis", []) if isinstance(commit.get("invariant_basis"), list) else []
        if basis:
            lines.append(f"- Invariant basis: {', '.join(str(x) for x in basis[:6])}")
        if mathematical_program:
            lines.append(f"- Source regime: {mathematical_program.get('source_regime', '')}")
            lines.append(f"- Target regime: {mathematical_program.get('target_regime', '')}")
            lines.append(f"- Source assumption: {mathematical_program.get('source_assumption', '')}")
            lines.append(f"- Target payoff: {mathematical_program.get('target_payoff', '')}")
            lines.append(f"- Bridge question: {mathematical_program.get('bridge_question', '')}")
            lines.append(f"- Invariant transport claim: {mathematical_program.get('invariant_transport', '')}")
            lines.append(f"- Conditional theorem template: {mathematical_program.get('theorem_template', '')}")
            lines.append(f"- Expected bridge object: {mathematical_program.get('typed_object_expectation', '')}")
            lines.append(f"- Missing witness/transport lemma: {mathematical_program.get('missing_witness_or_transport', '')}")
            checklist = mathematical_program.get("inspection_checklist", []) if isinstance(mathematical_program.get("inspection_checklist"), list) else []
            if checklist:
                lines.append("- Expert inspection checklist:")
                for item in checklist[:4]:
                    lines.append(f"  - {item}")
        statement_delta = b.get("statement_delta", {}) if isinstance(b.get("statement_delta"), dict) else {}
        search_state = b.get("search_space_state", {}) if isinstance(b.get("search_space_state"), dict) else {}
        if statement_delta:
            lines.append("- Statement delta:")
            lines.append(f"  - Route synopsis: {statement_delta.get('route_synopsis', '')}")
            lines.append(f"  - Model shift: {statement_delta.get('model_shift', '')}")
            lines.append(f"  - Threshold shift: {statement_delta.get('threshold_shift', '')}")
            lines.append(f"  - Consequence shift: {statement_delta.get('consequence_shift', '')}")
            lines.append(
                f"  - Typed object expectation: {statement_delta.get('typed_object_expectation', '')} ({statement_delta.get('typing_status', '')})"
            )
            lines.append(f"  - Missing witness/transport: {statement_delta.get('missing_witness_or_transport', '')}")
        if search_state:
            lines.append("- Search-space history:")
            lines.append(f"  - Route signature: {search_state.get('route_signature', '')}")
            lines.append(f"  - Revisit status: {search_state.get('revisit_status', '')}")
            lines.append(f"  - Prior outcome: {search_state.get('prior_outcome', '')}")
            lines.append(f"  - Previous visits: {search_state.get('visit_count', 0)}")
        lines.append("")

    lines.append("## Bridge Axes")
    lines.append("")
    for ax in report.get("bridge_axes", []):
        lines.append(f"### {ax['axis']}")
        lines.append(f"- Count: {ax['count']}")
        for b in ax.get("top_bridges", []):
            lines.append(f"- {b['bridge_id']}: {b['from_id']} -> {b['to_id']} (score={b['score']})")
        lines.append("")

    lines.append("## Recommended Run Order")
    lines.append("")
    for i, bid in enumerate(report.get("recommended_run_order", []), start=1):
        lines.append(f"{i}. {bid}")

    return "\n".join(lines) + "\n"


def main() -> int:
    """
    Relevance: Operates within the concept bridge planning layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds parsing, computation, and artifact emission into a reproducible script execution.
    """

    logger = ReasoningLogger("kb-concept-bridge-planner")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--analysis", required=True)
    ap.add_argument("--entrypoints", required=True)
    ap.add_argument("--pathways", required=True)
    ap.add_argument("--phyp", required=True)
    ap.add_argument("--coherence-report")
    ap.add_argument("--kb", help="Optional KB markdown path used to ground theorem excerpts and claim focus.")
    ap.add_argument("--concept", required=True)
    ap.add_argument("--search-space-state", help="Optional persisted search-space state JSON used to deprioritize stale routes.")
    ap.add_argument("--top-k", type=int, default=20)
    ap.add_argument("--output-json")
    ap.add_argument("--output-md")
    args = ap.parse_args()
    logger.step(
        "Parsed bridge-planner arguments",
        "\n".join(
            [
                f"analysis={args.analysis}",
                f"entrypoints={args.entrypoints}",
                f"pathways={args.pathways}",
                f"phyp={args.phyp}",
                f"coherence_report={args.coherence_report or ''}",
                f"kb={args.kb or ''}",
                f"concept={args.concept}",
                f"search_space_state={args.search_space_state or ''}",
                f"top_k={args.top_k}",
                f"output_json={args.output_json or ''}",
                f"output_md={args.output_md or ''}",
            ]
        ),
    )

    analysis_path = Path(args.analysis)
    entrypoints_path = Path(args.entrypoints)
    pathways_path = Path(args.pathways)
    phyp_path = Path(args.phyp)
    coherence_path = Path(args.coherence_report) if args.coherence_report else None
    kb_path = Path(args.kb) if args.kb else None
    concept_path = Path(args.concept)
    search_space_state_path = Path(args.search_space_state) if args.search_space_state else None

    for p in [analysis_path, entrypoints_path, pathways_path, phyp_path, concept_path]:
        if not p.exists():
            log_path = logger.finalize("error", summary=f"Missing input: {p}")
            print(f"[LOG] {log_path}", file=sys.stderr)
            raise SystemExit(f"[ERROR] Missing input: {p}")
    if coherence_path and not coherence_path.exists():
        log_path = logger.finalize("error", summary=f"Missing input: {coherence_path}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Missing input: {coherence_path}")
    if kb_path and not kb_path.exists():
        log_path = logger.finalize("error", summary=f"Missing input: {kb_path}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Missing input: {kb_path}")
    if search_space_state_path and not search_space_state_path.exists():
        search_space_state_path = None

    try:
        analysis = validate_connection_analysis(json.loads(analysis_path.read_text(encoding="utf-8")), name="analysis")
        entrypoints = validate_entrypoints(json.loads(entrypoints_path.read_text(encoding="utf-8")), name="entrypoints")
        pathways = validate_pathways(json.loads(pathways_path.read_text(encoding="utf-8")), name="pathways")
        phyp = validate_phyp(yaml.safe_load(phyp_path.read_text(encoding="utf-8")), name="phyp")
        coherence = (
            validate_coherence_report(json.loads(coherence_path.read_text(encoding="utf-8")), name="coherence")
            if coherence_path
            else {}
        )
    except ValueError as exc:
        log_path = logger.finalize("error", summary=str(exc))
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] {exc}")
    phase_of = _phase_map(concept_path)
    kb_statements = load_statement_index(kb_path)
    search_space_state = (
        load_search_space_state(search_space_state_path, kb_ref="")
        if search_space_state_path
        else {"branches": {}}
    )

    report = _build(
        analysis=analysis,
        entrypoints=entrypoints,
        pathways=pathways,
        phyp=phyp,
        coherence=coherence,
        phase_of=phase_of,
        top_k=max(1, args.top_k),
        kb_statements=kb_statements,
        search_space_state=search_space_state,
    )
    programs = report.get("bridge_programs", []) if isinstance(report.get("bridge_programs"), list) else []
    axes = report.get("bridge_axes", []) if isinstance(report.get("bridge_axes"), list) else []
    logger.step(
        "Bridge concept trace",
        "\n".join(
            [
                "top_bridge_programs="
                + "; ".join(
                    f"{str(item.get('bridge_id', '')).strip()}:{str(item.get('from_id', '')).strip()}->{str(item.get('to_id', '')).strip()}:{float(item.get('effective_bridge_score', item.get('bridge_score', 0.0)) or 0.0):.4f}:"
                    f"{str((item.get('inferential_commitment', {}) if isinstance(item.get('inferential_commitment'), dict) else {}).get('target_consequence_schema', '')).strip() or 'statement-conclusion'}:"
                    f"{str((item.get('inferential_commitment', {}) if isinstance(item.get('inferential_commitment'), dict) else {}).get('preserved_invariant', '')).strip() or 'support-interface'}"
                    for item in programs[:6]
                    if isinstance(item, dict)
                    and str(item.get("bridge_id", "")).strip()
                    and str(item.get("from_id", "")).strip()
                    and str(item.get("to_id", "")).strip()
                ),
                "top_bridge_axes="
                + "; ".join(
                    str(item.get("axis", "")).strip()
                    for item in axes[:6]
                    if isinstance(item, dict) and str(item.get("axis", "")).strip()
                ),
                "top_bridge_theorem_templates="
                + "; ".join(
                    f"{str(item.get('bridge_id', '')).strip()}:{str((item.get('mathematical_program', {}) if isinstance(item.get('mathematical_program'), dict) else {}).get('theorem_template', '')).strip()}"
                    for item in programs[:4]
                    if isinstance(item, dict)
                    and str(item.get("bridge_id", "")).strip()
                    and str((item.get("mathematical_program", {}) if isinstance(item.get("mathematical_program"), dict) else {}).get("theorem_template", "")).strip()
                ),
                "top_bridge_statement_deltas="
                + "; ".join(
                    f"{str(item.get('bridge_id', '')).strip()}:{str((item.get('statement_delta', {}) if isinstance(item.get('statement_delta'), dict) else {}).get('route_synopsis', '')).strip()}"
                    for item in programs[:4]
                    if isinstance(item, dict)
                    and str(item.get("bridge_id", "")).strip()
                    and str((item.get("statement_delta", {}) if isinstance(item.get("statement_delta"), dict) else {}).get("route_synopsis", "")).strip()
                ),
            ]
        ),
    )

    if args.output_json:
        out = Path(args.output_json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"[OK] Wrote JSON: {out}")
        logger.add_output("bridge_plan_json", out)

    md = _to_markdown(report)
    if args.output_md:
        out = Path(args.output_md)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md, encoding="utf-8")
        print(f"[OK] Wrote Markdown: {out}")
        logger.add_output("bridge_plan_md", out)

    print(f"[OK] Bridge programs: {len(report.get('bridge_programs', []))}")
    if report.get("bridge_programs"):
        top = report["bridge_programs"][0]
        print(
            f"[OK] Top bridge: {top['bridge_id']} ({top['from_id']} -> {top['to_id']}, "
            f"score={top.get('effective_bridge_score', top['bridge_score'])})"
        )
        logger.step(
            "Computed top bridge",
            "\n".join(
                [
                    f"bridge_id={top['bridge_id']}",
                    f"from={top['from_id']}",
                    f"to={top['to_id']}",
                    f"score={top['bridge_score']}",
                    f"effective_score={top.get('effective_bridge_score', top['bridge_score'])}",
                    "antecedent="
                    + str(
                        (top.get("inferential_commitment", {}) if isinstance(top.get("inferential_commitment"), dict) else {}).get(
                            "support_antecedent_schema", ""
                        )
                    ).strip(),
                    "consequence="
                    + str(
                        (top.get("inferential_commitment", {}) if isinstance(top.get("inferential_commitment"), dict) else {}).get(
                            "target_consequence_schema", ""
                        )
                    ).strip(),
                    "invariant="
                    + str(
                        (top.get("inferential_commitment", {}) if isinstance(top.get("inferential_commitment"), dict) else {}).get(
                            "preserved_invariant", ""
                        )
                    ).strip(),
                    "barrier="
                    + str(
                        (top.get("inferential_commitment", {}) if isinstance(top.get("inferential_commitment"), dict) else {}).get(
                            "barrier_scope", ""
                        )
                    ).strip(),
                    "theorem_template="
                    + str(
                        (top.get("mathematical_program", {}) if isinstance(top.get("mathematical_program"), dict) else {}).get(
                            "theorem_template", ""
                        )
                    ).strip(),
                    "statement_delta="
                    + str(
                        (top.get("statement_delta", {}) if isinstance(top.get("statement_delta"), dict) else {}).get(
                            "route_synopsis", ""
                        )
                    ).strip(),
                ]
            ),
        )
    log_path = logger.finalize(
        "success",
        summary=f"Generated {len(report.get('bridge_programs', []))} bridge programs.",
    )
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
