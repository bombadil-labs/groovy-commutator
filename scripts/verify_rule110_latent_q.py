#!/usr/bin/env python3
"""Independent tuple replay of saved Q witnesses and cross-width checks.

No import from the experimental evaluator. Read-only; assertions are semantic
checks, not independent human review or a full-line theorem.
"""
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "results/rule110_latent_q_20261007.json"
report = json.loads(RESULT.read_text(encoding="utf-8"))
cache = {}


def unpack(x, n):
    return tuple((int(x) >> i) & 1 for i in range(n))


def evolve(s):
    return tuple((110 >> (4 * s[(i - 1) % len(s)] + 2 * s[i] + s[(i + 1) % len(s)])) & 1
                 for i in range(len(s)))


def pack(s):
    return sum(b << i for i, b in enumerate(s))


def fields(s):
    h = evolve(s)
    hh = evolve(h)
    hd = evolve(tuple(a ^ b for a, b in zip(s, h)))
    g = tuple(a ^ b ^ c for a, b, c in zip(h, hh, hd))
    p = tuple(s[i] ^ s[i + 1] for i in range(0, len(s), 2))
    return p, g


def load(n, arm):
    if (n, arm) not in cache:
        row = report["profiles"][str(n)][arm]
        a = np.load(ROOT / row["certificate"]["path"])
        for name, digest in row["certificate"]["array_sha256"].items():
            assert hashlib.sha256(np.asarray(a[name], dtype="<u4").tobytes()).hexdigest() == digest
        cache[n, arm] = a
    return cache[n, arm]


def symbol(x, n, arm, j):
    p, g = fields(unpack(x, n))
    a = load(n, arm)
    q = unpack(a["qclass"][a["labels"][x]], n)
    if arm == "G":
        return g[j % n] + 2 * q[j % n]
    b = (2 * j) % n
    return p[j % (n // 2)] + 2 * g[b] + 4 * g[b + 1] + 8 * q[b] + 16 * q[b + 1]


def check_local(w, radius, arm, nx, ny):
    for name, n in (("x", nx), ("y", ny)):
        x = w[name]
        key = 0
        for j in range(-radius, radius + 1):
            key = (key << (2 if arm == "G" else 5)) | symbol(x, n, arm, j)
        assert key == w["context"]
        nxt = pack(evolve(evolve(unpack(x, n))))
        assert symbol(nxt, n, arm, 0) == w["target_" + name]
    assert w["target_x"] != w["target_y"]


count = 0
for n in report["widths"]:
    for arm in ("G", "PG"):
        row = report["profiles"][str(n)][arm]
        load(n, arm)
        for radius, record in row.get("locality", {}).items():
            if record["status"] == "conflict":
                check_local(record["witness"], int(radius), arm, n, n)
                count += 1
    # Inspect ALL nonsingleton PG fibers, rather than only the first example.
    a = load(n, "PG")
    labs = a["labels"]
    actual = sorted(tuple(map(int, np.flatnonzero(labs == c)))
                    for c in np.flatnonzero(np.bincount(labs) > 1))
    mask = (1 << n) - 1
    alt = sum(1 << i for i in range(0, n, 2))
    assert actual == [(0, mask), (alt, mask ^ alt)]

for arm in ("G", "PG"):
    for radius, record in report["joint_locality"][arm].items():
        if record["status"] == "conflict":
            w = record["witness"]
            check_local(w, int(radius), arm, w["n_x"], w["n_y"])
            count += 1
    for record in report["repetition"][arm]:
        d, n = record["d"], record["n"]
        a, b = load(d, arm), load(n, arm)
        failures = 0
        for x in range(1 << d):
            repeated = pack(unpack(x, d) * (n // d))
            qsmall = int(a["qclass"][a["labels"][x]])
            qlarge = int(b["qclass"][b["labels"][repeated]])
            failures += pack(unpack(qsmall, d) * (n // d)) != qlarge
        assert failures == record["conflicts"]

execution = json.loads((ROOT / "results/rule110_latent_q_20261007/execution.json").read_text())
assert hashlib.sha256(RESULT.read_bytes()).hexdigest() == execution["result_sha256"]
archive = ROOT / "results/rule110_latent_q_20261007/initial-windows-crlf"
initial = json.loads((archive / "result.json").read_text(encoding="utf-8"))
for path, digest in initial["source_hashes"].items():
    assert hashlib.sha256((archive / path).read_bytes()).hexdigest() == digest
initial_execution = json.loads((archive / "execution.json").read_text())
assert hashlib.sha256((archive / "result.json").read_bytes()).hexdigest() == initial_execution["result_sha256"]
assert {k: v for k, v in initial.items() if k != "source_hashes"} == {
    k: v for k, v in report.items() if k != "source_hashes"}
print(f"Verified {count} local/cross-width collisions, every repetition pair, all exceptional PG fibers, and result seal.")
