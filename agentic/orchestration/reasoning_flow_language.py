# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Parser and validator for the Epistemic Reasoning Flow Language (ERFL)."""
from __future__ import annotations

import re
import json
from dataclasses import dataclass
from pathlib import Path

TYPE_CODES = {
    "D": "deductive_entailment",
    "A": "abductive_hypothesis_formation",
    "I": "inductive_generalization",
    "T": "structural_analogy_transfer",
    "C": "contrastive_counterfactual_reasoning",
    "M": "model_based_reasoning",
    "R": "critical_refutational_testing",
    "E": "evidential_status_calibration",
}
TOKEN = re.compile(r'\s*(?:(?P<relation>-[a-z][a-z_]*>)|(?P<arrow>>)|(?P<choice>\|)|(?P<parallel>&)|(?P<lpar>\()|(?P<rpar>\))|(?P<optional>\?)|(?P<gap>[a-z][a-z0-9_-]*(?::|[ \t]+)_\[[a-z][a-z0-9_-]*(?:,[a-z][a-z0-9_-]*)*->[a-z][a-z0-9_-]*(?:,[a-z][a-z0-9_-]*)*\])|(?P<typed>(?:[a-z][a-z0-9_-]*(?::|[ \t]+))?[DAITCMRE]\[[a-z][a-z0-9_-]*(?:,[a-z][a-z0-9_-]*)*->[a-z][a-z0-9_-]*(?:,[a-z][a-z0-9_-]*)*\])|(?P<type>[DAITCMRE]))')
IDENT = r"[a-z][a-z0-9_-]*"
KIND_IDENT = r"[A-Z][A-Za-z0-9_]*"
PREDICATE = re.compile(rf"(?P<subject>{IDENT}|reasoning)\.(?P<status>{IDENT})$")
RELATION_REGISTRY = Path(__file__).resolve().parents[1] / "registries/epistemic_relations.yaml"


def _load_relations() -> dict[str, set[tuple[str, str]]]:
    payload = json.loads(RELATION_REGISTRY.read_text(encoding="utf-8"))
    codes = payload["type_codes"]
    result: dict[str, set[tuple[str, str]]] = {}
    for row in payload["relations"]:
        if row["source_types"] == ["="]:
            result[row["id"]] = {(code, code) for code in codes}
            continue
        sources = codes if row["source_types"] == ["*"] else row["source_types"]
        targets = codes if row["target_types"] == ["*"] else row["target_types"]
        result[row["id"]] = {(source, target) for source in sources for target in targets}
    return result


RELATIONS = _load_relations()


class FlowSyntaxError(ValueError):
    pass


def logical_lines(text: str) -> list[str]:
    """Collapse explicitly continued physical lines into ERFL statements.

    A trailing ``...`` continues the current statement on the next non-empty
    line. Indentation is deliberately ignored and remains available for visual
    alignment.
    """
    result: list[str] = []
    parts: list[str] = []
    continuing = False
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        continued = line.endswith("...")
        if continued:
            line = line[:-3].rstrip()
        if continuing or parts:
            parts.append(line)
        else:
            parts = [line]
        continuing = continued
        if not continued:
            result.append(" ".join(part for part in parts if part))
            parts = []
    if continuing or parts:
        raise FlowSyntaxError("dangling '...' continuation at end of document")
    return result


@dataclass
class Tokens:
    values: list[tuple[str, str]]
    index: int = 0

    def peek(self, kind: str) -> bool:
        return self.index < len(self.values) and self.values[self.index][0] == kind

    def take(self, kind: str) -> str:
        if not self.peek(kind):
            found = self.values[self.index] if self.index < len(self.values) else "end"
            raise FlowSyntaxError(f"expected {kind}, found {found}")
        value = self.values[self.index][1]
        self.index += 1
        return value


def _tokens(text: str) -> Tokens:
    values: list[tuple[str, str]] = []
    position = 0
    while position < len(text):
        match = TOKEN.match(text, position)
        if not match:
            raise FlowSyntaxError(f"invalid route syntax near {text[position:]!r}")
        kind = match.lastgroup
        assert kind is not None
        values.append((kind, match.group(kind)))
        position = match.end()
    return Tokens(values)


