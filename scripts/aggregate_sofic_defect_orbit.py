"""Aggregate sharded Note 036 / sofic-defect-orbit results."""
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
    ap.add_argument("--controls", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    control = json.loads(args.controls.read_text())
    assert control["experiment"] == "sofic-defect-orbit-controls"
    assert control["controls"]["ok"] is True
    c35 = next(c for c in control["controls"]["cases"] if c["rule"] == 35)
    c5 = next(c for c in control["controls"]["cases"] if c["rule"] == 5)
    assert c35["first_visible"] == 3
    assert c5["first_visible"] is None

    shards = [json.loads(p.read_text()) for p in sorted(args.input_dir.rglob("*.json"))]
    shards = [x for x in shards if x.get("experiment") == "sofic-defect-orbit"]
    if not shards:
        raise SystemExit("no sofic-defect-orbit shards")
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
    assert survivors == EXPECTED_SURVIVORS, survivors
    classes = Counter()
    for r in rows:
        if r["research034_survivors"]:
            classes[r["wclass"]] += r["research034_survivors"]
    assert dict(sorted(classes.items())) == EXPECTED_CLASSES, classes

    statuses = Counter()
    status_classes = {}
    horizon_counts = {}
    censor_reasons = Counter()
    censor_horizons = Counter()
    censor_classes = Counter()
    sentinel = []
    for r in rows:
        for lang in r["languages"]:
            if lang["is_r122_161_sentinel"]:
                sentinel.append({"rule": r["rule"], "wclass": r["wclass"], **lang})
            for s in lang["statuses"]:
                statuses[s["status"]] += 1
                status_classes.setdefault(s["status"], Counter())[r["wclass"]] += 1
                horizon_counts.setdefault(s["status"], Counter())[str(s["horizon"])] += 1
                if s["status"] == "finite-witness":
                    assert s["horizon"] >= 7, (r["rule"], lang["pair"], s)
                elif s["status"] == "censored":
                    censor_reasons[s.get("reason", "unknown")] += 1
                    censor_horizons[str(s["horizon"])] += 1
                    censor_classes[r["wclass"]] += 1
    assert sum(statuses.values()) == EXPECTED_SURVIVORS
    sentinel_questions = sum(len(l["statuses"]) for l in sentinel)
    assert sentinel_questions == 12

    finite_witness = statuses.get("finite-witness", 0)
    finite_closure = statuses.get("finite-sofic-closure", 0)
    resolved = finite_witness + finite_closure
    unresolved = statuses.get("unresolved-through-12", 0)
    censored = statuses.get("censored", 0)
    assert resolved + unresolved + censored == EXPECTED_SURVIVORS

    def hypothesis_status(success):
        if success:
            return "pass"
        if censored:
            return "inconclusive-due-to-censoring"
        return "fail"

    out = {
        "ok": True,
        "experiment": "sofic-defect-orbit",
        "publication_identity": {"canonical_slug": "sofic-defect-orbit", "note_number": "036"},
        "rules": 256,
        "block_size": 3,
        "cadence": 3,
        "hmax": 12,
        "research034_survivors": survivors,
        "survivor_seed_languages": sum(r["survivor_seed_languages"] for r in rows),
        "status_counts": dict(sorted(statuses.items())),
        "resolved_total": resolved,
        "finite_witness_resolutions": finite_witness,
        "finite_sofic_closure_resolutions": finite_closure,
        "unresolved_through_12": unresolved,
        "censored": censored,
        "resolved_fraction": resolved / survivors,
        "primary_hypotheses": {
            "exact_sofic_adds_information_beyond_width3": hypothesis_status(resolved > 0),
            "finite_window_danger_sometimes_spurious": hypothesis_status(finite_closure > 0),
        },
        "censoring_by_reason": dict(sorted(censor_reasons.items())),
        "censoring_by_horizon": dict(sorted(censor_horizons.items(), key=lambda kv: int(kv[0]))),
        "censoring_by_wolfram_class": dict(sorted(censor_classes.items())),
        "status_by_wolfram_class": {k: dict(sorted(v.items())) for k, v in sorted(status_classes.items())},
        "status_by_horizon": {k: dict(sorted(v.items(), key=lambda kv: int(kv[0]))) for k, v in sorted(horizon_counts.items())},
        "first_finite_witness": canonical(rows, "finite-witness"),
        "first_finite_sofic_closure": canonical(rows, "finite-sofic-closure"),
        "first_unresolved": canonical(rows, "unresolved-through-12"),
        "first_censored": canonical(rows, "censored"),
        "rule122_161_sentinels": sentinel,
        "control_summary": {
            "rule35_first_visible": c35["first_visible"],
            "rule5_first_visible_through_3": c5["first_visible"],
            "rule5_control_closure_horizon": control["controls"]["rule5_control_closure_horizon"],
        },
        "resource_limits": shards[0]["resource_limits"],
        "source_hashes_scope": "Frozen prepublication source bytes used for this result; live files may differ by publication-identity-only normalization.",
        "source_hashes": shards[0]["source_hashes"],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
