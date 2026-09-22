#!/usr/bin/env python3
"""The Groovy field research suite: exact closure data for all elementary CA.

Every verdict comes from ``groovy.groovy_field.decide`` and carries its evidence
status: a law by an exhaustive finite-window table (``certify_law``, shared
packed arithmetic), a counterexample by an explicit eventually periodic pair
verified with the tuple implementation (``witness`` + ``verify_witness``).
A verdict whose certificate could not be produced within budget is recorded
as such and never counted as a theorem.

Stages (see docs/research/2026-09-22-groovy-field-program.md):
  validate  decider vs brute-force rings, all rules, G alone, k = 1, 2
  tracks110 Rule 110: every radius-one extra track, k = 1, 2, 3
  census    all 256 rules: G alone (k <= 4) and every track (k <= 2, then 3)
  reachable all 256 rules: G alone after burn-in t = 1, 2
Run:  python scripts/groovy_field_suite.py STAGE [--jobs N]
Use --output-dir for a new run; existing artifacts are never overwritten.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from groovy.groovy_field import (decide, witness, verify_witness,  # noqa: E402
                                 certify_law, ring_collision)

OUT = ROOT / "results" / "groovy_field_20260922"


def output_path(directory, name):
    """Refuse an overwrite before spending time evaluating a stage."""
    path = Path(directory) / name
    if path.exists():
        raise FileExistsError(f"Preserving {path}; choose a fresh --output-dir")
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def source_hashes():
    paths = [ROOT / "src/groovy/groovy_field.py", *sorted((ROOT / "scripts").glob("groovy_field_*.py"))]
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def write_record(path, doc):
    with path.open("x") as f:
        f.write(json.dumps(doc, indent=1, sort_keys=True) + "\n")


def entry(rec):
    """Keep the compact verdict and the evidence needed to interpret/replay it."""
    out = {"verdict": code(rec), **rec}
    if code(rec) == "L":
        out["radius"] = rec["certificate"]["radius"]
    return out


def certified(rule, tracks, k, t):
    """Decide and certify one case. Returns a compact record."""
    v = decide(rule, tracks, k, t)
    rec = {"status": v.status, "rule": rule, "tracks": list(tracks), "k": k, "t": t,
           "edges": v.edges}
    if v.status == "law":
        c = certify_law(rule, tracks, k, t, r_max=8)
        rec["certificate"] = c
        rec["certified"] = c["status"] == "certified"
    elif v.status == "counterexample":
        w = witness(v)
        chk = verify_witness(rule, tracks, k, t, w)
        rec["certified"] = chk["verified"]
        rec["periods"] = [w["left_period"], w["right_period"]]
        rec["witness"] = w
        rec["verification"] = chk
    else:
        rec["certified"] = False
        rec["edges"] = v.edges
    return rec


def code(rec):
    """One-character verdict: L law, C counterexample, T too large, ? uncertified."""
    if not rec["certified"]:
        return "T" if rec["status"] == "too_large" else "?"
    return "L" if rec["status"] == "law" else "C"


# ---------------------------------------------------------------- stages

def job_validate(rule):
    out = {}
    for k in (1, 2):
        rec = certified(rule, (), k, 0)
        ring = next((n for n in range(1, 9) if ring_collision(rule, (), k, 0, n)), None)
        out[f"k{k}"] = {**entry(rec), "first_ring_collision": ring,
                        "consistent": not (ring is not None and rec["status"] == "law")}
    return rule, out


def job_tracks110(track):
    out = {}
    for k in (1, 2, 3):
        rec = certified(110, (track,), k, 0)
        out[f"k{k}"] = entry(rec)
    return track, out


def job_census(rule):
    res = {"G_only": {}, "tracks": {}}
    for k in (1, 2, 3, 4):
        rec = certified(rule, (), k, 0)
        res["G_only"][f"k{k}"] = entry(rec)
        if code(rec) == "L":
            break
    for k in (1, 2):
        s, radii, records = [], [], []
        for tr in range(256):
            rec = certified(rule, (tr,), k, 0)
            s.append(code(rec))
            radii.append(rec["certificate"]["radius"] if code(rec) == "L" else -1)
            records.append(entry(rec))
        res["tracks"][f"k{k}"] = {"verdicts": "".join(s), "radius": radii, "records": records}
    if "L" not in res["tracks"]["k2"]["verdicts"]:
        records = [entry(certified(rule, (tr,), 3, 0)) for tr in range(256)]
        res["tracks"]["k3"] = {"verdicts": "".join(r["verdict"] for r in records), "records": records}
    return rule, res


def job_reachable(rule):
    res = {}
    for t in (1, 2):
        for k in (1, 2, 3):
            rec = certified(rule, (), k, t)
            res[f"t{t}k{k}"] = entry(rec)
            if code(rec) in ("L", "T"):
                break
    return rule, res


def tail_kind(a: str, b: str) -> str:
    """How two aligned periodic tails (one period each) differ."""
    if a == b:
        return "equal"
    p = len(a)
    if set(a) == {"0"} and set(b) == {"1"} or set(a) == {"1"} and set(b) == {"0"}:
        return "uniform_swap"
    if any(b == a[s:] + a[:s] for s in range(1, p)):
        return "phase"
    if b == "".join("1" if c == "0" else "0" for c in a):
        return "complement"
    return "other"


def classify(rec):
    """Kinds of the left and right tail differences of a certified witness."""
    w = rec["witness"]
    lp, rp = rec["periods"]
    s, s2 = w["S"], w["S_prime"]
    left, right = tail_kind(s[:lp], s2[:lp]), tail_kind(s[-rp:], s2[-rp:])
    if left == right == "equal":
        return "finite"
    kinds = sorted({left, right} - {"equal"})
    return "+".join(kinds)


def job_taxonomy(rule):
    """What G alone fails to see: classify the witness at every failing k <= 4."""
    out = {}
    for k in (1, 2, 3, 4):
        rec = certified(rule, (), k, 0)
        if code(rec) != "C":
            out[f"k{k}"] = entry(rec)
            break
        out[f"k{k}"] = {"kind": classify(rec), **entry(rec)}
    if rule == 110:
        out["tracks_k2"] = {}
        for tr in range(256):
            rec = certified(110, (tr,), 2, 0)
            if code(rec) == "C":
                out["tracks_k2"][str(tr)] = {"kind": classify(rec), **entry(rec)}
    return rule, out


STAGES = {"validate": (job_validate, range(256)),
          "taxonomy": (job_taxonomy, range(256)),
          "tracks110": (job_tracks110, range(256)),
          "census": (job_census, range(256)),
          "reachable": (job_reachable, range(256))}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=STAGES)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--output-dir", type=Path, default=OUT)
    a = ap.parse_args()
    path = output_path(a.output_dir, f"{a.stage}.json")
    fn, items = STAGES[a.stage]
    t0 = time.time()
    with Pool(a.jobs) as pool:
        data = dict(pool.imap_unordered(fn, items))
    doc = {"stage": a.stage, "schema": "groovy-field-v2", "source_hashes": source_hashes(),
           "elapsed_seconds": round(time.time() - t0, 1),
           "data": {str(key): data[key] for key in sorted(data)}}
    write_record(path, doc)
    print(a.stage, "done in", doc["elapsed_seconds"], "s")


if __name__ == "__main__":
    main()
