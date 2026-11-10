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
"""Generate workflow graph reports from AGENTS.md."""

from __future__ import annotations

import argparse
import html
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


STACK_HEADING_RE = re.compile(r"^###\s+(.+?)\s*$")
PROJECT_STACK_HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")
SKILL_RE = re.compile(r"\$([A-Za-z0-9_-]+)")
NUMBERED_SKILL_RE = re.compile(r"^\d+\.\s+`\$([A-Za-z0-9_-]+)`")
FIELD_RE = re.compile(r"^-\s+(Mode|Trigger|Artifact entrypoints|Handoff):\s*(.*)$")

DISPLAY_TOKEN_OVERRIDES = {
    "api": "API",
    "cdc": "CDC",
    "fec": "FEC",
    "html": "HTML",
    "json": "JSON",
    "mcp": "MCP",
    "prbs": "PRBS",
    "rtl": "RTL",
    "rtlpy": "RTLPy",
    "rx": "RX",
    "sv": "SV",
    "tx": "TX",
}

EDGE_LABEL_TAXONOMY: dict[str, dict[str, str]] = {
    "family_contains_workflow": {
        "label_template": "groups {output}",
        "default_output": "workflow_group",
        "description": "Hierarchy edge from workflow family to one contained workflow stack.",
    },
    "workflow_entry": {
        "label_template": "starts with {output}",
        "default_output": "workflow_context",
        "description": "Entry edge from a workflow stack to its first ordered hook.",
    },
    "workflow_sequence": {
        "label_template": "passes {output}",
        "default_output": "workflow_context",
        "description": "Ordered in-stack handoff where one hook's result becomes the next hook's input surface.",
    },
    "workflow_reflective_loop": {
        "label_template": "returns {output}",
        "default_output": "workflow_update",
        "description": "Guarded reflective edge that can revise criteria, hooks, or workflow structure.",
    },
    "stack_uses_skill": {
        "label_template": "invokes {output}",
        "default_output": "workflow_context",
        "description": "Invocation edge from a workflow stack to a reusable skill hook.",
    },
    "skill_handoff": {
        "label_template": "hands off {output}",
        "default_output": "workflow_context",
        "description": "Cross-skill edge showing the expected output type handed to the next hook.",
    },
    "reflective_feedback": {
        "label_template": "feeds back {output}",
        "default_output": "workflow_update",
        "description": "Cross-stack feedback edge from review/refinement/guard conclusions to the workflow definition.",
    },
    "reflective_external_reference": {
        "label_template": "leaves view as {output}",
        "default_output": "workflow_update",
        "description": "Dashed boundary edge used when a reflective target exists but the concrete target node is outside the active view.",
    },
}


@dataclass
class Stack:
    title: str
    slug: str
    mode: str
    trigger: str
    artifact_entrypoints: str
    handoff: str
    description: str
    skills: list[str]
    guardrails: list[str]
    source_line: int
    family: str
    reflection_roles: list[str]


def slugify(value: str) -> str:
    value = value.lower().replace("`", "")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "workflow"


def display_label(value: str) -> str:
    """Turn machine-facing IDs into compact review-facing labels."""
    value = value.replace("$", "").strip()
    parts = [part for part in re.split(r"[-_\s]+", value) if part]
    return " ".join(DISPLAY_TOKEN_OVERRIDES.get(part.lower(), part.capitalize()) for part in parts)


def skill_display_label(skill: str) -> str:
    return display_label(skill)


def output_display_label(output_type: str) -> str:
    return display_label(output_type)


def edge_label(edge_type: str, output_type: str = "") -> str:
    taxonomy = EDGE_LABEL_TAXONOMY.get(edge_type)
    if not taxonomy:
        return display_label(edge_type)
    output = output_display_label(output_type or taxonomy["default_output"])
    return taxonomy["label_template"].format(output=output)


def clean_markdown(value: str) -> str:
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = value.replace("`", "")
    return " ".join(value.split())


def stack_sections(text: str) -> list[tuple[str, int, list[str]]]:
    lines = text.splitlines()
    sections: list[tuple[str, int, list[str]]] = []
    current_title = ""
    current_start = 0
    current_lines: list[str] = []
    for lineno, line in enumerate(lines, start=1):
        match = STACK_HEADING_RE.match(line)
        if match:
            title = match.group(1).strip()
            is_workflow_stack = title == "Default Workflow Skill" or title.endswith("Stack")
            if current_title:
                sections.append((current_title, current_start, current_lines))
                current_title = ""
                current_lines = []
            if is_workflow_stack:
                current_title = title
                current_start = lineno
                current_lines = []
            continue
        if current_title:
            current_lines.append(line)
    if current_title:
        sections.append((current_title, current_start, current_lines))
    return sections


def classify_family(title: str, trigger: str, skills: list[str]) -> str:
    haystack = " ".join([title, trigger, *skills]).lower()
    rules = [
        ("Control Plane", ("default workflow", "shared_runner", "route", "router", "control")),
        ("Meta Learning", ("meta", "second-order", "feedback", "skill evolution", "sufficiency")),
        ("Source Intake", ("specification", "rtl interpretation", "book", "source", "prose", "diagram")),
        ("Mathematical Discovery And Proof", ("theorem", "proof", "conjecture", "abduce", "deduce", "mathlib")),
        ("Execution And Runtime", ("rtlpy", "emulator", "execution", "runtime", "mcp")),
        ("Testing And Validation", ("test", "vacuity", "coverage", "scenario", "oracle", "validation")),
        ("Review And Signoff", ("critic", "review", "signoff", "consistency", "calibration", "redundancy", "audit")),
        ("Reference And Comparison", ("reference", "inverse", "post-hoc", "comparison", "gold", "why-not")),
        ("Writing And Reporting", ("writing", "report", "readability", "explanation", "html")),
        ("Project Specific", ("rx impairment", "project workflow", "use-case")),
    ]
    for family, needles in rules:
        if any(needle in haystack for needle in needles):
            return family
    return "Specialized Deep Dives"


def reflection_roles(title: str, trigger: str, skills: list[str], guardrails: list[str]) -> list[str]:
    haystack = " ".join([title, trigger, *skills, *guardrails]).lower()
    roles = []
    role_rules = [
        ("Critique", ("critic", "review", "audit", "diagnosis", "diagnostic")),
        ("Gap Planning", ("gap", "todo", "planner", "planning", "forecast")),
        ("Refinement", ("refiner", "refinement", "improvement", "repair", "calibration")),
        ("Guard", ("guard", "closure", "monotonic", "gate")),
        ("Second Order", ("second-order", "feedback", "meta", "abduction", "abductive")),
    ]
    for role, needles in role_rules:
        if any(needle in haystack for needle in needles):
            roles.append(role)
    return roles


def parse_stacks(contract_path: Path) -> list[Stack]:
    text = contract_path.read_text(encoding="utf-8")
    stacks: list[Stack] = []
    for title, source_line, lines in stack_sections(text):
        fields = {
            "Mode": "",
            "Trigger": "",
            "Artifact entrypoints": "",
            "Handoff": "",
        }
        skills: list[str] = []
        guardrails: list[str] = []
        in_guardrails = False
        for line in lines:
            field_match = FIELD_RE.match(line)
            if field_match:
                fields[field_match.group(1)] = clean_markdown(field_match.group(2))
            if line.strip().startswith("Guardrails:"):
                in_guardrails = True
                continue
            heading_match = STACK_HEADING_RE.match(line)
            if heading_match:
                in_guardrails = False
            for skill in SKILL_RE.findall(line):
                if skill not in skills:
                    skills.append(skill)
            if in_guardrails and line.startswith("- "):
                guardrails.append(clean_markdown(line[2:]))
        family = classify_family(title, fields["Trigger"], skills)
        roles = reflection_roles(title, fields["Trigger"], skills, guardrails)
        stacks.append(
            Stack(
                title=title,
                slug=slugify(title),
                mode=fields["Mode"],
                trigger=fields["Trigger"],
                artifact_entrypoints=fields["Artifact entrypoints"],
                handoff=fields["Handoff"],
                description=workflow_description(title, fields["Mode"], fields["Trigger"], fields["Handoff"]),
                skills=skills,
                guardrails=guardrails,
                source_line=source_line,
                family=family,
                reflection_roles=roles,
            )
        )
    return stacks


def project_stack_sections(text: str) -> list[tuple[str, int, list[str]]]:
    """Extract project-support stack sections from proj_skills/INDEX.md."""
    lines = text.splitlines()
    sections: list[tuple[str, int, list[str]]] = []
    current_title = ""
    current_start = 0
    current_lines: list[str] = []
    for lineno, line in enumerate(lines, start=1):
        match = PROJECT_STACK_HEADING_RE.match(line)
        if match:
            if current_title:
                sections.append((current_title, current_start, current_lines))
            title = match.group(1).strip()
            is_project_stack = title in {
                "Project Front Door",
                "Workflow Architecture",
                "Workflow Governance And Health",
                "Project Evolution",
            }
            current_title = title if is_project_stack else ""
            current_start = lineno
            current_lines = []
            continue
        if current_title:
            current_lines.append(line)
    if current_title:
        sections.append((current_title, current_start, current_lines))
    return sections


