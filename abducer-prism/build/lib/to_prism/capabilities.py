"""Public-CLI capability probing and conservative runtime support matrix."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

CAPABILITY_MATRIX: dict[str, dict[str, str]] = {
    "canonical-prism": {"syntax": "supported", "cli": "check/compile/run"},
    "ai-generate-fake": {"syntax": "supported", "cli": "fake-handler"},
    "ai-generate-codex": {"syntax": "supported", "cli": "codex-handler"},
    "ai-generate-litellm": {"syntax": "supported", "cli": "litellm-handler"},
    "python-call": {"syntax": "supported", "cli": "installed-entry-point"},
    "codex-hooks": {"syntax": "typed", "cli": "codex-only-limited-cwd"},
    "claude-hooks": {"syntax": "typed", "cli": "no-runtime-handler"},
    "opencode-hooks": {"syntax": "unsupported", "cli": "unsupported"},
    "dynamic-agent-tools": {"syntax": "metadata-only", "cli": "unsupported"},
    "process-run": {"syntax": "effect-contract-only", "cli": "unsupported"},
    "network-request": {"syntax": "effect-contract-only", "cli": "unsupported"},
    "mcp-call": {"syntax": "effect-contract-only", "cli": "unsupported"},
    "typed-domain-input": {"syntax": "parameter", "cli": "fixture-harness-only"},
}


def probe_prism(executable: str) -> dict[str, Any]:
    path = Path(shutil.which(executable) or executable).resolve()
    if not path.is_file():
        raise ValueError(f"Prism executable does not exist: {path}")
    completed = subprocess.run(
        [str(path), "--help"], text=True, capture_output=True, check=False
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr.strip() or "Prism capability probe failed")
    commands = [
        command
        for command in ("parse", "check", "compile", "run", "verify-run", "build")
        if command in completed.stdout
    ]
    required = {"parse", "check", "compile", "run", "verify-run", "build"}
    if set(commands) != required:
        raise RuntimeError(
            f"incompatible Prism CLI; missing {sorted(required - set(commands))}"
        )
    return {
        "schema_version": 1,
        "executable_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "commands": commands,
        "matrix": CAPABILITY_MATRIX,
        "version_status": "provisional-executable-digest-and-probes",
    }


def write_capability_probe(executable: str, output: Path) -> dict[str, Any]:
    payload = probe_prism(executable)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return payload


__all__ = ["CAPABILITY_MATRIX", "probe_prism", "write_capability_probe"]
