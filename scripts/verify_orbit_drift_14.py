#!/usr/bin/env python3
"""Hash and saved-cycle accounting only: no CA transition or graph enumeration."""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import hashlib
import io
import json
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = "experiments/orbit_drift_14_20260914/run"
RESULT = "results/orbit_drift_14_20260914.json"
INPUTS = ["scripts/orbit_drift_14.py", "src/groovy/ca.py",
          "docs/research/protocols/orbit-drift-20260914.md",
          "scripts/verify_orbit_drift_14.py",
          "review/orbit_drift_independent_review.py", "review/orbit_drift_independent_review.json",
          *(f"{RUN}/{p}" for p in ("cycles.json", "annotations.csv", "execution.json"))]
COLUMNS = ["rule", "n", "representative", "word_cell_0_first", "p", "d", "q",
           "a", "a_signed", "m", "family_representative", "family_cycle_count"]


def need(ok, why):
    if not ok:
        raise ValueError(why)


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def shift(s, a):
    return sum(((s >> ((i + a) % 14)) & 1) << i for i in range(14))


def quantities(c):
    s, p = c[0], len(c)
    d = next(a for a in range(1, 15) if shift(s, a) == s)
    rotations = {shift(s, a): a for a in range(d)}
    q = next(t for t in range(1, p + 1) if c[t % p] in rotations)
    a = rotations[c[q % p]]
    m = d // gcd(d, a)
    need(p == q * m, "period factorization")
    return dict(p=p, d=d, q=q, a=a, a_signed=a if 2*a <= d else a-d, m=m)


def account():
    data = json.loads((ROOT / RUN / "cycles.json").read_text())
    run = json.loads((ROOT / RUN / "execution.json").read_text())
    need(data["n"] == 14 and data["target_periods"] == {"110": 91, "54": 112}, "fixed domain")
    need(run["status"] == "completed", "incomplete evaluation")
    need(run["elapsed_seconds"] <= 60 and run["peak_rss_mib"] <= 512, "budget violation")
    for p, digest in run["source_sha256"].items():
        need(sha(p) == digest, f"execution source hash: {p}")
    for p, digest in run["artifact_sha256"].items():
        need(sha(f"{RUN}/{p}") == digest, f"execution artifact hash: {p}")
    review = json.loads((ROOT / "review/orbit_drift_independent_review.json").read_text())
    need(review["status"] == "passed" and review["reviewed_implementation_commit"] == run["implementation_commit"], "independent review pin")
    for p, digest in review["inputs_sha256"].items():
        need(sha(p) == digest, f"review input hash: {p}")
    expected_controls = [(170, 1, [14, 14, 1, 1]), (204, 1, [1, 14, 1, 0]),
                         (170, 5461, [2, 2, 1, 1])]
    need(len(run["controls"]) == 3, "control count")
    for control, (rule, seed, expected) in zip(run["controls"], expected_controls):
        need(control["rule"] == rule and control["seed"] == seed and control["passed"], "control identity")
        need(control["expected"] == expected, "control expected values")
        need([control["quantities"][k] for k in ("p", "d", "q", "a")] == expected, "control record")
    need([r["rule"] for r in data["rules"]] == [110, 54], "rule cohort")
    targets, spectra, cycle_count, periodic_states = {}, {}, 0, 0
    for rule_data in data["rules"]:
        rule = rule_data["rule"]
        need(rule_data["successors_cross_checked"] == 16384, "scalar check count")
        spectrum, seen = Counter(), set()
        for c in rule_data["cycles"]:
            states, p = c["states"], c["p"]
            need(len(states) == p and len(set(states)) == p, "primitive cycle size")
            need(all(type(s) is int and 0 <= s < 16384 for s in states), "state domain")
            need(c["representative"] == states[0] == min(states), "canonical representative")
            need(not seen.intersection(states), "overlapping temporal cycles")
            seen.update(states)
            spectrum[str(p)] += 1
            if p == data["target_periods"][str(rule)]:
                targets[rule, states[0]] = states
        need(dict(spectrum) == rule_data["spectrum"], "saved spectrum")
        need(rule_data["reported_spectrum_matches"] == (dict(spectrum) == rule_data["reported_spectrum"]), "spectrum comparison")
        spectra[str(rule)] = dict(spectrum)
        cycle_count += len(rule_data["cycles"])
        periodic_states += len(seen)
    keys = [(a["rule"], a["representative"]) for a in data["annotations"]]
    need(len(keys) == len(set(keys)) and set(keys) == set(targets), "complete target annotations")
    families = Counter()
    for row in data["annotations"]:
        c = targets[row["rule"], row["representative"]]
        expected = quantities(c)
        need(all(row[k] == v for k, v in expected.items()), "saved decomposition")
        need(row["word_cell_0_first"] == "".join(str((c[0] >> i) & 1) for i in range(14)), "word convention")
        need(row["n"] == 14 and row["phase_checks"] == len(c), "annotation domain")
        for t in range(len(c)):
            need(quantities(c[t:] + c[:t]) == expected, "phase invariance")
        family = min(shift(s, a) for s in c for a in range(14))
        need(row["family_representative"] == family, "rotation family")
        families[row["rule"], family] += 1
        q, a = row["q"], row["a"]
        need(row["witness"] == dict(initial=c[0], after_q=c[q % len(c)],
                                    translated_initial=shift(c[0], a),
                                    first_q_steps=[c[t % len(c)] for t in range(q + 1)]), "exact witness")
    for row in data["annotations"]:
        need(row["family_cycle_count"] == families[row["rule"], row["family_representative"]], "family cycle count")
    buf = io.StringIO(newline="")
    writer = csv.DictWriter(buf, fieldnames=COLUMNS, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(data["annotations"])
    need(buf.getvalue().encode() == (ROOT / RUN / "annotations.csv").read_bytes(), "CSV differs from saved annotations")
    return dict(schema=1, source_hashes={p: sha(p) for p in INPUTS},
                implementation_commit=run["implementation_commit"],
                summary=dict(n=14, rules=[110, 54], all_cycle_count=cycle_count,
                             all_periodic_states=periodic_states, target_cycles=len(targets),
                             target_periodic_states=sum(map(len, targets.values())),
                             rotation_families=len(families), spectra=spectra,
                             reported_spectra_match=all(r["reported_spectrum_matches"] for r in data["rules"]),
                             scalar_successors_checked=sum(r["successors_cross_checked"] for r in data["rules"])),
                timing=dict(elapsed_seconds=run["elapsed_seconds"], peak_rss_mib=run["peak_rss_mib"]),
                annotations=[{k: r[k] for k in COLUMNS} for r in data["annotations"]],
                verification="Automatic tier hashes inputs and checks saved sequences/rotations. It does not execute the CA or establish graph completeness; local author/reviewer enumeration supplies that evidence.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write canonical account from saved data")
    args = parser.parse_args()
    expected = json.dumps(account(), indent=2, sort_keys=True) + "\n"
    path = ROOT / RESULT
    if args.write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(expected)
    else:
        need(path.read_text() == expected, "canonical account differs; inspect the change before regenerating")
    print("OK: provenance and saved-cycle accounting; no CA execution")


if __name__ == "__main__":
    main()
