"""Frozen-protocol Rule 110 history forecasts, scored by local ether compatibility.

Run --check-only before evaluation. Defaults read the committed protocol.
Labels use three fine rows ending at the forecast anchor, never future targets.
Models see only projected bits and are trained on disjoint random trajectories.
CSV counts retain every region, including empty regions (rates are then null).
Spatial controls back off through successively smaller radii to the marginal;
history controls back off through shorter histories to the marginal. Ties are 0.
No independence assumption is made about cells or successive times.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import sys
import time
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from groovy.ca import apply_rule  # noqa: E402
from experiment_history_validation import examples, fit, projected  # noqa: E402

PROTOCOL = ROOT / "docs/research/protocols/ether-regions-20260907.json"
REGIONS = ("background", "ambiguous", "departure", "all")


def evolve(initial, steps):
    rows = np.empty((steps + 1, len(initial)), dtype=np.uint8)
    rows[0] = initial
    for t in range(steps):
        rows[t + 1] = apply_rule(rows[t], 110)
    return rows


def row_keys(rows, radius):
    # Keep each row separate: the largest three-row patch needs 87 bits.
    key = np.zeros(rows.shape, dtype=np.uint32)
    for dx in range(-radius, radius + 1):
        key = (key << 1) | np.roll(rows, -dx, axis=1)
    return key


@lru_cache(None)
def reference_patches(word, radius):
    ref = evolve(np.array(list(word), dtype=np.uint8), 8)
    code = row_keys(ref, radius)
    return np.unique(np.stack([code[k:k + 7] for k in range(3)], axis=-1)
                     .reshape(-1, 3), axis=0)


def matches_ether(raw, anchors, radius, word):
    codes = [row_keys(raw[anchors - 2 + lag], radius) for lag in range(3)]
    matches = np.zeros(codes[0].shape, dtype=bool)
    for a, b, c in reference_patches(word, radius):
        matches |= (codes[0] == a) & (codes[1] == b) & (codes[2] == c)
    return matches


def fine_labels(raw, anchors, short, long, word):
    short_match = matches_ether(raw, anchors, short, word)
    long_match = matches_ether(raw, anchors, long, word)
    assert np.all(~long_match | short_match)
    return np.where(long_match, 0, np.where(short_match, 1, 2)).astype(np.uint8)


def target_labels(fine, kind, block, stride):
    # Target block j*b..j*b+b-1, expanded by its full fine causal radius.
    expansion = stride + (kind == "derivative")
    result = np.zeros((fine.shape[0], fine.shape[1] // block), dtype=np.uint8)
    for dx in range(-expansion, block + expansion):
        result = np.maximum(result, np.roll(fine, -dx, axis=1)[:, ::block])
    return result.ravel()


def check_detector(config):
    word = config["ether_word"]
    assert config["rule"] == 110 and config["detector_past_rows"] == 3
    ref = evolve(np.tile(np.array(list(word), dtype=np.uint8), 6), 12)
    assert np.array_equal(ref[0], ref[7])
    assert all(not np.array_equal(ref[0], ref[t]) for t in range(1, 7))
    anchors = np.arange(2, 12)
    checks = {"ether_temporal_period": 7, "detectors": []}
    for short, long in config["detectors"]:
        for phase in range(len(word)):
            labels = fine_labels(np.roll(ref, phase, axis=1), anchors, short, long, word)
            assert np.all(labels == 0)
        perturbed = ref.copy()
        perturbed[2, 42] ^= 1
        label = fine_labels(perturbed, np.array([2]), short, long, word)
        assert label[0, 42] == 2
        assert label[0, 0] == 0
        shifted = fine_labels(np.roll(perturbed, 11, axis=1), np.array([2]), short, long, word)
        assert np.array_equal(shifted, np.roll(label, 11, axis=1))
        future_changed = perturbed.copy()
        future_changed[3:] ^= 1
        assert np.array_equal(label, fine_labels(future_changed, np.array([2]), short, long, word))
        # Compare the encoded detector with a literal patch comparison on non-ether data.
        sample = evolve(np.random.default_rng(9001).integers(0, 2, 84, dtype=np.uint8), 5)
        phases = evolve(np.tile(np.array(list(word), dtype=np.uint8), 6), 8)
        for radius in (short, long):
            got = matches_ether(sample, np.array([2, 4]), radius, word)
            for ti, anchor in enumerate((2, 4)):
                for center in (0, 19, 83):
                    ix = (center + np.arange(-radius, radius + 1)) % 84
                    patch = sample[anchor - 2:anchor + 1, ix]
                    expected = any(np.array_equal(patch, phases[t:t + 3,
                        (x + np.arange(-radius, radius + 1)) % 84])
                        for t in range(7) for x in range(14))
                    assert bool(got[ti, center]) == expected
        checks["detectors"].append({"short": short, "long": long,
            "coherent_phases": len(reference_patches(word, long)),
            "all_phases_background": True, "single_flip_detected": True,
            "translation_covariant": True, "future_independent": True,
            "literal_patch_crosscheck": True, "long_implies_short": True})
    # Full causal footprint aggregation, including periodic wrap and all observers.
    fine = np.zeros((1, 420), dtype=np.uint8)
    fine[0, 0], fine[0, 211] = 2, 1
    for kind, block, stride in config["observers"]:
        out = target_labels(fine, kind, block, stride)
        radius = stride + (kind == "derivative")
        expected = [max(fine[0, (np.arange(j * block - radius,
                    (j + 1) * block + radius)) % 420]) for j in range(420 // block)]
        assert np.array_equal(out, expected)
    # Wide keys must retain all 21 bits and never cross row boundaries.
    bits = np.random.default_rng(9002).integers(0, 2, (9, 42), dtype=np.uint8)
    k, _ = examples(bits, 0, 6, radius=10)
    literal = sum(int(bits[6, dx % 42]) << (10 - dx) for dx in range(-10, 11))
    assert k[0] == literal
    train_seeds = sum(config["train_ensembles"], [])
    assert len(set(train_seeds)) == len(train_seeds)
    assert not set(train_seeds) & set(config["test_seeds"] + config["perturbed_seeds"])
    checks["causal_footprints_and_wide_keys"] = True
    checks["disjoint_training_and_test_seeds"] = True
    return checks


def make_raw(config, n, kind, seed):
    rng = np.random.default_rng(seed)
    if kind == "random":
        initial = rng.integers(0, 2, n, dtype=np.uint8)
    else:
        initial = np.tile(np.array(list(config["ether_word"]), dtype=np.uint8), n // 14)
        if kind == "perturbed":
            # Exact nearest-integer 2% without replacement (8 or 17 flipped bits).
            initial[rng.choice(n, round(n * config["perturbation_fraction"]), replace=False)] ^= 1
    fine_steps = config["burn"] + config["steps"] * max(x[2] for x in config["observers"])
    return evolve(initial, fine_steps)


def observe(raw, config, kind, block, stride):
    times = config["burn"] + np.arange(config["steps"] + 1) * stride
    return np.stack([projected(raw[t], 110, kind, block) for t in times])


def add_counts(output, identity, labels, y, pred, support, supported, baseline):
    for detector, lab in labels.items():
        for ri, region in enumerate(REGIONS):
            mask = np.ones(len(y), dtype=bool) if region == "all" else lab == ri
            output.append({**identity, "detector": detector, "region": region,
                "samples": int(mask.sum()), "errors": int(np.sum((pred != y) & mask)),
                "seen": int(np.sum((support > 0) & mask)),
                "supported": int(np.sum(supported & mask)),
                "supported_errors": int(np.sum((pred != y) & supported & mask)),
                "baseline_errors": int(np.sum((baseline != y) & mask)),
                "fixed": int(np.sum((baseline != y) & (pred == y) & mask)),
                "broken": int(np.sum((baseline == y) & (pred != y) & mask))})


def evaluate_observer(config, n, observer, training, tests):
    kind, block, stride = observer
    start, threshold = config["hmax"], config["min_support"]
    anchors = config["burn"] + np.arange(start, config["steps"]) * stride
    test_rows = [observe(raw, config, *observer) for _, _, raw in tests]
    labels = [{f"r{short}-{long}": target_labels(
        fine_labels(raw, anchors, short, long, config["ether_word"]), *observer)
        for short, long in config["detectors"]} for _, _, raw in tests]
    output = []
    for ensemble, seeds in enumerate(config["train_ensembles"], 1):
        train_rows = [observe(training[seed], config, *observer) for seed in seeds]
        backoff = baseline = None
        for h in range(start + 1):
            count, prediction, marginal = fit(train_rows, h, start)
            if backoff is None:
                backoff = [np.full((config["steps"] - start) * (n // block),
                                  marginal, dtype=np.uint8) for _ in tests]
            for i, ((test_kind, seed, _), rows) in enumerate(zip(tests, test_rows)):
                key, y = examples(rows, h, start)
                support = count[key]
                supported = support >= threshold
                backoff[i][supported] = prediction[key[supported]]
                if h == 0:
                    if baseline is None:
                        baseline = []
                    baseline.append(backoff[i].copy())
                identity = dict(n=n, projection=kind, block=block, stride=stride,
                    ensemble=ensemble, test_kind=test_kind, test_seed=seed,
                    model="history", depth=h, radius=1)
                add_counts(output, identity, labels[i], y, backoff[i], support, supported, baseline[i])
        # Successively wider spatial contexts; retain every requested comparator only.
        spatial_backoff = [x.copy() for x in baseline]
        for radius in range(2, max(config["snapshot_control_radii"]) + 1):
            count, prediction, _ = fit(train_rows, 0, start, radius=radius)
            for i, ((test_kind, seed, _), rows) in enumerate(zip(tests, test_rows)):
                key, y = examples(rows, 0, start, radius=radius)
                support = count[key]
                supported = support >= threshold
                spatial_backoff[i][supported] = prediction[key[supported]]
                if radius in config["snapshot_control_radii"]:
                    identity = dict(n=n, projection=kind, block=block, stride=stride,
                        ensemble=ensemble, test_kind=test_kind, test_seed=seed,
                        model="snapshot", depth=0, radius=radius)
                    add_counts(output, identity, labels[i], y, spatial_backoff[i], support,
                               supported, baseline[i])
    return output


def ratio(a, b):
    return a / b if b else None


def summarize(rows):
    fields = ("n", "projection", "block", "stride", "ensemble", "test_kind",
              "detector", "region", "model", "depth", "radius")
    groups = defaultdict(list)
    for row in rows:
        groups[tuple(row[k] for k in fields)].append(row)
    output = []
    for key, group in groups.items():
        record = dict(zip(fields, key))
        for field in ("samples", "errors", "seen", "supported", "supported_errors",
                      "baseline_errors", "fixed", "broken"):
            record[field] = sum(r[field] for r in group)
        assert record["baseline_errors"] - record["errors"] == record["fixed"] - record["broken"]
        record["error"] = ratio(record["errors"], record["samples"])
        record["baseline_error"] = ratio(record["baseline_errors"], record["samples"])
        record["supported_fraction"] = ratio(record["supported"], record["samples"])
        record["coverage"] = ratio(record["seen"], record["samples"])
        valid = [r for r in group if r["samples"]]
        differences = [(r["baseline_errors"] - r["errors"]) / r["samples"] for r in valid]
        record["seed_gain_min"] = min(differences) if valid else None
        record["seed_gain_max"] = max(differences) if valid else None
        record["test_trajectories"] = len(group)
        output.append(record)
    lookup = {tuple(r[k] for k in fields): r for r in output}
    for r in output:
        all_key = tuple("all" if k == "region" else r[k] for k in fields)
        total = lookup[all_key]
        r["frequency"] = ratio(r["samples"], total["samples"])
        r["contribution"] = ratio(r["baseline_errors"] - r["errors"], total["samples"])
        if r["region"] == "all":
            parts = [lookup[tuple(region if k == "region" else r[k] for k in fields)]
                     for region in REGIONS[:3]]
            for field in ("samples", "errors", "baseline_errors", "fixed", "broken"):
                assert sum(p[field] for p in parts) == r[field]
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=PROTOCOL)
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--output-prefix", default="ether_regions_20260907")
    args = parser.parse_args()
    config = json.loads(args.protocol.read_text())
    started = time.monotonic()
    checks = check_detector(config)
    print(json.dumps(checks), flush=True)
    if args.check_only:
        return
    prefix = ROOT / "results" / args.output_prefix
    output = []
    for n in config["sizes"]:
        training = {s: make_raw(config, n, "random", s) for s in sum(config["train_ensembles"], [])}
        tests = [("random", s, make_raw(config, n, "random", s)) for s in config["test_seeds"]]
        tests += [("ether", 0, make_raw(config, n, "ether", 0))]
        tests += [("perturbed", s, make_raw(config, n, "perturbed", s))
                  for s in config["perturbed_seeds"]]
        for observer in config["observers"]:
            output.extend(evaluate_observer(config, n, observer, training, tests))
            # Reproducible checkpoint after each observer; never changes the protocol.
            with prefix.with_suffix(".csv").open("w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=list(output[0]), lineterminator="\n")
                writer.writeheader()
                writer.writerows(output)
            print(f"completed n={n}, observer={observer}, rows={len(output)}, seconds={time.monotonic()-started:.1f}", flush=True)
    summary = summarize(output)
    columns = list(summary[0])
    prefix.with_suffix(".json").write_text(json.dumps({"columns": columns,
        "rows": [[row[key] for key in columns] for row in summary]}, separators=(",", ":")) + "\n")
    metadata = {"protocol": str(args.protocol.relative_to(ROOT)), "parameters": config,
        "protocol_commit": "3374637d7a025f10bdb10b82faed2311ce0434f2",
        "protocol_sha256": hashlib.sha256(args.protocol.read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "checks": checks, "python": platform.python_version(), "numpy": np.__version__,
        "rng": "numpy.default_rng (PCG64)", "row_count": len(output),
        "elapsed_seconds": round(time.monotonic() - started, 2),
        "implementation_details": ["Shared fine trajectories across observers; observation windows differ by stride.",
            "Pure ether seed 0; one phase tested for prediction, all phases checked by detector.",
            "Perturbation samples exactly round(0.02*n) initial sites without replacement.",
            "Spatial backoff uses successively smaller radii; history uses successively shorter histories.",
            "Two training ensembles share held-out trajectories; they are sensitivity repeats, not 16 independent test seeds.",
            "Regional rates pool integer counts; seed ranges are conditional on training, not confidence intervals."]}
    prefix.with_name(prefix.name + "_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"Saved {len(output)} rows and verified regional accounting", flush=True)


if __name__ == "__main__":
    main()
