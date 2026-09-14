"""Bounded sequential native-lift pilot; see the frozen 2026-09-14 protocol.

Each parent is an immutable, completed native law. Production construction uses
only that law, its declared finite invariant family, and its fixed recipe.
An original-ECA oracle appears only in the independent verification functions.
No scientific run occurs on import or in --self-test.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time

import numpy as np

RULES = (90, 54, 110, 157, 171, 233)
WIDTH = 7
PROTOCOL = "docs/research/protocols/sequential-lift-6d-pilot-20260914.md"
BASELINE = "8c3f4081c03cc73a960287494c143f5674aea7df"


@dataclass(frozen=True)
class Recipe:
    mask: str
    temporal: bool = False
    directed: bool = False

    @property
    def period(self):
        return 5 if self.temporal else 4


def recipe_for(rule):
    if rule not in RULES:
        raise ValueError("Rule outside frozen population")
    return Recipe("stay-one" if rule == 157 else "birth", rule in (171, 233), rule in (171, 233))


def all_words(width=WIDTH):
    return ((np.arange(1 << width)[:, None] >> np.arange(width - 1, -1, -1)) & 1).astype(np.uint8)


def rss_bytes():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024


class Budget:
    def __init__(self, total_deadline, seconds=120):
        self.deadline = min(total_deadline, time.perf_counter() + seconds)

    def check(self):
        if time.perf_counter() > self.deadline:
            raise TimeoutError("Frozen computation deadline")
        if rss_bytes() > 4 * 1024**3:
            raise MemoryError("Frozen 4 GiB RSS soft ceiling")


class PatchKeys:
    """Exact ordered trees for full radius-two binary neighborhoods.

    A leaf is five horizontal bits. Each subsequent level interns ordered
    five-tuples of child identifiers. Dict keys compare exact bytes: hash
    collisions cannot identify different patterns. No physical phase label
    enters a key. Lookup may cache new trees but never changes rule outputs.
    """
    def __init__(self, dimension):
        self.dimension = dimension
        self.ids = [dict() for _ in range(dimension - 1)]
        self.nodes = [[] for _ in range(dimension - 1)]

    def keys(self, grid, budget=None):
        if grid.ndim - 1 != self.dimension:
            raise ValueError("Wrong grid dimension")
        result = np.zeros(grid.shape, dtype=np.uint32)
        for dx in range(-2, 3):
            result = (result << 1) | np.roll(grid, -dx, axis=-1)
        for depth, axis in enumerate(range(grid.ndim - 2, 0, -1)):
            if budget:
                budget.check()
            # Full five entries, including exact repeats on period-four axes.
            chunks = np.stack([np.roll(result, -offset, axis=axis) for offset in range(-2, 3)], axis=-1)
            flat = np.ascontiguousarray(chunks.reshape(-1, 5), dtype=np.uint32)
            packed = flat.view("V20").ravel()
            unique, inverse = np.unique(packed, return_inverse=True)
            index = np.empty(len(unique), dtype=np.uint32)
            pool, nodes = self.ids[depth], self.nodes[depth]
            for i, value in enumerate(unique):
                key = bytes(value)
                found = pool.get(key)
                if found is None:
                    found = len(nodes)
                    pool[key] = found
                    nodes.append(tuple(int(v) for v in np.frombuffer(key, dtype=np.uint32)))
                index[i] = found
            result = index[inverse].reshape(grid.shape)
        if budget:
            budget.check()
        return result

    def expand(self, identifier, depth=None):
        if depth is None:
            depth = self.dimension - 2
        if depth < 0:
            return tuple((int(identifier) >> bit) & 1 for bit in range(4, -1, -1))
        return tuple(bit for child in self.nodes[depth][int(identifier)] for bit in self.expand(child, depth - 1))

    def stats(self):
        return [len(nodes) for nodes in self.nodes]


def table_from_constraints(keys, targets):
    flat = keys.ravel()
    values = np.broadcast_to(targets, keys.shape).ravel().astype(np.uint8)
    masks = np.zeros(int(flat.max()) + 1, dtype=np.uint8)
    np.bitwise_or.at(masks, flat, np.left_shift(np.uint8(1), values))
    conflicts = np.flatnonzero(masks == 3)
    witness = None
    if len(conflicts):
        key = int(conflicts[0])
        events = [int(np.flatnonzero((flat == key) & (values == bit))[0]) for bit in (0, 1)]
        witness = {"key_id": key, "events": events, "targets": [0, 1]}
    return (masks == 2).astype(np.uint8), {"passes": not len(conflicts), "conflicting_keys": len(conflicts), "forced_keys": int(np.count_nonzero(masks)), "witness": witness}


def lookup(table, keys):
    result = np.zeros(keys.shape, dtype=np.uint8)
    valid = keys < len(table)
    result[valid] = table[keys[valid]]
    return result


class ECALaw:
    def __init__(self, rule):
        self.rule = rule

    def step(self, grid, budget=None):
        index = (np.roll(grid, 1, axis=-1) << 2) | (grid << 1) | np.roll(grid, -1, axis=-1)
        return ((self.rule >> index) & 1).astype(np.uint8)


class NativeLaw:
    def __init__(self, keyer, derivative, decoder):
        self.keyer = keyer
        self.derivative = derivative.copy()
        self.decoder = decoder.copy()
        self.derivative.flags.writeable = False
        self.decoder.flags.writeable = False
        self.table_digest = hashlib.sha256(self.derivative.tobytes() + self.decoder.tobytes()).hexdigest()

    def step(self, grid, budget=None):
        return grid ^ lookup(self.derivative, self.keyer.keys(grid, budget))

    def recover(self, grid, budget=None):
        decoded = lookup(self.decoder, self.keyer.keys(grid, budget))
        parent = decoded[:, 0]
        if not np.array_equal(decoded, np.broadcast_to(parent[:, None], decoded.shape)):
            raise AssertionError("Parent decoder differs across child phases")
        return parent

    def assert_immutable(self):
        assert self.table_digest == hashlib.sha256(self.derivative.tobytes() + self.decoder.tobytes()).hexdigest()


def shift_vector(grid, amount):
    result = np.roll(grid, -amount, axis=-1)
    if grid.ndim > 2:
        result = np.roll(result, -amount, axis=1)
    return result


def encode_native(x, y, z, recipe):
    delta = x ^ y
    p = x ^ shift_vector(x, 1)
    m = (1 - x) & delta if recipe.mask == "birth" else x & (1 - delta)
    left, right = shift_vector(x, -1), shift_vector(x, 2)
    q = ((1 - left) if recipe.directed else left) & right
    fields = [p, delta]
    if recipe.temporal:
        fields.append(1 ^ x ^ z)
    fields.extend([m, q])
    return np.stack(fields, axis=1)


def direct_patch(grid, event):
    source, *coordinate = event
    shape = grid.shape[1:]
    return tuple(int(grid[(source,) + tuple((c + o) % n for c, o, n in zip(coordinate, offsets, shape))])
                 for offsets in itertools.product(range(-2, 3), repeat=len(shape)))


def reference_source_step(grid, rule):
    # Scalar truth-table definition, independent of the production vector step.
    answer = np.empty_like(grid)
    for row in range(len(grid)):
        for i in range(grid.shape[-1]):
            bits = [int(grid[row, j % grid.shape[-1]]) for j in (i - 1, i, i + 1)]
            answer[row, i] = (rule >> (4 * bits[0] + 2 * bits[1] + bits[2])) & 1
    return answer


def reference_stack(a, b, c, rule):
    def moved(x, amount):
        y = np.take(x, (np.arange(x.shape[-1]) + amount) % x.shape[-1], axis=-1)
        if x.ndim > 2:
            y = np.take(y, (np.arange(y.shape[1]) + amount) % y.shape[1], axis=1)
        return y
    delta = np.not_equal(a, b).astype(np.uint8)
    polar = np.not_equal(a, moved(a, 1)).astype(np.uint8)
    marker = np.logical_and(a, np.logical_not(delta)) if rule == 157 else np.logical_and(np.logical_not(a), delta)
    first, second = moved(a, -1), moved(a, 2)
    ref = np.logical_and(np.logical_not(first) if rule in (171, 233) else first, second)
    fields = [polar, delta]
    if rule in (171, 233):
        fields.append(np.equal(a, c))
    fields.extend([marker, ref])
    return np.stack(fields, axis=1).astype(np.uint8)


def oracle(rule, dimension):
    states = [all_words()]
    for _ in range(2 * (dimension - 1) + 2):
        states.append(reference_source_step(states[-1], rule))
    for _ in range(dimension - 1):
        states = [reference_stack(states[t], states[t + 1], states[t + 2], rule) for t in range(len(states) - 2)]
    assert len(states) == 3
    return states


def verify_patches(grid, keys, keyer):
    period = grid.shape[1]
    checks = 0
    for source in (0, 1, 42, 85, 127):
        for phase in (0, 1, period - 1):
            event = (source,) + (phase,) * (grid.ndim - 2) + (0,)
            assert keyer.expand(int(keys[event])) == direct_patch(grid, event), event
            checks += 1
    return checks


def decode_witness(gate, grid, targets, rule, dimension):
    witness = gate["witness"]
    if witness is None:
        return None
    events = [tuple(int(v) for v in np.unravel_index(e, grid.shape)) for e in witness["events"]]
    patches = [direct_patch(grid, event) for event in events]
    assert patches[0] == patches[1]
    expanded = np.broadcast_to(targets, grid.shape)
    assert [int(expanded[event]) for event in events] == [0, 1]
    return {"rule": rule, "dimension": dimension, "events": [list(e) for e in events],
            "source_words": [all_words()[e[0]].tolist() for e in events], "targets": [0, 1],
            "full_patch_bits": len(patches[0]), "full_patch_hex": np.packbits(patches[0], bitorder="big").tobytes().hex(),
            "directly_reproduced": True}


def run_floor(rule, dimension, parent, family, chain, total_deadline):
    start = time.perf_counter()
    budget = Budget(total_deadline)
    recipe = recipe_for(rule)
    before = [law.table_digest for law in chain]
    y = parent.step(family, budget)
    z = parent.step(y, budget)
    w = parent.step(z, budget)
    child = encode_native(family, y, z, recipe)
    target = encode_native(y, z, w, recipe)
    keyer = PatchKeys(dimension)
    keys = keyer.keys(child, budget)
    derivative, native = table_from_constraints(keys, child ^ target)
    decoder, recovery = table_from_constraints(keys, family[:, None])
    row = {"rule": rule, "dimension": dimension, "source_width": WIDTH, "source_states": 1 << WIDTH,
           "transverse_period": recipe.period, "fields_per_source_site": recipe.period ** (dimension - 1),
           "cells_per_configuration": int(np.prod(child.shape[1:])), "checked_native_cells": int(child.size),
           "full_neighborhood_bits": 5 ** dimension, "distinct_periodic_neighborhood_bits": 5 * recipe.period ** (dimension - 1),
           "native": native, "parent_recovery": recovery, "completion": "all unforced derivative and decoder outputs zero",
           "build_seconds": time.perf_counter() - start}
    for gate, targets in ((native, child ^ target), (recovery, family[:, None])):
        gate["witness"] = decode_witness(gate, child, targets, rule, dimension)
    if not native["passes"] or not recovery["passes"]:
        row.update(status="failed", wall_seconds=time.perf_counter() - start, peak_rss_bytes=rss_bytes())
        return row, None, None
    law = NativeLaw(keyer, derivative, decoder)
    verify_start = time.perf_counter()
    row["direct_patch_checks"] = verify_patches(child, keys, keyer)
    expected = oracle(rule, dimension)
    assert np.array_equal(child, expected[0]), (rule, dimension, "reference encoding")
    step_start = time.perf_counter()
    actual1 = law.step(child, budget)
    actual2 = law.step(actual1, budget)
    row["two_native_batch_steps_seconds"] = time.perf_counter() - step_start
    assert np.array_equal(actual1, expected[1]), (rule, dimension, "first native step")
    assert np.array_equal(actual2, expected[2]), (rule, dimension, "second native step")
    # Check every immediate-parent decoder output, not only the selected slice.
    decoded = lookup(decoder, keys)
    assert np.array_equal(decoded, np.broadcast_to(family[:, None], decoded.shape))
    recovered = decoded[:, 0]
    for ancestor in reversed(chain):
        recovered = ancestor.recover(recovered, budget)
    assert np.array_equal(recovered, all_words()), (rule, dimension, "composed source recovery")
    for ancestor, digest in zip(chain, before):
        ancestor.assert_immutable()
        assert digest == ancestor.table_digest
    law.assert_immutable()
    row.update(status="passed", native_replay=True, decoder_replay=True, composed_source_recovery=True,
               parent_rules_unchanged=True, verification_seconds=time.perf_counter() - verify_start,
               key_nodes_by_depth=keyer.stats(), forced_table_sha256=law.table_digest,
               wall_seconds=time.perf_counter() - start, peak_rss_bytes=rss_bytes())
    return row, law, child


def self_test():
    grid = np.zeros((3, 4, 4, 7), dtype=np.uint8)
    grid[0, 0, 0, 0] = 1
    keyer = PatchKeys(3)
    keys = keyer.keys(grid)
    forward, reverse = {}, {}
    for event in np.ndindex(grid.shape):
        patch = direct_patch(grid, event)
        identifier = int(keys[event])
        assert identifier not in forward or forward[identifier] == patch
        assert patch not in reverse or reverse[patch] == identifier
        forward[identifier] = patch
        reverse[patch] = identifier
        assert keyer.expand(identifier) == patch
    assert len(forward) > 1
    assert np.array_equal(keys[1], keys[2])
    _, gate = table_from_constraints(np.array([7, 7]), np.array([0, 1]))
    assert not gate["passes"] and gate["witness"]["targets"] == [0, 1]
    law = NativeLaw(keyer, np.zeros(1, dtype=np.uint8), np.zeros(1, dtype=np.uint8))
    assert np.array_equal(law.step(np.ones_like(grid)), np.ones_like(grid))
    print(json.dumps({"self_test": "passed", "direct_patches": int(grid.size), "unique_patches": len(forward)}), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--implementation-commit", default="unrecorded")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if args.output is None or args.implementation_commit == "unrecorded":
        parser.error("Canonical run requires --output and --implementation-commit")
    args.output.mkdir(parents=True, exist_ok=False)
    start = time.perf_counter()
    deadline = start + 15 * 60
    records = []
    with (args.output / "floors.jsonl").open("w") as log:
        for rule in RULES:
            family = all_words()
            parent = ECALaw(rule)
            chain = []
            for dimension in range(2, 7):
                if time.perf_counter() > deadline:
                    row = {"rule": rule, "dimension": dimension, "status": "censored", "reason": "total budget"}
                    new_law = new_family = None
                else:
                    try:
                        row, new_law, new_family = run_floor(rule, dimension, parent, family, chain, deadline)
                    except (TimeoutError, MemoryError) as error:
                        row = {"rule": rule, "dimension": dimension, "status": "censored", "reason": str(error), "peak_rss_bytes": rss_bytes()}
                        new_law = new_family = None
                records.append(row)
                log.write(json.dumps(row, sort_keys=True) + "\n")
                log.flush()
                print(json.dumps({k: row[k] for k in ("rule", "dimension", "status", "build_seconds", "wall_seconds", "peak_rss_bytes", "reason") if k in row}), flush=True)
                if row["status"] != "passed":
                    break
                parent, family = new_law, new_family
                chain.append(parent)
            del parent, family, chain
    root = Path(__file__).resolve().parents[1]
    hashes = {path: hashlib.sha256((root / path).read_bytes()).hexdigest() for path in (PROTOCOL, "scripts/sequential_lift_6d_pilot.py")}
    summary = {"schema_version": 1, "scope": "Six fixed recipes, every width-seven source state, all physical phases and positions; sequential native and recovery only",
               "baseline_commit": BASELINE, "implementation_commit": args.implementation_commit, "source_hashes": hashes,
               "rules": list(RULES), "width": WIDTH, "max_dimension": 6, "source_states_per_rule": 128,
               "passed_6d": [r["rule"] for r in records if r["dimension"] == 6 and r["status"] == "passed"],
               "failures": [r for r in records if r["status"] == "failed"], "censored": [r for r in records if r["status"] == "censored"],
               "completed_floors": len(records), "wall_seconds": time.perf_counter() - start, "peak_rss_bytes": rss_bytes()}
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
