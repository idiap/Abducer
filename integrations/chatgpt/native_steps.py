# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Bounded adapters for real native operations in agent-driven workflows.

These functions validate authored conceptual artifacts or run COHERE's native
state machine with an explicit child executor. They do not generate substitute
scientific results or claim to execute the complete conceptual workflow. The
caller supplies an isolated workspace and trusted release; original hook and
domain policies remain authoritative inside those operations.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
from typing import Callable
from uuid import uuid4

from jsonschema import Draft202012Validator, ValidationError

from .native_hooks import NativeHookDispatcher

CONCEPTUAL_VALIDATOR_SOURCES = (
    "agentic/scripts/validate_hypothesis_exploration.py",
    "agentic/scripts/agentic_common.py",
    "agentic/scripts/abstraction_machinery_selection.py",
    "agentic/scripts/formal_subgoal_control.py",
    "agentic/spec/hypothesis_exploration_map.schema.json",
    "agentic/spec/formal_subgoal_control.schema.json",
    "agentic/spec/conceptual_pressure_packet.schema.json",
    "agentic/spec/abducer_validation_packet.schema.json",
)


def _validate_packet(validator, packet):
    """Return a bounded schema rejection without echoing the entire user packet."""
    try:
        validator.validate(packet)
    except ValidationError as error:
        location = "/".join(str(part) for part in error.absolute_path) or "root"
        raise ValueError(
            f"COHERE native schema rejected {location}: {error.validator}"
        ) from None


def _confined(root: Path, relative: str) -> Path:
    if (
        not isinstance(relative, str)
        or not relative
        or "\\" in relative
        or "\0" in relative
    ):
        raise ValueError("Invalid native artifact path")
    logical = PurePosixPath(relative)
    if logical.is_absolute() or any(
        part in {"", ".", ".."} for part in relative.split("/")
    ):
        raise ValueError("Native artifact path must be normalized and relative")
    candidate = root.joinpath(*logical.parts)
    for part in (candidate, *candidate.parents):
        if part == root.parent:
            break
        if part.is_symlink():
            raise ValueError("Native operation cannot follow symlinks")
    if not candidate.resolve().is_relative_to(root):
        raise ValueError("Native artifact path escapes workspace")
    return candidate


def _pin(source_root: Path, workspace: Path, paths: list[str]) -> None:
    """Verify native code/schema bytes before executing workspace-owned modules."""
    if source_root == workspace:
        raise ValueError("Native operations require a separate writable workspace")
    for relative in paths:
        expected = _confined(source_root, relative).read_bytes()
        actual = _confined(workspace, relative).read_bytes()
        if actual != expected:
            raise ValueError("Native operation source drift: " + relative)


def _module(workspace: Path, relative: str):
    """Load only a fixed, source-verified native module, never a caller path."""
    spec = importlib.util.spec_from_file_location(
        "abducer_native_step_" + uuid4().hex, _confined(workspace, relative)
    )
    if spec is None or spec.loader is None:
        raise ValueError("Native module unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_hypothesis_map(
    *, source_root: Path, workspace: Path, map_path: str, timeout_seconds: int = 60
) -> dict:
    """Run the original conceptual-map validator on a caller-authored artifact.

    Only this validator operation completes. Its success does not mean the full
    abductive workflow ran, that a release gate passed, or that a proof is valid.
    """
    source_root, workspace = Path(source_root).resolve(strict=True), Path(
        workspace
    ).resolve(strict=True)
    if type(timeout_seconds) is not int or not 1 <= timeout_seconds <= 300:
        raise ValueError("Validator timeout must be between 1 and 300 seconds")
    sources = list(CONCEPTUAL_VALIDATOR_SOURCES)
    _pin(source_root, workspace, sources)
    path = _confined(workspace, map_path)
    if path.stat().st_size > 2 * 1024 * 1024:
        raise ValueError("Conceptual map exceeds the bounded artifact budget")
    raw = path.read_bytes()
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("Conceptual map must be an object")
    # Native repo_path checks relative spelling; the adapter additionally keeps
    # references inside the isolated workspace when symlinks are present.
    for field in ("kb_path", "source_graph"):
        if field in payload:
            _confined(workspace, payload[field])
    hooks = NativeHookDispatcher(source_root=source_root, workspace=workspace)
    receipt = hooks.require(
        "PreToolUse",
        {
            "command": "python agentic/scripts/validate_hypothesis_exploration.py "
            + map_path,
            "path": map_path,
            "mutation_class": "read",
            "evidence": "native conceptual artifact validation",
        },
    )
    environment = {
        key: os.environ[key] for key in ("PATH", "LANG", "LC_ALL") if key in os.environ
    }
    environment.update(PYTHONDONTWRITEBYTECODE="1", PYTHONPATH=str(workspace))
    completed = subprocess.run(
        [sys.executable, str(_confined(workspace, sources[0])), map_path],
        cwd=workspace,
        env=environment,
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
        check=False,
    )
    if path.read_bytes() != raw:
        raise ValueError("Conceptual map changed during validation")
    return {
        "operation": "validate_hypothesis_map",
        "workflow_id": "conceptual_hypothesis_exploration_workflow",
        "status": "passed" if completed.returncode == 0 else "failed",
        "artifact": map_path,
        "artifact_sha256": hashlib.sha256(raw).hexdigest(),
        "exit_code": completed.returncode,
        "stdout": completed.stdout[:16000],
        "stderr": completed.stderr[:16000],
        "hook_receipt": receipt.as_dict(),
        "native_workflow_executed": False,
        "scientific_truth_verified": False,
        "scope": "Original deterministic artifact validator only; no candidate generation, release or proof authority.",
    }


