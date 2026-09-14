"""Frozen all-256 finite on-beam census. Scientific evaluation is off CI only."""
from __future__ import annotations

import argparse
import base64
import csv
from dataclasses import dataclass
import gzip
import hashlib
import io
import itertools
import json
from pathlib import Path
import platform
import resource
import sys
import tarfile
import tempfile
import time

import numpy as np

import sequential_lift_6d_pilot as core
import on_beam_rule_analysis as analysis

ROOT = Path(__file__).resolve().parent.parent
PROTOCOL = "docs/research/protocols/on-beam-256-4d-classes-20260914.md"
RECIPES = "results/binary_lift_20260914/rule_coverage.csv"
LABELS = "experiments/on_beam_256_4d_20260914/labels.json"
BASELINE = "a2dfba2801ac6f53d7cea4306927c5b6f246f140"
SOURCES = ("scripts/on_beam_256_4d.py", "scripts/on_beam_rule_analysis.py",
           "scripts/sequential_lift_6d_pilot.py", PROTOCOL, RECIPES, LABELS)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def resident():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024


class Budget:
    def __init__(self, deadline):
        self.deadline = deadline

    def check(self):
        if time.perf_counter() > self.deadline:
            raise TimeoutError("frozen cooperative wall budget")
        if resident() > 4 * 1024**3:
            raise MemoryError("frozen 4 GiB RSS soft ceiling")


@dataclass(frozen=True)
class Recipe:
    mask: str
    sign: int
    q: str
    order: str

    def record(self):
        return {"mask": self.mask, "sign": self.sign, "q": self.q, "order": self.order}


def load_recipes():
    with (ROOT / RECIPES).open() as stream:
        rows = list(csv.DictReader(stream))
    result = {int(r["rule"]): Recipe(r["selected_mask"], int(r["selected_shift"]),
                                    r["selected_Q"], r["selected_order"]) for r in rows}
    assert len(rows) == len(result) == 256 and set(result) == set(range(256))
    assert all(r.order in ("PDMQ", "PDQM") for r in result.values())
    return result


def moved(array, dx, dy):
    answer = np.roll(array, -dx, axis=-1)
    if array.ndim > 2:
        answer = np.roll(answer, -dy, axis=1)
    return answer


def encode(x, y, recipe):
    delta = x ^ y
    p = x ^ moved(x, recipe.sign, 1)
    if recipe.mask == "birth":
        mask = (1 - x) & delta
    elif recipe.mask == "death":
        mask = x & delta
    elif recipe.mask == "stay_one":
        mask = x & (1 - delta)
    elif recipe.mask == "stay_zero":
        mask = (1 - x) & (1 - delta)
    else:
        raise ValueError(recipe.mask)
    parts = recipe.q.split(":")
    a, b = int(parts[1]), int(parts[2])
    left, right = moved(x, a, a * recipe.sign), moved(x, b, b * recipe.sign)
    if parts[0] == "pair":
        q = left & right
    elif parts[3] == "not-left-and-right":
        q = (1 - left) & right
    elif parts[3] == "left-and-not-right":
        q = left & (1 - right)
    else:
        raise ValueError(recipe.q)
    fields = {"P": p, "D": delta, "M": mask, "Q": q}
    return np.stack([fields[name] for name in recipe.order], axis=1)


def reference_encode(x, y, recipe):
    """Independent array indexing/Boolean implementation for complete verification."""
    def offset(dx, dy):
        out = np.take(x, (np.arange(x.shape[-1]) + dx) % x.shape[-1], axis=-1)
        if x.ndim > 2:
            out = np.take(out, (np.arange(x.shape[1]) + dy) % x.shape[1], axis=1)
        return out.astype(bool)
    before, after = x.astype(bool), y.astype(bool)
    delta = before != after
    mask = {"birth": (~before) & after, "death": before & (~after),
            "stay_one": before & after, "stay_zero": (~before) & (~after)}[recipe.mask]
    parts = recipe.q.split(":")
    a, b = map(int, parts[1:3])
    left, right = offset(a, a * recipe.sign), offset(b, b * recipe.sign)
    if parts[0] == "pair":
        q = np.logical_and(left, right)
    elif parts[3] == "not-left-and-right":
        q = np.logical_and(np.logical_not(left), right)
    else:
        q = np.logical_and(left, np.logical_not(right))
    fields = {"P": before != offset(recipe.sign, 1), "D": delta, "M": mask, "Q": q}
    return np.stack([fields[c] for c in recipe.order], axis=1).astype(np.uint8)


