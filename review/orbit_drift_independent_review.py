#!/usr/bin/env python3
"""Independent scalar review of the fixed Rule 110/54, N=14 unit.

No import from the author implementation or CA library. Graph cycles are
reconstructed with path visitation, rather than indegree pruning. Translation
and ECA evolution act on explicit bit lists rather than integer rotations.
Run locally, never as automatic CI.
"""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from math import gcd
from pathlib import Path
import struct
import time

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "experiments/orbit_drift_14_20260914/run"
N = 14


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bits(s):
    return [int(bool(s & (1 << i))) for i in range(N)]


def number(row):
    return sum(value * (2 ** i) for i, value in enumerate(row))


def rotate(s, a):
    row = bits(s)
    a %= N
    return number(row[a:] + row[:a])


def step(s, rule):
    row = bits(s)
    truth = [(rule // (2 ** k)) % 2 for k in range(8)]
    return number([truth[4 * row[(i - 1) % N] + 2 * row[i] + row[(i + 1) % N]]
                   for i in range(N)])


def cycles_by_paths(successors):
    finished = set()
    cycles = []
    for seed in range(len(successors)):
        if seed in finished:
            continue
        trail = []
        positions = {}
        current = seed
        while current not in finished and current not in positions:
            positions[current] = len(trail)
            trail.append(current)
            current = successors[current]
        if current in positions:
            cycle = trail[positions[current]:]
            start = cycle.index(min(cycle))
            cycles.append(cycle[start:] + cycle[:start])
        finished.update(trail)
    assert len(finished) == (1 << N)
    return sorted(cycles, key=lambda cycle: cycle[0])


def phase_quantities(cycle, phase):
    state = cycle[phase]
    p = len(cycle)
    stabilizers = [a for a in range(1, N + 1) if rotate(state, a) == state]
    d = min(stabilizers)
    assert stabilizers == list(range(d, N + 1, d))
    rotations = [rotate(state, a) for a in range(d)]
    assert len(set(rotations)) == d
    matches = [(t, a) for t in range(1, p + 1) for a in range(d)
               if cycle[(phase + t) % p] == rotations[a]]
    q, a = min(matches)
    m = d // gcd(d, a)
    assert p == q * m
    assert matches == [(k * q, (k * a) % d) for k in range(1, m + 1)]
    return dict(p=p, d=d, q=q, a=a, a_signed=a if a <= d/2 else a-d, m=m)


def main():
    started = time.perf_counter()
    saved = json.loads((RUN / "cycles.json").read_text())
    execution = json.loads((RUN / "execution.json").read_text())
    for path, expected in execution["source_sha256"].items():
        assert sha(ROOT / path) == expected, path
    for path, expected in execution["artifact_sha256"].items():
        assert sha(RUN / path) == expected, path
    assert execution["implementation_commit"] == "3d8a5eae255ef8da1a1f1a679889d5891244d037"
    known_answers = [(170, 1, (14, 14, 1, 1)), (204, 1, (1, 14, 1, 0)),
                     (170, sum(1 << i for i in range(0, N, 2)), (2, 2, 1, 1))]
    for rule, state, expected in known_answers:
        cycle = [state]
        while (nxt := step(cycle[-1], rule)) != state:
            assert nxt not in cycle
            cycle.append(nxt)
        quantities = phase_quantities(cycle, 0)
        assert tuple(quantities[k] for k in ("p", "d", "q", "a")) == expected

    evidence = []
    phase_checks = 0
    for rule, target in [(110, 91), (54, 112)]:
        successors = [step(state, rule) for state in range(1 << N)]
        successor_hash = hashlib.sha256(b"".join(struct.pack("<I", s) for s in successors)).hexdigest()
        cycles = cycles_by_paths(successors)
        record = next(r for r in saved["rules"] if r["rule"] == rule)
        assert successor_hash == record["successor_sha256"]
        assert cycles == [r["states"] for r in record["cycles"]]
        spectrum = {str(p): count for p, count in sorted(Counter(map(len, cycles)).items())}
        assert spectrum == record["spectrum"] == record["reported_spectrum"]
        state_to_cycle = {state: cycle[0] for cycle in cycles for state in cycle}
        targets = [c for c in cycles if len(c) == target]
        annotations = [a for a in saved["annotations"] if a["rule"] == rule]
        assert len(targets) == len(annotations)
        reviewed = []
        for cycle in targets:
            annotation = next(a for a in annotations if a["representative"] == cycle[0])
            quantities = phase_quantities(cycle, 0)
            assert all(annotation[k] == v for k, v in quantities.items())
            for phase in range(len(cycle)):
                assert phase_quantities(cycle, phase) == quantities
                phase_checks += 1
            family_members = sorted({state_to_cycle[rotate(cycle[0], a)] for a in range(N)})
            family = min(family_members)
            assert family == annotation["family_representative"]
            assert len(family_members) == annotation["family_cycle_count"]
            q, a = quantities["q"], quantities["a"]
            assert annotation["witness"] == dict(initial=cycle[0], after_q=cycle[q],
                                                  translated_initial=rotate(cycle[0], a),
                                                  first_q_steps=cycle[:q+1])
            reviewed.append(dict(representative=cycle[0], **quantities,
                                 family_representative=family, family_members=family_members))
        evidence.append(dict(rule=rule, graph_states=len(successors),
                             successor_sha256=successor_hash, spectrum=spectrum,
                             total_cycles=len(cycles), periodic_states=sum(map(len, cycles)),
                             annotations=reviewed))
    output = dict(status="passed", reviewer="Codex (OpenAI), /root/orbit_drift_review",
                  reviewed_implementation_commit=execution["implementation_commit"],
                  reviewed_utc=datetime.now(timezone.utc).isoformat(),
                  elapsed_seconds=time.perf_counter()-started,
                  independent_method="Explicit bit-list ECA and translation; path-visitation cycle extraction; every target temporal phase and every spacetime return checked.",
                  author_scientific_imports=False, graphs_cross_checked=2,
                  successor_states_cross_checked=2*(1 << N), known_answer_controls=3,
                  target_temporal_phases_cross_checked=phase_checks,
                  inputs_sha256={"review/orbit_drift_independent_review.py":sha(Path(__file__)),
                      **{str(path.relative_to(ROOT)):sha(path) for path in
                         [RUN / "cycles.json", RUN / "execution.json", RUN / "annotations.csv"]}},
                  rules=evidence)
    path = ROOT / "review/orbit_drift_independent_review.json"
    path.write_text(json.dumps(output, indent=2, sort_keys=True)+"\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
