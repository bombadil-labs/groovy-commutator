"""Preserved-accounting and optional full archive checks; never run a CA sweep."""
from __future__ import annotations

import argparse
import base64
from collections import Counter
import hashlib
import json
from pathlib import Path
import tarfile

import numpy as np

import on_beam_rule_analysis as analysis

ROOT = Path(__file__).resolve().parents[1]
RUN = "experiments/on_beam_256_4d_20260914/run"
RESULT = "results/on_beam_256_4d_20260914.json"
SOURCES = {
    "script": "scripts/on_beam_256_4d.py",
    "analysis_script": "scripts/on_beam_rule_analysis.py",
    "native_core": "scripts/sequential_lift_6d_pilot.py",
    "accounting": "scripts/verify_on_beam_256_4d.py",
    "protocol": "docs/research/protocols/on-beam-256-4d-classes-20260914.md",
    "recipes": "results/binary_lift_20260914/rule_coverage.csv",
    "labels": "experiments/on_beam_256_4d_20260914/labels.json",
    **{name: f"{RUN}/{name}.json" for name in ("execution", "summary", "analysis", "archive_manifest")},
    "floors": f"{RUN}/floors.jsonl",
    "paths": f"{RUN}/paths.jsonl",
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def digest(path):
    with (ROOT / path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read(name):
    return json.loads((ROOT / SOURCES[name]).read_text())


def rows(name):
    return [json.loads(line) for line in (ROOT / SOURCES[name]).read_text().splitlines()]


def derive():
    execution, summary, saved_analysis, manifest = [read(n) for n in ("execution", "summary", "analysis", "archive_manifest")]
    floors, paths, labels = rows("floors"), rows("paths"), read("labels")
    assert execution["widths"] == [7, 8] and execution["rules"] == list(range(256))
    assert execution["dimensions"] == [2, 3, 4]
    assert set(execution["source_hashes"]) == {SOURCES[k] for k in ("script", "analysis_script", "native_core", "protocol", "recipes", "labels")}
    for path, value in execution["source_hashes"].items():
        assert digest(path) == value, path
    expected_paths = {(w, r) for w in (7, 8) for r in range(256)}
    expected_floors = {(w, r, d) for w, r in expected_paths for d in (2, 3, 4)}
    assert len(paths) == len(expected_paths) and {(r["width"], r["rule"]) for r in paths} == expected_paths
    assert len(floors) == len(expected_floors) and {(r["width"], r["rule"], r["dimension"]) for r in floors} == expected_floors
    classes, orbits = analysis.class_map(labels)
    for row in paths:
        assert row["status"] == "passed" and row["last_floor"] == 4
        assert row["orbit"] == min(analysis.orbit(row["rule"]))
        assert row["class"] == classes[row["orbit"]]
    members = []
    for row in floors:
        w, r, d = row["width"], row["rule"], row["dimension"]
        assert row["status"] == "passed"
        assert row["recipe"] == execution["recipes"][str(r)]
        assert row["source_states"] == 2**w and row["phase_count"] == 4**(d-1)
        assert row["constraint_cells"] == 2**w * w * 4**(d-1)
        assert row["direct_patch_checks"] == 15
        for key in ("native", "parent_recovery"):
            assert row[key]["passes"] and row[key]["conflicting_keys"] == 0
            assert row[key]["witness"] is None
        for key in ("native_replay", "parent_replay", "source_recovery", "parents_immutable"):
            assert row[key] is True
        count, phases = row["source_states"], row["phase_count"]
        detail, f = row["phase_analysis"], row["features"]
        assert detail["truth_shape"] == [phases, count]
        assert len(detail["phase_degrees"]) == len(detail["phase_terms"]) == phases
        assert all(0 <= x <= w for x in detail["phase_degrees"])
        assert all(0 <= x <= count for x in detail["phase_terms"])
        assert f["source_degree_fraction"] == sum(detail["phase_degrees"]) / phases / w
        assert f["source_term_fraction"] == sum(detail["phase_terms"]) / phases / count
        assert f["affine_phase_fraction"] == sum(x <= 1 for x in detail["phase_degrees"]) / phases
        assert f["source_rank_fraction"] == detail["source_rank"] / min(phases, count)
        assert f["key_fraction"] == row["native"]["forced_keys"] / (count * phases)
        assert all(np.isfinite(x) and 0 <= x <= 1 for x in f.values())
        assert row["partial_rule"]["path"] == f"w{w}/rule{r:03d}/d{d}.json"
        members.append(row["partial_rule"])
    assert members == manifest["members"] and len({m["path"] for m in members}) == len(members)
    expected = {"paths": len(paths), "passed_paths": len(paths), "failed_paths": 0, "censored_paths": 0,
                "floors": len(floors), "passed_floors": len(floors), "archive_members": len(members),
                "archive_bytes": manifest["archive_size"],
                "native_constraint_cells": sum(r["constraint_cells"] for r in floors),
                "direct_patch_checks": sum(r["direct_patch_checks"] for r in floors)}
    assert all(summary[k] == v for k, v in expected.items())
    assert 0 < summary["wall_seconds"] < 900 and 0 < summary["peak_rss_bytes"] < 4*1024**3
    recomputed = analysis.analyze(floors, paths, {int(k): v for k, v in execution["recipes"].items()}, labels)
    assert json.loads(json.dumps(recomputed)) == saved_analysis, "Saved analysis differs"
    return {"schema_version": 1, "date": "2026-09-14", "implementation_commit": execution["implementation_commit"],
            "baseline_commit": execution["baseline_commit"], "source_paths": SOURCES,
            "source_hashes": {k: digest(p) for k, p in SOURCES.items()},
            "scope": "All 256 ECA sources; all width-seven/eight words; fixed four-field recipes; newly synthesized immutable native radius-two laws through 4D; no G or full-shift claim.",
            "summary": summary, "orbit_class_counts": dict(Counter(classes.values())),
            "rule_class_counts": dict(Counter(classes[o] for o, members in orbits.items() for _ in members)),
            "predictions": saved_analysis["predictions"],
            "classification": {w: {"balanced_accuracy": {v: m["balanced_accuracy"] for v, m in scores["views"].items()},
                                       "incremental_balanced_accuracy": scores["incremental_balanced_accuracy"]}
                               for w, scores in saved_analysis["models"].items()},
            "global_exchangeability_p": saved_analysis["models"]["7"]["permutation_reference"]["one_sided_p"],
            "archive": {"sha256": manifest["archive_sha256"], "bytes": manifest["archive_size"],
                        "preservation": "Exact gzip delivered as a private user-scoped downloadable artifact. Repository contains public reproduction code and hashes, not the large archive bytes.",
                        "ci": "Source hashes, complete raw accounting and saved-analysis recomputation only. External archive bytes require --archive locally."}}


def check_archive(path):
    """Stream every preserved member, check hashes, codecs and source-phase metrics."""
    from on_beam_256_4d import binary_rank, mobius
    manifest = read("archive_manifest")
    assert path.stat().st_size == manifest["archive_size"]
    assert digest(path) == manifest["archive_sha256"]
    indexed = {r["partial_rule"]["path"]: r for r in rows("floors")}
    with tarfile.open(path, "r|gz") as archive:
        for expected in manifest["members"]:
            member = archive.next()
            assert member is not None and member.isfile() and member.name == expected["path"]
            assert member.size == expected["size"]
            data = archive.extractfile(member).read()
            assert sha(data) == expected["sha256"]
            record, row = json.loads(data), indexed[member.name]
            for key in ("width", "rule", "dimension", "recipe"):
                assert record[key] == row[key]
            assert record["format"] == "ordered-five-tuple-physical-neighborhood-v1"
            assert record["radius"] == 2 and record["unforced_derivative"] == record["unforced_decoder"] == 0
            counts = record["node_counts"]
            assert counts == row["node_counts"] and len(counts) == row["dimension"] - 1
            assert len(record["nodes_delta_i32le_columns"]) == len(counts)
            for depth, (encoded, n) in enumerate(zip(record["nodes_delta_i32le_columns"], counts)):
                raw = base64.b64decode(encoded, validate=True)
                assert len(raw) == n * 5 * 4
                nodes = np.frombuffer(raw, dtype="<i4").reshape(5, n).T.cumsum(axis=0, dtype=np.int64)
                assert nodes.min() >= 0 and nodes.max() < (32 if depth == 0 else counts[depth-1])
            k = record["forced_root_count"]
            assert k == counts[-1] == row["native"]["forced_keys"]
            for name in ("forced_derivative_bits_big", "forced_decoder_bits_big"):
                raw = base64.b64decode(record[name], validate=True)
                assert len(raw) == (k+7)//8
                bits = np.unpackbits(np.frombuffer(raw, dtype=np.uint8), bitorder="big")
                assert not np.any(bits[k:])
                if name == "forced_derivative_bits_big":
                    assert float(bits[:k].mean()) == row["features"]["forced_flip_fraction"]
            shape = record["source_phase_shape"]
            assert shape == row["phase_analysis"]["truth_shape"]
            raw = base64.b64decode(record["source_phase_derivative_bits_big"], validate=True)
            assert len(raw) == shape[0] * shape[1] // 8
            truth = np.unpackbits(np.frombuffer(raw, dtype=np.uint8), bitorder="big").reshape(shape)
            coeff = mobius(truth)
            weights = np.array([i.bit_count() for i in range(shape[1])])
            assert np.where(coeff, weights[None, :], 0).max(axis=1).tolist() == row["phase_analysis"]["phase_degrees"]
            assert coeff.sum(axis=1).tolist() == row["phase_analysis"]["phase_terms"]
            assert binary_rank(truth) == row["phase_analysis"]["source_rank"]
            assert float(truth.mean()) == row["features"]["event_flip_fraction"]
        assert archive.next() is None
    print(json.dumps({"archive": "verified", "members": len(manifest["members"]), "sha256": manifest["archive_sha256"]}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--archive", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(derive(), indent=2) + "\n"
    if args.write:
        (ROOT / RESULT).write_text(rendered)
    else:
        assert (ROOT / RESULT).read_text() == rendered, "Canonical account differs"
        import check_result_integrity as integrity
        assert not integrity.check(RESULT), integrity.check(RESULT)
    if args.archive:
        check_archive(args.archive.resolve())
    print(json.dumps({"accounting": "passed", "analysis_recomputed": True, "ca_sweep": False}))


if __name__ == "__main__":
    main()
