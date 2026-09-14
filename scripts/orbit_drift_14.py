#!/usr/bin/env python3
"""Frozen N=14, Rules 110/54 orbit annotation. Run locally, never in CI."""
from __future__ import annotations

import argparse
from collections import Counter, deque
import csv
from datetime import datetime, timezone
import hashlib
import json
from math import gcd
from pathlib import Path
import platform
import resource
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from groovy.ca import apply_rule

N = 14
SOURCES = ["scripts/orbit_drift_14.py", "src/groovy/ca.py",
           "docs/research/protocols/orbit-drift-20260914.md"]
REPORTED = {110: {1: 1, 7: 2, 12: 7, 14: 1, 21: 2, 91: 2},
            54: {1: 1, 4: 49, 112: 4}}
TARGET = {110: 91, 54: 112}
COLUMNS = ["rule", "n", "representative", "word_cell_0_first", "p", "d", "q",
           "a", "a_signed", "m", "family_representative", "family_cycle_count"]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def tau(state: int, a: int, n: int = N) -> int:
    """(tau_a S)_i = S_(i+a): positive a moves bits toward lower indices."""
    a %= n
    return ((state >> a) | (state << (n - a))) & ((1 << n) - 1)


def scalar_step(state: int, rule: int, n: int = N) -> int:
    """Independent literal neighborhoods, without the repository lookup helper."""
    out = 0
    for i in range(n):
        left = (state >> ((i - 1) % n)) & 1
        center = (state >> i) & 1
        right = (state >> ((i + 1) % n)) & 1
        out |= ((rule >> (4 * left + 2 * center + right)) & 1) << i
    return out


def decomposition(cycle: list[int]) -> dict:
    p, state = len(cycle), cycle[0]
    if len(set(cycle)) != p:
        raise AssertionError("cycle repeats before its reported period")
    d = next(a for a in range(1, N + 1) if tau(state, a) == state)
    rotations = {tau(state, a): a for a in range(d)}
    q = next(t for t in range(1, p + 1) if cycle[t % p] in rotations)
    a = rotations[cycle[q % p]]
    m = d // gcd(d, a)
    if p != q * m or N % d:
        raise AssertionError("period/drift identity failed")
    return dict(p=p, d=d, q=q, a=a, a_signed=a if 2*a <= d else a-d, m=m)


def extract_cycles(successors: np.ndarray, budget) -> list[list[int]]:
    indegree = np.bincount(successors, minlength=len(successors))
    queue = deque(int(i) for i in np.flatnonzero(indegree == 0))
    pruned = 0
    while queue:
        state = queue.popleft()
        nxt = int(successors[state])
        indegree[nxt] -= 1
        if indegree[nxt] == 0:
            queue.append(nxt)
        pruned += 1
        if pruned % 1024 == 0:
            budget()
    seen = set()
    cycles = []
    for seed in np.flatnonzero(indegree > 0):
        seed = int(seed)
        if seed in seen:
            continue
        cycle, state = [], seed
        while state not in seen:
            seen.add(state)
            cycle.append(state)
            state = int(successors[state])
        if state != seed:
            raise AssertionError("cycle extraction did not close at its seed")
        k = cycle.index(min(cycle))
        cycles.append(cycle[k:] + cycle[:k])
    if len(seen) != int(np.count_nonzero(indegree > 0)):
        raise AssertionError("periodic vertices were omitted")
    return sorted(cycles, key=lambda c: c[0])


def graph(rule: int, budget) -> tuple[list[list[int]], dict]:
    start = time.perf_counter()
    indices = np.arange(1 << N, dtype=np.uint32)
    positions = np.arange(N, dtype=np.uint32)
    bits = ((indices[:, None] >> positions) & 1).astype(np.uint8)
    # apply_rule rolls over the flattened array. Padding protects each word.
    padded = np.concatenate((bits[:, -1:], bits, bits[:, :1]), axis=1)
    updated = apply_rule(padded, rule)[:, 1:-1]
    successors = updated @ (np.uint32(1) << positions)
    budget()
    for state in range(1 << N):
        if int(successors[state]) != scalar_step(state, rule):
            raise AssertionError(f"successor disagreement: rule={rule}, state={state}")
        if state % 1024 == 0:
            budget()
    cycles = extract_cycles(successors, budget)
    budget()
    return cycles, dict(successors_cross_checked=1 << N,
                        successor_sha256=hashlib.sha256(successors.astype("<u4").tobytes()).hexdigest(),
                        graph_and_scalar_check_seconds=time.perf_counter() - start)


