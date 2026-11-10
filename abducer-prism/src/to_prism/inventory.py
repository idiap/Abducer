# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Non-executing, provider-neutral project inventory."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tomllib
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from . import __version__
from .fingerprint import DEFAULT_IGNORE_RULES, IgnoreRule, fingerprint_tree
from .jsonio import canonical_bytes
from .paths import canonical_path
from .provider_profiles import (
    ArtifactMatch,
    classify_path,
    hook_event,
    hook_handler_status,
    load_profiles,
)

INVENTORY_SCHEMA_VERSION = "1.0"
DISPOSITIONS = {"convert", "wrap", "copy", "exclude", "unsupported", "unresolved"}

_SCRIPT_EXTENSIONS = {
    ".bash",
    ".cmd",
    ".fish",
    ".js",
    ".mjs",
    ".ps1",
    ".py",
    ".rb",
    ".sh",
    ".ts",
}
_CONFIG_EXTENSIONS = {".json", ".toml", ".yaml", ".yml"}
_SECRET_NAMES = re.compile(
    r"(?i)(^|/)(\.env($|\.)|id_(rsa|dsa|ecdsa|ed25519)$|credentials?\.|secrets?\.|.*\.(pem|p12|pfx|key)$)"
)
_SECRET_CONTENT = re.compile(
    rb"(?i)(-----BEGIN [A-Z ]*PRIVATE KEY-----|(?:api[_-]?key|token|password|secret)\s*[:=]\s*[^\s]{8,})"
)
_ENV_REFERENCE = re.compile(
    r"(?:os\.(?:environ|getenv)\s*\(?\s*['\"]([A-Z][A-Z0-9_]*)|\$\{?([A-Z][A-Z0-9_]*)\}?)"
)


def stable_item_id(provider: str, relative_path: str, identity: str = "file") -> str:
    payload = f"{provider}\0{relative_path}\0{identity}".encode("utf-8")
    return "item_" + hashlib.sha256(payload).hexdigest()[:24]


def iter_inventory_items(inventory: dict[str, Any]):
    """Yield file records followed by their semantic child records."""

    for item in inventory.get("items", []):
        yield item
        yield from item.get("semantic_elements", [])


def _provider_for(path: str) -> str:
    parts = {part.lower() for part in PurePosixPath(path).parts}
    if ".codex" in parts or "codex" in parts:
        return "codex"
    if ".claude" in parts or "claude" in parts:
        return "claude"
    if ".opencode" in parts or "opencode" in parts:
        return "opencode"
    if PurePosixPath(path).name == "SKILL.md":
        return "open-agent-skill"
    return "generic"


def _profile_kind(kind: str, fallback: str) -> str:
    return {
        "agent": "agent",
        "command": "command",
        "configuration": "configuration",
        "executable_plugin": "script",
        "executable_tool": "tool",
        "hook_configuration": "hook_group",
        "instructions": "reference",
        "mcp_configuration": "mcp_capability",
        "permission_rule": "configuration",
        "plugin_manifest": "configuration",
        "skill": "skill",
        "skill_resource": fallback,
    }.get(kind, fallback)


def _kind_for(path: str, executable: bool) -> str:
    pure = PurePosixPath(path)
    name = pure.name.lower()
    parts = {part.lower() for part in pure.parts}
    if pure.name == "SKILL.md":
        return "skill"
    if name in {"hooks.json", "settings.json", "settings.local.json"} and (
        ".codex" in parts or ".claude" in parts or ".opencode" in parts
    ):
        return "hook_group" if name == "hooks.json" else "configuration"
    if name in {"agents.md", "claude.md"} or "agents" in parts:
        return "agent"
    if "commands" in parts:
        return "command"
    if "tools" in parts:
        return "tool"
    if "scripts" in parts or executable or pure.suffix.lower() in _SCRIPT_EXTENSIONS:
        return "script"
    if "test" in name or "tests" in parts or "spec" in name:
        return "test"
    if "mcp" in name:
        return "mcp_capability"
    if name in {"main.py", "__main__.py", "main.js", "main.ts"}:
        return "entry_point"
    if pure.suffix.lower() in _CONFIG_EXTENSIONS:
        return "configuration"
    if pure.suffix.lower() in {".md", ".mdx", ".rst", ".txt"}:
        return "reference"
    return "asset"


