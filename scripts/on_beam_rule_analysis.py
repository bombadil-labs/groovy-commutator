"""Frozen descriptive/held-orbit analysis; no cellular-automaton evaluation."""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path

import numpy as np

FEATURES = (
    "key_fraction", "forced_flip_fraction", "event_flip_fraction",
    "source_degree_fraction", "source_term_fraction", "affine_phase_fraction",
    "source_rank_fraction",
)
SOURCE_FEATURES = ("event_flip_fraction", "source_degree_fraction",
                   "source_term_fraction", "image_fraction")
RECIPE_FIELDS = {
    "mask": ("birth", "death", "stay_one", "stay_zero"),
    "sign": (-1, 1),
    "q": ("pair:-1:2", "pair:-2:1", "directed:-1:2:not-left-and-right",
          "directed:-2:1:left-and-not-right"),
    "order": ("PDMQ", "PDQM"),
}


def reflection(rule):
    return sum(((rule >> i) & 1) << (((i & 1) << 2) | (i & 2) | ((i & 4) >> 2))
               for i in range(8))


def conjugate(rule):
    return sum((1 - ((rule >> (7 - i)) & 1)) << i for i in range(8))


def orbit(rule):
    return sorted({rule, reflection(rule), conjugate(rule), reflection(conjugate(rule))})


def class_map(labels):
    representatives = {int(r): int(c) for c, rules in labels["representatives"].items()
                       for r in rules}
    orbits = {min(orbit(r)): orbit(r) for r in range(256)}
    assert len(orbits) == len(representatives) == 88
    assert set(orbits) == set(representatives)
    assert sum(map(len, orbits.values())) == 256
    return representatives, orbits


def recipe_vector(recipe):
    return [float(recipe[field] == option) for field, options in RECIPE_FIELDS.items()
            for option in options]


def stats(values):
    x = np.asarray(values, dtype=float)
    if not len(x):
        return None
    return {"mean": float(x.mean()), "median": float(np.median(x)),
            "min": float(x.min()), "max": float(x.max())}


def prepared_distances(x):
    """Training-only scale for each held-out orbit; centering cancels in distances."""
    x = np.asarray(x, dtype=float)
    scales = []
    for i in range(len(x)):
        train = np.delete(x, i, axis=0)
        varying = np.ptp(train, axis=0) > 0
        inv = np.zeros(x.shape[1], dtype=float)
        inv[varying] = 1 / train[:, varying].std(axis=0, ddof=0)
        scales.append(inv)
    return x, np.asarray(scales)


def predict(prepared, labels):
    x, scales = prepared
    y = np.asarray(labels, dtype=int)
    counts = np.bincount(y, minlength=5)
    if min(counts[1:5]) < 2:
        return {"status": "censored", "reason": "fewer than two orbits in a class"}
    sums = np.stack([x[y == c].sum(axis=0) for c in range(1, 5)])
    answer = []
    for i in range(len(x)):
        centers = []
        for c in range(1, 5):
            own = int(y[i] == c)
            centers.append((sums[c - 1] - own * x[i]) / (counts[c] - own))
        distances = (((np.asarray(centers) - x[i]) * scales[i]) ** 2).sum(axis=1)
        answer.append(int(np.argmin(distances)) + 1)
    confusion = np.zeros((4, 4), dtype=int)
    for truth, inferred in zip(y, answer):
        confusion[truth - 1, inferred - 1] += 1
    recalls = np.diag(confusion) / confusion.sum(axis=1)
    return {"status": "completed", "true": y.tolist(), "predicted": answer,
            "confusion": confusion.tolist(), "recall": recalls.tolist(),
            "accuracy": float(np.trace(confusion) / len(y)),
            "balanced_accuracy": float(recalls.mean())}


