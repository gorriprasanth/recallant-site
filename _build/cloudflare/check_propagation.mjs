import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {verifyBytes} from './propagation.mjs';
const expected=createHash('sha256').update('current').digest('hex');
let calls=0;const budget={used:0,maximum:2};
await verifyBytes({response:new Response('old'),request:async()=>{calls++;return new Response('current')},expected,budget,delay:async()=>{},label:'test.html'});
assert.equal(calls,1);assert.equal(budget.used,1);
await assert.rejects(verifyBytes({response:new Response('old'),request:async()=>{calls++;return new Response('old')},expected,budget,delay:async()=>{},label:'test.html'}),/budget exhausted/);
assert.equal(calls,2);assert.equal(budget.used,2);
for(const options of [{response:new Response('old',{status:404})},{response:new Response('old'),validate:()=>{throw new Error('security-header failure')}}]){
 await assert.rejects(verifyBytes({request:async()=>{throw new Error('must never retry')},expected,budget:{used:0,maximum:6},delay:async()=>{},label:'test.html',...options}));
}
await assert.rejects(verifyBytes({response:new Response('old'),request:async()=>new Response('current'),expected,label:'local-no-retries'}),/budget exhausted/);
console.log('Propagation checks passed: convergence, shared exhaustion, status/security rejection, local default disabled.');
