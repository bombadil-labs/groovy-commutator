#!/usr/bin/env python3
"""Summarize the Groovy-field suite outputs into results/groovy_field_20260922/summary.json.

Includes sanity checks that must hold if the data are right:
* mirror-image rules have identical G-only and burn-in verdicts;
* retaining the source (track 204) closes every rule at k = 1;
* unresolved and decider-only verdicts are counted, not silently promoted.
"""
from __future__ import annotations

import hashlib
import argparse
import json
from collections import Counter
from pathlib import Path
from groovy_field_suite import output_path, write_record

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "results" / "groovy_field_20260922"
SOURCES = ["src/groovy/groovy_field.py", "scripts/groovy_field_suite.py",
           "scripts/groovy_field_rule110_lift.py", "scripts/groovy_field_summarize.py",
           "scripts/groovy_field_followups.py"]


def load(name):
    return json.loads((DIR / f"{name}.json").read_text())["data"]


def mirror(rule):
    out = 0
    for i in range(8):
        l, c, r = (i >> 2) & 1, (i >> 1) & 1, i & 1
        if (rule >> i) & 1:
            out |= 1 << (4 * r + 2 * c + l)
    return out


def g_uniform(rule, c):
    """G on the uniform configuration c^Z (a D0 computation)."""
    u = lambda x: (rule >> (7 * x)) & 1          # phi(xxx)
    e = u(c)
    return e ^ u(e) ^ u(c ^ e)


def min_k(entry):
    for k in (1, 2, 3, 4):
        v = entry.get(f"k{k}")
        if v is None:
            break
        if v["verdict"] == "L":
            return k
        if v["verdict"] in ("T", "?"):
            return f"unresolved at k={k}"
    return ">4"


