#!/usr/bin/env python3
"""Finite-width packing and transverse-freedom diagnostic.

Implements the frozen 2026-09-11 protocol after Claude/Fable Gate-1 approval.
The theorem controls (T1--T3 plus closed-form strip controls) are available via
``--controls-only`` and do not execute the bounded T4 primary diagnostic.

Primary T4 domain:
  n = 6..12
  completions = H128, H160
  coordinates = K, O
  depths h = 0..4
  inherited Rule32 first-image family only

The implementation uses exact finite-ring integer bitsets. Bit position i is
site i; left/right neighbors wrap modulo n. Counts and partitions are invariant
to this internal site-label convention.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/transverse_freedom_20260911.json"
PROTOCOL = ROOT / "docs/research/protocols/transverse-freedom-20260911.md"
RINGS = tuple(range(6, 13))
COMPLETIONS = (128, 160)
KINDS = ("K", "O")
DEPTHS = tuple(range(5))


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ring_step(state: int, n: int, rule: int) -> int:
    """Exact ECA update on an n-ring, site i stored in bit i."""
    out = 0
    for i in range(n):
        left = (state >> ((i - 1) % n)) & 1
        center = (state >> i) & 1
        right = (state >> ((i + 1) % n)) & 1
        code = (left << 2) | (center << 1) | right
        out |= ((rule >> code) & 1) << i
    return out


def pair_xor(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a[0] ^ b[0], a[1] ^ b[1]


def first_image(source: int, n: int) -> tuple[int, int]:
    """E(S)=(D(S),G(S)) on the periodic ring for Rule32."""
    fs = ring_step(source, n, 32)
    d = source ^ fs
    d_fs = fs ^ ring_step(fs, n, 32)
    f_d = ring_step(d, n, 32)
    g = d_fs ^ f_d
    return d, g


def make_ops(n: int, top: int):
    @lru_cache(maxsize=None)
    def H(pair: tuple[int, int]) -> tuple[int, int]:
        u, v = pair
        return ring_step(u, n, 32) ^ v, ring_step(v, n, top)

    @lru_cache(maxsize=None)
    def A(j: int, pair: tuple[int, int]) -> tuple[int, int]:
        if j == 0:
            return pair_xor(pair, H(pair))
        return pair_xor(A(j - 1, H(pair)), H(A(j - 1, pair)))

    @lru_cache(maxsize=None)
    def Hpow(j: int, pair: tuple[int, int]) -> tuple[int, int]:
        cur = pair
        for _ in range(j):
            cur = H(cur)
        return cur

    @lru_cache(maxsize=None)
    def O(j: int, pair: tuple[int, int]) -> tuple[int, int]:
        return A(0, Hpow(j, pair))

    return H, A, O


def tuple_key(rows: list[tuple[int, int]]) -> tuple[int, ...]:
    out: list[int] = []
    for u, v in rows:
        out.extend((u, v))
    return tuple(out)


def partition_signature(values: list[tuple[int, ...]]) -> tuple[int, ...]:
    """Canonical equality-partition label sequence in encounter order."""
    label: dict[tuple[int, ...], int] = {}
    out: list[int] = []
    for value in values:
        if value not in label:
            label[value] = len(label)
        out.append(label[value])
    return tuple(out)


def t1_controls() -> list[dict]:
    """Small exact pack/unpack indexing controls; T1 itself is analytic."""
    checks = []
    alphabet = 3
    n = 5
    for w in (1, 2, 3, 4):
        rows = [[(11 * y + 7 * x + 2) % alphabet for x in range(n)] for y in range(w)]
        packed = [tuple(rows[y][x] for y in range(w)) for x in range(n)]
        unpacked = [[packed[x][y] for x in range(n)] for y in range(w)]
        ok = unpacked == rows
        if not ok:
            raise AssertionError(("T1 pack roundtrip", w))
        checks.append({"alphabet_size": alphabet, "ring": n, "width": w, "roundtrip": True})
    return checks


def t2_controls() -> list[dict]:
    """Declared exact finite samples of the analytic capacity inequality."""
    rows = []
    A = 4
    q = 4
    for K in (1, 2):
        for n in (3, 5):
            for w in (1, 2, 3, 4):
                source = A ** (w * n)
                target = q ** (K * n)
                fits = source <= target
                expected = w <= K
                if fits != expected:
                    raise AssertionError(("T2 sample", K, n, w, source, target))
                rows.append({
                    "source_alphabet": A,
                    "target_alphabet": q,
                    "K": K,
                    "ring": n,
                    "width": w,
                    "source_states": source,
                    "target_capacity": target,
                    "fits_capacity": fits,
                })
    return rows


def strip_controls() -> list[dict]:
    """Tiny enumerations checking independent/duplicated-row closed forms."""
    rows = []
    for n in (2, 3):
        base = 4 ** n
        for w in (1, 2, 3):
            independent_expected = 4 ** (w * n)
            independent_seen = len({x for x in range(independent_expected)})
            duplicated_seen = len({tuple([x] * w) for x in range(base)})
            if independent_seen != independent_expected or duplicated_seen != base:
                raise AssertionError(("strip controls", n, w))
            rows.append({
                "ring": n,
                "width": w,
                "independent_count": independent_seen,
                "independent_closed_form": independent_expected,
                "duplicated_count": duplicated_seen,
                "duplicated_closed_form": base,
            })
    return rows


def controls_only() -> dict:
    return {
        "T1_column_pack": t1_controls(),
        "T2_capacity_samples": t2_controls(),
        "strip_closed_forms": strip_controls(),
        "status": "all theorem/indexing controls passed; T4 primary diagnostic not executed",
    }


def base_family(n: int) -> tuple[list[tuple[int, int]], dict[tuple[int, int], list[int]]]:
    fibers: dict[tuple[int, int], list[int]] = {}
    for source in range(1 << n):
        x = first_image(source, n)
        fibers.setdefault(x, []).append(source)
    return sorted(fibers), fibers


def cell_metrics(values: list[tuple[int, ...]], b_count: int, n: int, h: int) -> dict:
    c_count = len(set(values))
    if c_count > b_count:
        raise AssertionError(("T3 source bound", n, h, c_count, b_count))
    log_c = math.log2(c_count) if c_count else float("-inf")
    log_b = math.log2(b_count) if b_count else float("-inf")
    return {
        "B_count": b_count,
        "C_count": c_count,
        "information_rate_bits_per_longitudinal_site": log_c / n,
        "nominal_represented_bits_per_site": 2 * (h + 1),
        "log2_C_over_log2_B": (log_c / log_b) if b_count > 1 else None,
    }


def evaluate_ring(n: int) -> dict:
    B, fibers = base_family(n)
    b_count = len(B)
    if b_count > (1 << n):
        raise AssertionError(("B source bound", n, b_count))

    by_top: dict[int, dict] = {}
    raw: dict[tuple[int, str, int], list[tuple[int, ...]]] = {}

    for top in COMPLETIONS:
        _, A, O = make_ops(n, top)
        top_data = {"K": {}, "O": {}}
        previous_counts = {"K": None, "O": None}
        for kind in KINDS:
            for h in DEPTHS:
                vals = []
                for x in B:
                    rows = [(A(j, x) if kind == "K" else O(j, x)) for j in range(h + 1)]
                    vals.append(tuple_key(rows))
                raw[(top, kind, h)] = vals
                metrics = cell_metrics(vals, b_count, n, h)
                prev = previous_counts[kind]
                if prev is not None and metrics["C_count"] < prev:
                    raise AssertionError(("T4 monotonicity", n, top, kind, h, prev, metrics["C_count"]))
                previous_counts[kind] = metrics["C_count"]
                top_data[kind][str(h)] = metrics
        by_top[top] = top_data

    controls = []
    for top in COMPLETIONS:
        for h in DEPTHS:
            ksig = partition_signature(raw[(top, "K", h)])
            osig = partition_signature(raw[(top, "O", h)])
            if ksig != osig:
                raise AssertionError(("K/O partition", n, top, h))
            controls.append({"type": "K_O_same_partition", "completion": top, "h": h, "ok": True})

    for kind in KINDS:
        for h in DEPTHS:
            s128 = partition_signature(raw[(128, kind, h)])
            s160 = partition_signature(raw[(160, kind, h)])
            if s128 != s160:
                raise AssertionError(("completion partition", n, kind, h))
            controls.append({"type": "H128_H160_same_partition", "kind": kind, "h": h, "ok": True})

    for h in DEPTHS:
        if raw[(128, "O", h)] != raw[(160, "O", h)]:
            raise AssertionError(("O literal completion independence", n, h))
        controls.append({"type": "O_literal_equal", "h": h, "ok": True})

    source_fiber_hist: dict[str, int] = {}
    for preimages in fibers.values():
        k = str(len(preimages))
        source_fiber_hist[k] = source_fiber_hist.get(k, 0) + 1

    return {
        "n": n,
        "binary_source_states": 1 << n,
        "B_count": b_count,
        "B_source_fiber_histogram": dict(sorted(source_fiber_hist.items(), key=lambda kv: int(kv[0]))),
        "cells": {str(top): by_top[top] for top in COMPLETIONS},
        "controls": controls,
    }


def git_last_change(path: Path) -> str | None:
    env_key = "TRANSVERSE_FREEDOM_IMPLEMENTATION_COMMIT" if path.resolve() == Path(__file__).resolve() else None
    if env_key and env_key in os.environ:
        return os.environ[env_key]
    try:
        rel = str(path.resolve().relative_to(ROOT.resolve()))
        return subprocess.check_output(["git", "-C", str(ROOT), "log", "-1", "--format=%H", "--", rel], text=True).strip() or None
    except Exception:
        return None


def run_full() -> dict:
    controls = controls_only()
    rings = [evaluate_ring(n) for n in RINGS]

    counts = []
    for ring in rings:
        for top in COMPLETIONS:
            for kind in KINDS:
                for h in DEPTHS:
                    counts.append(ring["cells"][str(top)][kind][str(h)]["C_count"])
    if len(counts) != 140:
        raise AssertionError(("cell count", len(counts)))

    result = {
        "protocol": "finite-width packing and transverse freedom — 2026-09-11",
        "implementation_commit": git_last_change(Path(__file__)),
        "source_hashes": {
            "script": sha_file(Path(__file__)),
            "protocol": sha_file(PROTOCOL),
        },
        "frozen_domain": {
            "rings": list(RINGS),
            "completions": list(COMPLETIONS),
            "coordinates": list(KINDS),
            "depths": list(DEPTHS),
            "domain": "inherited Rule32 first-image family only",
        },
        "theorem_controls": controls,
        "rings": rings,
        "summary": {
            "ring_count": len(rings),
            "diagnostic_cells": len(counts),
            "all_controls_passed": True,
            "max_C_count": max(counts),
            "min_C_count": min(counts),
            "interpretation": "bounded exact image-count diagnostic; theorem controls T1-T3 remain analytic statements",
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, sort_keys=True, indent=2, allow_nan=False) + "\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls-only", action="store_true", help="run theorem/indexing controls only; do not execute T4 or write result")
    args = parser.parse_args()
    if args.controls_only:
        print(json.dumps(controls_only(), sort_keys=True, indent=2))
        return 0
    result = run_full()
    print(json.dumps(result["summary"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
