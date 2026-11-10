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
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest
from to_prism.fingerprint import fingerprint_tree
from to_prism.inventory import inspect_project

KIT_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = KIT_ROOT / "tests" / "fixtures"
PILOTS = KIT_ROOT / "tests" / "provider-pilots"


@dataclass(frozen=True, slots=True)
class ProviderCase:
    name: str
    pre_event: str
    post_event: str
    stop_event: str


PROVIDERS = (
    ProviderCase("codex", "PreToolUse", "PostToolUse", "Stop"),
    ProviderCase("claude", "PreToolUse", "PostToolUse", "Stop"),
    ProviderCase(
        "opencode", "tool.execute.before", "tool.execute.after", "session.idle"
    ),
)


def _declared_command(case: ProviderCase, event: str) -> list[str]:
    if case.name == "opencode":
        frontend = (
            KIT_ROOT / "integration-hooks" / "opencode" / "to-prism-guards.ts"
        ).read_text(encoding="utf-8")
        assert (
            '["to-prism", "guard", "--provider", "opencode", "--event", event]'
            in frontend
        )
        assert f'runGuard("{event}"' in frontend
        return ["to-prism", "guard", "--provider", "opencode", "--event", event]

    configuration_path = (
        KIT_ROOT / "integration-hooks" / case.name / "hooks.json"
        if case.name == "codex"
        else KIT_ROOT / "integration-hooks" / case.name / "settings.json"
    )
    configuration = json.loads(configuration_path.read_text(encoding="utf-8"))
    command = configuration["hooks"][event][0]["hooks"][0]["command"]
    return shlex.split(command)


def _native_payload(
    case: ProviderCase,
    *,
    tool: str,
    arguments: dict[str, Any],
    cwd: Path,
) -> dict[str, Any]:
    if case.name == "opencode":
        return {
            "input": {"tool": tool, "sessionID": "fixture-session"},
            "output": {"args": arguments},
        }
    return {
        "cwd": str(cwd),
        "hook_event_name": case.pre_event,
        "session_id": "fixture-session",
        "tool_input": arguments,
        "tool_name": tool,
    }


def _run_frontend(
    case: ProviderCase,
    event: str,
    payload: dict[str, Any] | str,
    *,
    source: Path,
    output: Path,
    phase: str,
    context: bool = True,
) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PATH"] = f"{KIT_ROOT / 'bin'}{os.pathsep}{environment.get('PATH', '')}"
    environment["PYTHON"] = sys.executable
    if context:
        environment.update(
            {
                "TO_PRISM_SOURCE_ROOT": str(source),
                "TO_PRISM_OUTPUT_ROOT": str(output),
                "TO_PRISM_PHASE": phase,
            }
        )
    else:
        for name in (
            "TO_PRISM_SOURCE_ROOT",
            "TO_PRISM_OUTPUT_ROOT",
            "TO_PRISM_PHASE",
        ):
            environment.pop(name, None)
    stdin = payload if isinstance(payload, str) else json.dumps(payload)
    return subprocess.run(
        _declared_command(case, event),
        input=stdin,
        text=True,
        capture_output=True,
        cwd=KIT_ROOT,
        env=environment,
        check=False,
    )


def _roots(tmp_path: Path) -> tuple[Path, Path]:
    source = tmp_path / "source"
    source.mkdir()
    (source / "README.md").write_text("fixture\n", encoding="utf-8")
    return source, tmp_path / "output"


def _assert_rejected(completed: subprocess.CompletedProcess[str], text: str) -> None:
    assert completed.returncode == 3
    assert completed.stdout == ""
    error = json.loads(completed.stderr)
    assert error["status"] == "rejected"
    assert text in error["error"]


@pytest.mark.parametrize("case", PROVIDERS, ids=lambda case: case.name)
def test_frontend_blocks_source_mutation_without_mutating_source(
    case: ProviderCase, tmp_path: Path
) -> None:
    source, output = _roots(tmp_path)
    before = fingerprint_tree(source).digest
    if case.name == "codex":
        payload = _native_payload(
            case,
            tool="apply_patch",
            arguments={"command": "*** Update File: README.md\n"},
            cwd=source,
        )
    elif case.name == "claude":
        payload = _native_payload(
            case,
            tool="Write",
            arguments={"file_path": str(source / "README.md"), "content": "changed"},
            cwd=source,
        )
    else:
        payload = _native_payload(
            case,
            tool="write",
            arguments={"filePath": str(source / "README.md"), "content": "changed"},
            cwd=source,
        )

    completed = _run_frontend(
        case, case.pre_event, payload, source=source, output=output, phase="generate"
    )

    _assert_rejected(completed, "write")
    assert fingerprint_tree(source).digest == before


@pytest.mark.parametrize("case", PROVIDERS, ids=lambda case: case.name)
def test_frontend_blocks_credential_shaped_read(
    case: ProviderCase, tmp_path: Path
) -> None:
    source, output = _roots(tmp_path)
    arguments = (
        {"filePath": str(source / ".env")}
        if case.name == "opencode"
        else {"file_path": str(source / ".env")}
    )
    payload = _native_payload(
        case,
        tool="read" if case.name == "opencode" else "Read",
        arguments=arguments,
        cwd=source,
    )

    completed = _run_frontend(
        case, case.pre_event, payload, source=source, output=output, phase="inspect"
    )

    _assert_rejected(completed, "credential-shaped")


