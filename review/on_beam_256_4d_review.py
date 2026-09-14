"""Independent Gate-2 evidence checker; imports no scientific implementation."""
from pathlib import Path
import base64
import hashlib
import itertools
import json
import re
import tarfile
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "experiments/on_beam_256_4d_20260914/run"
OUT = Path(__file__).with_suffix(".json")
START = time.perf_counter()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def anf(truth):
    coefficients = truth.copy()
    stride = 1
    while stride < truth.shape[1]:
        blocks = coefficients.reshape(len(coefficients), -1, 2 * stride)
        blocks[:, :, stride:] ^= blocks[:, :, :stride]
        stride *= 2
    weight = np.fromiter((x.bit_count() for x in range(truth.shape[1])), int)
    degrees = (coefficients * weight).max(axis=1)
    return degrees, coefficients.sum(axis=1)


def rank(matrix):
    a = matrix.copy()
    n = 0
    for col in range(a.shape[1]):
        pivots = np.flatnonzero(a[n:, col])
        if not len(pivots):
            continue
        pivot = n + int(pivots[0])
        a[[n, pivot]] = a[[pivot, n]]
        for row in range(n + 1, len(a)):
            if a[row, col]:
                a[row] ^= a[n]
        n += 1
        if n == len(a):
            break
    return n


def bitstream(value, count):
    data = base64.b64decode(value, validate=True)
    assert len(data) == (count + 7) // 8
    bits = np.unpackbits(np.frombuffer(data, np.uint8), bitorder="big")
    assert not bits[count:].any()
    return bits[:count]


def source_step(x, rule):
    return np.array([(rule >> (4 * int(x[(i - 1) % len(x)]) + 2 * int(x[i]) + int(x[(i + 1) % len(x)]))) & 1
                     for i in range(len(x))], dtype=np.uint8)


def fields(x, y, recipe):
    output = np.empty((4,) + x.shape, dtype=np.uint8)
    qparts = recipe["q"].split(":")
    a, b = map(int, qparts[1:3])
    sign = recipe["sign"]
    for at in np.ndindex(x.shape):
        def value(dx, dy):
            address = list(at)
            address[-1] = (address[-1] + dx) % x.shape[-1]
            if x.ndim > 1:
                address[0] = (address[0] + dy) % x.shape[0]
            return int(x[tuple(address)])
        before, after = int(x[at]), int(y[at])
        masks = {"birth": int(not before and after), "death": int(before and not after),
                 "stay_one": before & after, "stay_zero": int(not before and not after)}
        left, right = value(a, a * sign), value(b, b * sign)
        if qparts[0] == "pair":
            q = left & right
        elif qparts[3] == "not-left-and-right":
            q = (1 - left) & right
        else:
            q = left & (1 - right)
        parts = {"P": before ^ value(sign, 1), "D": before ^ after,
                 "M": masks[recipe["mask"]], "Q": q}
        for phase, symbol in enumerate(recipe["order"]):
            output[(phase,) + at] = parts[symbol]
    return output


def prepared(word, rule, dimension, recipe):
    states = [word]
    for _ in range(dimension + 1):
        states.append(source_step(states[-1], rule))
    for _ in range(dimension - 1):
        states = [fields(x, y, recipe) for x, y in zip(states, states[1:])]
    assert len(states) == 3
    return states


def exported_keys(grid, nodes):
    addresses = list(np.ndindex(grid.shape))
    ids = np.empty(grid.shape, dtype=np.uint32)
    for at in addresses:
        number = 0
        for offset in (-2, -1, 0, 1, 2):
            number = 2 * number + int(grid[at[:-1] + ((at[-1] + offset) % grid.shape[-1],)])
        ids[at] = number
    for axis, level in zip(range(grid.ndim - 2, -1, -1), nodes):
        pool = {tuple(int(x) for x in row): i for i, row in enumerate(level)}
        result = np.empty(grid.shape, dtype=np.uint32)
        for at in addresses:
            pattern = []
            for offset in (-2, -1, 0, 1, 2):
                other = list(at)
                other[axis] = (other[axis] + offset) % grid.shape[axis]
                pattern.append(int(ids[tuple(other)]))
            result[at] = pool[tuple(pattern)]
        ids = result
    return ids


