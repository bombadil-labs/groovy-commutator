#!/usr/bin/env python3
"""Exact symbolic-language presentation of G-anchored commutator jets.

For each fixed prefix (G), (G,Q), ... through A5, construct the labeled
source de Bruijn graph of the sliding-block image, determinize it, minimize
the finite block-language DFA, and report entropy/context ambiguity.

Protocol:
  docs/research/protocols/commutator-jet-language-20261007.md
"""
from __future__ import annotations

import hashlib
import json
import math
from collections import Counter, defaultdict, deque
from pathlib import Path

import numpy as np

RULES = (110, 62)
PREFIX_ENDS = (1, 2, 3, 4, 5)  # G through A5
OUT = Path("results/commutator_jet_language_20261007.json")


def step_line(a: np.ndarray, rule: int) -> np.ndarray:
    left = np.concatenate(([0], a[:-1]))
    right = np.concatenate((a[1:], [0]))
    idx = (left << 2) | (a << 1) | right
    lut = np.array([(rule >> i) & 1 for i in range(8)], dtype=np.uint8)
    return lut[idx]


def local_level_truth(rule: int, level: int) -> np.ndarray:
    """Truth table for A_level at one site from its complete source window."""
    radius = level + 1
    width = 2 * radius + 1
    out = np.zeros(1 << width, dtype=np.uint8)
    pad = level + 4

    for word in range(1 << width):
        core = np.array([(word >> i) & 1 for i in range(width)], dtype=np.uint8)
        source = np.pad(core, (pad, pad))

        source_rows = [source]
        for _ in range(level + 2):
            source_rows.append(step_line(source_rows[-1], rule))

        temporal = [
            source_rows[t] ^ source_rows[t + 1]
            for t in range(len(source_rows) - 1)
        ]
        levels = [temporal]
        for _ in range(level):
            prev = levels[-1]
            levels.append([
                prev[t + 1] ^ step_line(prev[t], rule)
                for t in range(len(prev) - 1)
            ])

        out[word] = levels[level][0][pad + radius]
    return out


def pack_symbol(
    word: int,
    max_radius: int,
    levels: tuple[int, ...],
    truths: dict[int, np.ndarray],
) -> int:
    symbol = 0
    for out_pos, level in enumerate(levels):
        radius = level + 1
        subword = 0
        bit_pos = 0
        for source_pos in range(max_radius - radius, max_radius + radius + 1):
            subword |= ((word >> source_pos) & 1) << bit_pos
            bit_pos += 1
        symbol |= int(truths[level][subword]) << out_pos
    return symbol


def labeled_source_graph(rule: int, levels: tuple[int, ...]):
    max_radius = max(level + 1 for level in levels)
    source_state_bits = 2 * max_radius
    nstates = 1 << source_state_bits
    truths = {level: local_level_truth(rule, level) for level in levels}

    transitions: list[dict[int, set[int]]] = [
        defaultdict(set) for _ in range(nstates)
    ]
    alphabet = set()

    for state in range(nstates):
        for new_bit in (0, 1):
            source_word = state | (new_bit << source_state_bits)
            symbol = pack_symbol(
                source_word, max_radius, levels, truths
            )
            next_state = (
                (state >> 1)
                | (new_bit << (source_state_bits - 1))
            )
            transitions[state][symbol].add(next_state)
            alphabet.add(symbol)

    return transitions, tuple(sorted(alphabet)), max_radius


def determinize(transitions, alphabet):
    start = frozenset(range(len(transitions)))
    subsets = [start]
    subset_index = {start: 0}
    dfa_transitions: list[dict[int, int]] = []
    queue = deque([start])

    while queue:
        subset = queue.popleft()
        row = {}
        for symbol in alphabet:
            dest = set()
            for state in subset:
                dest.update(transitions[state].get(symbol, ()))
            if not dest:
                continue
            frozen = frozenset(dest)
            if frozen not in subset_index:
                subset_index[frozen] = len(subsets)
                subsets.append(frozen)
                queue.append(frozen)
            row[symbol] = subset_index[frozen]
        dfa_transitions.append(row)

    return subsets, dfa_transitions


def minimize_partial_dfa(dfa_transitions, alphabet):
    """Minimize with one explicit rejecting sink; all real states accept."""
    n = len(dfa_transitions)
    sink = n

    full = []
    for row in dfa_transitions:
        full.append([row.get(symbol, sink) for symbol in alphabet])
    full.append([sink] * len(alphabet))

    classes = [0] * n + [1]
    while True:
        ids = {}
        new = []
        for state in range(n + 1):
            signature = (
                0 if state < n else 1,
                tuple(classes[d] for d in full[state]),
            )
            if signature not in ids:
                ids[signature] = len(ids)
            new.append(ids[signature])
        if new == classes:
            break
        classes = new

    nclasses = max(classes) + 1
    quotient = [{} for _ in range(nclasses)]
    accepting = [False] * nclasses
    for state in range(n):
        accepting[classes[state]] = True

    sink_class = classes[sink]
    representatives = {}
    for state, cls in enumerate(classes):
        representatives.setdefault(cls, state)

    for cls, rep in representatives.items():
        for symbol_pos, symbol in enumerate(alphabet):
            dest = classes[full[rep][symbol_pos]]
            if dest != sink_class:
                quotient[cls][symbol] = dest

    return {
        "state_class": classes,
        "transitions": quotient,
        "accepting": accepting,
        "start": classes[0],
        "sink": sink_class,
    }


