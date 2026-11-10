# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Validate the exact Abducer workflow trace, not merely artifact counts.

The fixture binds three layers together: the former ERFL source at one immutable
Git revision, the current typed Prism source, and the compiler's normalized
reasoning-composition IR. A source change is therefore review-visible even when
it preserves node counts. Policy clauses are normalized separately so trigger,
destination, accept, and stop mutations cannot hide behind equal cardinality.

This validator establishes structural trace preservation only. It does not run
handlers, execute cross-workflow routing, or establish behavioral equivalence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Iterator
from zipfile import ZipFile


WORKFLOW_DIR = Path(__file__).resolve().parent
TOOLKIT_ROOT = WORKFLOW_DIR.parent
REPO_ROOT = TOOLKIT_ROOT.parent
FIXTURE_PATH = WORKFLOW_DIR / "topology-fixture.json"
CATALOG_PATH = REPO_ROOT / "agentic/registries/reasoning_flow_catalog.yaml"
MANIFEST_PATH = WORKFLOW_DIR / "manifest.json"
PRISM_PATH = Path(os.environ.get("PRISM_PATH", TOOLKIT_ROOT / ".venv/bin/prism"))
ARCHIVE_PATH = Path(
    os.environ.get("TO_PRISM_ARCHIVE", "/Users/afreitas/Documents/to_prism.zip")
)
RETIRED_ARCHIVE_PREFIX = ("to_prism", ".venv")
EXPECTED_WORKFLOW_COUNT = 19
EXPECTED_LAYERS = ("types", "occurrences", "relations", "reasoning")


class ValidationError(RuntimeError):
    """Signal one mismatch between immutable evidence and delivered structure."""


def _sha256(data: bytes) -> str:
    """Return a stable lowercase digest for source, fixture, or compiler bytes."""

    return hashlib.sha256(data).hexdigest()


def _file_sha256(path: Path) -> str:
    """Hash one potentially large file without retaining all bytes in memory."""

    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    """Read one JSON object and reject non-object top-level values."""

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValidationError(f"expected JSON object: {path}")
    return value


def _git_bytes(revision: str, relative_path: str) -> bytes:
    """Read an immutable repository object without restoring it to the worktree."""

    return subprocess.run(
        ["git", "-C", str(REPO_ROOT), "show", f"{revision}:{relative_path}"],
        check=True,
        capture_output=True,
    ).stdout


def _former_trace(text: str) -> tuple[str, list[str]]:
    """Extract the exact ERFL route and ordered policy clauses from one source."""

    logical = [line.strip() for line in text.splitlines() if line.strip()]
    routes = [line.removeprefix("route ") for line in logical if line.startswith("route ")]
    if len(routes) != 1:
        raise ValidationError(f"expected one ERFL route, found {len(routes)}")
    policies = [line.removeprefix("on ") for line in logical if line.startswith("on ")]
    return routes[0], policies


def _normalized_policy_outcomes(clauses: list[str]) -> list[str]:
    """Normalize exact ERFL guards/actions to the manifest's durable vocabulary."""

    outcomes: list[str] = []
    for clause in clauses:
        condition, action = (part.strip() for part in clause.split("=>", 1))
        status = condition.split(".", 1)[1]
        if action.startswith("switch @"):
            outcomes.append(action.removeprefix("switch @"))
        elif action == "accept":
            outcomes.append(f"accept:{status}")
        elif action == "stop":
            outcomes.append(f"stop:{status}")
        else:
            raise ValidationError(f"unsupported policy action: {action}")
    return outcomes


def _prism_source_argument(source: Path, project_root: Path) -> str:
    """Return a project-root-relative source path for deterministic imports."""

    try:
        return str(source.resolve().relative_to(project_root.resolve()))
    except ValueError as error:
        raise ValidationError(f"source escapes Prism project root: {source}") from error


def _compile_document(source: Path, project_root: Path = TOOLKIT_ROOT) -> dict[str, Any]:
    """Compile a workflow from its module root and return public Prism JSON IR."""

    completed = subprocess.run(
        [str(PRISM_PATH), "compile", _prism_source_argument(source, project_root)],
        check=True,
        capture_output=True,
        text=True,
        cwd=project_root,
    )
    value = json.loads(completed.stdout)
    if not isinstance(value, dict):
        raise ValidationError(f"compiler returned non-object IR for {source.name}")
    return value


