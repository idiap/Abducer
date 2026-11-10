# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Provider-neutral command line interface."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Sequence

from . import __version__
from .baseline import build_baseline_descriptor, execute_baseline
from .contracts import build_contracts
from .decisions import build_decisions, invalidate_changed_decisions
from .fingerprint import fingerprint_tree
from .graph import build_workflow_graph
from .guard import GuardRejection, evaluate_from_environment
from .inventory import inspect_project
from .jsonio import canonical_json, read_json, write_json, write_text
from .lock import build_lock, generated_file_records
from .paths import (
    ConversionPaths,
    PathSafetyError,
    publish_directory,
    staging_directory,
)
from .reasoning import build_reasoning_map
from .report import build_report, render_report_markdown
from .schemas import SCHEMA_FILES, SchemaValidationError, require_valid
from .update import (
    changed_dependencies,
    detect_update_conflicts,
    semantic_inventory_diff,
)

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_SAFETY = 3
EXIT_VALIDATION = 4
EXIT_REVIEW_REQUIRED = 5


def _safe_copy_output(output: Path, stage: Path) -> None:
    if output.is_symlink() or not output.is_dir():
        raise PathSafetyError("existing output must be a real directory")
    shutil.copytree(output, stage, dirs_exist_ok=True, symlinks=True)
    conversion = stage / "conversion"
    if conversion.is_symlink():
        raise PathSafetyError("managed conversion directory must not be a symlink")
    conversion.mkdir(parents=True, exist_ok=True)


def _emit_result(value: dict[str, Any]) -> None:
    sys.stdout.write(canonical_json(value))


def _cmd_inspect(args: argparse.Namespace) -> int:
    paths = ConversionPaths.resolve(args.source, args.output)
    before = fingerprint_tree(paths.source)
    inventory = require_valid(inspect_project(paths.source), "inventory")
    report = require_valid(build_report(inventory), "report")
    if args.dry_run:
        _emit_result(inventory)
    else:
        with staging_directory(paths.output) as stage:
            conversion = stage / "conversion"
            conversion.mkdir(parents=True)
            write_json(conversion / "inventory.json", inventory)
            write_json(conversion / "report.json", report)
            write_text(conversion / "report.md", render_report_markdown(report))
            publish_directory(stage, paths.output, replace=args.replace)
    after = fingerprint_tree(paths.source)
    if before.digest != after.digest:
        raise PathSafetyError("source mutation detected during inspect")
    if not args.dry_run:
        _emit_result(
            {
                "command": "inspect",
                "items": len(inventory["items"]),
                "source_unchanged": True,
                "status": "ok",
            }
        )
    return EXIT_OK


def _load_current(paths: ConversionPaths) -> dict[str, Any]:
    if not paths.output.is_dir() or paths.output.is_symlink():
        raise FileNotFoundError("output does not contain an inspected conversion")
    inventory = read_json(paths.output / "conversion" / "inventory.json")
    return require_valid(inventory, "inventory")


