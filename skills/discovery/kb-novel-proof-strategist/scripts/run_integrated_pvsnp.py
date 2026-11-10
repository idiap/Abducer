#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""Run integrated test across hardness, bridge, strategy, and hypothesis-validation skills on P vs NP artifacts."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from reasoning_log import ReasoningLogger


_LOG_LINE_RE = re.compile(r"^\[LOG\]\s+(.+?)\s*$")


def _extract_log_paths(text: str) -> list[str]:
    """
    Relevance: Operates within the proof strategy design layer.
    Concept: Extraction of structured signals from raw text or artifact payloads.
    Contribution: Provides clean, typed inputs so downstream reasoning steps remain auditable.
    """

    paths: list[str] = []
    for line in text.splitlines():
        match = _LOG_LINE_RE.match(line.strip())
        if not match:
            continue
        path_text = match.group(1).strip()
        if path_text:
            paths.append(path_text)
    return paths


def _run(cmd: list[str], logger: ReasoningLogger, stage: str) -> None:
    """
    Relevance: Operates within the proof strategy design layer.
    Concept: Controlled subprocess execution with logging and error propagation.
    Contribution: Ensures stage execution is traceable and integrated into run-level reasoning logs.
    """

    logger.step(
        f"Running stage: {stage}",
        "\n".join(
            [
                "command=" + " ".join(cmd),
            ]
        ),
    )
    print("[RUN]", " ".join(cmd))
    env = os.environ.copy()
    env["ABDUCER_RUN_ID"] = logger.run_id
    result = subprocess.run(cmd, check=False, capture_output=True, text=True, env=env)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    for idx, log_path in enumerate(_extract_log_paths((result.stdout or "") + "\n" + (result.stderr or "")), start=1):
        logger.add_output(f"{stage}.reasoning_log.{idx}", log_path)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, cmd, output=result.stdout, stderr=result.stderr)
    logger.step(f"Completed stage: {stage}")