def recurrent_sccs(transitions, accepting):
    adjacency = [
        {dest for dest in row.values() if accepting[dest]}
        for row in transitions
    ]
    index = 0
    indices = [-1] * len(transitions)
    low = [0] * len(transitions)
    stack = []
    on_stack = set()
    components = []

    def visit(v):
        nonlocal index
        indices[v] = low[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)

        for w in adjacency[v]:
            if indices[w] < 0:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on_stack:
                low[v] = min(low[v], indices[w])

        if low[v] == indices[v]:
            comp = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                comp.append(w)
                if w == v:
                    break
            components.append(comp)

    for v in range(len(transitions)):
        if accepting[v] and indices[v] < 0:
            visit(v)

    recurrent = []
    for comp in components:
        if len(comp) > 1:
            recurrent.append(comp)
        else:
            v = comp[0]
            if v in adjacency[v]:
                recurrent.append(comp)
    return recurrent


def entropy_and_block_counts(
    transitions,
    accepting,
    start,
    block_max: int = 16,
):
    nodes = [i for i, ok in enumerate(accepting) if ok]
    position = {node: i for i, node in enumerate(nodes)}
    matrix = np.zeros((len(nodes), len(nodes)), dtype=np.float64)

    for source in nodes:
        for dest in transitions[source].values():
            if accepting[dest]:
                matrix[position[source], position[dest]] += 1.0

    eigenvalues = np.linalg.eigvals(matrix)
    rho = float(max(abs(v) for v in eigenvalues)) if len(eigenvalues) else 0.0
    entropy = math.log2(rho) if rho > 0 else float("-inf")

    counts = []
    current = {start: 1}
    for _ in range(block_max):
        nxt = defaultdict(int)
        for state, count in current.items():
            for dest in transitions[state].values():
                if accepting[dest]:
                    nxt[dest] += count
        counts.append(int(sum(nxt.values())))
        current = nxt

    return rho, entropy, counts


def prefix_result(rule: int, end_level: int) -> dict:
    levels = tuple(range(1, end_level + 1))
    transitions, alphabet, radius = labeled_source_graph(rule, levels)
    subsets, dfa = determinize(transitions, alphabet)
    minimized = minimize_partial_dfa(dfa, alphabet)
    recurrent = recurrent_sccs(
        minimized["transitions"], minimized["accepting"]
    )
    rho, entropy, block_counts = entropy_and_block_counts(
        minimized["transitions"],
        minimized["accepting"],
        minimized["start"],
    )

    subset_sizes = [len(s) for s in subsets]
    return {
        "prefix_levels": list(levels),
        "prefix_names": ["G", "Q", "R", "A4", "A5"][:end_level],
        "source_radius": radius,
        "source_debruijn_states": len(transitions),
        "realized_alphabet_size": len(alphabet),
        "determinized_states": len(subsets),
        "minimal_dfa_accepting_states": int(sum(minimized["accepting"])),
        "recurrent_scc_count": len(recurrent),
        "recurrent_states": int(sum(len(c) for c in recurrent)),
        "largest_recurrent_scc": max((len(c) for c in recurrent), default=0),
        "perron_eigenvalue": rho,
        "topological_entropy_bits_per_site": entropy,
        "entropy_gap_from_source": 1.0 - entropy,
        "allowed_block_counts_length_1_to_16": block_counts,
        "compatible_source_contexts": {
            "minimum": min(subset_sizes),
            "median": float(np.median(subset_sizes)),
            "maximum": max(subset_sizes),
            "has_singleton_context": min(subset_sizes) == 1,
        },
    }


def main() -> None:
    result = {
        "schema": "commutator-jet-language-v1",
        "date": "2026-10-07",
        "protocol": (
            "docs/research/protocols/"
            "commutator-jet-language-20261007.md"
        ),
        "rules": {},
    }

    for rule in RULES:
        rows = [prefix_result(rule, end) for end in PREFIX_ENDS]
        result["rules"][str(rule)] = rows

    result["summary"] = {
        "110_minimal_dfa_states": [
            row["minimal_dfa_accepting_states"]
            for row in result["rules"]["110"]
        ],
        "62_minimal_dfa_states": [
            row["minimal_dfa_accepting_states"]
            for row in result["rules"]["62"]
        ],
        "110_entropy": [
            row["topological_entropy_bits_per_site"]
            for row in result["rules"]["110"]
        ],
        "62_entropy": [
            row["topological_entropy_bits_per_site"]
            for row in result["rules"]["62"]
        ],
        "110_first_full_entropy_to_1e-12": next(
            (
                row["prefix_names"]
                for row in result["rules"]["110"]
                if abs(row["topological_entropy_bits_per_site"] - 1.0)
                < 1e-12
            ),
            None,
        ),
        "62_first_full_entropy_to_1e-12": next(
            (
                row["prefix_names"]
                for row in result["rules"]["62"]
                if abs(row["topological_entropy_bits_per_site"] - 1.0)
                < 1e-12
            ),
            None,
        ),
        "presentation_state_counts_stabilize_through_A5": False,
    }

    result["source_hashes"] = {
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
