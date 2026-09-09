"""Post-outcome diagnostic: locate frozen raw-NFA control censoring without changing any ceiling."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from experiment_sofic_defect_orbit_raw import (  # noqa:E402
    ResourceCeiling,
    graph_stats,
    graph_visible_mask,
    raw_image_limited,
    target_id,
)
from experiment_reachable_context_invariants import DIAGONAL, paired_table  # noqa:E402
from experiment_causal_witness_horizon import macro_rule  # noqa:E402
from sofic_graph import initial_one_seed_graph  # noqa:E402

SPECS = [
    (35, "00000001", (2, 6)),
    (5, "01001100", (0, 2)),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    rows = []
    for rule, key, pair in SPECS:
        tid = target_id(key)
        seed = 8 * pair[0] + pair[1]
        ph = paired_table(macro_rule(rule))
        x = initial_one_seed_graph(DIAGONAL, seed)
        slices = []
        censor = None
        for t in range(4):
            slices.append({"horizon": t, **graph_stats(x), "target_visible": bool((graph_visible_mask(x) >> tid) & 1)})
            if t == 3:
                break
            try:
                x, stats = raw_image_limited(x, ph)
                slices[-1]["next_raw_image"] = stats
            except ResourceCeiling as exc:
                censor = {
                    "source_horizon": t,
                    "attempted_next_horizon": t + 1,
                    "kind": exc.kind,
                    "limit": exc.limit,
                    "observed": exc.observed,
                }
                slices[-1]["censoring"] = censor
                break
        rows.append({"rule": rule, "target": key, "pair": f"{pair[0]}-{pair[1]}", "censoring": censor, "slices": slices})
    out = {
        "ok": True,
        "kind": "post-outcome diagnostic only",
        "changes_frozen_thresholds": False,
        "controls": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
