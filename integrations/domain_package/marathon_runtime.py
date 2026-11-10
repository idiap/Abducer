# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Run a selected source marathon inside Lunar's native package worker.

The package binding selects a persisted run and its canonical authorization.
This adapter copies the immutable package to the confined output workspace,
invokes the existing CLI, and publishes only reports produced by that invocation.
It never manufactures canonical receipts or substitutes the old Prism demo.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import sys

TARGET = "yang-mills-existence-and-mass-gap-target"
RUN_ID = "yang-mills-smoke-marathon"
REPORT_ROOT = "agentic/reports/discovery_marathon/targets/" + TARGET


def confined(root: Path, value: str) -> Path:
    """Resolve package-relative inputs without accepting traversal or symlinks."""
    path = PurePosixPath(value)
    if not value or path.is_absolute() or any(p in {".", ".."} for p in value.split("/")) or "\\" in value:
        raise ValueError("Expected a confined repository-relative path")
    candidate = root / path
    if candidate.is_symlink() or any(p.is_symlink() for p in candidate.parents if p != root.parent):
        raise ValueError("Runtime inputs cannot contain symlinks")
    candidate.resolve().relative_to(root.resolve())
    return candidate


def read_binding(source: Path, inputs: dict | None = None) -> dict:
    """Select only a packaged target/run; filenames never come from the form."""
    if inputs is not None and (not isinstance(inputs, dict) or set(inputs) != {"target_id", "run_id"}):
        raise ValueError("Select a target and run from the package")
    binding_path = source.parent / "marathon-binding.json"
    if not binding_path.is_file():
        raise ValueError("This package lacks a marathon catalog; re-export it with the current integration")
    binding = json.loads(binding_path.read_text())
    if binding.get("version") == 2:
        if not isinstance(inputs, dict) or set(inputs) != {"target_id", "run_id"}:
            raise ValueError("Select a target and run from the package")
        matches = [run for run in binding["runs"]
                   if all(run.get(key) == inputs[key] for key in ("target_id", "run_id"))]
        if len(matches) != 1:
            raise ValueError("Selected target/run is not available in this package")
        binding = matches[0]
    elif inputs and any(binding.get(key) != inputs.get(key) for key in ("target_id", "run_id")):
        raise ValueError("Selected target/run differs from the package binding")
    if binding.get("initialize") is True:
        if binding.get("run_id") != "new" or binding.get("target_id") not in {
            "p-vs-np-target", "yang-mills-existence-and-mass-gap-target"}:
            raise ValueError("Unregistered automatic initialization target")
        return binding
    if not binding.get("canonical_theory_cycle"):
        raise ValueError(
            "Research cannot start: the selected marathon has no committed canonical theory cycle. "
            "Create a current canonical binding for this run and re-export with --canonical-theory-cycle. "
            "Historical reports and the seven-step demo are not research execution.")
    return binding


