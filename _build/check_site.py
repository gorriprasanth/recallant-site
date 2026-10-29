#!/usr/bin/env python3
"""Offline checks for generated Recallant pages and preserved research evidence.

Run from any directory with Python 3.10+. No browser, network, credentials or
email submission is used. The historical study baseline is deliberately fixed;
changes to that evidence require a separately reviewed baseline update.
"""
from __future__ import annotations

from collections import Counter
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import parse_qs, unquote, urljoin, urlsplit


ROOT = Path(__file__).resolve().parent.parent
SITE = "https://recallant.com/"
BASELINE = "dcb51907a4c6ab92aa13c840117efce3ca0e49d9"
CONTENT_PAGES = {
    "index.html", "services.html", "plans.html", "research.html",
    "helpdesk-study.html", "sample-snapshot.html", "about.html",
    "method.html", "contact.html", "privacy.html", "404.html",
}
VERIFICATION = "googlef44257636166e7ad.html"
# SHA-256 of UTF-8 source bytes with CRLF/CR normalized to LF at BASELINE.
EVIDENCE_HASHES = {
    "_build/content/study-source.html": "fb19862a47dd9935eefde2d7759faea4b7399429f5d7f64e3ee7719517091a47",
    "_build/data/helpdesk-explorer.json": "c03b824e3f7a01a4a4482533bb22193ddebe3ab0850bd1cab81cfdcb0cddf643",
}
REQUESTS = {
    "recallant-snapshot", "recallant-pilot", "recallant-audit", "recallant-monitoring",
}
NUMBER = re.compile(r"\d+(?:\.\d+)?")


def normalized_hash(raw: bytes) -> str:
    return hashlib.sha256(raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")).hexdigest()


class Document(HTMLParser):
    def __init__(self, text: str):
        super().__init__(convert_charrefs=True)
        self.ids = Counter()
        self.h1s = 0
        self.refs = []
        self.links = []
        self.canonicals = []
        self.forms = 0
        self.json_blocks = []
        self.visible = []
        self.tables = []
        self._table_depth = 0
        self._table = None
        self._cell = None
        self._script = None
        self.feed(text)
        self.close()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids[a["id"]] += 1
        self.h1s += tag == "h1"
        self.forms += tag == "form"
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "link" and "canonical" in a.get("rel", "").split():
            self.canonicals.append(a.get("href", ""))
        for attr in ("href", "src", "poster"):
            if a.get(attr):
                self.refs.append(a[attr])
        if a.get("srcset"):
            self.refs.extend(item.strip().split()[0] for item in a["srcset"].split(",") if item.strip())
        if tag == "script":
            kind = a.get("type", "").lower()
            self._script = (kind, [])
        if tag == "table":
            self._table_depth += 1
            if self._table_depth == 1:
                self._table = []
        if tag in ("td", "th") and self._table_depth == 1:
            self._cell = []

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data):
        if self._script is not None:
            self._script[1].append(data)
        else:
            self.visible.append(data)
        if self._cell is not None:
            self._cell.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._script is not None:
            kind, parts = self._script
            if kind in ("application/ld+json", "application/json"):
                self.json_blocks.append((kind, "".join(parts)))
            self._script = None
        if tag in ("td", "th") and self._cell is not None:
            values = tuple(NUMBER.findall(" ".join(self._cell)))
            if values:
                self._table.append(values)
            self._cell = None
        if tag == "table":
            if self._table_depth == 1:
                self.tables.append(tuple(self._table))
                self._table = None
            self._table_depth -= 1


def public_files():
    """GitHub Pages' branch layout excludes dot/underscore source directories."""
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if any(part.startswith((".", "_")) for part in relative.parts):
            continue
        if path.is_file():
            yield path


