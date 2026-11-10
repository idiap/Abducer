#!/usr/bin/env python3
"""Validate local API key configuration without printing secrets."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from agentic_common import ROOT, clean_text, fail, rel
from api_key_config import DEFAULT_ENV, DEFAULT_JSON, EXAMPLE_ENV, EXAMPLE_JSON, SUPPORTED_ENV_KEYS, is_placeholder, load_api_key_values, parse_env_file, resolve_config_path


def git_check_ignored(path: Path) -> bool:
    result = subprocess.run(["git", "check-ignore", "-q", str(path)], cwd=ROOT)
    return result.returncode == 0


def validate_example_files() -> None:
    for path in [EXAMPLE_JSON, EXAMPLE_ENV]:
        if not path.exists():
            fail(f"missing example API config {rel(path)}")
    values, _ = load_api_key_values(EXAMPLE_JSON, allow_missing=False)
    for key, value in values.items():
        if key.endswith("API_KEY") and not is_placeholder(value):
            fail(f"{rel(EXAMPLE_JSON)} must not contain a real-looking {key}")
    env_values = parse_env_file(EXAMPLE_ENV)
    for key, value in env_values.items():
        if key.endswith("API_KEY") and not is_placeholder(value):
            fail(f"{rel(EXAMPLE_ENV)} must not contain a real-looking {key}")


def validate_ignore_rules() -> None:
    for path in [DEFAULT_JSON, DEFAULT_ENV, ROOT / "config/foo.local.json", ROOT / "config/foo.local.env"]:
        if not git_check_ignored(path):
            fail(f"{rel(path)} must be ignored by git")


def validate_actual_config(path: Path | None, *, require_openai: bool) -> None:
    if path is None:
        if require_openai:
            fail("missing config/api_keys.json or config/api_keys.env")
        print("No local API key config found; environment-only mode is allowed.")
        return
    values, summary = load_api_key_values(path, allow_missing=False)
    unknown = [key for key in values if key not in SUPPORTED_ENV_KEYS]
    if unknown:
        fail(f"{rel(path)} contains unsupported keys: {unknown}")
    if require_openai and is_placeholder(values.get("OPENAI_API_KEY", values.get("AZURE_OPENAI_API_KEY", ""))):
        fail(f"{rel(path)} must contain a non-placeholder OPENAI_API_KEY or AZURE_OPENAI_API_KEY")
    if summary.get("active_provider") == "azure_openai":
        for key in ["AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_RESPONSES_ENDPOINT", "AZURE_OPENAI_MODEL"]:
            if not clean_text(values.get(key)):
                fail(f"{rel(path)} azure_openai config missing {key}")
        effort = clean_text(values.get("AZURE_OPENAI_REASONING_EFFORT") or values.get("OPENAI_REASONING_EFFORT"))
        if effort and effort not in {"minimal", "low", "medium", "high"}:
            fail(f"{rel(path)} reasoning effort must be one of minimal, low, medium, high")
        endpoint = values["AZURE_OPENAI_ENDPOINT"].rstrip("/")
        responses = values["AZURE_OPENAI_RESPONSES_ENDPOINT"].rstrip("/")
        if responses.endswith("/responses"):
            expected_base = responses[: -len("/responses")]
            if endpoint.rstrip("/") != expected_base:
                fail(f"{rel(path)} AZURE_OPENAI_ENDPOINT should be the base endpoint {expected_base}")
    print(f"validated API key config source={summary['source']} provider={summary.get('active_provider', '')} keys={summary['configured_keys']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config")
    parser.add_argument("--require-openai", action="store_true")
    args = parser.parse_args()
    validate_example_files()
    validate_ignore_rules()
    path = resolve_config_path(args.config)
    validate_actual_config(path, require_openai=args.require_openai)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
