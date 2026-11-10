# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""Rank best conceptual entry points for a KB using concept structures.

Inputs:
- KB markdown with statement YAML blocks
- Concept evolution markdown
- Connector analysis JSON
- Proof hypotheses YAML (phyp)

Output:
- ranked entry points (JSON and/or Markdown)
"""

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
from contracts import validate_coherence_report

STATEMENT_BLOCK_PATTERN = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)
STATEMENT_ID_PATTERN = re.compile(r"`(st\.[A-Za-z0-9._-]+)`")


def _load_kb_statements(kb_path: Path, include_statuses: set[str]) -> dict[str, dict[str, Any]]:
    """
    Relevance: Operates within the entrypoint ranking layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Provides clean, typed inputs so downstream reasoning steps remain auditable.
    """

    content = kb_path.read_text(encoding="utf-8")
    statements: dict[str, dict[str, Any]] = {}

    for match in STATEMENT_BLOCK_PATTERN.finditer(content):
        try:
            payload = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            continue
        if not isinstance(payload, dict):
            continue

        sid = str(payload.get("id", "")).strip()
        kind = str(payload.get("kind", "")).strip().lower()
        if not sid or not kind:
            continue

        status = str(payload.get("status", "tentative")).strip().lower()
        if status not in include_statuses:
            continue

        statements[sid] = {
            "id": sid,
            "kind": kind,
            "status": status,
            "informal": str(payload.get("informal", "")).strip(),
            "latex": str(payload.get("latex", "")).strip(),
            "notes": str(payload.get("notes", "")).strip(),
            "depends_on": payload.get("depends_on", []),
        }

    return statements


def _load_concept_map(concept_path: Path) -> tuple[dict[str, str], list[str]]:
    """
    Relevance: Operates within the entrypoint ranking layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Provides clean, typed inputs so downstream reasoning steps remain auditable.
    """

    id_to_phase: dict[str, str] = {}
    ordered_phases: list[str] = []
    current_phase = "Unspecified"

    for line in concept_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            current_phase = line.replace("## ", "", 1).strip()
            if current_phase not in ordered_phases:
                ordered_phases.append(current_phase)
            continue

        for sid in STATEMENT_ID_PATTERN.findall(line):
            id_to_phase[sid] = current_phase

    if "Unspecified" not in ordered_phases:
        ordered_phases.append("Unspecified")

    return id_to_phase, ordered_phases


def _phase_weight(phase: str) -> float:
    """
    Relevance: Operates within the entrypoint ranking layer.
    Concept: Typed classification used to guide scoring and prioritization.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    p = phase.lower()
    if "meta-complexity" in p or "hardness magnification" in p:
        return 1.0
    if "algorithms" in p or "derandomization" in p or "proof complexity" in p or "communication" in p:
        return 0.9
    if "barrier" in p:
        return 0.82
    if "nonuniform" in p or "circuit" in p:
        return 0.75
    if "np-completeness" in p:
        return 0.65
    if "correspondence" in p:
        return 0.92
    if "representation" in p or "duality" in p:
        return 0.94
    if "regularity" in p or "compact-open" in p:
        return 0.84
    if "fixed-point" in p or "common-fixed-point" in p:
        return 0.93
    if "averaging" in p or "cesaro" in p:
        return 0.82
    if "intersection" in p or "compactness" in p:
        return 0.88
    if "spectral" in p or "generator" in p:
        return 0.78
    if "foundational" in p or "core" in p:
        return 0.45
    if "current kb state" in p or "trajectory" in p:
        return 0.88
    return 0.6


