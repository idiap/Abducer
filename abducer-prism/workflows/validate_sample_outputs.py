# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Validate documentary sample payloads against the reasoning/type authority.

The sample layer deliberately stays outside the four semantic Prism layers.  This
validator supplies the missing cross-file contract: every reasoning binding must
have exactly one marker and one payload declaration, while Prism itself checks the
payload constructor and field types.  A marker names ``Generated[T]`` because that
is the real occurrence result; the source literal shows only the unwrapped ``T``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path


WORKFLOW_DIR = Path(__file__).parent
MARKER_RE = re.compile(
    r"^# @sample "
    r"workflow=(?P<workflow>\S+) "
    r"reasoning=(?P<reasoning>\S+) "
    r"binding=(?P<binding>\S+) "
    r"occurrence=(?P<occurrence>\S+) "
    r"output=(?P<output>Generated\[[^\]]+\]) "
    r"stage=(?P<stage>\d+) "
    r"branch=(?P<branch>\S+) "
    r"mode=(?P<mode>\S+) "
    r"example_set=(?P<example_set>\S+) "
    r"projection_status=(?P<projection_status>\S+)$"
)
BINDING_RE = re.compile(r"^\s*\[(?P<binding>[A-Za-z_]\w*):\s*(?P<occurrence>[A-Za-z_]\w*)\(")
OCCURRENCE_RE = re.compile(
    r"^type\s+(?P<name>[A-Za-z_]\w*)\s*=.*?->\s*Generated\[(?P<payload>[^\]]+)\]\s*$"
)
CONSTANT_RE = re.compile(
    r"^\s*sample_(?P<binding>[A-Za-z_]\w*)_value\s*:\s*(?P<payload>[A-Za-z_]\w*)\s*="
)
BUILDER_RE = re.compile(
    r"^\s*def\s+sample_(?P<binding>[A-Za-z_]\w*)_value_builder\(\)\s*->\s*(?P<payload>[A-Za-z_]\w*)\s*:"
)
PLACEHOLDER_RE = re.compile(r"\b(?:todo|tbd|placeholder|unknown|n/?a)\b|example output", re.I)


@dataclass(frozen=True)
class ExpectedStep:
    binding: str
    occurrence: str
    output: str
    stage: int
    branch: str


class SampleValidationError(ValueError):
    """Raised when a sample corpus breaks its source-grounded contract."""


def _workflow_id(path: Path) -> str:
    workflow_root = path.resolve().parents[1]
    manifest = json.loads((workflow_root / "manifest.json").read_text(encoding="utf-8"))
    source = f"{path.parent.name}/reasoning.prism"
    for item in manifest.get("workflows", []):
        if item.get("source") == source:
            return str(item["id"])
    return path.parent.name


def _occurrence_outputs(path: Path) -> dict[str, str]:
    outputs: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = OCCURRENCE_RE.match(line)
        if match:
            outputs[match.group("name")] = f"Generated[{match.group('payload')}]"
    return outputs


def _reasoning_steps(path: Path, occurrence_outputs: dict[str, str]) -> tuple[str, list[ExpectedStep]]:
    """Extract aliases and their source topology without treating prompt/file order as semantics."""
    lines = path.read_text(encoding="utf-8").splitlines()
    reasoning_match = next(
        (match for line in lines if (match := re.match(r"^reasoning\s+(\w+)\(", line))),
        None,
    )
    if reasoning_match is None:
        raise SampleValidationError(f"{path}: missing reasoning declaration")
    reasoning_name = reasoning_match.group(1)
    steps: list[ExpectedStep] = []
    stage = 0
    parallel_stack: list[tuple[int, int]] = []
    parallel_number = 0
    sequence_line = next((line for line in lines if line.strip() == "sequence:"), None)
    if sequence_line is None:
        raise SampleValidationError(f"{path}: missing sequence block")
    binding_indent = len(sequence_line) - len(sequence_line.lstrip()) + 4
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        while parallel_stack and indent <= parallel_stack[-1][0]:
            parallel_stack.pop()
        if indent == binding_indent and line.strip() == "parallel:":
            stage += 1
            parallel_number += 1
            parallel_stack.append((indent, parallel_number))
            continue
        if indent == binding_indent and line.lstrip().startswith("["):
            stage += 1
        binding_match = BINDING_RE.match(line)
        if binding_match is None:
            continue
        binding = binding_match.group("binding")
        occurrence = binding_match.group("occurrence")
        if occurrence not in occurrence_outputs:
            raise SampleValidationError(f"{path}: {binding} references unknown occurrence {occurrence}")
        branch = "main"
        if parallel_stack:
            # Branch names stay reader-facing; shared stage plus the source order
            # of the enclosing parallel block carries the topology coordinate.
            branch = binding
        steps.append(ExpectedStep(binding, occurrence, occurrence_outputs[occurrence], stage, branch))
    if not steps:
        raise SampleValidationError(f"{path}: no reasoning bindings found")
    return reasoning_name, steps


