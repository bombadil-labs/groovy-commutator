"""Aggregate the frozen symbolic defect-normalization survivor census."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

EXPECTED_PRIMARY_RULES = (122, 154, 161, 164, 166, 180, 210, 218)
SOURCE_RULE_FAMILY = 256
EXPECTED_SEED_LANGUAGES = 22
EXPECTED_TARGET_QUESTIONS = 170
EXPECTED_TARGET_CLASSES = {"II": 158, "III": 12}
PROTOCOL = "docs/research/protocols/symbolic-defect-normalization-20260909.md"
DOMAIN_ADDENDUM = "docs/research/protocols/symbolic-defect-normalization-domain-20260909.md"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact_certificate(lang):
    cert = lang.get("first_certificate")
    if not cert:
        return None
    return {
        "rule": lang["rule"],
        "wclass": lang["wclass"],
        "pair_index": lang["pair_index"],
        "pair": lang["pair"],
        "seed_symbol": lang["seed_symbol"],
        "incoming_target_ids": lang["incoming_target_ids"],
        "t": cert["t"],
        "k": cert["k"],
        "j": cert["j"],
        "delta": cert["delta"],
        "rail": cert["rail"],
        "max_mdd_nodes": cert["max_mdd_nodes"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", type=Path, required=True)
    ap.add_argument("--controls", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    controls = json.loads(args.controls.read_text())
    assert controls["experiment"] == "symbolic-defect-normalization-controls"
    assert controls["controls"]["ok"] is True

    shards = [json.loads(p.read_text()) for p in sorted(args.input_dir.rglob("*.json"))]
    shards = [x for x in shards if x.get("experiment") == "symbolic-defect-normalization"]
    if not shards:
        raise SystemExit("no symbolic-defect-normalization shards")
    assert {x["schema"] for x in shards} == {1}
    assert {x["tmax"] for x in shards} == {6}
    assert {x["node_budget"] for x in shards} == {5_000_000}
    assert {x["seed_wall_seconds"] for x in shards} == {1200}
    assert len({json.dumps(x["source_hashes"], sort_keys=True) for x in shards}) == 1

    coverage = []
    rows = []
    for shard in shards:
        coverage.extend(range(shard["rule_start"], shard["rule_end"]))
        rows.extend(shard["rows"])
    assert sorted(coverage) == list(EXPECTED_PRIMARY_RULES) and len(set(coverage)) == len(EXPECTED_PRIMARY_RULES), coverage
    rows.sort(key=lambda r: r["rule"])
    assert [r["rule"] for r in rows] == list(EXPECTED_PRIMARY_RULES)

    langs = []
    for row in rows:
        for lang in row["languages"]:
            langs.append({"rule": row["rule"], "wclass": row["wclass"], **lang})
    langs.sort(key=lambda l: (l["rule"], l["pair_index"]))

    seed_languages = len(langs)
    target_questions = sum(len(l["incoming_target_ids"]) for l in langs)
    assert seed_languages == EXPECTED_SEED_LANGUAGES, seed_languages
    assert target_questions == EXPECTED_TARGET_QUESTIONS, target_questions

    target_classes = Counter()
    for lang in langs:
        target_classes[lang["wclass"]] += len(lang["incoming_target_ids"])
    assert dict(sorted(target_classes.items())) == EXPECTED_TARGET_CLASSES, target_classes

    statuses = Counter(l["status"] for l in langs)
    certified = [l for l in langs if l["status"] == "certified"]
    no_cert = [l for l in langs if l["status"] == "no-certificate-in-frozen-family"]
    censored = [l for l in langs if l["status"] == "censored"]
    resolved_targets = sum(len(l["incoming_target_ids"]) for l in certified)

    if resolved_targets:
        hypothesis = "pass"
    elif censored:
        hypothesis = "inconclusive-due-to-censoring"
    else:
        hypothesis = "fail"

    by_class = {}
    for status in sorted(statuses):
        c = Counter(l["wclass"] for l in langs if l["status"] == status)
        by_class[status] = dict(sorted(c.items()))

    target_by_class = Counter()
    for lang in certified:
        target_by_class[lang["wclass"]] += len(lang["incoming_target_ids"])

    cert_params = Counter()
    for lang in certified:
        c = lang["first_certificate"]
        cert_params[f"t{c['t']}-k{c['k']}-j{c['j']}-d{c['delta']}-{c['rail']}"] += 1

    first = compact_certificate(certified[0]) if certified else None
    sentinels = [
        {
            "rule": l["rule"],
            "wclass": l["wclass"],
            "pair": l["pair"],
            "seed_symbol": l["seed_symbol"],
            "incoming_target_ids": l["incoming_target_ids"],
            "status": l["status"],
            "first_certificate": compact_certificate(l),
            "first_censoring": l.get("first_censoring"),
            "max_mdd_nodes": l["max_mdd_nodes"],
            "elapsed_seconds": l["elapsed_seconds"],
        }
        for l in langs if l["is_r122_161_sentinel"]
    ]
    assert sum(len(x["incoming_target_ids"]) for x in sentinels) == 12

    max_nodes = max((l["max_mdd_nodes"] for l in langs), default=0)
    out = {
        "ok": True,
        "experiment": "symbolic-defect-normalization",
        "working_identity": "symbolic-defect-normalization",
        "public_note_number": None,
        "source_rule_family": SOURCE_RULE_FAMILY,
        "primary_rules": list(EXPECTED_PRIMARY_RULES),
        "seed_languages": seed_languages,
        "target_questions": target_questions,
        "target_questions_by_wolfram_class": dict(sorted(target_classes.items())),
        "seed_status_counts": dict(sorted(statuses.items())),
        "seed_status_by_wolfram_class": by_class,
        "certified_seed_languages": len(certified),
        "no_certificate_seed_languages": len(no_cert),
        "censored_seed_languages": len(censored),
        "exact_permanence_resolutions": resolved_targets,
        "resolved_targets_by_wolfram_class": dict(sorted(target_by_class.items())),
        "primary_hypothesis": hypothesis,
        "first_canonical_certificate": first,
        "certificate_parameter_counts": dict(sorted(cert_params.items())),
        "rule122_161_sentinels": sentinels,
        "language_summaries": [
            {
                "rule": l["rule"], "wclass": l["wclass"], "pair_index": l["pair_index"],
                "pair": l["pair"], "seed_symbol": l["seed_symbol"],
                "incoming_target_ids": l["incoming_target_ids"], "status": l["status"],
                "candidate_status_counts": l["candidate_status_counts"],
                "tested_candidates": l["tested_candidates"],
                "frozen_family_candidates": l["frozen_family_candidates"],
                "first_certificate": compact_certificate(l),
                "first_censoring": l.get("first_censoring"),
                "max_mdd_nodes": l["max_mdd_nodes"], "elapsed_seconds": l["elapsed_seconds"],
            }
            for l in langs
        ],
        "maximum_mdd_nodes_observed": max_nodes,
        "resource_limits": {"mdd_nodes_per_position": 5_000_000, "seed_wall_seconds": 1200, "tmax": 6},
        "controls": controls["controls"],
        "source_hashes": shards[0]["source_hashes"],
        "aggregate_source_hashes": {
            "scripts/aggregate_symbolic_defect_normalization.py": file_hash(Path(__file__)),
            PROTOCOL: file_hash(Path(PROTOCOL)),
            DOMAIN_ADDENDUM: file_hash(Path(DOMAIN_ADDENDUM)),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "seed_status_counts": out["seed_status_counts"],
        "exact_permanence_resolutions": resolved_targets,
        "primary_hypothesis": hypothesis,
        "first_canonical_certificate": first,
        "maximum_mdd_nodes_observed": max_nodes,
    }, indent=2))


if __name__ == "__main__":
    main()
