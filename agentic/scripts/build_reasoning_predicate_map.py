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
"""Build the system-level ERFL predicate map from canonical reasoning programs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from agentic.orchestration.reasoning_flow_language import parse_file

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "agentic/registries/reasoning_flow_catalog.yaml"
MAP_OUTPUT = ROOT / "agentic/reasoning_flows/all-reasoning.pmap"
JSON_OUTPUT = ROOT / "agentic/state/reasoning_predicate_map.json"
DOC_OUTPUT = ROOT / "docs/reference/reasoning-predicate-map.md"


def relation_signature(node: dict) -> list[str]:
    """Return relations in structural order, collapsing repeated names."""
    ordered: list[str] = []

    def add(name: str) -> None:
        if name not in ordered:
            ordered.append(name)

    def visit(value: dict) -> None:
        if value["op"] == "optional":
            visit(value["value"])
        elif value["op"] in {"choice", "all"}:
            for branch in value["values"]:
                visit(branch)
        elif value["op"] == "sequence":
            visit(value["values"][0])
            for relation, successor in zip(value["relations"], value["values"][1:]):
                add(relation["name"])
                visit(successor)

    visit(node)
    return ordered


def build() -> dict:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    known = {row["id"] for row in catalog["flows"]}
    entries = []
    for row in catalog["flows"]:
        reasoning = parse_file(ROOT / row["path"], known_workflows=known)
        predicates = relation_signature(reasoning["steps"])
        for repeat in reasoning["repeats"]:
            for predicate in relation_signature(repeat["body"]):
                if predicate not in predicates:
                    predicates.append(predicate)
        targets = [
            handler["action"].removeprefix("switch @")
            for handler in reasoning["handlers"]
            if handler["action"].startswith("switch @")
        ]
        output_name = reasoning["goal"]["target_state"]
        entries.append(
            {
                "reasoning": reasoning["id"],
                "predicates": predicates,
                "output": output_name,
                "output_id": f"{reasoning['id']}.{output_name}",
                "connects_to": targets,
                "terminal": not targets,
            }
        )
    return {
        "schema_version": "1.0.0",
        "abstraction": "reasoning_predicate_map",
        "principle": "Internal steps collapse to an ordered relation signature; named calibrated outputs mediate every inter-reasoning connection.",
        "entries": entries,
    }


def render_map(payload: dict) -> str:
    lines = ["map abducer {"]
    for entry in payload["entries"]:
        predicates = ", ".join(entry["predicates"]) or "calibrate"
        output = f"output::{entry['output_id']}"
        lines.append(f"  reasoning::{entry['reasoning']} -{predicates}> {output}")
        for target in entry["connects_to"]:
            lines.append(f"  {output} -> reasoning::{target}")
        if entry["terminal"]:
            lines.append(f"  {output} -> terminal")
    lines.append("}")
    return "\n".join(lines) + "\n"


def _doc_preamble() -> str:
    """Retain leading legal notices while keeping generated body checks exact."""
    if not DOC_OUTPUT.is_file():
        return ""
    text = DOC_OUTPUT.read_text(encoding="utf-8")
    cursor = 0
    while text.startswith("<!--", cursor):
        end = text.find("-->", cursor)
        if end < 0:
            raise ValueError("unterminated predicate-map comment preamble")
        if "SPDX-" not in text[cursor:end]:
            break
        cursor = end + 3
        while cursor < len(text) and text[cursor].isspace():
            cursor += 1
    return text[:cursor]


def render_doc(payload: dict, source: str) -> str:
    return _doc_preamble() + "\n".join(
        [
            "# Reasoning predicate map",
            "",
            "This system-level ERFL projection collapses each detailed `steps` expression",
            "to its ordered, duplicate-free predicate signature. The domain is a named",
            "reasoning program; the range is its named calibrated output. Only that output",
            "connects to downstream reasoning programs.",
            "",
            "```text",
            source.rstrip(),
            "```",
            "",
            "The map hides occurrences, ports, skills, artifacts, and runtime order. It",
            "preserves relation names, output identity, terminality, and cross-reasoning",
            "connections. A predicate list summarizes structure; it does not assert that",
            "every predicate applies directly between the source program and its output.",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = build()
    source = render_map(payload)
    expected = {
        MAP_OUTPUT: source,
        JSON_OUTPUT: json.dumps(payload, indent=2) + "\n",
        DOC_OUTPUT: render_doc(payload, source),
    }
    if args.write:
        for path, content in expected.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    elif args.check:
        stale = [
            str(path.relative_to(ROOT))
            for path, content in expected.items()
            if not path.is_file() or path.read_text(encoding="utf-8") != content
        ]
        if stale:
            raise SystemExit(f"stale reasoning predicate map outputs: {stale}")
    else:
        print(source, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
