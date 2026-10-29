/* Offline campaign-link checks against the actual site source and generated pages. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.join(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'assets/js/site.js'), 'utf8');
const block = source.split('/* ---------------------------------------------------------------- campaign context (no storage or analytics) */')[1]
  .split('/* ---------------------------------------------------------------- navigation tone and state */')[0];
assert(block, 'Campaign implementation must be present.');
function link(href, download = false) {
  return { href, getAttribute(name) { return name === 'href' ? this.href : null; },
    hasAttribute(name) { return name === 'download' && download; },
    setAttribute(name, value) { assert.equal(name, 'href'); this.href = value; } };
}
function run(url, links) {
  vm.runInNewContext(block, { URL, window: { location: { href: url } }, $$: () => links });
  return links;
}
function pageLinks(file) {
  const html = fs.readFileSync(path.join(root, file), 'utf8');
  return [...html.matchAll(/<a\b([^>]*?)href="([^"]+)"([^>]*)>/g)].map(m => link(m[2].replace(/&amp;/g, '&'), /\bdownload(?:=|\s|$)/.test(m[1] + m[3])));
}
const campaign = 'utm_source=linkedin&utm_medium=organic_social&utm_campaign=recallant-launch&utm_content=evidence-first';
const home = run('https://recallant.com/?' + campaign, pageLinks('index.html'));
const services = home.find(a => new URL(a.href, 'https://recallant.com/').pathname === '/services.html');
assert(services, 'Home must have a Services navigation link.');
const serviceLinks = run(services.href, pageLinks('services.html'));
const contact = serviceLinks.find(a => new URL(a.href, services.href).pathname === '/contact.html');
assert(contact, 'Services must have a Contact navigation link.');
const contactLinks = run(contact.href, pageLinks('contact.html'));
const enquiries = contactLinks.filter(a => a.href.startsWith('https://signalandsyllable.com/contact?'));
assert.equal(enquiries.length, 4);
for (const a of enquiries) {
  const u = new URL(a.href);
  assert.equal(u.searchParams.get('service'), 'Recallant');
  assert(['recallant-snapshot', 'recallant-pilot', 'recallant-audit', 'recallant-monitoring'].includes(u.searchParams.get('request')));
  for (const [key, value] of new URLSearchParams(campaign)) assert.equal(u.searchParams.get(key), value);
}
const untouched = [link('#scope'), link(' #scope '), link('mailto:hello@recallant.com'), link('/assets/og.png'), link('/guide.pdf'),
  link('/download', true), link('https://example.com/page'), link('https://signalandsyllable.com/'),
  link('https://signalandsyllable.com/contact?service=Storyline&request=recallant-pilot'),
  link('https://signalandsyllable.com/contact?service=Recallant&request=recallant-unknown'),
  link('https://signalandsyllable.com/contact?service=Recallant&service=Storyline&request=recallant-pilot')];
const originals = untouched.map(a => a.href);
run('https://recallant.com/?' + campaign, untouched);
assert.deepEqual(untouched.map(a => a.href), originals, 'Do not alter fragments, mail, downloads or unrelated destinations.');
const preserved = run('https://recallant.com/?' + campaign + '&email=private%40example.com', [link('plans.html?offer=pilot&utm_source=partner#scope')])[0];
const p = new URL(preserved.href);
assert.equal(p.searchParams.get('utm_source'), 'partner');
assert.equal(p.searchParams.get('offer'), 'pilot');
assert.equal(p.hash, '#scope');
assert(!p.searchParams.has('email'));
const invalid = run('https://recallant.com/?utm_source=linkedin&utm_source=x&utm_medium=UPPERCASE&utm_campaign=' + 'a'.repeat(65) + '&utm_content=hello%20world', [link('contact.html')])[0];
assert.equal(invalid.href, 'contact.html', 'Reject duplicate, uppercase, oversized and space-containing values.');
const noCampaign = run('https://recallant.com/', [link('contact.html')])[0];
assert.equal(noCampaign.href, 'contact.html');
console.log('Campaign checks passed: actual three-page enquiry journey, four contexts, destination exclusions, validation and existing-query preservation. No network, cookies or storage.');