def parse_expression(text: str) -> dict:
    tokens = _tokens(text.strip())

    def atom() -> dict:
        if tokens.peek("gap"):
            raw = tokens.take("gap")
            head, binding = raw[:-1].split("[", 1)
            alias, code = head.split(":", 1) if ":" in head else head.split()
            inputs, outputs = binding.split("->", 1)
            node = {
                "op": "gap", "code": code, "reasoning_type": "unresolved_projection_gap",
                "alias": alias, "inputs": inputs.split(","), "outputs": outputs.split(","),
            }
        elif tokens.peek("typed"):
            raw = tokens.take("typed")
            head, binding = raw[:-1].split("[", 1)
            if ":" in head:
                alias, code = head.split(":", 1)
            else:
                parts = head.split()
                alias, code = (parts[0], parts[1]) if len(parts) == 2 else (None, parts[0])
            inputs, outputs = binding.split("->", 1)
            node = {
                "op": "type", "code": code, "reasoning_type": TYPE_CODES[code],
                "alias": alias, "inputs": inputs.split(","), "outputs": outputs.split(","),
            }
        elif tokens.peek("type"):
            code = tokens.take("type")
            node = {"op": "type", "code": code, "reasoning_type": TYPE_CODES[code], "alias": None, "inputs": [], "outputs": []}
        elif tokens.peek("lpar"):
            tokens.take("lpar")
            node = sequence()
            tokens.take("rpar")
        else:
            raise FlowSyntaxError("route atom must be a reasoning type or parenthesized expression")
        if tokens.peek("optional"):
            tokens.take("optional")
            node = {"op": "optional", "value": node}
        return node

    def parallel() -> dict:
        values = [atom()]
        while tokens.peek("parallel"):
            tokens.take("parallel")
            values.append(atom())
        return values[0] if len(values) == 1 else {"op": "all", "values": values}

    def choice() -> dict:
        values = [parallel()]
        while tokens.peek("choice"):
            tokens.take("choice")
            values.append(parallel())
        return values[0] if len(values) == 1 else {"op": "choice", "values": values}

    def sequence() -> dict:
        values = [choice()]
        relations: list[dict] = []
        while tokens.peek("arrow") or tokens.peek("relation"):
            if tokens.peek("relation"):
                raw = tokens.take("relation")
                relations.append({"name": raw[1:-1], "explicit": True})
            else:
                tokens.take("arrow")
                relations.append({"name": "feeds", "explicit": False})
            values.append(choice())
        return values[0] if len(values) == 1 else {"op": "sequence", "values": values, "relations": relations}

    result = sequence()
    if tokens.index != len(tokens.values):
        raise FlowSyntaxError(f"unexpected token {tokens.values[tokens.index]}")
    return result


def reasoning_codes(node: dict) -> list[str]:
    if node["op"] == "gap":
        return []
    if node["op"] == "type":
        return [node["code"]]
    if node["op"] == "optional":
        return reasoning_codes(node["value"])
    return [code for value in node["values"] for code in reasoning_codes(value)]


def entry_codes(node: dict) -> set[str]:
    if node["op"] == "gap":
        return {"_"}
    if node["op"] == "type":
        return {node["code"]}
    if node["op"] == "optional":
        return entry_codes(node["value"])
    if node["op"] == "sequence":
        return entry_codes(node["values"][0])
    return set().union(*(entry_codes(value) for value in node["values"]))


def exit_codes(node: dict) -> set[str]:
    if node["op"] == "gap":
        return {"_"}
    if node["op"] == "type":
        return {node["code"]}
    if node["op"] == "optional":
        return exit_codes(node["value"])
    if node["op"] == "sequence":
        return exit_codes(node["values"][-1])
    return set().union(*(exit_codes(value) for value in node["values"]))


def input_handles(node: dict) -> set[str]:
    if node["op"] in {"type", "gap"}:
        return set(node.get("inputs", []))
    if node["op"] == "optional":
        return input_handles(node["value"])
    if node["op"] == "sequence":
        return input_handles(node["values"][0])
    return set().union(*(input_handles(value) for value in node["values"]))


def output_handles(node: dict) -> set[str]:
    if node["op"] in {"type", "gap"}:
        return set(node.get("outputs", []))
    if node["op"] == "optional":
        return output_handles(node["value"])
    if node["op"] == "sequence":
        return output_handles(node["values"][-1])
    if node["op"] == "choice":
        branch_outputs = [output_handles(value) for value in node["values"]]
        if branch_outputs and any(value != branch_outputs[0] for value in branch_outputs[1:]):
            raise FlowSyntaxError("choice branches must expose the same output handles")
        return branch_outputs[0] if branch_outputs else set()
    return set().union(*(output_handles(value) for value in node["values"]))


def occurrences(node: dict) -> list[dict]:
    if node["op"] in {"type", "gap"}:
        return [node]
    if node["op"] == "optional":
        return occurrences(node["value"])
    return [item for value in node["values"] for item in occurrences(value)]