def prepare_cohere_fast(
    *, source_root: Path, workspace: Path, command: str, target: str
) -> dict:
    """Parse native explicit activation and construct its bound input envelope.

    This prepares metadata only. It does not execute children, enable a domain,
    or invent evidence. The returned request can carry additional user context
    before being submitted to ``run_cohere_fast``.
    """
    source_root, workspace = Path(source_root).resolve(strict=True), Path(
        workspace
    ).resolve(strict=True)
    if (
        not isinstance(command, str)
        or len(command) > 500
        or not isinstance(target, str)
        or not 1 <= len(target) <= 16000
    ):
        raise ValueError("Invalid bounded COHERE activation")
    paths = [
        "hooks/scripts/cohere_fast_intake.py",
        "agentic/orchestration/cohere_fast_runner.py",
        "agentic/registries/domain_skill_bundles.yaml",
        "agentic/registries/cohere_fast_workflow_contracts.yaml",
    ]
    _pin(source_root, workspace, paths)
    activation = _module(workspace, paths[0]).parse_invocation(command, target=target)
    native = _module(workspace, paths[1])
    return {
        "activation_receipt": activation,
        "request": {
            "artifact_type": "DomainRunRequest",
            "workflow_id": "cohere_fast",
            "domain_id": activation["domain_id"],
            "run_id": activation["run_id"],
            "schema_version": "1.0",
            "target": activation["target"],
            "activation_receipt_digest": native.canonical_digest(activation),
        },
        "native_workflow_executed": False,
    }


