import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {verifyBytes} from './propagation.mjs';

export const privatePaths=[
 '/_build/build.py','/_build/README.md','/_build/content/study-source.html',
 '/_build/data/helpdesk-explorer.json','/_build/cloudflare/worker.mjs',
 '/.github/workflows/check-site.yml','/.git/config','/.env','/.dev.vars',
 '/config/private.json','/package.json','/package-lock.json','/wrangler.jsonc','/_config.yml',
 '/.cloudflare/manifest.json','/node_modules/wrangler/package.json','/api/enquiry',
 '/%5fbuild/build.py','/%2egit/config','/assets/%2e%2e/%5fbuild/README.md',
 '/_build%2fREADME.md','/assets%5c..%5c_build%5cREADME.md','/services','/unknown.html'
];
const digest=body=>createHash('sha256').update(body).digest('hex');
function headers(response,{preview=false}={}){
 assert.equal(response.headers.get('x-content-type-options'),'nosniff');
 assert.equal(response.headers.get('x-frame-options'),'DENY');
 assert.match(response.headers.get('content-security-policy')||'',/script-src 'self'/);
 assert.match(response.headers.get('cache-control')||'',/\bno-transform\b/);
 if(preview){assert.match(response.headers.get('cache-control'),/no-store/);assert.equal(response.headers.get('x-robots-tag'),'noindex, nofollow');}
}
export async function checkRoutes({base,manifest,fetcher=fetch,preview=false,propagationBudget=null}){
 let checks=0;
 const get=(path,options={})=>fetcher(new Request(new URL(path,base),{redirect:'manual',signal:AbortSignal.timeout(15000),...options}));
 for(const file of manifest.files){
  const response=await get('/'+file.path);assert.equal(response.status,200,file.path);headers(response,{preview});
  if(preview&&file.path==='robots.txt')assert.equal(await response.text(),'User-agent: *\nDisallow: /\n');
  else await verifyBytes({response,request:()=>get('/'+file.path),expected:file.sha256,validate:r=>headers(r,{preview}),budget:propagationBudget,label:file.path});
  checks++;
 }
 const homepage=await get('/');await verifyBytes({response:homepage,request:()=>get('/'),expected:manifest.files.find(file=>file.path==='index.html').sha256,validate:r=>headers(r,{preview}),budget:propagationBudget,label:'/'});checks++;
 const head=await get('/services.html',{method:'HEAD'});assert.equal(head.status,200);assert.equal((await head.arrayBuffer()).byteLength,0);headers(head,{preview});checks++;
 for(const path of privatePaths){const response=await get(path);assert.equal(response.status,404,path+' must not be publicly served');headers(response,{preview});checks++;}
 const missing=await get('/missing-route');await verifyBytes({response:missing,request:()=>get('/missing-route'),status:404,expected:manifest.files.find(file=>file.path==='404.html').sha256,validate:r=>headers(r,{preview}),budget:propagationBudget,label:'/missing-route'});checks++;
 const post=await get('/contact.html',{method:'POST',body:'must-not-collect'});assert.equal(post.status,405);assert.equal(post.headers.get('allow'),'GET, HEAD');checks++;
 return checks;
}