def main() -> int:
    errors = []
    docs = {}
    checked_refs = 0
    json_count = 0

    def fail(message):
        errors.append(message)

    if (ROOT / ".nojekyll").exists():
        fail(".nojekyll would bypass the source-directory exclusion used by this branch-published site")
    for name in sorted(CONTENT_PAGES):
        path = ROOT / name
        if not path.is_file():
            fail(f"Missing generated page: {name}")
            continue
        raw = path.read_text(encoding="utf-8")
        doc = docs[name] = Document(raw)
        duplicates = sorted(str(k) for k, n in doc.ids.items() if n > 1)
        if duplicates:
            fail(f"{name}: duplicate IDs: {', '.join(duplicates)}")
        if doc.h1s != 1:
            fail(f"{name}: expected one H1; found {doc.h1s}")
        canonical = SITE + ("" if name == "index.html" else name)
        if doc.canonicals != [canonical]:
            fail(f"{name}: canonical must be exactly {canonical}")
        if doc.forms:
            fail(f"{name}: local form found; enquiries must use the explicit shared-desk links")
        if not any(kind == "application/ld+json" for kind, _ in doc.json_blocks):
            fail(f"{name}: missing structured JSON")
        for kind, payload in doc.json_blocks:
            try:
                json.loads(payload)
                json_count += 1
            except json.JSONDecodeError as exc:
                fail(f"{name}: invalid {kind}: {exc.msg}")

    public = list(public_files())
    for path in public:
        name = path.relative_to(ROOT).as_posix()
        lowered = name.lower()
        if any(token in lowered for token in ("recallant-overview", "recallant-handoff")):
            fail(f"Private overview/handoff must not be published: {name}")
        if path.suffix.lower() not in (".html", ".js", ".json", ".txt", ".md"):
            continue
        raw = path.read_text(encoding="utf-8")
        if re.search(r"formspree|data-snapshot-form|mqpeglzv", raw, re.I):
            fail(f"{name}: obsolete form endpoint or active form hook remains")
        plain = " ".join(Document(raw).visible).lower() if path.suffix == ".html" else raw.lower()
        if any(marker in plain for marker in ("recallant: full handoff pack", "recallant company overview", "where the secret lives", "outreach tracker (last update")):
            fail(f"{name}: private overview/handoff content detected")
        if path.suffix == ".html" and "/" not in name and name not in CONTENT_PAGES | {VERIFICATION}:
            fail(f"Unexpected published HTML page: {name}")

    def check_ref(source, ref):
        nonlocal checked_refs
        if ref.startswith(("mailto:", "tel:", "data:")):
            return
        base = SITE + source
        parsed = urlsplit(urljoin(base, ref))
        if parsed.netloc not in ("recallant.com", "www.recallant.com"):
            return
        relative = unquote(parsed.path).lstrip("/") or "index.html"
        if relative.endswith("/"):
            relative += "index.html"
        target = (ROOT / relative).resolve()
        try:
            parts = target.relative_to(ROOT).parts
        except ValueError:
            fail(f"{source}: path escapes public root: {ref}")
            return
        if any(part.startswith((".", "_")) for part in parts):
            fail(f"{source}: private source link: {ref}")
            return
        checked_refs += 1
        if not target.is_file():
            fail(f"{source}: missing local target: {ref}")
            return
        fragment = unquote(parsed.fragment)
        if fragment and target.suffix == ".html":
            key = target.relative_to(ROOT).as_posix()
            target_doc = docs.get(key)
            if target_doc is None:
                target_doc = Document(target.read_text(encoding="utf-8"))
            if fragment not in target_doc.ids:
                fail(f"{source}: missing anchor: {ref}")

    for name, doc in docs.items():
        for ref in doc.refs:
            check_ref(name, ref)
    for path in public:
        if path.suffix.lower() == ".css":
            name = path.relative_to(ROOT).as_posix()
            for match in re.finditer(r"url\(\s*(['\"]?)(.*?)\1\s*\)", path.read_text(encoding="utf-8")):
                check_ref(name, match.group(2))

    if "contact.html" in docs:
        contexts = []
        for href in docs["contact.html"].links:
            parsed = urlsplit(href)
            if parsed.netloc != "signalandsyllable.com" or parsed.path != "/contact":
                continue
            query = parse_qs(parsed.query, keep_blank_values=True)
            request = query.get("request", [])
            if parsed.scheme != "https" or query.get("service") != ["Recallant"] or len(request) != 1 or request[0] not in REQUESTS or set(query) != {"service", "request"} or parsed.fragment:
                fail(f"contact.html: invalid shared enquiry context: {href}")
            else:
                contexts.append(request[0])
        if Counter(contexts) != Counter(REQUESTS):
            fail("contact.html: each of the four exact shared enquiry contexts must appear once")
        if not any(href.startswith("mailto:gorripatiprasanth@gmail.com") for href in docs["contact.html"].links):
            fail("contact.html: missing confirmed direct email fallback")

    for name, expected in EVIDENCE_HASHES.items():
        path = ROOT / name
        if not path.is_file() or normalized_hash(path.read_bytes()) != expected:
            fail(f"Retained research source changed from {BASELINE[:7]}: {name}")
    try:
        historical = subprocess.check_output(
            ["git", "show", f"{BASELINE}:helpdesk-study.html"], cwd=ROOT, stderr=subprocess.PIPE
        ).decode("utf-8")
        original_tables = Document(historical).tables
        current_tables = docs.get("helpdesk-study.html")
        if not original_tables:
            fail("Historical study baseline has no numeric tables")
        elif current_tables is not None and original_tables != current_tables.tables:
            fail("Published study numeric table values/order changed from the historical baseline; labels may change, values may not")
    except subprocess.CalledProcessError:
        fail(f"Baseline commit {BASELINE[:7]} unavailable; fetch repository history before running this check")

    if not (ROOT / VERIFICATION).is_file():
        fail("Existing Google verification file is missing")
    if not (ROOT / "CNAME").is_file() or (ROOT / "CNAME").read_text().strip() != "recallant.com":
        fail("CNAME must retain recallant.com")

    if errors:
        print("Recallant checks FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS: {len(docs)} pages; {checked_refs} local links/assets/anchors; {json_count} JSON blocks.")
    print("PASS: four shared enquiry routes, direct email fallback, no obsolete forms or private handoff content.")
    print(f"PASS: both retained research sources and published study numeric tables match {BASELINE[:7]}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
