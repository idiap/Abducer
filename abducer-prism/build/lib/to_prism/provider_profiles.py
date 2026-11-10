"""Load and query the versioned provider facts shipped with ``to_prism``.

Profile files use the JSON subset of YAML.  That keeps the conversion kit
self-contained: loading provider facts does not require PyYAML and never
executes configuration from the inspected project.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from fnmatch import fnmatchcase
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping

PROFILE_SCHEMA_VERSION = 1
SUPPORTED_PROVIDERS = frozenset({"codex", "claude", "opencode", "open-agent-skill"})


class ProviderProfileError(ValueError):
    """A bundled provider profile is malformed or unsupported."""


@dataclass(frozen=True, slots=True)
class ArtifactMatch:
    """One profile rule that recognizes a source-relative path."""

    provider: str
    profile_version: str
    rule_id: str
    kind: str
    relative_path: str
    priority: int


def default_profiles_directory() -> Path:
    """Return the profile directory without relying on the process cwd."""

    development = Path(__file__).resolve().parents[2] / "profiles"
    if development.is_dir():
        return development
    installed = Path(sys.prefix) / "share" / "to-prism" / "profiles"
    if installed.is_dir():
        return installed
    raise ProviderProfileError("to-prism provider profiles are not installed")


def load_profile(
    provider: str, profiles_directory: Path | None = None
) -> dict[str, Any]:
    """Load and validate one bundled JSON-compatible YAML profile."""

    if provider not in SUPPORTED_PROVIDERS:
        raise ProviderProfileError(f"unknown provider profile: {provider}")
    directory = profiles_directory or default_profiles_directory()
    path = directory / f"{provider}.yaml"
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ProviderProfileError(f"provider profile is missing: {provider}") from exc
    except json.JSONDecodeError as exc:
        raise ProviderProfileError(
            f"provider profile {provider} is not JSON-compatible YAML: {exc.msg}"
        ) from exc
    _validate_profile(raw, expected_provider=provider)
    from .schemas import require_valid

    require_valid(raw, "provider-profile")
    return raw


def load_profiles(
    providers: Iterable[str] | None = None,
    profiles_directory: Path | None = None,
) -> tuple[dict[str, Any], ...]:
    """Load profiles in deterministic provider-name order."""

    names = sorted(set(providers or SUPPORTED_PROVIDERS))
    return tuple(load_profile(name, profiles_directory) for name in names)


def classify_path(
    relative_path: str | PurePosixPath,
    profiles: Iterable[Mapping[str, Any]],
) -> tuple[ArtifactMatch, ...]:
    """Return every matching artifact rule, highest priority first.

    Multiple matches are intentional.  For example, ``.claude/skills`` is a
    native Claude layout and a compatibility layout understood by OpenCode.
    The inventory layer must retain that ownership ambiguity rather than
    silently selecting one vendor.
    """

    normalized = _normalized_relative_path(relative_path)
    matches: list[ArtifactMatch] = []
    for profile in profiles:
        provider = str(profile["provider"])
        version = str(profile["profile_version"])
        for rule in profile["artifact_rules"]:
            if any(_glob_matches(normalized, glob) for glob in rule["globs"]):
                matches.append(
                    ArtifactMatch(
                        provider=provider,
                        profile_version=version,
                        rule_id=str(rule["id"]),
                        kind=str(rule["kind"]),
                        relative_path=normalized,
                        priority=int(rule["priority"]),
                    )
                )
    return tuple(
        sorted(
            matches,
            key=lambda item: (-item.priority, item.provider, item.rule_id),
        )
    )


def hook_event(profile: Mapping[str, Any], event_name: str) -> Mapping[str, Any] | None:
    """Return an exact hook event contract; unknown names never fuzzy-match."""

    event = profile["hooks"]["events"].get(event_name)
    return event if isinstance(event, Mapping) else None


def hook_handler_status(profile: Mapping[str, Any], handler_type: str) -> str | None:
    """Return the provider's declared status for an exact handler type."""

    handler = profile["hooks"]["handler_types"].get(handler_type)
    if not isinstance(handler, Mapping):
        return None
    status = handler.get("status")
    return status if isinstance(status, str) else None


