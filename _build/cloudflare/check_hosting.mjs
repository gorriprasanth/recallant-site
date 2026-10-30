import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,unlinkSync,existsSync} from 'node:fs';
import {mkdtemp,rm,writeFile} from 'node:fs/promises';
import path from 'node:path';
import {tmpdir} from 'node:os';
import {createServer} from 'node:net';
import {spawn} from 'node:child_process';
import worker from './worker.mjs';
import {root,output,checkPackage} from './package.mjs';
import {checkRoutes,privatePaths} from './check_routes.mjs';

const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
const manifest=checkPackage();
const config=JSON.parse(readFileSync(path.join(root,'wrangler.jsonc'),'utf8'));
assert.equal(config.assets.directory,'.cloudflare/public');assert.equal(config.assets.run_worker_first,true);
assert.equal(config.assets.html_handling,'none');assert.equal(config.workers_dev,false);assert.equal(config.preview_urls,false);
assert.equal(config.env.preview.workers_dev,true);assert.equal(config.env.preview.vars.DEPLOYMENT_ENV,'preview');
const fixture=path.join(output,'private-upload-check.txt');
writeFileSync(fixture,'Local test marker; never upload.',{flag:'wx'});
try{assert.throws(()=>checkPackage(),/exact public allowlist/);}finally{unlinkSync(fixture);}

const assetRequests=[];
const assetBinding={async fetch(request){
 const pathname=new URL(request.url).pathname;assetRequests.push(pathname);
 const file=path.join(output,pathname.slice(1));
 if(!existsSync(file))return new Response('Private fallback must never be exposed.',{status:200});
 const type=pathname.endsWith('.html')?'text/html; charset=utf-8':'application/octet-stream';
 return new Response(request.method==='HEAD'?null:readFileSync(file),{headers:{'Content-Type':type}});
}};
const production={ASSETS:assetBinding,DEPLOYMENT_ENV:'production'};
const unitChecks=await checkRoutes({base:'https://recallant.com',manifest,fetcher:request=>worker.fetch(request,production)});
for(const path of privatePaths)assert.ok(!assetRequests.includes(path),'Private requests must never be forwarded to the asset binding');
for(const origin of ['http://recallant.com','http://www.recallant.com','https://www.recallant.com']){
 const response=await worker.fetch(new Request(origin+'/services.html?utm_campaign=launch&x=a%2Bb'),production);
 assert.equal(response.status,308);assert.equal(response.headers.get('location'),'https://recallant.com/services.html?utm_campaign=launch&x=a%2Bb');
}
assert.equal((await worker.fetch(new Request('https://unapproved.example/services.html'),production)).status,421);
assert.equal((await worker.fetch(new Request('https://recallant.com/'),{ASSETS:assetBinding})).status,503);

function localEnvironment(){
 const names=new Set(['path','systemroot','windir','comspec','pathext','temp','tmp','home','userprofile','localappdata','appdata']);
 return {...Object.fromEntries(Object.entries(process.env).filter(([key])=>names.has(key.toLowerCase()))),WRANGLER_SEND_METRICS:'false',CLOUDFLARE_LOAD_DEV_VARS_FROM_DOT_ENV:'false',CI:'true'};
}
async function port(){const server=createServer();await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(0,'127.0.0.1',resolve);});const value=server.address().port;await new Promise(resolve=>server.close(resolve));return value;}
async function stop(child){
 if(!child||child.exitCode!==null)return;
 if(process.platform==='win32'){const task=spawn('taskkill.exe',['/PID',String(child.pid),'/T','/F'],{windowsHide:true,stdio:'ignore'});await new Promise(resolve=>{task.once('exit',resolve);task.once('error',resolve);});}
 else child.kill();
 if(child.exitCode===null)await Promise.race([new Promise(resolve=>child.once('exit',resolve)),sleep(3000)]);
 if(child.exitCode===null)child.kill('SIGKILL');
}
const directory=await mkdtemp(path.join(tmpdir(),'recallant-hosting-check-'));
let child;let outputLog='';
try{
 const chosenPort=await port();const base='http://127.0.0.1:'+chosenPort;
 const local={...config,name:'recallant-local-check',main:path.join(root,config.main),env:undefined,assets:{...config.assets,directory:output},vars:{DEPLOYMENT_ENV:'preview'},workers_dev:false,preview_urls:false};
 const configPath=path.join(directory,'wrangler.json');await writeFile(configPath,JSON.stringify(local));
 const cli=path.join(root,'node_modules/wrangler/bin/wrangler.js');assert.ok(existsSync(cli),'Run npm ci before hosting checks');
 child=spawn(process.execPath,[cli,'dev','--local','--config',configPath,'--port',String(chosenPort),'--ip','127.0.0.1','--persist-to',path.join(directory,'state')],{cwd:directory,env:localEnvironment(),windowsHide:true,stdio:['ignore','pipe','pipe']});
 for(const stream of [child.stdout,child.stderr])stream.on('data',bytes=>{outputLog=(outputLog+bytes.toString()).slice(-8000);});
 child.on('error',error=>{outputLog+='\n'+error.message;});
 let started=false;
 for(let attempt=0;attempt<120;attempt++){
  if(child.exitCode!==null)throw Error('Local Worker exited: '+outputLog);
  try{const response=await fetch(base+'/robots.txt',{signal:AbortSignal.timeout(500)});if(response.status===200&&response.headers.get('x-robots-tag')==='noindex, nofollow'){started=true;break;}}catch{}
  await sleep(250);
 }
 assert.ok(started,'Local Worker was not ready within the bounded startup window: '+outputLog);
 const runtimeChecks=await checkRoutes({base,manifest,preview:true});
 console.log(JSON.stringify({publicFiles:manifest.files.length,unitChecks,runtimeChecks,canonicalRedirects:3,privatePaths:privatePaths.length,realEmailsSent:0,externalEnquiries:0}));
}finally{
 await stop(child);
 const resolved=path.resolve(directory);assert.ok(resolved.startsWith(path.resolve(tmpdir())+path.sep)&&path.basename(resolved).startsWith('recallant-hosting-check-'));
 await rm(resolved,{recursive:true,force:true,maxRetries:5,retryDelay:200});
}
