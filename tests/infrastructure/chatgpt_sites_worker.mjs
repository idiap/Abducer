// SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
// SPDX-License-Identifier: MIT
// Exercise the real Sites adapter with a real SQLite database behind a D1 shim.
// Usage: node tests/infrastructure/chatgpt_sites_worker.mjs LIBRARY.json
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {DatabaseSync} from 'node:sqlite';
import {test} from 'node:test';
import {createWorker} from '../../integrations/chatgpt/sites/worker.mjs';

const library = JSON.parse(await readFile(process.argv[2] || '/tmp/abducer-sites-library.json', 'utf8'));
const migration = await readFile(new URL('../../integrations/chatgpt/sites/schema.sql', import.meta.url), 'utf8');
const origin = 'https://abducer.test';
const html = '<!doctype html><title>Abducer Explorer test</title>';
const worker = createWorker(library, html, origin);
let sequence = 0;

function database() {
  const sqlite = new DatabaseSync(':memory:');
  sqlite.exec(migration);
  return {
    sqlite,
    DB: {prepare(sql) {
      return {bind(...args) {
        const statement = sqlite.prepare(sql);
        return {
          async first() {return statement.get(...args) || null;},
          async all() {return {results: statement.all(...args)};},
          async run() {return {meta: statement.run(...args)};}
        };
      }};
    }}
  };
}

async function rpc(method, params = {}, {user = 'alice', env = {}, requestOrigin, body} = {}) {
  const headers = {'Content-Type': 'application/json'};
  if (user) headers['oai-authenticated-user-id'] = user;
  if (requestOrigin) headers.Origin = requestOrigin;
  const response = await worker.fetch(new Request(origin + '/mcp', {
    method: 'POST', headers,
    body: body ?? JSON.stringify({jsonrpc:'2.0', id: ++sequence, method, params})
  }), env);
  return {response, data: await response.json()};
}

async function call(name, args = {}, options = {}) {
  const {response, data} = await rpc('tools/call', {name, arguments: args}, options);
  assert.equal(response.status, 200);
  return data.result;
}

function successful(result) {
  assert.equal(result.isError, false, JSON.stringify(result));
  assert.deepEqual(JSON.parse(result.content[0].text), result.structuredContent);
  return result.structuredContent;
}

function errorCode(result) {
  assert.equal(result.isError, true);
  return JSON.parse(result.content[0].text).error.code;
}

test('MCP discovery advertises actual tools, UI and explicit runtime limits', async () => {
  const discovery = (await rpc('server/discover', {}, {user:null})).data.result;
  assert.ok(discovery.supportedVersions.includes('2026-07-28'));
  assert.match(discovery.instructions, /Native Python jobs are unavailable/);
  const tools = (await rpc('tools/list', {}, {user:null})).data.result.tools;
  assert.equal(new Set(tools.map(t => t.name)).size, tools.length);
  assert.equal(tools.some(t => t.name === 'start_research_run'), false);
  assert.equal(tools.find(t => t.name === 'save_project_note').annotations.readOnlyHint, false);
  const ui = tools.find(t => t.name === 'open_explorer')._meta.ui.resourceUri;
  const resource = (await rpc('resources/read', {uri:ui})).data.result.contents[0];
  assert.equal(resource.text, html);
  assert.equal(resource.mimeType, 'text/html;profile=mcp-app');
  const profile = successful(await call('get_profile'));
  assert.equal(profile.release, library.release);
  assert.deepEqual(profile.counts, {skills:221, workflows:34, graphs:19});
  assert.equal(profile.capabilities.native_execution, false);
});

test('tool calls require authenticated Sites identity even for catalog reads', async () => {
  for (const name of ['get_profile', 'list_workflows', 'list_projects']) {
    assert.equal(errorCode(await call(name, {}, {user:null})), 'unauthenticated');
  }
});

test('canonical skill pagination exactly reconstructs original instructions and hash', async () => {
  const skill = [...library.skills].sort((a,b) => b.content.length - a.content.length)[0];
  let offset = 0, text = '';
  while (offset !== null) {
    const page = successful(await call('get_skill', {name:skill.name, offset, limit:313}));
    assert.equal(page.sha256, skill.sha256);
    assert.equal(page.path, skill.path);
    assert.equal(page.offset, offset);
    assert.equal(page.total_chars, skill.content.length);
    text += page.content;
    offset = page.next_offset;
  }
  assert.equal(text, skill.content);
  const eof = successful(await call('get_skill', {name:skill.name, offset:skill.content.length}));
  assert.equal(eof.content, '');
  assert.equal(eof.next_offset, null);
  assert.equal(errorCode(await call('get_skill', {name:skill.name, offset:skill.content.length + 1})), 'invalid_request');
});

