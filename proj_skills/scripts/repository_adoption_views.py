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
"""Project immutable historical records through Abducer's existing public views.

This maintenance interface never dispatches a scientific operation. Native trace
packets use the existing monitor builder and HTML renderer; unknown legacy JSON
gets an explicit archival view. The manifest binds source bytes, view bytes and
rendering metadata, without inventing missing historical invocation identities.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import html
import importlib.util
import json
import re
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PROJECTION_VERSION = "abducer.repository-adoption-view/v1"
OUTPUT_NAMES = ("projection.json", "view.html")
# Freeze the currently reviewed claim boundary, including indentation and order.
# Blank/comment-only lines and trailing spaces are excluded; code changes fail.
RELEASE_BASELINE = {
    "types.prism": "f953a0683f94f436bbb9a85bad52bd84071ed94c81698baa6e257c15c6b4c7fa",
    "occurrences.prism": "ed0ebb94486315bb1d75121a425b3dfd98599efd5b815113043e5e64fa7c04d3",
    "relations.prism": "474fcd3babc84cc6311e927d62401cf8c077eea612a0f26f8045bba23a4bd565",
    "reasoning.prism": "1520cb07d1615dc34eb8dedde3680bbc91e4873b810e52d5c21c86c6ed168fa9",
}


class ViewError(ValueError):
    """A view cannot safely claim a supported source or intact artifact join."""


def _digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def _read_json(raw: bytes) -> Any:
    """Reject duplicate keys and non-JSON floats instead of losing source facts."""
    def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in rows:
            if key in result:
                raise ViewError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def invalid_constant(value: str) -> None:
        raise ViewError(f"non-JSON numeric constant: {value}")

    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=invalid_constant)


def _module(filename: str):
    """Import a fixed repository renderer; invocation input cannot select code."""
    path = ROOT / "agentic/scripts" / filename
    spec = importlib.util.spec_from_file_location("_adoption_" + path.stem, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    previous = sys.path[:]
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = previous
    return module


def _records(source: Any) -> list[dict[str, Any]]:
    """Keep raw records and JSON pointers; labels are presentation, never facts."""
    if isinstance(source, dict):
        field = next((key for key in ("events", "timeline", "entries") if isinstance(source.get(key), list)), None)
        rows = [(f"/{field}/{i}", row) for i, row in enumerate(source[field])] if field else [("", source)]
    elif isinstance(source, list):
        rows = [(f"/{i}", row) for i, row in enumerate(source)]
    else:
        rows = [("", source)]
    result = []
    for pointer, row in rows:
        obj = row if isinstance(row, dict) else {}
        inference = obj.get("public_inference") if isinstance(obj.get("public_inference"), dict) else {}
        skill = obj.get("skill") or obj.get("skill_id")
        rationale = obj.get("rationale_summary") or obj.get("warrant") or inference.get("warrant")
        mapping = obj.get("reasoning_types") or obj.get("operator") or inference.get("operator")
        result.append({"source_pointer": pointer, "record": copy.deepcopy(row), "display": {
            "skill": skill if skill else "No skill recorded",
            "rationale": rationale if rationale else "Rationale not recorded",
            "reasoning_mapping": mapping if mapping else "Unassigned",
        }})
    return result


def _record_html(records: list[dict[str, Any]]) -> str:
    sections = []
    for entry in records:
        display = entry["display"]
        def escaped(value: Any) -> str:
            return html.escape(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False))
        sections.append('<article><h3>' + escaped(display["skill"]) + '</h3><dl>'
                        '<dt>Source pointer</dt><dd>' + escaped(entry["source_pointer"] or "/ (document)") + '</dd>'
                        '<dt>Reasoning mapping</dt><dd>' + escaped(display["reasoning_mapping"]) + '</dd>'
                        '<dt>Public rationale</dt><dd>' + escaped(display["rationale"]) + '</dd></dl>'
                        '<details><summary>Unchanged source record</summary><pre>' + escaped(entry["record"]) + '</pre></details></article>')
    return '<section aria-label="Historical source records"><h2>Historical source records</h2>' + ''.join(sections) + '</section>'


def _native_view(source: Any) -> tuple[str | None, str, dict[str, Any], Any]:
    """Use existing presentation routes only for their recognized native shapes."""
    if not isinstance(source, dict):
        return None, "legacy-json", {}, None
    is_trace = "events" in source and "declared_route" in source and "identity" in source
    is_packet = "timeline" in source and "lens" in source and "identity" in source
    if not (is_trace or is_packet):
        return None, "legacy-json", {}, None
    version = "2.0" if is_trace else "1.0"
    if source.get("schema_version") != version:
        raise ViewError(f"unsupported native {'trace' if is_trace else 'packet'} version")
    if not isinstance(source["identity"], dict):
        raise ViewError("native identity must be an object")
    rows = source.get("events" if is_trace else "timeline")
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ViewError("native records must be objects")
    # A legacy record without IDs stays archival: the native builder creates graph
    # identifiers, which must not be mistaken for recovered invocation identities.
    if not source["identity"].get("run_id") or any(not row.get("event_id") or not row.get("run_id") for row in rows):
        return None, "legacy-json-missing-native-identity", {}, None
    if any(row["run_id"] != source["identity"]["run_id"] for row in rows):
        raise ViewError("native record run identity disagrees with trace identity")
    context: dict[str, Any] = {"purpose": "presentation-only; not historical skill metadata", "implementations": {}}
    renderer_path = ROOT / "agentic/scripts/generate_public_reasoning_trace_html.py"
    context["implementations"][str(renderer_path.relative_to(ROOT))] = _digest(renderer_path.read_bytes())
    if is_trace:
        builder_path = ROOT / "agentic/scripts/build_public_reasoning_monitor_packet.py"
        lenses_path = ROOT / "agentic/registries/reasoning_trace_lenses.yaml"
        lenses_raw = lenses_path.read_bytes()
        lenses = _read_json(lenses_raw)
        context["implementations"][str(builder_path.relative_to(ROOT))] = _digest(builder_path.read_bytes())
        context["lenses"] = {"locator": str(lenses_path.relative_to(ROOT)), "sha256": _digest(lenses_raw), "snapshot": lenses}
        packet = _module(builder_path.name).build_packet(copy.deepcopy(source), lenses)
        if _json_bytes(packet.get("identity")) != _json_bytes(source["identity"]) or _json_bytes(packet.get("timeline")) != _json_bytes(rows):
            raise ViewError("native monitor builder changed historical identity or events")
        route = "native-monitor-builder-and-html-renderer"
    else:
        packet = copy.deepcopy(source)
        route = "native-html-renderer"
    rendered = _module(renderer_path.name).render(packet)
    return rendered, route, context, packet


def render_history(source: Path, output_dir: Path, *, expected_sha256: str | None = None) -> dict[str, Any]:
    """Publish a fresh view directory; source and existing destinations stay intact."""
    source = Path(source).resolve(strict=True)
    output_dir = Path(output_dir).absolute()
    if output_dir.exists() or output_dir.is_symlink():
        raise FileExistsError(f"view destination already exists: {output_dir}")
    # Resolve the explicitly supplied parent, including macOS /tmp and /var
    # aliases. The destination itself must still be absent and never a symlink.
    output_dir = output_dir.parent.resolve(strict=True) / output_dir.name
    raw = source.read_bytes()
    source_hash = _digest(raw)
    if expected_sha256 is not None and expected_sha256 != source_hash:
        raise ViewError("source digest does not match expected historical bytes")
    parsed = _read_json(raw)
    records = _records(parsed)
    rendered, route, context, packet = _native_view(parsed)
    record_html = _record_html(records)
    notice = ('<aside role="note">Read-only historical projection. Presentation IDs are not new invocations; '
              'missing historical metadata remains explicit. This view grants no execution or scientific authority.</aside>')
    if rendered is None:
        rendered = '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Historical source view</title></head><body>' + notice + record_html + '</body></html>'
    else:
        rendered = rendered.replace('<main>', '<main>' + notice + record_html, 1)
    projection = {"projection_version": PROJECTION_VERSION, "source": {"locator": str(source), "sha256": source_hash},
                  "route": route, "source_document": parsed, "records": records,
                  "rendering_context": context, "native_packet": packet}
    outputs = {"projection.json": _json_bytes(projection), "view.html": rendered.encode("utf-8")}
    manifest = {"projection_version": PROJECTION_VERSION, "source": projection["source"], "route": route,
                "outputs": {name: {"sha256": _digest(data), "bytes": len(data)} for name, data in outputs.items()},
                "rendering_context_sha256": _digest(_json_bytes(context))}
    # Build entirely in memory, recheck history, then exclusively create only these
    # owned files. A failure never deletes or overwrites a pre-existing artifact.
    if _digest(source.read_bytes()) != source_hash:
        raise ViewError("historical source changed during rendering")
    output_dir.mkdir(parents=False, exist_ok=False)
    created: list[Path] = []
    try:
        for name, data in {**outputs, "manifest.json": _json_bytes(manifest)}.items():
            path = output_dir / name
            with path.open("xb") as stream:
                created.append(path)
                stream.write(data)
        verify_view(output_dir / "manifest.json")
    except BaseException:
        for path in reversed(created):
            path.unlink(missing_ok=True)
        output_dir.rmdir()
        raise
    return {"manifest": str(output_dir / "manifest.json"), **manifest}


def verify_view(manifest_path: Path) -> dict[str, Any]:
    """Verify source/view byte joins; hashes detect drift, not malicious attestation."""
    manifest_path = Path(manifest_path)
    manifest = _read_json(manifest_path.read_bytes())
    if not isinstance(manifest, dict) or manifest.get("projection_version") != PROJECTION_VERSION:
        raise ViewError("unsupported projection manifest version")
    if not isinstance(manifest.get("outputs"), dict) or set(manifest["outputs"]) != set(OUTPUT_NAMES):
        raise ViewError("manifest must name only the fixed projection and HTML outputs")
    source = manifest.get("source")
    if not isinstance(source, dict) or not isinstance(source.get("locator"), str):
        raise ViewError("manifest is missing source locator")
    source_path = Path(source["locator"])
    if not source_path.is_absolute():
        raise ViewError("source locator must identify the original absolute path")
    if _digest(source_path.read_bytes()) != source.get("sha256"):
        raise ViewError("historical source digest mismatch")
    output_bytes = {}
    for name in OUTPUT_NAMES:
        path = manifest_path.parent / name
        if path.is_symlink():
            raise ViewError("projection output must not be a symlink")
        raw = path.read_bytes()
        expected = manifest["outputs"][name]
        if not isinstance(expected, dict) or expected.get("sha256") != _digest(raw) or expected.get("bytes") != len(raw):
            raise ViewError(f"output digest/size mismatch: {name}")
        output_bytes[name] = raw
    projection = _read_json(output_bytes["projection.json"])
    if not isinstance(projection, dict):
        raise ViewError("projection must be an object")
    if projection.get("projection_version") != PROJECTION_VERSION or _json_bytes(projection.get("source")) != _json_bytes(source) or projection.get("route") != manifest.get("route"):
        raise ViewError("projection and manifest source/version/route join mismatch")
    source_doc = _read_json(source_path.read_bytes())
    if _json_bytes(projection.get("source_document")) != _json_bytes(source_doc) or _json_bytes(projection.get("records")) != _json_bytes(_records(source_doc)):
        raise ViewError("projection rewrites historical facts or record pointers")
    packet = projection.get("native_packet")
    route = projection.get("route")
    if route == "native-monitor-builder-and-html-renderer":
        if not isinstance(source_doc, dict):
            raise ViewError("native trace source must be an object")
        if not isinstance(packet, dict) or _json_bytes(packet.get("identity")) != _json_bytes(source_doc.get("identity")) or _json_bytes(packet.get("timeline")) != _json_bytes(source_doc.get("events")):
            raise ViewError("native packet changed historical identity or events")
    elif route == "native-html-renderer":
        if _json_bytes(packet) != _json_bytes(source_doc):
            raise ViewError("native packet differs from historical source packet")
    elif route in {"legacy-json", "legacy-json-missing-native-identity"}:
        if packet is not None:
            raise ViewError("legacy history must not invent a native packet")
    else:
        raise ViewError("unknown projection route")
    if packet is not None:
        embedded = re.search(r'<script id="trace-data" type="application/json">(.*?)</script>', output_bytes["view.html"].decode("utf-8"), re.S)
        if not embedded or _json_bytes(_read_json(embedded.group(1).encode("utf-8"))) != _json_bytes(packet):
            raise ViewError("HTML embedded packet disagrees with projection")
    if _digest(_json_bytes(projection.get("rendering_context"))) != manifest.get("rendering_context_sha256"):
        raise ViewError("rendering metadata snapshot mismatch")
    return {"status": "verified", "source_sha256": source["sha256"], "route": manifest["route"], "projection_version": PROJECTION_VERSION}


def release_probe(repository_root: Path = ROOT) -> dict[str, Any]:
    """Check the reviewed unresolved release boundary without executing its graph."""
    root = Path(repository_root)
    directory = root / "abducer-prism/workflows/release_promotion_loop"
    observed = {}
    for name, expected in RELEASE_BASELINE.items():
        raw = (directory / name).read_bytes()
        code = '\n'.join(line.rstrip() for line in raw.decode("utf-8").splitlines() if line.strip() and not line.lstrip().startswith('#'))
        if _digest(code.encode()) != expected:
            raise ViewError(f"release semantic baseline changed: {name}")
        observed[name] = _digest(raw)
    manifest = _read_json((directory.parent / "manifest.json").read_bytes())
    rows = [row for row in manifest.get("workflows", []) if row.get("id") == "release_promotion_loop"]
    if len(rows) != 1:
        raise ViewError("release workflow must resolve uniquely in manifest")
    row = rows[0]
    if row.get("policy_outcomes") != ["accept:promoted", "target_navigation_loop", "conceptual_hypothesis_exploration_loop", "stop:rejected"]:
        raise ViewError("release disposition routes changed")
    materialization = row.get("materialization", {})
    if materialization.get("status") != "blocked_unresolved_projection_gap" or materialization.get("executable_artifacts_emitted") is not False:
        raise ViewError("release projection blocker or execution boundary changed")
    if any((directory / name).exists() for name in ("main.prism", "materialization.prism")):
        raise ViewError("unresolved release unexpectedly has executable layers")
    samples = row.get("sample_outputs", {})
    if samples.get("epistemic_claim") != "documentation_only" or samples.get("mode") != "curated_simulated_payloads":
        raise ViewError("release samples must remain simulated documentation")
    raw_samples = (directory / "sample_outputs.prism").read_bytes()
    if samples.get("sha256") != "sha256:" + _digest(raw_samples):
        raise ViewError("release sample digest mismatch")
    observed["sample_outputs.prism"] = _digest(raw_samples)
    return {"status": "preserved", "workflow_id": "release_promotion_loop", "execution_performed": False,
            "projection_status": "blocked_unresolved_projection_gap", "files": observed}


def main(argv: list[str] | None = None) -> int:
    """Expose three fixed maintenance operations, with JSON results and no dispatch."""
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="operation", required=True)
    render = commands.add_parser("render-history")
    render.add_argument("--source", required=True, type=Path)
    render.add_argument("--output-dir", required=True, type=Path)
    render.add_argument("--expected-sha256")
    verify = commands.add_parser("verify-view")
    verify.add_argument("--manifest", required=True, type=Path)
    release = commands.add_parser("release-probe")
    release.add_argument("--repository-root", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        if args.operation == "render-history":
            result = render_history(args.source, args.output_dir, expected_sha256=args.expected_sha256)
        elif args.operation == "verify-view":
            result = verify_view(args.manifest)
        else:
            result = release_probe(args.repository_root)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({"status": "error", "error": str(error)}), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
