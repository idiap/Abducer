"""Render reviewed conversion models into canonical, checked Prism projects."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import __version__
from .adapters import (
    AdapterError,
    generate_python_adapter_package,
    prism_python_wrapper,
)
from .capabilities import write_capability_probe
from .conformance import canonical_sha256, validate_generated_layers
from .dependencies import (
    DependencyManifest,
    bundle_dependencies,
    bundle_prebuilt_dependencies,
    validate_dependency_bundle,
    write_dependency_lock,
    write_offline_bootstrap,
)
from .schemas import validate_document
from .semantic_types import (
    SemanticContract,
    SemanticTypeError,
    render_fixture,
    render_types,
    validate_semantic_contract,
)
from .snapshot import create_allowlisted_snapshot


class GenerationError(RuntimeError):
    """A reviewed model cannot be rendered as a complete Prism project."""


@dataclass(frozen=True, slots=True)
class GeneratedProject:
    root: Path
    main: Path
    source_hashes: dict[str, str]
    dependency_manifest: DependencyManifest | None


def generate_project(
    *,
    source_root: Path,
    output_root: Path,
    model: dict[str, Any],
    prism_executable: str,
    prism_source: Path | None = None,
    wheelhouse: Path | None = None,
    bundle: bool = False,
    download_external: bool = False,
    handler: str = "fake",
) -> GeneratedProject:
    """Generate one atomic canonical Prism project from an approved model."""
    schema_issues = validate_document(model, "generation-plan")
    if schema_issues:
        raise GenerationError(
            "invalid semantic generation plan: "
            + "; ".join(str(issue) for issue in schema_issues)
        )
    source_root = source_root.resolve()
    output_root = output_root.resolve()
    if source_root == output_root or source_root in output_root.parents:
        raise GenerationError("output must not be inside the source project")
    workflows = model.get("workflows")
    if not isinstance(workflows, list) or not workflows:
        raise GenerationError("reviewed model must contain at least one workflow")
    if len(workflows) != 1:
        raise GenerationError("v1 generation requires exactly one workflow per project")
    workflow = workflows[0]
    if not isinstance(workflow, dict):
        raise GenerationError("workflow model must be an object")
    steps = _steps(workflow)
    try:
        semantic = validate_semantic_contract(model, workflow, steps)
    except SemanticTypeError as exc:
        raise GenerationError(f"semantic typing gate failed: {exc}") from exc
    with tempfile.TemporaryDirectory(prefix="to-prism-generate-") as temporary:
        staging = Path(temporary) / "prism_project"
        staging.mkdir()
        (staging / "generated").mkdir()
        (staging / "tests").mkdir()
        _write_types(staging, semantic, steps)
        built_steps = _build_skills(
            source_root=source_root,
            project_root=staging,
            steps=steps,
            prism_executable=prism_executable,
        )
        built_hooks = _build_hooks(
            source_root=source_root,
            project_root=staging,
            hooks=model.get("hooks", []),
            prism_executable=prism_executable,
        )
        adapter_specs = model.get("python_adapters", [])
        if not isinstance(adapter_specs, list):
            raise GenerationError("python_adapters must be a list")
        if bundle:
            missing_licenses = [
                str(specification.get("source_path", ""))
                for specification in adapter_specs
                if not str(specification.get("license", "")).strip()
            ]
            if missing_licenses:
                raise GenerationError(
                    "portable Python adapters require reviewed license dispositions: "
                    f"{missing_licenses}"
                )
        _validate_adapter_dispositions(built_steps, adapter_specs)
        _validate_python_adapter_contracts(adapter_specs, semantic)
        _validate_computed_step_adapters(built_steps, adapter_specs)
        try:
            generate_python_adapter_package(
                source_root=source_root,
                project_root=staging,
                specifications=adapter_specs,
            )
        except AdapterError as exc:
            raise GenerationError(f"invalid Python leaf adapter: {exc}") from exc
        _write_python_effects(
            staging,
            adapter_specs,
            semantic=semantic,
        )
        if any(step["semantic_role"] == "epistemic" for step in built_steps):
            _write_reasoning(staging, semantic, built_steps)
        active_hook = None
        if handler == "codex" and built_hooks.get("codex", {}).get("runtime_active"):
            active_hook = built_hooks["codex"]
        _write_materialization(
            staging,
            semantic,
            built_steps,
            adapter_specs=adapter_specs,
            active_hook=active_hook,
        )
        _write_main(staging, semantic, built_steps)
        _write_fixture_test(staging)
        _write_project_metadata(staging, model, handler)
        layer_issues = validate_generated_layers(staging, model)
        if layer_issues:
            raise GenerationError(
                "generated layer conformance failed: " + "; ".join(layer_issues)
            )
        snapshot_entries = model.get("vendored_files", [])
        if not isinstance(snapshot_entries, list):
            raise GenerationError("vendored_files must be a list")
        create_allowlisted_snapshot(
            source_root=source_root,
            project_root=staging,
            entries=snapshot_entries,
        )
        write_capability_probe(prism_executable, staging / "capabilities.json")
        for prism_source_file in sorted(staging.rglob("*.prism")):
            relative_source = prism_source_file.relative_to(staging).as_posix()
            _run_prism(prism_executable, staging, "check", relative_source)
            _run_prism(prism_executable, staging, "compile", relative_source)
        dependency_manifest = None
        if bundle:
            if prism_source is not None:
                dependency_manifest = bundle_dependencies(
                    prism_source=prism_source,
                    project_root=staging,
                    handler=handler,
                    python_adapter=bool(model.get("python_adapters")),
                    wheelhouse=wheelhouse,
                    build_wheels=True,
                    download_external=download_external,
                )
            else:
                prebuilt_vendor = _prebuilt_vendor(wheelhouse)
                dependency_manifest = bundle_prebuilt_dependencies(
                    prebuilt_vendor=prebuilt_vendor,
                    project_root=staging,
                    python_adapter=bool(model.get("python_adapters")),
                )
            write_dependency_lock(staging, dependency_manifest)
            write_offline_bootstrap(staging)
            dependency_failures = validate_dependency_bundle(
                staging, require_all_external=True
            )
            if dependency_failures:
                raise GenerationError(
                    "portable dependency closure is incomplete: "
                    + "; ".join(dependency_failures)
                )
        else:
            _write_development_launcher(staging, prism_executable)
        hashes = _hash_generated_sources(staging)
        conversion = staging / "conversion"
        conversion.mkdir()
        (conversion / "generation.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "generator": "to_prism",
                    "generator_version": __version__,
                    "generation_plan_sha256": "sha256:" + canonical_sha256(model),
                    "authoritative_target": "canonical-.prism",
                    "workflow": str(workflow.get("id", "converted-workflow")),
                    "source_hashes": hashes,
                    "portable": bundle,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        if output_root.exists():
            raise GenerationError(f"output already exists: {output_root}")
        output_root.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(staging, output_root, copy_function=shutil.copy2)
    return GeneratedProject(
        root=output_root,
        main=output_root / "main.prism",
        source_hashes=hashes,
        dependency_manifest=dependency_manifest,
    )


def _prebuilt_vendor(explicit: Path | None) -> Path:
    candidates: list[Path] = []
    if explicit is not None:
        candidates.extend(
            (explicit, explicit.parent if explicit.name == "wheels" else explicit)
        )
    configured = os.environ.get("TO_PRISM_TOOLCHAIN_ROOT")
    if configured:
        candidates.append(Path(configured) / "vendor")
    candidates.append(Path(__file__).resolve().parents[2] / "vendor")
    for candidate in candidates:
        if (candidate / "manifest.json").is_file() and (candidate / "wheels").is_dir():
            return candidate
    raise GenerationError(
        "portable generation requires --prism-source or a complete bundled vendor toolchain"
    )


def _steps(workflow: dict[str, Any]) -> list[dict[str, Any]]:
    raw = workflow.get("steps")
    if not isinstance(raw, list) or not raw:
        raise GenerationError("workflow must contain at least one step")
    steps: list[dict[str, Any]] = []
    names: set[str] = set()
    for index, item in enumerate(raw, 1):
        if not isinstance(item, dict):
            raise GenerationError(f"workflow step {index} must be an object")
        name = _identifier(str(item.get("id", f"step_{index}")))
        if name in names:
            raise GenerationError(f"duplicate normalized step id: {name}")
        names.add(name)
        reasoning_type = item.get("reasoning_type")
        if reasoning_type is not None and not re.fullmatch(
            r"[A-Z][A-Za-z0-9_]*", str(reasoning_type)
        ):
            raise GenerationError(
                f"step {name} has invalid reasoning type: {reasoning_type!r}"
            )
        relation_type = item.get("relation_type")
        if relation_type is not None and not re.fullmatch(
            r"[A-Z][A-Za-z0-9_]*", str(relation_type)
        ):
            raise GenerationError(
                f"step {name} has invalid project-local relation type: {relation_type!r}"
            )
        steps.append(
            {
                **item,
                "id": name,
                "reasoning_type": str(reasoning_type) if reasoning_type else None,
                "relation_type": str(relation_type) if relation_type else None,
            }
        )
    return steps


def _build_skills(
    *,
    source_root: Path,
    project_root: Path,
    steps: Iterable[dict[str, Any]],
    prism_executable: str,
) -> list[dict[str, Any]]:
    built: list[dict[str, Any]] = []
    scratch = project_root / ".to_prism_build"
    scratch.mkdir()
    for step in steps:
        skill_specs = step.get("skills")
        if not isinstance(skill_specs, list) or not skill_specs:
            raise GenerationError(
                f"step {step['id']} must be materialized by one or more reviewed skills"
            )
        compiled_skills: list[dict[str, Any]] = []
        for skill_index, skill in enumerate(skill_specs, 1):
            if not isinstance(skill, dict):
                raise GenerationError(
                    f"step {step['id']} skill {skill_index} must be an object"
                )
            skill_path = skill.get("path")
            source = (source_root / str(skill_path or "")).resolve()
            if source_root not in source.parents:
                raise GenerationError(f"skill escapes source root: {skill_path}")
            instruction = source / "SKILL.md" if source.is_dir() else source
            if not instruction.is_file():
                raise GenerationError(f"skill has no SKILL.md: {skill_path}")
            clean = scratch / step["id"] / str(skill_index) / instruction.parent.name
            dispositions = skill.get("resource_dispositions", {})
            if not isinstance(dispositions, dict):
                raise GenerationError(
                    f"skill {skill_path} resource_dispositions must be an object"
                )
            skipped = _copy_skill_without_executables(instruction.parent, clean)
            undispositioned = sorted(
                path for path in skipped if path not in dispositions
            )
            invalid = sorted(
                path
                for path in skipped
                if dispositions.get(path) not in {"adapter", "exclude"}
            )
            if undispositioned or invalid:
                raise GenerationError(
                    f"skill {skill_path} has non-transpilable resources without a reviewed disposition: "
                    f"{sorted(set(undispositioned + invalid))}"
                )
            if step.get("material_kind", "agent") == "computed":
                compiled_skills.append(
                    {
                        **skill,
                        "export": None,
                        "module": None,
                        "skipped_resources": skipped,
                    }
                )
                continue
            output = (
                project_root / "generated" / f"{step['id']}_skill_{skill_index}.prism"
            )
            completed = subprocess.run(
                [
                    prism_executable,
                    "build",
                    "skill",
                    str(clean),
                    "--contract",
                    f"types.{step['input_type']}",
                    "--out",
                    str(output),
                ],
                cwd=project_root,
                text=True,
                capture_output=True,
                check=False,
            )
            if completed.returncode:
                raise GenerationError(
                    f"skill build failed for {skill_path}: "
                    f"{completed.stderr.strip() or completed.stdout.strip()}"
                )
            payload = json.loads(completed.stdout)
            compiled_skills.append(
                {
                    **skill,
                    "export": payload["export"],
                    "module": f"generated.{step['id']}_skill_{skill_index}",
                    "skipped_resources": skipped,
                }
            )
        built.append({**step, "compiled_skills": compiled_skills})
    shutil.rmtree(scratch)
    return built


def _validate_adapter_dispositions(
    steps: list[dict[str, Any]], specifications: list[dict[str, Any]]
) -> None:
    adapter_sources = {
        Path(str(item.get("source_path", ""))).as_posix() for item in specifications
    }
    for step in steps:
        for skill in step.get("compiled_skills", []):
            skill_path = skill.get("path")
            dispositions = skill.get("resource_dispositions", {})
            for relative in skill.get("skipped_resources", []):
                if dispositions.get(relative) != "adapter":
                    continue
                expected = (Path(str(skill_path)) / relative).as_posix()
                if expected not in adapter_sources:
                    raise GenerationError(
                        f"resource {expected} is marked adapter but has no Python adapter specification"
                    )


def _validate_computed_step_adapters(
    steps: list[dict[str, Any]], specifications: list[dict[str, Any]]
) -> None:
    adapters = {str(item.get("operation", "")): item for item in specifications}
    for step in steps:
        if step.get("material_kind", "agent") != "computed":
            continue
        operation = str(step.get("adapter_operation", ""))
        adapter = adapters.get(operation)
        if adapter is None:
            raise GenerationError(
                f"computed step {step['id']} references missing Python adapter operation {operation}"
            )
        if str(adapter.get("input_type", "")) != step["input_type"]:
            raise GenerationError(
                f"computed step {step['id']} adapter input must be {step['input_type']}"
            )
        if str(adapter.get("output_type", "")) != step["output_type"]:
            raise GenerationError(
                f"computed step {step['id']} adapter output must be {step['output_type']}"
            )


def _copy_skill_without_executables(source: Path, destination: Path) -> list[str]:
    executable_suffixes = {".py", ".sh", ".bash", ".zsh", ".js", ".ts", ".rb", ".pl"}
    skipped: list[str] = []
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source).as_posix()
        if path.is_symlink():
            skipped.append(relative)
            continue
        if not path.is_file():
            continue
        if path.suffix.lower() in executable_suffixes or path.name.lower() in {
            ".env",
            "credentials.json",
            "secrets.json",
        }:
            skipped.append(relative)
            continue
        target = destination / Path(relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        if relative == "SKILL.md":
            target.write_text(
                _normalize_skill_frontmatter(path.read_text(encoding="utf-8")),
                encoding="utf-8",
            )
        else:
            shutil.copy2(path, target)
    return skipped


_SKILL_FRONTMATTER = re.compile(
    r"\A---[ \t]*\r?\n.*?\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL
)
_LEADING_HTML_PREAMBLE = re.compile(
    r"\A(?P<preamble>(?:[ \t\r\n]*<!--[\s\S]*?-->)+[ \t\r\n]*)"
)


def _normalize_skill_frontmatter(text: str) -> str:
    """Expose valid skill frontmatter without changing the source artifact.

    Some repositories place an SPDX or documentation preamble in leading HTML
    comments. Prism's skill builder requires YAML frontmatter at byte zero, so
    the clean staging copy moves only that recognized preamble immediately
    after the frontmatter. Any other prefix remains an error instead of being
    silently discarded.
    """
    direct = _SKILL_FRONTMATTER.match(text)
    if direct is not None:
        return text
    preamble_match = _LEADING_HTML_PREAMBLE.match(text)
    if preamble_match is None:
        raise GenerationError(
            "SKILL.md must contain YAML frontmatter at byte zero or after a leading HTML-comment preamble"
        )
    remainder = text[preamble_match.end() :]
    frontmatter_match = _SKILL_FRONTMATTER.match(remainder)
    if frontmatter_match is None:
        raise GenerationError(
            "SKILL.md leading HTML-comment preamble is not followed by valid YAML frontmatter"
        )
    frontmatter = frontmatter_match.group(0)
    body = remainder[frontmatter_match.end() :]
    return frontmatter + preamble_match.group("preamble") + body


def _build_hooks(
    *,
    source_root: Path,
    project_root: Path,
    hooks: object,
    prism_executable: str,
) -> dict[str, dict[str, Any]]:
    if not isinstance(hooks, list):
        raise GenerationError("hooks model must be a list")
    grouped: dict[str, list[tuple[dict[str, Any], dict[str, Any]]]] = {}
    for index, hook in enumerate(hooks, 1):
        if not isinstance(hook, dict):
            raise GenerationError(f"hook {index} must be an object")
        provider = str(hook.get("provider", ""))
        if provider not in {"codex", "claude"}:
            raise GenerationError(f"unsupported hook provider: {provider}")
        relative = Path(str(hook.get("path", "")))
        source = (source_root / relative).resolve()
        if source_root not in source.parents or not source.is_file():
            raise GenerationError(f"invalid hook path: {relative}")
        try:
            hook_payload = json.loads(source.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise GenerationError(
                f"hook configuration is not valid JSON: {relative}"
            ) from exc
        if not isinstance(hook_payload, dict) or not isinstance(
            hook_payload.get("hooks"), dict
        ):
            raise GenerationError(
                f"hook configuration must contain one hooks object: {relative}"
            )
        unsupported_fields = sorted(set(hook_payload) - {"description", "hooks"})
        if unsupported_fields:
            raise GenerationError(
                f"hook configuration has undispositioned top-level fields: {unsupported_fields}"
            )
        grouped.setdefault(provider, []).append((hook, hook_payload))
    built: dict[str, dict[str, Any]] = {}
    for provider, configurations in sorted(grouped.items()):
        merged_hooks: dict[str, list[Any]] = {}
        descriptions: list[str] = []
        runtime_active = False
        for specification, payload in configurations:
            for event, groups in payload["hooks"].items():
                if not isinstance(groups, list):
                    raise GenerationError(f"hook event {event} must contain a list")
                merged_hooks.setdefault(str(event), []).extend(groups)
            if isinstance(payload.get("description"), str):
                descriptions.append(payload["description"])
            if specification.get("runtime") == "active":
                runtime_active = True
                _require_portable_hook_commands(payload)
        merged_payload: dict[str, Any] = {"hooks": merged_hooks}
        if descriptions:
            merged_payload["description"] = "\n".join(descriptions)
        native = project_root / "generated" / f"{provider}_hooks.native.json"
        native.write_text(
            json.dumps(merged_payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        output = project_root / "generated" / f"{provider}_hooks.prism"
        completed = subprocess.run(
            [
                prism_executable,
                "build",
                "hooks",
                provider,
                str(native),
                "--out",
                str(output),
            ],
            cwd=project_root,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode:
            raise GenerationError(
                f"hook build failed for {provider}: "
                f"{completed.stderr.strip() or completed.stdout.strip()}"
            )
        payload = json.loads(completed.stdout)
        built[provider] = {
            "export": payload["export"],
            "module": f"generated.{provider}_hooks",
            "provider_type": provider.capitalize(),
            "runtime_active": runtime_active,
        }
    return built


def _require_portable_hook_commands(payload: dict[str, Any]) -> None:
    """Reject active hooks whose commands rely on the absent source working tree."""
    script_suffixes = (".py", ".sh", ".bash", ".zsh", ".js", ".ts")
    for groups in payload.get("hooks", {}).values():
        for group in groups:
            for handler in group.get("hooks", []):
                command = handler.get("command")
                if not isinstance(command, str):
                    continue
                tokens = command.split()
                if any(
                    token.startswith(".")
                    or ("/" in token and not token.startswith(("http://", "https://")))
                    or token.endswith(script_suffixes)
                    for token in tokens
                ):
                    raise GenerationError(
                        "active Codex hooks must be self-contained PATH commands; "
                        f"project-relative command is unsupported: {command}"
                    )


def _write_types(
    root: Path, semantic: SemanticContract, steps: list[dict[str, Any]]
) -> None:
    rendered = render_types(semantic.types)
    if len({str(step["failure_type"]) for step in steps}) > 1:
        rendered += "type ConvertedWorkflowFailure:\n    | ModelFailure\n    | PythonError\n\n"
    (root / "types.prism").write_text(
        rendered,
        encoding="utf-8",
    )


def _write_reasoning(
    root: Path, semantic: SemanticContract, steps: list[dict[str, Any]]
) -> None:
    imports = sorted(
        {semantic.input_type, semantic.output_type}
        | {step["input_type"] for step in steps}
        | {step["output_type"] for step in steps}
    )
    lines = ["from types import (", *(f"    {name}," for name in imports), ")", ""]
    epistemic_steps = [step for step in steps if step["semantic_role"] == "epistemic"]
    methods: dict[str, tuple[str, str]] = {}
    for step in epistemic_steps:
        method = step["reasoning_type"]
        signature = (step["input_type"], step["output_type"])
        if method in methods and methods[method] != signature:
            raise GenerationError(
                f"reasoning type {method} is reused with incompatible contracts"
            )
        methods[method] = signature
    for method, (input_type, output_type) in methods.items():
        lines.extend(
            [
                f"# {next(step['reasoning_rationale'] for step in epistemic_steps if step['reasoning_type'] == method)}",
                f"type {method} = (source: {input_type}) -> Generated[{output_type}]",
                "",
            ]
        )
    declared_relations: dict[str, tuple[str, str]] = {}
    for step in epistemic_steps:
        relation = step["relation_type"]
        if not relation:
            continue
        signature = (step["input_type"], step["output_type"])
        if relation in declared_relations and declared_relations[relation] != signature:
            raise GenerationError(
                f"relation type {relation} is reused with incompatible contracts"
            )
        if relation in declared_relations:
            continue
        declared_relations[relation] = signature
        lines.extend(
            [
                f"type {relation}Certificate:",
                f"    source: {step['input_type']}",
                f"    target: Generated[{step['output_type']}]",
                "",
                f"relation {relation}(",
                f"    source: {step['input_type']},",
                f"    target: Generated[{step['output_type']}],",
                f") -> {relation}Certificate",
                "",
            ]
        )
    if semantic.mode == "mixed":
        (root / "reasoning.prism").write_text("\n".join(lines), encoding="utf-8")
        return
    lines.extend(
        [
            f"# {semantic.workflow_description}",
            f"reasoning {semantic.workflow_name}(",
            f"    {semantic.input_name}: {semantic.input_type},",
            f") -> Generated[{semantic.output_type}]:",
            "    sequence:",
        ]
    )
    prior = semantic.input_name
    for step in steps:
        relation_suffix = (
            f" by {step['relation_type']}" if step["relation_type"] else ""
        )
        lines.append(f"        # Granularity: {step['granularity_rationale']}")
        lines.append(
            f"        [{step['id']}: {step['reasoning_type']}({prior})]{relation_suffix}"
        )
        prior = f"{step['id']}.value"
    lines.append(f"    return {steps[-1]['id']}")
    lines.append("")
    (root / "reasoning.prism").write_text("\n".join(lines), encoding="utf-8")


def _write_materialization(
    root: Path,
    semantic: SemanticContract,
    steps: list[dict[str, Any]],
    *,
    adapter_specs: list[dict[str, Any]],
    active_hook: dict[str, Any] | None,
) -> None:
    type_imports = sorted(
        {semantic.input_type, semantic.output_type}
        | {step["input_type"] for step in steps}
        | {step["output_type"] for step in steps}
    )
    if len({str(step["failure_type"]) for step in steps}) > 1:
        type_imports.append("ConvertedWorkflowFailure")
    lines = ["from types import (", *(f"    {name}," for name in type_imports), ")"]
    if semantic.mode == "epistemic":
        lines.append(f"from reasoning import {semantic.workflow_name}")
    for step in steps:
        for skill in step["compiled_skills"]:
            if skill["export"] is not None:
                lines.append(f"from {skill['module']} import {skill['export']}")
    adapter_functions = {
        str(specification.get("operation")): f"python_leaf_{index}"
        for index, specification in enumerate(adapter_specs, 1)
    }
    if adapter_functions:
        lines.append(
            "from python_effects import " + ", ".join(adapter_functions.values())
        )
    if active_hook is not None:
        lines.append(f"from {active_hook['module']} import {active_hook['export']}")
    relations = sorted(
        {step["relation_type"] for step in steps if step["relation_type"]}
    )
    for relation in relations:
        lines.append(f"from reasoning import {relation}Certificate")
    lines.append("")
    for step in steps:
        if step.get("material_kind", "agent") == "computed":
            operation = str(step["adapter_operation"])
            function = adapter_functions.get(operation)
            if function is None:
                raise GenerationError(
                    f"computed step {step['id']} references missing Python adapter operation {operation}"
                )
            skill_comments = [
                f"# Skill {skill['path']}: {skill['role']} — {skill['contribution']}"
                for skill in step["compiled_skills"]
            ]
            lines.extend(
                [
                    f"# {step['description']}",
                    f"# Granularity: {step['granularity_rationale']}",
                    *skill_comments,
                    f"def {step['id']}_compute(",
                    f"    task: {step['input_type']},",
                    "    python_access: PythonCall,",
                    f") -> Result[Computed[{step['output_type']}], PythonError] ! {{Python.Call}}:",
                    f"    value = try {function}(task, python_access)",
                    f"    return Ok(compute(value, procedure = {json.dumps(step['procedure'])}))",
                    "",
                ]
            )
            continue
        relation = step["relation_type"]
        if not relation:
            continue
        builder = f"{step['id']}_relation_builder"
        lines.extend(
            [
                f"def {builder}(",
                f"    source: {step['input_type']},",
                f"    target: Generated[{step['output_type']}],",
                f") -> {relation}Certificate:",
                f"    return {relation}Certificate(source = source, target = target)",
                "",
            ]
        )
    for step in steps:
        if step.get("material_kind", "agent") == "computed":
            continue
        exports = ", ".join(skill["export"] for skill in step["compiled_skills"])
        skill_comments = [
            f"# Skill {skill['path']}: {skill['role']} — {skill['contribution']}"
            for skill in step["compiled_skills"]
        ]
        lines.extend(
            [
                f"# {step['description']}",
                f"# Granularity: {step['granularity_rationale']}",
                *skill_comments,
                f"agent {step['id']}_agent(",
                f"    task: {step['input_type']},",
                f") -> Result[Generated[{step['output_type']}], ModelFailure]",
                "    ! {AI.Generate, Context.Disclose}:",
                f"    skills: Skills[{step['input_type']}] = [{exports}]",
                *(
                    [
                        f"    hooks: Hooks[{active_hook['provider_type']}] = {active_hook['export']}"
                    ]
                    if active_hook is not None
                    else []
                ),
                "",
            ]
        )
    if semantic.mode == "epistemic":
        lines.append(f"converted_workflow = {semantic.workflow_name}(")
        for step in steps:
            lines.append(f"    {step['id']} = {step['id']}_agent,")
            if step["relation_type"]:
                lines.append(f"    {step['id']}_by = {step['id']}_relation_builder,")
        lines.extend((")", ""))
    else:
        workflow_effects = sorted(
            {effect for step in steps for effect in step["effects"]}
        )
        failures = {str(step["failure_type"]) for step in steps}
        failure_type = (
            "ConvertedWorkflowFailure" if len(failures) > 1 else next(iter(failures))
        )
        result_wrapper = "Computed" if semantic.output_provenance == "computed" else "Generated"
        capabilities = (
            ["    python_access: PythonCall,"]
            if any(step.get("material_kind", "agent") == "computed" for step in steps)
            else []
        )
        lines.extend(
            [
                f"# {semantic.workflow_description}",
                f"workflow {semantic.workflow_name}(",
                f"    {semantic.input_name}: {semantic.input_type},",
                *capabilities,
                f") -> {result_wrapper}[{semantic.output_type}]",
                f"    fails {failure_type}",
                "    ! {" + ", ".join(workflow_effects) + "}:",
                "    sequence:",
            ]
        )
        prior = semantic.input_name
        for step in steps:
            suffix = "_compute" if step.get("material_kind", "agent") == "computed" else "_agent"
            arguments = f"{prior}, python_access" if suffix == "_compute" else prior
            lines.append(f"        [{step['id']}: {step['id']}{suffix}({arguments})]")
            prior = f"{step['id']}.value"
        lines.extend((f"    return {steps[-1]['id']}", ""))
    (root / "materialization.prism").write_text("\n".join(lines), encoding="utf-8")


def _write_main(
    root: Path, semantic: SemanticContract, steps: list[dict[str, Any]]
) -> None:
    has_computed = any(
        step.get("material_kind", "agent") == "computed" for step in steps
    )
    fixture = render_fixture(
        semantic.fixture, semantic.input_type, semantic.types, indent=4
    )
    if semantic.mode == "epistemic":
        imports = f"""from materialization import converted_workflow