def _frontmatter(data: bytes) -> dict[str, str]:
    """Extract scalar frontmatter safely; this is not a general YAML parser."""

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return {}
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    result: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if not line or line[:1].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key in {"name", "description"}:
            result[key] = value.strip().strip("'\"")
    return result


def _metadata(path: Path, kind: str, data: bytes) -> dict[str, Any]:
    if kind == "skill":
        return _frontmatter(data)
    if kind in {"configuration", "hook_group"} and path.suffix.lower() in {
        ".json",
        ".toml",
    }:
        parsed = _parse_configuration(path, data)
        if parsed is None:
            return {"parse_status": "malformed"}
        if isinstance(parsed, dict):
            return {
                "parse_status": "parsed",
                "top_level_keys": sorted(str(key) for key in parsed),
            }
    return {}


def _parse_configuration(path: Path, data: bytes) -> Any:
    try:
        if path.suffix.lower() == ".json":
            return json.loads(data)
        if path.suffix.lower() == ".toml":
            return tomllib.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError, tomllib.TOMLDecodeError):
        return None
    return None


def _environment_names(data: bytes) -> list[str]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return []
    return sorted({left or right for left, right in _ENV_REFERENCE.findall(text)})


def _json_environment_names(value: Any) -> list[str]:
    names: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key).lower() in {"env", "environment"} and isinstance(item, dict):
                names.update(str(name) for name in item if str(name))
            names.update(_json_environment_names(item))
    elif isinstance(value, list):
        for item in value:
            names.update(_json_environment_names(item))
    return sorted(names)


def _json_permissions(value: Any) -> list[str]:
    if not isinstance(value, dict) or not isinstance(
        value.get("permissions") or value.get("permission"), dict
    ):
        return []
    permissions = value.get("permissions") or value.get("permission")
    result: set[str] = set()
    for policy, declaration in permissions.items():
        if isinstance(declaration, list):
            result.update(
                f"{policy}:{name}" for name in declaration if isinstance(name, str)
            )
        elif isinstance(declaration, str):
            result.add(f"{policy}:{declaration}")
        elif isinstance(declaration, dict):
            result.update(
                f"{policy}:{name}:{decision}"
                for name, decision in declaration.items()
                if isinstance(decision, str)
            )
    return sorted(result)


