"""Aggregate the frozen Research035 lazy-union recovery."""
from __future__ import annotations
import argparse, json
from collections import Counter
from pathlib import Path

EXPECTED_SURVIVORS = 170
EXPECTED_CLASSES = {"II": 158, "III": 12}


def canonical(rows, status):
    for r in rows:
        for lang in r["languages"]:
            for s in lang["statuses"]:
                if s["status"] == status:
                    return {"rule": r["rule"], "wclass": r["wclass"], "pair": lang["pair"], "seed_symbol": lang["seed_symbol"], "width3_word_count": lang["width3_word_count"], **s, "closure_horizon": lang["closure_horizon"], "censoring": lang["censoring"]}
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    shards = [json.loads(p.read_text()) for p in sorted(args.input_dir.rglob("*.json"))]
    shards = [x for x in shards if x.get("experiment") == "sofic-defect-orbit-lazy-recovery"]
    if not shards:
        raise SystemExit("no lazy recovery shards")
    assert {x["schema"] for x in shards} == {1}
    assert {x["hmax"] for x in shards} == {12}
    assert len({json.dumps(x["source_hashes"], sort_keys=True) for x in shards}) == 1
    assert len({json.dumps(x["resource_limits"], sort_keys=True) for x in shards}) == 1

    coverage = []
    rows = []
    for x in shards:
        coverage.extend(range(x["rule_start"], x["rule_end"]))
        rows.extend(x["rows"])
    assert sorted(coverage) == list(range(256)) and len(set(coverage)) == 256
    rows.sort(key=lambda x: x["rule"])
    assert [r["rule"] for r in rows] == list(range(256))
    survivors = sum(r["research034_survivors"] for r in rows)
    assert survivors == EXPECTED_SURVIVORS
    classes = Counter()
    for r in rows:
        if r["research034_survivors"]:
            classes[r["wclass"]] += r["research034_survivors"]
    assert dict(sorted(classes.items())) == EXPECTED_CLASSES

    statuses = Counter()
    status_classes = {}
    status_horizons = {}
    censor_stage = Counter()
    censor_reason = Counter()
    censor_horizon = Counter()
    sentinels = []
    for r in rows:
        for lang in r["languages"]:
            if lang["is_r122_161_sentinel"]:
                sentinels.append({"rule": r["rule"], "wclass": r["wclass"], **lang})
            for s in lang["statuses"]:
                statuses[s["status"]] += 1
                status_classes.setdefault(s["status"], Counter())[r["wclass"]] += 1
                status_horizons.setdefault(s["status"], Counter())[str(s["horizon"])] += 1
                if s["status"] == "finite-witness":
                    assert s["horizon"] >= 7
                if s["status"] == "censored":
                    censor_stage[s.get("stage", "unknown")] += 1
                    censor_reason[s.get("reason", "unknown")] += 1
                    censor_horizon[str(s["horizon"])] += 1
    assert sum(statuses.values()) == EXPECTED_SURVIVORS
    assert sum(len(x["statuses"]) for x in sentinels) == 12

    fw = statuses.get("finite-witness", 0)
    fc = statuses.get("finite-sofic-closure", 0)
    unresolved = statuses.get("unresolved-through-12", 0)
    censored = statuses.get("censored", 0)
    resolved = fw + fc
    assert resolved + unresolved + censored == EXPECTED_SURVIVORS

    def hypothesis_status(success):
        if success:
            return "pass"
        if censored:
            return "inconclusive-due-to-censoring"
        return "fail"

    out = {
        "ok": True,
        "experiment": "sofic-defect-orbit-lazy-recovery",
        "rules": 256,
        "hmax": 12,
        "research034_survivors": survivors,
        "survivor_seed_languages": sum(r["survivor_seed_languages"] for r in rows),
        "status_counts": dict(sorted(statuses.items())),
        "finite_witness_resolutions": fw,
        "finite_sofic_closure_resolutions": fc,
        "resolved_total": resolved,
        "unresolved_through_12": unresolved,
        "censored": censored,
        "resolved_fraction": resolved / survivors,
        "primary_hypotheses": {
            "exact_sofic_adds_information_beyond_width3": hypothesis_status(resolved > 0),
            "finite_window_danger_sometimes_spurious": hypothesis_status(fc > 0),
        },
        "status_by_wolfram_class": {k: dict(sorted(v.items())) for k, v in sorted(status_classes.items())},
        "status_by_horizon": {k: dict(sorted(v.items(), key=lambda kv: int(kv[0]))) for k, v in sorted(status_horizons.items())},
        "censoring_by_stage": dict(sorted(censor_stage.items())),
        "censoring_by_reason": dict(sorted(censor_reason.items())),
        "censoring_by_horizon": dict(sorted(censor_horizon.items(), key=lambda kv: int(kv[0]))),
        "first_finite_witness": canonical(rows, "finite-witness"),
        "first_finite_sofic_closure": canonical(rows, "finite-sofic-closure"),
        "first_unresolved": canonical(rows, "unresolved-through-12"),
        "first_censored": canonical(rows, "censored"),
        "rule122_161_sentinels": sentinels,
        "primary_censoring_baseline": {"censored": 170, "resolved": 0},
        "resource_limits": shards[0]["resource_limits"],
        "source_hashes": shards[0]["source_hashes"],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
