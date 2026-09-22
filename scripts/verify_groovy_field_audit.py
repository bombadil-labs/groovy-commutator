#!/usr/bin/env python3
"""Bounded review replay, not a rerun or recertification of the whole census.

--record writes a fresh correction record; --check replays it; --integrity
checks pinned result and implementation bytes using this unit's manifest.
Positive tables and the finite-ring SCC test use unpacked arithmetic below,
independent of the primary decider's packed arithmetic. No SciPy is required.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "scripts")]
from groovy.groovy_field import decide, witness, verify_witness  # noqa: E402
from groovy_field_rule110_lift import extract_table, lifted_step  # noqa: E402

DIRECTORY = ROOT / "results/groovy_field_20260922"
RECORD = DIRECTORY / "review_audit.json"
MANIFEST = DIRECTORY / "review_manifest.json"
ORIGINAL = "7c55ffa8d9925c5041498c2c7915bb2d51d78a02"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def step(w, rule):
    return tuple((rule >> (4*a + 2*b + c)) & 1 for a, b, c in zip(w, w[1:], w[2:]))


def groovy(w, rule):
    e = step(w, rule)
    d = tuple(a ^ b for a, b in zip(w[1:-1], e))
    return tuple(a ^ b ^ c for a, b, c in zip(e[1:-1], step(e, rule), step(d, rule)))


def centre(w, j, rule=110):
    for _ in range(j):
        w = step(w, rule)
    g = groovy(w, rule)
    return g[len(g)//2]


def matrix_law(rule, k, radius):
    """Exhaustive independent truth-table replay over the complete source cone.

    Digest: sorted unique keys as little-endian uint64, then uint8 outputs.
    Key order is oldest history first, each window left to right.
    """
    length = 2*max(radius+k+1, k+2) + 1
    size = 1 << length
    lut = np.array([(rule >> i) & 1 for i in range(8)], dtype=np.uint8)

    def evolve(w):
        return lut[4*w[:, :-2] + 2*w[:, 1:-1] + w[:, 2:]]

    keys, values = np.zeros(size, np.uint64), np.zeros(size, np.uint8)
    for lo in range(0, size, 65536):
        hi = min(size, lo+65536)
        w = ((np.arange(lo, hi, dtype=np.uint32)[:, None]
              >> np.arange(length-1, -1, -1, dtype=np.uint32)) & 1).astype(np.uint8)
        key = np.zeros(hi-lo, np.uint64)
        for j in range(k+1):
            e = evolve(w)
            g = e[:, 1:-1] ^ evolve(e) ^ evolve(w[:, 1:-1] ^ e)
            c = g.shape[1]//2
            if j < k:
                for i in range(c-radius, c+radius+1):
                    key = (key << 1) | g[:, i]
                w = e
            else:
                values[lo:hi] = g[:, c]
        keys[lo:hi] = key
    order = np.argsort(keys, kind="stable")
    keys, values = keys[order], values[order]
    equal = keys[1:] == keys[:-1]
    if np.any(equal & (values[1:] != values[:-1])):
        raise AssertionError(f"inconsistent independent law: {rule=}, {k=}")
    first = np.r_[True, ~equal]
    raw = keys[first].astype("<u8").tobytes() + values[first].tobytes()
    return {"rule": rule, "k": k, "radius": radius, "source_bits": length,
            "source_windows": size, "realized_patterns": int(first.sum()),
            "table_sha256": hashlib.sha256(raw).hexdigest()}


def finite_ring_certificate():
    """Rule 110, k=3: no differing-next 3-edge path can lie on a cycle.

    A periodic counterexample would be a closed pair-graph walk containing
    such a path. Conversely that path can be closed iff its endpoints share
    an SCC. This proves all finite rings, not a bounded ring enumeration.
    """
    def bits(v, n):
        return tuple((v >> i) & 1 for i in range(n-1, -1, -1))

    histories = [tuple(centre(bits(v, 9), j) for j in range(3)) for v in range(512)]
    groups = defaultdict(list)
    for v, h in enumerate(histories):
        groups[h].append(v)
    adjacency, reverse = defaultdict(list), defaultdict(list)
    for group in groups.values():
        for a in group:
            for b in group:
                start, end = (a >> 1)*256 + (b >> 1), (a & 255)*256 + (b & 255)
                adjacency[start].append(end)
                reverse[end].append(start)
    nodes = sorted(set(adjacency) | set(reverse))
    # Iterative Kosaraju: explicit iterators preserve DFS finishing order.
    seen, finished = set(), []
    for node in nodes:
        if node in seen:
            continue
        seen.add(node)
        stack = [(node, iter(adjacency.get(node, ())))]
        while stack:
            v, children = stack[-1]
            nxt = next(children, None)
            if nxt is None:
                finished.append(v)
                stack.pop()
            elif nxt not in seen:
                seen.add(nxt)
                stack.append((nxt, iter(adjacency.get(nxt, ()))))
    component, count = {}, 0
    for node in reversed(finished):
        if node in component:
            continue
        component[node] = count
        todo = [node]
        while todo:
            for nxt in reverse.get(todo.pop(), ()):
                if nxt not in component:
                    component[nxt] = count
                    todo.append(nxt)
        count += 1
    signatures = defaultdict(lambda: [[], []])
    for v in range(2048):
        sig = tuple(histories[(v >> shift) & 511] for shift in (2, 1, 0))
        signatures[sig][centre(bits(v, 11), 3)].append(v)
    tested, periodic = 0, 0
    for zeros, ones in signatures.values():
        for a in zeros:
            for b in ones:
                start, end = (a >> 3)*256 + (b >> 3), (a & 255)*256 + (b & 255)
                tested += 2  # the reverse orientation has the same SCC test
                periodic += 2*int(component[start] == component[end])
    if periodic:
        raise AssertionError("periodic Rule-110 memory-3 counterexample")
    return {"rule": 110, "k": 3, "edges": sum(map(len, adjacency.values())),
            "nodes": len(nodes), "strong_components": count,
            "oriented_defect_pairs": tested, "periodic_defect_pairs": periodic}


def ring_step(s, rule):
    n = len(s)
    return tuple((rule >> (4*s[i-1]+2*s[i]+s[(i+1) % n])) & 1 for i in range(n))


def ring_g(s, rule):
    e = ring_step(s, rule)
    return tuple(a ^ b ^ c for a, b, c in zip(e, ring_step(e, rule),
        ring_step(tuple(a ^ b for a, b in zip(s, e)), rule)))


def boundary_examples():
    def string(s):
        return "".join(map(str, s))

    complement = []
    for word in ("001", "110"):
        s = tuple(map(int, word))
        complement.append({"S": word, "gradient": string(ring_step(s, 60)),
                           "G": string(ring_g(s, 110))})
    limit = []
    for word in ("011010", "011100"):
        s = tuple(map(int, word))
        e = ring_step(s, 110)
        orbit = e
        period = 1
        while orbit != s and period <= 64:
            orbit = ring_step(orbit, 110)
            period += 1
        if orbit != s:
            raise AssertionError("limit-set witness is not temporally periodic")
        limit.append({"S": word, "G": string(ring_g(s, 110)),
                      "next_G": string(ring_g(e, 110)), "temporal_period": period})
    s = (0, 0, 1)
    def observation(w):
        return tuple(np.array(v, dtype=np.uint8) for v in (ring_g(w, 110), ring_step(w, 128)))
    a, b = observation(s), observation(ring_step(s, 110))
    table = extract_table()
    ba, bb = lifted_step(a, b, table)
    da = tuple(x ^ y for x, y in zip(a, ba))
    db = tuple(x ^ y for x, y in zip(b, bb))
    try:
        lifted_step(da, db, table)
    except KeyError:
        undefined = True
    else:
        undefined = False
    if not undefined:
        raise AssertionError("off-image example unexpectedly defined")
    return {"complement_split": complement, "limit_set_k1": limit,
            "native_G_boundary": {"source": string(s), "Z": list(map(string, a+b)),
                "B_Z": list(map(string, ba+bb)), "D_B_Z": list(map(string, da+db)),
                "B_D_B_Z_undefined": undefined, "table_patterns": len(table)}}


def build_record(selected=None):
    census = json.loads((DIRECTORY / "census.json").read_text())["data"]
    retained = []
    for rule, data in census.items():
        rec = data["G_only"]["k1"]
        if "witness" not in rec:
            continue
        wit = {**rec["witness"], "left_period": rec["periods"][0], "right_period": rec["periods"][1]}
        if not verify_witness(int(rule), (), 1, 0, wit)["verified"]:
            raise AssertionError(f"invalid retained witness for {rule}")
        retained.append(int(rule))
    if selected is None:
        selected = [{"rule": rule, "k": k, "tracks": [], "t": 0,
                     "witness": witness(decide(rule, (), k, 0))}
                    for rule, ks in ((30, (1, 2)), (54, (1, 2, 3, 4)), (110, (3, 5))) for k in ks]
    for rec in selected:
        if not verify_witness(rec["rule"], rec["tracks"], rec["k"], rec["t"], rec["witness"])["verified"]:
            raise AssertionError("invalid selected witness")
    return {"schema": "groovy-field-review-audit-v1", "original_commit": ORIGINAL,
            "scope": "bounded replay; no recertification of unretained census witnesses",
            "retained_k1_witnesses_verified": sorted(retained), "selected_witnesses": selected,
            "independent_laws": [matrix_law(30, 3, 6), matrix_law(54, 5, 4)],
            "finite_ring_proof": finite_ring_certificate(), "boundaries": boundary_examples()}


def integrity():
    manifest = json.loads(MANIFEST.read_text())
    for path, expected in manifest["sha256"].items():
        if digest(ROOT / path) != expected:
            raise AssertionError(f"integrity mismatch: {path}")
    summary = json.loads((DIRECTORY / "summary.json").read_text())
    if summary["source_hashes"] != manifest["original_source_hashes"]:
        raise AssertionError("original source-hash record changed")
    print("Groovy-field unit integrity passed (byte provenance, not a scientific proof).")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--record", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--integrity", action="store_true")
    args = ap.parse_args()
    if args.integrity:
        integrity()
    elif args.record:
        if RECORD.exists():
            raise FileExistsError(RECORD)
        record = build_record()
        with RECORD.open("x") as f:
            f.write(json.dumps(record, indent=2, sort_keys=True) + "\n")
        print("Recorded bounded audit:", RECORD.relative_to(ROOT))
    else:
        integrity()
        expected = json.loads(RECORD.read_text())
        if build_record(expected["selected_witnesses"]) != expected:
            raise AssertionError("review audit replay differs")
        print("Replay passed: 220 retained witnesses, 8 selected witnesses, two exhaustive laws, SCC proof and boundary examples.")


if __name__ == "__main__":
    main()
