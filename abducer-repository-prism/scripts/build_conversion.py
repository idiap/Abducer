#!/usr/bin/env python3
"""Generate the deterministic, source-grounded Abducer PRISM conversion tree.

The canonical manifest and reviewed typed workflow modules are the authority for
workflow identity and topology.  This generator deliberately does not reuse the
older fixture/fake-handler entrypoints: every occurrence becomes a real typed PRISM
model agent, and selected repository skills are compiled as ``Skill[T]`` artifacts.
Unresolved source projections remain explicitly generative; generation closes the
runtime binding gap without claiming a new deterministic scientific implementation.

All discovery and output order is repository-relative and sorted.  Generated JSON is
canonical, generated text is UTF-8/LF with one terminal newline, and no timestamp,
temporary path, random identifier, credential, or host-specific username is emitted.
"""
from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "abducer-repository-prism"
MANIFEST_PATH = ROOT / "abducer-prism/workflows/manifest.json"
LEDGER_PATH = ROOT / ".prism/add-abducer-prism-materialization-workflows/materialization-binding-ledger.json"
SKILL_ROOTS = ("skills", "proj_skills", "prism_me", "abducer-prism/skills", "external")
DEFAULT_SKILLS = {
    "Abductive": "skills/reasoning/kb-abduce",
    "Analogical": "skills/reasoning/proof-bridge-object-forger",
    "Contrastive": "skills/evaluation/counterfactual-route-prober",
    "Deductive": "skills/reasoning/kb-deduce",
    "Evidential": "skills/evaluation/epistemic-status-ledger",
    "Inductive": "skills/reasoning/kb-induce",
    "ModelBased": "skills/reasoning/dynamic-symbolic-simulation-experimenter",
    "Refutational": "skills/evaluation/counterexample-hunter",
}

DISCOVERY_REPORT_SECTIONS = (
    ("overview", "Summary"),
    ("physics_math_strategy", "Mathematical Strategy"),
    ("timeline", "Timeline"),
    ("ranked_queue", "Ranked Analyses"),
    ("skills", "Skill Use"),
    ("contributions", "Contributions"),
    ("result_atlas", "Result Atlas"),
    ("literature", "Problem & Literature"),
    ("macro_strategy", "Macro Strategies"),
    ("strategy_judge", "Strategy Judge"),
    ("artifact_or_stop", "Artifact-Or-Stop"),
    ("story", "Story"),
    ("branches", "Branches"),
    ("reviews", "Deep Reviews"),
)

EXAMPLE_INPUTS: dict[str, dict[str, Any]] = {
    "target_navigation_loop": {
        "target_id": "markov-kakutani-fixed-point-theorem",
    },
    "discovery_marathon_loop": {
        "context_summary": (
            "Compare fixed-point proof routes for a commuting finite family of affine "
            "self-maps on a compact convex set; retain every unproved premise."
        ),
    },
    "abducer_work_loop": {
        "obligation": (
            "Identify a testable induction route for extending a common fixed point "
            "from n commuting affine maps to n+1 maps."
        ),
    },
    "conceptual_hypothesis_exploration_loop": {
        "obstruction": (
            "The current route does not justify why the fixed-point set of the first n "
            "maps is preserved by the remaining commuting map."
        ),
    },
    "release_promotion_loop": {
        "run_id": "markov-kakutani-review-01",
        "evidence_ref": "KB/markov-kakutani-fixed-point-theorem.kb.md",
    },
    "evidence_to_proof_route_onramp": {
        "source_id": "markov-kakutani-kb-route",
    },
    "conceptual_frontier_deepening": {
        "frozen_context": (
            "Work only with a finite commuting family first; distinguish compactness, "
            "convexity, affinity, and commutativity obligations."
        ),
    },
    "theorem_proof_delivery": {
        "queue_item_id": "mk-finite-family-induction",
        "premises": {
            "premise_set_id": "mk-standard-premises",
            "exact_statement": (
                "A finite commuting family of continuous affine self-maps of a nonempty "
                "compact convex subset of a locally convex space has a common fixed point."
            ),
        },
    },
    "scientific_contribution_cultivation": {
        "result_id": "mk-finite-family-proof-route",
    },
    "manuscript_result_elaboration": {
        "draft_id": "mk-fixed-point-method-note",
    },
    "deep_review_and_reorientation": {
        "review_evidence_summary": (
            "The finite-family induction route is plausible, but preservation of the "
            "intermediate fixed-point set and the infinite-family limit remain separate."
        ),
    },
    "timeline-paper-independent-workflow": {
        "timeline_ref": "mk-reasoning-timeline-01",
    },
    "ym-representational-dynamics-overlay": {
        "target_id": "yang-mills-existence-and-mass-gap",
        "continuum_boundary_ref": "KB/yang-mills-existence-and-mass-gap.kb.md",
    },
    "cohere_fast": {
        "domain_id": "yang-mills",
        "target_ref": "finite-regulator-to-continuum-mass-gap-route",
    },
    "cohere_fast_scope_and_ground": {
        "domain_id": "yang-mills",
        "target_ref": "finite-regulator-to-continuum-mass-gap-route",
        "sources_ref": "KB/yang-mills-existence-and-mass-gap.kb.md",
    },
    "cohere_fast_adaptive_frontier": {
        "domain_id": "yang-mills",
        "target_ref": "finite-regulator-frontier",
        "claim_ceiling": "conditional finite-regulator statements only",
    },
    "cohere_fast_derivation_and_proof": {
        "domain_id": "yang-mills",
        "frontier_ref": "finite-regulator-frontier",
        "claim_ceiling": "conditional derivation with explicit open obligations",
    },
    "cohere_fast_independent_audit": {
        "domain_id": "yang-mills",
        "derivation_ref": "conditional-finite-regulator-derivation",
        "open_obligations_ref": "continuum-limit-and-uniformity-obligations",
        "claim_ceiling": "no continuum mass-gap claim without discharged obligations",
    },
    "cohere_fast_manuscript_release": {
        "domain_id": "yang-mills",
        "audit_ref": "independent-audit-finite-regulator-01",
        "claim_ceiling": "claim-bounded presentation of conditional results",
    },
}


def canonical_json(value: Any) -> str:
    """Serialize stable finite JSON with a single terminal newline."""
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"


def digest_bytes(value: bytes) -> str:
    """Return a lowercase SHA-256 digest for a source or generated payload."""
    return hashlib.sha256(value).hexdigest()


def digest_file(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def write(path: Path, content: str) -> None:
    """Write normalized generated text only when its bytes changed."""
    normalized = content.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n") + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text(encoding="utf-8") != normalized:
        path.write_text(normalized, encoding="utf-8", newline="\n")


def source_revision() -> str:
    """Return a content identity without creating a commit-generation cycle.

    Generated files are committed with the source changes they describe, so embedding
    ``git rev-parse HEAD`` would always record the parent commit and would make a clean
    post-commit regeneration dirty. The canonical manifest and materialization ledger
    define the conversion surface; their content digest is stable before and after the
    generated tree is committed. The complete per-file fingerprint below still binds
    every workflow and skill byte.
    """
    authorities = [MANIFEST_PATH, LEDGER_PATH]
    identity = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": digest_file(path),
        }
        for path in sorted(authorities, key=lambda item: item.relative_to(ROOT).as_posix())
    ]
    return digest_bytes(canonical_json(identity).encode("utf-8"))


def parse_front_matter(path: Path) -> tuple[str, str]:
    """Read display metadata while preserving the full skill file as instructions."""
    text = path.read_text(encoding="utf-8")
    name = path.parent.name
    description = name.replace("-", " ")
    header = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.S)
    if header:
        for key, value in re.findall(r"(?m)^(name|description):\s*(.+)$", header.group(1)):
            value = value.strip().strip("\"'")
            if key == "name" and value:
                name = value
            elif key == "description" and value:
                description = value
    return name, description


def skill_id(root: str) -> str:
    """Build a readable, collision-resistant id from the repository-relative root."""
    slug = re.sub(r"[^a-z0-9]+", "-", root.lower()).strip("-")[:120]
    return f"skill-{slug}-{digest_bytes(root.encode())[:12]}"