def _sample_blocks(path: Path) -> list[tuple[dict[str, str], str, int]]:
    blocks: list[tuple[dict[str, str], str, int]] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines):
        marker = MARKER_RE.match(line)
        if marker is None:
            continue
        end = next((j for j in range(index + 1, len(lines)) if lines[j].startswith("# @sample ")), len(lines))
        blocks.append((marker.groupdict(), "\n".join(lines[index + 1 : end]), index + 1))
    return blocks


def _alignment_digest(path: Path) -> str:
    """Hash only stable marker metadata so prose edits do not hide graph drift."""
    markers = [line for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("# @sample ")]
    return hashlib.sha256(("\n".join(markers) + "\n").encode()).hexdigest()


def _validate_file(path: Path) -> dict[str, object]:
    workflow = _workflow_id(path)
    reasoning_path = path.parent / "reasoning.prism"
    occurrence_path = path.parent / "occurrences.prism"
    occurrence_outputs = _occurrence_outputs(occurrence_path)
    reasoning, expected = _reasoning_steps(reasoning_path, occurrence_outputs)
    blocks = _sample_blocks(path)
    if len(blocks) != len(expected):
        raise SampleValidationError(f"{path}: expected {len(expected)} markers, found {len(blocks)}")
    seen: set[str] = set()
    example_sets: set[str] = set()
    for (metadata, body, line_number), expected_step in zip(blocks, expected, strict=True):
        key = f"{workflow}::{reasoning}::{metadata['binding']}"
        if key in seen:
            raise SampleValidationError(f"{path}:{line_number}: duplicate alignment key {key}")
        seen.add(key)
        checks = {
            "workflow": workflow,
            "reasoning": reasoning,
            "binding": expected_step.binding,
            "occurrence": expected_step.occurrence,
            "output": expected_step.output,
            "stage": str(expected_step.stage),
            "branch": expected_step.branch,
            "mode": "simulated",
        }
        for field, wanted in checks.items():
            if metadata[field] != wanted:
                raise SampleValidationError(
                    f"{path}:{line_number}: {field}={metadata[field]!r}, expected {wanted!r}"
                )
        if metadata["projection_status"] not in {"resolved", "unresolved"}:
            raise SampleValidationError(f"{path}:{line_number}: invalid projection_status")
        expected_projection = "unresolved" if expected_step.occurrence.startswith("Unresolved") else "resolved"
        if metadata["projection_status"] != expected_projection:
            raise SampleValidationError(f"{path}:{line_number}: projection status does not match occurrence")
        example_sets.add(metadata["example_set"])
        if PLACEHOLDER_RE.search(body):
            raise SampleValidationError(f"{path}:{line_number}: placeholder text in sample body")
        if not re.search(r"\b(sample_[A-Za-z_]\w*_value(?:_builder)?|def)\b", body):
            raise SampleValidationError(f"{path}:{line_number}: marker has no payload declaration")
    if len(example_sets) != 1:
        raise SampleValidationError(f"{path}: expected one coherent example_set, found {sorted(example_sets)}")
    allowed_import = f"from workflows.{path.parent.name}.types import"
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("from ") and not line.startswith(allowed_import):
            raise SampleValidationError(f"{path}: sample imports outside its types module")
        if re.match(r"^(type|workflow|reasoning|relation|agent|tool)\s", line):
            raise SampleValidationError(f"{path}: sample declares a semantic/material construct")
    declared = {m.group("binding"): m.group("payload") for m in map(CONSTANT_RE.match, path.read_text(encoding="utf-8").splitlines()) if m}
    declared.update({m.group("binding"): m.group("payload") for m in map(BUILDER_RE.match, path.read_text(encoding="utf-8").splitlines()) if m})
    for metadata, _, line_number in blocks:
        binding = metadata["binding"]
        if binding not in declared:
            raise SampleValidationError(f"{path}:{line_number}: no typed declaration for {binding}")
        payload = metadata["output"][len("Generated[") : -1]
        if declared[binding] != payload:
            raise SampleValidationError(f"{path}:{line_number}: declaration payload disagrees with marker")
    return {"step_count": len(blocks), "alignment_sha256": _alignment_digest(path)}


