"""Aggregate the frozen phase-splice source-recoder primary census."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

EXPECTED_RULES = (122, 154, 161, 164, 166, 180, 210, 218)
EXPECTED_SEEDS = 22
EXPECTED_QUESTIONS = 170
EXPECTED_CLASSES = {"II": 158, "III": 12}
EXPECTED_POLICIES = ["LR", "RL"]
PROTOCOL = "docs/research/protocols/phase-splice-source-recoder-20260909.md"
ADDENDUM = "docs/research/protocols/phase-splice-source-recoder-resource-addendum-20260909.md"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact_candidate(rec):
    out = {
        "t": rec["t"], "k": rec["k"], "j": rec["j"],
        "delta": rec["delta"], "policy": rec["policy"],
        "status": rec["status"],
        "max_mdd_nodes": rec.get("max_mdd_nodes", 0),
        "elapsed_seconds": rec.get("elapsed_seconds"),
    }
    for key in ("failing_position", "reason", "position", "node_budget"):
        if key in rec:
            out[key] = rec[key]
    if rec.get("counterexample") is not None:
        out["counterexample"] = rec["counterexample"]
    return out


def compact_certificate(rule, wclass, lang):
    rec = lang.get("first_certificate")
    if rec is None:
        return None
    return {
        "rule": rule,
        "wclass": wclass,
        "pair_index": lang["pair_index"],
        "pair": lang["pair"],
        "seed_symbol": lang["seed_symbol"],
        "incoming_target_ids": lang["incoming_target_ids"],
        "t": rec["t"], "k": rec["k"], "j": rec["j"],
        "delta": rec["delta"], "policy": rec["policy"],
        "max_mdd_nodes": rec.get("max_mdd_nodes", 0),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", type=Path, required=True)
    ap.add_argument("--controls", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    controls = json.loads(args.controls.read_text())
    assert controls["experiment"] == "phase-splice-source-recoder-controls"
    assert controls["controls"]["ok"] is True
    assert controls["controls"]["rule5"]["status"] == "pass"
    assert controls["controls"]["rule35"]["all_fail"] is True
    assert controls["controls"]["rule35"]["fresh_candidates_t_le_3"] == 22

    shards = [json.loads(p.read_text()) for p in sorted(args.input_dir.rglob("*.json"))]
    shards = [x for x in shards if x.get("experiment") == "phase-splice-source-recoder"]
    if not shards:
        raise SystemExit("no phase-splice shards")
    assert len(shards) == len(EXPECTED_RULES), len(shards)
    assert {x["schema"] for x in shards} == {1}
    assert {x["tmax"] for x in shards} == {6}
    assert {tuple(x["fresh_policies"]) for x in shards} == {tuple(EXPECTED_POLICIES)}
    assert {x["resource_limits"]["mdd_nodes_per_position"] for x in shards} == {5_000_000}
    assert {x["resource_limits"]["seed_wall_seconds"] for x in shards} == {1200}
    hashes = {json.dumps(x["source_hashes"], sort_keys=True) for x in shards}
    assert len(hashes) == 1
    assert json.loads(next(iter(hashes))) == controls["source_hashes"]

    coverage = []
    rows = []
    for shard in shards:
        coverage.extend(range(shard["rule_start"], shard["rule_end"]))
        rows.extend(shard["rows"])
    assert sorted(coverage) == list(EXPECTED_RULES), coverage
    assert len(set(coverage)) == len(EXPECTED_RULES)
    rows.sort(key=lambda r: r["rule"])
    assert [r["rule"] for r in rows] == list(EXPECTED_RULES)

    languages = []
    for row in rows:
        for lang in row["languages"]:
            languages.append({"rule": row["rule"], "wclass": row["wclass"], **lang})
    languages.sort(key=lambda x: (x["rule"], x["pair_index"]))

    assert len(languages) == EXPECTED_SEEDS, len(languages)
    questions = sum(len(x["incoming_target_ids"]) for x in languages)
    assert questions == EXPECTED_QUESTIONS, questions
    class_counts = Counter()
    for lang in languages:
        class_counts[lang["wclass"]] += len(lang["incoming_target_ids"])
    assert dict(sorted(class_counts.items())) == EXPECTED_CLASSES, class_counts

    statuses = Counter(x["status"] for x in languages)
    certified = [x for x in languages if x["status"] == "phase-splice-certified"]
    censored = [x for x in languages if x["status"] == "censored"]
    unresolved = [x for x in languages if x["status"] == "no-phase-splice-through-6"]
    assert len(certified) + len(censored) + len(unresolved) == EXPECTED_SEEDS

    resolved_questions = sum(len(x["incoming_target_ids"]) for x in certified)
    censored_questions = sum(len(x["incoming_target_ids"]) for x in censored)
    unresolved_questions = sum(len(x["incoming_target_ids"]) for x in unresolved)
    assert resolved_questions + censored_questions + unresolved_questions == EXPECTED_QUESTIONS

    if resolved_questions:
        hypothesis = "pass"
    elif censored:
        hypothesis = "inconclusive-due-to-censoring"
    else:
        hypothesis = "fail"

    cert_params = Counter()
    for lang in certified:
        c = lang["first_certificate"]
        cert_params[f"t{c['t']}-k{c['k']}-j{c['j']}-d{c['delta']}-{c['policy']}"] += 1

    max_nodes = max((x["max_mdd_nodes"] for x in languages), default=0)
    first_cert = None
    if certified:
        first = min(certified, key=lambda x: (x["rule"], x["pair_index"]))
        first_cert = compact_certificate(first["rule"], first["wclass"], first)

    sentinels = []
    for lang in languages:
        if lang["is_r122_161_sentinel"]:
            sentinels.append({
                "rule": lang["rule"], "wclass": lang["wclass"],
                "pair": lang["pair"], "seed_symbol": lang["seed_symbol"],
                "incoming_target_ids": lang["incoming_target_ids"],
                "status": lang["status"],
                "first_certificate": compact_certificate(lang["rule"], lang["wclass"], lang),
                "first_censoring": lang.get("first_censoring"),
                "max_mdd_nodes": lang["max_mdd_nodes"],
                "elapsed_seconds": lang["elapsed_seconds"],
            })
    assert sum(len(x["incoming_target_ids"]) for x in sentinels) == 12

    summaries = []
    for lang in languages:
        summaries.append({
            "rule": lang["rule"], "wclass": lang["wclass"],
            "pair_index": lang["pair_index"], "pair": lang["pair"],
            "seed_symbol": lang["seed_symbol"],
            "incoming_target_ids": lang["incoming_target_ids"],
            "status": lang["status"],
            "tested_candidates": lang["tested_candidates"],
            "frozen_family_candidates": lang["frozen_family_candidates"],
            "candidate_status_counts": lang["candidate_status_counts"],
            "first_certificate": compact_certificate(lang["rule"], lang["wclass"], lang),
            "first_censoring": lang.get("first_censoring"),
            "max_mdd_nodes": lang["max_mdd_nodes"],
            "elapsed_seconds": lang["elapsed_seconds"],
            "tested": [compact_candidate(x) for x in lang["tested"]],
        })

    out = {
        "ok": True,
        "experiment": "phase-splice-source-recoder",
        "working_identity": "phase-splice-source-recoder",
        "public_note_number": None,
        "primary_rules": list(EXPECTED_RULES),
        "seed_languages": EXPECTED_SEEDS,
        "target_questions": EXPECTED_QUESTIONS,
        "target_questions_by_wolfram_class": EXPECTED_CLASSES,
        "fresh_policies": EXPECTED_POLICIES,
        "seed_status_counts": dict(sorted(statuses.items())),
        "certified_seed_languages": len(certified),
        "unresolved_seed_languages": len(unresolved),
        "censored_seed_languages": len(censored),
        "exact_permanence_resolutions": resolved_questions,
        "unresolved_target_questions": unresolved_questions,
        "censored_target_questions": censored_questions,
        "primary_hypothesis": hypothesis,
        "first_canonical_certificate": first_cert,
        "certificate_parameter_counts": dict(sorted(cert_params.items())),
        "maximum_mdd_nodes_observed": max_nodes,
        "rule122_161_sentinels": sentinels,
        "language_summaries": summaries,
        "resource_limits": {"mdd_nodes_per_position": 5_000_000, "seed_wall_seconds": 1200, "tmax": 6},
        "controls": controls["controls"],
        "source_hashes": shards[0]["source_hashes"],
        "aggregate_source_hashes": {
            "scripts/aggregate_phase_splice_source_recoder.py": file_hash(Path(__file__)),
            PROTOCOL: file_hash(Path(PROTOCOL)),
            ADDENDUM: file_hash(Path(ADDENDUM)),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "seed_status_counts": out["seed_status_counts"],
        "exact_permanence_resolutions": resolved_questions,
        "unresolved_target_questions": unresolved_questions,
        "censored_target_questions": censored_questions,
        "primary_hypothesis": hypothesis,
        "first_canonical_certificate": first_cert,
        "maximum_mdd_nodes_observed": max_nodes,
    }, indent=2))


if __name__ == "__main__":
    main()
