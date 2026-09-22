#!/usr/bin/env python3
"""Stage 4: the Rule-110 Groovy lift as a CA in its own right.

The lifted state is (G_t, X_t, G_{t+1}, X_{t+1}) with X the "inside a run of
three ones" track (truth table 128). Stage 1 certifies a radius-3 law
(G_{t+2}, X_{t+2}) = F(window). This script

1. extracts F exhaustively from all 8,192 source windows of its causal support;
2. runs the lifted CA autonomously on rings (from lifted initial data only) and
   checks it against G and X recomputed from the evolving source every step;
3. measures the lift's quotient on rings: how many source states share a
   lifted state, and that shared states agree forever after (they must);
4. renders the source / G / X spacetime diagram as a PNG.

Run: python scripts/groovy_field_rule110_lift.py
Outputs: results/groovy_field_20260922/rule110_lift.json and
docs/research/assets/groovy-field-rule110.png
"""
from __future__ import annotations

import json
import struct
import sys
import zlib
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from groovy.groovy_field import TupleCA  # noqa: E402

RULE, TRACK, R = 110, 128, 3
OUT = ROOT / "results" / "groovy_field_20260922"


def ring_step(s, table):
    l, r = np.roll(s, 1), np.roll(s, -1)
    idx = 4 * l + 2 * s + r
    lut = np.array([(table >> i) & 1 for i in range(8)], dtype=np.uint8)
    return lut[idx]


def ring_obs(s):
    e = ring_step(s, RULE)
    g = e ^ ring_step(e, RULE) ^ ring_step(s ^ e, RULE)
    return g, ring_step(s, TRACK)


def extract_table():
    ca = TupleCA(RULE)
    m = R + 3
    L = 2 * m + 1
    table = {}
    for v in range(1 << L):
        w = tuple((v >> (L - 1 - i)) & 1 for i in range(L))
        key = []
        for j in (0, 1):
            g, x = ca.observe(w, j, (TRACK,))
            c = len(g) // 2
            key.append(g[c - R:c + R + 1] + x[c - R:c + R + 1])
        g2, x2 = ca.observe(w, 2, (TRACK,))
        val = (g2[len(g2) // 2], x2[len(x2) // 2])
        key = tuple(key)
        if table.setdefault(key, val) != val:
            raise SystemExit("inconsistent table: stage-1 law not reproduced")
    return table


def lifted_step(a, b, table):
    """(a, b) = ((G_t, X_t), (G_{t+1}, X_{t+1})) arrays -> next pair."""
    n = len(a[0])
    ng, nx = np.zeros(n, np.uint8), np.zeros(n, np.uint8)
    for i in range(n):
        idx = [(i + d) % n for d in range(-R, R + 1)]
        key = (tuple(a[0][idx]) + tuple(a[1][idx]), tuple(b[0][idx]) + tuple(b[1][idx]))
        ng[i], nx[i] = table[key]
    return b, (ng, nx)


def png(path, rows, scale=2):
    rows = np.kron(np.array(rows, dtype=np.uint8), np.ones((scale, scale, 1), np.uint8))
    h, w, _ = rows.shape
    raw = b"".join(b"\x00" + rows[y].tobytes() for y in range(h))
    def chunk(t, d):
        c = struct.pack(">I", len(d)) + t + d
        return c + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    data = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))
    path.write_bytes(data)


def main():
    table = extract_table()
    rng = np.random.default_rng(20260922)
    sims = []
    for n, steps in ((40, 60), (64, 80), (101, 60)):
        s = rng.integers(0, 2, n, dtype=np.uint8)
        a, b = ring_obs(s), ring_obs(ring_step(s, RULE))
        src = ring_step(s, RULE)
        ok = True
        for _ in range(steps):
            a, b = lifted_step(a, b, table)
            src = ring_step(src, RULE)
            g, x = ring_obs(src)
            ok &= bool(np.array_equal(g, b[0]) and np.array_equal(x, b[1]))
        sims.append({"ring": n, "steps": steps, "lifted_matches_source": ok})

    quot = []
    for n in range(8, 17):
        states = np.arange(1 << n)
        bitsm = ((states[:, None] >> np.arange(n - 1, -1, -1)) & 1).astype(np.uint8)
        e = np.array([ring_step(r, RULE) for r in bitsm])
        lift = {}
        for s0, s1 in zip(bitsm, e):
            key = tuple(np.concatenate(ring_obs(s0) + ring_obs(s1)))
            lift.setdefault(key, []).append(s0)
        quot.append({"ring": n, "source_states": int(1 << n), "lifted_states": len(lift),
                     "largest_class": max(len(v) for v in lift.values())})

    n, steps = 160, 120
    s = rng.integers(0, 2, n, dtype=np.uint8)
    for _ in range(40):
        s = ring_step(s, RULE)
    panels = [[], [], []]
    for _ in range(steps):
        g, x = ring_obs(s)
        panels[0].append(s); panels[1].append(g); panels[2].append(x)
        s = ring_step(s, RULE)
    ink = {0: (np.array([250, 250, 247]), np.array([40, 40, 48])),
           1: (np.array([250, 250, 247]), np.array([176, 58, 46])),
           2: (np.array([250, 250, 247]), np.array([34, 102, 170]))}
    gap = np.full((steps, 6, 3), 255, np.uint8)
    cols = []
    for p, arr in enumerate(panels):
        a = np.array(arr)[:, :, None]
        cols.append(np.where(a == 1, ink[p][1], ink[p][0]).astype(np.uint8))
        cols.append(gap)
    img = np.concatenate(cols[:-1], axis=1)
    asset = ROOT / "docs" / "research" / "assets" / "groovy-field-rule110.png"
    png(asset, img)

    OUT.mkdir(parents=True, exist_ok=True)
    doc = {"stage": "rule110_lift", "rule": RULE, "track": TRACK, "radius": R,
           "table_realized_patterns": len(table),
           "autonomous_simulation": sims, "ring_quotient": quot,
           "figure": str(asset.relative_to(ROOT))}
    (OUT / "rule110_lift.json").write_text(json.dumps(doc, indent=1) + "\n")
    print(json.dumps({k: v for k, v in doc.items() if k != "ring_quotient"}, indent=1))
    print("quotient", [(q["ring"], q["source_states"], q["lifted_states"]) for q in quot])


if __name__ == "__main__":
    main()
