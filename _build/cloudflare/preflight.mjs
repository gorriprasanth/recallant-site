import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {checkPackage,root} from './package.mjs';

const target=process.argv[2];assert.ok(['preview','production'].includes(target));
checkPackage();
const operatorOAuth=process.argv.includes('--operator-oauth');
assert.ok(!operatorOAuth||!process.env.CI,'Operator OAuth is a local-only explicit option, never a CI credential fallback.');
assert.ok(process.env.CLOUDFLARE_ACCOUNT_ID,'Set the reviewed Cloudflare account ID in the process environment; it is never printed.');
assert.ok(operatorOAuth||process.env.CLOUDFLARE_API_TOKEN,'Set the deployment API token, or explicitly select --operator-oauth locally after checking the intended Wrangler account.');
if(target==='production'){
 assert.equal(process.env.CLOUDFLARE_DEPLOY_ENABLED,'true','Production deployment is disabled until the reviewed migration gate is enabled.');
 const git=args=>execFileSync('git',args,{cwd:root,encoding:'utf8'}).trim();
 const revision=git(['rev-parse','HEAD']);
 if(process.env.CI){assert.equal(process.env.GITHUB_REF,'refs/heads/main');assert.equal(process.env.GITHUB_SHA,revision);}
 else assert.equal(git(['branch','--show-current']),'main','Only main may be deployed to production.');
 assert.equal(git(['status','--porcelain']),'','Commit the reviewed changes before production deployment.');
 const remote=execFileSync('git',['ls-remote','--exit-code','https://github.com/gorriprasanth/recallant-site.git','refs/heads/main'],{cwd:root,encoding:'utf8',timeout:15000}).trim();
 assert.match(remote,/^[a-f0-9]{40}\s+refs\/heads\/main$/);
 assert.equal(remote.split(/\s+/)[0],revision,'A newer main revision exists; verify and deploy that revision instead of rolling the site back.');
}
console.log(`Deployment preflight passed for ${target}. No deployment performed by this check.`);
