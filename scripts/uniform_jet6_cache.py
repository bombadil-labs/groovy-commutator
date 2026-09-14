"""Frozen six-field finite-family cache rebuild; scientific execution is off CI."""
from __future__ import annotations

import argparse
import base64
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import platform
import resource
import tempfile
import time

import numpy as np

import on_beam_256_4d as old
import on_beam_rule_analysis as statistics
import sequential_lift_6d_pilot as core

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = "docs/research/protocols/uniform-jet6-cache-20260914.md"
BASELINE = "bbe6d8b677544d7521fee572e8fcd04328971967"
OLD_RUN = ROOT / "experiments/on_beam_256_4d_20260914/run"
SOURCES = ("scripts/uniform_jet6_cache.py", "scripts/uniform_jet6_analysis.py",
           "scripts/on_beam_256_4d.py", "scripts/on_beam_rule_analysis.py",
           "scripts/sequential_lift_6d_pilot.py", PROTOCOL, old.LABELS, old.RECIPES,
           "experiments/on_beam_256_4d_20260914/run/floors.jsonl",
           "experiments/on_beam_256_4d_20260914/run/paths.jsonl",
           "experiments/on_beam_256_4d_20260914/run/summary.json")


def frozen(array):
    value = np.array(array, copy=True)
    value.flags.writeable = False
    return value


def radii(dimension, mode="jet6"):
    return (3 if mode == "jet6" else 2,) * (dimension - 1) + (2,)


def shifted(x, dx):
    result = np.roll(x, -dx, axis=-1)
    return np.roll(result, -1, axis=1) if x.ndim > 2 else result


def fields(x, y, z=None, mode="jet6", recipe=None):
    if mode == "old4":
        return old.encode(x, y, recipe)
    d, t = x ^ y, x ^ z
    return np.stack((x ^ shifted(x, 1), x ^ shifted(x, -1), d, t,
                     x & d, x & (1 ^ d)), axis=1)


def flip_fields(x, y, z, w):
    d, t = x ^ y, x ^ z
    return np.stack((d ^ shifted(d, 1), d ^ shifted(d, -1), t,
                     d ^ z ^ w, d ^ (y & t), y & t), axis=1)


def reference_fields(x, y, z):
    def move(dx):
        out = np.take(x, (np.arange(x.shape[-1]) + dx) % x.shape[-1], axis=-1)
        if x.ndim > 2:
            out = np.take(out, (np.arange(x.shape[1]) + 1) % x.shape[1], axis=1)
        return out.astype(bool)
    a, b, c = x.astype(bool), y.astype(bool), z.astype(bool)
    return np.stack((a != move(1), a != move(-1), a != b, a != c,
                     a & ~b, a & b), axis=1).astype(np.uint8)


def scalar_fields(x, y, z):
    answer = np.empty((len(x), 6, *x.shape[1:]), dtype=np.uint8)
    for at in np.ndindex(x.shape):
        def move(dx):
            index = list(at)
            index[-1] = (index[-1] + dx) % x.shape[-1]
            if x.ndim > 2:
                index[1] = (index[1] + 1) % x.shape[1]
            return int(x[tuple(index)])
        a, b, c = int(x[at]), int(y[at]), int(z[at])
        values = (a ^ move(1), a ^ move(-1), a ^ b, a ^ c,
                  int(a == 1 and b == 0), int(a == 1 and b == 1))
        for phase, value in enumerate(values):
            answer[(at[0], phase, *at[1:])] = value
    return answer


class Reference:
    """Lazy original-ECA oracle, independent of production native law/cache."""
    def __init__(self, rule, width, mode, recipe):
        self.rule, self.mode, self.recipe = rule, mode, recipe
        self.values = {(1, 0): core.all_words(width)}

    def get(self, dimension, tick):
        key = dimension, tick
        if key not in self.values:
            if dimension == 1:
                value = core.reference_source_step(self.get(1, tick-1), self.rule)
            else:
                x, y = self.get(dimension-1, tick), self.get(dimension-1, tick+1)
                if self.mode == "jet6":
                    value = reference_fields(x, y, self.get(dimension-1, tick+2))
                else:
                    value = old.reference_encode(x, y, self.recipe)
            self.values[key] = value
        return self.values[key]


