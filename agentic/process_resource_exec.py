# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Sealed stdlib-only resource-limit trampoline for supervised local workers.

This file is intentionally executable by absolute path under ``python -I -B``.
It does not import the surrounding package, read stdin, or write stdout.  Its
only job is to validate an exact execution plan, apply inherited per-process
kernel limits, and replace itself with the logical worker command.

The plan and observations provide exact local-byte authority, not
cryptographic authenticity: an attacker able to mutate and restore the Python
interpreter or this file between observations remains outside the claim.
"""

from __future__ import annotations

import base64
import binascii
import hashlib
import json
import math
import os
import platform
import resource
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, NoReturn, Sequence


RESOURCE_EXEC_SCHEMA_VERSION = "2.0.0"
RESOURCE_EXEC_PLAN_KIND = "trusted_local_resource_limit_exec"
RESOURCE_EXEC_DIAGNOSTIC_PREFIX = b"ABDUCER_RESOURCE_EXEC_V1 "
RESOURCE_EXEC_SETUP_FAILURE = 125
RESOURCE_EXEC_CANNOT_EXECUTE = 126
RESOURCE_EXEC_NOT_FOUND = 127
MAX_PLAN_TOKEN_BYTES = 64 * 1024
MAX_DIAGNOSTIC_BYTES = 4096
SHA256_PREFIX = "sha256:"

RESOURCE_EXEC_SCOPE = {
    "address_space": (
        "inherited_per_process_virtual_address_space_not_group_rss"
    ),
    "cpu": "inherited_per_process_integer_second_cpu_limit",
    "file_size": "inherited_per_file_size_limit_not_aggregate_workspace_quota",
    "hard_aggregate_disk_limit": False,
    "hard_group_cpu_limit": False,
    "hard_group_rss_limit": False,
}

_PLAN_KEYS = {
    "schema_version",
    "plan_kind",
    "platform_system",
    "logical_argv_digest",
    "cwd",
    "environment_digest",
    "supervision_environment_digest",
    "declared_limits",
    "kernel_limits",
    "scope",
}
_DECLARED_LIMIT_KEYS = {
    "remaining_cpu_ns",
    "cpu_grace_ns",
    "workspace_disk_bytes",
    "process_memory_bytes",
}
_KERNEL_LIMIT_KEYS = {
    "rlimit_cpu_soft_seconds",
    "rlimit_cpu_hard_seconds",
    "rlimit_fsize_bytes",
    "rlimit_as_bytes",
}


class ResourceExecPlanError(ValueError):
    """Raised when an execution plan or its live binding is invalid."""


def canonical_json_bytes(value: Any) -> bytes:
    """Serialize protocol material into its only accepted JSON form."""

    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return SHA256_PREFIX + hashlib.sha256(value).hexdigest()


def digest_value(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def _require_exact_keys(raw: Mapping[str, Any], expected: set[str], label: str) -> None:
    actual = set(raw)
    if actual != expected:
        raise ResourceExecPlanError(
            f"{label} keys differ: missing={sorted(expected - actual)!r}, "
            f"extra={sorted(actual - expected)!r}"
        )


def _require_int(
    value: object,
    label: str,
    *,
    minimum: int,
) -> int:
    if type(value) is not int or value < minimum:
        raise ResourceExecPlanError(f"{label} must be an integer >= {minimum}")
    return value


def _is_sha256(value: object) -> bool:
    if not isinstance(value, str) or not value.startswith(SHA256_PREFIX):
        return False
    suffix = value[len(SHA256_PREFIX) :]
    return len(suffix) == 64 and all(character in "0123456789abcdef" for character in suffix)


def _validate_protocol_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise ResourceExecPlanError(f"{label} must be a non-empty NUL-free string")
    return value


def _validate_argv(argv: Sequence[str]) -> tuple[str, ...]:
    if isinstance(argv, (str, bytes)) or not argv:
        raise ResourceExecPlanError("logical argv must be a non-empty sequence")
    result = tuple(_validate_protocol_string(value, "logical argv item") for value in argv)
    return result


def _validate_environment(environment: Mapping[str, str]) -> dict[str, str]:
    if not isinstance(environment, Mapping):
        raise ResourceExecPlanError("environment must be a mapping")
    result: dict[str, str] = {}
    for key, value in environment.items():
        if not isinstance(key, str) or not key or "=" in key or "\x00" in key:
            raise ResourceExecPlanError("environment names must be non-empty and exclude '=' and NUL")
        if not isinstance(value, str) or "\x00" in value:
            raise ResourceExecPlanError("environment values must be strings without NUL")
        result[key] = value
    return result


def supervision_environment_digest(environment: Mapping[str, str]) -> str:
    """Return the secret-safe environment identity used by supervision."""

    exact_environment = _validate_environment(environment)
    rows = [
        {
            "name": name,
            "value_sha256": sha256_bytes(value.encode("utf-8")),
        }
        for name, value in sorted(exact_environment.items())
    ]
    return digest_value(rows)


@dataclass(frozen=True, slots=True)
class ResourceExecPlan:
    """Closed, canonical resource-limit execution plan."""

    platform_system: str
    logical_argv_digest: str
    cwd: str
    environment_digest: str
    supervision_environment_digest: str
    remaining_cpu_ns: int
    cpu_grace_ns: int
    workspace_disk_bytes: int
    process_memory_bytes: int
    rlimit_cpu_soft_seconds: int
    rlimit_cpu_hard_seconds: int
    rlimit_fsize_bytes: int
    rlimit_as_bytes: int | None

    def __post_init__(self) -> None:
        if self.platform_system not in {"Darwin", "Linux"}:
            raise ResourceExecPlanError("resource exec supports only Darwin or Linux")
        if not _is_sha256(self.logical_argv_digest):
            raise ResourceExecPlanError("logical argv digest is invalid")
        if not _is_sha256(self.environment_digest):
            raise ResourceExecPlanError("environment digest is invalid")
        if not _is_sha256(self.supervision_environment_digest):
            raise ResourceExecPlanError(
                "supervision environment digest is invalid"
            )
        cwd = Path(_validate_protocol_string(self.cwd, "cwd"))
        if not cwd.is_absolute() or cwd != cwd.resolve(strict=True) or not cwd.is_dir():
            raise ResourceExecPlanError("cwd must be a live canonical absolute directory")
        _require_int(self.remaining_cpu_ns, "remaining_cpu_ns", minimum=1)
        _require_int(self.cpu_grace_ns, "cpu_grace_ns", minimum=0)
        _require_int(self.workspace_disk_bytes, "workspace_disk_bytes", minimum=0)
        _require_int(self.process_memory_bytes, "process_memory_bytes", minimum=1)
        soft = _require_int(
            self.rlimit_cpu_soft_seconds,
            "rlimit_cpu_soft_seconds",
            minimum=1,
        )
        hard = _require_int(
            self.rlimit_cpu_hard_seconds,
            "rlimit_cpu_hard_seconds",
            minimum=2,
        )
        if hard <= soft:
            raise ResourceExecPlanError("CPU hard limit must exceed the soft limit")
        _require_int(self.rlimit_fsize_bytes, "rlimit_fsize_bytes", minimum=0)
        if self.rlimit_fsize_bytes != self.workspace_disk_bytes:
            raise ResourceExecPlanError("file-size limit must equal the declared disk budget")
        expected_soft = max(1, math.ceil(self.remaining_cpu_ns / 1_000_000_000))
        expected_hard = max(
            expected_soft + 1,
            math.ceil((self.remaining_cpu_ns + self.cpu_grace_ns) / 1_000_000_000),
        )
        if soft != expected_soft or hard != expected_hard:
            raise ResourceExecPlanError("CPU kernel limits do not match declared nanosecond limits")
        if self.platform_system == "Darwin":
            if self.rlimit_as_bytes is not None:
                raise ResourceExecPlanError("Darwin plans must not declare RLIMIT_AS")
        elif self.rlimit_as_bytes != self.process_memory_bytes:
            raise ResourceExecPlanError("Linux RLIMIT_AS must equal the declared memory budget")

    @classmethod
    def build(
        cls,
        *,
        logical_argv: Sequence[str],
        cwd: Path | str,
        environment: Mapping[str, str],
        remaining_cpu_ns: int,
        cpu_grace_ns: int,
        workspace_disk_bytes: int,
        process_memory_bytes: int,
        platform_system: str | None = None,
    ) -> "ResourceExecPlan":
        exact_argv = _validate_argv(logical_argv)
        exact_environment = _validate_environment(environment)
        canonical_cwd = Path(cwd).resolve(strict=True)
        if not canonical_cwd.is_dir():
            raise ResourceExecPlanError("cwd must identify a directory")
        system = platform_system or platform.system()
        remaining = _require_int(remaining_cpu_ns, "remaining_cpu_ns", minimum=1)
        grace = _require_int(cpu_grace_ns, "cpu_grace_ns", minimum=0)
        disk = _require_int(workspace_disk_bytes, "workspace_disk_bytes", minimum=0)
        memory = _require_int(process_memory_bytes, "process_memory_bytes", minimum=1)
        soft = max(1, math.ceil(remaining / 1_000_000_000))
        hard = max(soft + 1, math.ceil((remaining + grace) / 1_000_000_000))
        return cls(
            platform_system=system,
            logical_argv_digest=digest_value(list(exact_argv)),
            cwd=str(canonical_cwd),
            environment_digest=digest_value(exact_environment),
            supervision_environment_digest=supervision_environment_digest(
                exact_environment
            ),
            remaining_cpu_ns=remaining,
            cpu_grace_ns=grace,
            workspace_disk_bytes=disk,
            process_memory_bytes=memory,
            rlimit_cpu_soft_seconds=soft,
            rlimit_cpu_hard_seconds=hard,
            rlimit_fsize_bytes=disk,
            rlimit_as_bytes=memory if system == "Linux" else None,
        )

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "ResourceExecPlan":
        if not isinstance(raw, Mapping):
            raise ResourceExecPlanError("resource exec plan must be an object")
        _require_exact_keys(raw, _PLAN_KEYS, "resource exec plan")
        if raw["schema_version"] != RESOURCE_EXEC_SCHEMA_VERSION:
            raise ResourceExecPlanError("resource exec schema version is unsupported")
        if raw["plan_kind"] != RESOURCE_EXEC_PLAN_KIND:
            raise ResourceExecPlanError("resource exec plan kind is unsupported")
        declared = raw["declared_limits"]
        kernel = raw["kernel_limits"]
        scope = raw["scope"]
        if not isinstance(declared, Mapping) or not isinstance(kernel, Mapping):
            raise ResourceExecPlanError("resource exec limit sections must be objects")
        _require_exact_keys(declared, _DECLARED_LIMIT_KEYS, "declared limits")
        _require_exact_keys(kernel, _KERNEL_LIMIT_KEYS, "kernel limits")
        if scope != RESOURCE_EXEC_SCOPE:
            raise ResourceExecPlanError("resource exec scope differs from the closed contract")
        return cls(
            platform_system=raw["platform_system"],
            logical_argv_digest=raw["logical_argv_digest"],
            cwd=raw["cwd"],
            environment_digest=raw["environment_digest"],
            supervision_environment_digest=raw[
                "supervision_environment_digest"
            ],
            remaining_cpu_ns=declared["remaining_cpu_ns"],
            cpu_grace_ns=declared["cpu_grace_ns"],
            workspace_disk_bytes=declared["workspace_disk_bytes"],
            process_memory_bytes=declared["process_memory_bytes"],
            rlimit_cpu_soft_seconds=kernel["rlimit_cpu_soft_seconds"],
            rlimit_cpu_hard_seconds=kernel["rlimit_cpu_hard_seconds"],
            rlimit_fsize_bytes=kernel["rlimit_fsize_bytes"],
            rlimit_as_bytes=kernel["rlimit_as_bytes"],
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": RESOURCE_EXEC_SCHEMA_VERSION,
            "plan_kind": RESOURCE_EXEC_PLAN_KIND,
            "platform_system": self.platform_system,
            "logical_argv_digest": self.logical_argv_digest,
            "cwd": self.cwd,
            "environment_digest": self.environment_digest,
            "supervision_environment_digest": (
                self.supervision_environment_digest
            ),
            "declared_limits": {
                "remaining_cpu_ns": self.remaining_cpu_ns,
                "cpu_grace_ns": self.cpu_grace_ns,
                "workspace_disk_bytes": self.workspace_disk_bytes,
                "process_memory_bytes": self.process_memory_bytes,
            },
            "kernel_limits": {
                "rlimit_cpu_soft_seconds": self.rlimit_cpu_soft_seconds,
                "rlimit_cpu_hard_seconds": self.rlimit_cpu_hard_seconds,
                "rlimit_fsize_bytes": self.rlimit_fsize_bytes,
                "rlimit_as_bytes": self.rlimit_as_bytes,
            },
            "scope": dict(RESOURCE_EXEC_SCOPE),
        }

    def canonical_bytes(self) -> bytes:
        return canonical_json_bytes(self.as_dict())

    def digest(self) -> str:
        return sha256_bytes(self.canonical_bytes())

    def base64_token(self) -> str:
        return base64.b64encode(self.canonical_bytes()).decode("ascii")


def decode_plan_token(token: str) -> ResourceExecPlan:
    """Decode the only accepted standard-Base64/canonical-JSON plan form."""

    if not isinstance(token, str) or not token or len(token.encode("ascii", errors="ignore")) != len(token):
        raise ResourceExecPlanError("plan token must be non-empty ASCII")
    if len(token) > MAX_PLAN_TOKEN_BYTES:
        raise ResourceExecPlanError("plan token exceeds its fixed byte ceiling")
    try:
        encoded = token.encode("ascii")
        decoded = base64.b64decode(encoded, validate=True)
    except (UnicodeEncodeError, binascii.Error) as exc:
        raise ResourceExecPlanError("plan token is not validating standard Base64") from exc
    if base64.b64encode(decoded) != encoded:
        raise ResourceExecPlanError("plan token is not in canonical Base64 form")
    try:
        raw = json.loads(decoded.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ResourceExecPlanError("plan token does not contain UTF-8 JSON") from exc
    if canonical_json_bytes(raw) != decoded:
        raise ResourceExecPlanError("plan JSON is not canonical")
    return ResourceExecPlan.from_mapping(raw)


def validate_live_binding(
    plan: ResourceExecPlan,
    *,
    logical_argv: Sequence[str],
    cwd: Path | str,
    environment: Mapping[str, str],
    platform_system: str | None = None,
) -> tuple[tuple[str, ...], dict[str, str]]:
    """Validate the plan against the exact live exec inputs."""

    exact_argv = _validate_argv(logical_argv)
    exact_environment = _validate_environment(environment)
    exact_cwd = Path(cwd).resolve(strict=True)
    if str(exact_cwd) != plan.cwd:
        raise ResourceExecPlanError("live cwd differs from the resource exec plan")
    if digest_value(list(exact_argv)) != plan.logical_argv_digest:
        raise ResourceExecPlanError("live logical argv differs from the resource exec plan")
    if digest_value(exact_environment) != plan.environment_digest:
        raise ResourceExecPlanError("live environment differs from the resource exec plan")
    if (
        supervision_environment_digest(exact_environment)
        != plan.supervision_environment_digest
    ):
        raise ResourceExecPlanError(
            "live supervision environment differs from the resource exec plan"
        )
    if (platform_system or platform.system()) != plan.platform_system:
        raise ResourceExecPlanError("live platform differs from the resource exec plan")
    return exact_argv, exact_environment


def apply_kernel_limits(plan: ResourceExecPlan) -> None:
    """Apply the plan's accurately scoped inherited kernel limits."""

    resource.setrlimit(
        resource.RLIMIT_CPU,
        (plan.rlimit_cpu_soft_seconds, plan.rlimit_cpu_hard_seconds),
    )
    resource.setrlimit(
        resource.RLIMIT_FSIZE,
        (plan.rlimit_fsize_bytes, plan.rlimit_fsize_bytes),
    )
    if plan.platform_system == "Linux":
        if not hasattr(resource, "RLIMIT_AS") or plan.rlimit_as_bytes is None:
            raise ResourceExecPlanError("Linux RLIMIT_AS is unavailable")
        resource.setrlimit(
            resource.RLIMIT_AS,
            (plan.rlimit_as_bytes, plan.rlimit_as_bytes),
        )


