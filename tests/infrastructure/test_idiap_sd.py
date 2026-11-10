# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Keep disclosure previews read-only and contributor decisions evidence-bound."""

from __future__ import annotations

import copy
import hashlib
import importlib
import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest


@pytest.fixture
def modules(monkeypatch):
    root = Path(__file__).resolve().parents[2]
    monkeypatch.syspath_prepend(str(root / ".idiap-sd"))
    return importlib.import_module("idiap_sd"), importlib.import_module(
        "plan_attribution"
    )


@pytest.fixture
def config():
    root = Path(__file__).resolve().parents[2]
    value = json.loads((root / ".idiap-sd/config.json").read_text())
    value["file_overrides"] = {}
    value["directory_overrides"] = []
    return value


# REUSE-IgnoreStart
def test_attribution_excludes_tracked_workspace_settings(
    modules, tmp_path, monkeypatch
):
    audit, _ = modules
    monkeypatch.chdir(tmp_path)
    subprocess.run(["git", "init", "-q"], check=True)
    Path(".codex").mkdir()
    Path(".codex/config.toml").write_text("private = true\n")
    Path("project.py").write_text("pass\n")
    Path("preserved.zip").write_bytes(b"tracked project archive")
    subprocess.run(["git", "add", "."], check=True)
    Path(".gitignore").write_text("/.codex/\n/.idiap-sd/\n/AGENTS.md\n*.zip\n")
    Path("AGENTS.md").write_text("local instructions\n")
    Path(".idiap-sd").mkdir()
    Path(".idiap-sd/config.json").write_text("{}\n")
    assert audit.paths() == [
        Path(".gitignore"),
        Path("preserved.zip"),
        Path("project.py"),
    ]


def test_preview_does_not_write_source_or_sidecar(
    modules, config, tmp_path, monkeypatch
):
    _, planner = modules
    monkeypatch.chdir(tmp_path)
    target = Path("frozen.py")
    original = b"print('unchanged source')\n"
    target.write_bytes(original)
    config["file_overrides"] = {
        str(target): {
            "use_reuse_toml": True,
            "preservation_reason": "Fixture hash contract",
        }
    }
    before = sorted(tmp_path.iterdir())
    plan = planner.describe(target, config, {("afreitas", "andre.freitas@idiap.ch")})
    assert target.read_bytes() == original
    assert sorted(tmp_path.iterdir()) == before
    assert plan["destination"] == "REUSE.toml"
    assert plan["source_sha256"] == hashlib.sha256(original).hexdigest()
    assert plan["action"] == "reconcile"
    assert plan["mapped_contributors"] == ["Andre Freitas <andre.freitas@idiap.ch>"]


def test_history_evidence_is_required_for_contributor_credit(modules, config):
    audit, _ = modules
    assert audit.contributors_for(Path("new.py"), config, set()) == []
    mapped = audit.contributors_for(
        Path("shared.py"),
        config,
        {
            ("afreitas", "afreitas@admins-macbook-pro.home"),
            ("danilo gusicuma", "danilo.m.gusicuma@gmail.com"),
        },
    )
    assert [item["id"] for item in mapped] == ["andre", "danilo"]


def test_combined_work_keeps_each_copyright_holder(modules, config):
    audit, _ = modules
    value = copy.deepcopy(config)
    value["copyright"] = [
        config["copyright"],
        "Copyright (c) 2017-2022 The MathJax Consortium",
    ]
    value["license"] = "MIT AND Apache-2.0"
    text = audit.metadata(value, [], "")
    assert text.count("SPDX-FileCopyrightText:") == 2
    assert text.endswith("SPDX-License-Identifier: MIT AND Apache-2.0\n")


def test_preview_retains_preexisting_contributor(
    modules, config, tmp_path, monkeypatch
):
    _, planner = modules
    monkeypatch.chdir(tmp_path)
    target = Path("credited.py")
    target.write_text(
        "# SPDX-FileContributor: Prior Author <prior@example.org>\nprint(1)\n"
    )
    body, mapped = planner.proposed_metadata(target, config, set())
    assert "SPDX-FileContributor: Prior Author <prior@example.org>" in body
    assert mapped == []


def test_existing_metadata_is_a_noop_in_preview(modules, config, tmp_path, monkeypatch):
    audit, planner = modules
    monkeypatch.chdir(tmp_path)
    target = Path("correct.py")
    target.write_text(audit.metadata(config, [], "# ") + "print(1)\n")
    plan = planner.describe(target, config, set())
    assert plan["action"] == "unchanged"
    assert plan["strategy"] == "inline-comment"


