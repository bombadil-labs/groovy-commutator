#!/usr/bin/env python3
"""Retrospective timing audit of PR #279; never rewrites its frozen evidence.

Count stored driven-gadget disagreements on K arms, then replay one failing
trial for each of bases 51, 90 and 110. Compare the historical post-step stream
with the pre-step input required by gadget(). This is a diagnostic selected
after seeing the failure, not a new prediction or a corrected full census.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RUN = "experiments/held_structures_20260918/run.py"
ROWS = "results/held_structures_20260918/rows.json"
OUT = ROOT / "results/held_structures_20260921_timing_audit.json"


def main():
    spec = importlib.util.spec_from_file_location("held_timing", ROOT / RUN)
    u9 = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = u9
    spec.loader.exec_module(u9)
    rows = json.loads((ROOT / ROWS).read_text())["rows"]
    kept = [r for r in rows if r["arm"] in ("Kall_plus", "Kall_minus", "Kex")]
    trials = [(r, t) for r in kept for t in r["trials"]]
    witnesses = []
    for base in (51, 90, 110):
        row, trial = next((r, t) for r, t in trials
                          if r["base"] == base and t["heal_driven_pred"] != t["heal"])
        u, rep, j = row["u"], trial["rep"], trial["origin"]
        rng = np.random.default_rng(u9.seed("transverse", u, rep))
        x = (rng.random(u9.W) < 0.5).astype(np.uint8)
        for _ in range(256):
            x = u9.eca_step(x, base)
        start = tuple(int(x[(j + d) % u9.W]) for d in (-1, 0, 1))
        assert list(start) == trial["start"]
        state = np.vstack([x, x.copy()])
        state[1, j] ^= 1
        rule = u9.HandedRule("timing-audit", row["table"])
        _, _, trans = u9.gadget(u)
        before, after, free_before = [], [], []
        healing = 129
        fx = x.copy()
        for t in range(1, 129):
            before.append(tuple(int(state[0, (j + d) % u9.W]) for d in (-2, 2)))
            free_before.append(tuple(int(fx[(j + d) % u9.W]) for d in (-2, 2)))
            state = u9.handed_step(state, rule)
            fx = u9.eca_step(fx, base)
            after.append(tuple(int(state[0, (j + d) % u9.W]) for d in (-2, 2)))
            if healing == 129 and not u9.defects(state).any():
                healing = t
        predict = lambda stream: u9.gadget_heal(trans, start, stream)[0] or 129
        old, corrected, free_corrected = map(predict, (after, before, free_before))
        assert healing == trial["heal"]
        assert old == trial["heal_driven_pred"] and old != healing
        assert corrected == healing
        if base == 51:
            assert before == free_before and free_corrected == healing
        witnesses.append({"base": base, "completion": u, "arm": row["arm"],
                          "rep": rep, "origin": j, "actual_heal": healing,
                          "historical_post_step_prediction": old,
                          "corrected_pre_step_driven_prediction": corrected,
                          "corrected_pre_step_free_prediction": free_corrected})
    sources = [RUN, ROWS, "scripts/audit_held_structure_stream_timing.py"]
    result = {
        "status": "retrospective diagnostic; full experiment not regenerated",
        "K_arm_trials": len(trials),
        "stored_driven_healing_mismatches": sum(t["heal_driven_pred"] != t["heal"] for _, t in trials),
        "invalidated_prediction_keys": ["P4a", "P4c", "P4d"],
        "witnesses": witnesses,
        "source_hashes": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in sources},
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
