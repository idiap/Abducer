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
"""Load local API key configuration without exposing secrets."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, fail, load_json_object, rel


CONFIG_DIR = ROOT / "config"
DEFAULT_JSON = CONFIG_DIR / "api_keys.json"
DEFAULT_ENV = CONFIG_DIR / "api_keys.env"
EXAMPLE_JSON = CONFIG_DIR / "api_keys.example.json"
EXAMPLE_ENV = CONFIG_DIR / "api_keys.example.env"
SUPPORTED_ENV_KEYS = {
    "OPENAI_API_KEY",
    "OPENAI_ORG_ID",
    "OPENAI_PROJECT_ID",
    "OPENAI_BASE_URL",
    "OPENAI_MODEL",
    "OPENAI_REASONING_EFFORT",
    "OPENAI_MAX_OUTPUT_TOKENS",
    "OPENAI_API_TIMEOUT_SECONDS",
    "OPENAI_MAX_CONCURRENT_BRANCHES",
    "OPENAI_BRANCH_REQUEST_SPACING_SECONDS",
    "AZURE_OPENAI_API_KEY",
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_RESPONSES_ENDPOINT",
    "AZURE_OPENAI_MODEL",
    "AZURE_OPENAI_REASONING_EFFORT",
    "AZURE_OPENAI_MAX_OUTPUT_TOKENS",
    "AZURE_OPENAI_API_TIMEOUT_SECONDS",
    "AZURE_OPENAI_MAX_CONCURRENT_BRANCHES",
    "AZURE_OPENAI_BRANCH_REQUEST_SPACING_SECONDS",
    "ANTHROPIC_API_KEY",
    "GOOGLE_API_KEY",
}
SECRET_KEY_RE = re.compile(r"(API_KEY|TOKEN|SECRET|PASSWORD)", re.IGNORECASE)


def parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            fail(f"{rel(path)}:{lineno} must be KEY=value")
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not key:
            fail(f"{rel(path)}:{lineno} has empty key")
        values[key] = value
    return values


def resolve_config_path(raw: str | None = None) -> Path | None:
    if raw:
        path = Path(raw)
        return path if path.is_absolute() else ROOT / path
    if DEFAULT_JSON.exists():
        return DEFAULT_JSON
    if DEFAULT_ENV.exists():
        return DEFAULT_ENV
    return None


def load_api_key_values(path: Path | None = None, *, allow_missing: bool = True) -> tuple[dict[str, str], dict[str, Any]]:
    selected = path or resolve_config_path()
    if selected is None:
        if allow_missing:
            return {}, {"source": "environment-only", "active_provider": "", "configured_keys": []}
        fail("missing API key config; expected config/api_keys.json or config/api_keys.env")
    if not selected.exists():
        if allow_missing:
            return {}, {"source": rel(selected), "active_provider": "", "configured_keys": [], "missing": True}
        fail(f"missing API key config: {rel(selected)}")
    if selected.suffix == ".env":
        values = parse_env_file(selected)
        return values, {"source": rel(selected), "active_provider": "env", "configured_keys": sorted(values)}
    payload = load_json_object(selected)
    provider = clean_text(payload.get("active_provider")) or "openai"
    providers = payload.get("providers")
    if not isinstance(providers, dict) or provider not in providers:
        fail(f"{rel(selected)} active_provider `{provider}` is not in providers")
    provider_payload = providers[provider]
    if not isinstance(provider_payload, dict):
        fail(f"{rel(selected)} provider `{provider}` must be an object")
    env = provider_payload.get("env")
    if not isinstance(env, dict):
        fail(f"{rel(selected)} provider `{provider}` missing env object")
    values = {str(key): str(value) for key, value in env.items() if clean_text(value)}
    return values, {"source": rel(selected), "active_provider": provider, "configured_keys": sorted(values)}


def environment_with_api_keys(path: str | None = None, *, require_api_key: bool = False) -> tuple[dict[str, str], dict[str, Any]]:
    config_path = resolve_config_path(path)
    values, summary = load_api_key_values(config_path, allow_missing=not require_api_key)
    env = dict(os.environ)
    for key, value in values.items():
        if key not in SUPPORTED_ENV_KEYS and SECRET_KEY_RE.search(key):
            summary.setdefault("warnings", []).append(f"unrecognized secret-like key {key}")
        if clean_text(value) and not value.startswith("replace-with-"):
            env[key] = value
    if clean_text(env.get("AZURE_OPENAI_API_KEY")) and not clean_text(env.get("OPENAI_API_KEY")):
        env["OPENAI_API_KEY"] = env["AZURE_OPENAI_API_KEY"]
    if clean_text(env.get("AZURE_OPENAI_MODEL")) and not clean_text(env.get("OPENAI_MODEL")):
        env["OPENAI_MODEL"] = env["AZURE_OPENAI_MODEL"]
    if clean_text(env.get("AZURE_OPENAI_REASONING_EFFORT")) and not clean_text(env.get("OPENAI_REASONING_EFFORT")):
        env["OPENAI_REASONING_EFFORT"] = env["AZURE_OPENAI_REASONING_EFFORT"]
    if clean_text(env.get("AZURE_OPENAI_ENDPOINT")) and not clean_text(env.get("OPENAI_BASE_URL")):
        env["OPENAI_BASE_URL"] = env["AZURE_OPENAI_ENDPOINT"]
    has_openai = bool(clean_text(env.get("OPENAI_API_KEY")))
    summary["has_openai_api_key"] = has_openai
    summary["redacted"] = {key: redact(env.get(key, "")) for key in sorted(set(values) | {"OPENAI_API_KEY"}) if env.get(key)}
    if require_api_key and not has_openai:
        fail("OpenAI API key required: set OPENAI_API_KEY in config/api_keys.json, config/api_keys.env, or the process environment")
    return env, summary


def redact(value: str) -> str:
    if not value:
        return ""
    if len(value) <= 8:
        return "***"
    return f"{value[:4]}...{value[-4:]}"


def is_placeholder(value: str) -> bool:
    lowered = clean_text(value).lower()
    return not lowered or lowered in {"replace-with-local-key", "your-key-here", "changeme"} or "replace" in lowered
