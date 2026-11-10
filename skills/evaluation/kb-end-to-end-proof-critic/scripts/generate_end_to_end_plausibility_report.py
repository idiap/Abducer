#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Generate an end-to-end proof plausibility report from current artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from end_to_end_plausibility import build_plausibility_report_from_artifacts
from end_to_end_plausibility import render_plausibility_markdown
from kb_context import kb_ref_from_artifacts_dir
from reasoning_log import ReasoningLogger


def write_report(report: dict, *, output_json: Path, output_md: Path) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    output_md.write_text(render_plausibility_markdown(report), encoding="utf-8")


def main() -> int:
    logger = ReasoningLogger("kb-end-to-end-proof-critic")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifacts-dir", required=True, help="Path to artifacts/<kb-ref>.")
    ap.add_argument("--output-json", default="", help="Optional output JSON path.")
    ap.add_argument("--output-md", default="", help="Optional output Markdown path.")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    artifacts_dir = Path(args.artifacts_dir)
    if not artifacts_dir.is_absolute():
        artifacts_dir = (repo_root / artifacts_dir).resolve()
    kb_ref = kb_ref_from_artifacts_dir(artifacts_dir)
    if not kb_ref:
        raise SystemExit("[ERROR] Could not resolve kb_ref for end-to-end proof critic.")

    output_json = Path(args.output_json) if args.output_json else artifacts_dir / "end-to-end-proof-plausibility.json"
    output_md = Path(args.output_md) if args.output_md else artifacts_dir / "end-to-end-proof-plausibility.md"
    if not output_json.is_absolute():
        output_json = (repo_root / output_json).resolve()
    if not output_md.is_absolute():
        output_md = (repo_root / output_md).resolve()

    report = build_plausibility_report_from_artifacts(repo_root, artifacts_dir)
    write_report(report, output_json=output_json, output_md=output_md)

    decision = report.get("decision", {}) if isinstance(report.get("decision"), dict) else {}
    logger.step(
        "Generated end-to-end proof plausibility report",
        "\n".join(
            [
                f"kb_ref={kb_ref}",
                f"plausibility_score={report.get('plausibility_score', 0.0):.3f}",
                f"plausible_solution_detected={decision.get('plausible_solution_detected', False)}",
                f"decision={decision.get('decision', '')}",
            ]
        ),
        surface_focus="end-to-end-proof-plausibility",
        surface_stage="proof-critic",
        surface_metrics={
            "plausibility_score": float(report.get("plausibility_score", 0.0) or 0.0),
            "critic_count": int(report.get("metadata", {}).get("critic_count", 0) or 0),
            "plausible_solution_detected": 1 if decision.get("plausible_solution_detected") else 0,
        },
        surface_taxonomy={"reasoning_types": ["proof-critic", "plausibility-assessment"]},
    )
    logger.add_output("end_to_end_plausibility_json", output_json)
    logger.add_output("end_to_end_plausibility_md", output_md)
    log_path = logger.finalize(
        "success",
        summary=f"Generated end-to-end proof plausibility report for `{kb_ref}`.",
    )
    print(f"[OK] Wrote plausibility JSON: {output_json}")
    print(f"[OK] Wrote plausibility Markdown: {output_md}")
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
