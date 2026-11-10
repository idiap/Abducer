# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

KIT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KIT_ROOT / "src"))

from to_prism.provider_profiles import (  # noqa: E402
    ProviderProfileError,
    classify_path,
    hook_event,
    hook_handler_status,
    load_profile,
    load_profiles,
)


def test_all_bundled_profiles_validate_without_yaml_dependency() -> None:
    profiles = load_profiles()

    assert [profile["provider"] for profile in profiles] == [
        "claude",
        "codex",
        "open-agent-skill",
        "opencode",
    ]
    assert all(profile["profile_version"] == "2026-08-19" for profile in profiles)


@pytest.mark.parametrize(
    ("provider", "relative_path", "kind"),
    [
        ("codex", ".codex/hooks.json", "hook_configuration"),
        ("codex", ".codex/agents/reviewer.toml", "agent"),
        ("codex", ".agents/skills/review/SKILL.md", "skill"),
        ("claude", ".claude/settings.json", "configuration"),
        ("claude", ".claude/agents/reviewer.md", "agent"),
        ("claude", ".mcp.json", "mcp_configuration"),
        ("opencode", "opencode.json", "configuration"),
        ("opencode", ".opencode/plugins/guard.ts", "executable_plugin"),
        ("opencode", ".opencode/tools/risk-score.ts", "executable_tool"),
    ],
)
def test_realistic_fixture_paths_match_provider_rules(
    provider: str, relative_path: str, kind: str
) -> None:
    profile = load_profile(provider)

    matches = classify_path(relative_path, [profile])

    assert any(match.provider == provider and match.kind == kind for match in matches)


def test_compatible_skill_layout_retains_mixed_provider_ownership() -> None:
    profiles = load_profiles()

    claude_skill = classify_path(".claude/skills/shared/SKILL.md", profiles)
    portable_skill = classify_path(".agents/skills/portable/SKILL.md", profiles)

    assert {match.provider for match in claude_skill} == {
        "claude",
        "open-agent-skill",
        "opencode",
    }
    assert {match.provider for match in portable_skill} == {
        "codex",
        "open-agent-skill",
        "opencode",
    }
    assert claude_skill[0].provider == "claude"
    assert portable_skill[0].provider == "codex"


def test_unknown_hook_events_and_handler_types_do_not_fuzzy_match() -> None:
    codex = load_profile("codex")

    assert hook_event(codex, "PreToolUse") is not None
    assert hook_event(codex, "pretooluse") is None
    assert hook_event(codex, "BeforeToolUse") is None
    assert hook_handler_status(codex, "command") == "executed"
    assert hook_handler_status(codex, "http") is None


def test_opencode_contract_is_executable_plugin_not_declarative_hooks() -> None:
    profile = load_profile("opencode")

    assert profile["hooks"]["contract"] == "javascript_or_typescript_plugin_callbacks"
    assert profile["hooks"]["unknown_event"] == "opaque_executable"
    assert profile["hooks"]["configuration_globs"]
    assert all(
        not glob.endswith("hooks.json")
        for glob in profile["hooks"]["configuration_globs"]
    )


def test_paths_must_be_canonical_and_source_relative() -> None:
    profiles = load_profiles(["codex"])

    with pytest.raises(ProviderProfileError, match="source-relative"):
        classify_path("../outside/.codex/hooks.json", profiles)
    with pytest.raises(ProviderProfileError, match="source-relative"):
        classify_path("/tmp/project/.codex/hooks.json", profiles)


def test_profile_loader_rejects_unknown_schema_version(tmp_path: Path) -> None:
    original = load_profile("codex")
    original["schema_version"] = 99
    (tmp_path / "codex.yaml").write_text(json.dumps(original), encoding="utf-8")

    with pytest.raises(
        ProviderProfileError, match="unsupported provider profile schema"
    ):
        load_profile("codex", tmp_path)


def test_declarative_guard_configs_use_only_profile_events_and_logical_command() -> (
    None
):
    cases = (
        ("codex", KIT_ROOT / "integration-hooks" / "codex" / "hooks.json"),
        ("claude", KIT_ROOT / "integration-hooks" / "claude" / "settings.json"),
    )
    for provider, path in cases:
        profile = load_profile(provider)
        configuration = json.loads(path.read_text(encoding="utf-8"))
        for event_name, groups in configuration["hooks"].items():
            assert hook_event(profile, event_name) is not None
            for group in groups:
                for handler in group["hooks"]:
                    assert handler["type"] == "command"
                    assert handler["command"].startswith(
                        f"to-prism guard --provider {provider} --event {event_name}"
                    )
                    assert "/Users/" not in handler["command"]


def test_opencode_guard_frontend_uses_exact_events_and_installed_command() -> None:
    profile = load_profile("opencode")
    frontend = (
        KIT_ROOT / "integration-hooks" / "opencode" / "to-prism-guards.ts"
    ).read_text(encoding="utf-8")

    for event_name in ("tool.execute.before", "tool.execute.after", "session.idle"):
        assert hook_event(profile, event_name) is not None
        assert f'"{event_name}"' in frontend
    assert '["to-prism", "guard"' in frontend
    assert "/Users/" not in frontend


def test_provider_sources_are_official_primary_domains() -> None:
    allowed_hosts = (
        "https://developers.openai.com/",
        "https://learn.chatgpt.com/",
        "https://code.claude.com/",
        "https://opencode.ai/",
        "https://agentskills.io/",
    )

    for profile in load_profiles():
        assert all(
            source["url"].startswith(allowed_hosts) for source in profile["sources"]
        )


def test_each_realistic_fixture_has_at_least_one_native_provider_marker() -> None:
    fixtures = KIT_ROOT / "tests" / "fixtures"
    for provider in ("codex", "claude", "opencode"):
        fixture = fixtures / provider
        profile = load_profile(provider)
        matched = []
        for path in fixture.rglob("*"):
            if path.is_file():
                matched.extend(
                    classify_path(path.relative_to(fixture).as_posix(), [profile])
                )
        assert matched, provider
        assert any(match.priority >= 100 for match in matched), provider