def prepare(*, workflow_id, inputs, mode, run_id, run_root, network_authority, on_reasoning, **kwargs):
    """Check immutable prerequisites before creating state or calling a model."""
    # The runtime interface supplies this hook; preparation emits no reasoning.
    del on_reasoning
    if workflow_id != "discovery_marathon_loop" or mode != "live":
        raise ValueError("Only the live Discovery Marathon is registered")
    source = Path(__file__).resolve().parents[2]
    binding = read_binding(source, inputs)
    target_id = binding["target_id"]
    if binding.get("initialize") is True:
        if not network_authority or not callable(kwargs.get("public_fetch")):
            raise ValueError("Starting a new run requires the declared public literature reads")
        # The host request identity gives a separate run even when two users
        # choose the same target. The form never supplies a writable path.
        binding = {**binding, "run_id": "lunar-marathon-" + hashlib.sha256(str(run_id).encode()).hexdigest()[:24]}
        digest = hashlib.sha256(json.dumps(binding, sort_keys=True).encode()).hexdigest()
        return {"prepared_input": {"entry_argument_name": "context", "value": binding,
                    "request_digest": digest, "analysis_results": {}},
            "state": {"source": str(source), "run_root": str(run_root), "binding": binding, "initial_cycle_count": 0},
            "events": [{"kind": "stage", "payload": {"stage_id": "prepare", "component_id": workflow_id,
                "status": "completed", "safe_summary": "New run selected; literature and theory initialization will run first."}}]}
    state_path = confined(source, f"agentic/runs/discovery_marathons/{binding['run_id']}/run_state.json")
    run_state = json.loads(state_path.read_text())
    if (run_state.get("target_id"), run_state.get("run_id")) != (target_id, binding["run_id"]):
        raise ValueError("Marathon state differs from the package target/run binding")
    cycle_path = confined(source, binding["canonical_theory_cycle"])
    cycle = json.loads(cycle_path.read_text())
    if (cycle.get("target_id"), cycle.get("run_id")) != (target_id, binding["run_id"]):
        raise ValueError("Canonical cycle target/run differs from the selected marathon")
    if not confined(source, binding["canonical_theory_state_root"]).is_dir():
        raise ValueError("Canonical transaction store is absent from the package")
    digest = hashlib.sha256(json.dumps(binding, sort_keys=True).encode()).hexdigest()
    return {"prepared_input": {"entry_argument_name": "context", "value": binding,
                               "request_digest": digest, "analysis_results": {}},
            "state": {"source": str(source), "run_root": str(run_root), "binding": binding,
                      "initial_cycle_count": run_state["cycle_count"]},
            "events": [{"kind": "stage", "payload": {"stage_id": "prepare",
                "component_id": workflow_id, "status": "completed",
                "safe_summary": "Run selected; source runner will verify its canonical authorization."}}]}


def initialize_marathon_branches(workspace: Path, binding: dict, gate: dict):
    """Translate exact committed hypotheses into the legacy runner's branch shape."""
    from agentic.discovery.contracts import canonical_digest
    initializer = importlib.import_module("init_discovery_marathon")
    common = importlib.import_module("discovery_marathon_common")
    cycle = json.loads(confined(workspace, binding["canonical_theory_cycle"]).read_text())
    seeds = json.loads(confined(workspace, binding["canonical_branch_seeds"]).read_text())
    if (seeds["target_id"], seeds["run_id"], seeds["canonical_cycle_digest"]) != (
            binding["target_id"], binding["run_id"], canonical_digest(cycle)):
        raise ValueError("Marathon seed lineage differs from its canonical cycle")
    if [row["binding"] for row in seeds["branches"]] != cycle["identity_map"]["branch_bindings"]:
        raise ValueError("Marathon branch identities differ from canonical genealogy")
    descriptor = next(row for row in cycle["operator_evidence"]["role_bindings"] if row["role"] == "high_risk_portfolio")
    data = confined(workspace, descriptor["original_path"]).read_bytes()
    if "sha256:" + hashlib.sha256(data).hexdigest() != descriptor["sha256"]:
        raise ValueError("Canonical portfolio bytes changed before marathon initialization")
    portfolio = json.loads(data)
    if seeds["source_portfolio"] != portfolio:
        raise ValueError("Marathon seeds differ from the canonical portfolio")
    hypotheses = {row["hypothesis_id"]: row for row in portfolio["hypotheses"]}
    state, _ = initializer.build_initial_state(binding["target_id"], hours=6, cycle_minutes=30,
                                              max_active_branches=3, run_id=binding["run_id"])
    branches = []
    for index, row in enumerate(seeds["branches"], 1):
        hypothesis, identity = row["hypothesis"], row["binding"]
        if hypotheses.get(identity["hypothesis_id"]) != hypothesis:
            raise ValueError("Marathon hypothesis differs from its exact canonical ancestor")
        branch = common.default_branch({"title": hypothesis["mechanism_key"].replace("_", " "),
            "controlled_interface": hypothesis["maturation_question"], "hypothesis": hypothesis["intuitive_leap"],
            "mathematical_mechanism": hypothesis["mechanism"],
            "dependencies": hypothesis["assumptions_or_invariants_risked"],
            "falsifiers": hypothesis["correction_conditions"],
            "promotion_signal": "Require existing proof and transfer gates before any claim promotion."},
            binding["run_id"], binding["target_id"], index)
        branch["branch_id"] = identity["branch_id"]
        branch["local_memory_path"] = common.rel(common.branch_path(binding["run_id"], identity["branch_id"]))
        branch["canonical_hypothesis"] = hypothesis
        branch["canonical_identity_binding"] = identity
        branch["status"] = "active" if identity["branch_id"] in gate["eligible_branch_ids"] else "watch"
        branches.append(branch)
    state["branch_registry"] = [{key: row[key] for key in (
        "branch_id", "title", "status", "priority", "local_memory_path")} for row in branches]
    state["active_branch_ids"] = [row["branch_id"] for row in branches if row["status"] == "active"]
    state["canonical_initialization"] = {"status": gate["status"],
        "cycle_id": cycle["cycle_id"], "committed_state_version": cycle["committed_state_version"],
        "preference_decision": cycle["conceptual_authority"]["decision"],
        "research_authorized": bool(gate["eligible_branch_ids"]),
        "summary": ("Current canonical theory authorizes the selected branches." if gate["eligible_branch_ids"]
                    else "Initialization completed. The conceptual review requires revision of every candidate; no research branch investment is authorized.")}
    initializer.persist_run(state, branches)
    return state


