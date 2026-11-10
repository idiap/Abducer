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

"""Generate a self-contained dark HTML reasoning monitor."""

from __future__ import annotations

import html
import json

from agentic_common import ROOT, load_json_object, rel


PACKET = ROOT / "agentic/reports/reasoning_monitor/latest.json"
OUT = ROOT / "agentic/reports/reasoning_monitor/latest.html"


CSS = r"""
:root {
  color-scheme: dark;
  --bg: #090d12;
  --panel: #111821;
  --panel-2: #17202b;
  --line: #263241;
  --text: #eef4f8;
  --muted: #a9b5c2;
  --target: #f2c94c;
  --frontier: #4cc9f0;
  --pressure: #d65db1;
  --route: #64d68a;
  --validation: #7aa2ff;
  --milestone: #2fd6b5;
  --drift: #ffb454;
  --fail: #ff6678;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font: 14px/1.45 ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
button, select, input { font: inherit; }
.shell {
  min-height: 100vh;
  display: grid;
  grid-template-rows: auto auto 1fr;
}
.topbar {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 18px;
  padding: 20px clamp(16px, 3vw, 34px) 14px;
  border-bottom: 1px solid var(--line);
  background: #0b1016;
}
.title-block { min-width: 0; }
.eyebrow {
  margin: 0 0 6px;
  color: var(--target);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: .08em;
}
h1 {
  margin: 0;
  font-size: clamp(22px, 3vw, 34px);
  line-height: 1.08;
  letter-spacing: 0;
}
.goal {
  margin: 8px 0 0;
  max-width: 1050px;
  color: var(--muted);
}
.status-stack {
  display: grid;
  grid-template-columns: repeat(2, minmax(120px, 1fr));
  gap: 8px;
  align-self: start;
}
.metric {
  min-width: 0;
  padding: 10px 12px;
  border: 1px solid var(--line);
  background: var(--panel);
}
.metric strong { display: block; font-size: 20px; line-height: 1.1; }
.metric span { color: var(--muted); font-size: 12px; }
.controls {
  display: grid;
  grid-template-columns: minmax(180px, 1fr) repeat(4, minmax(130px, 180px));
  gap: 10px;
  padding: 12px clamp(16px, 3vw, 34px);
  border-bottom: 1px solid var(--line);
  background: #0d131a;
}
.search, .select {
  width: 100%;
  min-height: 38px;
  color: var(--text);
  background: var(--panel);
  border: 1px solid var(--line);
  padding: 8px 10px;
  border-radius: 6px;
}
.tabs {
  display: flex;
  gap: 8px;
  padding: 14px clamp(16px, 3vw, 34px) 4px;
  overflow-x: auto;
}
.tab {
  border: 1px solid var(--line);
  color: var(--muted);
  background: var(--panel);
  min-height: 36px;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  white-space: nowrap;
}
.tab.active {
  color: var(--text);
  border-color: var(--frontier);
  background: #132433;
}
.content {
  padding: 14px clamp(16px, 3vw, 34px) 36px;
}
.grid {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(320px, .9fr);
  gap: 14px;
}
.panel {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 14px;
  min-width: 0;
}
.panel h2, .panel h3 { margin: 0 0 10px; letter-spacing: 0; }
.panel h2 { font-size: 18px; }
.panel h3 { font-size: 15px; }
.muted { color: var(--muted); }
.commitments {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 8px;
}
.commitment, .card {
  border: 1px solid var(--line);
  background: var(--panel-2);
  border-radius: 8px;
  padding: 10px;
  min-width: 0;
}
.commitment strong, .card strong { display: block; overflow-wrap: anywhere; }
.card { margin-bottom: 10px; }
.card[data-lane="target"] { border-left: 4px solid var(--target); }
.card[data-lane="dependency"] { border-left: 4px solid var(--frontier); }
.card[data-lane="conceptual"] { border-left: 4px solid var(--pressure); }
.card[data-lane="candidate"] { border-left: 4px solid var(--route); }
.card[data-lane="validation"] { border-left: 4px solid var(--validation); }
.card[data-lane="milestone"] { border-left: 4px solid var(--milestone); }
.card[data-lane="drift"] { border-left: 4px solid var(--drift); }
.row {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}
.pill {
  display: inline-flex;
  align-items: center;
  min-height: 24px;
  border-radius: 999px;
  border: 1px solid var(--line);
  padding: 2px 8px;
  color: var(--text);
  background: #101721;
  font-size: 12px;
}
.pill.target { border-color: var(--target); color: var(--target); }
.pill.success { border-color: var(--milestone); color: var(--milestone); }
.pill.warn { border-color: var(--drift); color: var(--drift); }
.pill.fail { border-color: var(--fail); color: var(--fail); }
.meter {
  width: 100%;
  height: 8px;
  background: #0d131a;
  border: 1px solid var(--line);
  border-radius: 999px;
  overflow: hidden;
  margin: 8px 0;
}
.meter > span {
  display: block;
  height: 100%;
  background: var(--route);
}
details {
  margin-top: 8px;
  border-top: 1px solid var(--line);
  padding-top: 8px;
}
summary { cursor: pointer; color: var(--frontier); }
ul { padding-left: 18px; }
li { margin: 4px 0; overflow-wrap: anywhere; }
.section { display: none; }
.section.active { display: block; }
.timeline {
  position: relative;
  padding-left: 16px;
}
.timeline::before {
  content: "";
  position: absolute;
  left: 4px;
  top: 4px;
  bottom: 8px;
  width: 2px;
  background: var(--line);
}
.timeline .card { position: relative; }
.timeline .card::before {
  content: "";
  position: absolute;
  left: -17px;
  top: 14px;
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--frontier);
}
.empty {
  color: var(--muted);
  padding: 18px;
  border: 1px dashed var(--line);
  border-radius: 8px;
}
.code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 12px;
  color: #cbd6e2;
  overflow-wrap: anywhere;
}
.story-intro {
  max-width: 980px;
  color: var(--muted);
}
.story-beat h4 {
  margin: 12px 0 4px;
  color: var(--frontier);
  font-size: 13px;
}
.equation-stack {
  display: grid;
  gap: 8px;
  margin: 10px 0 12px;
}
.equation {
  border: 1px solid var(--line);
  background: #0d131a;
  border-radius: 6px;
  padding: 9px 10px;
}
.equation-label {
  display: block;
  margin-bottom: 4px;
  color: var(--muted);
  font-size: 12px;
}
.equation-code {
  display: block;
  color: #f7fbff;
  font-family: ui-serif, Georgia, "Times New Roman", serif;
  font-size: 16px;
  overflow-wrap: anywhere;
}
.math-roman, .math-text {
  font-family: Inter, ui-sans-serif, system-ui, sans-serif;
  font-style: normal;
}
.math-cal {
  font-family: ui-serif, Georgia, "Times New Roman", serif;
  font-style: italic;
  letter-spacing: 0;
}
.math-arrow {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  margin: 0 2px;
}
.math-arrow-label {
  color: #cbd6e2;
  font-size: 11px;
}
.overline {
  text-decoration: overline;
}
.milestone-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 10px;
}
.milestone-card h4 {
  margin: 12px 0 4px;
  color: var(--milestone);
  font-size: 13px;
}
.reorientation-card h4 {
  margin: 12px 0 4px;
  color: var(--pressure);
  font-size: 13px;
}
.control-columns {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 10px;
}
@media (max-width: 920px) {
  .topbar { grid-template-columns: 1fr; }
  .status-stack { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .controls { grid-template-columns: 1fr 1fr; }
  .grid { grid-template-columns: 1fr; }
}
@media (max-width: 560px) {
  .controls { grid-template-columns: 1fr; }
  .status-stack { grid-template-columns: 1fr; }
  .tabs { padding-top: 10px; }
}
"""


