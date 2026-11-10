# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Assemble the self-contained Explorer with its shared report admission code."""

from pathlib import Path


def explorer_html() -> str:
    """Embed the same report viewer used by Sites, without a CDN dependency."""
    directory = Path(__file__).with_name("ui")
    script = (directory / "report_viewer.js").read_text()
    return (directory / "explorer.html").read_text().replace(
        "<!-- ABDUCER_REPORT_VIEWER -->", "<script>" + script + "</script>"
    )
