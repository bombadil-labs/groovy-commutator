#!/usr/bin/env python3
"""Exact bounded Rule-110 middle-track search.

Searches all 256 radius-one Boolean tracks sampled at even sites for present-
time autonomous closure of (block parity, centered Groovy, track) at cadence
two, macro radius <= 2. Successful radius-two tracks are then audited for
global source-fiber compression on rings 12, 14 and 16.

Protocol:
  docs/research/protocols/rule110-middle-tracks-20261007.md
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

OUT = Path("results/rule110_middle_tracks_20261007.json")
RULE = 110


def f(rule: int, l: int, c: int, r: int) -> int:
    return (rule >> ((l << 2) | (c << 1) | r)) & 1


def h_at(bits: list[int], lo: int, p: int) -> int:
    return f(RULE, bits[p - 1 - lo], bits[p - lo], bits[p + 1 - lo])


def g_at(bits: list[int], lo: int, p: int) -> int:
    hp = {q: h_at(bits, lo, q) for q in (p - 1, p, p + 1)}
    h2 = f(RULE, hp[p - 1], hp[p], hp[p + 1])
    d = {q: bits[q - lo] ^ hp[q] for q in (p - 1, p, p + 1)}
    hd = f(RULE, d[p - 1], d[p], d[p + 1])
    return hp[p] ^ h2 ^ hd ^ (RULE & 1)


def pgg_symbol(bits: list[int], lo: int, j: int) -> tuple[int, int, int]:
    a = 2 * j
    return (
        bits[a - lo] ^ bits[a + 1 - lo],
        g_at(bits, lo, a),
        g_at(bits, lo, a + 1),
    )


def track_index(bits: list[int], lo: int, j: int) -> int:
    p = 2 * j
    return (
        (bits[p - 1 - lo] << 2)
        | (bits[p - lo] << 1)
        | bits[p + 1 - lo]
    )


def next_base_and_track_index(bits: list[int], lo: int) -> tuple[tuple[int, int, int], int]:
    h1 = {p: h_at(bits, lo, p) for p in range(-3, 5)}
    h2 = {
        p: f(RULE, h1[p - 1], h1[p], h1[p + 1])
        for p in range(-2, 4)
    }

    def g2(p: int) -> int:
        hp = {
            q: f(RULE, h2[q - 1], h2[q], h2[q + 1])
            for q in (p - 1, p, p + 1)
        }
        hh2 = f(RULE, hp[p - 1], hp[p], hp[p + 1])
        d = {q: h2[q] ^ hp[q] for q in (p - 1, p, p + 1)}
        hd = f(RULE, d[p - 1], d[p], d[p + 1])
        return hp[p] ^ hh2 ^ hd ^ (RULE & 1)

    base = (h2[0] ^ h2[1], g2(0), g2(1))
    idx = (h2[-1] << 2) | (h2[0] << 1) | h2[1]
    return base, idx


def precompute(radius: int):
    lo = -2 * radius - 2
    hi = 2 * radius + 3
    # Next central P/G/T needs original source positions -4..5.
    lo = min(lo, -4)
    hi = max(hi, 5)
    width = hi - lo + 1

    rows = []
    for word in range(1 << width):
        bits = [(word >> i) & 1 for i in range(width)]
        base_context = tuple(
            value
            for j in range(-radius, radius + 1)
            for value in pgg_symbol(bits, lo, j)
        )
        track_inputs = tuple(
            track_index(bits, lo, j)
            for j in range(-radius, radius + 1)
        )
        next_base, next_idx = next_base_and_track_index(bits, lo)
        rows.append((word, base_context, track_inputs, next_base, next_idx))
    return width, rows


def track_factor(track: int, radius: int, rows) -> dict:
    table = {}
    for word, base_context, track_inputs, next_base, next_idx in rows:
        track_context = tuple((track >> idx) & 1 for idx in track_inputs)
        key = base_context + track_context
        target = next_base + ((track >> next_idx) & 1,)
        old = table.get(key)
        if old is not None and old[0] != target:
            return {
                "pass": False,
                "contexts_before_conflict": len(table),
                "conflict": {
                    "word_x": old[1],
                    "word_y": word,
                    "next_x": list(old[0]),
                    "next_y": list(target),
                },
            }
        table[key] = (target, word)
    return {"pass": True, "distinct_contexts": len(table), "conflict": None}


def step_state(state: int, n: int) -> int:
    out = 0
    for i in range(n):
        l = (state >> ((i - 1) % n)) & 1
        c = (state >> i) & 1
        r = (state >> ((i + 1) % n)) & 1
        out |= f(RULE, l, c, r) << i
    return out


def parity_state(state: int, n: int) -> int:
    out = 0
    for j in range(n // 2):
        out |= (
            ((state >> (2 * j)) & 1)
            ^ ((state >> (2 * j + 1)) & 1)
        ) << j
    return out


def centered_g_state(state: int, n: int) -> int:
    h = step_state(state, n)
    h2 = step_state(h, n)
    d = state ^ h
    return h ^ h2 ^ step_state(d, n) ^ step_state(0, n)


def track_field(state: int, n: int, track: int) -> int:
    out = 0
    for j in range(n // 2):
        i = 2 * j
        l = (state >> ((i - 1) % n)) & 1
        c = (state >> i) & 1
        r = (state >> ((i + 1) % n)) & 1
        out |= f(track, l, c, r) << j
    return out


def fiber_stats(track: int, n: int) -> dict:
    fibers = Counter()
    for state in range(1 << n):
        key = (
            parity_state(state, n),
            centered_g_state(state, n),
            track_field(state, n, track),
        )
        fibers[key] += 1

    hist = Counter(fibers.values())
    conditional_bits = sum(
        (size * count / (1 << n)) * (0 if size == 1 else (size.bit_length() - 1))
        for size, count in hist.items()
    )
    # Every observed fiber in this bounded search is size 1 or 2; compute the
    # exact uniform conditional entropy directly from that histogram.
    conditional_exact = sum(
        (size * count / (1 << n)) * __import__("math").log2(size)
        for size, count in hist.items()
    )
    return {
        "n": n,
        "distinct_encodings": len(fibers),
        "largest_fiber": max(fibers.values()),
        "fiber_histogram": {str(k): v for k, v in sorted(hist.items())},
        "conditional_source_bits": conditional_exact,
    }


def main() -> None:
    width1, rows1 = precompute(1)
    width2, rows2 = precompute(2)

    radius1 = []
    radius2 = []
    radius2_details = {}
    for track in range(256):
        r1 = track_factor(track, 1, rows1)
        if r1["pass"]:
            radius1.append(track)
            continue
        r2 = track_factor(track, 2, rows2)
        if r2["pass"]:
            radius2.append(track)
            radius2_details[str(track)] = {
                "distinct_contexts": r2["distinct_contexts"]
            }

    fibers = {
        str(track): {
            str(n): fiber_stats(track, n)
            for n in (12, 14, 16)
        }
        for track in radius2
    }

    # Group tracks by their exact fiber pattern across all three rings.
    groups = {}
    for track in radius2:
        signature = tuple(
            (
                fibers[str(track)][str(n)]["distinct_encodings"],
                fibers[str(track)][str(n)]["largest_fiber"],
                tuple(sorted(fibers[str(track)][str(n)]["fiber_histogram"].items())),
            )
            for n in (12, 14, 16)
        )
        key = json.dumps(signature)
        groups.setdefault(key, []).append(track)

    group_rows = []
    for key, tracks in groups.items():
        exemplar = str(tracks[0])
        group_rows.append({
            "tracks": tracks,
            "count": len(tracks),
            "rings": {
                str(n): fibers[exemplar][str(n)]
                for n in (12, 14, 16)
            },
        })
    group_rows.sort(
        key=lambda row: row["rings"]["12"]["conditional_source_bits"],
        reverse=True,
    )

    result = {
        "schema": "rule110-middle-tracks-v1",
        "date": "2026-10-07",
        "protocol": "docs/research/protocols/rule110-middle-tracks-20261007.md",
        "candidate_family": (
            "T_j=t(X_{2j-1},X_{2j},X_{2j+1}), all 256 radius-one Boolean t"
        ),
        "radius1": {
            "source_width": width1,
            "closing_tracks": radius1,
            "closing_count": len(radius1),
        },
        "radius2": {
            "source_width": width2,
            "closing_tracks": radius2,
            "closing_count": len(radius2),
            "details": radius2_details,
        },
        "fiber_groups": group_rows,
        "summary": {
            "radius1_closing_count": len(radius1),
            "radius2_closing_count": len(radius2),
            "all_radius2_closers_largest_fiber_at_most_two": all(
                fibers[str(track)]["16"]["largest_fiber"] <= 2
                for track in radius2
            ),
            "max_conditional_source_bits_n12": max(
                fibers[str(track)]["12"]["conditional_source_bits"]
                for track in radius2
            ) if radius2 else None,
            "max_conditional_source_bits_n16": max(
                fibers[str(track)]["16"]["conditional_source_bits"]
                for track in radius2
            ) if radius2 else None,
            "middle_representation_found": False,
        },
    }
    result["source_hashes"] = {
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
