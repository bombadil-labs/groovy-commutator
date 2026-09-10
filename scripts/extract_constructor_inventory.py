"""Extract issue66's descriptive inventory from saved results; no CA evaluation."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "finite_role": "results/ternary_commutator_lift_20260909_summary.json",
    "intrinsic_role": "results/local_ternary_lift_20260909_summary.json",
    "full_gradient": "results/full_gradient_closure_20260910.json",
    "axial_axis_order": "results/guard_free_axial_lift_20260910.json",
}

def extract():
    raw = {k: (ROOT / p).read_bytes() for k, p in SOURCES.items()}
    data = {k: json.loads(v) for k, v in raw.items()}
    finite = data["finite_role"]
    intrinsic = data["intrinsic_role"]
    gradient = data["full_gradient"]
    axial = data["axial_axis_order"]
    sets = {
        "finite_role": sorted(itertools.chain.from_iterable(finite["closure_rules_by_depth"].values())),
        "intrinsic_role": intrinsic["finite_local_closure_rules"],
        "full_gradient": gradient["radius_one_rules"],
        "axial_axis_order": axial["compatible_and_axis_permutation_equivariant_rules"],
    }
    for values in sets.values():
        assert values == sorted(set(values))
        assert all(type(v) is int and 0 <= v < 256 for v in values)
    assert len(sets["finite_role"]) == finite["finite_closure_rule_count"]
    assert len(sets["intrinsic_role"]) == intrinsic["finite_local_closure_within_depth_4_count"]
    assert sets["full_gradient"] == gradient["constant_complement_response_rules"]
    assert sets["axial_axis_order"] == sorted(set(axial["all_interfaces_rules"]) & set(axial["axis_permutation_equivariant_rules"]))
    domains = {
        "finite_role": {"constructor": "cumulative L/R/C role vocabulary", "substrate": "binary periodic ring n=8", "max_depth": finite["max_depth"]},
        "intrinsic_role": {"constructor": "cumulative L/R/C local-rule vocabulary", "substrate": "infinite binary one-dimensional lattice", "max_depth": intrinsic["max_depth"]},
        "full_gradient": {"constructor": "full-gradient factor of ordered two-axis macro law", "substrate": "infinite binary two-dimensional lattice; 66 replication-compatible sources", "max_radius": 1},
        "axial_axis_order": {"constructor": "axial replication plus axis-order independence", "substrate": "local infinite-lattice 1D-to-2D and 2D-to-3D interfaces"},
    }
    def intersection(*keys):
        return sorted(set.intersection(*(set(sets[k]) for k in keys)))
    return {
        "status": "descriptive extraction of existing results; not an experiment",
        "source_files": {k: {"path": SOURCES[k], "sha256": hashlib.sha256(raw[k]).hexdigest()} for k in SOURCES},
        "sets": {k: {**domains[k], "count": len(v), "rules": v} for k, v in sets.items()},
        "pairwise_intersections": [
            {"left": a, "right": b, "rules": intersection(a, b)}
            for a, b in itertools.combinations(sets, 2)
        ],
        "triple_intersections": {
            "finite_role_full_gradient_axial_axis_order": intersection("finite_role", "full_gradient", "axial_axis_order"),
            "intrinsic_role_full_gradient_axial_axis_order": intersection("intrinsic_role", "full_gradient", "axial_axis_order"),
        },
        "nonlinear_gradient_comparisons": [
            {"rule": rule, **{key: rule in values for key, values in sets.items()}}
            for rule in (142, 178, 212, 232)
        ],
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = extract()
    if args.check:
        assert result == json.loads(args.check.read_text()), "Saved inventory differs from its source extraction"
        print("All four source sets and six pairwise intersections match the saved inventory.")
    elif args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    else:
        print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