def run_cohere_fast(
    *,
    source_root: Path,
    workspace: Path,
    command: str,
    target: str,
    request: dict,
    executor: Callable[[dict, dict], dict],
) -> dict:
    """Run original COHERE composition with a trusted host's real child executor.

    The executor is a server-side callable, never a client-supplied command.
    It may consume externally authored packets, but every packet is validated
    against the native schema and current activation before the native runner
    persists it. Source feature flags are read unchanged; this adapter never
    enables a disabled domain. Resume is intentionally not exposed until the
    native callback/input reconstruction has its own parity qualification.
    """
    source_root, workspace = Path(source_root).resolve(strict=True), Path(
        workspace
    ).resolve(strict=True)
    if (
        not isinstance(command, str)
        or len(command) > 500
        or not isinstance(target, str)
        or not 1 <= len(target) <= 16000
    ):
        raise ValueError("Invalid bounded COHERE activation")
    if not callable(executor) or not isinstance(request, dict):
        raise ValueError("COHERE requires a real child executor and request object")
    sources = [
        "hooks/scripts/cohere_fast_intake.py",
        "hooks/scripts/cohere_fast_policy.py",
        "agentic/orchestration/cohere_fast_runner.py",
        "agentic/registries/domain_skill_bundles.yaml",
        "agentic/registries/cohere_fast_workflow_contracts.yaml",
        "agentic/registries/cohere_fast_subworkflows.yaml",
        "agentic/spec/cohere_fast_artifacts.schema.json",
    ]
    _pin(source_root, workspace, sources)
    intake = _module(workspace, sources[0])
    policy = _module(workspace, sources[1])
    native = _module(workspace, sources[2])
    hooks = NativeHookDispatcher(source_root=source_root, workspace=workspace)
    hook_receipts = []

    def event(name: str, payload: dict):
        receipt = hooks.require(name, payload)
        hook_receipts.append(receipt.as_dict())

    event("UserPromptSubmit", {"prompt": command, "target": target})
    activation = intake.parse_invocation(command, target=target)
    prefix = f"cohere-fast/{activation['domain_id']}/{activation['run_id']}/"
    run_relative = "artifacts/" + prefix.rstrip("/")
    run_root = _confined(workspace, run_relative)
    if run_root.exists():
        raise ValueError(
            "COHERE run already exists; automatic replay/resume is not admitted"
        )
    schema = json.loads(_confined(workspace, sources[-1]).read_text())
    validator = Draft202012Validator(schema)
    _validate_packet(validator, request)
    if request.get("artifact_type") != "DomainRunRequest":
        raise ValueError("COHERE requires a DomainRunRequest")
    for key in ("workflow_id", "domain_id", "run_id", "target"):
        if request.get(key) != activation.get(key):
            raise ValueError("COHERE request activation binding mismatch")
    if request.get("activation_receipt_digest") != native.canonical_digest(activation):
        raise ValueError("COHERE activation receipt digest mismatch")
    pending = None
    last_packet = copy.deepcopy(request)
    attempts = {}
    policy_receipts = []

    def finish_pending():
        nonlocal pending
        if pending is not None:
            event(
                "PostSkillUse",
                {"skill": "cohere-fast-orchestrator", "expected_artifacts": pending},
            )
            pending = None

    def execute(child: dict, packet: dict) -> dict:
        nonlocal pending, last_packet
        finish_pending()
        attempts[child["id"]] = attempts.get(child["id"], 0) + 1
        binding = {
            **activation,
            "activation_receipt": activation,
            "skill": "cohere-fast-orchestrator",
            "artifact_prefix": prefix,
            "subworkflow_id": child["id"],
            "parent_run_id": activation["run_id"],
        }
        decision = policy.authorize(binding)
        policy_receipts.append(decision)
        if decision["decision"] != "accept":
            raise ValueError("COHERE domain policy blocked: " + decision["reason"])
        if (
            child["id"] == "manuscript-release"
            and last_packet.get("audit_status") != "accepted"
        ):
            raise ValueError(
                "An accepted independent-audit packet is required before manuscript release"
            )
        event(
            "PreSkillUse",
            {
                "skill": "cohere-fast-orchestrator",
                "controlled": True,
                "workflow_id": "cohere_fast",
                "step_id": child["id"],
            },
        )
        # This callback runs under the worker's trusted host/tool boundary.
        # Copy objects so it cannot rewrite native child contracts or receipts.
        result = executor(copy.deepcopy(child), copy.deepcopy(packet))
        if not isinstance(result, dict) or result.get("state") not in {
            "accepted",
            "failed",
            "quarantined",
            "stopped",
        }:
            raise ValueError("COHERE executor returned an invalid native result")
        output = result.get("packet")
        if not isinstance(output, dict):
            raise ValueError("COHERE executor must return its actual typed packet")
        _validate_packet(validator, output)
        if output.get("artifact_type") == "DomainRunRequest":
            raise ValueError(
                "COHERE child cannot return the original request as its result"
            )
        for key in ("workflow_id", "domain_id", "run_id"):
            if output.get(key) != activation[key]:
                raise ValueError("COHERE child packet binding mismatch")
        if (
            output.get("artifact_type") == "CohereFastStagePacket"
            and output.get("stage_id") != child["id"]
        ):
            raise ValueError("COHERE child packet stage mismatch")
        if (
            output.get("artifact_type") == "CohereFastStagePacket"
            and result["state"] == "accepted"
            and output.get("disposition") != "accepted"
        ):
            raise ValueError(
                "COHERE accepted state contradicts child packet disposition"
            )
        artifacts = result.get("artifacts", {})
        if not isinstance(artifacts, dict) or len(artifacts) > 100:
            raise ValueError("COHERE artifact count exceeds budget")
        total = 0
        for relative, content in artifacts.items():
            if not isinstance(content, (str, bytes)):
                raise ValueError("COHERE artifacts must contain authored text or bytes")
            path = _confined(run_root, relative)
            total += len(content.encode() if isinstance(content, str) else content)
            if total > 4 * 1024 * 1024:
                raise ValueError("COHERE artifact bytes exceed budget")
            event(
                "PreToolUse",
                {
                    "command": "native COHERE artifact write",
                    "path": path.relative_to(workspace).as_posix(),
                    "evidence": "validated child packet",
                },
            )
        receipt_path = run_relative + "/receipts/" + child["id"] + ".json"
        event(
            "PreToolUse",
            {
                "command": "native COHERE receipt write",
                "path": receipt_path,
                "evidence": "native child receipt",
            },
        )
        # Native retries do not persist an intermediate failed callback result.
        if result["state"] == "failed" and attempts[child["id"]] < int(
            child.get("budget", {}).get("max_attempts", 1)
        ):
            event(
                "PostSkillUse",
                {"skill": "cohere-fast-orchestrator", "expected_artifacts": []},
            )
        else:
            pending = [run_relative + "/" + relative for relative in artifacts] + [
                receipt_path
            ]
        last_packet = copy.deepcopy(output)
        return result

    result = native.CohereFastRunner(workspace / "artifacts").run(
        activation, copy.deepcopy(request), execute
    )
    finish_pending()
    event("Stop", {"controlled": True, "workflow_id": "cohere_fast"})
    return {
        "operation": "run_cohere_fast_authored_packets",
        "result": result,
        "activation_receipt": activation,
        "hook_receipts": hook_receipts,
        "domain_policy_receipts": policy_receipts,
        "final_packet": last_packet,
        "scientific_truth_verified": False,
        "scope": "Native COHERE composition and validation of host-authored packets; callback evidence retains its original scientific status.",
    }
