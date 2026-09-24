"""Independent scalar/table replay of the finite observer-orbit record."""

from __future__ import annotations

from collections import defaultdict
import hashlib
import json
from pathlib import Path
import sys


N = 6
SIZE = 1 << N
PERIODS = range(1, 7)


def eca30(state: int) -> int:
    bits = [(state // (2**i)) % 2 for i in range(N)]
    new_bits = []
    for i in range(N):
        triple = 4 * bits[(i - 1) % N] + 2 * bits[i] + bits[(i + 1) % N]
        new_bits.append((30 // (2**triple)) % 2)
    return sum(value * (2**i) for i, value in enumerate(new_bits))


def groovy_direct(state: int) -> int:
    first = eca30(state)
    return (first ^ eca30(first)) ^ eca30(state ^ first)


def canonical_cycle(cycle: list[int]) -> tuple[int, ...]:
    offset = cycle.index(min(cycle))
    return tuple(cycle[offset:] + cycle[:offset])


def cycle_set(next_states: list[int]) -> set[tuple[int, ...]]:
    result = set()
    for state in range(SIZE):
        positions = {}
        trace = []
        while state not in positions:
            positions[state] = len(trace)
            trace.append(state)
            state = next_states[state]
        result.add(canonical_cycle(trace[positions[state]:]))
    return result


def trace_powers(vertices: list[int], pairs: set[tuple[int, int]]) -> list[int]:
    indices = {value: index for index, value in enumerate(vertices)}
    n = len(vertices)
    adjacency = [[0] * n for _ in range(n)]
    for a, b in pairs:
        adjacency[indices[a]][indices[b]] = 1
    matrix = [row[:] for row in adjacency]
    traces = []
    for k in PERIODS:
        traces.append(sum(matrix[i][i] for i in range(n)))
        if k < max(PERIODS):
            matrix = [
                [sum(matrix[i][h] * adjacency[h][j] for h in range(n)) for j in range(n)]
                for i in range(n)
            ]
    return traces


def real_periodic_words(cycles: set[tuple[int, ...]], observed: list[int], k: int) -> set[tuple[int, ...]]:
    result = set()
    for cycle in cycles:
        sequence = tuple(observed[state] for state in cycle)
        if sequence != tuple(sequence[(i + k) % len(sequence)] for i in range(len(sequence))):
            continue
        result.update(
            tuple(sequence[(j + offset) % len(sequence)] for j in range(k))
            for offset in range(len(sequence))
        )
    return result


def check(path: Path) -> None:
    record = json.loads(path.read_text(encoding="utf-8"))
    assert record["schema"] == "observer-orbit-preflight-v1"
    assert record["width"] == N and record["rule"] == 30 and record["max_period"] == 6
    runner = Path(__file__).with_name("run.py")
    assert hashlib.sha256(runner.read_bytes()).hexdigest() == record["implementation_sha256"]
    assert len(record["implementation_commit"]) == 40
    next_states = [eca30(state) for state in range(SIZE)]
    assert next_states == record["source_transition"]
    cycles = cycle_set(next_states)
    assert {tuple(cycle) for cycle in record["source_cycles"]} == cycles
    assert SIZE - sum(len(cycle) for cycle in cycles) == record["source_transient_states"]
    g = [groovy_direct(state) for state in range(SIZE)]
    observations = {
        "native_g": g,
        "three_row_history": [
            g[state] + 64 * g[next_states[state]] + 4096 * g[next_states[next_states[state]]]
            for state in range(SIZE)
        ],
        "identity": list(range(SIZE)),
    }
    expected = {}
    for name, observed in observations.items():
        case = record["cases"][name]
        assert case["name"] == name and case["observation_table"] == observed
        vertices = sorted(set(observed))
        assert case["vertices"] == vertices
        edge_sources: dict[tuple[int, int], list[int]] = defaultdict(list)
        for source, target in enumerate(next_states):
            edge_sources[(observed[source], observed[target])].append(source)
        edges = {(row["from"], row["to"]) for row in case["edges"]}
        assert edges == set(edge_sources) and len(case["edges"]) == len(edges)
        for row in case["edges"]:
            assert row["example_source"] == min(edge_sources[(row["from"], row["to"])])
        closed = trace_powers(vertices, edges)
        real_sets = [real_periodic_words(cycles, observed, k) for k in PERIODS]
        phantoms = [total - len(real) for total, real in zip(closed, real_sets)]
        assert all(value >= 0 for value in phantoms)
        assert case["rooted_closed_walks"] == closed
        assert case["true_periodic_words"] == list(map(len, real_sets))
        assert case["phantom_words"] == phantoms
        assert {tuple(values) for values in case["source_cycle_observations"]} == {
            tuple(observed[state] for state in cycle) for cycle in cycles
        }
        witness = case["first_primitive_phantom"]
        if any(phantoms):
            assert witness is not None
            k = witness["period"]
            word = tuple(witness["word"])
            assert k == len(word) == next(i for i, n in enumerate(phantoms, 1) if n)
            assert word == min(word[i:] + word[:i] for i in range(k))
            assert all(k % d or any(word[i] != word[i % d] for i in range(k)) for d in range(1, k))
            assert word not in real_sets[k - 1]
            for i, state in enumerate(witness["edge_sources"]):
                assert state == min(edge_sources[(word[i], word[(i + 1) % k])])
        else:
            assert witness is None
        expected[name] = phantoms
    assert record["predictions"] == {
        "P1_primitive_phantom_within_six": "supported" if any(expected["native_g"]) else "failed",
        "P2_history_no_phantoms": "supported" if not any(expected["three_row_history"]) else "failed",
        "P3_identity_no_phantoms": "supported" if not any(expected["identity"]) else "failed",
    }
    print("OK: independent Rule-30 truth-table replay, graph powers, cycles and witnesses")


if __name__ == "__main__":
    check(Path(sys.argv[1]))
