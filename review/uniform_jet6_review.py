"""Independent review checks; run only after the author's timing process ends.

Archive/oracle/statistical checks use no experimental implementation. The final
bounded cache unit control imports the production cache solely as its subject.
"""
from pathlib import Path
import base64
from collections import Counter
import hashlib
import itertools
import json
import sys
import tarfile
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "experiments/uniform_jet6_cache_20260914/run"
OLD = ROOT / "experiments/on_beam_256_4d_20260914/run"
FEATURES = ("key_fraction", "forced_flip_fraction", "event_flip_fraction",
            "source_degree_fraction", "source_term_fraction", "affine_phase_fraction",
            "source_rank_fraction")
SOURCE_FEATURES = ("event_flip_fraction", "source_degree_fraction", "source_term_fraction", "image_fraction")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def unpack(value, count):
    raw = base64.b64decode(value, validate=True)
    assert len(raw) == (count + 7) // 8
    bits = np.unpackbits(np.frombuffer(raw, np.uint8), bitorder="big")
    assert not bits[count:].any()
    return bits[:count]


def anf(truth):
    coefficients = truth.copy()
    stride = 1
    while stride < truth.shape[1]:
        blocks = coefficients.reshape(len(coefficients), -1, 2 * stride)
        blocks[:, :, stride:] ^= blocks[:, :, :stride]
        stride *= 2
    weights = np.array([i.bit_count() for i in range(truth.shape[1])])
    return (coefficients * weights).max(axis=1), coefficients.sum(axis=1)


def rank(truth):
    matrix = truth.copy()
    pivot = 0
    for column in range(matrix.shape[1]):
        candidates = np.flatnonzero(matrix[pivot:, column])
        if not len(candidates):
            continue
        found = pivot + int(candidates[0])
        matrix[[pivot, found]] = matrix[[found, pivot]]
        affected = matrix[:, column].astype(bool)
        affected[:pivot+1] = False
        matrix[affected] ^= matrix[pivot]
        pivot += 1
        if pivot == len(matrix):
            break
    return pivot


def source_step(grid, rule):
    width = grid.shape[-1]
    return np.array([[(rule >> (4*int(row[(i-1) % width]) + 2*int(row[i]) + int(row[(i+1) % width]))) & 1
                      for i in range(width)] for row in grid], dtype=np.uint8)


def independent_fields(x, y, z):
    plus = np.concatenate((x[..., 1:], x[..., :1]), axis=-1)
    minus = np.concatenate((x[..., -1:], x[..., :-1]), axis=-1)
    if x.ndim > 2:
        plus = np.concatenate((plus[:, 1:], plus[:, :1]), axis=1)
        minus = np.concatenate((minus[:, 1:], minus[:, :1]), axis=1)
    return np.stack((x ^ plus, x ^ minus, x ^ y, x ^ z,
                     x * (1-y), x * y), axis=1)


def reference(width, rule):
    words = np.array(list(itertools.product((0, 1), repeat=width)), dtype=np.uint8)
    states = [words]
    for _ in range(8):
        states.append(source_step(states[-1], rule))
    levels = {1: states}
    for dimension in (2, 3, 4):
        states = [independent_fields(a, b, c) for a, b, c in zip(states, states[1:], states[2:])]
        levels[dimension] = states
    return levels


