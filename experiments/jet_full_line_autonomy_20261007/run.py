#!/usr/bin/env python3
"""Exact full-line autonomy of G-anchored commutator jets, and local factor radius.

A reproducible, review-driven descriptive follow-up to the Rule-54 period-four
fiber reinterpretation. This is not a preregistered prediction.

  python experiments/jet_full_line_autonomy_20261007/run.py --output /tmp/jet-autonomy.json

Requires NumPy and the sibling exact Boolean truth-table construction
experiments/jet_gqr_256/jet_algebra.py.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "jet_gqr_256"))
from jet_algebra import local_truth_tables  # noqa: E402

RULES = (30, 54, 62, 110)
MAX_LEVEL = 5
NAMES = ("G", "Q", "R", "A4", "A5")


def source_labels(fields, end_level):
    """The current J_m site label of every complete source edge."""
    r = end_level + 1
    bit_count = 2 * r
    words = np.arange(1 << (bit_count + 1), dtype=np.uint32)
    label = np.zeros(len(words), dtype=np.uint8)
    for k in range(1, end_level + 1):
        kr = k + 1
        sub = (words >> (r - kr)) & ((1 << (2 * kr + 1)) - 1)
        label |= fields[k][sub].astype(np.uint8) << (k - 1)
    return words, label, bit_count


def pair_graph(fields, m):
    words, labels, sbits = source_labels(fields, m)
    nsrc = 1 << sbits
    bins = [words[labels == value] for value in range(1 << m)]
    edge_count = sum(len(b) * len(b) for b in bins)
    source = np.empty(edge_count, dtype=np.int64)
    target = np.empty(edge_count, dtype=np.int64)
    index = 0
    for b in bins:
        n = len(b) ** 2
        a = np.repeat(b, len(b))
        c = np.tile(b, len(b))
        source[index:index + n] = (a.astype(np.int64) & (nsrc - 1)) * nsrc + (
            c.astype(np.int64) & (nsrc - 1)
        )
        target[index:index + n] = (a.astype(np.int64) >> 1) * nsrc + (
            c.astype(np.int64) >> 1
        )
        index += n
    vertices, inverses = np.unique(np.r_[source, target], return_inverse=True)
    es = inverses[:edge_count].astype(np.int32)
    ed = inverses[edge_count:].astype(np.int32)
    return vertices, es, ed, sbits, edge_count


def biinfinite_core(es, ed, n):
    alive = np.ones(n, dtype=bool)
    for _ in range(100):
        kept = alive[es] & alive[ed]
        outgoing = np.bincount(es[kept], minlength=n)
        incoming = np.bincount(ed[kept], minlength=n)
        again = alive & (outgoing > 0) & (incoming > 0)
        if np.array_equal(again, alive):
            break
        alive = again
    else:
        raise RuntimeError("bi-infinite support pruning did not stabilize")
    kept = alive[es] & alive[ed]
    remap = np.full(n, -1, dtype=np.int32)
    remap[alive] = np.arange(int(alive.sum()), dtype=np.int32)
    return alive, remap[es[kept]], remap[ed[kept]]


def exact_full_line_factor(fields, m):
    started = time.monotonic()
    vertices, es, ed, sbits, ecount = pair_graph(fields, m)
    alive, ces, ced = biinfinite_core(es, ed, len(vertices))
    core = vertices[alive]
    base = 1 << sbits
    adjacency = defaultdict(list)
    for a, b in zip(ces.tolist(), ced.tolist()):
        adjacency[a].append(b)

    next_field = fields[m + 1]
    paths = 0
    failures = 0
    first = None
    for v0 in range(len(core)):
        x0 = int(core[v0] // base)
        y0 = int(core[v0] % base)
        for v1 in adjacency.get(v0, ()):
            v = int(core[v1])
            x1 = (v // base) >> (sbits - 1) & 1
            y1 = (v % base) >> (sbits - 1) & 1
            for v2 in adjacency.get(v1, ()):
                v = int(core[v2])
                x2 = (v // base) >> (sbits - 1) & 1
                y2 = (v % base) >> (sbits - 1) & 1
                for v3 in adjacency.get(v2, ()):
                    v = int(core[v3])
                    x3 = (v // base) >> (sbits - 1) & 1
                    y3 = (v % base) >> (sbits - 1) & 1
                    x = x0 | (x1 << sbits) | (x2 << (sbits + 1)) | (x3 << (sbits + 2))
                    y = y0 | (y1 << sbits) | (y2 << (sbits + 1)) | (y3 << (sbits + 2))
                    paths += 1
                    if next_field[x] != next_field[y]:
                        failures += 1
                        if first is None:
                            first = {
                                "source_x_word": x, "source_y_word": y,
                                "next_field_x": int(next_field[x]),
                                "next_field_y": int(next_field[y]),
                            }
    return {
        "jet_end": m, "prefix": list(NAMES[:m]),
        "source_radius": m + 1,
        "equal_label_pair_edges": ecount,
        "biinfinite_pair_vertices": len(core),
        "biinfinite_pair_edges": len(ces),
        "three_edge_paths_checked": paths,
        "next_field_disagreements": failures,
        "first_witness": first,
        "autonomous_full_line": failures == 0,
        "seconds": time.monotonic() - started,
    }


def central_conflicts(fields, m):
    """All differing-next-field pairs with equal current jet on sites -1,0,+1."""
    r = m + 1
    bit_count = 2 * r + 3
    words = np.arange(1 << bit_count, dtype=np.uint32)
    packed = np.zeros(len(words), dtype=np.uint32)
    for site in range(3):
        window = (words >> site) & ((1 << (2 * r + 1)) - 1)
        symbol = np.zeros(len(words), dtype=np.uint32)
        for k in range(1, m + 1):
            kr = k + 1
            sub = (window >> (r - kr)) & ((1 << (2 * kr + 1)) - 1)
            symbol |= fields[k][sub].astype(np.uint32) << (k - 1)
        packed |= symbol << (site * m)

    by_key = defaultdict(lambda: [[], []])
    for word, key in enumerate(packed):
        by_key[int(key)][int(fields[m + 1][word])].append(word)

    left, right = [], []
    for zeros, ones in by_key.values():
        if zeros and ones:
            left.append(np.repeat(np.asarray(zeros, dtype=np.int64), len(ones)))
            right.append(np.tile(np.asarray(ones, dtype=np.int64), len(zeros)))
    if not left:
        return np.zeros(0, dtype=np.int64), np.zeros(0, dtype=np.int64)
    return np.concatenate(left), np.concatenate(right)


def minimum_radius(fields, m, cap=12):
    """Exact first symmetric jet radius for the next residual.

    For central conflicting three-edge pairs, each additional window radius
    needs one equal-J source-pair predecessor and successor edge. Boolean
    reachability in the *unpruned* pair graph is necessary and sufficient.
    """
    vertices, es, ed, sbits, ecount = pair_graph(fields, m)
    base = 1 << sbits
    x, y = central_conflicts(fields, m)
    if len(x) == 0:
        return {"first_passing_radius": 1, "bad_counts_by_radius": [0], "paired_source_edges": ecount}

    first = (x & (base - 1)) * base + (y & (base - 1))
    last = (x >> 3) * base + (y >> 3)
    v0 = np.searchsorted(vertices, first)
    v3 = np.searchsorted(vertices, last)
    assert np.all(vertices[v0] == first)
    assert np.all(vertices[v3] == last)

    left = np.ones(len(vertices), dtype=bool)
    right = np.ones(len(vertices), dtype=bool)
    counts = []
    radius = None
    for t in range(cap):
        surviving = int(np.count_nonzero(left[v0] & right[v3]))
        counts.append(surviving)
        if surviving == 0:
            radius = t + 1
            break
        left = np.bincount(ed, weights=left[es].astype(np.uint8), minlength=len(vertices)) > 0
        right = np.bincount(es, weights=right[ed].astype(np.uint8), minlength=len(vertices)) > 0
    return {
        "first_passing_radius": radius,
        "bad_counts_by_radius": counts,
        "paired_source_edges": ecount,
        "meaning": "exact minimum on admissible jet image; None means not resolved within cap",
    }


def periodic_ring_check(rule, n):
    states = np.arange(1 << n, dtype=np.uint32)
    bits = ((states[:, None] >> np.arange(n, dtype=np.uint32)) & 1).astype(np.uint8)
    local = 4 * np.roll(bits, 1, axis=1) + 2 * bits + np.roll(bits, -1, axis=1)
    lookup = np.array([(rule >> i) & 1 for i in range(8)], dtype=np.uint8)
    step = (lookup[local].astype(np.uint64) * (1 << np.arange(n, dtype=np.uint64))).sum(axis=1).astype(np.uint32)
    jet = [states ^ step]
    for _ in range(6):
        a = jet[-1]
        jet.append(a[step] ^ step[a])
    rows = []
    for m in range(1, 6):
        prefix = np.stack(jet[1:m + 1], axis=1)
        next_prefix = np.column_stack([prefix, jet[m + 1]])
        distinct = len(np.unique(prefix, axis=0))
        after = len(np.unique(next_prefix, axis=0))
        rows.append({"end_level": m, "split_classes": after - distinct, "closed": after == distinct})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    result = {
        "schema": "jet-full-line-autonomy-v1",
        "date": "2026-10-07",
        "protocol": "docs/research/protocols/jet-full-line-autonomy-20261007.md",
        "provenance": "post-exploratory exact reproduction; not a prospective prediction",
        "rules": {},
        "ring_control": {},
    }
    for rule in RULES:
        fields = local_truth_tables(rule, 6)
        rows = [exact_full_line_factor(fields, m) for m in range(1, 6)]
        first = next((x["jet_end"] for x in rows if x["autonomous_full_line"]), None)
        radius = minimum_radius(fields, first) if first is not None else None
        result["rules"][str(rule)] = {
            "full_line_prefixes": rows,
            "first_autonomous_prefix": first,
            "minimum_local_radius": radius,
        }
        result["ring_control"][str(rule)] = {
            str(n): periodic_ring_check(rule, n)
            for n in (8, 10, 12, 14, 16)
        }
        print(
            f"Rule {rule}: first whole-line autonomous G-prefix={first},"
            f" radius={None if radius is None else radius['first_passing_radius']},"
            f" core paths={[r['three_edge_paths_checked'] for r in rows]}",
            flush=True,
        )
    result["summary"] = {
        "first_autonomous_prefix": {
            key: value["first_autonomous_prefix"] for key, value in result["rules"].items()
        },
        "minimum_local_radius": {
            key: None if value["minimum_local_radius"] is None
            else value["minimum_local_radius"]["first_passing_radius"]
            for key, value in result["rules"].items()
        },
    }
    result["source_hashes"] = {
        "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "algebra_sha256": hashlib.sha256((ROOT / "experiments/jet_gqr_256/jet_algebra.py").read_bytes()).hexdigest(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
