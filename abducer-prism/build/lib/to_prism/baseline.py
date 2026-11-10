"""Native baseline descriptors; discovery never executes candidates."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from . import __version__
from .model import SCHEMA_VERSION
from .safety import redact_text


def discover_baseline_candidates(source: Path) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    package_json = source / "package.json"
    if package_json.is_file() and not package_json.is_symlink():
        try:
            parsed = json.loads(package_json.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            parsed = {}
        scripts = parsed.get("scripts", {}) if isinstance(parsed, dict) else {}
        if isinstance(scripts, dict):
            for name in ("test", "check"):
                if isinstance(scripts.get(name), str):
                    candidates.append(
                        {
                            "command": ["npm", "run", name],
                            "evidence": {
                                "kind": "package-script",
                                "location": "package.json",
                            },
                            "requires_approval": True,
                        }
                    )
    if (source / "pyproject.toml").is_file() or (source / "pytest.ini").is_file():
        candidates.append(
            {
                "command": ["python", "-m", "pytest"],
                "evidence": {"kind": "python-test-config", "location": "."},
                "requires_approval": True,
            }
        )
    if (source / "Makefile").is_file():
        candidates.append(
            {
                "command": ["make", "test"],
                "evidence": {"kind": "make-target-candidate", "location": "Makefile"},
                "requires_approval": True,
            }
        )
    candidates.sort(key=lambda item: item["command"])
    return candidates


def build_baseline_descriptor(source: Path, source_fingerprint: str) -> dict[str, Any]:
    return {
        "artifact": "baseline",
        "candidates": discover_baseline_candidates(source),
        "execution": {
            "authorized": False,
            "classification": "unavailable",
            "reason": "candidate commands require explicit review and authorization",
        },
        "schema_version": SCHEMA_VERSION,
        "source_fingerprint": source_fingerprint,
        "tool": {"name": "to-prism", "version": __version__},
    }


def _validate_isolatable_symlinks(source: Path) -> None:
    for path in source.rglob("*"):
        if not path.is_symlink():
            continue
        raw = os.readlink(path)
        if Path(raw).is_absolute():
            raise ValueError(
                f"baseline cannot isolate absolute symlink: {path.relative_to(source)}"
            )
        target = path.resolve(strict=False)
        if target != source and source not in target.parents:
            raise ValueError(
                f"baseline symlink escapes source: {path.relative_to(source)}"
            )


def _bounded_redacted(value: str, workspace: Path, limit: int) -> str:
    normalized = value.replace(str(workspace), "<workspace>")
    normalized = redact_text(normalized)
    if len(normalized.encode("utf-8")) <= limit:
        return normalized
    encoded = normalized.encode("utf-8")[:limit]
    return encoded.decode("utf-8", errors="replace") + "\n<output-truncated>"


def execute_baseline(
    *,
    source: Path,
    source_fingerprint: str,
    command: list[str],
    timeout_seconds: float = 60.0,
    attempts: int = 1,
    output_limit: int = 64 * 1024,
    network_policy: str = "deny",
    environment: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Run an explicitly approved argv in disposable copied workspaces.

    Stdlib alone cannot impose a portable network namespace.  Consequently
    execution is rejected for ``deny`` rather than claiming unenforced
    isolation; callers must explicitly approve ``inherit``.
    """

    if not command or not all(isinstance(part, str) and part for part in command):
        raise ValueError("baseline command must be a non-empty argv array")
    if attempts < 1 or attempts > 3:
        raise ValueError("baseline attempts must be between 1 and 3")
    if timeout_seconds <= 0 or timeout_seconds > 600:
        raise ValueError("baseline timeout must be in (0, 600] seconds")
    if output_limit < 1024 or output_limit > 1024 * 1024:
        raise ValueError("baseline output limit must be between 1 KiB and 1 MiB")
    if network_policy not in {"deny", "inherit"}:
        raise ValueError("network policy must be deny or inherit")
    if network_policy == "deny":
        raise ValueError(
            "network=deny is not executable without an OS sandbox; explicitly authorize network=inherit or use an external sandbox"
        )
    _validate_isolatable_symlinks(source)
    records: list[dict[str, Any]] = []
    for attempt in range(1, attempts + 1):
        with tempfile.TemporaryDirectory(prefix="to-prism-baseline-") as temporary:
            temporary_root = Path(temporary)
            workspace = temporary_root / "workspace"
            shutil.copytree(
                source, workspace, symlinks=True, copy_function=shutil.copy2
            )
            home = temporary_root / "home"
            home.mkdir()
            clean_environment = {
                "HOME": str(home),
                "LANG": os.environ.get("LANG", "C.UTF-8"),
                "LC_ALL": os.environ.get("LC_ALL", "C.UTF-8"),
                "PATH": os.environ.get("PATH", ""),
                "TO_PRISM_BASELINE": "1",
            }
            for key, value in sorted((environment or {}).items()):
                if (
                    not key
                    or "SECRET" in key.upper()
                    or "TOKEN" in key.upper()
                    or "PASSWORD" in key.upper()
                ):
                    raise ValueError(
                        f"credential-shaped baseline environment binding rejected: {key!r}"
                    )
                clean_environment[key] = value
            try:
                completed = subprocess.run(
                    command,
                    cwd=workspace,
                    env=clean_environment,
                    text=True,
                    capture_output=True,
                    timeout=timeout_seconds,
                    check=False,
                )
                record = {
                    "attempt": attempt,
                    "exit_code": completed.returncode,
                    "stderr": _bounded_redacted(
                        completed.stderr, workspace, output_limit
                    ),
                    "stdout": _bounded_redacted(
                        completed.stdout, workspace, output_limit
                    ),
                    "timed_out": False,
                }
            except subprocess.TimeoutExpired as exc:
                stdout = (
                    exc.stdout.decode()
                    if isinstance(exc.stdout, bytes)
                    else (exc.stdout or "")
                )
                stderr = (
                    exc.stderr.decode()
                    if isinstance(exc.stderr, bytes)
                    else (exc.stderr or "")
                )
                record = {
                    "attempt": attempt,
                    "exit_code": None,
                    "stderr": _bounded_redacted(stderr, workspace, output_limit),
                    "stdout": _bounded_redacted(stdout, workspace, output_limit),
                    "timed_out": True,
                }
            records.append(record)
    signatures = {
        (record["exit_code"], record["stdout"], record["stderr"], record["timed_out"])
        for record in records
    }
    successes = sum(
        record["exit_code"] == 0 and not record["timed_out"] for record in records
    )
    if len(signatures) == 1 and successes == attempts:
        classification = "reproducible"
    elif successes == attempts:
        classification = "nondeterministic"
    elif 0 < successes < attempts:
        classification = "flaky"
    else:
        classification = "failed"
    return {
        "artifact": "baseline",
        "candidates": [],
        "execution": {
            "attempts": records,
            "authorized": True,
            "classification": classification,
            "command": command,
            "filesystem_policy": "disposable-copy",
            "network_policy": network_policy,
            "output_limit_bytes": output_limit,
            "timeout_seconds": timeout_seconds,
        },
        "schema_version": SCHEMA_VERSION,
        "source_fingerprint": source_fingerprint,
        "tool": {"name": "to-prism", "version": __version__},
    }