JS = r"""
const DATA = JSON.parse(document.getElementById('monitor-data').textContent);
const state = { tab: 'overview', lane: 'all', status: 'all', commitment: 'all', evidence: 'all', q: '' };
const $ = (id) => document.getElementById(id);
function esc(value) {
  return String(value ?? '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
}
function list(items, cls='') {
  if (!items || !items.length) return '<p class="muted">None.</p>';
  return `<ul class="${cls}">${items.map(x => `<li>${esc(x)}</li>`).join('')}</ul>`;
}
function listSection(title, items) {
  return items && items.length ? `<h4>${esc(title)}</h4>${list(items)}` : '';
}
function equationBlock(eq) {
  const source = eq.latex || eq.display || '';
  const rendered = renderMathText(source);
  return `<div class="equation">
    <span class="equation-label">${esc(eq.label || 'equation')}</span>
    <span class="equation-code">${rendered}</span>
    ${eq.valid_when ? `<span class="muted">Valid when: ${esc(eq.valid_when)}</span>` : ''}
  </div>`;
}
function equationStack(items) {
  return items && items.length ? `<div class="equation-stack">${items.map(equationBlock).join('')}</div>` : '';
}
function renderScripts(text) {
  let previous = '';
  while (previous !== text) {
    previous = text;
    text = text
      .replace(/\^\{([^{}]+)\}/g, '<sup>$1</sup>')
      .replace(/_\{([^{}]+)\}/g, '<sub>$1</sub>');
  }
  return text
    .replace(/\^([A-Za-z0-9α-ωΑ-Ω∞⊥]+)/g, '<sup>$1</sup>')
    .replace(/_([A-Za-z0-9α-ωΑ-Ω∞⊥]+)/g, '<sub>$1</sub>');
}
function normalizeMathSource(value) {
  let text = String(value ?? '');
  for (let i = 0; i < 2; i += 1) {
    text = text
      .replace(/&amp;/gi, '&')
      .replace(/&lt;/gi, '<')
      .replace(/&gt;/gi, '>')
      .replace(/&le;/gi, '≤')
      .replace(/&ge;/gi, '≥')
      .replace(/&ne;/gi, '≠');
  }
  return text;
}
function renderMathText(value) {
  let text = esc(normalizeMathSource(value)).trim();
  text = text
    .replace(/^\$\$?|\$\$?$/g, '')
    .replace(/^\\\(|\\\)$/g, '')
    .replace(/^\\\[|\\\]$/g, '');
  text = text
    .replace(/\\left/g, '')
    .replace(/\\right/g, '')
    .replace(/\\xrightarrow(?:\[([^\]]*)\])?\{([^}]*)\}/g, (_, below, above) => {
      const lower = below ? `<span class="math-arrow-label">${below}</span>` : '';
      const upper = above ? `<span class="math-arrow-label">${above}</span>` : '';
      return `<span class="math-arrow">${lower}<span>→</span>${upper}</span>`;
    })
    .replace(/\\frac\{([^{}]+)\}\{([^{}]+)\}/g, '<span class="math-frac"><sup>$1</sup>/<sub>$2</sub></span>')
    .replace(/\\operatorname\{([^{}]+)\}/g, '<span class="math-roman">$1</span>')
    .replace(/\\mathrm\{([^{}]+)\}/g, '<span class="math-roman">$1</span>')
    .replace(/\\text\{([^{}]+)\}/g, '<span class="math-text">$1</span>')
    .replace(/\\mathcal\s*\{?([A-Za-z])\}?/g, (_, ch) => {
      const cal = { H: 'ℋ', B: 'ℬ', C: '𝒞', F: 'ℱ', O: '𝒪' };
      return `<span class="math-cal">${cal[ch] || ch}</span>`;
    })
    .replace(/\\overline\s*\{([^{}]+)\}/g, '<span class="overline">$1</span>')
    .replace(/\\overline\s+([A-Za-z](?:_[A-Za-z0-9]+)?)/g, '<span class="overline">$1</span>');
  const commandMap = [
    [/\\forall/g, '∀'],
    [/\\exists/g, '∃'],
    [/\\infty/g, '∞'],
    [/\\varepsilon/g, 'ε'],
    [/\\epsilon/g, 'ε'],
    [/\\Delta/g, 'Δ'],
    [/\\Omega/g, 'Ω'],
    [/\\Theta/g, 'Θ'],
    [/\\lambda/g, 'λ'],
    [/\\mu/g, 'μ'],
    [/\\psi/g, 'ψ'],
    [/\\perp/g, '⊥'],
    [/\\subseteq/g, '⊆'],
    [/\\subset/g, '⊂'],
    [/\\in/g, '∈'],
    [/\\geq?/g, '≥'],
    [/\\leq?/g, '≤'],
    [/\\neq?/g, '≠'],
    [/\\Rightarrow/g, '⇒'],
    [/\\Longrightarrow/g, '⇒'],
    [/\\rightarrow/g, '→'],
    [/\\to/g, '→'],
    [/\\mapsto/g, '↦'],
    [/\\langle/g, '⟨'],
    [/\\rangle/g, '⟩'],
    [/\\cdots/g, '⋯'],
    [/\\dots/g, '…'],
    [/\\int/g, '∫'],
    [/\\sum/g, '∑'],
    [/\\sup/g, 'sup'],
    [/\\quad/g, ' '],
    [/\\qquad/g, ' '],
    [/\\,/g, ' '],
    [/\\\|/g, '‖'],
  ];
  for (const [pattern, replacement] of commandMap) text = text.replace(pattern, replacement);
  text = text
    .replace(/Omega/g, 'Ω')
    .replace(/Delta/g, 'Δ')
    .replace(/lambda/g, 'λ')
    .replace(/mu/g, 'μ')
    .replace(/infinity/g, '∞')
    .replace(/&gt;=/g, '≥')
    .replace(/&lt;=/g, '≤')
    .replace(/!=/g, '≠')
    .replace(/-&gt;/g, '→')
    .replace(/=&gt;/g, '⇒')
    .replace(/&lt;([^&<>]+)&gt;/g, '⟨$1⟩')
    .replace(/&lt;/g, '﹤')
    .replace(/&gt;/g, '﹥')
    .replace(/ subset /g, ' ⊆ ')
    .replace(/H_YM/g, 'H<sub>YM</sub>')
    .replace(/S_YM\^cont/g, 'S<sub>YM</sub><sup>cont</sup>')
    .replace(/P_perp/g, 'P<sub>⊥</sub>')
    .replace(/B_k/g, 'B<sub>k</sub>')
    .replace(/C_O/g, 'C<sub>O</sub>')
    .replace(/mu_O/g, 'μ<sub>O</sub>')
    .replace(/conjugate\(([^)]+)\)/g, '<span class="overline">$1</span>')
    .replace(/exp\(([^)]+)\)/g, 'e<sup>$1</sup>');
  text = renderScripts(text);
  return text
    .replace(/\\[ ;:!]/g, ' ')
    .replace(/\\\\/g, ' ')
    .replace(/\\/g, '')
    .replace(/\s{2,}/g, ' ');
}
function pill(text, cls='') { return `<span class="pill ${cls}">${esc(text)}</span>`; }
function metric(value, label) { return `<div class="metric"><strong>${esc(value)}</strong><span>${esc(label)}</span></div>`; }
function eventCard(ev) {
  const lane = ev.visual_encoding?.lane || 'reflection';
  const obligations = ev.proof_obligations || [];
  return `<article class="card" data-lane="${esc(lane)}">
    <div class="row">${pill(lane)}${pill(ev.epistemic_status)}${pill(ev.visual_encoding?.salience || 'medium', ev.visual_encoding?.salience === 'critical' ? 'fail' : '')}</div>
    <h3>${esc(ev.title)}</h3>
    <p>${esc(ev.narrative_summary)}</p>
    <p class="muted">${esc(ev.conceptual_move)}</p>
    <details><summary>Objects, obligations, evidence</summary>
      <h4>Mathematical Objects</h4>${list(ev.mathematical_objects)}
      <h4>Proof Obligations</h4>${list(obligations)}
      <h4>Evidence</h4>${list(ev.evidence_paths, 'code')}
      <p class="muted">${esc(ev.uncertainty)}</p>
    </details>
  </article>`;
}
function routeCard(route) {
  const score = Math.round((Number(route.target_relevance_score || 0)) * 100);
  const lane = route.route_disposition === 'proof_queue' ? 'candidate' : 'validation';
  const domainTerms = route.domain_specificity?.route_terms || [];
  const family = route.route_blueprint?.route_family || '';
  const derivationArtifacts = route.route_blueprint?.derivation_artifacts || [];
  return `<article class="card" data-lane="${lane}">
    <div class="row">${pill(`#${route.priority}`)}${pill(route.route_disposition)}${pill(`drift ${route.drift_risk}`, route.drift_risk === 'high' ? 'fail' : route.drift_risk === 'medium' ? 'warn' : '')}</div>
    <h3>${esc(family || route.creative_operation || route.candidate_id)}</h3>
    <p>${esc(route.proposed_transformation)}</p>
    ${route.source_witness ? `<p class="muted">${esc(route.source_witness)}</p>` : ''}
    <div class="meter" aria-label="target relevance"><span style="width:${score}%"></span></div>
    <p class="muted">Target relevance ${score}% · ${esc(route.routing_decision)} · ${esc(route.validation_packet_id)}</p>
    <div class="row">${(route.cited_commitment_ids || []).map(c => pill(c, 'target')).join('')}</div>
    <details><summary>Validation and evidence</summary>
      <h4>Domain Terms</h4>${list(domainTerms)}
      <h4>Gate Summary</h4><p class="code">${esc(JSON.stringify(route.gate_summary || {}))}</p>
      <h4>Hard Gates</h4><p class="code">${esc(JSON.stringify(route.hard_gates || {}))}</p>
      <h4>Obligations</h4>${list((route.obligations || []).map(o => `${o.status}: ${o.requirement}`))}
      <h4>Disconfirming Observations</h4>${list(route.disconfirming_observations)}
      ${derivationArtifacts.length ? `<h4>Derivation Artifacts</h4>${list(derivationArtifacts, 'code')}` : ''}
      <h4>Source Artifacts</h4>${list(route.source_artifacts, 'code')}
    </details>
  </article>`;
}
function frontierCard(item) {
  return `<article class="card" data-lane="dependency">
    <div class="row">${pill(item.kind)}${pill(item.status)}</div>
    <h3>${esc(item.node_id)}</h3>
    <p>${esc(item.label)}</p>
    <p class="muted">${esc(item.next_action)}</p>
    <details><summary>Evidence and parents</summary>${list(item.evidence_paths, 'code')}${list(item.parents, 'code')}</details>
  </article>`;
}
function obligationCard(ob) {
  return `<article class="card" data-lane="${ob.source === 'candidate_validation' ? 'validation' : 'dependency'}">
    <div class="row">${pill(ob.source)}${pill(ob.status || 'open')}</div>
    <h3>${esc(ob.gate || 'obligation')}</h3>
    <p>${esc(ob.requirement)}</p>
    ${ob.candidate_id ? `<p class="code">${esc(ob.candidate_id)}</p>` : ''}
  </article>`;
}
function evidenceCard(ev) {
  return `<article class="card" data-lane="drift">
    <div class="row">${pill(ev.exists ? 'present' : 'missing', ev.exists ? '' : 'fail')}${pill(ev.role)}</div>
    <p class="code">${esc(ev.path)}</p>
  </article>`;
}
function empiricalRequestCard(req) {
  return `<article class="card" data-lane="validation">
    <div class="row">${pill(req.evidence_mode || 'evidence')}${pill(req.proximity_class || 'proximity')}</div>
    <h3>${esc(req.observable_or_quantity)}</h3>
    <h4>Linked Theoretical Step</h4><p>${esc(req.linked_theoretical_step)}</p>
    <h4>Empirical Question</h4><p>${esc(req.empirical_question)}</p>
    ${listSection('Search Plan', req.search_plan)}
    ${listSection('Support Criteria', req.support_criteria)}
    ${listSection('Refutation Criteria', req.refutation_criteria)}
    <h4>Transfer Gap</h4><p>${esc(req.transfer_gap)}</p>
    <h4>Proof Boundary</h4><p>${esc(req.proof_boundary)}</p>
    <h4>Integration Action</h4><p>${esc(req.integration_action)}</p>
  </article>`;
}
function statusPill(status) {
  if (status === 'potential_breakthrough_signal') return pill(status, 'success');
  if (status === 'achieved') return pill(status, 'success');
  if (status === 'route_in_play_not_achieved') return pill(status, 'warn');
  return pill(status || 'unknown');
}
function milestoneCard(ms, compact=false) {
  const body = compact ? `
    <p>${esc(ms.why_big_deal)}</p>
    <p class="muted">${esc(ms.next_action)}</p>
  ` : `
    <p>${esc(ms.why_big_deal)}</p>
    <h4>Potentially Achieved When</h4><p>${esc(ms.potentially_achieved_when)}</p>
    <h4>Success Signal</h4><p>${esc(ms.success_signal)}</p>
    ${equationStack(ms.equations || [])}
    ${listSection('Certification Evidence', ms.certification_evidence)}
    ${listSection('Disqualifiers', ms.disqualifiers)}
    <h4>Next Action</h4><p>${esc(ms.next_action)}</p>
  `;
  return `<article class="card milestone-card" data-lane="milestone">
    <div class="row">${statusPill(ms.current_status)}${(ms.linked_commitments || []).slice(0, 4).map(c => pill(c, 'target')).join('')}</div>
    <h3>${esc(ms.label)}</h3>
    ${body}
  </article>`;
}
function reorientationModeCard(mode) {
  return `<article class="card reorientation-card" data-lane="conceptual">
    <div class="row">${pill(mode.mode || 'mode')}</div>
    <h3>${esc(mode.mode || 'Reorientation mode')}</h3>
    <h4>Deep Meaning</h4><p>${esc(mode.deep_meaning)}</p>
    <h4>Yang-Mills Use</h4><p>${esc(mode.yang_mills_use)}</p>
    <h4>Trigger</h4><p>${esc(mode.trigger)}</p>
    <h4>Allowed Action</h4><p>${esc(mode.allowed_action)}</p>
    <h4>Forbidden Shortcut</h4><p>${esc(mode.forbidden_shortcut)}</p>
  </article>`;
}
function decisionPointCard(point) {
  return `<article class="card reorientation-card" data-lane="validation">
    <div class="row">${pill('checkpoint')}</div>
    <h3>${esc(point.checkpoint)}</h3>
    <h4>If Progress</h4><p>${esc(point.if_progress)}</p>
    <h4>If Stalls</h4><p>${esc(point.if_stalls)}</p>
    <h4>Backtrack If</h4><p>${esc(point.backtrack_if)}</p>
    <h4>Pivot If</h4><p>${esc(point.pivot_if)}</p>
    <h4>Next Experiment</h4><p>${esc(point.next_experiment)}</p>
  </article>`;
}
function reorientationActionCard(action) {
  return `<article class="card reorientation-card" data-lane="milestone">
    <div class="row">${pill(action.mode || 'action')}${pill(action.priority || 'priority')}</div>
    <h3>${esc(action.action_id)}</h3>
    <p>${esc(action.action)}</p>
    <h4>Why Now</h4><p>${esc(action.why_now)}</p>
    <h4>Success Condition</h4><p>${esc(action.success_condition)}</p>
  </article>`;
}
function routeAssessmentCard(route) {
  return `<article class="card reorientation-card" data-lane="candidate">
    <div class="row">${pill(route.recommended_move || 'move')}${(route.protected_commitments || []).slice(0, 4).map(c => pill(c, 'target')).join('')}</div>
    <h3>${esc(route.candidate_id)}</h3>
    <p class="muted">${esc(route.route_family)}</p>
    <h4>Current Read</h4><p>${esc(route.current_read)}</p>
    <h4>Obstruction Type</h4><p>${esc(route.obstruction_type)}</p>
    <h4>Backtrack Trigger</h4><p>${esc(route.backtrack_trigger)}</p>
    <h4>Pivot Trigger</h4><p>${esc(route.pivot_trigger)}</p>
    <h4>Next Probe</h4><p>${esc(route.next_probe)}</p>
  </article>`;
}
function pivotWatchCard(route) {
  return `<article class="card reorientation-card" data-lane="validation">
    <div class="row">${pill('pivot watch')}</div>
    <h3>${esc(route.candidate_id)}</h3>
    <p class="muted">${esc(route.route_family)}</p>
    <h4>Why Not Proof Queue Now</h4><p>${esc(route.why_not_proof_queue_now)}</p>
    <h4>Promotion Condition</h4><p>${esc(route.promotion_condition)}</p>
  </article>`;
}
function subgoalControlCard(control) {
  return `<article class="card reorientation-card" data-lane="reflection">
    <div class="row">${pill(control.decision || 'decision')}${pill(`${control.repeated_blocker_count ?? 0} repeated blockers`, Number(control.repeated_blocker_count || 0) > 1 ? 'warn' : '')}</div>
    <h3>${esc(control.target_object_link)}</h3>
    <h4>Learning From Failure</h4><p>${esc(control.learning_from_failure)}</p>
    <h4>Next Action</h4><p>${esc(control.next_action)}</p>
    <h4>Backtrack Trigger</h4><p>${esc(control.backtrack_trigger)}</p>
    <h4>Pivot Trigger</h4><p>${esc(control.pivot_trigger)}</p>
    <h4>Quarantine Trigger</h4><p>${esc(control.quarantine_trigger)}</p>
    <h4>Stop Condition</h4><p>${esc(control.stop_condition)}</p>
    ${listSection('Essential Commitments Preserved', control.essential_commitments_preserved)}
    ${listSection('Adaptation History', control.adaptation_history)}
  </article>`;
}
function machineryCard(item) {
  return `<article class="card reorientation-card" data-lane="candidate">
    <div class="row">${pill(item.machinery_role || 'role')}${pill(item.current_bottleneck || 'bottleneck')}</div>
    <h3>${esc(item.selected_machinery)}</h3>
    <h4>Controlled Interface</h4><p>${esc(item.controlled_interface)}</p>
    <h4>Why Best Available</h4><p>${esc(item.why_best_available)}</p>
    <h4>Bridge Obligation</h4><p>${esc(item.required_bridge_obligation)}</p>
    <h4>Target Object Link</h4><p>${esc(item.target_object_link)}</p>
    <h4>Yang-Mills Example Alignment</h4><p>${esc(item.example_alignment)}</p>
    ${listSection('Assumptions Required', item.assumptions_required)}
    ${listSection('Invalid Use Modes', item.invalid_use_modes)}
    <h4>Validation Handoff</h4><p class="code">${esc(item.validation_handoff)}</p>
  </article>`;
}
function stretchProgramCard(item) {
  return `<article class="card reorientation-card" data-lane="conceptual">
    <div class="row">${pill(item.machinery_role || 'role')}${pill(item.status || 'status')}</div>
    <h3>${esc(item.title)}</h3>
    <h4>Controlled Interface</h4><p>${esc(item.controlled_interface)}</p>
    <h4>Hypothesis</h4><p>${esc(item.hypothesis)}</p>
    <h4>Mathematical Mechanism</h4><p>${esc(item.mathematical_mechanism)}</p>
    ${equationStack(item.equations || [])}
    ${listSection('Dependencies', item.dependencies)}
    ${listSection('Falsifiers', item.falsifiers)}
    ${listSection('Next Experiments', item.next_experiments)}
    <h4>Expected Learning</h4><p>${esc(item.expected_learning)}</p>
    <h4>Promotion Signal</h4><p>${esc(item.promotion_signal)}</p>
    <h4>Pivot Signal</h4><p>${esc(item.pivot_signal)}</p>
  </article>`;
}
function chainEdgeCard(edge) {
  return `<article class="card reorientation-card" data-lane="validation">
    <div class="row">${pill(edge.from || 'from')}${pill(edge.to || 'to')}</div>
    <h3>${esc(edge.bridge_obligation)}</h3>
    ${listSection('Assumptions', edge.assumptions)}
    <h4>Output</h4><p>${esc(edge.output)}</p>
    <h4>Failure Mode</h4><p>${esc(edge.failure_mode)}</p>
    <h4>Validator Handoff</h4><p class="code">${esc(edge.validator_handoff)}</p>
  </article>`;
}
function matchesText(blob) {
  const q = state.q.trim().toLowerCase();
  return !q || JSON.stringify(blob).toLowerCase().includes(q);
}
function matchesEvent(ev) {
  if (state.lane !== 'all' && ev.visual_encoding?.lane !== state.lane) return false;
  if (state.status !== 'all' && ev.epistemic_status !== state.status) return false;
  if (state.commitment !== 'all' && !(ev.target_commitments || []).includes(state.commitment)) return false;
  if (state.evidence !== 'all' && !(ev.evidence_paths || []).some(p => p.includes(state.evidence))) return false;
  return matchesText(ev);
}
function matchesRoute(route) {
  if (state.status !== 'all' && route.epistemic_status !== state.status && route.route_disposition !== state.status) return false;
  if (state.commitment !== 'all' && !(route.cited_commitment_ids || []).includes(state.commitment)) return false;
  if (state.evidence !== 'all' && !(route.source_artifacts || []).some(p => p.includes(state.evidence))) return false;
  return matchesText(route);
}
function renderOverview() {
  const spine = DATA.target_spine;
  const commitments = (spine.commitments || []).map(c => `<div class="commitment"><strong>${esc(c.id)}</strong><span class="muted">${esc(c.label || c.validation_question)}</span></div>`).join('');
  const topRoutes = DATA.candidate_routes.slice(0, 4).filter(matchesRoute).map(routeCard).join('');
  const milestones = (DATA.success_milestones?.items || []).slice(0, 3).map(ms => milestoneCard(ms, true)).join('');
  return `<div class="grid">
    <section class="panel"><h2>Target Spine</h2><div class="commitments">${commitments}</div></section>
    <section class="panel"><h2>Current Pressure</h2>
      ${metric(DATA.frontier.total, 'open frontier nodes')}
      ${metric(DATA.candidate_routes.length, 'candidate routes')}
      ${metric(DATA.proof_obligations.total, 'tracked proof obligations')}
      ${metric(DATA.stale_workflow.critical_findings, 'stale active findings')}
    </section>
    <section class="panel"><h2>Success Milestones</h2><p class="muted">${esc(DATA.success_milestones?.purpose || '')}</p><div class="milestone-grid">${milestones}</div></section>
    <section class="panel"><h2>Top Route Candidates</h2>${topRoutes || '<div class="empty">No routes match the current filters.</div>'}</section>
    <section class="panel"><h2>Reasoning Timeline</h2><div class="timeline">${DATA.reasoning_events.events.filter(matchesEvent).map(eventCard).join('') || '<div class="empty">No events match the current filters.</div>'}</div></section>
  </div>`;
}
function renderTimeline() {
  return `<section class="panel"><h2>Timeline</h2><div class="timeline">${DATA.reasoning_events.events.filter(matchesEvent).map(eventCard).join('') || '<div class="empty">No events match the current filters.</div>'}</div></section>`;
}
function renderFrontier() {
  const rows = DATA.frontier.items.filter(matchesText).map(frontierCard).join('');
  return `<section class="panel"><h2>Dependency Frontier</h2><p class="muted">${DATA.frontier.total} open nodes over ${DATA.frontier.node_count} total nodes.</p>${rows || '<div class="empty">No frontier nodes match the current filters.</div>'}</section>`;
}
function renderCandidates() {
  const rows = DATA.candidate_routes.filter(matchesRoute).map(routeCard).join('');
  return `<section class="panel"><h2>Candidate Routes</h2>${rows || '<div class="empty">No candidates match the current filters.</div>'}</section>`;
}
function storyBeatCard(beat, index) {
  return `<article class="card story-beat" data-lane="reflection">
    <div class="row">${pill(`move ${index}`)}${pill(beat.phase || 'strategy')}</div>
    <h3>${esc(beat.headline)}</h3>
    <h4>Tried</h4><p>${esc(beat.tried)}</p>
    <h4>Underlying mathematics and Physics mechanism</h4>
    <p>${esc(beat.physics_story)}</p>
    ${equationStack(beat.equations || [])}
    ${listSection('Why it did not pay off', beat.why_it_did_not_pay_off)}
    ${listSection('What paid off', beat.what_paid_off)}
    ${listSection('What we learned', beat.what_we_learned)}
    ${listSection('Remaining blockers', beat.remaining_blockers)}
    ${listSection('Why this is the next goal', beat.why_this_is_the_next_goal)}
    ${listSection('Next recursive questions', beat.next_recursive_questions)}
    <h4>Decision</h4><p>${esc(beat.decision)}</p>
    <h4>Moved to</h4><p>${esc(beat.moved_to)}</p>
    ${beat.supporting_artifacts?.length ? `<details><summary>Supporting artifacts</summary>${list(beat.supporting_artifacts, 'code')}</details>` : ''}
  </article>`;
}
function contradictionCard(route) {
  return `<article class="card story-beat" data-lane="reflection">
    <div class="row">${pill(route.computed_verdict || 'unvalidated', route.computed_verdict === 'promote' ? 'success' : 'warn')}${pill(route.audit_skill || 'auditor')}${pill(`${route.finding_count || 0} findings`)}</div>
    <h3>${esc(route.strategy)}</h3>
    <p class="muted">${esc(route.route_family)}</p>
    <h4>Exact negation</h4><p>${esc(route.exact_negation)}</p>
    <h4>Contradiction carrier</h4><p>${esc(route.contradiction_carrier)}</p>
    ${equationStack(route.equation_checkpoints || [])}
    <h4>Derived consequence</h4><p>${esc(route.derived_consequence)}</p>
    <h4>Conflict target</h4><p>${esc(route.conflict_target)}</p>
    ${listSection('Preserved commitments', route.preserved_commitments)}
    ${listSection('Proof obligations', route.proof_obligations)}
    ${listSection('Failure modes', route.failure_modes)}
    <h4>What failure would teach</h4><p>${esc(route.learning_if_failed)}</p>
    <h4>Audit learning</h4><p>${esc(route.mathematical_learning)}</p>
    <h4>Same-theory invariant</h4><p>${esc(route.same_theory_invariant)}</p>
  </article>`;
}
function renderStrategy() {
  const story = DATA.interpretative_strategy_story || {};
  const beats = story.story_beats || [];
  const contradiction = DATA.contradiction_routes || {};
  const contradictionCards = (contradiction.items || []).map(contradictionCard).join('');
  return `<section class="panel">
    <h2>${esc(story.title || 'Physics Strategy Story')}</h2>
    <p class="story-intro">${esc(story.current_thesis || '')}</p>
    <p class="muted">${esc(story.mode || '')}</p>
    <h3>What Counts As A Physics Explanation</h3>
    ${list(story.physics_explanation_contract || [])}
    <div class="timeline">${beats.map((beat, idx) => storyBeatCard(beat, idx + 1)).join('') || '<div class="empty">No strategy story beats are available.</div>'}</div>
    <h3>Proof By Contradiction Branches</h3>
    <p class="story-intro">${esc(contradiction.generative_review?.summary || '')}</p>
    <div class="control-columns">${contradictionCards || '<div class="empty">No contradiction branches are available.</div>'}</div>
    <h3>Anti-Drift Rules</h3>${list(story.anti_drift_rules)}
  </section>`;
}
function renderMilestones() {
  const milestones = DATA.success_milestones || {};
  const rows = (milestones.items || []).filter(matchesText).map(ms => milestoneCard(ms)).join('');
  return `<section class="panel">
    <h2>${esc(milestones.title || 'Success Milestones')}</h2>
    <p class="story-intro">${esc(milestones.purpose || '')}</p>
    <h3>Promotion Policy</h3>${list(milestones.promotion_policy)}
    <div class="milestone-grid">${rows || '<div class="empty">No milestones match the current filters.</div>'}</div>
  </section>`;
}
function renderReorientation() {
  const control = DATA.reorientation_control || {};
  const modes = (control.reorientation_modes || []).map(reorientationModeCard).join('');
  const points = (control.decision_points || []).map(decisionPointCard).join('');
  const actions = (control.active_reorientation_queue || []).map(reorientationActionCard).join('');
  const routeAssessments = (control.route_assessments || []).map(routeAssessmentCard).join('');
  const pivotWatch = (control.pivot_watchlist || []).map(pivotWatchCard).join('');
  const metrics = control.loop_metrics || {};
  const contract = control.bounded_reflection_contract || {};
  const recommendation = control.current_recommendation || {};
  return `<section class="panel">
    <h2>${esc(control.title || 'Reorientation Control')}</h2>
    <p class="story-intro">${esc(control.purpose || '')}</p>
    <h3>Current Diagnosis</h3><p>${esc(control.current_diagnosis || '')}</p>
    <h3>Current Recommendation</h3><p>${esc(recommendation.decision || '')}</p>
    ${list([
      recommendation.rationale,
      recommendation.backtrack_guard,
      recommendation.pivot_guard,
      recommendation.quarantine_guard,
      recommendation.formal_subgoal_guard
    ].filter(Boolean))}
    <div class="status-stack">
      ${metric(metrics.active_proof_routes || 0, 'active proof routes')}
      ${metric(metrics.discovery_routes || 0, 'discovery routes')}
      ${metric(metrics.blocked_or_bridge_frontier || 0, 'blocked or bridge frontier')}
    </div>
    <h3>Bounded Reflection Contract</h3>
    <p>Max reflection passes before action: ${esc(contract.max_reflection_passes_before_action || '')}</p>
    ${listSection('Required Output Per Pass', contract.required_output_per_pass)}
    ${listSection('Stop Reflecting When', contract.stop_reflecting_when)}
    <p class="muted">${esc(contract.resume_search_when || '')}</p>
    <h3>Route-Level Diagnosis</h3><div class="control-columns">${routeAssessments || '<div class="empty">No route-level assessments available.</div>'}</div>
    <h3>Control Policy</h3>${list(control.control_policy)}
    <h3>Reorientation Modes</h3><div class="control-columns">${modes || '<div class="empty">No modes available.</div>'}</div>
    <h3>Decision Checkpoints</h3><div class="control-columns">${points || '<div class="empty">No decision checkpoints available.</div>'}</div>
    <h3>Pivot Watchlist</h3><div class="control-columns">${pivotWatch || '<div class="empty">No pivot watchlist entries available.</div>'}</div>
    <h3>Active Reorientation Queue</h3><div class="control-columns">${actions || '<div class="empty">No reorientation actions available.</div>'}</div>
  </section>`;
}
function renderSubgoals() {
  const policy = DATA.formal_subgoal_control_policy || {};
  const summary = DATA.reorientation_control?.formal_subgoal_control_summary || {};
  const counts = summary.decision_counts || {};
  const controls = DATA.candidate_routes.map(route => route.subgoal_control).filter(Boolean).filter(matchesText);
  const decisionLabels = [
    ['persist_adapt', 'Persist Or Adapt'],
    ['backtrack', 'Backtrack'],
    ['pivot', 'Pivot'],
    ['quarantine', 'Quarantine'],
    ['stop', 'Stop']
  ];
  return `<section class="panel">
    <h2>Formal Subgoal Control</h2>
    <p class="story-intro">${esc(policy.purpose || '')}</p>
    <div class="status-stack">
      ${metric(summary.active_control_count || controls.length, 'active controls')}
      ${metric(counts.persist_adapt || 0, 'persist/adapt')}
      ${metric((summary.stale_repeated_blockers || []).length, 'stale blockers')}
      ${metric(DATA.candidate_routes.length, 'candidate routes')}
    </div>
    <h3>Universal Decision Criteria</h3>
    <div class="control-columns">
      ${decisionLabels.map(([key, label]) => `<article class="card reorientation-card" data-lane="reflection"><div class="row">${pill(key)}</div><h3>${label}</h3><p>${esc(policy.decision_criteria?.[key] || '')}</p></article>`).join('')}
    </div>
    <h3>Universal Invariants</h3>${list(policy.universal_invariants || [])}
    <h3>Live Route Decisions</h3>
    <div class="control-columns">${controls.map(subgoalControlCard).join('') || '<div class="empty">No subgoal-control decisions match the current filters.</div>'}</div>
  </section>`;
}
function renderMachinery() {
  const machinery = DATA.machinery_selection || {};
  const roles = machinery.policy?.roles || {};
  const summary = machinery.summary || {};
  const chain = machinery.abstraction_chain || {};
  const roleCards = Object.entries(roles).map(([role, description]) => `<article class="card reorientation-card" data-lane="reflection"><div class="row">${pill(role)}</div><p>${esc(description)}</p></article>`).join('');
  const items = (machinery.items || []).filter(matchesText).map(machineryCard).join('');
  const edges = (chain.bridge_obligations || []).map(chainEdgeCard).join('');
  return `<section class="panel">
    <h2>${esc(machinery.title || 'Machinery Selection')}</h2>
    <p class="story-intro">${esc(machinery.purpose || '')}</p>
    <div class="status-stack">
      ${metric(summary.selection_count || 0, 'machinery selections')}
      ${metric((summary.missing_core_roles || []).length, 'missing core roles')}
      ${metric(Object.keys(summary.role_counts || {}).length, 'universal roles')}
      ${metric((chain.bridge_obligations || []).length, 'abstraction-chain arrows')}
    </div>
    <h3>Universal Machinery Roles</h3>
    <div class="control-columns">${roleCards}</div>
    <h3>Active Route Machinery</h3>
    <div class="control-columns">${items || '<div class="empty">No machinery selections match the current filters.</div>'}</div>
    <h3>Abstraction Chain</h3>
    <p class="story-intro">${esc(chain.interpretation || '')}</p>
    <div class="control-columns">${edges || '<div class="empty">No abstraction-chain arrows available.</div>'}</div>
  </section>`;
}
function renderStretch() {
  const stretch = DATA.discovery_stretch || {};
  const programs = (stretch.programs || []).filter(matchesText).map(stretchProgramCard).join('');
  const queue = (stretch.next_run_queue || []).map(item => `<article class="card reorientation-card" data-lane="milestone"><div class="row">${pill(item.queue_id || 'queue')}</div><p>${esc(item.action)}</p><h4>Why First</h4><p>${esc(item.why_first)}</p></article>`).join('');
  return `<section class="panel">
    <h2>${esc(stretch.title || 'Large-Stretch Discovery Exploration')}</h2>
    <p class="story-intro">${esc(stretch.purpose || '')}</p>
    <p>${esc(stretch.stretch_thesis || '')}</p>
    <div class="status-stack">
      ${metric(stretch.quality_gate || 'unknown', 'quality gate')}
      ${metric((stretch.programs || []).length, 'programs')}
      ${metric(Object.keys(stretch.role_counts || {}).length, 'roles')}
      ${metric((stretch.next_run_queue || []).length, 'next actions')}
    </div>
    <h3>Discovery Programs</h3>
    <div class="control-columns">${programs || '<div class="empty">No stretch programs match the current filters.</div>'}</div>
    <h3>Next Run Queue</h3>
    <div class="control-columns">${queue || '<div class="empty">No queued stretch actions available.</div>'}</div>
  </section>`;
}
function marathonBranchCard(item) {
  return `<article class="card reorientation-card" data-lane="reflection">
    <div class="row">${pill(item.status || 'status')}${pill(`priority ${item.priority ?? ''}`)}</div>
    <h3>${esc(item.title)}</h3>
    <h4>Controlled Interface</h4><p>${esc(item.controlled_interface)}</p>
    <h4>Latest Learning</h4><p>${esc(item.latest_learning)}</p>
    <h4>Control Decision</h4><p class="code">${esc(JSON.stringify(item.latest_control_decision || {}))}</p>
    <h4>Next Experiment</h4><p>${esc(item.next_experiment)}</p>
  </article>`;
}
function marathonCycleCard(item) {
  return `<article class="card reorientation-card" data-lane="candidate">
    <div class="row">${pill(item.cycle_id || 'cycle')}${(item.selected_branch_ids || []).slice(0, 3).map(x => pill(x)).join('')}</div>
    <p>${esc(item.cycle_learning)}</p>
    ${listSection('Next Cycle Queue', item.next_cycle_queue)}
  </article>`;
}
function renderMarathon() {
  const marathon = DATA.discovery_marathon || {};
  const branches = (marathon.branch_summaries || []).filter(matchesText).map(marathonBranchCard).join('');
  const cycles = (marathon.cycle_summaries || []).filter(matchesText).map(marathonCycleCard).join('');
  const reviews = (marathon.deep_reviews || []).map(review => `<article class="card reorientation-card" data-lane="validation"><div class="row">${pill(review.review_id || 'review')}${pill(review.recommendation || 'recommendation')}</div><p>${esc(review.summary)}</p></article>`).join('');
  return `<section class="panel">
    <h2>${esc(marathon.title || 'Discovery Marathon')}</h2>
    <p class="story-intro">${esc(marathon.purpose || '')}</p>
    <div class="status-stack">
      ${metric(marathon.status || 'unknown', 'run status')}
      ${metric(marathon.cycle_count || 0, 'persisted packets')}
      ${metric(marathon.research_cycle_count || 0, 'research cycles')}
      ${metric(marathon.synthetic_cycle_count || 0, 'synthetic packets')}
      ${metric((marathon.branch_summaries || []).length, 'branches')}
      ${metric(marathon.breakthrough_status || 'none', 'breakthrough status')}
    </div>
    <h3>What Actually Changed</h3>${list(marathon.what_actually_changed || [])}
    <h3>Branch Learning</h3><div class="control-columns">${branches || '<div class="empty">No marathon branches match the current filters.</div>'}</div>
    <h3>Cycle Learning</h3><div class="control-columns">${cycles || '<div class="empty">No marathon cycles match the current filters.</div>'}</div>
    <h3>Deep Reviews</h3><div class="control-columns">${reviews || '<div class="empty">No deep reviews recorded yet.</div>'}</div>
  </section>`;
}
function renderDebt() {
  const rows = DATA.proof_obligations.items.filter(matchesText).slice(0, 120).map(obligationCard).join('');
  return `<section class="panel"><h2>Proof Debt</h2><p class="muted">${DATA.proof_obligations.total} obligations are tracked. Visual progress is not proof completion.</p>${rows || '<div class="empty">No obligations match the current filters.</div>'}</section>`;
}
function renderEvidence() {
  const rows = DATA.evidence_ledger.items.filter(matchesText).map(evidenceCard).join('');
  const empirical = DATA.empirical_evidence_requests || {};
  const empiricalRows = (empirical.items || []).filter(matchesText).map(empiricalRequestCard).join('');
  return `<section class="panel">
    <h2>Closely Related Empirical Evidence</h2>
    <p class="story-intro">${esc(empirical.purpose || '')}</p>
    <div class="control-columns">${empiricalRows || '<div class="empty">No empirical evidence requests match the current filters.</div>'}</div>
    <h2>Evidence Ledger</h2><p class="muted">${DATA.evidence_ledger.total} artifacts, ${DATA.evidence_ledger.missing.length} missing.</p>
    ${rows || '<div class="empty">No evidence paths match the current filters.</div>'}
  </section>`;
}
function graphNodeCard(node) {
  return `<article class="card" data-lane="conceptual">
    <div class="row">${pill(node.node_type || 'node')}${pill(node.epistemic_status || 'status')}</div>
    <h3>${esc(node.label || node.id)}</h3>
    <p>${esc(node.description || '')}</p>
    <p class="code">${esc(node.id || '')}</p>
  </article>`;
}
function graphEdgeCard(edge) {
  return `<article class="card" data-lane="candidate">
    <div class="row">${pill(edge.edge_type || 'edge')}${pill(edge.epistemic_status || 'status')}${pill(edge.sign || 'sign')}</div>
    <h3>${esc(edge.source)} -> ${esc(edge.target)}</h3>
    <p><strong>Direction:</strong> ${esc(edge.direction || '')}</p>
    <p><strong>Regime:</strong> ${(edge.validity_regime || []).map(x => `<span class="pill">${esc(x)}</span>`).join('')}</p>
    <details><summary>Assumptions and failure modes</summary>
      <h3>Assumptions</h3>${list(edge.assumptions || [])}
      <h3>Failure Modes</h3>${list(edge.failure_modes || [])}
      <h3>Evidence</h3>${list(edge.evidence_paths || [])}
    </details>
  </article>`;
}
function renderQualitative() {
  const graph = DATA.qualitative_mechanistic_graph || {};
  const nodes = (graph.nodes || []).filter(matchesText).map(graphNodeCard).join('');
  const edges = (graph.edges || []).filter(matchesText).map(graphEdgeCard).join('');
  return `<section class="panel"><h2>Qualitative Mechanistic Graph</h2>
    <p class="muted">${esc(graph.purpose || '')}</p>
    <div class="status-stack">
      ${metric(graph.summary?.node_count || 0, 'qualitative nodes')}
      ${metric(graph.summary?.edge_count || 0, 'relation edges')}
      ${metric(Object.keys(graph.summary?.status_counts || {}).length, 'status types')}
      ${metric((graph.updates || []).length, 'graph updates')}
    </div>
    <h3>Relation Edges</h3><div class="control-columns">${edges || '<div class="empty">No qualitative relation edges match the current filters.</div>'}</div>
    <h3>Variables, Regimes, Mechanisms</h3><div class="control-columns">${nodes || '<div class="empty">No qualitative graph nodes match the current filters.</div>'}</div>
  </section>`;
}
function renderDrift() {
  const checks = (DATA.stale_workflow.active_checks || []).map(x => `<li><span class="code">${esc(x.path)}</span>: ${esc(x.status)}</li>`).join('');
  const findings = (DATA.stale_workflow.findings || []).map(x => `<li>${esc(x.severity)} ${esc(x.path)}: ${esc(x.message)}</li>`).join('');
  return `<section class="panel"><h2>Drift Guard</h2>
    <p>${esc(DATA.stale_workflow.historical_artifact_count)} historical artifacts are isolated from the active state.</p>
    <p>${pill(`${DATA.stale_workflow.critical_findings} critical active findings`, DATA.stale_workflow.critical_findings ? 'fail' : '')}</p>
    <h3>Active Checks</h3><ul>${checks}</ul>
    <h3>Findings</h3>${findings ? `<ul>${findings}</ul>` : '<p class="muted">None.</p>'}
  </section>`;
}
function render() {
  const map = { overview: renderOverview, timeline: renderTimeline, frontier: renderFrontier, candidates: renderCandidates, strategy: renderStrategy, milestones: renderMilestones, reorientation: renderReorientation, subgoals: renderSubgoals, machinery: renderMachinery, stretch: renderStretch, marathon: renderMarathon, qualitative: renderQualitative, debt: renderDebt, evidence: renderEvidence, drift: renderDrift };
  $('view').innerHTML = map[state.tab]();
  document.querySelectorAll('.tab').forEach(btn => btn.classList.toggle('active', btn.dataset.tab === state.tab));
}
function fillFilters() {
  const lanes = [...new Set(DATA.reasoning_events.events.map(e => e.visual_encoding?.lane).filter(Boolean))].sort();
  const statuses = [...new Set(DATA.reasoning_events.events.map(e => e.epistemic_status).concat(DATA.candidate_routes.map(r => r.route_disposition)).filter(Boolean))].sort();
  const commitments = DATA.target_spine.commitment_ids || [];
  const evidence = [...new Set(DATA.evidence_ledger.items.map(e => e.path.split('/').slice(0,2).join('/')))].sort();
  const fill = (id, values) => { $(id).innerHTML = '<option value="all">All</option>' + values.map(v => `<option value="${esc(v)}">${esc(v)}</option>`).join(''); };
  fill('laneFilter', lanes);
  fill('statusFilter', statuses);
  fill('commitmentFilter', commitments);
  fill('evidenceFilter', evidence);
}
document.addEventListener('DOMContentLoaded', () => {
  $('targetId').textContent = DATA.target.target_id;
  $('goal').textContent = DATA.target.raw_goal;
  $('metrics').innerHTML = [
    metric(DATA.target_spine.commitment_ids.length, 'commitments'),
    metric(DATA.frontier.total, 'frontier'),
    metric(DATA.candidate_routes.length, 'routes'),
    metric(DATA.reorientation_control?.active_reorientation_queue?.length || 0, 'reorient')
  ].join('');
  fillFilters();
  document.querySelectorAll('.tab').forEach(btn => btn.addEventListener('click', () => { state.tab = btn.dataset.tab; render(); }));
  ['laneFilter','statusFilter','commitmentFilter','evidenceFilter'].forEach(id => $(id).addEventListener('change', e => { state[id.replace('Filter','')] = e.target.value; render(); }));
  $('query').addEventListener('input', e => { state.q = e.target.value; render(); });
  render();
});
"""


