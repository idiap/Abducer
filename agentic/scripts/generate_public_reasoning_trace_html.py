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
"""Render a self-contained, workflow-neutral expert reasoning trace."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


CSS = r"""
:root{color-scheme:dark;--bg:#090d12;--panel:#111923;--panel2:#17222e;--line:#2a3948;--text:#edf4f8;--muted:#aab8c4;--accent:#70b7ff;--warn:#ffbd66;--bad:#ff6b7a;--good:#62d391}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}button,input,select{font:inherit}.top{padding:22px clamp(16px,4vw,48px);border-bottom:1px solid var(--line);background:#0b1118}.eyebrow{color:var(--accent);text-transform:uppercase;letter-spacing:.1em;font-size:12px}.top h1{margin:5px 0;font-size:clamp(24px,4vw,40px)}.focus{max-width:1000px;color:var(--muted)}.identity,.metrics{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}.pill,.metric{border:1px solid var(--line);background:var(--panel);padding:6px 9px;border-radius:7px}.metric strong{display:block;font-size:19px}.metric span,.meta{color:var(--muted);font-size:12px}.controls{position:sticky;top:0;z-index:3;padding:10px clamp(16px,4vw,48px);background:#0d141c;border-bottom:1px solid var(--line);display:grid;grid-template-columns:minmax(180px,1fr) auto;gap:10px}.controls input{background:var(--panel);color:var(--text);border:1px solid var(--line);border-radius:6px;padding:9px}.tabs{display:flex;overflow:auto;gap:6px}.tab{white-space:nowrap;background:var(--panel);color:var(--muted);border:1px solid var(--line);padding:8px 10px;border-radius:6px;cursor:pointer}.tab[aria-selected=true]{color:var(--text);border-color:var(--accent)}main{padding:18px clamp(16px,4vw,48px) 50px}.view{display:none}.view.active{display:block}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(330px,100%),1fr));gap:12px}.card{background:var(--panel);border:1px solid var(--line);border-radius:9px;padding:13px;margin-bottom:10px;overflow-wrap:anywhere}.card h2,.card h3{margin:0 0 8px}.status{display:inline-block;border-left:3px solid var(--accent);padding-left:7px}.gap{border-color:var(--warn)}.failure{border-color:var(--bad)}.good{border-color:var(--good)}dl{display:grid;grid-template-columns:minmax(100px,160px) 1fr;gap:5px 10px;margin:8px 0}dt{color:var(--muted)}dd{margin:0}.route{display:flex;gap:8px;overflow:auto;padding-bottom:8px}.step{min-width:190px}.arrow{align-self:center;color:var(--muted)}pre{white-space:pre-wrap;background:#0a1017;border:1px solid var(--line);padding:10px;border-radius:6px}.edge{font-family:ui-monospace,monospace;font-size:12px}.empty{color:var(--muted);font-style:italic}.notice{border-left:4px solid var(--warn)}@media(max-width:700px){.controls{position:static;grid-template-columns:1fr}.tabs{width:100%}dl{grid-template-columns:1fr}.top{padding-top:16px}}
"""


JS = r"""
const packet=JSON.parse(document.getElementById('trace-data').textContent);
const MAX_VISIBLE_CARDS=2000;
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const text=v=>typeof v==='string'?v:JSON.stringify(v??'',null,2);
const meta=o=>Object.entries(o||{}).filter(([,v])=>v!==''&&v!=null&&(typeof v!=='object'||Object.keys(v).length)).map(([k,v])=>`<dt>${esc(k.replaceAll('_',' '))}</dt><dd>${esc(text(v))}</dd>`).join('');
const card=(title,body,klass='')=>`<article class="card ${klass}" data-search="${esc((title+' '+text(body)).toLowerCase())}"><h3>${esc(title)}</h3>${body}</article>`;
const empty=label=>`<p class="empty">No ${esc(label)} recorded. This lane is explicit and has not been omitted.</p>`;
function bounded(rows){return rows.length>MAX_VISIBLE_CARDS?rows.slice(0,MAX_VISIBLE_CARDS):rows;}
function truncation(rows){return rows.length>MAX_VISIBLE_CARDS?`<p class="notice card">Showing ${MAX_VISIBLE_CARDS} of ${rows.length} cards. The complete validated packet remains embedded in this file.</p>`:'';}
function list(id,rows,title,render){document.getElementById(id).innerHTML=rows.length?bounded(rows).map((r,i)=>card(title(r,i),render(r,i),r.kind==='failure'?'failure':'')).join('')+truncation(rows):empty(id.replaceAll('-',' '));}
document.documentElement.style.setProperty('--accent',packet.lens.accent||'#70b7ff');
document.getElementById('title').textContent=packet.lens.visible_name;
document.getElementById('focus').textContent=packet.lens.focus_question;
document.getElementById('identity').innerHTML=Object.entries(packet.identity).filter(([,v])=>v).map(([k,v])=>`<span class="pill"><b>${esc(k.replaceAll('_',' '))}</b> ${esc(v)}</span>`).join('');
const c=packet.coverage; document.getElementById('metrics').innerHTML=[['Control coverage',Math.round(c.control_coverage*100)+'%'],['Semantic coverage',Math.round(c.semantic_coverage*100)+'%'],['Evidence resolution',Math.round(c.evidence_resolution*100)+'%'],['Visible trace gaps',c.trace_gaps]].map(([l,v])=>`<div class="metric"><strong>${esc(v)}</strong><span>${esc(l)}</span></div>`).join('');
document.getElementById('route').innerHTML=packet.declared_route.length?`<div class="route">${packet.declared_route.map((r,i)=>`${i?'<span class="arrow" aria-hidden="true">→</span>':''}<article class="card step ${r.observability_gap?'gap':'good'}" data-search="${esc(text(r).toLowerCase())}"><span class="meta">${esc(r.mode)} · ${esc(r.status)}</span><h3>${esc(r.step_id)}</h3><div>${esc(r.skill)}</div>${r.observability_gap?`<p class="status">${esc(r.observability_gap)}</p>`:''}</article>`).join('')}</div>`:empty('declared route');
list('inferences',packet.inferences,r=>r.conclusion||r.question||r.event_id,r=>`<dl><dt>Step</dt><dd>${esc(r.step_id)}</dd><dt>Question</dt><dd>${esc(r.question)}</dd><dt>Premises</dt><dd>${esc(text(r.premises))}</dd><dt>Operator</dt><dd>${esc(r.operator)}</dd><dt>Public warrant</dt><dd>${esc(r.warrant)}</dd><dt>Conclusion</dt><dd>${esc(r.conclusion)}</dd><dt>Uncertainty</dt><dd>${esc(text(r.uncertainty))}</dd><dt>Scope</dt><dd>${esc(text(r.scope))}</dd></dl>`);
list('timeline',packet.timeline,r=>`${r.sequence}. ${r.event_family}`,r=>`<dl>${meta({event_id:r.event_id,step:r.step_id,skill:r.skill,timestamp:r.timestamp,disposition:r.workflow_disposition,parents:r.parent_event_ids})}</dl>`);
list('claims',packet.claims,r=>r.text,r=>`<dl>${meta({epistemic_status:r.epistemic_status,integrity_status:r.integrity_status,workflow_disposition:r.workflow_disposition,scope:r.scope,evidence_ids:r.evidence_ids,obligation_ids:r.obligation_ids,trace_incomplete:r.trace_incomplete})}</dl>`);
list('evidence',packet.evidence,r=>r.label||r.path||r.evidence_id,r=>`<dl>${meta(r)}</dl>`);
list('failures',packet.alternatives_and_failures,r=>r.kind,r=>`<dl>${meta(r)}</dl>`);
list('scope',packet.scope_ledger,r=>r.step_id||r.event_id,r=>`<pre>${esc(text(r.scope))}</pre>`);
list('gates',packet.decisions_and_gates,r=>`${r.family}: ${r.disposition}`,r=>`<dl>${meta(r)}</dl>`);
list('obligations',packet.obligations,r=>r.requirement||r.obligation_id,r=>`<dl>${meta(r)}</dl>`);
list('artifacts',packet.artifacts_and_receipts,r=>r.path||r.artifact_type||r.artifact_id,r=>`<dl>${meta(r)}</dl>`);
list('authority',packet.authority_ledger,r=>r.step_id||r.event_id,r=>`<dl>${meta(r)}</dl>`);
list('handoffs',packet.handoffs,r=>r.target_workflow||r.workflow||r.event_id,r=>`<dl>${meta(r)}</dl>`);
document.getElementById('graph').innerHTML=`<div class="grid">${card('Nodes',`<p>${packet.graph.nodes.length} typed nodes</p>`)}${card('Edges',`<p>${packet.graph.edges.length} typed edges</p>`)}</div>`+bounded(packet.graph.edges).map(e=>`<div class="card edge" data-search="${esc(text(e).toLowerCase())}">${esc(e.source)} <b>—${esc(e.type)}→</b> ${esc(e.target)}</div>`).join('')+truncation(packet.graph.edges);
document.getElementById('coverage').innerHTML=`<div class="grid">${card('Coverage summary',`<dl>${meta(c)}</dl>`)}${card('Interpretation',`<p>Control coverage records execution visibility. Semantic coverage separately requires a public inference summary or justified conditional N/A. Integrity receipts do not establish scientific correctness.</p>`,'notice')}</div>`;
list('projections',packet.specialized_projections||[],r=>r.projection_kind,r=>`<dl>${meta(r)}</dl>`);
const tabs=[...document.querySelectorAll('.tab')];
function activateTab(tab,focus=false){tabs.forEach(x=>{x.setAttribute('aria-selected','false');x.tabIndex=-1});document.querySelectorAll('.view').forEach(x=>x.classList.remove('active'));tab.setAttribute('aria-selected','true');tab.tabIndex=0;document.getElementById('view-'+tab.dataset.view).classList.add('active');if(focus)tab.focus();}
tabs.forEach((tab,index)=>{tab.addEventListener('click',()=>activateTab(tab));tab.addEventListener('keydown',event=>{let next=index;if(event.key==='ArrowRight')next=(index+1)%tabs.length;else if(event.key==='ArrowLeft')next=(index-1+tabs.length)%tabs.length;else if(event.key==='Home')next=0;else if(event.key==='End')next=tabs.length-1;else return;event.preventDefault();activateTab(tabs[next],true);});});
document.getElementById('query').addEventListener('input',e=>{const q=e.target.value.toLowerCase();document.querySelectorAll('[data-search]').forEach(x=>x.hidden=!x.dataset.search.includes(q));});
"""


VIEWS = [
    ("overview", "Overview"), ("route", "Workflow Route"), ("graph", "Inference Graph"),
    ("timeline", "Timeline"), ("claims", "Claims & Evidence"), ("failures", "Alternatives & Failures"),
    ("scope", "Scope"), ("gates", "Decisions & Gates"), ("obligations", "Obligations"),
    ("artifacts", "Artifacts & Receipts"), ("authority", "Authority"), ("handoffs", "Handoffs"),
    ("coverage", "Trace Coverage"),
]


def render(packet: dict) -> str:
    encoded = json.dumps(packet, ensure_ascii=False, sort_keys=True, separators=(",", ":")).replace("<", "\\u003c")
    tabs = "".join(f'<button id="tab-{key}" class="tab" data-view="{key}" aria-controls="view-{key}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}" role="tab">{html.escape(label)}</button>' for i, (key, label) in enumerate(VIEWS))
    sections = []
    for i, (key, label) in enumerate(VIEWS):
        active = " active" if i == 0 else ""
        if key == "overview":
            body = '<div id="metrics" class="metrics"></div><div class="grid"><section class="card"><h2>Expert reading contract</h2><p>Inspectable public rationale only: execution, artifact integrity, and scientific epistemic status are distinct.</p></section><section class="card"><h2>Current lens</h2><p id="lens-spine"></p></section></div><section id="inferences"></section><h2>Established specialized projections</h2><section id="projections"></section>'
        elif key == "route": body = '<section id="route"></section>'
        elif key == "graph": body = '<section id="graph"></section>'
        elif key == "claims": body = '<div class="grid"><section><h2>Claims</h2><div id="claims"></div></section><section><h2>Typed evidence</h2><div id="evidence"></div></section></div>'
        else: body = f'<section id="{key}"></section>'
        sections.append(f'<section id="view-{key}" class="view{active}" role="tabpanel" aria-labelledby="tab-{key}"><h2>{html.escape(label)}</h2>{body}</section>')
    title = html.escape(str(packet.get("lens", {}).get("visible_name", "Public Reasoning Trace")))
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{CSS}</style></head><body><header class="top"><div class="eyebrow">Expert public reasoning trace</div><h1 id="title">{title}</h1><p id="focus" class="focus"></p><div id="identity" class="identity"></div></header><div class="controls"><input id="query" type="search" aria-label="Filter visible trace cards" placeholder="Filter step, claim, evidence, status…"><nav class="tabs" role="tablist">{tabs}</nav></div><main>{''.join(sections)}</main><script id="trace-data" type="application/json">{encoded}</script><script>{JS}\ndocument.getElementById('lens-spine').textContent=packet.lens.spine_label||'Declared workflow route';</script></body></html>'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    packet = json.loads(args.packet.read_text(encoding="utf-8"))
    output = args.output or args.packet.with_suffix(".html")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(packet), encoding="utf-8")
    print(json.dumps({"output": str(output), "bytes": output.stat().st_size}, sort_keys=True))


if __name__ == "__main__":
    main()
