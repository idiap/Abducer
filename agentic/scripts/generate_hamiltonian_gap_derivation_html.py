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

"""Generate self-contained HTML with rendered MathML for the Hamiltonian derivation."""

from __future__ import annotations

import html

from agentic_common import ROOT, load_json_object, rel


REPORT = ROOT / "agentic/reports/hamiltonian_gap_derivation/latest.json"
OUT = ROOT / "agentic/reports/hamiltonian_gap_derivation/latest.html"


CSS = r"""
:root {
  color-scheme: dark;
  --bg: #080b10;
  --panel: #111821;
  --panel-2: #17202b;
  --line: #2a3544;
  --text: #eef5f8;
  --muted: #aeb8c5;
  --math: #e9f7ff;
  --accent: #70d6ff;
  --target: #f2c94c;
  --warn: #ffbc66;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font: 15px/1.55 ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
.shell { max-width: 1180px; margin: 0 auto; padding: 28px clamp(16px, 3vw, 36px) 44px; }
.top {
  border-bottom: 1px solid var(--line);
  padding-bottom: 18px;
  margin-bottom: 18px;
}
.eyebrow {
  color: var(--target);
  text-transform: uppercase;
  letter-spacing: .08em;
  font-size: 12px;
  margin: 0 0 8px;
}
h1 { margin: 0; font-size: clamp(26px, 4vw, 42px); line-height: 1.05; letter-spacing: 0; }
h2 { font-size: 22px; margin: 28px 0 10px; }
h3 { font-size: 18px; margin: 22px 0 8px; }
p { margin: 8px 0; }
.muted { color: var(--muted); }
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
  gap: 10px;
  margin: 18px 0;
}
.card, .step {
  border: 1px solid var(--line);
  background: var(--panel);
  border-radius: 8px;
  padding: 14px;
}
.card strong { display: block; color: var(--accent); margin-bottom: 4px; }
.step { margin: 12px 0; border-left: 4px solid var(--accent); }
.formula {
  margin: 12px 0;
  padding: 14px;
  border: 1px solid #314257;
  background: #0b1119;
  border-radius: 8px;
  overflow-x: auto;
}
math {
  display: block;
  color: var(--math);
  font-size: 1.22rem;
  line-height: 1.7;
  min-width: max-content;
}
.tex {
  margin-top: 8px;
  color: var(--muted);
  font: 12px/1.4 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  white-space: pre-wrap;
}
.equation-context {
  border: 1px solid #334150;
  background: #0d141d;
  border-radius: 8px;
  padding: 12px 14px;
  margin: 12px 0;
}
.equation-context h4 {
  margin: 0 0 8px;
  font-size: 14px;
  color: var(--target);
}
.equation-context ul {
  margin: 6px 0 0;
}
.equation-context li strong {
  color: var(--accent);
}
ul { padding-left: 20px; }
li { margin: 5px 0; }
.progress-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 10px;
  margin: 12px 0 18px;
}
.progress-card {
  border: 1px solid var(--line);
  background: var(--panel-2);
  border-radius: 8px;
  padding: 14px;
}
.progress-card strong {
  display: block;
  color: var(--target);
  margin-bottom: 8px;
}
.why-label {
  color: var(--accent);
  font-weight: 700;
}
.warning {
  border-color: var(--warn);
  background: #1b1510;
}
.code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  color: var(--muted);
  overflow-wrap: anywhere;
}
@media (max-width: 720px) {
  math { font-size: 1rem; }
  .shell { padding-top: 20px; }
}
"""


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