test('workflow graph and paginated source remain source-faithful', async () => {
  const row = library.workflows.find(w => w.graph && w.viewer?.source_text);
  const actual = successful(await call('get_workflow', {workflow_id:row.id}));
  assert.deepEqual(actual.workflow.graph, row.graph);
  assert.equal(actual.workflow.execution_status, 'inspectable');
  assert.equal(actual.owner_skill, library.skills.find(s => s.path === row.owner)?.name || null);
  let offset = 0, source = '';
  while (offset !== null) {
    const page = successful(await call('get_workflow_source', {workflow_id:row.id, offset, limit:1001}));
    source += page.content;
    offset = page.next_offset;
  }
  assert.equal(source, row.viewer.source_text);
  assert.equal(errorCode(await call('get_workflow_source', {workflow_id:row.id, format:'shell'})), 'invalid_request');
});

test('skill search is bounded and never returns full instruction bodies', async () => {
  const first = successful(await call('search_skills', {limit:5}));
  assert.equal(first.skills.length, 5);
  assert.equal(first.total, 221);
  assert.equal(first.next_offset, 5);
  assert.ok(first.skills.every(s => !Object.hasOwn(s, 'content')));
  const second = successful(await call('search_skills', {offset:5, limit:5}));
  assert.equal(second.skills[0].name, library.skills[5].name);
  for (const args of [{limit:101}, {offset:-1}, {query:5}, {query:'x'.repeat(1001)}]) {
    assert.equal(errorCode(await call('search_skills', args)), 'invalid_request');
  }
});

test('real SQL stores only owned projects and rejects cross-user reads and writes', async () => {
  const env = database();
  try {
    const created = successful(await call('create_project', {title:'Question', question:'How does this follow?'}, {env})).project;
    assert.equal(created.revision, 1);
    assert.equal(Object.hasOwn(created, 'owner_id'), false);
    assert.equal(successful(await call('list_projects', {}, {env})).projects.length, 1);
    assert.deepEqual(successful(await call('list_projects', {}, {env,user:'bob'})).projects, []);
    assert.equal(errorCode(await call('get_project', {project_id:created.id}, {env,user:'bob'})), 'not_found');
    assert.equal(errorCode(await call('save_project_note', {project_id:created.id, note:'malicious', expected_revision:1}, {env,user:'bob'})), 'not_found');
    assert.equal(errorCode(await call('get_project', {project_id:"' OR 1=1 --"}, {env,user:'bob'})), 'not_found');
    const stored = successful(await call('get_project', {project_id:created.id}, {env})).project;
    assert.equal(stored.revision, 1);
    assert.deepEqual(stored.notes, []);
  } finally {env.sqlite.close();}
});

test('optimistic revisions allow one concurrent note and reject stale overwrites', async () => {
  const env = database();
  try {
    const p = successful(await call('create_project', {title:'Revision', question:'Test concurrent updates'}, {env})).project;
    const args = {project_id:p.id, expected_revision:1};
    const results = await Promise.all([
      call('save_project_note', {...args, note:'First hypothesis'}, {env}),
      call('save_project_note', {...args, note:'Second hypothesis'}, {env})
    ]);
    assert.equal(results.filter(r => !r.isError).length, 1);
    assert.equal(errorCode(results.find(r => r.isError)), 'revision_conflict');
    const stored = successful(await call('get_project', {project_id:p.id}, {env})).project;
    assert.equal(stored.revision, 2);
    assert.equal(stored.notes.length, 1);
    assert.equal(stored.notes[0].scientific_truth_verified, false);
    assert.equal(errorCode(await call('save_project_note', {...args, note:'stale replacement'}, {env})), 'revision_conflict');
  } finally {env.sqlite.close();}
});

test('a prepared plan grants no execution or scientific authority and does not mutate projects', async () => {
  const env = database();
  try {
    const p = successful(await call('create_project', {title:'Plan', question:'What explains the observation?'}, {env})).project;
    const workflow = library.workflows.find(w => library.skills.some(s => s.path === w.owner));
    const planned = successful(await call('prepare_research_plan', {project_id:p.id, workflow_id:workflow.id}, {env})).plan;
    assert.equal(planned.execution, 'ChatGPT-guided');
    assert.equal(planned.limits.native_execution, false);
    assert.equal(planned.limits.scientific_truth_verified, false);
    assert.equal(planned.release, library.release);
    assert.equal(planned.skill_names[0], library.skills.find(s => s.path === workflow.owner).name);
    assert.deepEqual(successful(await call('get_project', {project_id:p.id}, {env})).project, p);
    assert.equal(errorCode(await call('prepare_research_plan', {project_id:p.id, workflow_id:workflow.id}, {env,user:'bob'})), 'not_found');
  } finally {env.sqlite.close();}
});

