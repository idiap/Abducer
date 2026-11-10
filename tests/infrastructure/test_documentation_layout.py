# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Guard the thematic documentation layout and its local navigation links."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

REPO = Path(__file__).resolve().parents[2]
DOCS = REPO / "docs"
# Shared reader-facing areas coexist with stable specialist collections.
COMMON_THEMES = {
    "getting-started", "concepts", "guides", "architecture", "reference",
    "development", "operations", "governance", "archive",
}
THEMES = COMMON_THEMES | {
    "architecture",
    "case-studies",
    "examples",
    "generated",
    "integrations",
    "operations",
    "plans-and-reviews",
    "publications",
    "reference",
    "research-methods",
    "testing",
    "workflows",
}
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def test_docs_root_is_a_thematic_front_door() -> None:
    # Finder metadata is not project documentation and may appear on macOS.
    root_files = sorted(path.name for path in DOCS.iterdir() if path.is_file() and path.name != ".DS_Store")
    assert root_files == ["README.md"]
    assert {path.name for path in DOCS.iterdir() if path.is_dir()} == THEMES
    assert all((DOCS / theme / "README.md").is_file() for theme in COMMON_THEMES)


def test_documentation_markdown_links_resolve() -> None:
    broken: list[str] = []
    for document in DOCS.rglob("*.md"):
        text = document.read_text(encoding="utf-8")
        for raw in LINK_RE.findall(text):
            target = unquote(raw.strip().strip("<>").split("#", 1)[0])
            if not target or target.startswith(("http:", "https:", "mailto:", "data:")):
                continue
            assert "docs/../" not in target, f"Non-canonical documentation link in {document}: {raw}"
            if not (document.parent / target).resolve().exists():
                broken.append(f"{document.relative_to(REPO)} -> {raw}")
    assert not broken, "Broken documentation links:\n" + "\n".join(broken)


def test_every_markdown_document_is_reachable_from_the_front_door() -> None:
    pending = [DOCS / "README.md"]
    visited: set[Path] = set()
    while pending:
        document = pending.pop()
        if document in visited:
            continue
        visited.add(document)
        for raw in LINK_RE.findall(document.read_text(encoding="utf-8")):
            target = unquote(raw.strip().strip("<>").split("#", 1)[0])
            candidate = (document.parent / target).resolve()
            if candidate.is_file() and candidate.suffix == ".md" and DOCS in candidate.parents:
                pending.append(candidate)
    expected = set(DOCS.rglob("*.md"))
    assert visited == expected, "Unreachable docs:\n" + "\n".join(
        str(path.relative_to(REPO)) for path in sorted(expected - visited)
    )


def test_active_markdown_consumers_resolve_documentation_links() -> None:
    roots = [REPO / "README.md", REPO / "skills", REPO / "proj_skills", REPO / "prism_me"]
    documents = [roots[0]]
    for root in roots[1:]:
        documents.extend(root.rglob("*.md"))
    broken: list[str] = []
    for document in documents:
        for raw in LINK_RE.findall(document.read_text(encoding="utf-8")):
            target = unquote(raw.strip().strip("<>").split("#", 1)[0])
            if "docs/" not in target or target.startswith(("http:", "https:")):
                continue
            if not (document.parent / target).resolve().exists():
                broken.append(f"{document.relative_to(REPO)} -> {raw}")
    assert not broken, "Broken active documentation consumers:\n" + "\n".join(broken)