MATHML_BY_STEP = {
    1: r"""
<math display="block">
  <semantics>
    <mrow>
      <mi>U</mi><mo>(</mo><mi>t</mi><mo>)</mo><mo>=</mo>
      <msup><mi>e</mi><mrow><mo>-</mo><mi>i</mi><mi>t</mi><mi>H</mi></mrow></msup>
      <mo>,</mo><mspace width="1em"/>
      <mi>H</mi><mo>=</mo><msup><mi>H</mi><mo>*</mo></msup>
      <mo>,</mo><mspace width="1em"/>
      <mi>H</mi><mo>&ge;</mo><mn>0</mn>
    </mrow>
    <annotation encoding="application/x-tex">U(t)=e^{-itH},\qquad H=H^*,\qquad H\ge 0.</annotation>
  </semantics>
</math>
""",
    2: r"""
<math display="block">
  <semantics>
    <mrow>
      <msub><mi>P</mi><mn>0</mn></msub><mo>=</mo><mo>|</mo><mi>&Omega;</mi><mo>&rangle;</mo><mo>&langle;</mo><mi>&Omega;</mi><mo>|</mo>
      <mo>,</mo><mspace width="1em"/>
      <msub><mi>P</mi><mo>&perp;</mo></msub><mo>=</mo><mi>I</mi><mo>-</mo><msub><mi>P</mi><mn>0</mn></msub>
      <mo>,</mo><mspace width="1em"/>
      <mi>H</mi><mi>&Omega;</mi><mo>=</mo><mn>0</mn>
    </mrow>
    <annotation encoding="application/x-tex">P_0=\lvert\Omega\rangle\langle\Omega\rvert,\qquad P_\perp=I-P_0,\qquad H\Omega=0.</annotation>
  </semantics>
</math>
""",
    3: r"""
<math display="block">
  <semantics>
    <mrow>
      <msub><mi>E</mi><mi>H</mi></msub><mo>(</mo><mo>(</mo><mn>0</mn><mo>,</mo><mi>&Delta;</mi><mo>)</mo><mo>)</mo>
      <msub><mi>P</mi><mo>&perp;</mo></msub><mo>=</mo><mn>0</mn>
      <mspace width="1em"/><mo>&Longleftrightarrow;</mo><mspace width="1em"/>
      <mi>spec</mi><mo>(</mo><mi>H</mi><mo>|</mo><msub><mi>P</mi><mo>&perp;</mo></msub><msub><mi>H</mi><mi>YM</mi></msub><mo>)</mo>
      <mo>&sube;</mo><mo>[</mo><mi>&Delta;</mi><mo>,</mo><mi>&infin;</mi><mo>)</mo>
    </mrow>
    <annotation encoding="application/x-tex">E_H((0,\Delta))P_\perp=0\quad\Longleftrightarrow\quad \operatorname{spec}(H|_{P_\perp\mathcal H_{\mathrm{YM}}})\subset[\Delta,\infty).</annotation>
  </semantics>
</math>
""",
    4: r"""
<math display="block">
  <semantics>
    <mrow>
      <mi>&psi;</mi><mo>&perp;</mo><mi>&Omega;</mi><mo>&Longrightarrow;</mo>
      <mo>&langle;</mo><mi>&psi;</mi><mo>,</mo><mi>H</mi><mi>&psi;</mi><mo>&rangle;</mo>
      <mo>=</mo><msubsup><mo>&int;</mo><mrow><mo>[</mo><mi>&Delta;</mi><mo>,</mo><mi>&infin;</mi><mo>)</mo></mrow><mrow></mrow></msubsup>
      <mi>&lambda;</mi><mspace width=".2em"/><mi>d</mi><msub><mi>&mu;</mi><mi>&psi;</mi></msub><mo>(</mo><mi>&lambda;</mi><mo>)</mo>
      <mo>&ge;</mo><mi>&Delta;</mi><msup><mrow><mo>||</mo><mi>&psi;</mi><mo>||</mo></mrow><mn>2</mn></msup>
    </mrow>
    <annotation encoding="application/x-tex">\psi\perp\Omega \Longrightarrow \langle\psi,H\psi\rangle=\int_{[\Delta,\infty)}\lambda\,d\mu_\psi(\lambda)\ge\Delta\|\psi\|^2.</annotation>
  </semantics>
</math>
""",
    5: r"""
<math display="block">
  <semantics>
    <mrow>
      <msub><mi>C</mi><mi>A</mi></msub><mo>(</mo><mi>t</mi><mo>)</mo><mo>=</mo>
      <mo>&langle;</mo><mi>A</mi><mi>&Omega;</mi><mo>,</mo><msup><mi>e</mi><mrow><mo>-</mo><mi>t</mi><mi>H</mi></mrow></msup><mi>A</mi><mi>&Omega;</mi><mo>&rangle;</mo>
      <mo>=</mo><msubsup><mo>&int;</mo><mrow><mo>[</mo><mi>&Delta;</mi><mo>,</mo><mi>&infin;</mi><mo>)</mo></mrow><mrow></mrow></msubsup>
      <msup><mi>e</mi><mrow><mo>-</mo><mi>t</mi><mi>&lambda;</mi></mrow></msup><mspace width=".2em"/><mi>d</mi><msub><mi>&mu;</mi><mi>A</mi></msub><mo>(</mo><mi>&lambda;</mi><mo>)</mo>
      <mo>&le;</mo><msup><mi>e</mi><mrow><mo>-</mo><mi>&Delta;</mi><mi>t</mi></mrow></msup><msup><mrow><mo>||</mo><mi>A</mi><mi>&Omega;</mi><mo>||</mo></mrow><mn>2</mn></msup>
    </mrow>
    <annotation encoding="application/x-tex">C_A(t)=\langle A\Omega,e^{-tH}A\Omega\rangle=\int_{[\Delta,\infty)}e^{-t\lambda}\,d\mu_A(\lambda)\le e^{-\Delta t}\|A\Omega\|^2.</annotation>
  </semantics>
</math>
""",
    6: r"""
<math display="block">
  <semantics>
    <mrow>
      <mover><mrow><mo>{</mo><mo>(</mo><mi>A</mi><mo>-</mo><mo>&langle;</mo><mi>&Omega;</mi><mo>,</mo><mi>A</mi><mi>&Omega;</mi><mo>&rangle;</mo><mo>)</mo><mi>&Omega;</mi><mo>:</mo><mi>A</mi><mo>&in;</mo><msub><mi>A</mi><mi>ginv</mi></msub><mo>}</mo></mrow><mo>&macr;</mo></mover>
      <mo>=</mo><msub><mi>P</mi><mo>&perp;</mo></msub><msub><mi>H</mi><mi>YM</mi></msub>
    </mrow>
    <annotation encoding="application/x-tex">\overline{\{(A-\langle\Omega,A\Omega\rangle)\Omega:A\in\mathcal A_{\mathrm{ginv}}\}}=P_\perp\mathcal H_{\mathrm{YM}}.</annotation>
  </semantics>
</math>
""",
    7: r"""
<math display="block">
  <semantics>
    <mrow>
      <mi>inf</mi><mi>&sigma;</mi><mo>(</mo><msub><mi>H</mi><mi>a</mi></msub><mo>|</mo><msub><mi>P</mi><mrow><mo>&perp;</mo><mo>,</mo><mi>a</mi></mrow></msub><mo>)</mo>
      <mo>&ge;</mo><msub><mi>&Delta;</mi><mi>a</mi></msub>
      <mo>,</mo><mspace width="1em"/>
      <mi>liminf</mi><mspace width=".2em"/><msub><mi>&Delta;</mi><mi>a</mi></msub><mo>&ge;</mo><mi>&Delta;</mi><mo>&gt;</mo><mn>0</mn>
    </mrow>
    <annotation encoding="application/x-tex">\inf\sigma(H_a|_{P_{\perp,a}})\ge\Delta_a,\quad \liminf_{a\to0}\Delta_a\ge\Delta>0.</annotation>
  </semantics>
</math>
""",
}


