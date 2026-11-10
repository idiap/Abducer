#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Read-only MCP stdio access to packaged normalized workflow contracts.

This small synchronous server implements only discovery and retrieval. It uses
the standard library so an installed plugin can start it with Python 3.11,
without installing a scientific runtime or an MCP SDK. The plugin generator
copies this source unchanged; do not maintain the packaged copy independently.
Asset RPCs read only exact manifest keys from a source-owned immutable snapshot.
No RPC accepts an arbitrary filesystem path, launches a workflow, or writes an artifact.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys

VERSIONS = ("2024-11-05", "2025-03-26", "2025-06-18", "2025-11-25")
LIMIT = 1024 * 1024
BOUNDARY = (
    "Draft, interface-only workflow contract. Normalized execution adapters are "
    "unavailable. Inspection does not execute, prove, approve, publish or promote "
    "anything. Native activation, evidence, budget and receipt gates still apply."
)


class RPCError(Exception):
    """Keep protocol errors distinct from retrieval errors returned by tools."""

    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code = code


def reject_constant(value: str):
    """JSON-RPC uses JSON numbers, which exclude NaN and infinities."""
    raise ValueError(f"Non-JSON numeric constant: {value}")


def default_catalog() -> Path:
    """Resolve a packaged server first, then this source-tree entry point."""
    package = Path(__file__).resolve().parents[1] / "workflows.json"
    if package.is_file():
        return package
    return Path(__file__).resolve().parents[2] / "plugins/abducer/workflows.json"


