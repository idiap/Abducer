// SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
//
// SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
// Neuro-symbolic AI Group
//
// SPDX-License-Identifier: MIT
// Validate the actual Lunar HTML admission code against the original YM report.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash, webcrypto } from 'node:crypto';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const [lunar, htmlPath] = process.argv.slice(2);
assert(lunar && htmlPath, 'Pass LUNAR_ROOT and HTML_REPORT');
globalThis.crypto ??= webcrypto;
const { nativeHtmlReport, verifiedHtmlDocument } = await import(pathToFileURL(resolve(lunar, 'app/frontend/src/lib/prism-runs.js')));
const document = readFileSync(htmlPath, 'utf8');
const sha256 = createHash('sha256').update(document).digest('hex');
const report = { path: 'full_timeline.html', sha256, media_type: 'text/html' };
const output = { structured_value: { html_report: report } };
const run = { id: 'run-test', artifacts: [{ safe_locator: report.path, content_digest: `sha256:${sha256}`,
  media_type: 'text/html', url: '/api/prism/runs/run-test/artifacts/artifact-test' }] };
assert.equal(nativeHtmlReport(run, output).url, run.artifacts[0].url);
const framed = await verifiedHtmlDocument(document, sha256);
assert(framed.includes('id="marathon-data"'));
assert(framed.includes("connect-src 'none'"));
assert(framed.includes('data-embedded-dependency="mathjax-tex-svg"'));
await assert.rejects(verifiedHtmlDocument(document + 'tampered', sha256), /integrity/);
for (const changes of [{ content_digest: 'sha256:' + '0'.repeat(64) }, { media_type: 'text/plain' },
  { url: 'https://attacker.invalid/report' }, { url: '/api/prism/runs/other-run/artifacts/other' }]) {
  assert.throws(() => nativeHtmlReport({ ...run, artifacts: [{ ...run.artifacts[0], ...changes }] }, output), /inventory/);
}
assert.equal(nativeHtmlReport(run, { structured_value: {} }), null);
console.log(JSON.stringify({ status: 'pass', sha256, source_bytes: Buffer.byteLength(document),
  renderer: 'original HTML', tamper_and_cross_run_checks: 'passed' }));
