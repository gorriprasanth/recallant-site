import assert from 'node:assert/strict';
import {checkPackage} from './package.mjs';
import {checkRoutes} from './check_routes.mjs';

const argument=name=>process.argv[process.argv.indexOf(name)+1];
const base=argument('--base');assert.ok(process.argv.includes('--base')&&base,'Pass the exact reviewed public HTTPS origin with --base');
const url=new URL(base);assert.equal(url.protocol,'https:');assert.equal(url.pathname,'/');assert.ok(!url.username&&!url.password&&!url.search&&!url.hash);
const preview=process.argv.includes('--preview');
assert.ok(preview?url.hostname.endsWith('.workers.dev'):url.origin==='https://recallant.com','Unexpected public verification target');
const checks=await checkRoutes({base,manifest:checkPackage(),preview});
if(!preview){for(const origin of ['http://recallant.com','http://www.recallant.com','https://www.recallant.com']){
 const response=await fetch(origin+'/services.html?utm_campaign=launch&x=a%2Bb',{redirect:'manual',signal:AbortSignal.timeout(15000)});
 assert.equal(response.status,308);assert.equal(response.headers.get('location'),'https://recallant.com/services.html?utm_campaign=launch&x=a%2Bb');
}}
console.log(JSON.stringify({base:url.origin,checks,preview,realEmailsSent:0,retries:0}));