def packed_patches(grid, coordinates, radius):
    """Independent physical bit gathering, with no production DAG or IDs."""
    size = int(np.prod([2*r + 1 for r in radius]))
    output = np.zeros((len(coordinates), (size+7)//8), dtype=np.uint8)
    for bit, offsets in enumerate(itertools.product(*(range(-r, r+1) for r in radius))):
        address = (coordinates[:, 0],) + tuple((coordinates[:, i+1] + offset) % grid.shape[i+1]
                                               for i, offset in enumerate(offsets))
        output[:, bit//8] |= grid[address] << (7-bit % 8)
    return output


def literal_predictions(x, y):
    predictions = []
    y = np.asarray(y)
    for held in range(len(y)):
        mask = np.arange(len(y)) != held
        train, target = x[mask], x[held]
        mean, scale = train.mean(axis=0), train.std(axis=0)
        keep = np.ptp(train, axis=0) > 0
        train = (train[:, keep] - mean[keep]) / scale[keep]
        target = (target[keep] - mean[keep]) / scale[keep]
        distances = [np.sum((target-train[y[mask] == c].mean(axis=0))**2) for c in (1, 2, 3, 4)]
        predictions.append(int(np.argmin(distances)) + 1)
    return predictions


def reflected(rule):
    return sum(((rule >> (((i & 1) << 2) | (i & 2) | (i >> 2))) & 1) << i for i in range(8))


def conjugated(rule):
    return sum((1 - ((rule >> (7-i)) & 1)) << i for i in range(8))


def unit_controls():
    sys.path.insert(0, str(ROOT / "scripts"))
    import uniform_jet6_cache as subject
    rng = np.random.default_rng(920260914)
    field_cases = patches = 0
    for dimension in (1, 2, 3):
        shape = (2,) + (2,)*(dimension-1) + (4,)
        for _ in range(5):
            x, y, z, w = [rng.integers(0, 2, shape, dtype=np.uint8) for _ in range(4)]
            actual = subject.fields(x, y, z)
            assert np.array_equal(actual, independent_fields(x, y, z))
            assert np.array_equal(subject.flip_fields(x, y, z, w), actual ^ independent_fields(y, z, w))
            assert np.array_equal(actual[:, 4] ^ actual[:, 5], x)
            field_cases += 1
    for dimension in (1, 2, 3, 4):
        grid = rng.integers(0, 2, (2,) + (2,)*(dimension-1) + (3,), dtype=np.uint8)
        radius = (3,)*(dimension-1) + (2,)
        keyer = subject.PhysicalKeys(radius)
        keys = keyer.keys(grid)
        coordinates = np.array(list(np.ndindex(grid.shape)))
        wanted = packed_patches(grid, coordinates, radius)
        for event, packed in zip(coordinates, wanted):
            actual = np.packbits(keyer.expand(int(keys[tuple(event)])), bitorder="big")
            assert np.array_equal(actual, packed)
            patches += 1
    original = np.array(list(itertools.product((0, 1), repeat=6)), dtype=np.uint8).reshape(64, 2, 3)
    grid = original.copy()
    keyer = subject.PhysicalKeys((3, 2))
    keys = keyer.keys(grid)
    wanted = np.roll(grid, 1, axis=-1) ^ np.roll(grid, 1, axis=1)
    derivative = np.zeros(int(keys.max()) + 1, dtype=np.uint8)
    targets = grid ^ wanted
    for root in range(len(derivative)):
        values = np.unique(targets[keys == root])
        assert len(values) == 1
        derivative[root] = values[0]
    law = subject.NativeLaw(keyer, derivative, np.zeros_like(derivative))
    beam = subject.Beam(grid, law, keys)
    derivative ^= 1
    grid ^= 1
    keys[:] = 0
    assert np.array_equal(beam.state(0), original)
    wanted = original
    for tick in range(1, 6):
        wanted = np.roll(wanted, 1, axis=-1) ^ np.roll(wanted, 1, axis=1)
        assert np.array_equal(beam.state(tick), wanted)
        assert np.array_equal(beam.keys(tick), keyer.keys(wanted))
    assert beam.native_evaluations == 1
    identity = subject.Beam(original, subject.NativeLaw(keyer, np.zeros_like(derivative), np.zeros_like(derivative)))
    assert np.array_equal(identity.state(5), original)
    try:
        beam.grid[0, 0, 0] ^= 1
        raise AssertionError("Published cache grid is writable")
    except ValueError:
        pass
    return {"independent_field_cases": field_cases, "independent_physical_patches": patches,
            "native_cache_ticks_checked": 5, "law_scope_and_caller_mutation": True}


def main():
    started = time.perf_counter()
    execution = json.loads((RUN / "execution.json").read_text())
    summary = json.loads((RUN / "summary.json").read_text())
    benchmark = json.loads((RUN / "benchmark.json").read_text())
    assert benchmark["status"] != "running", "Wait for the author's timing process"
    for name, value in execution["source_hashes"].items():
        assert sha((ROOT / name).read_bytes()) == value, name
    manifest = json.loads((RUN / "archive_manifest.json").read_text())
    path = RUN / manifest["archive_path"]
    assert path.stat().st_size == manifest["archive_size"]
    with path.open("rb") as stream:
        assert hashlib.file_digest(stream, "sha256").hexdigest() == manifest["archive_sha256"]
    rows = [json.loads(line) for line in (RUN / "floors.jsonl").read_text().splitlines()]
    good = [row for row in rows if row["status"] == "passed"]
    indexed = {row["partial_rule"]["path"]: row for row in good}
    assert len(indexed) == len(manifest["members"]) == summary["archive_members"]
    references = {}
    fresh_updates = fresh_decoder_cells = bounded_floors = roots = source_baselines = truth_bits = 0
    with tarfile.open(path, "r|gz") as archive:
        for expected in manifest["members"]:
            member = archive.next()
            assert member is not None and member.isfile() and member.name == expected["path"]
            data = archive.extractfile(member).read()
            assert len(data) == expected["size"] == member.size and sha(data) == expected["sha256"]
            record, row = json.loads(data), indexed[member.name]
            assert data == json.dumps(record, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
            width, rule, dimension = (row[k] for k in ("width", "rule", "dimension"))
            assert member.name == f"w{width}/rule{rule:03d}/d{dimension}.json"
            for name in ("width", "rule", "dimension", "mode"):
                assert record[name] == row[name]
            assert record["mode"] == "jet6" and record["recipe"] == {"family": "uniform-six-field"}
            assert record["format"] == "grid-referenced-physical-partial-rule-v1"
            shape = [2**width] + [6]*(dimension-1) + [width]
            radius = [3]*(dimension-1) + [2]
            assert record["grid_shape"] == shape and record["radii_array_order"] == radius
            if (width, rule) not in references:
                references = {(width, rule): reference(width, rule)}
            levels = references[width, rule]
            grid = unpack(record["grid_bits_big"], int(np.prod(shape))).reshape(shape)
            assert np.array_equal(grid, levels[dimension][0])
            assert np.array_equal(grid[:, 4] ^ grid[:, 5], levels[dimension-1][0])
            count = record["forced_root_count"]
            assert count == row["native"]["forced_keys"]
            raw = base64.b64decode(record["representative_flat_indices_u32le"], validate=True)
            assert len(raw) == count * 4
            representatives = np.frombuffer(raw, dtype="<u4")
            assert len(np.unique(representatives)) == count and representatives.max() < grid.size
            derivative = unpack(record["forced_derivative_bits_big"], count)
            decoder = unpack(record["forced_decoder_bits_big"], count)
            assert record["native_table_sha256"] == row["native_sha256"] == sha(derivative.tobytes() + decoder.tobytes())
            assert record["unforced_derivative"] == record["unforced_decoder"] == 0
            delta = grid ^ levels[dimension][1]
            assert np.array_equal(derivative, delta.ravel()[representatives])
            parent = np.broadcast_to(levels[dimension-1][0][:, None], grid.shape)
            assert np.array_equal(decoder, parent.ravel()[representatives])
            phase_shape = [6**(dimension-1), 2**width]
            assert record["source_phase_shape"] == phase_shape
            truth = unpack(record["source_phase_derivative_bits_big"], int(np.prod(phase_shape))).reshape(phase_shape)
            assert np.array_equal(truth, delta[..., 0].reshape(2**width, -1).T)
            degrees, terms = anf(truth)
            truth_rank = rank(truth)
            expected_features = {"key_fraction": count / (2**width * 6**(dimension-1)),
                                 "forced_flip_fraction": float(derivative.mean()), "event_flip_fraction": float(truth.mean()),
                                 "source_degree_fraction": float(degrees.mean()) / width,
                                 "source_term_fraction": float(terms.mean()) / 2**width,
                                 "affine_phase_fraction": float((degrees <= 1).mean()),
                                 "source_rank_fraction": truth_rank / min(phase_shape)}
            assert expected_features == row["features"]
            assert row["phase_analysis"]["phase_degrees"] == degrees.tolist()
            assert row["phase_analysis"]["phase_terms"] == terms.tolist()
            assert row["phase_analysis"]["source_rank"] == truth_rank
            roots += count
            truth_bits += truth.size
            if width == 7 and rule in (30, 110):
                positions = np.array(np.unravel_index(representatives, grid.shape)).T
                physical = packed_patches(grid, positions, radius)
                laws = {patch.tobytes(): (int(a), int(b)) for patch, a, b in zip(physical, derivative, decoder)}
                assert len(laws) == count, "Duplicate physical representative patches"
                selected = [0, 1, 42, 85, 127]
                actual = grid[selected].copy()
                positions = np.array(list(np.ndindex(actual.shape)))
                for tick in (0, 1):
                    patches = packed_patches(actual, positions, radius)
                    outputs = np.array([laws.get(p.tobytes(), (0, 0)) for p in patches], dtype=np.uint8)
                    recovered = outputs[:, 1].reshape(actual.shape)
                    wanted = np.broadcast_to(levels[dimension-1][tick][selected, None], actual.shape)
                    assert np.array_equal(recovered, wanted)
                    fresh_decoder_cells += actual.size
                    actual ^= outputs[:, 0].reshape(actual.shape)
                    assert np.array_equal(actual, levels[dimension][tick+1][selected])
                    fresh_updates += actual.size
                bounded_floors += 1
        assert archive.next() is None
    paths = [json.loads(line) for line in (RUN / "paths.jsonl").read_text().splitlines()]
    for entry in paths:
        if "source_features" not in entry:
            continue
        width, rule = entry["width"], entry["rule"]
        words = np.array(list(itertools.product((0, 1), repeat=width)), dtype=np.uint8)
        successor = source_step(words, rule)
        delta = words ^ successor
        degrees, terms = anf(delta[:, 0][None])
        baseline = {"event_flip_fraction": float(delta.mean()), "source_degree_fraction": float(degrees[0]) / width,
                    "source_term_fraction": float(terms[0]) / 2**width,
                    "image_fraction": len({r.tobytes() for r in successor}) / len(words)}
        assert baseline == entry["source_features"]
        source_baselines += 1
    labels = json.loads((ROOT / "experiments/on_beam_256_4d_20260914/labels.json").read_text())
    orbits = {}
    for rule in range(256):
        members = sorted({rule, reflected(rule), conjugated(rule), reflected(conjugated(rule))})
        orbits[min(members)] = members
    classes = {int(rule): int(c) for c, rules in labels["representatives"].items() for rule in rules}
    analysis = json.loads((RUN / "analysis.json").read_text())
    old_rows = [json.loads(line) for line in (OLD / "floors.jsonl").read_text().splitlines()]
    old_paths = [json.loads(line) for line in (OLD / "paths.jsonl").read_text().splitlines()]
    models = 0
    for sensitivity in (False, True):
        group = analysis["sensitivity" if sensitivity else "models"]
        for width in (7, 8):
            for name, saved_rows, saved_paths in (("jet6", good, paths), ("old4", old_rows, old_paths)):
                result = group[str(width)][name]
                if result["status"] != "completed":
                    continue
                cohort = result["orbits"]
                target = [classes[o] for o in cohort]
                floors = {(r["rule"], r["dimension"]): r for r in saved_rows if r["width"] == width}
                pathmap = {r["rule"]: r for r in saved_paths if r["width"] == width}
                source = np.array([np.mean([[pathmap[r]["source_features"][f] for f in SOURCE_FEATURES]
                                            for r in orbits[o]], axis=0) for o in cohort])
                lift = {d: np.array([np.mean([[floors[r, d]["features"][f] for f in FEATURES]
                                              for r in orbits[o]], axis=0) for o in cohort]) for d in (2, 3, 4)}
                all_lifts = np.concatenate([lift[d] for d in (2, 3, 4)], axis=1)
                views = {"source": source, **{f"lift{d}": lift[d] for d in (2, 3, 4)},
                         "lift_all": all_lifts, "source_lift_all": np.concatenate((source, all_lifts), axis=1)}
                for name, values in views.items():
                    prediction = literal_predictions(values, target)
                    assert prediction == result["views"][name]["predicted"]
                    models += 1
    controls = unit_controls()
    report = {"reviewer": "Codex (OpenAI), independent reviewing agent /root/independent_pilot_review",
              "status": "passed", "implementation_commit": execution["implementation_commit"],
              "scope": "Full archive bytes/arrays, independent finite-family oracle and representative outputs/metrics; bounded physical native replay; no complete independent forced-key census",
              "archive_sha256": manifest["archive_sha256"], "archive_bytes": manifest["archive_size"],
              "archive_members": len(good), "representative_outputs_checked": roots,
              "source_truth_bits_checked": truth_bits, "source_baselines_checked": source_baselines,
              "literal_model_fits": models, "bounded_native_floors": bounded_floors,
              "fresh_native_cell_updates": fresh_updates, "fresh_uniform_decoder_cells": fresh_decoder_cells,
              "cache_controls": controls, "review_script_sha256": sha(Path(__file__).read_bytes()),
              "wall_seconds": time.perf_counter()-started}
    Path(__file__).with_suffix(".json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
