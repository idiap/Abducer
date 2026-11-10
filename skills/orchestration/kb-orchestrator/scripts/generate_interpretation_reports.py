#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""Generate human-readable reports interpreting reasoning and discovery artifacts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from reasoning_log import ReasoningLogger

GENERIC_MATH_TAGS = {
    "lower-bound",
    "hardness-vs-randomness",
    "circuit-complexity",
    "proof-complexity",
    "algebraic-method",
    "nonuniform-circuits",
    "uniform-model",
    "oracle-model",
    "randomness",
    "meta-complexity",
}


def _safe_float(value: Any, default: float = 0.0) -> float:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Defensive conversion/parsing to keep scoring and reporting robust.
    Contribution: Reduces runtime ambiguity and prevents malformed artifacts from destabilizing the workflow.
    """

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_int(value: Any, default: int = 0) -> int:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Defensive conversion/parsing to keep scoring and reporting robust.
    Contribution: Reduces runtime ambiguity and prevents malformed artifacts from destabilizing the workflow.
    """

    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _load_json(path: Path) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Provides clean, typed inputs so downstream reasoning steps remain auditable.
    """

    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if isinstance(payload, dict):
        return payload
    return {}


def _present(payload: dict[str, Any]) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    return "yes" if payload else "no"


def _top_rows(rows: list[dict[str, Any]], key: str, n: int = 5, reverse: bool = True) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    items = [r for r in rows if isinstance(r, dict)]
    items.sort(key=lambda x: _safe_float(x.get(key), 0.0), reverse=reverse)
    return items[: max(0, n)]


def _compact_text(value: Any, limit: int = 220) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Produces concise concept labels for human-readable reports.
    """

    text = " ".join(str(value or "").split())
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 3)].rstrip() + "..."


def _concept_weight(concept: str) -> int:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Typed prioritization of concept labels by inferential specificity.
    Contribution: Keeps human-readable reports focused on theorem-level mathematical content instead of broad topical buckets.
    """

    text = str(concept).strip()
    if not text:
        return 0
    weight = 1
    lower = text.lower()
    if lower in GENERIC_MATH_TAGS:
        weight -= 1
    if "implies" in lower or "collapse" in lower or "separation" in lower:
        weight += 3
    if "not-in" in lower or "not-equal" in lower or "hardness" in lower or "complete" in lower:
        weight += 2
    if lower.endswith("-lower-bound") or "-lower-bound" in lower:
        weight += 2
    if any(token in lower for token in ("mcsp", "pit", "ips", "permanent", "acc0", "ac0", "frege", "nexp", "ph")):
        weight += 1
    return max(0, weight)


def _profile_terms(profile: Any) -> list[str]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Extraction of structured mathematical labels from typed connector profiles.
    Contribution: Surfaces theorem-level antecedents, consequences, implications, and invariants in interpretation artifacts.
    """

    if not isinstance(profile, dict):
        return []
    ordered_terms: list[str] = []
    for key in (
        "implication_signatures",
        "consequence_signatures",
        "antecedent_signatures",
        "claim_signatures",
        "model_signatures",
        "reduction_signatures",
    ):
        values = profile.get(key, [])
        if not isinstance(values, list):
            continue
        for item in values:
            text = str(item).strip()
            if text:
                ordered_terms.append(text)
    return ordered_terms


def _collect_concept_trace(
    entrypoints: dict[str, Any],
    pathways: dict[str, Any],
    hardness: dict[str, Any],
) -> dict[str, Any]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Construction of derived graph/model structures used by later stages.
    Contribution: Builds a cross-artifact concept communication snapshot.
    """

    tracks = entrypoints.get("concept_tracks", []) if isinstance(entrypoints.get("concept_tracks"), list) else []
    pathways_rows = pathways.get("pathways", []) if isinstance(pathways.get("pathways"), list) else []
    hardness_comm = hardness.get("concept_communication", {}) if isinstance(hardness.get("concept_communication"), dict) else {}

    phase_tracks: list[dict[str, Any]] = []
    for track in tracks[:6]:
        if not isinstance(track, dict):
            continue
        anchors = []
        for row in track.get("top_entrypoints", []) if isinstance(track.get("top_entrypoints"), list) else []:
            if not isinstance(row, dict):
                continue
            sid = str(row.get("statement_id", "")).strip()
            if sid:
                anchors.append(sid)
        phase_tracks.append(
            {
                "phase": str(track.get("phase", "Unspecified")).strip() or "Unspecified",
                "anchor_count": len(anchors),
                "anchors": anchors[:4],
            }
        )

    pathway_trace: list[dict[str, Any]] = []
    for row in pathways_rows[:6]:
        if not isinstance(row, dict):
            continue
        pathway_trace.append(
            {
                "path_id": str(row.get("path_id", "")).strip(),
                "entry_statement_id": str(row.get("entry_statement_id", "")).strip(),
                "entry_phase": str(row.get("entry_phase", "Unspecified")).strip() or "Unspecified",
                "pathway_score": _safe_float(row.get("pathway_score", 0.0)),
                "goal": _compact_text(row.get("goal", ""), 180),
            }
        )

    return {
        "phase_tracks": phase_tracks,
        "pathway_trace": pathway_trace,
        "hardness_phase_pressure": hardness_comm.get("phase_pressure", {}) if isinstance(hardness_comm.get("phase_pressure"), dict) else {},
        "hardness_entrypoint_concepts": hardness_comm.get("top_entrypoint_concepts", [])
        if isinstance(hardness_comm.get("top_entrypoint_concepts"), list)
        else [],
    }


def _collect_math_surface(analysis: dict[str, Any]) -> list[str]:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Summarizes the dominant mathematical concepts currently driving reasoning.
    """

    counter: Counter[str] = Counter()
    for row in analysis.get("top_interventions", []) if isinstance(analysis.get("top_interventions"), list) else []:
        if not isinstance(row, dict):
            continue
        for concept in row.get("concept_focus", []) if isinstance(row.get("concept_focus"), list) else []:
            c = str(concept).strip()
            if c:
                counter[c] += 2 * _concept_weight(c)
        for concept in _profile_terms(row.get("concept_profile")):
            counter[concept] += 3 * _concept_weight(concept)
    for row in (analysis.get("connection_candidates", []) if isinstance(analysis.get("connection_candidates"), list) else [])[:30]:
        if not isinstance(row, dict):
            continue
        for concept in row.get("concept_evidence", []) if isinstance(row.get("concept_evidence"), list) else []:
            c = str(concept).strip()
            if c:
                counter[c] += _concept_weight(c)
        for concept in _profile_terms(row.get("from_profile")) + _profile_terms(row.get("to_profile")):
            counter[concept] += 2 * _concept_weight(concept)
    return [concept for concept, score in counter.most_common(16) if score > 0][:12]