class WorkflowServer:
    """Serve one immutable in-memory inventory for the lifetime of a session."""

    def __init__(self, catalog: Path):
        self.catalog_path = catalog.resolve()
        self._assets = None
        payload = json.loads(catalog.read_text(encoding="utf-8"))
        if payload.get("schema_version") != "abducer.workflow-catalog/v1":
            raise ValueError("Unsupported workflow catalog")
        self.rows = payload["workflows"]
        self.version = payload["plugin_version"]
        self.by_id = {}
        for row in self.rows:
            identity = row["id"]
            if identity in self.by_id or row["contract"]["id"] != identity:
                raise ValueError("Duplicate or inconsistent workflow identity")
            if row["contract"]["schema_version"] != "workflow-skill/v1":
                raise ValueError("Unsupported workflow contract")
            self.by_id[identity] = row
        if not self.by_id:
            raise ValueError("Workflow catalog is empty")
        self.initialized = False
        self.ready = False

    def asset_catalog(self):
        """Freeze the declared closure only when a client requests source bytes.

        Installed routing-only plugins still support their original workflow
        inspection. Full byte export needs the catalog in its verified checkout
        layout; no current-directory, environment or ancestor search fills gaps.
        """
        if self._assets is not None:
            return self._assets
        root = self.catalog_path.parent.parent.parent
        if (
            self.catalog_path != root / "plugins/abducer/workflows.json"
            or not (root / "agentic/registries/skill_registry.yaml").is_file()
            or not (root / "pyproject.toml").is_file()
        ):
            raise ValueError(
                "Full asset export requires the Abducer source checkout; "
                "the installed routing catalog remains available for workflow inspection"
            )
        try:
            public = json.loads(
                (self.catalog_path.parent / "source-skills.json").read_text()
            )["skills"]
            skills = [row["source"] for row in public] + [
                "plugins/abducer/skills/" + row["entry"] + "/SKILL.md"
                for row in self.rows
            ]
            if len(set(skills)) != len(skills):
                raise ValueError("Duplicate public skill asset identity")
            # Isolated Python omits the script directory from sys.path. Load this
            # trusted sibling explicitly rather than adding arbitrary search roots.
            spec = importlib.util.spec_from_file_location(
                "abducer_mcp_agent_assets", Path(__file__).with_name("agent_assets.py")
            )
            if spec is None or spec.loader is None:
                raise ValueError("The packaged source asset reader is unavailable")
            helper = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(helper)
            snapshot = helper.AssetCatalog(
                root,
                skills=skills,
                workflows=[row["descriptor"] for row in self.rows],
                contracts=[(row["descriptor"], row["contract"]) for row in self.rows],
                source_files=[row["owner"] for row in self.rows],
            )
            # Native reads and the byte snapshot must describe the same source
            # revision, including private owners referenced by public workflows.
            expected = [(row["source"], row["sha256"]) for row in public]
            for row in self.rows:
                expected.extend(
                    [
                        (row["descriptor"], row["descriptor_sha256"]),
                        (row["owner"], row["owner_sha256"]),
                    ]
                )
            if any(
                snapshot.assets[path]["sha256"] != digest for path, digest in expected
            ):
                raise ValueError(
                    "Source assets changed; refresh the generated public catalogs"
                )
            self._assets = snapshot
            return snapshot
        except (OSError, ValueError, KeyError, TypeError) as error:
            raise ValueError(
                "Source asset snapshot unavailable: "
                + str(error).replace(str(root), "[source]")
            ) from None

    def summary(self, row: dict) -> dict:
        """Keep list responses compact while exposing lifecycle and aliases."""
        return {
            k: row[k]
            for k in (
                "id",
                "namespace",
                "version",
                "entry",
                "aliases",
                "owner",
                "descriptor",
                "lifecycle",
                "coverage",
            )
        }

    def get(self, identity: object) -> dict:
        if not isinstance(identity, str) or identity not in self.by_id:
            raise ValueError("Unknown canonical workflow ID")
        return self.by_id[identity]

    def uri(self, identity: str) -> str:
        return "abducer://workflows/" + identity

    def resource(self, row: dict) -> dict:
        return {
            "uri": self.uri(row["id"]),
            "name": row["id"],
            "description": BOUNDARY,
            "mimeType": "application/json",
        }

    def tools(self) -> list[dict]:
        annotations = {
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        }
        return [
            {
                "name": "list_workflows",
                "description": "List every normalized Abducer workflow and its native owner. "
                + BOUNDARY,
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False,
                },
                "annotations": annotations,
            },
            {
                "name": "get_workflow",
                "description": "Read one canonical workflow contract, source mapping and gaps. "
                + BOUNDARY,
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "workflow_id": {"type": "string", "enum": list(self.by_id)}
                    },
                    "required": ["workflow_id"],
                    "additionalProperties": False,
                },
                "annotations": annotations,
            },
            {
                "name": "list_agent_assets",
                "description": "List the immutable public skill/workflow source closure, with digest-checked byte reads and pagination. Inspection only.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "cursor": {"type": ["string", "null"], "pattern": "^[0-9]+$"}
                    },
                    "additionalProperties": False,
                },
                "annotations": annotations,
            },
            {
                "name": "read_agent_asset",
                "description": "Read one exact declared source asset from this session's immutable snapshot. Scripts are reference bytes, not execution grants.",
                "inputSchema": {
                    "type": "object",
                    "properties": {"path": {"type": "string", "minLength": 1}},
                    "required": ["path"],
                    "additionalProperties": False,
                },
                "annotations": annotations,
            },
        ]

    def request(self, method: str, params: dict) -> dict:
        """Implement the advertised MCP subset with lifecycle/argument checks."""
        if method == "initialize":
            if self.initialized:
                raise RPCError(-32600, "Already initialized")
            if (
                not isinstance(params.get("protocolVersion"), str)
                or not isinstance(params.get("capabilities"), dict)
                or not isinstance(params.get("clientInfo"), dict)
            ):
                raise RPCError(
                    -32602, "protocolVersion, capabilities and clientInfo required"
                )
            requested = params["protocolVersion"]
            self.initialized = True
            return {
                "protocolVersion": requested if requested in VERSIONS else VERSIONS[-1],
                "capabilities": {"tools": {}, "resources": {}, "prompts": {}},
                "serverInfo": {"name": "abducer-workflows", "version": self.version},
                "instructions": BOUNDARY,
            }
        if method == "ping":
            return {}
        if not self.ready:
            raise RPCError(-32002, "Complete initialization first")
        if method in {
            "tools/list",
            "resources/list",
            "prompts/list",
            "resources/templates/list",
        } and params.get("cursor"):
            raise RPCError(-32602, "No pagination cursor is supported")
        if method == "tools/list":
            return {"tools": self.tools()}
        if method == "tools/call":
            name, args = params.get("name"), params.get("arguments", {})
            if not isinstance(name, str) or name not in {
                "list_workflows",
                "get_workflow",
                "list_agent_assets",
                "read_agent_asset",
            }:
                raise RPCError(-32602, "Unknown tool")
            try:
                if not isinstance(args, dict):
                    raise ValueError("Invalid tool arguments")
                if name == "list_workflows" and not args:
                    value = {"workflows": [self.summary(r) for r in self.rows]}
                elif name == "get_workflow" and set(args) == {"workflow_id"}:
                    value = self.get(args["workflow_id"])
                elif name == "list_agent_assets" and set(args) <= {"cursor"}:
                    value = self.asset_catalog().list(args.get("cursor"))
                elif name == "read_agent_asset" and set(args) == {"path"}:
                    value = self.asset_catalog().read(args["path"])
                else:
                    raise ValueError("Invalid tool arguments")
                return {
                    "content": [
                        {"type": "text", "text": json.dumps(value, ensure_ascii=False)}
                    ],
                    "isError": False,
                }
            except ValueError as exc:
                return {
                    "content": [{"type": "text", "text": str(exc)}],
                    "isError": True,
                }
        if method == "resources/list":
            return {"resources": [self.resource(r) for r in self.rows]}
        if method == "resources/templates/list":
            return {"resourceTemplates": []}
        if method == "resources/read":
            uri = params.get("uri")
            row = next((r for r in self.rows if self.uri(r["id"]) == uri), None)
            if row is None:
                raise RPCError(-32002, "Unknown workflow resource")
            return {
                "contents": [
                    {
                        "uri": uri,
                        "mimeType": "application/json",
                        "text": json.dumps(row, ensure_ascii=False),
                    }
                ]
            }
        if method == "prompts/list":
            return {
                "prompts": [
                    {
                        "name": r["id"],
                        "description": "Inspect " + r["id"] + ". " + BOUNDARY,
                    }
                    for r in self.rows
                ]
            }
        if method == "prompts/get":
            try:
                row = self.get(params.get("name"))
            except ValueError as exc:
                raise RPCError(-32602, str(exc)) from exc
            if params.get("arguments") not in (None, {}):
                raise RPCError(-32602, "This inspection prompt takes no arguments")
            return {
                "description": BOUNDARY,
                "messages": [
                    {
                        "role": "user",
                        "content": {
                            "type": "text",
                            "text": "Inspect this source-bound workflow contract and explain its steps, native owner and unresolved gaps. "
                            + BOUNDARY
                            + "\n"
                            + json.dumps(row, ensure_ascii=False),
                        },
                    }
                ],
            }
        raise RPCError(-32601, "Method not found")

    def handle(self, message: object) -> dict | None:
        """Notifications never get replies; malformed requests do."""
        identity = message.get("id") if isinstance(message, dict) else None
        if (
            not isinstance(message, dict)
            or message.get("jsonrpc") != "2.0"
            or not isinstance(message.get("method"), str)
            or (
                "id" in message
                and (isinstance(identity, bool) or not isinstance(identity, (str, int)))
            )
        ):
            return {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32600, "message": "Invalid request"},
            }
        if "id" not in message:
            if message["method"] == "notifications/initialized" and self.initialized:
                self.ready = True
            return None
        try:
            params = message.get("params", {})
            if not isinstance(params, dict):
                raise RPCError(-32602, "params must be an object")
            return {
                "jsonrpc": "2.0",
                "id": identity,
                "result": self.request(message["method"], params),
            }
        except RPCError as exc:
            return {
                "jsonrpc": "2.0",
                "id": identity,
                "error": {"code": exc.code, "message": str(exc)},
            }


def main() -> int:
    # Discovery must also work when the source checkout is mounted read-only.
    sys.dont_write_bytecode = True
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=default_catalog())
    args = parser.parse_args()
    try:
        server = WorkflowServer(args.catalog)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Abducer MCP catalog unavailable: {exc}", file=sys.stderr)
        return 1
    # Newline-delimited UTF-8 JSON is the MCP stdio transport. stdout is
    # reserved exclusively for protocol messages, including on parse errors.
    while line := sys.stdin.buffer.readline(LIMIT + 1):
        if len(line) > LIMIT:
            while not line.endswith(b"\n"):
                line = sys.stdin.buffer.readline(LIMIT + 1)
                if not line:
                    break
            reply = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32600, "message": "Request exceeds 1 MiB"},
            }
        else:
            try:
                reply = server.handle(json.loads(line, parse_constant=reject_constant))
            except (ValueError, UnicodeDecodeError):
                reply = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": "Parse error"},
                }
        if reply is not None:
            print(json.dumps(reply, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