manifest = json.loads((RUN / "archive_manifest.json").read_text())
rows = [json.loads(s) for s in (RUN / "floors.jsonl").read_text().splitlines()]
paths = [json.loads(s) for s in (RUN / "paths.jsonl").read_text().splitlines()]
execution = json.loads((RUN / "execution.json").read_text())
saved_analysis = json.loads((RUN / "analysis.json").read_text())
summary = json.loads((RUN / "summary.json").read_text())
by_name = {row["partial_rule"]["path"]: row for row in rows}
assert len(by_name) == len(rows) == len(manifest["members"]) == 1536
assert {(r["width"], r["rule"], r["dimension"]) for r in rows} == set(itertools.product((7, 8), range(256), (2, 3, 4)))
for path, expected in execution["source_hashes"].items():
    assert digest((ROOT / path).read_bytes()) == expected
archive_hash = hashlib.sha256()
with (RUN / "partial_rules.tar.gz").open("rb") as stream:
    for part in manifest["parts"]:
        encoded = (RUN / part["path"]).read_bytes()
        assert len(encoded) == part["size"] and digest(encoded) == part["sha256"]
        decoded = base64.b64decode(encoded.strip(), validate=True)
        assert stream.read(len(decoded)) == decoded
        archive_hash.update(decoded)
    assert not stream.read(1)
assert archive_hash.hexdigest() == manifest["archive_sha256"]
assert (RUN / "partial_rules.tar.gz").stat().st_size == manifest["archive_size"]
control_rules = {3, 77, 179, 232}
control_exports = {}
node_total = root_total = truth_total = checked = 0
with tarfile.open(RUN / "partial_rules.tar.gz", "r|gz") as archive:
    for info, meta in zip(archive, manifest["members"], strict=True):
        assert info.isfile() and info.name == meta["path"] and info.size == meta["size"]
        assert re.fullmatch(r"w[78]/rule\d{3}/d[234]\.json", info.name)
        raw = archive.extractfile(info).read()
        assert digest(raw) == meta["sha256"]
        record = json.loads(raw)
        assert json.dumps(record, sort_keys=True, separators=(",", ":"), allow_nan=False).encode() == raw
        row = by_name[info.name]
        w, d, rule = row["width"], row["dimension"], row["rule"]
        assert row["partial_rule"] == meta and row["status"] == "passed"
        assert record["width"] == w and record["dimension"] == d and record["rule"] == rule
        assert record["recipe"] == row["recipe"] == execution["recipes"][str(rule)]
        assert record["format"] == "ordered-five-tuple-physical-neighborhood-v1"
        assert record["radius"] == 2 and record["unforced_derivative"] == record["unforced_decoder"] == 0
        assert record["node_counts"] == row["node_counts"]
        assert len(record["node_counts"]) == len(record["nodes_delta_i32le_columns"]) == d - 1
        levels = []
        upper = 32
        for n, encoded in zip(record["node_counts"], record["nodes_delta_i32le_columns"]):
            data = base64.b64decode(encoded, validate=True)
            assert len(data) == n * 5 * 4
            columns = np.frombuffer(data, dtype="<i4").reshape(5, n).astype(np.int64)
            restored = np.cumsum(columns, axis=1).T.copy()
            assert restored.min() >= 0 and restored.max() < upper
            assert len(np.unique(restored, axis=0)) == n
            levels.append(restored)
            upper = n
            node_total += n
        k = record["forced_root_count"]
        assert k == upper == row["native"]["forced_keys"] == row["parent_recovery"]["forced_keys"]
        derivative = bitstream(record["forced_derivative_bits_big"], k)
        decoder = bitstream(record["forced_decoder_bits_big"], k)
        assert digest(derivative.tobytes() + decoder.tobytes()) == row["native_sha256"]
        shape = [4 ** (d - 1), 1 << w]
        assert record["source_phase_shape"] == row["phase_analysis"]["truth_shape"] == shape
        truth = bitstream(record["source_phase_derivative_bits_big"], int(np.prod(shape))).reshape(shape)
        degrees, terms = anf(truth)
        rnk = rank(truth)
        assert degrees.tolist() == row["phase_analysis"]["phase_degrees"]
        assert terms.tolist() == row["phase_analysis"]["phase_terms"]
        assert rnk == row["phase_analysis"]["source_rank"]
        expected = {"key_fraction": k / (shape[0] * shape[1]), "forced_flip_fraction": float(derivative.mean()),
                    "event_flip_fraction": float(truth.mean()), "source_degree_fraction": float(degrees.mean() / w),
                    "source_term_fraction": float(terms.mean() / (1 << w)), "affine_phase_fraction": float(np.mean(degrees <= 1)),
                    "source_rank_fraction": rnk / min(shape)}
        assert row["features"] == expected, info.name
        assert row["constraint_cells"] == (1 << w) * w * 4 ** (d - 1)
        assert row["direct_patch_checks"] == 15
        for gate in ("native", "parent_recovery"):
            assert row[gate]["passes"] and row[gate]["conflicting_keys"] == 0 and row[gate]["witness"] is None
        assert all(row[g] for g in ("native_replay", "parent_replay", "source_recovery", "parents_immutable"))
        if rule in control_rules:
            control_exports[w, rule, d] = (levels, derivative, decoder, record["recipe"])
        root_total += k
        truth_total += truth.size
        checked += 1
        if checked % 256 == 0:
            print(json.dumps({"archive_members_verified": checked, "seconds": round(time.perf_counter() - START, 2)}), flush=True)