def execute(*, state, services):
    """Invoke the same CLI and report pipeline, with no gate or renderer override."""
    source = Path(state["source"])
    output = Path(state["run_root"])
    workspace = output / "workspace"
    services.event("stage", {"stage_id": "workspace", "component_id": "discovery_marathon_loop",
        "status": "running", "safe_summary": "Preparing the isolated research workspace and report sources."})
    # The package is immutable. All scheduler, transaction and report writes go
    # to this per-run copy; previous local research is never mutated by Lunar.
    for path in source.rglob("*"):
        if path.is_symlink():
            raise ValueError("Runtime snapshot contains a symlink")
    shutil.copytree(source, workspace)
    services.event("stage", {"stage_id": "workspace", "component_id": "discovery_marathon_loop",
        "status": "completed", "safe_summary": "Research workspace ready."})
    # Keep the request snapshot stable when execution adds committed output paths.
    binding = dict(state["binding"])
    state["binding"] = binding
    target_id = binding["target_id"]
    report_dir = confined(workspace, "agentic/reports/discovery_marathon/targets/" + target_id)
    for name in ("latest.html", "full_timeline.html", "latest.json", "latest.md"):
        (report_dir / name).unlink(missing_ok=True)
    previous_path, previous_argv, previous_cwd = list(sys.path), sys.argv, Path.cwd()
    previous_pythonpath = os.environ.get("PYTHONPATH")
    outcome = "research_cycle_completed"
    try:
        sys.path[:0] = [str(workspace / "agentic/scripts"), str(workspace)]
        os.environ["PYTHONPATH"] = os.pathsep.join([str(workspace), str(workspace / "agentic/scripts")])
        os.chdir(workspace)
        if binding.get("initialize") is True:
            initialization = importlib.import_module("agentic.discovery.bootstrap_pipeline")
            if Path(initialization.__file__).resolve() != workspace / "agentic/discovery/bootstrap_pipeline.py":
                raise ValueError("Initialization module was loaded outside the isolated workspace")
            initialized = initialization.initialize_canonical_theory(workspace=workspace,
                root=workspace / "agentic/runs/discovery_initializations" / binding["run_id"],
                target_id=target_id, run_id=binding["run_id"], model_id=services.model.model_id,
                completion=services.completion, public_fetch=services.public_fetch, event=services.event)
            binding.update(initialized)
            from agentic.discovery.theory_gate import verify_canonical_theory_cycle
            gate = verify_canonical_theory_cycle(confined(workspace, binding["canonical_theory_cycle"]),
                target_id=target_id, run_id=binding["run_id"], state_root=confined(workspace, binding["canonical_theory_state_root"]))
            initialize_marathon_branches(workspace, binding, gate)
            if not gate["eligible_branch_ids"]:
                outcome = "initialization_requires_revision"
        sys.argv = ["run_discovery_marathon.py", "--target", target_id, "--run-id", binding["run_id"],
            "--resume", "--execution-mode", "research", "--branch-engine", "api", "--max-cycles", "1",
            "--api-max-workers", "1", "--canonical-theory-cycle", binding["canonical_theory_cycle"],
            "--canonical-theory-state-root", binding["canonical_theory_state_root"]]
        runner = importlib.import_module("run_discovery_marathon")
        if Path(runner.__file__).resolve() != workspace / "agentic/scripts/run_discovery_marathon.py":
            raise ValueError("Marathon module was loaded outside the isolated workspace")
        services.event("stage", {"stage_id": "marathon", "component_id": "discovery_marathon_loop",
                                "status": "running", "safe_summary": f"Running {binding['run_id']} for {target_id}."})
        if outcome == "initialization_requires_revision":
            services.event("stage", {"stage_id": "marathon", "component_id": "discovery_marathon_loop",
                "status": "completed", "safe_summary": "Initialization requires conceptual revision; generating the report with zero research cycles."})
            runner.rebuild_reports(binding["run_id"], target_id)
            status = 0
        else:
            with runner.bind_host_model(services.completion, services.model.model_id):
                status = runner.main()
        if status != 0:
            raise ValueError(f"Source marathon failed with exit status {status}; no report released")
    except SystemExit as exc:
        raise ValueError(f"Source marathon stopped: {exc}; no report released") from exc
    finally:
        sys.path[:] = previous_path
        sys.argv = previous_argv
        os.chdir(previous_cwd)
        if previous_pythonpath is None:
            os.environ.pop("PYTHONPATH", None)
        else:
            os.environ["PYTHONPATH"] = previous_pythonpath
    final_state = json.loads(confined(workspace, f"agentic/runs/discovery_marathons/{binding['run_id']}/run_state.json").read_text())
    expected_cycles = state["initial_cycle_count"] + (outcome == "research_cycle_completed")
    if final_state["cycle_count"] != expected_cycles:
        raise ValueError("Source runner did not persist exactly one new cycle")
    return {"workspace": str(workspace), "cycle_count": final_state["cycle_count"], "execution_outcome": outcome,
            "runner_sha256": hashlib.sha256((workspace / "agentic/scripts/run_discovery_marathon.py").read_bytes()).hexdigest()}


