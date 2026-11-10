// SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
// SPDX-License-Identifier: MIT
// Server-only bridge. Build concatenates this module with the Sites Worker;
// browser code and tool arguments never receive the shared signing key.
const nativeBridgeString = maxLength => ({type:'string',minLength:1,maxLength});
const nativeBridgeSchema = (properties={},required=[]) => ({type:'object',properties,required,additionalProperties:false});
const nativeBridgeTool = (name,description,properties={},required=[],write=false) => ({
  name,description,inputSchema:nativeBridgeSchema(properties,required),
  annotations:{readOnlyHint:!write,destructiveHint:false,idempotentHint:!write,openWorldHint:write}
});
export const nativeBridgeDefinitions = [
  nativeBridgeTool('get_execution_capabilities','Read the authenticated native backend readiness and qualified workflows; connection alone does not mean execution is available.'),
  nativeBridgeTool('get_workflow_dependencies','Read a page of declared native workflow dependencies and unresolved references.',{workflow_id:nativeBridgeString(160),offset:{type:'integer',minimum:0},limit:{type:'integer',minimum:1,maximum:100}},['workflow_id']),
  nativeBridgeTool('get_workflow_dependency_source','Read an exact bounded source file admitted by the selected workflow dependency manifest.',{workflow_id:nativeBridgeString(160),path:nativeBridgeString(1000),offset:{type:'integer',minimum:0},limit:{type:'integer',minimum:1,maximum:16000}},['workflow_id','path']),
  nativeBridgeTool('validate_hypothesis_map','Run the canonical conceptual hypothesis-map validator for an owned project. This validates a supplied artifact and does not execute the entire scientific workflow or establish scientific truth.',{project_id:nativeBridgeString(80),content:nativeBridgeString(48000)},['project_id','content'],true),
  nativeBridgeTool('get_validation_receipt','Retrieve an existing native conceptual validation receipt for an owned project without running the validator again.',{project_id:nativeBridgeString(80),receipt_id:nativeBridgeString(32)},['project_id','receipt_id']),
  nativeBridgeTool('list_validation_receipts','List bounded receipt identities, statuses, timestamps and submitted-artifact hashes for an owned project; use these to recover a lost validation response.',{project_id:nativeBridgeString(80),limit:{type:'integer',minimum:1,maximum:50,default:20}},['project_id']),
  nativeBridgeTool('prepare_research_run','Prepare a bounded native research plan for an owned Sites project. Does not start model work.',{
    project_id:nativeBridgeString(80),workflow_id:nativeBridgeString(160),inputs:{type:'object'},
    budget_seconds:{type:'integer',minimum:1,maximum:7200},max_model_calls:{type:'integer',minimum:1,maximum:50},max_output_tokens:{type:'integer',minimum:1,maximum:32000}
  },['project_id','workflow_id','inputs'],true),
  {...nativeBridgeTool('start_research_run','Start the reviewed native plan within its declared budget. Reuse the same idempotency key only to recover this exact start.',{plan_id:nativeBridgeString(160),idempotency_key:nativeBridgeString(128)},['plan_id','idempotency_key'],true),annotations:{readOnlyHint:false,destructiveHint:false,idempotentHint:true,openWorldHint:true}},
  nativeBridgeTool('get_run_status','Read an owned native run and its recorded outcome.',{job_id:nativeBridgeString(160)},['job_id']),
  nativeBridgeTool('get_pending_model_request','Read one page of an owned native model request awaiting this ChatGPT conversation. Read all pages, preserve the original messages/schema, then submit the actual JSON response.',{job_id:nativeBridgeString(160),offset:{type:'integer',minimum:0},limit:{type:'integer',minimum:1,maximum:16000}},['job_id']),
  {...nativeBridgeTool('submit_model_response','Submit this conversation’s JSON response to an owned pending native model request. Schema acceptance does not establish scientific truth; retry only identical content.',{job_id:nativeBridgeString(160),request_id:nativeBridgeString(160),content:nativeBridgeString(393216)},['job_id','request_id','content'],true),annotations:{readOnlyHint:false,destructiveHint:false,idempotentHint:true,openWorldHint:false}},
  nativeBridgeTool('list_runs','List native runs bound to an owned Sites project.',{project_id:nativeBridgeString(80),limit:{type:'integer',minimum:1,maximum:100}},['project_id']),
  nativeBridgeTool('list_run_artifacts','List verified artifacts belonging to an accessible native run.',{job_id:nativeBridgeString(160)},['job_id']),
  nativeBridgeTool('get_report','Read a bounded, digest-verified native artifact excerpt.',{job_id:nativeBridgeString(160),artifact_id:nativeBridgeString(160),offset:{type:'integer',minimum:0},length:{type:'integer',minimum:1,maximum:65536}},['job_id','artifact_id']),
  nativeBridgeTool('cancel_run','Request cancellation of an owned native run; actual termination is reported by its recorded status.',{job_id:nativeBridgeString(160)},['job_id'],true)
];

const nativeBridgeHex = bytes => [...new Uint8Array(bytes)].map(value=>value.toString(16).padStart(2,'0')).join('');
const nativeBridgeFail = (message,code='native_unavailable') => {throw Object.assign(new Error(message),{code});};
const nativeBridgeDefinitionMap = new Map(nativeBridgeDefinitions.map(item=>[item.name,item]));

export function nativeBridgeConfigured(env={}) {
  return !!(env.ABDUCER_NATIVE_BRIDGE_URL && env.ABDUCER_NATIVE_BRIDGE_KEY && env.ABDUCER_NATIVE_BRIDGE_AUDIENCE);
}

