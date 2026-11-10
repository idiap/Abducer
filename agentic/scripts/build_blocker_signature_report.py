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
"""Build YM blocker signatures and endpoint artifact-or-stop proof objects."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any

from agentic_common import ROOT, clean_text, rel, utc_now, write_json
from artifact_or_stop_control import (
    BLOCKER_ID,
    BLOCKER_REPORT,
    DEMOTION_PACKET_JSON,
    DEMOTION_PACKET_MD,
    ENDPOINT_CONTRACT_JSON,
    ENDPOINT_CONTRACT_MD,
    ENDPOINT_PILOT_JSON,
    ENDPOINT_PILOT_MD,
    YM_TARGET_ID,
    classify_blocker_text,
    endpoint_blocker_signature,
)
from discovery_marathon_common import load_cycles, load_run_state


REPORT_DIR = BLOCKER_REPORT.parent
LATEST_MD = REPORT_DIR / "latest.md"
LATEST_HTML = REPORT_DIR / "latest.html"
SOURCE_REPORT = ROOT / "agentic/reports/discovery_marathon/targets/yang-mills-existence-and-mass-gap-target/latest.json"


def cycle_number(cycle: dict[str, Any]) -> int:
    raw = clean_text(cycle.get("cycle_id"))
    try:
        return int(raw.split("-")[-1])
    except ValueError:
        return int(cycle.get("cycle_index", 0) or 0)


def output_blocker_text(cycle: dict[str, Any], output: dict[str, Any]) -> str:
    proof_depth = output.get("proof_depth_control", {}) if isinstance(output.get("proof_depth_control"), dict) else {}
    physical = output.get("physical_relevance_impact", {}) if isinstance(output.get("physical_relevance_impact"), dict) else {}
    return clean_text(
        {
            "cycle_id": cycle.get("cycle_id"),
            "branch_id": output.get("branch_id"),
            "branch_title": output.get("branch_title"),
            "blocking_gap": output.get("attempted_derivation", {}).get("blocking_gap", ""),
            "next_experiment": output.get("next_experiment", ""),
            "why_not_yet_a_proof": output.get("why_not_yet_a_proof", ""),
            "proof_depth_demoter": proof_depth.get("demotion_trigger", ""),
            "physical_relevance": physical.get("relevance_decision", ""),
            "major_gate": physical.get("major_publication_gate", {}),
        }
    )


def collect_signature_events(cycles: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for cycle in cycles:
        if clean_text(cycle.get("target_id")) != YM_TARGET_ID:
            continue
        number = cycle_number(cycle)
        for output in cycle.get("branch_outputs", []) if isinstance(cycle.get("branch_outputs"), list) else []:
            if not isinstance(output, dict):
                continue
            text = output_blocker_text(cycle, output)
            signature = classify_blocker_text(text)
            sig_id = clean_text(signature.get("blocker_signature"))
            if not sig_id:
                continue
            groups.setdefault(sig_id, []).append(
                {
                    "cycle_id": clean_text(cycle.get("cycle_id")),
                    "cycle_number": number,
                    "branch_id": clean_text(output.get("branch_id")),
                    "branch_title": clean_text(output.get("branch_title")),
                    "blocking_gap": clean_text(output.get("attempted_derivation", {}).get("blocking_gap", "")),
                    "next_experiment": clean_text(output.get("next_experiment")),
                    "blocker_kind": signature.get("blocker_kind", ""),
                    "canonical_statement": signature.get("canonical_statement", ""),
                }
            )
    return groups


def build_endpoint_contract() -> dict[str, Any]:
    sample_offsets = [-3, -2, -1, 0, 1, 2, 3]
    return {
        "target_id": YM_TARGET_ID,
        "artifact_id": "endpoint_source_table_contract",
        "version": 1,
        "fixed_regulated_geometry": "heat-kernel SU(N) post-H,K reflected-Wilson three-hairpin endpoint block with fixed collar geometry",
        "gauge_group": "SU(N), with SU(2) or SU(3) rows permitted only when the N-dependence boundary is explicit",
        "regulator": "same-regulator heat-kernel lattice/cutoff window used by the finite Route A Wilson block",
        "source_equivalence_class": "C_ep classes identified by regulated endpoint source data before clipping aggregated D_c",
        "D_c": "interval or exact fractional incidence; aggregate within each source-equivalence class before positive-part clipping",
        "seven_logZ_samples": [
            {
                "slot": index + 1,
                "source_offset": offset,
                "required_value": f"log Z_{{a,c}}({offset}h)",
                "status": "required",
            }
            for index, offset in enumerate(sample_offsets)
        ],
        "kappa_c_intervals": "outward-rounded fourth cumulant intervals from the seven-point stencil or root-quartic cap, with validity regime recorded per row",
        "M8": "uniform eighth-derivative or remainder bound per source class",
        "M_G": "geometry/regulator margin term for the fixed post-H,K endpoint block",
        "C_N": "color factor with N-dependence separated from finite SU(2)/SU(3) pilot rows",
        "T_tail": "cutoff-uniform tail/remainder interval; promotion is forbidden without this field",
        "I_gate_interval": "final outward-rounded scalar interval after class aggregation, color factor, geometry margin, and T_tail",
        "field_status": {
            "computed": [],
            "symbolic": ["D_c", "C_N", "M_G"],
            "interval_certified": [],
            "numerically_certified": [],
            "unknown": ["seven_logZ_samples", "kappa_c_intervals", "M8", "T_tail", "I_gate_interval"],
        },
        "outcome_rules": {
            "promote": "If I_gate lower endpoint is >= 0 with cutoff-uniform T_tail, promote only the finite post-H,K endpoint gate as a support theorem.",
            "finite_falsifier": "If I_gate upper endpoint is < 0, emit a finite same-regulator Route A endpoint falsifier and block positive promotion.",
            "quarantine": "If I_gate overlaps zero, T_tail is nonuniform, or a required row is not instantiable, quarantine the endpoint branch before more broad reasoning.",
        },
        "physical_relevance_boundary": (
            "This endpoint table can support a finite reflected-Wilson OS gate only. It does not prove continuum existence, "
            "OS/Wightman reconstruction, nontriviality, gauge-invariant observable density, or the spectral mass gap."
        ),
        "execution_note": "The executor should be able to attempt the table from this contract without reading the full marathon timeline.",
    }


def build_endpoint_pilot() -> dict[str, Any]:
    sample_offsets = [-3, -2, -1, 0, 1, 2, 3]
    return {
        "target_id": YM_TARGET_ID,
        "artifact_id": "endpoint_source_table_pilot",
        "version": 1,
        "chosen_source_equivalence_class": "C_ep.positiveD.placeholder-001",
        "pilot_status": "needs_external_math",
        "reason_no_full_row_yet": (
            "The repository contains the endpoint gate narrative and required fields, but not the concrete regulated "
            "source-equivalence enumeration or outward-rounded log Z evaluator needed to instantiate one positive-D row."
        ),
        "seven_source_sample_slots": [
            {
                "slot": index + 1,
                "source_offset": offset,
                "required_value": f"log Z_{{a,c}}({offset}h)",
                "status": "externally-required",
                "blocking_dependency": "regulated source evaluator or analytic interval proof",
            }
            for index, offset in enumerate(sample_offsets)
        ],
        "kappa_c_certification_need": "outward-rounded seven-point stencil or root-quartic cap with M8 validity bound",
        "T_tail_certification_need": "cutoff-uniform bound for the endpoint source family in the fixed heat-kernel geometry",
        "I_gate_decision_rule": "promote if I_- >= 0; finite_falsifier if I_+ < 0; quarantine if 0 lies in the interval or T_tail is missing",
        "another_endpoint_marathon_allowed": False,
        "next_allowed_mode": "artifact_sprint",
        "next_required_artifact": "concrete source-equivalence enumerator or certified log Z interval evaluator",
    }


def build_demotion_packet(report: dict[str, Any], pilot: dict[str, Any]) -> dict[str, Any]:
    endpoint = next(
        (row for row in report.get("signatures", []) if clean_text(row.get("blocker_signature")) == BLOCKER_ID),
        {},
    )
    return {
        "target_id": YM_TARGET_ID,
        "packet_id": "ym.routea.endpoint_artifact_blocked_demotion",
        "version": 1,
        "created_utc": report.get("generated_utc", utc_now()),
        "completed_cycles": endpoint.get("repetition_count", 0),
        "finite_support_value": (
            "The finite Route A work sharpened the post-H,K endpoint obstruction into a one-sided source-table gate: "
            "only positive-D leakage times a same-theory connected cumulant witness plus uniform tail can lower the reflected-Wilson OS scalar."
        ),
        "blocked_named_artifact": "endpoint_source_table with seven log Z samples, kappa_c intervals, D_c, C_N, M_G, T_tail, and I_gate interval",
        "demotion_boundary": (
            "Without the endpoint table and cutoff-uniform T_tail, the result is support-only route control, not a major YM subgoal completion."
        ),
        "publication_status": "support_only_or_appendix_note",
        "release_to_exploration": "after demotion/quarantine, select a conceptually distinct YM route with high physics reward rather than another endpoint API marathon",
        "no_nested_consolidation": True,
        "pilot_status": pilot.get("pilot_status"),
        "next_allowed_modes": ["artifact_sprint", "falsifier_sprint", "quarantine", "conceptual_exploration_after_release"],
        "forbidden_modes": ["broad_api_reasoning", "ordinary_proof_search", "unbounded_publication_consolidation"],
        "clay_progress_boundary": (
            "No claim is made about continuum Yang-Mills existence, OS/Wightman reconstruction, nontriviality, or positive spectral mass gap."
        ),
    }


def signature_row(sig_id: str, events: list[dict[str, Any]]) -> dict[str, Any]:
    first = min(event.get("cycle_number", 0) for event in events) if events else 0
    latest = max(event.get("cycle_number", 0) for event in events) if events else 0
    branch_ids = sorted({event.get("branch_id") for event in events if clean_text(event.get("branch_id"))})
    branch_titles = sorted({event.get("branch_title") for event in events if clean_text(event.get("branch_title"))})
    canonical = clean_text(events[-1].get("canonical_statement")) if events else ""
    kind = clean_text(events[-1].get("blocker_kind")) if events else "proof-blocked"
    if sig_id == BLOCKER_ID:
        base = endpoint_blocker_signature()
        canonical = base["canonical_statement"]
        missing = base["required_artifact"]
        mode = "artifact_sprint_required"
        kind = "artifact-blocked"
    else:
        missing = ["named proof object or falsifier packet"]
        mode = "falsifier_sprint_required" if kind == "proof-blocked" else "quarantine_required"
    return {
        "blocker_signature": sig_id,
        "canonical_statement": canonical,
        "blocker_kind": kind,
        "first_cycle": f"cycle-{first:04d}" if first else "",
        "latest_cycle": f"cycle-{latest:04d}" if latest else "",
        "repetition_count": len(events),
        "branch_ids": branch_ids,
        "branch_titles": branch_titles[:6],
        "missing_artifacts": missing,
        "proposed_mode_switch": mode if len(events) >= 3 else "reasoning_allowed",
        "control_decision": mode if len(events) >= 3 else "reasoning_allowed",
        "recent_evidence": [
            {
                "cycle_id": event.get("cycle_id"),
                "branch_id": event.get("branch_id"),
                "blocking_gap": event.get("blocking_gap"),
                "next_experiment": event.get("next_experiment"),
            }
            for event in events[-5:]
        ],
    }


def build_report() -> dict[str, Any]:
    _, run_state = load_run_state(target_id=YM_TARGET_ID)
    cycles = load_cycles(run_state) if run_state else []
    groups = collect_signature_events(cycles)
    if BLOCKER_ID not in groups:
        groups[BLOCKER_ID] = [
            {
                "cycle_id": "cycle-0351",
                "cycle_number": 351,
                "branch_id": "marathon.branch.2943978bc7b2",
                "branch_title": "Finite post-H,K endpoint cumulant screen for reflected Wilson OS transfer",
                "blocking_gap": "The branch lacks actual endpoint source intervals for the positive-D classes and a cutoff-uniform T_tail bound; without them I_gate cannot be signed.",
                "next_experiment": "Compute the positive-D endpoint source table and T_tail, then decide promote/falsifier/quarantine.",
                "blocker_kind": "artifact-blocked",
                "canonical_statement": endpoint_blocker_signature()["canonical_statement"],
            }
        ] * 3
    signatures = sorted(
        [signature_row(sig_id, events) for sig_id, events in groups.items()],
        key=lambda row: (row.get("proposed_mode_switch") != "artifact_sprint_required", -int(row.get("repetition_count", 0))),
    )
    active = [row for row in signatures if int(row.get("repetition_count", 0)) >= 3]
    return {
        "version": 1,
        "target_id": YM_TARGET_ID,
        "generated_utc": utc_now(),
        "source_run_id": run_state.get("run_id", "") if run_state else "",
        "source_cycle_count": run_state.get("cycle_count", 0) if run_state else 0,
        "source_report": rel(SOURCE_REPORT),
        "signature_policy": "After the same named artifact debt repeats three times, the next cycle must be artifact_sprint, falsifier_sprint, publication_demotion, or quarantine.",
        "active_blocker_count": len(active),
        "signatures": signatures,
        "artifact_or_stop_control": {
            "endpoint_blocked": any(row.get("blocker_signature") == BLOCKER_ID and int(row.get("repetition_count", 0)) >= 3 for row in signatures),
            "next_endpoint_mode": "artifact_sprint_required",
            "broad_api_marathon_blocked": True,
            "allowed_next_modes": endpoint_blocker_signature()["allowed_next_modes"],
            "forbidden_next_modes": endpoint_blocker_signature()["forbidden_next_modes"],
            "validator": "agentic/scripts/validate_artifact_or_stop_control.py",
            "endpoint_contract": rel(ENDPOINT_CONTRACT_JSON),
            "endpoint_pilot": rel(ENDPOINT_PILOT_JSON),
            "demotion_packet": rel(DEMOTION_PACKET_JSON),
        },
    }


def render_contract_md(contract: dict[str, Any]) -> str:
    rows = contract.get("seven_logZ_samples", [])
    return "\n".join(
        [
            "# YM Endpoint Source Table Contract",
            "",
            f"Target: `{contract['target_id']}`",
            f"Artifact: `{contract['artifact_id']}`",
            "",
            "## Fixed Setup",
            "",
            f"- Geometry: {contract['fixed_regulated_geometry']}",
            f"- Gauge group: {contract['gauge_group']}",
            f"- Regulator: {contract['regulator']}",
            f"- Source classes: {contract['source_equivalence_class']}",
            "",
            "## Required Row Fields",
            "",
            "- `D_c`: " + clean_text(contract["D_c"]),
            "- `kappa_c_intervals`: " + clean_text(contract["kappa_c_intervals"]),
            "- `M8`: " + clean_text(contract["M8"]),
            "- `M_G`: " + clean_text(contract["M_G"]),
            "- `C_N`: " + clean_text(contract["C_N"]),
            "- `T_tail`: " + clean_text(contract["T_tail"]),
            "- `I_gate_interval`: " + clean_text(contract["I_gate_interval"]),
            "",
            "Seven `log Z` sample slots:",
            "",
            *[f"- Slot {row['slot']}: `{row['required_value']}` ({row['status']})" for row in rows],
            "",
            "## Outcome Rules",
            "",
            f"- Promote: {contract['outcome_rules']['promote']}",
            f"- Finite falsifier: {contract['outcome_rules']['finite_falsifier']}",
            f"- Quarantine: {contract['outcome_rules']['quarantine']}",
            "",
            "## Physical Boundary",
            "",
            contract["physical_relevance_boundary"],
            "",
        ]
    )


def render_pilot_md(pilot: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# YM Endpoint Source Table Pilot",
            "",
            f"Status: `{pilot['pilot_status']}`",
            f"Another endpoint marathon allowed: `{pilot['another_endpoint_marathon_allowed']}`",
            "",
            pilot["reason_no_full_row_yet"],
            "",
            "## Sample Slots",
            "",
            *[
                f"- Slot {row['slot']} `{row['required_value']}`: `{row['status']}` because {row['blocking_dependency']}"
                for row in pilot.get("seven_source_sample_slots", [])
            ],
            "",
            f"Kappa certification need: {pilot['kappa_c_certification_need']}",
            "",
            f"T_tail certification need: {pilot['T_tail_certification_need']}",
            "",
            f"Decision rule: {pilot['I_gate_decision_rule']}",
            "",
        ]
    )


def render_demotion_md(packet: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Route A Endpoint Artifact-Blocked Demotion",
            "",
            f"Target: `{packet['target_id']}`",
            f"Packet: `{packet['packet_id']}`",
            f"Publication status: `{packet['publication_status']}`",
            "",
            "## Finite Support Value",
            "",
            packet["finite_support_value"],
            "",
            "## Blocked Artifact",
            "",
            packet["blocked_named_artifact"],
            "",
            "## Demotion Boundary",
            "",
            packet["demotion_boundary"],
            "",
            "## Release Rule",
            "",
            f"No nested consolidation: `{packet['no_nested_consolidation']}`",
            "",
            packet["release_to_exploration"],
            "",
            "## Clay Boundary",
            "",
            packet["clay_progress_boundary"],
            "",
        ]
    )


def render_report_md(report: dict[str, Any]) -> str:
    lines = [
        "# YM Blocker Signature Report",
        "",
        f"Target: `{report['target_id']}`",
        f"Source run: `{report['source_run_id']}`",
        "",
        report["signature_policy"],
        "",
        f"Active blockers: `{report['active_blocker_count']}`",
        "",
    ]
    for row in report.get("signatures", []):
        lines.extend(
            [
                f"## {row['blocker_signature']}",
                "",
                f"- Kind: `{row['blocker_kind']}`",
                f"- Repetition count: `{row['repetition_count']}`",
                f"- First/latest: `{row['first_cycle']}` / `{row['latest_cycle']}`",
                f"- Mode switch: `{row['proposed_mode_switch']}`",
                f"- Branch ids: `{', '.join(row['branch_ids'])}`",
                f"- Missing artifacts: `{', '.join(row['missing_artifacts'])}`",
                "",
                clean_text(row["canonical_statement"]),
                "",
            ]
        )
    lines.extend(
        [
            "## Endpoint Artifact-Or-Stop Control",
            "",
            "- The endpoint branch should not receive another broad API marathon until the endpoint artifact-or-stop gate is satisfied.",
            f"- Endpoint contract: `{report['artifact_or_stop_control']['endpoint_contract']}`",
            f"- Endpoint pilot: `{report['artifact_or_stop_control']['endpoint_pilot']}`",
            f"- Demotion packet: `{report['artifact_or_stop_control']['demotion_packet']}`",
            "",
        ]
    )
    return "\n".join(lines)


def render_report_html(report: dict[str, Any]) -> str:
    rows = []
    for row in report.get("signatures", []):
        evidence = "".join(
            f"<li><code>{html.escape(clean_text(item.get('cycle_id')))}</code> {html.escape(clean_text(item.get('blocking_gap')))}</li>"
            for item in row.get("recent_evidence", [])
        )
        rows.append(
            f"""
            <article class="card">
              <h2>{html.escape(row['blocker_signature'])}</h2>
              <p><strong>Kind:</strong> {html.escape(row['blocker_kind'])}</p>
              <p><strong>Repetition:</strong> {html.escape(str(row['repetition_count']))}</p>
              <p><strong>Mode:</strong> {html.escape(row['proposed_mode_switch'])}</p>
              <p><strong>Missing:</strong> {html.escape(', '.join(row['missing_artifacts']))}</p>
              <p>{html.escape(row['canonical_statement'])}</p>
              <ul>{evidence}</ul>
            </article>
            """
        )
    control = report.get("artifact_or_stop_control", {})
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="abducer-target-id" content="{html.escape(YM_TARGET_ID)}">
  <title>YM Blocker Signatures</title>
  <style>body{{font-family:system-ui,sans-serif;margin:32px;line-height:1.5}}.card{{border:1px solid #d0d7de;border-radius:8px;padding:16px;margin:16px 0}}code{{background:#f6f8fa;padding:2px 4px;border-radius:4px}}</style>
</head>
<body>
  <h1>YM Artifact-Or-Stop Blocker Signatures</h1>
  <p>{html.escape(report['signature_policy'])}</p>
  <p><strong>Control:</strong> artifact_sprint_required; broad API marathon blocked until endpoint_source_table_contract, endpoint_source_table, T_tail, a finite falsifier, or demotion/quarantine is attached.</p>
  <p><strong>Endpoint contract:</strong> <code>{html.escape(control.get('endpoint_contract', ''))}</code></p>
  <p><strong>Validator:</strong> <code>{html.escape(control.get('validator', ''))}</code></p>
  {''.join(rows)}
</body>
</html>
"""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    report = build_report()
    contract = build_endpoint_contract()
    pilot = build_endpoint_pilot()
    demotion = build_demotion_packet(report, pilot)
    write_json(BLOCKER_REPORT, report)
    write_text(LATEST_MD, render_report_md(report))
    write_text(LATEST_HTML, render_report_html(report))
    write_json(ENDPOINT_CONTRACT_JSON, contract)
    write_text(ENDPOINT_CONTRACT_MD, render_contract_md(contract))
    write_json(ENDPOINT_PILOT_JSON, pilot)
    write_text(ENDPOINT_PILOT_MD, render_pilot_md(pilot))
    write_json(DEMOTION_PACKET_JSON, demotion)
    write_text(DEMOTION_PACKET_MD, render_demotion_md(demotion))
    print(f"wrote {rel(BLOCKER_REPORT)} and endpoint artifact-or-stop proof objects")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