def _build_model(inventory: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    contracts = require_valid(build_contracts(inventory), "contracts")
    workflow = require_valid(build_workflow_graph(inventory, contracts), "workflow")
    reasoning_map = require_valid(build_reasoning_map(workflow), "reasoning-map")
    decisions = require_valid(build_decisions(inventory), "decisions")
    report = require_valid(build_report(inventory, contracts, workflow), "report")
    return contracts, workflow, reasoning_map, decisions, report


def _write_model(stage: Path, artifacts: tuple[dict[str, Any], ...]) -> None:
    names = ("contracts", "workflow", "reasoning-map", "decisions", "report")
    conversion = stage / "conversion"
    for name, artifact in zip(names, artifacts, strict=True):
        write_json(conversion / f"{name}.json", artifact)
    write_text(conversion / "report.md", render_report_markdown(artifacts[-1]))


def _cmd_model(args: argparse.Namespace) -> int:
    paths = ConversionPaths.resolve(args.source, args.output)
    inventory = _load_current(paths)
    current = inspect_project(paths.source)
    if current["source"]["fingerprint"] != inventory["source"]["fingerprint"]:
        raise PathSafetyError("source changed since inspect; run update")
    artifacts = _build_model(inventory)
    if args.dry_run:
        _emit_result(
            {
                "command": "model",
                "contracts": len(artifacts[0]["contracts"]),
                "status": "review_required",
                "workflows": len(artifacts[1]["workflows"]),
            }
        )
        return EXIT_OK
    with staging_directory(paths.output) as stage:
        _safe_copy_output(paths.output, stage)
        _write_model(stage, artifacts)
        publish_directory(stage, paths.output, replace=True)
    _emit_result(
        {
            "command": "model",
            "contracts": len(artifacts[0]["contracts"]),
            "status": "review_required",
            "workflows": len(artifacts[1]["workflows"]),
        }
    )
    return EXIT_OK


def _cmd_baseline(args: argparse.Namespace) -> int:
    paths = ConversionPaths.resolve(args.source, args.output)
    inventory = _load_current(paths)
    current = fingerprint_tree(paths.source)
    if current.digest != inventory["source"]["fingerprint"]:
        raise PathSafetyError("source changed since inspect; run update")
    if args.authorize:
        if not args.command_json:
            raise ValueError(
                "--authorize requires --command-json with an explicit argv array"
            )
        try:
            command = json.loads(args.command_json)
        except json.JSONDecodeError as exc:
            raise ValueError("--command-json must be valid JSON") from exc
        if not isinstance(command, list):
            raise ValueError("--command-json must decode to an argv array")
        credentials = [
            item["id"]
            for item in inventory["items"]
            if item.get("security", {}).get("classification") == "credential-shaped"
        ]
        if credentials and not args.allow_credentials:
            raise ValueError(
                "baseline source contains credential-shaped paths; remove them or explicitly pass --allow-credentials"
            )
        if args.dry_run:
            descriptor = build_baseline_descriptor(paths.source, current.digest)
            descriptor["execution"]["reason"] = (
                "dry-run: approved command was validated but not executed"
            )
            descriptor["execution"]["requested_command"] = command
        else:
            descriptor = execute_baseline(
                source=paths.source,
                source_fingerprint=current.digest,
                command=command,
                timeout_seconds=args.timeout,
                attempts=args.attempts,
                output_limit=args.output_limit,
                network_policy=args.network,
            )
    else:
        descriptor = build_baseline_descriptor(paths.source, current.digest)
    require_valid(descriptor, "baseline")
    if args.dry_run:
        _emit_result(descriptor)
    else:
        with staging_directory(paths.output) as stage:
            _safe_copy_output(paths.output, stage)
            write_json(stage / "conversion" / "baseline.json", descriptor)
            publish_directory(stage, paths.output, replace=True)
        _emit_result(
            {
                "candidates": len(descriptor["candidates"]),
                "command": "baseline",
                "executed": bool(descriptor["execution"]["authorized"]),
                "status": (
                    descriptor["execution"]["classification"]
                    if descriptor["execution"]["authorized"]
                    else "review_required"
                ),
            }
        )
    if fingerprint_tree(paths.source).digest != current.digest:
        raise PathSafetyError("source mutation detected during baseline discovery")
    return EXIT_OK


def _cmd_update(args: argparse.Namespace) -> int:
    paths = ConversionPaths.resolve(args.source, args.output)
    old_inventory = _load_current(paths)
    new_inventory = require_valid(inspect_project(paths.source), "inventory")
    diff = semantic_inventory_diff(old_inventory, new_inventory)
    changed = changed_dependencies(diff)
    lock_path = paths.output / "conversion" / "to-prism.lock.json"
    if lock_path.is_file():
        lock_document = require_valid(read_json(lock_path), "to-prism-lock")
        conflicts = detect_update_conflicts(paths.output, lock_document)
        if conflicts:
            _emit_result(
                {
                    "command": "update",
                    "conflicts": conflicts,
                    "status": "review_required",
                }
            )
            return EXIT_REVIEW_REQUIRED
    artifacts = list(_build_model(new_inventory))
    decisions_path = paths.output / "conversion" / "decisions.json"
    if decisions_path.is_file():
        old_decisions = require_valid(read_json(decisions_path), "decisions")
        carried = invalidate_changed_decisions(old_decisions, changed)
        fresh_by_id = {item["id"]: item for item in artifacts[3]["decisions"]}
        for decision in carried["decisions"]:
            fresh_by_id[decision["id"]] = decision
        artifacts[3] = {
            **artifacts[3],
            "decisions": sorted(fresh_by_id.values(), key=lambda item: item["id"]),
        }
        require_valid(artifacts[3], "decisions")
    if args.dry_run:
        _emit_result(
            {
                "changed_items": sorted(changed),
                "command": "update",
                "diff": diff,
                "status": "review_required" if changed else "unchanged",
            }
        )
        return EXIT_OK
    with staging_directory(paths.output) as stage:
        _safe_copy_output(paths.output, stage)
        write_json(stage / "conversion" / "inventory.json", new_inventory)
        _write_model(stage, tuple(artifacts))
        write_json(stage / "conversion" / "update.json", diff)
        publish_directory(stage, paths.output, replace=True)
    _emit_result(
        {
            "changed_items": sorted(changed),
            "command": "update",
            "diff": diff,
            "status": "review_required" if changed else "unchanged",
        }
    )
    return EXIT_OK


def _cmd_validate(args: argparse.Namespace) -> int:
    document = read_json(args.path)
    require_valid(document, args.schema)
    _emit_result(
        {
            "command": "validate",
            "schema": args.schema or document["artifact"],
            "status": "ok",
        }
    )
    return EXIT_OK


def _cmd_guard(args: argparse.Namespace) -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        raise GuardRejection(
            "guard stdin must contain exactly one JSON object"
        ) from exc
    result = evaluate_from_environment(args.provider, args.event, payload)
    _emit_result(result)
    return EXIT_OK


def _cmd_doctor(args: argparse.Namespace) -> int:
    """Validate a transferred toolkit without inspecting an external project."""
    from .capabilities import probe_prism
    from .provider_profiles import load_profiles
    from .schemas import SCHEMA_FILES, load_schema

    profiles = load_profiles()
    for schema_name in SCHEMA_FILES:
        load_schema(schema_name)
    prism_status: dict[str, Any]
    resolved = shutil.which(args.prism)
    if resolved is None:
        prism_status = {"status": "unavailable"}
    else:
        try:
            capability = probe_prism(resolved)
        except (OSError, RuntimeError, ValueError) as exc:
            prism_status = {"status": "incompatible", "reason": str(exc)}
        else:
            prism_status = {
                "status": "compatible",
                "commands": capability["commands"],
                "executable_sha256": capability["executable_sha256"],
            }
    ready = prism_status["status"] == "compatible" or not args.require_prism
    _emit_result(
        {
            "command": "doctor",
            "profiles": [item["provider"] for item in profiles],
            "prism": prism_status,
            "python": f"{sys.version_info.major}.{sys.version_info.minor}",
            "schemas": sorted(SCHEMA_FILES),
            "status": "ready" if ready else "failed",
            "version": __version__,
        }
    )
    return EXIT_OK if ready else EXIT_VALIDATION


def _select_generation_model(
    paths: ConversionPaths,
    *,
    plan_path: str | None,
) -> dict[str, Any]:
    del paths
    if not plan_path:
        raise ValueError(
            "--plan is required: run to-prism-derive-types, review the induced "
            "domain/reasoning taxonomy, and supply an approved generation-plan"
        )
    return _load_approved_plan(plan_path)


def _load_approved_plan(path: str) -> dict[str, Any]:
    return require_valid(read_json(path), "generation-plan")


def _prism_identity(executable: str) -> dict[str, Any]:
    resolved = shutil.which(executable) or executable
    path = Path(resolved).resolve()
    digest = None
    if path.is_file():
        digest = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
    completed = subprocess.run(
        [str(path), "--version"], text=True, capture_output=True, check=False
    )
    return {
        "executable_sha256": digest,
        "version": (completed.stdout or completed.stderr).strip()[:256],
    }


def _record_generation_lock(paths: ConversionPaths, prism_executable: str) -> None:
    inventory = _load_current(paths)
    decisions_path = paths.output / "conversion" / "decisions.json"
    decisions = (
        read_json(decisions_path)
        if decisions_path.is_file()
        else build_decisions(inventory)
    )
    files = [
        path.relative_to(paths.output).as_posix()
        for path in sorted((paths.output / "prism_project").rglob("*"))
        if path.is_file() and not path.is_symlink()
    ]
    profiles = {
        item["name"]: item["profile_version"] for item in inventory.get("providers", [])
    }
    lock_document = build_lock(
        inventory=inventory,
        decisions=decisions,
        generated_files=generated_file_records(paths.output, files),
        profile_versions=profiles,
        prism=_prism_identity(prism_executable),
        template_version="1.0",
    )
    require_valid(lock_document, "to-prism-lock")
    write_json(paths.output / "conversion" / "to-prism.lock.json", lock_document)


def _cmd_generate(args: argparse.Namespace) -> int:
    from .generation import generate_project

    paths = ConversionPaths.resolve(args.source, args.output)
    model = _select_generation_model(
        paths,
        plan_path=args.plan,
    )
    if args.dry_run:
        _emit_result(
            {
                "command": "generate",
                "portable": args.portable,
                "status": "ready",
                "workflows": len(model["workflows"]),
            }
        )
        return EXIT_OK
    before = fingerprint_tree(paths.source)
    generate_project(
        source_root=paths.source,
        output_root=paths.output / "prism_project",
        model=model,
        prism_executable=args.prism,
        prism_source=Path(args.prism_source) if args.prism_source else None,
        wheelhouse=Path(args.wheelhouse) if args.wheelhouse else None,
        bundle=args.portable,
        download_external=args.download_dependencies,
        handler=args.prism_handler,
    )
    if fingerprint_tree(paths.source).digest != before.digest:
        raise PathSafetyError("source mutation detected during generation")
    _record_generation_lock(paths, args.prism)
    _emit_result(
        {
            "command": "generate",
            "portable": args.portable,
            "source_unchanged": True,
            "status": "ok",
        }
    )
    return EXIT_OK


def _cmd_verify(args: argparse.Namespace) -> int:
    from .verification import verify_generated_project

    paths = ConversionPaths.resolve(args.source, args.output)
    project = paths.output / "prism_project"
    if args.dry_run:
        _emit_result(
            {
                "command": "verify",
                "project_present": project.is_dir(),
                "status": "ready" if project.is_dir() else "failed",
            }
        )
        return EXIT_OK if project.is_dir() else EXIT_VALIDATION
    before = fingerprint_tree(paths.source)
    result = verify_generated_project(
        project_root=project,
        prism_executable=args.prism,
        handler=args.prism_handler,
        run_fixture=not args.skip_run,
        portable=args.portable,
    )
    if fingerprint_tree(paths.source).digest != before.digest:
        raise PathSafetyError("source mutation detected during verification")
    _emit_result(
        {
            "command": "verify",
            "levels": result.levels,
            "publishable": result.publishable,
            "source_unchanged": True,
            "status": "ok" if result.publishable else "failed",
        }
    )
    return EXIT_OK if result.publishable else EXIT_VALIDATION


def _cmd_convert(args: argparse.Namespace) -> int:
    paths = ConversionPaths.resolve(args.source, args.output)
    if paths.output.exists():
        raise FileExistsError("convert requires a new output directory")
    before = fingerprint_tree(paths.source)
    inventory = require_valid(inspect_project(paths.source), "inventory")
    artifacts = _build_model(inventory)
    approved_plan = _load_approved_plan(args.plan) if args.plan else None
    if args.dry_run:
        _emit_result(
            {
                "command": "convert",
                "portable": not args.linked,
                "status": "ready" if args.plan else "review_required",
                "workflows": len(artifacts[1]["workflows"]),
            }
        )
        return EXIT_OK if args.plan else EXIT_REVIEW_REQUIRED
    with staging_directory(paths.output) as stage:
        conversion = stage / "conversion"
        conversion.mkdir(parents=True)
        write_json(conversion / "inventory.json", inventory)
        _write_model(stage, artifacts)
        # Publication stops at the review gate unless the caller supplied a
        # separately reviewed generation plan.
        if not args.plan:
            if fingerprint_tree(paths.source).digest != before.digest:
                raise PathSafetyError(
                    "source mutation detected during conversion modeling"
                )
            publish_directory(stage, paths.output)
            _emit_result(
                {
                    "command": "convert",
                    "status": "review_required",
                    "staged": True,
                    "workflows": len(artifacts[1]["workflows"]),
                }
            )
            return EXIT_REVIEW_REQUIRED
        from .generation import generate_project

        generate_project(
            source_root=paths.source,
            output_root=stage / "prism_project",
            model=approved_plan,
            prism_executable=args.prism,
            prism_source=Path(args.prism_source) if args.prism_source else None,
            wheelhouse=Path(args.wheelhouse) if args.wheelhouse else None,
            bundle=not args.linked,
            download_external=args.download_dependencies,
            handler=args.prism_handler,
        )
        if fingerprint_tree(paths.source).digest != before.digest:
            raise PathSafetyError("source mutation detected during conversion")
        publish_directory(stage, paths.output)
    _record_generation_lock(paths, args.prism)
    _emit_result(
        {
            "command": "convert",
            "portable": not args.linked,
            "source_unchanged": True,
            "status": "ok",
        }
    )
    return EXIT_OK


def _unavailable(command: str) -> Callable[[argparse.Namespace], int]:
    def run(_: argparse.Namespace) -> int:
        raise ValueError(
            f"{command} requires the generation/verification component; inspect and model artifacts are available"
        )

    return run


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="to-prism")
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    doctor = subcommands.add_parser(
        "doctor", help="validate this transferred toolkit and optional Prism CLI"
    )
    doctor.add_argument("--prism", default="prism")
    doctor.add_argument("--require-prism", action="store_true")
    doctor.set_defaults(command_handler=_cmd_doctor)

    def paths(command: str, help_text: str) -> argparse.ArgumentParser:
        child = subcommands.add_parser(command, help=help_text)
        child.add_argument(
            "--source", required=True, help="read-only external project root"
        )
        child.add_argument(
            "--output", required=True, help="separate conversion output root"
        )
        child.add_argument("--dry-run", action="store_true")
        return child

    inspect = paths("inspect", "fingerprint and inventory without execution")
    inspect.add_argument(
        "--replace", action="store_true", help="replace an existing output atomically"
    )
    inspect.set_defaults(command_handler=_cmd_inspect)
    model = paths("model", "build conservative contracts and workflow graphs")
    model.set_defaults(command_handler=_cmd_model)
    baseline = paths(
        "baseline", "discover native baseline candidates without executing"
    )
    baseline.add_argument(
        "--authorize", action="store_true", help="execute one explicitly reviewed argv"
    )
    baseline.add_argument(
        "--command-json", help="JSON argv array; shell parsing is never used"
    )
    baseline.add_argument("--timeout", type=float, default=60.0)
    baseline.add_argument("--attempts", type=int, default=1)
    baseline.add_argument("--output-limit", type=int, default=65536)
    baseline.add_argument("--network", choices=("deny", "inherit"), default="deny")
    baseline.add_argument("--allow-credentials", action="store_true")
    baseline.set_defaults(command_handler=_cmd_baseline)
    update = paths("update", "re-inventory and invalidate affected decisions")
    update.set_defaults(command_handler=_cmd_update)
    generate = paths("generate", "render and check one reviewed Prism workflow")
    generate.add_argument(
        "--plan", required=True, help="reviewed semantic generation-plan JSON"
    )
    generate.add_argument("--prism", default="prism")
    generate.add_argument(
        "--handler",
        dest="prism_handler",
        choices=("fake", "codex", "litellm"),
        default="fake",
    )
    generate.set_defaults(portable=True)
    generate.add_argument(
        "--development-no-bundle",
        action="store_false",
        dest="portable",
        help="use an ambient Prism executable; development-only and never portable",
    )
    generate.add_argument("--prism-source")
    generate.add_argument("--wheelhouse")
    generate.add_argument(
        "--download-dependencies",
        action="store_true",
        help="authorize network downloads for missing third-party wheels",
    )
    generate.set_defaults(command_handler=_cmd_generate)
    verify = paths("verify", "verify generated canonical Prism through the public CLI")
    verify.add_argument("--prism", default="prism")
    verify.add_argument(
        "--handler",
        dest="prism_handler",
        choices=("fake", "codex", "litellm"),
        default="fake",
    )
    verify.add_argument("--portable", action="store_true")
    verify.add_argument("--skip-run", action="store_true")
    verify.set_defaults(command_handler=_cmd_verify)
    convert = paths(
        "convert", "inspect, model, generate, and publish through review gates"
    )
    convert.add_argument("--plan", help="approved generation-plan JSON")
    convert.add_argument("--prism", default="prism")
    convert.add_argument(
        "--handler",
        dest="prism_handler",
        choices=("fake", "codex", "litellm"),
        default="fake",
    )
    convert.add_argument(
        "--linked", action="store_true", help="do not claim portable output"
    )
    convert.add_argument("--prism-source")
    convert.add_argument("--wheelhouse")
    convert.add_argument(
        "--download-dependencies",
        action="store_true",
        help="authorize network downloads for missing third-party wheels",
    )
    convert.set_defaults(command_handler=_cmd_convert)
    validate = subcommands.add_parser(
        "validate", help="validate a versioned conversion artifact"
    )
    validate.add_argument("path")
    validate.add_argument(
        "--schema",
        choices=sorted(SCHEMA_FILES),
    )
    validate.set_defaults(command_handler=_cmd_validate)
    guard = subcommands.add_parser(
        "guard", help="evaluate one provider guard event from JSON stdin"
    )
    guard.add_argument(
        "--provider", required=True, choices=("codex", "claude", "opencode")
    )
    guard.add_argument("--event", required=True)
    guard.set_defaults(command_handler=_cmd_guard)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.command_handler(args))
    except (PathSafetyError, GuardRejection) as exc:
        sys.stderr.write(canonical_json({"error": str(exc), "status": "rejected"}))
        return EXIT_SAFETY
    except (SchemaValidationError, ValueError, FileNotFoundError, OSError) as exc:
        sys.stderr.write(canonical_json({"error": str(exc), "status": "failed"}))
        return EXIT_VALIDATION


if __name__ == "__main__":
    raise SystemExit(main())
