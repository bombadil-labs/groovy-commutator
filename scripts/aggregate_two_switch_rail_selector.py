"""Aggregate the frozen two-switch rail-selector census and write compact companions."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", type=Path, required=True)
    ap.add_argument("--controls", type=Path, required=True)
    ap.add_argument("--full-output", type=Path, required=True)
    ap.add_argument("--summary-output", type=Path, required=True)
    ap.add_argument("--markdown-output", type=Path, required=True)
    args = ap.parse_args()

    controls = json.loads(args.controls.read_text())
    assert controls["controls"]["ok"] is True
    assert controls["controls"]["rule204"]["status"] == "pass"
    assert controls["controls"]["rule35"]["all_fail"] is True
    assert controls["controls"]["rule35"]["fresh_candidates_t_le_3"] == 62

    seeds = [json.loads(p.read_text()) for p in sorted(args.input_dir.glob("*.json"))]
    assert len(seeds) == 22, len(seeds)
    rows = [x["result"] for x in seeds]
    rows.sort(key=lambda r: r["seed_index"])
    assert [r["seed_index"] for r in rows] == list(range(22))
    assert sum(len(r["incoming_target_ids"]) for r in rows) == 170
    assert {x["family_size"] for x in seeds} == {2788}
    hashes = {json.dumps(x["source_hashes"], sort_keys=True) for x in seeds}
    assert len(hashes) == 1
    source_hashes = json.loads(next(iter(hashes)))
    assert source_hashes == controls["source_hashes"]

    statuses = Counter(r["status"] for r in rows)
    certified = [r for r in rows if r["status"] == "two-switch-certified"]
    negative = [r for r in rows if r["status"] == "no-two-switch-through-6"]
    censored = [r for r in rows if r["status"] == "censored"]
    resolved_q = sum(len(r["incoming_target_ids"]) for r in certified)
    negative_q = sum(len(r["incoming_target_ids"]) for r in negative)
    censored_q = sum(len(r["incoming_target_ids"]) for r in censored)
    assert resolved_q + negative_q + censored_q == 170
    outcome = "positive-needs-z3-audit" if certified else (
        "inconclusive-due-to-censoring" if censored else "complete-exact-negative"
    )

    first = min(certified, key=lambda r: r["seed_index"]) if certified else None
    first_cert = None if first is None else {
        "seed_index": first["seed_index"], "rule": first["rule"], "pair": first["pair"],
        **{k: first["first_certificate"][k] for k in ("t", "k", "j", "delta", "u", "v", "orientation")},
    }
    max_vars = max(r["max_cnf_variables"] for r in rows)
    max_clauses = max(r["max_cnf_clauses"] for r in rows)

    full = {
        "ok": True,
        "experiment": "two-switch-rail-selector",
        "working_identity": "two-switch-rail-selector",
        "public_note_number": None,
        "solver": "Minisat22 via python-sat",
        "family_candidates_per_seed": 2788,
        "seed_languages": 22,
        "target_questions": 170,
        "seed_status_counts": dict(sorted(statuses.items())),
        "certified_seed_languages": len(certified),
        "exact_negative_seed_languages": len(negative),
        "censored_seed_languages": len(censored),
        "exact_permanence_resolutions": resolved_q,
        "negative_target_questions": negative_q,
        "censored_target_questions": censored_q,
        "primary_outcome": outcome,
        "first_canonical_certificate": first_cert,
        "maximum_cnf_variables": max_vars,
        "maximum_cnf_clauses": max_clauses,
        "resource_limits": {"seed_wall_seconds": 1200, "tmax": 6, "max_cnf_variables": 1314, "max_cnf_clauses": 9943},
        "controls": controls["controls"],
        "source_hashes": source_hashes,
        "seed_results": rows,
    }
    args.full_output.parent.mkdir(parents=True, exist_ok=True)
    args.full_output.write_text(json.dumps(full, separators=(",", ":")) + "\n")
    raw = args.full_output.read_bytes()

    summary_keys = (
        "ok", "experiment", "working_identity", "public_note_number", "solver",
        "family_candidates_per_seed", "seed_languages", "target_questions", "seed_status_counts",
        "certified_seed_languages", "exact_negative_seed_languages", "censored_seed_languages",
        "exact_permanence_resolutions", "negative_target_questions", "censored_target_questions",
        "primary_outcome", "first_canonical_certificate", "maximum_cnf_variables",
        "maximum_cnf_clauses", "resource_limits", "controls", "source_hashes",
    )
    summary = {k: full[k] for k in summary_keys}
    summary["full_result"] = str(args.full_output)
    summary["full_result_sha256"] = hashlib.sha256(raw).hexdigest()
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(json.dumps(summary, indent=2) + "\n")

    md = f"""# Two-switch rail-selector census — compact report

## Primary outcome

- Outcome: **{outcome}**
- Fresh selector family: **2,788 LRL/RLR island candidates per seed** through `t<=6`
- Seed languages: **22**
- Target questions: **170**
- Seed status counts: `{dict(sorted(statuses.items()))}`
- Exact permanence resolutions: **{resolved_q}**
- Exact-negative target questions: **{negative_q}**
- Censored target questions: **{censored_q}**
- First canonical certificate: `{first_cert}`

## Symbolic cost

- Maximum CNF variables: **{max_vars}** / 1,314 structural maximum
- Maximum CNF clauses: **{max_clauses}** / 9,943 structural maximum
- Per-seed wall: **1,200 seconds**, enforced inside each SAT solve

## Controls

- Rule 204 two-switch positive control: **pass**
- Rule 35 fresh two-switch candidates through t=3: **62/62 fail with scalar replay**

## Provenance

- Full durable audit: `{args.full_output}`
- Full result SHA-256: `{summary['full_result_sha256']}`
- Parent protocol: `docs/research/protocols/two-switch-rail-selector-20260910.md`
- Wall-enforcement correction: `docs/research/protocols/two-switch-rail-selector-wall-enforcement-20260910.md`
"""
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.write_text(md)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
