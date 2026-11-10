# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""Executable orchestrator for deterministic KB skill routes.

The orchestrator is the control-plane for scripted skills:
- maps user intent to a stage route,
- enforces stage prerequisites,
- propagates a shared run ID to all child scripts,
- captures child reasoning logs and final artifacts.

Prompt-only skills (`kb-abduce`, `kb-deduce`, `kb-explain`, `kb-induce`) are
not executed here; this script handles deterministic Python stages.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from kb_context import canonical_artifacts_dir
from kb_context import resolve_kb_reference
from reasoning_log import ReasoningLogger


_LOG_LINE_RE = re.compile(r"^\[LOG\]\s+(.+?)\s*$")


def _extract_log_paths(text: str) -> list[str]:
    """
    Relevance: Operates within the orchestration and observability layer.
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


def _run(cmd: list[str], logger: ReasoningLogger, stage: str) -> list[Path]:
    """Run one stage command with run-id propagation and log capture."""
    logger.step(f"Running stage: {stage}", f"command={' '.join(cmd)}")
    print("[RUN]", " ".join(cmd))
    env = os.environ.copy()
    # Keep all stage logs correlated by a single orchestrator-level run ID.
    env["ABDUCER_RUN_ID"] = logger.run_id
    result = subprocess.run(cmd, check=False, capture_output=True, text=True, env=env)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    child_logs = _extract_log_paths((result.stdout or "") + "\n" + (result.stderr or ""))
    if child_logs:
        for idx, path in enumerate(child_logs, start=1):
            logger.add_output(f"{stage}.reasoning_log.{idx}", path)
    else:
        logger.step("No child log marker captured", f"stage={stage}")
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, cmd, output=result.stdout, stderr=result.stderr)
    logger.step(f"Completed stage: {stage}")
    return child_logs


def _path_or_default(path_str: str | None, default: Path) -> Path:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if path_str:
        return Path(path_str)
    return default


def _build_log_index_cmd(
    py: str,
    log_index_script: Path,
    artifacts_dir: Path,
    kb: Path,
    kb_ref: str,
    log_root: Path,
    run_id: str,
    log_index_json: Path,
    log_index_md: Path,
    expected_agents: set[str],
    expected_stages: set[str],
) -> list[str]:
    """Build a normalized command for run-level reasoning-log indexing."""
    cmd = [
        py,
        str(log_index_script),
        "--artifacts-dir",
        str(artifacts_dir),
        "--kb",
        str(kb),
        "--kb-ref",
        str(kb_ref),
        "--reasoning-log-root",
        str(log_root),
        "--run-id",
        str(run_id),
        "--output-json",
        str(log_index_json),
        "--output-md",
        str(log_index_md),
    ]
    for agent in sorted(expected_agents):
        cmd.extend(["--expected-agent", agent])
    for stage in sorted({s.strip() for s in expected_stages if s.strip()}):
        cmd.extend(["--expected-stage", stage])
    return cmd


def _build_surface_index_cmd(
    py: str,
    surface_index_script: Path,
    artifacts_dir: Path,
    kb: Path,
    kb_ref: str,
    surface_root: Path,
    run_id: str,
    surface_index_json: Path,
    surface_index_md: Path,
    expected_agents: set[str],
) -> list[str]:
    """Build a normalized command for run-level surfaced-reasoning indexing."""
    cmd = [
        py,
        str(surface_index_script),
        "--artifacts-dir",
        str(artifacts_dir),
        "--kb",
        str(kb),
        "--kb-ref",
        str(kb_ref),
        "--reasoning-surface-root",
        str(surface_root),
        "--run-id",
        str(run_id),
        "--output-json",
        str(surface_index_json),
        "--output-md",
        str(surface_index_md),
    ]
    for agent in sorted(expected_agents):
        cmd.extend(["--expected-agent", agent])
    return cmd


def _build_conceptual_dynamics_cmd(
    py: str,
    conceptual_dynamics_script: Path,
    artifacts_dir: Path,
    kb: Path,
    kb_ref: str,
    surface_root: Path,
    run_id: str,
    output_json: Path,
    output_md: Path,
    output_html: Path,
) -> list[str]:
    """Build a normalized command for conceptual-dynamics monitoring."""
    return [
        py,
        str(conceptual_dynamics_script),
        "--artifacts-dir",
        str(artifacts_dir),
        "--kb",
        str(kb),
        "--kb-ref",
        str(kb_ref),
        "--reasoning-surface-root",
        str(surface_root),
        "--run-id",
        str(run_id),
        "--output-json",
        str(output_json),
        "--output-md",
        str(output_md),
        "--output-html",
        str(output_html),
    ]


def _build_conceptual_space_animation_cmd(
    py: str,
    conceptual_space_animation_script: Path,
    artifacts_dir: Path,
    conceptual_dynamics_json: Path,
    output_json: Path,
    output_md: Path,
    output_html: Path,
) -> list[str]:
    """Build a normalized command for conceptual-space animation synthesis."""
    return [
        py,
        str(conceptual_space_animation_script),
        "--artifacts-dir",
        str(artifacts_dir),
        "--conceptual-dynamics",
        str(conceptual_dynamics_json),
        "--output-json",
        str(output_json),
        "--output-md",
        str(output_md),
        "--output-html",
        str(output_html),
    ]


def _build_search_space_tree_cmd(
    py: str,
    search_space_tree_script: Path,
    artifacts_dir: Path,
    kb_ref: str,
    run_id: str,
    state_json: Path,
    output_json: Path,
    output_md: Path,
) -> list[str]:
    """Build a normalized command for persistent search-space tree synthesis."""
    return [
        py,
        str(search_space_tree_script),
        "--artifacts-dir",
        str(artifacts_dir),
        "--kb-ref",
        str(kb_ref),
        "--run-id",
        str(run_id),
        "--state-json",
        str(state_json),
        "--output-json",
        str(output_json),
        "--output-md",
        str(output_md),
    ]


def _refresh_report_post_finalize(cmd: list[str], run_id: str) -> None:
    """Refresh derived run-level reports after orchestrator finalization.

    This ensures the orchestrator's own final status is included in the index.
    """
    env = os.environ.copy()
    env["ABDUCER_RUN_ID"] = run_id
    result = subprocess.run(cmd, check=False, capture_output=True, text=True, env=env)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.returncode != 0:
        print(
            "[WARN] Post-finalize report refresh failed "
            f"(exit={result.returncode}).",
            file=sys.stderr,
        )


def _resolve_phyp_doc_pattern(raw_pattern: str, kb_ref: str) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Stable naming and path-derivation helper for KB-scoped artifact export.
    Contribution: Keeps phyp document export isolated to the active KB instead of re-exporting unrelated problem artifacts.
    """

    pattern = str(raw_pattern or "").strip()
    if pattern:
        return pattern
    return f"{kb_ref}*.md"


