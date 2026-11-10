// SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
// SPDX-License-Identifier: MIT
// Open original native-renderer HTML under the production CSP. Scientific
// contents are an explicit empty-run UI fixture, never a new research result.
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createServer} from 'node:http';
import {createHash} from 'node:crypto';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
const [playwrightProject,reportPath]=process.argv.slice(2);
const {chromium}=await import(pathToFileURL(resolve(playwrightProject,'node_modules/playwright/index.mjs')).href);
const raw=await readFile(reportPath),text=raw.toString('utf8'),chars=Array.from(text),sha256=createHash('sha256').update(raw).digest('hex');
const helper=await readFile(new URL('../../integrations/chatgpt/ui/report_viewer.js',import.meta.url),'utf8');
const csp="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; img-src data:; base-uri 'none'; form-action 'none'";
const html='<!doctype html><meta charset="utf-8"><main id="report"></main><script>'+helper+'</script><script>AbducerReports.mount({container:document.querySelector("main"),jobId:"run",artifact:{id:"html",name:"full_timeline.html",media_type:"text/html",sha256:'+JSON.stringify(sha256)+'},call:async(name,args)=>(await fetch("/page",{method:"POST",body:JSON.stringify(args)})).json()});</script>';
const server=createServer(async(req,res)=>{if(req.url==='/'){res.writeHead(200,{'Content-Type':'text/html','Content-Security-Policy':csp});res.end(html);return;}if(req.url==='/page'){let body='';for await(const part of req)body+=part;const args=JSON.parse(body),end=Math.min(args.offset+args.length,chars.length);res.setHeader('Content-Type','application/json');res.end(JSON.stringify({job_id:'run',artifact_id:'html',media_type:'text/html',sha256,offset:args.offset,total_characters:chars.length,next_offset:end<chars.length?end:null,text:chars.slice(args.offset,end).join('')}));return;}res.writeHead(404);res.end();});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({headless:true});
try{
 const page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[];
 page.on('pageerror',e=>errors.push(String(e)));
 await page.goto('http://127.0.0.1:'+server.address().port);
 await page.getByRole('button',{name:'Open reasoning HTML'}).click();
 const frame=page.frameLocator('#report iframe');
 await frame.locator('#marathon-data').waitFor({state:'attached'});
 await frame.locator('[data-tab="timeline"]').click();
 await frame.locator('#view').waitFor({state:'visible'});
 const actual=page.frames().find(f=>f!==page.mainFrame());
 await actual.waitForFunction(()=>!!window.MathJax?.typesetPromise);
 await actual.evaluate(async()=>{const p=document.createElement('p');p.id='equation-probe';p.textContent='\\[E=mc^2\\]';document.body.append(p);await MathJax.typesetPromise([p]);});
 await frame.locator('#equation-probe mjx-container svg').waitFor();
 const downloadPromise=page.waitForEvent('download');await page.getByRole('link',{name:'Download original HTML'}).click();
 const download=await downloadPromise;assert.deepEqual(await readFile(await download.path()),raw);
 await page.screenshot({path:'/tmp/abducer-reasoning-report-desktop.png',fullPage:true});
 await page.setViewportSize({width:390,height:844});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({passed:true,native_renderer:true,original_bytes:raw.length,timeline:true,embedded_mathjax:true,download_sha256:sha256,mobile_width:390}));
}finally{await browser.close();await new Promise(r=>server.close(r));}