def _process_report(
    kb: str,
    artifacts_dir: Path,
    analysis: dict[str, Any],
    coherence: dict[str, Any],
    entrypoints: dict[str, Any],
    pathways: dict[str, Any],
    hardness: dict[str, Any],
    bridges: dict[str, Any],
    strategies: dict[str, Any],
    proof_sketches: dict[str, Any],
    hypothesis_eval: dict[str, Any],
    hypothesis_loop: dict[str, Any],
    revision: dict[str, Any],
    reasoning_dynamics: dict[str, Any] | None = None,
    conjectures: dict[str, Any] | None = None,
) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    lines: list[str] = []
    now = dt.datetime.now(dt.UTC).isoformat()

    lines.append("# Reasoning Process Report")
    lines.append("")
    lines.append("This report explains what each reasoning stage produced, in plain language.")
    lines.append("")
    lines.append("## Run Context")
    lines.append("")
    lines.append(f"- Generated (UTC): {now}")
    lines.append(f"- KB: {kb or 'unknown'}")
    lines.append(f"- Artifacts directory: {artifacts_dir}")
    lines.append("")

    analysis_stats = analysis.get("stats", {}) if isinstance(analysis.get("stats"), dict) else {}
    coherence_profile = coherence.get("coherence_profile", {}) if isinstance(coherence.get("coherence_profile"), dict) else {}
    eval_summary = hypothesis_eval.get("summary", {}) if isinstance(hypothesis_eval.get("summary"), dict) else {}
    loop_summary = hypothesis_loop.get("final_summary", {}) if isinstance(hypothesis_loop.get("final_summary"), dict) else {}
    rev_summary = revision.get("revision_summary", {}) if isinstance(revision.get("revision_summary"), dict) else {}
    conjectures = conjectures or {}
    dynamics_summary = (
        reasoning_dynamics.get("summary", {})
        if isinstance(reasoning_dynamics, dict) and isinstance(reasoning_dynamics.get("summary"), dict)
        else {}
    )
    concept_trace = _collect_concept_trace(entrypoints=entrypoints, pathways=pathways, hardness=hardness)
    phase_tracks = concept_trace.get("phase_tracks", []) if isinstance(concept_trace.get("phase_tracks"), list) else []
    hardness_phase_pressure = (
        concept_trace.get("hardness_phase_pressure", {})
        if isinstance(concept_trace.get("hardness_phase_pressure"), dict)
        else {}
    )
    math_surface = _collect_math_surface(analysis)

    stage_rows = [
        (
            "Relational Scan",
            _present(analysis),
            (
                f"{_safe_int(analysis_stats.get('statement_count'))} statements, "
                f"{len(analysis.get('connection_candidates', []) if isinstance(analysis.get('connection_candidates'), list) else [])} candidate links"
                if analysis
                else "artifact not available"
            ),
        ),
        (
            "Coherence Evaluation",
            _present(coherence),
            (
                f"global coherence={_safe_float(coherence_profile.get('global_coherence')):.4f}, "
                f"{len(coherence.get('hypothesis_coherence', []) if isinstance(coherence.get('hypothesis_coherence'), list) else [])} hypothesis signals"
                if coherence
                else "artifact not available"
            ),
        ),
        (
            "Entrypoint Ranking",
            _present(entrypoints),
            (
                f"{len(entrypoints.get('ranked_entrypoints', []) if isinstance(entrypoints.get('ranked_entrypoints'), list) else [])} ranked entry points"
                if entrypoints
                else "artifact not available"
            ),
        ),
        (
            "Pathway Synthesis",
            _present(pathways),
            (
                f"{len(pathways.get('pathways', []) if isinstance(pathways.get('pathways'), list) else [])} pathways"
                if pathways
                else "artifact not available"
            ),
        ),
        (
            "Hardness Articulation",
            _present(hardness),
            (
                f"{len(hardness.get('essential_elements', []) if isinstance(hardness.get('essential_elements'), list) else [])} hardness elements, "
                f"{len(hardness.get('anti_barrier_programs', []) if isinstance(hardness.get('anti_barrier_programs'), list) else [])} anti-barrier programs"
                if hardness
                else "artifact not available"
            ),
        ),
        (
            "Bridge Planning",
            _present(bridges),
            (
                f"{len(bridges.get('bridge_programs', []) if isinstance(bridges.get('bridge_programs'), list) else [])} bridge programs"
                if bridges
                else "artifact not available"
            ),
        ),
        (
            "Conjecture Mode",
            _present(conjectures),
            (
                f"{len(conjectures.get('abstraction_conjectures', []) if isinstance(conjectures.get('abstraction_conjectures'), list) else [])} abstraction conjectures"
                if conjectures
                else "artifact not available"
            ),
        ),
        (
            "Strategy Design",
            _present(strategies),
            (
                f"{len(strategies.get('strategies', []) if isinstance(strategies.get('strategies'), list) else [])} strategies"
                if strategies
                else "artifact not available"
            ),
        ),
        (
            "Proof Sketching",
            _present(proof_sketches),
            (
                f"{len(proof_sketches.get('proof_sketches', []) if isinstance(proof_sketches.get('proof_sketches'), list) else [])} proof sketches"
                if proof_sketches
                else "artifact not available"
            ),
        ),
        (
            "Hypothesis Evaluation",
            _present(hypothesis_eval),
            (
                "verdict counts: " + json.dumps(eval_summary.get("verdict_counts", {}), ensure_ascii=False)
                if hypothesis_eval
                else "artifact not available"
            ),
        ),
        (
            "Hypothesis Loop",
            _present(hypothesis_loop),
            (
                f"rounds executed={_safe_int(hypothesis_loop.get('metadata', {}).get('rounds_executed', 0) if isinstance(hypothesis_loop.get('metadata'), dict) else 0)}, "
                f"open={_safe_int(loop_summary.get('open_count', 0))}"
                if hypothesis_loop
                else "artifact not available"
            ),
        ),
        (
            "Revision Loop",
            _present(revision),
            (
                f"{len(revision.get('revision_actions', []) if isinstance(revision.get('revision_actions'), list) else [])} revision actions, "
                f"priority program size={len(revision.get('priority_program', []) if isinstance(revision.get('priority_program'), list) else [])}"
                if revision
                else "artifact not available"
            ),
        ),
        (
            "Reasoning Dynamics",
            _present(reasoning_dynamics or {}),
            (
                f"states={_safe_int(dynamics_summary.get('state_count', 0))}, "
                f"timespan={_safe_float(dynamics_summary.get('time_span_seconds', 0.0)):.3f}s, "
                f"concept updates={_safe_int(dynamics_summary.get('concept_evolution', {}).get('update_count', 0) if isinstance(dynamics_summary.get('concept_evolution'), dict) else 0)}"
                if dynamics_summary
                else "artifact not available"
            ),
        ),
    ]

    lines.append("## Stage Snapshot")
    lines.append("")
    lines.append("| Stage | Artifact Present | Human Summary |")
    lines.append("|---|---|---|")
    for stage, present, summary in stage_rows:
        lines.append(f"| {stage} | {present} | {summary} |")
    lines.append("")

    lines.append("## What To Read First")
    lines.append("")
    paper_argument = artifacts_dir / "paper-style-argument.md"
    if coherence:
        lines.append("1. Read `coherence-report.md` to understand which hypotheses help or hurt global theory fit.")
    else:
        lines.append("1. Coherence report is missing; run `coherence-eval` first to get global theory-fit diagnostics.")
    if bridges or conjectures or strategies or proof_sketches:
        lines.append("2. Read `bridge-plan.md`, `concept-gap-abstractions.md`, `proof-strategies.md`, `proof-sketches.md`, and `paper-style-argument.md` to see which bridges matter, which abstractions are missing, which strategies follow, and how the strongest conjectures translate into a paper-style mathematical route.")
    else:
        lines.append("2. Bridge/conjecture/strategy artifacts are missing; run `bridge-plan`, `conjecture`, `strategies`, and `proof-sketch` to surface prioritized discovery programs.")
    if hypothesis_loop or revision:
        lines.append("3. Read `hypothesis-refutation-loop.md` and `revision-loop.md` to see why progress stalled and what to repair next.")
    else:
        lines.append("3. Loop/revision artifacts are missing; run `hypothesis-loop` and `revision-loop` for convergence diagnostics.")
    if not paper_argument.exists():
        lines.append("4. `paper-style-argument.md` is missing; rerun `proof-sketch` to render the strongest final pathway as a paper-style conditional argument.")
    lines.append("")

    lines.append("## Process Interpretation")
    lines.append("")
    if analysis:
        lines.append(
            f"- The relational scan found {_safe_int(analysis_stats.get('statement_count'))} usable statements with "
            f"{len(analysis.get('connection_candidates', [])) if isinstance(analysis.get('connection_candidates'), list) else 0} bridge candidates."
        )
    if coherence:
        lines.append(
            f"- Coherence baseline is {_safe_float(coherence_profile.get('global_coherence')):.4f}; "
            "use this as the global quality anchor when retaining hypotheses."
        )
    if hypothesis_eval:
        lines.append(
            "- Hypothesis evaluation currently yields "
            + json.dumps(eval_summary.get("verdict_counts", {}), ensure_ascii=False)
            + "; unresolved items should not be treated as failures, only as pending work."
        )
    if revision:
        lines.append(
            f"- Revision loop proposes {_safe_int(rev_summary.get('revision_count', 0) or len(revision.get('revision_actions', [])))} repairs to change the search regime, not just rerun the same loop."
        )
    if conjectures:
        lines.append(
            f"- Conjecture mode identified {len(conjectures.get('abstraction_conjectures', []) if isinstance(conjectures.get('abstraction_conjectures'), list) else [])} bridge-filling abstraction proposals, making missing mathematical objects explicit."
        )
    if proof_sketches:
        lines.append(
            f"- Proof-sketch mode translated {len(proof_sketches.get('proof_sketches', []) if isinstance(proof_sketches.get('proof_sketches'), list) else [])} conjectures into structured proof programs with obligations, barrier checks, and abort conditions."
        )
    if dynamics_summary:
        graph_growth = dynamics_summary.get("graph_growth", {}) if isinstance(dynamics_summary.get("graph_growth"), dict) else {}
        lines.append(
            f"- Reasoning dynamics tracked {_safe_int(dynamics_summary.get('state_count', 0))} states; "
            f"graph growth {_safe_int(graph_growth.get('nodes_initial', 0))}->{_safe_int(graph_growth.get('nodes_final', 0))} nodes and "
            f"{_safe_int(graph_growth.get('edges_initial', 0))}->{_safe_int(graph_growth.get('edges_final', 0))} edges."
        )
    if phase_tracks:
        top_track = phase_tracks[0]
        lines.append(
            f"- Concept communication currently concentrates on phase '{top_track.get('phase', 'Unspecified')}' "
            f"with anchors: {', '.join(top_track.get('anchors', [])[:3]) or '(none)'}."
        )
    elif hardness_phase_pressure:
        top_phase = sorted(hardness_phase_pressure.items(), key=lambda kv: int(kv[1]), reverse=True)[0]
        lines.append(f"- Concept communication pressure is highest on phase '{top_phase[0]}' ({top_phase[1]} top anchors).")
    if not any([analysis, coherence, hypothesis_eval, revision]):
        lines.append("- Not enough artifacts were found to interpret the reasoning process.")
    lines.append("")

    lines.append("## Concept Communication Snapshot")
    lines.append("")
    if hardness_phase_pressure:
        pressure = ", ".join(
            f"{phase}={count}"
            for phase, count in sorted(hardness_phase_pressure.items(), key=lambda kv: int(kv[1]), reverse=True)
        )
        lines.append(f"- Hardness phase pressure: {pressure}")
    if phase_tracks:
        lines.append("- Concept tracks from entrypoint ranking:")
        for track in phase_tracks[:5]:
            lines.append(
                f"  - {track.get('phase', 'Unspecified')}: "
                f"{', '.join(track.get('anchors', [])[:4]) or '(no anchors)'}"
            )
    else:
        lines.append("- Concept tracks from entrypoint ranking: unavailable")
    if math_surface:
        lines.append("- Dominant mathematical concepts in this run: " + ", ".join(math_surface))
    lines.append("")

    lines.append("## Conjecture Snapshot")
    lines.append("")
    top_conjectures = _top_rows(
        conjectures.get("abstraction_conjectures", []) if isinstance(conjectures.get("abstraction_conjectures"), list) else [],
        "priority",
        n=5,
    )
    if not top_conjectures:
        lines.append("- No conjectured bridge-filling abstractions are available.")
    for row in top_conjectures:
        lines.append(
            f"- `{row.get('conjecture_id', '')}` [{row.get('abstraction_type', '')}] "
            f"{row.get('abstraction_label', '')} (priority {_safe_float(row.get('priority', 0.0)):.4f})"
        )
        lines.append(
            f"  - gap={row.get('gap_target', '')}; consequence={row.get('target_consequence_schema', '')}; invariant={row.get('preserved_invariant', '')}"
        )
        definitional = row.get("definitional_profile", {}) if isinstance(row.get("definitional_profile"), dict) else {}
        necessary = definitional.get("necessary_attributes", []) if isinstance(definitional.get("necessary_attributes"), list) else []
        counterfactuals = row.get("counterfactual_probes", []) if isinstance(row.get("counterfactual_probes"), list) else []
        if necessary:
            lines.append(
                "  - necessary="
                + ", ".join(str(attr.get("attribute", "")).strip() for attr in necessary[:2] if isinstance(attr, dict))
            )
        if counterfactuals:
            lines.append(
                "  - counterfactual="
                + str(counterfactuals[0].get("intervention", "") if isinstance(counterfactuals[0], dict) else "")
            )
    lines.append("")

    lines.append("## Proof Sketch Snapshot")
    lines.append("")
    top_sketches = _top_rows(
        proof_sketches.get("proof_sketches", []) if isinstance(proof_sketches.get("proof_sketches"), list) else [],
        "sketch_score",
        n=5,
    )
    if not top_sketches:
        lines.append("- No proof sketches are available.")
    for row in top_sketches:
        lines.append(
            f"- `{row.get('sketch_id', '')}` [{row.get('proof_strategy_family', '')}] "
            f"{row.get('conjecture_id', '')} via {row.get('strategy_id', '')} "
            f"(score {_safe_float(row.get('sketch_score', 0.0)):.4f})"
        )
        lines.append(
            f"  - target={row.get('target_consequence_schema', '')}; invariant={row.get('preserved_invariant', '')}; barrier={row.get('barrier_scope', '')}"
        )
        obligations = row.get("proof_obligations", []) if isinstance(row.get("proof_obligations"), list) else []
        if obligations:
            lines.append(
                "  - first obligation="
                + str(obligations[0].get("requirement", "") if isinstance(obligations[0], dict) else "")
            )
        counterfactual = row.get("counterfactual_test", {}) if isinstance(row.get("counterfactual_test"), dict) else {}
        if counterfactual:
            lines.append(
                "  - sketch counterfactual="
                + str(counterfactual.get("intervention", ""))
            )
    if (artifacts_dir / "paper-style-argument.md").exists():
        lines.append("- `paper-style-argument.md` renders the top sketch as a paper-style conditional argument with a proposition, lemmas, and proof.")
    lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _discovery_report(
    kb: str,
    artifacts_dir: Path,
    analysis: dict[str, Any],
    coherence: dict[str, Any],
    entrypoints: dict[str, Any],
    pathways: dict[str, Any],
    hardness: dict[str, Any],
    bridges: dict[str, Any],
    strategies: dict[str, Any],
    proof_sketches: dict[str, Any],
    hypothesis_eval: dict[str, Any],
    hypothesis_loop: dict[str, Any],
    revision: dict[str, Any],
    reasoning_dynamics: dict[str, Any] | None = None,
    conjectures: dict[str, Any] | None = None,
) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    lines: list[str] = []
    now = dt.datetime.now(dt.UTC).isoformat()

    lines.append("# Discovery Interpretation Report")
    lines.append("")
    lines.append("This report narrates the discovery state in human-readable terms.")
    lines.append("")
    lines.append("## Context")
    lines.append("")
    lines.append(f"- Generated (UTC): {now}")
    lines.append(f"- KB: {kb or 'unknown'}")
    lines.append(f"- Artifacts directory: {artifacts_dir}")
    lines.append("")

    analysis_stats = analysis.get("stats", {}) if isinstance(analysis.get("stats"), dict) else {}
    coherence_profile = coherence.get("coherence_profile", {}) if isinstance(coherence.get("coherence_profile"), dict) else {}
    loop_summary = hypothesis_loop.get("final_summary", {}) if isinstance(hypothesis_loop.get("final_summary"), dict) else {}
    conjectures = conjectures or {}
    dynamics_summary = (
        reasoning_dynamics.get("summary", {})
        if isinstance(reasoning_dynamics, dict) and isinstance(reasoning_dynamics.get("summary"), dict)
        else {}
    )
    concept_trace = _collect_concept_trace(entrypoints=entrypoints, pathways=pathways, hardness=hardness)
    math_surface = _collect_math_surface(analysis)

    lines.append("## Current Discovery Posture")
    lines.append("")
    lines.append(f"- Statement coverage in reasoning graph: {_safe_int(analysis_stats.get('statement_count', 0))}")
    lines.append(f"- Candidate conceptual/bridge links: {len(analysis.get('connection_candidates', []) if isinstance(analysis.get('connection_candidates'), list) else [])}")
    if coherence:
        lines.append(f"- Global coherence baseline: {_safe_float(coherence_profile.get('global_coherence', 0.0)):.4f}")
    else:
        lines.append("- Global coherence baseline: unavailable (coherence-report.json not found)")
    lines.append(f"- Open hypotheses after loop: {_safe_int(loop_summary.get('open_count', 0))}")
    lines.append(
        f"- Bridge-filling abstractions conjectured: {len(conjectures.get('abstraction_conjectures', []) if isinstance(conjectures.get('abstraction_conjectures'), list) else [])}"
    )
    lines.append("")

    lines.append("## Concept Communication Trace")
    lines.append("")
    phase_tracks = concept_trace.get("phase_tracks", []) if isinstance(concept_trace.get("phase_tracks"), list) else []
    hardness_phase_pressure = (
        concept_trace.get("hardness_phase_pressure", {})
        if isinstance(concept_trace.get("hardness_phase_pressure"), dict)
        else {}
    )
    hardness_entrypoint_concepts = (
        concept_trace.get("hardness_entrypoint_concepts", [])
        if isinstance(concept_trace.get("hardness_entrypoint_concepts"), list)
        else []
    )
    if hardness_phase_pressure:
        lines.append(
            "- Hardness phase pressure: "
            + ", ".join(
                f"{phase}={count}"
                for phase, count in sorted(hardness_phase_pressure.items(), key=lambda kv: int(kv[1]), reverse=True)
            )
        )
    if phase_tracks:
        lines.append("- Entrypoint concept tracks:")
        for track in phase_tracks[:6]:
            lines.append(
                f"  - {track.get('phase', 'Unspecified')}: "
                f"{', '.join(track.get('anchors', [])[:4]) or '(no anchors)'}"
            )
    if hardness_entrypoint_concepts:
        lines.append("- Hardness concept anchors:")
        for row in hardness_entrypoint_concepts[:6]:
            if not isinstance(row, dict):
                continue
            lines.append(
                f"  - {row.get('statement_id', '')} [{row.get('phase', 'Unspecified')}]: "
                f"{_compact_text(row.get('concept_label', ''), 140)}"
            )
    if not any([hardness_phase_pressure, phase_tracks, hardness_entrypoint_concepts]):
        lines.append("- No explicit concept communication trace found in current artifacts.")
    if math_surface:
        lines.append("- Dominant mathematical concepts in connector evidence: " + ", ".join(math_surface))
    lines.append("")

    lines.append("## Reasoning Dynamics Summary")
    lines.append("")
    if dynamics_summary:
        graph_growth = dynamics_summary.get("graph_growth", {}) if isinstance(dynamics_summary.get("graph_growth"), dict) else {}
        op_totals = dynamics_summary.get("operation_totals", {}) if isinstance(dynamics_summary.get("operation_totals"), dict) else {}
        concept = dynamics_summary.get("concept_evolution", {}) if isinstance(dynamics_summary.get("concept_evolution"), dict) else {}
        final_concept = concept.get("final_state", {}) if isinstance(concept.get("final_state"), dict) else {}
        lines.append(f"- States tracked: {_safe_int(dynamics_summary.get('state_count', 0))}")
        lines.append(f"- Time span (s): {_safe_float(dynamics_summary.get('time_span_seconds', 0.0)):.3f}")
        lines.append(
            f"- Graph growth: nodes {_safe_int(graph_growth.get('nodes_initial', 0))}->{_safe_int(graph_growth.get('nodes_final', 0))}, "
            f"edges {_safe_int(graph_growth.get('edges_initial', 0))}->{_safe_int(graph_growth.get('edges_final', 0))}"
        )
        lines.append(
            f"- Inferential operations: stage_started={_safe_int(op_totals.get('stage_started', 0))}, "
            f"stage_completed={_safe_int(op_totals.get('stage_completed', 0))}, "
            f"declared_output={_safe_int(op_totals.get('declared_output', 0))}, "
            f"emits_output={_safe_int(op_totals.get('emits_output', 0))}, "
            f"invokes_agent={_safe_int(op_totals.get('invokes_agent', 0))}"
        )
        if final_concept:
            lines.append(
                f"- Concept topology index: {_safe_float(final_concept.get('concept_topology_index', 0.0)):.4f}; "
                f"hypothesis_total={_safe_int(final_concept.get('hypothesis_total', 0))}"
            )
    else:
        lines.append("- Reasoning dynamics artifact not available.")
    lines.append("- Visualization artifacts:")
    lines.append(f"  - `{artifacts_dir / 'process-graph.html'}`")
    lines.append(f"  - `{artifacts_dir / 'reasoning-dynamics.html'}`")
    lines.append(f"  - `{artifacts_dir / 'reasoning-dynamics.md'}`")
    lines.append("")

    lines.append("## Highest-Informative Intervention Points")
    lines.append("")
    top_interventions = _top_rows(analysis.get("top_interventions", []) if isinstance(analysis.get("top_interventions"), list) else [], "score", n=6)
    if not top_interventions:
        lines.append("- No intervention ranking available.")
    for item in top_interventions:
        sid = str(item.get("statement_id", ""))
        score = _safe_float(item.get("score", 0.0))
        rationale = str(item.get("rationale", "")).strip()
        lines.append(f"- `{sid}` (score {score:.4f}): {rationale or 'High leverage statement in current graph.'}")
        focus = item.get("concept_focus", []) if isinstance(item.get("concept_focus"), list) else []
        if focus:
            lines.append(f"  - concepts: {', '.join(str(x) for x in focus[:6])}")
    lines.append("")

    lines.append("## Coherence-Sensitive Hypothesis Readout")
    lines.append("")
    coh_rows = coherence.get("hypothesis_coherence", []) if isinstance(coherence.get("hypothesis_coherence"), list) else []
    top_positive = sorted(
        [r for r in coh_rows if _safe_float(r.get("coherence_delta_global"), 0.0) >= 0.0],
        key=lambda x: (_safe_float(x.get("coherence_delta_global"), 0.0), _safe_float(x.get("explanatory_power_local"), 0.0)),
        reverse=True,
    )[:5]
    top_negative = sorted(
        [r for r in coh_rows if _safe_float(r.get("coherence_delta_global"), 0.0) < 0.0],
        key=lambda x: _safe_float(x.get("coherence_delta_global"), 0.0),
    )[:5]

    lines.append("Positive contributions (good retention candidates):")
    if not top_positive:
        lines.append("- none")
    for row in top_positive:
        lines.append(
            f"- `{row.get('hypothesis_id', '')}` [{row.get('kind', '')}] "
            f"coh_delta={_safe_float(row.get('coherence_delta_global')):.4f}, "
            f"expl={_safe_float(row.get('explanatory_power_local')):.4f}"
        )

    lines.append("")
    lines.append("Negative contributions (reformulate or demote):")
    if not top_negative:
        lines.append("- none")
    for row in top_negative:
        lines.append(
            f"- `{row.get('hypothesis_id', '')}` [{row.get('kind', '')}] "
            f"coh_delta={_safe_float(row.get('coherence_delta_global')):.4f}, "
            f"expl={_safe_float(row.get('explanatory_power_local')):.4f}"
        )
    lines.append("")

    lines.append("## Bridge and Strategy Interpretation")
    lines.append("")
    top_bridges = _top_rows(bridges.get("bridge_programs", []) if isinstance(bridges.get("bridge_programs"), list) else [], "bridge_score", n=5)
    if not top_bridges:
        lines.append("- No bridge programs available.")
    for b in top_bridges:
        lines.append(
            f"- `{b.get('bridge_id', '')}`: `{b.get('from_id', '')}` -> `{b.get('to_id', '')}` "
            f"({b.get('bridge_type', 'bridge')}, score {_safe_float(b.get('bridge_score')):.4f})."
        )
        commitment = b.get("inferential_commitment", {}) if isinstance(b.get("inferential_commitment"), dict) else {}
        if commitment:
            lines.append(
                f"  - antecedent={commitment.get('support_antecedent_schema', '') or 'unconditional'}; "
                f"consequence={commitment.get('target_consequence_schema', '') or 'statement-conclusion'}"
            )
            lines.append(
                f"  - invariant={commitment.get('preserved_invariant', '') or 'support-to-target interface'}; "
                f"barrier={commitment.get('barrier_scope', '') or 'none'}"
            )

    lines.append("")
    top_strategies = _top_rows(strategies.get("strategies", []) if isinstance(strategies.get("strategies"), list) else [], "strategy_score", n=4)
    if top_strategies:
        lines.append("Most promising strategy anchors:")
    else:
        lines.append("- No strategy portfolio available.")
    for s in top_strategies:
        fert = _safe_float(s.get("concept_fertility", 0.0))
        lines.append(
            f"- `{s.get('strategy_id', '')}` around `{s.get('anchor_statement_id', '')}`: "
            f"score {_safe_float(s.get('strategy_score')):.4f}, concept fertility {fert:.4f}."
        )
    lines.append("")

    lines.append("## Proof Sketch Interpretation")
    lines.append("")
    top_sketches = _top_rows(
        proof_sketches.get("proof_sketches", []) if isinstance(proof_sketches.get("proof_sketches"), list) else [],
        "sketch_score",
        n=5,
    )
    if not top_sketches:
        lines.append("- No proof sketches available.")
    for sketch in top_sketches:
        lines.append(
            f"- `{sketch.get('sketch_id', '')}` [{sketch.get('proof_strategy_family', '')}] "
            f"{sketch.get('conjecture_id', '')} via `{sketch.get('strategy_id', '')}`"
        )
        lines.append(
            f"  - target={sketch.get('target_consequence_schema', '')}; antecedent={sketch.get('support_antecedent_schema', '') or 'unconditional'}; invariant={sketch.get('preserved_invariant', '')}"
        )
        obligations = sketch.get("proof_obligations", []) if isinstance(sketch.get("proof_obligations"), list) else []
        if obligations:
            lines.append(
                f"  - first proof obligation: {str(obligations[0].get('requirement', '')).strip()}"
            )
        aborts = sketch.get("abort_conditions", []) if isinstance(sketch.get("abort_conditions"), list) else []
        if aborts:
            lines.append(f"  - first abort condition: {str(aborts[0]).strip()}")
    if (artifacts_dir / "paper-style-argument.md").exists():
        lines.append("- The strongest sketch has also been rendered as `paper-style-argument.md`, which is the closest artifact to a mathematical research-note presentation of the current route.")
    lines.append("")

    lines.append("## Conjectured Mathematical Abstractions")
    lines.append("")
    top_conjectures = _top_rows(
        conjectures.get("abstraction_conjectures", []) if isinstance(conjectures.get("abstraction_conjectures"), list) else [],
        "priority",
        n=6,
    )
    if not top_conjectures:
        lines.append("- No abstraction conjectures available.")
    for row in top_conjectures:
        lines.append(
            f"- `{row.get('conjecture_id', '')}` [{row.get('abstraction_type', '')}] "
            f"{row.get('abstraction_label', '')}: {row.get('mathematical_object_role', '')}"
        )
        lines.append(
            f"  - bridge={row.get('bridge_id', '')}; gap={row.get('gap_target', '')}; priority={_safe_float(row.get('priority', 0.0)):.4f}"
        )
        definitional = row.get("definitional_profile", {}) if isinstance(row.get("definitional_profile"), dict) else {}
        necessary = definitional.get("necessary_attributes", []) if isinstance(definitional.get("necessary_attributes"), list) else []
        sufficient = definitional.get("sufficient_attribute_sets", []) if isinstance(definitional.get("sufficient_attribute_sets"), list) else []
        counterfactuals = row.get("counterfactual_probes", []) if isinstance(row.get("counterfactual_probes"), list) else []
        if necessary:
            lines.append(
                f"  - necessary attributes: {', '.join(str(attr.get('attribute', '')).strip() for attr in necessary[:3] if isinstance(attr, dict))}"
            )
        if sufficient:
            first = sufficient[0] if isinstance(sufficient[0], dict) else {}
            attrs = first.get("attributes", []) if isinstance(first.get("attributes"), list) else []
            lines.append(f"  - sufficient set ({first.get('label', '')}): {', '.join(str(x) for x in attrs[:4])}")
        if counterfactuals:
            first_probe = counterfactuals[0] if isinstance(counterfactuals[0], dict) else {}
            lines.append(
                f"  - counterfactual probe: {first_probe.get('intervention', '')} => {first_probe.get('expected_bridge_effect', '')}"
            )
    lines.append("")

    lines.append("## Hardness and Barrier Interpretation")
    lines.append("")
    essentials = hardness.get("essential_elements", []) if isinstance(hardness.get("essential_elements"), list) else []
    anti = hardness.get("anti_barrier_programs", []) if isinstance(hardness.get("anti_barrier_programs"), list) else []
    if essentials:
        for e in essentials[:4]:
            lines.append(
                f"- {e.get('name', 'Unnamed element')} ({e.get('severity', 'n/a')}, score {_safe_float(e.get('score')):.4f}): "
                f"{str(e.get('diagnosis', '')).strip()}"
            )
    else:
        lines.append("- No hardness diagnosis available.")

    if anti:
        lines.append("")
        lines.append("Anti-barrier programs to test:")
        for program in anti[:4]:
            fam = str(program.get("barrier_family", "unknown"))
            change = "; ".join([str(x) for x in (program.get("minimal_conceptual_changes") or [])[:2]])
            lines.append(f"- {fam}: {change or 'introduce a barrier-escaping representation/method change.'}")
    lines.append("")

    lines.append("## Hypothesis-State Interpretation")
    lines.append("")
    eval_counts = {}
    if isinstance(hypothesis_eval.get("summary"), dict):
        eval_counts = hypothesis_eval["summary"].get("verdict_counts", {}) or {}
    lines.append(f"- Immediate verdict profile: {json.dumps(eval_counts, ensure_ascii=False)}")
    lines.append(
        f"- Loop final state: supported={_safe_int(loop_summary.get('supported_count', 0))}, "
        f"refuted={_safe_int(loop_summary.get('refuted_count', 0))}, "
        f"open={_safe_int(loop_summary.get('open_count', 0))}."
    )

    rev_actions = revision.get("revision_actions", []) if isinstance(revision.get("revision_actions"), list) else []
    if rev_actions:
        lines.append("- Revision loop suggests these high-priority conceptual repairs:")
        for a in rev_actions[:4]:
            lines.append(
                f"  - `{a.get('revision_id', '')}` [{a.get('revision_type', '')}]: "
                f"{a.get('action', '')}"
            )
    lines.append("")

    lines.append("## Suggested Next Moves (Human Workflow)")
    lines.append("")
    lines.append("1. Keep only hypotheses with non-negative coherence delta unless there is strong external evidence.")
    lines.append("2. Execute top bridge programs in recommended order and log outcome against target theorem IDs.")
    lines.append("3. Use anti-barrier programs as explicit experimental tracks, not just commentary.")
    lines.append("4. If open hypotheses remain high after one more round, apply revision-loop actions before re-running abduction/deduction.")
    lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds parsing, computation, and artifact emission into a reproducible script execution.
    """

    logger = ReasoningLogger("kb-interpretation-reporter")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifacts-dir", required=True, help="Path to artifacts/<kb-slug> directory.")
    ap.add_argument("--kb", default="", help="Optional KB path for report context.")
    ap.add_argument("--output-process-md", help="Output path for stage/process report markdown.")
    ap.add_argument("--output-discovery-md", help="Output path for discovery interpretation markdown.")
    args = ap.parse_args()

    artifacts_dir = Path(args.artifacts_dir)
    if not artifacts_dir.exists():
        log_path = logger.finalize("error", summary=f"Artifacts directory not found: {artifacts_dir}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Artifacts directory not found: {artifacts_dir}")

    output_process = Path(args.output_process_md) if args.output_process_md else artifacts_dir / "reasoning-process-report.md"
    output_discovery = Path(args.output_discovery_md) if args.output_discovery_md else artifacts_dir / "discovery-interpretation-report.md"

    logger.step(
        "Parsed interpretation-report arguments",
        "\n".join(
            [
                f"artifacts_dir={artifacts_dir}",
                f"kb={args.kb}",
                f"output_process_md={output_process}",
                f"output_discovery_md={output_discovery}",
            ]
        ),
    )

    analysis = _load_json(artifacts_dir / "connection-analysis.json")
    coherence = _load_json(artifacts_dir / "coherence-report.json")
    entrypoints = _load_json(artifacts_dir / "entrypoints.json")
    pathways = _load_json(artifacts_dir / "entrypoint-pathways.json")
    hardness = _load_json(artifacts_dir / "epistemic-hardness.json")
    bridges = _load_json(artifacts_dir / "bridge-plan.json")
    conjectures = _load_json(artifacts_dir / "concept-gap-abstractions.json")
    strategies = _load_json(artifacts_dir / "proof-strategies.json")
    proof_sketches = _load_json(artifacts_dir / "proof-sketches.json")
    hypothesis_eval = _load_json(artifacts_dir / "hypothesis-evaluation.json")
    hypothesis_loop = _load_json(artifacts_dir / "hypothesis-refutation-loop.json")
    revision = _load_json(artifacts_dir / "revision-loop.json")
    reasoning_dynamics = _load_json(artifacts_dir / "reasoning-dynamics.json")

    process_text = _process_report(
        kb=args.kb,
        artifacts_dir=artifacts_dir,
        analysis=analysis,
        coherence=coherence,
        entrypoints=entrypoints,
        pathways=pathways,
        hardness=hardness,
        bridges=bridges,
        strategies=strategies,
        proof_sketches=proof_sketches,
        hypothesis_eval=hypothesis_eval,
        hypothesis_loop=hypothesis_loop,
        revision=revision,
        reasoning_dynamics=reasoning_dynamics,
        conjectures=conjectures,
    )
    discovery_text = _discovery_report(
        kb=args.kb,
        artifacts_dir=artifacts_dir,
        analysis=analysis,
        coherence=coherence,
        entrypoints=entrypoints,
        pathways=pathways,
        hardness=hardness,
        bridges=bridges,
        strategies=strategies,
        proof_sketches=proof_sketches,
        hypothesis_eval=hypothesis_eval,
        hypothesis_loop=hypothesis_loop,
        revision=revision,
        reasoning_dynamics=reasoning_dynamics,
        conjectures=conjectures,
    )

    output_process.parent.mkdir(parents=True, exist_ok=True)
    output_discovery.parent.mkdir(parents=True, exist_ok=True)
    output_process.write_text(process_text, encoding="utf-8")
    output_discovery.write_text(discovery_text, encoding="utf-8")
    concept_trace = _collect_concept_trace(entrypoints=entrypoints, pathways=pathways, hardness=hardness)
    phase_tracks = concept_trace.get("phase_tracks", []) if isinstance(concept_trace.get("phase_tracks"), list) else []
    logger.step(
        "Built concept communication summary for interpretation reports",
        "\n".join(
            [
                f"phase_track_count={len(phase_tracks)}",
                "top_phase_tracks="
                + ", ".join(str(t.get("phase", "")).strip() for t in phase_tracks[:4] if str(t.get("phase", "")).strip()),
                f"hardness_phase_pressure={json.dumps(concept_trace.get('hardness_phase_pressure', {}), ensure_ascii=False)}",
            ]
        ),
    )

    print(f"[OK] Wrote process report: {output_process}")
    print(f"[OK] Wrote discovery report: {output_discovery}")
    logger.add_output("reasoning_process_report_md", output_process)
    logger.add_output("discovery_interpretation_report_md", output_discovery)
    log_path = logger.finalize(
        "success",
        summary=(
            f"Generated human-readable interpretation reports in {artifacts_dir}."
        ),
    )
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
