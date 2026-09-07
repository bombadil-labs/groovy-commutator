"""Independent-seed validation of finite observed history as a predictor.

No microdynamics are changed. Each model estimates P(next projected bit | a
radius-one neighborhood at the current and h previous observed times).
Every depth uses the SAME target times, starting at hmax. Models use eight
training trajectories and report four independent test trajectories separately.

Sparse-history control: below min_support observations, back off to the
longest shorter supported history, ultimately to a training-only marginal
majority. We also retain the recovered baseline's zero-default predictions.
The backed-off predictor is evaluated on ALL test samples, never just the seen
subset. Coverage and supported-subset error are separate diagnostics.

The current-only radius-three comparator has seven bits, matching h=6's seven
observed TIMES only in count of samples, not information capacity: h=6 sees
21 bits. Its purpose is a spatial context control, not a capacity-matched test.
Counts are observations, NOT independent replicates; no cell-level CIs.

Outputs: per-test-seed CSV, aggregate JSON, parameter/runtime JSON, SVG figure.
Purely empirical minimum history is computed post hoc at thresholds .01/.05/.10;
it is not a proof of sufficient state, nor a tuned model's unbiased test score.
"""
from __future__ import annotations

import argparse
import csv
import json
import platform
import sys
import zlib
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from groovy.ca import apply_rule  # noqa: E402

RULES = [0, 4, 51, 170, 184, 41, 30, 45, 90, 54, 106, 110]
OBSERVERS = [("parity", 2, 2), ("parity", 4, 4),
             ("majority", 3, 1), ("majority", 5, 1),
             ("derivative", 1, 1)]
TRAIN_SEEDS = list(range(101, 109))
TEST_SEEDS = list(range(201, 205))


