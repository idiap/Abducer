# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""Evaluate proof hypotheses against KB structure and classify support/refutation status."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

import yaml

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from hypothesis_eval import apply_results_to_payload
from hypothesis_eval import evaluate_hypotheses
from hypothesis_eval import load_analysis_scores
from hypothesis_eval import load_coherence_signals
from hypothesis_eval import load_hypothesis_evidence
from hypothesis_eval import load_hypothesis_payload
from hypothesis_eval import load_kb_statements
from reasoning_log import ReasoningLogger


def _to_markdown(report: dict[str, Any]) -> str:
    """
    Relevance: Operates within the hypothesis evaluation layer.
    Concept: Rendering internal outputs into human-readable artifacts.
    Contribution: Improves interpretability by exposing machine results in analyst-friendly form.
    """

    lines: list[str] = []
    lines.append("# Hypothesis Evaluation Report")
    lines.append("")

    meta = report.get("metadata", {})
    summary = report.get("summary", {})
    verdict_counts = summary.get("verdict_counts", {})

    lines.append("## Stats")
    lines.append("")
    lines.append(f"- Hypotheses evaluated: {meta.get('hypothesis_count', 0)}")
    lines.append(f"- Support threshold: {meta.get('support_threshold', 0.0)}")
    lines.append(f"- Refute threshold: {meta.get('refute_threshold', 0.0)}")
    lines.append(f"- Margin: {meta.get('margin', 0.0)}")
    lines.append(f"- Force resolution: {meta.get('force_resolution', False)}")
    lines.append(f"- Coherence signals: {meta.get('coherence_signal_count', 0)}")
    lines.append(f"- Global coherence baseline: {meta.get('global_coherence', 0.0)}")
    lines.append("")
    lines.append("## Verdict Counts")
    lines.append("")
    for key in sorted(verdict_counts.keys()):
        lines.append(f"- {key}: {verdict_counts.get(key, 0)}")
    lines.append("")

    lines.append("## Results")
    lines.append("")
    lines.append("| hypothesis_id | verdict | next_status | support | refute | confidence | action |")
    lines.append("|---|---|---|---|---|---|---|")
    for item in report.get("results", []):
        lines.append(
            "| {id} | {verdict} | {status} | {support:.4f} | {refute:.4f} | {confidence:.4f} | {action} |".format(
                id=item.get("hypothesis_id", ""),
                verdict=item.get("verdict", ""),
                status=item.get("next_status", ""),
                support=float(item.get("support_score", 0.0) or 0.0),
                refute=float(item.get("refute_score", 0.0) or 0.0),
                confidence=float(item.get("confidence", 0.0) or 0.0),
                action=item.get("recommended_action", ""),
            )
        )
    lines.append("")

    lines.append("## Mathematical Readout")
    lines.append("")
    for item in report.get("results", [])[:12]:
        commitment = item.get("inferential_commitment", {}) if isinstance(item.get("inferential_commitment"), dict) else {}
        signals = item.get("signals", {}) if isinstance(item.get("signals"), dict) else {}
        reasons = item.get("reasons", []) if isinstance(item.get("reasons"), list) else []
        lines.append(
            f"### {item.get('hypothesis_id', '')} [{item.get('kind', '')}]"
        )
        lines.append(
            f"- Verdict: {item.get('verdict', '')} (support={float(item.get('support_score', 0.0) or 0.0):.4f}, "
            f"refute={float(item.get('refute_score', 0.0) or 0.0):.4f}, confidence={float(item.get('confidence', 0.0) or 0.0):.4f})"
        )
        if commitment:
            lines.append(
                f"- Antecedent schema: {commitment.get('support_antecedent_schema', '') or 'unconditional'}"
            )
            lines.append(
                f"- Target consequence: {commitment.get('target_consequence_schema', '') or 'statement-conclusion'}"
            )
            lines.append(
                f"- Preserved invariant: {commitment.get('preserved_invariant', '') or 'support-to-target interface'}"
            )
            lines.append(f"- Barrier scope: {commitment.get('barrier_scope', '') or 'none'}")
        lines.append(
            f"- Alignment signals: antecedent={float(signals.get('antecedent_alignment', 0.0) or 0.0):.4f}, "
            f"consequence={float(signals.get('consequence_alignment', 0.0) or 0.0):.4f}, "
            f"invariant={float(signals.get('invariant_alignment', 0.0) or 0.0):.4f}, "
            f"barrier={float(signals.get('barrier_alignment', 0.0) or 0.0):.4f}"
        )
        if reasons:
            lines.append("- Key reasons: " + "; ".join(str(x) for x in reasons[:4]))
        lines.append("")
    return "\n".join(lines) + "\n"


