#!/usr/bin/env python3
"""Bounded exact quotient audit of the Nakamura current/previous/age interface.

Protocol: docs/research/protocols/nakamura-retention-20260921.md.
--write produces the canonical report; --check [FILE] regenerates it and
replays its witnesses. This does not search alternative simulator designs.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from groovy.ca import apply_rule

OUT = ROOT / "results/nakamura_retention_20260921.json"
INPUTS = ["scripts/verify_nakamura_retention.py", "src/groovy/ca.py",
          "docs/research/protocols/nakamura-retention-20260921.md"]
ALPHABET = tuple(itertools.product((0, 1), (0, 1), range(3)))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def enabled(state, site):
    age = state[site][2]
    return all((state[j % len(state)][2] - age) % 3 != 2 for j in (site - 1, site + 1))


def update(state, site, rule):
    if not enabled(state, site):
        return state
    current, _, age = state[site]
    left, right = state[(site - 1) % len(state)], state[(site + 1) % len(state)]
    l = left[0] if left[2] == age else left[1]
    r = right[0] if right[2] == age else right[1]
    value = (rule >> (4 * l + 2 * current + r)) & 1
    return state[:site] + ((value, current, (age + 1) % 3),) + state[site + 1:]


def project(state, keep_mask):
    # Each fixed (current, age) fiber contains precisely two previous bits.
    # A mask bit of one keeps that distinction; zero identifies the pair.
    return tuple(2 * (3 * c + a) + (p if keep_mask & (1 << (3 * c + a)) else 0)
                 for c, p, a in state)


def current_word(state):
    return "".join(str(c) for c, _, _ in state)


def local_diamonds(rule):
    count = 0
    for state in itertools.product(ALPHABET, repeat=4):
        if not (enabled(state, 1) and enabled(state, 2)):
            continue
        first, second = update(state, 1, rule), update(state, 2, rule)
        require(enabled(first, 2) and enabled(second, 1), "enabledness was lost")
        simultaneous = (state[0], first[1], second[2], state[3])
        require(update(first, 2, rule) == update(second, 1, rule) == simultaneous,
                "local diamond failed")
        count += 1
    return {"windows_checked": 12 ** 4, "jointly_enabled_windows": count,
            "commutes_with_simultaneous": True, "enabledness_persists": True}


def replay_prefix(record, rule):
    source = record["source"]
    age = record["initial_age"]
    sites = record["updates"]
    require(len(source) == 5 and set(source) <= {"0", "1"}, "bad source ring")
    require(age in (0, 1, 2), "bad initial phase")
    require(sites == sorted(set(sites)) and all(0 <= i < 5 for i in sites), "bad prefix")
    state = tuple((int(c), int(c), age) for c in source)
    for site in sites:
        require(enabled(state, site), "prefix contains a blocked update")
        state = update(state, site, rule)
    return state


def prefixes(rule):
    unique = {}
    for row in itertools.product((0, 1), repeat=5):
        source = "".join(map(str, row))
        next_row = apply_rule(np.array(row, dtype=np.uint8), rule)
        for age in range(3):
            for subset in range(32):
                sites = [i for i in range(5) if subset & (1 << i)]
                record = {"source": source, "initial_age": age, "updates": sites}
                state = replay_prefix(record, rule)
                expected = tuple((int(next_row[i]), row[i], (age + 1) % 3)
                                 if i in sites else (row[i], row[i], age) for i in range(5))
                require(state == expected, "prefix differs from synchronous source readout")
                unique.setdefault(state, record)
    return [(state, record, tuple(enabled(state, i) for i in range(5)),
             tuple(update(state, i, rule) for i in range(5))) for state, record in unique.items()]


def check_witness(witness, rule, mask):
    x = replay_prefix(witness["x"], rule)
    y = replay_prefix(witness["y"], rule)
    i = witness["update_site"]
    require(type(i) is int and 0 <= i < 5, "bad update site")
    require(project(x, mask) == project(y, mask), "witness observations differ initially")
    ex, ey = enabled(x, i), enabled(y, i)
    nx, ny = update(x, i, rule), update(y, i, rule)
    require(ex != ey or (ex and project(nx, mask) != project(ny, mask)),
            "witness has no projected successor conflict")
    require(witness["enabled"] == [ex, ey], "incorrect recorded enabledness")
    require(witness["next_current"] == [current_word(nx), current_word(ny)], "incorrect output bits")
    require(witness["different_current"] == (current_word(nx) != current_word(ny)),
            "incorrect current-bit conflict label")


def audit_rule(rule):
    records = prefixes(rule)
    candidates = []
    for mask in range(64):
        seen = {}
        witness = None
        for state, record, allowed, successors in records:
            key = project(state, mask)
            if key not in seen:
                seen[key] = (record, allowed, tuple(project(s, mask) for s in successors), successors)
                continue
            old_record, old_allowed, old_projected, old_successors = seen[key]
            for i in range(5):
                if allowed[i] != old_allowed[i] or (allowed[i] and project(successors[i], mask) != old_projected[i]):
                    witness = {"x": old_record, "y": record, "update_site": i,
                               "enabled": [old_allowed[i], allowed[i]],
                               "next_current": [current_word(old_successors[i]), current_word(successors[i])],
                               "different_current": current_word(old_successors[i]) != current_word(successors[i])}
                    check_witness(witness, rule, mask)
                    break
            if witness is not None:
                break
        candidates.append({"keep_mask": mask, "alphabet_size": 6 + mask.bit_count(),
                           "status": "refuted" if witness else "survives_finite_check",
                           "witness": witness})
    require(candidates[63]["witness"] is None, "identity quotient failed")
    if rule == 204:
        require(all(c["witness"] is None for c in candidates), "identity-source control failed")
    return {"rule": rule, "local_diamonds": local_diamonds(rule), "prefix_records": 3072,
            "unique_reachable_configurations": len(records),
            "reachable_local_states": [list(s) for s in sorted(set(s for r in records for s in r[0]))],
            "candidate_count": 64,
            "surviving_masks": [c["keep_mask"] for c in candidates if c["witness"] is None],
            "candidates": candidates}


def report():
    return {"schema": 1, "protocol": "nakamura-retention-20260921",
            "protocol_freeze_commit": "5b54f39", "review": "none; explicit solo authorization",
            "source_hashes": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in INPUTS},
            "domain": {"ring": 5, "prefix": "each site zero or one updates",
                       "initial_ages": [0, 1, 2], "readout": "current and age exactly preserved"},
            "rules": {str(r): audit_rule(r) for r in (110, 204)}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", nargs="?", const=str(OUT), metavar="FILE")
    args = parser.parse_args()
    actual = report()
    if args.check:
        saved = json.loads(Path(args.check).read_text())
        for r, result in saved["rules"].items():
            for candidate in result["candidates"]:
                if candidate["witness"]:
                    check_witness(candidate["witness"], int(r), candidate["keep_mask"])
        require(saved == actual, "canonical result differs from deterministic replay")
    elif args.write:
        OUT.write_text(json.dumps(actual, indent=2) + "\n")
    print(json.dumps({r: {"surviving_masks": value["surviving_masks"],
                         "reachable_local_states": len(value["reachable_local_states"]),
                         "prefixes": value["unique_reachable_configurations"],
                         "diamonds": value["local_diamonds"]}
                      for r, value in actual["rules"].items()}))


if __name__ == "__main__":
    main()