def scalar_encode(x, y, recipe):
    out = np.empty((x.shape[0], 4, *x.shape[1:]), dtype=np.uint8)
    for index in np.ndindex(x.shape):
        def bit(dx, dy):
            at = list(index)
            at[-1] = (at[-1] + dx) % x.shape[-1]
            if x.ndim > 2:
                at[1] = (at[1] + dy) % x.shape[1]
            return int(x[tuple(at)])
        before, after = int(x[index]), int(y[index])
        delta = before ^ after
        mask = {"birth": int(before == 0 and after == 1),
                "death": int(before == 1 and after == 0),
                "stay_one": int(before == 1 and after == 1),
                "stay_zero": int(before == 0 and after == 0)}[recipe.mask]
        parts = recipe.q.split(":")
        a, b = map(int, parts[1:3])
        left, right = bit(a, a * recipe.sign), bit(b, b * recipe.sign)
        q = left & right if parts[0] == "pair" else ((1 - left) & right if parts[3] == "not-left-and-right" else left & (1 - right))
        values = {"P": before ^ bit(recipe.sign, 1), "D": delta, "M": mask, "Q": q}
        for phase, name in enumerate(recipe.order):
            out[(index[0], phase, *index[1:])] = values[name]
    return out


def reference_family(rule, width, dimension, recipe):
    states = [core.all_words(width)]
    for _ in range(dimension + 1):
        states.append(core.reference_source_step(states[-1], rule))
    for _ in range(dimension - 1):
        states = [reference_encode(a, b, recipe) for a, b in zip(states, states[1:])]
    assert len(states) == 3
    return states


def mobius(truth):
    coefficients = truth.copy()
    width = truth.shape[1].bit_length() - 1
    indices = np.arange(truth.shape[1])
    for bit in range(width):
        high = indices[(indices & (1 << bit)) != 0]
        coefficients[:, high] ^= coefficients[:, high ^ (1 << bit)]
    return coefficients


def binary_rank(matrix):
    basis = {}
    for packed in np.packbits(matrix, axis=1, bitorder="little"):
        row = int.from_bytes(packed.tobytes(), "little")
        while row:
            lead = row.bit_length() - 1
            if lead in basis:
                row ^= basis[lead]
            else:
                basis[lead] = row
                break
    return len(basis)


def truth_features(delta):
    count = delta.shape[0]
    width = count.bit_length() - 1
    truth = delta[..., 0].reshape(count, -1).T.copy()
    coefficients = mobius(truth)
    weights = np.array([i.bit_count() for i in range(count)], dtype=np.uint8)
    degrees = np.where(coefficients, weights[None, :], 0).max(axis=1)
    terms = coefficients.sum(axis=1)
    rank = binary_rank(truth)
    record = {"source_degree_fraction": float(degrees.mean() / width),
              "source_term_fraction": float(terms.mean() / count),
              "affine_phase_fraction": float(np.mean(degrees <= 1)),
              "source_rank_fraction": rank / min(truth.shape),
              "event_flip_fraction": float(delta.mean())}
    detail = {"phase_degrees": degrees.tolist(), "phase_terms": terms.tolist(),
              "source_rank": rank, "truth_shape": list(truth.shape)}
    return record, detail, truth


def pack(array, dtype=None):
    value = np.asarray(array, dtype=dtype)
    return base64.b64encode(value.tobytes()).decode()