def test_bulk_history_matches_follow_for_renames_and_recreation(
    modules, tmp_path, monkeypatch
):
    audit, _ = modules
    monkeypatch.chdir(tmp_path)

    def git(*args):
        return subprocess.run(
            [
                "git",
                "-c",
                "user.name=Test Committer",
                "-c",
                "user.email=committer@example.org",
                *args,
            ],
            capture_output=True,
            check=True,
        )

    def commit(author):
        git("add", ".")
        git(
            "commit",
            "-qm",
            author,
            "--author",
            f"{author} <{author.lower()}@example.org>",
        )

    git("init", "-q")
    Path("original.py").write_text("print('initial')\n")
    Path("stable.py").write_text("print('initial')\n")
    Path("recreated.py").write_text("print('old contents')\n")
    commit("Alpha")
    Path("original.py").write_text("print('modified')\n")
    Path("stable.py").write_text("print('modified')\n")
    Path("recreated.py").unlink()
    commit("Beta")
    git("mv", "original.py", "renamed.py")
    Path("recreated.py").write_text("print('different generation')\n")
    commit("Gamma")
    candidates = [
        Path(name)
        for name in ("original.py", "renamed.py", "stable.py", "recreated.py", "new.py")
    ]
    assert audit.histories_for(candidates) == {
        path: audit.authors(path) for path in candidates
    }


def test_merge_history_uses_exact_follow_queries(modules, monkeypatch):
    audit, _ = modules
    monkeypatch.setattr(audit, "git", lambda *args: SimpleNamespace(stdout=b"merge\n"))
    monkeypatch.setattr(
        audit, "authors", lambda path: {(str(path), "author@example.org")}
    )
    paths = [Path("a.py"), Path("b.py")]
    assert audit.histories_for(paths) == {
        path: {(str(path), "author@example.org")} for path in paths
    }


@pytest.mark.parametrize(
    "name,preamble,body",
    [
        ("script.py", "\ufeff#!/usr/bin/python3\n# coding: utf-8\n", "print(1)\n"),
        ("guide.md", "---\ntitle: Example\n---\n", "# Guide\n"),
        ("image.svg", '<?xml version="1.0"?>\n', "<svg/>\n"),
        ("style.css", '@charset "UTF-8";\n', "a { color: red; }\n"),
        ("Dockerfile", "# syntax=docker/dockerfile:1\n", "FROM scratch\n"),
    ],
)
def test_header_preserves_preamble_and_is_idempotent(
    modules, config, tmp_path, monkeypatch, name, preamble, body
):
    audit, _ = modules
    monkeypatch.chdir(tmp_path)
    target = Path(name)
    target.write_text(preamble + body)
    assert audit.apply_metadata(target, config, []) == []
    first = target.read_bytes()
    assert first.decode().startswith(preamble)
    assert first.decode().endswith(body)
    assert audit.apply_metadata(target, config, []) == []
    assert target.read_bytes() == first


def test_spdx_literal_does_not_impersonate_a_header(
    modules, config, tmp_path, monkeypatch
):
    audit, _ = modules
    monkeypatch.chdir(tmp_path)
    target = Path("literal.py")
    target.write_text('example = "SPDX-License-Identifier: Apache-2.0"\n')
    assert audit.apply_metadata(target, config, []) == []
    assert target.read_text().startswith("# SPDX-FileCopyrightText:")


def test_migration_retains_sidecar_credit_and_prior_copyright(
    modules, config, tmp_path, monkeypatch
):
    audit, _ = modules
    monkeypatch.chdir(tmp_path)
    target = Path("credited.py")
    target.write_text(
        "# SPDX-FileCopyrightText: 2020 Prior Holder\n# SPDX-License-Identifier: MIT\nprint(1)\n"
    )
    sidecar = audit.license_path(target)
    sidecar.write_text(
        "SPDX-License-Identifier: MIT\nSPDX-FileContributor: Prior Author <prior@example.org>\n"
    )
    assert audit.apply_metadata(target, config, []) == []
    assert "2020 Prior Holder" in target.read_text()
    assert "Prior Author <prior@example.org>" in target.read_text()
    assert not sidecar.exists()


def test_directory_rules_preserve_bytes_and_exact_contributor_credit(
    modules, config, tmp_path, monkeypatch
):
    audit, _ = modules
    policy = importlib.import_module("reuse_policy")
    monkeypatch.chdir(tmp_path)
    Path("data").mkdir()
    paths = [Path("data/a.json"), Path("data/b.json")]
    for path in paths:
        path.write_bytes(b'{"untouched":true}\n')
    contributors = [config["contributors"][0]]
    fields = policy.effective_fields(paths[0], config, contributors, audit)
    policy.write_annotations(dict.fromkeys(paths, fields), paths)
    assert '"data/**"' in Path("REUSE.toml").read_text()
    for path in paths:
        assert audit.check_metadata(path, config, contributors) == []
        assert path.read_bytes() == b'{"untouched":true}\n'
    fields["SPDX-FileContributor"] = []
    policy.write_annotations(dict.fromkeys(paths, fields), paths)
    assert any(
        "SPDX-FileContributor" in problem
        for problem in audit.check_metadata(paths[0], config, contributors)
    )


def test_last_matching_toml_rule_wins(modules):
    policy = importlib.import_module("reuse_policy")
    rules = [
        {"path": "data/**", "SPDX-License-Identifier": "MIT"},
        {"path": "data/vendor.json", "SPDX-License-Identifier": "Apache-2.0"},
    ]
    assert policy.matching_annotation(Path("data/vendor.json"), rules) is rules[1]
    assert policy.matching_annotation(Path("data/own.json"), rules) is rules[0]


