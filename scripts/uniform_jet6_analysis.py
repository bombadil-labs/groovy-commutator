"""Fixed descriptive/held-orbit cache comparison; no CA construction or tuning."""
from collections import Counter
import json
from pathlib import Path

import numpy as np

import on_beam_rule_analysis as prior

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / "experiments/on_beam_256_4d_20260914/run"
LABELS = ROOT / "experiments/on_beam_256_4d_20260914/labels.json"


def read_rows(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def analyze(rows, paths):
    labels = json.loads(LABELS.read_text())
    classes, orbits = prior.class_map(labels)
    current = {(r["width"], r["rule"], r["dimension"]): r for r in rows if r["status"] == "passed"}
    historical = {(r["width"], r["rule"], r["dimension"]): r for r in read_rows(OLD/"floors.jsonl") if r["status"] == "passed"}
    newpaths = {(r["width"], r["rule"]): r for r in paths}
    oldpaths = {(r["width"], r["rule"]): r for r in read_rows(OLD/"paths.jsonl")}
    common = [o for o, members in sorted(orbits.items())
              if all((w, r, d) in current and (w, r, d) in historical
                     for w in (7, 8) for r in members for d in (2, 3, 4))]
    for w in (7, 8):
        for o in common:
            for r in orbits[o]:
                assert newpaths[w, r]["source_features"] == oldpaths[w, r]["source_features"]

    def score(floors, pathmap, width, cohort):
        counts = Counter(classes[o] for o in cohort)
        if any(counts[c] < 2 for c in (1, 2, 3, 4)):
            return {"status": "censored", "class_counts": dict(counts),
                    "reason": "fewer than two complete symmetry orbits in a class"}
        y = [classes[o] for o in cohort]
        source = np.array([np.mean([[pathmap[width, r]["source_features"][f]
                                   for f in prior.SOURCE_FEATURES] for r in orbits[o]], axis=0) for o in cohort])
        lift = {d: np.array([np.mean([[floors[width, r, d]["features"][f]
                                      for f in prior.FEATURES] for r in orbits[o]], axis=0) for o in cohort])
                for d in (2, 3, 4)}
        all_lifts = np.concatenate([lift[d] for d in (2, 3, 4)], axis=1)
        views = {"source": source, **{f"lift{d}": lift[d] for d in (2, 3, 4)},
                 "lift_all": all_lifts, "source_lift_all": np.concatenate([source, all_lifts], axis=1)}
        scores = {name: prior.predict(prior.prepared_distances(values), y) for name, values in views.items()}
        return {"status": "completed", "orbits": cohort, "class_counts": dict(counts), "views": scores,
                "incremental_balanced_accuracy": scores["source_lift_all"]["balanced_accuracy"] - scores["source"]["balanced_accuracy"]}

    def descriptive(floors, width, dimension):
        summaries, spread = {}, []
        for c in (1, 2, 3, 4):
            cohort = [o for o in common if classes[o] == c]
            values = []
            for o in cohort:
                raw = np.array([[floors[width, r, dimension]["features"][f] for f in prior.FEATURES]
                                for r in orbits[o]])
                values.append(raw.mean(axis=0))
                spread.append({"orbit": o, "range": np.ptp(raw, axis=0).tolist()})
            summaries[str(c)] = {"orbits": len(cohort), "features": {
                f: prior.stats([v[i] for v in values]) for i, f in enumerate(prior.FEATURES)}}
        return {"classes": summaries, "within_orbit_ranges": spread}

    result = {"status": "completed", "class_convention": labels["convention"],
              "inference_unit": "symmetry orbit, equal member averaging",
              "comparison_cohort": "orbits complete through4D at both widths under both operators",
              "common_orbits": common, "excluded_orbits": sorted(set(orbits)-set(common)),
              "class_counts": dict(Counter(classes[o] for o in common)),
              "models": {}, "sensitivity": {}, "descriptive": {}, "outcomes": {},
              "scope": "Source-coordinate features; one constant six-field recipe; no new significance test or classifier tuning"}
    for width in (7, 8):
        w = str(width)
        result["models"][w] = {}
        result["sensitivity"][w] = {}
        result["descriptive"][w] = {}
        outcomes = {}
        for c in (1, 2, 3, 4):
            outcomes[str(c)] = dict(Counter(newpaths.get((width, r), {}).get("status", "not_run")
                                            for r in range(256) if classes[min(prior.orbit(r))] == c))
        result["outcomes"][w] = outcomes
        for name, floors, pathmap in (("jet6", current, newpaths), ("old4", historical, oldpaths)):
            result["models"][w][name] = score(floors, pathmap, width, common)
            result["sensitivity"][w][name] = score(floors, pathmap, width,
                                                  [o for o in common if o not in labels["sensitivity_exclude_orbits"]])
            result["descriptive"][w][name] = {str(d): descriptive(floors, width, d) for d in (2, 3, 4)}
        if all(result["models"][w][name]["status"] == "completed" for name in ("jet6", "old4")):
            result["models"][w]["paired_balanced_accuracy_difference"] = {
                name: result["models"][w]["jet6"]["views"][name]["balanced_accuracy"] -
                      result["models"][w]["old4"]["views"][name]["balanced_accuracy"]
                for name in result["models"][w]["jet6"]["views"]}
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    print(json.dumps(analyze(read_rows(args.run/"floors.jsonl"), read_rows(args.run/"paths.jsonl")), indent=2))
