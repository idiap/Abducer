// SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
// SPDX-License-Identifier: MIT
// Run against a real Chromium iframe using an explicit Playwright installation:
// node tests/infrastructure/chatgpt_explorer_browser.mjs /path/to/project-with-playwright
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import { pathToFileURL } from 'node:url';

const installed=process.argv[2];
const {chromium}=installed
  ? await import(pathToFileURL(path.resolve(installed,'node_modules/@playwright/test/index.mjs')))
  : await import('@playwright/test');
const html=fs.readFileSync('integrations/chatgpt/ui/explorer.html','utf8').replace('<!-- ABDUCER_REPORT_VIEWER -->','<script>'+fs.readFileSync('integrations/chatgpt/ui/report_viewer.js','utf8')+'</script>');
const viewer=JSON.parse(fs.readFileSync('integrations/domain_package/assets/bundle.json','utf8')).projects[0].workflows.find(x=>x.id==='conceptual_hypothesis_exploration_loop');
const workflowId='conceptual_hypothesis_exploration_workflow';
const encoded=value=>JSON.stringify(value).replaceAll('<','\\u003c');
const host=`<!doctype html><html><body><iframe title="Explorer" sandbox="allow-scripts" src="/explorer" style="width:100%;height:1100px;border:0"></iframe><script>
const viewer=${encoded(viewer)};window.calls=[];
const answers={
search_skills:()=>({skills:[{name:'kb-abduce'}],next_cursor:null}),get_skill:()=>({name:'kb-abduce',source:'skills/reasoning/kb-abduce/SKILL.md',sha256:'skill-hash',instructions:'Canonical abductive procedure'}),
get_profile:()=>({name:'Named Researcher'}),list_projects:()=>({projects:[{id:'project-a',name:'Project A',role:'researcher',version:1}]}),
list_workflows:()=>({release:'release-a',workflows:[{id:'${workflowId}'}]}),
get_capabilities:()=>({release:'release-a',dependency_setup:{status:'ready',packages:{loaded:12,verified_count:51,python:{version:"3.12.13"}},skills:221,workflows:34,source_files:1248},executable_workflows:['discovery_marathon_workflow'],limits:{}}),
get_workflow:()=>({release:'release-a',workflow:{id:'${workflowId}',contract:{description:'Source-backed contract'}},viewer}),
prepare_research_run:()=>({plan_id:'plan-a',expires_at:9999999999}),start_research_run:()=>({job_id:'job-a',status:'queued'}),
get_run_status:()=>({job_id:'job-a',status:'succeeded',scientific_truth_verified:false}),
list_runs:()=>({runs:[{job_id:'job-a',status:'succeeded'}]}),list_run_artifacts:()=>({artifacts:[{id:'artifact-a',name:'Evidence report',media_type:'text/html',sha256:'digest-a'}]}),
get_report:()=>({text:'<img src=x onerror="window.attacked=true"> Evidence remains unverified.',media_type:'text/html',has_more:false})};
window.addEventListener('message',e=>{if(e.source!==document.querySelector('iframe').contentWindow)return;const m=e.data;window.calls.push(m);if(m.id===undefined)return;let result={};if(m.method==='tools/call')result={structuredContent:answers[m.params.name](m.params.arguments)};e.source.postMessage({jsonrpc:'2.0',id:m.id,result},'*');});
</script></body></html>`;
const server=http.createServer((request,response)=>{response.setHeader('Content-Type','text/html; charset=utf-8');response.end(request.url==='/explorer'?html:host);});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const browser=await chromium.launch({headless:true});
try{
 const page=await browser.newPage({viewport:{width:1100,height:1200}});
 const errors=[];page.on('pageerror',error=>errors.push(String(error)));
 await page.goto(`http://127.0.0.1:${server.address().port}`);
 const frame=page.frameLocator('iframe');
 await frame.locator('#account').filter({hasText:'Named Researcher'}).waitFor();
 await frame.locator('#setup-status').filter({hasText:'221 skills'}).waitFor();
 assert.match(await frame.locator('#setup-status').textContent(),/Python 3.12.13.*51 packages verified/);
 assert.equal(await page.evaluate(()=>window.calls.some(x=>x.params?.name==='start_research_run')),false);
 await frame.locator('#workflow-list button').click();
 await frame.locator('#graph svg g.node').first().waitFor();
 assert.equal(await frame.locator('#graph svg g.node').count(),viewer.graph.nodes.length);
 assert.equal(await frame.locator('#graph svg line').count(),viewer.graph.edges.length);
 await frame.locator('#graph svg g.node').first().focus();await page.keyboard.press('Enter');
 await page.waitForFunction(()=>window.calls.some(x=>x.method==='ui/update-model-context'));
 await frame.locator('#source-panel summary').click();
 assert((await frame.locator('#source-text').textContent()).length>50);
 assert((await frame.locator('#filter').boundingBox()).height<65,'Sidebar search must not stretch to graph height');
 assert((await frame.locator('#workflow-list button').first().boundingBox()).height<140,'Workflow buttons must remain compact');
 await frame.locator('body').evaluate(()=>window.scrollTo(0,0));
 if(process.argv[3])await page.screenshot({path:process.argv[3],fullPage:true});
 await frame.locator('#tab-skills').click();await frame.locator('#search-skills').click();await frame.locator('#skill-list button').click();
 await frame.locator('#skill-text').filter({hasText:'Canonical abductive procedure'}).waitFor();
 await frame.locator('#tab-research').click();
 await frame.locator('#allow-network').check();
 await frame.locator('#plan-form button').click();
 await page.waitForTimeout(300);if(!await frame.locator('#start').isVisible())throw new Error('Plan did not render: '+await frame.locator('#notice').textContent());await frame.locator('#start').waitFor({state:'visible'});await frame.locator('#start').click();
 await frame.locator('#job-status').filter({hasText:'succeeded'}).waitFor();
 await frame.locator('#view-reports').click();await frame.locator('#artifact-list button').click();
 await frame.locator('#report-body pre').filter({hasText:'Evidence remains unverified'}).waitFor();
 assert.equal(await frame.locator('#report-body img').count(),0);
 assert.equal(await frame.locator('#report-body script').count(),0);
 const calls=await page.evaluate(()=>window.calls);
 const plan=calls.find(x=>x.params?.name==='prepare_research_run').params.arguments;
 assert.deepEqual(plan.inputs,{target_id:'p-vs-np-target',allow_public_network:true});
 assert.equal(plan.project_id,'project-a');assert.equal(plan.max_output_tokens,32000);
 await page.setViewportSize({width:420,height:1000});
 await frame.locator('#tab-workflows').click();
 assert(await frame.locator('#graph svg').isVisible());
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({status:'pass',browser:'Chromium',opaque_iframe:true,graph_nodes:viewer.graph.nodes.length,graph_edges:viewer.graph.edges.length,research_flow:true,report_xss_safe:true,mobile:true}));
}finally{await browser.close();await new Promise(resolve=>server.close(resolve));}
