#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Generate flat plugin entry skills without duplicating Abducer's runtime.

The public inventory deliberately matches agentic_common.iter_skill_dirs.
Deeper domain-private skills share names with public skills and must remain
behind their workflow's receipt gate. Generated adapters resolve the original
checkout rather than executing relative to a host-managed installation cache.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
import tomllib

import yaml
from reuse.global_licensing import AnnotationsItem

ROOT = Path(__file__).resolve().parents[2]
PLUGIN = Path("plugins/abducer")
WORKFLOWS = Path("agentic/reasoning_flows/workflow_skill_v1")


def json_bytes(value: object) -> bytes:
    """Keep manifests and inventories reproducible across platforms."""
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def public_skills(root: Path) -> list[dict[str, str]]:
    """Reject ambiguous public identities before any output is written."""
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for path in sorted((root / "skills").glob("*/*/SKILL.md")):
        content = path.read_bytes()
        text = content.decode("utf-8-sig")
        match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", text, re.S)
        if not match:
            raise ValueError(f"Missing frontmatter: {path}")
        frontmatter = yaml.safe_load(match.group(1))
        name = frontmatter.get("name")
        description = frontmatter.get("description")
        if (
            not isinstance(name, str)
            or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)
            or len(name) > 64
            or name != path.parent.name
            or name in seen
        ):
            raise ValueError(f"Invalid or duplicate skill identity: {path}")
        if (
            not isinstance(description, str)
            or not description.strip()
            or len(description) > 1024
        ):
            raise ValueError(f"Missing or oversized description: {path}")
        seen.add(name)
        rows.append(
            {
                "name": name,
                "description": description,
                "source": path.relative_to(root).as_posix(),
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        )
    if not rows:
        raise ValueError("No public Abducer skills found")
    return sorted(rows, key=lambda row: row["name"])


def adapter(row: dict[str, str]) -> bytes:
    """Expose source metadata while loading the actual procedure on demand."""
    frontmatter = yaml.safe_dump(
        {"name": row["name"], "description": row["description"]},
        sort_keys=False,
        allow_unicode=True,
        width=1000,
    )
    body = f"""# {row["name"]}

This entry uses the canonical Abducer skill `{row["source"]}` in a writable
Abducer checkout. The installed plugin contains routing instructions, not the
research runtime.

1. Locate this installed SKILL.md, then run the read-only resolver beside the
   plugin: `python3 "<this-skill-directory>/../../scripts/resolve_checkout.py"
   --skill {row["name"]}`. It uses `ABDUCER_ROOT` when set, otherwise searches
   the current directory and its parents. An explicit checkout can be passed
   with `--root "/path/to/abducer"`. Quote paths, including paths with spaces.
2. If resolution fails, stop this route and report the resolver's error. Request
   a checkout path or the documented runtime setup; do not fabricate outputs.
3. Read the returned `skill_file` in full. Follow that canonical procedure and
   resolve its relative scripts and references from its original skill directory.
4. Execute repository-relative commands with the returned `root` as working
   directory. Preserve the source skill's target, budget, evidence, claim-status
   and validation gates. Write research artifacts only in the selected checkout,
   never in the installed plugin cache.

When the procedure names a public companion skill, use the matching entry in
this plugin, or read its canonical source in the same checkout. Domain-private
skills remain accessible only through their canonical activation procedure;
generic domain prose does not authorize an opt-in workflow.
"""
    return ("---\n" + frontmatter + "---\n\n" + body).encode()


def workflow_catalog(root: Path) -> list[dict]:
    """Expose every normalized identity, including support and private owners.

    Exposure licenses contract inspection only. Native activation requirements
    remain in the descriptor and canonical owning skill. A missing index is an
    error, so deleting the normalization cannot silently remove all workflows.
    """
    index = yaml.safe_load((root / WORKFLOWS / "index.yaml").read_text())
    rows = []
    names = set()
    for item in index["workflows"]:
        paths = {}
        for key in ("descriptor", "owner"):
            path = (root / item[key]).resolve()
            if not path.is_relative_to(root.resolve()) or not path.is_file():
                raise ValueError(f"Missing or escaped workflow {key}: {item[key]}")
            paths[key] = path
        raw = paths["descriptor"].read_bytes()
        contract = yaml.safe_load(raw)
        if any(item[key] != contract[key] for key in ("namespace", "id", "version")):
            raise ValueError("Workflow index identity differs from descriptor")
        if item["owner"] != contract["extensions"]["abducer.owner"]["path"]:
            raise ValueError("Workflow index owner differs from descriptor")
        # A stable prefix avoids collisions with native skills such as
        # pvsnp-forcedrows-proof-workflow while keeping both entry points.
        entry = "workflow-" + item["id"].removesuffix("_workflow").replace("_", "-")
        if (
            not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", entry)
            or len(entry) > 64
            or entry in names
        ):
            raise ValueError(f"Invalid or ambiguous workflow entry: {entry}")
        names.add(entry)
        rows.append(
            {
                **{
                    key: item[key]
                    for key in (
                        "namespace",
                        "id",
                        "version",
                        "aliases",
                        "owner",
                        "descriptor",
                    )
                },
                "entry": entry,
                "descriptor_sha256": hashlib.sha256(raw).hexdigest(),
                "owner_sha256": hashlib.sha256(paths["owner"].read_bytes()).hexdigest(),
                "lifecycle": contract["lifecycle"],
                "coverage": contract["provenance"]["coverage"],
                "contract": contract,
            }
        )
    if not rows:
        raise ValueError("Normalized workflow inventory is empty")
    return sorted(rows, key=lambda row: row["entry"])


def workflow_adapter(row: dict) -> bytes:
    """Create a client-safe hyphenated entry without renaming native IDs."""
    frontmatter = yaml.safe_dump(
        {
            "name": row["entry"],
            "description": f"Inspect the {row['id']} workflow contract, native steps, source owner and unresolved execution gaps. Use when this normalized workflow or its source mapping is requested; native execution retains its original activation gates.",
        },
        sort_keys=False,
        width=1000,
    )
    body = f"""# {row["id"]}

This entry exposes `{row["namespace"]}:{row["id"]}@{row["version"]}`.
The packaged `../../workflows.json` contains its complete contract. The MCP
`get_workflow` tool, resource `abducer://workflows/{row["id"]}` and prompt
`{row["id"]}` expose the same contract without requiring a checkout.

To inspect the canonical checkout source, run:
`python3 "<this-skill-directory>/../../scripts/resolve_checkout.py"
--workflow {row["id"]}`. Set `ABDUCER_ROOT` or add `--root "/path/to/abducer"`
when outside the checkout. Read the returned `workflow_file` and `skill_file`
in full; resolve relative paths from those original source directories.

This contract is draft and interface-only. Normalized execution adapters are
unavailable. Explain source steps, conditions, artifacts, authority and gaps;
do not treat inspection as workflow execution or approval. Stop checkout routing
if resolution fails and report its setup/version error; the packaged contract
remains available for inspection.

If the user explicitly requests native execution, follow the canonical owning
skill `{row["owner"]}` in the resolved checkout and preserve its activation,
target, domain receipt, budget and evidence gates. Loading this entry does not
satisfy opt-in or private-domain prerequisites. Write research artifacts only
in the checkout, never in the installed plugin cache. No normalized adapter,
scientific validity, proof, publication or promotion authority is added here.
"""
    return ("---\n" + frontmatter + "---\n\n" + body).encode()


def package_reuse(root: Path, managed_paths) -> bytes:
    """Project repository attribution into the independently installed package.

    The root REUSE.toml is the reviewed attribution source. Preserve its exact
    per-file contributor sets instead of assigning every generated skill to a
    guessed author or depending on metadata outside the installed package.
    """
    source = root / "REUSE.toml"
    rules = (
        tomllib.loads(source.read_text()).get("annotations", [])
        if source.exists()
        else []
    )
    compiled = [(rule, AnnotationsItem.from_dict(rule)) for rule in rules]
    grouped = {}
    for path in sorted(managed_paths):
        if not path.is_relative_to(PLUGIN) or (
            path.name != "SKILL.md" and path.suffix != ".json"
        ):
            continue
        fields = {}
        for rule, matcher in compiled:
            if matcher.matches(path.as_posix()):
                for key, value in rule.items():
                    if key.startswith("SPDX-"):
                        fields.setdefault(key, set()).update(
                            [value] if isinstance(value, str) else value
                        )
        if not fields:
            fields = {
                "SPDX-FileCopyrightText": {
                    "© 2026 Idiap Research Institute <contact@idiap.ch>"
                },
                "SPDX-License-Identifier": {"MIT"},
            }
        normalized = {k: sorted(v) for k, v in sorted(fields.items()) if v}
        signature = json.dumps(normalized, ensure_ascii=False, sort_keys=True)
        grouped.setdefault(signature, []).append(path.relative_to(PLUGIN).as_posix())
    existing = root / PLUGIN / "REUSE.toml"
    header = (
        existing.read_text().split("version =", 1)[0]
        if existing.exists()
        else "# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>\n# SPDX-License-Identifier: MIT\n"
    )
    lines = [header.rstrip(), "version = 1", ""]
    for signature, paths in sorted(grouped.items(), key=lambda pair: pair[1][0]):
        lines += [
            "[[annotations]]",
            "path = [",
            *("  " + json.dumps(path, ensure_ascii=False) + "," for path in paths),
            "]",
            'precedence = "aggregate"',
        ]
        lines += [
            json.dumps(key) + " = " + json.dumps(value, ensure_ascii=False)
            for key, value in json.loads(signature).items()
        ]
        lines.append("")
    return ("\n".join(lines)).encode()


def expected_files(root: Path = ROOT) -> dict[Path, bytes]:
    """Build the full managed file set; all catalog paths stay inside the repo."""
    metadata = json.loads(
        (root / "integrations/agent_plugins/metadata.json").read_text()
    )
    rows = public_skills(root)
    workflows = workflow_catalog(root)
    if {r["name"] for r in rows} & {r["entry"] for r in workflows}:
        raise ValueError("Workflow entry collides with a public skill")
    files = {
        PLUGIN / "LICENSES/MIT.txt": (root / "LICENSES/MIT.txt").read_bytes(),
        PLUGIN / "LICENSE": (root / "LICENSES/MIT.txt")
        .read_text()
        .replace(
            "Copyright (c) <year> <copyright holders>",
            "© 2026 Idiap Research Institute <contact@idiap.ch>",
        )
        .encode(),
        PLUGIN / "plugin.json": json_bytes(
            {
                "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
                **metadata,
            }
        ),
        PLUGIN / ".codex-plugin/plugin.json": json_bytes(
            {**metadata, "skills": "./skills/", "mcpServers": "./.codex-mcp.json"}
        ),
        PLUGIN / ".claude-plugin/plugin.json": json_bytes(metadata),
        PLUGIN / "source-skills.json": json_bytes({"skills": rows}),
        PLUGIN / "workflows.json": json_bytes(
            {
                "schema_version": "abducer.workflow-catalog/v1",
                "plugin_version": metadata["version"],
                "workflows": workflows,
            }
        ),
        PLUGIN / "scripts/workflow_mcp.py": (
            root / "integrations/workflow_mcp/server.py"
        ).read_bytes(),
        PLUGIN / "scripts/agent_assets.py": (
            root / "integrations/workflow_mcp/agent_assets.py"
        ).read_bytes(),
        PLUGIN / "mcp.json": json_bytes(
            {
                "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
                "mcpServers": {
                    "abducer-workflows": {
                        "type": "stdio",
                        "command": "python3",
                        "args": ["${PLUGIN_ROOT}/scripts/workflow_mcp.py"],
                    }
                },
            }
        ),
        PLUGIN / ".codex-mcp.json": json_bytes(
            {
                "mcpServers": {
                    "abducer-workflows": {
                        "command": "python3",
                        "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/workflow_mcp.py"],
                    }
                }
            }
        ),
        PLUGIN / ".mcp.json": json_bytes(
            {
                "mcpServers": {
                    "abducer-workflows": {
                        "command": "python3",
                        "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/workflow_mcp.py"],
                    }
                }
            }
        ),
        Path(".agents/plugins/marketplace.json"): json_bytes(
            {
                "name": "abducer",
                "interface": {"displayName": "Abducer"},
                "plugins": [
                    {
                        "name": metadata["name"],
                        "source": {"source": "local", "path": "./plugins/abducer"},
                        "policy": {
                            "installation": "AVAILABLE",
                            "authentication": "ON_INSTALL",
                        },
                        "category": "Productivity",
                    }
                ],
            }
        ),
        Path(".claude-plugin/marketplace.json"): json_bytes(
            {
                "name": "abducer",
                "owner": metadata["author"],
                "plugins": [
                    {
                        "name": metadata["name"],
                        "source": "./plugins/abducer",
                        "description": metadata["description"],
                    }
                ],
            }
        ),
    }
    for row in rows:
        files[PLUGIN / "skills" / row["name"] / "SKILL.md"] = adapter(row)
    for row in workflows:
        files[PLUGIN / "skills" / row["entry"] / "SKILL.md"] = workflow_adapter(row)
    files[PLUGIN / "REUSE.toml"] = package_reuse(root, files)
    return files


def synchronize(root: Path, *, check: bool) -> list[str]:
    """Report stale adapters; only generated SKILL.md files may be removed."""
    expected = expected_files(root)
    existing = {
        path.relative_to(root) for path in (root / PLUGIN / "skills").glob("*/SKILL.md")
    }
    stale = sorted(existing - expected.keys())
    changed = [
        path
        for path, content in expected.items()
        if not (root / path).is_file() or (root / path).read_bytes() != content
    ]
    if not check:
        for path in stale:
            (root / path).unlink()
            if not any((root / path.parent).iterdir()):
                (root / path.parent).rmdir()
        for path in changed:
            (root / path).parent.mkdir(parents=True, exist_ok=True)
            (root / path).write_bytes(expected[path])
    return [str(path) for path in sorted(set(stale + changed))]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Reject generated drift")
    args = parser.parse_args()
    changes = synchronize(ROOT, check=args.check)
    if args.check and changes:
        print("Stale plugin files:\n" + "\n".join(changes))
        return 1
    print(
        f"{'Checked' if args.check else 'Generated'} {len(public_skills(ROOT))} public skills and {len(workflow_catalog(ROOT))} workflows"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