def agent_invocation_contract(bindings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Describe the exact native agent/skill receipts expected at runtime.

    Workflow ``skill_ids`` are package dependencies, not proof that a skill ran.  This
    contract is deliberately occurrence-level so the isolated worker can compare the
    engine's native trace with the material graph and Lunar can validate the same
    receipts shown by the run UI.
    """
    grouped: dict[str, list[str]] = {}
    for binding in bindings:
        grouped.setdefault(binding["alias"], []).append(
            PurePosixPath(binding["skill_path"]).name
        )
    return [
        {
            "agent_name": alias + "_material_agent",
            "workflow_occurrence": alias,
            "activated_skill_ids": list(dict.fromkeys(skill_names)),
        }
        for alias, skill_names in grouped.items()
    ]


def discover_skills() -> tuple[list[dict[str, Any]], dict[str, str]]:
    """Inventory every in-scope skill tree with no heuristic runtime exclusions."""
    roots: set[str] = set()
    for supplied in SKILL_ROOTS:
        base = ROOT / supplied
        if not base.exists():
            continue
        roots.update(
            path.parent.relative_to(ROOT).as_posix()
            for path in base.rglob("SKILL.md")
            if path.is_file()
        )
    rows = []
    mapping = {}
    for root in sorted(roots):
        path = ROOT / root / "SKILL.md"
        name, description = parse_front_matter(path)
        identifier = skill_id(root)
        mapping[root] = identifier
        rows.append(
            {
                "id": identifier,
                "name": name,
                "root": root,
                "description": description,
                "groups": list(PurePosixPath(root).parts[:-1]),
                # The converter's v1 exporter currently sorts capabilities as a
                # hashable set while Lunar's v1 resource schema expects objects.
                # An empty list is the only value accepted by both contracts;
                # complete capability instructions remain in SKILL.md.
                "capabilities": [],
                "exclude": ["**/__pycache__/**", "**/*.pyc", "**/.DS_Store"],
                "metadata": {
                    "conversion_disposition": "converted",
                    "execution_posture": "instruction-capability",
                },
            }
        )
    return rows, mapping


def parse_types(text: str) -> dict[str, dict[str, Any]]:
    """Parse the deliberately simple record/variant declarations in reviewed modules."""
    result: dict[str, dict[str, Any]] = {}
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        match = re.match(r"^type\s+(\w+):\s*$", lines[index])
        if match is None:
            index += 1
            continue
        name = match.group(1)
        index += 1
        fields: list[tuple[str, str]] = []
        variants: list[str] = []
        while index < len(lines) and (not lines[index].strip() or lines[index].startswith((" ", "\t"))):
            field = re.match(r"\s+(\w+):\s*(.+?)\s*$", lines[index])
            variant = re.match(r"\s*\|\s*(\w+)\s*$", lines[index])
            if field:
                fields.append((field.group(1), field.group(2)))
            if variant:
                variants.append(variant.group(1))
            index += 1
        result[name] = {"fields": fields, "variants": variants}
    return result


def schema_for_type(type_name: str, declarations: dict[str, dict[str, Any]], default: Any) -> dict[str, Any]:
    """Translate the source input type closure into a closed JSON Schema."""
    type_name = type_name.strip()
    if type_name == "String":
        return {"type": "string", "minLength": 1, "maxLength": 16000, "default": default}
    if type_name in {"Int", "Integer"}:
        return {"type": "integer", "default": default}
    if type_name in {"Float", "Number"}:
        return {"type": "number", "default": default}
    if type_name == "Bool":
        return {"type": "boolean", "default": default}
    list_match = re.fullmatch(r"List\[(.+)\]", type_name)
    if list_match:
        values = default if isinstance(default, list) else ["source-grounded item"]
        item_default = values[0] if values else "source-grounded item"
        return {
            "type": "array",
            "minItems": 1,
            "items": schema_for_type(list_match.group(1), declarations, item_default),
            "default": values,
        }
    option_match = re.fullmatch(r"Option\[(.+)\]", type_name)
    if option_match:
        return {
            "anyOf": [
                {"type": "null"},
                schema_for_type(option_match.group(1), declarations, default),
            ],
            "default": default,
        }
    declaration = declarations.get(type_name)
    if declaration is None:
        raise ValueError(f"unsupported input type {type_name!r}")
    if declaration["variants"]:
        value = default if isinstance(default, str) else declaration["variants"][0]
        return {"type": "string", "enum": declaration["variants"], "default": value}
    if not isinstance(default, dict):
        raise ValueError(f"record input {type_name} requires an object default")
    properties = {
        name: schema_for_type(field_type, declarations, default[name])
        for name, field_type in declaration["fields"]
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": properties,
        "required": [name for name, _ in declaration["fields"]],
        "default": default,
    }


def workflow_shape(reasoning: str, occurrences: str) -> dict[str, Any]:
    """Extract the single-input reasoning declaration and exact occurrence sequence."""
    declaration = re.search(
        r"reasoning\s+(?P<name>\w+)\s*\((?P<parameters>.*?)\)\s*"
        r"->\s*Generated\[(?P<output>\w+)\]:(?P<body>.*)\Z",
        reasoning,
        re.S,
    )
    if declaration is None:
        raise ValueError("reasoning declaration not found")
    parameters = re.findall(r"(?m)^\s*(\w+)\s*:\s*(\w+)\s*,?\s*$", declaration.group("parameters"))
    if len(parameters) != 1:
        raise ValueError(f"expected one reasoning input, found {parameters!r}")
    signatures = {
        match.group("name"): (match.group("input"), match.group("output"))
        for match in re.finditer(
            r"(?m)^type\s+(?P<name>\w+)\s*=\s*(?P<input>\w+)\s*"
            r"->\s*Generated\[(?P<output>\w+)\]\s*$",
            occurrences,
        )
    }
    calls = [
        {"alias": alias, "method": method, "input": signatures[method][0], "output": signatures[method][1]}
        for alias, method in re.findall(r"\[(\w+)\s*:\s*(\w+)\(", declaration.group("body"))
    ]
    if not calls:
        raise ValueError("reasoning declaration has no occurrences")
    return {
        "reasoning": declaration.group("name"),
        "input_name": parameters[0][0],
        "input_type": parameters[0][1],
        "output_type": declaration.group("output"),
        "body": declaration.group("body"),
        "calls": calls,
    }


def localize_imports(text: str, module_id: str) -> str:
    """Make reviewed modules self-contained inside one exported project root."""
    return text.replace(f"from workflows.{module_id}.", "from ")


def record_owners(types_text: str, occurrences_text: str) -> dict[str, str]:
    """Map nominal records to the local module that owns their runtime identity."""
    owners = {name: "types" for name in parse_types(types_text)}
    owners.update({name: "occurrences" for name in parse_types(occurrences_text)})
    return owners


def choose_projection_skills(skill_paths: list[str]) -> list[str]:
    """Choose bounded executable guidance for a formerly unresolved projection.

    The complete declared list remains a project reference.  Execution favors a named
    orchestrator or program skill; otherwise small lists are retained and large lists
    contribute stable boundary representatives to avoid an unbounded model prompt.
    """
    orchestrators = [path for path in skill_paths if "orchestrator" in path or path.endswith("ym-run-clay-program")]
    if orchestrators:
        return sorted(orchestrators)
    ordered = sorted(skill_paths)
    if len(ordered) <= 4:
        return ordered
    return sorted({*ordered[:2], *ordered[-2:]})


def skill_attachments(skill_root: Path) -> str:
    """Encode referenced skill support files into the PRISM skill artifact."""
    encoded = {}
    for path in sorted(skill_root.rglob("*"), key=lambda item: item.relative_to(skill_root).as_posix()):
        if not path.is_file() or path.name == "SKILL.md" or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        encoded[path.relative_to(skill_root).as_posix()] = base64.b64encode(path.read_bytes()).decode("ascii")
    return json.dumps(encoded, sort_keys=True, separators=(",", ":"))


def output_contract_guidance(
    output_type: str, declarations: dict[str, dict[str, Any]]
) -> str:
    """Render model-visible constraints omitted by the current PRISM JSON Schema adapter."""
    declaration = declarations[output_type]
    # A closed source variant is projected to ``String`` at the provider boundary.
    # Calling that value an "object" encouraged otherwise schema-capable models to
    # wrap the constructor in an invented record, which the runtime correctly
    # rejected.  Spell out the JSON scalar shape independently of record outputs.
    if declaration["variants"]:
        alternatives = ", ".join(
            f"`{variant}`" for variant in declaration["variants"]
        )
        return (
            "## Packaged PRISM Output Contract\n\n"
            f"Return exactly one JSON string for the generated `{output_type}` value. "
            "Do not return an object, field wrapper, explanation, or paraphrase.\n\n"
            f"- The entire value must be exactly one of: {alternatives}."
        )
    constraints = []
    for field, field_type in declaration["fields"]:
        variants = declarations.get(field_type, {}).get("variants", [])
        if variants:
            constraints.append(
                f"- `{field}` must be exactly one of: "
                + ", ".join(f"`{variant}`" for variant in variants)
                + "."
            )
    suffix = "\n".join(constraints) if constraints else "- Follow the exact generated JSON schema without extra fields."
    return (
        "## Packaged PRISM Output Contract\n\n"
        f"Return exactly the generated `{output_type}` JSON object. Do not paraphrase "
        "closed variant values.\n\n"
        + suffix
    )


def variant_constraints(
    output_type: str, declarations: dict[str, dict[str, Any]]
) -> dict[str, list[str]]:
    """Return direct closed-variant fields for one nominal output record."""
    if declarations[output_type]["variants"]:
        return {"__value__": declarations[output_type]["variants"]}
    return {
        field: declarations[field_type]["variants"]
        for field, field_type in declarations[output_type]["fields"]
        if declarations.get(field_type, {}).get("variants")
    }


def material_type_projection(
    declarations: dict[str, dict[str, Any]], roots: list[str]
) -> tuple[dict[str, str], str]:
    """Replace model-produced closed variants with adapter-verifiable strings.

    Lunar's current provider schema erases nominal variant constructors from model
    response schemas.  Material records therefore use strings at the model boundary;
    the runtime adapter validates those strings against the source alternatives.
    Original source declarations remain packaged unchanged for inspection.
    """
    projected: dict[str, str] = {}
    rendered: dict[str, str] = {}
    visiting: set[str] = set()

    def transform(expression: str) -> str:
        expression = expression.strip()
        wrapper = re.fullmatch(r"(List|Option)\[(.+)\]", expression)
        if wrapper:
            child = transform(wrapper.group(2))
            return f"{wrapper.group(1)}[{child}]"
        declaration = declarations.get(expression)
        if declaration is None:
            return expression
        if declaration["variants"]:
            projected[expression] = "String"
            return "String"
        if expression in projected:
            return projected[expression]
        if expression in visiting:
            raise ValueError(f"recursive material type projection is unsupported: {expression}")
        visiting.add(expression)
        fields = [(name, transform(field_type)) for name, field_type in declaration["fields"]]
        visiting.remove(expression)
        if fields == declaration["fields"]:
            projected[expression] = expression
            return expression
        target = "Material" + expression
        projected[expression] = target
        rendered[target] = "\n".join(
            [f"type {target}:", *[f"    {name}: {field_type}" for name, field_type in fields]]
        )
        return target

    for root in roots:
        transform(root)
    return projected, "\n\n".join(rendered[name] for name in sorted(rendered))


def render_skill_module(
    alias: str,
    ordinal: int,
    skill_path: str,
    input_type: str,
    output_type: str,
    owner: str,
    declarations: dict[str, dict[str, Any]],
) -> tuple[str, str]:
    """Compile one real repository skill tree for a typed PRISM model agent."""
    root = ROOT / skill_path
    skill_file = root / "SKILL.md"
    if not skill_file.is_file():
        raise ValueError(f"selected runtime skill is missing: {skill_path}")
    name, description = parse_front_matter(skill_file)
    variable = f"{alias}_skill_{ordinal}"
    instructions = (
        skill_file.read_text(encoding="utf-8").rstrip()
        + "\n\n"
        + output_contract_guidance(output_type, declarations)
        + "\n"
    )
    text = "\n".join(
        (
            f"from {owner} import {input_type}",
            "",
            f"{variable}: Skill[{input_type}] = skill_artifact[{input_type}](",
            f"    {json.dumps(name, ensure_ascii=False)},",
            '    "0.0.0+repository-conversion",',
            f"    {json.dumps(name, ensure_ascii=False)},",
            f"    {json.dumps(description, ensure_ascii=False)},",
            f"    {json.dumps(instructions, ensure_ascii=False)},",
            f"    {json.dumps(skill_attachments(root), ensure_ascii=False)},",
            ")",
        )
    )
    return variable, text


def output_schema(*, typed_report: bool = False) -> dict[str, Any]:
    """Describe the complete verified worker result returned to Lunar."""
    structured_required = [
        "final_disposition",
        "reasoning_result",
        "execution_provenance",
    ]
    structured_properties: dict[str, Any] = {
        "final_disposition": {
            "type": "object",
            "required": ["status", "reasoning_complete", "blockers"],
            "properties": {
                "status": {"const": "passed"},
                "reasoning_complete": {"const": True},
                "blockers": {"type": "array", "maxItems": 0},
            },
        },
        "reasoning_result": {"type": "object"},
        "execution_provenance": {"type": "object"},
    }
    if typed_report:
        structured_required.append("typed_report")
        structured_properties["typed_report"] = {
            "type": "object",
            "required": ["version", "report", "native", "sections"],
            "properties": {
                "version": {"const": "1"},
                "report": {"type": "object"},
                "native": {"type": "object"},
                "sections": {"type": "object"},
            },
        }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "markdown",
            "structured_value",
            "analysis_results",
            "compact_prism_input",
            "narrative_slots",
            "report_verification",
        ],
        "properties": {
            "markdown": {"type": "string", "minLength": 1},
            "structured_value": {
                "type": "object",
                "required": structured_required,
                "properties": structured_properties,
            },
            "analysis_results": {"type": "object"},
            "compact_prism_input": {"type": "object"},
            "narrative_slots": {"type": "array"},
            "report_verification": {
                "type": "object",
                "required": ["status", "reasoning_complete"],
                "properties": {
                    "status": {"const": "passed"},
                    "reasoning_complete": {"const": True},
                },
            },
        },
    }


def render_discovery_report_function(
    *,
    function_name: str = "assemble_discovery_report",
    routing_type: str = "MaterialDiscoveryRoutingAssessment",
) -> str:
    """Return the genuine PRISM ``Report`` projection for Discovery Marathon.

    The material workflow and the reviewed reasoning view both use this renderer.
    Keeping the same typed report constructor in both graphs makes Lunar's
    source-derived reasoning contract identical to the runtime event stream.
    """
    tab_rows = []
    template_rows = []
    for slug, label in DISCOVERY_REPORT_SECTIONS:
        tab_rows.append(
            f'        r.Tab(id="{slug}", label="{label}", sections=[{slug}_section]),'
        )
        template_rows.append(
            f'        r.TemplateTab(id="{slug}", sections=[r.MarkdownSlot(id="{slug}-content")]),'
        )
    return "\n".join(
        [
            f"def {function_name}(",
            "    context: DiscoveryRunContext,",
            "    scope: BoundedDiscoveryScope,",
            "    hypothesis: DiscriminatingDiscoveryHypothesis,",
            "    pattern: ProvisionalDiscoveryPattern,",
            "    implications: HypothesisModelImplications,",
            "    contrast: HypothesisContrastAssessment,",
            "    refutation: HypothesisRefutationAssessment,",
            f"    routing: {routing_type},",
            ") -> r.Report:",
            '    overview_text: String = "# Discovery Marathon Report\\n\\n## Final disposition\\n\\nDiscovery disposition: **" + routing.disposition + "**\\n\\n" + routing.routing_basis + "\\n\\n## Completed reasoning steps\\n\\n- search_scope\\n- discovery_hypothesis\\n- discovery_pattern\\n- model_implications\\n- contrast_assessment\\n- refutation_assessment\\n- routing_assessment\\n\\n## Typed reasoning result\\n\\n" + routing.routing_basis + "\\n\\n## Execution provenance\\n\\nThe report is the terminal typed value of the executed PRISM graph. Lunar retains the native trace and section ancestry.\\n\\n## Interpretation and limits\\n\\nRuntime completion does not prove a theorem or validate a scientific claim."',
            '    physics_math_strategy_text: String = "### Bounded scope\\n\\n" + scope.bounded_scope + "\\n\\n### Candidate hypothesis\\n\\n" + hypothesis.hypothesis + "\\n\\n### Provisional pattern\\n\\n" + pattern.provisional_pattern + "\\n\\n### Bounded model implications\\n\\n" + implications.bounded_model_implications',
            '    timeline_text: String = "The seven declared reasoning occurrences completed before this typed report was assembled.\\n\\n| # | Reasoning stage | Status |\\n| ---: | --- | --- |\\n| 1 | search_scope | completed |\\n| 2 | discovery_hypothesis | completed |\\n| 3 | discovery_pattern | completed |\\n| 4 | model_implications | completed |\\n| 5 | contrast_assessment | completed |\\n| 6 | refutation_assessment | completed |\\n| 7 | routing_assessment | completed |"',
            '    ranked_queue_text: String = "1. **Validate sources and exact theorem hypotheses.** " + routing.routing_basis + "\\n2. **Discharge the strongest refutation pressure.** " + refutation.scoped_refutation + "\\n3. **Test the controlled contrast.** " + contrast.controlled_contrast + "\\n4. **Check bounded implications.** " + implications.bounded_model_implications',
            '    skills_text: String = "Seven packaged skills were bound to the seven executed occurrences. Skill use supports generation and critique; it is not independent scientific verification.\\n\\n| Stage | Packaged skill |\\n| --- | --- |\\n| search_scope | epistemic-status-ledger |\\n| discovery_hypothesis | kb-abduce |\\n| discovery_pattern | kb-induce |\\n| model_implications | dynamic-symbolic-simulation-experimenter |\\n| contrast_assessment | counterfactual-route-prober |\\n| refutation_assessment | counterexample-hunter |\\n| routing_assessment | epistemic-status-ledger |"',
            '    contributions_text: String = "- Preserved the user-supplied problem boundary through all seven typed stages.\\n- Produced separate abductive and inductive formation records.\\n- Produced separate model-based and contrastive probes before refutation.\\n- Retained a closed routing disposition with explicit limitations.\\n- Scientific novelty remains **not claimed**; all substantive content is model-generated."',
            '    result_atlas_text: String = "### Search scope\\n\\n" + scope.bounded_scope + "\\n\\n### Discovery hypothesis\\n\\n" + hypothesis.hypothesis + "\\n\\n### Discovery pattern\\n\\n" + pattern.provisional_pattern + "\\n\\n### Model implications\\n\\n" + implications.bounded_model_implications + "\\n\\n### Controlled contrast\\n\\n" + contrast.controlled_contrast + "\\n\\n### Refutation assessment\\n\\n" + refutation.scoped_refutation + "\\n\\n### Routing assessment\\n\\n" + routing.routing_basis',
            '    literature_text: String = "### Problem statement\\n\\n" + context.context_summary + "\\n\\n### Literature status\\n\\nThis workflow requested no public-network authority and performed no live literature acquisition. References mentioned by generated outputs remain leads requiring source retrieval and validation."',
            '    macro_strategy_text: String = "### Formation route\\n\\n" + hypothesis.hypothesis + "\\n\\n### Pattern route\\n\\n" + pattern.provisional_pattern + "\\n\\n### Model-pressure route\\n\\n" + implications.bounded_model_implications',
            '    strategy_judge_text: String = "### Controlled contrast\\n\\n" + contrast.controlled_contrast + "\\n\\n### Refutation assessment\\n\\n" + refutation.scoped_refutation + "\\n\\n### Routing judgment\\n\\n**" + routing.disposition + "**\\n\\n" + routing.routing_basis',
            '    artifact_or_stop_text: String = "**Decision:** " + routing.disposition + "\\n\\n" + routing.routing_basis + "\\n\\nRepository-compatible artifacts are released only after Lunar verifies reasoning completion and report integrity. A passed runtime is not a proof certificate."',
            '    story_text: String = "The run began by bounding the search:\\n\\n" + scope.bounded_scope + "\\n\\nIt formed an abductive hypothesis and an inductive pattern:\\n\\n" + hypothesis.hypothesis + "\\n\\n" + pattern.provisional_pattern + "\\n\\nThe probe lanes were merged by refutation before routing:\\n\\n" + routing.routing_basis',
            '    branches_text: String = "### Formation branch · abductive\\n\\n" + hypothesis.hypothesis + "\\n\\n### Formation branch · inductive\\n\\n" + pattern.provisional_pattern + "\\n\\n### Probe branch · model implications\\n\\n" + implications.bounded_model_implications + "\\n\\n### Probe branch · controlled contrast\\n\\n" + contrast.controlled_contrast + "\\n\\n### Merge · refutation\\n\\n" + refutation.scoped_refutation',
            '    reviews_text: String = "### Epistemology\\n\\nGenerated hypotheses, probes, refutation, and routing remain distinct evidence classes.\\n\\n### Mathematics\\n\\nThe content remains conditional until hypotheses, proof steps, counterexamples, and sources are checked.\\n\\n### AI research\\n\\nOne schema-valid run does not measure calibration or cross-model agreement.\\n\\n### Software engineering\\n\\nThe typed PRISM Report, native trace, section ancestry, source hashes, and artifacts are retained for replay."',
            *[
                f'    {slug}_section: r.Section = r.Markdown(id="{slug}-content", text={slug}_text)'
                for slug, unused in DISCOVERY_REPORT_SECTIONS
            ],
            "    tabs: List[r.Tab] = [",
            *tab_rows,
            "    ]",
            '    report_sections: List[r.Section] = [r.Tabs(id="discovery-sections", tabs=tabs)]',
            "    template_tabs: List[r.TemplateTab] = [",
            *template_rows,
            "    ]",
            '    template_sections: List[r.TemplateSection] = [r.TabsSlot(id="discovery-sections", tabs=template_tabs)]',
            '    template: r.TemplateChoice = r.WithTemplate(snapshot=r.Template(id="abducer-discovery-marathon-v1", title="Discovery Marathon", sections=template_sections))',
            '    return r.Report(id="discovery-marathon-report", title="Discovery Marathon Report", sections=report_sections, template=template)',
        ]
    )


def render_reasoning_view(workflow_id: str, text: str) -> str:
    """Render the Lunar-visible reasoning graph for one converted workflow.

    Discovery Marathon has a terminal typed-report occurrence in the executable
    graph. Lunar derives its host reasoning contract from this reviewed view, so
    the view must expose the same occurrence rather than ending one step early.
    """
    if workflow_id != "discovery_marathon_loop":
        return text

    text = text.replace(
        "from types import (",
        "import prism.reporting.report as r\n\nfrom types import (",
        1,
    )
    text, signature_replacements = re.subn(
        r"(reasoning\s+DiscoveryMarathonLoop\(.*?\)\s*->\s*)Generated\[DiscoveryRoutingAssessment\](\s*:)",
        r"\1r.Report\2",
        text,
        count=1,
        flags=re.DOTALL,
    )
    if signature_replacements != 1:
        raise ValueError("Discovery Marathon reasoning view has no unique output signature")

    report_return = """        [typed_report: assemble_discovery_report_view(
            run_context,
            search_scope.value,
            discovery_hypothesis.value,
            discovery_pattern.value,
            model_implications.value,
            contrast_assessment.value,
            refutation_assessment.value,
            routing_assessment.value,
        )]

    return typed_report"""
    text, return_replacements = re.subn(
        r"(?m)^\s+return\s+routing_assessment\s*$",
        report_return,
        text,
        count=1,
    )
    if return_replacements != 1:
        raise ValueError("Discovery Marathon reasoning view has no unique routing return")

    marker = "reasoning DiscoveryMarathonLoop("
    if marker not in text:
        raise ValueError("Discovery Marathon reasoning view declaration is missing")
    report_function = render_discovery_report_function(
        function_name="assemble_discovery_report_view",
        routing_type="DiscoveryRoutingAssessment",
    )
    return text.replace(marker, report_function + "\n\n" + marker, 1)


def render_material_main(
    row: dict[str, Any],
    shape: dict[str, Any],
    types_text: str,
    occurrences_text: str,
    ledger_bindings: dict[str, str],
) -> tuple[str, list[dict[str, Any]]]:
    """Render the complete material reasoning path and its real skill bindings."""
    is_discovery_report = row["id"] == "discovery_marathon_loop"
    module_id = row.get("module_id", row["id"])
    owners = record_owners(types_text, occurrences_text)
    declarations = {**parse_types(types_text), **parse_types(occurrences_text)}
    material_types, material_types_text = material_type_projection(
        declarations,
        [type_name for call in shape["calls"] for type_name in (call["input"], call["output"])],
    )
    if material_types.get(shape["input_type"], shape["input_type"]) != shape["input_type"]:
        raise ValueError(f"{row['id']} requires an unsupported projected public input")
    if material_types_text:
        material_support_imports = [
            "from types import (",
            *[f"    {name}," for name in sorted(parse_types(types_text))],
            ")",
        ]
        material_occurrence_types = sorted(parse_types(occurrences_text))
        if material_occurrence_types:
            material_support_imports.extend(
                [
                    "",
                    "from occurrences import (",
                    *[f"    {name}," for name in material_occurrence_types],
                    ")",
                ]
            )
        write(
            OUTPUT / "projects" / row["id"] / "prism_project/generated/material_types.prism",
            "\n".join(material_support_imports) + "\n\n" + material_types_text,
        )
    manifest_skills = [item["path"] for item in row.get("skill_bindings", [])]
    imports = ["from types import (", *[f"    {name}," for name in sorted(parse_types(types_text))], ")"]
    occurrence_records = sorted(parse_types(occurrences_text))
    if occurrence_records:
        imports.extend(["from occurrences import (", *[f"    {name}," for name in occurrence_records], ")"])
    material_import = ""
    projected_records = sorted(set(material_types.values()) - set(declarations) - {"String"})
    if projected_records:
        material_import = "\n".join(
            ["from generated.material_types import (", *[f"    {name}," for name in projected_records], ")"]
        )

    generated_imports: list[str] = []
    agents: list[str] = []
    binding_evidence: list[dict[str, Any]] = []
    body = shape["body"].replace(shape["input_name"], shape["input_name"])
    material_output_type = material_types.get(shape["output_type"], shape["output_type"])
    for call in shape["calls"]:
        alias, method = call["alias"], call["method"]
        agent_input_type = material_types.get(call["input"], call["input"])
        agent_output_type = material_types.get(call["output"], call["output"])
        selected: list[str]
        reason: str
        if alias in ledger_bindings:
            selected = [ledger_bindings[alias]]
            reason = "reviewed materialization binding ledger"
        else:
            selected = [path for prefix, path in DEFAULT_SKILLS.items() if method.startswith(prefix)]
            reason = "reasoning-method class policy"
            if not selected and method.startswith("Unresolved"):
                selected = choose_projection_skills(manifest_skills)
                reason = "bounded representative guidance for unresolved source projection"
        if not selected:
            raise ValueError(f"{row['id']}:{alias} has no executable skill binding")
        skill_variables = []
        for ordinal, skill_path in enumerate(sorted(set(selected)), start=1):
            owner = "generated.material_types" if agent_input_type != call["input"] else owners.get(call["input"])
            if owner is None:
                raise ValueError(f"cannot locate input owner for {row['id']}:{alias}")
            variable, content = render_skill_module(
                alias,
                ordinal,
                skill_path,
                agent_input_type,
                call["output"],
                owner,
                declarations,
            )
            filename = f"generated/{alias}_skill_{ordinal}.prism"
            write(OUTPUT / "projects" / row["id"] / "prism_project" / filename, content)
            generated_imports.append(f"from generated.{alias}_skill_{ordinal} import {variable}")
            skill_variables.append(variable)
            binding_evidence.append(
                {
                    "alias": alias,
                    "method": method,
                    "input_type": call["input"],
                    "output_type": call["output"],
                    "skill_path": skill_path,
                    "selection_reason": reason,
                }
            )
        agent_name = f"{alias}_material_agent"
        agents.append(
            "\n".join(
                (
                    f"# Real model capability for source occurrence {alias}:{method}.",
                    f"agent {agent_name}(",
                    f"    task: {agent_input_type},",
                    f") -> Result[Generated[{agent_output_type}], ModelFailure]",
                    "    ! {AI.Generate, Context.Disclose}:",
                    f"    skills: Skills[{agent_input_type}] = [{', '.join(skill_variables)}]",
                )
            )
        )
        body = re.sub(
            rf"(\[{re.escape(alias)}\s*:\s*){re.escape(method)}(?=\()",
            rf"\1{agent_name}",
            body,
        )
    for source_type, projected_type in material_types.items():
        if source_type != projected_type and projected_type != "String":
            body = re.sub(rf"\b{re.escape(source_type)}(?=\()", projected_type, body)
    body = re.sub(r"\s+by\s+\w+(?:\[[^\]]+\])?", "", body)
    if is_discovery_report:
        report_return = """        [typed_report: assemble_discovery_report(
            run_context,
            search_scope.value,
            discovery_hypothesis.value,
            discovery_pattern.value,
            model_implications.value,
            contrast_assessment.value,
            refutation_assessment.value,
            routing_assessment.value,
        )]
    return typed_report"""
        body, replacements = re.subn(
            r"(?m)^\s+return\s+routing_assessment\s*$",
            report_return,
            body,
        )
        if replacements != 1:
            raise ValueError("Discovery Marathon material workflow has no unique report return")

    material_name = "Materialized" + shape["reasoning"]
    reasoning_steps = [call["alias"] for call in shape["calls"]]
    if is_discovery_report:
        reasoning_steps.append("typed_report")
    schema = schema_for_type(shape["input_type"], parse_types(types_text), EXAMPLE_INPUTS[row["id"]])
    provenance_contract = {
        "agent_invocations": agent_invocation_contract(binding_evidence),
        # Availability is not consumption. A converter may add required source reads
        # only when the material runtime genuinely reads and uses those resources.
        "required_source_reads": [],
    }
    annotation = {
        "declaration": material_name,
        "id": row["id"],
        "entry_argument": shape["input_name"],
        "input_schema": schema,
        "output_schema": output_schema(typed_report=is_discovery_report),
        "prepare_hook": "abducer-workflow-prepare",
        "execute_hook": "abducer-workflow-execute",
        "verify_hook": "abducer-workflow-verify",
        "metadata": {
            "description": row["function"],
            "model_required": True,
            "network_required": False,
            "required_host_capabilities": ["model", "prism-engine", "reasoning-events"],
            "timeout_seconds": 1800,
            "reasoning_required": True,
            "reasoning_contract": {
                "workflow": shape["reasoning"],
                "steps": reasoning_steps,
            },
            "completion_contract": {
                "terminal_state": "completed",
                "reasoning_events_min": len(reasoning_steps) * 2,
                "reasoning_complete": True,
                "allowed_final_statuses": ["passed", "completed"],
                "forbid_blockers": True,
            },
            "provenance_contract": provenance_contract,
            "semantic_mode": "operational-model-generated",
            "source_materialization_status": row.get("materialization", {}).get("status"),
            "scientific_truth_verified": False,
        },
    }
    if is_discovery_report:
        annotation["metadata"]["report_contract"] = {
            "schema_version": "abducer.discovery-marathon-report/v1",
            "presentation": "prism-typed-report/v1",
            "terminal_output_type": "prism.reporting.report.Report",
            "required_sections": [label for unused, label in DISCOVERY_REPORT_SECTIONS],
            "required_artifacts": [
                "typed-report.json",
                "report.md",
                "result.json",
                "latest.md",
                "latest.json",
                "latest.html",
                "full_timeline.html",
            ],
        }
    workflow_output = "r.Report" if is_discovery_report else f"Generated[{material_output_type}]"
    main_output = (
        "Result[r.Report, ModelFailure]"
        if is_discovery_report
        else f"Result[Generated[{material_output_type}], ModelFailure]"
    )
    sections = [
        "# lunar-runtime: " + json.dumps(annotation, sort_keys=True, separators=(",", ":")),
        (
            "# Host-executed material graph for the complete reviewed reasoning path.\n"
            "# Generated values retain the source epistemic boundary and are not native proof or experiment receipts."
        ),
        "import prism.reporting.report as r" if is_discovery_report else "",
        "\n".join(imports),
        material_import,
        "\n".join(sorted(generated_imports)),
        *agents,
        render_discovery_report_function() if is_discovery_report else "",
        (
            f"workflow {material_name}(\n"
            f"    {shape['input_name']}: {shape['input_type']},\n"
            f") -> {workflow_output}\n"
            "    fails ModelFailure\n"
            "    ! {AI.Generate, Context.Disclose}:"
            + body
        ),
        (
            "def main(\n"
            f"    {shape['input_name']}: {shape['input_type']},\n"
            "    model_access: ModelGenerate,\n"
            "    disclosure: ContextDisclose,\n"
            f") -> {main_output} "
            "! {AI.Generate, Context.Disclose}:\n"
            f"    return solve {material_name}({shape['input_name']})"
        ),
    ]
    return "\n\n".join(section for section in sections if section).rstrip() + "\n", binding_evidence


def render_runtime(contracts: dict[str, Any]) -> str:
    """Return the shared Lunar runtime adapter source.

    The execute function intentionally contains the direct ``execute_prism`` call so
    the converter validator can prove there is no native shortcut around reasoning.
    """
    template = r'''"""Lunar hooks for all source-grounded Abducer PRISM workflows.

Preparation validates the exact closed contract and preserves the UI value. Execution
always traverses the packaged PRISM graph with the host reasoning callback. Verification
requires complete source occurrence coverage and renders runtime validity separately
from any scientific disposition contained in the generated result.
"""
from __future__ import annotations

import html
import hashlib
import json
from pathlib import Path
import re
from types import SimpleNamespace


def _encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


CONTRACTS = json.loads(__ABDUCER_CONTRACTS__)

DISCOVERY_REPORT_SECTIONS = (
    ("overview", "Summary"),
    ("physics_math_strategy", "Mathematical Strategy"),
    ("timeline", "Timeline"),
    ("ranked_queue", "Ranked Analyses"),
    ("skills", "Skill Use"),
    ("contributions", "Contributions"),
    ("result_atlas", "Result Atlas"),
    ("literature", "Problem & Literature"),
    ("macro_strategy", "Macro Strategies"),
    ("strategy_judge", "Strategy Judge"),
    ("artifact_or_stop", "Artifact-Or-Stop"),
    ("story", "Story"),
    ("branches", "Branches"),
    ("reviews", "Deep Reviews"),
)

DISCOVERY_STEP_FIELDS = {
    "search_scope": "bounded_scope",
    "discovery_hypothesis": "hypothesis",
    "discovery_pattern": "provisional_pattern",
    "model_implications": "bounded_model_implications",
    "contrast_assessment": "controlled_contrast",
    "refutation_assessment": "scoped_refutation",
    "routing_assessment": "routing_basis",
    "typed_report": "prism.reporting.report.Report",
}

DISCOVERY_SKILL_BINDINGS = (
    ("search_scope", "epistemic-status-ledger"),
    ("discovery_hypothesis", "kb-abduce"),
    ("discovery_pattern", "kb-induce"),
    ("model_implications", "dynamic-symbolic-simulation-experimenter"),
    ("contrast_assessment", "counterfactual-route-prober"),
    ("refutation_assessment", "counterexample-hunter"),
    ("routing_assessment", "epistemic-status-ledger"),
)


def _contracts():
    return CONTRACTS


def _validate(value, schema, path="input"):
    kind = schema.get("type")
    if kind == "object":
        if not isinstance(value, dict):
            raise ValueError(path + " must be an object")
        expected = set(schema.get("properties", {}))
        if set(value) != expected:
            raise ValueError(path + " fields must be exactly: " + ", ".join(sorted(expected)))
        for name, child in schema.get("properties", {}).items():
            _validate(value[name], child, path + "." + name)
    elif kind == "string":
        if not isinstance(value, str) or not value.strip():
            raise ValueError(path + " must be a nonblank string")
        if len(value) > schema.get("maxLength", 16000):
            raise ValueError(path + " exceeds its maximum length")
        if "enum" in schema and value not in schema["enum"]:
            raise ValueError(path + " is outside the declared alternatives")
    elif kind == "array":
        if not isinstance(value, list) or len(value) < schema.get("minItems", 0):
            raise ValueError(path + " must be a nonempty array")
        for index, item in enumerate(value):
            _validate(item, schema["items"], path + "[" + str(index) + "]")
    elif kind == "integer":
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError(path + " must be an integer")
    elif kind == "number":
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError(path + " must be a number")
    elif kind == "boolean":
        if not isinstance(value, bool):
            raise ValueError(path + " must be a boolean")
    elif "anyOf" in schema:
        if value is None:
            return
        _validate(value, schema["anyOf"][1], path)
    else:
        raise ValueError(path + " uses an unsupported schema type")


def prepare(*, workflow_id, inputs, run_root, network_authority, **unused):
    """Validate one exact input record and retain a content-addressed run state."""
    contracts = _contracts()
    if workflow_id not in contracts:
        raise ValueError("Unknown Abducer workflow: " + workflow_id)
    if network_authority:
        raise ValueError("Abducer repository workflows do not request network authority")
    contract = contracts[workflow_id]
    _validate(inputs, contract["schema"])
    digest = hashlib.sha256(_encoded(inputs).encode("utf-8")).hexdigest()
    prepared = {
        "entry_argument_name": contract["argument"],
        "value": inputs,
        "request_digest": digest,
        "analysis_results": {
            "execution_scope": "source-grounded-model-reasoning",
            "scientific_truth_verified": False,
        },
    }
    return {
        "prepared_input": prepared,
        "state": {
            "workflow_id": workflow_id,
            "inputs": inputs,
            "prepared": prepared,
            "contract": contract,
            "run_root": str(run_root),
        },
        "events": [{"kind": "input", "payload": {
            "input_key": "inputs",
            "kind": "inline-json",
            "safe_locator": "run-input:" + workflow_id,
            "content_digest": "sha256:" + digest,
            "metadata": {"workflow_id": workflow_id, "status": "validated"},
        }}],
    }


def _plain_value(value):
    while hasattr(value, "value"):
        value = value.value
    if hasattr(value, "fields"):
        value = value.fields
    return json.loads(json.dumps(value, default=_encoded_result, ensure_ascii=False, allow_nan=False))


def _plain_result(execution):
    return _plain_value(execution.typed_result)


def _encoded_result(value):
    if hasattr(value, "fields"):
        if value.fields:
            return value.fields
        return value.type_name.rsplit(".", 1)[-1]
    if hasattr(value, "value"):
        return value.value
    raise TypeError("unsupported PRISM result value")


def _trace_step_results(execution, expected):
    """Recover each accepted occurrence output from the real PRISM trace."""
    results = {}
    for event in execution.trace:
        outcome = getattr(event, "outcome", None)
        name = getattr(event, "name", None)
        if (
            getattr(event, "kind", None) != "workflow-node"
            or name not in expected
            or outcome is None
            or outcome.execution != "completed"
            or outcome.contract != "satisfied"
        ):
            continue
        metadata = getattr(event, "metadata", {})
        if "result" not in metadata:
            raise ValueError("Completed reasoning occurrence omitted its typed result")
        value = _plain_value(metadata["result"])
        if name in results and results[name] != value:
            raise ValueError("A reasoning occurrence emitted conflicting typed results")
        results[name] = value
    if set(results) != set(expected):
        raise ValueError("Typed results are missing for a declared reasoning occurrence")
    return results


def _emit_agent_receipts(execution, contract, services):
    """Project native PRISM agent trace entries into Lunar worker stage receipts.

    Custom package hooks own this bridge.  Merely returning ``execution.trace`` from
    the hook does not persist it, so every expected invocation is checked against the
    native trace before a UI-visible receipt is emitted.
    """
    expected = contract["provenance_contract"]["agent_invocations"]
    agents = [event for event in execution.trace if event.kind == "agent-invoked"]
    effects = [event for event in execution.trace if event.kind == "effect"]
    if len(agents) != len(expected):
        raise ValueError("Native PRISM agent trace does not match the provenance contract")
    if len(effects) != len(agents):
        raise ValueError("Native PRISM agent trace has incomplete effect linkage")
    receipts = []
    for expected_row, agent, effect in zip(expected, agents, effects, strict=True):
        skills = list(agent.metadata.get("skills", ()))
        if agent.name != expected_row["agent_name"]:
            raise ValueError("Native PRISM agent trace changed invocation order or identity")
        if skills != expected_row["activated_skill_ids"]:
            raise ValueError("Native PRISM agent trace changed activated skill bindings")
        record_id = effect.metadata.get("record")
        record = execution.effect_records.get(record_id)
        if record is None:
            raise ValueError("Native PRISM agent trace references a missing effect record")
        detail = {
            "event_kind": "agent-invoked",
            "agent_name": agent.name,
            "workflow_occurrence": expected_row["workflow_occurrence"],
            "activated_skill_ids": skills,
            "selected_model": services.model.safe_snapshot,
            "effect_record_id": record_id,
            "input_digest": record.invocation.input_digest,
            "output_digest": record.observation.output_digest,
        }
        services.event("stage", {
            "stage_id": expected_row["workflow_occurrence"],
            "component_id": agent.name,
            "status": agent.status,
            "safe_summary": "Activated skills: " + ", ".join(skills),
            "detail": detail,
        })
        receipts.append(detail)
    return receipts


def execute(*, state, services):
    """Execute the complete PRISM graph and forward normalized reasoning events."""
    from prism_engine import execute_prism

    observed = []
    contract = state["contract"]
    expected_workflow = contract["reasoning_workflow"]
    material_workflow = contract["material_workflow"]

    def reasoning(**payload):
        step = payload.get("reasoning_step")
        if isinstance(step, dict) and step.get("workflow") in {
            material_workflow,
            "material_main." + material_workflow,
        }:
            payload = dict(payload)
            payload["reasoning_step"] = {**step, "workflow": expected_workflow}
        observed.append(payload)
        services.event("reasoning", payload)

    root = Path(state["run_root"])
    reasoning_root = root / "reasoning"
    reasoning_root.mkdir(exist_ok=False)
    prism_execution = execute_prism(
        source=Path("/package") / contract["entry_file"],
        entry_argument=contract["argument"],
        prepared_input=state["prepared"],
        selected_model=services.model,
        artifact_root=reasoning_root,
        completion=services.completion,
        on_reasoning=reasoning,
    )
    if prism_execution.status != "accepted" or prism_execution.diagnostics:
        raise ValueError("The complete Abducer PRISM graph did not finish cleanly")
    agent_receipts = _emit_agent_receipts(prism_execution, contract, services)
    transitions = {}
    for payload in observed:
        step = payload.get("reasoning_step")
        if not isinstance(step, dict) or step.get("workflow") != expected_workflow:
            continue
        name = step.get("name")
        status = payload.get("status")
        occurrence = str(payload.get("source_event_key", "")).rpartition(":")[0]
        if name and status in {"running", "completed"}:
            row = transitions.setdefault(occurrence, {"name": name, "statuses": []})
            if row["name"] != name:
                raise ValueError("A reasoning occurrence changed identity")
            row["statuses"].append(status)
    expected = contract["expected_steps"]
    if sorted(row["name"] for row in transitions.values()) != sorted(expected):
        raise ValueError("Reasoning completion is missing a declared source occurrence")
    if any(row["statuses"] != ["running", "completed"] for row in transitions.values()):
        raise ValueError("Reasoning occurrence transitions are incomplete")
    step_results = _trace_step_results(prism_execution, expected)
    # Discovery Marathon returns a genuine PRISM Report.  Its scientific routing
    # result remains the final reasoning occurrence, not the report container.
    result_value = (
        step_results["routing_assessment"]
        if state["workflow_id"] == "discovery_marathon_loop"
        else _plain_result(prism_execution)
    )
    for field, alternatives in contract.get("variant_constraints", {}).items():
        candidate = result_value if field == "__value__" else (
            result_value.get(field) if isinstance(result_value, dict) else None
        )
        if candidate not in alternatives:
            raise ValueError(
                "Generated result violates the closed source variant for "
                + ("value" if field == "__value__" else field)
            )
    return SimpleNamespace(
        prism_execution=prism_execution,
        reasoning_result=result_value,
        reasoning_event_count=len(observed),
        completed_steps=expected,
        transitions=transitions,
        step_results=step_results,
        agent_receipts=agent_receipts,
    )


def _markdown(workflow_id, value):
    final = value["final_disposition"]
    return (
        "# " + workflow_id.replace("_", " ").replace("-", " ").title() + "\n\n"
        "## Final disposition\n\n"
        "Runtime status: **" + final["status"] + "**\n\n"
        + final["summary"] + "\n\n"
        "## Completed reasoning steps\n\n"
        + "\n".join("- `" + step + "`" for step in final["completed_reasoning_steps"])
        + "\n\n## Typed reasoning result\n\n```json\n"
        + json.dumps(value["reasoning_result"], indent=2, ensure_ascii=False, allow_nan=False)
        + "\n```\n\n## Execution provenance\n\n```json\n"
        + json.dumps(value["execution_provenance"], indent=2, ensure_ascii=False, allow_nan=False)
        + "\n```\n\n## Interpretation and limits\n\n"
        + "\n".join("- " + item for item in final["limitations"])
        + "\n"
    )


def _digest_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _quote(value):
    text = str(value).strip()
    return "\n".join("> " + line if line else ">" for line in text.splitlines())


def _step_text(step_results, step):
    value = step_results[step]
    field = DISCOVERY_STEP_FIELDS[step]
    if not isinstance(value, dict) or field not in value:
        raise ValueError("Discovery report input is missing " + step + "." + field)
    text = value[field]
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Discovery report input contains an empty " + step + "." + field)
    return text.strip()


def _discovery_sections(state, execution, structured):
    """Map live typed results into the repository's fourteen report surfaces."""
    steps = execution.step_results
    context = state["inputs"]["context_summary"].strip()
    scope = _step_text(steps, "search_scope")
    hypothesis = _step_text(steps, "discovery_hypothesis")
    pattern = _step_text(steps, "discovery_pattern")
    implications = _step_text(steps, "model_implications")
    contrast = _step_text(steps, "contrast_assessment")
    refutation = _step_text(steps, "refutation_assessment")
    routing = _step_text(steps, "routing_assessment")
    disposition = structured["reasoning_result"]["disposition"]
    final = structured["final_disposition"]
    provenance = structured["execution_provenance"]
    completed = "\n".join("- `" + step + "`" for step in final["completed_reasoning_steps"])
    limits = "\n".join("- " + item for item in final["limitations"])
    step_rows = "\n".join(
        "| " + str(index) + " | `" + step + "` | completed | `" + DISCOVERY_STEP_FIELDS[step] + "` |"
        for index, step in enumerate(final["completed_reasoning_steps"], start=1)
    )
    skill_rows = "\n".join(
        "| `" + step + "` | `" + skill + "` | model-generated typed result |"
        for step, skill in DISCOVERY_SKILL_BINDINGS
    )
    atlas = json.dumps(steps, indent=2, ensure_ascii=False, allow_nan=False, sort_keys=True)
    typed = json.dumps(structured["reasoning_result"], indent=2, ensure_ascii=False, allow_nan=False, sort_keys=True)
    evidence = json.dumps(provenance, indent=2, ensure_ascii=False, allow_nan=False, sort_keys=True)
    artifact_action = {
        "Promotable": "Promote the candidate to source validation and proof-obligation discharge.",
        "Reorient": "Return the candidate to conceptual reorientation before promotion.",
        "TargetReset": "Reset the target boundary before another discovery cycle.",
        "Stalled": "Stop and record the unresolved blocker before spending another cycle.",
    }[disposition]
    bodies = {
        "overview": (
            "This report projects one complete live PRISM Discovery Marathon run into the "
            "same fourteen-section information architecture used by the repository report.\n\n"
            "### Run scope\n\n" + _quote(context) + "\n\n"
            "## Final disposition\n\nRuntime status: **" + final["status"] + "**  \n"
            "Discovery disposition: **" + disposition + "**\n\n" + final["summary"] + "\n\n"
            "## Completed reasoning steps\n\n" + completed + "\n\n"
            "## Typed reasoning result\n\n```json\n" + typed + "\n```\n\n"
            "## Execution provenance\n\n```json\n" + evidence + "\n```\n\n"
            "## Interpretation and limits\n\n" + limits
        ),
        "physics_math_strategy": (
            "### Bounded scope\n\n" + _quote(scope) + "\n\n"
            "### Candidate hypothesis\n\n" + _quote(hypothesis) + "\n\n"
            "### Provisional pattern\n\n" + _quote(pattern) + "\n\n"
            "### Bounded model implications\n\n" + _quote(implications)
        ),
        "timeline": (
            "The ordered runtime trace completed every declared reasoning occurrence. "
            "Parallel declarations retain their PRISM semantics; this table records their released order.\n\n"
            "| # | Reasoning stage | Runtime status | Typed evidence field |\n"
            "| ---: | --- | --- | --- |\n" + step_rows
        ),
        "ranked_queue": (
            "1. **Validate sources and exact theorem hypotheses.** " + routing + "\n"
            "2. **Discharge the strongest refutation pressure.** " + refutation + "\n"
            "3. **Test the controlled contrast.** " + contrast + "\n"
            "4. **Check the bounded implications.** " + implications
        ),
        "skills": (
            "These packaged skills were bound to the seven executed occurrences. Skill use "
            "supports generation and critique; it is not independent scientific verification.\n\n"
            "| Reasoning stage | Packaged skill | Evidence class |\n"
            "| --- | --- | --- |\n" + skill_rows
        ),
        "contributions": (
            "- Preserved the user-supplied problem boundary through all seven typed stages.\n"
            "- Produced separate abductive and inductive formation records.\n"
            "- Produced separate model-based and contrastive probes before refutation.\n"
            "- Retained a closed routing disposition with explicit limitations.\n"
            "- Scientific novelty remains **not claimed**; all substantive content is model-generated."
        ),
        "result_atlas": (
            "The atlas preserves the complete typed output of every reasoning occurrence.\n\n"
            "```json\n" + atlas + "\n```"
        ),
        "literature": (
            "### Problem statement\n\n" + _quote(context) + "\n\n"
            "### Literature status\n\n"
            "This workflow requested no public-network authority and performed no live literature "
            "acquisition. Any titles or references mentioned by model outputs are leads requiring "
            "source retrieval, identity checks, and exact-locator validation before use as evidence."
        ),
        "macro_strategy": (
            "### Formation route\n\n" + _quote(hypothesis) + "\n\n"
            "### Pattern route\n\n" + _quote(pattern) + "\n\n"
            "### Model-pressure route\n\n" + _quote(implications)
        ),
        "strategy_judge": (
            "### Controlled contrast\n\n" + _quote(contrast) + "\n\n"
            "### Refutation assessment\n\n" + _quote(refutation) + "\n\n"
            "### Routing judgment\n\n**" + disposition + "**\n\n" + _quote(routing)
        ),
        "artifact_or_stop": (
            "**Decision:** " + disposition + "\n\n" + artifact_action + "\n\n"
            "Released artifacts: `report.md`, `result.json`, `latest.md`, `latest.json`, "
            "`latest.html`, and `full_timeline.html`. A passed runtime is not a proof certificate."
        ),
        "story": (
            "The run began by bounding the search:\n\n" + _quote(scope) + "\n\n"
            "It then formed a hypothesis and a pattern:\n\n" + _quote(hypothesis) + "\n\n"
            + _quote(pattern) + "\n\n"
            "The two probe lanes supplied implications and contrast pressure, which were merged "
            "by the refutation stage before the final routing judgment:\n\n" + _quote(routing)
        ),
        "branches": (
            "### Formation branch · abductive\n\n" + _quote(hypothesis) + "\n\n"
            "### Formation branch · inductive\n\n" + _quote(pattern) + "\n\n"
            "### Probe branch · model implications\n\n" + _quote(implications) + "\n\n"
            "### Probe branch · controlled contrast\n\n" + _quote(contrast) + "\n\n"
            "### Merge · refutation\n\n" + _quote(refutation)
        ),
        "reviews": (
            "### Epistemology\n\nThe run separates generated hypotheses, probes, refutation, and routing. "
            "No generated statement is promoted to established fact by runtime success.\n\n"
            "### Mathematics\n\nThe mathematical content remains conditional until its hypotheses, proof steps, "
            "counterexamples, and cited sources are independently checked.\n\n"
            "### AI research\n\nThe seven typed calls completed under a closed schema. One successful run does not "
            "measure stability, calibration, or cross-model agreement.\n\n"
            "### Software engineering\n\nThe PRISM graph, ordered reasoning events, source/module hashes, report layout, and "
            "artifact digests are retained for replay and inspection."
        ),
    }
    return [(slug, label, bodies[slug]) for slug, label in DISCOVERY_REPORT_SECTIONS]


def _assemble_native_report(sections):
    chunks = []
    blocks = []
    groups = []
    cursor = 0

    def add(text, kind, group_keys):
        nonlocal cursor
        value = text.strip() + "\n\n"
        block = {
            "id": "block-" + str(len(blocks) + 1),
            "kind": kind,
            "start": cursor,
            "end": cursor + len(value),
            "group_keys": group_keys,
            "source_text_sha256": _digest_text(" ".join(value.split())),
        }
        if kind == "heading":
            block["heading_key"] = block["id"]
        blocks.append(block)
        chunks.append(value)
        cursor += len(value)

    add("# Discovery Marathon Report", "heading", [])
    add(
        "Live PRISM execution report with repository-compatible Discovery Marathon sections.",
        "prose",
        [],
    )
    for index, (slug, label, body) in enumerate(sections, start=1):
        key = "tab-" + slug
        groups.append({"key": key, "kind": "tab", "label": label})
        add("## " + label, "heading", [key])
        for paragraph in body.strip().split("\n\n"):
            kind = "heading" if re.fullmatch(r"#{1,6} .+", paragraph.strip()) else "prose"
            add(paragraph, kind, [key])
    markdown = "".join(chunks)
    layout = {
        "schema_version": "lunar.native-report/v1",
        "groups": groups,
        "blocks": blocks,
        "content_sha256": _digest_text(markdown),
    }
    layout["metadata_sha256"] = _digest_text(
        json.dumps(layout, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    )
    return markdown, layout


def _markdown_fragment_html(value):
    rendered = []
    for paragraph in value.strip().split("\n\n"):
        lines = paragraph.splitlines()
        if len(lines) == 1 and re.fullmatch(r"#{1,6} .+", lines[0]):
            marker, title = lines[0].split(" ", 1)
            level = min(6, len(marker) + 1)
            rendered.append("<h" + str(level) + ">" + html.escape(title) + "</h" + str(level) + ">")
        elif lines and lines[0].startswith("```") and lines[-1] == "```":
            rendered.append("<pre><code>" + html.escape("\n".join(lines[1:-1])) + "</code></pre>")
        elif lines and all(line.startswith("- ") for line in lines):
            rendered.append("<ul>" + "".join("<li>" + html.escape(line[2:]) + "</li>" for line in lines) + "</ul>")
        elif lines and all(re.match(r"^\d+\. ", line) for line in lines):
            rendered.append("<ol>" + "".join("<li>" + html.escape(line.split(". ", 1)[1]) + "</li>" for line in lines) + "</ol>")
        elif lines and all(line.startswith(">") for line in lines):
            rendered.append("<blockquote>" + "<br>".join(html.escape(line[1:].lstrip()) for line in lines) + "</blockquote>")
        elif lines and lines[0].startswith("|"):
            rendered.append("<pre class=\"table\">" + html.escape(paragraph) + "</pre>")
        else:
            rendered.append("<p>" + "<br>".join(html.escape(line) for line in lines) + "</p>")
    return "".join(rendered)


def _discovery_html(sections, active_slug):
    buttons = []
    panels = []
    for slug, label, body in sections:
        active = slug == active_slug
        buttons.append(
            '<button class="tab' + (" active" if active else "") + '" data-tab="'
            + slug + '" aria-selected="' + ("true" if active else "false") + '">'
            + html.escape(label) + "</button>"
        )
        panels.append(
            '<section class="panel' + (" active" if active else "") + '" data-panel="'
            + slug + '"><h2>' + html.escape(label) + "</h2>"
            + _markdown_fragment_html(body) + "</section>"
        )
    return (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        "<title>Discovery Marathon Report</title><style>"
        ":root{color-scheme:light dark;font-family:Inter,system-ui,sans-serif}body{margin:0;background:#10141d;color:#edf2f7}"
        "header,main{max-width:1180px;margin:auto;padding:24px}nav{display:flex;gap:8px;overflow:auto;padding:0 24px 16px}"
        ".tab{border:1px solid #526071;background:#202938;color:inherit;border-radius:999px;padding:8px 13px;white-space:nowrap}"
        ".tab.active{background:#2563eb;border-color:#60a5fa}.panel{display:none;background:#171e2a;border:1px solid #384457;border-radius:14px;padding:22px}"
        ".panel.active{display:block}blockquote,pre{white-space:pre-wrap;background:#0d121a;border-left:3px solid #60a5fa;padding:12px;overflow:auto}"
        "h1,h2,h3{color:#f8fafc}p,li{line-height:1.55}.table{font-size:.9rem}</style></head><body>"
        "<header><h1>Discovery Marathon Report</h1><p>Live typed PRISM execution · repository-compatible report contract</p></header>"
        "<nav aria-label=\"Report sections\">" + "".join(buttons) + "</nav><main>" + "".join(panels) + "</main>"
        "<script>document.querySelectorAll('.tab').forEach(function(button){button.addEventListener('click',function(){"
        "document.querySelectorAll('.tab').forEach(function(item){item.classList.remove('active');item.setAttribute('aria-selected','false')});"
        "document.querySelectorAll('.panel').forEach(function(item){item.classList.remove('active')});button.classList.add('active');"
        "button.setAttribute('aria-selected','true');document.querySelector('[data-panel=\"'+button.dataset.tab+'\"]').classList.add('active')})});</script>"
        "</body></html>\n"
    )


def _validate_discovery_report(markdown, layout, latest_html, timeline_html):
    labels = [label for unused, label in DISCOVERY_REPORT_SECTIONS]
    if [group["label"] for group in layout["groups"]] != labels:
        raise ValueError("Discovery report layout omitted a required native section")
    if layout["content_sha256"] != _digest_text(markdown):
        raise ValueError("Discovery report layout content digest is invalid")
    metadata = {key: value for key, value in layout.items() if key != "metadata_sha256"}
    if layout["metadata_sha256"] != _digest_text(
        json.dumps(metadata, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    ):
        raise ValueError("Discovery report layout metadata digest is invalid")
    required = [
        "## " + label for label in labels
    ] + [
        "## Final disposition",
        "## Completed reasoning steps",
        "## Typed reasoning result",
        "## Execution provenance",
        "## Interpretation and limits",
    ]
    missing = [heading for heading in required if heading not in markdown]
    if missing:
        raise ValueError("Discovery report is missing required headings: " + ", ".join(missing))
    for document in (latest_html, timeline_html):
        if document.count('<button class="tab') != len(labels) or document.count('<section class="panel') != len(labels):
            raise ValueError("Discovery HTML report omitted a required tab or panel")


def _validate_typed_discovery_report(typed_report):
    """Require the PRISM Report value to carry the compatible fourteen-tab surface."""
    labels = [label for unused, label in DISCOVERY_REPORT_SECTIONS]
    if typed_report.get("version") != "1":
        raise ValueError("Discovery PRISM Report uses an unsupported codec version")
    report = typed_report.get("report")
    if not isinstance(report, dict) or report.get("id") != "discovery-marathon-report":
        raise ValueError("Discovery PRISM Report identity is invalid")
    sections = report.get("sections")
    if not isinstance(sections, list) or len(sections) != 1:
        raise ValueError("Discovery PRISM Report must contain one typed tab group")
    tab_group = sections[0]
    if tab_group.get("kind") != "tabs" or tab_group.get("id") != "discovery-sections":
        raise ValueError("Discovery PRISM Report omitted its typed tab group")
    tabs = tab_group.get("tabs")
    if not isinstance(tabs, list) or [tab.get("label") for tab in tabs] != labels:
        raise ValueError("Discovery PRISM Report omitted a required compatible tab")
    for (slug, unused), tab in zip(DISCOVERY_REPORT_SECTIONS, tabs):
        content = tab.get("sections")
        if (
            tab.get("id") != slug
            or not isinstance(content, list)
            or len(content) != 1
            or content[0].get("kind") != "markdown"
            or content[0].get("id") != slug + "-content"
            or not str(content[0].get("text", "")).strip()
        ):
            raise ValueError("Discovery PRISM Report contains an invalid typed tab: " + slug)
    template = report.get("template")
    template_sections = template.get("sections") if isinstance(template, dict) else None
    if (
        not isinstance(template_sections, list)
        or len(template_sections) != 1
        or template_sections[0].get("kind") != "tabs"
        or [tab.get("id") for tab in template_sections[0].get("tabs", [])]
        != [slug for slug, unused in DISCOVERY_REPORT_SECTIONS]
    ):
        raise ValueError("Discovery PRISM Report template is incompatible")


def verify(*, state, execution, **unused):
    """Reject incomplete reasoning and render a runtime-only passing disposition."""
    expected = state["contract"]["expected_steps"]
    if execution.prism_execution.status != "accepted":
        raise ValueError("PRISM execution was not accepted")
    if execution.completed_steps != expected or execution.reasoning_event_count < len(expected) * 2:
        raise ValueError("Reasoning completion evidence is incomplete")
    result_value = execution.reasoning_result
    if not isinstance(result_value, dict):
        result_value = {"value": result_value}
    provenance = {
        "request_digest": state["prepared"]["request_digest"],
        "source_hash": execution.prism_execution.source_hash,
        "module_hashes": dict(execution.prism_execution.module_hashes),
        "reasoning_event_count": execution.reasoning_event_count,
        "agent_invocations": execution.agent_receipts,
    }
    final = {
        "status": "passed",
        "summary": (
            "The complete declared PRISM reasoning graph ran to acceptance and its "
            "typed generated result was retained."
        ),
        "reasoning_complete": True,
        "blockers": [],
        "completed_reasoning_steps": expected,
        "limitations": [
            "Runtime completion does not prove a theorem or validate a scientific claim.",
            "No native theorem prover, experiment, source validator, or release backend was executed.",
            "Any domain disposition inside the typed result remains model-generated and must be reviewed on its own evidence.",
        ],
    }
    structured = {
        "final_disposition": final,
        "reasoning_result": result_value,
        "execution_provenance": provenance,
    }
    root = Path(state["run_root"])
    report_checks = [
        "complete_reasoning_trace",
        "typed_prism_result",
        "deterministic_report_projection",
    ]
    if state["workflow_id"] == "discovery_marathon_loop":
        from dataclasses import replace
        from prism_stdlib.report_codec import decode_report, export_report

        report_output = execution.prism_execution.run_output
        report_value = report_output.result
        report_provenance = report_output.provenance
        references = {
            item.identity: item for item in report_provenance.values
        } if report_provenance is not None else {}
        report_reference = report_provenance.result if report_provenance is not None else None
        # The effectful entrypoint returns Result[Report, ModelFailure].  The report
        # codec requires the accepted inner named Report and its matching native graph
        # root. Select the already-recorded ``value`` child without synthesizing or
        # deleting any provenance values, activities, trace entries, or effects.
        while not hasattr(report_value, "fields") and hasattr(report_value, "value"):
            report_value = report_value.value
            parent = references.get(report_reference)
            report_reference = dict(parent.children).get("value") if parent else None
        if not hasattr(report_value, "fields"):
            raise ValueError("Discovery workflow did not return a named PRISM Report")
        if report_provenance is None or report_reference not in references:
            raise ValueError("Discovery PRISM Report has no native provenance reference")
        typed_report = export_report(replace(
            report_output,
            result=report_value,
            provenance=replace(report_provenance, result=report_reference),
        ))
        decode_report(typed_report, attachments={})
        _validate_typed_discovery_report(typed_report)
        sections = _discovery_sections(state, execution, structured)
        markdown, layout = _assemble_native_report(sections)
        latest_html = _discovery_html(sections, "overview")
        timeline_html = _discovery_html(sections, "timeline")
        _validate_discovery_report(markdown, layout, latest_html, timeline_html)
        report_artifacts = [
            "report.md",
            "result.json",
            "latest.md",
            "latest.json",
            "latest.html",
            "full_timeline.html",
        ]
        structured.update(
            {
                "report_layout": layout,
                "typed_report": typed_report,
                "report_contract": {
                    "schema_version": "abducer.discovery-marathon-report/v1",
                    "presentation": "prism-typed-report/v1",
                    "terminal_output_type": "prism.reporting.report.Report",
                    "compatibility": "repository-section-compatible",
                    "required_sections": [label for unused, label in DISCOVERY_REPORT_SECTIONS],
                    "artifacts": report_artifacts,
                    "typed_report_artifact": "typed-report.json",
                },
                "discovery_report": {
                    "context_summary": state["inputs"]["context_summary"],
                    "stages": execution.step_results,
                    "routing": result_value,
                },
            }
        )
        payload = json.dumps(structured, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"
        (root / "latest.md").write_text(markdown, encoding="utf-8")
        (root / "latest.json").write_text(payload, encoding="utf-8")
        (root / "latest.html").write_text(latest_html, encoding="utf-8")
        (root / "full_timeline.html").write_text(timeline_html, encoding="utf-8")
        (root / "typed-report.json").write_text(
            json.dumps(typed_report, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n",
            encoding="utf-8",
        )
        report_checks.extend(
            [
                "repository_compatible_sections",
                "prism_typed_report",
                "native_report_layout",
                "self_contained_html_reports",
            ]
        )
    else:
        markdown = _markdown(state["workflow_id"], structured)
    (root / "report.md").write_text(markdown, encoding="utf-8")
    (root / "result.json").write_text(
        json.dumps(structured, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    return {
        "result": {
            "markdown": markdown,
            "structured_value": structured,
            "analysis_results": {
                "execution_scope": "source-grounded-model-reasoning",
                "reasoning_complete": True,
                "scientific_truth_verified": False,
                "report_compatibility": (
                    "abducer.discovery-marathon-report/v1"
                    if state["workflow_id"] == "discovery_marathon_loop"
                    else "generic-runtime-report/v1"
                ),
                "report_type": (
                    "prism.reporting.report.Report"
                    if state["workflow_id"] == "discovery_marathon_loop"
                    else "runtime-markdown"
                ),
            },
            "compact_prism_input": state["inputs"],
            "narrative_slots": [],
            "report_verification": {
                "status": "passed",
                "reasoning_complete": True,
                "repository_report_compatible": state["workflow_id"] == "discovery_marathon_loop",
                "checks": report_checks,
            },
        },
        "events": [{"kind": "artifact", "payload": {
            "workflow_id": state["workflow_id"],
            "status": "rendered",
        }}],
    }
'''
    return template.replace("__ABDUCER_CONTRACTS__", repr(canonical_json(contracts)))


def source_fingerprint(paths: list[Path]) -> dict[str, Any]:
    """Fingerprint every declared conversion input in stable path order."""
    rows = []
    for path in sorted(set(paths), key=lambda item: item.relative_to(ROOT).as_posix()):
        if path.is_file():
            rows.append(
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "sha256": digest_file(path),
                    "size": path.stat().st_size,
                }
            )
    return {
        "schema_version": 1,
        "source_revision": source_revision(),
        "files": rows,
        "aggregate_sha256": digest_bytes(canonical_json(rows).encode("utf-8")),
    }


def build() -> dict[str, Any]:
    """Generate the conversion tree and root exporter configuration."""
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    ledger_by_workflow = {
        row["id"]: {item["binding_alias"]: item["skill_path"] for item in row.get("bindings", [])}
        for row in ledger["workflows"]
    }
    skills, skill_ids = discover_skills()
    if len(manifest["workflows"]) != 19 or len(skills) != 359:
        raise ValueError("canonical inventory count changed; review before regenerating")

    workflow_rows = []
    workflow_catalog = []
    runtime_contracts = {}
    fingerprint_paths = [MANIFEST_PATH, LEDGER_PATH]
    for row in sorted(manifest["workflows"], key=lambda item: item["id"]):
        workflow_id = row["id"]
        module_id = row.get("module_id", workflow_id)
        source_root = ROOT / "abducer-prism/workflows" / module_id
        texts = {name: (source_root / f"{name}.prism").read_text(encoding="utf-8") for name in ("types", "occurrences", "relations", "reasoning")}
        fingerprint_paths.extend(source_root / f"{name}.prism" for name in texts)
        source_workflow = ROOT / row["source_workflow"]["path"]
        fingerprint_paths.append(source_workflow)
        shape = workflow_shape(texts["reasoning"], texts["occurrences"])
        project = OUTPUT / "projects" / workflow_id
        prism_project = project / "prism_project"
        for name, content in texts.items():
            localized = localize_imports(content, module_id)
            if name == "reasoning":
                localized = render_reasoning_view(workflow_id, localized)
            write(prism_project / f"{name}.prism", localized)
        material, execution_bindings = render_material_main(
            row,
            shape,
            texts["types"],
            texts["occurrences"],
            ledger_by_workflow.get(workflow_id, {}),
        )
        write(prism_project / "material_main.prism", material)
        schema = schema_for_type(shape["input_type"], parse_types(texts["types"]), EXAMPLE_INPUTS[workflow_id])
        entry_file = f"repository/projects/{workflow_id}/prism_project/material_main.prism"
        runtime_contracts[workflow_id] = {
            "argument": shape["input_name"],
            "entry_file": entry_file,
            "expected_steps": [
                *[item["alias"] for item in shape["calls"]],
                *(["typed_report"] if workflow_id == "discovery_marathon_loop" else []),
            ],
            "material_workflow": "Materialized" + shape["reasoning"],
            "reasoning_workflow": shape["reasoning"],
            "schema": schema,
            "variant_constraints": variant_constraints(
                shape["output_type"],
                {**parse_types(texts["types"]), **parse_types(texts["occurrences"])},
            ),
            "provenance_contract": {
                "agent_invocations": agent_invocation_contract(execution_bindings),
                "required_source_reads": [],
            },
        }
        declared_skill_paths = sorted({item["path"] for item in row.get("skill_bindings", [])})
        execution_skill_paths = sorted({item["skill_path"] for item in execution_bindings})
        all_skill_paths = sorted(set(declared_skill_paths) | set(execution_skill_paths))
        missing_skills = [path for path in all_skill_paths if path not in skill_ids]
        if missing_skills:
            raise ValueError(f"{workflow_id} references undiscovered skills: {missing_skills}")
        evidence = {
            "schema_version": 1,
            "workflow_id": workflow_id,
            "module_id": module_id,
            "source_workflow": {
                "path": source_workflow.relative_to(ROOT).as_posix(),
                "sha256": digest_file(source_workflow),
            },
            "reviewed_projection": {
                name: {
                    "path": (source_root / f"{name}.prism").relative_to(ROOT).as_posix(),
                    "sha256": digest_file(source_root / f"{name}.prism"),
                }
                for name in sorted(texts)
            },
            "source_materialization": row.get("materialization", {}),
            "declared_skill_paths": declared_skill_paths,
            "execution_skill_bindings": execution_bindings,
            "behavioral_equivalence_claimed": False,
        }
        architecture = {
            "schema_version": 1,
            "workflow_id": workflow_id,
            "reasoning": shape["reasoning"],
            "input": {"name": shape["input_name"], "type": shape["input_type"]},
            "output_type": shape["output_type"],
            "occurrences": shape["calls"],
            "materialization": "model-backed-agents-with-repository-skill-artifacts",
            "claim_ceiling": "runtime and reasoning completion; no scientific truth verification",
        }
        reasoning_steps = [item["alias"] for item in shape["calls"]]
        if workflow_id == "discovery_marathon_loop":
            reasoning_steps.append("typed_report")
        hook_coverage = {
            "schema_version": 1,
            "workflow_id": workflow_id,
            "prepare": "abducer-workflow-prepare",
            "execute": "abducer-workflow-execute",
            "verify": "abducer-workflow-verify",
            "reasoning_steps": reasoning_steps,
            "complete": True,
        }
        generation = {
            "schema_version": 1,
            "generator": "abducer-repository-prism/scripts/build_conversion.py",
            "workflow_id": workflow_id,
            "source_revision": source_revision(),
            "generated_files": sorted(
                path.relative_to(project).as_posix()
                for path in project.rglob("*")
                if path.is_file()
            ),
        }
        for name, value in (
            ("source-evidence.json", evidence),
            ("workflow-architecture-plan.json", architecture),
            ("hook-coverage.json", hook_coverage),
            ("generation.json", generation),
        ):
            write(project / "conversion" / name, canonical_json(value))
        workflow_rows.append(
            {
                "id": workflow_id,
                "name": shape["reasoning"],
                "root": project.relative_to(ROOT).as_posix(),
                "entrypoint": "prism_project/material_main.prism",
                "reasoning_entrypoint": "prism_project/reasoning.prism",
                "description": row["function"],
                "public_output_type": (
                    "prism.reporting.report.Report"
                    if workflow_id == "discovery_marathon_loop"
                    else shape["output_type"]
                ),
                "semantic_mode": "operational-model-generated",
                "skill_ids": [skill_ids[path] for path in all_skill_paths],
                "metadata": {
                    "source_workflow": row["source_workflow"]["path"],
                    "source_materialization_status": row.get("materialization", {}).get("status"),
                    "behavioral_equivalence_claimed": False,
                },
            }
        )
        workflow_catalog.append(
            {
                "id": workflow_id,
                "module_id": module_id,
                "function": row["function"],
                "disposition": "converted",
                "reasoning": shape["reasoning"],
                "input_type": shape["input_type"],
                "output_type": shape["output_type"],
                "steps": reasoning_steps,
                "declared_skill_count": len(declared_skill_paths),
                "execution_skill_count": len(execution_skill_paths),
            }
        )

    data_sources = []
    for kb in sorted((ROOT / "KB").glob("*.kb.md")):
        key = kb.name.removesuffix(".kb.md")
        paths = [kb.relative_to(ROOT).as_posix()]
        companion = ROOT / "InformalMathLib" / key
        if companion.is_dir():
            paths.append(companion.relative_to(ROOT).as_posix())
            fingerprint_paths.extend(path for path in companion.rglob("*") if path.is_file())
        fingerprint_paths.append(kb)
        data_sources.append(
            {
                "id": "kb-" + key,
                "name": key.replace("-", " ").title(),
                "paths": paths,
                "prefix": "kb/" + key,
                "descriptor": {
                    "kind": "mathematical-knowledge-base",
                    "trust": "authored-source",
                    "claim_ceiling": "packaged research state; no new mathematical verification",
                },
                "remote_references": [],
                "exclude": ["**/.DS_Store", "**/__pycache__/**", "**/*.pyc"],
            }
        )
    if len(data_sources) != 7:
        raise ValueError("canonical KB count changed; review before regenerating")

    for skill in skills:
        fingerprint_paths.extend(path for path in (ROOT / skill["root"]).rglob("*") if path.is_file())
    fingerprint = source_fingerprint(fingerprint_paths)
    write(OUTPUT / "conversion/source-fingerprint.json", canonical_json(fingerprint))
    write(
        OUTPUT / "conversion/generation.json",
        canonical_json(
            {
                "schema_version": 1,
                "generator": "abducer-repository-prism/scripts/build_conversion.py",
                "source_revision": source_revision(),
                "counts": {
                    "workflows": len(workflow_rows),
                    "skills": len(skills),
                    "data_sources": len(data_sources),
                },
                "source_fingerprint_sha256": digest_file(OUTPUT / "conversion/source-fingerprint.json"),
            }
        ),
    )
    write(OUTPUT / "workflow_catalog.json", canonical_json({"schema_version": 1, "workflows": workflow_catalog}))
    write(
        OUTPUT / "skill_dispositions.json",
        canonical_json(
            {
                "schema_version": 1,
                "skills": [
                    {"id": row["id"], "source_root": row["root"], "disposition": "converted"}
                    for row in skills
                ],
            }
        ),
    )
    write(OUTPUT / "runtime/workflow-inputs.json", canonical_json(runtime_contracts))
    write(OUTPUT / "runtime/abducer_lunar_runtime.py", render_runtime(runtime_contracts))

    readme = """# Abducer Repository PRISM Conversion

This tree is the deterministic conversion source for one Lunar package containing all
19 canonical Abducer reasoning workflows, all 359 skill trees, and all seven KB-backed
data sources. Each project keeps its source reasoning topology visible and provides a
separate `material_main.prism` whose occurrences execute as typed model-backed agents.

## Build and validate

Run the converter's `export_repository_prism.py` with repository root `.` and config
`prism-export.json`, passing the local Lunar checkout and `--verify-reproducible`.
Then run both the converter validator and `abducer-prism/validate_imported_prism_packages.py`
unchanged. Offline validity is necessary but not sufficient: import the archive through
Lunar, prepare its runtime, and validate one completed UI run per workflow.

## Interpreting results

A report-level final status of `passed` means the complete typed PRISM graph executed,
all declared occurrence transitions were recorded, and the result was rendered. It does
not mean a theorem was proved, an experiment ran, or a scientific claim was promoted.
The source-domain disposition inside `reasoning_result` may therefore be cautious or
negative while runtime verification correctly passes.

For example, `theorem_proof_delivery` may return a failure-certificate or quarantine
variant after all three reasoning steps complete. The run remains operationally valid;
the negative theorem disposition must remain visible and must not be rewritten as proof.
"""
    write(OUTPUT / "README.md", readme)
    catalog_lines = [
        "# Workflow Catalog",
        "",
        "This catalog explains the executable projects generated from the canonical manifest.",
        "",
        "| Workflow | Reasoning | Steps | Input → output |",
        "| --- | --- | ---: | --- |",
    ]
    for row in workflow_catalog:
        catalog_lines.append(
            f"| `{row['id']}` | `{row['reasoning']}` | {len(row['steps'])} | "
            f"`{row['input_type']}` → `{row['output_type']}` |"
        )
    catalog_lines.extend(
        [
            "",
            "Every row is converted and runtime-bound. The generated value remains subject to the source claim ceiling.",
        ]
    )
    write(OUTPUT / "workflow_catalog.md", "\n".join(catalog_lines))

    config = {
        "schema_version": 1,
        "package": {"key": "abducer-repository-prism", "display_name": "Abducer Repository PRISM"},
        "python": ">=3.12,<3.15",
        "skills": skills,
        "data_sources": data_sources,
        "workflows": workflow_rows,
        "runtime": {
            "requirements_lock": None,
            "planning_hooks": [],
            "entrypoints": [
                {
                    "id": f"abducer-workflow-{operation}",
                    "operation": operation,
                    "source": "abducer-repository-prism/runtime/abducer_lunar_runtime.py",
                    "target": "abducer_lunar_runtime.py",
                    "callable": operation,
                }
                for operation in ("prepare", "execute", "verify")
            ],
        },
        "exclusions": [
            {"path": "prior ZIP archives", "reason": "outputs are evidence, never conversion sources"},
            {"path": "mutable run/log/trace state", "reason": "host state is not deterministic package input"},
            {"path": "credentials and local configuration", "reason": "secrets remain host-owned"},
            {"path": "historical reports", "reason": "not executable workflow, skill, or declared data source"},
        ],
    }
    write(ROOT / "prism-export.json", canonical_json(config))
    repository_metadata = OUTPUT / "projects" / "abducer_work_loop" / "conversion"
    write(
        repository_metadata / "repository-workflow-catalog.json",
        canonical_json({"schema_version": 1, "workflows": workflow_catalog}),
    )
    write(
        repository_metadata / "repository-skill-dispositions.json",
        canonical_json(
            {
                "schema_version": 1,
                "skills": [
                    {"id": row["id"], "source_root": row["root"], "disposition": "converted"}
                    for row in skills
                ],
            }
        ),
    )
    write(
        repository_metadata / "repository-source-fingerprint.json",
        canonical_json(fingerprint),
    )
    write(
        repository_metadata / "repository-generation.json",
        (OUTPUT / "conversion/generation.json").read_text(encoding="utf-8"),
    )
    write(repository_metadata / "repository-export-config.json", canonical_json(config))
    return {
        "status": "generated",
        "workflows": len(workflow_rows),
        "skills": len(skills),
        "data_sources": len(data_sources),
        "fingerprinted_files": len(fingerprint["files"]),
    }


if __name__ == "__main__":
    print(canonical_json(build()), end="")