class PhysicalKeys:
    """Exact mixed-radius tuple DAG; source-batch indices never enter a key."""
    def __init__(self, radius):
        self.radius = tuple(radius)
        self.ids = [dict() for _ in radius[:-1]]
        self.nodes = [[] for _ in radius[:-1]]
        self.calls = 0

    def keys(self, grid, budget=None):
        assert grid.ndim == len(self.radius) + 1
        self.calls += 1
        result = np.zeros(grid.shape, dtype=np.uint32)
        for dx in range(-self.radius[-1], self.radius[-1]+1):
            result = (result << 1) | np.roll(grid, -dx, axis=-1)
        for depth, axis in enumerate(range(grid.ndim-2, 0, -1)):
            if budget:
                budget.check()
            r = self.radius[axis-1]
            arity = 2*r+1
            chunks = np.stack([np.roll(result, -a, axis=axis) for a in range(-r, r+1)], axis=-1)
            packed = np.ascontiguousarray(chunks, dtype="<u4").reshape(-1, arity).view(f"V{4*arity}").ravel()
            unique, inverse = np.unique(packed, return_inverse=True)
            remap = np.empty(len(unique), dtype=np.uint32)
            pool, nodes = self.ids[depth], self.nodes[depth]
            for i, item in enumerate(unique):
                key = bytes(item)
                identifier = pool.get(key)
                if identifier is None:
                    identifier = len(nodes)
                    pool[key] = identifier
                    nodes.append(tuple(int(v) for v in np.frombuffer(key, dtype="<u4")))
                remap[i] = identifier
            result = remap[inverse].reshape(grid.shape)
        return result

    def expand(self, identifier, depth=None):
        if depth is None:
            depth = len(self.radius)-2
        if depth < 0:
            return tuple((int(identifier) >> bit) & 1 for bit in range(2*self.radius[-1], -1, -1))
        return tuple(b for child in self.nodes[depth][int(identifier)]
                     for b in self.expand(child, depth-1))


def direct_patch(grid, event, radius):
    source, *coordinate = event
    return tuple(int(grid[(source,) + tuple((c+a) % n for c, a, n in zip(coordinate, offsets, grid.shape[1:]))])
                 for offsets in itertools.product(*(range(-r, r+1) for r in radius)))


class NativeLaw:
    def __init__(self, keyer, derivative, decoder):
        self.keyer = keyer
        self.derivative, self.decoder = frozen(derivative), frozen(decoder)
        self.digest = old.sha(self.derivative.tobytes() + self.decoder.tobytes())

    def assert_immutable(self):
        assert self.digest == old.sha(self.derivative.tobytes() + self.decoder.tobytes())

    def step_grid(self, grid, budget=None):
        self.assert_immutable()
        return grid ^ core.lookup(self.derivative, self.keyer.keys(grid, budget))


class Beam:
    """Memoization scoped to one immutable native law and exact finite family.

    Build native successors once, then establish an exact row-byte reindexing.
    Subsequent family/key reindexing follows that checked native map, never an
    original-ECA oracle. Public input arrays are copied to prevent stale caches.
    """
    def __init__(self, array, law, keys=None, budget=None):
        self.grid, self.law, self.budget = frozen(array), law, budget
        self.base_keys = None if keys is None else frozen(keys)
        self.states = {0: self.grid}
        self.indices = {0: np.arange(len(array))}
        self.key_states = {}
        self.next_index = None
        self.native_evaluations = self.state_hits = self.key_hits = 0

    def keys(self, tick=0):
        if self.base_keys is None:
            self.base_keys = frozen(self.law.keyer.keys(self.grid, self.budget))
        if tick == 0:
            self.key_hits += 1
            return self.base_keys
        self.state(tick)
        if tick not in self.key_states:
            self.key_states[tick] = frozen(self.base_keys[self.indices[tick]])
        self.key_hits += 1
        return self.key_states[tick]

    def state(self, tick):
        if isinstance(self.law, NativeLaw):
            self.law.assert_immutable()
        if tick in self.states:
            self.state_hits += 1
            return self.states[tick]
        if self.budget:
            self.budget.check()
        if self.next_index is None:
            if isinstance(self.law, NativeLaw):
                self.law.assert_immutable()
                successor = self.grid ^ core.lookup(self.law.derivative, self.keys())
            else:
                successor = self.law.step(self.grid)
            self.native_evaluations += 1
            # Exact bytes, including all spatial cells; dimensions are fixed by this Beam.
            family = {row.tobytes(): i for i, row in enumerate(self.grid)}
            assert len(family) == len(self.grid), "Source encoding must be injective"
            try:
                self.next_index = np.array([family[row.tobytes()] for row in successor], dtype=np.int64)
            except KeyError as exc:
                raise AssertionError("Native successor left its finite family") from exc
            assert np.array_equal(successor, self.grid[self.next_index])
        self.state(tick-1)
        self.indices[tick] = self.next_index[self.indices[tick-1]]
        self.states[tick] = frozen(self.grid[self.indices[tick]])
        return self.states[tick]

    def recovered(self):
        decoded = core.lookup(self.law.decoder, self.keys())
        parent = decoded[:, 0]
        assert np.array_equal(decoded, np.broadcast_to(parent[:, None], decoded.shape))
        return parent

    def counters(self):
        return {"native_family_evaluations": self.native_evaluations,
                "state_cache_hits": self.state_hits, "key_cache_hits": self.key_hits,
                "physical_key_builds": self.law.keyer.calls if isinstance(self.law, NativeLaw) else 0,
                "materialized_ticks": sorted(self.states),
                "array_cache_bytes": sum(a.nbytes for a in self.states.values()) +
                     (self.base_keys.nbytes if self.base_keys is not None else 0) +
                     sum(a.nbytes for a in self.key_states.values())}


