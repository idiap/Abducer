// SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
// SPDX-License-Identifier: MIT
// Admission regressions for the real shared viewer: pagination and original
// bytes, identity/range drift, Unicode, corruption, limits and cancellation.
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {webcrypto,createHash} from 'node:crypto';
globalThis.crypto ??= webcrypto;
await import('../../integrations/chatgpt/ui/report_viewer.js');
const text='<!doctype html><p>🧪 ΔE = 0</p><!--'+'x'.repeat(400000)+'-->';
const hash=createHash('sha256').update(text).digest('hex');
const artifact={id:'html',media_type:'text/html',sha256:hash};
const chars=Array.from(text);
const reply=args=>{const end=Math.min(args.offset+args.length,chars.length);return {job_id:'run',artifact_id:'html',media_type:'text/html',sha256:hash,offset:args.offset,total_characters:chars.length,text:chars.slice(args.offset,end).join(''),next_offset:end<chars.length?end:null};};
let active=0,maximum=0;
const call=async(name,args)=>{assert.equal(name,'get_report');active++;maximum=Math.max(maximum,active);await new Promise(r=>setImmediate(r));active--;return reply(args);};
const result=await AbducerReports.load({call,jobId:'run',artifact});
assert.equal(result.text,text);assert.equal(createHash('sha256').update(result.raw).digest('hex'),hash);assert(maximum<=4);
for(const change of [
  v=>({...v,job_id:'other'}), v=>({...v,artifact_id:'other'}),
  v=>({...v,media_type:'text/plain'}), v=>({...v,sha256:'0'.repeat(64)}),
  v=>({...v,offset:1}), v=>({...v,next_offset:0}),
  v=>({...v,total_characters:65*1024*1024}), v=>({...v,text:v.text.slice(1)}),
  v=>({...v,text:v.text.replace('doctype','DOCTYPe')}),
]) await assert.rejects(AbducerReports.load({jobId:'run',artifact,call:async(_name,args)=>change(reply(args))}));
await assert.rejects(AbducerReports.load({jobId:'run',artifact,call:async(_name,args)=>({...reply(args),total_characters:chars.length+(args.offset?1:0)})}),/changed/);
let current=true;
await assert.rejects(AbducerReports.load({jobId:'run',artifact,isCurrent:()=>current,call:async(_name,args)=>{current=false;return reply(args);}}),/selection/);
let requests=0,progress=0;
await assert.rejects(AbducerReports.load({jobId:'run',artifact,progress:()=>progress++,call:async(_name,args)=>{
  requests++;
  if(args.offset===65536)throw Error('Network interrupted');
  if(args.offset)await new Promise(r=>setImmediate(r));
  return reply(args);
}}),/interrupted/);
const lastProgress=progress;await new Promise(r=>setImmediate(r));
assert.equal(progress,lastProgress);assert(requests<=5,'Failed download must stop scheduling pages');
assert.equal((await readFile(new URL('../../integrations/chatgpt/ui/report_viewer.js',import.meta.url),'utf8')).includes("setAttribute('sandbox', 'allow-scripts')"),true);
console.log(JSON.stringify({passed:true,complete_html:true,unicode:true,adversarial_cases:12,max_concurrency:maximum}));
