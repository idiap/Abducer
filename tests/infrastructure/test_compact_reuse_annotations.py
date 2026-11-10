# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Protect attribution exceptions while compacting REUSE path patterns."""

from copy import deepcopy

from reuse.global_licensing import AnnotationsItem

from agentic.scripts.compact_reuse_annotations import (
    compact_annotations,
    render_annotations,
    signature,
)


def rule(paths, contributor="Andre", license="MIT", precedence="closest"):
    return {
        "path": paths,
        "precedence": precedence,
        "SPDX-FileCopyrightText": "© 2026 Idiap Research Institute <contact@idiap.ch>",
        "SPDX-FileContributor": contributor,
        "SPDX-License-Identifier": license,
    }


def fields(rows, path):
    for row in reversed(rows):
        if AnnotationsItem.from_dict(row).matches(path):
            return signature(row)
    return None


def test_project_wildcards_retain_narrow_contributor_and_license_exceptions():
    paths = [
        "projects/a/prism_project/main.prism",
        "projects/b/prism_project/main.prism",
        "projects/a/prism_project/material_main.prism",
        "projects/b/prism_project/material_main.prism",
        "projects/vendor/prism_project/main.prism",
    ]
    rows = [
        rule([f"projects/{p}/prism_project/**" for p in ("a", "b")]),
        rule(
            [f"projects/{p}/prism_project/material_main.prism" for p in ("a", "b")],
            "Danilo",
        ),
        rule(["projects/vendor/**"], "Upstream", "Apache-2.0"),
    ]
    before = deepcopy(rows)
    compacted = compact_annotations(rows, paths)
    patterns = {p for row in compacted for p in row["path"]}
    assert "projects/*/prism_project/**" in patterns
    assert "projects/*/prism_project/material_main.prism" in patterns
    assert [fields(compacted, p) for p in paths] == [fields(before, p) for p in paths]
    assert rows == before


def test_refuses_wildcard_that_would_capture_another_contributor():
    rows = [rule(["skills/a/SKILL.md", "skills/b/SKILL.md"])]
    paths = ["skills/a/SKILL.md", "skills/b/SKILL.md", "skills/c/SKILL.md"]
    compacted = compact_annotations(rows, paths)
    assert fields(compacted, paths[-1]) is None
    assert compacted == rows


def test_prefix_wildcard_excludes_different_skill_family():
    rows = [
        rule(["skills/**"], "Danilo"),
        rule(["skills/results-alpha/SKILL.md", "skills/results-beta/SKILL.md"]),
    ]
    paths = [
        "skills/results-alpha/SKILL.md",
        "skills/results-beta/SKILL.md",
        "skills/other/SKILL.md",
    ]
    compacted = compact_annotations(rows, paths)
    assert "skills/results-*/SKILL.md" in {p for row in compacted for p in row["path"]}
    assert fields(compacted, paths[-1]) == fields(rows, paths[-1])


def test_retains_directory_default_when_all_current_files_have_exceptions():
    rows = [rule(["projects/**"], "Danilo"), rule(["projects/a.json"])]
    compacted = compact_annotations(rows, ["projects/a.json"])
    assert fields(compacted, "projects/future/deeper/file.json") == fields(
        rows, "projects/future/deeper/file.json"
    )


def test_never_combines_top_level_boundaries_into_root_fallback():
    rows = [rule(["alpha/data.json", "beta/data.json"])]
    compacted = compact_annotations(rows, rows[0]["path"])
    assert fields(compacted, "other/data.json") is None
    assert compacted == rows


def test_preserves_explicit_attribution_for_temporarily_absent_files():
    rows = [rule(["data/**"]), rule(["data/missing.json"], "Danilo")]
    compacted = compact_annotations(rows, ["data/current.json"])
    assert fields(compacted, "data/missing.json") == fields(rows, "data/missing.json")


def test_compaction_preserves_precedence_and_is_idempotent():
    rows = [
        rule(["a/**"], precedence="aggregate"),
        rule(["b/**"]),
        rule(["a/special.json"], "Danilo"),
        rule(["c/**"]),
    ]
    paths = ["a/x.json", "a/special.json", "b/x.json", "c/x.json"]
    compacted = compact_annotations(rows, paths)
    assert [fields(compacted, p) for p in paths] == [fields(rows, p) for p in paths]
    assert compact_annotations(compacted, paths) == compacted
    assert render_annotations(compacted) == render_annotations(
        compact_annotations(compacted, paths)
    )


def test_does_not_merge_matching_tables_across_conflicting_override():
    rows = [
        rule(["data/**"]),
        rule(["data/shared/**"], "Danilo"),
        rule(["data/shared/special.json"]),
    ]
    paths = ["data/base.json", "data/shared/base.json", "data/shared/special.json"]
    compacted = compact_annotations(rows, paths)
    assert [fields(compacted, p) for p in paths] == [fields(rows, p) for p in paths]
