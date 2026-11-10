# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Export verified public Abducer procedures for the managed Sites runtime.

The existing Catalog is the release authority: it validates canonical skill,
contract and viewer provenance before any output is written. This exporter only
copies those registered sources. It never scans research runs, user projects,
credentials, checkpoints or arbitrary repository files. Included instructions
are source material for ChatGPT-guided work, not executable worker authority.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from integrations.chatgpt.catalog import Catalog

ROOT = Path(__file__).resolve().parents[2]
MAX_EXPORT_BYTES = 12 * 1024 * 1024


def build_library(root: Path = ROOT) -> dict:
    """Build a deterministic, complete library from the canonical allowlist."""
    catalog = Catalog(root)
    skills = [
        {
            "name": row["name"],
            "description": row["description"],
            "content": catalog.sources[row["source"]],
            "path": row["source"],
            "sha256": row["sha256"],
        }
        for row in sorted(catalog.skills, key=lambda row: row["name"])
    ]
    workflows = []
    for summary in sorted(
        catalog.list_workflows()["workflows"], key=lambda row: row["id"]
    ):
        detail = catalog.get_workflow(summary["id"])
        contract = detail["workflow"]
        viewer = detail["viewer"]
        label = viewer["label"] if viewer else summary["id"]
        description = (
            viewer.get("summary", "")
            if viewer
            else contract["contract"].get("description", "")
        )
        workflows.append(
            {
                **summary,
                "workflow_id": summary["id"],
                "label": label,
                "title": label,
                "summary": description,
                "description": description,
                "contract": contract["contract"],
                "descriptor_sha256": contract["descriptor_sha256"],
                "owner_sha256": contract["owner_sha256"],
                "viewer": viewer,
                "graph": viewer["graph"] if viewer else None,
            }
        )
    return {
        "schema_version": 1,
        "release": catalog.release,
        "skills": skills,
        "workflows": workflows,
        "capabilities": {
            "skill_count": len(skills),
            "workflow_count": len(workflows),
            "graph_count": len(catalog.viewers),
            "source_inspection": True,
            "chat_guided_research": True,
            "native_execution": False,
            "scientific_truth_verified": False,
            "boundary": (
                "Canonical procedures, contracts and authored graph examples are "
                "source material, not executed research or verified scientific results. "
                "ChatGPT may guide research using these procedures and available tools. "
                "Local commands, references and prerequisite files require separately "
                "available capabilities; Sites does not run the Python research worker."
            ),
        },
    }


def export_bytes(root: Path = ROOT) -> bytes:
    """Serialize reproducibly and reject exports exceeding the bounded budget."""
    content = (
        json.dumps(
            build_library(root),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")
    if len(content) > MAX_EXPORT_BYTES:
        raise ValueError("Sites library exceeds the 12 MiB uncompressed export budget")
    return content


def main(argv: list[str] | None = None) -> int:
    """Atomically write the verified library; a failed build leaves output intact."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    content = export_bytes(args.source_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=args.output.parent, prefix=".abducer-library-", delete=False
        ) as stream:
            temporary = Path(stream.name)
            stream.write(content)
        os.replace(temporary, args.output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    library = json.loads(content)
    print(
        json.dumps(
            {
                "output": str(args.output),
                "release": library["release"],
                "bytes": len(content),
                "skills": len(library["skills"]),
                "workflows": len(library["workflows"]),
                "graphs": library["capabilities"]["graph_count"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