def packed(array):
    return base64.b64encode(np.packbits(array, bitorder="big").tobytes()).decode()


def unpacked(text, shape):
    raw = base64.b64decode(text, validate=True)
    count = int(np.prod(shape))
    assert len(raw) == (count+7)//8
    bits = np.unpackbits(np.frombuffer(raw, dtype=np.uint8), bitorder="big")
    assert not np.any(bits[count:])
    return bits[:count].reshape(shape)


def export_record(beam, truth, width, rule, dimension, mode, recipe):
    keys = beam.keys()
    unique, representatives = np.unique(keys.ravel(), return_index=True)
    assert np.array_equal(unique, np.arange(len(beam.law.derivative)))
    record = {"format": "grid-referenced-physical-partial-rule-v1", "rule": rule,
              "width": width, "dimension": dimension, "mode": mode,
              "recipe": {"family": "uniform-six-field"} if mode == "jet6" else recipe.record(),
              "radii_array_order": list(beam.law.keyer.radius),
              "neighborhood_order": "lexicographic offsets in stored spatial-axis order; source batch excluded",
              "grid_shape": list(beam.grid.shape), "grid_bits_big": packed(beam.grid),
              "representative_flat_indices_u32le": base64.b64encode(representatives.astype("<u4").tobytes()).decode(),
              "forced_root_count": len(unique), "forced_derivative_bits_big": packed(beam.law.derivative),
              "forced_decoder_bits_big": packed(beam.law.decoder),
              "source_phase_shape": list(truth.shape), "source_phase_derivative_bits_big": packed(truth),
              "unforced_derivative": 0, "unforced_decoder": 0,
              "native_table_sha256": beam.law.digest}
    # Verify every stored array and representative before the cache leaves this process.
    assert np.array_equal(unpacked(record["grid_bits_big"], beam.grid.shape), beam.grid)
    for name, original in (("forced_derivative_bits_big", beam.law.derivative),
                           ("forced_decoder_bits_big", beam.law.decoder),
                           ("source_phase_derivative_bits_big", truth)):
        assert np.array_equal(unpacked(record[name], original.shape), original)
    restored = np.frombuffer(base64.b64decode(record["representative_flat_indices_u32le"], validate=True), dtype="<u4")
    assert np.array_equal(restored, representatives)
    assert np.array_equal(keys.ravel()[restored], unique)
    return record, restored


def witness(gate, grid, targets, radius):
    if gate["witness"] is None:
        return None
    events = [tuple(int(x) for x in np.unravel_index(i, grid.shape)) for i in gate["witness"]["events"]]
    patches = [direct_patch(grid, e, radius) for e in events]
    assert patches[0] == patches[1]
    wanted = np.broadcast_to(targets, grid.shape)
    assert [int(wanted[e]) for e in events] == [0, 1]
    return {"events": [list(e) for e in events], "targets": [0, 1],
            "source_words": [core.all_words(grid.shape[-1])[e[0]].tolist() for e in events],
            "patch_bits": len(patches[0]), "patch_hex": np.packbits(patches[0], bitorder="big").tobytes().hex(),
            "directly_verified": True}


