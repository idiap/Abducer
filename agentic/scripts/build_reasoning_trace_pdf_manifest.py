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
"""Build and verify a public reasoning-trace PDF reproducibility manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Mapping, Sequence


SCHEMA_VERSION = "1.0"
DEFAULT_RENDERER = "public-reasoning-trace-latex"
DEFAULT_RENDERER_VERSION = "1.0"


class ManifestBindingError(ValueError):
    """The manifest is stale, unsafe, or semantically mismatched."""


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def canonical_digest(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def file_digest(path: Path) -> str:
    return sha256_bytes(Path(path).read_bytes())


def _template_digest(paths: Sequence[Path]) -> str:
    # Bind bytes and stable basenames, never machine-specific absolute paths.
    rows = [{"name": Path(path).name, "sha256": file_digest(Path(path))} for path in paths]
    return canonical_digest(sorted(rows, key=lambda row: row["name"]))


def _redact_public_text(value: str, limit: int = 12_000) -> str:
    value = value.replace("\x00", "")
    # Diagnostics are informational; local locations and likely credential
    # assignments have no reproducibility value and must not enter the manifest.
    value = re.sub(r"(?<![\w.-])/(?:Users|home|tmp|private|var|opt)/[^\s:]+", "<local-path>", value)
    value = re.sub(r"(?i)\b(token|secret|password|api[_-]?key)\s*[=:]\s*[^\s]+", r"\1=<redacted>", value)
    return value[-limit:]


def _compiler_projection(metadata: Mapping[str, Any]) -> dict[str, Any]:
    arguments = [str(item) for item in metadata.get("arguments", [])]
    if any(Path(arg).is_absolute() for arg in arguments):
        raise ManifestBindingError("compiler arguments contain an absolute local path")
    return {
        "disposition": str(metadata.get("disposition", "structural_only")),
        "engine": metadata.get("engine"),
        "engine_version": metadata.get("engine_version"),
        "arguments": arguments,
        "passes": int(metadata.get("passes", 0)),
        # Wall-clock build duration is deliberately excluded from the signed
        # reproducibility projection. It is useful transient telemetry, but it
        # would make two byte-identical rebuild manifests differ.
        "duration_seconds": 0.0,
        "source_date_epoch": int(metadata.get("source_date_epoch", 946684800)),
        "warnings": [_redact_public_text(str(item), 1000) for item in metadata.get("warnings", [])][:100],
        "diagnostics": _redact_public_text(str(metadata.get("diagnostics", ""))),
    }


def _all_semantic_ids(inventory: Mapping[str, Any]) -> list[str]:
    explicit = inventory.get("semantic_ids")
    if isinstance(explicit, list):
        return sorted({str(item) for item in explicit if str(item)})
    if isinstance(explicit, Mapping):
        return sorted({str(item) for values in explicit.values() if isinstance(values, list) for item in values if str(item)})
    semantic = inventory.get("semantic_inventory")
    if isinstance(semantic, Mapping) and isinstance(semantic.get("ids"), list):
        return sorted({str(item) for item in semantic["ids"] if str(item)})

    ids: set[str] = set()
    identity_keys = {"trace_id", "run_id", "workflow_id", "profile_id", "lens_id"}

    def walk(value: Any) -> None:
        if isinstance(value, Mapping):
            for key, item in value.items():
                if key not in identity_keys and (key == "id" or key.endswith("_id")) and isinstance(item, str) and item:
                    ids.add(item)
                else:
                    walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(inventory)
    return sorted(ids)


def _semantic_counts(inventory: Mapping[str, Any]) -> dict[str, int]:
    explicit = inventory.get("counts")
    if not isinstance(explicit, Mapping):
        semantic = inventory.get("semantic_inventory")
        explicit = semantic.get("counts") if isinstance(semantic, Mapping) else None
    if isinstance(explicit, Mapping):
        return {str(key): int(value) for key, value in sorted(explicit.items())}

    semantic_ids = inventory.get("semantic_ids")
    if isinstance(semantic_ids, Mapping):
        return {str(key): len(value) for key, value in sorted(semantic_ids.items()) if isinstance(value, list)}

    # Projection inventories conventionally expose these complete ordered lanes.
    result: dict[str, int] = {}
    for key, value in inventory.items():
        if isinstance(value, list):
            result[str(key)] = len(value)
    return result


def _page_count(pdf_path: Path) -> int:
    pdfinfo = shutil.which("pdfinfo")
    if pdfinfo:
        result = subprocess.run([pdfinfo, str(pdf_path)], capture_output=True, text=True,
                                encoding="utf-8", errors="replace", timeout=10, check=False)
        if result.returncode == 0:
            match = re.search(r"(?m)^Pages:\s*(\d+)\s*$", result.stdout)
            if match:
                return int(match.group(1))
    # Conservative fallback for development manifests. Cross-format validation
    # can require pdfinfo for release; this estimate never grants validity.
    return len(re.findall(rb"/Type\s*/Page\b", pdf_path.read_bytes()))


def build_manifest(
    packet: Mapping[str, Any],
    inventory: Mapping[str, Any],
    lens: Mapping[str, Any],
    tex_path: Path,
    pdf_path: Path,
    compile_metadata: Mapping[str, Any],
    *,
    template_paths: Sequence[Path] = (),
    renderer_version: str = DEFAULT_RENDERER_VERSION,
    renderer_name: str = DEFAULT_RENDERER,
) -> dict[str, Any]:
    identity = packet.get("identity")
    if not isinstance(identity, Mapping):
        raise ManifestBindingError("packet identity is missing")
    required = ("trace_id", "workflow_id", "run_id")
    if any(not identity.get(key) for key in required):
        raise ManifestBindingError("packet identity lacks trace_id, workflow_id, or run_id")
    tex_path, pdf_path = Path(tex_path), Path(pdf_path)
    if not tex_path.is_file() or not pdf_path.is_file():
        raise ManifestBindingError("TeX and PDF companions must exist")
    if not pdf_path.read_bytes().startswith(b"%PDF-"):
        raise ManifestBindingError("PDF companion has no PDF signature")
    ids = _all_semantic_ids(inventory)
    manifest: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "identity": {key: str(identity.get(key, "")) for key in ("trace_id", "workflow_id", "profile_id", "run_id")},
        "bindings": {
            "packet_sha256": canonical_digest(packet), "inventory_sha256": canonical_digest(inventory),
            "lens_sha256": canonical_digest(lens), "tex_sha256": file_digest(tex_path),
            "pdf_sha256": file_digest(pdf_path), "template_sha256": _template_digest(template_paths),
        },
        "renderer": {"name": renderer_name, "version": renderer_version},
        "compiler": _compiler_projection(compile_metadata),
        "pdf": {
            "page_count": _page_count(pdf_path), "byte_reproducibility": "pinned_environment",
            "semantic_reproducibility": "normalized_metadata_and_extracted_text",
        },
        "semantic_inventory": {
            "ids": ids, "counts": _semantic_counts(inventory),
            "truncations": list(inventory.get("truncations", [])),
            "split_volumes": list(inventory.get("split_volumes", [])),
        },
    }
    manifest["manifest_digest"] = canonical_digest(manifest)
    return manifest


def validate_manifest_bindings(
    manifest: Mapping[str, Any], packet: Mapping[str, Any], inventory: Mapping[str, Any],
    lens: Mapping[str, Any], tex_path: Path, pdf_path: Path, *,
    template_paths: Sequence[Path] = (), renderer_version: str = DEFAULT_RENDERER_VERSION,
) -> list[str]:
    errors: list[str] = []
    unsigned = dict(manifest)
    claimed_manifest_digest = unsigned.pop("manifest_digest", None)
    if claimed_manifest_digest != canonical_digest(unsigned):
        errors.append("manifest digest mismatch")
    expected_bindings = {
        "packet_sha256": canonical_digest(packet), "inventory_sha256": canonical_digest(inventory),
        "lens_sha256": canonical_digest(lens), "tex_sha256": file_digest(Path(tex_path)),
        "pdf_sha256": file_digest(Path(pdf_path)), "template_sha256": _template_digest(template_paths),
    }
    actual_bindings = manifest.get("bindings", {})
    for key, expected in expected_bindings.items():
        if actual_bindings.get(key) != expected:
            errors.append(f"stale or mismatched {key}")
    if manifest.get("renderer", {}).get("version") != renderer_version:
        errors.append("stale renderer version")
    identity = packet.get("identity", {})
    expected_identity = {key: str(identity.get(key, "")) for key in ("trace_id", "workflow_id", "profile_id", "run_id")}
    if manifest.get("identity") != expected_identity:
        errors.append("packet/manifest identity mismatch")
    semantic = manifest.get("semantic_inventory", {})
    if semantic.get("ids") != _all_semantic_ids(inventory):
        errors.append("semantic ID inventory mismatch")
    if semantic.get("counts") != _semantic_counts(inventory):
        errors.append("semantic counts mismatch")
    return errors


def _load(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _atomic_json(path: Path, value: Any) -> None:
    data = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True).encode() + b"\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(prefix=f".{path.name}.", dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name); stream.write(data); stream.flush()
    try:
        temporary.replace(path)
    except BaseException:
        temporary.unlink(missing_ok=True); raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", required=True, type=Path)
    parser.add_argument("--inventory", required=True, type=Path)
    parser.add_argument("--lens", type=Path, help="Lens JSON; defaults to packet.lens")
    parser.add_argument("--tex", required=True, type=Path)
    parser.add_argument("--pdf", required=True, type=Path)
    parser.add_argument("--compile-metadata", required=True, type=Path)
    parser.add_argument("--template", action="append", type=Path, default=[])
    parser.add_argument("--renderer-version", default=DEFAULT_RENDERER_VERSION)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    packet, inventory = _load(args.packet), _load(args.inventory)
    lens = _load(args.lens) if args.lens else packet.get("lens", {})
    manifest = build_manifest(packet, inventory, lens, args.tex, args.pdf, _load(args.compile_metadata),
                              template_paths=args.template, renderer_version=args.renderer_version)
    _atomic_json(args.output, manifest)
    print(json.dumps({"output": str(args.output), "manifest_digest": manifest["manifest_digest"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
