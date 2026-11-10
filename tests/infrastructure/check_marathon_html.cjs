// SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
//
// SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
// Neuro-symbolic AI Group
//
// SPDX-License-Identifier: MIT
/* Check generated HTML with a real DOM implementation; no network is enabled.
 * Use an installed jsdom via NODE_PATH. Visual checks remain a separate step.
 */
const fs = require('node:fs');
const assert = require('node:assert/strict');
const path = require('node:path');
const {JSDOM} = require('jsdom');

const [reportDir, referenceDir] = process.argv.slice(2);
assert(reportDir && referenceDir, 'Pass report and reference directories');
const result = {};
for (const name of ['latest.html', 'full_timeline.html']) {
  const raw = fs.readFileSync(path.join(reportDir, name), 'utf8');
  const dom = new JSDOM(raw, {runScripts: 'outside-only'});
  const doc = dom.window.document;
  const tabs = [...doc.querySelectorAll('button[data-tab]')];
  const reference = new JSDOM(fs.readFileSync(path.join(referenceDir, name), 'utf8'));
  assert.deepEqual(tabs.map(x => x.dataset.tab), [...reference.window.document.querySelectorAll('button[data-tab]')].map(x => x.dataset.tab));
  const tabScript = [...doc.scripts].find(x => x.textContent.includes('function activateTab(tabName)'));
  assert(tabScript, 'Original tab handler is present');
  dom.window.eval(tabScript.textContent);
  doc.dispatchEvent(new dom.window.Event('DOMContentLoaded'));
  for (const tab of tabs) {
    tab.click();
    const visible = [...doc.querySelectorAll('[data-panel]')].filter(x => !x.hidden);
    assert.equal(visible.length, 1, 'Exactly one panel is visible');
    assert.equal(visible[0].dataset.panel, tab.dataset.tab);
    assert.equal(tab.getAttribute('aria-selected'), 'true');
  }
  const data = JSON.parse(doc.querySelector('#marathon-data').textContent);
  assert.equal(data.report.target_id, 'markov-kakutani-fixed-point-theorem-target');
  assert.equal(data.report.research_cycle_count, 1, 'A completed research cycle is required');
  assert.equal(data.target_literature_evolution.source_record_count, 18);
  assert.equal(data.target_literature_evolution.references.length, data.target_literature_evolution.unique_work_count);
  const copy = doc.body.cloneNode(true);
  copy.querySelectorAll('script,style').forEach(x => x.remove());
  assert(!/P vs NP|MCSP\/MKtP|hardness magnification|Wilson hairpin/.test(copy.textContent), 'No unrelated target prose');
  result[name] = {tabs: tabs.map(x => x.dataset.tab), tab_clicks_passed: tabs.length,
    research_cycles: data.report.research_cycle_count,
    references: data.target_literature_evolution.references.length,
    embedded_mathjax: raw.includes('MathJax')};
  dom.window.close();
  reference.window.close();
}
console.log(JSON.stringify({status: 'passed', files: result}, null, 2));