def validate(workflow_root: Path = WORKFLOW_DIR) -> dict[str, object]:
    """Validate all workflow sample siblings and return stable coverage evidence."""
    paths = sorted(workflow_root.glob("*/sample_outputs.prism"))
    if len(paths) != 19:
        raise SampleValidationError(f"expected 19 sample modules, found {len(paths)}")
    per_workflow = {path.parent.name: _validate_file(path) for path in paths}
    binding_count = sum(item["step_count"] for item in per_workflow.values())
    if binding_count != 65:
        raise SampleValidationError(f"expected 65 bindings, found {binding_count}")
    manifest = json.loads((workflow_root / "manifest.json").read_text(encoding="utf-8"))
    manifest_by_source = {item["source"].split("/")[0]: item for item in manifest["workflows"]}
    for module, item in per_workflow.items():
        entry = manifest_by_source.get(module)
        if entry is None or "sample_outputs" not in entry:
            raise SampleValidationError(f"{module}: manifest sample_outputs metadata missing")
        sample = entry["sample_outputs"]
        expected_path = f"{module}/sample_outputs.prism"
        if sample.get("path") != expected_path:
            raise SampleValidationError(f"{module}: unsafe sample path")
        path = workflow_root / sample["path"]
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        if sample["sha256"] != f"sha256:{actual_hash}":
            raise SampleValidationError(f"{module}: manifest sample hash drift")
        if sample["step_count"] != item["step_count"]:
            raise SampleValidationError(f"{module}: manifest sample step count drift")
        if sample["alignment_sha256"] != f"sha256:{item['alignment_sha256']}":
            raise SampleValidationError(f"{module}: manifest sample alignment drift")
    bundle = "\n".join(
        f"{workflow}:{item['step_count']}:{hashlib.sha256((workflow_root / workflow / 'sample_outputs.prism').read_bytes()).hexdigest()}:{item['alignment_sha256']}"
        for workflow, item in sorted(per_workflow.items())
    )
    bundle_hash = hashlib.sha256(bundle.encode()).hexdigest()
    root_bundle = manifest.get("sample_outputs_bundle", {}).get("sha256")
    if root_bundle != f"sha256:{bundle_hash}":
        raise SampleValidationError("manifest sample_outputs_bundle hash drift")
    return {
        "workflow_count": len(paths),
        "binding_count": binding_count,
        "per_workflow": per_workflow,
        "sample_bundle_sha256": bundle_hash,
    }


def self_test() -> None:
    """Reject a binding-marker mutation and a placeholder payload mutation."""
    import shutil
    import tempfile

    mutations = (
        ("marker", "binding=search_scope", "binding=wrong_binding"),
        ("payload", "sample_search_scope_value", "sample_search_scope_value # TODO"),
    )
    for label, before, after in mutations:
        with tempfile.TemporaryDirectory(prefix=f"abducer-prism-samples-{label}-") as temporary:
            root = Path(temporary) / "workflows"
            shutil.copytree(WORKFLOW_DIR, root)
            target = root / "discovery_marathon_loop" / "sample_outputs.prism"
            text = target.read_text(encoding="utf-8")
            if before not in text:
                raise SampleValidationError(f"self-test mutation anchor missing: {label}")
            target.write_text(text.replace(before, after, 1), encoding="utf-8")
            try:
                validate(root)
            except SampleValidationError:
                continue
            raise SampleValidationError(f"self-test mutation was not rejected: {label}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit stable JSON evidence")
    parser.add_argument("--self-test", action="store_true", help="run adversarial mutation checks")
    args = parser.parse_args()
    evidence = validate()
    if args.self_test:
        self_test()
    if args.json:
        import json

        print(json.dumps(evidence, indent=2, sort_keys=True))
    else:
        print(f"sample-modules={evidence['workflow_count']}")
        print(f"sample-bindings={evidence['binding_count']}")
        print(f"sample-bundle-sha256={evidence['sample_bundle_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