def run_floor(rule, width, dimension, parent, chain, reference, mode, recipe, budget, archive):
    start = time.perf_counter()
    budget.check()
    before = [b.law.digest for b in chain]
    x, y, z = parent.grid, parent.state(1), parent.state(2)
    w = parent.state(3) if mode == "jet6" else None
    child = fields(x, y, z, mode, recipe)
    target = fields(y, z, w, mode, recipe)
    keyer = PhysicalKeys(radii(dimension, mode))
    keys = keyer.keys(child, budget)
    derivative, native = core.table_from_constraints(keys, child ^ target)
    decoder, recovery = core.table_from_constraints(keys, x[:, None])
    period = 6 if mode == "jet6" else 4
    aligned = bool(np.array_equal(child[:, 4] ^ child[:, 5], x)) if mode == "jet6" else None
    row = {"rule": rule, "width": width, "dimension": dimension, "mode": mode,
           "period": period, "source_states": 2**width, "phase_count": period**(dimension-1),
           "constraint_cells": child.size, "radii_array_order": list(keyer.radius),
           "native": native, "uniform_parent_recovery": recovery, "aligned_recovery": aligned,
           "build_seconds": time.perf_counter()-start}
    native["witness"] = witness(native, child, child ^ target, keyer.radius)
    recovery["witness"] = witness(recovery, child, x[:, None], keyer.radius)
    if not native["passes"] or not recovery["passes"] or aligned is False:
        row.update(status="failed", failure_kind="native" if not native["passes"] else "aligned_decoder" if aligned is False else "uniform_decoder",
                   wall_seconds=time.perf_counter()-start)
        return row, None
    law = NativeLaw(keyer, derivative, decoder)
    beam = Beam(child, law, keys, budget)
    check_start = time.perf_counter()
    if mode == "jet6":
        assert np.array_equal(child ^ target, flip_fields(x, y, z, w))
    for tick in range(3):
        assert np.array_equal(beam.state(tick), reference.get(dimension, tick)), (rule, width, dimension, tick)
    recovered = beam.recovered()
    assert np.array_equal(recovered, x)
    for ancestor in reversed(chain):
        # Exact equality justifies reuse of this ancestor's physical keys.
        assert np.array_equal(recovered, ancestor.grid)
        recovered = ancestor.recovered()
    assert np.array_equal(recovered, core.all_words(width))
    for b, digest in zip(chain, before):
        b.law.assert_immutable()
        assert digest == b.law.digest
    law.assert_immutable()
    # An uncached key pass on a fixed sample checks batch reindexing physically.
    sample = np.array([0, 1, min(42, 2**width-1), 2**width-1])
    sampled = keyer.keys(beam.state(2)[sample], budget)
    assert np.array_equal(sampled, beam.keys(2)[sample])
    direct_checks = 0
    for source in (0, 1, 42, 85, 2**width-1):
        for phase in (0, 1, period-1):
            at = (source,) + (phase,)*(dimension-1) + (0,)
            assert keyer.expand(int(keys[at])) == direct_patch(child, at, keyer.radius)
            direct_checks += 1
    row.update(verification_seconds=time.perf_counter()-check_start, native_replay=True,
               parent_replay=True, source_recovery=True, parents_immutable=True,
               direct_patch_checks=direct_checks, uncached_sample_states=len(sample))
    metric_start = time.perf_counter()
    features, detail, truth = old.truth_features(child ^ target)
    features["key_fraction"] = len(derivative) / ((2**width) * period**(dimension-1))
    features["forced_flip_fraction"] = float(derivative.mean())
    row.update(features=features, phase_analysis=detail, metric_seconds=time.perf_counter()-metric_start)
    export_start = time.perf_counter()
    record, reps = export_record(beam, truth, width, rule, dimension, mode, recipe)
    for root in (0, len(reps)//2, len(reps)-1):
        at = tuple(int(v) for v in np.unravel_index(int(reps[root]), child.shape))
        assert direct_patch(child, at, keyer.radius) == keyer.expand(root)
    member = archive.add(f"w{width}/rule{rule:03d}/d{dimension}.json", record)
    row.update(status="passed", partial_rule=member, native_sha256=law.digest,
               node_counts=[len(n) for n in keyer.nodes], cache=beam.counters(),
               export_seconds=time.perf_counter()-export_start, wall_seconds=time.perf_counter()-start,
               peak_rss_bytes=old.resident())
    return row, beam


def source_features(beam):
    f, _, _ = old.truth_features(beam.grid ^ beam.state(1))
    return {"event_flip_fraction": f["event_flip_fraction"],
            "source_degree_fraction": f["source_degree_fraction"],
            "source_term_fraction": f["source_term_fraction"],
            "image_fraction": len(set(beam.next_index.tolist())) / len(beam.grid)}


def key_microbenchmark(beam):
    measurements = {"cached": [], "uncached": []}
    grid = beam.state(1)
    for repeat in range(3):
        order = ("cached", "uncached") if repeat % 2 == 0 else ("uncached", "cached")
        answers = {}
        for mode in order:
            start = time.perf_counter()
            answers[mode] = beam.keys(1) if mode == "cached" else beam.law.keyer.keys(grid, beam.budget)
            measurements[mode].append(time.perf_counter()-start)
        assert np.array_equal(answers["cached"], answers["uncached"])
    return {"seconds": measurements, "cached_median": float(np.median(measurements["cached"])),
            "uncached_median": float(np.median(measurements["uncached"])), "cells": grid.size,
            "all_keys_equal": True}


def run_path(rule, width, mode, deadline, archive, recipe=None, micro=False):
    start = time.perf_counter()
    budget = old.Budget(min(deadline, start+120))
    reference = Reference(rule, width, mode, recipe)
    parent = Beam(core.all_words(width), core.ECALaw(rule), budget=budget)
    base_features = source_features(parent)
    chain, rows, microseconds = [], [], 0.0
    status, reason, last = "passed", None, 1
    for dimension in (2, 3, 4):
        try:
            row, beam = run_floor(rule, width, dimension, parent, chain, reference, mode, recipe, budget, archive)
        except (TimeoutError, MemoryError) as exc:
            status, reason = "censored", str(exc)
            rows.append({"rule": rule, "width": width, "dimension": dimension, "mode": mode,
                         "status": "censored", "reason": reason})
            break
        except AssertionError as exc:
            status, reason = "failed", "verification: " + str(exc)
            rows.append({"rule": rule, "width": width, "dimension": dimension, "mode": mode,
                         "status": "failed", "failure_kind": "verification", "reason": reason})
            break
        rows.append(row)
        if row["status"] != "passed":
            status, reason = "failed", row["failure_kind"]
            break
        last = dimension
        if micro:
            mstart = time.perf_counter()
            row["key_microbenchmark"] = key_microbenchmark(beam)
            microseconds += time.perf_counter()-mstart
        parent = beam
        chain.append(beam)
    return rows, {"rule": rule, "width": width, "mode": mode, "status": status,
                  "reason": reason, "last_floor": last,
                  "later_floors_untested": [d for d in (2, 3, 4) if d > rows[-1]["dimension"]],
                  "source_features": base_features,
                  "cache_at_path_end": [b.counters() for b in chain],
                  "microbenchmark_seconds": microseconds,
                  "wall_seconds": time.perf_counter()-start-microseconds}


def benchmark(output):
    started = time.perf_counter()
    deadline = started+300
    records = []
    recipes = old.load_recipes()
    with tempfile.TemporaryDirectory() as temporary:
        for repeat in range(3):
            modes = ("old4", "jet6") if repeat % 2 == 0 else ("jet6", "old4")
            for mode in modes:
                for rule in (0, 30, 90, 110):
                    archive = old.Archive(Path(temporary) / f"{repeat}-{mode}-{rule}.tar.gz")
                    try:
                        rows, path = run_path(rule, 7, mode, deadline, archive, recipes[rule], micro=True)
                    finally:
                        archive.close()
                    with archive.path.open("rb") as stream:
                        checksum = hashlib.file_digest(stream, "sha256").hexdigest()
                    records.append({"repeat": repeat, "mode": mode, "rule": rule, "rows": rows,
                                    "path": path, "archive_bytes": archive.path.stat().st_size,
                                    "archive_sha256": checksum})
                    (output / "benchmark.json").write_bytes(old.canonical({"status": "running", "records": records}))
                    if time.perf_counter() > deadline:
                        result = {"status": "censored", "reason": "300-second timing budget", "records": records}
                        (output / "benchmark.json").write_bytes(old.canonical(result))
                        return result
    medians = {}
    for mode in ("old4", "jet6"):
        by_rule = {str(rule): float(np.median([r["path"]["wall_seconds"] for r in records
                                              if r["mode"] == mode and r["rule"] == rule and r["path"]["status"] == "passed"]))
                   for rule in (0, 30, 90, 110)
                   if all(r["path"]["status"] == "passed" for r in records if r["mode"] == mode and r["rule"] == rule)}
        medians[mode] = {"per_rule_median_seconds": by_rule,
                         "pooled_median_seconds": float(np.median(list(by_rule.values()))) if by_rule else None}
    result = {"status": "completed", "wall_seconds": time.perf_counter()-started,
              "scope": "Selected width-seven cold paths, matched backend; microbenchmarks excluded from path wall times",
              "medians": medians, "records": records}
    (output / "benchmark.json").write_bytes(old.canonical(result))
    return result


def self_test():
    rng = np.random.default_rng(20260914)
    count = 0
    for dimension in (1, 2, 3):
        shape = (2,) + (3,)*(dimension-1) + (5,)
        for _ in range(12):
            x, y, z, w = [rng.integers(0, 2, shape, dtype=np.uint8) for _ in range(4)]
            a = fields(x, y, z)
            assert np.array_equal(a, reference_fields(x, y, z))
            assert np.array_equal(a, scalar_fields(x, y, z))
            assert np.array_equal(a ^ fields(y, z, w), flip_fields(x, y, z, w))
            assert np.array_equal(a[:, 4] ^ a[:, 5], x)
            count += 1
    patches = 0
    for dimension in (1, 2, 3, 4):
        grid = rng.integers(0, 2, (2,) + (2,)*(dimension-1) + (3,), dtype=np.uint8)
        keyer = PhysicalKeys(radii(dimension))
        keys = keyer.keys(grid)
        for event in np.ndindex(grid.shape):
            assert keyer.expand(int(keys[event])) == direct_patch(grid, event, keyer.radius)
            patches += 1
        assert np.array_equal(keyer.keys(grid[::-1]), keys[::-1])
        moved = np.roll(grid, 1, axis=1)
        assert np.array_equal(keyer.keys(moved), np.roll(keys, 1, axis=1))
    words = core.all_words(3)
    identity = Beam(words, core.ECALaw(204))
    negation = Beam(words, core.ECALaw(51))
    words[:] ^= 1
    assert np.array_equal(identity.state(3), core.all_words(3))
    assert np.array_equal(negation.state(3), 1 ^ core.all_words(3))
    assert np.array_equal(negation.state(2), core.all_words(3))
    assert identity.native_evaluations == negation.native_evaluations == 1
    recipes = old.load_recipes()
    previous = {(r["rule"], r["dimension"]): r for r in [json.loads(x) for x in (OLD_RUN / "floors.jsonl").read_text().splitlines()]
                if r["width"] == 7}
    with tempfile.TemporaryDirectory() as temporary:
        archive = old.Archive(Path(temporary) / "controls.tar.gz")
        try:
            floors = []
            for rule in (90, 54, 110, 157):
                rows, path = run_path(rule, 7, "old4", time.perf_counter()+120, archive, recipes[rule])
                assert path["status"] == "passed", path
                for row in rows:
                    prior = previous[rule, row["dimension"]]
                    assert row["native"]["forced_keys"] == prior["native"]["forced_keys"]
                    assert row["features"] == prior["features"]
                    assert row["phase_analysis"] == prior["phase_analysis"]
                floors.extend(rows)
        finally:
            archive.close()
    # Known metrics and the exact symmetry orbit partition use the unchanged code.
    labels = json.loads((ROOT / old.LABELS).read_text())
    assert len(statistics.class_map(labels)[1]) == 88
    assert old.binary_rank(np.array([[1, 0], [0, 1]], dtype=np.uint8)) == 2
    assert np.array_equal(old.mobius(np.array([[0, 1, 1, 0]], dtype=np.uint8)), [[0, 1, 1, 0]])
    return {"status": "passed", "scalar_field_cases": count, "mixed_radius_direct_patches": patches,
            "previous_floor_controls": len(floors), "cache_law_and_mutation_controls": True}


def execute(output, implementation_commit):
    import uniform_jet6_analysis as report
    output.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    deadline = started+1200
    execution = {"utc_start": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                 "baseline_commit": BASELINE, "implementation_commit": implementation_commit,
                 "source_hashes": {p: old.sha((ROOT/p).read_bytes()) for p in SOURCES},
                 "python": platform.python_version(), "numpy": np.__version__, "platform": platform.platform(),
                 "widths": [7, 8], "rules": list(range(256)), "dimensions": [2, 3, 4],
                 "operator": "uniform-six-field", "period": 6, "radii": "line2/lifted3",
                 "cache_representation": "grid-referenced-physical-partial-rule-v1"}
    (output / "execution.json").write_bytes(old.canonical(execution))
    all_rows, paths, finalization_censor = [], [], None
    archive = old.Archive(output / "uniform_jet6_rules.tar.gz")
    try:
        with (output / "floors.jsonl").open("w") as rowlog, (output / "paths.jsonl").open("w") as pathlog:
            for width in (7, 8):
                for rule in range(256):
                    if time.perf_counter() > deadline or old.resident() > 4*1024**3:
                        rows = []
                        path = {"rule": rule, "width": width, "mode": "jet6", "status": "censored",
                                "reason": "overall wall or RSS budget", "last_floor": 1,
                                "later_floors_untested": [2, 3, 4]}
                    else:
                        rows, path = run_path(rule, width, "jet6", deadline, archive)
                    all_rows.extend(rows)
                    paths.append(path)
                    for row in rows:
                        rowlog.write(old.canonical(row).decode()+"\n")
                    pathlog.write(old.canonical(path).decode()+"\n")
                    rowlog.flush()
                    pathlog.flush()
                    if rule % 32 == 31:
                        print(json.dumps({"width": width, "through_rule": rule,
                                          "paths": dict(Counter(p["status"] for p in paths)),
                                          "wall_seconds": time.perf_counter()-started}), flush=True)
    finally:
        # Always produce a readable archive, including interrupted/budgeted paths.
        archive.close()
    if time.perf_counter() > deadline:
        finalization_censor = "Primary deadline reached during archive finalization; preserve completed members"
    with archive.path.open("rb") as stream:
        archive_hash = hashlib.file_digest(stream, "sha256").hexdigest()
    manifest = {"format": "canonical-json-in-deterministic-tar-gzip", "archive_path": archive.path.name,
                "archive_sha256": archive_hash, "archive_size": archive.path.stat().st_size,
                "members": archive.members}
    (output / "archive_manifest.json").write_bytes(old.canonical(manifest))
    if time.perf_counter() <= deadline:
        analysis = report.analyze(all_rows, paths)
        (output / "analysis.json").write_bytes(old.canonical(analysis))
    else:
        analysis = {"status": "censored", "reason": "Primary deadline reached before class analysis"}
        (output / "analysis.json").write_bytes(old.canonical(analysis))
        finalization_censor = analysis["reason"]
    passed = [r for r in all_rows if r["status"] == "passed"]
    if time.perf_counter() > deadline and finalization_censor is None:
        finalization_censor = "Primary deadline reached during metadata or analysis finalization"
    summary = {"paths": len(paths), "path_status": dict(Counter(p["status"] for p in paths)),
               "floors_recorded": len(all_rows), "passed_floors": len(passed),
               "native_failure_floors": sum(r.get("failure_kind") == "native" for r in all_rows),
               "uniform_decoder_failure_floors": sum(r.get("failure_kind") == "uniform_decoder" for r in all_rows),
               "constraint_cells": sum(r.get("constraint_cells", 0) for r in all_rows),
               "direct_patch_checks": sum(r.get("direct_patch_checks", 0) for r in all_rows),
               "stage_seconds": {k: sum(r.get(k, 0) for r in all_rows) for k in
                                 ("build_seconds", "verification_seconds", "metric_seconds", "export_seconds")},
               "archive_bytes": manifest["archive_size"], "archive_members": len(archive.members),
               "wall_seconds": time.perf_counter()-started, "peak_rss_bytes": old.resident(),
               "finalization_censor": finalization_censor}
    (output / "summary.json").write_bytes(old.canonical(summary))
    print(json.dumps(summary), flush=True)
    comparison = benchmark(output)
    print(json.dumps({"benchmark": comparison["status"], "medians": comparison.get("medians")}), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--implementation-commit")
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps(self_test()))
    else:
        if args.output is None or not args.implementation_commit:
            parser.error("--output and --implementation-commit are required")
        execute(args.output, args.implementation_commit)


if __name__ == "__main__":
    main()
