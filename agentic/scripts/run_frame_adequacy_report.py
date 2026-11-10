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

"""Generate frame-adequacy report from dependency graph roles."""

from __future__ import annotations

from agentic_common import ROOT, kb_ref_from_path, load_json_object, repo_path


def main() -> int:
    target = load_json_object(ROOT / "agentic" / "state" / "current_target.json")
    kb_ref = kb_ref_from_path(repo_path(target["kb_path"], must_exist=True))
    graph = load_json_object(ROOT / "agentic" / "state" / "dependency_graphs" / f"{kb_ref}.json")
    kind_counts = graph["summary"]["kind_counts"]
    proxy_risks = [node for node in graph["nodes"] if node["kind"] in {"connector_bridge", "intervention"}]
    proof_debts = [node for node in graph["nodes"] if node["status"] in {"proof-debt", "route-lemma"}]
    blockers = [node for node in graph["nodes"] if node["status"] == "blocked"]
    lines = [
        "# Frame Adequacy Report",
        "",
        "This report asks whether the current vocabulary can state, diagnose, and evaluate the target dependencies.",
        "",
        "## Role Coverage",
        "",
    ]
    for kind, count in sorted(kind_counts.items()):
        lines.append(f"- `{kind}`: {count}")
    lines.extend(["", "## Adequacy Signals", ""])
    lines.append(f"- Proxy-eval risk nodes: {len(proxy_risks)}")
    lines.append(f"- Proof-debt or route-lemma nodes: {len(proof_debts)}")
    lines.append(f"- Blocked nodes: {len(blockers)}")
    lines.extend(["", "## Decision", ""])
    if proof_debts:
        lines.append("warn: the frame is adequate for control-plane navigation, but mathematical proof debt remains explicit.")
    else:
        lines.append("pass: no unresolved proof-debt roles detected.")
    out = ROOT / "agentic" / "reports" / "frame_adequacy" / "latest.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
