"""Fail-closed provider frontend normalization for converter guard hooks."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

from .paths import ConversionPaths, PathSafetyError, canonical_path, is_within

EVENTS = {
    "codex": {"PreToolUse", "PermissionRequest", "PostToolUse", "Stop"},
    "claude": {"PreToolUse", "PermissionRequest", "PostToolUse", "Stop"},
    "opencode": {"tool.execute.before", "tool.execute.after", "session.idle"},
}
PRE_EVENTS = {"PreToolUse", "PermissionRequest", "tool.execute.before"}
STOP_EVENTS = {"Stop", "session.idle"}
_PATH_KEY = re.compile(
    r"(?i)((^|_)(file|path|directory|cwd|target|destination)(_|$)|^(filePath|directoryPath)$)"
)
_COMMAND_KEY = re.compile(r"(?i)(^|_)(command|cmd|shell)(_|$)")
_SECRET_PATH = re.compile(
    r"(?i)(^|/)(\.env($|\.)|id_(rsa|dsa|ecdsa|ed25519)$|credentials?|secrets?|.*\.(pem|p12|pfx|key)$)"
)


class GuardRejection(PermissionError):
    pass


def normalize_request(provider: str, event: str, payload: Any) -> dict[str, Any]:
    if provider not in EVENTS or event not in EVENTS[provider]:
        raise GuardRejection("unknown provider or lifecycle event")
    if not isinstance(payload, dict):
        raise GuardRejection("guard payload must be one JSON object")
    if provider == "opencode":
        if event.startswith("tool.") and not isinstance(payload.get("input"), dict):
            raise GuardRejection("OpenCode tool callback requires an input object")
        if event == "session.idle" and "event" not in payload:
            raise GuardRejection("OpenCode session.idle requires an event payload")
    return {
        "event": event,
        "payload": payload,
        "protocol_version": 1,
        "provider": provider,
    }


def _strings_by_key(value: Any, matcher: re.Pattern[str]) -> list[str]:
    result: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if matcher.search(str(key)):
                if isinstance(item, str):
                    result.append(item)
                elif isinstance(item, list):
                    result.extend(part for part in item if isinstance(part, str))
            result.extend(_strings_by_key(item, matcher))
    elif isinstance(value, list):
        for item in value:
            result.extend(_strings_by_key(item, matcher))
    return result


def _requested_paths(value: Any) -> list[str]:
    result: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            normalized_key = str(key).lower()
            if _PATH_KEY.search(str(key)) and isinstance(item, str):
                result.append(item)
            elif normalized_key in {"patchtext", "patch_text"} and isinstance(
                item, str
            ):
                for line in item.splitlines():
                    match = re.match(
                        r"^(?:\*\*\* (?:Add|Update|Delete) File:|---|\+\+\+)\s+(?:[ab]/)?(.+?)\s*$",
                        line,
                    )
                    if match and match.group(1) != "/dev/null":
                        result.append(match.group(1))
            result.extend(_requested_paths(item))
    elif isinstance(value, list):
        for item in value:
            result.extend(_requested_paths(item))
    return result


def _tool_name(payload: dict[str, Any]) -> str:
    for key in ("tool_name", "tool", "name"):
        value = payload.get(key)
        if isinstance(value, str):
            return value.lower()
    nested = payload.get("input")
    return _tool_name(nested) if isinstance(nested, dict) else ""


def _looks_like_write(tool_name: str) -> bool:
    return any(
        word in tool_name for word in ("write", "edit", "patch", "delete", "move")
    )


def _looks_like_execute(tool_name: str) -> bool:
    return any(
        word in tool_name
        for word in ("exec", "shell", "bash", "terminal", "command", "run", "process")
    )


def _resolved_candidate(raw: str, source: Path, payload: dict[str, Any]) -> Path:
    candidate = Path(raw).expanduser()
    if candidate.is_absolute():
        return canonical_path(candidate)
    cwd_value = payload.get("cwd")
    cwd = canonical_path(cwd_value) if isinstance(cwd_value, str) else source
    return canonical_path(cwd / candidate)


def _completion_artifacts_present(output: Path) -> bool:
    required = (
        "conversion/inventory.json",
        "conversion/contracts.json",
        "conversion/workflow.json",
        "conversion/report.md",
    )
    return all((output / relative).is_file() for relative in required)


def evaluate_request(
    request: dict[str, Any],
    *,
    source_root: str | os.PathLike[str] | None,
    output_root: str | os.PathLike[str] | None,
    phase: str | None,
) -> dict[str, Any]:
    if not source_root or not output_root or not phase:
        raise GuardRejection("guard context is incomplete")
    try:
        paths = ConversionPaths.resolve(source_root, output_root)
    except PathSafetyError as exc:
        raise GuardRejection(str(exc)) from exc
    event = request["event"]
    payload = request["payload"]
    tool_name = _tool_name(payload)
    paths_found = _requested_paths(payload)
    commands = _strings_by_key(payload, _COMMAND_KEY)
    if event in PRE_EVENTS:
        if phase in {"inspect", "discovery", "model"} and (
            commands or _looks_like_execute(tool_name)
        ):
            raise GuardRejection(f"execution is not authorized during {phase}")
        if _looks_like_write(tool_name) and not paths_found:
            raise GuardRejection(
                "write-like tool request has no inspectable target path"
            )
        for raw in paths_found:
            normalized = raw.replace("\\", "/")
            if _SECRET_PATH.search(normalized):
                raise GuardRejection("credential-shaped path is protected")
            try:
                candidate = _resolved_candidate(raw, paths.source, payload)
            except (OSError, RuntimeError, PathSafetyError) as exc:
                raise GuardRejection("cannot safely resolve requested path") from exc
            if _looks_like_write(tool_name) and is_within(candidate, paths.source):
                raise GuardRejection(
                    "write target resolves inside protected source root"
                )
    if event in STOP_EVENTS and phase in {"generate", "verify", "publish", "convert"}:
        if not _completion_artifacts_present(paths.output):
            raise GuardRejection("conversion completion artifacts are incomplete")
    return {
        "allowed": True,
        "event": event,
        "protocol_version": 1,
        "provider": request["provider"],
    }


def evaluate_from_environment(
    provider: str, event: str, payload: Any
) -> dict[str, Any]:
    request = normalize_request(provider, event, payload)
    return evaluate_request(
        request,
        source_root=os.environ.get("TO_PRISM_SOURCE_ROOT"),
        output_root=os.environ.get("TO_PRISM_OUTPUT_ROOT"),
        phase=os.environ.get("TO_PRISM_PHASE"),
    )
