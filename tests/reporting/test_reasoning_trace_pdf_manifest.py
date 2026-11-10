# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
import copy
import json
from pathlib import Path

import pytest

from agentic.scripts.build_reasoning_trace_pdf_manifest import (
    ManifestBindingError,
    build_manifest,
    validate_manifest_bindings,
)


def inputs(tmp_path):
    packet = {
        "identity": {"trace_id": "trace-1", "workflow_id": "proof", "profile_id": "", "run_id": "run-1"},
        "lens": {"lens_id": "proof"},
        "inferences": [{"event_id": "inf-1"}],
    }
    inventory = {
        "schema_version": "1.0", "semantic_ids": ["inf-1", "step-1"],
        "counts": {"inferences": 1, "route_steps": 1}, "truncations": [], "split_volumes": [],
    }
    tex, pdf, template = tmp_path / "trace.tex", tmp_path / "trace.pdf", tmp_path / "template.tex"
    tex.write_text("deterministic tex", encoding="utf-8")
    pdf.write_bytes(b"%PDF-1.4\nfixture")
    template.write_text("fixed template", encoding="utf-8")
    metadata = {
        "disposition": "compiled", "engine": "pdflatex", "engine_version": "test",
        "arguments": ["pdflatex", "-no-shell-escape", "reasoning-trace.tex"], "passes": 2,
        "duration_seconds": 0.25, "source_date_epoch": 946684800,
        "warnings": [], "diagnostics": "ok",
    }
    return packet, inventory, packet["lens"], tex, pdf, template, metadata


def test_manifest_binds_all_inputs_and_has_stable_semantic_projection(tmp_path):
    packet, inventory, lens, tex, pdf, template, metadata = inputs(tmp_path)
    first = build_manifest(packet, inventory, lens, tex, pdf, metadata, template_paths=[template])
    second = build_manifest(copy.deepcopy(packet), copy.deepcopy(inventory), copy.deepcopy(lens), tex, pdf, metadata, template_paths=[template])
    assert first == second
    assert first["semantic_inventory"]["ids"] == ["inf-1", "step-1"]
    assert first["semantic_inventory"]["counts"] == {"inferences": 1, "route_steps": 1}
    assert first["manifest_digest"].startswith("sha256:")
    assert validate_manifest_bindings(first, packet, inventory, lens, tex, pdf, template_paths=[template]) == []


def test_manifest_is_stable_across_wall_clock_build_durations(tmp_path):
    packet, inventory, lens, tex, pdf, template, metadata = inputs(tmp_path)
    first = build_manifest(packet, inventory, lens, tex, pdf, metadata, template_paths=[template])
    metadata["duration_seconds"] = 987.654
    second = build_manifest(packet, inventory, lens, tex, pdf, metadata, template_paths=[template])
    assert first == second
    assert first["compiler"]["duration_seconds"] == 0.0


def test_manifest_flattens_canonical_print_inventory_semantic_id_groups(tmp_path):
    packet, inventory, lens, tex, pdf, template, metadata = inputs(tmp_path)
    inventory.pop("counts")
    inventory["semantic_ids"] = {"inferences": ["inf-1"], "route_steps": ["step-1", "step-2"]}
    manifest = build_manifest(packet, inventory, lens, tex, pdf, metadata)
    assert manifest["semantic_inventory"]["ids"] == ["inf-1", "step-1", "step-2"]
    assert manifest["semantic_inventory"]["counts"] == {"inferences": 1, "route_steps": 2}


@pytest.mark.parametrize("target", ["packet", "inventory", "lens", "tex", "pdf", "template", "renderer"])
def test_any_bound_change_is_reported_as_stale(tmp_path, target):
    packet, inventory, lens, tex, pdf, template, metadata = inputs(tmp_path)
    manifest = build_manifest(packet, inventory, lens, tex, pdf, metadata, template_paths=[template])
    renderer_version = "1.0"
    if target == "packet": packet["new"] = True
    elif target == "inventory": inventory["counts"]["inferences"] = 2
    elif target == "lens": lens["focus"] = "changed"
    elif target == "tex": tex.write_text("changed", encoding="utf-8")
    elif target == "pdf": pdf.write_bytes(b"%PDF-changed")
    elif target == "template": template.write_text("changed", encoding="utf-8")
    else: renderer_version = "2.0"
    assert validate_manifest_bindings(manifest, packet, inventory, lens, tex, pdf,
                                      template_paths=[template], renderer_version=renderer_version)


def test_manifest_rejects_absolute_arguments_and_redacts_public_diagnostics(tmp_path):
    packet, inventory, lens, tex, pdf, template, metadata = inputs(tmp_path)
    metadata["arguments"] = ["/usr/local/bin/pdflatex"]
    with pytest.raises(ManifestBindingError, match="absolute"):
        build_manifest(packet, inventory, lens, tex, pdf, metadata)
    metadata["arguments"] = ["pdflatex"]
    metadata["diagnostics"] = "at /Users/alice/private/file.tex token=very-secret"
    manifest = build_manifest(packet, inventory, lens, tex, pdf, metadata)
    encoded = json.dumps(manifest)
    assert "/Users/alice" not in encoded
    assert "very-secret" not in encoded


def test_manifest_conforms_to_schema_when_jsonschema_available(tmp_path):
    jsonschema = pytest.importorskip("jsonschema")
    packet, inventory, lens, tex, pdf, template, metadata = inputs(tmp_path)
    manifest = build_manifest(packet, inventory, lens, tex, pdf, metadata, template_paths=[template])
    schema = json.loads(Path("agentic/spec/public_reasoning_trace_pdf_manifest.schema.json").read_text())
    jsonschema.Draft202012Validator(schema).validate(manifest)
