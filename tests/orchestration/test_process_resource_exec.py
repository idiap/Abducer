# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Closed-contract tests for the stdlib resource-limit exec trampoline."""

from __future__ import annotations

import base64
import concurrent.futures
import copy
import json
import os
import platform
import resource
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

import agentic.process_resource_exec as resource_exec
from agentic.process_resource_exec import (
    RESOURCE_EXEC_DIAGNOSTIC_PREFIX,
    RESOURCE_EXEC_SCOPE,
    RESOURCE_EXEC_SETUP_FAILURE,
    ResourceExecPlan,
    ResourceExecPlanError,
    apply_kernel_limits,
    canonical_json_bytes,
    decode_plan_token,
    supervision_environment_digest,
    validate_live_binding,
)


pytestmark = pytest.mark.skipif(
    platform.system() not in {"Darwin", "Linux"},
    reason="the sealed resource trampoline currently supports Darwin and Linux",
)

_PYTHON = str(Path(sys.executable).resolve(strict=True))
_LAUNCHER = str(Path(resource_exec.__file__).resolve(strict=True))


def _environment(**extra: str) -> dict[str, str]:
    environment = {
        "LANG": "C",
        "LC_ALL": "C",
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONUTF8": "1",
        **extra,
    }
    # macOS inserts this deterministic per-user CoreFoundation binding before
    # Python initializes.  Supplying it explicitly makes the replacement
    # environment, and therefore its digest, exact rather than ambient.
    if platform.system() == "Darwin" and "__CF_USER_TEXT_ENCODING" in os.environ:
        environment["__CF_USER_TEXT_ENCODING"] = os.environ["__CF_USER_TEXT_ENCODING"]
    return environment


def _plan(
    tmp_path: Path,
    *,
    logical_argv: list[str] | None = None,
    environment: dict[str, str] | None = None,
    platform_system: str | None = None,
) -> ResourceExecPlan:
    return ResourceExecPlan.build(
        logical_argv=logical_argv or [_PYTHON, "-I", "-B", "-c", "pass"],
        cwd=tmp_path,
        environment=environment or _environment(),
        remaining_cpu_ns=5_000_000_000,
        cpu_grace_ns=1_000_000_000,
        workspace_disk_bytes=2 * 1024 * 1024,
        process_memory_bytes=768 * 1024 * 1024,
        platform_system=platform_system,
    )


def _transport(plan: ResourceExecPlan, logical_argv: list[str]) -> list[str]:
    return [
        _PYTHON,
        "-I",
        "-B",
        _LAUNCHER,
        "--resource-plan-base64",
        plan.base64_token(),
        "--",
        *logical_argv,
    ]


def test_plan_round_trip_is_canonical_and_live_bound(tmp_path: Path) -> None:
    environment = _environment(BOUND_VALUE="exact")
    logical_argv = [_PYTHON, "-I", "-B", "-c", "print('bound')"]
    plan = _plan(tmp_path, logical_argv=logical_argv, environment=environment)
    reopened = decode_plan_token(plan.base64_token())
    assert reopened == plan
    assert reopened.as_dict()["scope"] == RESOURCE_EXEC_SCOPE
    assert (
        reopened.supervision_environment_digest
        == supervision_environment_digest(environment)
    )
    assert base64.b64decode(plan.base64_token(), validate=True) == plan.canonical_bytes()
    assert validate_live_binding(
        reopened,
        logical_argv=logical_argv,
        cwd=tmp_path,
        environment=environment,
    ) == (tuple(logical_argv), environment)


def test_live_binding_rejects_forged_supervision_environment_cross_digest(
    tmp_path: Path,
) -> None:
    environment = _environment(BOUND_VALUE="exact")
    logical_argv = [_PYTHON, "-I", "-B", "-c", "pass"]
    raw = _plan(
        tmp_path,
        logical_argv=logical_argv,
        environment=environment,
    ).as_dict()
    raw["supervision_environment_digest"] = "sha256:" + "0" * 64
    forged = ResourceExecPlan.from_mapping(raw)
    with pytest.raises(
        ResourceExecPlanError,
        match="live supervision environment differs",
    ):
        validate_live_binding(
            forged,
            logical_argv=logical_argv,
            cwd=tmp_path,
            environment=environment,
        )