from reasoning import {semantic.workflow_name}
from types import {semantic.input_type}, {semantic.output_type}
"""
        resolution = (
            f"solve {semantic.workflow_name}({semantic.input_name}) "
            f"using converted_workflow({semantic.input_name})"
        )
    else:
        imported_types = [semantic.input_type, semantic.output_type]
        if len({str(step["failure_type"]) for step in steps}) > 1:
            imported_types.append("ConvertedWorkflowFailure")
        imports = (
            f"from materialization import {semantic.workflow_name}\n"
            + "from types import "
            + ", ".join(imported_types)
            + "\n"
        )
        resolution = (
            f"solve {semantic.workflow_name}({semantic.input_name}, python_access)"
            if has_computed
            else f"solve {semantic.workflow_name}({semantic.input_name})"
        )
    indented_fixture = fixture.replace("\n", "\n    ")
    wrapper = "Computed" if semantic.output_provenance == "computed" else "Generated"
    failures = {str(step["failure_type"]) for step in steps}
    failure = (
        "ConvertedWorkflowFailure"
        if len(failures) > 1
        else next(iter(failures))
    )
    python_parameter = "    python_access: PythonCall,\n" if has_computed else ""
    effects = ", ".join(sorted({effect for step in steps for effect in step["effects"]}))
    text = f"""{imports}