# Fresh bounded native execution from exported laws, using no production code.
native_cells = recovery_cells = 0
for width, rule in itertools.product((7, 8), sorted(control_rules)):
    integer = (17 + rule) % (1 << width)
    word = np.array([(integer >> bit) & 1 for bit in range(width - 1, -1, -1)], dtype=np.uint8)
    top = None
    for d in (2, 3, 4):
        nodes, derivative, decoder, recipe = control_exports[width, rule, d]
        expected = prepared(word, rule, d, recipe)
        current = expected[0]
        for future in expected[1:]:
            ids = exported_keys(current, nodes)
            current = current ^ derivative[ids]
            assert np.array_equal(current, future), (width, rule, d, "fresh native step")
            native_cells += current.size
        recovered = decoder[exported_keys(expected[0], nodes)]
        parent = word if d == 2 else prepared(word, rule, d - 1, recipe)[0]
        assert np.array_equal(recovered, np.broadcast_to(parent[None], recovered.shape))
        recovery_cells += recovered.size
        top = expected[0]
    for d in (4, 3, 2):
        nodes, derivative, decoder, recipe = control_exports[width, rule, d]
        recovered = decoder[exported_keys(top, nodes)]
        assert np.array_equal(recovered, np.broadcast_to(recovered[0], recovered.shape))
        top = recovered[0]
    assert np.array_equal(top, word)

# Independently reconstruct source baselines and orbit-level model features.
source_names = ("event_flip_fraction", "source_degree_fraction", "source_term_fraction", "image_fraction")
feature_names = ("key_fraction", "forced_flip_fraction", "event_flip_fraction", "source_degree_fraction", "source_term_fraction", "affine_phase_fraction", "source_rank_fraction")
path_map = {(p["width"], p["rule"]): p for p in paths}
floor_map = {(r["width"], r["rule"], r["dimension"]): r for r in rows}
assert len(path_map) == 512 and all(p["status"] == "passed" and p["last_floor"] == 4 for p in paths)
for width in (7, 8):
    words = np.array([[(i >> b) & 1 for b in range(width - 1, -1, -1)] for i in range(1 << width)], dtype=np.uint8)
    for rule in range(256):
        successors = np.array([source_step(word, rule) for word in words])
        delta = words ^ successors
        degrees, terms = anf(delta[:, 0][None])
        expected = {"event_flip_fraction": float(delta.mean()), "source_degree_fraction": float(degrees[0] / width),
                    "source_term_fraction": float(terms[0] / (1 << width)), "image_fraction": len({bytes(row) for row in successors}) / len(words)}
        assert path_map[width, rule]["source_features"] == expected


def reflected(rule):
    return sum(((rule >> int(f"{x:03b}"[::-1], 2)) & 1) << x for x in range(8))


def conjugated(rule):
    return sum((1 - ((rule >> (7 - x)) & 1)) << x for x in range(8))


orbits = {}
for rule in range(256):
    members = sorted({rule, reflected(rule), conjugated(rule), reflected(conjugated(rule))})
    orbits[min(members)] = members
labels = json.loads((ROOT / "experiments/on_beam_256_4d_20260914/labels.json").read_text())
class_for = {r: int(c) for c, representatives in labels["representatives"].items() for r in representatives}
assert sorted(orbits) == saved_analysis["common_orbits"] and not saved_analysis["excluded_orbits"]
recipe_options = {"mask": ("birth", "death", "stay_one", "stay_zero"), "sign": (-1, 1),
                  "q": ("pair:-1:2", "pair:-2:1", "directed:-1:2:not-left-and-right", "directed:-2:1:left-and-not-right"),
                  "order": ("PDMQ", "PDQM")}