def controls(budget) -> list[dict]:
    results = []
    alternating = sum(1 << i for i in range(0, N, 2))
    for rule, seed, expected in [(170, 1, (14, 14, 1, 1)),
                                 (204, 1, (1, 14, 1, 0)),
                                 (170, alternating, (2, 2, 1, 1))]:
        cycle, seen, state = [], set(), seed
        while state not in seen:
            seen.add(state)
            cycle.append(state)
            bits = np.array([(state >> i) & 1 for i in range(N)], dtype=np.uint8)
            nxt = sum(int(bit) << i for i, bit in enumerate(apply_rule(bits, rule)))
            if nxt != scalar_step(state, rule):
                raise AssertionError("control successor disagreement")
            state = nxt
            budget()
        if state != seed:
            raise AssertionError("control is not periodic from its seed")
        quantities = decomposition(cycle)
        if tuple(quantities[k] for k in ("p", "d", "q", "a")) != expected:
            raise AssertionError("known-answer control failed")
        results.append(dict(rule=rule, seed=seed, expected=list(expected),
                            quantities=quantities, passed=True))
    return results


def annotate(rule: int, cycles: list[list[int]], budget) -> list[dict]:
    records = []
    for cycle in cycles:
        if len(cycle) != TARGET[rule]:
            continue
        quantities = decomposition(cycle)
        for phase in range(len(cycle)):
            rotated_time = cycle[phase:] + cycle[:phase]
            if decomposition(rotated_time) != quantities:
                raise AssertionError("decomposition changes with temporal phase")
            budget()
        family = min(tau(s, a) for s in cycle for a in range(N))
        q, a = quantities["q"], quantities["a"]
        records.append(dict(rule=rule, n=N, representative=cycle[0],
                            word_cell_0_first="".join(str((cycle[0] >> i) & 1) for i in range(N)),
                            **quantities, family_representative=family,
                            phase_checks=len(cycle),
                            witness=dict(initial=cycle[0], after_q=cycle[q % len(cycle)],
                                         translated_initial=tau(cycle[0], a),
                                         first_q_steps=[cycle[t % len(cycle)] for t in range(q + 1)])))
    families = Counter(r["family_representative"] for r in records)
    for record in records:
        record["family_cycle_count"] = families[record["family_representative"]]
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--implementation-commit", required=True)
    args = parser.parse_args()
    if len(args.implementation_commit) != 40 or any(c not in "0123456789abcdef" for c in args.implementation_commit):
        parser.error("implementation commit must be a full hexadecimal SHA")
    args.output.mkdir(parents=True, exist_ok=False)
    start = time.perf_counter()
    execution = dict(status="running", implementation_commit=args.implementation_commit,
                     started_utc=datetime.now(timezone.utc).isoformat(),
                     source_sha256={p: sha(ROOT / p) for p in SOURCES},
                     python=platform.python_version(), numpy=np.__version__,
                     platform=platform.platform(), budget_seconds=60, budget_rss_mib=512)
    data = dict(schema=1, n=N, translation="tau_a(S)[i] = S[(i+a) mod 14]",
                target_periods=TARGET, rules=[], annotations=[])

    def budget():
        if time.perf_counter() - start > 60:
            raise RuntimeError("60-second budget exhausted")
        if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 > 512:
            raise RuntimeError("512 MiB RSS budget exhausted")

    try:
        execution["controls"] = controls(budget)
        for rule in (110, 54):
            cycles, metadata = graph(rule, budget)
            spectrum = dict(sorted(Counter(map(len, cycles)).items()))
            data["rules"].append(dict(rule=rule, spectrum=spectrum,
                                      reported_spectrum=REPORTED[rule],
                                      reported_spectrum_matches=spectrum == REPORTED[rule],
                                      cycles=[dict(representative=c[0], p=len(c), states=c) for c in cycles],
                                      **metadata))
            # Preserve the recovered cycle graph before annotation.
            save(args.output / "cycles.json", data)
            data["annotations"].extend(annotate(rule, cycles, budget))
            save(args.output / "cycles.json", data)
        budget()
        execution["status"] = "completed"
    except Exception as exc:
        execution["status"] = "failed"
        execution["failure"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        execution["finished_utc"] = datetime.now(timezone.utc).isoformat()
        execution["elapsed_seconds"] = time.perf_counter() - start
        execution["peak_rss_mib"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
        save(args.output / "cycles.json", data)
        with (args.output / "annotations.csv").open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(data["annotations"])
        execution["artifact_sha256"] = {p: sha(args.output / p) for p in ("cycles.json", "annotations.csv")}
        save(args.output / "execution.json", execution)
        print(json.dumps(dict(status=execution["status"], elapsed_seconds=execution["elapsed_seconds"],
                              peak_rss_mib=execution["peak_rss_mib"],
                              annotations=[{k: r[k] for k in COLUMNS} for r in data["annotations"]]), indent=2))


if __name__ == "__main__":
    main()