def main(
    model_access: ModelGenerate,
    disclosure: ContextDisclose,
{python_parameter}) -> Result[{wrapper}[{semantic.output_type}], {failure}] ! {{{effects}}}:
    {semantic.input_name} = {indented_fixture}
    return {resolution}
"""
    (root / "main.prism").write_text(text, encoding="utf-8")


def _write_fixture_test(root: Path) -> None:
    (root / "tests" / "fixture.json").write_text(
        json.dumps({"handler": "fake", "entrypoint": "main.prism"}, indent=2) + "\n",
        encoding="utf-8",
    )


def _write_python_effects(
    root: Path,
    specifications: list[dict[str, Any]],
    *,
    semantic: SemanticContract,
) -> None:
    if not specifications:
        return
    imported_types = sorted(
        {str(item.get("input_type", "")) for item in specifications}
        | {str(item.get("output_type", "")) for item in specifications}
    )
    if "" in imported_types:
        raise GenerationError(
            "Python adapters require explicit input_type and output_type"
        )
    lines = [
        "from types import (",
        *(f"    {name}," for name in imported_types),
        ")",
        "",
    ]
    for index, specification in enumerate(specifications, 1):
        operation = str(specification.get("operation", ""))
        input_type = str(specification.get("input_type", ""))
        output_type = str(specification.get("output_type", ""))
        lines.append(
            prism_python_wrapper(
                operation,
                f"python_leaf_{index}",
                input_type=input_type,
                output_type=output_type,
            )
        )
        if input_type == semantic.input_type:
            fixture = render_fixture(
                semantic.fixture, semantic.input_type, semantic.types, indent=4
            ).replace("\n", "\n    ")
            harness = f"""from python_effects import python_leaf_{index}
