# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Keep skill credit in REUSE tables, including independently installed plugins.

The live disclosure audit checks exact Git histories. These fast regression
checks protect placement and package propagation without running research.
"""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
import tomllib

from reuse.global_licensing import AnnotationsItem

ROOT = Path(__file__).resolve().parents[2]


def rules(path):
    return [
        (r, AnnotationsItem.from_dict(r))
        for r in tomllib.loads(path.read_text())["annotations"]
    ]


def fields(path, compiled):
    values = {}
    for rule, matcher in compiled:
        if matcher.matches(path):
            values = {
                key: set([value] if isinstance(value, str) else value)
                for key, value in rule.items()
                if key.startswith("SPDX-")
            }
    return values


def skill_paths():
    return [
        p
        for p in subprocess.check_output(
            ["git", "ls-files"], cwd=ROOT, text=True
        ).splitlines()
        if p.endswith("/SKILL.md")
    ]


def test_every_tracked_skill_has_explicit_table_attribution():
    compiled = rules(ROOT / "REUSE.toml")
    for path in skill_paths():
        metadata = fields(path, compiled)
        for key in [
            "SPDX-FileCopyrightText",
            "SPDX-License-Identifier",
            "SPDX-FileContributor",
        ]:
            assert metadata.get(key), (path, key)


def test_maintained_skills_have_no_inline_license_notices():
    for path in skill_paths():
        if path.split("/", 1)[0] in {"skills", "prism_me", "proj_skills", "plugins"}:
            text = (ROOT / path).read_text()
            assert not any(
                "SPDX-" in c for c in re.findall(r"<!--(.*?)-->", text, re.S)
            ), path


def test_installed_plugin_retains_all_root_contributor_credit():
    root_rules = rules(ROOT / "REUSE.toml")
    plugin_rules = rules(ROOT / "plugins/abducer/REUSE.toml")
    for path in skill_paths():
        if path.startswith("plugins/abducer/"):
            expected = fields(path, root_rules)
            installed = fields(path.removeprefix("plugins/abducer/"), plugin_rules)
            for key in [
                "SPDX-FileCopyrightText",
                "SPDX-License-Identifier",
                "SPDX-FileContributor",
            ]:
                assert expected[key] <= installed[key], (path, key)