def validate_relational_coherence(flow: dict, *, require_explicit: bool = True) -> list[dict]:
    """Validate local epistemic compatibility without inventing hidden adapters."""
    checks: list[dict] = []

    def visit(node: dict, location: str) -> None:
        if node["op"] == "optional":
            visit(node["value"], location + ".optional")
            return
        if node["op"] in {"choice", "all"}:
            for index, value in enumerate(node["values"]):
                visit(value, f"{location}.{node['op']}[{index}]")
            return
        if node["op"] != "sequence":
            return
        for index, value in enumerate(node["values"]):
            visit(value, f"{location}.sequence[{index}]")
        for index, relation in enumerate(node["relations"]):
            name = relation["name"]
            if require_explicit and not relation["explicit"]:
                raise FlowSyntaxError(f"{location}: unlabelled dependency is not relationally coherent")
            if name not in RELATIONS:
                raise FlowSyntaxError(f"{location}: unknown epistemic relation {name}")
            pairs = {
                (source, target)
                for source in exit_codes(node["values"][index])
                for target in entry_codes(node["values"][index + 1])
            }
            unknown_gap = any("_" in pair for pair in pairs)
            invalid = [] if unknown_gap else sorted(pairs - RELATIONS[name])
            if invalid:
                raise FlowSyntaxError(f"{location}: relation {name} is incoherent for {invalid}")
            left_outputs = output_handles(node["values"][index])
            right_inputs = input_handles(node["values"][index + 1])
            if not left_outputs or not right_inputs or not left_outputs.intersection(right_inputs):
                raise FlowSyntaxError(
                    f"{location}: relation {name} has no conserved claim/state handle "
                    f"between {sorted(left_outputs)} and {sorted(right_inputs)}"
                )
            checks.append({
                "location": location, "relation": name, "pairs": sorted(pairs),
                "claim_policy": "conserve_source_taint_and_weakest_claim_ceiling",
                "coherence": "unknown_gap" if unknown_gap else "locally_valid",
            })

    visit(flow["steps"], "steps")
    step_occurrences = occurrences(flow["steps"])
    aliases = [row.get("alias") for row in step_occurrences]
    if require_explicit and any(not alias for alias in aliases):
        raise FlowSyntaxError("every reasoning occurrence needs a local alias and input/output binding")
    if len(set(aliases)) != len(aliases):
        raise FlowSyntaxError("reasoning occurrence aliases must be unique")
    by_alias = {row["alias"]: row for row in step_occurrences if row.get("alias")}
    for index, repeat in enumerate(flow["repeats"]):
        if not repeat.get("measure"):
            raise FlowSyntaxError(f"repeat[{index}] requires an observable progress measure")
        visit(repeat["body"], f"repeat[{index}]")
        repeated = occurrences(repeat["body"])
        repeat_aliases = [row.get("alias") for row in repeated]
        if any(not alias for alias in repeat_aliases) or len(set(repeat_aliases)) != len(repeat_aliases):
            raise FlowSyntaxError(f"repeat[{index}] requires unique named occurrences")
        subject = repeat["until"].split(".", 1)[0]
        repeat_by_alias = {row["alias"]: row for row in repeated}
        if subject != "reasoning" and subject not in repeat_by_alias:
            raise FlowSyntaxError(f"repeat[{index}] predicate references an occurrence outside its body")
        if subject != "reasoning" and repeat_by_alias[subject]["code"] != "E":
            raise FlowSyntaxError(f"repeat[{index}] termination requires a calibrated occurrence")
        if exit_codes(repeat["body"]) != {"E"}:
            raise FlowSyntaxError(f"repeat[{index}] body must terminate in calibration")
    if exit_codes(flow["steps"]) != {"E"}:
        raise FlowSyntaxError("every complete steps path must terminate in calibration")
    for handler in flow["handlers"]:
        subject = handler["when"].split(".", 1)[0]
        if subject != "reasoning" and subject not in by_alias:
            raise FlowSyntaxError(f"handler references unknown occurrence alias: {subject}")
        if handler["action"] in {"accept"} or handler["action"].startswith("switch @"):
            if subject == "reasoning" or by_alias[subject]["code"] != "E":
                raise FlowSyntaxError("acceptance and workflow switches require a calibrated occurrence guard")
    declared_kbs = {row["id"] for row in flow.get("knowledge_bases", [])}
    for interaction in flow.get("kb_interactions", []):
        if interaction["kb"] not in declared_kbs:
            raise FlowSyntaxError(f"KB interaction references unknown KB: {interaction['kb']}")
        if interaction["occurrence"] not in by_alias:
            raise FlowSyntaxError(f"KB interaction references unknown occurrence: {interaction['occurrence']}")
        occurrence = by_alias[interaction["occurrence"]]
        if interaction["operation"] in {"query", "search"}:
            if interaction["kb"] not in occurrence.get("inputs", []):
                raise FlowSyntaxError("KB query/search must expose the KB handle as an input")
        elif occurrence["code"] != "E":
            raise FlowSyntaxError("KB persistence requires a calibrated E occurrence")
    return checks