from types import {input_type}, {output_type}

def main(
    python_access: PythonCall,
) -> Result[{output_type}, PythonError] ! {{Python.Call}}:
    request = {fixture}
    return python_leaf_{index}(request, python_access)
"""
            (root / "tests" / f"python_leaf_{index}.prism").write_text(
                harness, encoding="utf-8"
            )
    (root / "python_effects.prism").write_text("\n".join(lines), encoding="utf-8")


def _validate_python_adapter_contracts(
    specifications: list[dict[str, Any]], semantic: SemanticContract
) -> None:
    """Keep opaque Python at an exact, reviewable scalar leaf boundary."""
    for specification in specifications:
        operation = str(specification.get("operation", ""))
        input_type = str(specification.get("input_type", ""))
        output_type = str(specification.get("output_type", ""))
        input_field = str(specification.get("input_field", ""))
        output_field = str(specification.get("output_field", ""))
        if input_type not in semantic.types or output_type not in semantic.types:
            raise GenerationError(
                f"Python adapter {operation} must use declared nominal types"
            )
        input_definition = semantic.types[input_type]
        output_definition = semantic.types[output_type]
        matching_inputs = [
            field for field in input_definition.fields if field.name == input_field
        ]
        matching_outputs = [
            field for field in output_definition.fields if field.name == output_field
        ]
        if input_definition.kind != "record" or len(matching_inputs) != 1:
            raise GenerationError(
                f"Python adapter {operation} input_field must identify one field of {input_type}"
            )
        if matching_inputs[0].type != "String":
            raise GenerationError(
                f"Python adapter {operation} input_field must be String in v1"
            )
        if (
            output_definition.kind != "record"
            or len(output_definition.fields) != 1
            or len(matching_outputs) != 1
            or matching_outputs[0].type != "String"
        ):
            raise GenerationError(
                f"Python adapter {operation} output must be a one-field nominal String record in v1"
            )


def _write_project_metadata(root: Path, model: dict[str, Any], handler: str) -> None:
    (root / "pyproject.toml").write_text(
        """[project]
