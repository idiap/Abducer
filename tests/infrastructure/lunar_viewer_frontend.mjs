// SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
//
// SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
// Neuro-symbolic AI Group
//
// SPDX-License-Identifier: MIT
// Exercise Lunar's actual browser-side bundle validator and graph layout.
// Usage: node tests/infrastructure/lunar_viewer_frontend.mjs LUNAR_ROOT BUNDLE_JSON
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const [lunarRoot, bundleFile] = process.argv.slice(2);
assert(lunarRoot && bundleFile, 'Pass the explicit Lunar checkout and exported bundle');
const viewer = await import(pathToFileURL(path.resolve(lunarRoot, 'app/frontend/src/lib/prism-viewer.js')));
const bundle = viewer.validatePrismBundle(JSON.parse(fs.readFileSync(bundleFile, 'utf8')));
assert.equal(bundle.projects.length, 1);
assert.equal(bundle.projects[0].id, 'abducer-prism');
let occurrences = 0;
let authoredExamples = 0;
let browserSources = 0;
for (const workflow of bundle.projects[0].workflows) {
  const layout = viewer.layoutComplexGraph(workflow);
  assert(layout.nodes.length > 0, `${workflow.id}: no rendered nodes`);
  const ids = new Set(layout.nodes.map(n => n.id));
  for (const node of layout.nodes) {
    assert(Number.isFinite(node.position.x) && Number.isFinite(node.position.y));
  }
  for (const edge of layout.edges) {
    assert(ids.has(edge.source) && ids.has(edge.target), `${workflow.id}: dangling layout edge`);
  }
  const sources = viewer.workflowSources(workflow);
  assert(sources.some(s => s.path === 'reasoning.prism'));
  assert(sources.some(s => s.path === 'sample_outputs.prism'));
  viewer.prismFileNavigationIndex(sources);
  browserSources += sources.length;
  for (const node of workflow.graph.nodes.filter(n => n.kind === 'occurrence')) {
    occurrences += 1;
    assert(node.input_type && node.output_type, `${workflow.id}/${node.id}: untyped occurrence`);
    assert(node.output_example, `${workflow.id}/${node.id}: missing authored example`);
    authoredExamples += 1;
    viewer.mainLabel(node);
    viewer.searchable(node);
  }
}
const relations = viewer.projectRelations(bundle.projects[0]);
for (const relation of relations) viewer.workflowRelationshipSemantics(relation, relation.source);
assert.equal(bundle.projects[0].workflows.length, 19);
console.log(JSON.stringify({status: 'pass', frontend: 'Lunar prism-viewer.js',
  projects: bundle.projects.length, visible_workflows: bundle.projects[0].workflows.length,
  occurrences, authored_examples: authoredExamples, browser_sources: browserSources,
  atlas_relations: relations.length}, null, 2));
