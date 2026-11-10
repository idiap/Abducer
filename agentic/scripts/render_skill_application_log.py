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

"""Render runtime skill application logs to Markdown."""

from __future__ import annotations

import json

from agentic_common import ROOT, rel


def main() -> int:
    logs = sorted((ROOT / "agentic" / "traces" / "skill_applications").glob("*.jsonl"))
    out_dir = ROOT / "agentic" / "reports" / "skill_application_logs"
    out_dir.mkdir(parents=True, exist_ok=True)
    for path in logs:
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        lines = [f"# Skill Application Log: {path.stem}", ""]
        for row in rows:
            evidence = ", ".join(row.get("evidence_paths", [])) or "none"
            lines.append(f"- `{row['event']}` `{row['skill_id']}`: {row.get('summary', '')} Evidence: {evidence}")
        out = out_dir / f"{path.stem}.md"
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"rendered {len(logs)} skill application reports")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
