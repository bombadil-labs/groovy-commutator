#!/usr/bin/env python3
"""Exact finite censuses for dimensional rule-as-geometry overlap.

Primary preregistered test:
  For each ECA rule r, place its eight output bits on the Moore ring in address
  order and allow only physical D4 rotations/reflections locally. Enumerate all
  3x3 and 4x4 periodic binary fields whose ring at every site lies in that one
  D4 orbit.

Exploratory follow-up (kept explicitly separate):
  After the primary result was known, allow the ring orbit to depend on the
  center bit and enumerate the resulting (r0, r1) orbit pairs on 4x4 fields.
  This follow-up is descriptive and not preregistered evidence for Class IV.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

RING = ((0, -1), (1, -1), (1, 0), (1, 1),
        (0, 1), (-1, 1), (-1, 0), (-1, -1))
RING_INDEX = {p: i for i, p in enumerate(RING)}


def d4_maps() -> list[tuple[int, ...]]:
    transforms = (
        lambda x, y: (x, y),
        lambda x, y: (-y, x),
        lambda x, y: (-x, -y),
        lambda x, y: (y, -x),
        lambda x, y: (-x, y),
        lambda x, y: (x, -y),
        lambda x, y: (y, x),
        lambda x, y: (-y, -x),
    )
    return list(dict.fromkeys(
        tuple(RING_INDEX[f(x, y)] for x, y in RING) for f in transforms
    ))


D4_MAPS = d4_maps()


def transform_code(code: int, mapping: tuple[int, ...]) -> int:
    out = 0
    for source in range(8):
        out |= ((code >> source) & 1) << mapping[source]
    return out


def orbit(code: int) -> frozenset[int]:
    return frozenset(transform_code(code, m) for m in D4_MAPS)


ORBITS = tuple(orbit(r) for r in range(256))
ORBIT_CANON = tuple(min(o) for o in ORBITS)
RULES_BY_CODE = tuple(
    frozenset(r for r in range(256) if code in ORBITS[r])
    for code in range(256)
)


def bit(state: int, n: int, x: int, y: int) -> int:
    return (state >> ((y % n) * n + (x % n))) & 1


def ring_code(state: int, n: int, x: int, y: int) -> int:
    out = 0
    for i, (dx, dy) in enumerate(RING):
        out |= bit(state, n, x + dx, y + dy) << i
    return out


def state_rows(state: int, n: int) -> list[str]:
    return ["".join(str(bit(state, n, x, y)) for x in range(n)) for y in range(n)]


def primary_census(n: int) -> tuple[list[int], list[int | None]]:
    counts = [0] * 256
    witnesses: list[int | None] = [None] * 256
    for state in range(1 << (n * n)):
        possible: set[int] | None = None
        for y in range(n):
            for x in range(n):
                here = RULES_BY_CODE[ring_code(state, n, x, y)]
                possible = set(here) if possible is None else possible.intersection(here)
                if not possible:
                    break
            if not possible:
                break
        if possible:
            for rule in possible:
                counts[rule] += 1
                if witnesses[rule] is None:
                    witnesses[rule] = state
    return counts, witnesses


def center_conditioned_pair(state: int, n: int) -> tuple[int, int] | None:
    by_center = (set(), set())
    for y in range(n):
        for x in range(n):
            c = bit(state, n, x, y)
            by_center[c].add(ORBIT_CANON[ring_code(state, n, x, y)])
            if len(by_center[c]) > 1:
                return None
    if not by_center[0] or not by_center[1]:
        return None
    return next(iter(by_center[0])), next(iter(by_center[1]))


def selector_step(state: int, n: int, axis: str) -> int:
    out = 0
    for y in range(n):
        for x in range(n):
            ring = ring_code(state, n, x, y)
            c = bit(state, n, x, y)
            if axis == "horizontal":
                west = (ring >> 6) & 1
                east = (ring >> 2) & 1
                q = 4 * west + 2 * c + east
            elif axis == "vertical":
                north = ring & 1
                south = (ring >> 4) & 1
                q = 4 * north + 2 * c + south
            else:
                raise ValueError(axis)
            out |= ((ring >> q) & 1) << (y * n + x)
    return out


def persistence(state: int, n: int, axis: str, cap: int = 32) -> dict:
    seen: dict[int, int] = {}
    pairs: list[list[int]] = []
    current = state
    for t in range(cap + 1):
        pair = center_conditioned_pair(current, n)
        if pair is None:
            return {"valid_steps": t, "closed_cycle": False, "cycle_length": None, "pairs": pairs}
        pairs.append(list(pair))
        if current in seen:
            return {
                "valid_steps": t,
                "closed_cycle": True,
                "cycle_length": t - seen[current],
                "pairs": pairs,
            }
        seen[current] = t
        current = selector_step(current, n, axis)
    return {"valid_steps": cap + 1, "closed_cycle": False, "cycle_length": None, "pairs": pairs}


def exploratory_center_conditioned_4() -> dict:
    pair_counts: Counter[tuple[int, int]] = Counter()
    witnesses: dict[tuple[int, int], int] = {}
    persistence_by_pair: dict[tuple[int, int], dict[str, Counter]] = defaultdict(
        lambda: {"horizontal": Counter(), "vertical": Counter()}
    )
    total = 0
    for state in range(1 << 16):
        pair = center_conditioned_pair(state, 4)
        if pair is None:
            continue
        total += 1
        pair_counts[pair] += 1
        witnesses.setdefault(pair, state)
        for axis in ("horizontal", "vertical"):
            p = persistence(state, 4, axis)
            key = (p["valid_steps"], p["closed_cycle"], p["cycle_length"])
            persistence_by_pair[pair][axis][key] += 1

    records = []
    for pair in sorted(pair_counts):
        witness = witnesses[pair]
        records.append({
            "center0_orbit_canonical": pair[0],
            "center1_orbit_canonical": pair[1],
            "field_count": pair_counts[pair],
            "witness_state": witness,
            "witness_rows": state_rows(witness, 4),
            "selector_persistence": {
                axis: [
                    {
                        "valid_steps": k[0],
                        "closed_cycle": k[1],
                        "cycle_length": k[2],
                        "field_count": count,
                    }
                    for k, count in sorted(
                        persistence_by_pair[pair][axis].items(),
                        key=lambda item: (item[0][0], item[0][1], -1 if item[0][2] is None else item[0][2]),
                    )
                ]
                for axis in ("horizontal", "vertical")
            },
        })
    return {"field_count": total, "pair_count": len(pair_counts), "pairs": records}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("results/oriented_ring_overlap_20260909.json"))
    args = parser.parse_args()

    primary = {}
    for n in (3, 4):
        counts, witnesses = primary_census(n)
        passing = [r for r, c in enumerate(counts) if c]
        primary[str(n)] = {
            "passing_rules": passing,
            "passing_rule_count": len(passing),
            "counts": {str(r): counts[r] for r in passing},
            "witnesses": {
                str(r): {"state": witnesses[r], "rows": state_rows(witnesses[r], n)}
                for r in passing
            },
        }

    result = {
        "protocol": "docs/research/protocols/oriented-ring-overlap-20260909.md",
        "rule_ring_order": ["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
        "d4_map_count": len(D4_MAPS),
        "orbit_size_histogram": dict(sorted(Counter(map(len, ORBITS)).items())),
        "primary": primary,
        "exploratory_post_primary": {
            "description": "center-conditioned D4 ring orbit pairs on 4x4; defined after primary result was known",
            **exploratory_center_conditioned_4(),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "primary": {n: primary[n]["passing_rules"] for n in primary},
        "exploratory_pairs": [
            [p["center0_orbit_canonical"], p["center1_orbit_canonical"], p["field_count"]]
            for p in result["exploratory_post_primary"]["pairs"]
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
