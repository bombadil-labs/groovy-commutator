#!/usr/bin/env python3
"""Radius-one obstruction check for the eight frozen whole-field survivors."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

from verify_nakamura_retention import ROOT, enabled, prefixes, project, replay_prefix, require, update

OUT = ROOT / "results/nakamura_local_retention_20260921.json"
INPUTS = ["scripts/verify_nakamura_local_retention.py", "scripts/verify_nakamura_retention.py",
          "src/groovy/ca.py", "docs/research/protocols/nakamura-retention-20260921.md",
          "docs/research/protocols/nakamura-local-retention-20260921.md",
          "results/nakamura_retention_20260921.json"]


def neighbourhood(state, site, mask):
    q = project(state, mask)
    return tuple(q[j % len(q)] for j in (site - 1, site, site + 1))


def check_witness(w, rule, mask):
    x, y = replay_prefix(w["x"], rule), replay_prefix(w["y"], rule)
    i, j = w["sites"]
    require(all(type(v) is int and 0 <= v < 5 for v in (i, j)), "bad centre position")
    key = neighbourhood(x, i, mask)
    require(key == neighbourhood(y, j, mask) == tuple(w["observed_neighbourhood"]),
            "local observations differ")
    ex, ey = enabled(x, i), enabled(y, j)
    nx, ny = update(x, i, rule), update(y, j, rule)
    ox, oy = project(nx, mask)[i], project(ny, mask)[j]
    require(ex != ey or (ex and ox != oy), "no local successor conflict")
    require(w["enabled"] == [ex, ey] and w["successor_labels"] == [ox, oy], "bad recorded outputs")
    require(w["successor_current"] == [nx[i][0], ny[j][0]], "bad current-bit outputs")


def audit(rule):
    records = prefixes(rule)
    candidates = []
    for mask in range(56, 64):
        seen = {}
        witness = None
        for state, record, allowed, successors in records:
            for site in range(5):
                key = neighbourhood(state, site, mask)
                output = project(successors[site], mask)[site]
                if key in seen:
                    old_record, old_site, old_allowed, old_output, old_current = seen[key]
                    if allowed[site] != old_allowed or (allowed[site] and output != old_output):
                        witness = {"x": old_record, "y": record, "sites": [old_site, site],
                                   "observed_neighbourhood": list(key),
                                   "enabled": [old_allowed, allowed[site]],
                                   "successor_labels": [old_output, output],
                                   "successor_current": [old_current, successors[site][site][0]]}
                        check_witness(witness, rule, mask)
                        break
                else:
                    seen[key] = (record, site, allowed[site], output, successors[site][site][0])
            if witness is not None:
                break
        candidates.append({"keep_mask": mask, "alphabet_size": 6 + mask.bit_count(),
                           "status": "refuted" if witness else "survives_finite_check", "witness": witness})
    require(candidates[-1]["witness"] is None, "identity quotient failed locality")
    if rule == 204:
        require(all(c["witness"] is None for c in candidates), "identity control failed locality")
    return {"rule": rule, "unique_prefixes": len(records), "candidates": candidates,
            "surviving_masks": [c["keep_mask"] for c in candidates if c["witness"] is None]}


def report():
    prior = json.loads((ROOT / INPUTS[-1]).read_text())
    require(prior["rules"]["110"]["surviving_masks"] == list(range(56, 64)), "prior domain changed")
    return {"schema": 1, "protocol": "nakamura-local-retention-20260921",
            "protocol_freeze_commit": "bc7741b", "review": "none; explicit solo authorization",
            "source_hashes": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in INPUTS},
            "radius": 1, "ring": 5, "rules": {str(r): audit(r) for r in (110, 204)}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", nargs="?", const=str(OUT), metavar="FILE")
    args = parser.parse_args()
    actual = report()
    if args.check:
        saved = json.loads(Path(args.check).read_text())
        for rule, data in saved["rules"].items():
            for candidate in data["candidates"]:
                if candidate["witness"]:
                    check_witness(candidate["witness"], int(rule), candidate["keep_mask"])
        require(saved == actual, "locality result differs from exact replay")
    elif args.write:
        OUT.write_text(json.dumps(actual, indent=2) + "\n")
    print(json.dumps({r: {"surviving_masks": data["surviving_masks"]} for r, data in actual["rules"].items()}))


if __name__ == "__main__":
    main()