@pytest.mark.parametrize(
    "mutation",
    (
        "extra_key",
        "missing_key",
        "noncanonical_json",
        "noncanonical_base64",
        "malformed_base64",
        "wrong_scope",
    ),
)
def test_decoder_rejects_every_noncanonical_or_open_plan_form(
    tmp_path: Path,
    mutation: str,
) -> None:
    raw = _plan(tmp_path).as_dict()
    if mutation == "extra_key":
        raw["extra"] = True
        token = base64.b64encode(canonical_json_bytes(raw)).decode("ascii")
    elif mutation == "missing_key":
        raw.pop("scope")
        token = base64.b64encode(canonical_json_bytes(raw)).decode("ascii")
    elif mutation == "noncanonical_json":
        token = base64.b64encode(json.dumps(raw, indent=2).encode("utf-8")).decode("ascii")
    elif mutation == "noncanonical_base64":
        token = _plan(tmp_path).base64_token() + "\n"
    elif mutation == "malformed_base64":
        token = "!!!"
    else:
        raw["scope"]["hard_group_cpu_limit"] = True
        token = base64.b64encode(canonical_json_bytes(raw)).decode("ascii")
    with pytest.raises(ResourceExecPlanError):
        decode_plan_token(token)


@pytest.mark.parametrize("binding", ("argv", "cwd", "environment", "platform"))
def test_live_binding_rejects_every_identity_change(tmp_path: Path, binding: str) -> None:
    environment = _environment()
    logical_argv = [_PYTHON, "-I", "-B", "-c", "pass"]
    plan = _plan(tmp_path, logical_argv=logical_argv, environment=environment)
    changed_argv = logical_argv
    changed_cwd: Path = tmp_path
    changed_environment = environment
    changed_platform = platform.system()
    if binding == "argv":
        changed_argv = [*logical_argv, "changed"]
    elif binding == "cwd":
        changed_cwd = tmp_path / "different"
        changed_cwd.mkdir()
    elif binding == "environment":
        changed_environment = {**environment, "CHANGED": "1"}
    else:
        changed_platform = "Linux" if platform.system() == "Darwin" else "Darwin"
    with pytest.raises(ResourceExecPlanError):
        validate_live_binding(
            plan,
            logical_argv=changed_argv,
            cwd=changed_cwd,
            environment=changed_environment,
            platform_system=changed_platform,
        )