def _semantic_config_records(
    *,
    item: dict[str, Any],
    parsed: Any,
    profile: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    if not isinstance(parsed, dict):
        return []
    records: list[dict[str, Any]] = []
    hooks = parsed.get("hooks")
    if isinstance(hooks, dict):
        for event_name in sorted(hooks):
            groups = hooks[event_name]
            if not isinstance(groups, list):
                continue
            known_event = (
                hook_event(profile, event_name) if profile is not None else None
            )
            for group_index, group in enumerate(groups):
                if not isinstance(group, dict) or not isinstance(
                    group.get("hooks"), list
                ):
                    continue
                for handler_index, handler in enumerate(group["hooks"]):
                    if not isinstance(handler, dict):
                        continue
                    handler_type = str(handler.get("type", "unknown"))
                    native_status = (
                        hook_handler_status(profile, handler_type)
                        if profile is not None
                        else None
                    )
                    identity = f"hook:{event_name}:{group_index}:{handler_index}:{handler_type}"
                    record = {
                        "confidence": "explicit",
                        "dependencies": [item["id"]],
                        "disposition": (
                            "unresolved"
                            if known_event is not None and native_status is not None
                            else "unsupported"
                        ),
                        "entry_type": "file",
                        "environment_names": list(item["environment_names"]),
                        "evidence": [
                            {
                                "kind": "json-pointer",
                                "location": (
                                    f"{item['path']}#/hooks/{event_name}/{group_index}/hooks/{handler_index}"
                                ),
                            }
                        ],
                        "executable": False,
                        "id": stable_item_id(item["provider"], item["path"], identity),
                        "kind": "hook_handler",
                        "metadata": {
                            "event": event_name,
                            "handler_type": handler_type,
                            "matcher_declared": "matcher" in group,
                            "native_status": native_status or "unsupported",
                            "timeout_declared": "timeout" in handler,
                        },
                        "path": item["path"],
                        "permissions": list(item["permissions"]),
                        "profile_version": item["profile_version"],
                        "provider": item["provider"],
                        "provider_ownership": list(item["provider_ownership"]),
                        "security": dict(item["security"]),
                        "side_effect_hints": (
                            ["process"]
                            if handler_type == "command"
                            else ["network"]
                            if handler_type == "http"
                            else ["model"]
                            if handler_type in {"prompt", "agent"}
                            else ["opaque-executable"]
                        ),
                    }
                    if "content_hash" in item:
                        record["content_hash"] = item["content_hash"]
                    records.append(record)
    mcp = parsed.get("mcp") or parsed.get("mcpServers") or parsed.get("mcp_servers")
    if isinstance(mcp, dict):
        for name, declaration in sorted(mcp.items(), key=lambda pair: str(pair[0])):
            if not isinstance(declaration, dict):
                continue
            identity = f"mcp:{name}"
            records.append(
                {
                    "confidence": "explicit",
                    "dependencies": [item["id"]],
                    "disposition": "unresolved",
                    "entry_type": "file",
                    "environment_names": _json_environment_names(declaration),
                    "evidence": [
                        {
                            "kind": "json-pointer",
                            "location": f"{item['path']}#/mcp/{name}",
                        }
                    ],
                    "executable": False,
                    "id": stable_item_id(item["provider"], item["path"], identity),
                    "kind": "mcp_capability",
                    "metadata": {
                        "name": str(name),
                        "transport": declaration.get("type", "unresolved"),
                    },
                    "path": item["path"],
                    "permissions": [],
                    "profile_version": item["profile_version"],
                    "provider": item["provider"],
                    "provider_ownership": list(item["provider_ownership"]),
                    "security": dict(item["security"]),
                    "side_effect_hints": ["external-capability"],
                    **(
                        {"content_hash": item["content_hash"]}
                        if "content_hash" in item
                        else {}
                    ),
                }
            )
    return records


def _security(
    relative_path: str, data: bytes, entry_type: str, symlink_policy: str | None = None
) -> dict[str, Any]:
    if entry_type not in {"file", "symlink"}:
        return {"classification": "unsafe-special", "content_captured": False}
    if _SECRET_NAMES.search(relative_path) or _SECRET_CONTENT.search(data):
        return {"classification": "credential-shaped", "content_captured": False}
    if entry_type == "symlink":
        return {
            "classification": (
                "symlink" if symlink_policy == "internal" else "unsafe-symlink"
            ),
            "content_captured": False,
        }
    return {"classification": "ordinary", "content_captured": False}


def inspect_project(
    source: str | os.PathLike[str],
    *,
    ignore_rules: Iterable[IgnoreRule] | None = None,
) -> dict[str, Any]:
    """Inventory files and obvious semantic artifacts without execution."""

    root = canonical_path(source, must_exist=True)
    rules = tuple(DEFAULT_IGNORE_RULES if ignore_rules is None else ignore_rules)
    tree = fingerprint_tree(root, ignore_rules=rules)
    profiles = load_profiles()
    profiles_by_provider = {str(profile["provider"]): profile for profile in profiles}
    items: list[dict[str, Any]] = []
    providers: set[str] = set()
    for entry in tree.entries:
        if entry.type == "directory":
            continue
        matches = classify_path(entry.path, profiles)
        primary: ArtifactMatch | None = matches[0] if matches else None
        provider = primary.provider if primary else _provider_for(entry.path)
        profile_version = primary.profile_version if primary else "unprofiled"
        providers.update(match.provider for match in matches)
        providers.add(provider)
        data = b""
        if entry.type == "file":
            # Metadata inspection is bounded. Full bytes were already streamed by the
            # fingerprint phase and are never interpreted or executed.
            try:
                with (root / entry.path).open("rb") as stream:
                    data = stream.read(256 * 1024)
            except OSError as exc:
                raise RuntimeError(f"cannot inspect {entry.path!r}: {exc}") from exc
        fallback_kind = _kind_for(entry.path, entry.executable)
        kind = _profile_kind(primary.kind, fallback_kind) if primary else fallback_kind
        symlink_policy = None
        if entry.type == "symlink" and entry.symlink_target is not None:
            raw_target = Path(entry.symlink_target)
            if raw_target.is_absolute():
                symlink_policy = "absolute"
            else:
                lexical_target = (root / entry.path).parent / raw_target
                resolved_target = lexical_target.resolve(strict=False)
                symlink_policy = (
                    "internal"
                    if resolved_target == root or root in resolved_target.parents
                    else "escape"
                )
        security = _security(entry.path, data, entry.type, symlink_policy)
        identity = _frontmatter(data).get("name", "file") if kind == "skill" else "file"
        side_effect_hints = (
            ["process"]
            if kind == "script"
            else ["lifecycle"]
            if kind in {"hook_group", "hook_handler"}
            else []
        )
        item: dict[str, Any] = {
            "confidence": "explicit",
            "dependencies": [],
            "disposition": (
                "exclude"
                if security["classification"] == "credential-shaped"
                else "unsupported"
                if entry.type not in {"file", "symlink"}
                or symlink_policy in {"absolute", "escape"}
                else "unresolved"
            ),
            "entry_type": entry.type,
            "environment_names": _environment_names(data),
            "evidence": [{"kind": "source-path", "location": entry.path}],
            "executable": entry.executable,
            "id": stable_item_id(provider, entry.path, identity),
            "kind": kind,
            "metadata": _metadata(root / entry.path, kind, data),
            "path": entry.path,
            "permissions": [],
            "profile_version": profile_version,
            "provider": provider,
            "provider_ownership": [
                {
                    "kind": match.kind,
                    "priority": match.priority,
                    "profile_version": match.profile_version,
                    "provider": match.provider,
                    "rule_id": match.rule_id,
                }
                for match in matches
            ],
            "security": security,
            "side_effect_hints": side_effect_hints,
        }
        if entry.digest and security["classification"] != "credential-shaped":
            item["content_hash"] = entry.digest
        if entry.symlink_target is not None and symlink_policy == "internal":
            item["symlink_target"] = entry.symlink_target
        if symlink_policy is not None:
            item["symlink_policy"] = symlink_policy
        items.append(item)
        if entry.type == "file" and kind in {"configuration", "hook_group"}:
            parsed_configuration = _parse_configuration(root / entry.path, data)
            if isinstance(parsed_configuration, dict):
                item["environment_names"] = sorted(
                    set(item["environment_names"])
                    | set(_json_environment_names(parsed_configuration))
                )
                item["permissions"] = _json_permissions(parsed_configuration)
                item["semantic_elements"] = sorted(
                    _semantic_config_records(
                        item=item,
                        parsed=parsed_configuration,
                        profile=profiles_by_provider.get(provider),
                    ),
                    key=lambda element: element["id"],
                )
    items.sort(key=lambda item: (item["path"], item["kind"], item["id"]))
    classified = sum(item["disposition"] != "unresolved" for item in items)
    semantic_elements = [
        element for item in items for element in item.get("semantic_elements", [])
    ]
    semantic_classified = sum(
        item["disposition"] != "unresolved" for item in semantic_elements
    )
    document: dict[str, Any] = {
        "artifact": "inventory",
        "coverage": {
            "classified": classified,
            "total": len(items),
            "unresolved": len(items) - classified,
        },
        "items": items,
        "providers": [
            {
                "name": provider,
                "profile_version": next(
                    (
                        str(profile["profile_version"])
                        for profile in profiles
                        if profile["provider"] == provider
                    ),
                    "unprofiled",
                ),
            }
            for provider in sorted(providers)
        ],
        "schema_version": INVENTORY_SCHEMA_VERSION,
        "semantic_coverage": {
            "classified": semantic_classified,
            "total": len(semantic_elements),
            "unresolved": len(semantic_elements) - semantic_classified,
        },
        "source": {
            "fingerprint": tree.digest,
            "ignore_rules": [rule.to_dict() for rule in rules],
            "scope": ".",
        },
        "tool": {"name": "to-prism", "version": __version__},
    }
    # Assert it can pass through the canonical encoder before returning it.
    canonical_bytes(document)
    return document


build_inventory = inspect_project
