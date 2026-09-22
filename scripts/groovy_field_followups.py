#!/usr/bin/env python3
"""Cheap follow-ups to the Groovy-field census (hypotheses 1-3 of the checkpoint).

  complement  Does complementing a rule's output (phi -> 255-phi) switch G-only
              closure, and does the rule's D0 map explain the switches? Uses
              census.json only; no new decisions.
  universal3  Which radius-one tracks close every rule with memory <= 3?
              Reuses census verdicts for k = 1, 2 and decides k = 3 only
              where needed (certified like the suite).
  gonly5      G alone at memory 5 for rules with no law at memory <= 4 or
              unresolved there.
Run: python scripts/groovy_field_followups.py STAGE [--jobs N]
Outputs: results/groovy_field_20260922/followup_STAGE.json
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from groovy_field_suite import certified, code  # noqa: E402

DIR = ROOT / "results" / "groovy_field_20260922"
CENSUS = json.loads((DIR / "census.json").read_text())["data"]
D0 = {(0, 0): "both->0", (1, 1): "both->1", (0, 1): "identity", (1, 0): "swap"}


def min_k(rule):
    e = CENSUS[str(rule)]["G_only"]
    for k in (1, 2, 3, 4):
        v = e.get(f"k{k}")
        if v is None:
            break
        if v["verdict"] == "L":
            return k
        if v["verdict"] in "?T":
            return "unresolved"
    return ">4"


def d0(rule):
    return D0[(rule & 1, (rule >> 7) & 1)]


def stage_complement():
    rows, table = [], Counter()
    for r in range(256):
        c = 255 - r
        if c < r:
            continue
        a, b = min_k(r), min_k(c)
        closes = lambda x: isinstance(x, int)
        kind = ("unresolved" if "unresolved" in (a, b) else
                "both close" if closes(a) and closes(b) else
                "neither closes" if not closes(a) and not closes(b) else "switches")
        table[(kind, f"{d0(r)}|{d0(c)}")] += 1
        rows.append({"rule": r, "complement": c, "min_k": [a, b],
                     "d0": [d0(r), d0(c)], "kind": kind})
    by_kind = Counter(r["kind"] for r in rows)
    by_d0 = {}
    for (kind, pair), n in table.items():
        by_d0.setdefault(pair, {})[kind] = n
    switches = [r for r in rows if r["kind"] == "switches"]
    closer_d0 = Counter(r["d0"][0] if isinstance(r["min_k"][0], int) else r["d0"][1] for r in switches)
    return {"pairs": len(rows), "by_kind": dict(by_kind), "by_d0_pair": by_d0,
            "switches_closing_side_d0": dict(closer_d0), "rows": rows}


def job_universal3(track):
    fails = []
    for r in range(256):
        t = CENSUS[str(r)]["tracks"]
        if "L" in (t["k1"]["verdicts"][track], t["k2"]["verdicts"][track]):
            continue
        k3 = t.get("k3")
        v = k3["verdicts"][track] if k3 else code(certified(r, (track,), 3, 0))
        if v != "L":
            fails.append([r, v])
    return track, fails


def job_gonly5(rule):
    rec = certified(rule, (), 5, 0)
    out = {"verdict": code(rec)}
    if code(rec) == "L":
        out["radius"] = rec["certificate"]["radius"]
    elif code(rec) == "C":
        out["periods"] = rec["periods"]
    elif rec["status"] == "too_large":
        out["edges"] = rec["edges"]
    return rule, out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["complement", "universal3", "gonly5"])
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    t0 = time.time()
    if a.stage == "complement":
        data = stage_complement()
    else:
        fn, items = ((job_universal3, range(256)) if a.stage == "universal3" else
                     (job_gonly5, [r for r in range(256) if not isinstance(min_k(r), int)]))
        with Pool(a.jobs) as pool:
            raw = dict(pool.imap_unordered(fn, items))
        data = {str(k): raw[k] for k in sorted(raw)}
    doc = {"stage": a.stage, "schema": "groovy-field-v1",
           "elapsed_seconds": round(time.time() - t0, 1), "data": data}
    (DIR / f"followup_{a.stage}.json").write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n")
    print(a.stage, "done in", doc["elapsed_seconds"], "s")


if __name__ == "__main__":
    main()