def test_trampoline_preserves_exact_cwd_environment_stdin_and_kernel_limits(
    tmp_path: Path,
) -> None:
    environment = _environment(BOUND_VALUE="exact")
    worker_code = (
        "import json,os,resource,sys; "
        "print(json.dumps({"
        "'cwd':os.getcwd(),"
        "'env':dict(os.environ),"
        "'stdin':sys.stdin.buffer.read().decode('utf-8'),"
        "'cpu':resource.getrlimit(resource.RLIMIT_CPU),"
        "'fsize':resource.getrlimit(resource.RLIMIT_FSIZE),"
        "'as':resource.getrlimit(resource.RLIMIT_AS) if hasattr(resource,'RLIMIT_AS') else None"
        "},sort_keys=True))"
    )
    logical_argv = [_PYTHON, "-I", "-B", "-c", worker_code]
    plan = _plan(tmp_path, logical_argv=logical_argv, environment=environment)
    completed = subprocess.run(
        _transport(plan, logical_argv),
        cwd=tmp_path,
        env=environment,
        input=b"opaque-stdin",
        capture_output=True,
        timeout=10,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr.decode(errors="replace")
    assert completed.stderr == b""
    observed = json.loads(completed.stdout)
    assert observed["cwd"] == str(tmp_path.resolve(strict=True))
    assert observed["env"] == environment
    assert observed["stdin"] == "opaque-stdin"
    assert observed["cpu"] == [
        plan.rlimit_cpu_soft_seconds,
        plan.rlimit_cpu_hard_seconds,
    ]
    assert observed["fsize"] == [plan.rlimit_fsize_bytes, plan.rlimit_fsize_bytes]
    if platform.system() == "Linux":
        assert observed["as"] == [plan.rlimit_as_bytes, plan.rlimit_as_bytes]
    else:
        assert plan.rlimit_as_bytes is None


def test_apply_kernel_limits_is_platform_exact(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[int, tuple[int, int]]] = []
    monkeypatch.setattr(resource_exec.resource, "setrlimit", lambda kind, value: calls.append((kind, value)))
    system = platform.system()
    plan = _plan(tmp_path, platform_system=system)
    apply_kernel_limits(plan)
    assert calls[0] == (
        resource.RLIMIT_CPU,
        (plan.rlimit_cpu_soft_seconds, plan.rlimit_cpu_hard_seconds),
    )
    assert calls[1] == (
        resource.RLIMIT_FSIZE,
        (plan.rlimit_fsize_bytes, plan.rlimit_fsize_bytes),
    )
    if system == "Linux":
        assert calls[2] == (
            resource.RLIMIT_AS,
            (plan.rlimit_as_bytes, plan.rlimit_as_bytes),
        )
    else:
        assert len(calls) == 2


def test_setup_failure_is_bounded_stderr_only(tmp_path: Path) -> None:
    completed = subprocess.run(
        [
            _PYTHON,
            "-I",
            "-B",
            _LAUNCHER,
            "--resource-plan-base64",
            "!!!",
            "--",
            "/bin/true",
        ],
        cwd=tmp_path,
        env=_environment(),
        input=b"must-not-be-consumed-as-diagnostics",
        capture_output=True,
        timeout=10,
        check=False,
    )
    assert completed.returncode == RESOURCE_EXEC_SETUP_FAILURE
    assert completed.stdout == b""
    assert completed.stderr.startswith(RESOURCE_EXEC_DIAGNOSTIC_PREFIX)
    assert len(completed.stderr) <= resource_exec.MAX_DIAGNOSTIC_BYTES


def test_worker_exit_125_passes_through_without_launcher_reclassification(tmp_path: Path) -> None:
    logical_argv = [_PYTHON, "-I", "-B", "-c", "raise SystemExit(125)"]
    environment = _environment()
    plan = _plan(tmp_path, logical_argv=logical_argv, environment=environment)
    completed = subprocess.run(
        _transport(plan, logical_argv),
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        timeout=10,
        check=False,
    )
    assert completed.returncode == 125
    assert completed.stdout == b""
    assert completed.stderr == b""


def test_parallel_trampolines_do_not_use_a_fork_preexec_callback(tmp_path: Path) -> None:
    logical_argv = ["/usr/bin/true"]
    environment = _environment()
    plan = _plan(tmp_path, logical_argv=logical_argv, environment=environment)
    transport = _transport(plan, logical_argv)

    def run_one(_index: int) -> int:
        return subprocess.run(
            transport,
            cwd=tmp_path,
            env=environment,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            timeout=10,
            check=False,
        ).returncode

    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
        returncodes = list(pool.map(run_one, range(32)))
    assert returncodes == [0] * 32


def test_plan_mapping_rejects_inconsistent_cpu_and_platform_limits(tmp_path: Path) -> None:
    raw = _plan(tmp_path).as_dict()
    for mutation in ("cpu", "darwin_as", "linux_as"):
        changed: dict[str, Any] = copy.deepcopy(raw)
        if mutation == "cpu":
            changed["kernel_limits"]["rlimit_cpu_soft_seconds"] += 1
        elif mutation == "darwin_as":
            changed["platform_system"] = "Darwin"
            changed["kernel_limits"]["rlimit_as_bytes"] = 1
        else:
            changed["platform_system"] = "Linux"
            changed["kernel_limits"]["rlimit_as_bytes"] = None
        with pytest.raises(ResourceExecPlanError):
            ResourceExecPlan.from_mapping(changed)
