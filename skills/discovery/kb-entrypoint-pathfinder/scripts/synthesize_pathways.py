# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""Build proof pathway agendas from ranked conceptual entry points."""

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
from contracts import validate_connection_analysis
from contracts import validate_entrypoints
from contracts import validate_phyp


def _clamp01(value: float) -> float:
    """
    Relevance: Operates within the pathway synthesis layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    return max(0.0, min(1.0, value))


def _find_related_hypotheses(entry_id: str, hypotheses: list[dict[str, Any]], max_items: int) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the pathway synthesis layer.
    Concept: Selection/retrieval of the most relevant candidates for reasoning.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    related = []
    for hyp in hypotheses:
        if not isinstance(hyp, dict):
            continue
        if entry_id in {str(hyp.get("target_statement_id", "")).strip(), str(hyp.get("support_statement_id", "")).strip()}:
            related.append(hyp)
    related.sort(key=lambda h: float(h.get("priority", 0.0) or 0.0), reverse=True)
    return related[: max_items]


def _find_related_links(entry_id: str, links: list[dict[str, Any]], max_items: int) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the pathway synthesis layer.
    Concept: Selection/retrieval of the most relevant candidates for reasoning.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    related = []
    for link in links:
        if not isinstance(link, dict):
            continue
        if entry_id in {str(link.get("from_id", "")).strip(), str(link.get("to_id", "")).strip()}:
            related.append(link)
    related.sort(key=lambda l: float(l.get("score", 0.0) or 0.0), reverse=True)
    return related[: max_items]


def _build_pathways(
    recommendations: dict[str, Any],
    phyp: dict[str, Any],
    analysis: dict[str, Any],
    top_entrypoints: int,
    max_hypotheses_per_path: int,
    max_links_per_path: int,
) -> dict[str, Any]:
    """
    Relevance: Operates within the pathway synthesis layer.
    Concept: Construction of derived graph/model structures used by later stages.
    Contribution: Creates the structural substrate that enables cross-stage scoring and interpretation.
    """

    ranked = recommendations.get("ranked_entrypoints", [])
    hypotheses = phyp.get("hypotheses", [])
    links = analysis.get("connection_candidates", [])

    pathways: list[dict[str, Any]] = []

    for rank, item in enumerate(ranked[: max(1, top_entrypoints)], start=1):
        if not isinstance(item, dict):
            continue
        entry_id = str(item.get("statement_id", "")).strip()
        if not entry_id:
            continue

        entry_score = float(item.get("entry_score", 0.0) or 0.0)
        related_hyp = _find_related_hypotheses(entry_id, hypotheses, max_items=max_hypotheses_per_path)
        related_links = _find_related_links(entry_id, links, max_items=max_links_per_path)

        hyp_avg = 0.0
        if related_hyp:
            hyp_avg = sum(float(h.get("priority", 0.0) or 0.0) for h in related_hyp) / len(related_hyp)

        link_avg = 0.0
        if related_links:
            link_avg = sum(float(l.get("score", 0.0) or 0.0) for l in related_links) / len(related_links)

        pathway_score = _clamp01(0.50 * entry_score + 0.30 * hyp_avg + 0.20 * link_avg)

        hypotheses_summary = [
            {
                "id": str(h.get("id", "")).strip(),
                "kind": str(h.get("kind", "")).strip(),
                "priority": round(float(h.get("priority", 0.0) or 0.0), 4),
                "target": str(h.get("target_statement_id", "")).strip(),
                "support": str(h.get("support_statement_id", "")).strip(),
            }
            for h in related_hyp
        ]

        links_summary = [
            {
                "from_id": str(l.get("from_id", "")).strip(),
                "to_id": str(l.get("to_id", "")).strip(),
                "score": round(float(l.get("score", 0.0) or 0.0), 4),
            }
            for l in related_links
        ]

        pathway = {
            "path_id": f"path.{rank:03d}",
            "rank": rank,
            "entry_statement_id": entry_id,
            "entry_kind": str(item.get("kind", "")).strip(),
            "entry_phase": str(item.get("phase", "")).strip(),
            "entry_concept_focus": [
                str(x).strip()
                for x in (item.get("concept_focus", []) if isinstance(item.get("concept_focus"), list) else [])
                if str(x).strip()
            ][:8],
            "entry_score": round(entry_score, 4),
            "pathway_score": round(pathway_score, 4),
            "goal": f"Develop a proof pathway centered on {entry_id}.",
            "supporting_hypotheses": hypotheses_summary,
            "supporting_links": links_summary,
            "execution_plan": [
                f"Run kb-abduce on target {entry_id} using top related hypotheses as seeds.",
                f"Inject top 1-2 tentative links touching {entry_id} in a scratch KB and run kb-deduce.",
                "Keep only hypothesis/link sets that improve conditional entailment coverage.",
                "If no improvement, move to next-ranked pathway.",
            ],
        }
        pathways.append(pathway)

    pathways.sort(key=lambda p: p["pathway_score"], reverse=True)

    return {
        "metadata": {
            "pathway_count": len(pathways),
            "entrypoints_considered": min(len(ranked), max(1, top_entrypoints)),
            "scoring": "0.50*entry_score + 0.30*avg_hypothesis_priority + 0.20*avg_link_score",
        },
        "pathways": pathways,
    }


def _to_markdown(report: dict[str, Any]) -> str:
    """
    Relevance: Operates within the pathway synthesis layer.
    Concept: Rendering internal outputs into human-readable artifacts.
    Contribution: Improves interpretability by exposing machine results in analyst-friendly form.
    """

    lines: list[str] = []
    lines.append("# Entry Point Pathways")
    lines.append("")
    meta = report.get("metadata", {})
    lines.append("## Stats")
    lines.append("")
    lines.append(f"- Pathways: {meta.get('pathway_count', 0)}")
    lines.append(f"- Entry points considered: {meta.get('entrypoints_considered', 0)}")
    lines.append("")

    lines.append("## Ranked Pathways")
    lines.append("")
    for p in report.get("pathways", []):
        lines.append(f"### {p['path_id']} - {p['entry_statement_id']}")
        lines.append(f"- Rank: {p['rank']}")
        lines.append(f"- Phase: {p['entry_phase']}")
        if p.get("entry_concept_focus"):
            lines.append(f"- Entry concepts: {', '.join(p.get('entry_concept_focus', [])[:6])}")
        lines.append(f"- Entry score: {p['entry_score']}")
        lines.append(f"- Pathway score: {p['pathway_score']}")
        lines.append(f"- Goal: {p['goal']}")
        lines.append("- Supporting hypotheses:")
        if p.get("supporting_hypotheses"):
            for h in p["supporting_hypotheses"]:
                lines.append(f"  - {h['id']} ({h['kind']}, priority={h['priority']})")
        else:
            lines.append("  - none")
        lines.append("- Supporting links:")
        if p.get("supporting_links"):
            for l in p["supporting_links"]:
                lines.append(f"  - {l['from_id']} -> {l['to_id']} (score={l['score']})")
        else:
            lines.append("  - none")
        lines.append("- Execution plan:")
        for step in p.get("execution_plan", []):
            lines.append(f"  - {step}")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    """
    Relevance: Operates within the pathway synthesis layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds parsing, computation, and artifact emission into a reproducible script execution.
    """

    logger = ReasoningLogger("kb-entrypoint-pathfinder")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recommendations", required=True, help="Path to entrypoint recommendations JSON.")
    parser.add_argument("--phyp", required=True, help="Path to proof hypotheses YAML.")
    parser.add_argument("--analysis", required=True, help="Path to connection-analysis JSON.")
    parser.add_argument("--top-entrypoints", type=int, default=8)
    parser.add_argument("--max-hypotheses-per-path", type=int, default=4)
    parser.add_argument("--max-links-per-path", type=int, default=3)
    parser.add_argument("--output-json", help="Optional output JSON path.")
    parser.add_argument("--output-md", help="Optional output Markdown path.")
    args = parser.parse_args()
    logger.step(
        "Parsed pathway arguments",
        "\n".join(
            [
                f"recommendations={args.recommendations}",
                f"phyp={args.phyp}",
                f"analysis={args.analysis}",
                f"top_entrypoints={args.top_entrypoints}",
                f"max_hypotheses_per_path={args.max_hypotheses_per_path}",
                f"max_links_per_path={args.max_links_per_path}",
                f"output_json={args.output_json or ''}",
                f"output_md={args.output_md or ''}",
            ]
        ),
    )

    rec_path = Path(args.recommendations)
    phyp_path = Path(args.phyp)
    analysis_path = Path(args.analysis)

    for path in [rec_path, phyp_path, analysis_path]:
        if not path.exists():
            log_path = logger.finalize("error", summary=f"Missing input file: {path}")
            print(f"[LOG] {log_path}", file=sys.stderr)
            raise SystemExit(f"[ERROR] Missing input file: {path}")

    recommendations = json.loads(rec_path.read_text(encoding="utf-8"))
    phyp = yaml.safe_load(phyp_path.read_text(encoding="utf-8"))
    analysis = json.loads(analysis_path.read_text(encoding="utf-8"))

    try:
        recommendations = validate_entrypoints(recommendations, name="recommendations")
        phyp = validate_phyp(phyp, name="phyp")
        analysis = validate_connection_analysis(analysis, name="analysis")
    except ValueError as exc:
        log_path = logger.finalize("error", summary=str(exc))
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] {exc}")

    report = _build_pathways(
        recommendations=recommendations,
        phyp=phyp,
        analysis=analysis,
        top_entrypoints=max(1, args.top_entrypoints),
        max_hypotheses_per_path=max(1, args.max_hypotheses_per_path),
        max_links_per_path=max(1, args.max_links_per_path),
    )
    pathways = report.get("pathways", []) if isinstance(report.get("pathways"), list) else []
    logger.step(
        "Pathway concept trace",
        "\n".join(
            [
                "top_pathways="
                + "; ".join(
                    f"{str(item.get('path_id', '')).strip()}:{str(item.get('entry_statement_id', '')).strip()}:{float(item.get('pathway_score', 0.0) or 0.0):.4f}"
                    for item in pathways[:6]
                    if isinstance(item, dict) and str(item.get("path_id", "")).strip()
                ),
                "top_phases="
                + "; ".join(
                    str(item.get("entry_phase", "")).strip()
                    for item in pathways[:6]
                    if isinstance(item, dict) and str(item.get("entry_phase", "")).strip()
                ),
                "top_pathway_concepts="
                + "; ".join(
                    f"{str(item.get('path_id', '')).strip()}[{', '.join(item.get('entry_concept_focus', [])[:4])}]"
                    for item in pathways[:6]
                    if isinstance(item, dict) and str(item.get("path_id", "")).strip()
                ),
            ]
        ),
    )

    if args.output_json:
        out = Path(args.output_json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"[OK] Wrote JSON: {out}")
        logger.add_output("entrypoint_pathways_json", out)

    markdown = _to_markdown(report)
    if args.output_md:
        out = Path(args.output_md)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(markdown, encoding="utf-8")
        print(f"[OK] Wrote Markdown: {out}")
        logger.add_output("entrypoint_pathways_md", out)

    print(f"[OK] Pathways: {len(report.get('pathways', []))}")
    if report.get("pathways"):
        top = report["pathways"][0]
        print(f"[OK] Top pathway: {top['path_id']} ({top['entry_statement_id']}, score={top['pathway_score']})")
        logger.step(
            "Computed top pathway",
            f"path_id={top['path_id']}\nentry_statement_id={top['entry_statement_id']}\nscore={top['pathway_score']}",
        )
    log_path = logger.finalize(
        "success",
        summary=f"Synthesized {len(report.get('pathways', []))} entrypoint pathways.",
    )
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