def _slug_from_phyp_path(path: Path) -> str:
    """
    Relevance: Operates within the hypothesis evaluation layer.
    Concept: Stable naming and path-derivation helper for artifact routing.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    name = path.name
    if name.endswith(".proof-hypotheses.yaml"):
        name = name[: -len(".proof-hypotheses.yaml")]
    return name or "kb"


def main() -> int:
    """
    Relevance: Operates within the hypothesis evaluation layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds parsing, computation, and artifact emission into a reproducible script execution.
    """

    logger = ReasoningLogger("kb-hypothesis-evaluator")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--kb", required=True, help="Path to KB markdown file.")
    ap.add_argument("--phyp", required=True, help="Path to proof hypothesis YAML.")
    ap.add_argument("--analysis", help="Optional connection-analysis JSON/YAML.")
    ap.add_argument("--evidence-json", help="Optional hypothesis evidence JSON/YAML.")
    ap.add_argument("--coherence-report", help="Optional coherence-report JSON/YAML.")
    ap.add_argument("--support-threshold", type=float, default=0.62)
    ap.add_argument("--refute-threshold", type=float, default=0.62)
    ap.add_argument("--margin", type=float, default=0.08)
    ap.add_argument(
        "--force-resolution",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Force non-inconclusive verdict by comparing support vs refute score.",
    )
    ap.add_argument("--output-json", help="Output JSON report path.")
    ap.add_argument("--output-md", help="Output Markdown report path.")
    ap.add_argument("--output-phyp-md", help="Optional output path for Markdown mirror under phyp/.")
    ap.add_argument("--output-phyp", help="Optional output path for hypothesis YAML with updated statuses.")
    args = ap.parse_args()
    logger.step(
        "Parsed hypothesis-evaluator arguments",
        "\n".join(
            [
                f"kb={args.kb}",
                f"phyp={args.phyp}",
                f"analysis={args.analysis or ''}",
                f"evidence_json={args.evidence_json or ''}",
                f"coherence_report={args.coherence_report or ''}",
                f"support_threshold={args.support_threshold}",
                f"refute_threshold={args.refute_threshold}",
                f"margin={args.margin}",
                f"force_resolution={args.force_resolution}",
                f"output_json={args.output_json or ''}",
                f"output_md={args.output_md or ''}",
                f"output_phyp_md={args.output_phyp_md or ''}",
                f"output_phyp={args.output_phyp or ''}",
            ]
        ),
    )

    kb_path = Path(args.kb)
    phyp_path = Path(args.phyp)
    analysis_path = Path(args.analysis) if args.analysis else None
    evidence_path = Path(args.evidence_json) if args.evidence_json else None
    coherence_path = Path(args.coherence_report) if args.coherence_report else None

    for p in [kb_path, phyp_path]:
        if not p.exists():
            log_path = logger.finalize("error", summary=f"Missing input: {p}")
            print(f"[LOG] {log_path}", file=sys.stderr)
            raise SystemExit(f"[ERROR] Missing input: {p}")
    if analysis_path and not analysis_path.exists():
        log_path = logger.finalize("error", summary=f"Missing analysis file: {analysis_path}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Missing analysis file: {analysis_path}")
    if evidence_path and not evidence_path.exists():
        log_path = logger.finalize("error", summary=f"Missing evidence file: {evidence_path}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Missing evidence file: {evidence_path}")
    if coherence_path and not coherence_path.exists():
        log_path = logger.finalize("error", summary=f"Missing coherence file: {coherence_path}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Missing coherence file: {coherence_path}")

    try:
        payload = load_hypothesis_payload(phyp_path)
        statements = load_kb_statements(kb_path)
        analysis_scores = load_analysis_scores(analysis_path)
        evidence_by_hypothesis = load_hypothesis_evidence(evidence_path)
        coherence_by_hypothesis, coherence_profile = load_coherence_signals(coherence_path)
    except Exception as exc:
        log_path = logger.finalize("error", summary=f"Failed to parse inputs: {exc}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise

    logger.step(
        "Loaded evaluation inputs",
        "\n".join(
            [
                f"statement_count={len(statements)}",
                f"hypothesis_count={len(payload.get('hypotheses', []))}",
                f"analysis_pairs={len(analysis_scores)}",
                f"evidence_items={len(evidence_by_hypothesis)}",
                f"coherence_items={len(coherence_by_hypothesis)}",
            ]
        ),
    )

    report = evaluate_hypotheses(
        hypotheses=[h for h in payload.get("hypotheses", []) if isinstance(h, dict)],
        statements=statements,
        analysis_scores=analysis_scores,
        evidence_by_hypothesis=evidence_by_hypothesis,
        coherence_by_hypothesis=coherence_by_hypothesis,
        coherence_profile=coherence_profile,
        support_threshold=max(0.0, min(1.0, args.support_threshold)),
        refute_threshold=max(0.0, min(1.0, args.refute_threshold)),
        margin=max(0.0, min(1.0, args.margin)),
        force_resolution=bool(args.force_resolution),
    )
    report["metadata"]["kb"] = str(kb_path)
    report["metadata"]["phyp"] = str(phyp_path)
    if analysis_path:
        report["metadata"]["analysis"] = str(analysis_path)
    if evidence_path:
        report["metadata"]["evidence_json"] = str(evidence_path)
    if coherence_path:
        report["metadata"]["coherence_report"] = str(coherence_path)
    logger.step(
        "Hypothesis inferential readout",
        "\n".join(
            [
                f"{str(item.get('hypothesis_id', '')).strip()}:{str(item.get('verdict', '')).strip()}:"
                f"{str((item.get('inferential_commitment', {}) if isinstance(item.get('inferential_commitment'), dict) else {}).get('support_antecedent_schema', '')).strip()}=>"
                f"{str((item.get('inferential_commitment', {}) if isinstance(item.get('inferential_commitment'), dict) else {}).get('target_consequence_schema', '')).strip()}:"
                f"invariant={str((item.get('inferential_commitment', {}) if isinstance(item.get('inferential_commitment'), dict) else {}).get('preserved_invariant', '')).strip()}:"
                f"barrier={str((item.get('inferential_commitment', {}) if isinstance(item.get('inferential_commitment'), dict) else {}).get('barrier_scope', '')).strip()}"
                for item in report.get("results", [])[:8]
                if isinstance(item, dict)
            ]
        ),
    )

    if args.output_json:
        out_json = Path(args.output_json)
    else:
        slug = _slug_from_phyp_path(phyp_path)
        out_json = Path("artifacts") / slug / "hypothesis-evaluation.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[OK] Wrote JSON: {out_json}")
    logger.add_output("hypothesis_evaluation_json", out_json)

    markdown = _to_markdown(report)
    if args.output_md:
        out_md = Path(args.output_md)
    else:
        slug = _slug_from_phyp_path(phyp_path)
        out_md = Path("artifacts") / slug / "hypothesis-evaluation.md"
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(markdown, encoding="utf-8")
    print(f"[OK] Wrote Markdown: {out_md}")
    logger.add_output("hypothesis_evaluation_md", out_md)

    if args.output_phyp_md:
        phyp_md = Path(args.output_phyp_md)
        phyp_md.parent.mkdir(parents=True, exist_ok=True)
        phyp_md.write_text(markdown, encoding="utf-8")
        print(f"[OK] Wrote phyp Markdown: {phyp_md}")
        logger.add_output("hypothesis_evaluation_phyp_md", phyp_md)

    if args.output_phyp:
        out_phyp = Path(args.output_phyp)
        out_phyp.parent.mkdir(parents=True, exist_ok=True)
        updated_payload = copy.deepcopy(payload)
        updated_payload = apply_results_to_payload(
            payload=updated_payload,
            results=report.get("results", []),
            round_index=1,
        )
        updated_payload["metadata"]["evaluation_report_json"] = str(out_json)
        updated_payload["metadata"]["evaluation_report_md"] = str(out_md)
        out_phyp.write_text(
            yaml.safe_dump(updated_payload, sort_keys=False, allow_unicode=False, width=1000),
            encoding="utf-8",
        )
        print(f"[OK] Wrote Updated Hypotheses: {out_phyp}")
        logger.add_output("updated_hypotheses_yaml", out_phyp)

    verdict_counts = report.get("summary", {}).get("verdict_counts", {})
    print(f"[OK] Evaluated hypotheses: {report.get('metadata', {}).get('hypothesis_count', 0)}")
    print(f"[OK] Supported: {verdict_counts.get('supported', 0) + verdict_counts.get('provisionally-supported', 0)}")
    print(f"[OK] Refuted: {verdict_counts.get('refuted', 0) + verdict_counts.get('provisionally-refuted', 0)}")
    print(f"[OK] Inconclusive: {verdict_counts.get('inconclusive', 0)}")

    top_result = next(iter(report.get("results", [])), None)
    if isinstance(top_result, dict):
        logger.step(
            "Top-ranked hypothesis result",
            "\n".join(
                [
                    f"hypothesis_id={top_result.get('hypothesis_id', '')}",
                    f"verdict={top_result.get('verdict', '')}",
                    f"support_score={top_result.get('support_score', 0.0)}",
                    f"refute_score={top_result.get('refute_score', 0.0)}",
                ]
            ),
        )

    log_path = logger.finalize(
        "success",
        summary=f"Evaluated {report.get('metadata', {}).get('hypothesis_count', 0)} hypotheses.",
    )
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
