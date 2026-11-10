// SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
// SPDX-License-Identifier: MIT
// Optional argv[2] is a local Python bridge supplied by its integration test.
import assert from 'node:assert/strict';
import {createHmac,createHash} from 'node:crypto';
import {createNativeBridge,nativeBridgeDefinitions} from '../../integrations/chatgpt/sites/native_bridge.mjs';

const env={ABDUCER_NATIVE_BRIDGE_URL:'https://native.example',ABDUCER_NATIVE_BRIDGE_KEY:'12'.repeat(32),ABDUCER_NATIVE_BRIDGE_AUDIENCE:'site-test-audience'};
const request=new Request('https://sites.example/api',{headers:{'oai-authenticated-user-id':'sites-alice'}});
let calls=0;
const bridge=createNativeBridge({fetchImpl:async(url,init)=>{
  calls++;
  assert.equal(url,'https://native.example/bridge/v1/call');
  const body=JSON.parse(init.body);
  assert.equal(body.principal,'sites-alice');
  assert.equal(body.audience,env.ABDUCER_NATIVE_BRIDGE_AUDIENCE);
  const message=['abducer-bridge-v1','POST','/bridge/v1/call',body.audience,init.headers['X-Abducer-Timestamp'],init.headers['X-Abducer-Nonce'],createHash('sha256').update(init.body).digest('hex')].join('\n');
  assert.equal(init.headers['X-Abducer-Signature'],createHmac('sha256',Buffer.from(env.ABDUCER_NATIVE_BRIDGE_KEY,'hex')).update(message).digest('hex'));
  assert.equal(init.redirect,'manual');
  if(body.operation==='prepare_research_run')assert.equal(body.arguments.title,'From owned storage');
  return Response.json({result:{verified:true}});
}});
assert.equal(nativeBridgeDefinitions.length,15);
assert.equal((await bridge.call('get_execution_capabilities',{},request,env)).verified,true);
await assert.rejects(()=>bridge.call('get_execution_capabilities',{principal:'someone-else'},request,env),/Invalid native arguments/);
await assert.rejects(()=>bridge.call('get_execution_capabilities',{},new Request('https://sites.example'),env),/identity/);
await assert.rejects(()=>bridge.call('get_execution_capabilities',{},request,{...env,ABDUCER_NATIVE_BRIDGE_URL:'http://localhost:8001'}),/HTTPS/);
await assert.rejects(()=>bridge.call('get_execution_capabilities',{},request,{}),/not configured/);
await assert.rejects(()=>bridge.call('prepare_research_run',{project_id:'p',workflow_id:'w',inputs:{}},request,env,{owned:async()=>{throw Error('not owned');}}),/not owned/);
assert.equal(calls,1);
await bridge.call('prepare_research_run',{project_id:'p',workflow_id:'w',inputs:{}},request,env,{owned:async(_env,user,id)=>{assert.equal(user,'sites-alice');assert.equal(id,'p');return {id,title:'From owned storage'};}});
await assert.rejects(()=>bridge.call('get_validation_receipt',{project_id:'p',receipt_id:'a'.repeat(32)},request,env,{owned:async()=>{throw Error('not owned');}}),/not owned/);
assert.equal((await bridge.call('get_validation_receipt',{project_id:'p',receipt_id:'a'.repeat(32)},request,env,{owned:async(_env,user,id)=>{assert.equal(user,'sites-alice');assert.equal(id,'p');return {id,title:'From owned storage'};}})).verified,true);
await assert.rejects(()=>bridge.call('list_validation_receipts',{project_id:'p'},request,env,{owned:async()=>{throw Error('not owned');}}),/not owned/);
await assert.rejects(()=>createNativeBridge({fetchImpl:async()=>Response.json({huge:'x'.repeat(524288)})}).call('get_execution_capabilities',{},request,env),/bounded size/);
await assert.rejects(()=>createNativeBridge({fetchImpl:async()=>new Response('<html>upstream secret</html>')}).call('get_execution_capabilities',{},request,env),/invalid response/);
let redirectCalls=0;
await assert.rejects(()=>createNativeBridge({fetchImpl:async(_url,init)=>{redirectCalls++;assert.equal(init.redirect,'manual');return new Response(null,{status:302,headers:{Location:'https://untrusted.example'}});}}).call('get_execution_capabilities',{},request,env),/redirects are disabled/);
assert.equal(redirectCalls,1);

if(process.argv[2]) {
  // Only the test transport rewrites HTTPS to its ephemeral loopback listener.
  const local=process.argv[2];
  const actual=createNativeBridge({fetchImpl:async(_url,init)=>fetch(local+'/bridge/v1/call',init)});
  const capabilities=await actual.call('get_execution_capabilities',{},request,env);
  assert.equal(capabilities.bridge_authenticated,true);
  const plan=await actual.call('prepare_research_run',{project_id:'javascript-project',workflow_id:'discovery_marathon_workflow',inputs:{target_id:'p-vs-np-target',allow_public_network:true}},request,env,{owned:async()=>({id:'javascript-project',title:'JavaScript signed request'})});
  const start={plan_id:plan.plan_id,idempotency_key:'javascript-idempotent-start'};
  const first=await actual.call('start_research_run',start,request,env);
  const retry=await actual.call('start_research_run',start,request,env);
  assert.equal(first.job_id,retry.job_id);
  const cancelled=await actual.call('cancel_run',{job_id:first.job_id},request,env);
  assert.equal(cancelled.status,'cancelled');
}
console.log(JSON.stringify({passed:true,python_bridge:!!process.argv[2],authenticated_signing:true,ownership:true}));
