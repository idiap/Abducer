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

"""Build a single-tabbed HTML interface over report artifacts."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
from pathlib import Path
from typing import Any

from markdown_it import MarkdownIt


REPO_ROOT = Path(__file__).resolve().parents[4]
SUPPORTED_FORMATS = (".html", ".md", ".tex", ".pdf")
DEFAULT_REPORT_PRIORITY = (
    "work-state",
    "end-to-end-proof-plausibility",
    "proof-cycle-summary",
    "proof-queue",
    "proof-queue-report",
    "macro-proof-state",
    "macro-strategy-report",
    "promising-directions-report",
    "meta-reflection-report",
    "reasoning-log-index",
    "reasoning-surface-index",
    "discovery-breakthrough-profile",
    "discovery-branch-synthesis",
    "discovery-pattern-routing",
    "expert-conjectures",
    "process-graph",
    "reasoning-dynamics",
    "conceptual-dynamics",
    "conceptual-space-animation",
    "search-space-tree",
)
LEGACY_REPORT_STEMS = {
    "proof-queue-report",
    "review-reasoner-report",
}
NON_REPORT_STEMS = {
    "kb.revised",
    "prior-art-pass-input",
    "process-graph-evolution",
    "report-hub",
    "legacy-report-inventory",
}

_MD = MarkdownIt("commonmark", {"html": True}).enable("table")
_LATEX_ENV_RE = re.compile(r"\\begin\{([a-zA-Z*]+)\}(.*?)\\end\{\1\}", re.DOTALL)
_LATEX_CMD_ARG_RE = re.compile(r"\\([A-Za-z]+)\*?\{")
_MATH_RE = re.compile(r"(\\\[(?:.|\n)*?\\\]|\\\((?:.|\n)*?\\\)|(?<!\\)\$(?:\\.|[^$])+(?<!\\)\$)", re.DOTALL)


def _clean_text(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _slug_to_label(stem: str) -> str:
    parts = [chunk for chunk in stem.replace("_", "-").split("-") if chunk]
    out: list[str] = []
    for part in parts:
        if part.isupper():
            out.append(part)
        elif part in {"kb", "np", "pdl", "html", "json", "pdf"}:
            out.append(part.upper())
        else:
            out.append(part.capitalize())
    return " ".join(out) or stem


def _report_category(stem: str, *, has_html: bool) -> str:
    if has_html:
        return "Interactive"
    if any(token in stem for token in ("proof", "plausibility", "queue", "work-state", "macro", "meta", "reasoning")):
        return "Core"
    if any(token in stem for token in ("discovery", "concept", "entrypoint", "bridge", "search-space", "coherence", "revision", "expert")):
        return "Discovery"
    return "Other"


def _protected_math(text: str) -> tuple[str, dict[str, str]]:
    tokens: dict[str, str] = {}

    def _replace(match: re.Match[str]) -> str:
        key = f"@@MATH{len(tokens)}@@"
        tokens[key] = match.group(0)
        return key

    return _MATH_RE.sub(_replace, text), tokens


def _restore_math(text: str, tokens: dict[str, str]) -> str:
    restored = text
    for key, value in tokens.items():
        restored = restored.replace(key, value)
    return restored


def _split_tex_items(body: str) -> list[str]:
    body = body.strip()
    if not body:
        return []
    parts = re.split(r"(?<!\\)\\item(?:\s*\[[^\]]*\])?\s*", body)
    return [chunk.strip() for chunk in parts if _clean_text(chunk)]


def _split_tex_rows(body: str) -> list[list[str]]:
    cleaned = re.sub(r"\\(?:toprule|midrule|bottomrule|endhead|endfirsthead|endfoot|endlastfoot)\b", "", body)
    rows: list[list[str]] = []
    for raw_row in re.split(r"(?<!\\)\\\\", cleaned):
        row = raw_row.strip()
        if not row:
            continue
        cols = [col.strip() for col in re.split(r"(?<!\\)&", row)]
        if any(_clean_text(col) for col in cols):
            rows.append(cols)
    return rows


def _replace_command(text: str, command: str, tag: str) -> str:
    pattern = re.compile(rf"\\{command}\{{([^{{}}]*)\}}")
    previous = None
    rendered = text
    while rendered != previous:
        previous = rendered
        rendered = pattern.sub(lambda m: f"<{tag}>{_convert_tex_inline(m.group(1))}</{tag}>", rendered)
    return rendered


def _convert_tex_inline(text: str) -> str:
    protected, math_tokens = _protected_math(text)
    rendered = html.escape(protected)
    for src, dst in (
        ("\\textasciicircum{}", "^"),
        ("\\textasciitilde{}", "~"),
        ("\\textbackslash{}", "\\"),
        ("\\%", "%"),
        ("\\_", "_"),
        ("\\&", "&"),
        ("\\#", "#"),
        ("\\$", "$"),
        ("\\{", "{"),
        ("\\}", "}"),
        ("~", " "),
    ):
        rendered = rendered.replace(html.escape(src), dst)
    rendered = _replace_command(rendered, "textbf", "strong")
    rendered = _replace_command(rendered, "textit", "em")
    rendered = _replace_command(rendered, "emph", "em")
    rendered = _replace_command(rendered, "texttt", "code")
    rendered = re.sub(
        r"\\url\{([^{}]+)\}",
        lambda m: f'<a href="{html.escape(m.group(1), quote=True)}">{html.escape(m.group(1))}</a>',
        rendered,
    )
    rendered = re.sub(
        r"\\href\{([^{}]+)\}\{([^{}]+)\}",
        lambda m: f'<a href="{html.escape(m.group(1), quote=True)}">{_convert_tex_inline(m.group(2))}</a>',
        rendered,
    )
    rendered = rendered.replace("\\\\", "<br>")
    rendered = rendered.replace("\n", " ")
    rendered = re.sub(r"\s{2,}", " ", rendered).strip()
    return _restore_math(rendered, math_tokens)


def _latex_environment_to_html(name: str, body: str) -> str:
    env = name.lower().rstrip("*")
    if env == "itemize":
        items = "".join(f"<li>{_latex_to_html_fragment(item)}</li>" for item in _split_tex_items(body))
        return f"<ul>{items}</ul>"
    if env == "enumerate":
        items = "".join(f"<li>{_latex_to_html_fragment(item)}</li>" for item in _split_tex_items(body))
        return f"<ol>{items}</ol>"
    if env in {"longtable", "tabular"}:
        body = re.sub(r"^\s*\{[^{}]*\}\s*", "", body, count=1)
        rows = _split_tex_rows(body)
        if not rows:
            return ""
        header = rows[0]
        data_rows = rows[1:]
        thead = "".join(f"<th>{_convert_tex_inline(col)}</th>" for col in header)
        tbody = "".join(
            "<tr>" + "".join(f"<td>{_latex_to_html_fragment(col)}</td>" for col in row) + "</tr>"
            for row in data_rows
        )
        return f"<div class=\"table-wrap\"><table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table></div>"
    if env in {"quote", "abstract"}:
        return f"<blockquote>{_latex_to_html_fragment(body)}</blockquote>"
    if env == "center":
        return f"<div class=\"tex-center\">{_latex_to_html_fragment(body)}</div>"
    return f"<pre class=\"tex-source\">{html.escape(body.strip())}</pre>"


def _latex_to_html_fragment(text: str) -> str:
    rendered = text.strip()
    if not rendered:
        return ""
    previous = None
    while rendered != previous:
        previous = rendered
        rendered = _LATEX_ENV_RE.sub(lambda m: _latex_environment_to_html(m.group(1), m.group(2)), rendered)
    rendered = re.sub(
        r"\\(?:section|section\*|subsection|subsection\*|subsubsection|subsubsection\*|paragraph|paragraph\*)\{([^{}]*)\}",
        "",
        rendered,
    )
    blocks: list[str] = []
    for chunk in re.split(r"\n\s*\n", rendered):
        piece = chunk.strip()
        if not piece:
            continue
        if piece.startswith("<"):
            blocks.append(piece)
            continue
        blocks.append(f"<p>{_convert_tex_inline(piece)}</p>")
    return "\n".join(blocks)


def latex_to_html(source: str, *, source_name: str = "") -> str:
    text = source.replace("\r\n", "\n")
    title_match = re.search(r"\\title\{([^{}]+)\}", text)
    title = _convert_tex_inline(title_match.group(1)) if title_match else _slug_to_label(Path(source_name).stem)
    document_match = re.search(r"\\begin\{document\}(.*)\\end\{document\}", text, re.DOTALL)
    body = document_match.group(1) if document_match else text
    body = re.sub(r"(?m)^\s*%.*$", "", body)
    body = re.sub(r"\\maketitle", "", body)
    body = re.sub(r"\\date\{[^{}]*\}", "", body)
    body = re.sub(
        r"\\section\*?\{([^{}]*)\}",
        lambda m: f"\n\n<h2>{_convert_tex_inline(m.group(1))}</h2>\n\n",
        body,
    )
    body = re.sub(
        r"\\subsection\*?\{([^{}]*)\}",
        lambda m: f"\n\n<h3>{_convert_tex_inline(m.group(1))}</h3>\n\n",
        body,
    )
    body = re.sub(
        r"\\subsubsection\*?\{([^{}]*)\}",
        lambda m: f"\n\n<h4>{_convert_tex_inline(m.group(1))}</h4>\n\n",
        body,
    )
    body = re.sub(
        r"\\paragraph\*?\{([^{}]*)\}",
        lambda m: f"\n\n<h5>{_convert_tex_inline(m.group(1))}</h5>\n\n",
        body,
    )
    content = _latex_to_html_fragment(body)
    converter_note = (
        "<p class=\"format-note\">Rendered from LaTeX using the built-in best-effort converter with MathJax math support."
        " For full TeX fidelity, a Pandoc or LaTeXML export path can be added later.</p>"
    )
    return (
        f'<article class="report-body tex-report">'
        f'<header class="report-heading"><h1>{title}</h1>{converter_note}</header>'
        f"{content}"
        f"</article>"
    )


def markdown_to_html(source: str, *, source_name: str = "") -> str:
    rendered = _MD.render(source)
    label = _slug_to_label(Path(source_name).stem)
    return (
        f'<article class="report-body markdown-report">'
        f'<header class="report-heading"><div class="eyebrow">Markdown</div><h1>{label}</h1></header>'
        f"{rendered}"
        f"</article>"
    )


def _relative_path(target: Path, *, start: Path) -> str:
    return os.path.relpath(target, start).replace("\\", "/")


def _include_in_hub(path: Path, *, output_html: Path | None = None) -> bool:
    if not path.is_file() or path.suffix.lower() not in SUPPORTED_FORMATS:
        return False
    if output_html is not None and path.resolve() == output_html.resolve():
        return False
    stem = path.stem
    if stem in NON_REPORT_STEMS:
        return False
    if stem in LEGACY_REPORT_STEMS:
        return False
    return True


def discover_report_groups(artifacts_dir: Path, *, output_html: Path | None = None) -> list[dict[str, Any]]:
    groups: dict[str, dict[str, Any]] = {}
    for path in sorted(artifacts_dir.iterdir()):
        if not _include_in_hub(path, output_html=output_html):
            continue
        stem = path.stem
        group = groups.setdefault(
            stem,
            {
                "key": stem,
                "label": _slug_to_label(stem),
                "formats": {},
            },
        )
        group["formats"][path.suffix.lower().lstrip(".")] = path
    ordered = list(groups.values())
    for group in ordered:
        group["category"] = _report_category(group["key"], has_html="html" in group["formats"])
        group["default_format"] = next(
            (fmt for fmt in ("html", "md", "tex", "pdf") if fmt in group["formats"]),
            "",
        )
    priority_index = {key: idx for idx, key in enumerate(DEFAULT_REPORT_PRIORITY)}
    ordered.sort(
        key=lambda row: (
            priority_index.get(row["key"], 10_000),
            row["category"],
            row["label"].lower(),
        )
    )
    return ordered


def build_hub_manifest(artifacts_dir: Path, *, output_html: Path) -> dict[str, Any]:
    report_groups = discover_report_groups(artifacts_dir, output_html=output_html)
    reports: list[dict[str, Any]] = []
    category_counts: dict[str, int] = {}
    format_counts: dict[str, int] = {"md": 0, "html": 0, "tex": 0, "pdf": 0}
    for group in report_groups:
        category_counts[group["category"]] = category_counts.get(group["category"], 0) + 1
        formats: dict[str, Any] = {}
        for fmt, path in group["formats"].items():
            format_counts[fmt] = format_counts.get(fmt, 0) + 1
            if fmt == "html":
                formats[fmt] = {
                    "kind": "iframe",
                    "src": _relative_path(path, start=output_html.parent),
                }
            elif fmt == "pdf":
                relative = _relative_path(path, start=output_html.parent)
                formats[fmt] = {
                    "kind": "iframe",
                    "src": relative,
                    "download": relative,
                }
            elif fmt == "md":
                formats[fmt] = {
                    "kind": "inline",
                    "rendered_html": markdown_to_html(path.read_text(encoding="utf-8"), source_name=path.name),
                }
            elif fmt == "tex":
                formats[fmt] = {
                    "kind": "inline",
                    "rendered_html": latex_to_html(path.read_text(encoding="utf-8"), source_name=path.name),
                }
        reports.append(
            {
                "key": group["key"],
                "label": group["label"],
                "category": group["category"],
                "default_format": group["default_format"],
                "available_formats": [fmt for fmt in ("html", "md", "tex", "pdf") if fmt in formats],
                "formats": formats,
            }
        )
    return {
        "metadata": {
            "artifacts_dir": str(artifacts_dir),
            "title": f"{artifacts_dir.name} Report Hub",
            "report_count": len(reports),
            "category_counts": category_counts,
            "format_counts": format_counts,
        },
        "reports": reports,
    }


def render_report_hub_html(manifest: dict[str, Any]) -> str:
    payload = json.dumps(manifest, ensure_ascii=False)
    title = html.escape(_clean_text(manifest.get("metadata", {}).get("title")))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <script>
    window.MathJax = {{
      tex: {{
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
      }},
      svg: {{
        fontCache: 'global'
      }}
    }};
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
  <style>
    :root {{
      --bg: #f4efe6;
      --panel: #fffdf9;
      --panel-alt: #f8f2e8;
      --border: #d9cdbd;
      --text: #231f1a;
      --muted: #645b4f;
      --accent: #b5522d;
      --accent-soft: #f3d8ca;
      --shadow: 0 20px 40px rgba(60, 41, 21, 0.08);
      --code-bg: #f3ede4;
    }}
    * {{
      box-sizing: border-box;
    }}
    body {{
      margin: 0;
      font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
      color: var(--text);
      background:
        radial-gradient(circle at top left, rgba(219, 163, 118, 0.26), transparent 26%),
        radial-gradient(circle at top right, rgba(95, 141, 179, 0.18), transparent 22%),
        linear-gradient(180deg, #fcf8f2 0%, var(--bg) 100%);
    }}
    .page {{
      display: grid;
      grid-template-columns: 320px minmax(0, 1fr);
      min-height: 100vh;
    }}
    .sidebar {{
      border-right: 1px solid var(--border);
      background: rgba(255, 252, 247, 0.92);
      backdrop-filter: blur(14px);
      padding: 22px 18px;
      position: sticky;
      top: 0;
      align-self: start;
      height: 100vh;
      overflow: auto;
    }}
    .brand {{
      margin-bottom: 18px;
    }}
    .eyebrow {{
      font-size: 12px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 8px;
    }}
    .brand h1 {{
      margin: 0;
      font-size: 28px;
      line-height: 1.08;
    }}
    .brand p {{
      margin: 10px 0 0 0;
      color: var(--muted);
      line-height: 1.5;
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
      margin: 20px 0;
    }}
    .stat {{
      padding: 12px 13px;
      border-radius: 16px;
      background: var(--panel-alt);
      border: 1px solid var(--border);
    }}
    .stat strong {{
      display: block;
      font-size: 20px;
    }}
    .stat span {{
      display: block;
      font-size: 12px;
      color: var(--muted);
      margin-top: 4px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }}
    .search {{
      width: 100%;
      padding: 12px 14px;
      border-radius: 999px;
      border: 1px solid var(--border);
      background: #fff;
      color: var(--text);
      margin-bottom: 18px;
    }}
    .category {{
      margin-bottom: 18px;
    }}
    .category h2 {{
      margin: 0 0 8px 0;
      font-size: 13px;
      color: var(--muted);
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}
    .tab-list {{
      display: grid;
      gap: 8px;
    }}
    .report-tab {{
      border: 1px solid var(--border);
      background: rgba(255, 255, 255, 0.72);
      color: var(--text);
      padding: 11px 12px;
      border-radius: 14px;
      text-align: left;
      cursor: pointer;
      transition: transform 120ms ease, border-color 120ms ease, background 120ms ease;
    }}
    .report-tab:hover {{
      transform: translateX(1px);
      border-color: var(--accent);
    }}
    .report-tab.active {{
      border-color: var(--accent);
      background: linear-gradient(135deg, #fff7f0 0%, var(--accent-soft) 100%);
      box-shadow: 0 12px 24px rgba(181, 82, 45, 0.12);
    }}
    .tab-title {{
      display: block;
      font-weight: 700;
      margin-bottom: 4px;
    }}
    .tab-meta {{
      font-size: 12px;
      color: var(--muted);
    }}
    .main {{
      padding: 24px 26px 36px 26px;
      min-width: 0;
    }}
    .hero {{
      padding: 20px 22px;
      border-radius: 24px;
      background: linear-gradient(135deg, rgba(255,255,255,0.92) 0%, rgba(248,239,225,0.94) 100%);
      border: 1px solid var(--border);
      box-shadow: var(--shadow);
      margin-bottom: 18px;
    }}
    .hero h2 {{
      margin: 0;
      font-size: 24px;
    }}
    .hero p {{
      margin: 10px 0 0 0;
      color: var(--muted);
      line-height: 1.5;
      max-width: 920px;
    }}
    .format-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin: 16px 0 18px 0;
    }}
    .format-pill {{
      border: 1px solid var(--border);
      background: #fff;
      padding: 10px 14px;
      border-radius: 999px;
      cursor: pointer;
      font-size: 13px;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      transition: border-color 120ms ease, background 120ms ease;
    }}
    .format-pill.active {{
      border-color: var(--accent);
      background: var(--accent-soft);
    }}
    .viewer-card {{
      border: 1px solid var(--border);
      border-radius: 24px;
      background: rgba(255, 253, 249, 0.96);
      box-shadow: var(--shadow);
      overflow: hidden;
      min-height: 72vh;
    }}
    .viewer-head {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      padding: 14px 18px;
      border-bottom: 1px solid var(--border);
      background: rgba(248, 242, 232, 0.8);
    }}
    .viewer-head strong {{
      font-size: 15px;
    }}
    .viewer-note {{
      font-size: 12px;
      color: var(--muted);
    }}
    .viewer-body {{
      padding: 22px;
      min-height: 64vh;
      overflow: auto;
    }}
    .viewer-body iframe {{
      width: 100%;
      min-height: 70vh;
      border: 0;
      background: #fff;
    }}
    .report-body {{
      max-width: 960px;
      margin: 0 auto;
      line-height: 1.6;
    }}
    .report-heading {{
      margin-bottom: 18px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--border);
    }}
    .report-heading h1 {{
      margin: 0;
      font-size: 30px;
      line-height: 1.1;
    }}
    .format-note {{
      margin: 10px 0 0 0;
      color: var(--muted);
    }}
    .report-body h1, .report-body h2, .report-body h3, .report-body h4, .report-body h5 {{
      line-height: 1.2;
      margin-top: 1.3em;
      margin-bottom: 0.5em;
    }}
    .report-body pre {{
      padding: 14px 16px;
      overflow: auto;
      border-radius: 16px;
      background: var(--code-bg);
      border: 1px solid var(--border);
    }}
    .report-body code {{
      background: var(--code-bg);
      border-radius: 6px;
      padding: 0.14em 0.35em;
    }}
    .report-body blockquote {{
      margin: 1.1em 0;
      padding: 0.8em 1em;
      border-left: 4px solid var(--accent);
      background: rgba(243, 216, 202, 0.28);
      border-radius: 0 14px 14px 0;
    }}
    .report-body table {{
      width: 100%;
      border-collapse: collapse;
      margin: 1em 0 1.4em 0;
    }}
    .report-body th, .report-body td {{
      border: 1px solid var(--border);
      padding: 10px 12px;
      vertical-align: top;
      text-align: left;
    }}
    .report-body th {{
      background: rgba(248, 242, 232, 0.9);
    }}
    .table-wrap {{
      overflow: auto;
    }}
    .tex-source {{
      white-space: pre-wrap;
    }}
    .empty {{
      color: var(--muted);
      font-style: italic;
    }}
    @media (max-width: 1080px) {{
      .page {{
        grid-template-columns: 1fr;
      }}
      .sidebar {{
        position: static;
        height: auto;
        border-right: 0;
        border-bottom: 1px solid var(--border);
      }}
      .viewer-card {{
        min-height: auto;
      }}
      .viewer-body iframe {{
        min-height: 60vh;
      }}
    }}
  </style>
</head>
<body>
  <div class="page">
    <aside class="sidebar">
      <div class="brand">
        <div class="eyebrow">Unified Report Interface</div>
        <h1 id="hub-title"></h1>
        <p id="hub-summary"></p>
      </div>
      <div class="stats">
        <div class="stat"><strong id="report-count">0</strong><span>Reports</span></div>
        <div class="stat"><strong id="interactive-count">0</strong><span>Interactive</span></div>
        <div class="stat"><strong id="markdown-count">0</strong><span>Markdown</span></div>
        <div class="stat"><strong id="tex-count">0</strong><span>LaTeX</span></div>
      </div>
      <input id="search" class="search" type="search" placeholder="Filter reports">
      <div id="tab-sections"></div>
    </aside>
    <main class="main">
      <section class="hero">
        <div class="eyebrow">Entry Point</div>
        <h2 id="current-title"></h2>
        <p id="current-summary"></p>
      </section>
      <div id="format-bar" class="format-bar"></div>
      <section class="viewer-card">
        <div class="viewer-head">
          <div>
            <strong id="viewer-format-label"></strong>
            <div id="viewer-note" class="viewer-note"></div>
          </div>
          <a id="open-link" target="_blank" rel="noopener noreferrer">Open raw artifact</a>
        </div>
        <div id="viewer-body" class="viewer-body"></div>
      </section>
    </main>
  </div>
  <script id="report-manifest" type="application/json">{payload}</script>
  <script>
    const manifest = JSON.parse(document.getElementById('report-manifest').textContent);
    const reports = manifest.reports || [];
    const reportByKey = Object.fromEntries(reports.map((report) => [report.key, report]));
    const categoryOrder = ['Core', 'Discovery', 'Interactive', 'Other'];
    let activeReportKey = reports.length ? reports[0].key : '';
    let activeFormat = activeReportKey ? reportByKey[activeReportKey].default_format : '';

    const hubTitle = document.getElementById('hub-title');
    const hubSummary = document.getElementById('hub-summary');
    const reportCount = document.getElementById('report-count');
    const interactiveCount = document.getElementById('interactive-count');
    const markdownCount = document.getElementById('markdown-count');
    const texCount = document.getElementById('tex-count');
    const tabSections = document.getElementById('tab-sections');
    const search = document.getElementById('search');
    const currentTitle = document.getElementById('current-title');
    const currentSummary = document.getElementById('current-summary');
    const formatBar = document.getElementById('format-bar');
    const viewerBody = document.getElementById('viewer-body');
    const viewerFormatLabel = document.getElementById('viewer-format-label');
    const viewerNote = document.getElementById('viewer-note');
    const openLink = document.getElementById('open-link');

    function counts() {{
      const formatCounts = manifest.metadata?.format_counts || {{}};
      hubTitle.textContent = manifest.metadata?.title || 'Report Hub';
      hubSummary.textContent = `${{manifest.metadata?.report_count || 0}} report groups, unified across Markdown, HTML, PDF, and LaTeX-backed views.`;
      reportCount.textContent = String(manifest.metadata?.report_count || 0);
      interactiveCount.textContent = String(formatCounts.html || 0);
      markdownCount.textContent = String(formatCounts.md || 0);
      texCount.textContent = String(formatCounts.tex || 0);
    }}

    function reportGroups(filterText) {{
      const needle = (filterText || '').trim().toLowerCase();
      const grouped = new Map();
      for (const category of categoryOrder) {{
        grouped.set(category, []);
      }}
      for (const report of reports) {{
        const haystack = `${{report.label}} ${{report.key}} ${{report.category}}`.toLowerCase();
        if (needle && !haystack.includes(needle)) continue;
        if (!grouped.has(report.category)) grouped.set(report.category, []);
        grouped.get(report.category).push(report);
      }}
      return grouped;
    }}

    function renderTabs() {{
      const grouped = reportGroups(search.value);
      const parts = [];
      for (const category of categoryOrder) {{
        const rows = grouped.get(category) || [];
        if (!rows.length) continue;
        const buttons = rows.map((report) => `
          <button class="report-tab ${{report.key === activeReportKey ? 'active' : ''}}" type="button" data-report-key="${{report.key}}">
            <span class="tab-title">${{report.label}}</span>
            <span class="tab-meta">${{report.available_formats.join(' / ').toUpperCase()}}</span>
          </button>
        `).join('');
        parts.push(`<section class="category"><h2>${{category}}</h2><div class="tab-list">${{buttons}}</div></section>`);
      }}
      tabSections.innerHTML = parts.join('') || '<p class="empty">No reports match the current filter.</p>';
      tabSections.querySelectorAll('[data-report-key]').forEach((button) => {{
        button.addEventListener('click', () => {{
          activeReportKey = button.dataset.reportKey;
          activeFormat = reportByKey[activeReportKey].default_format;
          renderTabs();
          renderViewer();
        }});
      }});
    }}

    function formatLabel(format) {{
      return format.toUpperCase() + (format === 'tex' ? ' rendered to HTML' : format === 'md' ? ' rendered to HTML' : '');
    }}

    function renderViewer() {{
      const report = reportByKey[activeReportKey];
      if (!report) {{
        currentTitle.textContent = 'No report available';
        currentSummary.textContent = 'The current artifacts directory did not contain supported report files.';
        formatBar.innerHTML = '';
        viewerBody.innerHTML = '<p class="empty">No report content available.</p>';
        viewerFormatLabel.textContent = '';
        viewerNote.textContent = '';
        openLink.removeAttribute('href');
        return;
      }}
      if (!report.formats[activeFormat]) {{
        activeFormat = report.default_format;
      }}
      currentTitle.textContent = report.label;
      currentSummary.textContent = `Category: ${{report.category}}. Available formats: ${{report.available_formats.join(', ').toUpperCase()}}.`;
      formatBar.innerHTML = report.available_formats.map((format) => `
        <button class="format-pill ${{format === activeFormat ? 'active' : ''}}" type="button" data-format="${{format}}">
          ${{format.toUpperCase()}}
        </button>
      `).join('');
      formatBar.querySelectorAll('[data-format]').forEach((button) => {{
        button.addEventListener('click', () => {{
          activeFormat = button.dataset.format;
          renderViewer();
        }});
      }});
      const formatData = report.formats[activeFormat];
      viewerFormatLabel.textContent = formatLabel(activeFormat);
      viewerNote.textContent = activeFormat === 'tex'
        ? 'LaTeX is converted to structural HTML and handed to MathJax for math rendering.'
        : activeFormat === 'md'
          ? 'Markdown is pre-rendered into HTML.'
          : activeFormat === 'html'
            ? 'Interactive report embedded directly.'
            : 'Raw PDF embedded directly.';
      const rawLink = formatData.src || formatData.download || '#';
      openLink.href = rawLink;
      openLink.textContent = activeFormat === 'html' ? 'Open raw HTML' : activeFormat === 'pdf' ? 'Open PDF' : `Open raw ${{activeFormat.toUpperCase()}}`;
      if (formatData.kind === 'iframe') {{
        viewerBody.innerHTML = `<iframe title="${{report.label}} (${{activeFormat}})" src="${{formatData.src}}"></iframe>`;
      }} else {{
        viewerBody.innerHTML = formatData.rendered_html || '<p class="empty">No rendered content available.</p>';
        if (window.MathJax && typeof window.MathJax.typesetPromise === 'function') {{
          window.MathJax.typesetPromise([viewerBody]).catch(() => null);
        }}
      }}
    }}

    counts();
    renderTabs();
    renderViewer();
    search.addEventListener('input', renderTabs);
  </script>
</body>
</html>
"""


def write_report_hub(*, artifacts_dir: Path, output_html: Path) -> dict[str, Any]:
    manifest = build_hub_manifest(artifacts_dir, output_html=output_html)
    output_html.parent.mkdir(parents=True, exist_ok=True)
    output_html.write_text(render_report_hub_html(manifest), encoding="utf-8")
    return manifest


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifacts-dir", required=True, help="Path to artifacts/<kb-ref>.")
    ap.add_argument("--output-html", default="", help="Optional output HTML path.")
    args = ap.parse_args()

    artifacts_dir = Path(args.artifacts_dir)
    if not artifacts_dir.is_absolute():
        artifacts_dir = (REPO_ROOT / artifacts_dir).resolve()
    if not artifacts_dir.exists():
        raise SystemExit(f"[ERROR] Artifacts directory does not exist: {artifacts_dir}")
    output_html = Path(args.output_html) if args.output_html else artifacts_dir / "report-hub.html"
    if not output_html.is_absolute():
        output_html = (REPO_ROOT / output_html).resolve()
    manifest = write_report_hub(artifacts_dir=artifacts_dir, output_html=output_html)
    print(f"[OK] Wrote report hub HTML: {output_html}")
    print(f"[OK] Included report groups: {manifest['metadata']['report_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
