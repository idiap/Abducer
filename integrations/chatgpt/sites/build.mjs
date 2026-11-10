// SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
// SPDX-License-Identifier: MIT
// Package only the verified public catalog and Sites adapter, never runtime data.
import {readFile,writeFile,mkdir,copyFile,access} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const root=dirname(fileURLToPath(import.meta.url));
const [libraryPath,destination,origin]=process.argv.slice(2);
if(!libraryPath||!destination)throw Error('Usage: node build.mjs LIBRARY_JSON SITE_CHECKOUT HTTPS_ORIGIN');
const library=JSON.parse(await readFile(resolve(libraryPath),'utf8'));
const manifestPath=resolve(destination,'.openai/hosting.json');
const manifest=JSON.parse(await readFile(manifestPath,'utf8'));
if(!manifest.project_id||!origin?.startsWith('https://')||new URL(origin).origin!==origin)throw Error('Registered project and expected origin required');
const worker=await readFile(resolve(root,'worker.mjs'),'utf8');
const nativeBridge=await readFile(resolve(root,'native_bridge.mjs'),'utf8');
const reportViewer=await readFile(resolve(root,'../ui/report_viewer.js'),'utf8');
const html=(await readFile(resolve(root,'explorer.html'),'utf8')).replace('<!-- ABDUCER_REPORT_VIEWER -->','<script>'+reportViewer+'</script>');
const tutorial=await readFile(resolve(root,'tutorial.html'),'utf8');
await mkdir(resolve(destination,'worker'),{recursive:true});
const output=nativeBridge+'\n'+worker+'\nexport default createWorker('+JSON.stringify(library)+','+JSON.stringify(html)+','+JSON.stringify(origin)+','+JSON.stringify(tutorial)+',createNativeBridge());\n';
await writeFile(resolve(destination,'worker/index.js'),output);
delete manifest.static;manifest.d1='DB';manifest.r2=null;manifest.capabilities=['mcp'];
await writeFile(manifestPath,JSON.stringify(manifest,null,2)+'\n');
await mkdir(resolve(destination,'drizzle/meta'),{recursive:true});
const sql=resolve(destination,'drizzle/0000_projects.sql');
try{await access(sql);}catch{await copyFile(resolve(root,'schema.sql'),sql);}
const journal=resolve(destination,'drizzle/meta/_journal.json');
try{await access(journal);}catch{await writeFile(journal,JSON.stringify({version:'7',dialect:'sqlite',entries:[{idx:0,version:'6',when:1792944000000,tag:'0000_projects',breakpoints:true}]},null,2)+'\n');}
console.log(JSON.stringify({release:library.release,worker_bytes:Buffer.byteLength(output),worker_sha256:createHash('sha256').update(output).digest('hex')}));
