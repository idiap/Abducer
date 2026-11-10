# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""Iteratively evaluate proof hypotheses and converge toward support/refutation outcomes."""

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
from hypothesis_eval import is_resolved_status
from hypothesis_eval import load_analysis_scores
from hypothesis_eval import load_coherence_signals
from hypothesis_eval import load_hypothesis_evidence
from hypothesis_eval import load_hypothesis_payload
from hypothesis_eval import load_kb_statements
from reasoning_log import ReasoningLogger


def _slug_from_phyp_path(path: Path) -> str:
    """
    Relevance: Operates within the iterative refutation loop layer.
    Concept: Stable naming and path-derivation helper for artifact routing.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    name = path.name
    if name.endswith(".proof-hypotheses.yaml"):
        return name[: -len(".proof-hypotheses.yaml")]
    return path.stem or "kb"


def _round_threshold(start: float, step: float, round_index: int, floor: float = 0.45) -> float:
    """
    Relevance: Operates within the iterative refutation loop layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    return max(floor, min(1.0, start - step * max(0, round_index - 1)))


def _to_markdown(report: dict[str, Any]) -> str:
    """
    Relevance: Operates within the iterative refutation loop layer.
    Concept: Rendering internal outputs into human-readable artifacts.
    Contribution: Improves interpretability by exposing machine results in analyst-friendly form.
    """

    lines: list[str] = []
    lines.append("# Hypothesis Refutation Loop Report")
    lines.append("")

    meta = report.get("metadata", {})
    lines.append("## Stats")
    lines.append("")
    lines.append(f"- KB: {meta.get('kb', '')}")
    lines.append(f"- Hypotheses: {meta.get('hypothesis_count', 0)}")
    lines.append(f"- Rounds requested: {meta.get('rounds_requested', 0)}")
    lines.append(f"- Rounds executed: {meta.get('rounds_executed', 0)}")
    lines.append(f"- Force final resolution: {meta.get('force_final_resolution', False)}")
    lines.append(f"- Anneal without new evidence: {meta.get('anneal_without_new_evidence', False)}")
    lines.append(f"- Global coherence baseline: {meta.get('global_coherence', 0.0)}")
    lines.append(f"- Belief revisions: {len(report.get('belief_revision_actions', []))}")
    lines.append("")

    lines.append("## Round Summaries")
    lines.append("")
    lines.append(
        "| round | support_threshold | refute_threshold | evidence_items | resolved_this_round | supported | refuted | provisional | inconclusive |"
    )
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for r in report.get("rounds", []):
        counts = r.get("verdict_counts", {})
        lines.append(
            "| {round} | {st:.4f} | {rt:.4f} | {evidence} | {resolved} | {sup} | {ref} | {prov} | {inc} |".format(
                round=r.get("round", 0),
                st=float(r.get("support_threshold", 0.0) or 0.0),
                rt=float(r.get("refute_threshold", 0.0) or 0.0),
                evidence=int(r.get("evidence_items", 0) or 0),
                resolved=int(r.get("resolved_this_round", 0) or 0),
                sup=int(counts.get("supported", 0) + counts.get("provisionally-supported", 0)),
                ref=int(counts.get("refuted", 0) + counts.get("provisionally-refuted", 0)),
                prov=int(counts.get("provisionally-supported", 0) + counts.get("provisionally-refuted", 0)),
                inc=int(counts.get("inconclusive", 0)),
            )
        )
    lines.append("")

    final_summary = report.get("final_summary", {})
    lines.append("## Final Status")
    lines.append("")
    lines.append(f"- Supported: {final_summary.get('supported_count', 0)}")
    lines.append(f"- Refuted: {final_summary.get('refuted_count', 0)}")
    lines.append(f"- Provisionally supported: {final_summary.get('provisionally_supported_count', 0)}")
    lines.append(f"- Provisionally refuted: {final_summary.get('provisionally_refuted_count', 0)}")
    lines.append(f"- Open (unresolved + provisional): {final_summary.get('open_count', 0)}")
    lines.append("")

    lines.append("## Promotion Candidates")
    lines.append("")
    for item in report.get("promotion_candidates", []):
        lines.append(
            f"- {item.get('hypothesis_id', '')} (priority={item.get('priority', 0.0)}, confidence={item.get('confidence', 0.0)})"
        )
    if not report.get("promotion_candidates"):
        lines.append("- none")
    lines.append("")

    lines.append("## Refutation Candidates")
    lines.append("")
    for item in report.get("refutation_candidates", []):
        lines.append(
            f"- {item.get('hypothesis_id', '')} (priority={item.get('priority', 0.0)}, confidence={item.get('confidence', 0.0)})"
        )
    if not report.get("refutation_candidates"):
        lines.append("- none")
    lines.append("")

    lines.append("## Belief Revision Actions")
    lines.append("")
    for item in report.get("belief_revision_actions", []):
        lines.append(f"- {item.get('hypothesis_id', '')}: {item.get('action', '')} ({item.get('reason', '')})")
    if not report.get("belief_revision_actions"):
        lines.append("- none")
    lines.append("")
    return "\n".join(lines) + "\n"