test('input bounds and unexpected arguments reject before writing records', async () => {
  const env = database();
  try {
    for (const args of [
      {title:'x'.repeat(201), question:'ok'},
      {title:'ok', question:'x'.repeat(8001)},
      {title:'ok', question:'ok', owner_id:'bob'},
      {title:'  ', question:'ok'},
      {title:'Missing question'}
    ]) assert.equal(errorCode(await call('create_project', args, {env})), 'invalid_request');
    assert.deepEqual(successful(await call('list_projects', {}, {env})).projects, []);
    assert.equal(errorCode(await call('list_projects')), 'storage_unavailable');
    const oversized = await rpc('ping', {}, {body:'x'.repeat(65537)});
    assert.equal(oversized.response.status, 400);
  } finally {env.sqlite.close();}
});

test('hostile origins and cross-origin browser writes are refused', async () => {
  assert.equal((await rpc('tools/list', {}, {requestOrigin:'https://evil.test'})).response.status, 403);
  assert.equal((await rpc('tools/list', {}, {requestOrigin:'https://chatgpt.com'})).response.status, 200);
  for (const requestOrigin of [undefined, 'https://evil.test', 'https://chatgpt.com']) {
    const headers = {'Content-Type':'application/json', 'oai-authenticated-user-id':'alice'};
    if (requestOrigin) headers.Origin = requestOrigin;
    const response = await worker.fetch(new Request(origin + '/api', {method:'POST',headers,body:JSON.stringify({name:'get_profile'})}));
    assert.equal(response.status, 403);
  }
  const response = await worker.fetch(new Request(origin + '/api', {method:'POST',headers:{'Content-Type':'application/json',Origin:origin,'oai-authenticated-user-id':'alice'},body:JSON.stringify({name:'get_profile'})}));
  assert.equal(response.status, 200);
  assert.equal(successful(await response.json()).name, 'Abducer');
});

test('per-user project and per-project note quotas are enforced without partial writes', async () => {
  const env = database();
  try {
    const statement = env.sqlite.prepare("INSERT INTO projects (id,owner_id,title,question,revision,notes,created_at,updated_at) VALUES (?,?,'Quota','Bounded',1,'[]','2026-10-25','2026-10-25')");
    for (let index=0; index<100; index++) statement.run('project-'+index, 'alice');
    assert.equal(errorCode(await call('create_project', {title:'Overflow', question:'Must reject'}, {env})), 'quota_exceeded');
    assert.equal(env.sqlite.prepare('SELECT count(*) AS count FROM projects').get().count, 100);
    successful(await call('create_project', {title:'Independent quota', question:'Bob may create'}, {env,user:'bob'}));
    const notes = Array.from({length:100}, (_,index) => ({id:String(index), text:'Existing note', scientific_truth_verified:false}));
    env.sqlite.prepare('UPDATE projects SET notes = ? WHERE id = ?').run(JSON.stringify(notes), 'project-0');
    assert.equal(errorCode(await call('save_project_note', {project_id:'project-0', note:'Overflow note', expected_revision:1}, {env})), 'quota_exceeded');
    const stored = env.sqlite.prepare('SELECT notes, revision FROM projects WHERE id = ?').get('project-0');
    assert.deepEqual(JSON.parse(stored.notes), notes);
    assert.equal(stored.revision, 1);
  } finally {env.sqlite.close();}
});

test('aggregate note budget rejects a valid-sized note without altering previous data', async () => {
  const env = database();
  try {
    const p = successful(await call('create_project', {title:'Aggregate budget', question:'Bound the complete note collection'}, {env})).project;
    const notes = [{id:'existing', text:'x'.repeat(47000), scientific_truth_verified:false}];
    env.sqlite.prepare('UPDATE projects SET notes = ? WHERE id = ?').run(JSON.stringify(notes), p.id);
    assert.equal(errorCode(await call('save_project_note', {project_id:p.id, note:'x'.repeat(2000), expected_revision:1}, {env})), 'quota_exceeded');
    const stored = env.sqlite.prepare('SELECT notes, revision FROM projects WHERE id = ?').get(p.id);
    assert.deepEqual(JSON.parse(stored.notes), notes);
    assert.equal(stored.revision, 1);
  } finally {env.sqlite.close();}
});

test('browser API rejects null and array envelopes as invalid requests', async () => {
  for (const body of ['null', '[]']) {
    const response = await worker.fetch(new Request(origin + '/api', {
      method:'POST', body,
      headers:{'Content-Type':'application/json', Origin:origin, 'oai-authenticated-user-id':'alice'}
    }));
    assert.equal(response.status, 400);
    assert.equal(errorCode(await response.json()), 'invalid_request');
  }
});