def verify(*, state, execution, services):
    """Release the newly generated HTML bytes with their source run identity."""
    output = Path(state["run_root"])
    workspace = Path(execution["workspace"])
    if workspace.resolve() != (output / "workspace").resolve():
        raise ValueError("Execution workspace differs from the prepared run")
    target_id = state["binding"]["target_id"]
    report_dir = confined(workspace, "agentic/reports/discovery_marathon/targets/" + target_id)
    report = json.loads((report_dir / "latest.json").read_text())
    if (report.get("target_id"), report.get("run_id")) != (target_id, state["binding"]["run_id"]):
        raise ValueError("Generated report target/run mismatch")
    if report.get("cycle_count") != execution["cycle_count"]:
        raise ValueError("Generated report does not include the newly persisted cycle")
    descriptors = {}
    for name in ("latest.html", "full_timeline.html", "latest.json", "latest.md"):
        content = (report_dir / name).read_bytes()
        if not content:
            raise ValueError("Generated report is empty: " + name)
        (output / name).write_bytes(content)
        descriptors[name] = {"path": name, "sha256": hashlib.sha256(content).hexdigest(),
                             "media_type": "text/html" if name.endswith(".html") else "application/json" if name.endswith(".json") else "text/markdown"}
    markdown = (output / "latest.md").read_text()
    result = {"markdown": markdown,
              "structured_value": {"target_id": target_id, "run_id": report["run_id"],
                  "cycle_count": execution["cycle_count"], "html_report": descriptors["full_timeline.html"],
                  "execution_outcome": execution.get("execution_outcome", "research_cycle_completed"),
                  "report_artifacts": descriptors, "runner_sha256": execution["runner_sha256"]},
              "analysis_results": {}, "compact_prism_input": state["binding"], "narrative_slots": [],
              "report_verification": {"status": "passed", "scope": "source runner success and report identity",
                                      "scientific_truth_verified": False}}
    (output / "marathon-result.json").write_text(json.dumps(result, indent=2))
    return {"result": result, "events": []}
