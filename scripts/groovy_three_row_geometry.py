#!/usr/bin/env python3
"""Bounded raw-three-row phase test; a negative certifies an infinite-plane fact.

The search uses the repository's numpy CA engine. Certificate verification
uses an independent scalar Boolean expression for Rule 30, with periodic
indexing. --record refuses overwrite; --check verifies pinned bytes and the
stored certificate, then replays the bounded search (never a broad census).
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import resource
import signal
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from groovy.ca import apply_rule  # noqa: E402

PROTOCOL = "docs/research/protocols/groovy-three-row-geometry-20260922.md"
PROTOCOL_COMMIT = "5fdd92803f74cecae8e429a61025506bd0197073"
INSPECTED_MAIN = "a8dee2d0510f22e7f992a65346e3167cd64ac2dd"
RECORD = ROOT / "results/groovy_three_row_geometry_20260922.json"
PINNED = (PROTOCOL, "scripts/groovy_three_row_geometry.py", "src/groovy/ca.py")
MAX_PERIOD = 12


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def field_rows(word):
    """Four Groovy rows, strings with x increasing from left to right."""
    state = np.array([int(c) for c in word], dtype=np.uint8)
    rows = []
    for _ in range(4):
        evolved = apply_rule(state, 30)
        g = evolved ^ apply_rule(evolved, 30) ^ apply_rule(state ^ evolved, 30)
        rows.append("".join(map(str, g.tolist())))
        state = evolved
    return rows


def rotated(rows, phase):
    """Rows y=0,1,2 after R_phase; rows must contain exactly three strings."""
    return tuple(rows[(y + phase) % 3] for y in range(3))


def periodic_search(max_period=MAX_PERIOD):
    counts = []
    for n in range(1, max_period + 1):
        seen = {}
        phase_cases = 0
        for value in range(1 << n):
            word = format(value, f"0{n}b")
            rows = field_rows(word)
            for phase in range(3):
                phase_cases += 1
                before = rotated(rows[:3], phase)
                after = rotated(rows[1:], phase)
                previous = seen.get(before)
                if previous is not None and previous["after"] != after:
                    old = previous["example"]
                    new = {"source": word, "phase": phase, "g_rows": rows}
                    defect = next([x, y] for y in range(3) for x in range(n)
                                  if previous["after"][y][x] != after[y][x])
                    counts.append({"period": n, "source_words_visited": value + 1,
                                   "phase_cases": phase_cases, "complete": False})
                    return {"status": "whole_plane_collision", "counts": counts,
                            "certificate": {"horizontal_period": n,
                                            "examples": [old, new],
                                            "input_rows": list(before),
                                            "output_rows": [list(previous["after"]),
                                                            list(after)],
                                            "defect_xy": defect}}
                if previous is None:
                    seen[before] = {"after": after,
                                    "example": {"source": word, "phase": phase,
                                                "g_rows": rows}}
        counts.append({"period": n, "source_words_visited": 1 << n,
                       "phase_cases": phase_cases, "complete": True})
    return {"status": "no_collision_within_period_cap", "counts": counts,
            "certificate": None}


def scalar_rows(word):
    """Independent verifier: Rule 30 is left XOR (center OR right)."""
    def step(s):
        n = len(s)
        return tuple(s[(i - 1) % n] ^ (s[i] | s[(i + 1) % n])
                     for i in range(n))

    s = tuple(int(c) for c in word)
    rows = []
    for _ in range(4):
        e = step(s)
        ee = step(e)
        ed = step(tuple(a ^ b for a, b in zip(s, e)))
        rows.append("".join(str(a ^ b ^ c) for a, b, c in zip(e, ee, ed)))
        s = e
    return rows


def verify_certificate(cert):
    """Validate full periodic inputs/targets, rather than a cropped patch."""
    n = cert["horizontal_period"]
    if type(n) is not int or not 1 <= n <= MAX_PERIOD:
        raise ValueError("invalid horizontal period")
    if len(cert["examples"]) != 2:
        raise ValueError("exactly two examples are required")
    inputs, outputs = [], []
    for example in cert["examples"]:
        word, phase = example["source"], example["phase"]
        if (not isinstance(word, str) or len(word) != n or set(word) - {"0", "1"}
                or type(phase) is not int or phase not in (0, 1, 2)):
            raise ValueError("invalid source or phase")
        rows = scalar_rows(word)
        if rows != example["g_rows"]:
            raise ValueError("stored Groovy rows disagree with scalar replay")
        # Explicit indexing, without using the search's rotated helper.
        inputs.append([rows[(y + phase) % 3] for y in range(3)])
        outputs.append([rows[1 + (y + phase) % 3] for y in range(3)])
    if inputs[0] != inputs[1] or inputs[0] != cert["input_rows"]:
        raise ValueError("the two periodic planes are not identical")
    if outputs != cert["output_rows"] or outputs[0] == outputs[1]:
        raise ValueError("required successor planes do not disagree as recorded")
    defect = cert["defect_xy"]
    if (len(defect) != 2 or any(type(v) is not int for v in defect)
            or not (0 <= defect[0] < n and 0 <= defect[1] < 3)):
        raise ValueError("invalid defect coordinate")
    x, y = defect
    if outputs[0][y][x] == outputs[1][y][x]:
        raise ValueError("declared defect does not differ")
    return {"verified": True, "method": "scalar Rule-30 Boolean formula",
            "identical_full_periodic_inputs": True,
            "different_required_successors": True,
            "defect_outputs": [outputs[0][y][x], outputs[1][y][x]],
            "scope": "all finite neighborhoods, via periodic extension to Z^2"}


def evidence():
    search = periodic_search()
    negative = search["status"] == "whole_plane_collision"
    return {"search": search,
            "local_stencil_test": {
                "status": "not_evaluated",
                "reason": ("whole-plane obstruction already excludes every stencil"
                           if negative else "complete-cone implementation required next")},
            "verification": (verify_certificate(search["certificate"])
                             if negative else None)}


def integrity(record):
    expected = {p: sha(ROOT / p) for p in PINNED}
    if record["source_hashes"] != expected:
        raise ValueError("pinned protocol/implementation bytes changed")


def enforce_budget():
    resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))

    def expired(signum, frame):
        raise TimeoutError("120-second evaluation wall budget exhausted")

    signal.signal(signal.SIGALRM, expired)
    signal.alarm(120)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--record", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--integrity", action="store_true")
    args = parser.parse_args()
    if args.record:
        if RECORD.exists():
            raise FileExistsError(f"refusing to overwrite {RECORD}")
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                       text=True).strip()
        for path in PINNED:
            committed = subprocess.check_output(["git", "show", f"{head}:{path}"], cwd=ROOT)
            if committed != (ROOT / path).read_bytes():
                raise ValueError(f"implementation must be committed before evaluation: {path}")
        result = {"schema_version": 1, "rule": 30, "memory": 3,
                  "source_cadence": 1, "vertical_period": 3,
                  "max_horizontal_period": MAX_PERIOD,
                  "protocol_commit": PROTOCOL_COMMIT,
                  "inspected_main": INSPECTED_MAIN, "implementation_commit": head,
                  "source_hashes": {p: sha(ROOT / p) for p in PINNED}}
        enforce_budget()
        try:
            result.update(evidence())
        except (TimeoutError, MemoryError) as exc:
            result.update({"search": {"status": "resource_limit", "reason": str(exc)},
                           "local_stencil_test": {"status": "not_evaluated",
                                                  "reason": "evaluation resource limit"},
                           "verification": None})
        finally:
            signal.alarm(0)
        RECORD.parent.mkdir(exist_ok=True)
        with RECORD.open("x") as file:
            json.dump(result, file, indent=2)
            file.write("\n")
        print(json.dumps(result, indent=2))
    else:
        record = json.loads(RECORD.read_text())
        integrity(record)
        if args.check:
            enforce_budget()
            actual = evidence()
            expected = {k: record[k] for k in ("search", "local_stencil_test", "verification")}
            if actual != expected:
                raise ValueError("bounded replay differs from stored evidence")
            signal.alarm(0)
        print("PASS: pinned bytes" + (" and independent certificate / bounded replay" if args.check else ""))


if __name__ == "__main__":
    main()