def mathml_for_step(step: dict) -> str:
    return MATHML_BY_STEP.get(int(step.get("step", 0)), f"<pre>{esc(step.get('formula', ''))}</pre>")


def render_list(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def render_progress(items: list[object]) -> str:
    cards = []
    for item in items:
        if isinstance(item, dict):
            cards.append(
                "<article class='progress-card'>"
                f"<strong>{esc(item.get('claim'))}</strong>"
                f"<p><span class='why-label'>Why:</span> {esc(item.get('why'))}</p>"
                "</article>"
            )
        else:
            cards.append(f"<article class='progress-card'><strong>{esc(item)}</strong></article>")
    return "<div class='progress-list'>" + "".join(cards) + "</div>"


def render_equation_context(step: dict) -> str:
    context = step.get("equation_context", {})
    if not isinstance(context, dict):
        return ""
    rows = []
    for definition in context.get("definitions", []):
        rows.append(f"<li><strong>Definition:</strong> {esc(definition)}</li>")
    assumptions_used = context.get("assumptions_used", [])
    if assumptions_used:
        rows.append(f"<li><strong>Assumptions used:</strong> {esc(', '.join(assumptions_used))}</li>")
    for condition in context.get("valid_when", []):
        rows.append(f"<li><strong>Valid when:</strong> {esc(condition)}</li>")
    if not rows:
        return ""
    return "<div class='equation-context'><h4>Equation Context</h4><ul>" + "".join(rows) + "</ul></div>"


def render_derivation(item: dict) -> str:
    symbols = "".join(
        f"<div class='card'><strong>{esc(symbol)}</strong><span>{esc(meaning)}</span></div>"
        for symbol, meaning in item.get("symbols", {}).items()
    )
    assumptions = "".join(
        "<div class='card'>"
        f"<strong>{esc(row.get('id'))} {esc(row.get('name'))}</strong>"
        f"<p>{esc(row.get('formula'))}</p>"
        f"<p class='muted'>Source: <span class='code'>{esc(row.get('source_kb'))}</span> · {esc(row.get('status'))}</p>"
        "</div>"
        for row in item.get("assumptions", [])
    )
    steps = []
    for step in item.get("derivation_steps", []):
        formula = esc(step.get("formula", ""))
        steps.append(
            "<section class='step'>"
            f"<h3>{esc(step.get('step'))}. {esc(step.get('title'))}</h3>"
            f"<p>{esc(step.get('derivation'))}</p>"
            f"{render_equation_context(step)}"
            f"<div class='formula'>{mathml_for_step(step)}<div class='tex'>{formula}</div></div>"
            f"<p class='muted'>Open obligation: {esc(step.get('open_obligation'))}</p>"
            "</section>"
        )
    return (
        f"<section><h2>Route {esc(item.get('candidate_id'))}</h2>"
        f"<p class='code'>{esc(item.get('route_text'))}</p>"
        f"<h3>Mathematical Subclaim</h3><p>{esc(item.get('mathematical_subclaim'))}</p>"
        f"<h3>Symbols</h3><div class='grid'>{symbols}</div>"
        f"<h3>Assumptions</h3><div class='grid'>{assumptions}</div>"
        f"<h3>Rendered Derivation</h3>{''.join(steps)}"
        f"<section class='card warning'><h3>Candidate Derivation</h3><p>{esc(item.get('candidate_derivation'))}</p></section>"
        f"<h3>What Would Count As Progress</h3>{render_progress(item.get('what_would_count_as_progress', []))}"
        f"<h3>What Does Not Count</h3>{render_list(item.get('what_does_not_count', []))}"
        "</section>"
    )


def render_html(report: dict) -> str:
    derivations = "".join(render_derivation(item) for item in report.get("derivations", []))
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Hamiltonian Gap Derivation</title>
  <style>{CSS}</style>
</head>
<body>
  <main class="shell">
    <header class="top">
      <p class="eyebrow">Yang-Mills Long-Horizon Reasoning</p>
      <h1>Hamiltonian Spectral-Gap Derivation</h1>
      <p class="muted">Target: <span class="code">{esc(report.get('target_id'))}</span></p>
      <p>{esc(report.get('scope'))}</p>
    </header>
    {derivations}
  </main>
</body>
</html>
"""


def main() -> int:
    report = load_json_object(REPORT)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render_html(report), encoding="utf-8")
    print(f"Wrote {rel(OUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