def projected(s, rule, kind, block):
    if kind == "derivative":
        return s ^ apply_rule(s, rule)
    x = s.reshape(-1, block)
    if kind == "parity":
        return np.bitwise_xor.reduce(x, axis=1)
    if kind == "majority":
        return (x.sum(axis=1) > block // 2).astype(np.uint8)
    raise ValueError(kind)


def trajectory(rule, kind, block, stride, n, steps, burn, seed):
    if n % block:
        raise ValueError("Ring width must be divisible by block size")
    s = np.random.default_rng(seed).integers(0, 2, n, dtype=np.uint8)
    for _ in range(burn):
        s = apply_rule(s, rule)
    out = [projected(s, rule, kind, block)]
    raw = []
    for _ in range(steps):
        for _ in range(stride):
            raw.append(s.copy())
            s = apply_rule(s, rule)
        out.append(projected(s, rule, kind, block))
    # Global row-major packing; no per-row padding. Same ring and time window.
    payload = np.packbits(np.stack(raw).ravel()).tobytes()
    comp = len(zlib.compress(payload, 9)) / len(payload)
    return np.stack(out), comp


def contexts(rows, radius=1):
    key = np.zeros(rows.shape, dtype=np.int32)
    for offset in range(-radius, radius + 1):
        key = (key << 1) | np.roll(rows, -offset, axis=1)
    return key


def examples(rows, h, start, radius=1):
    ng = contexts(rows, radius)
    key = np.zeros((len(rows) - 1 - start, rows.shape[1]), dtype=np.int32)
    for lag in range(h + 1):
        key |= ng[start-lag:len(rows)-1-lag] << ((2 * radius + 1) * lag)
    return key.ravel(), rows[start+1:].ravel()


def fit(rows, h, start, radius=1):
    pairs = [examples(x, h, start, radius) for x in rows]
    k = np.concatenate([x[0] for x in pairs])
    y = np.concatenate([x[1] for x in pairs])
    size = 1 << ((2 * radius + 1) * (h + 1))
    count = np.bincount(k, minlength=size).astype(np.int32)
    ones = np.bincount(k[y == 1], minlength=size).astype(np.int32)
    return count, (2 * ones > count).astype(np.uint8), int(y.sum() > len(y) / 2)


def evaluate(rule, kind, block, stride, n, args):
    train = [trajectory(rule, kind, block, stride, n, args.steps, args.burn, s)[0]
             for s in TRAIN_SEEDS]
    test = [trajectory(rule, kind, block, stride, n, args.steps, args.burn, s)
            for s in TEST_SEEDS]
    spatial_count, spatial_pred, marginal = fit(train, 0, args.hmax, radius=3)
    spatial_errors = []
    for mt, _ in test:
        k, y = examples(mt, 0, args.hmax, radius=3)
        pred = np.where(spatial_count[k] >= args.min_support, spatial_pred[k], marginal)
        spatial_errors.append(float(np.mean(pred != y)))
    backoff = [np.full((args.steps - args.hmax) * mt.shape[1], marginal, dtype=np.uint8)
               for mt, _ in test]
    output = []
    for h in range(args.hmax + 1):
        count, pred, _ = fit(train, h, args.hmax)
        for i, (seed, (mt, comp)) in enumerate(zip(TEST_SEEDS, test)):
            k, y = examples(mt, h, args.hmax)
            support = count[k]
            supported = support >= args.min_support
            naive = pred[k]
            backoff[i][supported] = naive[supported]
            output.append({"rule": rule, "projection": kind, "block": block,
                "stride": stride, "n": n, "test_seed": seed, "history": h,
                "test_samples": len(y), "error": float(np.mean(backoff[i] != y)),
                "zero_default_error": float(np.mean(naive != y)),
                "coverage": float(np.mean(support > 0)),
                "supported_fraction": float(supported.mean()),
                "supported_error": float(np.mean(naive[supported] != y[supported]))
                    if supported.any() else None,
                "radius3_current_error": spatial_errors[i],
                "raw_compression": comp})
    return output


def summarize(rows):
    result = []
    for rule in sorted({x["rule"] for x in rows}):
        for n in sorted({x["n"] for x in rows}):
            for kind, block, stride in OBSERVERS:
                subset = [x for x in rows if (x["rule"], x["n"], x["projection"], x["block"])
                          == (rule, n, kind, block)]
                curves = []
                for h in sorted({x["history"] for x in subset}):
                    d = [x for x in subset if x["history"] == h]
                    curves.append({"history": h, **{field: float(np.mean([x[field] for x in d]))
                        for field in ("error", "zero_default_error", "coverage", "supported_fraction")},
                        "test_seed_min_error": min(x["error"] for x in d),
                        "test_seed_max_error": max(x["error"] for x in d)})
                e0, eh = curves[0]["error"], curves[-1]["error"]
                result.append({"rule": rule, "n": n, "projection": kind, "block": block,
                    "stride": stride, "curve": curves,
                    "repair": None if e0 == 0 else (e0 - eh) / e0,
                    "observed_h_star": {str(t): next((x["history"] for x in curves if x["error"] <= t), None)
                                        for t in (.01, .05, .10)},
                    "radius3_current_error": float(np.mean([x["radius3_current_error"] for x in subset])),
                    "raw_compression": float(np.mean([x["raw_compression"] for x in subset]))})
    return result


def plot_summary(summary, destination):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    colors = {170: "#6b7280", 30: "#ce6c29", 90: "#3171a8", 54: "#8172a2",
              106: "#ad506c", 110: "#21856a"}
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), sharey=True)
    for ax, (kind, block) in zip(axes, [("parity", 2), ("parity", 4), ("majority", 3)]):
        for rule, color in colors.items():
            d = next(x for x in summary if (x["rule"], x["n"], x["projection"], x["block"])
                     == (rule, 420, kind, block))
            curve = d["curve"]
            hs = [x["history"] for x in curve]
            ax.plot(hs, [x["error"] for x in curve], label=f"Rule {rule}", color=color, marker="o", ms=3)
            ax.fill_between(hs, [x["test_seed_min_error"] for x in curve],
                            [x["test_seed_max_error"] for x in curve], color=color, alpha=.10)
        ax.set(title=f"{kind.capitalize()}, block {block}", xlabel="Previous observed time steps")
        ax.set_ylim(-.015, .52)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=.2)
    axes[0].set_ylabel("Held-out next-bit error")
    axes[-1].legend(loc="upper right", fontsize=8)
    fig.suptitle("History repairs different losses under different projections", fontsize=14)
    fig.text(.5, .005, "n=420 · 8 training seeds, 4 test seeds · shaded range: test trajectories · support-aware backoff", ha="center", fontsize=9)
    fig.tight_layout(rect=(0, .035, 1, 1))
    fig.savefig(destination, metadata={"Date": None})
    plt.close(fig)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--rules", nargs="+", type=int, default=RULES)
    p.add_argument("--sizes", nargs="+", type=int, default=[300, 420])
    p.add_argument("--steps", type=int, default=512)
    p.add_argument("--burn", type=int, default=150)
    p.add_argument("--hmax", type=int, default=6)
    p.add_argument("--min-support", type=int, default=5)
    p.add_argument("--output-prefix", default="history_validation_20260907")
    args = p.parse_args()
    if not 0 <= args.hmax <= 6 or args.steps <= args.hmax or args.burn < 0 or args.min_support < 1:
        p.error("Require 0 <= hmax <= 6, steps > hmax, burn >= 0, and min-support >= 1")
    if any(r not in range(256) for r in args.rules) or any(n < 60 or n % 60 for n in args.sizes):
        p.error("Rules must be 0..255; sizes must be positive multiples of 60")
    prefix = ROOT / "results" / args.output_prefix
    rows = []
    for n in args.sizes:
        for rule in args.rules:
            for kind, block, stride in OBSERVERS:
                rows.extend(evaluate(rule, kind, block, stride, n, args))
            print(f"completed rule {rule}, n={n}", flush=True)
    with prefix.with_suffix(".csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = summarize(rows)
    prefix.with_suffix(".json").write_text(json.dumps(summary, indent=2) + "\n")
    metadata = {"parameters": vars(args), "train_seeds": TRAIN_SEEDS, "test_seeds": TEST_SEEDS,
                "observers": OBSERVERS, "rng": "numpy.default_rng (PCG64)",
                "python": platform.python_version(), "numpy": np.__version__,
                "zlib": zlib.ZLIB_RUNTIME_VERSION, "row_count": len(rows),
                "uncertainty": "Per-test-trajectory range, conditional on one shared training ensemble; no iid-cell CIs"}
    prefix.with_name(prefix.name + "_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    if 420 in args.sizes and {170, 30, 90, 54, 106, 110}.issubset(args.rules):
        plot_summary(summary, prefix.with_suffix(".svg"))
    print(f"Wrote {len(rows)} per-seed observations under {prefix.name}")


if __name__ == "__main__":
    main()
