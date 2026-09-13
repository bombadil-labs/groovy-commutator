"""Aggregate the terminal bounded source-recoder synthesis experiment."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import experiment_bounded_source_recoder_synthesis as exp  # noqa:E402


def infra_row(seed_index: int):
    row = exp.load_domain()[seed_index]
    return {
        **row, "seed_index": seed_index, "status": "infrastructure-censored",
        "censoring_reason": "worker-exited-without-valid-artifact", "first_certificate": None,
        "structures_attempted": None, "exact_negative_structures": None,
        "censored_structures": None, "max_state_completed": None,
        "elapsed_seconds": None, "structures": [],
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
    assert controls["controls"]["rule5"]["status"] == "pass"
    assert controls["controls"]["rule35"]["status"] == "pass"

    got, invalid, source_hashes = {}, [], None
    for p in sorted(args.input_dir.glob("*.json")):
        try:
            x = json.loads(p.read_text())
            r = x["result"]
            idx = int(r["seed_index"])
            if idx in got:
                raise ValueError(f"duplicate seed {idx}")
            if source_hashes is None:
                source_hashes = x["source_hashes"]
            elif x["source_hashes"] != source_hashes:
                raise ValueError("source-hash mismatch")
            got[idx] = r
        except Exception as exc:
            invalid.append({"path": str(p), "error": repr(exc)})
    rows = [got.get(i, infra_row(i)) for i in range(22)]
    assert [r["seed_index"] for r in rows] == list(range(22))
    assert sum(len(r["incoming_target_ids"]) for r in rows) == 170

    statuses = Counter(r["status"] for r in rows)
    certified = [r for r in rows if r["status"] == "bounded-recoder-certified"]
    negative = [r for r in rows if r["status"] == "no-bounded-recoder-through-4"]
    censored = [r for r in rows if r["status"] == "censored"]
    infra = [r for r in rows if r["status"] == "infrastructure-censored"]
    allowed = {"bounded-recoder-certified", "no-bounded-recoder-through-4", "censored", "infrastructure-censored"}
    assert all(r["status"] in allowed for r in rows)
    q = lambda xs: sum(len(r["incoming_target_ids"]) for r in xs)
    resolved_q, negative_q, censored_q, infra_q = map(q, (certified, negative, censored, infra))
    assert resolved_q + negative_q + censored_q + infra_q == 170
    outcome = "positive-needs-independent-audit" if certified else (
        "complete-exact-bounded-negative" if len(negative) == 22 else "terminal-inconclusive-due-to-censoring")
    first = min(certified, key=lambda r: r["seed_index"]) if certified else None
    first_cert = None
    if first is not None:
        c = first["first_certificate"]
        first_cert = {k: c[k] for k in ("m", "t", "k", "j", "delta", "iterations", "counterexamples")}
        first_cert.update({"seed_index": first["seed_index"], "rule": first["rule"], "pair": first["pair"]})
    state_completed = Counter(str(r["max_state_completed"]) for r in rows if isinstance(r.get("max_state_completed"), int))
    structures_attempted = [r["structures_attempted"] for r in rows if isinstance(r.get("structures_attempted"), int)]

    full = {
        "ok": True, "experiment": "bounded-source-recoder-synthesis",
        "working_identity": "bounded-source-recoder-synthesis", "public_note_number": None,
        "program_role": "final-substantive-checkpoint",
        "solver": "Minisat22 CEGIS over manual fine-ECA CNF",
        "max_states": exp.MAX_STATES, "max_horizon": exp.TMAX,
        "seed_languages": 22, "target_questions": 170,
        "seed_status_counts": dict(sorted(statuses.items())),
        "certified_seed_languages": len(certified), "exact_negative_seed_languages": len(negative),
        "scientific_censored_seed_languages": len(censored), "infrastructure_censored_seed_languages": len(infra),
        "exact_permanence_resolutions": resolved_q, "exact_negative_target_questions": negative_q,
        "scientific_censored_target_questions": censored_q, "infrastructure_censored_target_questions": infra_q,
        "primary_outcome": outcome, "first_canonical_certificate": first_cert,
        "max_state_completed_distribution": dict(sorted(state_completed.items())),
        "max_structures_attempted": max(structures_attempted, default=None),
        "resource_limits": {"seed_wall_seconds": exp.SEED_WALL_SECONDS,
                            "max_cegis_counterexamples_per_structure": exp.MAX_CEGIS_COUNTEREXAMPLES,
                            "max_synthesis_variables": exp.MAX_SYNTH_VARS, "max_synthesis_clauses": exp.MAX_SYNTH_CLAUSES,
                            "max_verification_variables": exp.MAX_VERIFY_VARS, "max_verification_clauses": exp.MAX_VERIFY_CLAUSES},
        "controls": controls["controls"], "source_hashes": source_hashes or controls["source_hashes"],
        "invalid_artifacts": invalid, "seed_results": rows,
    }
    args.full_output.parent.mkdir(parents=True, exist_ok=True)
    args.full_output.write_text(json.dumps(full, separators=(",", ":")) + "\n")
    raw = args.full_output.read_bytes()
    summary = {k: v for k, v in full.items() if k != "seed_results"}
    summary["full_result"] = str(args.full_output)
    summary["full_result_sha256"] = hashlib.sha256(raw).hexdigest()
    summary["censored_seeds"] = [{"seed_index": r["seed_index"], "rule": r["rule"], "pair": r["pair"],
                                  "status": r["status"], "reason": r.get("censoring_reason"),
                                  "incoming_target_ids": r["incoming_target_ids"]} for r in censored + infra]
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(json.dumps(summary, indent=2) + "\n")
    md = f"""# Bounded adaptive source-recoder synthesis — compact report

## Final checkpoint outcome

- Outcome: **{outcome}**
- Machine class: deterministic adaptive rail selector with at most **4 proof states**
- Search horizon: `t<=6`
- Seed languages: **22**; target questions: **170**
- Seed statuses: `{dict(sorted(statuses.items()))}`
- Exact permanence resolutions: **{resolved_q}**
- Exact bounded-negative questions: **{negative_q}**
- Scientific-censored questions: **{censored_q}**
- Infrastructure-censored questions: **{infra_q}**
- First canonical certificate: `{first_cert}`
- Completed-state distribution: `{dict(sorted(state_completed.items()))}`

## Interpretation

This is the final new source-recoder family in the current Dynamics of Erased Distinctions program. Exact negatives apply only to the frozen `m<=4`, adaptive rail-selection class through `t<=6`. Censoring remains representational/computational evidence only. Regardless of outcome, the next step is the program-level synthesis and terminus note, not a larger selector family.

## Controls

- Rule 5 positive synthesis control: **pass**
- Rule 35 bounded negative synthesis control: **pass**

## Provenance

- Full durable audit: `{args.full_output}`
- Full SHA-256: `{summary['full_result_sha256']}`
- Frozen protocol: `docs/research/protocols/bounded-source-recoder-synthesis-20260910.md`
"""
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.write_text(md)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
