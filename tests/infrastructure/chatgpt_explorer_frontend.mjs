// SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
// SPDX-License-Identifier: MIT
// Exercise the shipped inline script with a deterministic DOM/host bridge.
// This covers client state and message behavior; browser rendering is separate.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import { webcrypto } from 'node:crypto';

class Element {
  constructor(tag='div') { this.tagName=tag; this.children=[]; this.attributes={}; this.value=''; this.textContent=''; this.hidden=false; this.disabled=false; this.className=''; }
  remove() {}
  append(...children) { this.children.push(...children); if(this.tagName==='select'&&!this.value&&children[0])this.value=children[0].value; }
  replaceChildren(...children) { this.children=[];this.value='';this.append(...children); }
  setAttribute(name,value) { this.attributes[name]=value; }
  getAttribute(name) { return this.attributes[name]; }
  set selectedIndex(index) { this.value=this.children[index]?.value||''; }
}
const html=fs.readFileSync('integrations/chatgpt/ui/explorer.html','utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
assert(!script.includes('innerHTML'), 'Untrusted research must not be interpreted as markup');
assert(!script.includes('fetch('), 'UI must use the authenticated host bridge');
const elements=new Map([...html.matchAll(/<(\w+)[^>]*\bid="([^"]+)"/g)].map(m=>[m[2],new Element(m[1])]));
const viewer=JSON.parse(fs.readFileSync('integrations/domain_package/assets/bundle.json','utf8')).projects[0].workflows.find(x=>x.id==='conceptual_hypothesis_exploration_loop');
const calls=[]; let onMessage;let sequence=0;
const workflowId='conceptual_hypothesis_exploration_workflow';
const responses={
  get_profile:()=>({name:'Researcher A'}),
  search_skills:()=>({skills:[{name:'kb-abduce'}],next_cursor:null}),
  get_skill:()=>({name:'kb-abduce',source:'skills/reasoning/kb-abduce/SKILL.md',sha256:'skill-hash',instructions:'Canonical abductive procedure'}),
  list_projects:()=>({projects:[{id:'project-a',name:'Research A',role:'researcher',version:1}]}),
  list_workflows:()=>({release:'release-a',workflows:[{id:workflowId}]}),
  get_capabilities:()=>({release:'release-a',executable_workflows:['discovery_marathon_workflow'],limits:{}}),
  get_workflow:()=>({release:'release-a',workflow:{id:workflowId,contract:{description:'Inspect a reasoning contract'}},viewer}),
  prepare_research_run:()=>({plan_id:'plan-a',expires_at:9999999999}),
  start_research_run:()=>({job_id:'job-a',status:'queued'}),
  get_run_status:()=>({job_id:'job-a',status:'succeeded',scientific_truth_verified:false}),
  list_runs:()=>({runs:[{job_id:'job-a',status:'succeeded',workflow_id:'discovery_marathon_workflow'}]}),
  list_run_artifacts:()=>({artifacts:[{id:'report-a',name:'report.html',media_type:'text/html',sha256:'digest-a'}]}),
  get_report:()=>({text:'<script>window.attacked=true</script><p>Evidence</p>',media_type:'text/html',has_more:false}),
};
const parent={postMessage(message){calls.push(message);if(message.id===undefined)return;queueMicrotask(()=>{let result={};let error;try{if(message.method==='tools/call'){const fn=responses[message.params.name];if(!fn)throw new Error('Unknown tool');result={structuredContent:fn(message.params.arguments)};}}catch(e){error={message:e.message};}onMessage({source:parent,data:{jsonrpc:'2.0',id:message.id,result,error}});});}};
const context=vm.createContext({window:{parent,addEventListener(name,fn){if(name==='message')onMessage=fn;}},document:{getElementById:id=>elements.get(id),createElement:tag=>new Element(tag),createElementNS:(_ns,tag)=>new Element(tag)},setTimeout,clearTimeout,console,crypto:webcrypto,TextEncoder,URL,Blob});
vm.runInContext(fs.readFileSync('integrations/chatgpt/ui/report_viewer.js','utf8'),context);
vm.runInContext(script,context);
const flush=async()=>{for(let i=0;i<12;i++)await new Promise(resolve=>setImmediate(resolve));};
await flush();
assert.equal(elements.get('account').textContent,'Researcher A');
assert(calls.some(x=>x.method==='ui/initialize'));
assert(calls.some(x=>x.method==='ui/notifications/initialized'));
assert.equal(elements.get('project').value,'project-a');
elements.get('workflow-list').children[0].onclick();await flush();
assert.equal(elements.get('workflow-title').textContent,viewer.label);
assert(elements.get('graph').children[0].children.length>0);
const sourceText=elements.get('source-text').textContent;
assert(sourceText.includes('reasoning')||sourceText.includes('SPDX'));
const svg=elements.get('graph').children[0];
const node=svg.children.find(x=>x.attributes.class==='node');
node.onclick();await flush();
const selected=calls.find(x=>x.method==='ui/update-model-context');
assert.equal(selected.params.structuredContent.abducer_selection.project_id,'project-a');
assert.equal(selected.params.structuredContent.abducer_selection.workflow_id,workflowId);
elements.get('search-skills').onclick();await flush();elements.get('skill-list').children[0].onclick();await flush();
assert.equal(elements.get('skill-text').textContent,'Canonical abductive procedure');
elements.get('target-id').value='p-vs-np-target';elements.get('allow-network').checked=true;
elements.get('budget').value='7200';elements.get('model-calls').value='50';
elements.get('plan-form').onsubmit({preventDefault(){}});await flush();
assert.equal(elements.get('plan').hidden,false);
elements.get('start').onclick();await flush();elements.get('start').onclick();await flush();
const starts=calls.filter(x=>x.params?.name==='start_research_run');
assert.equal(starts.length,2);assert.equal(starts[0].params.arguments.idempotency_key,starts[1].params.arguments.idempotency_key);
assert.equal(elements.get('job-status').textContent,'succeeded');
elements.get('view-reports').onclick();await flush();elements.get('artifact-list').children[0].onclick();await flush();
assert.equal(elements.get('report-body').children[0].tagName,'pre');
assert(elements.get('report-body').children[0].textContent.includes('<script>'));
assert.equal(context.window.attacked,undefined);
elements.get('project').value='';elements.get('project').onchange();
assert.equal(elements.get('plan').hidden,true);assert.equal(elements.get('job').hidden,true);
assert.equal(elements.get('report-body').children.length,0);
console.log(JSON.stringify({status:'pass',bridge:true,source_graph:true,idempotent_start:true,report_text_safe:true}));
