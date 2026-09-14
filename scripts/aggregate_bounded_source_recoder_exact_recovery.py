#!/usr/bin/env python3
"""Aggregate resumable exact bounded-source-recoder recovery batches."""
from __future__ import annotations
import argparse, json
from collections import Counter
from pathlib import Path

RECOVERY_SEEDS = (1, 6, 11, 14, 16, 17, 18, 20)
FINAL = {"bounded-recoder-certified", "no-bounded-recoder-through-4"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", type=Path, required=True)
    ap.add_argument("--controls", type=Path, required=True)
    ap.add_argument("--checkpoint-dir", type=Path, required=True)
    ap.add_argument("--progress-output", type=Path, required=True)
    ap.add_argument("--markdown-output", type=Path, required=True)
    args = ap.parse_args()
    controls = json.loads(args.controls.read_text())
    assert controls["controls"]["ok"] is True
    paths = sorted(args.input_dir.glob("recovery-seed-*.json"))
    assert len(paths) == len(RECOVERY_SEEDS), [p.name for p in paths]
    wrappers = [json.loads(p.read_text()) for p in paths]
    rows = [x["result"] for x in wrappers]
    rows.sort(key=lambda r: int(r["seed_index"]))
    assert tuple(int(r["seed_index"]) for r in rows) == RECOVERY_SEEDS
    hashes = {json.dumps(x["source_hashes"], sort_keys=True) for x in wrappers}
    assert len(hashes) == 1
    assert json.loads(next(iter(hashes))) == controls["source_hashes"]
    args.checkpoint_dir.mkdir(parents=True, exist_ok=True)
    for r in rows:
        (args.checkpoint_dir / f"checkpoint-seed-{r['seed_index']}.json").write_text(
            json.dumps(r, indent=2, sort_keys=True) + "\n")
    counts = Counter(r["status"] for r in rows)
    assert set(counts) <= FINAL | {"pending"}, counts
    completed = [r for r in rows if r["status"] in FINAL]
    pending = [r for r in rows if r["status"] == "pending"]
    certificates = [r for r in rows if r["status"] == "bounded-recoder-certified"]
    progress = {
        "ok": True,
        "experiment": "bounded-source-recoder-exact-recovery",
        "status": "complete" if not pending else "pending",
        "recovery_seed_languages": 8,
        "status_counts": dict(sorted(counts.items())),
        "completed_seed_languages": len(completed),
        "pending_seed_languages": len(pending),
        "certified_seed_languages": len(certificates),
        "parent_exact_negative_seed_languages": 14,
        "exact_total_classified_seed_languages": 14 + len(completed),
        "all_22_classified": not pending,
        "source_hashes": json.loads(next(iter(hashes))),
        "controls": controls["controls"],
        "seeds": [{
            "seed_index": r["seed_index"], "rule": r["rule"], "pair": r["pair"],
            "status": r["status"], "batches": r.get("batches"),
            "parent_start_ordinal": r.get("parent_start_ordinal"),
            "current_ordinal": r.get("current_ordinal"),
            "remaining_structures": r.get("remaining_structures"),
            "recovery_exact_negative_structures": len(r.get("recovery_exact_negative_structures", [])),
            "certificate": r.get("certificate"), "stats": r.get("stats", {}),
        } for r in rows],
    }
    args.progress_output.parent.mkdir(parents=True, exist_ok=True)
    args.progress_output.write_text(json.dumps(progress, indent=2, sort_keys=True) + "\n")
    lines = [
        "# Exact bounded source-recoder recovery — progress", "",
        f"- Status: **{progress['status']}**",
        f"- Recovery seeds complete: **{len(completed)}/8**",
        f"- Total frontier seeds exactly classified: **{14 + len(completed)}/22**",
        f"- Certificates recovered: **{len(certificates)}**",
        "- Pending is scheduling state only; this recovery has no scientific `censored` status.", "",
        "| seed | rule | pair | status | ordinal | remaining | batches |",
        "| ---: | ---: | --- | --- | ---: | ---: | ---: |",
    ]
    for r in rows:
        lines.append(f"| {r['seed_index']} | {r['rule']} | {r['pair']} | {r['status']} | {r.get('current_ordinal')} | {r.get('remaining_structures')} | {r.get('batches')} |")
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.write_text("\n".join(lines) + "\n")
    print(json.dumps(progress, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
