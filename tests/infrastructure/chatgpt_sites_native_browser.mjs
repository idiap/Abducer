// SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
// SPDX-License-Identifier: MIT
// Real Explorer, Sites Worker, signing bridge and SQLite; native responses are
// explicit UI fixtures. No model, research workflow or remote service is run.
// node tests/infrastructure/chatgpt_sites_native_browser.mjs LIBRARY_JSON PLAYWRIGHT_PROJECT
import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
import {DatabaseSync} from 'node:sqlite';
import {webcrypto,createHash} from 'node:crypto';
import {createWorker} from '../../integrations/chatgpt/sites/worker.mjs';
import {createNativeBridge} from '../../integrations/chatgpt/sites/native_bridge.mjs';

const [libraryPath,playwrightProject]=process.argv.slice(2);
if(!libraryPath||!playwrightProject)throw Error('Expected catalog JSON and Playwright project');
const library=JSON.parse(await readFile(libraryPath,'utf8'));
const reportViewer=await readFile(new URL('../../integrations/chatgpt/ui/report_viewer.js',import.meta.url),'utf8');
const html=(await readFile(new URL('../../integrations/chatgpt/sites/explorer.html',import.meta.url),'utf8')).replace('<!-- ABDUCER_REPORT_VIEWER -->','<script>'+reportViewer+'</script>');
const {chromium}=await import(pathToFileURL(resolve(playwrightProject,'node_modules/playwright/index.mjs')).href);
const origin='https://abducer.andrenfreitas.chatgpt.site', sql=new DatabaseSync(':memory:');
sql.exec(await readFile(new URL('../../integrations/chatgpt/sites/schema.sql',import.meta.url),'utf8'));
const env={ABDUCER_NATIVE_BRIDGE_URL:'https://native.fixture.test',ABDUCER_NATIVE_BRIDGE_KEY:'ab'.repeat(32),ABDUCER_NATIVE_BRIDGE_AUDIENCE:'browser-fixture',DB:{prepare(query){return {bind(...args){const prepared=sql.prepare(query);return {async first(){return prepared.get(...args)||null;},async all(){return {results:prepared.all(...args)};},async run(){return {meta:prepared.run(...args)};}};}};}}};
let available=false,loseFirstStart=true,job=null;
const calls=[],starts=[],networkRequests=[];
const modelPayload=JSON.stringify({messages:[{role:'user',content:'Original native prompt '+ 'x'.repeat(17000)}],response_format:{type:'json_schema',json_schema:{schema:{type:'object',properties:{answer:{type:'string'}},required:['answer'],additionalProperties:false}}}});
const report='<!doctype html><title>Reasoning fixture</title><p id="equation">ΔE = 0 · 🧪</p><button id="timeline" onclick="document.querySelector(\'#evidence\').hidden=false">Timeline</button><p id="evidence" hidden>Recorded evidence</p><script>try{parent.document.body.dataset.attacked="yes"}catch{};fetch("/escape").catch(()=>{});</script><!--'+'evidence '.repeat(18000)+'-->';
const reportHash=createHash('sha256').update(report).digest('hex');
const bridge=createNativeBridge({cryptoImpl:webcrypto,fetchImpl:async(url,options)=>{
  const request=JSON.parse(options.body),{operation,arguments:args}=request;
  assert.equal(request.principal,'native-browser-user');assert.match(options.headers['X-Abducer-Signature'],/^[a-f0-9]{64}$/);
  calls.push({operation,args});let result;
  if(operation==='get_execution_capabilities'){
    if(!available)return Response.json({error:{code:'native_unavailable',message:'The native worker is offline.'}},{status:503});
    result={dependency_setup:{status:'ready',packages:{loaded:12,verified_count:51,python:{version:"3.12.13"}},skills:221,workflows:34,source_files:1248},executable_workflows:['discovery_marathon_workflow'],execution_reason:'A source-matched worker is online.',worker_online:true,model_providers:['chatgpt'],native_hooks_enabled:true,targets:['p-vs-np-target','yang-mills-existence-and-mass-gap-target'],limits:{timeout_seconds:7200,max_model_calls:50,max_output_tokens:32000},workflow_execution:[{workflow_id:'discovery_marathon_workflow',execution_status:'executable',reason:'Qualified native adapter.'},{workflow_id:'cohere_fast_workflow',execution_status:'agent-driven',reason:'Needs authored child packets.'}]};
  }else if(operation==='list_runs')result={runs:job?[job]:[]};
  else if(operation==='prepare_research_run')result={plan_id:'fixture-plan',contract_workflow_id:args.workflow_id,workflow_id:'discovery_marathon_loop',inputs:args.inputs,budget:{timeout_seconds:args.budget_seconds,max_model_calls:args.max_model_calls,max_output_tokens:args.max_output_tokens},expires_at:Date.now()/1000+900};
  else if(operation==='start_research_run'){
    starts.push(args.idempotency_key);job??={job_id:'fixture-native-job',status:'running',workflow_id:'discovery_marathon_loop',contract_workflow_id:'discovery_marathon_workflow',model_handoff_waiting:true,pending_model_request:{request_id:'fixture-request',sequence:1},cancel_requested:false};
    if(loseFirstStart){loseFirstStart=false;return Response.json({error:{code:'native_unavailable',message:'Start response lost; recover this exact start.'}},{status:502});}result=job;
  }else if(operation==='get_run_status')result=job;
  else if(operation==='get_pending_model_request'){
    const offset=args.offset||0,end=Math.min(offset+(args.limit||16000),modelPayload.length);
    result={job_id:job.job_id,request_id:'fixture-request',pending:true,sequence:1,offset,content:modelPayload.slice(offset,end),total_chars:modelPayload.length,next_offset:end<modelPayload.length?end:null};
  }else if(operation==='cancel_run'){job.cancel_requested=true;result=job;}
  else if(operation==='list_run_artifacts')result={artifacts:[{id:'fixture-report',name:'full_timeline.html',sha256:reportHash,media_type:'text/html'}]};
  else if(operation==='get_report'){const chars=Array.from(report),offset=args.offset||0,end=Math.min(offset+(args.length||16000),chars.length);result={job_id:args.job_id,artifact_id:args.artifact_id,text:chars.slice(offset,end).join(''),offset,total_characters:chars.length,next_offset:end<chars.length?end:null,sha256:reportHash,media_type:'text/html'};}
  else if(operation==='get_workflow_dependencies')result={workflow_id:args.workflow_id,entries:[{path:'hooks/hooks.json',sha256:'b'.repeat(64)}],issues:[],declared_sources_complete:true,next_offset:null};
  else if(operation==='get_workflow_dependency_source')result={workflow_id:args.workflow_id,path:args.path,content:'{"hooks": ["PreSkillUse", "Stop"]}',next_offset:null};
  else throw Error('Unexpected fixture operation '+operation);
  return Response.json({result});
}});
const worker=createWorker(library,html,origin,null,bridge);
const embed=`<!doctype html><html><body><iframe title="Abducer" src="/" style="width:100%;height:100vh;border:0"></iframe><script>window.sentMessages=[];window.addEventListener('message',async e=>{if(e.source!==document.querySelector('iframe').contentWindow)return;const m=e.data;if(!m.id)return;let result={};try{if(m.method==='tools/call'){const response=await fetch('/api',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:m.params.name,arguments:m.params.arguments})});result=await response.json();}if(m.method==='ui/message')window.sentMessages.push(m.params);e.source.postMessage({jsonrpc:'2.0',id:m.id,result},'*');}catch(error){e.source.postMessage({jsonrpc:'2.0',id:m.id,error:{message:error.message}},'*');}});</script></body></html>`;
const server=createServer(async(req,res)=>{try{if(req.url==='/embedded'){res.writeHead(200,{'Content-Type':'text/html'});res.end(embed);return;}let body='';for await(const chunk of req)body+=chunk;const headers=new Headers(req.headers);headers.set('oai-authenticated-user-id','native-browser-user');if(headers.has('Origin'))headers.set('Origin',origin);const response=await worker.fetch(new Request(origin+req.url,{method:req.method,headers,...(body?{body}:{})}),env);res.writeHead(response.status,Object.fromEntries(response.headers));res.end(Buffer.from(await response.arrayBuffer()));}catch(error){res.writeHead(500);res.end(String(error));}});
await new Promise(done=>server.listen(0,'127.0.0.1',done));
const browser=await chromium.launch({headless:true}),page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[];
page.on('pageerror',error=>errors.push(String(error)));
const url='http://127.0.0.1:'+server.address().port;
page.on('request',request=>networkRequests.push(request.url()));
try{
  await page.goto(url);await page.locator('.node').first().waitFor();
  assert.match(await page.locator('#setup-status').textContent(),/Catalog loaded/);
  assert.equal(starts.length,0);
  await page.click('#tab-projects');await page.fill('#project-title','Native browser fixture');await page.fill('#project-question','Which evidence changes this hypothesis?');await page.locator('#project-form').evaluate(form=>form.requestSubmit());
  await page.waitForFunction(()=>document.querySelector('#native-status').textContent==='Execution unavailable');
  assert.equal(await page.locator('#native-prepare').isDisabled(),true);
  assert.equal(calls.some(c=>c.operation==='start_research_run'),false);
  available=true;await page.click('#native-refresh');await page.waitForFunction(()=>document.querySelector('#native-status').textContent==='Execution available');
  assert.equal(await page.locator('#native-workflow option').count(),1);
  assert.match(await page.locator('#native-budget-note').textContent(),/token usage is not measured/);
  await page.locator('#native-readiness summary').click();await page.locator('#native-workflow-statuses button').first().click();await page.locator('#native-dependency-list button').first().click();
  await page.waitForFunction(()=>document.querySelector('#native-dependency-source').textContent.includes('PreSkillUse'));
  await page.check('#native-network');await page.fill('#native-minutes','5');await page.fill('#native-calls','2');await page.locator('#native-form').evaluate(form=>form.requestSubmit());
  await page.locator('#native-plan').waitFor({state:'visible'});assert.equal(starts.length,0);
  const prepared=calls.find(c=>c.operation==='prepare_research_run').args;assert.equal(prepared.budget_seconds,300);assert.equal(prepared.max_model_calls,2);assert.equal(prepared.inputs.allow_public_network,true);
  await page.click('#native-start');await page.waitForFunction(()=>document.querySelector('#native-start').textContent==='Retry this same start');
  await page.click('#native-start');await page.locator('#native-run-detail').waitFor({state:'visible'});assert.equal(starts.length,2);assert.equal(starts[0],starts[1]);assert.match(await page.locator('#native-plan-summary').textContent(),/has been submitted/);
  await page.click('#native-model-read');await page.locator('#native-model-more').waitFor({state:'visible'});await page.click('#native-model-more');await page.waitForFunction(()=>document.querySelector('#native-model-more').hidden);
  assert.match(await page.locator('#native-model-meta').textContent(),/characters 16000/);
  assert.match(await page.locator('#native-model-content').textContent(),/additionalProperties/);
  assert.equal(await page.locator('#native-model-send').isVisible(),false);
  await page.context().grantPermissions(['clipboard-read','clipboard-write'],{origin:url});await page.click('#native-model-copy');
  assert.match(await page.evaluate(()=>navigator.clipboard.readText()),/Read get_pending_model_request.*every next_offset/);
  assert.equal(calls.some(c=>c.operation==='submit_model_response'),false);
  job={...job,status:'succeeded',model_handoff_waiting:false,outcome:{execution_outcome:'initialization_requires_revision',scientific_truth_verified:false,native_hook_coverage:{owner_skill:'long-horizon-route-portfolio-manager',chatgpt_global_hooks:false}}};
  await page.click('#native-run-refresh');await page.locator('#native-artifacts button').waitFor();await page.locator('#native-artifacts button').click();
  await page.waitForFunction(()=>document.querySelector('#native-report-content').textContent.includes('Reasoning fixture'));
  assert.equal(await page.locator('#native-report-content img').count(),0);
  await page.getByRole('button',{name:'Open reasoning HTML'}).click();
  const reportFrame=page.frameLocator('#native-report iframe');
  await reportFrame.locator('#timeline').click();await reportFrame.locator('#evidence').waitFor({state:'visible'});
  assert.equal(await page.locator('#native-report iframe').getAttribute('sandbox'),'allow-scripts');
  assert.equal(await page.locator('body').getAttribute('data-attacked'),null);
  assert.equal(networkRequests.some(url=>url.endsWith('/escape')),false);
  assert.equal(await reportFrame.locator('#equation').textContent(),'ΔE = 0 · 🧪');
  const downloadPromise=page.waitForEvent('download');await page.getByRole('link',{name:'Download original HTML'}).click();const download=await downloadPromise;
  assert.equal(createHash('sha256').update(await readFile(await download.path())).digest('hex'),reportHash);
  await page.click('#native-report-more');await page.waitForFunction(()=>document.querySelector('#native-report-meta').textContent.includes('character 16000'));
  assert.equal(await page.locator('#native-report iframe').count(),0);
  assert.match(await page.locator('#native-run-content').textContent(),/initialization_requires_revision/);assert.match(await page.locator('#native-run-list button').textContent(),/succeeded/);
  await page.setViewportSize({width:390,height:844});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);await page.screenshot({path:'/tmp/abducer-native-explorer-mobile.png',fullPage:true});
  job={...job,status:'running',model_handoff_waiting:true,outcome:undefined};await page.click('#native-run-refresh');await page.click('#native-cancel');
  await page.waitForFunction(()=>document.querySelector('#native-run-summary').textContent.includes('waiting for the worker'));
  assert.equal(await page.locator('#native-run-status').textContent(),'running');assert.equal(await page.locator('#native-cancel').isDisabled(),true);
  job={...job,status:'cancelled',model_handoff_waiting:false};await page.click('#native-run-refresh');await page.waitForFunction(()=>document.querySelector('#native-run-status').textContent==='cancelled');
  // The embedded bridge sends a real continuation request, never a fixture answer.
  job={...job,status:'running',model_handoff_waiting:true,cancel_requested:false};
  await page.setViewportSize({width:1440,height:1000});await page.goto(url+'/embedded');const frame=page.frameLocator('iframe');
  await frame.locator('.node').first().waitFor();await frame.locator('#setup-status').filter({hasText:'Dependencies loaded'}).waitFor();assert.match(await frame.locator('#setup-status').textContent(),/Python 3.12.13.*51 packages verified.*221 skills.*34 workflows.*1248 supporting files/);await frame.locator('#tab-projects').click();await frame.locator('#project-list button').first().click();await frame.locator('#native-run-list button').first().click();await frame.locator('#native-model-send').click();
  await page.waitForFunction(()=>window.sentMessages.length===1);const handoff=await page.evaluate(()=>window.sentMessages[0]);assert.equal(handoff.role,'user');assert.match(handoff.content[0].text,/fixture-native-job/);assert.match(handoff.content[0].text,/submit_model_response/);
  assert.equal(calls.some(c=>c.operation==='submit_model_response'),false);
  assert.deepEqual(errors,[]);console.log(JSON.stringify({passed:true,source:'actual Worker and signing bridge',native_backend:'controlled fixture',native_hooks:'not executed by browser fixture',idempotent_start_recovery:true,pending_request_pagination:true,embedded_handoff:true,mobile_width:390}));
}finally{await browser.close();server.close();sql.close();}
