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
"""Report target-specific marathon pointers and profile separation status."""

from __future__ import annotations

from agentic_common import ROOT, load_json_object, rel, utc_now, write_json
from discovery_marathon_common import ACTIVE_POINTER, TARGET_ACTIVE_DIR, load_run_state
from target_profiles import TARGET_PROFILES, target_profile


OUT_JSON = ROOT / "agentic/reports/target_run_separation/latest.json"
OUT_MD = ROOT / "agentic/reports/target_run_separation/latest.md"


def main() -> int:
    rows = []
    for target_id in sorted(TARGET_PROFILES):
        profile = target_profile(target_id)
        pointer_path = TARGET_ACTIVE_DIR / f"{target_id}.json"
        pointer = load_json_object(pointer_path) if pointer_path.exists() else {}
        _, run_state = load_run_state(pointer.get("run_id")) if pointer else (ROOT, {})
        rows.append(
            {
                "target_id": target_id,
                "display_name": profile["display_name"],
                "domain": profile["domain"],
                "strategy_tab_label": profile["strategy_tab_label"],
                "story_tab_label": profile["story_tab_label"],
                "pointer_path": rel(pointer_path),
                "has_pointer": bool(pointer),
                "run_id": pointer.get("run_id", ""),
                "run_state_path": pointer.get("path", ""),
                "run_status": run_state.get("status", ""),
                "branch_count": len(run_state.get("branch_registry", [])) if run_state else 0,
                "profile_guard": {
                    "forbidden_cross_target_terms": profile.get("forbidden_cross_target_terms", []),
                    "consistency_markers": profile.get("consistency_markers", []),
                },
            }
        )
    active = load_json_object(ACTIVE_POINTER) if ACTIVE_POINTER.exists() else {}
    report = {
        "version": 1,
        "generated_utc": utc_now(),
        "active_pointer": active,
        "targets": rows,
        "separation_contract": [
            "Each target has a separate active pointer under agentic/runs/discovery_marathons/active_targets/.",
            "The global active_run.json may switch between targets, but target-specific pointers are preserved.",
            "Marathon branch prompts are generated from target_profiles.py, not from another target's current report.",
            "Cycle validation checks target-specific consistency markers and rejects known cross-target vocabulary.",
        ],
    }
    write_json(OUT_JSON, report)
    lines = [
        "# Target Run Separation",
        "",
        f"- Generated: `{report['generated_utc']}`",
        f"- Global active run: `{active.get('run_id', '')}` for `{active.get('target_id', '')}`",
        "",
        "## Targets",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"### {row['display_name']}",
                "",
                f"- Target id: `{row['target_id']}`",
                f"- Domain: {row['domain']}",
                f"- Pointer: `{row['pointer_path']}`",
                f"- Run: `{row['run_id']}` ({row['run_status'] or 'missing'})",
                f"- Branches: {row['branch_count']}",
                f"- Strategy label: {row['strategy_tab_label']}",
                f"- Story label: {row['story_tab_label']}",
                "",
            ]
        )
    lines.extend(["## Separation Contract", ""])
    lines.extend(f"- {item}" for item in report["separation_contract"])
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {rel(OUT_JSON)}")
    print(f"Wrote {rel(OUT_MD)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