def test_text_sidecar_exception_is_rejected(modules, config, tmp_path, monkeypatch):
    audit, _ = modules
    policy = importlib.import_module("reuse_policy")
    monkeypatch.chdir(tmp_path)
    Path("data.json").write_text("{}\n")
    with pytest.raises(ValueError, match="points to text"):
        policy.strategy(
            Path("data.json"),
            {
                **config,
                "use_sidecar": True,
                "isolated_binary": True,
                "preservation_reason": "test",
            },
            audit,
        )


def test_directory_coalescing_does_not_spread_author_credit(
    modules, config, tmp_path, monkeypatch
):
    audit, _ = modules
    policy = importlib.import_module("reuse_policy")
    monkeypatch.chdir(tmp_path)
    Path("data").mkdir()
    paths = [Path("data/andre.json"), Path("data/danilo.json"), Path("data/more.json")]
    people = [*config["contributors"], config["contributors"][0]]
    entries = {}
    for path, contributor in zip(paths, people):
        path.write_text("{}\n")
        entries[path] = policy.effective_fields(path, config, [contributor], audit)
    policy.write_annotations(entries, paths)
    rules = policy.load_rules()
    assert '"data/**"' in Path("REUSE.toml").read_text()
    assert all(rule["precedence"] == "closest" for rule in rules)
    for path, contributor in zip(paths, people):
        assert policy.matching_annotation(path, rules)["SPDX-FileContributor"] == [
            contributor["spdx_contributor"]
        ]


def test_generated_annotations_pass_real_reuse_lint(
    modules, config, tmp_path, monkeypatch
):
    audit, _ = modules
    policy = importlib.import_module("reuse_policy")
    license_text = Path(__file__).resolve().parents[2] / "LICENSES/MIT.txt"
    canonical = license_text.read_text()
    monkeypatch.chdir(tmp_path)
    Path("LICENSES").mkdir()
    Path("LICENSES/MIT.txt").write_text(canonical)
    Path("data").mkdir()
    path = Path("data/payload.json")
    path.write_text("{}\n")
    policy.write_annotations(
        {path: policy.effective_fields(path, config, config["contributors"], audit)},
        [path],
    )
    result = subprocess.run(
        [sys.executable, "-m", "reuse", "lint"], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_directory_defaults_defer_to_inline_and_sidecar_notices(
    modules, config, tmp_path, monkeypatch
):
    from reuse.project import Project

    audit, _ = modules
    policy = importlib.import_module("reuse_policy")
    monkeypatch.chdir(tmp_path)
    Path("data").mkdir()
    paths = [Path("data/a.json"), Path("data/b.json")]
    for path in paths:
        path.write_text("{}\n")
    fields = policy.effective_fields(paths[0], config, config["contributors"], audit)
    policy.write_annotations(dict.fromkeys(paths, fields), paths)
    notice = (
        "SPDX-FileCopyrightText: 2020 Upstream Author\n"
        "SPDX-License-Identifier: Apache-2.0\n"
    )
    inline = Path("data/vendor.py")
    inline.write_text("".join("# " + line + "\n" for line in notice.splitlines()))
    binary = Path("data/vendor.bin")
    binary.write_bytes(b"\x00")
    Path("data/vendor.bin.license").write_text(notice)
    project = Project.from_directory(tmp_path)
    for path in [inline, binary]:
        info = project.reuse_info_of(path)
        assert {str(expr) for item in info for expr in item.spdx_expressions} == {
            "Apache-2.0"
        }
        assert {text.name for item in info for text in item.copyright_notices} == {
            "Upstream Author"
        }


def test_conflicting_license_leaves_source_and_sidecar_untouched(
    modules, config, tmp_path, monkeypatch
):
    audit, _ = modules
    monkeypatch.chdir(tmp_path)
    path = Path("conflict.py")
    original = b"# SPDX-License-Identifier: Apache-2.0\nprint(1)\n"
    path.write_bytes(original)
    sidecar = audit.license_path(path)
    sidecar.write_text("SPDX-License-Identifier: MIT\n")
    with pytest.raises(ValueError, match="conflicts"):
        audit.apply_metadata(path, config, [])
    assert path.read_bytes() == original
    assert sidecar.read_text() == "SPDX-License-Identifier: MIT\n"


# REUSE-IgnoreEnd


def test_json_serialized_yaml_uses_toml_without_changing_parser_input(
    modules, config, tmp_path, monkeypatch
):
    audit, _ = modules
    policy = importlib.import_module("reuse_policy")
    monkeypatch.chdir(tmp_path)
    path = Path("registry.yaml")
    original = b'{"version": 1}\n'
    path.write_bytes(original)
    assert policy.strategy(path, config, audit) == "reuse-toml"
    assert audit.apply_metadata(path, config, []) == []
    policy.write_annotations(
        {path: policy.effective_fields(path, config, [], audit)}, [path]
    )
    assert audit.check_metadata(path, config, []) == []
    assert path.read_bytes() == original
    assert json.loads(path.read_text()) == {"version": 1}