def analyze(rows, paths, recipes, labels, budget=None):
    classes, orbits = class_map(labels)
    floors = {(r["width"], r["rule"], r["dimension"]): r for r in rows
              if r["status"] == "passed"}
    path_map = {(p["width"], p["rule"]): p for p in paths}
    common = [o for o, members in sorted(orbits.items())
              if all((w, r, 4) in floors for w in (7, 8) for r in members)]
    result = {"class_convention": labels["convention"], "inference_unit": "symmetry orbit",
              "common_orbits": common, "excluded_orbits": sorted(set(orbits) - set(common)),
              "common_class_counts": dict(Counter(classes[o] for o in common)),
              "outcomes": {}, "descriptive": {}, "models": {}, "sensitivity": {}}
    for width in (7, 8):
        outcomes = {}
        for category in ("class", "recipe"):
            groups = {}
            for rule in range(256):
                group = str(classes[min(orbit(rule))]) if category == "class" else json.dumps(recipes[rule], sort_keys=True)
                counts = groups.setdefault(group, Counter())
                counts["total"] += 1
                counts[path_map.get((width, rule), {}).get("status", "not_run")] += 1
            outcomes[category] = {k: dict(v) for k, v in groups.items()}
        result["outcomes"][str(width)] = outcomes
        description = {}
        for dimension in (2, 3, 4):
            d = {}
            for stratum in ("all", "birth_positive_pair_PDMQ"):
                class_values = {c: [] for c in range(1, 5)}
                spreads = []
                for o, members in sorted(orbits.items()):
                    if not all((width, r, dimension) in floors for r in members):
                        continue
                    selected = members if stratum == "all" else [r for r in members if recipes[r] == {
                        "mask": "birth", "sign": 1, "q": "pair:-1:2", "order": "PDMQ"}]
                    if not selected:
                        continue
                    values = np.array([[floors[width, r, dimension]["features"][f]
                                        for f in FEATURES] for r in selected])
                    class_values[classes[o]].append((o, len(selected), values.mean(axis=0)))
                    spreads.append({"orbit": o, "range": np.ptp(values, axis=0).tolist()})
                summaries = {}
                for c, entries in class_values.items():
                    summaries[str(c)] = {"orbits": len(entries), "rules": sum(n for _, n, _ in entries),
                        "features": {f: stats([v[i] for _, _, v in entries]) for i, f in enumerate(FEATURES)}}
                d[stratum] = {"classes": summaries, "within_orbit_ranges": spreads}
            description[str(dimension)] = d
        result["descriptive"][str(width)] = description

        def run_models(cohort, permutations=False):
            if budget:
                budget.check()
            counts = Counter(classes[o] for o in cohort)
            if any(counts[c] < 2 for c in range(1, 5)):
                return {"status": "censored", "reason": "fewer than two complete orbits in a class",
                        "orbits": cohort, "class_counts": dict(counts)}
            y = [classes[o] for o in cohort]
            source, recipe, lifted = [], [], {d: [] for d in (2, 3, 4)}
            for o in cohort:
                members = orbits[o]
                source.append(np.mean([[path_map[width, r]["source_features"][f]
                                        for f in SOURCE_FEATURES] for r in members], axis=0))
                recipe.append(np.mean([recipe_vector(recipes[r]) for r in members], axis=0))
                for d in (2, 3, 4):
                    lifted[d].append(np.mean([[floors[width, r, d]["features"][f]
                                               for f in FEATURES] for r in members], axis=0))
            source, recipe = np.asarray(source), np.asarray(recipe)
            lifted = {d: np.asarray(v) for d, v in lifted.items()}
            both = np.concatenate([source, recipe], axis=1)
            all_lifts = np.concatenate([lifted[d] for d in (2, 3, 4)], axis=1)
            views = {"source": source, "recipe": recipe, "source_recipe": both,
                     **{f"lift{d}": lifted[d] for d in (2, 3, 4)}, "lift_all": all_lifts,
                     "source_recipe_lift_all": np.concatenate([both, all_lifts], axis=1)}
            prepared = {name: prepared_distances(x) for name, x in views.items()}
            scores = {name: predict(p, y) for name, p in prepared.items()}
            delta = scores["source_recipe_lift_all"]["balanced_accuracy"] - scores["source_recipe"]["balanced_accuracy"]
            answer = {"status": "completed", "orbits": cohort, "class_counts": dict(counts),
                      "views": scores, "incremental_balanced_accuracy": delta}
            if permutations:
                rng = np.random.Generator(np.random.PCG64(20260914))
                null = []
                for iteration in range(199):
                    if budget and iteration % 10 == 0:
                        budget.check()
                    shuffled = rng.permutation(y)
                    full = predict(prepared["source_recipe_lift_all"], shuffled)["balanced_accuracy"]
                    baseline = predict(prepared["source_recipe"], shuffled)["balanced_accuracy"]
                    null.append(full - baseline)
                answer["permutation_reference"] = {"null": "global orbit-label exchangeability; not conditional incremental information",
                    "seed": 20260914, "differences": null,
                    "one_sided_p": (1 + sum(v >= delta for v in null)) / 200}
            return answer

        result["models"][str(width)] = run_models(common, permutations=width == 7)
        result["sensitivity"][str(width)] = run_models([o for o in common if o not in labels["sensitivity_exclude_orbits"]])
    models = result["models"]
    result["predictions"] = {"P1_all_paths_pass": all(path_map.get((w, r), {}).get("status") == "passed"
                                                    for w in (7, 8) for r in range(256))}
    if all(models[str(w)]["status"] == "completed" for w in (7, 8)):
        result["predictions"]["P3_usefulness_criterion"] = (
            all(models[str(w)]["incremental_balanced_accuracy"] >= 0.05 for w in (7, 8))
            and models["7"]["permutation_reference"]["one_sided_p"] <= 0.05)
    else:
        result["predictions"]["P3_usefulness_criterion"] = "censored"
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    records = [json.loads(line) for line in (args.run / "floors.jsonl").read_text().splitlines()]
    paths = [json.loads(line) for line in (args.run / "paths.jsonl").read_text().splitlines()]
    recipe_data = json.loads((args.run / "execution.json").read_text())["recipes"]
    labels = json.loads(Path("experiments/on_beam_256_4d_20260914/labels.json").read_text())
    print(json.dumps(analyze(records, paths, {int(k): v for k, v in recipe_data.items()}, labels), indent=2))
