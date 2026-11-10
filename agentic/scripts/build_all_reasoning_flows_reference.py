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
"""Build the single-file Markdown reference for every canonical ERFL flow."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from agentic.orchestration.reasoning_flow_language import logical_lines, occurrences, parse, parse_expression

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "agentic/registries/reasoning_flow_catalog.yaml"
PHYSICS_EXAMPLES = ROOT / "agentic/registries/reasoning_flow_physics_examples.yaml"
OUTPUT = ROOT / "docs/reference/all-reasoning-flows.md"
PREDICATE_MAP = ROOT / "agentic/reasoning_flows/all-reasoning.pmap"

TYPE_NAMES = {
    "D": "deductive entailment",
    "A": "abductive hypothesis formation",
    "I": "inductive generalization",
    "T": "structural analogy and transfer",
    "C": "contrastive counterfactual reasoning",
    "M": "model-based reasoning",
    "R": "critical refutational testing",
    "E": "epistemic status calibration",
}

RELATION_EXPLANATIONS = {
    "requires": "requires the next occurrence structurally; this dependency adds no evidential warrant",
    "assume": "retains the preceding candidate explicitly as a premise for conditional reasoning",
    "test": "subjects the preceding claim or candidate to critical testing",
    "calibrate": "uses the preceding findings to update epistemic status without creating a new substantive claim",
    "constrain": "uses the preceding state to narrow what the next occurrence may produce",
    "generalize": "forms a scoped provisional pattern from the preceding cases",
    "transfer": "attempts a structural transfer while retaining correspondence and side-condition obligations",
    "probe": "examines the preceding candidate through a model or controlled contrast",
    "revise": "uses the preceding assessment to initiate a revised reasoning occurrence",
    "preserve": "carries the same epistemic interface forward without increasing its authority",
    "feeds": "passes into the next occurrence through an unlabelled legacy dependency",
}


def _humanize(value: str) -> str:
    return value.replace("_", " ").replace("-", " ")


def _join_handles(handles: list[str]) -> str:
    quoted = [f"`{handle}`" for handle in handles]
    if len(quoted) == 1:
        return quoted[0]
    return ", ".join(quoted[:-1]) + f" and {quoted[-1]}"


def _describe_expression(node: dict) -> str:
    if node["op"] == "gap":
        return (
            f"`{node['alias']}` marks an unresolved reasoning region that carries "
            f"{_join_handles(node['inputs'])} into {_join_handles(node['outputs'])}; "
            "no reasoning type is inferred for it"
        )
    if node["op"] == "type":
        alias = f"`{node['alias']}`" if node.get("alias") else "an unnamed occurrence"
        if node.get("inputs"):
            interface = (
                f", consuming {_join_handles(node['inputs'])} and producing "
                f"{_join_handles(node['outputs'])}"
            )
        else:
            interface = ""
        return f"{alias} performs {TYPE_NAMES[node['code']]}{interface}"
    if node["op"] == "optional":
        return f"optionally, {_describe_expression(node['value'])}"
    if node["op"] == "all":
        branches = "; ".join(
            f"branch {index}: {_describe_expression(value)}"
            for index, value in enumerate(node["values"], start=1)
        )
        return f"all of these branches are required—{branches}"
    if node["op"] == "choice":
        branches = "; ".join(
            f"alternative {index}: {_describe_expression(value)}"
            for index, value in enumerate(node["values"], start=1)
        )
        return f"the route retains alternatives—{branches}"
    if node["op"] == "sequence":
        description = _describe_expression(node["values"][0])
        for relation, value in zip(node["relations"], node["values"][1:]):
            explanation = RELATION_EXPLANATIONS[relation["name"]]
            description += f"; it then {explanation}, after which {_describe_expression(value)}"
        return description
    raise ValueError(f"unsupported ERFL expression node: {node['op']}")


def _subject_description(subject: str, aliases: dict[str, dict]) -> str:
    if subject == "reasoning":
        return "the reasoning program as a whole"
    occurrence = aliases.get(subject)
    if occurrence is None:
        return f"occurrence `{subject}`"
    if occurrence["code"] == "_":
        return f"unresolved occurrence `{subject}`"
    return f"`{subject}` ({TYPE_NAMES[occurrence['code']]})"


def interpret_line(line: str, flow: dict, aliases: dict[str, dict]) -> str:
    stripped = line.strip()
    if stripped.startswith("erfl "):
        return (
            f"Declares that this program uses ERFL version `{stripped.split()[1]}`, "
            "fixing the grammar and validation rules used to read the remaining lines."
        )
    if stripped.startswith("reasoning "):
        reasoning_id = stripped.split()[1]
        return f"Begins the canonical reasoning program named `{reasoning_id}`."
    if stripped.startswith("@KB "):
        match = re.fullmatch(r'@KB ([a-z][a-z0-9_-]*) connect\(file\("([^"]+)"\)\)', stripped)
        assert match is not None
        return (
            f"Connects external KB symbol `{match.group(1)}` to file-backed resource "
            f"`{match.group(2)}` before reasoning begins."
        )
    if stripped.startswith("knowledge "):
        match = re.fullmatch(
            r'knowledge ([a-z][a-z0-9_-]*) at "([^"]+)" access '
            r'(read|read_write) persist (none|versioned)', stripped,
        )
        assert match is not None
        access = "read-only" if match.group(3) == "read" else "read-and-write"
        return (
            f"Binds local handle `{match.group(1)}` to the specific KB `{match.group(2)}` "
            f"with {access} access and `{match.group(4)}` persistence. Reading or writing "
            "the KB does not change the authority of its members."
        )
    if stripped.startswith("goal "):
        match = re.fullmatch(r'goal "([^"]+)" -> ([a-z][a-z0-9_-]*)', stripped)
        assert match is not None
        return (
            f"Sets the epistemic objective to “{match.group(1)}” and names the required "
            f"resulting state `{match.group(2)}`. Reaching a control state alone does not "
            "establish the scientific claim."
        )
    if stripped.startswith("steps "):
        expression = parse_expression(stripped[6:])
        return f"Defines the main epistemic steps: {_describe_expression(expression)}."
    if match := re.fullmatch(
        r"([a-z][a-z0-9_-]*) <-(query|search)- ([a-z][a-z0-9_-]*)", stripped
    ):
        verb = "queries" if match.group(2) == "query" else "searches"
        return (
            f"Occurrence `{match.group(1)}` {verb} KB `{match.group(3)}`; "
            "the inverted arrow records information flowing from the KB into reasoning."
        )
    if match := re.fullmatch(
        r"([a-z][a-z0-9_-]*) -persist-> ([a-z][a-z0-9_-]*)", stripped
    ):
        return (
            f"Calibrated occurrence `{match.group(1)}` persists a successor of KB "
            f"`{match.group(2)}` without promoting member authority."
        )
    if stripped.startswith("repeat "):
        match = re.fullmatch(
            r"repeat (\d+)\.\.(\d+) \[(.+)\] until ([a-z][a-z0-9_-]*\.[a-z][a-z0-9_-]*) measure ([a-z][a-z0-9_-]*)",
            stripped,
        )
        assert match is not None
        return (
            f"Repeats the described reasoning block between {match.group(1)} and "
            f"{match.group(2)} times, stopping when `{match.group(4)}` holds and measuring "
            f"progress with `{match.group(5)}`. Repetition without new evidence or a real "
            "state delta does not increase confidence."
        )
    if stripped.startswith("on "):
        match = re.fullmatch(
            r"on ([a-z][a-z0-9_-]*)\.([a-z][a-z0-9_-]*) => (stop|accept|switch @([a-z][a-z0-9_-]*))",
            stripped,
        )
        assert match is not None
        subject, status, action, target = match.groups()
        prefix = (
            f"When {_subject_description(subject, aliases)} reports "
            f"`{status}` ({_humanize(status)}), "
        )
        if action == "stop":
            return (
                prefix
                + "the program stops. This is a workflow disposition and does not by itself "
                "prove the negation of a claim."
            )
        if action == "accept":
            return (
                prefix
                + "the program accepts the calibrated result for workflow purposes. Acceptance "
                "does not create additional scientific warrant."
            )
        return (
            prefix
            + f"control switches to `{target}`. The switch is operational: it must preserve "
            "scope, provenance, claim ceiling, taints, and open obligations, and it adds no warrant."
        )
    if stripped == "}":
        return f"Ends the `{flow['id']}` reasoning definition."
    raise ValueError(f"cannot interpret ERFL line: {stripped}")


def line_interpretations(source: str) -> list[tuple[str, str]]:
    flow = parse(source)
    nodes = occurrences(flow["steps"])
    for repeat in flow["repeats"]:
        nodes.extend(occurrences(repeat["body"]))
    aliases = {node["alias"]: node for node in nodes if node.get("alias")}
    source_lines = logical_lines(source)
    return [(line, interpret_line(line, flow, aliases)) for line in source_lines]


def physics_example_for_line(line: str, example: dict) -> str:
    stripped = line.strip()
    if stripped.startswith("erfl "):
        return (
            f"The following {example['flow_id']} example is expressed under the same "
            "ERFL semantics, so its physics content cannot gain authority from control flow."
        )
    if stripped.startswith("reasoning "):
        return example["scenario"]
    if stripped.startswith("@KB "):
        return "The reasoning uses the authoritative Yang–Mills KB as an external resource."
    if stripped.startswith("knowledge "):
        return (
            "This flow reads the problem's authoritative Yang–Mills KB and may persist "
            "only a versioned successor; generated candidates remain non-authoritative."
        )
    if stripped.startswith("goal "):
        return example["goal"]
    if stripped.startswith("steps "):
        return example["route"]
    if "<-query-" in stripped or "<-search-" in stripped:
        return "The occurrence reads only the KB material named in its input interface."
    if "-persist->" in stripped:
        return "Only the calibrated result may create a versioned KB successor."
    if stripped.startswith("repeat "):
        return example["iteration"]
    if stripped.startswith("on "):
        predicate = stripped[3:].split(" => ", 1)[0]
        return example["outcomes"][predicate]
    if stripped == "}":
        return (
            "This closes the physics example with every claim still limited by the "
            "scope, premises, negative findings, and open obligations stated above."
        )
    raise ValueError(f"cannot produce physics example for ERFL line: {stripped}")


def physics_example_label(line: str) -> str:
    stripped = line.strip()
    if stripped.startswith(("goal ", "steps ", "repeat ", "on ")):
        return "Concrete physics example"
    return "Physics context"


def render() -> str:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    physics_registry = json.loads(PHYSICS_EXAMPLES.read_text(encoding="utf-8"))
    physics_examples = {
        row["flow_id"]: row for row in physics_registry["examples"]
    }
    rows = catalog["flows"]
    # Keep the reference's editorial grouping while deriving every relation
    # from the canonical predicate map.
    predicate_lines = []
    seen_reasoning = False
    for line in PREDICATE_MAP.read_text(encoding="utf-8").splitlines():
        if line.startswith("  reasoning::"):
            if seen_reasoning:
                predicate_lines.append("")
            seen_reasoning = True
        if line.startswith("  output::"):
            line = "       -> " + line.strip()
        predicate_lines.append(line)
    predicate_map = "\n".join(predicate_lines).rstrip()
    lines = [
        "<!--",
        "SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>",
        "",
        "SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>",
        "Neuro-symbolic AI Group",
        "",
        "SPDX-License-" "Identifier: MIT",
        "-->",
        "# All reasoning flows",
        "",
        (
            "This single-file reference contains every canonical workflow represented in "
            "the Essential Reasoning Flow Language (ERFL). It is generated from the "
            "canonical flow catalog and the `.prism` sources; edit those sources rather "
            "than this file. Concrete illustrations are maintained in the physics-example "
            "registry."
        ),
        "",
        f"Catalog coverage: **{len(rows)} canonical flows**.",
        "",
        "An underscore occurrence (`_`) is an unresolved projection gap. A gap-bearing "
        "flow is descriptive and non-executable; it does not license an inferred reasoning type.",
        "",
        (
            "Each interpreted line is paired with a concrete mathematical-physics example "
            "from `agentic/registries/reasoning_flow_physics_examples.yaml`. The examples "
            "illustrate semantics; they are not evidence that the stated physics result holds."
        ),
        "",
        physics_registry["scope_note"],
        "",
        "## Reading long KB-grounded routes",
        "",
        (
            "The preamble binds a concrete KB for reading and versioned persistence. "
            "The steps must then consume the local handle explicitly. A trailing `...` "
            "continues the same logical statement, while indentation is visual only:"
        ),
        "",
        "```text",
        "erfl 0.3",
        (
            '@KB kb0 connect(file("KB/yang-mills-existence-and-mass-gap.kb.md"))'
        ),
        "reasoning kb_grounded_route {",
        '  goal "calibrate a KB-grounded route" -> reviewed',
        "  steps e0:E[kb0,source->ground] -constrain> ...",
        "      a0:A[ground->route] -assume> ...",
        "      d0:D[route->claim] -test> ...",
        "      r0:R[claim->verdict] -calibrate> ...",
        "      e1:E[claim,verdict->status]",
        "  e0 <-query- kb0",
        "  e1 -persist-> kb0",
        "  on e1.reviewed => accept",
        "}",
        "```",
        "",
        (
            "The KB declaration does not itself read, write, or validate any member. The "
            "inverted query arrow records consumption; the regular persistence arrow "
            "authorizes a calibrated successor. The five step "
            "lines parse as one statement; `...` changes only layout, not warrant."
        ),
        "",
        "## Reflective reasoning example",
        "",
        (
            "Reflection takes the system's own trace, claims, and obligations as its object. "
            "It is represented as calibration of the current reasoning state, abductive "
            "formation of a repair, and calibration of what the reflection actually supports:"
        ),
        "",
        "```text",
        "erfl 0.3",
        "reasoning reflective_route_review {",
        '  goal "explain why the active route stalled and propose a bounded repair" -> reflected',
        "  steps e0:E[trace,claims,obligations->self_model] -revise> ...",
        "        a0:A[self_model->repair] -calibrate> ...",
        "        e1:E[self_model,repair->reflection_status]",
        "  on e1.reflected => accept",
        "  on e1.no_discriminating_repair => stop",
        "}",
        "```",
        "",
        (
            "Physics example: after repeated failure to obtain a cutoff-uniform spectral "
            "estimate, the system identifies hidden dependence on lattice spacing as the "
            "recurring failure pattern and proposes a bounded norm-uniformity audit. The "
            "repair remains abductive until tested."
        ),
        "",
        "## Meta-reasoning example",
        "",
        (
            "Meta-reasoning compares reasoning strategies and governs which one should run "
            "next. It evaluates a portfolio and its history rather than directly proving the "
            "object-level scientific claim:"
        ),
        "",
        "```text",
        "erfl 0.3",
        '@KB kb0 connect(file("KB/yang-mills-existence-and-mass-gap.kb.md"))',
        "reasoning meta_strategy_review {",
        '  goal "select, revise, or stop the current reasoning strategy" -> governed',
        "  steps e0:E[kb0,portfolio,trace->strategy_state] -constrain> ...",
        "        (r0:R[strategy_state->defeaters] & a0:A[strategy_state->repairs]) -calibrate> ...",
        "        e1:E[defeaters,repairs->meta_status]",
        "  e0 <-search- kb0",
        "  e1 -persist-> kb0",
        "  on e1.strategy_selected => accept",
        "  on e1.stop_justified => stop",
        "}",
        "```",
        "",
        (
            "Physics example: the meta layer compares a transfer-matrix route, a "
            "correlation-decay route, and a representation-first route against accumulated "
            "failures. It selects another bounded cycle only when a discriminating test and "
            "measurable obligation reduction are available."
        ),
        "",
        (
            "Reflective and meta are higher-order roles here, not ninth and tenth primitive "
            "reasoning symbols. Their higher-order status comes from what their inputs denote "
            "and how the essential operations are composed."
        ),
        "",
        "## Whole-system predicate map",
        "",
        (
            "This projection collapses each detailed `steps` expression to its relation\n"
            "signature. Named outputs mediate every connection to another reasoning\n"
            "program. Indented arrows visually attach each output transition to the\n"
            "reasoning program immediately above it:"
        ),
        "",
        "```text",
        predicate_map,
        "```",
        "",
        (
            "The predicate map is generated from the same canonical programs. Its focused "
            "reference is `docs/reference/reasoning-predicate-map.md`."
        ),
        "",
        "## Index",
        "",
    ]
    for row in rows:
        lines.append(f"- [`{row['id']}`](#{row['id'].replace('_', '-').replace(':', '')})")

    for row in rows:
        flow_path = ROOT / row["path"]
        flow_source = flow_path.read_text(encoding="utf-8").rstrip()
        physics_example = physics_examples[row["id"]]
        source_refs = row.get("source_refs", [row["source"]])
        aliases = ", ".join(f"`{alias}`" for alias in row["aliases"]) or "None"
        sources = ", ".join(f"`{ref}`" for ref in source_refs)
        lines.extend(
            [
                "",
                f"## {row['id']}",
                "",
                f"**Function:** {row['function']}",
                "",
                f"**Aliases:** {aliases}",
                "",
                f"**Projection status:** `{row['projection_status']}`",
                "",
                f"**Source references:** {sources}",
                "",
                "**Fictional worked example:** " + physics_example["worked_example"],
                "",
                "```erfl",
                flow_source,
                "```",
                "",
                "### Line-by-line interpretation",
            ]
        )
        for index, (source_line, interpretation) in enumerate(
            line_interpretations(flow_source), start=1
        ):
            lines.extend(
                [
                    "",
                    f"{index}. `{source_line.strip()}`",
                    "",
                    f"   {interpretation}",
                    "",
                    (
                        f"   **{physics_example_label(source_line)}:** "
                        + physics_example_for_line(
                            source_line, physics_example
                        )
                    ),
                ]
            )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()

    rendered = render()
    if args.write:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(rendered, encoding="utf-8")
    elif args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != rendered:
            raise SystemExit(
                "stale combined reasoning-flow reference; run "
                "agentic/scripts/build_all_reasoning_flows_reference.py --write"
            )
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