def _write_failure(reason: str, exc: BaseException) -> None:
    payload = {
        "exception_type": type(exc).__name__,
        "message": str(exc)[:512],
        "reason": reason,
    }
    rendered = RESOURCE_EXEC_DIAGNOSTIC_PREFIX + canonical_json_bytes(payload) + b"\n"
    try:
        os.write(2, rendered[:MAX_DIAGNOSTIC_BYTES])
    except OSError:
        pass


def _fail(reason: str, exc: BaseException, exit_code: int) -> NoReturn:
    _write_failure(reason, exc)
    raise SystemExit(exit_code)


def _parse_transport_argv(argv: Sequence[str]) -> tuple[str, tuple[str, ...]]:
    if len(argv) < 4 or argv[0] != "--resource-plan-base64" or argv[2] != "--":
        raise ResourceExecPlanError(
            "argv must be --resource-plan-base64 TOKEN -- LOGICAL_ARGV..."
        )
    token = argv[1]
    logical_argv = _validate_argv(argv[3:])
    return token, logical_argv


def main(argv: Sequence[str] | None = None) -> NoReturn:
    """Validate, limit, and replace this process with the logical worker."""

    try:
        token, logical_argv = _parse_transport_argv(tuple(sys.argv[1:] if argv is None else argv))
        plan = decode_plan_token(token)
        live_environment = dict(os.environ)
        exact_argv, exact_environment = validate_live_binding(
            plan,
            logical_argv=logical_argv,
            cwd=Path.cwd(),
            environment=live_environment,
        )
        apply_kernel_limits(plan)
    except BaseException as exc:
        if isinstance(exc, (KeyboardInterrupt, SystemExit)):
            raise
        _fail("setup_failed", exc, RESOURCE_EXEC_SETUP_FAILURE)

    try:
        os.execvpe(exact_argv[0], list(exact_argv), exact_environment)
    except FileNotFoundError as exc:
        _fail("executable_not_found", exc, RESOURCE_EXEC_NOT_FOUND)
    except (PermissionError, IsADirectoryError) as exc:
        _fail("executable_not_executable", exc, RESOURCE_EXEC_CANNOT_EXECUTE)
    except OSError as exc:
        _fail("exec_failed", exc, RESOURCE_EXEC_CANNOT_EXECUTE)


if __name__ == "__main__":
    main()