def _correspondence_bonus(stmt: dict[str, Any]) -> float:
    """
    Relevance: Operates within the entrypoint ranking layer.
    Concept: Structural preference for statements that unify two regimes by equivalence or correspondence.
    Contribution: Elevates discovery targets that compress the theory, such as Stone-style representation theorems.
    """

    kind = str(stmt.get("kind", "")).strip().lower()
    if kind not in {"theorem", "lemma", "corollary"}:
        return 0.0
    blob = " ".join(
        [
            str(stmt.get("id", "")),
            str(stmt.get("informal", "")),
            str(stmt.get("latex", "")),
            str(stmt.get("notes", "")),
        ]
    ).lower()
    if any(token in blob for token in ("if and only if", " iff ", "correspondence", "bijection", "equivalence")):
        return 1.0
    if any(token in blob for token in ("represented by a unique", "regular borel measure", "radon measure")) and "functional" in blob:
        return 1.35
    if any(token in blob for token in ("common fixed point", "fixed by every", "commuting family")) and any(token in blob for token in ("compact convex", "affine")):
        return 1.20
    if "there exists a unique" in blob and any(token in blob for token in ("operator", "group", "generator")):
        return 0.8
    return 0.0


def _phase_from_notes(notes: str) -> str:
    """
    Relevance: Operates within the entrypoint ranking layer.
    Concept: Typed classification used to guide scoring and prioritization.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    for line in notes.splitlines():
        stripped = line.strip()
        if stripped.startswith("section:"):
            return stripped.split(":", 1)[1].strip()
    return "Unspecified"


def _safe_norm(values: dict[str, float]) -> dict[str, float]:
    """
    Relevance: Operates within the entrypoint ranking layer.
    Concept: Defensive conversion/parsing to keep scoring and reporting robust.
    Contribution: Reduces runtime ambiguity and prevents malformed artifacts from destabilizing the workflow.
    """

    if not values:
        return {}
    vmax = max(values.values())
    if vmax <= 0:
        return {k: 0.0 for k in values}
    return {k: v / vmax for k, v in values.items()}


def _clamp01(value: float) -> float:
    """
    Relevance: Operates within the entrypoint ranking layer.
    Concept: Defensive conversion/parsing to keep scoring and reporting robust.
    Contribution: Reduces runtime ambiguity and prevents malformed artifacts from destabilizing the workflow.
    """

    return max(0.0, min(1.0, float(value)))


def _build_recommendations(
    statements: dict[str, dict[str, Any]],
    concept_map: dict[str, str],
    analysis: dict[str, Any],
    phyp: dict[str, Any],
    coherence: dict[str, Any],
    top_k: int,
) -> dict[str, Any]:
    """
    Relevance: Operates within the entrypoint ranking layer.
    Concept: Construction of derived graph/model structures used by later stages.
    Contribution: Creates the structural substrate that enables cross-stage scoring and interpretation.
    """

    intervention_score: dict[str, float] = defaultdict(float)
    intervention_rationale: dict[str, str] = {}
    intervention_concepts: dict[str, list[str]] = {}

    for item in analysis.get("top_interventions", []):
        if not isinstance(item, dict):
            continue
        sid = str(item.get("statement_id", "")).strip()
        if sid:
            intervention_score[sid] = float(item.get("score", 0.0) or 0.0)
            intervention_rationale[sid] = str(item.get("rationale", "")).strip()
            intervention_concepts[sid] = [
                str(x).strip()
                for x in (item.get("concept_focus", []) if isinstance(item.get("concept_focus"), list) else [])
                if str(x).strip()
            ][:6]

    bridge_incident_raw: dict[str, float] = defaultdict(float)
    bridge_count: dict[str, int] = defaultdict(int)
    for item in analysis.get("connection_candidates", []):
        if not isinstance(item, dict):
            continue
        score = float(item.get("score", 0.0) or 0.0)
        src = str(item.get("from_id", "")).strip()
        dst = str(item.get("to_id", "")).strip()
        if src:
            bridge_incident_raw[src] += score
            bridge_count[src] += 1
        if dst:
            bridge_incident_raw[dst] += score
            bridge_count[dst] += 1

    bridge_incident = _safe_norm(dict(bridge_incident_raw))

    hyp_target_raw: dict[str, float] = defaultdict(float)
    hyp_support_raw: dict[str, float] = defaultdict(float)
    hyp_count: dict[str, int] = defaultdict(int)

    for hyp in phyp.get("hypotheses", []):
        if not isinstance(hyp, dict):
            continue
        priority = float(hyp.get("priority", 0.0) or 0.0)
        target = str(hyp.get("target_statement_id", "")).strip()
        support = str(hyp.get("support_statement_id", "")).strip()

        if target:
            hyp_target_raw[target] = max(hyp_target_raw[target], priority)
            hyp_count[target] += 1
        if support:
            hyp_support_raw[support] = max(hyp_support_raw[support], priority)
            hyp_count[support] += 1

    hyp_target = _safe_norm(dict(hyp_target_raw))
    hyp_support = _safe_norm(dict(hyp_support_raw))

    coherence_by_hypothesis: dict[str, dict[str, Any]] = {}
    if isinstance(coherence.get("hypothesis_coherence_index"), dict):
        for hid, row in coherence.get("hypothesis_coherence_index", {}).items():
            if isinstance(row, dict):
                coherence_by_hypothesis[str(hid).strip()] = row
    elif isinstance(coherence.get("hypothesis_coherence"), list):
        for row in coherence.get("hypothesis_coherence", []):
            if not isinstance(row, dict):
                continue
            hid = str(row.get("hypothesis_id", "")).strip()
            if hid:
                coherence_by_hypothesis[hid] = row

    coherence_stmt_raw: dict[str, float] = defaultdict(float)
    for hyp in phyp.get("hypotheses", []):
        if not isinstance(hyp, dict):
            continue
        hid = str(hyp.get("id", "")).strip()
        if not hid:
            continue
        row = coherence_by_hypothesis.get(hid, {})
        exp = float(row.get("explanatory_power_local", 0.0) or 0.0)
        delta = float(row.get("coherence_delta_global", 0.0) or 0.0)
        # Keep per-hypothesis coherence salience as a bounded scalar first.
        # Cross-statement normalization happens once below via `_safe_norm`.
        signal = _clamp01(0.65 * exp + 0.35 * max(0.0, delta))
        target = str(hyp.get("target_statement_id", "")).strip()
        support = str(hyp.get("support_statement_id", "")).strip()
        if target:
            coherence_stmt_raw[target] = max(coherence_stmt_raw[target], signal)
        if support:
            coherence_stmt_raw[support] = max(coherence_stmt_raw[support], signal * 0.85)
    coherence_stmt = _safe_norm(dict(coherence_stmt_raw))

    concept_graph = analysis.get("concept_graph", {}) if isinstance(analysis.get("concept_graph"), dict) else {}
    relations = concept_graph.get("relations", []) if isinstance(concept_graph.get("relations"), list) else []
    concept_touch_raw: dict[str, float] = defaultdict(float)
    for rel in relations:
        if not isinstance(rel, dict):
            continue
        src = str(rel.get("from", "")).strip()
        dst = str(rel.get("to", "")).strip()
        rel_name = str(rel.get("relation", "")).strip().lower()
        weight = float(rel.get("weight", 0.0) or 0.0)
        for node in [src, dst]:
            if node.startswith("statement:"):
                sid = node.split("statement:", 1)[1]
                if rel_name in {"defines", "uses", "generalizes", "reexpresses", "analogy_to"}:
                    concept_touch_raw[sid] += max(0.0, weight)
                elif rel_name in {"obstructs"}:
                    concept_touch_raw[sid] += max(0.0, weight) * 0.4
    concept_touch = _safe_norm(dict(concept_touch_raw))

    scored: list[dict[str, Any]] = []
    for sid, stmt in statements.items():
        phase = concept_map.get(sid)
        if not phase:
            phase = _phase_from_notes(str(stmt.get("notes", "")))
        if not phase:
            phase = "Unspecified"
        phase_score = _phase_weight(phase)
        i_score = float(intervention_score.get(sid, 0.0))
        h_score = 0.70 * float(hyp_target.get(sid, 0.0)) + 0.30 * float(hyp_support.get(sid, 0.0))
        b_score = float(bridge_incident.get(sid, 0.0))
        c_score = float(concept_touch.get(sid, 0.0))
        coh_score = float(coherence_stmt.get(sid, 0.0))
        corr_score = _correspondence_bonus(stmt)

        entry_score = (
            0.33 * i_score
            + 0.21 * h_score
            + 0.11 * b_score
            + 0.10 * phase_score
            + 0.10 * c_score
            + 0.07 * coh_score
            + 0.08 * corr_score
        )

        reasons = []
        if i_score > 0:
            reasons.append(f"intervention={i_score:.4f}")
        if h_score > 0:
            reasons.append(f"hypothesis-pressure={h_score:.4f}")
        if b_score > 0:
            reasons.append(f"bridge-incidence={b_score:.4f}")
        if c_score > 0:
            reasons.append(f"concept-centrality={c_score:.4f}")
        if coh_score > 0:
            reasons.append(f"coherence-salience={coh_score:.4f}")
        if corr_score > 0:
            reasons.append(f"correspondence-structure={corr_score:.4f}")
        reasons.append(f"phase='{phase}'")
        concept_focus = intervention_concepts.get(sid, [])
        if concept_focus:
            reasons.append("concepts=" + ", ".join(concept_focus[:4]))

        scored.append(
            {
                "statement_id": sid,
                "kind": stmt["kind"],
                "entry_score": round(entry_score, 4),
                "phase": phase,
                "concept_focus": concept_focus,
                "evidence": {
                    "intervention_score": round(i_score, 4),
                    "hypothesis_pressure": round(h_score, 4),
                    "bridge_incidence": round(b_score, 4),
                    "phase_weight": round(phase_score, 4),
                    "concept_centrality": round(c_score, 4),
                    "coherence_salience": round(coh_score, 4),
                    "correspondence_bonus": round(corr_score, 4),
                    "hypothesis_count": hyp_count.get(sid, 0),
                    "bridge_count": bridge_count.get(sid, 0),
                },
                "summary": (stmt["informal"] or stmt["latex"])[:220],
                "rationale": intervention_rationale.get(sid) or "; ".join(reasons),
            }
        )

    scored.sort(key=lambda x: x["entry_score"], reverse=True)
    ranked = scored[: max(1, top_k)]

    tracks: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in ranked:
        tracks[item["phase"]].append(item)

    concept_tracks = []
    for phase, items in sorted(tracks.items(), key=lambda kv: max(i["entry_score"] for i in kv[1]), reverse=True):
        concept_tracks.append(
            {
                "phase": phase,
                "top_entrypoints": [
                    {
                        "statement_id": i["statement_id"],
                        "entry_score": i["entry_score"],
                        "kind": i["kind"],
                    }
                    for i in items[:3]
                ],
            }
        )

    return {
        "metadata": {
            "statement_count": len(statements),
            "ranked_count": len(ranked),
            "analysis_top_interventions": len(analysis.get("top_interventions", [])),
            "analysis_connection_candidates": len(analysis.get("connection_candidates", [])),
            "hypothesis_count": len(phyp.get("hypotheses", [])),
            "coherence_signal_count": len(coherence_by_hypothesis),
            "scoring": {
                "entry_score": (
                    "0.33*intervention + 0.21*hypothesis_pressure + 0.11*bridge_incidence "
                    "+ 0.10*phase_weight + 0.10*concept_centrality + 0.07*coherence_salience "
                    "+ 0.08*correspondence_bonus"
                )
            },
        },
        "ranked_entrypoints": ranked,
        "concept_tracks": concept_tracks,
    }


def _to_markdown(report: dict[str, Any]) -> str:
    """
    Relevance: Operates within the entrypoint ranking layer.
    Concept: Rendering internal outputs into human-readable artifacts.
    Contribution: Improves interpretability by exposing machine results in analyst-friendly form.
    """

    lines: list[str] = []
    lines.append("# Conceptual Entry Points")
    lines.append("")

    meta = report.get("metadata", {})
    lines.append("## Stats")
    lines.append("")
    lines.append(f"- Statements analyzed: {meta.get('statement_count', 0)}")
    lines.append(f"- Ranked entry points: {meta.get('ranked_count', 0)}")
    lines.append(f"- Connector interventions used: {meta.get('analysis_top_interventions', 0)}")
    lines.append(f"- Connector links used: {meta.get('analysis_connection_candidates', 0)}")
    lines.append(f"- Proof hypotheses used: {meta.get('hypothesis_count', 0)}")
    lines.append(f"- Coherence signals used: {meta.get('coherence_signal_count', 0)}")
    lines.append("")

    lines.append("## Top Entry Points")
    lines.append("")
    lines.append("| rank | statement_id | kind | phase | entry_score | concepts | hyp_count | bridge_count |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for idx, item in enumerate(report.get("ranked_entrypoints", []), start=1):
        ev = item.get("evidence", {})
        concepts = ", ".join(item.get("concept_focus", [])[:4]) if isinstance(item.get("concept_focus"), list) else ""
        lines.append(
            f"| {idx} | {item['statement_id']} | {item['kind']} | {item['phase']} | {item['entry_score']} | {concepts} | {ev.get('hypothesis_count', 0)} | {ev.get('bridge_count', 0)} |"
        )
    lines.append("")

    lines.append("## Concept Tracks")
    lines.append("")
    for track in report.get("concept_tracks", []):
        lines.append(f"### {track['phase']}")
        for item in track.get("top_entrypoints", []):
            lines.append(f"- `{item['statement_id']}` ({item['kind']}), score={item['entry_score']}")
        lines.append("")

    lines.append("## Tactical Next Step")
    lines.append("")
    lines.append("Run `kb-abduce` on the top 3 entry points, then validate candidate bridges with `kb-deduce`.")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    """
    Relevance: Operates within the entrypoint ranking layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds parsing, computation, and artifact emission into a reproducible script execution.
    """

    logger = ReasoningLogger("kb-entrypoint-finder")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kb", required=True, help="Path to KB markdown file.")
    parser.add_argument("--concept", required=True, help="Path to concept-evolution markdown.")
    parser.add_argument("--analysis", required=True, help="Path to connection-analysis JSON.")
    parser.add_argument("--phyp", required=True, help="Path to proof hypotheses YAML.")
    parser.add_argument("--coherence-report", help="Optional coherence report JSON.")
    parser.add_argument(
        "--include-status",
        action="append",
        choices=["accepted", "tentative", "rejected"],
        default=["accepted", "tentative"],
        help="Statement statuses to include from KB (repeatable).",
    )
    parser.add_argument("--top-k", type=int, default=20, help="Number of entry points to keep.")
    parser.add_argument("--output-json", help="Optional output JSON path.")
    parser.add_argument("--output-md", help="Optional output Markdown path.")
    args = parser.parse_args()
    logger.step(
        "Parsed entrypoint arguments",
        "\n".join(
            [
                f"kb={args.kb}",
                f"concept={args.concept}",
                f"analysis={args.analysis}",
                f"phyp={args.phyp}",
                f"coherence_report={args.coherence_report or ''}",
                f"include_status={args.include_status}",
                f"top_k={args.top_k}",
                f"output_json={args.output_json or ''}",
                f"output_md={args.output_md or ''}",
            ]
        ),
    )

    kb_path = Path(args.kb)
    concept_path = Path(args.concept)
    analysis_path = Path(args.analysis)
    phyp_path = Path(args.phyp)
    coherence_path = Path(args.coherence_report) if args.coherence_report else None

    for path in [kb_path, concept_path, analysis_path, phyp_path]:
        if not path.exists():
            log_path = logger.finalize("error", summary=f"Missing input file: {path}")
            print(f"[LOG] {log_path}", file=sys.stderr)
            raise SystemExit(f"[ERROR] Missing input file: {path}")
    if coherence_path and not coherence_path.exists():
        log_path = logger.finalize("error", summary=f"Missing coherence file: {coherence_path}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Missing coherence file: {coherence_path}")

    include_statuses = {s.strip().lower() for s in args.include_status if str(s).strip()}
    statements = _load_kb_statements(kb_path, include_statuses=include_statuses)
    concept_map, _ = _load_concept_map(concept_path)
    analysis = json.loads(analysis_path.read_text(encoding="utf-8"))
    phyp = yaml.safe_load(phyp_path.read_text(encoding="utf-8"))
    coherence: dict[str, Any] = {}
    if coherence_path:
        try:
            coherence = validate_coherence_report(json.loads(coherence_path.read_text(encoding="utf-8")), name="coherence")
        except ValueError as exc:
            log_path = logger.finalize("error", summary=str(exc))
            print(f"[LOG] {log_path}", file=sys.stderr)
            raise SystemExit(f"[ERROR] {exc}")
    if not isinstance(phyp, dict):
        log_path = logger.finalize("error", summary="phyp file must be a YAML object")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit("[ERROR] phyp file must be a YAML object")

    report = _build_recommendations(
        statements=statements,
        concept_map=concept_map,
        analysis=analysis,
        phyp=phyp,
        coherence=coherence,
        top_k=max(1, args.top_k),
    )
    concept_tracks = report.get("concept_tracks", []) if isinstance(report.get("concept_tracks"), list) else []
    ranked = report.get("ranked_entrypoints", []) if isinstance(report.get("ranked_entrypoints"), list) else []
    logger.step(
        "Entrypoint concept trace",
        "\n".join(
            [
                "top_entrypoints="
                + "; ".join(
                    f"{str(item.get('statement_id', '')).strip()}:{float(item.get('entry_score', 0.0) or 0.0):.4f}"
                    for item in ranked[:6]
                    if isinstance(item, dict) and str(item.get("statement_id", "")).strip()
                ),
                "top_entrypoint_concepts="
                + "; ".join(
                    f"{str(item.get('statement_id', '')).strip()}[{', '.join(item.get('concept_focus', [])[:4])}]"
                    for item in ranked[:6]
                    if isinstance(item, dict) and str(item.get("statement_id", "")).strip()
                ),
                "top_concept_tracks="
                + "; ".join(
                    str(track.get("phase", "")).strip()
                    for track in concept_tracks[:6]
                    if isinstance(track, dict) and str(track.get("phase", "")).strip()
                ),
            ]
        ),
    )

    if args.output_json:
        out = Path(args.output_json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"[OK] Wrote JSON: {out}")
        logger.add_output("entrypoints_json", out)

    markdown = _to_markdown(report)
    if args.output_md:
        out = Path(args.output_md)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(markdown, encoding="utf-8")
        print(f"[OK] Wrote Markdown: {out}")
        logger.add_output("entrypoints_md", out)

    print(f"[OK] Ranked entry points: {len(report.get('ranked_entrypoints', []))}")
    if report.get("ranked_entrypoints"):
        best = report["ranked_entrypoints"][0]
        print(f"[OK] Top entry point: {best['statement_id']} (score={best['entry_score']})")
        logger.step(
            "Computed top entrypoint",
            f"statement_id={best['statement_id']}\nscore={best['entry_score']}",
        )
    log_path = logger.finalize(
        "success",
        summary=f"Ranked {len(report.get('ranked_entrypoints', []))} conceptual entry points.",
    )
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