def parse(text: str, *, known_workflows: set[str] | None = None) -> dict:
    lines = logical_lines(text)
    if not lines or lines[0] not in {"erfl 0.1", "erfl 0.2", "erfl 0.3"}:
        raise FlowSyntaxError("document must start with a supported ERFL version (0.1, 0.2, or 0.3)")
    header_index = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.startswith("reasoning ")),
        -1,
    )
    header = re.fullmatch(
        rf"reasoning ({IDENT}) \{{", lines[header_index] if header_index >= 0 else ""
    )
    if not header or lines[-1] != "}":
        raise FlowSyntaxError("reasoning needs 'reasoning <id> {' header and closing brace")
    flow: dict = {
        "version": lines[0].split()[1], "id": header.group(1),
        "handlers": [], "repeats": [], "knowledge_bases": [], "kb_interactions": [],
    }
    for line in lines[1:header_index]:
        resource = re.fullmatch(rf'@KB ({IDENT}) connect\(file\("([^"]+)"\)\)', line)
        if resource:
            knowledge = {"id": resource.group(1), "ref": resource.group(2), "connector": "file"}
            if any(row["id"] == knowledge["id"] for row in flow["knowledge_bases"]):
                raise FlowSyntaxError(f"duplicate knowledge-base id: {knowledge['id']}")
            flow["knowledge_bases"].append(knowledge)
            continue
        reference = re.fullmatch(
            rf'knowledge ({IDENT}) at "([^"]+)" access (read|read_write) persist (none|versioned)',
            line,
        )
        if not reference:
            raise FlowSyntaxError("ERFL preamble accepts only @KB resources or legacy knowledge references")
        knowledge = {
            "id": reference.group(1), "ref": reference.group(2),
            "access": reference.group(3), "persistence": reference.group(4),
        }
        if knowledge["access"] == "read" and knowledge["persistence"] != "none":
            raise FlowSyntaxError("read-only knowledge cannot declare persistence")
        if any(row["id"] == knowledge["id"] for row in flow["knowledge_bases"]):
            raise FlowSyntaxError(f"duplicate knowledge-base id: {knowledge['id']}")
        flow["knowledge_bases"].append(knowledge)

    index = header_index + 1
    while index < len(lines) - 1:
        line = lines[index]
        if line.startswith("knowledge "):
            raise FlowSyntaxError("knowledge references belong in the document preamble before reasoning")
        elif line.startswith("goal "):
            if "goal" in flow:
                raise FlowSyntaxError("reasoning may declare only one goal")
            if line == "goal {":
                goal = {"criteria": [], "evidence": [], "constraints": []}
                index += 1
                while index < len(lines) - 1 and lines[index] != "}":
                    field = lines[index]
                    scalar = re.fullmatch(r'(summary|target) "?([^\"]+)"?', field)
                    item = re.fullmatch(
                        rf'(criterion|evidence|constraint) ({IDENT}) "([^"]+)"', field
                    )
                    satisfaction = re.fullmatch(rf'satisfy (all|any)\(({IDENT}(?:,{IDENT})*)\)', field)
                    if scalar:
                        key = "description" if scalar.group(1) == "summary" else "target_state"
                        if key in goal:
                            raise FlowSyntaxError(f"structured goal repeats {scalar.group(1)}")
                        goal[key] = scalar.group(2)
                    elif item:
                        collection = {"criterion": "criteria", "evidence": "evidence", "constraint": "constraints"}[item.group(1)]
                        goal[collection].append({"id": item.group(2), "description": item.group(3)})
                    elif satisfaction:
                        if "satisfaction" in goal:
                            raise FlowSyntaxError("structured goal repeats satisfy")
                        goal["satisfaction"] = {
                            "operator": satisfaction.group(1),
                            "criteria": satisfaction.group(2).split(","),
                        }
                    else:
                        raise FlowSyntaxError(f"invalid structured goal field: {field}")
                    index += 1
                if index >= len(lines) - 1:
                    raise FlowSyntaxError("structured goal needs a closing brace")
                if "target_state" not in goal or not goal["criteria"]:
                    raise FlowSyntaxError("structured goal requires target and at least one criterion")
                criterion_ids = [row["id"] for row in goal["criteria"]]
                all_ids = criterion_ids + [row["id"] for row in goal["evidence"]] + [row["id"] for row in goal["constraints"]]
                if len(set(all_ids)) != len(all_ids):
                    raise FlowSyntaxError("structured goal item identifiers must be unique")
                if "satisfaction" not in goal:
                    raise FlowSyntaxError("structured goal requires an explicit satisfy policy")
                unknown = set(goal["satisfaction"]["criteria"]) - set(criterion_ids)
                if unknown:
                    raise FlowSyntaxError(f"satisfy references unknown criteria: {sorted(unknown)}")
                flow["goal"] = goal
            else:
                match = re.fullmatch(r'goal "([^"]+)" -> ([a-z][a-z0-9_-]*)', line)
                if not match:
                    raise FlowSyntaxError("goal syntax is shorthand 'goal \"text\" -> state' or a structured goal block")
                flow["goal"] = {"description": match.group(1), "target_state": match.group(2)}
        elif line.startswith("steps "):
            if "steps" in flow:
                raise FlowSyntaxError("reasoning may declare only one steps statement")
            flow["steps"] = parse_expression(line[6:])
        elif match := re.fullmatch(rf"({IDENT}) <-(query|search)- ({IDENT})", line):
            flow["kb_interactions"].append({
                "occurrence": match.group(1), "operation": match.group(2),
                "kb": match.group(3), "direction": "read",
            })
        elif match := re.fullmatch(rf"({IDENT}) -persist-> ({IDENT})", line):
            flow["kb_interactions"].append({
                "occurrence": match.group(1), "operation": "persist",
                "kb": match.group(2), "direction": "write",
            })
        elif line.startswith("repeat "):
            match = re.fullmatch(rf"repeat (\d+)\.\.(\d+) \[(.+)\] until ((?:{IDENT}|reasoning)\.{IDENT}) measure ({IDENT})", line)
            if not match:
                raise FlowSyntaxError("invalid repeat statement")
            minimum, maximum = int(match.group(1)), int(match.group(2))
            if minimum < 0 or maximum < minimum or maximum > 20:
                raise FlowSyntaxError("repeat bounds must satisfy 0 <= min <= max <= 20")
            predicate = match.group(4)
            if not PREDICATE.fullmatch(predicate):
                raise FlowSyntaxError(f"invalid repeat predicate: {predicate}")
            flow["repeats"].append({"min": minimum, "max": maximum, "body": parse_expression(match.group(3)), "until": predicate, "measure": match.group(5)})
        elif line.startswith("on "):
            match = re.fullmatch(r"on (.+) => (stop|accept|switch @[a-z][a-z0-9_-]*)", line)
            if not match or not PREDICATE.fullmatch(match.group(1)):
                raise FlowSyntaxError("invalid event handler")
            action = match.group(2)
            if action.startswith("switch @"):
                target = action[8:]
                if known_workflows is not None and target not in known_workflows:
                    raise FlowSyntaxError(f"unknown workflow switch target: {target}")
            flow["handlers"].append({"when": match.group(1), "action": action})
        else:
            raise FlowSyntaxError(f"unknown statement: {line}")
        index += 1
    if "goal" not in flow or "steps" not in flow:
        raise FlowSyntaxError("reasoning requires exactly one goal and steps statement")
    consumed = input_handles(flow["steps"])
    for repeat in flow["repeats"]:
        consumed.update(input_handles(repeat["body"]))
    unused_knowledge = {row["id"] for row in flow["knowledge_bases"]} - consumed
    if unused_knowledge:
        raise FlowSyntaxError(f"declared knowledge bases are not consumed: {sorted(unused_knowledge)}")
    codes = reasoning_codes(flow["steps"])
    if "E" not in codes:
        raise FlowSyntaxError("route must expose evidential status calibration (E)")
    if not any(handler["action"] in {"stop", "accept"} or handler["action"].startswith("switch @") for handler in flow["handlers"]):
        raise FlowSyntaxError("reasoning needs at least one explicit terminal or switch handler")
    seen_handlers: dict[str, str] = {}
    for handler in flow["handlers"]:
        previous = seen_handlers.setdefault(handler["when"], handler["action"])
        if previous != handler["action"]:
            raise FlowSyntaxError(f"contradictory handlers for {handler['when']}")
    return flow


def parse_file(path: Path, *, known_workflows: set[str] | None = None) -> dict:
    return parse(path.read_text(encoding="utf-8"), known_workflows=known_workflows)