def main() -> int:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds parsing, computation, and artifact emission into a reproducible script execution.
    """

    logger = ReasoningLogger("kb-orchestrator")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--intent",
        required=True,
        choices=[
            "cohere",
            "connect",
            "coherence-eval",
            "interpretation-reports",
            "process-graph",
            "reasoning-dynamics",
            "conceptual-dynamics",
            "conceptual-space-animation",
            "search-space-tree",
            "entrypoints",
            "hardness",
            "bridge-plan",
            "conjecture",
            "strategies",
            "proof-sketch",
            "expert-paper",
            "hypothesis-eval",
            "hypothesis-loop",
            "revision-loop",
            "abductive-loop",
            "pipeline",
        ],
    )
    ap.add_argument("--kb", required=True, help="Path to KB markdown file.")
    ap.add_argument("--concept", help="Path to concept-evolution markdown.")
    ap.add_argument("--analysis", help="Path to connection-analysis JSON.")
    ap.add_argument("--entrypoints", help="Path to entrypoints JSON.")
    ap.add_argument("--pathways", help="Path to entrypoint pathways JSON.")
    ap.add_argument("--phyp", help="Path to hypotheses YAML.")
    ap.add_argument("--coherence", help="Path to coherence-report JSON.")
    ap.add_argument("--bridges", help="Path to bridge-plan JSON.")
    ap.add_argument(
        "--kb-ref",
        default="",
        help="Optional canonical KB reference (e.g., p-vs-np). Must match front matter kb_id when present.",
    )
    ap.add_argument(
        "--artifacts-dir",
        help="Must match canonical artifacts/<kb-ref> for the reference KB; non-canonical values are rejected.",
    )
    ap.add_argument("--round-evidence-dir", help="Optional evidence directory for hypothesis loop.")
    ap.add_argument("--rounds", type=int, default=3, help="Round budget for hypothesis loop.")
    ap.add_argument(
        "--export-phyp-docs",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Export Markdown files in phyp/ to LaTeX and PDF after run.",
    )
    ap.add_argument(
        "--phyp-doc-pattern",
        default="",
        help="Glob pattern for phyp Markdown export (default: <kb-ref>*.md).",
    )
    ap.add_argument("--phyp-pdf-engine", default="xelatex", help="Pandoc PDF engine for phyp export.")
    ap.add_argument("--python", default=sys.executable, help="Python interpreter to use.")
    args = ap.parse_args()

    repo = Path(__file__).resolve().parents[4]
    py = args.python
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
        requested_artifacts_dir = Path(args.artifacts_dir)
        if not requested_artifacts_dir.is_absolute():
            requested_artifacts_dir = (repo / requested_artifacts_dir).resolve()
        if requested_artifacts_dir != expected_artifacts_dir:
            log_path = logger.finalize(
                "error",
                summary=(
                    "Non-canonical artifacts directory rejected. "
                    f"expected={expected_artifacts_dir} requested={requested_artifacts_dir}"
                ),
            )
            print(f"[LOG] {log_path}", file=sys.stderr)
            raise SystemExit(
                "[ERROR] artifacts are associated with the reference KB name. "
                f"Use canonical path: {expected_artifacts_dir.as_posix()}"
            )
    artifacts_dir = expected_artifacts_dir
    concept = _path_or_default(args.concept, artifacts_dir / "concept-evolution.md")
    analysis = _path_or_default(args.analysis, artifacts_dir / "connection-analysis.json")
    analysis_md = artifacts_dir / "connection-analysis.md"
    entrypoints = _path_or_default(args.entrypoints, artifacts_dir / "entrypoints.json")
    entrypoints_md = artifacts_dir / "entrypoints.md"
    pathways = _path_or_default(args.pathways, artifacts_dir / "entrypoint-pathways.json")
    pathways_md = artifacts_dir / "entrypoint-pathways.md"
    phyp = _path_or_default(args.phyp, repo / "phyp" / f"{kb_ref}.proof-hypotheses.yaml")
    coherence_json = _path_or_default(args.coherence, artifacts_dir / "coherence-report.json")
    coherence_md = artifacts_dir / "coherence-report.md"
    bridges = _path_or_default(args.bridges, artifacts_dir / "bridge-plan.json")
    bridges_md = artifacts_dir / "bridge-plan.md"
    conjectures_json = artifacts_dir / "concept-gap-abstractions.json"
    conjectures_md = artifacts_dir / "concept-gap-abstractions.md"
    hardness_json = artifacts_dir / "epistemic-hardness.json"
    hardness_md = artifacts_dir / "epistemic-hardness.md"
    strategies_json = artifacts_dir / "proof-strategies.json"
    strategies_md = artifacts_dir / "proof-strategies.md"
    novelty_prompt = artifacts_dir / "novelty-maximizing-prompt.txt"
    proof_sketches_json = artifacts_dir / "proof-sketches.json"
    proof_sketches_md = artifacts_dir / "proof-sketches.md"
    paper_style_argument_md = artifacts_dir / "paper-style-argument.md"
    hypothesis_eval_json = artifacts_dir / "hypothesis-evaluation.json"
    hypothesis_eval_md = artifacts_dir / "hypothesis-evaluation.md"
    phyp_eval_md = repo / "phyp" / f"{kb_ref}.hypotheses-evaluated.md"
    hypothesis_loop_json = artifacts_dir / "hypothesis-refutation-loop.json"
    hypothesis_loop_md = artifacts_dir / "hypothesis-refutation-loop.md"
    phyp_review_md = repo / "phyp" / f"{kb_ref}.hypotheses-reviewed.md"
    reviewed_phyp = repo / "phyp" / f"{kb_ref}.hypotheses-reviewed.yaml"
    revision_json = artifacts_dir / "revision-loop.json"
    revision_md = artifacts_dir / "revision-loop.md"
    revision_patched_kb = artifacts_dir / "kb.revised.md"
    revision_patched_phyp = artifacts_dir / "phyp.revised.yaml"
    process_report_md = artifacts_dir / "reasoning-process-report.md"
    discovery_report_md = artifacts_dir / "discovery-interpretation-report.md"
    log_index_json = artifacts_dir / "reasoning-log-index.json"
    log_index_md = artifacts_dir / "reasoning-log-index.md"
    surface_index_json = artifacts_dir / "reasoning-surface-index.json"
    surface_index_md = artifacts_dir / "reasoning-surface-index.md"
    process_graph_json = artifacts_dir / "process-graph.json"
    process_graph_evolution_json = artifacts_dir / "process-graph-evolution.json"
    process_graph_html = artifacts_dir / "process-graph.html"
    process_graph_states_dir = artifacts_dir / "process-graph-states"
    dynamics_json = artifacts_dir / "reasoning-dynamics.json"
    dynamics_md = artifacts_dir / "reasoning-dynamics.md"
    dynamics_html = artifacts_dir / "reasoning-dynamics.html"
    conceptual_dynamics_json = artifacts_dir / "conceptual-dynamics.json"
    conceptual_dynamics_md = artifacts_dir / "conceptual-dynamics.md"
    conceptual_dynamics_html = artifacts_dir / "conceptual-dynamics.html"
    conceptual_space_animation_json = artifacts_dir / "conceptual-space-animation.json"
    conceptual_space_animation_md = artifacts_dir / "conceptual-space-animation.md"
    conceptual_space_animation_html = artifacts_dir / "conceptual-space-animation.html"
    search_space_tree_json = artifacts_dir / "search-space-tree.json"
    search_space_tree_md = artifacts_dir / "search-space-tree.md"
    expert_paper_json = artifacts_dir / "expert-hypothesis-paper.json"
    expert_paper_md = artifacts_dir / "expert-hypothesis-paper.md"
    expert_paper_tex = artifacts_dir / "expert-hypothesis-paper.tex"
    log_root = repo / "artifacts" / "reasoning-logs"
    surface_root = repo / "artifacts" / "reasoning-surfaces"
    search_space_state_json = repo / "artifacts" / "search-space-state" / f"{kb_ref}.json"
    phyp_doc_pattern = _resolve_phyp_doc_pattern(args.phyp_doc_pattern, kb_ref)
    concept_generated = False
    expected_agents: set[str] = {"kb-orchestrator"}
    expected_stages_by_intent: dict[str, list[str]] = {
        "cohere": ["connect.analyze", "connect.generate-phyp", "coherence-eval"],
        "connect": ["connect.analyze", "connect.generate-phyp"],
        "coherence-eval": ["coherence-eval"],
        "interpretation-reports": ["interpretation-reports"],
        "process-graph": ["process-graph"],
        "reasoning-dynamics": ["process-graph", "reasoning-dynamics"],
        "conceptual-dynamics": ["conceptual-dynamics"],
        "conceptual-space-animation": ["conceptual-dynamics", "conceptual-space-animation"],
        "search-space-tree": ["search-space-tree"],
        "entrypoints": ["concept-evolution", "entrypoints.rank", "entrypoints.pathways"],
        "hardness": ["concept-evolution", "hardness"],
        "bridge-plan": ["concept-evolution", "bridge-plan"],
        "conjecture": ["conjecture"],
        "strategies": ["strategies"],
        "proof-sketch": ["proof-sketch"],
        "expert-paper": ["expert-paper"],
        "hypothesis-eval": ["hypothesis-eval"],
        "hypothesis-loop": ["hypothesis-loop"],
        "revision-loop": ["revision-loop"],
        "abductive-loop": [
            "connect.analyze",
            "connect.generate-phyp",
            "coherence-eval",
            "hypothesis-eval",
            "hypothesis-loop",
            "revision-loop",
            "interpretation-reports",
            "process-graph",
            "reasoning-dynamics",
        ],
        "pipeline": [
            "connect.analyze",
            "connect.generate-phyp",
            "coherence-eval",
            "concept-evolution",
            "entrypoints.rank",
            "entrypoints.pathways",
            "hardness",
            "bridge-plan",
            "conjecture",
            "strategies",
            "proof-sketch",
            "hypothesis-eval",
            "hypothesis-loop",
            "revision-loop",
            "interpretation-reports",
            "process-graph",
            "reasoning-dynamics",
            "expert-paper",
            "conceptual-space-animation",
            "search-space-tree",
        ],
    }
    expected_stages: set[str] = set(expected_stages_by_intent.get(args.intent, []))
    if args.export_phyp_docs:
        expected_stages.add("phyp-doc-export")
    expected_stages.add("reasoning-log-index")
    expected_stages.add("reasoning-surface-index")
    expected_stages.add("conceptual-dynamics")
    expected_stages.add("conceptual-space-animation")
    expected_stages.add("search-space-tree")

    def mark_expected(*agents: str) -> None:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        for agent in agents:
            agent_s = agent.strip()
            if agent_s:
                expected_agents.add(agent_s)

    # Emit a full argument snapshot early so each run is reproducible from log.
    logger.step(
        "Parsed orchestrator arguments",
        "\n".join(
            [
                f"intent={args.intent}",
                f"run_id={logger.run_id}",
                f"kb={kb}",
                f"kb_ref={kb_ref}",
                f"kb_ref_from_front_matter={kb_ctx.get('kb_ref_from_front_matter', '')}",
                f"kb_ref_from_filename={kb_ctx.get('kb_ref_from_filename', '')}",
                f"artifacts_dir={artifacts_dir}",
                f"phyp={phyp}",
                f"coherence={coherence_json}",
                f"round_evidence_dir={args.round_evidence_dir or ''}",
                f"rounds={args.rounds}",
                f"expected_stages={sorted(expected_stages)}",
                f"export_phyp_docs={args.export_phyp_docs}",
                f"phyp_doc_pattern={phyp_doc_pattern}",
                f"phyp_pdf_engine={args.phyp_pdf_engine}",
            ]
        ),
    )

    analyze_script = repo / "skills" / "discovery" / "kb-proof-connector" / "scripts" / "analyze_kb_graph.py"
    generate_phyp_script = repo / "skills" / "discovery" / "kb-proof-connector" / "scripts" / "generate_phyp.py"
    coherence_script = repo / "skills" / "discovery" / "kb-coherence-evaluator" / "scripts" / "evaluate_coherence.py"
    entrypoint_script = repo / "skills" / "discovery" / "kb-entrypoint-finder" / "scripts" / "recommend_entrypoints.py"
    pathway_script = repo / "skills" / "discovery" / "kb-entrypoint-pathfinder" / "scripts" / "synthesize_pathways.py"
    hardness_script = repo / "skills" / "discovery" / "kb-epistemic-hardness" / "scripts" / "articulate_hardness.py"
    bridge_script = repo / "skills" / "discovery" / "kb-concept-bridge-planner" / "scripts" / "plan_bridges.py"
    conjecture_script = repo / "skills" / "discovery" / "kb-gap-abstraction-conjecturer" / "scripts" / "conjecture_gap_abstractions.py"
    strategy_script = repo / "skills" / "discovery" / "kb-novel-proof-strategist" / "scripts" / "design_strategies.py"
    proof_sketch_script = repo / "skills" / "discovery" / "kb-proof-sketcher" / "scripts" / "generate_proof_sketches.py"
    expert_paper_script = repo / "skills" / "reporting" / "kb-expert-paper-generator" / "scripts" / "generate_expert_paper.py"
    concept_evolution_script = repo / "skills" / "orchestration" / "kb-orchestrator" / "scripts" / "generate_concept_evolution.py"
    hypothesis_eval_script = repo / "skills" / "evaluation" / "kb-hypothesis-evaluator" / "scripts" / "evaluate_hypotheses.py"
    hypothesis_loop_script = repo / "skills" / "evaluation" / "kb-hypothesis-refutation-loop" / "scripts" / "iterate_hypotheses.py"
    revision_loop_script = repo / "skills" / "evaluation" / "kb-revision-loop" / "scripts" / "revise_ontology.py"
    interpretation_report_script = repo / "skills" / "orchestration" / "kb-orchestrator" / "scripts" / "generate_interpretation_reports.py"
    log_index_script = repo / "skills" / "orchestration" / "kb-orchestrator" / "scripts" / "generate_reasoning_log_index.py"
    surface_index_script = repo / "skills" / "orchestration" / "kb-orchestrator" / "scripts" / "generate_reasoning_surface_index.py"
    process_graph_script = repo / "skills" / "orchestration" / "kb-orchestrator" / "scripts" / "generate_process_graph.py"
    dynamics_script = repo / "skills" / "orchestration" / "kb-orchestrator" / "scripts" / "generate_reasoning_dynamics.py"
    conceptual_dynamics_script = repo / "skills" / "orchestration" / "kb-orchestrator" / "scripts" / "generate_conceptual_dynamics.py"
    conceptual_space_animation_script = (
        repo / "skills" / "orchestration" / "kb-orchestrator" / "scripts" / "generate_conceptual_space_animation.py"
    )
    search_space_tree_script = repo / "skills" / "orchestration" / "kb-orchestrator" / "scripts" / "generate_search_space_tree.py"
    phyp_doc_export_script = repo / "skills" / "orchestration" / "kb-orchestrator" / "scripts" / "export_phyp_docs.py"

    def run_connect() -> None:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        mark_expected("kb-proof-connector")
        _run(
            [
                py,
                str(analyze_script),
                "--kb",
                str(kb),
                "--include-status",
                "accepted",
                "--include-status",
                "tentative",
                "--top-k",
                "20",
                "--min-similarity",
                "0.12",
                "--max-connections",
                "40",
                "--loop-rounds",
                "3",
                "--output-json",
                str(analysis),
                "--output-md",
                str(analysis_md),
            ],
            logger,
            "connect.analyze",
        )
        _run(
            [
                py,
                str(generate_phyp_script),
                "--analysis",
                str(analysis),
                "--kb",
                str(kb),
                "--output",
                str(phyp),
                "--top-links",
                "20",
                "--top-interventions",
                "12",
                "--top-conceptual",
                "12",
            ],
            logger,
            "connect.generate-phyp",
        )
        logger.add_output("connection_analysis_json", analysis)
        logger.add_output("connection_analysis_md", analysis_md)
        logger.add_output("proof_hypotheses_yaml", phyp)

    def run_coherence_eval() -> None:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        mark_expected("kb-coherence-evaluator")
        for p in [analysis, phyp]:
            if not p.exists():
                raise FileNotFoundError(f"Required coherence input missing: {p}")
        _run(
            [
                py,
                str(coherence_script),
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
            logger,
            "coherence-eval",
        )
        logger.add_output("coherence_report_json", coherence_json)

    def run_entrypoints() -> None:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        mark_expected("kb-entrypoint-finder", "kb-entrypoint-pathfinder")
        run_concept_evolution()
        if not analysis.exists():
            raise FileNotFoundError(f"Analysis file not found: {analysis}")
        if not phyp.exists():
            raise FileNotFoundError(f"Hypotheses file not found: {phyp}")
        cmd = [
            py,
            str(entrypoint_script),
            "--kb",
            str(kb),
            "--include-status",
            "accepted",
            "--include-status",
            "tentative",
            "--concept",
            str(concept),
            "--analysis",
            str(analysis),
            "--phyp",
            str(phyp),
            "--top-k",
            "20",
            "--output-json",
            str(entrypoints),
            "--output-md",
            str(entrypoints_md),
        ]
        if coherence_json.exists():
            cmd.extend(["--coherence-report", str(coherence_json)])
        _run(cmd, logger, "entrypoints.rank")
        _run(
            [
                py,
                str(pathway_script),
                "--recommendations",
                str(entrypoints),
                "--phyp",
                str(phyp),
                "--analysis",
                str(analysis),
                "--top-entrypoints",
                "8",
                "--output-json",
                str(pathways),
                "--output-md",
                str(pathways_md),
            ],
            logger,
            "entrypoints.pathways",
        )
        logger.add_output("entrypoints_json", entrypoints)
        logger.add_output("entrypoint_pathways_json", pathways)

    def run_concept_evolution() -> None:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Generates the phase-oriented concept scaffold required by entrypoint and hardness stages when a KB is run from scratch.
        """

        nonlocal concept_generated
        if concept_generated:
            return
        mark_expected("kb-concept-evolution")
        cmd = [
            py,
            str(concept_evolution_script),
            "--kb",
            str(kb),
            "--output-md",
            str(concept),
        ]
        if analysis.exists():
            cmd.extend(["--analysis", str(analysis)])
        if phyp.exists():
            cmd.extend(["--phyp", str(phyp)])
        _run(cmd, logger, "concept-evolution")
        logger.add_output("concept_evolution_md", concept)
        concept_generated = True

    def run_hardness() -> None:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        mark_expected("kb-epistemic-hardness")
        run_concept_evolution()
        for p in [concept, analysis, entrypoints, pathways, phyp]:
            if not p.exists():
                raise FileNotFoundError(f"Required hardness input missing: {p}")
        _run(
            [
                py,
                str(hardness_script),
                "--problem",
                kb_ref,
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
            logger,
            "hardness",
        )
        logger.add_output("epistemic_hardness_json", hardness_json)

    def run_bridge_plan() -> None:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        mark_expected("kb-concept-bridge-planner")
        run_concept_evolution()
        for p in [analysis, entrypoints, pathways, phyp, concept]:
            if not p.exists():
                raise FileNotFoundError(f"Required bridge-plan input missing: {p}")
        cmd = [
            py,
            str(bridge_script),
            "--analysis",
            str(analysis),
            "--entrypoints",
            str(entrypoints),
            "--pathways",
            str(pathways),
            "--phyp",
            str(phyp),
            "--kb",
            str(kb),
            "--concept",
            str(concept),
            "--search-space-state",
            str(search_space_state_json),
            "--top-k",
            "20",
            "--output-json",
            str(bridges),
            "--output-md",
            str(bridges_md),
        ]
        if coherence_json.exists():
            cmd.extend(["--coherence-report", str(coherence_json)])
        _run(cmd, logger, "bridge-plan")
        logger.add_output("bridge_plan_json", bridges)

    def run_strategies() -> None:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        mark_expected("kb-novel-proof-strategist")
        for p in [entrypoints, pathways, bridges, phyp]:
            if not p.exists():
                raise FileNotFoundError(f"Required strategies input missing: {p}")
        cmd = [
            py,
            str(strategy_script),
            "--entrypoints",
            str(entrypoints),
            "--pathways",
            str(pathways),
            "--bridges",
            str(bridges),
            "--phyp",
            str(phyp),
            "--top-k",
            "6",
            "--output-json",
            str(strategies_json),
            "--output-md",
            str(strategies_md),
            "--output-prompt",
            str(novelty_prompt),
        ]
        if coherence_json.exists():
            cmd.extend(["--coherence-report", str(coherence_json)])
        if conjectures_json.exists():
            cmd.extend(["--conjectures", str(conjectures_json)])
        _run(cmd, logger, "strategies")
        logger.add_output("proof_strategies_json", strategies_json)

    def run_proof_sketch() -> None:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        mark_expected("kb-proof-sketcher")
        for p in [conjectures_json, strategies_json, bridges, phyp]:
            if not p.exists():
                raise FileNotFoundError(f"Required proof-sketch input missing: {p}")
        cmd = [
            py,
            str(proof_sketch_script),
            "--conjectures",
            str(conjectures_json),
            "--strategies",
            str(strategies_json),
            "--bridges",
            str(bridges),
            "--phyp",
            str(phyp),
            "--kb",
            str(kb),
            "--top-k",
            "6",
            "--output-json",
            str(proof_sketches_json),
            "--output-md",
            str(proof_sketches_md),
            "--output-paper-md",
            str(paper_style_argument_md),
        ]
        if analysis.exists():
            cmd.extend(["--analysis", str(analysis)])
        if coherence_json.exists():
            cmd.extend(["--coherence-report", str(coherence_json)])
        if hardness_json.exists():
            cmd.extend(["--hardness", str(hardness_json)])
        _run(cmd, logger, "proof-sketch")
        logger.add_output("proof_sketches_json", proof_sketches_json)
        logger.add_output("proof_sketches_md", proof_sketches_md)
        logger.add_output("paper_style_argument_md", paper_style_argument_md)

    def run_conjecture() -> None:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        mark_expected("kb-gap-abstraction-conjecturer")
        for p in [analysis, entrypoints, pathways, bridges, phyp]:
            if not p.exists():
                raise FileNotFoundError(f"Required conjecture input missing: {p}")
        cmd = [
            py,
            str(conjecture_script),
            "--analysis",
            str(analysis),
            "--entrypoints",
            str(entrypoints),
            "--pathways",
            str(pathways),
            "--bridges",
            str(bridges),
            "--phyp",
            str(phyp),
            "--top-bridges",
            "12",
            "--max-conjectures-per-bridge",
            "3",
            "--output-json",
            str(conjectures_json),
            "--output-md",
            str(conjectures_md),
        ]
        if hardness_json.exists():
            cmd.extend(["--hardness", str(hardness_json)])
        _run(cmd, logger, "conjecture")
        logger.add_output("concept_gap_abstractions_json", conjectures_json)
        logger.add_output("concept_gap_abstractions_md", conjectures_md)

    def run_hypothesis_eval() -> None:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        mark_expected("kb-hypothesis-evaluator")
        for p in [analysis, phyp]:
            if not p.exists():
                raise FileNotFoundError(f"Required hypothesis-eval input missing: {p}")
        cmd = [
            py,
            str(hypothesis_eval_script),
            "--kb",
            str(kb),
            "--phyp",
            str(phyp),
            "--analysis",
            str(analysis),
            "--output-json",
            str(hypothesis_eval_json),
            "--output-md",
            str(hypothesis_eval_md),
            "--output-phyp-md",
            str(phyp_eval_md),
        ]
        if coherence_json.exists():
            cmd.extend(["--coherence-report", str(coherence_json)])
        _run(cmd, logger, "hypothesis-eval")
        logger.add_output("hypothesis_evaluation_json", hypothesis_eval_json)
        logger.add_output("hypothesis_evaluation_phyp_md", phyp_eval_md)

    def run_expert_paper() -> None:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Produces a paper-style synthesis plus expert hypothesis recommendations from final analysis artifacts.
        """

        mark_expected("kb-expert-paper-generator")
        phyp_for_paper = reviewed_phyp if reviewed_phyp.exists() else phyp
        if not phyp_for_paper.exists():
            raise FileNotFoundError(f"Required expert-paper input missing: {phyp_for_paper}")
        cmd = [
            py,
            str(expert_paper_script),
            "--kb",
            str(kb),
            "--kb-ref",
            str(kb_ref),
            "--artifacts-dir",
            str(artifacts_dir),
            "--phyp",
            str(phyp_for_paper),
            "--output-json",
            str(expert_paper_json),
            "--output-md",
            str(expert_paper_md),
            "--output-tex",
            str(expert_paper_tex),
        ]
        _run(cmd, logger, "expert-paper")
        logger.add_output("expert_hypothesis_paper_json", expert_paper_json)
        logger.add_output("expert_hypothesis_paper_md", expert_paper_md)
        logger.add_output("expert_hypothesis_paper_tex", expert_paper_tex)

    def run_hypothesis_loop() -> None:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        mark_expected("kb-hypothesis-refutation-loop")
        for p in [analysis, phyp]:
            if not p.exists():
                raise FileNotFoundError(f"Required hypothesis-loop input missing: {p}")
        cmd = [
            py,
            str(hypothesis_loop_script),
            "--kb",
            str(kb),
            "--phyp",
            str(phyp),
            "--analysis",
            str(analysis),
            "--rounds",
            str(max(1, args.rounds)),
            "--output-json",
            str(hypothesis_loop_json),
            "--output-md",
            str(hypothesis_loop_md),
            "--output-phyp-md",
            str(phyp_review_md),
            "--output-phyp",
            str(reviewed_phyp),
        ]
        if args.round_evidence_dir:
            cmd.extend(["--round-evidence-dir", args.round_evidence_dir])
        if coherence_json.exists():
            cmd.extend(["--coherence-report", str(coherence_json)])
        _run(cmd, logger, "hypothesis-loop")
        logger.add_output("hypothesis_refutation_loop_json", hypothesis_loop_json)
        logger.add_output("hypothesis_refutation_loop_phyp_md", phyp_review_md)
        logger.add_output("reviewed_hypotheses_yaml", reviewed_phyp)

    def run_revision_loop() -> None:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        mark_expected("kb-revision-loop")
        if not hypothesis_loop_json.exists():
            raise FileNotFoundError(f"Required revision-loop input missing: {hypothesis_loop_json}")
        phyp_for_revision = reviewed_phyp if reviewed_phyp.exists() else phyp
        cmd = [
            py,
            str(revision_loop_script),
            "--kb",
            str(kb),
            "--phyp",
            str(phyp_for_revision),
            "--hypothesis-loop",
            str(hypothesis_loop_json),
            "--output-json",
            str(revision_json),
            "--output-md",
            str(revision_md),
            "--output-patched-kb",
            str(revision_patched_kb),
            "--output-patched-phyp",
            str(revision_patched_phyp),
        ]
        if coherence_json.exists():
            cmd.extend(["--coherence-report", str(coherence_json)])
        if hardness_json.exists():
            cmd.extend(["--hardness", str(hardness_json)])
        _run(cmd, logger, "revision-loop")
        logger.add_output("revision_loop_json", revision_json)
        logger.add_output("revision_patched_kb", revision_patched_kb)
        logger.add_output("revision_patched_phyp", revision_patched_phyp)

    def run_interpretation_reports() -> None:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        mark_expected("kb-interpretation-reporter")
        if not artifacts_dir.exists():
            raise FileNotFoundError(f"Artifacts directory not found: {artifacts_dir}")
        _run(
            [
                py,
                str(interpretation_report_script),
                "--artifacts-dir",
                str(artifacts_dir),
                "--kb",
                str(kb),
                "--output-process-md",
                str(process_report_md),
                "--output-discovery-md",
                str(discovery_report_md),
            ],
            logger,
            "interpretation-reports",
        )
        logger.add_output("reasoning_process_report_md", process_report_md)
        logger.add_output("discovery_interpretation_report_md", discovery_report_md)

    def run_process_graph() -> None:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        mark_expected("kb-process-graph-visualizer")
        if not artifacts_dir.exists():
            raise FileNotFoundError(f"Artifacts directory not found: {artifacts_dir}")
        _run(
            [
                py,
                str(process_graph_script),
                "--artifacts-dir",
                str(artifacts_dir),
                "--reasoning-log-root",
                str(log_root),
                "--kb",
                str(kb),
                "--kb-ref",
                str(kb_ref),
                "--run-id",
                str(logger.run_id),
                "--output-json",
                str(process_graph_json),
                "--output-evolution-json",
                str(process_graph_evolution_json),
                "--output-html",
                str(process_graph_html),
                "--states-dir",
                str(process_graph_states_dir),
            ],
            logger,
            "process-graph",
        )
        logger.add_output("process_graph_json", process_graph_json)
        logger.add_output("process_graph_evolution_json", process_graph_evolution_json)
        logger.add_output("process_graph_html", process_graph_html)

    def run_reasoning_dynamics() -> None:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        mark_expected("kb-reasoning-dynamics")
        if not artifacts_dir.exists():
            raise FileNotFoundError(f"Artifacts directory not found: {artifacts_dir}")
        if not process_graph_evolution_json.exists():
            run_process_graph()
        _run(
            [
                py,
                str(dynamics_script),
                "--artifacts-dir",
                str(artifacts_dir),
                "--process-graph-evolution",
                str(process_graph_evolution_json),
                "--output-json",
                str(dynamics_json),
                "--output-md",
                str(dynamics_md),
                "--output-html",
                str(dynamics_html),
            ],
            logger,
            "reasoning-dynamics",
        )
        logger.add_output("reasoning_dynamics_json", dynamics_json)
        logger.add_output("reasoning_dynamics_md", dynamics_md)
        logger.add_output("reasoning_dynamics_html", dynamics_html)

    def run_conceptual_dynamics() -> None:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Produces a conceptual dashboard over evolving concepts, hypotheses, and reasoning styles.
        """

        mark_expected("kb-conceptual-dynamics")
        if not artifacts_dir.exists():
            raise FileNotFoundError(f"Artifacts directory not found: {artifacts_dir}")
        cmd = _build_conceptual_dynamics_cmd(
            py=py,
            conceptual_dynamics_script=conceptual_dynamics_script,
            artifacts_dir=artifacts_dir,
            kb=kb,
            kb_ref=kb_ref,
            surface_root=surface_root,
            run_id=logger.run_id,
            output_json=conceptual_dynamics_json,
            output_md=conceptual_dynamics_md,
            output_html=conceptual_dynamics_html,
        )
        _run(cmd, logger, "conceptual-dynamics")
        logger.add_output("conceptual_dynamics_json", conceptual_dynamics_json)
        logger.add_output("conceptual_dynamics_md", conceptual_dynamics_md)
        logger.add_output("conceptual_dynamics_html", conceptual_dynamics_html)

    def run_conceptual_space_animation() -> None:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Produces a scene-based, manim-style animation surface over the conceptual exploration.
        """

        mark_expected("kb-conceptual-space-animation")
        if not artifacts_dir.exists():
            raise FileNotFoundError(f"Artifacts directory not found: {artifacts_dir}")
        if not conceptual_dynamics_json.exists():
            run_conceptual_dynamics()
        cmd = _build_conceptual_space_animation_cmd(
            py=py,
            conceptual_space_animation_script=conceptual_space_animation_script,
            artifacts_dir=artifacts_dir,
            conceptual_dynamics_json=conceptual_dynamics_json,
            output_json=conceptual_space_animation_json,
            output_md=conceptual_space_animation_md,
            output_html=conceptual_space_animation_html,
        )
        _run(cmd, logger, "conceptual-space-animation")
        logger.add_output("conceptual_space_animation_json", conceptual_space_animation_json)
        logger.add_output("conceptual_space_animation_md", conceptual_space_animation_md)
        logger.add_output("conceptual_space_animation_html", conceptual_space_animation_html)

    def run_search_space_tree() -> None:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Persists a KB-scoped tree of explored search dimensions and revisited route history.
        """

        mark_expected("kb-search-space-tree")
        if not artifacts_dir.exists():
            raise FileNotFoundError(f"Artifacts directory not found: {artifacts_dir}")
        cmd = _build_search_space_tree_cmd(
            py=py,
            search_space_tree_script=search_space_tree_script,
            artifacts_dir=artifacts_dir,
            kb_ref=kb_ref,
            run_id=logger.run_id,
            state_json=search_space_state_json,
            output_json=search_space_tree_json,
            output_md=search_space_tree_md,
        )
        _run(cmd, logger, "search-space-tree")
        logger.add_output("search_space_tree_json", search_space_tree_json)
        logger.add_output("search_space_tree_md", search_space_tree_md)
        logger.add_output("search_space_state_json", search_space_state_json)

    def run_phyp_docs_export() -> None:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        mark_expected("phyp-doc-exporter")
        if not args.export_phyp_docs:
            return
        phyp_dir = repo / "phyp"
        if not phyp_dir.exists():
            raise FileNotFoundError(f"phyp directory not found: {phyp_dir}")
        _run(
            [
                py,
                str(phyp_doc_export_script),
                "--phyp-dir",
                str(phyp_dir),
                "--pattern",
                str(phyp_doc_pattern),
                "--pdf-engine",
                str(args.phyp_pdf_engine),
            ],
            logger,
            "phyp-doc-export",
        )

    def run_log_index() -> None:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        mark_expected("kb-log-indexer")
        cmd = _build_log_index_cmd(
            py=py,
            log_index_script=log_index_script,
            artifacts_dir=artifacts_dir,
            kb=kb,
            kb_ref=kb_ref,
            log_root=log_root,
            run_id=logger.run_id,
            log_index_json=log_index_json,
            log_index_md=log_index_md,
            expected_agents=expected_agents,
            expected_stages=expected_stages,
        )
        _run(cmd, logger, "reasoning-log-index")
        logger.add_output("reasoning_log_index_json", log_index_json)
        logger.add_output("reasoning_log_index_md", log_index_md)

    def run_surface_index() -> None:
        """
        Relevance: Operates within the orchestration and observability layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Produces a human-facing conceptual timeline over surfaced reasoning logs for the active run.
        """

        surface_expected_agents = {agent for agent in expected_agents if agent != "kb-surface-indexer"}
        mark_expected("kb-surface-indexer")
        cmd = _build_surface_index_cmd(
            py=py,
            surface_index_script=surface_index_script,
            artifacts_dir=artifacts_dir,
            kb=kb,
            kb_ref=kb_ref,
            surface_root=surface_root,
            run_id=logger.run_id,
            surface_index_json=surface_index_json,
            surface_index_md=surface_index_md,
            expected_agents=surface_expected_agents,
        )
        _run(cmd, logger, "reasoning-surface-index")
        logger.add_output("reasoning_surface_index_json", surface_index_json)
        logger.add_output("reasoning_surface_index_md", surface_index_md)

    try:
        if args.intent == "cohere":
            run_connect()
            run_coherence_eval()
        elif args.intent == "connect":
            run_connect()
        elif args.intent == "coherence-eval":
            run_coherence_eval()
        elif args.intent == "interpretation-reports":
            run_interpretation_reports()
        elif args.intent == "process-graph":
            run_process_graph()
        elif args.intent == "reasoning-dynamics":
            run_process_graph()
            run_reasoning_dynamics()
        elif args.intent == "conceptual-dynamics":
            pass
        elif args.intent == "conceptual-space-animation":
            pass
        elif args.intent == "search-space-tree":
            pass
        elif args.intent == "entrypoints":
            run_entrypoints()
        elif args.intent == "hardness":
            run_hardness()
        elif args.intent == "bridge-plan":
            run_bridge_plan()
        elif args.intent == "conjecture":
            run_conjecture()
        elif args.intent == "strategies":
            run_strategies()
        elif args.intent == "proof-sketch":
            run_proof_sketch()
        elif args.intent == "expert-paper":
            run_expert_paper()
        elif args.intent == "hypothesis-eval":
            run_hypothesis_eval()
        elif args.intent == "hypothesis-loop":
            run_hypothesis_loop()
        elif args.intent == "revision-loop":
            run_revision_loop()
        elif args.intent == "abductive-loop":
            run_connect()
            run_coherence_eval()
            print("[INFO] kb-abduce and kb-deduce are prompt-driven skills; run them between connect and hypothesis stages.")
            run_hypothesis_eval()
            run_hypothesis_loop()
            run_revision_loop()
            run_interpretation_reports()
            run_process_graph()
            run_reasoning_dynamics()
        elif args.intent == "pipeline":
            run_connect()
            run_coherence_eval()
            run_entrypoints()
            run_hardness()
            run_bridge_plan()
            run_conjecture()
            run_strategies()
            run_proof_sketch()
            run_hypothesis_eval()
            run_hypothesis_loop()
            run_revision_loop()
            run_interpretation_reports()
            run_process_graph()
            run_reasoning_dynamics()
            run_expert_paper()
        if args.export_phyp_docs:
            run_phyp_docs_export()
        run_surface_index()
        run_conceptual_dynamics()
        run_conceptual_space_animation()
        run_search_space_tree()
        run_log_index()
    except subprocess.CalledProcessError as exc:
        log_path = logger.finalize("error", summary=f"Stage failed with exit code {exc.returncode}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(exc.returncode)
    except Exception as exc:
        log_path = logger.finalize("error", summary=str(exc))
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] {exc}")

    log_path = logger.finalize("success", summary=f"Intent `{args.intent}` completed.")
    print(f"[LOG] {log_path}")
    # Refresh once more after finalization so kb-orchestrator is indexed with final status.
    refresh_surface_cmd = _build_surface_index_cmd(
        py=py,
        surface_index_script=surface_index_script,
        artifacts_dir=artifacts_dir,
        kb=kb,
        kb_ref=kb_ref,
        surface_root=surface_root,
        run_id=logger.run_id,
        surface_index_json=surface_index_json,
        surface_index_md=surface_index_md,
        expected_agents={agent for agent in expected_agents if agent != "kb-surface-indexer"},
    )
    _refresh_report_post_finalize(refresh_surface_cmd, run_id=logger.run_id)
    refresh_conceptual_cmd = _build_conceptual_dynamics_cmd(
        py=py,
        conceptual_dynamics_script=conceptual_dynamics_script,
        artifacts_dir=artifacts_dir,
        kb=kb,
        kb_ref=kb_ref,
        surface_root=surface_root,
        run_id=logger.run_id,
        output_json=conceptual_dynamics_json,
        output_md=conceptual_dynamics_md,
        output_html=conceptual_dynamics_html,
    )
    _refresh_report_post_finalize(refresh_conceptual_cmd, run_id=logger.run_id)
    refresh_animation_cmd = _build_conceptual_space_animation_cmd(
        py=py,
        conceptual_space_animation_script=conceptual_space_animation_script,
        artifacts_dir=artifacts_dir,
        conceptual_dynamics_json=conceptual_dynamics_json,
        output_json=conceptual_space_animation_json,
        output_md=conceptual_space_animation_md,
        output_html=conceptual_space_animation_html,
    )
    _refresh_report_post_finalize(refresh_animation_cmd, run_id=logger.run_id)
    refresh_search_space_cmd = _build_search_space_tree_cmd(
        py=py,
        search_space_tree_script=search_space_tree_script,
        artifacts_dir=artifacts_dir,
        kb_ref=kb_ref,
        run_id=logger.run_id,
        state_json=search_space_state_json,
        output_json=search_space_tree_json,
        output_md=search_space_tree_md,
    )
    _refresh_report_post_finalize(refresh_search_space_cmd, run_id=logger.run_id)
    refresh_cmd = _build_log_index_cmd(
        py=py,
        log_index_script=log_index_script,
        artifacts_dir=artifacts_dir,
        kb=kb,
        kb_ref=kb_ref,
        log_root=log_root,
        run_id=logger.run_id,
        log_index_json=log_index_json,
        log_index_md=log_index_md,
        expected_agents=expected_agents,
        expected_stages=expected_stages,
    )
    _refresh_report_post_finalize(refresh_cmd, run_id=logger.run_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
