# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""Establish proof strategies from intermediate artifacts and generate novelty-maximizing prompts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from reasoning_log import ReasoningLogger
from contracts import validate_bridges
from contracts import validate_coherence_report
from contracts import validate_conjecture_report
from contracts import validate_entrypoints
from contracts import validate_pathways
from contracts import validate_phyp


def _jaccard(a: set[str], b: set[str]) -> float:
    """
    Relevance: Operates within the proof strategy design layer.
    Concept: Lightweight semantic feature computation for graph reasoning heuristics.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if not a and not b:
        return 0.0
    u = a | b
    if not u:
        return 0.0
    return len(a & b) / len(u)


def _strategy_name(phase: str, anchor: str) -> str:
    """
    Relevance: Operates within the proof strategy design layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    p = phase.lower()
    if "barrier" in p:
        return f"Barrier-Aware Escape around {anchor}"
    if "representation" in p or "riesz" in p or "measure" in p:
        return f"Measure-Representation Route around {anchor}"
    if "regularity" in p or "compact-open" in p:
        return f"Regularity-Reconstruction Route around {anchor}"
    if "duality" in p or "variation" in p:
        return f"Integration-Duality Route around {anchor}"
    if "fixed-point" in p or "common-fixed-point" in p:
        return f"Invariant Fixed-Point Route around {anchor}"
    if "averaging" in p or "cesaro" in p:
        return f"Affine Averaging Route around {anchor}"
    if "intersection" in p or "compactness" in p:
        return f"Compactness-Intersection Route around {anchor}"
    if "stone" in p or "correspondence" in p:
        return f"Stone Correspondence Route around {anchor}"
    if "spectral" in p or "functional" in p:
        return f"Spectral-Calculus Route around {anchor}"
    if "unitary" in p or "generator" in p:
        return f"Generator-Recovery Route around {anchor}"
    if "self-adjoint" in p or "hilbert" in p:
        return f"Self-Adjoint Realization around {anchor}"
    if "magnification" in p or "meta-complexity" in p:
        return f"Magnification Route around {anchor}"
    if "derandom" in p or "pit" in p:
        return f"Derandomization-Lower-Bound Route around {anchor}"
    if "proof complexity" in p or "proof" in p:
        return f"Proof-Complexity Transfer around {anchor}"
    if "nonuniform" in p or "circuit" in p:
        return f"Nonuniform Separation Route around {anchor}"
    return f"Cross-Model Strategy around {anchor}"


