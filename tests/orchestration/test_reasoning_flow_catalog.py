# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from agentic.orchestration.reasoning_flow_language import logical_lines, parse_file

ROOT = Path(__file__).resolve().parents[2]
FLOW_ROOT = ROOT / "agentic/reasoning_flows"
CATALOG = ROOT / "agentic/registries/reasoning_flow_catalog.yaml"
PHYSICS_EXAMPLES = ROOT / "agentic/registries/reasoning_flow_physics_examples.yaml"


def load_catalog() -> dict:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def test_catalog_is_a_complete_bijection_over_canonical_flow_files() -> None:
    rows = load_catalog()["flows"]
    ids = [row["id"] for row in rows]
    paths = [row["path"] for row in rows]
    assert len(rows) == 19
    assert len(ids) == len(set(ids))
    assert len(paths) == len(set(paths))
    assert set(ids) == {path.stem for path in FLOW_ROOT.glob("*.prism")}

    known = set(ids)
    for row in rows:
        path = ROOT / row["path"]
        assert path.is_file()
        assert parse_file(path, known_workflows=known)["id"] == row["id"]


def test_aliases_are_unambiguous_and_not_canonical_duplicates() -> None:
    rows = load_catalog()["flows"]
    canonical = {row["id"] for row in rows}
    aliases = [alias for row in rows for alias in row["aliases"]]
    assert len(aliases) == len(set(aliases))
    assert canonical.isdisjoint(aliases)

    named = json.loads(
        (ROOT / "agentic/registries/named_workflow_contracts.yaml").read_text(encoding="utf-8")
    )
    indexed = {row["id"]: set(row["aliases"]) for row in rows}
    for workflow in named["workflows"]:
        assert set(workflow["aliases"]) <= indexed[workflow["id"]]


def test_cohere_fast_family_remains_switch_isolated() -> None:
    rows = load_catalog()["flows"]
    cohere_ids = {row["id"] for row in rows if row["id"].startswith("cohere_fast")}
    for flow_id in cohere_ids:
        text = (FLOW_ROOT / f"{flow_id}.prism").read_text(encoding="utf-8")
        switches = [line.split("switch @", 1)[1].strip() for line in text.splitlines() if "switch @" in line]
        assert all(target in cohere_ids for target in switches)

    expected_chain = {
        "cohere_fast": "cohere_fast_scope_and_ground",
        "cohere_fast_scope_and_ground": "cohere_fast_adaptive_frontier",
        "cohere_fast_adaptive_frontier": "cohere_fast_derivation_and_proof",
        "cohere_fast_derivation_and_proof": "cohere_fast_independent_audit",
        "cohere_fast_independent_audit": "cohere_fast_manuscript_release",
    }
    for source, target in expected_chain.items():
        assert f"switch @{target}" in (FLOW_ROOT / f"{source}.prism").read_text(encoding="utf-8")


def test_declared_handoffs_are_represented_exactly_as_switch_targets() -> None:
    catalog_ids = {row["id"] for row in load_catalog()["flows"]}
    registries = [
        ROOT / "agentic/registries/workflow_contracts.yaml",
        ROOT / "agentic/registries/named_workflow_contracts.yaml",
    ]
    for registry_path in registries:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        for contract in registry["workflows"]:
            flow = parse_file(
                FLOW_ROOT / f"{contract['id']}.prism", known_workflows=catalog_ids
            )
            represented = {
                handler["action"].removeprefix("switch @")
                for handler in flow["handlers"]
                if handler["action"].startswith("switch @")
            }
            source_targets = (
                set(contract.get("handoff_to", []))
                if "handoff_to" in contract
                else {handoff["workflow"] for handoff in contract.get("handoffs", [])}
            )
            assert represented == source_targets, contract["id"]


def test_source_references_exist() -> None:
    for row in load_catalog()["flows"]:
        refs = row.get("source_refs", [row["source"]])
        assert row["source"] in refs
        assert all((ROOT / ref).is_file() for ref in refs)


def test_physics_examples_cover_every_flow_and_branch() -> None:
    rows = load_catalog()["flows"]
    catalog_ids = {row["id"] for row in rows}
    registry = json.loads(PHYSICS_EXAMPLES.read_text(encoding="utf-8"))
    assert registry["schema_version"] == "1.0.0"
    assert registry["domain"].strip()
    assert registry["scope_note"].strip()
    examples = {row["flow_id"]: row for row in registry["examples"]}
    assert len(examples) == len(registry["examples"])
    assert set(examples) == catalog_ids

    for flow_id, example in examples.items():
        flow = parse_file(
            FLOW_ROOT / f"{flow_id}.prism", known_workflows=catalog_ids
        )
        predicates = {handler["when"] for handler in flow["handlers"]}
        assert set(example["outcomes"]) == predicates
        assert all(example[field].strip() for field in ("scenario", "goal", "route"))
        assert all(value.strip() for value in example["outcomes"].values())
        if flow["repeats"]:
            assert example.get("iteration", "").strip()


def test_single_file_reasoning_flow_reference_is_complete_and_fresh() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "agentic/scripts/build_all_reasoning_flows_reference.py",
            "--check",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    reference = (ROOT / "docs/reference/all-reasoning-flows.md").read_text(
        encoding="utf-8"
    )
    rows = load_catalog()["flows"]
    assert reference.count("```erfl") == len(rows)
    assert reference.count("### Line-by-line interpretation") == len(rows)
    assert reference.count("1. `erfl 0.2`") == len(rows) - 1
    assert reference.count("1. `erfl 0.3`") == 1
    semantic_prefixes = ("goal ", "steps ", "repeat ", "on ")
    expected_examples = sum(
        len(
            [
                line
                for line in logical_lines((ROOT / row["path"]).read_text(encoding="utf-8"))
                if line.strip().startswith(semantic_prefixes)
            ]
        )
        for row in rows
    )
    assert reference.count("**Concrete physics example:**") == expected_examples
    total_lines = sum(
        len(
            [
                line
                for line in logical_lines((ROOT / row["path"]).read_text(encoding="utf-8"))
            ]
        )
        for row in rows
    )
    assert reference.count("**Physics context:**") == total_lines - expected_examples
    registry = json.loads(PHYSICS_EXAMPLES.read_text(encoding="utf-8"))
    for example in registry["examples"]:
        assert example["scenario"] in reference
        assert example["goal"] in reference
        assert example["route"] in reference
        assert all(value in reference for value in example["outcomes"].values())
    for row in rows:
        assert f"## {row['id']}" in reference
        flow = (ROOT / row["path"]).read_text(encoding="utf-8").rstrip()
        assert flow in reference
        assert f"Ends the `{row['id']}` reasoning definition." in reference
