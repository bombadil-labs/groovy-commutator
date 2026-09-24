"""Exact, frozen six-cell observer-orbit preflight; see the dated protocol."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import resource
import signal


WIDTH = 6
STATE_COUNT = 1 << WIDTH
MAX_PERIOD = 6
PROTOCOL = "docs/research/protocols/observer-orbit-preflight-20260924.md"


def step(state: int) -> int:
    result = 0
    for site in range(WIDTH):
        left = (state >> ((site - 1) % WIDTH)) & 1
        center = (state >> site) & 1
        right = (state >> ((site + 1) % WIDTH)) & 1
        result |= (left ^ (center | right)) << site
    return result


def groovy(state: int) -> int:
    evolved = step(state)
    change = state ^ evolved
    return evolved ^ step(evolved) ^ step(change)


def source_cycles(successors: list[int]) -> list[list[int]]:
    processed: set[int] = set()
    cycles: list[list[int]] = []
    for seed in range(STATE_COUNT):
        if seed in processed:
            continue
        seen: dict[int, int] = {}
        path: list[int] = []
        current = seed
        while current not in seen and current not in processed:
            seen[current] = len(path)
            path.append(current)
            current = successors[current]
        if current in seen:
            cycle = path[seen[current] :]
            first = cycle.index(min(cycle))
            cycles.append(cycle[first:] + cycle[:first])
        processed.update(path)
    return sorted(cycles)


def true_words(cycles: list[list[int]], observation: list[int], k: int) -> set[tuple[int, ...]]:
    words: set[tuple[int, ...]] = set()
    for cycle in cycles:
        row = [observation[state] for state in cycle]
        length = len(row)
        if all(row[index] == row[(index + k) % length] for index in range(length)):
            for offset in range(length):
                words.add(tuple(row[(offset + j) % length] for j in range(k)))
    return words


def closed_walk_counts(vertices: list[int], neighbors: dict[int, list[int]]) -> list[int]:
    counts = [0] * MAX_PERIOD
    for start in vertices:
        frontier = {start: 1}
        for k in range(MAX_PERIOD):
            following: dict[int, int] = {}
            for node, paths in frontier.items():
                for nxt in neighbors[node]:
                    following[nxt] = following.get(nxt, 0) + paths
            counts[k] += following.get(start, 0)
            frontier = following
    return counts


def primitive(word: tuple[int, ...]) -> bool:
    return not any(
        len(word) % divisor == 0
        and all(word[index] == word[index % divisor] for index in range(len(word)))
        for divisor in range(1, len(word))
    )


def canonical_rotation(word: tuple[int, ...]) -> tuple[int, ...]:
    return min(word[index:] + word[:index] for index in range(len(word)))


def first_phantom(
    vertices: list[int], neighbors: dict[int, list[int]], realized: set[tuple[int, ...]], k: int
) -> tuple[int, ...] | None:
    candidates: set[tuple[int, ...]] = set()

    def walk(start: int, path: tuple[int, ...]) -> None:
        current = path[-1]
        if len(path) == k:
            if start in neighbors[current] and path not in realized and primitive(path):
                candidates.add(canonical_rotation(path))
            return
        for nxt in neighbors[current]:
            walk(start, path + (nxt,))

    for start in vertices:
        walk(start, (start,))
    return min(candidates) if candidates else None


def evaluate(name: str, observation: list[int], successors: list[int], cycles: list[list[int]]) -> dict:
    edge_witness: dict[tuple[int, int], int] = {}
    for state in range(STATE_COUNT):
        edge_witness.setdefault((observation[state], observation[successors[state]]), state)
    vertices = sorted(set(observation))
    neighbors = {node: sorted({v for u, v in edge_witness if u == node}) for node in vertices}
    closed = closed_walk_counts(vertices, neighbors)
    true_sets = [true_words(cycles, observation, k) for k in range(1, MAX_PERIOD + 1)]
    true_counts = [len(words) for words in true_sets]
    phantom = [c - r for c, r in zip(closed, true_counts)]
    assert all(p >= 0 for p in phantom)

    witness = None
    if any(phantom):
        k = next(i + 1 for i, count in enumerate(phantom) if count > 0)
        word = first_phantom(vertices, neighbors, true_sets[k - 1], k)
        if word is None:
            raise AssertionError("phantom count lacks a primitive phantom witness")
        witness = {
            "period": k,
            "word": list(word),
            "edge_sources": [edge_witness[(word[i], word[(i + 1) % k])] for i in range(k)],
        }

    return {
        "name": name,
        "observation_table": observation,
        "vertices": vertices,
        "edges": [
            {"from": u, "to": v, "example_source": s}
            for (u, v), s in sorted(edge_witness.items())
        ],
        "rooted_closed_walks": closed,
        "true_periodic_words": true_counts,
        "phantom_words": phantom,
        "source_cycle_observations": [
            [observation[state] for state in cycle] for cycle in cycles
        ],
        "first_primitive_phantom": witness,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--implementation-commit", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if len(args.implementation_commit) != 40 or any(
        digit not in "0123456789abcdef" for digit in args.implementation_commit.lower()
    ):
        parser.error("--implementation-commit must be a full git SHA")
    if args.output.exists():
        parser.error(f"refusing to overwrite {args.output}")
    resource.setrlimit(resource.RLIMIT_AS, (256 * 1024**2, 256 * 1024**2))
    signal.alarm(30)
    successors = [step(s) for s in range(STATE_COUNT)]
    cycles = source_cycles(successors)
    g = [groovy(s) for s in range(STATE_COUNT)]
    cases = {
        "native_g": evaluate("native_g", g, successors, cycles),
        "three_row_history": evaluate(
            "three_row_history",
            [g[s] | (g[successors[s]] << WIDTH) | (g[successors[successors[s]]] << (2 * WIDTH))
             for s in range(STATE_COUNT)],
            successors,
            cycles,
        ),
        "identity": evaluate("identity", list(range(STATE_COUNT)), successors, cycles),
    }
    predictions = {
        "P1_primitive_phantom_within_six": "supported" if any(cases["native_g"]["phantom_words"]) else "failed",
        "P2_history_no_phantoms": "supported" if not any(cases["three_row_history"]["phantom_words"]) else "failed",
        "P3_identity_no_phantoms": "supported" if not any(cases["identity"]["phantom_words"]) else "failed",
    }
    record = {
        "schema": "observer-orbit-preflight-v1",
        "protocol": PROTOCOL,
        "implementation_commit": args.implementation_commit,
        "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "width": WIDTH,
        "max_period": MAX_PERIOD,
        "rule": 30,
        "source_transition": successors,
        "source_cycles": cycles,
        "source_transient_states": STATE_COUNT - sum(len(cycle) for cycle in cycles),
        "cases": cases,
        "predictions": predictions,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as out:
        json.dump(record, out, indent=2, sort_keys=True)
        out.write("\n")
    print(json.dumps({"predictions": predictions,
                      "counts": {name: c["phantom_words"] for name, c in cases.items()}}, sort_keys=True))


if __name__ == "__main__":
    main()
