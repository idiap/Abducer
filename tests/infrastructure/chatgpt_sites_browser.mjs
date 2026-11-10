// SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
// SPDX-License-Identifier: MIT
// Browser integration against the exact built Sites Worker and real SQLite.
// A local adapter supplies test Sites identity; it does not verify hosted login.
// node tests/infrastructure/chatgpt_sites_browser.mjs GENERATED_WORKER PLAYWRIGHT_PROJECT SITE_ORIGIN
import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {readFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
import {DatabaseSync} from 'node:sqlite';

const [workerPath, playwrightProject, origin] = process.argv.slice(2);
if (!workerPath || !playwrightProject || !origin) throw Error('Expected generated Worker, Playwright project and Site origin');
const {default:worker} = await import(pathToFileURL(resolve(workerPath)).href);
const {chromium} = await import(pathToFileURL(resolve(playwrightProject, 'node_modules/playwright/index.mjs')).href);
const sqlite = new DatabaseSync(':memory:');
sqlite.exec(await readFile(new URL('../../integrations/chatgpt/sites/schema.sql', import.meta.url), 'utf8'));
const env = {DB:{prepare(sql){return {bind(...args){const q=sqlite.prepare(sql);return {
  async first(){return q.get(...args)||null;},
  async all(){return {results:q.all(...args)};},
  async run(){return {meta:q.run(...args)};}
};}};}}};
// Only this local test adapter injects identity and rewrites its own browser origin.
const server = createServer(async(req,res)=>{
  try {
    let body='';for await(const chunk of req)body+=chunk;
    const headers=new Headers(req.headers);
    headers.set('oai-authenticated-user-id','browser-test-user');
    if(headers.has('Origin'))headers.set('Origin',origin);
    const response=await worker.fetch(new Request(origin+req.url,{method:req.method,headers,...(body?{body}:{})}),env);
    res.writeHead(response.status,Object.fromEntries(response.headers));
    res.end(Buffer.from(await response.arrayBuffer()));
  } catch(error) {res.writeHead(500);res.end(String(error));}
});
await new Promise(done=>server.listen(0,'127.0.0.1',done));
const browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width:1440,height:1000}});
const errors=[];page.on('pageerror',error=>errors.push(String(error)));
const url='http://127.0.0.1:'+server.address().port;
try {
  await page.goto(url);
  await page.locator('.node').first().waitFor();
  const nodes=await page.locator('.node').count();assert.equal(nodes,8);
  await page.locator('.node').first().focus();await page.keyboard.press('Enter');
  assert.equal(await page.locator('#node-detail').isVisible(),true);
  await page.locator('#contract-details summary').click();
  await page.waitForFunction(()=>document.querySelector('#contract').textContent.includes('{'));
  // Exercise the same actual source paging endpoint used by the next-section UI.
  const source=await page.evaluate(async()=>{
    const read=async offset=>{const r=await fetch('/api',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:'get_workflow_source',arguments:{workflow_id:'conceptual_hypothesis_exploration_workflow',format:'contract',offset,limit:31}})});return (await r.json()).structuredContent;};
    const first=await read(0),second=await read(31);return {first,second};
  });
  assert.equal(source.first.next_offset,31);assert.equal(source.second.offset,31);assert.equal(source.second.content.length,31);
  await page.locator('#contract-details summary').click();
  await page.screenshot({path:'/tmp/abducer-sites-explorer-desktop.png',fullPage:true});
  await page.click('#tab-skills');await page.fill('#skill-query','hypothesis');
  await page.locator('#skill-search').evaluate(form=>form.requestSubmit());
  await page.locator('#skill-list button').first().click();
  await page.waitForFunction(()=>document.querySelector('#skill-content').textContent.includes('---'));
  await page.click('#tab-projects');await page.fill('#project-title','Browser test investigation');
  await page.fill('#project-question','What evidence discriminates these hypotheses?');
  await page.locator('#project-form').evaluate(form=>form.requestSubmit());
  await page.locator('#project-detail').waitFor({state:'visible'});
  await page.fill('#note','<img src=x onerror=alert(1)> is a literal observation');
  await page.locator('#note-form').evaluate(form=>form.requestSubmit());
  await page.waitForFunction(()=>document.querySelector('#notes').textContent.includes('onerror'));
  assert.equal(await page.locator('#notes img').count(),0);
  await page.reload();await page.locator('.node').first().waitFor();await page.click('#tab-projects');
  await page.locator('#project-list button').first().click();
  await page.waitForFunction(()=>document.querySelector('#notes').textContent.includes('onerror'));
  await page.click('#prepare-plan');await page.locator('#plan').waitFor({state:'visible'});
  assert.match(await page.locator('#plan-content').textContent(),/ChatGPT-guided/);
  assert.match(await page.locator('#plan-content').textContent(),/"native_execution": false/);
  await page.setViewportSize({width:390,height:844});await page.click('#tab-workflows');
  await page.screenshot({path:'/tmp/abducer-sites-explorer-mobile.png',fullPage:true});
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  // The tutorial is served by the exact same private Worker as the Explorer.
  await page.setViewportSize({width:1440,height:1000});
  const tutorialResponse=await page.goto(url+'/tutorial');
  assert.equal(tutorialResponse.status(),200);
  await page.locator('#prompt-connect').waitFor();
  assert.equal(await page.locator('[data-copy]').count(),6);
  await page.context().grantPermissions(['clipboard-read','clipboard-write'],{origin:url});
  await page.locator('[data-copy="prompt-connect"]').click();
  assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),await page.locator('#prompt-connect').textContent());
  // Removing each hypothesis must identify a different failed implication.
  await page.locator('#math-tab-base').focus();await page.keyboard.press('ArrowRight');
  assert.equal(await page.locator('#math-tab-compact').getAttribute('aria-selected'),'true');
  assert.match(await page.locator('#math-status').textContent(),/Finite-cover/);
  await page.keyboard.press('ArrowRight');
  assert.match(await page.locator('#math-status').textContent(),/Openness/);
  await page.keyboard.press('ArrowRight');
  assert.match(await page.locator('#math-status').textContent(),/Single-index/);
  await page.keyboard.press('Home');
  assert.equal(await page.locator('#math-tab-base').getAttribute('aria-selected'),'true');
  // Held-out expectations are independent constants, not page-generated values.
  for(const [model,at20,at30] of [['viscous','5.33 mm','3.56 mm'],['coulomb','4.00 mm','Regime limit'],['quadratic','6.00 mm','4.80 mm']]){
    await page.locator('#physics-tab-'+model).click();
    assert.equal(await page.locator('#pred-10').textContent(),'8.00 mm');
    assert.equal(await page.locator('#pred-20').textContent(),at20);
    assert.equal(await page.locator('#pred-30').textContent(),at30);
  }
  assert.equal(await page.locator('#ringdown-plot circle').count(),4);
  await page.locator('#amplitude').fill('24');
  for(const [model,at10] of [['viscous','16.00 mm'],['coulomb','20.00 mm'],['quadratic','12.00 mm']]){
    await page.locator('#physics-tab-'+model).click();
    assert.equal(await page.locator('#pred-10').textContent(),at10);
    assert.equal(await page.locator('#ringdown-plot circle').count(),0);
    assert.match(await page.locator('#prediction-summary').textContent(),/no observations/);
  }
  await page.locator('#reset-amplitude').click();
  assert.equal(await page.locator('#amplitude').inputValue(),'12');
  assert.equal(await page.locator('#ringdown-plot circle').count(),4);
  await page.locator('#physics-tab-viscous').click();
  await page.evaluate(()=>scrollTo(0,0));
  await page.locator('#toast').waitFor({state:'hidden'});
  await page.screenshot({path:'/tmp/abducer-tutorial-hero.png'});
  await page.screenshot({path:'/tmp/abducer-tutorial-desktop.png',fullPage:true});
  await page.setViewportSize({width:390,height:844});
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  await page.screenshot({path:'/tmp/abducer-tutorial-mobile.png',fullPage:true});
  const head=await page.request.head(url+'/tutorial');assert.equal(head.status(),200);assert.equal((await head.body()).length,0);
  const profile=await page.evaluate(async()=>{const r=await fetch('/api',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:'get_profile',arguments:{}})});return (await r.json()).structuredContent;});
  assert.equal(profile.tutorial_url,origin+'/tutorial');
  assert.deepEqual(errors,[]);
  console.log(JSON.stringify({passed:true,nodes,persistent_note:true,source_pagination:true,mobile_width:390,generated_worker:resolve(workerPath)}));
} finally {await browser.close();server.close();sqlite.close();}