def _validate_profile(value: object, *, expected_provider: str) -> None:
    if not isinstance(value, dict):
        raise ProviderProfileError("provider profile root must be an object")
    required = {
        "schema_version",
        "provider",
        "profile_version",
        "retrieved_at",
        "sources",
        "project_markers",
        "artifact_rules",
        "hooks",
        "limitations",
    }
    missing = sorted(required - value.keys())
    if missing:
        raise ProviderProfileError(
            f"provider profile missing fields: {', '.join(missing)}"
        )
    if value["schema_version"] != PROFILE_SCHEMA_VERSION:
        raise ProviderProfileError(
            f"unsupported provider profile schema: {value['schema_version']}"
        )
    if value["provider"] != expected_provider:
        raise ProviderProfileError(
            f"provider profile identity mismatch: expected {expected_provider}"
        )
    if not isinstance(value["profile_version"], str) or not value["profile_version"]:
        raise ProviderProfileError("profile_version must be a non-empty string")
    if not isinstance(value["sources"], list) or not value["sources"]:
        raise ProviderProfileError("provider profile must cite at least one source")
    for source in value["sources"]:
        if not isinstance(source, dict) or not all(
            isinstance(source.get(field), str) and source[field]
            for field in ("title", "url")
        ):
            raise ProviderProfileError("profile sources require title and url")
    if not isinstance(value["artifact_rules"], list):
        raise ProviderProfileError("artifact_rules must be an array")
    rule_ids: set[str] = set()
    for rule in value["artifact_rules"]:
        if not isinstance(rule, dict):
            raise ProviderProfileError("artifact rule must be an object")
        if set(("id", "kind", "globs", "priority")) - rule.keys():
            raise ProviderProfileError(
                "artifact rule lacks id, kind, globs, or priority"
            )
        if rule["id"] in rule_ids:
            raise ProviderProfileError(f"duplicate artifact rule: {rule['id']}")
        rule_ids.add(rule["id"])
        if (
            not isinstance(rule["globs"], list)
            or not rule["globs"]
            or not all(isinstance(glob, str) and glob for glob in rule["globs"])
        ):
            raise ProviderProfileError(f"artifact rule {rule['id']} has invalid globs")
        if not isinstance(rule["priority"], int):
            raise ProviderProfileError(
                f"artifact rule {rule['id']} priority must be integer"
            )
    hooks = value["hooks"]
    if not isinstance(hooks, dict):
        raise ProviderProfileError("hooks must be an object")
    if (
        set(
            (
                "contract",
                "configuration_globs",
                "events",
                "handler_types",
                "unknown_event",
            )
        )
        - hooks.keys()
    ):
        raise ProviderProfileError("hooks contract is incomplete")
    if hooks["unknown_event"] not in {"unsupported", "opaque_executable"}:
        raise ProviderProfileError("unknown hook events must fail closed")
    if not isinstance(hooks["events"], dict) or not isinstance(
        hooks["handler_types"], dict
    ):
        raise ProviderProfileError("hook events and handler types must be objects")


def _normalized_relative_path(path: str | PurePosixPath) -> str:
    raw = str(path).replace("\\", "/")
    parsed = PurePosixPath(raw)
    if parsed.is_absolute() or raw in {"", "."} or ".." in parsed.parts:
        raise ProviderProfileError(f"path must be canonical and source-relative: {raw}")
    return parsed.as_posix()


def _glob_matches(path: str, pattern: str) -> bool:
    # fnmatch treats ``**`` as recursive, but ``**/name`` does not match a
    # root-level ``name``.  Profiles use both semantics deliberately.
    return fnmatchcase(path, pattern) or (
        pattern.startswith("**/") and fnmatchcase(path, pattern[3:])
    )


__all__ = [
    "ArtifactMatch",
    "PROFILE_SCHEMA_VERSION",
    "ProviderProfileError",
    "SUPPORTED_PROVIDERS",
    "classify_path",
    "default_profiles_directory",
    "hook_event",
    "hook_handler_status",
    "load_profile",
    "load_profiles",
]
