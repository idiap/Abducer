# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Compatibility probes for real native rendering and immutable history sidecars."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from proj_skills.scripts import repository_adoption_views as views

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "proj_skills/scripts/repository_adoption_views.py"
FIXTURES = ROOT / "tests/fixtures/reasoning_trace/generated"


def cli(*args: str | Path) -> subprocess.CompletedProcess[str]:
    """Exercise the published route from an unrelated working directory."""
    return subprocess.run([sys.executable, str(SCRIPT), *(str(arg) for arg in args)],
                          cwd=ROOT.parent, text=True, capture_output=True, check=False)


def write_source(tmp_path: Path, value: object) -> Path:
    path = tmp_path / "history.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def rewrite_projection_and_digest(output: Path, transform) -> None:
    """Test joins independently from ordinary output checksum failures."""
    path = output / "projection.json"
    data = json.loads(path.read_text())
    transform(data)
    raw = views._json_bytes(data)
    path.write_bytes(raw)
    manifest = json.loads((output / "manifest.json").read_text())
    manifest["outputs"]["projection.json"] = {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
    (output / "manifest.json").write_text(json.dumps(manifest))


def test_cli_native_builder_renderer_and_verifier_preserve_exact_history(tmp_path: Path) -> None:
    source = tmp_path / "native.trace.json"
    original = (FIXTURES / "deep_review_and_reorientation.trace.json").read_bytes()
    source.write_bytes(original)
    output = tmp_path / "view"
    result = cli("render-history", "--source", source, "--output-dir", output,
                 "--expected-sha256", hashlib.sha256(original).hexdigest())
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["route"] == "native-monitor-builder-and-html-renderer"
    projection = json.loads((output / "projection.json").read_text())
    source_doc = json.loads(original)
    packet = projection["native_packet"]
    assert projection["source_document"] == source_doc
    assert packet["identity"] == source_doc["identity"]
    assert packet["timeline"] == source_doc["events"]
    embedded = re.search(r'<script id="trace-data" type="application/json">(.*?)</script>',
                         (output / "view.html").read_text(), re.S)
    assert embedded and json.loads(embedded.group(1)) == packet
    # Native output agrees with the established builder/render pipeline, not just
    # with our own serialization. Its generated IDs remain presentation IDs.
    native = tmp_path / "native.packet.json"
    built = subprocess.run([sys.executable, str(ROOT / "agentic/scripts/build_public_reasoning_monitor_packet.py"),
                            "--trace", str(source), "--output", str(native)], capture_output=True, text=True)
    assert built.returncode == 0, built.stderr
    assert packet == json.loads(native.read_text())
    verified = cli("verify-view", "--manifest", output / "manifest.json")
    assert verified.returncode == 0, verified.stderr
    assert json.loads(verified.stdout)["status"] == "verified"
    assert source.read_bytes() == original
    assert "Rationale not recorded" in (output / "view.html").read_text()


def test_native_monitor_packet_is_rendered_without_rebuilding(tmp_path: Path, monkeypatch) -> None:
    source = tmp_path / "packet.json"
    source.write_bytes((FIXTURES / "deep_review_and_reorientation.packet.json").read_bytes())
    real_module = views._module
    calls = []
    def selected_module(filename):
        calls.append(filename)
        return real_module(filename)
    monkeypatch.setattr(views, "_module", selected_module)
    result = views.render_history(source, tmp_path / "view")
    projection = json.loads((tmp_path / "view/projection.json").read_text())
    assert result["route"] == "native-html-renderer"
    assert projection["native_packet"] == json.loads(source.read_text())
    assert calls == ["generate_public_reasoning_trace_html.py"]


def test_unknown_history_keeps_missing_identity_and_escapes_text(tmp_path: Path, monkeypatch) -> None:
    source_doc = {"entries": [{"outcome": "rejected", "payload": '</script><script id="attack">boom</script>'}]}
    source = write_source(tmp_path, source_doc)
    monkeypatch.setattr(views, "_module", lambda _: pytest.fail("legacy projection must not invoke native modules"))
    output = tmp_path / "view"
    views.render_history(source, output)
    projection = json.loads((output / "projection.json").read_text())
    record = projection["records"][0]
    assert record["source_pointer"] == "/entries/0"
    assert record["record"] == source_doc["entries"][0]
    assert record["display"] == {"skill": "No skill recorded", "rationale": "Rationale not recorded", "reasoning_mapping": "Unassigned"}
    assert "run_id" not in record["record"] and "invocation_id" not in record["record"]
    rendered = (output / "view.html").read_text()
    assert '<script id="attack">' not in rendered
    assert '&lt;/script&gt;' in rendered
    assert views.verify_view(output / "manifest.json")["status"] == "verified"


def test_native_html_escapes_payload_and_preserves_status(tmp_path: Path) -> None:
    packet = json.loads((FIXTURES / "deep_review_and_reorientation.packet.json").read_text())
    packet["lens"]["visible_name"] = '</script><script id="attack">boom</script>'
    source = write_source(tmp_path, packet)
    views.render_history(source, tmp_path / "view")
    rendered = (tmp_path / "view/view.html").read_text()
    assert '<script id="attack">' not in rendered
    assert '\\u003c/script>' in rendered
    projected = json.loads((tmp_path / "view/projection.json").read_text())["native_packet"]
    assert projected == packet


@pytest.mark.parametrize("change", ["missing-event", "missing-run", "cross-run", "version"])
def test_native_missing_and_contradictory_identity_are_not_fabricated(tmp_path: Path, change: str) -> None:
    trace = json.loads((FIXTURES / "deep_review_and_reorientation.trace.json").read_text())
    if change == "missing-event":
        del trace["events"][0]["event_id"]
    elif change == "missing-run":
        del trace["identity"]["run_id"]
    elif change == "cross-run":
        trace["events"][0]["run_id"] = "different-run"
    else:
        trace["schema_version"] = "999"
    source = write_source(tmp_path, trace)
    output = tmp_path / "view"
    if change in {"cross-run", "version"}:
        with pytest.raises(views.ViewError):
            views.render_history(source, output)
        assert not output.exists()
    else:
        result = views.render_history(source, output)
        assert result["route"] == "legacy-json-missing-native-identity"
        projection = json.loads((output / "projection.json").read_text())
        assert projection["source_document"] == trace
        assert projection["native_packet"] is None


def test_existing_destinations_bad_digest_and_missing_history_fail_without_writes(tmp_path: Path) -> None:
    source = write_source(tmp_path, {"entries": []})
    output = tmp_path / "view"
    with pytest.raises(views.ViewError, match="digest"):
        views.render_history(source, output, expected_sha256="0" * 64)
    assert not output.exists()
    with pytest.raises(FileNotFoundError):
        views.render_history(tmp_path / "missing.json", output)
    assert not output.exists()
    views.render_history(source, output)
    snapshot = {path.name: path.read_bytes() for path in output.iterdir()}
    with pytest.raises(FileExistsError):
        views.render_history(source, output)
    assert snapshot == {path.name: path.read_bytes() for path in output.iterdir()}
    with pytest.raises(FileExistsError):
        views.render_history(source, source)


@pytest.mark.parametrize("tamper", ["source", "html", "projection", "missing-source", "escape", "symlink", "facts", "context", "version"])
def test_verifier_rejects_tamper_missing_history_and_path_escape(tmp_path: Path, tamper: str) -> None:
    source = write_source(tmp_path, {"entries": [{"skill": "original", "result": 1}]})
    output = tmp_path / "view"
    views.render_history(source, output)
    if tamper == "source":
        source.write_text('{}')
    elif tamper == "missing-source":
        source.unlink()
    elif tamper in {"html", "projection"}:
        (output / ("view.html" if tamper == "html" else "projection.json")).write_text('tampered')
    elif tamper == "symlink":
        (output / "view.html").unlink()
        (output / "view.html").symlink_to(source)
    elif tamper == "facts":
        rewrite_projection_and_digest(output, lambda doc: doc["source_document"]["entries"][0].update(result=True))
    elif tamper == "context":
        rewrite_projection_and_digest(output, lambda doc: doc["rendering_context"].update(forged="metadata"))
    else:
        manifest = json.loads((output / "manifest.json").read_text())
        if tamper == "escape":
            manifest["outputs"]["../history.json"] = manifest["outputs"].pop("view.html")
        else:
            manifest["projection_version"] = "unexpected/v100"
        (output / "manifest.json").write_text(json.dumps(manifest))
    with pytest.raises((views.ViewError, FileNotFoundError)):
        views.verify_view(output / "manifest.json")


def test_final_symlink_is_rejected_but_explicit_parent_alias_is_supported(tmp_path: Path) -> None:
    source = write_source(tmp_path, {})
    real = tmp_path / "actual"
    real.mkdir()
    link = tmp_path / "link"
    link.symlink_to(real, target_is_directory=True)
    with pytest.raises(FileExistsError):
        views.render_history(source, link)
    result = views.render_history(source, link / "view")
    assert Path(result["manifest"]) == real / "view/manifest.json"
    assert views.verify_view(real / "view/manifest.json")["status"] == "verified"


@pytest.mark.parametrize("raw", ['{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}'])
def test_lossy_json_is_rejected_before_publication(tmp_path: Path, raw: str) -> None:
    source = tmp_path / "history.json"
    source.write_text(raw)
    with pytest.raises(views.ViewError):
        views.render_history(source, tmp_path / "view")
    assert not (tmp_path / "view").exists()


def test_release_cli_reads_current_semantics_without_any_writes() -> None:
    directory = ROOT / "abducer-prism/workflows/release_promotion_loop"
    before = {p.name: p.read_bytes() for p in directory.iterdir() if p.is_file()}
    result = cli("release-probe", "--repository-root", ROOT)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["execution_performed"] is False
    assert before == {p.name: p.read_bytes() for p in directory.iterdir() if p.is_file()}


@pytest.mark.parametrize("mutation", ["order", "type", "unresolved", "manifest", "sample", "executable"])
def test_release_probe_rejects_changed_semantic_authority(tmp_path: Path, mutation: str) -> None:
    original = ROOT / "abducer-prism/workflows"
    target = tmp_path / "abducer-prism/workflows"
    shutil.copytree(original / "release_promotion_loop", target / "release_promotion_loop")
    shutil.copy2(original / "manifest.json", target / "manifest.json")
    release = target / "release_promotion_loop"
    if mutation == "order":
        path = release / "reasoning.prism"
        text = path.read_text()
        text = text.replace("return promotion_disposition", "return release_proposal")
        path.write_text(text)
    elif mutation == "type":
        path = release / "types.prism"
        path.write_text(path.read_text().replace("proposal_ref: String", "proof_ref: String"))
    elif mutation == "unresolved":
        path = release / "occurrences.prism"
        path.write_text(path.read_text().replace("UnresolvedReleaseProposalProjection", "ResolvedReleaseProposalProjection"))
    elif mutation == "sample":
        path = release / "sample_outputs.prism"
        path.write_text(path.read_text() + "\n# changed\n")
    elif mutation == "executable":
        (release / "main.prism").write_text("invented execution")
    else:
        manifest = json.loads((target / "manifest.json").read_text())
        row = next(row for row in manifest["workflows"] if row["id"] == "release_promotion_loop")
        row["materialization"]["status"] = "ready"
        (target / "manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(views.ViewError):
        views.release_probe(tmp_path)


@pytest.mark.parametrize("field", ["identity", "timeline"])
def test_rehashed_native_packet_cannot_disagree_with_historical_source(tmp_path: Path, field: str) -> None:
    source = tmp_path / "trace.json"
    source.write_bytes((FIXTURES / "deep_review_and_reorientation.trace.json").read_bytes())
    output = tmp_path / "view"
    views.render_history(source, output)
    def mutate(projection):
        if field == "identity":
            projection["native_packet"]["identity"]["run_id"] = "forged-run"
        else:
            projection["native_packet"]["timeline"][0]["workflow_disposition"] = "forged-acceptance"
    rewrite_projection_and_digest(output, mutate)
    with pytest.raises(views.ViewError, match="historical identity or events"):
        views.verify_view(output / "manifest.json")


@pytest.mark.parametrize("kind", ["manifest", "projection"])
def test_primitive_manifest_or_projection_is_a_contract_error(tmp_path: Path, kind: str) -> None:
    source = write_source(tmp_path, {"entries": []})
    output = tmp_path / "view"
    views.render_history(source, output)
    if kind == "manifest":
        (output / "manifest.json").write_text("1")
    else:
        raw = b"true"
        (output / "projection.json").write_bytes(raw)
        manifest = json.loads((output / "manifest.json").read_text())
        manifest["outputs"]["projection.json"] = {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
        (output / "manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(views.ViewError):
        views.verify_view(output / "manifest.json")
    result = cli("verify-view", "--manifest", output / "manifest.json")
    assert result.returncode == 1 and '"status": "error"' in result.stderr
    assert "Traceback" not in result.stderr
