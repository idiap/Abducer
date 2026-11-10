// SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
//
// SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
// Neuro-symbolic AI Group
//
// SPDX-License-Identifier: MIT
// Verify the exported registration using Lunar's actual Run-tab selection code.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const [lunar, manifestPath] = process.argv.slice(2);
assert(lunar && manifestPath, 'Usage: node lunar_runtime_frontend.mjs LUNAR_ROOT MANIFEST_JSON');
const library = (name) => import(pathToFileURL(resolve(lunar, 'app/frontend/src/lib', name)).href);
const { workflowExecutionOptions, canRunWorkflow } = await library('prism-runs.js');
const { schemaFormValidator, workflowInputSchema } = await library('schema-form.js');
const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
const options = workflowExecutionOptions('discovery_marathon_loop', manifest.runtime.workflows);
assert.equal(options.length, 1);
assert.deepEqual(options[0].modes, ['live']);
assert.equal(canRunWorkflow({ runnable: options[0], aiModelId: '' }), false);
assert.equal(canRunWorkflow({ runnable: options[0], aiModelId: 'owned-model' }), true);
assert.equal(options[0].execute_hook, 'abducer-execute');
assert.deepEqual(options[0].input_schema.required, ['target_id', 'run_id']);
const schema = workflowInputSchema(options[0]);
const runs = options[0].metadata.marathon_runs;
assert(runs.length > 0);
for (const run of runs) {
  assert(schemaFormValidator.isValid(schema, { target_id: run.target_id, run_id: run.run_id }, schema));
  assert(['blocked', 'requires_validation', 'initialization_available'].includes(run.readiness.status));
  for (const other of runs.filter((row) => row.target_id !== run.target_id)) {
    // The shared "new" sentinel is valid for every explicitly registered target.
    const exists = runs.some((row) => row.target_id === run.target_id && row.run_id === other.run_id);
    assert.equal(schemaFormValidator.isValid(schema, { target_id: run.target_id, run_id: other.run_id }, schema), exists);
  }
}
assert(!schemaFormValidator.isValid(schema, {}, schema));
assert.equal(options[0].metadata.execution_engine, 'python');
assert.equal(workflowExecutionOptions('theorem_proof_delivery', manifest.runtime.workflows).length, 0);
console.log(JSON.stringify({ status: 'pass', workflow: options[0].id, mode: 'live',
  required_input: 'selected target and run', selectable_runs: runs.length,
  model_required: true, runtime_preparation_required: true }, null, 2));
