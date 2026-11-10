// SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
// SPDX-License-Identifier: MIT
// Reuse the original scientific renderer. This helper only admits complete,
// digest-bound documents and mounts them in a separate opaque-origin frame.
(() => {
  const PAGE = 65536, MAX_BYTES = 64 * 1024 * 1024;
  const encoder = new TextEncoder();
  const sha256 = async bytes => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', bytes)), b => b.toString(16).padStart(2, '0')).join('');
  const policy = "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; font-src data:; media-src data:; connect-src 'none'; frame-src 'none'; worker-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'";

  async function load({call, jobId, artifact, isCurrent = () => true, progress = () => {}}) {
    if (!artifact?.id || artifact.media_type !== 'text/html' || !/^[a-f0-9]{64}$/.test(artifact.sha256)) throw Error('This run has no verified HTML artifact.');
    const parts = [];
    let total = null, received = 0, bytes = 0, aborted = false;
    async function page(offset) {
      if (aborted || !isCurrent()) throw Error('Report selection changed.');
      const value = await call('get_report', {job_id: jobId, artifact_id: artifact.id, offset, length: PAGE});
      if (aborted || !isCurrent()) throw Error('Report selection changed.');
      const text = value.text;
      if (value.job_id !== jobId || value.artifact_id !== artifact.id || value.sha256 !== artifact.sha256 || value.media_type !== 'text/html' || value.offset !== offset || typeof text !== 'string' || !Number.isSafeInteger(value.total_characters) || value.total_characters < 1 || value.total_characters > MAX_BYTES) throw Error('Report identity or range verification failed.');
      if (total === null) total = value.total_characters;
      if (value.total_characters !== total) throw Error('Report changed during download.');
      // Python offsets count Unicode code points, not JavaScript UTF-16 units.
      const count = Array.from(text).length, end = Math.min(offset + PAGE, total);
      if (count !== end - offset || value.next_offset !== (end < total ? end : null)) throw Error('Report is truncated or has an invalid next page.');
      bytes += encoder.encode(text).length;
      if (bytes > MAX_BYTES) throw Error('HTML report exceeds the 64 MiB display limit.');
      parts[offset / PAGE] = text;
      received += count;
      progress(received, total);
    }
    await page(0);
    // Four bounded reads keep large timeline reports usable without an
    // unbounded burst of calls. Selection changes stop scheduling new pages.
    let next = PAGE;
    try {
      await Promise.all(Array.from({length: Math.min(4, Math.ceil(total / PAGE) - 1)}, async () => {
        while (next < total) { const offset = next; next += PAGE; await page(offset); }
      }));
    } catch (error) {
      // Drain already issued reads without allowing progress from a failed
      // download to overwrite its error or schedule the rest of the document.
      aborted = true;
      throw error;
    }
    const text = parts.join(''), raw = encoder.encode(text);
    if (await sha256(raw) !== artifact.sha256) throw Error('Report integrity check failed; HTML was not opened.');
    if (!isCurrent()) throw Error('Report selection changed.');
    return {text, raw};
  }

  function mount({container, call, jobId, artifact, isCurrent = () => true}) {
    const controls = document.createElement('div');
    controls.className = 'reasoning-html-controls';
    const open = document.createElement('button');
    open.type = 'button'; open.textContent = 'Open reasoning HTML';
    const status = document.createElement('p'); status.setAttribute('role', 'status');
    const holder = document.createElement('div');
    controls.append(open, status, holder); container.append(controls);
    let alive = true, downloadUrl = null;
    const current = () => alive && isCurrent();
    open.onclick = async () => {
      open.disabled = true; status.textContent = 'Loading the complete report…';
      try {
        const result = await load({call, jobId, artifact, isCurrent: current, progress: (done, total) => { if (current()) status.textContent = 'Loading reasoning HTML · ' + Math.floor(100 * done / total) + '%'; }});
        if (!current()) return;
        const frame = document.createElement('iframe');
        frame.title = 'Run reasoning report'; frame.setAttribute('sandbox', 'allow-scripts');
        frame.setAttribute('referrerpolicy', 'no-referrer');
        frame.style.cssText = 'display:block;width:100%;height:75vh;min-height:480px;border:1px solid #dce2d5;background:white;margin-top:12px';
        // The policy is parsed before ANY report markup. No same-origin,
        // navigation, popup or form sandbox permissions are granted.
        frame.srcdoc = '<!doctype html><meta http-equiv="Content-Security-Policy" content="' + policy + '">' + result.text;
        const download = document.createElement('a');
        downloadUrl = URL.createObjectURL(new Blob([result.raw], {type: 'text/html;charset=utf-8'}));
        download.href = downloadUrl;
        download.download = (artifact.name || 'reasoning-report.html').split(/[\\/]/).pop();
        if (!download.download.endsWith('.html')) download.download += '.html';
        download.textContent = 'Download original HTML';
        holder.replaceChildren(download, frame);
        open.hidden = true;
        status.textContent = 'Complete report · SHA-256 verified. The recorded scientific outcome remains unchanged.';
      } catch (error) {
        if (current()) { status.textContent = error.message; open.disabled = false; }
      }
    };
    return () => { alive = false; if (downloadUrl) URL.revokeObjectURL(downloadUrl); controls.remove(); };
  }
  globalThis.AbducerReports = {load, mount};
})();
