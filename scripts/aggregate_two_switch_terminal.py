"""Terminal aggregate for the frozen two-switch census with explicit infrastructure censoring."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import experiment_two_switch_rail_selector_sat as base  # noqa:E402

TERMINAL_PROTOCOL = ROOT / "docs/research/protocols/two-switch-rail-selector-terminal-censoring-20260910.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def infra_row(seed_index: int):
    row = base.load_domain()[seed_index]
    return {
        **row,
        "seed_index": seed_index,
        "status": "infrastructure-censored",
        "tested_candidates": None,
        "frozen_family_candidates": base.FAMILY_SIZE,
        "first_certificate": None,
        "max_cnf_variables": None,
        "max_cnf_clauses": None,
        "solver_seconds": None,
        "elapsed_seconds": None,
        "tested": [],
        "censoring_reason": "worker-exited-without-valid-artifact",
    }


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

    got = {}
    invalid = []
    for p in sorted(args.input_dir.glob("*.json")):
        try:
            x = json.loads(p.read_text())
            r = x["result"]
            idx = int(r["seed_index"])
            if idx in got:
                raise ValueError(f"duplicate seed {idx}")
            got[idx] = r
        except Exception as exc:
            invalid.append({"path": str(p), "error": repr(exc)})

    rows = [got.get(i, infra_row(i)) for i in range(22)]
    assert [r["seed_index"] for r in rows] == list(range(22))
    assert sum(len(r["incoming_target_ids"]) for r in rows) == 170

    statuses = Counter(r["status"] for r in rows)
    certified = [r for r in rows if r["status"] == "two-switch-certified"]
    negative = [r for r in rows if r["status"] == "no-two-switch-through-6"]
    scientific_censored = [r for r in rows if r["status"] == "censored"]
    infra_censored = [r for r in rows if r["status"] == "infrastructure-censored"]
    other = [r for r in rows if r["status"] not in {"two-switch-certified","no-two-switch-through-6","censored","infrastructure-censored"}]
    assert not other, [r["status"] for r in other]

    q = lambda xs: sum(len(r["incoming_target_ids"]) for r in xs)
    resolved_q, negative_q = q(certified), q(negative)
    scientific_censored_q, infra_censored_q = q(scientific_censored), q(infra_censored)
    assert resolved_q + negative_q + scientific_censored_q + infra_censored_q == 170

    outcome = "positive-needs-independent-audit" if certified else (
        "inconclusive-due-to-censoring" if scientific_censored or infra_censored else "complete-exact-negative"
    )
    first = min(certified, key=lambda r: r["seed_index"]) if certified else None
    first_cert = None if first is None else {
        "seed_index": first["seed_index"], "rule": first["rule"], "pair": first["pair"],
        **{k: first["first_certificate"][k] for k in ("t","k","j","delta","u","v","orientation")},
    }

    numeric_vars = [r["max_cnf_variables"] for r in rows if isinstance(r.get("max_cnf_variables"), int)]
    numeric_clauses = [r["max_cnf_clauses"] for r in rows if isinstance(r.get("max_cnf_clauses"), int)]
    full = {
        "ok": True,
        "experiment": "two-switch-rail-selector-terminal",
        "working_identity": "two-switch-rail-selector",
        "public_note_number": None,
        "solver": "Minisat22 via python-sat",
        "family_candidates_per_seed": 2788,
        "seed_languages": 22,
        "target_questions": 170,
        "seed_status_counts": dict(sorted(statuses.items())),
        "certified_seed_languages": len(certified),
        "exact_negative_seed_languages": len(negative),
        "scientific_censored_seed_languages": len(scientific_censored),
        "infrastructure_censored_seed_languages": len(infra_censored),
        "exact_permanence_resolutions": resolved_q,
        "negative_target_questions": negative_q,
        "scientific_censored_target_questions": scientific_censored_q,
        "infrastructure_censored_target_questions": infra_censored_q,
        "primary_outcome": outcome,
        "first_canonical_certificate": first_cert,
        "maximum_cnf_variables_observed": max(numeric_vars, default=None),
        "maximum_cnf_clauses_observed": max(numeric_clauses, default=None),
        "resource_limits": {"seed_wall_seconds": 1200, "tmax": 6, "max_cnf_variables": 1314, "max_cnf_clauses": 9943},
        "controls": controls["controls"],
        "invalid_artifacts": invalid,
        "terminal_protocol_sha256": sha256(TERMINAL_PROTOCOL),
        "seed_results": rows,
    }
    args.full_output.parent.mkdir(parents=True, exist_ok=True)
    args.full_output.write_text(json.dumps(full, separators=(",", ":")) + "\n")
    raw = args.full_output.read_bytes()

    summary = {k: v for k, v in full.items() if k not in {"seed_results"}}
    summary["full_result"] = str(args.full_output)
    summary["full_result_sha256"] = hashlib.sha256(raw).hexdigest()
    summary["infrastructure_censored_seeds"] = [
        {"seed_index": r["seed_index"], "rule": r["rule"], "pair": r["pair"], "incoming_target_ids": r["incoming_target_ids"]}
        for r in infra_censored
    ]
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(json.dumps(summary, indent=2) + "\n")

    md = f"""# Two-switch rail-selector — terminal compact report

## Outcome

- Status: **{outcome}**
- Fresh family: **2,788 LRL/RLR candidates per seed**, `t<=6`
- Seed languages: **22**; target questions: **170**
- Seed statuses: `{dict(sorted(statuses.items()))}`
- Exact permanence resolutions: **{resolved_q}**
- Exact-negative questions: **{negative_q}**
- Scientific-censored questions: **{scientific_censored_q}**
- Infrastructure-censored questions: **{infra_censored_q}**
- First certificate: `{first_cert}`

## Interpretation

`infrastructure-censored` means a worker exited without a valid artifact; it is not evidence for or against the selector family. This terminal run ends backend/watchdog engineering for the hand-designed two-switch family. The next and final substantive checkpoint is bounded finite-state source-recoder synthesis.

## Provenance

- Full audit: `{args.full_output}`
- Full SHA-256: `{summary['full_result_sha256']}`
- Terminal protocol: `docs/research/protocols/two-switch-rail-selector-terminal-censoring-20260910.md`
"""
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.write_text(md)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