def partial_rule(law, truth, width, rule, dimension, recipe):
    nodes = [np.asarray(level, dtype="<u4").reshape(-1, 5) for level in law.keyer.nodes]
    differences = [np.diff(level.astype(np.int64), axis=0, prepend=np.zeros((1, 5), dtype=np.int64))
                   for level in nodes]
    assert all(np.max(np.abs(level), initial=0) < 2**31 for level in differences)
    return {"format": "ordered-five-tuple-physical-neighborhood-v1", "width": width,
            "rule": rule, "dimension": dimension, "recipe": recipe.record(), "radius": 2,
            "nodes_delta_i32le_columns": [pack(level.T.copy(), "<i4") for level in differences],
            "node_codec": "five column-major int32 little-endian difference streams; cumulative sum along node index from zero",
            "node_counts": [len(level) for level in nodes],
            "forced_root_count": len(law.derivative),
            "forced_derivative_bits_big": pack(np.packbits(law.derivative, bitorder="big")),
            "forced_decoder_bits_big": pack(np.packbits(law.decoder, bitorder="big")),
            "source_phase_derivative_bits_big": pack(np.packbits(truth, axis=1, bitorder="big")),
            "source_phase_shape": list(truth.shape),
            "unforced_derivative": 0, "unforced_decoder": 0}


def restore_partial(record):
    nodes = [np.frombuffer(base64.b64decode(v), dtype="<i4").reshape(5, n).T.cumsum(axis=0, dtype=np.int64).astype(np.uint32)
             for v, n in zip(record["nodes_delta_i32le_columns"], record["node_counts"])]
    k = record["forced_root_count"]
    derivative = np.unpackbits(np.frombuffer(base64.b64decode(record["forced_derivative_bits_big"]), dtype=np.uint8), bitorder="big")[:k]
    decoder = np.unpackbits(np.frombuffer(base64.b64decode(record["forced_decoder_bits_big"]), dtype=np.uint8), bitorder="big")[:k]
    return nodes, derivative, decoder


def expand_saved(nodes, identifier, depth):
    if depth < 0:
        return tuple((identifier >> bit) & 1 for bit in range(4, -1, -1))
    return tuple(bit for child in nodes[depth][identifier]
                 for bit in expand_saved(nodes, int(child), depth - 1))


class Archive:
    def __init__(self, path):
        self.path, self.members = path, []
        self.file = path.open("wb")
        self.gzip = gzip.GzipFile(filename="", mode="wb", fileobj=self.file, mtime=0, compresslevel=6)
        self.tar = tarfile.open(fileobj=self.gzip, mode="w|", format=tarfile.USTAR_FORMAT)

    def add(self, name, record):
        data = canonical(record)
        info = tarfile.TarInfo(name)
        info.size, info.mtime, info.mode = len(data), 0, 0o644
        self.tar.addfile(info, io.BytesIO(data))
        member = {"path": name, "size": len(data), "sha256": sha(data)}
        self.members.append(member)
        return member

    def close(self):
        self.tar.close()
        self.gzip.close()
        self.file.close()


def conflict(gate, grid, targets):
    if gate["witness"] is None:
        return None
    events = [tuple(int(v) for v in np.unravel_index(e, grid.shape))
              for e in gate["witness"]["events"]]
    patches = [core.direct_patch(grid, event) for event in events]
    assert patches[0] == patches[1]
    expected = np.broadcast_to(targets, grid.shape)
    assert [int(expected[event]) for event in events] == [0, 1]
    return {"events": [list(e) for e in events], "targets": [0, 1],
            "source_words": [core.all_words(grid.shape[-1])[e[0]].tolist() for e in events],
            "patch_bits": len(patches[0]),
            "patch_hex": np.packbits(patches[0], bitorder="big").tobytes().hex(),
            "directly_verified": True}


