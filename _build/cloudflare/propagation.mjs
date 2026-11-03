import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
const pause=ms=>new Promise(resolve=>setTimeout(resolve,ms));
// One budget for the entire run, enabled only for the public post-deploy check.
// Retry exact-byte mismatches on declared static GETs, never a POST or a
// private-path/security failure. All status and header checks remain immediate.
export async function verifyBytes({response,request,expected,status=200,validate=()=>{},budget,delay=pause,label}){
 let current=response;
 while(true){
  assert.equal(current.status,status,label+' status');
  validate(current);
  const actual=hash(Buffer.from(await current.arrayBuffer()));
  if(actual===expected)return;
  assert.ok(budget && budget.used<budget.maximum,label+' exact public bytes; propagation budget exhausted');
  budget.used++;
  console.log(JSON.stringify({event:'static-propagation-retry',path:label,retry:budget.used,maximum:budget.maximum,delayMilliseconds:10000}));
  await delay(10000);
  current=await request();
 }
}