def feature_views(width, cohort):
    source, recipe, lifted = [], [], {d: [] for d in (2, 3, 4)}
    for o in cohort:
        members = orbits[o]
        source.append(np.mean([[path_map[width, r]["source_features"][f] for f in source_names] for r in members], axis=0))
        recipe.append(np.mean([[float(execution["recipes"][str(r)][k] == option) for k, options in recipe_options.items() for option in options] for r in members], axis=0))
        for d in (2, 3, 4):
            lifted[d].append(np.mean([[floor_map[width, r, d]["features"][f] for f in feature_names] for r in members], axis=0))
    source, recipe = np.asarray(source), np.asarray(recipe)
    lifted = {d: np.asarray(x) for d, x in lifted.items()}
    both = np.hstack((source, recipe)); full = np.hstack([lifted[d] for d in (2, 3, 4)])
    return {"source": source, "recipe": recipe, "source_recipe": both, "lift_all": full,
            **{f"lift{d}": lifted[d] for d in (2, 3, 4)}, "source_recipe_lift_all": np.hstack((both, full))}


def literal_predictions(x, y):
    answer = []
    for held in range(len(y)):
        train_x, train_y = np.delete(x, held, axis=0), np.delete(y, held)
        mean, std = train_x.mean(axis=0), train_x.std(axis=0)
        active = np.ptp(train_x, axis=0) > 0
        scaled = (train_x[:, active] - mean[active]) / std[active]
        target = (x[held, active] - mean[active]) / std[active]
        distances = [np.sum((scaled[train_y == c].mean(axis=0) - target) ** 2) for c in (1, 2, 3, 4)]
        answer.append(int(np.argmin(distances)) + 1)
    return answer


def balanced(y, prediction):
    return float(np.mean([np.mean(np.asarray(prediction)[y == c] == c) for c in (1, 2, 3, 4)]))


model_fits = 0
for width in (7, 8):
    for kind, cohort in (("models", sorted(orbits)), ("sensitivity", sorted(set(orbits) - {41, 106}))):
        saved = saved_analysis[kind][str(width)]
        assert saved["orbits"] == cohort
        y = np.array([class_for[o] for o in cohort])
        for name, x in feature_views(width, cohort).items():
            prediction = literal_predictions(x, y)
            assert prediction == saved["views"][name]["predicted"], (width, kind, name)
            assert y.tolist() == saved["views"][name]["true"]
            assert balanced(y, prediction) == saved["views"][name]["balanced_accuracy"]
            model_fits += 1

cohort = sorted(orbits); y = np.array([class_for[o] for o in cohort]); views = feature_views(7, cohort)
rng = np.random.Generator(np.random.PCG64(20260914)); null = []
for iteration in range(199):
    shuffled = rng.permutation(y)
    augmented = literal_predictions(views["source_recipe_lift_all"], shuffled)
    baseline = literal_predictions(views["source_recipe"], shuffled)
    null.append(balanced(shuffled, augmented) - balanced(shuffled, baseline))
assert null == saved_analysis["models"]["7"]["permutation_reference"]["differences"]
observed = saved_analysis["models"]["7"]["incremental_balanced_accuracy"]
assert (1 + sum(x >= observed for x in null)) / 200 == saved_analysis["models"]["7"]["permutation_reference"]["one_sided_p"]
assert summary["native_constraint_cells"] == sum(row["constraint_cells"] for row in rows)
assert summary["direct_patch_checks"] == 15 * len(rows)
report = {"reviewer": "Codex (OpenAI), independent reviewing agent /root/independent_pilot_review",
          "scope": "Complete archive and metric verification; independent source baselines and literal held-orbit analysis; bounded fresh native execution from exports, not a complete scientific rerun",
          "status": "passed", "implementation_commit": execution["implementation_commit"],
          "archive_sha256": archive_hash.hexdigest(), "archive_bytes": manifest["archive_size"],
          "members_verified": checked, "transport_parts_verified": len(manifest["parts"]),
          "ordered_nodes_verified": node_total, "forced_roots_verified": root_total, "source_truth_bits_verified": truth_total,
          "source_baselines_verified": len(paths), "literal_model_fits": model_fits, "permutation_draws_verified": 199,
          "bounded_fresh_rules": sorted(control_rules), "bounded_fresh_widths": [7, 8],
          "bounded_fresh_floors": 24, "fresh_native_cell_updates": native_cells, "fresh_parent_decoder_cells": recovery_cells,
          "observed_incremental_balanced_accuracy": observed,
          "permutation_reference_p": saved_analysis["models"]["7"]["permutation_reference"]["one_sided_p"],
          "review_script_sha256": digest(Path(__file__).read_bytes()),
          "wall_seconds": time.perf_counter() - START}
OUT.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report), flush=True)
