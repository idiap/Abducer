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
"""Check strict-prefix Qrep replay examples for the Formula Footprints report."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agentic_common import ROOT, fail, rel


REPORT_DIR = ROOT / "agentic" / "reports" / "pvsnp_formula_footprints_referee_closure"
EXAMPLES_PATH = REPORT_DIR / "strict_prefix_qrep_prefix_scan_examples.json"


def load_examples() -> dict[str, Any]:
    try:
        payload = json.loads(EXAMPLES_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{rel(EXAMPLES_PATH)} is not valid JSON: {exc}")
    if not isinstance(payload, dict):
        fail(f"{rel(EXAMPLES_PATH)} must contain a JSON object")
    return payload


def reject(reason: str) -> dict[str, Any]:
    return {"accepted": False, "reason": reason, "k_qrep": [], "d_q": 0}


def scan(example: dict[str, Any]) -> dict[str, Any]:
    base_support = set(example.get("base_support", []))
    if not all(isinstance(item, str) for item in base_support):
        fail(f"example {example.get('id')} has invalid base_support")

    entries = example.get("dictionary_entries", [])
    if not isinstance(entries, list):
        fail(f"example {example.get('id')} dictionary_entries must be a list")

    by_id: dict[str, dict[str, Any]] = {}
    row_to_rep: dict[str, str] = {}
    k_qrep = set(base_support)
    d_q = 0

    for entry in entries:
        if not isinstance(entry, dict):
            fail(f"example {example.get('id')} has non-object dictionary entry")
        entry_id = entry.get("id")
        if not isinstance(entry_id, str) or not entry_id:
            fail(f"example {example.get('id')} has entry without id")
        if entry_id in by_id:
            return reject("duplicate_dictionary_entry")
        by_id[entry_id] = entry

        row = entry.get("row")
        representative = entry.get("representative")
        cert_line = entry.get("cert_line")
        first_use_line = entry.get("first_use_line")
        rank = entry.get("rank")
        if not isinstance(row, str) or not isinstance(representative, str):
            return reject("missing_row_or_representative")
        if not isinstance(cert_line, int) or not isinstance(first_use_line, int):
            return reject("missing_temporal_lines")
        if not isinstance(rank, int) or rank < 0:
            return reject("invalid_rank")
        if cert_line >= first_use_line:
            return reject("certificate_not_strict_prefix")
        if entry.get("append_only") is not True:
            return reject("non_append_only_dictionary")
        if entry.get("advice_free") is not True:
            return reject("advice_chosen_dictionary")
        if row in row_to_rep and row_to_rep[row] != representative:
            return reject("representative_rebinding")
        row_to_rep[row] = representative

        for dep_id in entry.get("dependencies", []):
            dep = by_id.get(dep_id)
            if dep is None:
                return reject("dependency_not_in_prefix")
            if not isinstance(dep.get("rank"), int) or dep["rank"] >= rank:
                return reject("dependency_rank_not_decreasing")

        support = entry.get("support", [])
        forest = entry.get("certificate_forest", [])
        if not isinstance(support, list) or not all(isinstance(item, str) for item in support):
            return reject("invalid_certificate_support")
        if not isinstance(forest, list) or not all(isinstance(item, str) for item in forest):
            return reject("invalid_certificate_forest")
        k_qrep.update(support)
        k_qrep.add(row)
        k_qrep.add(representative)
        d_q += len(forest) + len(set(support)) + 1

    return {"accepted": True, "reason": "accepted", "k_qrep": sorted(k_qrep), "d_q": d_q}


def main() -> int:
    payload = load_examples()
    if payload.get("status") != "implemented":
        fail("strict-prefix Qrep example packet must be implemented")
    examples = payload.get("examples", [])
    if not isinstance(examples, list) or len(examples) < 2:
        fail("strict-prefix Qrep example packet must contain at least two examples")

    seen_accept = False
    seen_reject = False
    for example in examples:
        if not isinstance(example, dict):
            fail("strict-prefix Qrep examples must be JSON objects")
        result = scan(example)
        expected = example.get("expected_result", {})
        if result["accepted"] != expected.get("accepted"):
            fail(f"example {example.get('id')} accepted={result['accepted']} expected {expected.get('accepted')}")
        expected_reason = expected.get("reason")
        if expected_reason and result["reason"] != expected_reason:
            fail(f"example {example.get('id')} reason={result['reason']} expected {expected_reason}")
        if result["accepted"]:
            seen_accept = True
            if result["d_q"] != expected.get("d_q"):
                fail(f"example {example.get('id')} D_Q={result['d_q']} expected {expected.get('d_q')}")
            if result["k_qrep"] != sorted(expected.get("k_qrep", [])):
                fail(f"example {example.get('id')} K_Qrep mismatch")
        else:
            seen_reject = True
            if expected_reason != "certificate_not_strict_prefix":
                fail(f"example {example.get('id')} must reject the delayed-certificate falsifier")

    if not seen_accept or not seen_reject:
        fail("strict-prefix Qrep examples must include one accepted and one rejected case")
    print(f"validated strict-prefix Qrep prefix scan examples in {rel(EXAMPLES_PATH)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