def main() -> int:
    """
    Relevance: Operates within the proof strategy design layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds parsing, computation, and artifact emission into a reproducible script execution.
    """

    logger = ReasoningLogger("kb-novel-proof-strategist")
    repo = Path(__file__).resolve().parents[4]
    py = sys.executable

    kb = repo / "KB" / "p-vs-np.kb.md"
    kb_slug = kb.name[: -len(".kb.md")] if kb.name.endswith(".kb.md") else kb.stem
    artifacts_dir = repo / "artifacts" / kb_slug
    concept = artifacts_dir / "concept-evolution.md"
    analysis = artifacts_dir / "connection-analysis.json"
    entrypoints = artifacts_dir / "entrypoints.json"
    pathways = artifacts_dir / "entrypoint-pathways.json"
    phyp = repo / "phyp" / "p-vs-np.proof-hypotheses.yaml"
    coherence_json = artifacts_dir / "coherence-report.json"
    coherence_md = artifacts_dir / "coherence-report.md"

    hardness_json = artifacts_dir / "epistemic-hardness.json"
    hardness_md = artifacts_dir / "epistemic-hardness.md"

    bridges_json = artifacts_dir / "bridge-plan.json"
    bridges_md = artifacts_dir / "bridge-plan.md"

    strategies_json = artifacts_dir / "proof-strategies.json"
    strategies_md = artifacts_dir / "proof-strategies.md"
    novelty_prompt = artifacts_dir / "novelty-maximizing-prompt.txt"
    hypothesis_eval_json = artifacts_dir / "hypothesis-evaluation.json"
    hypothesis_eval_md = artifacts_dir / "hypothesis-evaluation.md"
    phyp_eval_md = repo / "phyp" / "p-vs-np.hypotheses-evaluated.md"
    reviewed_phyp = repo / "phyp" / "p-vs-np.hypotheses-reviewed.yaml"
    hypothesis_loop_json = artifacts_dir / "hypothesis-refutation-loop.json"
    hypothesis_loop_md = artifacts_dir / "hypothesis-refutation-loop.md"
    phyp_review_md = repo / "phyp" / "p-vs-np.hypotheses-reviewed.md"
    revision_json = artifacts_dir / "revision-loop.json"
    revision_md = artifacts_dir / "revision-loop.md"
    process_report_md = artifacts_dir / "reasoning-process-report.md"
    discovery_report_md = artifacts_dir / "discovery-interpretation-report.md"
    log_index_json = artifacts_dir / "reasoning-log-index.json"
    log_index_md = artifacts_dir / "reasoning-log-index.md"

    logger.step(
        "Prepared integrated PvsNP run",
        "\n".join(
            [
                f"kb={kb}",
                f"concept={concept}",
                f"analysis={analysis}",
                f"entrypoints={entrypoints}",
                f"pathways={pathways}",
                f"phyp={phyp}",
                f"artifacts_dir={artifacts_dir}",
            ]
        ),
    )

    for p in [kb, concept, analysis, entrypoints, pathways, phyp]:
        if not p.exists():
            log_path = logger.finalize("error", summary=f"Missing input: {p}")
            print(f"[LOG] {log_path}", file=sys.stderr)
            raise SystemExit(f"[ERROR] Missing input: {p}")

    try:
        _run(
            [
                py,
                str(repo / "skills" / "discovery" / "kb-coherence-evaluator" / "scripts" / "evaluate_coherence.py"),
                "--kb",
                str(kb),
                "--analysis",
                str(analysis),
                "--phyp",
                str(phyp),
                "--output-json",
                str(coherence_json),
                "--output-md",
                str(coherence_md),
            ],
            logger=logger,
            stage="coherence-evaluator",
        )

        _run(
            [
                py,
                str(repo / "skills" / "discovery" / "kb-epistemic-hardness" / "scripts" / "articulate_hardness.py"),
                "--problem",
                "P vs NP",
                "--kb",
                str(kb),
                "--concept",
                str(concept),
                "--analysis",
                str(analysis),
                "--entrypoints",
                str(entrypoints),
                "--pathways",
                str(pathways),
                "--phyp",
                str(phyp),
                "--output-json",
                str(hardness_json),
                "--output-md",
                str(hardness_md),
            ],
            logger=logger,
            stage="epistemic-hardness",
        )

        _run(
            [
                py,
                str(repo / "skills" / "discovery" / "kb-concept-bridge-planner" / "scripts" / "plan_bridges.py"),
                "--analysis",
                str(analysis),
                "--entrypoints",
                str(entrypoints),
                "--pathways",
                str(pathways),
                "--phyp",
                str(phyp),
                "--coherence-report",
                str(coherence_json),
                "--concept",
                str(concept),
                "--top-k",
                "20",
                "--output-json",
                str(bridges_json),
                "--output-md",
                str(bridges_md),
            ],
            logger=logger,
            stage="concept-bridge-planner",
        )

        _run(
            [
                py,
                str(repo / "skills" / "discovery" / "kb-novel-proof-strategist" / "scripts" / "design_strategies.py"),
                "--entrypoints",
                str(entrypoints),
                "--pathways",
                str(pathways),
                "--bridges",
                str(bridges_json),
                "--phyp",
                str(phyp),
                "--coherence-report",
                str(coherence_json),
                "--top-k",
                "6",
                "--output-json",
                str(strategies_json),
                "--output-md",
                str(strategies_md),
                "--output-prompt",
                str(novelty_prompt),
            ],
            logger=logger,
            stage="novel-proof-strategist",
        )

        _run(
            [
                py,
                str(repo / "skills" / "evaluation" / "kb-hypothesis-evaluator" / "scripts" / "evaluate_hypotheses.py"),
                "--kb",
                str(kb),
                "--phyp",
                str(phyp),
                "--analysis",
                str(analysis),
                "--coherence-report",
                str(coherence_json),
                "--output-json",
                str(hypothesis_eval_json),
                "--output-md",
                str(hypothesis_eval_md),
                "--output-phyp-md",
                str(phyp_eval_md),
            ],
            logger=logger,
            stage="hypothesis-evaluator",
        )

        _run(
            [
                py,
                str(repo / "skills" / "evaluation" / "kb-hypothesis-refutation-loop" / "scripts" / "iterate_hypotheses.py"),
                "--kb",
                str(kb),
                "--phyp",
                str(phyp),
                "--analysis",
                str(analysis),
                "--coherence-report",
                str(coherence_json),
                "--rounds",
                "3",
                "--output-json",
                str(hypothesis_loop_json),
                "--output-md",
                str(hypothesis_loop_md),
                "--output-phyp-md",
                str(phyp_review_md),
                "--output-phyp",
                str(reviewed_phyp),
            ],
            logger=logger,
            stage="hypothesis-refutation-loop",
        )

        _run(
            [
                py,
                str(repo / "skills" / "evaluation" / "kb-revision-loop" / "scripts" / "revise_ontology.py"),
                "--kb",
                str(kb),
                "--phyp",
                str(reviewed_phyp),
                "--hypothesis-loop",
                str(hypothesis_loop_json),
                "--coherence-report",
                str(coherence_json),
                "--hardness",
                str(hardness_json),
                "--output-json",
                str(revision_json),
                "--output-md",
                str(revision_md),
            ],
            logger=logger,
            stage="revision-loop",
        )

        _run(
            [
                py,
                str(repo / "skills" / "orchestration" / "kb-orchestrator" / "scripts" / "export_phyp_docs.py"),
                "--phyp-dir",
                str(repo / "phyp"),
                "--pattern",
                "*.md",
                "--pdf-engine",
                "xelatex",
            ],
            logger=logger,
            stage="phyp-doc-export",
        )

        _run(
            [
                py,
                str(repo / "skills" / "orchestration" / "kb-orchestrator" / "scripts" / "generate_interpretation_reports.py"),
                "--artifacts-dir",
                str(artifacts_dir),
                "--kb",
                str(kb),
                "--output-process-md",
                str(process_report_md),
                "--output-discovery-md",
                str(discovery_report_md),
            ],
            logger=logger,
            stage="interpretation-reports",
        )

        log_index_cmd = [
            py,
            str(repo / "skills" / "orchestration" / "kb-orchestrator" / "scripts" / "generate_reasoning_log_index.py"),
            "--artifacts-dir",
            str(artifacts_dir),
            "--kb",
            str(kb),
            "--reasoning-log-root",
            str(repo / "artifacts" / "reasoning-logs"),
            "--run-id",
            str(logger.run_id),
            "--output-json",
            str(log_index_json),
            "--output-md",
            str(log_index_md),
            "--expected-agent",
            "kb-novel-proof-strategist",
            "--expected-agent",
            "kb-coherence-evaluator",
            "--expected-agent",
            "kb-epistemic-hardness",
            "--expected-agent",
            "kb-concept-bridge-planner",
            "--expected-agent",
            "kb-hypothesis-evaluator",
            "--expected-agent",
            "kb-hypothesis-refutation-loop",
            "--expected-agent",
            "kb-revision-loop",
            "--expected-agent",
            "phyp-doc-exporter",
            "--expected-agent",
            "kb-interpretation-reporter",
            "--expected-agent",
            "kb-log-indexer",
        ]
        _run(log_index_cmd, logger=logger, stage="reasoning-log-index")
    except subprocess.CalledProcessError as exc:
        log_path = logger.finalize("error", summary=f"Integrated run failed with exit code {exc.returncode}.")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(exc.returncode)

    logger.add_output("hardness_report_json", hardness_json)
    logger.add_output("hardness_report_md", hardness_md)
    logger.add_output("coherence_report_json", coherence_json)
    logger.add_output("coherence_report_md", coherence_md)
    logger.add_output("bridge_plan_json", bridges_json)
    logger.add_output("bridge_plan_md", bridges_md)
    logger.add_output("strategy_report_json", strategies_json)
    logger.add_output("strategy_report_md", strategies_md)
    logger.add_output("novelty_prompt", novelty_prompt)
    logger.add_output("hypothesis_evaluation_json", hypothesis_eval_json)
    logger.add_output("hypothesis_evaluation_md", hypothesis_eval_md)
    logger.add_output("hypothesis_evaluation_phyp_md", phyp_eval_md)
    logger.add_output("hypothesis_refutation_loop_json", hypothesis_loop_json)
    logger.add_output("hypothesis_refutation_loop_md", hypothesis_loop_md)
    logger.add_output("hypothesis_refutation_loop_phyp_md", phyp_review_md)
    logger.add_output("reviewed_hypotheses_yaml", reviewed_phyp)
    logger.add_output("revision_loop_json", revision_json)
    logger.add_output("revision_loop_md", revision_md)
    logger.add_output("reasoning_process_report_md", process_report_md)
    logger.add_output("discovery_interpretation_report_md", discovery_report_md)
    logger.add_output("reasoning_log_index_json", log_index_json)
    logger.add_output("reasoning_log_index_md", log_index_md)

    print("[OK] Integrated PvsNP test completed.")
    print(f"[OK] Hardness report: {hardness_json}")
    print(f"[OK] Bridge plan: {bridges_json}")
    print(f"[OK] Strategy report: {strategies_json}")
    print(f"[OK] Novelty prompt: {novelty_prompt}")
    print(f"[OK] Hypothesis evaluation: {hypothesis_eval_json}")
    print(f"[OK] Hypothesis refutation loop: {hypothesis_loop_json}")
    print(f"[OK] Revision loop: {revision_json}")
    print(f"[OK] Process report: {process_report_md}")
    print(f"[OK] Discovery report: {discovery_report_md}")
    print(f"[OK] Reasoning log index: {log_index_md}")
    print(f"[OK] phyp evaluation markdown: {phyp_eval_md}")
    print(f"[OK] phyp refutation markdown: {phyp_review_md}")
    print(f"[OK] Reviewed hypotheses: {reviewed_phyp}")
    log_path = logger.finalize("success", summary="Integrated PvsNP test completed successfully.")
    print(f"[LOG] {log_path}")
    env = os.environ.copy()
    env["ABDUCER_RUN_ID"] = logger.run_id
    refresh = subprocess.run(log_index_cmd, check=False, capture_output=True, text=True, env=env)
    if refresh.stdout:
        print(refresh.stdout, end="")
    if refresh.stderr:
        print(refresh.stderr, end="", file=sys.stderr)
    if refresh.returncode != 0:
        print(
            "[WARN] Post-finalize reasoning-log index refresh failed "
            f"(exit={refresh.returncode}).",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