def main():
    global DIR
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input-dir", type=Path, default=DIR)
    ap.add_argument("--output-dir", type=Path, default=DIR)
    args = ap.parse_args()
    path = output_path(args.output_dir, "summary.json")
    DIR = args.input_dir
    val, t110, tax, cen, rea = (load(n) for n in ("validate", "tracks110", "taxonomy", "census", "reachable"))
    lift = json.loads((DIR / "rule110_lift.json").read_text())
    S = {"sanity": {}}

    S["sanity"]["validate_consistent"] = all(x[k]["consistent"] for x in val.values() for k in x)
    S["sanity"]["validate_uncertified"] = sum(x[k]["verdict"] in "?T" for x in val.values() for k in x)

    gk = {int(r): min_k(x["G_only"]) for r, x in cen.items()}
    S["sanity"]["mirror_G_only_agree"] = all(gk[r] == gk[mirror(r)] for r in range(256))
    by = {}
    for r, k in gk.items():
        by.setdefault(str(k), []).append(r)
    S["G_only_min_k"] = {k: sorted(v) for k, v in sorted(by.items())}
    S["G_only_counts"] = {k: len(v) for k, v in sorted(by.items())}

    trk = {int(r): x["tracks"] for r, x in cen.items()}
    S["sanity"]["source_track_closes_k1_everywhere"] = all(trk[r]["k1"]["verdicts"][204] == "L" for r in range(256))
    S["sanity"]["uncertified_track_verdicts"] = sum(
        v in "?T" for x in trk.values() for k in x for v in x[k]["verdicts"])
    first = {}
    for r in range(256):
        m = next((k for k in ("k1", "k2", "k3") if k in trk[r] and "L" in trk[r][k]["verdicts"]), "none<=3")
        first[r] = m
    S["one_track_min_k"] = dict(Counter(first.values()))
    S["rules_needing_k3_or_more_with_best_track"] = sorted(r for r, m in first.items() if m not in ("k1",))
    nontrivial = [r for r in range(256)]
    for k in ("k1", "k2"):
        closing = [set(i for i, v in enumerate(trk[r][k]["verdicts"]) if v == "L") for r in nontrivial]
        univ = set.intersection(*closing)
        S[f"universal_tracks_{k}"] = sorted(univ)
    # rules whose G fails at k=1 but a single track closes at k=1 besides the source
    S["closing_tracks_k1_count"] = {r: trk[r]["k1"]["verdicts"].count("L") for r in range(256)}
    named = {"source_204": 204, "run111_128": 128, "run000_1": 1, "pair11_136": 136}
    S["named_tracks"] = {}
    for name, tr in named.items():
        S["named_tracks"][name] = {k: sum(trk[r][k]["verdicts"][tr] == "L" for r in range(256)) for k in ("k1", "k2")}
    S["named_tracks"]["D_rule^204"] = {k: sum(trk[r][k]["verdicts"][r ^ 204] == "L" for r in range(256))
                                       for k in ("k1", "k2")}

    # D0: does G separate the two uniform configurations?
    sep = {r: g_uniform(r, 0) != g_uniform(r, 1) for r in range(256)}
    S["D0"] = {}
    for flag in (True, False):
        rules = [r for r in range(256) if sep[r] == flag]
        S["D0"]["G_separates_uniform" if flag else "G_blind_to_uniform"] = {
            "rules": len(rules),
            "G_only_min_k": dict(Counter(str(gk[r]) for r in rules))}

    kinds1, kindsmax = Counter(), Counter()
    for r, x in tax.items():
        ks = [k for k in ("k1", "k2", "k3", "k4")
              if isinstance(x.get(k), dict) and "kind" in x[k]]
        if ks:
            kinds1[x[ks[0]]["kind"] if ks[0] == "k1" else "none"] += 1
            kindsmax[x[ks[-1]]["kind"]] += 1
    S["witness_kinds_G_only_k1"] = dict(kinds1)
    S["witness_kinds_G_only_last_failing_k"] = dict(kindsmax)
    S["rule110_tracks_k2_failure_kinds"] = dict(Counter(
        v["kind"] if isinstance(v, dict) else v for v in tax["110"]["tracks_k2"].values()))

    rk = {}
    for r, x in rea.items():
        def mk(t):
            for k in (1, 2, 3):
                v = x.get(f"t{t}k{k}")
                if v is None:
                    return "unresolved"
                if v["verdict"] == "L":
                    return k
                if v["verdict"] in "?T":
                    return f"unresolved at k={k}"
            return ">3"
        rk[int(r)] = (mk(1), mk(2))
    S["sanity"]["mirror_reachable_agree"] = all(rk[r] == rk[mirror(r)] for r in range(256))
    for t in (1, 2):
        S[f"burn_in_helps_rules_t{t}"] = sorted(r for r in range(256)
            if isinstance(rk[r][t-1], int)
            and (not isinstance(gk[r], int) or rk[r][t-1] < gk[r]))
    S["burn_in_min_k_t1"] = dict(Counter(str(v[0]) for v in rk.values()))
    S["burn_in_min_k_t2"] = dict(Counter(str(v[1]) for v in rk.values()))

    c110 = Counter(x["k1"]["verdict"] for x in t110.values())
    S["rule110"] = {
        "G_only": cen["110"]["G_only"],
        "tracks_k1": dict(c110),
        "tracks_k2": dict(Counter(x["k2"]["verdict"] for x in t110.values())),
        "tracks_k3": dict(Counter(x["k3"]["verdict"] for x in t110.values())),
        "tracks_never_k_le_3": sorted(int(t) for t, x in t110.items()
                                      if "L" not in (x["k1"]["verdict"], x["k2"]["verdict"], x["k3"]["verdict"])),
        "reachable": rea["110"],
        "lift": {k: lift[k] for k in ("table_realized_patterns", "autonomous_simulation", "ring_quotient")},
    }
    S["schema"] = "groovy-field-summary-v2"
    # These are the summarizer's sources, not the sources that generated old inputs.
    S["summary_source_hashes"] = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in SOURCES}
    S["input_hashes"] = {f"{n}.json": hashlib.sha256((DIR / f"{n}.json").read_bytes()).hexdigest()
                         for n in ("validate", "tracks110", "taxonomy", "census", "reachable", "rule110_lift")}
    write_record(path, S)
    print(json.dumps({k: v for k, v in S.items() if k not in ("closing_tracks_k1_count", "summary_source_hashes")}, indent=1)[:6000])


if __name__ == "__main__":
    main()