def render_html(packet: dict) -> str:
    data = html.escape(json.dumps(packet, sort_keys=True, ensure_ascii=False), quote=False)
    target_id = html.escape(packet["target"]["target_id"])
    generated = html.escape(packet["generated_utc"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Yang-Mills Reasoning Monitor</title>
  <style>{CSS}</style>
</head>
<body>
  <script id="monitor-data" type="application/json">{data}</script>
  <main class="shell">
    <header class="topbar">
      <div class="title-block">
        <p class="eyebrow">Abducer Reasoning Monitor · generated {generated}</p>
        <h1 id="targetId">{target_id}</h1>
        <p class="goal" id="goal"></p>
      </div>
      <div class="status-stack" id="metrics" aria-label="reasoning metrics"></div>
    </header>
    <section class="controls" aria-label="monitor filters">
      <input id="query" class="search" type="search" placeholder="Filter reasoning, obligations, evidence">
      <select id="laneFilter" class="select" aria-label="lane filter"></select>
      <select id="statusFilter" class="select" aria-label="status filter"></select>
      <select id="commitmentFilter" class="select" aria-label="commitment filter"></select>
      <select id="evidenceFilter" class="select" aria-label="evidence filter"></select>
    </section>
    <nav class="tabs" aria-label="monitor sections">
      <button class="tab active" data-tab="overview">Overview</button>
      <button class="tab" data-tab="timeline">Timeline</button>
      <button class="tab" data-tab="frontier">Frontier</button>
      <button class="tab" data-tab="candidates">Candidates</button>
      <button class="tab" data-tab="strategy">Strategy Story</button>
      <button class="tab" data-tab="milestones">Milestones</button>
      <button class="tab" data-tab="reorientation">Reorientation</button>
      <button class="tab" data-tab="subgoals">Subgoals</button>
      <button class="tab" data-tab="machinery">Machinery</button>
      <button class="tab" data-tab="stretch">Discovery Stretch</button>
      <button class="tab" data-tab="marathon">Marathon</button>
      <button class="tab" data-tab="qualitative">Qualitative Mechanism</button>
      <button class="tab" data-tab="debt">Proof Debt</button>
      <button class="tab" data-tab="evidence">Evidence</button>
      <button class="tab" data-tab="drift">Drift</button>
    </nav>
    <section id="view" class="content" aria-live="polite"></section>
  </main>
  <script>{JS}</script>
</body>
</html>
"""


def main() -> int:
    packet = load_json_object(PACKET)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render_html(packet), encoding="utf-8")
    print(f"Wrote {rel(OUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