def _hypothesis_lookup(phyp: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """
    Relevance: Operates within the proof strategy design layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    out: dict[str, dict[str, Any]] = {}
    for h in phyp.get("hypotheses", []) if isinstance(phyp.get("hypotheses"), list) else []:
        if not isinstance(h, dict):
            continue
        hid = str(h.get("id", "")).strip()
        if not hid:
            continue
        out[hid] = h
    return out


def _conjecture_lookup(conjectures: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """
    Relevance: Operates within the proof strategy design layer.
    Concept: Construction of derived graph/model structures used by later stages.
    Contribution: Makes conjectured bridge-filling abstractions available as first-class signals during strategy synthesis.
    """

    out: dict[str, list[dict[str, Any]]] = {}
    for row in conjectures.get("abstraction_conjectures", []) if isinstance(conjectures.get("abstraction_conjectures"), list) else []:
        if not isinstance(row, dict):
            continue
        bridge_id = str(row.get("bridge_id", "")).strip()
        if not bridge_id:
            continue
        out.setdefault(bridge_id, []).append(row)
    return out


def _candidate_from_pathway(
    pathway: dict[str, Any],
    bridge_lookup: dict[str, dict[str, Any]],
    hypothesis_lookup: dict[str, dict[str, Any]],
    coherence_index: dict[str, dict[str, Any]],
    conjecture_lookup: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    """
    Relevance: Operates within the proof strategy design layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    entry_id = str(pathway.get("entry_statement_id", "")).strip()
    phase = str(pathway.get("entry_phase", "Unspecified")).strip()
    pscore = float(pathway.get("pathway_score", 0.0) or 0.0)

    hyp_items = pathway.get("supporting_hypotheses", []) if isinstance(pathway.get("supporting_hypotheses"), list) else []
    link_items = pathway.get("supporting_links", []) if isinstance(pathway.get("supporting_links"), list) else []

    hyp_avg = 0.0
    weighted_hyp = 0.0
    hyp_weight_denom = 0.0
    hyp_ids = []
    status_counts = {
        "supported": 0,
        "refuted": 0,
        "provisional": 0,
        "unresolved": 0,
        "unknown": 0,
    }
    conceptual_kinds = {
        "definition-introduction",
        "representation-shift",
        "intermediate-invariant",
        "barrier-escape-principle",
        "analogy-transfer",
        "normal-form-reduction",
    }
    conceptual_count = 0
    coherence_positive = 0
    coherence_negative = 0
    explanatory_sum = 0.0
    coherence_delta_sum = 0.0
    if hyp_items:
        hyp_avg = sum(float(h.get("priority", 0.0) or 0.0) for h in hyp_items) / len(hyp_items)
        for h in hyp_items:
            hid = str(h.get("id", "")).strip()
            if not hid:
                continue
            hyp_ids.append(hid)
            h_priority = float(h.get("priority", 0.0) or 0.0)
            lookup = hypothesis_lookup.get(hid, {})
            status = str(lookup.get("status", "")).strip().lower()
            kind = str(lookup.get("kind", h.get("kind", ""))).strip().lower()
            if kind in conceptual_kinds:
                conceptual_count += 1
            coh = coherence_index.get(hid, {})
            exp = float(coh.get("explanatory_power_local", 0.0) or 0.0)
            cdelta = float(coh.get("coherence_delta_global", 0.0) or 0.0)
            explanatory_sum += max(0.0, exp)
            coherence_delta_sum += cdelta
            if cdelta > 0:
                coherence_positive += 1
            elif cdelta < 0:
                coherence_negative += 1
            if status == "supported":
                weight = 1.10
                status_counts["supported"] += 1
            elif status == "refuted":
                weight = 0.15
                status_counts["refuted"] += 1
            elif status in {"provisionally-supported", "provisionally-refuted"}:
                weight = 0.75
                status_counts["provisional"] += 1
            elif status in {"needs-testing", "tentative"}:
                weight = 1.0
                status_counts["unresolved"] += 1
            elif status:
                weight = 1.0
                status_counts["unknown"] += 1
            else:
                weight = 1.0
                status_counts["unknown"] += 1
            weighted_hyp += h_priority * weight
            hyp_weight_denom += weight

    weighted_hyp_avg = weighted_hyp / hyp_weight_denom if hyp_weight_denom > 0 else hyp_avg

    link_avg = 0.0
    link_pairs = []
    for l in link_items:
        src = str(l.get("from_id", "")).strip()
        dst = str(l.get("to_id", "")).strip()
        if src and dst:
            link_pairs.append((src, dst))
    if link_items:
        link_avg = sum(float(l.get("score", 0.0) or 0.0) for l in link_items) / len(link_items)

    bridge_ids = []
    bridge_scores = []
    abstraction_rows: list[dict[str, Any]] = []
    for src, dst in link_pairs:
        key = f"{src}->{dst}"
        b = bridge_lookup.get(key)
        if b:
            bridge_ids.append(str(b.get("bridge_id", "")).strip())
            bridge_scores.append(float(b.get("bridge_score", 0.0) or 0.0))
            abstraction_rows.extend(conjecture_lookup.get(str(b.get("bridge_id", "")).strip(), []))

    bridge_avg = sum(bridge_scores) / len(bridge_scores) if bridge_scores else 0.0
    support_score = 0.65 * weighted_hyp_avg + 0.35 * max(link_avg, bridge_avg)
    total_hyp = max(1, len(hyp_ids))
    status_bonus = (0.06 * status_counts["supported"] - 0.08 * status_counts["refuted"]) / total_hyp
    base_strength = max(0.0, min(1.0, 0.60 * pscore + 0.35 * support_score + 0.05 * (0.5 + status_bonus)))
    explanatory_avg = explanatory_sum / total_hyp
    coherence_avg = coherence_delta_sum / total_hyp
    unification_gain = min(1.0, len({str(x[0]) for x in link_pairs} | {str(x[1]) for x in link_pairs} | {entry_id}) / 8.0)
    proof_compression = min(1.0, 1.0 - min(1.0, len(link_pairs) / max(1.0, len(hyp_ids) + len(link_pairs))))
    transfer_power = min(1.0, len(set(bridge_ids)) / 5.0 + 0.4 * min(1.0, conceptual_count / max(1, total_hyp)))
    barrier_evasion = min(1.0, (0.6 * coherence_positive + 0.4 * conceptual_count) / max(1, total_hyp))
    lemma_generation = min(1.0, conceptual_count / max(1, total_hyp))
    abstraction_types = {
        str(row.get("abstraction_type", "")).strip()
        for row in abstraction_rows
        if isinstance(row, dict) and str(row.get("abstraction_type", "")).strip()
    }
    abstraction_leverage = min(1.0, len(abstraction_types) / 4.0)
    definitional_avg = (
        sum(float(row.get("definitional_completeness", 0.0) or 0.0) for row in abstraction_rows if isinstance(row, dict))
        / max(1, len(abstraction_rows))
        if abstraction_rows
        else 0.0
    )
    counterfactual_avg = (
        sum(float(row.get("counterfactual_sharpness", 0.0) or 0.0) for row in abstraction_rows if isinstance(row, dict))
        / max(1, len(abstraction_rows))
        if abstraction_rows
        else 0.0
    )
    coherence_bonus = max(0.0, coherence_avg)
    coherence_penalty = max(0.0, -coherence_avg) + 0.15 * min(1.0, coherence_negative / max(1, total_hyp))
    fertility = max(
        0.0,
        min(
            1.0,
            0.25 * unification_gain
            + 0.20 * proof_compression
            + 0.20 * transfer_power
            + 0.20 * barrier_evasion
            + 0.15 * lemma_generation
            + 0.10 * abstraction_leverage
            + 0.10 * definitional_avg
            + 0.10 * counterfactual_avg
            + 0.10 * explanatory_avg
            + 0.10 * coherence_bonus
            - 0.20 * coherence_penalty,
        ),
    )

    anchor_set = {entry_id}
    for src, dst in link_pairs:
        anchor_set.add(src)
        anchor_set.add(dst)

    return {
        "entry_id": entry_id,
        "phase": phase,
        "base_strength": base_strength,
        "pathway_score": pscore,
        "support_score": support_score,
        "hypothesis_ids": hyp_ids,
        "hypothesis_status_summary": status_counts,
        "bridge_ids": [b for b in bridge_ids if b],
        "concept_fertility": fertility,
        "fertility_components": {
            "unification_gain": round(unification_gain, 4),
            "proof_compression": round(proof_compression, 4),
            "transfer_power": round(transfer_power, 4),
            "barrier_evasion": round(barrier_evasion, 4),
            "lemma_generation": round(lemma_generation, 4),
            "abstraction_leverage": round(abstraction_leverage, 4),
            "definitional_avg": round(definitional_avg, 4),
            "counterfactual_avg": round(counterfactual_avg, 4),
            "explanatory_avg": round(explanatory_avg, 4),
            "coherence_avg": round(coherence_avg, 4),
        },
        "anchors": sorted(anchor_set),
        "abstraction_rows": abstraction_rows,
        "pathway": pathway,
    }


def _select_diverse(candidates: list[dict[str, Any]], top_k: int) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the proof strategy design layer.
    Concept: Selection/retrieval of the most relevant candidates for reasoning.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    selected: list[dict[str, Any]] = []

    while candidates and len(selected) < top_k:
        best_i = -1
        best_score = -1.0
        for i, c in enumerate(candidates):
            c_phase = c["phase"]
            c_anchors = set(c["anchors"])

            if not selected:
                novelty = 1.0
            else:
                phase_new = 1.0 if c_phase not in {s["phase"] for s in selected} else 0.35
                overlap = max(_jaccard(c_anchors, set(s["anchors"])) for s in selected)
                novelty = 0.6 * phase_new + 0.4 * (1.0 - overlap)

            fertility = float(c.get("concept_fertility", 0.0) or 0.0)
            combined = 0.55 * c["base_strength"] + 0.20 * novelty + 0.25 * fertility
            if combined > best_score:
                best_score = combined
                best_i = i

        chosen = candidates.pop(best_i)
        chosen["selection_score"] = best_score
        selected.append(chosen)

    return selected


def _build_dynamic_novelty_prompt(
    strategies: list[dict[str, Any]],
    coherence_profile: dict[str, Any],
    coherence_index: dict[str, dict[str, Any]],
    top_abstractions: list[dict[str, Any]] | None = None,
) -> str:
    """
    Relevance: Operates within the proof strategy design layer.
    Concept: Rendering internal outputs into human-readable artifacts.
    Contribution: Synthesizes an adaptive prompting policy from live diagnostic signals.
    """

    top_items = strategies[:3]
    if not top_items:
        return (
            "You are a proof-strategy synthesizer.\n"
            "No ranked strategies were produced; request additional connector/pathway evidence before proposing moves."
        )

    global_coh = float(coherence_profile.get("global_coherence", 0.0) or 0.0)
    negative_coh = sum(
        1 for row in coherence_index.values() if float(row.get("coherence_delta_global", 0.0) or 0.0) < 0.0
    )
    high_tension = float(coherence_profile.get("tension", 0.0) or 0.0)
    risk_mode = global_coh < 0.50 or high_tension > 0.40

    if risk_mode:
        novelty_weights = {
            "phase_diversity": 0.30,
            "bridge_originality": 0.22,
            "hypothesis_nonredundancy": 0.18,
            "minimal_assumption_gain": 0.10,
            "coherence_preservation": 0.20,
        }
    else:
        novelty_weights = {
            "phase_diversity": 0.38,
            "bridge_originality": 0.28,
            "hypothesis_nonredundancy": 0.20,
            "minimal_assumption_gain": 0.14,
            "coherence_preservation": 0.00,
        }

    top_strategy_lines = []
    for idx, item in enumerate(top_items, start=1):
        top_strategy_lines.append(
            (
                f"{idx}. {item.get('strategy_id', '')} | anchor={item.get('anchor_statement_id', '')} | "
                f"phase={item.get('phase', '')} | score={item.get('strategy_score', 0.0)} | "
                f"fertility={item.get('concept_fertility', 0.0)}"
            )
        )

    lines = [
        "You are a proof-strategy synthesizer optimizing novelty under rigor constraints.",
        "Inputs: KB slice, ranked strategies, bridge programs, hypothesis sets, coherence diagnostics.",
        "Objective: maximize expected proof progress while maximizing conceptual novelty.",
        (
            "Novelty score N = "
            f"{novelty_weights['phase_diversity']:.2f}*phase_diversity + "
            f"{novelty_weights['bridge_originality']:.2f}*bridge_originality + "
            f"{novelty_weights['hypothesis_nonredundancy']:.2f}*hypothesis_nonredundancy + "
            f"{novelty_weights['minimal_assumption_gain']:.2f}*minimal_assumption_gain"
            + (
                f" + {novelty_weights['coherence_preservation']:.2f}*coherence_preservation"
                if novelty_weights["coherence_preservation"] > 0
                else ""
            )
            + "."
        ),
        "Live diagnostics:",
        f"- global_coherence={global_coh:.4f}",
        f"- tension={high_tension:.4f}",
        f"- coherence_negative_hypotheses={negative_coh}",
        f"- risk_mode={'on' if risk_mode else 'off'}",
        (
            "- top_abstraction_conjectures="
            + "; ".join(
                f"{str(row.get('conjecture_id', '')).strip()}:{str(row.get('abstraction_type', '')).strip()}:{str(row.get('abstraction_label', '')).strip()}"
                for row in (top_abstractions or [])[:3]
                if isinstance(row, dict)
            )
            if top_abstractions
            else "- top_abstraction_conjectures=none"
        ),
        (
            "- top_definitional_requirements="
            + "; ".join(
                f"{str(row.get('conjecture_id', '')).strip()}:"
                + ", ".join(
                    str(attr.get("attribute", "")).strip()
                    for attr in (
                        row.get("definitional_profile", {}).get("necessary_attributes", [])
                        if isinstance(row.get("definitional_profile"), dict)
                        else []
                    )[:2]
                    if isinstance(attr, dict) and str(attr.get("attribute", "")).strip()
                )
                for row in (top_abstractions or [])[:3]
                if isinstance(row, dict) and str(row.get("conjecture_id", "")).strip()
            )
            if top_abstractions
            else "- top_definitional_requirements=none"
        ),
        (
            "- top_counterfactual_probes="
            + "; ".join(
                f"{str(row.get('conjecture_id', '')).strip()}:"
                + str(
                    (
                        row.get("counterfactual_probes", [{}])[0].get("intervention", "")
                        if isinstance(row.get("counterfactual_probes"), list) and row.get("counterfactual_probes")
                        else ""
                    )
                ).strip()
                for row in (top_abstractions or [])[:3]
                if isinstance(row, dict) and str(row.get("conjecture_id", "")).strip()
            )
            if top_abstractions
            else "- top_counterfactual_probes=none"
        ),
        "Top strategies:",
        *top_strategy_lines,
        "Hard constraints:",
        "1. Every proposed step must reference statement IDs.",
        "2. Each round must include at least one bridge from a phase different from the previous round.",
        "3. Reject moves that only restate existing dependencies without adding new conditional entailment paths.",
        "4. Prefer smallest hypothesis sets that unlock the largest new consequence set.",
        "5. If risk_mode=on, reject any move whose expected coherence impact is negative.",
        "6. Every selected move must state which necessary abstraction attribute it is instantiating.",
        "7. Every selected move must include one counterfactual probe that could falsify the bridge concept.",
        "Procedure:",
        "- Start from strategy 1; generate 3 candidate proof moves (anchor + bridge + hypothesis).",
        "- Score each move by (validity risk, novelty gain, expected entailment gain, coherence impact, definitional adequacy, counterfactual informativeness).",
        "- Keep one move, archive two alternatives, then rotate to another phase for next round.",
        "Output format:",
        "### Chosen Strategy",
        "### Candidate Moves (3)",
        "### Scores",
        "### Definitional Attribute Used",
        "### Counterfactual Probe",
        "### Selected Move and Rationale",
        "### Next-Round Phase Constraint",
    ]
    return "\n".join(lines)


def _build(
    entrypoints: dict[str, Any],
    pathways: dict[str, Any],
    bridges: dict[str, Any],
    phyp: dict[str, Any],
    coherence: dict[str, Any],
    conjectures: dict[str, Any],
    top_k: int,
) -> dict[str, Any]:
    """
    Relevance: Operates within the proof strategy design layer.
    Concept: Construction of derived graph/model structures used by later stages.
    Contribution: Creates the structural substrate that enables cross-stage scoring and interpretation.
    """

    hypothesis_lookup = _hypothesis_lookup(phyp if isinstance(phyp, dict) else {"hypotheses": []})
    coherence_index: dict[str, dict[str, Any]] = {}
    if isinstance(coherence.get("hypothesis_coherence_index"), dict):
        for hid, row in coherence.get("hypothesis_coherence_index", {}).items():
            if isinstance(row, dict):
                coherence_index[str(hid).strip()] = row
    elif isinstance(coherence.get("hypothesis_coherence"), list):
        for row in coherence.get("hypothesis_coherence", []):
            if not isinstance(row, dict):
                continue
            hid = str(row.get("hypothesis_id", "")).strip()
            if hid:
                coherence_index[hid] = row
    bridge_lookup: dict[str, dict[str, Any]] = {}
    for b in bridges.get("bridge_programs", []):
        if not isinstance(b, dict):
            continue
        src = str(b.get("from_id", "")).strip()
        dst = str(b.get("to_id", "")).strip()
        if src and dst:
            bridge_lookup[f"{src}->{dst}"] = b
    conjecture_lookup = _conjecture_lookup(conjectures if isinstance(conjectures, dict) else {})
    entrypoint_lookup: dict[str, dict[str, Any]] = {}
    for row in entrypoints.get("ranked_entrypoints", []):
        if not isinstance(row, dict):
            continue
        sid = str(row.get("statement_id", "")).strip()
        if sid:
            entrypoint_lookup[sid] = row

    candidates = []
    for p in pathways.get("pathways", []):
        if not isinstance(p, dict):
            continue
        candidates.append(_candidate_from_pathway(p, bridge_lookup, hypothesis_lookup, coherence_index, conjecture_lookup))

    candidates.sort(key=lambda x: x["base_strength"], reverse=True)
    selected = _select_diverse(candidates, top_k=max(1, top_k))

    strategies = []
    for i, s in enumerate(selected, start=1):
        anchor_row = entrypoint_lookup.get(s["entry_id"], {})
        anchor_concepts = [
            str(x).strip()
            for x in (anchor_row.get("concept_focus", []) if isinstance(anchor_row.get("concept_focus"), list) else [])
            if str(x).strip()
        ][:8]
        bridge_concepts: list[str] = []
        abstraction_concepts: list[str] = []
        definitional_focus: list[str] = []
        counterfactual_focus: list[str] = []
        for bid in s.get("bridge_ids", [])[:6]:
            bridge_obj = next(
                (b for b in bridges.get("bridge_programs", []) if isinstance(b, dict) and str(b.get("bridge_id", "")).strip() == str(bid).strip()),
                {},
            )
            for concept in bridge_obj.get("concept_evidence", []) if isinstance(bridge_obj.get("concept_evidence"), list) else []:
                c = str(concept).strip()
                if c and c not in bridge_concepts:
                    bridge_concepts.append(c)
                if len(bridge_concepts) >= 8:
                    break
            if len(bridge_concepts) >= 8:
                break
        for row in s.get("abstraction_rows", [])[:8]:
            if not isinstance(row, dict):
                continue
            label = str(row.get("abstraction_label", "")).strip()
            if label and label not in abstraction_concepts:
                abstraction_concepts.append(label)
            definitional = row.get("definitional_profile", {}) if isinstance(row.get("definitional_profile"), dict) else {}
            necessary = definitional.get("necessary_attributes", []) if isinstance(definitional.get("necessary_attributes"), list) else []
            for attr in necessary[:2]:
                if not isinstance(attr, dict):
                    continue
                text = str(attr.get("attribute", "")).strip()
                if text and text not in definitional_focus:
                    definitional_focus.append(text)
            counterfactuals = row.get("counterfactual_probes", []) if isinstance(row.get("counterfactual_probes"), list) else []
            for probe in counterfactuals[:2]:
                if not isinstance(probe, dict):
                    continue
                text = str(probe.get("intervention", "")).strip()
                if text and text not in counterfactual_focus:
                    counterfactual_focus.append(text)
        strategy = {
            "strategy_id": f"strat.{i:03d}",
            "name": _strategy_name(s["phase"], s["entry_id"]),
            "phase": s["phase"],
            "anchor_statement_id": s["entry_id"],
            "anchor_concepts": anchor_concepts,
            "bridge_concepts": bridge_concepts,
            "abstraction_concepts": abstraction_concepts[:8],
            "definitional_focus": definitional_focus[:6],
            "counterfactual_focus": counterfactual_focus[:4],
            "strategy_score": round(float(s["selection_score"]), 4),
            "base_strength": round(float(s["base_strength"]), 4),
            "concept_fertility": round(float(s.get("concept_fertility", 0.0)), 4),
            "fertility_components": s.get("fertility_components", {}),
            "novelty_rationale": (
                "Selected to maximize phase diversity and minimize anchor overlap while preserving high support strength."
            ),
            "bridge_ids": s["bridge_ids"][:5],
            "hypothesis_ids": s["hypothesis_ids"][:6],
            "hypothesis_status_summary": s.get("hypothesis_status_summary", {}),
            "execution_protocol": [
                f"Anchor on {s['entry_id']} and restate objective as conditional entailment gain.",
                "Run kb-abduce with hypothesis seeds from `hypothesis_ids`.",
                "Test top 1-2 `bridge_ids` in scratch dependencies and run kb-deduce.",
                "Retain only assumptions that increase derivable consequences without contradiction.",
                "Record deltas and feed surviving artifacts to next strategy round.",
            ],
        }
        strategies.append(strategy)

    coherence_profile = coherence.get("coherence_profile", {}) if isinstance(coherence.get("coherence_profile"), dict) else {}
    novelty_prompt = _build_dynamic_novelty_prompt(
        strategies,
        coherence_profile=coherence_profile,
        coherence_index=coherence_index,
        top_abstractions=conjectures.get("abstraction_conjectures", []) if isinstance(conjectures, dict) else [],
    )

    return {
        "metadata": {
            "input_entrypoints": len(entrypoints.get("ranked_entrypoints", [])),
            "input_pathways": len(pathways.get("pathways", [])),
            "input_bridges": len(bridges.get("bridge_programs", [])),
            "input_conjectures": len(conjectures.get("abstraction_conjectures", []))
            if isinstance(conjectures.get("abstraction_conjectures"), list)
            else 0,
            "input_hypotheses": len(phyp.get("hypotheses", [])),
            "input_coherence_signals": len(coherence_index),
            "indexed_hypotheses": len(hypothesis_lookup),
            "strategy_count": len(strategies),
            "selection_policy": "diversity + fertility aware greedy selection",
            "prompt_policy": "dynamic diagnostics-conditioned novelty synthesis",
        },
        "strategies": strategies,
        "novelty_maximizing_prompt": novelty_prompt,
    }


def _to_markdown(report: dict[str, Any]) -> str:
    """
    Relevance: Operates within the proof strategy design layer.
    Concept: Rendering internal outputs into human-readable artifacts.
    Contribution: Improves interpretability by exposing machine results in analyst-friendly form.
    """

    lines = []
    lines.append("# Proof Strategy Portfolio")
    lines.append("")

    meta = report.get("metadata", {})
    lines.append("## Stats")
    lines.append("")
    lines.append(f"- Strategies: {meta.get('strategy_count', 0)}")
    lines.append(f"- Pathways used: {meta.get('input_pathways', 0)}")
    lines.append(f"- Bridges used: {meta.get('input_bridges', 0)}")
    lines.append(f"- Conjectured abstractions used: {meta.get('input_conjectures', 0)}")
    lines.append(f"- Hypotheses used: {meta.get('input_hypotheses', 0)}")
    lines.append(f"- Coherence signals used: {meta.get('input_coherence_signals', 0)}")
    lines.append("")

    lines.append("## Strategies")
    lines.append("")
    lines.append("| strategy_id | name | phase | anchor | score | fertility | anchor_concepts |")
    lines.append("|---|---|---|---|---|---|---|")
    for s in report.get("strategies", []):
        lines.append(
            f"| {s['strategy_id']} | {s['name']} | {s['phase']} | {s['anchor_statement_id']} | {s['strategy_score']} | {s.get('concept_fertility', 0.0)} | {', '.join(s.get('anchor_concepts', [])[:4])} |"
        )
    lines.append("")

    for s in report.get("strategies", []):
        lines.append(f"### {s['strategy_id']} - {s['name']}")
        lines.append(f"- Anchor: {s['anchor_statement_id']}")
        lines.append(f"- Phase: {s['phase']}")
        lines.append(f"- Score: {s['strategy_score']}")
        lines.append(f"- Concept fertility: {s.get('concept_fertility', 0.0)}")
        if s.get("anchor_concepts"):
            lines.append(f"- Anchor concepts: {', '.join(s.get('anchor_concepts', [])[:8])}")
        if s.get("bridge_concepts"):
            lines.append(f"- Bridge concepts: {', '.join(s.get('bridge_concepts', [])[:8])}")
        if s.get("abstraction_concepts"):
            lines.append(f"- Abstraction concepts: {', '.join(s.get('abstraction_concepts', [])[:8])}")
        if s.get("definitional_focus"):
            lines.append(f"- Definitional focus: {', '.join(s.get('definitional_focus', [])[:6])}")
        if s.get("counterfactual_focus"):
            lines.append(f"- Counterfactual focus: {', '.join(s.get('counterfactual_focus', [])[:4])}")
        lines.append(f"- Bridges: {', '.join(s.get('bridge_ids', [])) if s.get('bridge_ids') else 'none'}")
        lines.append(f"- Hypotheses: {', '.join(s.get('hypothesis_ids', [])) if s.get('hypothesis_ids') else 'none'}")
        components = s.get("fertility_components", {}) if isinstance(s.get("fertility_components"), dict) else {}
        if components:
            lines.append("- Fertility components: " + ", ".join(f"{k}={v}" for k, v in components.items()))
        hss = s.get("hypothesis_status_summary", {}) if isinstance(s.get("hypothesis_status_summary"), dict) else {}
        if hss:
            lines.append(
                "- Hypothesis status summary: "
                + ", ".join(f"{k}={v}" for k, v in hss.items() if int(v) > 0)
            )
        lines.append("- Execution protocol:")
        for step in s.get("execution_protocol", []):
            lines.append(f"  - {step}")
        lines.append("")

    lines.append("## Novelty-Maximizing Prompt")
    lines.append("")
    lines.append("```text")
    lines.append(report.get("novelty_maximizing_prompt", ""))
    lines.append("```")

    return "\n".join(lines) + "\n"


def main() -> int:
    """
    Relevance: Operates within the proof strategy design layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds parsing, computation, and artifact emission into a reproducible script execution.
    """

    logger = ReasoningLogger("kb-novel-proof-strategist")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--entrypoints", required=True)
    ap.add_argument("--pathways", required=True)
    ap.add_argument("--bridges", required=True)
    ap.add_argument("--phyp", required=True)
    ap.add_argument("--coherence-report")
    ap.add_argument("--conjectures")
    ap.add_argument("--top-k", type=int, default=6)
    ap.add_argument("--output-json")
    ap.add_argument("--output-md")
    ap.add_argument("--output-prompt")
    args = ap.parse_args()
    logger.step(
        "Parsed novel-proof-strategist arguments",
        "\n".join(
            [
                f"entrypoints={args.entrypoints}",
                f"pathways={args.pathways}",
                f"bridges={args.bridges}",
                f"phyp={args.phyp}",
                f"coherence_report={args.coherence_report or ''}",
                f"conjectures={args.conjectures or ''}",
                f"top_k={args.top_k}",
                f"output_json={args.output_json or ''}",
                f"output_md={args.output_md or ''}",
                f"output_prompt={args.output_prompt or ''}",
            ]
        ),
    )

    entrypoints_path = Path(args.entrypoints)
    pathways_path = Path(args.pathways)
    bridges_path = Path(args.bridges)
    phyp_path = Path(args.phyp)
    coherence_path = Path(args.coherence_report) if args.coherence_report else None
    conjectures_path = Path(args.conjectures) if args.conjectures else None

    for p in [entrypoints_path, pathways_path, bridges_path, phyp_path]:
        if not p.exists():
            log_path = logger.finalize("error", summary=f"Missing input: {p}")
            print(f"[LOG] {log_path}", file=sys.stderr)
            raise SystemExit(f"[ERROR] Missing input: {p}")
    if coherence_path and not coherence_path.exists():
        log_path = logger.finalize("error", summary=f"Missing input: {coherence_path}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Missing input: {coherence_path}")
    if conjectures_path and not conjectures_path.exists():
        log_path = logger.finalize("error", summary=f"Missing input: {conjectures_path}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Missing input: {conjectures_path}")
    try:
        entrypoints = validate_entrypoints(json.loads(entrypoints_path.read_text(encoding="utf-8")), name="entrypoints")
        pathways = validate_pathways(json.loads(pathways_path.read_text(encoding="utf-8")), name="pathways")
        bridges = validate_bridges(json.loads(bridges_path.read_text(encoding="utf-8")), name="bridges")
        phyp = validate_phyp(yaml.safe_load(phyp_path.read_text(encoding="utf-8")), name="phyp")
        coherence = (
            validate_coherence_report(json.loads(coherence_path.read_text(encoding="utf-8")), name="coherence")
            if coherence_path
            else {}
        )
        conjectures = (
            validate_conjecture_report(json.loads(conjectures_path.read_text(encoding="utf-8")), name="conjectures")
            if conjectures_path
            else {}
        )

        report = _build(
            entrypoints=entrypoints,
            pathways=pathways,
            bridges=bridges,
            phyp=phyp,
            coherence=coherence,
            conjectures=conjectures,
            top_k=max(1, args.top_k),
        )
        strategies = report.get("strategies", []) if isinstance(report.get("strategies"), list) else []
        logger.step(
            "Strategy concept trace",
            "\n".join(
                [
                    "top_strategies="
                    + "; ".join(
                        f"{str(item.get('strategy_id', '')).strip()}:{str(item.get('anchor_statement_id', '')).strip()}:{float(item.get('strategy_score', 0.0) or 0.0):.4f}:[{', '.join(item.get('anchor_concepts', [])[:3])}]:[{', '.join(item.get('abstraction_concepts', [])[:2])}]"
                        for item in strategies[:6]
                        if isinstance(item, dict) and str(item.get("strategy_id", "")).strip()
                    ),
                    "novelty_prompt_preview="
                    + str(report.get("novelty_maximizing_prompt", "")).strip().replace("\n", " ")[:220],
                ]
            ),
        )

        if args.output_json:
            out = Path(args.output_json)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"[OK] Wrote JSON: {out}")
            logger.add_output("strategy_report_json", out)

        md = _to_markdown(report)
        if args.output_md:
            out = Path(args.output_md)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(md, encoding="utf-8")
            print(f"[OK] Wrote Markdown: {out}")
            logger.add_output("strategy_report_md", out)

        if args.output_prompt:
            out = Path(args.output_prompt)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(report.get("novelty_maximizing_prompt", "") + "\n", encoding="utf-8")
            print(f"[OK] Wrote Prompt: {out}")
            logger.add_output("novelty_maximizing_prompt", out)

        print(f"[OK] Strategies: {len(report.get('strategies', []))}")
        if report.get("strategies"):
            top = report["strategies"][0]
            print(f"[OK] Top strategy: {top['strategy_id']} ({top['anchor_statement_id']}, score={top['strategy_score']})")
            logger.step(
                "Selected top strategy",
                "\n".join(
                    [
                        f"strategy_id={top['strategy_id']}",
                        f"anchor={top['anchor_statement_id']}",
                        f"score={top['strategy_score']}",
                    ]
                ),
            )

        log_path = logger.finalize(
            "success",
            summary=f"Generated {len(report.get('strategies', []))} proof strategies.",
        )
        print(f"[LOG] {log_path}")
        return 0
    except Exception as exc:
        log_path = logger.finalize("error", summary=f"Strategy generation failed: {exc}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