@pytest.mark.parametrize("case", PROVIDERS, ids=lambda case: case.name)
def test_frontend_blocks_command_during_inspection(
    case: ProviderCase, tmp_path: Path
) -> None:
    source, output = _roots(tmp_path)
    payload = _native_payload(
        case,
        tool="bash" if case.name == "opencode" else "Bash",
        arguments={"command": "git status"},
        cwd=source,
    )

    completed = _run_frontend(
        case, case.pre_event, payload, source=source, output=output, phase="inspect"
    )

    _assert_rejected(completed, "execution is not authorized")


@pytest.mark.parametrize("case", PROVIDERS, ids=lambda case: case.name)
def test_frontend_allows_benign_read_with_clean_stdout(
    case: ProviderCase, tmp_path: Path
) -> None:
    source, output = _roots(tmp_path)
    arguments = (
        {"filePath": str(source / "README.md")}
        if case.name == "opencode"
        else {"file_path": str(source / "README.md")}
    )
    payload = _native_payload(
        case,
        tool="read" if case.name == "opencode" else "Read",
        arguments=arguments,
        cwd=source,
    )

    completed = _run_frontend(
        case, case.pre_event, payload, source=source, output=output, phase="inspect"
    )

    assert completed.returncode == 0
    assert completed.stderr == ""
    result = json.loads(completed.stdout)
    assert result == {
        "allowed": True,
        "event": case.pre_event,
        "protocol_version": 1,
        "provider": case.name,
    }


@pytest.mark.parametrize("case", PROVIDERS, ids=lambda case: case.name)
def test_post_frontend_is_advisory_after_tool_execution(
    case: ProviderCase, tmp_path: Path
) -> None:
    source, output = _roots(tmp_path)
    payload = _native_payload(
        case,
        tool="write" if case.name == "opencode" else "Write",
        arguments={"file_path": str(source / "README.md")},
        cwd=source,
    )

    completed = _run_frontend(
        case, case.post_event, payload, source=source, output=output, phase="generate"
    )

    assert completed.returncode == 0
    assert json.loads(completed.stdout)["allowed"] is True


@pytest.mark.parametrize("case", PROVIDERS, ids=lambda case: case.name)
def test_completion_frontend_requires_all_conversion_artifacts(
    case: ProviderCase, tmp_path: Path
) -> None:
    source, output = _roots(tmp_path)
    payload = (
        {"event": {"type": "session.idle"}}
        if case.name == "opencode"
        else {"hook_event_name": "Stop", "session_id": "fixture-session"}
    )

    incomplete = _run_frontend(
        case, case.stop_event, payload, source=source, output=output, phase="generate"
    )
    _assert_rejected(incomplete, "completion artifacts are incomplete")

    conversion = output / "conversion"
    conversion.mkdir(parents=True)
    for relative in ("inventory.json", "contracts.json", "workflow.json", "report.md"):
        (conversion / relative).write_text("{}\n", encoding="utf-8")
    complete = _run_frontend(
        case, case.stop_event, payload, source=source, output=output, phase="generate"
    )
    assert complete.returncode == 0
    assert json.loads(complete.stdout)["allowed"] is True


@pytest.mark.parametrize("case", PROVIDERS, ids=lambda case: case.name)
def test_frontend_fails_closed_on_invalid_payload_and_missing_context(
    case: ProviderCase, tmp_path: Path
) -> None:
    source, output = _roots(tmp_path)

    invalid = _run_frontend(
        case, case.pre_event, "[]", source=source, output=output, phase="inspect"
    )
    _assert_rejected(invalid, "payload")

    payload = _native_payload(
        case,
        tool="read" if case.name == "opencode" else "Read",
        arguments={"file_path": str(source / "README.md")},
        cwd=source,
    )
    no_context = _run_frontend(
        case,
        case.pre_event,
        payload,
        source=source,
        output=output,
        phase="inspect",
        context=False,
    )
    _assert_rejected(no_context, "guard context is incomplete")


@pytest.mark.parametrize(
    "pilot_path", sorted(PILOTS.glob("*.json")), ids=lambda path: path.stem
)
def test_provider_pilot_accounts_for_every_profiled_inventory_item(
    pilot_path: Path,
) -> None:
    pilot = json.loads(pilot_path.read_text(encoding="utf-8"))
    fixture = FIXTURES / pilot["fixture"]
    before = fingerprint_tree(fixture).digest

    inventory = inspect_project(fixture)

    assert fingerprint_tree(fixture).digest == before
    expected = {item["path"]: item for item in pilot["expected_profiled_inventory"]}
    actual = {item["path"]: item for item in inventory["items"]}
    profiled_paths = {
        path for path, item in actual.items() if item["profile_version"] != "unprofiled"
    }
    assert profiled_paths == set(expected)
    for path, expectation in expected.items():
        item = actual[path]
        assert item["kind"] == expectation["kind"]
        assert item["provider"] == expectation["provider"]
        assert item["profile_version"] == pilot["profile_version"]
        assert item["disposition"] in {
            "convert",
            "wrap",
            "copy",
            "exclude",
            "unsupported",
            "unresolved",
        }
        if "owners" in expectation:
            assert (
                sorted(owner["provider"] for owner in item["provider_ownership"])
                == expectation["owners"]
            )