name = "converted-prism-project"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []
""",
        encoding="utf-8",
    )
    (root / "conversion-model.json").write_text(
        json.dumps(model, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (root / "runtime.json").write_text(
        json.dumps({"handler": handler, "workspace": "."}, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )


def _write_development_launcher(root: Path, prism_executable: str) -> None:
    del prism_executable
    launcher = """#!/usr/bin/env sh
set -eu
PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PRISM_BIN=${PRISM_BIN:-prism}
cd "$PROJECT_DIR"
exec "$PRISM_BIN" "$@"
"""
    path = root / "prism"
    path.write_text(launcher, encoding="utf-8")
    path.chmod(0o755)


def _run_prism(executable: str, cwd: Path, command: str, path: str) -> dict[str, Any]:
    completed = subprocess.run(
        [executable, command, path],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode:
        raise GenerationError(
            f"prism {command} failed: {completed.stderr.strip() or completed.stdout.strip()}"
        )
    return json.loads(completed.stdout)


def _hash_generated_sources(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*.prism"))
    }


def _identifier(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9_]+", "_", value).strip("_").lower()
    if not normalized:
        normalized = "step"
    if normalized[0].isdigit():
        normalized = f"step_{normalized}"
    return normalized


def _pascal(value: str) -> str:
    result = "".join(
        item.capitalize() for item in _identifier(value).split("_") if item
    )
    return result or "ConvertedWorkflow"


__all__ = ["GeneratedProject", "GenerationError", "generate_project"]
