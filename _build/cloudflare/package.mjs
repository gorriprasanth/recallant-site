import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {copyFileSync,existsSync,lstatSync,mkdirSync,readFileSync,readdirSync,writeFileSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';

export const root=fileURLToPath(new URL('../../',import.meta.url));
export const publicNames=JSON.parse(readFileSync(new URL('./public-files.json',import.meta.url),'utf8'));
export const output=path.join(root,'.cloudflare/public');
export const manifestPath=path.join(root,'.cloudflare/manifest.json');
const generated=path.join(root,'.cloudflare/generated');
const sha=bytes=>createHash('sha256').update(bytes).digest('hex');
function safePath(base,relative){
 assert.ok(relative&&!relative.includes('\\')&&!path.isAbsolute(relative)&&!relative.split('/').some(part=>part==='..'||part==='.'),'Unsafe public path');
 const target=path.resolve(base,relative);assert.ok(target.startsWith(path.resolve(base)+path.sep),'Public path escaped its directory');
 let current=path.resolve(base);
 for(const part of relative.split('/')){current=path.join(current,part);if(existsSync(current))assert.ok(!lstatSync(current).isSymbolicLink(),'Symlinks and junctions cannot enter the public package');}
 return target;
}
function directory(target){
 assert.ok(path.resolve(target).startsWith(path.join(root,'.cloudflare')+path.sep)||target===path.join(root,'.cloudflare'));
 for(const name of ['.cloudflare',path.relative(root,target).replaceAll(path.sep,'/')])safePath(root,name);
 mkdirSync(target,{recursive:true});
}
function inventory(folder,prefix=''){
 return readdirSync(folder,{withFileTypes:true}).flatMap(item=>{
  const name=prefix+item.name;const target=safePath(folder,item.name);
  assert.ok(!item.isSymbolicLink(),'Unexpected symbolic asset');
  return item.isDirectory()?inventory(target,name+'/'):[name];
 });
}
export function checkPackage(){
 assert.equal(new Set(publicNames).size,29,'The reviewed public allowlist must have 29 unique files');
 assert.deepEqual(inventory(output).sort(),[...publicNames].sort(),'The upload directory must contain only the exact public allowlist');
 const manifest=JSON.parse(readFileSync(manifestPath,'utf8'));
 assert.equal(manifest.hostingProvider,'Cloudflare');
 assert.deepEqual(manifest.files.map(file=>file.path).sort(),[...publicNames].sort());
 for(const file of manifest.files){
  const bytes=readFileSync(safePath(output,file.path));const source=readFileSync(safePath(root,file.path));
  assert.equal(sha(bytes),file.sha256,file.path+' package hash');assert.equal(sha(source),file.sourceSha256,file.path+' source changed after packaging');
  if(file.path!=='privacy.html')assert.equal(sha(bytes),sha(source),file.path+' must retain the exact source bytes');
 }
 const privacy=readFileSync(path.join(output,'privacy.html'),'utf8');
 assert.ok(privacy.includes('hosted through Cloudflare'));assert.ok(!privacy.includes('hosted through GitHub Pages'));
 assert.ok(readFileSync(path.join(root,'privacy.html'),'utf8').includes('hosted through GitHub Pages'),'Default source remains accurate until the hosting switch');
 return manifest;
}
export function buildPackage(){
 for(const name of publicNames){assert.ok(!name.split('/').some(part=>part.startsWith('.')||part.startsWith('_')));safePath(root,name);}
 directory(path.join(root,'.cloudflare'));directory(generated);directory(output);
 const built=spawnSync(process.env.PYTHON||'python',['_build/build.py','--output',generated],{cwd:root,env:{...process.env,RECALLANT_HOSTING_PROVIDER:'Cloudflare',PYTHONUTF8:'1'},encoding:'utf8',windowsHide:true});
 assert.equal(built.status,0,built.stderr||'Cloudflare page generation failed');
 const files=[];
 for(const name of publicNames){
  const source=safePath(root,name);const prepared=safePath(generated,name);const target=safePath(output,name);
  mkdirSync(path.dirname(target),{recursive:true});
  copyFileSync(existsSync(prepared)?prepared:source,target);
  const bytes=readFileSync(target);files.push({path:name,sha256:sha(bytes),sourceSha256:sha(readFileSync(source)),bytes:bytes.length});
 }
 writeFileSync(manifestPath,JSON.stringify({hostingProvider:'Cloudflare',files},null,2)+'\n');
 return checkPackage();
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const result=process.argv.includes('--check')?checkPackage():buildPackage();
 console.log(`Verified ${result.files.length} public files; private source/configuration stays outside .cloudflare/public.`);
}