def run_floor(rule, width, dimension, recipe, parent, family, chain, budget, archive):
    start = time.perf_counter()
    budget.check()
    old = [law.table_digest for law in chain]
    y = parent.step(family, budget)
    z = parent.step(y, budget)
    child, target = encode(family, y, recipe), encode(y, z, recipe)
    keyer = core.PatchKeys(dimension)
    keys = keyer.keys(child, budget)
    derivative, native = core.table_from_constraints(keys, child ^ target)
    decoder, recovery = core.table_from_constraints(keys, family[:, None])
    row = {"rule": rule, "width": width, "dimension": dimension, "recipe": recipe.record(),
           "source_states": 1 << width, "phase_count": 4 ** (dimension - 1),
           "constraint_cells": int(child.size), "native": native, "parent_recovery": recovery,
           "build_seconds": time.perf_counter() - start}
    for gate, targets in ((native, child ^ target), (recovery, family[:, None])):
        gate["witness"] = conflict(gate, child, targets)
    if not native["passes"] or not recovery["passes"]:
        row.update(status="failed", wall_seconds=time.perf_counter() - start)
        return row, None, None
    law = core.NativeLaw(keyer, derivative, decoder)
    verification_start = time.perf_counter()
    expected = reference_family(rule, width, dimension, recipe)
    assert np.array_equal(child, expected[0]), (rule, width, dimension, "encoding")
    first = law.step(child, budget)
    second = law.step(first, budget)
    assert np.array_equal(first, expected[1]) and np.array_equal(second, expected[2]), (rule, width, dimension, "native")
    decoded = core.lookup(decoder, keys)
    assert np.array_equal(decoded, np.broadcast_to(family[:, None], decoded.shape))
    recovered = decoded[:, 0]
    for ancestor in reversed(chain):
        recovered = ancestor.recover(recovered, budget)
    assert np.array_equal(recovered, core.all_words(width)), (rule, width, dimension, "source recovery")
    for ancestor, digest in zip(chain, old):
        ancestor.assert_immutable()
        assert digest == ancestor.table_digest
    law.assert_immutable()
    row["verification_seconds"] = time.perf_counter() - verification_start
    features, detail, truth = truth_features(child ^ target)
    roots = np.unique(keys)
    assert np.array_equal(roots, np.arange(len(derivative))), "all exported roots are forced"
    features["key_fraction"] = len(roots) / ((1 << width) * 4 ** (dimension - 1))
    features["forced_flip_fraction"] = float(derivative[roots].mean())
    exported = partial_rule(law, truth, width, rule, dimension, recipe)
    nodes, saved_derivative, saved_decoder = restore_partial(exported)
    assert np.array_equal(saved_derivative, derivative) and np.array_equal(saved_decoder, decoder)
    direct_checks = 0
    for source in (0, 1, 42, 85, (1 << width) - 1):
        for phase in (0, 1, 3):
            event = (source,) + (phase,) * (dimension - 1) + (0,)
            identifier = int(keys[event])
            direct = core.direct_patch(child, event)
            assert direct == keyer.expand(identifier) == expand_saved(nodes, identifier, dimension - 2)
            assert int(saved_derivative[identifier]) == int((child ^ target)[event])
            direct_checks += 1
    budget.check()
    export_start = time.perf_counter()
    member = archive.add(f"w{width}/rule{rule:03d}/d{dimension}.json", exported)
    row.update(status="passed", features=features, phase_analysis=detail,
               direct_patch_checks=direct_checks, node_counts=keyer.stats(),
               native_replay=True, parent_replay=True, source_recovery=True, parents_immutable=True,
               native_sha256=law.table_digest, partial_rule=member,
               export_seconds=time.perf_counter() - export_start,
               wall_seconds=time.perf_counter() - start, peak_rss_bytes=resident())
    return row, law, child