def _pending_hypothesis_ids(payload: dict[str, Any]) -> list[str]:
    """
    Relevance: Operates within the iterative refutation loop layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    out: list[str] = []
    for h in payload.get("hypotheses", []):
        if not isinstance(h, dict):
            continue
        hid = str(h.get("id", "")).strip()
        status = str(h.get("status", "tentative")).strip().lower()
        if hid and not is_resolved_status(status):
            out.append(hid)
    return out


def _index_results(results: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """
    Relevance: Operates within the iterative refutation loop layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    out: dict[str, dict[str, Any]] = {}
    for item in results:
        if not isinstance(item, dict):
            continue
        hid = str(item.get("hypothesis_id", "")).strip()
        if hid:
            out[hid] = item
    return out


def _belief_revision_step(
    payload: dict[str, Any],
    results: list[dict[str, Any]],
    min_coherence_keep: float,
    severe_negative_coherence: float,
    margin: float,
) -> list[dict[str, Any]]:
    """
    Relevance: Operates within the iterative refutation loop layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    by_id = _index_results(results)
    actions: list[dict[str, Any]] = []

    for hyp in payload.get("hypotheses", []):
        if not isinstance(hyp, dict):
            continue
        hid = str(hyp.get("id", "")).strip()
        if not hid or hid not in by_id:
            continue
        result = by_id[hid]
        status = str(hyp.get("status", "tentative")).strip().lower()
        signals = result.get("signals", {}) if isinstance(result.get("signals"), dict) else {}
        coherence_delta = float(signals.get("coherence_delta_global", 0.0) or 0.0)
        support_score = float(result.get("support_score", 0.0) or 0.0)
        refute_score = float(result.get("refute_score", 0.0) or 0.0)

        if status in {"supported", "provisionally-supported"} and coherence_delta < min_coherence_keep:
            hyp["status"] = "tentative"
            action = {
                "hypothesis_id": hid,
                "action": "demote-to-tentative",
                "reason": f"coherence_delta_global={coherence_delta:.4f} below keep threshold {min_coherence_keep:.4f}",
            }
            actions.append(action)
        elif status in {"tentative", "needs-testing"} and coherence_delta < severe_negative_coherence:
            if refute_score >= support_score + margin:
                hyp["status"] = "provisionally-refuted"
                action = {
                    "hypothesis_id": hid,
                    "action": "mark-provisionally-refuted",
                    "reason": (
                        f"severe negative coherence ({coherence_delta:.4f}) with refute dominance "
                        f"(refute={refute_score:.4f}, support={support_score:.4f})"
                    ),
                }
                actions.append(action)

    if actions:
        meta = payload.get("metadata")
        if not isinstance(meta, dict):
            meta = {}
            payload["metadata"] = meta
        hist = meta.get("belief_revision_history")
        if not isinstance(hist, list):
            hist = []
            meta["belief_revision_history"] = hist
        hist.extend(actions)
    return actions


def _load_round_evidence(round_evidence_dir: Path | None, round_idx: int) -> tuple[dict[str, dict[str, Any]], Path | None]:
    """
    Relevance: Operates within the iterative refutation loop layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Provides clean, typed inputs so downstream reasoning steps remain auditable.
    """

    if round_evidence_dir is None:
        return {}, None
    evidence_path = round_evidence_dir / f"round-{round_idx}.json"
    if not evidence_path.exists():
        evidence_path = round_evidence_dir / f"round-{round_idx}.yaml"
        if not evidence_path.exists():
            return {}, None
    return load_hypothesis_evidence(evidence_path), evidence_path


def main() -> int:
    """
    Relevance: Operates within the iterative refutation loop layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds parsing, computation, and artifact emission into a reproducible script execution.
    """

    logger = ReasoningLogger("kb-hypothesis-refutation-loop")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--kb", required=True, help="Path to KB markdown file.")
    ap.add_argument("--phyp", required=True, help="Path to proof hypothesis YAML.")
    ap.add_argument("--analysis", help="Optional connection-analysis JSON/YAML.")
    ap.add_argument("--coherence-report", help="Optional coherence-report JSON/YAML.")
    ap.add_argument("--rounds", type=int, default=3, help="Maximum number of rounds.")
    ap.add_argument("--start-support-threshold", type=float, default=0.66)
    ap.add_argument("--start-refute-threshold", type=float, default=0.66)
    ap.add_argument("--threshold-step", type=float, default=0.05, help="Per-round threshold decrement.")
    ap.add_argument("--margin", type=float, default=0.08)
    ap.add_argument("--min-coherence-keep", type=float, default=0.0)
    ap.add_argument("--severe-negative-coherence", type=float, default=-0.12)
    ap.add_argument(
        "--round-evidence-dir",
        help="Optional directory containing round evidence files named round-<n>.json|yaml.",
    )
    ap.add_argument(
        "--anneal-without-new-evidence",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="If false, stop before round>1 when no new round evidence is available.",
    )
    ap.add_argument(
        "--force-final-resolution",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Force supported/refuted decision in final round for unresolved hypotheses.",
    )
    ap.add_argument("--output-json", help="Output JSON path.")
    ap.add_argument("--output-md", help="Output Markdown path.")
    ap.add_argument("--output-phyp-md", help="Optional output path for Markdown mirror under phyp/.")
    ap.add_argument("--output-phyp", help="Output updated hypotheses YAML path.")
    args = ap.parse_args()

    logger.step(
        "Parsed refutation-loop arguments",
        "\n".join(
            [
                f"kb={args.kb}",
                f"phyp={args.phyp}",
                f"analysis={args.analysis or ''}",
                f"coherence_report={args.coherence_report or ''}",
                f"rounds={args.rounds}",
                f"start_support_threshold={args.start_support_threshold}",
                f"start_refute_threshold={args.start_refute_threshold}",
                f"threshold_step={args.threshold_step}",
                f"margin={args.margin}",
                f"min_coherence_keep={args.min_coherence_keep}",
                f"severe_negative_coherence={args.severe_negative_coherence}",
                f"round_evidence_dir={args.round_evidence_dir or ''}",
                f"anneal_without_new_evidence={args.anneal_without_new_evidence}",
                f"force_final_resolution={args.force_final_resolution}",
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
    coherence_path = Path(args.coherence_report) if args.coherence_report else None
    round_evidence_dir = Path(args.round_evidence_dir) if args.round_evidence_dir else None

    for p in [kb_path, phyp_path]:
        if not p.exists():
            log_path = logger.finalize("error", summary=f"Missing input: {p}")
            print(f"[LOG] {log_path}", file=sys.stderr)
            raise SystemExit(f"[ERROR] Missing input: {p}")
    if analysis_path and not analysis_path.exists():
        log_path = logger.finalize("error", summary=f"Missing analysis file: {analysis_path}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Missing analysis file: {analysis_path}")
    if coherence_path and not coherence_path.exists():
        log_path = logger.finalize("error", summary=f"Missing coherence report: {coherence_path}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Missing coherence report: {coherence_path}")
    if round_evidence_dir and not round_evidence_dir.exists():
        log_path = logger.finalize("error", summary=f"Missing evidence directory: {round_evidence_dir}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] Missing evidence directory: {round_evidence_dir}")

    try:
        base_payload = load_hypothesis_payload(phyp_path)
        statements = load_kb_statements(kb_path)
        analysis_scores = load_analysis_scores(analysis_path)
        coherence_by_hypothesis, coherence_profile = load_coherence_signals(coherence_path)
    except Exception as exc:
        log_path = logger.finalize("error", summary=f"Failed to parse inputs: {exc}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise

    payload = copy.deepcopy(base_payload)
    max_rounds = max(1, args.rounds)
    round_reports: list[dict[str, Any]] = []
    results_index: dict[str, dict[str, Any]] = {}
    belief_revision_actions: list[dict[str, Any]] = []

    logger.step(
        "Loaded loop inputs",
        "\n".join(
            [
                f"statement_count={len(statements)}",
                f"hypothesis_count={len(payload.get('hypotheses', []))}",
                f"analysis_pairs={len(analysis_scores)}",
                f"coherence_items={len(coherence_by_hypothesis)}",
            ]
        ),
    )

    for round_idx in range(1, max_rounds + 1):
        pending_ids = _pending_hypothesis_ids(payload)
        if not pending_ids:
            logger.step("Loop converged", f"All hypotheses resolved before round {round_idx}.")
            break

        support_threshold = _round_threshold(args.start_support_threshold, args.threshold_step, round_idx)
        refute_threshold = _round_threshold(args.start_refute_threshold, args.threshold_step, round_idx)
        force_resolution = bool(args.force_final_resolution and round_idx == max_rounds)
        round_evidence, round_evidence_path = _load_round_evidence(round_evidence_dir, round_idx)
        if round_idx > 1 and not round_evidence and not args.anneal_without_new_evidence and not force_resolution:
            logger.step(
                "Stopping due to missing new evidence",
                f"round={round_idx}\nreason=no round evidence and annealing disabled",
            )
            break

        pending_set = set(pending_ids)
        pending_hypotheses = [
            h
            for h in payload.get("hypotheses", [])
            if isinstance(h, dict) and str(h.get("id", "")).strip() in pending_set
        ]
        eval_report = evaluate_hypotheses(
            hypotheses=pending_hypotheses,
            statements=statements,
            analysis_scores=analysis_scores,
            evidence_by_hypothesis=round_evidence,
            coherence_by_hypothesis=coherence_by_hypothesis,
            coherence_profile=coherence_profile,
            support_threshold=support_threshold,
            refute_threshold=refute_threshold,
            margin=max(0.0, min(1.0, args.margin)),
            force_resolution=force_resolution,
        )

        verdict_counts = eval_report.get("summary", {}).get("verdict_counts", {})
        resolved_this_round = (
            int(verdict_counts.get("supported", 0))
            + int(verdict_counts.get("refuted", 0))
        )

        round_reports.append(
            {
                "round": round_idx,
                "pending_before_round": len(pending_ids),
                "support_threshold": round(support_threshold, 4),
                "refute_threshold": round(refute_threshold, 4),
                "margin": round(float(args.margin), 4),
                "force_resolution": force_resolution,
                "evidence_items": len(round_evidence),
                "evidence_path": str(round_evidence_path) if round_evidence_path else "",
                "verdict_counts": verdict_counts,
                "resolved_this_round": resolved_this_round,
            }
        )

        payload = apply_results_to_payload(payload=payload, results=eval_report.get("results", []), round_index=round_idx)
        round_revisions = _belief_revision_step(
            payload=payload,
            results=eval_report.get("results", []),
            min_coherence_keep=float(args.min_coherence_keep),
            severe_negative_coherence=float(args.severe_negative_coherence),
            margin=max(0.0, min(1.0, args.margin)),
        )
        if round_revisions:
            round_reports[-1]["belief_revisions"] = round_revisions
            belief_revision_actions.extend(round_revisions)
        results_index.update(_index_results(eval_report.get("results", [])))

        logger.step(
            f"Round {round_idx} complete",
            "\n".join(
                [
                    f"pending={len(pending_ids)}",
                    f"evidence_items={len(round_evidence)}",
                    f"resolved_this_round={resolved_this_round}",
                    f"supported={verdict_counts.get('supported', 0) + verdict_counts.get('provisionally-supported', 0)}",
                    f"refuted={verdict_counts.get('refuted', 0) + verdict_counts.get('provisionally-refuted', 0)}",
                    f"inconclusive={verdict_counts.get('inconclusive', 0)}",
                ]
            ),
        )

        if resolved_this_round == 0 and not force_resolution:
            continue

    hypotheses = [h for h in payload.get("hypotheses", []) if isinstance(h, dict)]
    supported_ids: list[str] = []
    refuted_ids: list[str] = []
    provisionally_supported_ids: list[str] = []
    provisionally_refuted_ids: list[str] = []
    unresolved_ids: list[str] = []

    for h in hypotheses:
        hid = str(h.get("id", "")).strip()
        status = str(h.get("status", "needs-testing")).strip().lower()
        if not hid:
            continue
        if status == "supported":
            supported_ids.append(hid)
        elif status == "refuted":
            refuted_ids.append(hid)
        elif status == "provisionally-supported":
            provisionally_supported_ids.append(hid)
        elif status == "provisionally-refuted":
            provisionally_refuted_ids.append(hid)
        else:
            unresolved_ids.append(hid)

    promotion_candidates: list[dict[str, Any]] = []
    refutation_candidates: list[dict[str, Any]] = []
    for hid, result in results_index.items():
        priority = float(result.get("priority", 0.0) or 0.0)
        confidence = float(result.get("confidence", 0.0) or 0.0)
        row = {
            "hypothesis_id": hid,
            "priority": round(priority, 4),
            "confidence": round(confidence, 4),
            "action": result.get("recommended_action", ""),
        }
        status = str(result.get("next_status", "needs-testing")).lower()
        if status in {"supported", "provisionally-supported"} and confidence >= 0.25:
            promotion_candidates.append(row)
        if status in {"refuted", "provisionally-refuted"}:
            refutation_candidates.append(row)

    promotion_candidates.sort(key=lambda x: (x["priority"], x["confidence"]), reverse=True)
    refutation_candidates.sort(key=lambda x: (x["priority"], x["confidence"]), reverse=True)

    final_report = {
        "metadata": {
            "kb": str(kb_path),
            "phyp_input": str(phyp_path),
            "analysis": str(analysis_path) if analysis_path else "",
            "coherence_report": str(coherence_path) if coherence_path else "",
            "hypothesis_count": len(hypotheses),
            "rounds_requested": max_rounds,
            "rounds_executed": len(round_reports),
            "round_evidence_dir": str(round_evidence_dir) if round_evidence_dir else "",
            "anneal_without_new_evidence": bool(args.anneal_without_new_evidence),
            "force_final_resolution": bool(args.force_final_resolution),
            "min_coherence_keep": float(args.min_coherence_keep),
            "severe_negative_coherence": float(args.severe_negative_coherence),
            "global_coherence": float(coherence_profile.get("global_coherence", 0.0) or 0.0),
        },
        "rounds": round_reports,
        "final_summary": {
            "supported_count": len(supported_ids),
            "refuted_count": len(refuted_ids),
            "provisionally_supported_count": len(provisionally_supported_ids),
            "provisionally_refuted_count": len(provisionally_refuted_ids),
            "unresolved_count": len(unresolved_ids),
            "open_count": len(unresolved_ids) + len(provisionally_supported_ids) + len(provisionally_refuted_ids),
            "supported_ids": supported_ids,
            "refuted_ids": refuted_ids,
            "provisionally_supported_ids": provisionally_supported_ids,
            "provisionally_refuted_ids": provisionally_refuted_ids,
            "unresolved_ids": unresolved_ids,
        },
        "promotion_candidates": promotion_candidates[:25],
        "refutation_candidates": refutation_candidates[:25],
        "belief_revision_actions": belief_revision_actions,
    }

    slug = _slug_from_phyp_path(phyp_path)
    out_json = Path(args.output_json) if args.output_json else Path("artifacts") / slug / "hypothesis-refutation-loop.json"
    out_md = Path(args.output_md) if args.output_md else Path("artifacts") / slug / "hypothesis-refutation-loop.md"
    out_phyp_md = Path(args.output_phyp_md) if args.output_phyp_md else None
    out_phyp = Path(args.output_phyp) if args.output_phyp else Path("phyp") / f"{slug}.hypotheses-reviewed.yaml"

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    if out_phyp_md:
        out_phyp_md.parent.mkdir(parents=True, exist_ok=True)
    out_phyp.parent.mkdir(parents=True, exist_ok=True)

    out_json.write_text(json.dumps(final_report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown = _to_markdown(final_report)
    out_md.write_text(markdown, encoding="utf-8")
    if out_phyp_md:
        out_phyp_md.write_text(markdown, encoding="utf-8")
    payload["metadata"]["refutation_loop_report_json"] = str(out_json)
    payload["metadata"]["refutation_loop_report_md"] = str(out_md)
    if out_phyp_md:
        payload["metadata"]["refutation_loop_report_phyp_md"] = str(out_phyp_md)
    out_phyp.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False, width=1000), encoding="utf-8")

    print(f"[OK] Wrote JSON: {out_json}")
    print(f"[OK] Wrote Markdown: {out_md}")
    if out_phyp_md:
        print(f"[OK] Wrote phyp Markdown: {out_phyp_md}")
    print(f"[OK] Wrote Updated Hypotheses: {out_phyp}")
    print(f"[OK] Supported: {len(supported_ids)}")
    print(f"[OK] Refuted: {len(refuted_ids)}")
    print(f"[OK] Provisionally supported: {len(provisionally_supported_ids)}")
    print(f"[OK] Provisionally refuted: {len(provisionally_refuted_ids)}")
    print(f"[OK] Open: {len(unresolved_ids) + len(provisionally_supported_ids) + len(provisionally_refuted_ids)}")

    logger.add_output("hypothesis_refutation_loop_json", out_json)
    logger.add_output("hypothesis_refutation_loop_md", out_md)
    if out_phyp_md:
        logger.add_output("hypothesis_refutation_loop_phyp_md", out_phyp_md)
    logger.add_output("updated_hypotheses_yaml", out_phyp)

    if promotion_candidates:
        top = promotion_candidates[0]
        logger.step(
            "Top promotion candidate",
            f"hypothesis_id={top['hypothesis_id']}\npriority={top['priority']}\nconfidence={top['confidence']}",
        )
    if refutation_candidates:
        top = refutation_candidates[0]
        logger.step(
            "Top refutation candidate",
            f"hypothesis_id={top['hypothesis_id']}\npriority={top['priority']}\nconfidence={top['confidence']}",
        )

    log_path = logger.finalize(
        "success",
        summary=(
            f"Executed {len(round_reports)} rounds; supported={len(supported_ids)}, "
            f"refuted={len(refuted_ids)}, open={len(unresolved_ids) + len(provisionally_supported_ids) + len(provisionally_refuted_ids)}."
        ),
    )
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