def _check_source(source: Path, project_root: Path = TOOLKIT_ROOT) -> None:
    """Check a source with imports rooted in its containing Prism project."""

    subprocess.run(
        [str(PRISM_PATH), "check", _prism_source_argument(source, project_root)],
        check=True,
        capture_output=True,
        text=True,
        cwd=project_root,
    )


def _composition(document: dict[str, Any]) -> dict[str, Any]:
    """Select the one reasoning declaration that carries composition topology."""

    declarations = [
        item
        for item in document.get("declarations", [])
        if isinstance(item, dict) and "composition" in item
    ]
    if len(declarations) != 1:
        raise ValidationError(
            f"expected one compiled reasoning composition, found {len(declarations)}"
        )
    declaration = declarations[0]
    return {
        "name": declaration.get("name"),
        "parameters": declaration.get("parameters"),
        "return_type": declaration.get("return_type"),
        "composition": declaration.get("composition"),
    }


def _canonical_hash(value: Any) -> str:
    """Hash normalized JSON so key ordering cannot change trace identity."""

    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return _sha256(encoded)


def _top_level_declarations(source: str) -> list[tuple[str, str]]:
    """Return declaration kind/name pairs without interpreting nested syntax."""

    return re.findall(
        r"^(type|relation|reasoning|def|agent|workflow)\s+([A-Za-z_][A-Za-z0-9_]*)",
        source,
        flags=re.MULTILINE,
    )