export function createNativeBridge({fetchImpl=fetch,cryptoImpl=crypto,now=Date.now}={}) {
  return {
    definitions:nativeBridgeDefinitions,
    configured:nativeBridgeConfigured,
    async call(operation,args,request,env,{owned}={}) {
      const definition=nativeBridgeDefinitionMap.get(operation);
      if(!definition||!args||Array.isArray(args)||typeof args!=='object')nativeBridgeFail('Invalid native operation','invalid_request');
      const schema=definition.inputSchema;
      if(Object.keys(args).some(key=>!Object.hasOwn(schema.properties,key))||schema.required.some(key=>!Object.hasOwn(args,key)))nativeBridgeFail('Invalid native arguments','invalid_request');
      const principal=request.headers.get('oai-authenticated-user-id');
      if(!principal||principal.length>512)nativeBridgeFail('Signed-in Sites identity required','unauthenticated');
      if(!nativeBridgeConfigured(env))nativeBridgeFail('Native execution bridge is not configured');
      const keyHex=env.ABDUCER_NATIVE_BRIDGE_KEY,audience=env.ABDUCER_NATIVE_BRIDGE_AUDIENCE;
      if(typeof keyHex!=='string'||!/^[a-fA-F0-9]{64}$/.test(keyHex)||typeof audience!=='string'||!audience.trim()||audience.length>200)nativeBridgeFail('Native bridge configuration is invalid');
      let endpoint;
      try {
        endpoint=new URL(env.ABDUCER_NATIVE_BRIDGE_URL);
        if(endpoint.protocol!=='https:'||endpoint.username||endpoint.password||endpoint.search||endpoint.hash||!['/','/bridge/v1/call'].includes(endpoint.pathname))throw Error();
        endpoint.pathname='/bridge/v1/call';
      } catch {nativeBridgeFail('Native bridge URL must be an HTTPS service endpoint');}
      const payload={...args};
      // Ownership is obtained from the Sites database, never asserted by the
      // model. The backend maintains its own separate membership check as well.
      if(['prepare_research_run','list_runs','validate_hypothesis_map','get_validation_receipt','list_validation_receipts'].includes(operation)) {
        if(typeof owned!=='function')nativeBridgeFail('Project ownership verifier is unavailable');
        const project=await owned(env,principal,args.project_id);
        payload.project_id=project.id;payload.title=project.title;
      }
      const encoder=new TextEncoder();
      const body=JSON.stringify({version:1,audience,principal,operation,arguments:payload});
      const bytes=encoder.encode(body);
      if(bytes.length>(operation==='submit_model_response'?1048576:65536))nativeBridgeFail('Native request exceeds its bounded body limit','invalid_request');
      const timestamp=String(Math.floor(now()/1000));
      const nonce=nativeBridgeHex(cryptoImpl.getRandomValues(new Uint8Array(16)));
      const digest=nativeBridgeHex(await cryptoImpl.subtle.digest('SHA-256',bytes));
      const message=['abducer-bridge-v1','POST','/bridge/v1/call',audience,timestamp,nonce,digest].join('\n');
      const keyBytes=Uint8Array.from(keyHex.match(/../g),pair=>parseInt(pair,16));
      const key=await cryptoImpl.subtle.importKey('raw',keyBytes,{name:'HMAC',hash:'SHA-256'},false,['sign']);
      const signature=nativeBridgeHex(await cryptoImpl.subtle.sign('HMAC',key,encoder.encode(message)));
      let response;
      try {
        // workerd does not implement redirect:'error'. Manual mode plus an
        // explicit rejection preserves the no-forwarding boundary on Workers.
        response=await fetchImpl(endpoint.href,{method:'POST',headers:{'Content-Type':'application/json','X-Abducer-Timestamp':timestamp,'X-Abducer-Nonce':nonce,'X-Abducer-Signature':signature},body,redirect:'manual',signal:AbortSignal.timeout(30000)});
      } catch(error) {
        // Log the transport category only: no request, headers, body or secrets.
        console.error('native_transport_failure',JSON.stringify({name:String(error?.name||'Error').slice(0,60)}));
        nativeBridgeFail('Native backend could not be reached; check its recorded state before retrying a start');
      }
      if(response.status>=300&&response.status<400){await response.body?.cancel();nativeBridgeFail('Native backend redirects are disabled');}
      if(!response.headers.get('Content-Type')?.toLowerCase().startsWith('application/json'))nativeBridgeFail('Native backend returned an invalid response');
      const reader=response.body?.getReader();if(!reader)nativeBridgeFail('Native backend returned an empty response');
      let total=0;const chunks=[];
      while(true){const {value,done}=await reader.read();if(done)break;total+=value.length;if(total>524288){await reader.cancel();nativeBridgeFail('Native response exceeds bounded size');}chunks.push(value);}
      const joined=new Uint8Array(total);let offset=0;for(const chunk of chunks){joined.set(chunk,offset);offset+=chunk.length;}
      let decoded;
      try{decoded=JSON.parse(new TextDecoder().decode(joined));}catch{nativeBridgeFail('Native backend returned invalid JSON');}
      if(decoded?.error){const error=decoded.error;nativeBridgeFail(typeof error.message==='string'?error.message.slice(0,400):'Native request was rejected',typeof error.code==='string'&&/^[a-z_]{1,60}$/.test(error.code)?error.code:'native_unavailable');}
      if(!response.ok||!decoded||Array.isArray(decoded)||!Object.hasOwn(decoded,'result'))nativeBridgeFail('Native backend returned an invalid result');
      return decoded.result;
    }
  };
}