def parse_project_support_stacks(index_path: Path, source_line_offset: int = 100_000) -> list[Stack]:
    """Parse project-level reporting and visualization stacks as supplemental architecture."""
    text = index_path.read_text(encoding="utf-8")
    stacks: list[Stack] = []
    for title, source_line, lines in project_stack_sections(text):
        fields = {
            "Mode": "",
            "Trigger": "",
            "Artifact entrypoints": "",
            "Handoff": "",
        }
        numbered_skills: list[str] = []
        automatic_entrypoint = ""
        architecture_dependency = ""
        for line in lines:
            field_match = FIELD_RE.match(line)
            if field_match:
                fields[field_match.group(1)] = clean_markdown(field_match.group(2))
            numbered_match = NUMBERED_SKILL_RE.match(line.strip())
            if numbered_match and numbered_match.group(1) not in numbered_skills:
                numbered_skills.append(numbered_match.group(1))
            if line.startswith("- Automatic entrypoint:"):
                entrypoints = SKILL_RE.findall(line)
                automatic_entrypoint = entrypoints[0] if entrypoints else ""
            if line.startswith("- Architecture dependency:"):
                dependencies = SKILL_RE.findall(line)
                architecture_dependency = dependencies[0] if dependencies else ""

            if "Public entrypoint:" in line:
                entrypoints = SKILL_RE.findall(line)
                automatic_entrypoint = entrypoints[0] if entrypoints else automatic_entrypoint

        skills = list(numbered_skills)
        if automatic_entrypoint and automatic_entrypoint not in skills:
            skills.append(automatic_entrypoint)
        if not skills:
            skills = [
                skill
                for skill in (architecture_dependency, automatic_entrypoint)
                if skill
            ]
        stacks.append(
            Stack(
                title=title,
                slug=slugify(title),
                mode=fields["Mode"],
                trigger=fields["Trigger"],
                artifact_entrypoints=fields["Artifact entrypoints"],
                handoff=fields["Handoff"],
                description=workflow_description(title, fields["Mode"], fields["Trigger"], fields["Handoff"]),
                skills=skills,
                guardrails=[],
                source_line=source_line_offset + source_line,
                family="Project Support",
                reflection_roles=reflection_roles(title, fields["Trigger"], skills, []),
            )
        )
    return stacks


def shared_skills(stacks: list[Stack]) -> list[dict[str, object]]:
    users: dict[str, list[str]] = defaultdict(list)
    for stack in stacks:
        for skill in stack.skills:
            users[skill].append(stack.title)
    shared = [
        {"skill": skill, "count": len(stack_titles), "stacks": stack_titles}
        for skill, stack_titles in users.items()
        if len(stack_titles) > 1
    ]
    return sorted(shared, key=lambda item: (-int(item["count"]), str(item["skill"])))


