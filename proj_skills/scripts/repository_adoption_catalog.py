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
"""Derive ownership navigation without replacing registries or granting execution.

Only reviewed operations in the linked sidecar are callable contracts. A Python
helper next to SKILL.md is evidence of a helper, not an invented skill entrypoint.
Domain-private names remain scoped so they cannot shadow the public registry.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OPERATIONS = "proj_skills/repository_adoption_operations.json"
PUBLIC_REGISTRY = "agentic/registries/skill_registry.yaml"
PROJECT_CATALOG = "proj_skills/catalog.yaml"
GENERATOR = "proj_skills/scripts/repository_adoption_catalog.py"
SCHEMA = "abducer.repository-adoption-catalog/v1"
FIXED_BINDINGS = {
    "validate-project-skills": ("proj_skills/scripts/validate_proj_skills.py", "proj_skills/scripts/repository_adoption_adapter.py"),
    **{name: ("proj_skills/scripts/repository_adoption_views.py", None) for name in ("render-history", "verify-view", "release-probe")},
}
ROOTS = ("skills", "proj_skills", "prism_me", "abducer-prism/skills")
PRUNED = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}


class CatalogError(ValueError):
    """Discovery ambiguity must be repaired rather than silently overwritten."""


def _json(root: Path, relative: str) -> dict:
    return json.loads((root / relative).read_text(encoding="utf-8"))


def _name(path: Path) -> str:
    """Read the scalar frontmatter name using the existing maintenance convention."""
    text = path.read_text(encoding="utf-8-sig")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise CatalogError(f"missing frontmatter: {path}")
    frontmatter = text[4:].split("\n---\n", 1)[0]
    names = [line.split(":", 1)[1].strip().strip("\"'") for line in frontmatter.splitlines() if line.startswith("name:")]
    if len(names) != 1 or not names[0]:
        raise CatalogError(f"missing or duplicate name: {path}")
    return names[0]


def _classification(relative: str) -> tuple[str | None, str]:
    """Excluded snapshots never enter public name lookup, even below skill roots."""
    for marker, kind in (("fixtures", "fixture"), ("examples", "fixture"), ("retired", "retired"), ("archive", "retired"), ("generated", "generated"), ("build", "generated"), ("dist", "generated")):
        if marker in Path(relative).parts[:-1]:
            return None, kind
    if relative.startswith("skills/domain_specific/"):
        domain = relative.split("/")[2]
        return f"cohere_fast/{domain}", "domain-private"
    for prefix in ROOTS:
        if relative.startswith(prefix + "/"):
            return prefix, "canonical"
    if relative.startswith(("external/", "agentic/external/")):
        return None, "vendored"
    if relative.startswith(".prism/"):
        return None, "request-local-reference"
    if "/retired/" in relative or "/archive/" in relative:
        return None, "retired"
    if "/fixtures/" in relative or "/examples/" in relative:
        return None, "fixture"
    if "/generated/" in relative or "/build/" in relative or "/dist/" in relative:
        return None, "generated"
    raise CatalogError(f"unclassified skill root: {relative}")


def _skill_paths(root: Path):
    """Inspect repository sources, skipping environment internals and symlink trees."""
    for parent, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in PRUNED and not (Path(parent) / d).is_symlink())
        if "SKILL.md" in files:
            yield Path(parent) / "SKILL.md"


def build_catalog(root: Path = ROOT) -> dict:
    """Build a deterministic projection and reject registry/path/name ambiguity."""
    root = root.resolve()
    registry = _json(root, PUBLIC_REGISTRY)["skills"]
    public: dict[str, dict] = {}
    public_names: set[str] = set()
    for row in registry:
        if row["path"] in public or row["name"] in public_names:
            raise CatalogError(f"duplicate public registry identity: {row['name']}")
        public[row["path"]] = row
        public_names.add(row["name"])
    projects = _json(root, PROJECT_CATALOG)["skills"]
    if len(projects) != len(set(projects)):
        raise CatalogError("duplicate project catalog identity")
    sidecar = _json(root, OPERATIONS)
    if sidecar.get("schema_version") != "abducer.repository-adoption-operations/v1":
        raise CatalogError("unsupported operation sidecar version")
    operation_ids: set[str] = set()
    for operation in sidecar["operations"]:
        identity = operation["operation_id"]
        if identity in operation_ids:
            raise CatalogError(f"duplicate operation identity: {identity}")
        operation_ids.add(identity)
    for operation in sidecar["operations"]:
        identity = operation["operation_id"]
        required = {"operation_id", "owner", "implementation", "adapter", "invocation_mode", "input_contract", "output_contract", "side_effects", "provenance"}
        if set(operation) != required:
            raise CatalogError(f"invalid operation fields: {identity}")
        if identity not in FIXED_BINDINGS or (operation["implementation"], operation["adapter"]) != FIXED_BINDINGS[identity]:
            raise CatalogError(f"unknown or changed fixed operation binding: {identity}")
        if operation["owner"] != "proj_skills" or operation["invocation_mode"] != "cli" or not isinstance(operation["input_contract"], dict) or not isinstance(operation["output_contract"], dict):
            raise CatalogError(f"invalid operation contract: {identity}")
        for key in ("implementation", "adapter"):
            value = operation.get(key)
            if value is not None and (Path(value).is_absolute() or ".." in Path(value).parts or not (root / value).is_file()):
                raise CatalogError(f"invalid operation {key}: {value}")
    skills, excluded = [], []
    seen: set[str] = set()
    observed_public, observed_projects = set(), set()
    for path in sorted(_skill_paths(root)):
        relative = path.relative_to(root).as_posix()
        namespace, disposition = _classification(relative)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if namespace is None:
            excluded.append({"path": relative, "disposition": disposition, "sha256": digest, "reason": "Reference or derived source; not a canonical discovery root."})
            continue
        if path.is_symlink():
            raise CatalogError(f"canonical skill must not be a symlink: {relative}")
        name = _name(path)
        identity = f"{namespace}:{name}"
        if identity in seen:
            raise CatalogError(f"duplicate scoped skill identity: {identity}")
        seen.add(identity)
        directory = path.parent.relative_to(root).as_posix()
        authority = relative
        if namespace == "skills":
            if directory not in public or public[directory]["name"] != name:
                raise CatalogError(f"public registry/discovery disagreement: {relative}")
            observed_public.add(directory)
            authority = PUBLIC_REGISTRY
        elif namespace == "proj_skills":
            if name not in projects or path.parent.name != name:
                raise CatalogError(f"project catalog/discovery disagreement: {relative}")
            observed_projects.add(name)
            authority = PROJECT_CATALOG
        helpers = sorted(p.relative_to(root).as_posix() for p in (path.parent / "scripts").rglob("*.py")) if (path.parent / "scripts").is_dir() else []
        skills.append({
            "skill_id": identity, "name": name, "path": relative, "owner": namespace,
            "disposition": disposition, "invocation_mode": "instruction",
            "implementation_kind": "instruction-with-helpers" if helpers else "instruction-only",
            "operation_ids": [], "helper_sources": helpers,
            "input_contract": {"source": relative, "binding": "instruction-defined; no inferred callable signature"},
            "output_contract": {"source": relative, "binding": "instruction-defined; no execution attestation"},
            "source_sha256": digest,
            "field_provenance": {
                "name": relative + "#frontmatter.name", "path": "filesystem discovery",
                "skill_id/owner/disposition": GENERATOR + "#_classification",
                "invocation_mode/implementation_kind/operation_ids": "instruction discovery only; reviewed callable operations live in " + OPERATIONS,
                "helper_sources": "filesystem scripts/*.py; not operation registrations",
                "canonical_authority": authority,
                "input_contract/output_contract": relative,
                "source_sha256": "SHA-256 of original SKILL.md bytes",
            },
        })
    if set(public) != observed_public:
        raise CatalogError(f"registry paths not discovered: {sorted(set(public) - observed_public)}")
    if set(projects) != observed_projects:
        raise CatalogError(f"project skills not discovered: {sorted(set(projects) - observed_projects)}")
    return {"schema_version": SCHEMA, "generator": GENERATOR, "operation_registry": OPERATIONS,
            "canonical_roots": list(ROOTS), "pruned_environment_directories": sorted(PRUNED),
            "skills": skills, "excluded_sources": excluded, "operations": sidecar["operations"]}


def render_markdown(catalog: dict) -> str:
    """Explain the navigation's limits before presenting canonical ownership links."""
    lines = ["# Repository adoption catalog", "", "Generated ownership navigation for maintainers; regenerate with", "`python3 proj_skills/scripts/repository_adoption_catalog.py --write` and check with `--check`.", "Existing registries retain lookup authority. Scoped IDs distinguish domain-private names;", "they do not add public aliases or grant activation, execution, scientific, or promotion authority.", "Instruction contracts point to source documents; nearby helpers are never inferred callables.", "Excluded sources remain reference material. Environment/cache directories are explicitly pruned in the JSON view.", "", "## Registered pilot operations", "", "| Operation | Existing owner implementation | Invocation |", "| --- | --- | --- |"]
    for op in catalog["operations"]:
        lines.append(f"| `{op['operation_id']}` | [{op['implementation']}](../../{op['implementation']}) | {op['invocation_mode']} |")
    lines += ["", "## Canonical skill ownership", "", "| Scoped identity | Source contract | Disposition | Implementation |", "| --- | --- | --- | --- |"]
    for row in catalog["skills"]:
        lines.append(f"| `{row['skill_id']}` | [{row['name']}](../../{row['path']}) | {row['disposition']} | {row['implementation_kind']} |")
    lines += ["", "## Excluded reference sources", "", "These entries are accounted for but never installed or exposed as canonical operations.", "", "| Source | Disposition |", "| --- | --- |"]
    for row in catalog["excluded_sources"]:
        lines.append(f"| `{row['path']}` | {row['disposition']} |")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    """Regenerate only this optional projection, or detect stale checked-in views."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=ROOT)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    try:
        catalog = build_catalog(args.repository_root)
    except (CatalogError, OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"catalog error: {exc}\n")
    outputs = {"json": json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", "md": render_markdown(catalog)}
    for extension, content in outputs.items():
        target = args.repository_root / f"docs/generated/repository-adoption-catalog.{extension}"
        if args.write:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        elif args.check and (not target.is_file() or target.read_text(encoding="utf-8") != content):
            parser.exit(1, f"stale generated catalog: {target}\n")
    print(f"catalog: {len(catalog['skills'])} canonical skills; {len(catalog['excluded_sources'])} excluded sources; {len(catalog['operations'])} pilot operations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
