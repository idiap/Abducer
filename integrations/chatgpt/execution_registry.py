# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Native execution admission and inspectable declared dependency manifests.

Normalized workflow contracts describe interfaces; they do not grant execution.
This registry names the separately implemented adapter and exposes real native
entrypoints for the remaining workflows without pretending they are runnable.
The existing MCP asset reader supplies immutable source bytes. Dependency
traversal is static and explicit: it never imports a research module, reads run
outputs, or interprets a source reference as authority to execute it.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import unquote, urlsplit

import yaml
from markdown_it import MarkdownIt

from integrations.workflow_mcp.agent_assets import AssetCatalog

from .catalog import Catalog, CONTRACT_ID, TARGETS

NATIVE_EVENTS = (
    "UserPromptSubmit",
    "PreSkillUse",
    "PostSkillUse",
    "PreToolUse",
    "Stop",
)
TASK_REGISTRIES = {
    CONTRACT_ID: "registry/tasks/discovery-marathon/task_registry.json",
    "conceptual_hypothesis_exploration_workflow": "registry/tasks/hegelian-abducer-integration/task_registry.json",
    "cohere_fast_workflow": "registry/tasks/cohere-fast/task_registry.json",
}
SOURCE_PREFIXES = (
    "skills/",
    "proj_skills/",
    "prism_me/",
    "hooks/",
    "registry/",
    "agentic/scripts/",
    "agentic/spec/",
    "agentic/registries/",
    "agentic/orchestration/",
    "agentic/discovery/",
    "agentic/reasoning_flows/",
    "integrations/",
    "docs/",
    "abducer-prism/",
)
ROOT_SOURCES = {"pyproject.toml", "uv.lock", "README.md"}
SOURCE_SUFFIXES = {".py", ".md", ".json", ".yaml", ".yml", ".toml", ".prism"}
LINK = re.compile(r"\]\((?:<([^>]+)>|([^\s)]+))")
CODE = re.compile(r"`([^`\n]+)`")


