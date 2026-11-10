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

"""Run the Abducer Looper control-plane proof gate without changing evidence.

The default command is deliberately read-only.  Historical versions mixed
builders, navigators, and validators in one long sequence, so merely checking a
worktree could create a new run and then abort before validation finished.
Tracked-artifact regeneration now requires the explicit ``--refresh`` mode;
target navigation remains a separate command because an authoritative run must
receive an exact canonical cycle, state root, receipt root, and workspace.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import stat
import subprocess
import sys
from pathlib import Path

from agentic_common import ROOT


LEGACY_PIPELINE = [
    "agentic/scripts/run_target_navigation.py",
    "agentic/scripts/validate_target_packets.py",
    "agentic/scripts/validate_dependency_graph.py",
    "agentic/scripts/validate_active_target_workspace.py",
    "agentic/scripts/validate_target_relevance.py",
    "agentic/scripts/validate_hypothesis_exploration.py",
    "agentic/scripts/apply_gate_policy.py",
    "agentic/scripts/validate_skill_depth.py",
    "agentic/scripts/validate_subworkflow_skill_functionality.py",
    "agentic/scripts/validate_api_key_config.py",
    "agentic/scripts/build_reasoning_event_log.py",
    "agentic/scripts/validate_reasoning_event_logs.py",
    "agentic/scripts/build_abstraction_chain_packets.py",
    "agentic/scripts/build_gedanken_experiment_packets.py",
    "agentic/scripts/validate_gedanken_experiment_packets.py",
    "skills/reasoning/pvsnp-gedanken-complexity-lab/scripts/build_pvsnp_gedanken_packets.py",
    "agentic/scripts/validate_pvsnp_gedanken_conclusions.py",
    "agentic/scripts/build_symbolic_matrix_probe.py",
    "agentic/scripts/validate_symbolic_matrix_probe.py",
    "agentic/scripts/build_finite_algebra_interfaces.py",
    "agentic/scripts/validate_finite_algebra_interfaces.py",
    "agentic/scripts/build_analytic_estimate_obligations.py",
    "agentic/scripts/validate_analytic_estimate_obligations.py",
    "agentic/scripts/build_endpoint_incidence_certificate.py",
    "agentic/scripts/validate_endpoint_incidence_certificate.py",
    "skills/results_ellaboration/routea-symbolic-cas-auditor/scripts/audit_routea_symbolic_cas.py",
    "agentic/scripts/validate_routea_symbolic_cas_audit.py",
    "skills/reasoning/pvsnp-pressure-bridge-forger/scripts/build_pressure_bridges.py",
    "agentic/scripts/validate_pvsnp_pressure_bridges.py",
    "agentic/scripts/build_pvsnp_negative_tactic_packet.py",
    "agentic/scripts/validate_pvsnp_negative_tactics.py",
    "agentic/scripts/build_pvsnp_inference_quality_report.py",
    "agentic/scripts/validate_pvsnp_inference_quality.py",
    "agentic/scripts/build_result_subgoal_atlas.py",
    "agentic/scripts/validate_result_subgoal_atlas.py",
    "agentic/scripts/build_problem_space_map.py",
    "agentic/scripts/validate_problem_space_map.py",
    "agentic/scripts/build_derivation_vault.py",
    "agentic/scripts/validate_derivation_vault.py",
    "agentic/scripts/update_subgoal_state_from_cycle.py",
    "agentic/scripts/build_timeline_paper_interpretation.py",
    "agentic/scripts/validate_timeline_paper_interpretation.py",
    "agentic/scripts/build_timeline_paper_blueprint.py",
    "agentic/scripts/validate_timeline_paper_blueprint.py",
    "agentic/scripts/build_timeline_formal_derivation.py",
    "agentic/scripts/validate_timeline_formal_derivation.py",
    "agentic/scripts/build_timeline_paper_diagrams.py",
    "agentic/scripts/validate_timeline_paper_diagrams.py",
    "agentic/scripts/build_timeline_paper_sections.py",
    "agentic/scripts/validate_timeline_paper_sections.py",
    "agentic/scripts/build_timeline_latex_sections.py",
    "agentic/scripts/validate_timeline_latex_sections.py",
    "agentic/scripts/validate_bounded_numeric_probe.py",
    "agentic/scripts/build_qualitative_mechanistic_graph.py",
    "agentic/scripts/validate_qualitative_relation_packets.py",
    "agentic/scripts/validate_qualitative_mechanistic_graph.py",
    "agentic/scripts/build_subworkflow_integration_tests.py",
    "agentic/scripts/validate_parsimonious_probe_integration.py",
    "agentic/scripts/validate_equational_symbolic_integration.py",
    "agentic/scripts/build_reasoning_monitor_packet.py",
    "agentic/scripts/generate_reasoning_monitor_html.py",
    "agentic/scripts/run_long_horizon_probe.py",
    "agentic/scripts/validate_long_horizon_probe.py",
    "agentic/scripts/build_yang_mills_bridge_lemma_packets.py",
    "agentic/scripts/validate_yang_mills_bridge_lemma_packets.py",
    "agentic/scripts/build_discovery_stretch.py",
    "agentic/scripts/validate_discovery_stretch.py",
    "agentic/scripts/build_blocker_signature_report.py",
    "agentic/scripts/validate_artifact_or_stop_control.py",
    "agentic/scripts/build_discovery_marathon_report.py",
    "agentic/scripts/validate_proof_depth_control.py",
    "agentic/scripts/build_proof_learning_ledger.py",
    "agentic/scripts/validate_proof_learning_ledger.py",
    "agentic/scripts/build_proof_lockin_report.py",
    "agentic/scripts/validate_proof_lockin_report.py",
    "agentic/scripts/build_gedanken_experiment_packets.py",
    "agentic/scripts/validate_gedanken_experiment_packets.py",
    "skills/reasoning/pvsnp-gedanken-complexity-lab/scripts/build_pvsnp_gedanken_packets.py",
    "agentic/scripts/validate_pvsnp_gedanken_conclusions.py",
    "agentic/scripts/build_symbolic_matrix_probe.py",
    "agentic/scripts/validate_symbolic_matrix_probe.py",
    "agentic/scripts/build_finite_algebra_interfaces.py",
    "agentic/scripts/validate_finite_algebra_interfaces.py",
    "agentic/scripts/build_analytic_estimate_obligations.py",
    "agentic/scripts/validate_analytic_estimate_obligations.py",
    "agentic/scripts/build_endpoint_incidence_certificate.py",
    "agentic/scripts/validate_endpoint_incidence_certificate.py",
    "skills/results_ellaboration/routea-symbolic-cas-auditor/scripts/audit_routea_symbolic_cas.py",
    "agentic/scripts/validate_routea_symbolic_cas_audit.py",
    "skills/reasoning/pvsnp-pressure-bridge-forger/scripts/build_pressure_bridges.py",
    "agentic/scripts/validate_pvsnp_pressure_bridges.py",
    "agentic/scripts/build_pvsnp_negative_tactic_packet.py",
    "agentic/scripts/validate_pvsnp_negative_tactics.py",
    "agentic/scripts/build_pvsnp_inference_quality_report.py",
    "agentic/scripts/validate_pvsnp_inference_quality.py",
    "agentic/scripts/build_result_subgoal_atlas.py",
    "agentic/scripts/validate_result_subgoal_atlas.py",
    "agentic/scripts/build_problem_space_map.py",
    "agentic/scripts/validate_problem_space_map.py",
    "agentic/scripts/build_derivation_vault.py",
    "agentic/scripts/validate_derivation_vault.py",
    "agentic/scripts/update_subgoal_state_from_cycle.py",
    "agentic/scripts/build_timeline_paper_interpretation.py",
    "agentic/scripts/validate_timeline_paper_interpretation.py",
    "agentic/scripts/build_timeline_paper_blueprint.py",
    "agentic/scripts/validate_timeline_paper_blueprint.py",
    "agentic/scripts/build_timeline_formal_derivation.py",
    "agentic/scripts/validate_timeline_formal_derivation.py",
    "agentic/scripts/build_timeline_paper_diagrams.py",
    "agentic/scripts/validate_timeline_paper_diagrams.py",
    "agentic/scripts/build_timeline_paper_sections.py",
    "agentic/scripts/validate_timeline_paper_sections.py",
    "agentic/scripts/build_timeline_latex_sections.py",
    "agentic/scripts/validate_timeline_latex_sections.py",
    "agentic/scripts/validate_bounded_numeric_probe.py",
    "agentic/scripts/build_qualitative_mechanistic_graph.py",
    "agentic/scripts/validate_qualitative_relation_packets.py",
    "agentic/scripts/validate_qualitative_mechanistic_graph.py",
    "agentic/scripts/build_subworkflow_integration_tests.py",
    "agentic/scripts/validate_parsimonious_probe_integration.py",
    "agentic/scripts/validate_equational_symbolic_integration.py",
    "agentic/scripts/build_scientific_contribution_monitor.py",
    "agentic/scripts/validate_scientific_contribution_monitor.py",
    "agentic/scripts/validate_publishable_stepping_stone_fixtures.py",
    "agentic/scripts/validate_paper_relevance_marker_fixtures.py",
    "agentic/scripts/build_target_literature_evolution.py",
    "agentic/scripts/validate_target_literature_evolution.py",
    "agentic/scripts/build_avenue_literature_gap_warrant.py",
    "agentic/scripts/validate_avenue_literature_gap_warrant.py",
    "agentic/scripts/build_macro_strategy_report.py",
    "agentic/scripts/validate_macro_strategy_report.py",
    "agentic/scripts/build_strategy_progression_judge.py",
    "agentic/scripts/validate_strategy_progression_judge.py",
    "agentic/scripts/build_blocker_signature_report.py",
    "agentic/scripts/validate_artifact_or_stop_control.py",
    "agentic/scripts/generate_discovery_marathon_html.py",
    "agentic/scripts/validate_proof_depth_control.py",
    "agentic/scripts/build_proof_learning_ledger.py",
    "agentic/scripts/validate_proof_learning_ledger.py",
    "agentic/scripts/build_proof_lockin_report.py",
    "agentic/scripts/validate_proof_lockin_report.py",
    "agentic/scripts/validate_discovery_marathon_state.py",
    "agentic/scripts/validate_discovery_marathon_cycle.py",
    "agentic/scripts/validate_parallel_api_marathon.py",
    "agentic/scripts/validate_discovery_marathon_skill_dispatch.py",
    "agentic/scripts/validate_discovery_marathon_report.py",
    "agentic/scripts/validate_discovery_marathon_theme_scoping.py",
    "agentic/scripts/validate_marathon_deep_review.py",
    "agentic/scripts/build_empirical_evidence_requests.py",
    "agentic/scripts/validate_empirical_evidence_requests.py",
    "agentic/scripts/validate_proof_by_contradiction_routes.py",
    "agentic/scripts/build_reasoning_event_log.py",
    "agentic/scripts/validate_reasoning_event_logs.py",
    "agentic/scripts/build_abstraction_chain_packets.py",
    "agentic/scripts/build_reasoning_monitor_packet.py",
    "agentic/scripts/generate_reasoning_monitor_html.py",
    "agentic/scripts/validate_reasoning_monitor.py",
    "agentic/scripts/build_big_deal_goal_archive.py",
    "agentic/scripts/validate_big_deal_goal_archive.py",
    "agentic/scripts/build_hamiltonian_gap_derivation.py",
    "agentic/scripts/generate_hamiltonian_gap_derivation_html.py",
    "agentic/scripts/validate_hamiltonian_gap_derivation.py",
    "agentic/scripts/build_physics_math_interpretation.py",
    "agentic/scripts/validate_physics_math_interpretation.py",
    "agentic/scripts/run_timeline_paper_workflow.py",
    "agentic/scripts/validate_timeline_paper_forward_eval.py",
    "agentic/scripts/validate_skill_taxonomy_projections.py",
    "agentic/scripts/validate_named_workflow_task_projection.py",
    "agentic/scripts/validate_named_workflow_trace_contracts.py",
    "agentic/scripts/validate_public_reasoning_trace.py",
    "agentic/scripts/validate_public_reasoning_trace_pdf.py",
    "agentic/scripts/validate_skill_integration.py",
    "agentic/scripts/validate_task_skill_registry.py",
    "agentic/scripts/validate_workflow_contracts.py",
    "agentic/scripts/validate_hypothesis_exploration.py",
    "agentic/scripts/apply_gate_policy.py",
    "agentic/scripts/validate_todos.py",
    "agentic/scripts/validate_todo_completion.py",
    "agentic/scripts/run_hook_contract_tests.py",
    "agentic/scripts/validate_skill_application_logs.py",
    "agentic/scripts/validate_promotion_gates.py",
]


def _ordered_unique(values: list[str]) -> tuple[str, ...]:
    """Preserve dependency order while removing historical duplicate blocks."""

    return tuple(dict.fromkeys(values))


PIPELINE = _ordered_unique(LEGACY_PIPELINE)

# This is deliberately a closed allowlist.  A ``validate_`` prefix says
# nothing about filesystem behaviour: several historical validators also
# materialize reports or rerun acceptance commands.  New validators therefore
# do not enter the default proof gate until their write behaviour is reviewed.
READ_ONLY_VALIDATORS = (
    "agentic/scripts/validate_target_packets.py",
    "agentic/scripts/validate_dependency_graph.py",
    "agentic/scripts/validate_target_relevance.py",
    "agentic/scripts/validate_hypothesis_exploration.py",
    "agentic/scripts/validate_subworkflow_skill_functionality.py",
    "agentic/scripts/validate_api_key_config.py",
    "agentic/scripts/validate_reasoning_event_logs.py",
    "agentic/scripts/validate_gedanken_experiment_packets.py",
    "agentic/scripts/validate_pvsnp_gedanken_conclusions.py",
    "agentic/scripts/validate_symbolic_matrix_probe.py",
    "agentic/scripts/validate_finite_algebra_interfaces.py",
    "agentic/scripts/validate_analytic_estimate_obligations.py",
    "agentic/scripts/validate_endpoint_incidence_certificate.py",
    "agentic/scripts/validate_routea_symbolic_cas_audit.py",
    "agentic/scripts/validate_pvsnp_pressure_bridges.py",
    "agentic/scripts/validate_pvsnp_negative_tactics.py",
    "agentic/scripts/validate_pvsnp_inference_quality.py",
    "agentic/scripts/validate_result_subgoal_atlas.py",
    "agentic/scripts/validate_problem_space_map.py",
    "agentic/scripts/validate_derivation_vault.py",
    "agentic/scripts/validate_timeline_paper_interpretation.py",
    "agentic/scripts/validate_timeline_paper_blueprint.py",
    "agentic/scripts/validate_timeline_formal_derivation.py",
    "agentic/scripts/validate_timeline_paper_diagrams.py",
    "agentic/scripts/validate_timeline_paper_sections.py",
    "agentic/scripts/validate_timeline_latex_sections.py",
    "agentic/scripts/validate_bounded_numeric_probe.py",
    "agentic/scripts/validate_qualitative_relation_packets.py",
    "agentic/scripts/validate_qualitative_mechanistic_graph.py",
    "agentic/scripts/validate_parsimonious_probe_integration.py",
    "agentic/scripts/validate_equational_symbolic_integration.py",
    "agentic/scripts/validate_long_horizon_probe.py",
    "agentic/scripts/validate_yang_mills_bridge_lemma_packets.py",
    "agentic/scripts/validate_discovery_stretch.py",
    "agentic/scripts/validate_artifact_or_stop_control.py",
    "agentic/scripts/validate_proof_depth_control.py",
    "agentic/scripts/validate_proof_learning_ledger.py",
    "agentic/scripts/validate_proof_lockin_report.py",
    "agentic/scripts/validate_scientific_contribution_monitor.py",
    "agentic/scripts/validate_publishable_stepping_stone_fixtures.py",
    "agentic/scripts/validate_paper_relevance_marker_fixtures.py",
    "agentic/scripts/validate_target_literature_evolution.py",
    "agentic/scripts/validate_avenue_literature_gap_warrant.py",
    "agentic/scripts/validate_macro_strategy_report.py",
    "agentic/scripts/validate_strategy_progression_judge.py",
    "agentic/scripts/validate_discovery_marathon_state.py",
    "agentic/scripts/validate_discovery_marathon_cycle.py",
    "agentic/scripts/validate_parallel_api_marathon.py",
    "agentic/scripts/validate_discovery_marathon_skill_dispatch.py",
    "agentic/scripts/validate_discovery_marathon_report.py",
    "agentic/scripts/validate_discovery_marathon_theme_scoping.py",
    "agentic/scripts/validate_marathon_deep_review.py",
    "agentic/scripts/validate_empirical_evidence_requests.py",
    "agentic/scripts/validate_reasoning_monitor.py",
    "agentic/scripts/validate_big_deal_goal_archive.py",
    "agentic/scripts/validate_hamiltonian_gap_derivation.py",
    "agentic/scripts/validate_physics_math_interpretation.py",
    "agentic/scripts/validate_skill_taxonomy_projections.py",
    "agentic/scripts/validate_named_workflow_task_projection.py",
    "agentic/scripts/validate_named_workflow_trace_contracts.py",
    "agentic/scripts/validate_public_reasoning_trace.py",
    "agentic/scripts/validate_public_reasoning_trace_pdf.py",
    "agentic/scripts/validate_skill_integration.py",
    "agentic/scripts/validate_task_skill_registry.py",
    "agentic/scripts/validate_workflow_contracts.py",
    "agentic/scripts/validate_todos.py",
    "agentic/scripts/run_hook_contract_tests.py",
    "agentic/scripts/validate_skill_application_logs.py",
    "agentic/scripts/validate_promotion_gates.py",
)

# These commands validate while also generating evidence, or execute declared
# acceptance commands whose write surface is intentionally broader.  They are
# useful under explicit refresh but are not read-only validators.
REFRESH_ONLY_VALIDATORS = (
    "agentic/scripts/validate_active_target_workspace.py",
    "agentic/scripts/validate_skill_depth.py",
    "agentic/scripts/validate_proof_by_contradiction_routes.py",
    "agentic/scripts/validate_timeline_paper_forward_eval.py",
    "agentic/scripts/validate_todo_completion.py",
)

_CANDIDATE_VALIDATORS = {
    script
    for script in PIPELINE
    if Path(script).name.startswith("validate_")
    or Path(script).name == "run_hook_contract_tests.py"
}
_CLASSIFIED_VALIDATORS = set(READ_ONLY_VALIDATORS) | set(REFRESH_ONLY_VALIDATORS)
if _CANDIDATE_VALIDATORS != _CLASSIFIED_VALIDATORS:
    missing = sorted(_CANDIDATE_VALIDATORS - _CLASSIFIED_VALIDATORS)
    stale = sorted(_CLASSIFIED_VALIDATORS - _CANDIDATE_VALIDATORS)
    raise RuntimeError(
        "agentic validator write classification is incomplete; "
        f"unclassified={missing}, stale={stale}"
    )

# Compatibility name for callers that enumerate the default validation gate.
VALIDATION_SCRIPTS = READ_ONLY_VALIDATORS
REFRESH_SCRIPTS = _ordered_unique(
    [
        *(
            script
            for script in PIPELINE
            if script not in _CANDIDATE_VALIDATORS
            and script != "agentic/scripts/run_target_navigation.py"
        ),
        *REFRESH_ONLY_VALIDATORS,
    ]
)


PMP_PYTHON = ROOT / ".venv-pmp/bin/python"
PMP_SCRIPTS = {
    "skills/results_ellaboration/routea-symbolic-cas-auditor/scripts/audit_routea_symbolic_cas.py",
}


def interpreter_for(script: str) -> str:
    if script in PMP_SCRIPTS and PMP_PYTHON.exists():
        return str(PMP_PYTHON)
    return sys.executable


SNAPSHOT_EXCLUDED_DIRECTORY_NAMES = frozenset(
    {
        ".git",
        ".hypothesis",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".tox",
        ".venv",
        ".venv-pmp",
        "__pycache__",
        "node_modules",
    }
)
SNAPSHOT_EXCLUDED_SUFFIXES = frozenset({".pyc", ".pyo"})


def _repository_snapshot(root: Path = ROOT) -> dict[str, str]:
    """Digest the complete repository-owned surface, including ignored evidence.

    Git visibility is not an adequate read-only boundary because run receipts,
    reports, and target-local evidence may intentionally be ignored.  The walk
    excludes only version-control metadata, environments, and disposable
    interpreter/test caches.  Directory and symlink entries are included so an
    otherwise empty created namespace is still detected.
    """

    resolved_root = root.resolve()
    snapshot: dict[str, str] = {}
    for directory, names, filenames in os.walk(resolved_root, followlinks=False):
        directory_path = Path(directory)
        retained_names: list[str] = []
        for name in sorted(names):
            path = directory_path / name
            relative = path.relative_to(resolved_root).as_posix()
            if name in SNAPSHOT_EXCLUDED_DIRECTORY_NAMES:
                continue
            if path.is_symlink():
                snapshot[relative] = "symlink:" + os.readlink(path)
                continue
            snapshot[f"{relative}/"] = "directory"
            retained_names.append(name)
        names[:] = retained_names
        for name in sorted(filenames):
            path = directory_path / name
            if path.suffix in SNAPSHOT_EXCLUDED_SUFFIXES:
                continue
            relative = path.relative_to(resolved_root).as_posix()
            try:
                metadata = path.lstat()
                if stat.S_ISLNK(metadata.st_mode):
                    snapshot[relative] = "symlink:" + os.readlink(path)
                elif stat.S_ISREG(metadata.st_mode):
                    digest = hashlib.sha256()
                    with path.open("rb") as stream:
                        for block in iter(lambda: stream.read(1024 * 1024), b""):
                            digest.update(block)
                    snapshot[relative] = (
                        f"file:{stat.S_IMODE(metadata.st_mode):o}:{digest.hexdigest()}"
                    )
                else:
                    snapshot[relative] = f"special:{stat.S_IFMT(metadata.st_mode):o}"
            except FileNotFoundError:
                # A concurrent removal is represented by its absence in this
                # snapshot and will therefore be visible in the comparison.
                continue
    return snapshot


# Historical private name retained for focused callers while its semantics are
# now intentionally broader than Git-visible files.
_visible_file_snapshot = _repository_snapshot


def _changed_paths(before: dict[str, str], after: dict[str, str]) -> list[str]:
    return sorted(
        path
        for path in set(before) | set(after)
        if before.get(path) != after.get(path)
    )


def _run_scripts(scripts: tuple[str, ...]) -> int:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    # Validators are launched by file path, which otherwise places only
    # ``agentic/scripts`` on sys.path.  Keep the repository package importable
    # for validators that share ``agentic.discovery`` contracts.
    existing_pythonpath = environment.get("PYTHONPATH", "")
    environment["PYTHONPATH"] = str(ROOT) + (os.pathsep + existing_pythonpath if existing_pythonpath else "")
    for script in scripts:
        print(f"==> {script}")
        result = subprocess.run(
            [interpreter_for(script), script],
            cwd=ROOT,
            env=environment,
        )
        if result.returncode != 0:
            return result.returncode
    return 0


def _run_read_only_gate(scripts: tuple[str, ...]) -> int:
    """Run audited validators and compare the full surface even on failure."""

    before = _repository_snapshot()
    result = 1
    changed: list[str] = []
    try:
        result = _run_scripts(scripts)
    finally:
        changed = _changed_paths(before, _repository_snapshot())
        if changed:
            print(
                "ERROR: read-only validation changed repository files: "
                + ", ".join(changed[:20]),
                file=sys.stderr,
            )
    # A mutation is a stronger gate violation than the validator's own status.
    return 4 if changed else result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="explicitly regenerate legacy tracked artifacts before validating",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="print the selected scripts without executing them",
    )
    args = parser.parse_args()

    selected = (
        _ordered_unique([*REFRESH_SCRIPTS, *READ_ONLY_VALIDATORS])
        if args.refresh
        else READ_ONLY_VALIDATORS
    )
    if args.list:
        print("\n".join(selected))
        if not args.refresh:
            print(
                "Refresh-only omissions (run with --refresh): "
                + ", ".join(REFRESH_ONLY_VALIDATORS),
                file=sys.stderr,
            )
        return 0

    result = (
        _run_scripts(tuple(selected))
        if args.refresh
        else _run_read_only_gate(tuple(selected))
    )
    if result != 0:
        return result
    if args.refresh:
        print("All Abducer Looper refresh checks passed.")
    else:
        print("All Abducer Looper checks passed.")
        print("Validation mode: default read-only gate.")
        print(
            "Refresh-only validators omitted: "
            + ", ".join(REFRESH_ONLY_VALIDATORS)
            + ". Run with --refresh to execute their intentional write surfaces."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