def self_test():
    rng = np.random.default_rng(947)
    checks = 0
    for shape in ((2, 9), (2, 4, 9), (2, 4, 4, 9)):
        x, y = rng.integers(0, 2, size=(2, *shape), dtype=np.uint8)
        for mask, sign, q, order in itertools.product(*analysis.RECIPE_FIELDS.values()):
            recipe = Recipe(mask, sign, q, order)
            actual = encode(x, y, recipe)
            assert np.array_equal(actual, scalar_encode(x, y, recipe))
            assert np.array_equal(actual, reference_encode(x, y, recipe))
            checks += 1
    states = core.all_words(7)
    for rule in range(256):
        current = core.ECALaw(rule).step(states)
        assert np.array_equal(core.ECALaw(analysis.reflection(rule)).step(states[:, ::-1]), current[:, ::-1])
        assert np.array_equal(core.ECALaw(analysis.conjugate(rule)).step(1 - states), 1 - current)
    for width in range(1, 6):
        coeff = rng.integers(0, 2, size=(5, 1 << width), dtype=np.uint8)
        truth = np.array([[sum(int(row[m]) for m in range(1 << width) if (m & assignment) == m) % 2
                           for assignment in range(1 << width)] for row in coeff], dtype=np.uint8)
        assert np.array_equal(mobius(truth), coeff)
    for shape in ((3, 9), (12, 7), (8, 8)):
        matrix = rng.integers(0, 2, size=shape, dtype=np.uint8)
        independent = matrix.copy()
        rank = 0
        for column in range(shape[1]):
            pivots = np.flatnonzero(independent[rank:, column])
            if not len(pivots):
                continue
            pivot = rank + int(pivots[0])
            independent[[rank, pivot]] = independent[[pivot, rank]]
            for row in range(rank + 1, shape[0]):
                if independent[row, column]:
                    independent[row] ^= independent[rank]
            rank += 1
            if rank == shape[0]:
                break
        assert binary_rank(matrix) == rank
    labels = json.loads((ROOT / LABELS).read_text())
    analysis.class_map(labels)
    core.self_test()
    recipes = load_recipes()
    expected = {90: [507, 2025, 8097], 54: [475, 2025, 8097],
                110: [457, 2025, 8097], 157: [464, 2048, 8192]}
    with tempfile.TemporaryDirectory() as temporary:
        archive = Archive(Path(temporary) / "controls.tar.gz")
        try:
            for rule, counts in expected.items():
                parent, family, chain = core.ECALaw(rule), states, []
                for dimension, count in zip((2, 3, 4), counts):
                    row, law, child = run_floor(rule, 7, dimension, recipes[rule], parent,
                                               family, chain, Budget(time.perf_counter() + 60), archive)
                    assert row["status"] == "passed" and row["native"]["forced_keys"] == count
                    parent, family = law, child
                    chain.append(law)
        finally:
            archive.close()
        control_archive_bytes = archive.path.stat().st_size
    return {"field_constructor_controls": checks, "symmetry_rules": 256,
            "mobius_widths": 5, "rank_matrices": 3, "prior_pilot_floor_controls": 12,
            "control_archive_bytes": control_archive_bytes, "status": "passed"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--implementation-commit")
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps(self_test(), sort_keys=True))
        return
    if not args.output or not args.implementation_commit:
        parser.error("--output and --implementation-commit are required")
    if args.output.exists() and any(args.output.iterdir()):
        raise ValueError("Output directory must be empty; no outcome-dependent resume")
    args.output.mkdir(parents=True, exist_ok=True)
    output = args.output
    start = time.perf_counter()
    global_budget = Budget(start + 900)
    recipes = load_recipes()
    labels = json.loads((ROOT / LABELS).read_text())
    classes, orbits = analysis.class_map(labels)
    execution = {"baseline_commit": BASELINE, "implementation_commit": args.implementation_commit,
                 "python": sys.version, "numpy": np.__version__, "platform": platform.platform(),
                 "utc_start": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                 "widths": [7, 8], "rules": list(range(256)), "dimensions": [2, 3, 4],
                 "recipes": {r: v.record() for r, v in recipes.items()},
                 "source_hashes": {p: sha((ROOT / p).read_bytes()) for p in SOURCES}}
    (output / "execution.json").write_bytes(canonical(execution) + b"\n")
    archive = Archive(output / "partial_rules.tar.gz")
    rows, paths = [], []
    try:
        with (output / "floors.jsonl").open("w") as floors_log, (output / "paths.jsonl").open("w") as paths_log:
            for width in (7, 8):
                for rule in range(256):
                    path_start = time.perf_counter()
                    path = {"width": width, "rule": rule, "orbit": min(analysis.orbit(rule)),
                            "class": classes[min(analysis.orbit(rule))], "status": "passed", "last_floor": 1}
                    budget = Budget(min(global_budget.deadline, path_start + 60))
                    try:
                        budget.check()
                        family = core.all_words(width)
                        parent, chain = core.ECALaw(rule), []
                        successor = parent.step(family)
                        source, _, _ = truth_features(family ^ successor)
                        source["image_fraction"] = len(np.unique(successor, axis=0)) / len(family)
                        path["source_features"] = {f: source[f] for f in analysis.SOURCE_FEATURES}
                        for dimension in (2, 3, 4):
                            row, law, child = run_floor(rule, width, dimension, recipes[rule], parent,
                                                       family, chain, budget, archive)
                            rows.append(row)
                            floors_log.write(canonical(row).decode() + "\n")
                            floors_log.flush()
                            if row["status"] != "passed":
                                path["status"] = "failed"
                                path["failed_floor"] = dimension
                                break
                            path["last_floor"] = dimension
                            parent, family = law, child
                            chain.append(law)
                    except (TimeoutError, MemoryError) as error:
                        path.update(status="censored", reason=str(error))
                    path.update(wall_seconds=time.perf_counter() - path_start, peak_rss_bytes=resident())
                    paths.append(path)
                    paths_log.write(canonical(path).decode() + "\n")
                    paths_log.flush()
                    if rule % 32 == 31 or path["status"] != "passed":
                        print(json.dumps({"width": width, "through_rule": rule,
                              "passed_paths": sum(p["status"] == "passed" for p in paths),
                              "failed_paths": sum(p["status"] == "failed" for p in paths),
                              "censored_paths": sum(p["status"] == "censored" for p in paths),
                              "seconds": round(time.perf_counter() - start, 3)}), flush=True)
    finally:
        archive.close()
    archive_bytes = (output / "partial_rules.tar.gz").read_bytes()
    part_dir = output / "archive_parts"
    part_dir.mkdir()
    part_records = []
    for i, offset in enumerate(range(0, len(archive_bytes), 524288)):
        global_budget.check()
        data = base64.b64encode(archive_bytes[offset:offset + 524288]) + b"\n"
        name = f"part-{i:04d}.b64"
        (part_dir / name).write_bytes(data)
        part_records.append({"path": "archive_parts/" + name, "size": len(data), "sha256": sha(data)})
    manifest = {"format": "canonical-json-members-in-deterministic-tar-gzip-base64-parts-v1",
                "archive_size": len(archive_bytes), "archive_sha256": sha(archive_bytes),
                "members": archive.members, "parts": part_records}
    (output / "archive_manifest.json").write_bytes(canonical(manifest) + b"\n")
    try:
        global_budget.check()
        associations = analysis.analyze(rows, paths, {r: p.record() for r, p in recipes.items()}, labels, global_budget)
    except (TimeoutError, MemoryError) as error:
        associations = {"status": "censored", "reason": str(error)}
    (output / "analysis.json").write_bytes(canonical(associations) + b"\n")
    summary = {"paths": len(paths), "passed_paths": sum(p["status"] == "passed" for p in paths),
               "failed_paths": sum(p["status"] == "failed" for p in paths),
               "censored_paths": sum(p["status"] == "censored" for p in paths),
               "floors": len(rows), "passed_floors": sum(r["status"] == "passed" for r in rows),
               "native_constraint_cells": sum(r["constraint_cells"] for r in rows),
               "direct_patch_checks": sum(r.get("direct_patch_checks", 0) for r in rows),
               "archive_members": len(archive.members), "archive_bytes": len(archive_bytes),
               "wall_seconds": time.perf_counter() - start, "peak_rss_bytes": resident()}
    (output / "summary.json").write_bytes(canonical(summary) + b"\n")
    print(json.dumps(summary, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