class ExecutionRegistry:
    """Describe every catalog entry while admitting only registered adapters.

    ``runtime_enabled`` is trusted operator readiness, not a client parameter.
    It must only be true after the server checks worker/provider availability.
    This class does not certify model quality or imply full lifecycle parity.
    """

    def __init__(self, root: Path, *, catalog: Catalog | None = None):
        self.root = Path(root).resolve(strict=True)
        self.catalog = catalog or Catalog(self.root)
        if self.catalog.root != self.root:
            raise ValueError("Execution registry and catalog roots differ")
        self._aliases: dict[str, str] = {}
        for row in self.catalog.native.rows:
            for name in [row["id"], *row.get("aliases", [])]:
                if name in self._aliases and self._aliases[name] != row["id"]:
                    raise ValueError("Ambiguous native workflow alias")
                self._aliases[name] = row["id"]
        self._assets = None
        self._manifests: dict[str, dict] = {}
        self._imports: dict[str, set[str]] = {}
        self._references: dict[str, list[tuple[str, bool]]] = {}
        self._skill_directories: set[str] = set()
        self._markdown = MarkdownIt("commonmark")

    def _row(self, identity: str) -> dict:
        if not isinstance(identity, str) or identity not in self._aliases:
            raise ValueError("Unknown canonical workflow")
        return self.catalog.native.by_id[self._aliases[identity]]

    def get(self, workflow_id: str, *, runtime_enabled: bool = False) -> dict:
        """Expose coverage without upgrading interface YAML into executable code."""
        row = self._row(workflow_id)
        identity = row["id"]
        native = row["contract"]["extensions"]["abducer.native_identity"]["id"]
        result = {
            "workflow_id": identity,
            "native_id": native,
            "owner": row["owner"],
            "execution_status": "not-qualified",
            "execution_mode": "unqualified",
            "native_execution": False,
            "adapter_available": False,
            "entrypoints": [{"path": row["owner"], "kind": "agent_skill"}],
            "reason": "No separately qualified hosted adapter is registered for this native procedure.",
            "required_hook_events": list(NATIVE_EVENTS),
            "hook_policy": "native hooks/hooks.json; optional workflow_local policies are separate",
            "scientific_truth_verified": False,
        }
        if identity == CONTRACT_ID:
            result.update(
                execution_status=(
                    "executable" if runtime_enabled else "requires-runtime"
                ),
                execution_mode="native-adapter",
                native_execution=bool(runtime_enabled),
                adapter_available=True,
                adapter_module="integrations/domain_package/marathon_runtime.py",
                targets=list(TARGETS),
                reason="Existing prepare/execute/verify adapter; a configured worker and model provider are required.",
            )
            result["entrypoints"].append(
                {
                    "path": "integrations/domain_package/marathon_runtime.py",
                    "kind": "native_adapter",
                    "symbols": ["prepare", "execute", "verify"],
                }
            )
        elif identity == "conceptual_hypothesis_exploration_workflow":
            result.update(
                execution_status="agent-driven",
                execution_mode="agent-driven",
                bounded_operations=["validate_hypothesis_map"],
                reason="The creative workflow requires authored candidates and validation evidence. Deterministic map construction and validation are not autonomous abduction.",
            )
            result["entrypoints"].extend(
                [
                    {
                        "path": "agentic/scripts/build_hypothesis_exploration_map.py",
                        "kind": "deterministic_builder",
                    },
                    {
                        "path": "agentic/scripts/validate_hypothesis_exploration.py",
                        "kind": "validator",
                    },
                ]
            )
        elif identity.startswith("cohere_fast"):
            result.update(
                execution_status="agent-driven",
                execution_mode="agent-driven",
                bounded_operations=["run_cohere_fast_authored_packets"],
                reason="The native runner needs explicit domain activation and an executor supplying real child packets. Domain feature flags and independent-audit gates remain required.",
            )
            result["entrypoints"].append(
                {
                    "path": "agentic/orchestration/cohere_fast_runner.py",
                    "kind": "native_orchestrator",
                    "symbol": "CohereFastRunner.run",
                    "requires": "explicit activation receipt and child executor",
                }
            )
        return result

    def list(self, *, runtime_enabled: bool = False) -> dict:
        """Return all workflows, including honest non-executable coverage."""
        return {
            "release": self.catalog.release,
            "workflows": [
                self.get(row["id"], runtime_enabled=runtime_enabled)
                for row in self.catalog.native.rows
            ],
        }

    def require_native(self, workflow_id: str) -> dict:
        """Resolve an allowlisted native adapter; caller still checks readiness."""
        descriptor = self.get(workflow_id)
        if not descriptor["adapter_available"]:
            raise ValueError(
                "Workflow has no qualified native adapter: " + descriptor["reason"]
            )
        return descriptor

    def _asset_catalog(self):
        if self._assets is None:
            # Hosted runtime snapshots carry canonical procedures and generated
            # catalogs, but intentionally omit generated client routing stubs.
            # Reuse the same byte reader with the canonical inventory directly.
            rows = self.catalog.native.rows
            snapshot = AssetCatalog(
                self.root,
                skills=[row["source"] for row in self.catalog.skills],
                workflows=[row["descriptor"] for row in rows],
                contracts=[(row["descriptor"], row["contract"]) for row in rows],
                source_files=[row["owner"] for row in rows],
            )
            expected = [(row["source"], row["sha256"]) for row in self.catalog.skills]
            for row in rows:
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
                    "Source dependency assets changed after catalog verification"
                )
            self._assets = snapshot
            self._skill_directories.update(
                str(PurePosixPath(row["source"]).parent) for row in self.catalog.skills
            )
        return self._assets

    def _source_path(
        self, reference: str, parent: str, *, markdown_link: bool = False
    ) -> str | None:
        """Resolve source references while excluding output and private-input trees."""
        uri = urlsplit(reference)
        if uri.scheme or uri.netloc or uri.query or not uri.path:
            return None
        raw = unquote(uri.path)
        # Conversion outputs are authored during a run, not installable source.
        if raw.startswith("conversion/"):
            return None
        if any(marker in raw for marker in ("<", ">", "{", "}", "*")) or raw.startswith(
            (".codex/", ".prism/")
        ):
            return None
        if "\\" in raw or "\0" in raw or Path(raw).is_absolute():
            raise ValueError("Dependency reference is not a confined relative path")
        relative = self.root / PurePosixPath(parent).parent / raw
        if markdown_link and relative.is_file():
            path = relative
        elif (
            raw.startswith(
                SOURCE_PREFIXES
                + (
                    "agentic/",
                    "artifacts/",
                    "KB/",
                    "InformalMathLib/",
                    "config/",
                    "external/",
                    "output/",
                    "phyp/",
                    "tests/",
                )
            )
            or raw in ROOT_SOURCES
        ):
            path = self.root / raw
        else:
            path = self.root / PurePosixPath(parent).parent / raw
        resolved = path.resolve()
        if not resolved.is_relative_to(self.root):
            raise ValueError("Dependency reference escapes source root")
        logical = resolved.relative_to(self.root).as_posix()
        if not (logical.startswith(SOURCE_PREFIXES) or logical in ROOT_SOURCES):
            return None
        return logical

    def _python_imports(self, path: str, content: str) -> set[str]:
        """Follow local static imports without running Python module code."""
        if path in self._imports:
            return set(self._imports[path])
        found = set()
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return found
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
                bases = [self.root, self.root / PurePosixPath(path).parent]
            elif isinstance(node, ast.ImportFrom):
                modules = [node.module] if node.module else []
                modules.extend(
                    ".".join(filter(None, [node.module, alias.name]))
                    for alias in node.names
                    if alias.name != "*"
                )
                base = self.root / PurePosixPath(path).parent
                for _ in range(max(0, node.level - 1)):
                    base = base.parent
                bases = [base] if node.level else [self.root, base]
            else:
                continue
            for module in modules:
                for base in bases:
                    target = base.joinpath(*module.split("."))
                    for candidate in [
                        target.with_suffix(".py"),
                        target / "__init__.py",
                    ]:
                        if candidate.is_file() and candidate.resolve().is_relative_to(
                            self.root
                        ):
                            relative = candidate.relative_to(self.root).as_posix()
                            if relative.startswith(SOURCE_PREFIXES):
                                found.add(relative)
        self._imports[path] = found
        return set(found)

    def _markdown_references(self, path: str, content: str) -> list[tuple[str, bool]]:
        """Read actual links/inline paths, excluding fenced code and type syntax."""
        if path not in self._references:
            refs = []
            inline_paths = path.endswith("/SKILL.md") or (
                path.startswith("skills/") and "/references/" in path
            )
            for block in self._markdown.parse(content):
                for token in block.children or []:
                    if token.type == "link_open":
                        refs.append((token.attrGet("href"), True))
                    elif inline_paths and token.type == "code_inline":
                        value = token.content
                        if (
                            " " not in value
                            and "/" in value
                            and PurePosixPath(value).suffix in SOURCE_SUFFIXES
                        ):
                            refs.append((value, False))
            self._references[path] = refs
        return self._references[path]

    def dependency_manifest(self, workflow_id: str) -> dict:
        """Audit declared sources, skill resources and static source dependencies.

        This is an inspectable dependency manifest, not a claim that arbitrary
        dynamic imports or run inputs can be inferred. The actual executor uses
        its full verified runtime snapshot and checks invocation prerequisites.
        """
        row = self._row(workflow_id)
        identity = row["id"]
        if identity in self._manifests:
            return copy.deepcopy(self._manifests[identity])
        assets = self._asset_catalog()
        seed = {
            row["owner"],
            row["descriptor"],
            "hooks/hooks.json",
            "pyproject.toml",
            "uv.lock",
        }
        seed.update(
            source["path"] for source in row["contract"]["provenance"]["sources"]
        )
        seed.update(entry["path"] for entry in self.get(identity)["entrypoints"])
        task = TASK_REGISTRIES.get(identity)
        if identity.startswith("cohere_fast"):
            task = TASK_REGISTRIES["cohere_fast_workflow"]
            seed.update(
                {
                    "hooks/scripts/cohere_fast_intake.py",
                    "hooks/scripts/cohere_fast_policy.py",
                    "agentic/registries/domain_skill_bundles.yaml",
                    "agentic/spec/cohere_fast_artifacts.schema.json",
                }
            )
        registered = json.loads(
            (self.root / "agentic/registries/skill_registry.yaml").read_text()
        )
        skill_paths = {
            s["name"]: s["path"].rstrip("/") + "/SKILL.md" for s in registered["skills"]
        }
        skill_paths.update({s["name"]: s["source"] for s in self.catalog.skills})
        if identity.startswith("cohere_fast"):
            domains = yaml.safe_load(
                (self.root / "agentic/registries/domain_skill_bundles.yaml").read_text()
            )
            for bundle in domains["bundles"]:
                for name in bundle.get("allowed_skills", []):
                    if name in skill_paths:
                        seed.add(skill_paths[name])
        if task:
            seed.add(task)
            task_data = json.loads((self.root / task).read_text())
            for workflow in task_data.get("visible_workflows", []):
                for name in workflow.get("composed_skills", []):
                    if name in skill_paths:
                        seed.add(skill_paths[name])
        hook_config = json.loads((self.root / "hooks/hooks.json").read_text())
        seed.update(hook["script"] for hook in hook_config["hooks"])
        seed.add("hooks/scripts/hook_utils.py")
        visited, issues, resolutions = set(), [], []
        pending = list(sorted(seed))
        while pending:
            path = pending.pop()
            if path in visited:
                continue
            visited.add(path)
            try:
                # The shared reader rejects credentials, missing files and
                # escaping symlinks. Do not substitute current run artifacts.
                assets.add(assets.relative(path))
                asset = assets.assets[path]
                if path.endswith("/SKILL.md"):
                    directory = str(PurePosixPath(path).parent)
                    if directory not in self._skill_directories:
                        assets.directory(self.root / directory, frozenset())
                        self._skill_directories.add(directory)
                    prefix = str(PurePosixPath(path).parent) + "/"
                    pending.extend(
                        p
                        for p in assets.assets
                        if p.startswith(prefix) and p not in visited
                    )
                if asset["encoding"] != "text":
                    continue
                content = asset["content"]
                if path.endswith(".py"):
                    pending.extend(self._python_imports(path, content) - visited)
                if path.endswith(".md"):
                    for reference, markdown_link in self._markdown_references(
                        path, content
                    ):
                        dependency = self._source_path(
                            reference, path, markdown_link=markdown_link
                        )
                        # Resolve legacy skill/script spellings through the
                        # canonical skill directory, with recorded provenance.
                        parts = PurePosixPath(reference).parts
                        if (
                            dependency
                            and not (self.root / dependency).is_file()
                            and len(parts) == 2
                            and parts[0] in skill_paths
                        ):
                            relocated = str(
                                PurePosixPath(skill_paths[parts[0]]).parent
                                / "scripts"
                                / parts[1]
                            )
                            if (self.root / relocated).is_file():
                                resolutions.append(
                                    {
                                        "from": dependency,
                                        "to": relocated,
                                        "authority": "canonical_skill_scripts",
                                    }
                                )
                                dependency = relocated
                        # Preserve the authored reference and expose an explicit
                        # relocation through the canonical skill registry.
                        if (
                            dependency
                            and not (self.root / dependency).is_file()
                            and dependency.endswith("/SKILL.md")
                        ):
                            skill_name = PurePosixPath(dependency).parent.name
                            relocated = skill_paths.get(skill_name)
                            if relocated and (self.root / relocated).is_file():
                                resolutions.append(
                                    {
                                        "from": dependency,
                                        "to": relocated,
                                        "authority": "canonical_skill_registry",
                                    }
                                )
                                dependency = relocated
                        if dependency and dependency not in visited:
                            pending.append(dependency)
                if path.endswith(".json"):
                    try:
                        raw = json.loads(content)
                    except json.JSONDecodeError:
                        continue

                    def schema_refs(value):
                        if isinstance(value, dict):
                            ref = value.get("$ref")
                            if isinstance(ref, str) and not ref.startswith("#"):
                                dependency = self._source_path(ref, path)
                                if dependency:
                                    pending.append(dependency)
                            for child in value.values():
                                schema_refs(child)
                        elif isinstance(value, list):
                            for child in value:
                                schema_refs(child)

                    schema_refs(raw)
            except (OSError, ValueError) as error:
                issues.append(
                    {
                        "path": path,
                        "reason": str(error).replace(str(self.root), "[source]"),
                    }
                )
        entries = [
            {
                "path": path,
                "sha256": assets.assets[path]["sha256"],
                "encoding": assets.assets[path]["encoding"],
            }
            for path in sorted(visited)
            if path in assets.assets
        ]
        material = {
            "workflow_id": identity,
            "entries": entries,
            "issues": sorted(issues, key=lambda issue: issue["path"]),
            "resolved_references": sorted(
                {
                    json.dumps(value, sort_keys=True): value for value in resolutions
                }.values(),
                key=lambda value: value["from"],
            ),
        }
        manifest = {
            **material,
            "schema_version": "abducer.execution-dependencies/v1",
            "release": self.catalog.release,
            "manifest_sha256": hashlib.sha256(
                json.dumps(material, sort_keys=True).encode()
            ).hexdigest(),
            "declared_sources_complete": not issues,
            "runtime_closure_verified": False,
            "scope": "Declared sources, complete referenced skill directories, static local Python imports and JSON Schema references; dynamic imports and research inputs require runtime checks.",
        }
        self._manifests[identity] = manifest
        return copy.deepcopy(manifest)

    def read_dependency(
        self, workflow_id: str, path: str, *, offset: int = 0, limit: int = 16000
    ) -> dict:
        """Read only an exact declared asset key with bounded source pagination."""
        if (
            type(offset) is not int
            or offset < 0
            or type(limit) is not int
            or not 1 <= limit <= 16000
        ):
            raise ValueError("Invalid dependency page")
        manifest = self.dependency_manifest(workflow_id)
        allowed = {entry["path"] for entry in manifest["entries"]}
        if not isinstance(path, str) or path not in allowed:
            raise ValueError("Asset is not declared for this workflow")
        asset = self._asset_catalog().read(path)
        content = asset["content"]
        if offset > len(content):
            raise ValueError("Dependency offset exceeds source length")
        end = min(len(content), offset + limit)
        return {
            **{key: value for key, value in asset.items() if key != "content"},
            "workflow_id": manifest["workflow_id"],
            "release": self.catalog.release,
            "manifest_sha256": manifest["manifest_sha256"],
            "content": content[offset:end],
            "offset": offset,
            "total": len(content),
            "next_offset": end if end < len(content) else None,
        }
