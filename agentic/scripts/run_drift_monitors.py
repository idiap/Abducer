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

"""Generate drift report over Looper control-plane artifacts."""

from __future__ import annotations

from agentic_common import ROOT, kb_ref_from_path, load_json_object, repo_path


PROTECTED = [
    "agentic/spec/target_packet_schema.json",
    "agentic/spec/dependency_graph_schema.json",
    "agentic/registries/workflow_contracts.yaml",
    "hooks/hooks.json",
    "registry/taxonomy/workflow_taxonomy.json",
]


def main() -> int:
    target = load_json_object(ROOT / "agentic" / "state" / "current_target.json")
    kb_ref = kb_ref_from_path(repo_path(target["kb_path"], must_exist=True))
    graph = load_json_object(ROOT / "agentic" / "state" / "dependency_graphs" / f"{kb_ref}.json")
    missing = [path for path in PROTECTED if not (ROOT / path).exists()]
    stale = []
    graph_targets = {node["id"].replace("statement:", "") for node in graph["nodes"] if node["id"].startswith("statement:")}
    for claim in target["main_claim_ids"]:
        if claim not in graph_targets:
            stale.append(f"target claim absent from dependency graph: {claim}")
    lines = [
        "# Looper Drift Report",
        "",
        f"- Protected artifacts checked: {len(PROTECTED)}",
        f"- Missing protected artifacts: {len(missing)}",
        f"- Target/graph drift findings: {len(stale)}",
        "",
        "## Findings",
        "",
    ]
    if not missing and not stale:
        lines.append("None.")
    for item in missing:
        lines.append(f"- missing: `{item}`")
    for item in stale:
        lines.append(f"- stale: {item}")
    lines.extend(["", "## Decision", ""])
    lines.append("pass: no deterministic control-plane drift detected." if not missing and not stale else "block: drift must be repaired before promotion.")
    out = ROOT / "agentic" / "reports" / "drift" / "latest.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