def role_counts(stacks: list[Stack]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for stack in stacks:
        for role in stack.reflection_roles:
            counts[role] += 1
    return counts


def graph_elements(stacks: list[Stack]) -> list[dict[str, object]]:
    elements: list[dict[str, object]] = []
    seen_nodes: set[str] = set()
    seen_edges: set[str] = set()

    def add_node(node_id: str, label: str, node_type: str, **data: object) -> None:
        if node_id in seen_nodes:
            return
        seen_nodes.add(node_id)
        elements.append({"data": {"id": node_id, "label": label, "node_type": node_type, **data}})

    def add_edge(edge_id: str, source: str, target: str, label: str, **data: object) -> None:
        if edge_id in seen_edges:
            return
        seen_edges.add(edge_id)
        elements.append(
            {
                "data": {
                    "id": edge_id,
                    "source": source,
                    "target": target,
                    "label": label,
                    **data,
                }
            }
        )

    for stack in stacks:
        stack_id = f"stack:{stack.slug}"
        add_node(
            stack_id,
            stack.title,
            "stack",
            family=stack.family,
            description=stack.description,
            mode=stack.mode,
            trigger=stack.trigger,
            handoff=stack.handoff,
            hooks=len(stack.skills),
            roles=", ".join(stack.reflection_roles),
        )
        for index, skill in enumerate(stack.skills, start=1):
            skill_id = f"skill:{skill}"
            role = skill_role(skill)
            skill_label = skill_display_label(skill)
            output_type = edge_output_type(skill)
            posture = skill_execution_posture(skill)
            add_node(
                skill_id,
                skill_label,
                "skill",
                skill=skill,
                skill_label=skill_label,
                role=role,
                execution_posture=posture,
                execution_posture_detail=skill_execution_posture_description(posture),
                description=f"{skill_label} contributes {output_display_label(output_type)} evidence or action.",
                detailed_description=skill_detailed_description(skill),
            )
            add_edge(
                f"uses:{stack.slug}:{skill}",
                stack_id,
                skill_id,
                edge_label("stack_uses_skill", output_type),
                edge_type="stack_uses_skill",
                output_type=output_type,
                order=index,
                stack=stack.title,
                property=f"{stack.title} invokes {skill_label} as hook {index}.",
            )
            if index > 1:
                previous = stack.skills[index - 2]
                previous_label = skill_display_label(previous)
                add_edge(
                    f"handoff:{stack.slug}:{previous}:{skill}",
                    f"skill:{previous}",
                    skill_id,
                    edge_label("skill_handoff", output_type),
                    edge_type="skill_handoff",
                    output_type=output_type,
                    order=index,
                    stack=stack.title,
                    property=f"{previous_label} output feeds {skill_label} in {stack.title}.",
                )
        if {"Critique", "Gap Planning", "Refinement", "Guard"}.issubset(set(stack.reflection_roles)):
            add_edge(
                f"feedback:{stack.slug}",
                f"skill:{stack.skills[-1]}" if stack.skills else stack_id,
                stack_id,
                edge_label("reflective_feedback", "workflow_update"),
                edge_type="reflective_feedback",
                output_type="workflow_update",
                target_visibility="in_view",
                target_surface="workflow_stack",
                stack=stack.title,
                property="Review findings can update criteria, hooks, or skill definitions under guard control.",
            )
    return elements


def workflow_graph_elements(stacks: list[Stack]) -> list[dict[str, object]]:
    """Build a hierarchy-preserving graph: family -> workflow -> ordered hook steps."""
    elements: list[dict[str, object]] = []
    seen_nodes: set[str] = set()
    seen_edges: set[str] = set()

    def add_node(node_id: str, label: str, node_type: str, position: dict[str, float] | None = None, **data: object) -> None:
        if node_id in seen_nodes:
            return
        seen_nodes.add(node_id)
        element: dict[str, object] = {"data": {"id": node_id, "label": label, "node_type": node_type, **data}}
        if position:
            element["position"] = position
        elements.append(element)

    def add_edge(edge_id: str, source: str, target: str, label: str, **data: object) -> None:
        if edge_id in seen_edges:
            return
        seen_edges.add(edge_id)
        elements.append({"data": {"id": edge_id, "source": source, "target": target, "label": label, **data}})

    stacks_by_family: dict[str, list[Stack]] = defaultdict(list)
    for stack in stacks:
        stacks_by_family[stack.family].append(stack)

    for family, family_stacks in sorted(stacks_by_family.items(), key=lambda item: item[0]):
        family_id = f"family:{slugify(family)}"
        hook_count = sum(len(stack.skills) for stack in family_stacks)
        add_node(
            family_id,
            family,
            "family",
            description=f"{family} contains {len(family_stacks)} workflow stacks and {hook_count} ordered hooks.",
            stacks=len(family_stacks),
            hooks=hook_count,
        )

    sorted_stacks = sorted(stacks, key=lambda item: item.source_line)
    for workflow_order, stack in enumerate(sorted_stacks, start=1):
        family_id = f"family:{slugify(stack.family)}"
        stack_id = f"workflow:{stack.slug}"
        row_y = workflow_order * 86
        add_node(
            stack_id,
            stack.title,
            "workflow",
            position={"x": 80, "y": row_y},
            parent=family_id,
            family=stack.family,
            description=stack.description,
            mode=stack.mode,
            trigger=stack.trigger,
            handoff=stack.handoff,
            hooks=len(stack.skills),
            workflow_order=workflow_order,
            roles=", ".join(stack.reflection_roles),
        )
        add_edge(
            f"contains:{slugify(stack.family)}:{stack.slug}",
            family_id,
            stack_id,
            edge_label("family_contains_workflow", "workflow_group"),
            edge_type="family_contains_workflow",
            output_type="workflow_group",
            stack=stack.title,
            property=f"{stack.family} groups the {stack.title} workflow.",
        )
        previous_step_id = ""
        first_step_id = ""
        for index, skill in enumerate(stack.skills, start=1):
            step_id = f"step:{stack.slug}:{index}"
            role = skill_role(skill)
            skill_label = skill_display_label(skill)
            output_type = edge_output_type(skill)
            posture = skill_execution_posture(skill)
            add_node(
                step_id,
                f"{index}. {skill_label}",
                "workflow_step",
                position={"x": 180 + index * 58, "y": row_y},
                parent=stack_id,
                stack=stack.title,
                family=stack.family,
                skill=skill,
                skill_label=skill_label,
                role=role,
                execution_posture=posture,
                execution_posture_detail=skill_execution_posture_description(posture),
                step_index=index,
                output_type=output_type,
                description=f"Step {index} in {stack.title}: {skill_label} produces {output_display_label(output_type)}.",
                detailed_description=skill_detailed_description(skill, stack.title, index),
            )
            if index == 1:
                first_step_id = step_id
                add_edge(
                    f"entry:{stack.slug}:{skill}",
                    stack_id,
                    step_id,
                    edge_label("workflow_entry", output_type),
                    edge_type="workflow_entry",
                    output_type=output_type,
                    stack=stack.title,
                    order=index,
                    property=f"{stack.title} starts with {skill_label}.",
                )
            else:
                add_edge(
                    f"sequence:{stack.slug}:{index - 1}:{index}",
                    previous_step_id,
                    step_id,
                    edge_label("workflow_sequence", output_type),
                    edge_type="workflow_sequence",
                    output_type=output_type,
                    stack=stack.title,
                    order=index,
                    property=f"Step {index - 1} output feeds step {index} ({skill_label}) in {stack.title}.",
                )
            previous_step_id = step_id
        if (
            first_step_id
            and previous_step_id
            and {"Critique", "Gap Planning", "Refinement", "Guard"}.issubset(set(stack.reflection_roles))
        ):
            add_edge(
                f"loop:{stack.slug}",
                previous_step_id,
                first_step_id,
                edge_label("workflow_reflective_loop", "workflow_update"),
                edge_type="workflow_reflective_loop",
                output_type="workflow_update",
                target_visibility="in_view",
                target_surface="first_hook",
                stack=stack.title,
                property=f"{stack.title} can route guarded findings back to earlier workflow criteria or hooks.",
            )
    return elements


def workflow_drilldown_views(stacks: list[Stack]) -> dict[str, object]:
    """Build one preset, roomy hook-chain graph per workflow stack."""
    drilldowns: dict[str, object] = {}
    for stack in sorted(stacks, key=lambda item: item.source_line):
        elements: list[dict[str, object]] = []
        workflow_id = f"drill:{stack.slug}:workflow"
        elements.append(
            {
                "data": {
                    "id": workflow_id,
                    "label": stack.title,
                    "node_type": "drill_workflow",
                    "family": stack.family,
                    "description": stack.description,
                    "mode": stack.mode,
                    "trigger": stack.trigger,
                    "handoff": stack.handoff,
                    "hooks": len(stack.skills),
                    "roles": ", ".join(stack.reflection_roles),
                },
                "position": {"x": 90, "y": 160},
            }
        )
        previous_step_id = ""
        first_step_id = ""
        row_width = 5
        x_spacing = 250
        y_spacing = 150
        for index, skill in enumerate(stack.skills, start=1):
            col = (index - 1) % row_width
            row = (index - 1) // row_width
            step_id = f"drill:{stack.slug}:step:{index}"
            role = skill_role(skill)
            skill_label = skill_display_label(skill)
            output_type = edge_output_type(skill)
            posture = skill_execution_posture(skill)
            elements.append(
                {
                    "data": {
                        "id": step_id,
                        "label": f"{index}. {skill_label}",
                        "node_type": "drill_step",
                        "stack": stack.title,
                        "family": stack.family,
                        "skill": skill,
                        "skill_label": skill_label,
                        "role": role,
                        "execution_posture": posture,
                        "execution_posture_detail": skill_execution_posture_description(posture),
                        "step_index": index,
                        "output_type": output_type,
                        "description": f"Step {index}: {skill_label} produces {output_display_label(output_type)}.",
                        "detailed_description": skill_detailed_description(skill, stack.title, index),
                    },
                    "position": {"x": 360 + col * x_spacing, "y": 90 + row * y_spacing},
                }
            )
            if index == 1:
                first_step_id = step_id
                elements.append(
                    {
                        "data": {
                            "id": f"drill-entry:{stack.slug}",
                            "source": workflow_id,
                            "target": step_id,
                            "label": edge_label("workflow_entry", output_type),
                            "edge_type": "workflow_entry",
                            "output_type": output_type,
                            "stack": stack.title,
                            "order": index,
                            "property": f"{stack.title} starts with {skill_label}.",
                        }
                    }
                )
            else:
                elements.append(
                    {
                        "data": {
                            "id": f"drill-sequence:{stack.slug}:{index - 1}:{index}",
                            "source": previous_step_id,
                            "target": step_id,
                            "label": edge_label("workflow_sequence", output_type),
                            "edge_type": "workflow_sequence",
                            "output_type": output_type,
                            "stack": stack.title,
                            "order": index,
                            "property": f"Step {index - 1} output feeds step {index} ({skill_label}) in {stack.title}.",
                        }
                    }
                )
            previous_step_id = step_id
        if (
            first_step_id
            and previous_step_id
            and {"Critique", "Gap Planning", "Refinement", "Guard"}.issubset(set(stack.reflection_roles))
        ):
            elements.append(
                {
                    "data": {
                        "id": f"drill-loop:{stack.slug}",
                        "source": previous_step_id,
                        "target": first_step_id,
                        "label": edge_label("workflow_reflective_loop", "workflow_update"),
                        "edge_type": "workflow_reflective_loop",
                        "output_type": "workflow_update",
                        "target_visibility": "in_view",
                        "target_surface": "first_hook",
                        "stack": stack.title,
                        "property": f"{stack.title} can route guarded findings back to earlier workflow criteria or hooks.",
                    }
                }
            )
        drilldowns[stack.slug] = {
            "title": stack.title,
            "family": stack.family,
            "description": stack.description,
            "elements": elements,
        }
    return {
        "default_stack": sorted(stacks, key=lambda item: item.source_line)[0].slug if stacks else "",
        "stacks": drilldowns,
    }


def workflow_click_drilldown_view(stacks: list[Stack], drilldown: dict[str, object]) -> dict[str, object]:
    """Build a click-first workflow index that opens per-stack drilldowns."""
    elements: list[dict[str, object]] = []
    stacks_by_family: dict[str, list[Stack]] = defaultdict(list)
    for stack in stacks:
        stacks_by_family[stack.family].append(stack)

    family_order = sorted(stacks_by_family, key=lambda family: (-len(stacks_by_family[family]), family))
    workflow_index = 0
    columns = 3
    x_spacing = 350
    y_spacing = 140
    for family_index, family in enumerate(family_order):
        family_stacks = sorted(stacks_by_family[family], key=lambda item: item.source_line)
        family_header_id = f"click-family:{slugify(family)}"
        header_row = workflow_index // columns
        header_col = workflow_index % columns
        header_x = 140 + header_col * x_spacing
        header_y = 80 + header_row * y_spacing
        elements.append(
            {
                "data": {
                    "id": family_header_id,
                    "label": family,
                    "node_type": "click_family",
                    "family": family,
                    "description": f"Click a workflow in {family} to inspect its ordered hooks.",
                    "hooks": sum(len(stack.skills) for stack in family_stacks),
                },
                "position": {"x": header_x, "y": header_y},
            }
        )
        workflow_index += 1
        for stack in family_stacks:
            row = workflow_index // columns
            col = workflow_index % columns
            node_id = f"click-workflow:{stack.slug}"
            node_x = 140 + col * x_spacing
            node_y = 80 + row * y_spacing
            elements.append(
                {
                    "data": {
                        "id": node_id,
                        "label": stack.title,
                        "node_type": "click_workflow",
                        "stack_slug": stack.slug,
                        "family": stack.family,
                        "description": stack.description,
                        "mode": stack.mode,
                        "trigger": stack.trigger,
                        "handoff": stack.handoff,
                        "hooks": len(stack.skills),
                        "roles": ", ".join(stack.reflection_roles),
                    },
                    "position": {"x": node_x, "y": node_y},
                }
            )
            elements.append(
                {
                    "data": {
                        "id": f"click-family-link:{slugify(family)}:{stack.slug}",
                        "source": family_header_id,
                        "target": node_id,
                        "label": edge_label("family_contains_workflow", "workflow_group"),
                        "edge_type": "family_contains_workflow",
                        "output_type": "workflow_group",
                        "stack": stack.title,
                        "property": f"{family} contains {stack.title}.",
                    }
                }
            )
            if stack.reflection_roles:
                external_id = f"click-reflects-outside:{stack.slug}"
                elements.append(
                    {
                        "data": {
                            "id": external_id,
                            "label": "Reflective detail outside view",
                            "node_type": "external_reflection",
                            "stack_slug": stack.slug,
                            "stack": stack.title,
                            "family": stack.family,
                            "description": "This marker is not a workflow hook. It marks a reflective relation whose concrete hook or criteria target is outside the current index view; click the workflow to see the in-view loop when available.",
                            "target_visibility": "outside_view",
                            "target_surface": "drill_down_hook_chain",
                            "roles": ", ".join(stack.reflection_roles),
                        },
                        "position": {"x": node_x + 155, "y": node_y + 34},
                    }
                )
                elements.append(
                    {
                        "data": {
                            "id": f"click-reflective-external:{stack.slug}",
                            "source": node_id,
                            "target": external_id,
                            "label": edge_label("reflective_external_reference", "workflow_update"),
                            "edge_type": "reflective_external_reference",
                            "output_type": "workflow_update",
                            "target_visibility": "outside_view",
                            "target_surface": "drill_down_hook_chain",
                            "stack": stack.title,
                            "property": f"{stack.title} has reflective links whose detailed target is outside the click-index view; open the workflow to inspect the concrete loop.",
                        }
                    }
                )
            workflow_index += 1

    return {
        "title": "Click Drill Down",
        "description": "Click a workflow node to open its ordered hook chain. Use Back To Workflow Index to return to the full workflow chooser.",
        "index_elements": elements,
        "stacks": drilldown.get("stacks", {}),
        "default_stack": drilldown.get("default_stack", ""),
    }


def escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def truncate(value: str, limit: int = 84) -> str:
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "..."


def workflow_description(title: str, mode: str, trigger: str, handoff: str) -> str:
    def fragment(value: str) -> str:
        value = value.strip().rstrip(".")
        if not value:
            return ""
        return value[0].lower() + value[1:] if value[0].isupper() else value

    sentences = []
    if trigger:
        sentences.append(f"Use this workflow when {fragment(trigger)}.")
    elif mode:
        sentences.append(f"This workflow runs in {fragment(mode)} mode.")
    else:
        sentences.append(f"{title} coordinates a specialized workflow stack.")
    if handoff:
        sentences.append(f"It leaves {fragment(handoff)}.")
    return " ".join(sentences)


def skill_role(skill: str) -> str:
    lower = skill.lower()
    explicit_roles = {
        "debug-root-cause-repair-conceptualizer": "modeler",
        "debug-repair-proposal-designer": "planner",
    }
    if lower in explicit_roles:
        return explicit_roles[lower]
    rules = [
        ("critic", ("critic", "review", "audit", "diagnos", "signoff")),
        ("planner", ("planner", "plan", "todo", "forecast", "selector")),
        ("refiner", ("refiner", "refinement", "improvement", "repair")),
        ("guard", ("guard", "gate", "closure")),
        ("extractor", ("extractor", "reader", "intake", "miner", "cartographer")),
        ("generator", ("generator", "writer", "assembler", "reporter", "designer")),
        ("executor", ("runner", "execution", "emulator", "runtime")),
        ("modeler", ("modeler", "reasoner", "abducer", "mapper", "optimizer")),
    ]
    for role, needles in rules:
        if any(needle in lower for needle in needles):
            return role
    return "workflow-skill"


def skill_execution_posture(skill: str) -> str:
    lower = skill.lower()
    deterministic_needles = (
        "syntax",
        "grammar",
        "runner",
        "execution",
        "emulator",
        "validation",
        "validator",
        "coverage",
        "compile",
        "lint",
        "extractor",
        "reader",
        "intake",
        "gate",
        "guard",
    )
    generative_needles = (
        "critic",
        "review",
        "reasoner",
        "planner",
        "designer",
        "writer",
        "explainer",
        "abduct",
        "interpret",
        "forecast",
        "elicitor",
        "orchestrator",
        "synthesizer",
        "refiner",
        "modeler",
        "mapper",
    )
    has_deterministic = any(needle in lower for needle in deterministic_needles)
    has_generative = any(needle in lower for needle in generative_needles)
    if has_deterministic and has_generative:
        return "both"
    if has_deterministic:
        return "deterministic"
    if has_generative:
        return "generative"
    return "both"


def skill_role_description(role: str) -> str:
    return {
        "critic": "It checks an artifact, claim, or workflow decision for defects, overreach, or missing evidence.",
        "planner": "It turns findings or intent into ordered actions, TODOs, routing choices, or implementation slices.",
        "refiner": "It revisits prior outputs and tightens wording, criteria, prompts, or workflow structure under bounded iteration.",
        "guard": "It protects existing behavior and decides whether a proposed change is monotonic, scoped, and safe to apply.",
        "extractor": "It converts source material into structured evidence, facts, or inventory items for downstream reasoning.",
        "generator": "It produces a concrete artifact such as a report, plan, graph, scenario, checker, or explanation.",
        "executor": "It runs or routes executable evidence and records the resulting pass, fail, skip, or limitation posture.",
        "modeler": "It builds an intermediate semantic model so later hooks can reason over structure instead of raw text alone.",
        "workflow-skill": "It coordinates workflow context or carries a specialized project control responsibility.",
    }[role]


def skill_execution_posture_description(posture: str) -> str:
    return {
        "deterministic": "primarily rule, parser, graph, syntax, execution, or validation driven",
        "generative": "primarily judgment, interpretation, critique, design, or narrative generation driven",
        "both": "combines structured checks with interpretive or generative judgment",
    }[posture]


def indefinite_article(value: str) -> str:
    return "an" if value[:1].lower() in {"a", "e", "i", "o", "u"} else "a"


def skill_detailed_description(skill: str, stack_title: str = "", step_index: int | None = None) -> str:
    role = skill_role(skill)
    posture = skill_execution_posture(skill)
    output_type = edge_output_type(skill)
    label = skill_display_label(skill)
    role_label = display_label(role)
    location = f"Step {step_index} in {stack_title}. " if stack_title and step_index is not None else ""
    return (
        f"{location}{label} is {indefinite_article(role_label)} {role_label} hook that produces {output_display_label(output_type)}. "
        f"Execution posture: {display_label(posture)}; {skill_execution_posture_description(posture)}. "
        f"{skill_role_description(role)}"
    )


def edge_output_type(skill: str) -> str:
    explicit_outputs = {
        "debug-root-cause-repair-conceptualizer": "repair_concept",
        "debug-repair-proposal-designer": "repair_proposal",
    }
    if skill.lower() in explicit_outputs:
        return explicit_outputs[skill.lower()]
    role = skill_role(skill)
    return {
        "critic": "finding",
        "planner": "plan_or_todo",
        "refiner": "refinement",
        "guard": "gate_decision",
        "extractor": "evidence_packet",
        "generator": "generated_artifact",
        "executor": "execution_evidence",
        "modeler": "semantic_model",
        "workflow-skill": "workflow_context",
    }[role]


def family_color(index: int) -> str:
    colors = [
        "#0f766e",
        "#2563eb",
        "#7c3aed",
        "#be123c",
        "#ca8a04",
        "#0e7490",
        "#c2410c",
        "#4d7c0f",
        "#9333ea",
        "#334155",
    ]
    return colors[index % len(colors)]


def overview_svg(stacks: list[Stack]) -> str:
    families: dict[str, list[Stack]] = defaultdict(list)
    for stack in stacks:
        families[stack.family].append(stack)
    ordered = sorted(families.items(), key=lambda item: (-len(item[1]), item[0]))
    width = 1120
    col_width = 350
    row_height = 118
    columns = 3
    rows = (len(ordered) + columns - 1) // columns
    height = 80 + rows * row_height
    parts = [
        f"<svg viewBox='0 0 {width} {height}' role='img' aria-label='Workflow families overview'>",
        f"<rect width='{width}' height='{height}' rx='20' fill='#ffffff'/>",
        "<text x='36' y='38' class='chart-title'>Workflow families</text>",
    ]
    for index, (family, family_stacks) in enumerate(ordered):
        col = index % columns
        row = index // columns
        x = 34 + col * col_width
        y = 68 + row * row_height
        color = family_color(index)
        hook_count = sum(len(stack.skills) for stack in family_stacks)
        reflective_count = sum(1 for stack in family_stacks if stack.reflection_roles)
        parts.append(f"<rect x='{x}' y='{y}' width='316' height='92' rx='14' fill='#f8fafc' stroke='#dbe4ef'/>")
        parts.append(f"<rect x='{x}' y='{y}' width='8' height='92' rx='4' fill='{color}'/>")
        parts.append(f"<text x='{x + 22}' y='{y + 28}' class='family-label'>{escape(family)}</text>")
        parts.append(f"<text x='{x + 22}' y='{y + 54}' class='small-label'>{len(family_stacks)} stacks, {hook_count} hooks</text>")
        parts.append(f"<text x='{x + 22}' y='{y + 76}' class='small-label'>{reflective_count} reflective stacks</text>")
    parts.append("</svg>")
    return "\n".join(parts)


def shared_skill_svg(shared: list[dict[str, object]]) -> str:
    rows = shared[:12]
    width = 1120
    bar_height = 28
    gap = 13
    height = 80 + len(rows) * (bar_height + gap)
    max_count = max([int(row["count"]) for row in rows], default=1)
    parts = [
        f"<svg viewBox='0 0 {width} {height}' role='img' aria-label='Shared skills across workflow stacks'>",
        f"<rect width='{width}' height='{height}' rx='20' fill='#ffffff'/>",
        "<text x='36' y='38' class='chart-title'>Shared skills connecting stacks</text>",
    ]
    for index, item in enumerate(rows):
        y = 64 + index * (bar_height + gap)
        width_px = 42 + (int(item["count"]) / max_count) * 620
        parts.append(f"<text x='36' y='{y + 20}' class='bar-label'>{escape(skill_display_label(str(item['skill'])))}</text>")
        parts.append(f"<rect x='330' y='{y}' width='{width_px:.1f}' height='{bar_height}' rx='8' fill='{family_color(index)}'/>")
        parts.append(f"<text x='{350 + width_px:.1f}' y='{y + 20}' class='bar-count'>{item['count']} stacks</text>")
    parts.append("</svg>")
    return "\n".join(parts)


def reflective_loop_svg(stacks: list[Stack]) -> str:
    role_order = ["Critique", "Gap Planning", "Refinement", "Guard", "Second Order"]
    counts = role_counts(stacks)
    width, height = 1120, 280
    centers = [(128, 138), (350, 138), (572, 138), (794, 138), (1000, 138)]
    parts = [
        f"<svg viewBox='0 0 {width} {height}' role='img' aria-label='Reflective workflow loop roles'>",
        f"<rect width='{width}' height='{height}' rx='20' fill='#ffffff'/>",
        "<text x='36' y='38' class='chart-title'>Reflective loop map</text>",
        "<defs><marker id='arrow' markerWidth='10' markerHeight='10' refX='8' refY='3' orient='auto'><path d='M0,0 L0,6 L9,3 z' fill='#94a3b8'/></marker></defs>",
    ]
    for index in range(len(centers) - 1):
        x1, y1 = centers[index]
        x2, y2 = centers[index + 1]
        parts.append(f"<path d='M{x1 + 78},{y1} C{x1 + 120},{y1 - 45} {x2 - 120},{y2 - 45} {x2 - 78},{y2}' fill='none' stroke='#94a3b8' stroke-width='3' marker-end='url(#arrow)'/>")
    parts.append("<path d='M1000,202 C820,260 320,260 128,202' fill='none' stroke='#94a3b8' stroke-width='3' stroke-dasharray='8 8' marker-end='url(#arrow)'/>")
    for index, role in enumerate(role_order):
        x, y = centers[index]
        count = counts.get(role, 0)
        parts.append(f"<circle cx='{x}' cy='{y}' r='72' fill='#f8fafc' stroke='{family_color(index)}' stroke-width='4'/>")
        parts.append(f"<text x='{x}' y='{y - 8}' text-anchor='middle' class='loop-label'>{escape(role)}</text>")
        parts.append(f"<text x='{x}' y='{y + 22}' text-anchor='middle' class='loop-count'>{count} stacks</text>")
    parts.append("<text x='450' y='246' class='small-label'>Dashed return: findings update workflow criteria, hooks, or skill definitions.</text>")
    parts.append("</svg>")
    return "\n".join(parts)


def stack_details_html(stacks: list[Stack]) -> str:
    parts = []
    for stack in stacks:
        chips = "".join(f"<span class='chip'>{escape(skill_display_label(skill))}</span>" for skill in stack.skills)
        roles = "".join(f"<span class='role-chip'>{escape(role)}</span>" for role in stack.reflection_roles)
        guardrails = "".join(f"<li>{escape(item)}</li>" for item in stack.guardrails)
        parts.append(
            f"""
            <details class="stack-card">
              <summary>
                <span>{escape(stack.title)}</span>
                <em>{escape(stack.family)} · {len(stack.skills)} hooks</em>
              </summary>
              <div class="stack-meta">
                <p><strong>Description:</strong> {escape(stack.description)}</p>
                <p><strong>Mode:</strong> {escape(stack.mode)}</p>
                <p><strong>Trigger:</strong> {escape(truncate(stack.trigger, 240))}</p>
                <p><strong>Artifacts:</strong> {escape(truncate(stack.artifact_entrypoints, 240))}</p>
                <p><strong>Handoff:</strong> {escape(truncate(stack.handoff, 240))}</p>
              </div>
              <div class="chip-row">{chips or "<span class='empty'>No explicit hooks extracted.</span>"}</div>
              <div class="role-row">{roles}</div>
              {f"<ul class='guardrails'>{guardrails}</ul>" if guardrails else ""}
            </details>
            """
        )
    return "\n".join(parts)


def interactive_graph_section(model: dict[str, object]) -> str:
    graph = model["graph"]
    graph_json = json.dumps(graph["views"]).replace("</", "<\\/")
    edge_taxonomy = graph["edge_label_taxonomy"]
    semantics_html = "".join(
        f"<li><strong>{escape(edge_label(edge_type, str(spec['default_output'])))}:</strong> "
        f"<code>{escape(edge_type)}</code> · {escape(spec['description'])}</li>"
        for edge_type, spec in edge_taxonomy.items()
    )
    return f"""
  <section>
    <h2>Interactive Skill Graph</h2>
    <div class="panel">
      <p><strong>Recommended dynamic library:</strong> Cytoscape.js.</p>
      <p>{escape(graph["library_reason"])}</p>
      <ul>{semantics_html}</ul>
    </div>
    <div class="graph-controls" role="group" aria-label="Graph view selector">
      <button type="button" data-view="workflow_hierarchy" class="active">Workflow Sequence And Hierarchy</button>
      <button type="button" data-view="workflow_drilldown">Workflow Drill Down</button>
      <button type="button" data-view="node_click_drilldown">Click Drill Down</button>
      <button type="button" data-view="cross_stack_interactions">Cross-Stack Skill Interactions</button>
    </div>
    <div class="drill-selector" id="drill-selector" hidden>
      <label for="drill-stack-select">Workflow stack</label>
      <select id="drill-stack-select"></select>
    </div>
    <div class="click-drill-toolbar" id="click-drill-toolbar" hidden>
      <button type="button" id="click-drill-back">Back To Workflow Index</button>
      <span id="click-drill-status">Click a workflow node to drill down.</span>
    </div>
    <div class="interactive-layout">
      <div id="cy" aria-label="Interactive workflow skill graph"></div>
      <aside id="graph-inspector">
        <h3>Hover Or Select</h3>
        <p>Move over a family, workflow, ordered step, skill, or edge to inspect hierarchy, sequence, output type, and workflow property.</p>
      </aside>
    </div>
    <p class="fallback-note" id="graph-fallback">Static views below remain authoritative if the dynamic graph library is unavailable.</p>
  </section>
  <script id="workflow-graph-data" type="application/json">{graph_json}</script>
  <script>
    (function () {{
      var dataEl = document.getElementById('workflow-graph-data');
      var cyEl = document.getElementById('cy');
      var inspector = document.getElementById('graph-inspector');
      var controls = Array.prototype.slice.call(document.querySelectorAll('[data-view]'));
      var drillSelector = document.getElementById('drill-selector');
      var drillStackSelect = document.getElementById('drill-stack-select');
      var clickDrillToolbar = document.getElementById('click-drill-toolbar');
      var clickDrillBack = document.getElementById('click-drill-back');
      var clickDrillStatus = document.getElementById('click-drill-status');
      if (!window.cytoscape || !dataEl || !cyEl) {{
        document.getElementById('graph-fallback').textContent = 'Cytoscape.js did not load; use the static views and JSON model below.';
        return;
      }}
      var graphViews = JSON.parse(dataEl.textContent);
      var cy = null;
      var baseStyle = [
          {{ selector: 'node', style: {{
            'label': '', 'font-size': 10, 'text-wrap': 'wrap', 'text-max-width': 92,
            'background-color': '#0f766e', 'color': '#172033', 'text-valign': 'bottom', 'text-margin-y': 6,
            'width': 22, 'height': 22, 'border-width': 2, 'border-color': '#ffffff'
          }} }},
          {{ selector: 'node[node_type = "family"]', style: {{
            'label': 'data(label)', 'shape': 'round-rectangle', 'background-color': '#eef6ff',
            'border-color': '#bfdbfe', 'border-width': 2, 'font-weight': 800,
            'font-size': 12, 'text-max-width': 130, 'padding': 16
          }} }},
          {{ selector: 'node[node_type = "workflow"]', style: {{
            'label': 'data(label)', 'shape': 'round-rectangle', 'background-color': '#dbeafe',
            'border-color': '#2563eb', 'font-weight': 750, 'text-max-width': 120,
            'width': 58, 'height': 32, 'padding': 10
          }} }},
          {{ selector: 'node[node_type = "workflow_step"]', style: {{
            'shape': 'ellipse', 'background-color': '#0f766e', 'width': 20, 'height': 20
          }} }},
          {{ selector: 'node[node_type = "drill_workflow"]', style: {{
            'label': 'data(label)', 'shape': 'round-rectangle', 'background-color': '#dbeafe',
            'border-color': '#2563eb', 'font-weight': 850, 'font-size': 13,
            'text-max-width': 160, 'width': 86, 'height': 44, 'padding': 12
          }} }},
          {{ selector: 'node[node_type = "drill_step"]', style: {{
            'label': 'data(label)', 'shape': 'round-rectangle', 'background-color': '#f8fafc',
            'border-color': '#0f766e', 'color': '#172033', 'font-weight': 800,
            'text-max-width': 160, 'width': 120, 'height': 42, 'padding': 12
          }} }},
          {{ selector: 'node[node_type = "click_family"]', style: {{
            'label': 'data(label)', 'shape': 'round-rectangle', 'background-color': '#eef6ff',
            'border-color': '#bfdbfe', 'color': '#172033', 'font-weight': 850,
            'font-size': 12, 'text-max-width': 150, 'width': 112, 'height': 34, 'padding': 10
          }} }},
          {{ selector: 'node[node_type = "click_workflow"]', style: {{
            'label': 'data(label)', 'shape': 'round-rectangle', 'background-color': '#dbeafe',
            'border-color': '#2563eb', 'color': '#172033', 'font-weight': 800,
            'font-size': 11, 'text-max-width': 150, 'width': 122, 'height': 44, 'padding': 10
          }} }},
          {{ selector: 'node[node_type = "external_reflection"]', style: {{
            'label': 'data(label)', 'shape': 'diamond', 'background-color': '#fff7ed',
            'border-color': '#f97316', 'border-style': 'dashed', 'color': '#9a3412',
            'font-weight': 800, 'font-size': 9, 'text-max-width': 95, 'width': 28, 'height': 28
          }} }},
          {{ selector: 'node[node_type = "stack"]', style: {{
            'label': 'data(label)', 'shape': 'round-rectangle', 'width': 48, 'height': 30, 'background-color': '#2563eb',
            'font-weight': 700, 'text-max-width': 110
          }} }},
          {{ selector: 'node[role = "critic"]', style: {{ 'background-color': '#be123c' }} }},
          {{ selector: 'node[role = "planner"]', style: {{ 'background-color': '#ca8a04' }} }},
          {{ selector: 'node[role = "guard"]', style: {{ 'background-color': '#7c3aed' }} }},
          {{ selector: 'node[role = "generator"]', style: {{ 'background-color': '#0e7490' }} }},
          {{ selector: 'edge', style: {{
            'curve-style': 'bezier', 'target-arrow-shape': 'triangle', 'target-arrow-color': '#94a3b8',
            'line-color': '#94a3b8', 'width': 1.25, 'opacity': 0.42, 'label': '',
            'font-size': 8, 'text-background-color': '#ffffff', 'text-background-opacity': 0.85
          }} }},
          {{ selector: 'edge[edge_type = "skill_handoff"]', style: {{ 'line-style': 'dashed', 'line-color': '#0e7490', 'target-arrow-color': '#0e7490' }} }},
          {{ selector: 'edge[edge_type = "workflow_sequence"]', style: {{ 'line-color': '#0f766e', 'target-arrow-color': '#0f766e', 'width': 1.8 }} }},
          {{ selector: 'edge[edge_type = "workflow_entry"]', style: {{ 'line-color': '#2563eb', 'target-arrow-color': '#2563eb', 'width': 1.7 }} }},
          {{ selector: 'edge[edge_type = "family_contains_workflow"]', style: {{ 'line-color': '#cbd5e1', 'target-arrow-color': '#cbd5e1', 'line-style': 'dotted', 'opacity': 0.2 }} }},
          {{ selector: 'edge[edge_type = "reflective_feedback"]', style: {{ 'line-style': 'dotted', 'line-color': '#f97316', 'target-arrow-color': '#f97316', 'width': 2.5 }} }},
          {{ selector: 'edge[edge_type = "workflow_reflective_loop"]', style: {{ 'line-style': 'dotted', 'line-color': '#f97316', 'target-arrow-color': '#f97316', 'width': 2.5 }} }},
          {{ selector: 'edge[edge_type = "reflective_external_reference"]', style: {{ 'line-style': 'dashed', 'line-color': '#f97316', 'target-arrow-color': '#f97316', 'width': 2.1, 'opacity': 0.7 }} }},
          {{ selector: '.highlighted', style: {{ 'label': 'data(label)', 'opacity': 1, 'border-color': '#f97316', 'line-color': '#f97316', 'target-arrow-color': '#f97316', 'z-index': 999 }} }},
          {{ selector: '.dimmed', style: {{ 'opacity': 0.12 }} }}
        ];
      function springRestLength(edge) {{
        var edgeType = edge.data('edge_type') || '';
        if (edgeType === 'stack_uses_skill') {{ return 330; }}
        if (edgeType === 'skill_handoff') {{ return 230; }}
        if (edgeType === 'reflective_feedback') {{ return 380; }}
        return 270;
      }}
      function springElasticity(edge) {{
        var edgeType = edge.data('edge_type') || '';
        if (edgeType === 'stack_uses_skill') {{ return 56; }}
        if (edgeType === 'skill_handoff') {{ return 82; }}
        if (edgeType === 'reflective_feedback') {{ return 38; }}
        return 68;
      }}
      var layouts = {{
        workflow_hierarchy: {{ name: 'preset', fit: false, padding: 35 }},
        workflow_drilldown: {{ name: 'preset', fit: true, padding: 80 }},
        node_click_drilldown: {{ name: 'preset', fit: true, padding: 80 }},
        cross_stack_interactions: {{
          name: 'cose',
          animate: false,
          randomize: true,
          fit: true,
          padding: 95,
          idealEdgeLength: springRestLength,
          nodeRepulsion: 26000,
          nodeOverlap: 62,
          edgeElasticity: springElasticity,
          nestingFactor: 1.25,
          gravity: 0.12,
          numIter: 2200,
          initialTemp: 320,
          coolingFactor: 0.96,
          minTemp: 1.0
        }}
      }};
      var activeViewName = 'workflow_hierarchy';
      var activeDrillStack = graphViews.workflow_drilldown ? graphViews.workflow_drilldown.default_stack : '';
      var activeClickDrillStack = '';
      function configureDrillSelector() {{
        if (!drillStackSelect || !graphViews.workflow_drilldown) {{ return; }}
        var stacks = graphViews.workflow_drilldown.stacks || {{}};
        drillStackSelect.innerHTML = Object.keys(stacks).map(function (key) {{
          var item = stacks[key];
          return '<option value="' + key + '">' + item.title + '</option>';
        }}).join('');
        drillStackSelect.value = activeDrillStack;
      }}
      function inspect(ele) {{
        var d = ele.data();
        if (ele.isEdge()) {{
          inspector.innerHTML = '<h3>' + d.label + ' edge</h3>' +
            '<p><strong>Type:</strong> ' + (d.edge_type || '') + '</p>' +
            '<p><strong>Output:</strong> ' + (d.output_type || '') + '</p>' +
            '<p><strong>Order:</strong> ' + (d.order || '') + '</p>' +
            (d.target_visibility ? '<p><strong>Target visibility:</strong> ' + d.target_visibility + '</p>' : '') +
            (d.target_surface ? '<p><strong>Target surface:</strong> ' + d.target_surface + '</p>' : '') +
            '<p><strong>Stack:</strong> ' + (d.stack || '') + '</p>' +
            '<p>' + (d.property || '') + '</p>';
        }} else {{
          inspector.innerHTML = '<h3>' + d.label + '</h3>' +
            '<p><strong>Type:</strong> ' + (d.node_type || '') + '</p>' +
            '<p><strong>Family/role:</strong> ' + (d.family || d.role || '') + '</p>' +
            (d.stack ? '<p><strong>Workflow:</strong> ' + d.stack + '</p>' : '') +
            (d.skill ? '<p><strong>Skill:</strong> ' + (d.skill_label || d.label || d.skill) + '</p>' : '') +
            (d.execution_posture ? '<p><strong>Execution posture:</strong> ' + d.execution_posture + '</p>' : '') +
            (d.step_index ? '<p><strong>Step:</strong> ' + d.step_index + '</p>' : '') +
            (d.output_type ? '<p><strong>Output:</strong> ' + d.output_type + '</p>' : '') +
            (d.target_visibility ? '<p><strong>Target visibility:</strong> ' + d.target_visibility + '</p>' : '') +
            (d.target_surface ? '<p><strong>Target surface:</strong> ' + d.target_surface + '</p>' : '') +
            '<p>' + (d.detailed_description || d.description || '') + '</p>' +
            (d.trigger ? '<p><strong>Trigger:</strong> ' + d.trigger + '</p>' : '') +
            (d.handoff ? '<p><strong>Handoff:</strong> ' + d.handoff + '</p>' : '');
        }}
      }}
      function focusNeighborhood(ele) {{
        cy.elements().addClass('dimmed');
        ele.closedNeighborhood().removeClass('dimmed').addClass('highlighted');
      }}
      function renderGraph(viewName) {{
        activeViewName = viewName;
        var view = graphViews[viewName] || graphViews.workflow_hierarchy;
        var elements = view.elements;
        if (viewName === 'workflow_drilldown') {{
          if (drillSelector) {{ drillSelector.hidden = false; }}
          var stacks = view.stacks || {{}};
          activeDrillStack = activeDrillStack && stacks[activeDrillStack] ? activeDrillStack : view.default_stack;
          if (drillStackSelect) {{ drillStackSelect.value = activeDrillStack; }}
          var selectedStack = stacks[activeDrillStack] || {{ title: view.title, description: view.description, elements: [] }};
          elements = selectedStack.elements;
          view = {{
            title: selectedStack.title,
            description: selectedStack.description || view.description
          }};
          if (clickDrillToolbar) {{ clickDrillToolbar.hidden = true; }}
        }} else if (viewName === 'node_click_drilldown') {{
          if (drillSelector) {{ drillSelector.hidden = true; }}
          if (clickDrillToolbar) {{ clickDrillToolbar.hidden = false; }}
          var clickStacks = view.stacks || {{}};
          if (activeClickDrillStack && clickStacks[activeClickDrillStack]) {{
            var clickStack = clickStacks[activeClickDrillStack];
            elements = clickStack.elements;
            view = {{ title: clickStack.title, description: clickStack.description || view.description }};
            if (clickDrillStatus) {{ clickDrillStatus.textContent = 'Drilling into ' + clickStack.title + '.'; }}
          }} else {{
            elements = view.index_elements || [];
            if (clickDrillStatus) {{ clickDrillStatus.textContent = 'Click a workflow node to drill down.'; }}
          }}
        }} else if (drillSelector) {{
          drillSelector.hidden = true;
          if (clickDrillToolbar) {{ clickDrillToolbar.hidden = true; }}
        }}
        if (cy) {{ cy.destroy(); }}
        cy = cytoscape({{
          container: cyEl,
          elements: elements,
          layout: layouts[viewName] || layouts.workflow_hierarchy,
          style: baseStyle,
          minZoom: 0.18,
          maxZoom: 2.5
        }});
        inspector.innerHTML = '<h3>' + view.title + '</h3><p>' + view.description + '</p>';
        cy.on('mouseover tap', 'node, edge', function (evt) {{
          var ele = evt.target;
          inspect(ele);
          focusNeighborhood(ele);
        }});
        cy.on('tap', 'node[node_type = "click_workflow"]', function (evt) {{
          activeClickDrillStack = evt.target.data('stack_slug');
          renderGraph('node_click_drilldown');
        }});
        cy.on('mouseout', 'node, edge', function () {{
          cy.elements().removeClass('dimmed highlighted');
        }});
        cy.ready(function () {{
          if (viewName === 'workflow_hierarchy') {{
            cy.zoom(0.72);
            cy.pan({{ x: 70, y: 70 }});
          }} else if (viewName === 'workflow_drilldown' || viewName === 'node_click_drilldown') {{
            cy.fit(undefined, 80);
          }} else {{
            cy.fit(undefined, 95);
          }}
        }});
      }}
      controls.forEach(function (button) {{
        button.addEventListener('click', function () {{
          controls.forEach(function (item) {{ item.classList.remove('active'); }});
          button.classList.add('active');
          renderGraph(button.getAttribute('data-view'));
        }});
      }});
      if (drillStackSelect) {{
        drillStackSelect.addEventListener('change', function () {{
          activeDrillStack = drillStackSelect.value;
          renderGraph('workflow_drilldown');
        }});
      }}
      if (clickDrillBack) {{
        clickDrillBack.addEventListener('click', function () {{
          activeClickDrillStack = '';
          renderGraph('node_click_drilldown');
        }});
      }}
      configureDrillSelector();
      renderGraph('workflow_hierarchy');
    }})();
  </script>
"""


def build_topology_conceptual_core(
    stacks: list[Stack],
    shared: list[dict[str, object]],
    reflective: list[Stack],
) -> dict[str, object]:
    """Explain declared topology without implying that any workflow executed."""
    families = sorted({stack.family for stack in stacks})
    shared_hooks = [
        {
            "skill": str(item["skill"]),
            "workflows": list(item["stacks"]),
            "fanout": int(item["count"]),
        }
        for item in shared[:5]
    ]
    feedback_loops = [
        {
            "workflow": stack.title,
            "roles": list(stack.reflection_roles),
            "return_semantics": (
                "Critique, refinement, or guard findings may return to earlier workflow "
                "criteria or hooks; the return is not another forward sequence step."
            ),
        }
        for stack in reflective[:5]
    ]
    if stacks:
        thesis = (
            f"The declared architecture groups {len(stacks)} workflows into "
            f"{len(families)} families. Forward edges carry typed handoffs through each "
            "ordered stack, while shared hooks couple workflows and dashed returns preserve "
            "review or refinement loops."
        )
    else:
        thesis = "No declared workflow stacks were extracted, so no topology can be explained."
    return {
        "core_id": "workflow-architecture-conceptual-core",
        "report_family_id": "architecture",
        "report_kind": "architecture",
        "core_disposition": "full",
        "status": "complete" if stacks else "unavailable",
        "subject": "Declared workflow topology",
        "reasoning_mode": "topological",
        "focal_question": (
            "How do ordered workflow handoffs, shared hooks, and guarded feedback loops "
            "shape the architecture?"
        ),
        "supported_decision": "Where should an operator enter, follow, or revisit the declared workflow topology?",
        "topology_thesis": thesis,
        "legend": [
            {
                "kind": "forward_sequence",
                "label": "Forward handoff",
                "meaning": "One hook materializes the typed input consumed by the next hook.",
            },
            {
                "kind": "shared_hook",
                "label": "Shared hook",
                "meaning": "The same skill participates in more than one workflow stack.",
            },
            {
                "kind": "feedback_loop",
                "label": "Guarded return",
                "meaning": "A critic, refiner, or guard can return findings to an earlier decision surface.",
            },
        ],
        "shared_hooks": shared_hooks,
        "feedback_loops": feedback_loops,
        "complexity": (
            "Architecture complexity concentrates where a shared hook has high fanout or a "
            "feedback edge crosses an otherwise ordered stack."
        ),
        "reading_strategy": (
            "Start with one family and follow its ordered handoffs. Then inspect shared hooks "
            "for cross-stack coupling and feedback returns for iteration or closure behavior."
        ),
        "evidence_boundary": (
            "This model is extracted from coordination contracts. It describes declared "
            "architecture, not current execution, hook activation, success, or runtime cost."
        ),
        "excluded_ledger_detail": [
            "complete node and edge model",
            "expanded stack lane inventory",
            "interactive layout configuration",
        ],
        "maximum_narrative_words": 320,
        "visual_pattern_policy": "report_owned_no_shared_visual_pattern",
    }


def build_model(repo: Path, contract_path: Path) -> dict[str, object]:
    stacks = parse_stacks(contract_path)
    supplemental_sources: list[str] = []
    project_index = repo / "proj_skills" / "INDEX.md"
    if project_index.is_file() and project_index.resolve() != contract_path.resolve():
        stacks.extend(parse_project_support_stacks(project_index))
        supplemental_sources.append(str(project_index))
    skill_counter: Counter[str] = Counter()
    for stack in stacks:
        skill_counter.update(stack.skills)
    shared = shared_skills(stacks)
    families = Counter(stack.family for stack in stacks)
    reflective = [stack for stack in stacks if stack.reflection_roles]
    interaction_elements = graph_elements(stacks)
    workflow_elements = workflow_graph_elements(stacks)
    drilldown = workflow_drilldown_views(stacks)
    click_drilldown = workflow_click_drilldown_view(stacks, drilldown)
    conceptual_core = build_topology_conceptual_core(stacks, shared, reflective)
    return {
        "repo": str(repo),
        "source_document": str(contract_path),
        "supplemental_source_documents": supplemental_sources,
        "conceptual_core": conceptual_core,
        "summary": {
            "stacks": len(stacks),
            "total_hooks": sum(len(stack.skills) for stack in stacks),
            "unique_skills": len(skill_counter),
            "shared_skills": len(shared),
            "reflective_stacks": len(reflective),
            "families": len(families),
        },
        "families": dict(families),
        "shared_skills": shared,
        "reflection_role_counts": dict(role_counts(stacks)),
        "graph": {
            "library_recommendation": "Cytoscape.js",
            "library_reason": "Best fit for this repo because workflow interactions are graph-theoretic, semantically typed, moderately sized, and need node/edge hover/click inspection, compound hierarchy, and multiple graph views rather than only large-scale WebGL rendering.",
            "layout_strategy": {
                "workflow_hierarchy": "Preset hierarchy layout: families contain workflows, workflows contain ordered hook steps.",
                "workflow_drilldown": "Preset per-stack drill-down layout: one workflow at a time with large ordered hook nodes and explicit sequence or feedback edges.",
                "node_click_drilldown": "Click-first drill-down layout: start from a workflow index and open one stack's ordered hooks by clicking its workflow node.",
                "cross_stack_interactions": "Force-directed Cytoscape cose layout with typed spring rest lengths and elasticities, stronger node repulsion, overlap avoidance, and lower gravity to preserve the previous organic style while reducing clumping.",
                "force_layout_parameters": {
                    "springRestLength": {
                        "stack_uses_skill": 330,
                        "skill_handoff": 230,
                        "reflective_feedback": 380,
                        "default": 270,
                    },
                    "springElasticity": {
                        "stack_uses_skill": 56,
                        "skill_handoff": 82,
                        "reflective_feedback": 38,
                        "default": 68,
                    },
                    "nodeRepulsion": 26000,
                    "nodeOverlap": 62,
                    "gravity": 0.12,
                    "numIter": 2200,
                    "padding": 95,
                },
            },
            "edge_semantics": {
                "family_contains_workflow": "A workflow family contains a workflow stack.",
                "workflow_entry": "A workflow starts at its first hook.",
                "workflow_sequence": "One ordered hook step feeds the next hook step in the same workflow.",
                "workflow_reflective_loop": "A guarded review/refinement path can send findings back to earlier criteria or hooks.",
                "stack_uses_skill": "A workflow stack invokes a skill hook.",
                "skill_handoff": "One ordered hook hands its output to the next hook in the same stack.",
                "reflective_feedback": "A review/refinement/guard loop can feed findings back into the workflow definition.",
                "reflective_external_reference": "A dashed boundary edge marks a reflective relation whose concrete target is outside the active view.",
            },
            "edge_label_taxonomy": EDGE_LABEL_TAXONOMY,
            "views": {
                "workflow_hierarchy": {
                    "title": "Workflow Sequence And Hierarchy",
                    "description": "Shows family -> workflow -> ordered hook steps, with explicit entry, next-step, and reflective-loop edges.",
                    "elements": workflow_elements,
                },
                "workflow_drilldown": {
                    "title": "Workflow Drill Down",
                    "description": "Select one workflow stack and inspect its ordered hooks, handoff edges, output types, and reflective-loop edges with more room.",
                    **drilldown,
                },
                "node_click_drilldown": click_drilldown,
                "cross_stack_interactions": {
                    "title": "Cross-Stack Skill Interactions",
                    "description": "Shows shared skill nodes and cross-stack interaction edges for reuse and hook coupling analysis.",
                    "elements": interaction_elements,
                },
            },
            "elements": interaction_elements,
        },
        "stacks": [
            {
                "title": stack.title,
                "slug": stack.slug,
                "mode": stack.mode,
                "trigger": stack.trigger,
                "artifact_entrypoints": stack.artifact_entrypoints,
                "handoff": stack.handoff,
                "description": stack.description,
                "skills": stack.skills,
                "guardrails": stack.guardrails,
                "source_line": stack.source_line,
                "family": stack.family,
                "reflection_roles": stack.reflection_roles,
            }
            for stack in stacks
        ],
    }


def render_html(repo: Path, model: dict[str, object]) -> str:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    stacks = [
        Stack(
            title=item["title"],
            slug=item["slug"],
            mode=item["mode"],
            trigger=item["trigger"],
            artifact_entrypoints=item["artifact_entrypoints"],
            handoff=item["handoff"],
            description=item["description"],
            skills=list(item["skills"]),
            guardrails=list(item["guardrails"]),
            source_line=int(item["source_line"]),
            family=item["family"],
            reflection_roles=list(item["reflection_roles"]),
        )
        for item in model["stacks"]
    ]
    summary = model["summary"]
    conceptual_core = model["conceptual_core"]
    stat_cards = "\n".join(
        f"<div class='stat'><span>{escape(label)}</span><strong>{value}</strong></div>"
        for label, value in [
            ("Workflow stacks", summary["stacks"]),
            ("Total hooks", summary["total_hooks"]),
            ("Unique skills", summary["unique_skills"]),
            ("Shared skills", summary["shared_skills"]),
            ("Reflective stacks", summary["reflective_stacks"]),
            ("Families", summary["families"]),
        ]
    )
    design_notes = [
        "Use small multiples: workflow hierarchy, ordered hook sequence, shared-skill reuse, reflective loop, and detailed stack lanes.",
        "Keep workflow sequence explicit with family -> workflow -> ordered step hierarchy and next-step edges.",
        "Keep loops separate from linear stack order so critic/refiner/guard behavior is visible without tangling every edge.",
        "Show hooks as ordered chips inside collapsible lanes; this preserves hierarchy while keeping the first screen readable.",
        "Use an interactive Cytoscape.js layer for granular skill-to-skill edge inspection, with static SVG views as the durable fallback.",
    ]
    notes_html = "".join(f"<li>{escape(note)}</li>" for note in design_notes)
    legend_html = "".join(
        f"""
        <li data-kind="{escape(item['kind'])}">
          <i aria-hidden="true"></i>
          <strong>{escape(item['label'])}</strong>
          <span>{escape(item['meaning'])}</span>
        </li>
        """
        for item in conceptual_core["legend"]
    )
    shared_hook_html = "".join(
        f"<li><strong>{escape(skill_display_label(item['skill']))}</strong>"
        f"<span>{escape(', '.join(item['workflows']))}</span></li>"
        for item in conceptual_core["shared_hooks"]
    ) or "<li><strong>No shared hooks</strong><span>Each extracted hook belongs to one workflow.</span></li>"
    feedback_html = "".join(
        f"<li><strong>{escape(item['workflow'])}</strong>"
        f"<span>{escape(', '.join(item['roles']) or 'reflective return')}</span></li>"
        for item in conceptual_core["feedback_loops"]
    ) or "<li><strong>No feedback loops</strong><span>No reflective role was extracted.</span></li>"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Project Workflow Graphs</title>
  <style>
    :root {{ --ink:#172033; --muted:#64748b; --line:#dbe4ef; --wash:#f6f8fb; --accent:#0f766e; }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      background: radial-gradient(circle at 18% 4%, #dff8f2 0, transparent 28%), linear-gradient(180deg, #f8fbff, #eef3f8);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }}
    main {{ max-width: 1200px; margin: 0 auto; padding: 48px 24px 72px; }}
    .eyebrow {{ color: var(--accent); font-weight: 800; letter-spacing: .08em; text-transform: uppercase; font-size: 12px; }}
    h1 {{ font-size: clamp(40px, 6vw, 78px); line-height: .94; margin: 10px 0 18px; letter-spacing: 0; max-width: 980px; }}
    .lead {{ color: var(--muted); font-size: 19px; max-width: 880px; }}
    section {{ margin: 34px 0; }}
    h2 {{ font-size: 28px; margin: 0 0 18px; }}
    .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; }}
    .stat, .panel, details {{
      background: rgba(255,255,255,.9);
      border: 1px solid rgba(203, 213, 225, .82);
      border-radius: 16px;
      box-shadow: 0 18px 45px rgba(15, 23, 42, .06);
    }}
    .stat {{ padding: 16px; min-height: 104px; }}
    .stat span {{ display:block; color:var(--muted); font-size:13px; }}
    .stat strong {{ display:block; font-size:32px; margin-top:10px; }}
    .panel {{ padding: 18px 22px; }}
    .panel ul {{ margin: 8px 0 0; padding-left: 22px; color: #334155; }}
    .panel p {{ margin: 8px 0; color: #334155; }}
    .topology-reading {{
      padding: 26px 28px;
      border: 1px solid rgba(15, 118, 110, .24);
      border-radius: 22px;
      background: linear-gradient(135deg, rgba(255,255,255,.94), rgba(236,254,255,.72));
      box-shadow: 0 22px 54px rgba(15, 23, 42, .07);
    }}
    .topology-reading > p {{ max-width: 940px; color: #334155; font-size: 17px; }}
    .topology-legend {{ list-style: none; padding: 0; margin: 22px 0; display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }}
    .topology-legend li {{ min-height: 126px; padding: 16px; border-top: 3px solid #94a3b8; background: #ffffffb8; }}
    .topology-legend li[data-kind="forward_sequence"] {{ border-top-color: #0f766e; }}
    .topology-legend li[data-kind="shared_hook"] {{ border-top-color: #0e7490; }}
    .topology-legend li[data-kind="feedback_loop"] {{ border-top-color: #c2410c; }}
    .topology-legend i {{ display: block; width: 44px; height: 2px; margin: 2px 0 14px; background: currentColor; }}
    .topology-legend li[data-kind="feedback_loop"] i {{ border-top: 2px dashed #c2410c; background: none; }}
    .topology-legend strong, .topology-legend span {{ display: block; }}
    .topology-legend span {{ margin-top: 6px; color: var(--muted); font-size: 13px; }}
    .coupling-reading {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-top: 20px; }}
    .coupling-reading h3 {{ margin: 0 0 9px; font-size: 17px; }}
    .coupling-reading ul {{ list-style: none; padding: 0; margin: 0; }}
    .coupling-reading li {{ padding: 8px 0; border-bottom: 1px solid var(--line); }}
    .coupling-reading li span {{ display: block; color: var(--muted); font-size: 12px; }}
    .topology-limit {{ margin-top: 20px; color: var(--muted); font-size: 14px; }}
    .graph-controls {{ display:flex; flex-wrap:wrap; gap:10px; margin: 14px 0; }}
    .graph-controls button {{ border:1px solid #cbd5e1; background:#ffffff; color:#334155; border-radius:999px; padding:9px 14px; font-weight:800; cursor:pointer; }}
    .graph-controls button.active {{ background:#0f766e; border-color:#0f766e; color:#ffffff; }}
    .drill-selector {{ display:flex; align-items:center; gap:10px; margin: 10px 0 14px; color:#334155; font-weight:800; }}
    .drill-selector[hidden] {{ display:none; }}
    .drill-selector select {{ min-width: 320px; max-width: 100%; border:1px solid #cbd5e1; border-radius:12px; padding:9px 12px; background:#ffffff; color:#172033; font-weight:750; }}
    .click-drill-toolbar {{ display:flex; flex-wrap:wrap; align-items:center; gap:12px; margin: 10px 0 14px; color:#334155; font-weight:750; }}
    .click-drill-toolbar[hidden] {{ display:none; }}
    .click-drill-toolbar button {{ border:1px solid #cbd5e1; background:#ffffff; color:#334155; border-radius:999px; padding:9px 14px; font-weight:800; cursor:pointer; }}
    .click-drill-toolbar button:hover {{ border-color:#0f766e; color:#0f766e; }}
    .interactive-layout {{ display: block; margin-top: 14px; }}
    #cy {{ min-height: 980px; width: 100%; border-radius: 20px; border: 1px solid rgba(203, 213, 225, .82); background: rgba(255,255,255,.92); box-shadow: 0 18px 45px rgba(15, 23, 42, .06); }}
    #graph-inspector {{ margin-top: 14px; border-radius: 20px; border: 1px solid rgba(203, 213, 225, .82); background: rgba(255,255,255,.92); padding: 18px 22px; color: #334155; box-shadow: 0 18px 45px rgba(15, 23, 42, .06); }}
    #graph-inspector h3 {{ margin: 0 0 10px; color: var(--ink); }}
    #graph-inspector p {{ margin: 8px 0; }}
    .fallback-note {{ color: var(--muted); font-size: 13px; }}
    .chart-shell {{ overflow-x:auto; margin: 14px 0; }}
    svg {{ width: 100%; min-width: 860px; height: auto; display: block; border-radius: 20px; box-shadow: 0 18px 45px rgba(15, 23, 42, .06); }}
    .chart-title {{ font-size: 20px; font-weight: 850; fill: #172033; }}
    .family-label {{ font-size: 16px; font-weight: 800; fill: #172033; }}
    .small-label {{ font-size: 13px; fill: #64748b; }}
    .bar-label {{ font-size: 14px; font-weight: 750; fill: #334155; }}
    .bar-count {{ font-size: 13px; font-weight: 800; fill: #475569; }}
    .loop-label {{ font-size: 16px; font-weight: 850; fill: #172033; }}
    .loop-count {{ font-size: 13px; font-weight: 750; fill: #64748b; }}
    details {{ padding: 16px 20px; margin: 12px 0; }}
    summary {{ cursor:pointer; display:flex; justify-content:space-between; gap:18px; align-items:center; font-weight:850; }}
    summary em {{ color: var(--muted); font-style: normal; font-size: 13px; font-weight: 750; }}
    .stack-meta {{ margin-top: 14px; color:#334155; }}
    .stack-meta p {{ margin: 6px 0; }}
    .chip-row, .role-row {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:14px; }}
    .chip {{ background:#ecfeff; color:#0e7490; border:1px solid #bae6fd; border-radius:999px; padding:5px 9px; font-size:12px; font-weight:800; }}
    .role-chip {{ background:#fff7ed; color:#c2410c; border:1px solid #fed7aa; border-radius:999px; padding:5px 9px; font-size:12px; font-weight:800; }}
    .guardrails {{ margin: 14px 0 0; color:#475569; }}
    .empty {{ color:var(--muted); }}
    code {{ background:#eef6f5; color:#0f766e; padding:2px 5px; border-radius:6px; }}
    footer {{ color: var(--muted); margin-top:34px; font-size:13px; }}
    @media (max-width: 760px) {{
      .topology-legend, .coupling-reading {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
<main>
  <header>
    <div class="eyebrow">Workflow graph system</div>
    <h1>{escape(repo.name)} workflow interactions, with semantic graph detail.</h1>
    <p class="lead">A visual map of agentic workflow stacks, shared hooks, and reflective loops extracted from <code>{escape(Path(model["source_document"]).name)}</code>. Generated {escape(generated_at)}.</p>
  </header>

  <section>
    <h2>Current Workflow Surface</h2>
    <div class="stats">{stat_cards}</div>
  </section>

  <section class="topology-reading" data-conceptual-core="workflow-topology">
    <div class="eyebrow">Architecture reading</div>
    <h2>How work moves through the workflow system</h2>
    <p>{escape(conceptual_core["topology_thesis"])}</p>
    <p>{escape(conceptual_core["reading_strategy"])}</p>
    <ul class="topology-legend">{legend_html}</ul>
    <div class="coupling-reading">
      <div><h3>Shared hooks</h3><ul>{shared_hook_html}</ul></div>
      <div><h3>Guarded returns</h3><ul>{feedback_html}</ul></div>
    </div>
    <p class="topology-limit"><strong>Evidence limit.</strong> {escape(conceptual_core["evidence_boundary"])}</p>
  </section>

  <section>
    <h2>Representation Choice</h2>
    <div class="panel"><ul>{notes_html}</ul></div>
  </section>

  {interactive_graph_section(model)}

  <section>
    <h2>Overview</h2>
    <div class="chart-shell">{overview_svg(stacks)}</div>
  </section>

  <section>
    <h2>Interactions</h2>
    <div class="chart-shell">{shared_skill_svg(model["shared_skills"])}</div>
  </section>

  <section>
    <h2>Reflective Loops</h2>
    <div class="chart-shell">{reflective_loop_svg(stacks)}</div>
  </section>

  <section>
    <h2>Expanded Stack Lanes</h2>
    {stack_details_html(stacks)}
  </section>

  <footer>Generated by <code>proj_skills/project-workflow-graph-reporter</code>. Static graphs are embedded so the report remains usable offline.</footer>
</main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository root to analyze.")
    parser.add_argument("--contract", help="Workflow contract path. Defaults to AGENTS.md under the repository root.")
    parser.add_argument("--output", required=True, help="HTML output path.")
    parser.add_argument("--json-output", help="Optional JSON model output path.")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    contract_path = Path(args.contract).resolve() if args.contract else repo / "AGENTS.md"
    if not contract_path.is_file():
        raise SystemExit(f"Workflow contract not found: {contract_path}")

    model = build_model(repo, contract_path)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rendered_html = render_html(repo, model)
    output_path.write_text(
        "\n".join(line.rstrip() for line in rendered_html.splitlines()) + "\n",
        encoding="utf-8",
    )

    if args.json_output:
        json_path = Path(args.json_output)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(model, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {output_path}")
    if args.json_output:
        print(f"Wrote {args.json_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