def _validate_layer_shape(workflow_dir: Path, manifest_items: list[dict[str, Any]]) -> None:
    """Enforce the example-derived semantic ownership of all four Prism layers."""

    expected_files: set[Path] = set()
    allowed = {
        "types": {"type"},
        "occurrences": {"type"},
        "relations": {"type", "relation"},
        "reasoning": {"reasoning"},
    }
    for item in manifest_items:
        module_id = item.get("module_id")
        if not isinstance(module_id, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", module_id):
            raise ValidationError(f"{item.get('id')}: invalid Prism module id")
        layers = item.get("layers")
        if not isinstance(layers, dict) or tuple(layers) != EXPECTED_LAYERS:
            raise ValidationError(f"{item.get('id')}: expected exactly four ordered layers")
        layer_hashes = item.get("layer_hashes")
        if not isinstance(layer_hashes, dict) or tuple(layer_hashes) != EXPECTED_LAYERS:
            raise ValidationError(f"{item.get('id')}: expected one hash per layer")

        for layer in EXPECTED_LAYERS:
            relative = Path(layers[layer])
            if relative != Path(module_id, f"{layer}.prism"):
                raise ValidationError(f"{item.get('id')}: unsafe or drifted {layer} path")
            path = workflow_dir / relative
            if not path.is_file():
                raise ValidationError(f"{item.get('id')}: missing {layer}.prism")
            actual_hash = f"sha256:{_sha256(path.read_bytes())}"
            if layer_hashes[layer] != actual_hash:
                raise ValidationError(f"{item.get('id')}: {layer} layer hash drift")
            expected_files.add(path.resolve())
            source = path.read_text(encoding="utf-8")
            declarations = _top_level_declarations(source)
            forbidden = [kind for kind, _ in declarations if kind not in allowed[layer]]
            if forbidden:
                raise ValidationError(f"{item.get('id')}: forbidden {forbidden[0]} in {layer}.prism")
            if layer == "reasoning" and sum(kind == "reasoning" for kind, _ in declarations) != 1:
                raise ValidationError(f"{item.get('id')}: reasoning layer must own one graph")
            if layer == "occurrences":
                aliases = re.findall(r"^type\s+\w+\s*=\s*(.+)$", source, flags=re.MULTILINE)
                if not aliases or any("-> Generated[" not in alias for alias in aliases):
                    raise ValidationError(f"{item.get('id')}: invalid occurrence provenance")
            if layer == "types" and re.search(r"^type\s+\w+\s*=", source, flags=re.MULTILINE):
                raise ValidationError(f"{item.get('id')}: callable alias belongs in occurrences")
            if layer == "relations" and not any(kind == "relation" for kind, _ in declarations):
                raise ValidationError(f"{item.get('id')}: relation layer has no relation")

    # Upper materialization/application modules are validated independently.  This
    # historical gate continues to own the exact four-layer semantic baseline.
    observed_files = {
        path.resolve()
        for path in workflow_dir.glob("*/*.prism")
        if path.stem in EXPECTED_LAYERS
    }
    if observed_files != expected_files:
        raise ValidationError("layered Prism file set differs from manifest")


def _is_retired_runtime_member(member_name: str) -> bool:
    """Return whether a ZIP member belongs to the deliberately removed old venv."""

    return Path(member_name).parts[:2] == RETIRED_ARCHIVE_PREFIX


def _validate_archive_extraction(fixture: dict[str, Any]) -> None:
    """Require every retained reference member to be byte-identical after extraction."""

    if not ARCHIVE_PATH.is_file():
        raise ValidationError(f"source archive is required for parity: {ARCHIVE_PATH}")
    if _file_sha256(ARCHIVE_PATH) != fixture["archive_sha256"]:
        raise ValidationError("source archive differs from reviewed fixture")

    file_count = 0
    with ZipFile(ARCHIVE_PATH) as archive:
        for member in archive.infolist():
            if member.is_dir() or _is_retired_runtime_member(member.filename):
                continue
            parts = Path(member.filename).parts
            if len(parts) < 2 or parts[0] != "to_prism":
                raise ValidationError(f"archive member has unexpected root: {member.filename}")
            extracted = TOOLKIT_ROOT.joinpath(*parts[1:])
            file_count += 1
            if not extracted.is_file() or extracted.is_symlink():
                raise ValidationError(f"archive member missing or non-regular: {member.filename}")
            digest = hashlib.sha256()
            with archive.open(member) as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
            if _file_sha256(extracted) != digest.hexdigest():
                raise ValidationError(f"archive member byte drift: {member.filename}")
    if file_count != fixture["archive_file_count"]:
        raise ValidationError(
            f"archive file count drift: expected {fixture['archive_file_count']}, found {file_count}"
        )


def _archive_file_count() -> int:
    """Count retained reference members while excluding the retired old venv."""

    with ZipFile(ARCHIVE_PATH) as archive:
        return sum(
            1
            for member in archive.infolist()
            if not member.is_dir() and not _is_retired_runtime_member(member.filename)
        )


def _occurrences(value: Any) -> Iterator[dict[str, Any]]:
    """Yield compiled occurrence nodes recursively across sequence/parallel groups."""

    if isinstance(value, dict):
        if "alias" in value and "component" in value and "output_type" in value:
            yield value
        for child in value.values():
            yield from _occurrences(child)
    elif isinstance(value, list):
        for child in value:
            yield from _occurrences(child)


def _assert_all_generated(composition: dict[str, Any], workflow_id: str) -> None:
    """Require generated provenance for every compiled epistemic occurrence."""

    nodes = list(_occurrences(composition))
    if not nodes:
        raise ValidationError(f"{workflow_id}: compiled composition has no occurrences")
    raw = [node.get("alias") for node in nodes if node.get("output_type", {}).get("name") != "Generated"]
    if raw:
        raise ValidationError(f"{workflow_id}: non-generated occurrences: {raw}")


def _fixture_entry(
    workflow_id: str,
    source_name: str,
    revision: str,
    manifest_item: dict[str, Any],
) -> dict[str, Any]:
    """Build one review fixture entry from immutable and compiled evidence."""

    former_path = f"agentic/reasoning_flows/{workflow_id}.rflow"
    former_bytes = _git_bytes(revision, former_path)
    route, policies = _former_trace(former_bytes.decode("utf-8"))
    source_path = WORKFLOW_DIR / source_name
    sample_meta = manifest_item.get("sample_outputs")
    if not isinstance(sample_meta, dict):
        raise ValidationError(f"{workflow_id}: manifest has no sample_outputs metadata")
    sample_name = sample_meta.get("path")
    sample_relative = Path(sample_name) if isinstance(sample_name, str) else Path()
    if (
        not isinstance(sample_name, str)
        or sample_relative.is_absolute()
        or ".." in sample_relative.parts
        or sample_relative != Path(workflow_id, "sample_outputs.prism")
    ):
        raise ValidationError(f"{workflow_id}: unsafe sample_outputs path")
    sample_path = WORKFLOW_DIR / sample_name
    if not sample_path.is_file():
        raise ValidationError(f"{workflow_id}: sample_outputs.prism is missing")
    sample_alignment = sample_meta.get("alignment_sha256")
    if not isinstance(sample_alignment, str) or not sample_alignment.startswith("sha256:"):
        raise ValidationError(f"{workflow_id}: invalid sample alignment digest")
    document = _compile_document(source_path, TOOLKIT_ROOT)
    composition = _composition(document)
    _assert_all_generated(composition, workflow_id)
    return {
        "id": workflow_id,
        "former_source": former_path,
        "former_sha256": _sha256(former_bytes),
        "former_route": route,
        "policy_clauses": policies,
        "prism_source": source_name,
        "prism_sha256": _sha256(source_path.read_bytes()),
        "compiled_composition_sha256": _canonical_hash(composition),
        "projection_status": manifest_item["catalog_projection_status"],
        "sample_outputs": {
            "path": sample_name,
            "sha256": _sha256(sample_path.read_bytes()),
            "alignment_sha256": sample_alignment.removeprefix("sha256:"),
            "step_count": sample_meta.get("step_count"),
        },
    }


def build_fixture() -> dict[str, Any]:
    """Build the exhaustive fixture for review; callers decide whether to persist it."""

    manifest = _read_json(MANIFEST_PATH)
    revision = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    items = manifest.get("workflows", [])
    if len(items) != EXPECTED_WORKFLOW_COUNT:
        raise ValidationError(f"manifest must contain {EXPECTED_WORKFLOW_COUNT} workflows")
    entries = [
        _fixture_entry(item["id"], item["source"], revision, item)
        for item in items
    ]
    bundle_digest = _canonical_hash(
        sorted([[entry["id"], entry["prism_sha256"]] for entry in entries])
    )
    sample_bundle = manifest.get("sample_outputs_bundle")
    if not isinstance(sample_bundle, dict) or not isinstance(sample_bundle.get("sha256"), str):
        raise ValidationError("manifest has no sample_outputs_bundle digest")
    return {
        "schema_version": "1.0.0",
        "evidence_level": "reviewed-structural-trace",
        "source_revision": revision,
        "archive_sha256": _file_sha256(ARCHIVE_PATH),
        "archive_file_count": _archive_file_count(),
        "catalog_sha256": _sha256(CATALOG_PATH.read_bytes()),
        "manifest_sha256": _sha256(MANIFEST_PATH.read_bytes()),
        "prism_executable_sha256": _sha256(PRISM_PATH.read_bytes()),
        "source_bundle_sha256": bundle_digest,
        "sample_outputs_bundle_sha256": sample_bundle["sha256"].removeprefix("sha256:"),
        "workflow_count": EXPECTED_WORKFLOW_COUNT,
        "workflows": entries,
    }


def validate(workflow_dir: Path = WORKFLOW_DIR) -> None:
    """Validate an installed bundle against the reviewed exhaustive fixture."""

    fixture = _read_json(FIXTURE_PATH)
    manifest = _read_json(workflow_dir / "manifest.json")
    catalog = _read_json(CATALOG_PATH)
    entries = fixture.get("workflows", [])
    manifest_items = manifest.get("workflows", [])
    catalog_items = catalog.get("flows", [])
    _validate_layer_shape(workflow_dir, manifest_items)
    for label, items in (
        ("fixture", entries),
        ("manifest", manifest_items),
        ("catalog", catalog_items),
    ):
        if len(items) != EXPECTED_WORKFLOW_COUNT:
            raise ValidationError(f"{label} must contain exactly {EXPECTED_WORKFLOW_COUNT} workflows")

    fixture_by_id = {item["id"]: item for item in entries}
    manifest_by_id = {item["id"]: item for item in manifest_items}
    catalog_by_id = {item["id"]: item for item in catalog_items}
    expected_ids = set(fixture_by_id)
    if any(len(mapping) != EXPECTED_WORKFLOW_COUNT for mapping in (fixture_by_id, manifest_by_id, catalog_by_id)):
        raise ValidationError("workflow IDs must be unique in fixture, manifest, and catalog")
    if set(manifest_by_id) != expected_ids or set(catalog_by_id) != expected_ids:
        raise ValidationError("fixture, manifest, and catalog ID sets differ")

    source_names = [item["source"] for item in manifest_items]
    if len(set(source_names)) != EXPECTED_WORKFLOW_COUNT:
        raise ValidationError("manifest source paths must be unique")
    if _sha256(CATALOG_PATH.read_bytes()) != fixture["catalog_sha256"]:
        raise ValidationError("catalog bytes differ from reviewed fixture")
    if _sha256((workflow_dir / "manifest.json").read_bytes()) != fixture["manifest_sha256"]:
        raise ValidationError("manifest bytes differ from reviewed fixture")
    if _sha256(PRISM_PATH.read_bytes()) != fixture["prism_executable_sha256"]:
        raise ValidationError("Prism executable differs from reviewed fixture")
    expected_manifest_provenance = {
        "source_revision": fixture["source_revision"],
        "archive_sha256": fixture["archive_sha256"],
        "catalog_sha256": fixture["catalog_sha256"],
        "runtime": "abducer-prism/vendor/wheels (transient extracted Prism CLI)",
        "topology_fixture": FIXTURE_PATH.name,
    }
    for field, expected_value in expected_manifest_provenance.items():
        if manifest.get(field) != expected_value:
            raise ValidationError(f"manifest provenance drift: {field}")
    _validate_archive_extraction(fixture)

    bundle_rows: list[list[str]] = []
    for workflow_id in sorted(expected_ids):
        expected = fixture_by_id[workflow_id]
        manifest_item = manifest_by_id[workflow_id]
        catalog_item = catalog_by_id[workflow_id]
        source_name = manifest_item["source"]
        relative_source = Path(source_name)
        if (
            source_name != expected["prism_source"]
            or relative_source.is_absolute()
            or ".." in relative_source.parts
            or relative_source.name != "reasoning.prism"
        ):
            raise ValidationError(f"{workflow_id}: unsafe or drifted manifest source")
        source_path = workflow_dir / relative_source
        if not source_path.is_file():
            raise ValidationError(f"{workflow_id}: manifest source does not resolve")
        if _sha256(source_path.read_bytes()) != expected["prism_sha256"]:
            raise ValidationError(f"{workflow_id}: Prism source differs from reviewed fixture")
        if catalog_item["projection_status"] != expected["projection_status"]:
            raise ValidationError(f"{workflow_id}: catalog projection status drift")
        if manifest_item["catalog_projection_status"] != expected["projection_status"]:
            raise ValidationError(f"{workflow_id}: manifest projection status drift")

        former_bytes = _git_bytes(fixture["source_revision"], expected["former_source"])
        former_route, policy_clauses = _former_trace(former_bytes.decode("utf-8"))
        if _sha256(former_bytes) != expected["former_sha256"]:
            raise ValidationError(f"{workflow_id}: former source hash drift")
        if former_route != expected["former_route"] or policy_clauses != expected["policy_clauses"]:
            raise ValidationError(f"{workflow_id}: former route or policy trace drift")
        if manifest_item["policy_outcomes"] != _normalized_policy_outcomes(policy_clauses):
            raise ValidationError(f"{workflow_id}: policy trigger/action mapping drift")

        project_root = workflow_dir.parent
        _check_source(source_path, project_root)
        document = _compile_document(source_path, project_root)
        composition = _composition(document)
        _assert_all_generated(composition, workflow_id)
        if _canonical_hash(composition) != expected["compiled_composition_sha256"]:
            raise ValidationError(f"{workflow_id}: compiled topology/type trace drift")
        bundle_rows.append([workflow_id, expected["prism_sha256"]])

    if _canonical_hash(bundle_rows) != fixture["source_bundle_sha256"]:
        raise ValidationError("source bundle digest drift")

    sample_bundle = manifest.get("sample_outputs_bundle")
    if not isinstance(sample_bundle, dict):
        raise ValidationError("manifest sample_outputs_bundle metadata is missing")
    if sample_bundle.get("sha256", "").removeprefix("sha256:") != fixture.get(
        "sample_outputs_bundle_sha256"
    ):
        raise ValidationError("sample outputs bundle digest drift")
    for workflow_id in sorted(expected_ids):
        expected = fixture_by_id[workflow_id]
        manifest_item = manifest_by_id[workflow_id]
        sample_meta = manifest_item.get("sample_outputs")
        expected_sample = expected.get("sample_outputs")
        if not isinstance(sample_meta, dict) or not isinstance(expected_sample, dict):
            raise ValidationError(f"{workflow_id}: sample outputs fixture metadata missing")
        if sample_meta.get("path") != expected_sample.get("path"):
            raise ValidationError(f"{workflow_id}: sample outputs path drift")
        sample_path = workflow_dir / sample_meta["path"]
        if not sample_path.is_file():
            raise ValidationError(f"{workflow_id}: sample outputs source is missing")
        if _sha256(sample_path.read_bytes()) != expected_sample.get("sha256"):
            raise ValidationError(f"{workflow_id}: sample outputs source differs from fixture")
        if sample_meta.get("alignment_sha256", "").removeprefix("sha256:") != expected_sample.get(
            "alignment_sha256"
        ):
            raise ValidationError(f"{workflow_id}: sample outputs alignment drift")
        if sample_meta.get("step_count") != expected_sample.get("step_count"):
            raise ValidationError(f"{workflow_id}: sample outputs step count drift")


def self_test() -> None:
    """Prove relation, parallel, and policy mutations fail the reviewed gate."""

    mutations = (
        (
            "reasoning-ownership",
            "discovery_marathon_loop/reasoning.prism",
            "reasoning DiscoveryMarathonLoop(",
            "type MisplacedDomainRecord:\n    value: String\n\nreasoning DiscoveryMarathonLoop(",
        ),
        (
            "types-ownership",
            "discovery_marathon_loop/types.prism",
            "type DiscoveryRunContext:",
            "type MisplacedOccurrence = String -> String\n\ntype DiscoveryRunContext:",
        ),
        (
            "relation",
            "discovery_marathon_loop/reasoning.prism",
            "by ScopesDiscoveryFormation",
            "by GroundsDiscoveryRefutation",
        ),
        ("parallel", "discovery_marathon_loop/reasoning.prism", "parallel:", "sequence:"),
        ("policy", "manifest.json", "release_promotion_loop", "wrong_release_target"),
        (
            "provenance",
            "manifest.json",
            '"source_revision": "f90f0c6fe08f0a14884d8a2bdda611a81ccf72bf"',
            '"source_revision": "0000000000000000000000000000000000000000"',
        ),
    )
    for label, relative_path, before, after in mutations:
        with tempfile.TemporaryDirectory(prefix=f"abducer-prism-{label}-") as temporary:
            mutated = Path(temporary) / "workflows"
            shutil.copytree(WORKFLOW_DIR, mutated)
            target = mutated / relative_path
            original = target.read_text(encoding="utf-8")
            if before not in original:
                raise ValidationError(f"self-test mutation anchor missing: {label}")
            target.write_text(original.replace(before, after, 1), encoding="utf-8")
            try:
                validate(mutated)
            except (ValidationError, subprocess.CalledProcessError):
                continue
            raise ValidationError(f"self-test mutation was not rejected: {label}")


def main() -> int:
    """Expose fixture printing, validation, and adversarial regression modes."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--print-fixture", action="store_true")
    parser.add_argument(
        "--write-fixture",
        action="store_true",
        help="atomically refresh the reviewed fixture after an intentional bundle change",
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.print_fixture:
        print(json.dumps(build_fixture(), indent=2, sort_keys=True))
        return 0
    if args.write_fixture:
        document = json.dumps(build_fixture(), indent=2, sort_keys=True) + "\n"
        temporary = FIXTURE_PATH.with_suffix(".json.tmp")
        temporary.write_text(document, encoding="utf-8")
        temporary.replace(FIXTURE_PATH)
        print(f"wrote reviewed fixture: {FIXTURE_PATH}")
        return 0
    validate()
    if args.self_test:
        self_test()
    print("validated exhaustive 19-workflow topology, types, policies, provenance")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
