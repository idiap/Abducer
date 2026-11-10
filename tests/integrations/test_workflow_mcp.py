# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Exercise every workflow through the real isolated packaged MCP process.

These checks establish discovery and read-only contract parity. No research
runtime binding is imported, and no scientific workflow is executed.
"""

from __future__ import annotations

import importlib.util
import base64
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest
import yaml

from integrations.agent_plugins.generate import (
    PLUGIN,
    ROOT,
    WORKFLOWS,
    workflow_catalog,
)


def request(identity, method, params=None):
    value = {"jsonrpc": "2.0", "id": identity, "method": method}
    if params is not None:
        value["params"] = params
    return value


def opening(version="2025-11-25"):
    return [
        request(
            0,
            "initialize",
            {
                "protocolVersion": version,
                "capabilities": {},
                "clientInfo": {"name": "contract-test", "version": "1.0.0"},
            },
        ),
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
    ]


def exchange(script, messages, cwd):
    """Run newline-framed RPC, retaining malformed raw input probes."""
    raw = "\n".join(m if isinstance(m, str) else json.dumps(m) for m in messages) + "\n"
    result = subprocess.run(
        [sys.executable, "-I", str(script)],
        input=raw,
        text=True,
        capture_output=True,
        cwd=cwd,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr
    assert not result.stderr
    return [json.loads(line) for line in result.stdout.splitlines()]


@pytest.fixture
def package(tmp_path):
    installed = tmp_path / "isolated installed plugin"
    shutil.copytree(ROOT / PLUGIN, installed)
    return installed


def test_every_workflow_has_plugin_entry_and_packaged_contract():
    native = yaml.safe_load((ROOT / WORKFLOWS / "index.yaml").read_text())["workflows"]
    packaged = json.loads((ROOT / PLUGIN / "workflows.json").read_text())["workflows"]
    assert len(packaged) == len(native) == 34
    assert {r["id"] for r in packaged} == {r["id"] for r in native}
    for row in packaged:
        assert row["contract"] == yaml.safe_load((ROOT / row["descriptor"]).read_text())
        content = (ROOT / PLUGIN / "skills" / row["entry"] / "SKILL.md").read_text()
        assert yaml.safe_load(content.split("---", 2)[1])["name"] == row["entry"]
        assert "--workflow " + row["id"] in content
        assert "Normalized execution adapters are" in content
        assert "Loading this entry does not" in content


def test_all_workflows_roundtrip_tools_resources_and_prompts(package, tmp_path):
    rows = workflow_catalog(ROOT)
    messages = opening() + [
        request(1, "tools/list"),
        request(2, "resources/list"),
        request(3, "prompts/list"),
        request(4, "tools/call", {"name": "list_workflows"}),
    ]
    for i, row in enumerate(rows, 10):
        messages.extend(
            [
                request(
                    i * 3,
                    "tools/call",
                    {"name": "get_workflow", "arguments": {"workflow_id": row["id"]}},
                ),
                request(
                    i * 3 + 1,
                    "resources/read",
                    {"uri": "abducer://workflows/" + row["id"]},
                ),
                request(i * 3 + 2, "prompts/get", {"name": row["id"]}),
            ]
        )
    responses = {
        r["id"]: r
        for r in exchange(package / "scripts/workflow_mcp.py", messages, tmp_path)
    }
    assert responses[0]["result"]["protocolVersion"] == "2025-11-25"
    assert set(responses[0]["result"]["capabilities"]) == {
        "tools",
        "resources",
        "prompts",
    }
    assert (
        len(responses[2]["result"]["resources"])
        == len(responses[3]["result"]["prompts"])
        == 34
    )
    catalog = json.loads(responses[4]["result"]["content"][0]["text"])["workflows"]
    assert {r["id"] for r in catalog} == {r["id"] for r in rows}
    assert all(
        tool["annotations"]["readOnlyHint"] for tool in responses[1]["result"]["tools"]
    )
    for i, row in enumerate(rows, 10):
        tool = responses[i * 3]["result"]
        assert not tool["isError"]
        assert json.loads(tool["content"][0]["text"]) == row
        assert json.loads(responses[i * 3 + 1]["result"]["contents"][0]["text"]) == row
        prompt = responses[i * 3 + 2]["result"]
        assert "interface-only" in prompt["description"]
        assert row["id"] in prompt["messages"][0]["content"]["text"]


def test_bad_requests_do_not_crash_or_gain_execution(package, tmp_path):
    messages = [
        request(1, "tools/list"),
        "not json",
        "NaN",
        [],
        request(2, "initialize", {}),
        *opening(),
        request(3, "tools/call", {"name": []}),
        request(
            4,
            "tools/call",
            {"name": "get_workflow", "arguments": {"workflow_id": "../../secret"}},
        ),
        request(
            5,
            "tools/call",
            {
                "name": "get_workflow",
                "arguments": {
                    "workflow_id": "theorem_proof_delivery_workflow",
                    "execute": True,
                },
            },
        ),
        request(6, "resources/read", {"uri": "file:///etc/passwd"}),
        request(7, "workflow/execute", {}),
        request(8, "prompts/get", {"name": "unknown"}),
        request(9, "ping"),
        {"jsonrpc": "2.0", "method": "notifications/cancelled"},
    ]
    result = exchange(package / "scripts/workflow_mcp.py", messages, tmp_path)
    keyed = {r["id"]: r for r in result if r["id"] is not None}
    assert keyed[1]["error"]["code"] == -32002
    assert keyed[2]["error"]["code"] == keyed[3]["error"]["code"] == -32602
    assert keyed[4]["result"]["isError"] and keyed[5]["result"]["isError"]
    assert "error" in keyed[6] and keyed[7]["error"]["code"] == -32601
    assert "error" in keyed[8] and keyed[9]["result"] == {}
    assert any(r.get("error", {}).get("code") == -32700 for r in result)


def test_oversized_request_is_drained_before_next_message(package, tmp_path):
    messages = ["x" * (1024 * 1024 + 1), *opening(), request(1, "ping")]
    result = exchange(package / "scripts/workflow_mcp.py", messages, tmp_path)
    assert result[0]["error"]["code"] == -32600
    assert "exceeds" in result[0]["error"]["message"]
    assert result[-1] == {"jsonrpc": "2.0", "id": 1, "result": {}}


@pytest.mark.parametrize(
    "version,expected",
    [
        ("2024-11-05", "2024-11-05"),
        ("2025-03-26", "2025-03-26"),
        ("2025-06-18", "2025-06-18"),
        ("future-version", "2025-11-25"),
    ],
)
def test_version_negotiation(package, tmp_path, version, expected):
    result = exchange(package / "scripts/workflow_mcp.py", opening(version), tmp_path)
    assert result[0]["result"]["protocolVersion"] == expected


def test_every_owner_resolves_and_descriptor_tamper_fails(tmp_path):
    path = ROOT / PLUGIN / "scripts/resolve_checkout.py"
    spec = importlib.util.spec_from_file_location("workflow_resolver", path)
    resolver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(resolver)
    for row in workflow_catalog(ROOT):
        result = resolver.resolve(row["id"], str(ROOT), workflow=True)
        assert Path(result["workflow_file"]) == ROOT / row["descriptor"]
        assert Path(result["skill_file"]) == ROOT / row["owner"]
    row = next(r for r in workflow_catalog(ROOT) if r["id"] == "abducer_work_workflow")
    for source in [row["owner"], row["descriptor"], "pyproject.toml"]:
        target = tmp_path / source
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / source, target)
    descriptor = tmp_path / row["descriptor"]
    descriptor.write_text(descriptor.read_text() + "\n# changed\n")
    with pytest.raises(ValueError, match="workflow versions differ"):
        resolver.resolve(row["id"], str(tmp_path), workflow=True)


def test_host_mcp_configs_use_same_bundled_server():
    for name, variable in [
        ("mcp.json", "PLUGIN_ROOT"),
        (".mcp.json", "CLAUDE_PLUGIN_ROOT"),
        (".codex-mcp.json", "CLAUDE_PLUGIN_ROOT"),
    ]:
        config = json.loads((ROOT / PLUGIN / name).read_text())["mcpServers"][
            "abducer-workflows"
        ]
        assert config["command"] == "python3"
        assert config["args"] == ["${" + variable + "}/scripts/workflow_mcp.py"]
    assert (ROOT / PLUGIN / "scripts/workflow_mcp.py").read_bytes() == (
        ROOT / "integrations/workflow_mcp/server.py"
    ).read_bytes()


def source_server(catalog=None):
    """Load the canonical protocol dispatcher without a scientific runtime."""
    path = ROOT / "integrations/workflow_mcp/server.py"
    spec = importlib.util.spec_from_file_location("asset_workflow_server", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    server = module.WorkflowServer(catalog or ROOT / PLUGIN / "workflows.json")
    for message in opening():
        server.handle(message)
    return server


def asset_call(server, name, arguments=None):
    """Use the same JSON-RPC argument and lifecycle boundary as stdio clients."""
    response = server.handle(
        request(99, "tools/call", {"name": name, "arguments": arguments or {}})
    )
    assert "error" not in response
    return response["result"]


def asset_value(server, name, arguments=None):
    response = asset_call(server, name, arguments)
    assert not response["isError"], response
    return json.loads(response["content"][0]["text"])


def test_source_asset_manifest_reconciles_public_skills_and_every_declared_byte():
    server = source_server()
    entries, cursor = [], None
    while True:
        page = asset_value(
            server, "list_agent_assets", {"cursor": cursor} if cursor else {}
        )
        assert page["schema_version"] == "agent-skills.mcp-assets/v1"
        entries.extend(page["entries"])
        cursor = page["next_cursor"]
        if cursor is None:
            break
    assert len(entries) > 100
    assert len({row["path"] for row in entries}) == len(entries)
    public = json.loads((ROOT / PLUGIN / "source-skills.json").read_text())["skills"]
    expected_skills = {row["source"] for row in public} | {
        str(PLUGIN / "skills" / row["entry"] / "SKILL.md") for row in server.rows
    }
    assert {row["path"] for row in entries if row["kind"] == "skill"} == expected_skills
    assert {row["path"] for row in entries if row["kind"] == "workflow"} == {
        row["descriptor"] for row in server.rows
    }
    for row in entries:
        result = asset_value(server, "read_agent_asset", {"path": row["path"]})
        payload = (
            result["content"].encode()
            if result["encoding"] == "text"
            else base64.b64decode(result["content"])
        )
        assert hashlib.sha256(payload).hexdigest() == row["sha256"] == result["sha256"]
        assert payload == (ROOT / row["path"]).read_bytes()


@pytest.fixture
def tiny_source(tmp_path):
    """Supply a complete tiny source layout, so negative tests never edit ROOT."""
    root = tmp_path / "source"

    def write(path, content):
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        return hashlib.sha256(content.encode()).hexdigest()

    owner = "skills/demo/SKILL.md"
    owner_digest = write(
        owner,
        "---\nname: demo\ndescription: Demo source.\n---\nInspect without execution.\n",
    )
    contract = {
        "schema_version": "workflow-skill/v1",
        "id": "demo_workflow",
        "types": {},
        "provenance": {"sources": []},
    }
    descriptor = "workflows/demo.yaml"
    descriptor_digest = write(descriptor, json.dumps(contract))
    row = {
        "id": "demo_workflow",
        "namespace": "fixture",
        "version": "1.0.0",
        "entry": "workflow-demo",
        "aliases": [],
        "owner": owner,
        "descriptor": descriptor,
        "lifecycle": "draft",
        "coverage": "interface_only",
        "owner_sha256": owner_digest,
        "descriptor_sha256": descriptor_digest,
        "contract": contract,
    }
    write(
        "plugins/abducer/skills/workflow-demo/SKILL.md",
        "---\nname: workflow-demo\ndescription: Inspect demo.\n---\nInspection only.\n",
    )
    write(
        "plugins/abducer/source-skills.json",
        json.dumps({"skills": [{"source": owner, "sha256": owner_digest}]}),
    )
    write(
        "plugins/abducer/workflows.json",
        json.dumps(
            {
                "schema_version": "abducer.workflow-catalog/v1",
                "plugin_version": "1.0.0",
                "workflows": [row],
            }
        ),
    )
    write("agentic/registries/skill_registry.yaml", "{}")
    write("pyproject.toml", "[project]\nname='fixture'\nversion='1.0.0'\n")
    return root


def test_asset_snapshot_is_frozen_and_new_sessions_reject_stale_native_digests(
    tiny_source,
):
    catalog = tiny_source / "plugins/abducer/workflows.json"
    server = source_server(catalog)
    asset_value(server, "list_agent_assets")
    before = asset_value(server, "read_agent_asset", {"path": "skills/demo/SKILL.md"})
    (tiny_source / "skills/demo/SKILL.md").write_text("changed source bytes")
    assert (
        asset_value(server, "read_agent_asset", {"path": "skills/demo/SKILL.md"})
        == before
    )
    result = asset_call(source_server(catalog), "list_agent_assets")
    assert result["isError"] and "Source assets changed" in result["content"][0]["text"]


@pytest.mark.parametrize(
    "name,args",
    [
        ("read_agent_asset", {"path": "../../private"}),
        ("read_agent_asset", {"path": "/etc/passwd"}),
        ("read_agent_asset", {"path": "%2e%2e/private"}),
        ("read_agent_asset", {"path": "unknown"}),
        ("read_agent_asset", {"path": []}),
        ("list_agent_assets", {"cursor": "-1"}),
        ("list_agent_assets", {"cursor": 100}),
        ("list_agent_assets", {"cursor": "999999"}),
        ("list_agent_assets", {"execute": True}),
    ],
)
def test_asset_rpc_rejects_undeclared_paths_and_invalid_arguments(
    tiny_source, name, args
):
    result = asset_call(
        source_server(tiny_source / "plugins/abducer/workflows.json"), name, args
    )
    assert result["isError"]
    assert "changed source bytes" not in result["content"][0]["text"]


@pytest.mark.parametrize("escape", [False, True])
def test_asset_export_rejects_credentials_and_symlink_escape(
    tiny_source, tmp_path, escape
):
    if escape:
        outside = tmp_path / "private.txt"
        outside.write_text("fixture-private-secret")
        (tiny_source / "skills/demo/link.txt").symlink_to(outside)
    else:
        (tiny_source / "skills/demo/.env").write_text("fixture-private-secret")
    result = asset_call(
        source_server(tiny_source / "plugins/abducer/workflows.json"),
        "list_agent_assets",
    )
    assert result["isError"]
    assert "fixture-private-secret" not in str(result)


def test_installed_asset_unavailability_does_not_remove_existing_workflow_reads(
    package, tmp_path
):
    responses = exchange(
        package / "scripts/workflow_mcp.py",
        opening()
        + [
            request(1, "tools/call", {"name": "list_agent_assets"}),
            request(2, "tools/call", {"name": "list_workflows"}),
        ],
        tmp_path,
    )
    result = {row["id"]: row for row in responses}
    assert result[1]["result"]["isError"]
    assert (
        "requires the Abducer source checkout"
        in result[1]["result"]["content"][0]["text"]
    )
    assert not result[2]["result"]["isError"]
    assert len(json.loads(result[2]["result"]["content"][0]["text"])["workflows"]) == 34
    assert (package / "scripts/agent_assets.py").read_bytes() == (
        ROOT / "integrations/workflow_mcp/agent_assets.py"
    ).read_bytes()


@pytest.mark.parametrize(
    "script",
    ["integrations/workflow_mcp/server.py", "plugins/abducer/scripts/workflow_mcp.py"],
)
def test_source_asset_rpc_runs_in_isolated_python_without_writing_reader_cache(
    tmp_path, script
):
    """The supported real transport must not depend on cwd, sys.path or writes."""
    entry = ROOT / script

    def cache_state():
        return {
            str(path): (path.stat().st_mtime_ns, path.stat().st_size)
            for path in entry.parent.glob("__pycache__/*")
            if path.is_file()
        }

    before = cache_state()
    path = "skills/orchestration/work/SKILL.md"
    results = exchange(
        entry,
        opening()
        + [
            request(1, "tools/call", {"name": "list_agent_assets"}),
            request(
                2,
                "tools/call",
                {"name": "read_agent_asset", "arguments": {"path": path}},
            ),
        ],
        tmp_path,
    )
    indexed = {row["id"]: row for row in results}
    assert not indexed[1]["result"]["isError"]
    manifest = json.loads(indexed[1]["result"]["content"][0]["text"])
    assert len(manifest["entries"]) == 100 and manifest["next_cursor"] == "100"
    assert not indexed[2]["result"]["isError"]
    asset = json.loads(indexed[2]["result"]["content"][0]["text"])
    assert asset["content"].encode() == (ROOT / path).read_bytes()
    assert asset["sha256"] == hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
    assert cache_state() == before
