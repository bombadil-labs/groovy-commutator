"""Aggregate sharded Research034 width-3 reachable-language results."""
from __future__ import annotations
import argparse, json
from collections import Counter
from pathlib import Path

EXPECTED_R032_RESIDUAL = 5360
EXPECTED_R033_CERTS = 5132
EXPECTED_R033_SURVIVORS = 228
EXPECTED_R033_SURVIVOR_CLASSES = {"II": 216, "III": 12}


def first_case(rows, pred):
    for r in rows:
        for l in r["languages"]:
            if pred(r, l):
                return {"rule": r["rule"], "wclass": r["wclass"], **l}
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    shards = [json.loads(p.read_text()) for p in sorted(args.input_dir.rglob("*.json"))]
    shards = [x for x in shards if x.get("experiment") == "window3-reachable-language"]
    if not shards:
        raise SystemExit("no Research034 shards")
    assert {x["schema"] for x in shards} == {1}
    assert {x["window_width"] for x in shards} == {3}
    assert {x["block_size"] for x in shards} == {3}
    assert {x["cadence"] for x in shards} == {3}
    assert len({json.dumps(x["source_hashes"], sort_keys=True) for x in shards}) == 1

    coverage = []
    rows = []
    for x in shards:
        coverage.extend(range(x["rule_start"], x["rule_end"]))
        rows.extend(x["rows"])
    assert sorted(coverage) == list(range(256)) and len(set(coverage)) == 256
    rows.sort(key=lambda r: r["rule"])
    assert [r["rule"] for r in rows] == list(range(256))

    r032 = sum(r["research032_noncongruence_residual"] for r in rows)
    r033cert = sum(r["research033_edge_certificates"] for r in rows)
    r033left = sum(r["research033_edge_survivors"] for r in rows)
    assert (r032, r033cert, r033left) == (
        EXPECTED_R032_RESIDUAL,
        EXPECTED_R033_CERTS,
        EXPECTED_R033_SURVIVORS,
    )

    r033classes = Counter()
    for r in rows:
        n = r["research033_edge_survivors"]
        if n:
            r033classes[r["wclass"]] += n
    assert dict(sorted(r033classes.items())) == EXPECTED_R033_SURVIVOR_CLASSES

    mechanism = first_case(
        rows,
        lambda r, l: r["rule"] == 5 and l["pair"] == "0-2" and 102 in l["incoming_target_ids"],
    )
    assert mechanism is not None
    assert mechanism["edge_count"] == 230 and mechanism["edge_rounds"] == 4

    sentinels = []
    for r in rows:
        if r["rule"] not in (122, 161):
            continue
        for l in r["languages"]:
            if l["is_r122_161_sentinel"]:
                sentinels.append({"rule": r["rule"], "wclass": r["wclass"], **l})
    sentinel_questions = sum(len(x["incoming_target_ids"]) for x in sentinels)
    assert sentinel_questions == 12

    certs = sum(r["width3_certificates"] for r in rows)
    left = sum(r["remaining_after_width3"] for r in rows)
    assert certs + left == EXPECTED_R033_SURVIVORS

    certclass = Counter()
    leftclass = Counter()
    for r in rows:
        for l in r["languages"]:
            certclass[r["wclass"]] += len(l["width3_certified_target_ids"])
            leftclass[r["wclass"]] += len(l["width3_unresolved_target_ids"])

    first_cert = first_case(rows, lambda r, l: bool(l["width3_certified_target_ids"]))
    first_left = first_case(rows, lambda r, l: bool(l["width3_unresolved_target_ids"]))
    rule5_safe = 102 in mechanism["width3_certified_target_ids"]

    out = {
        "ok": True,
        "experiment": "window3-reachable-language",
        "rules": 256,
        "block_size": 3,
        "cadence": 3,
        "window_width": 3,
        "research032_noncongruence_residual": r032,
        "research033_edge_certificates": r033cert,
        "research033_edge_survivors": r033left,
        "survivor_seed_languages": sum(r["survivor_seed_languages"] for r in rows),
        "width3_certificates": certs,
        "remaining_after_width3": left,
        "resolved_fraction_of_r033_residual": certs / r033left,
        "remaining_fraction_of_r033_residual": left / r033left,
        "primary_hypotheses": {
            "width3_strictly_improves_on_edges": certs > 0,
            "rule5_splice_hypothesis": rule5_safe,
        },
        "certificates_by_wolfram_class": dict(sorted(certclass.items())),
        "remaining_by_wolfram_class": dict(sorted(leftclass.items())),
        "rule5_mechanism": mechanism,
        "first_width3_certificate": first_cert,
        "first_width3_unresolved": first_left,
        "rule122_161_sentinels": sentinels,
        "source_hashes": shards[0]["source_hashes"],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
