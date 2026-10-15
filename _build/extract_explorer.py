"""Extract per-question explorer data from the helpdesk study run (read-only).

Run from the project workspace, where the raw study run lives:
    python3 _build/extract_explorer.py _build/data/helpdesk-explorer.json
The raw answers (responses.jsonl) are not in this repo; the output JSON is committed.
"""
import json, re, sys
from urllib.parse import urlparse
from collections import Counter, defaultdict

RUN = "/mnt/project-files/geo-agency/runs/helpdesk-2026-10"
AUDIT = "/mnt/project-files/geo-agency/engine/examples/helpdesk-study.audit.json"
OUT = sys.argv[1]

audit = json.load(open(AUDIT))
res = json.load(open(f"{RUN}/report/results.json"))
names = {k: v["name"] for k, v in res["brands"].items()}
names["hubspot"] = "HubSpot"  # short label for charts
stab = {p["prompt_id"]: p for p in res["prompt_stability"]}

def text_of(r):
    t = []
    for o in r["raw"]["response"]["output"]:
        for c in (o.get("content") or []):
            if isinstance(c, dict) and c.get("text"):
                t.append(c["text"])
    return "\n".join(t)

def dom(u):
    n = re.sub(r"^www\.", "", urlparse(u).netloc.lower())
    parts = n.split(".")
    if len(parts) > 2 and parts[-2] not in ("co", "com"):
        n = ".".join(parts[-2:])
    return n

cites = defaultdict(Counter)
for line in open(f"{RUN}/responses.jsonl"):
    r = json.loads(line)
    t = text_of(r)
    resl = [o for o in r["raw"]["response"]["output"] if "results" in o]
    idmap = {x["id"]: dom(x["url"]) for x in (resl[0]["results"] if resl else [])}
    cited = {idmap.get(int(n)) for n in re.findall(r"\[(\d+)\]", t)} - {None}
    for c in cited:
        cites[r["prompt_id"]][c] += 1

cat_label = {"discovery": "Best for", "alternatives": "Alternatives", "comparison": "Comparisons", "problem": "How-to"}
out = []
for p in audit["prompts"]:
    if p["category"] == "branded":
        continue
    s = stab[p["id"]]
    n = s["samples"]
    first = sorted(((names[b], c) for b, c in s["top_pick_counts"].items()), key=lambda x: (-x[1], x[0]))
    firsts = dict(first)
    named = sorted(((names[b], round(v * n)) for b, v in s["mention_rates"].items() if v > 0),
                   key=lambda x: (-x[1], -firsts.get(x[0], 0), x[0]))
    src = sorted(cites[p["id"]].items(), key=lambda x: (-x[1], x[0]))[:4]
    out.append({"id": p["id"], "q": p["text"], "cat": cat_label.get(p["category"], p["category"]),
                "runs": n, "named": named, "first": first, "sources": src})
json.dump(out, open(OUT, "w"), indent=1)
print(len(out), "questions")
