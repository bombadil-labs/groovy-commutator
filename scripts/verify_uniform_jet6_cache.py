"""Post-run provenance/accounting, archive checks and lazy cache reader controls."""
import argparse
import base64
from collections import Counter
import hashlib
import json
from pathlib import Path
import tarfile

import numpy as np

import uniform_jet6_analysis as analysis
import uniform_jet6_cache as science

ROOT = Path(__file__).resolve().parents[1]
RUN = "experiments/uniform_jet6_cache_20260914/run"
RESULT = "results/uniform_jet6_cache_20260914.json"
SOURCES = {path: path for path in science.SOURCES}
SOURCES.update({name: path for name, path in (
    ("accounting", "scripts/verify_uniform_jet6_cache.py"),
    ("reader", "scripts/read_uniform_jet6_cache.py"),
    *[(name, f"{RUN}/{name}.json") for name in ("execution", "summary", "analysis", "archive_manifest", "benchmark")],
    ("floors", f"{RUN}/floors.jsonl"), ("paths", f"{RUN}/paths.jsonl"))})


def digest(path):
    with (ROOT/path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read(name):
    return json.loads((ROOT/SOURCES[name]).read_text())


def rows(name):
    return [json.loads(line) for line in (ROOT/SOURCES[name]).read_text().splitlines()]


def derive():
    execution, summary, manifest, benchmark = [read(n) for n in ("execution", "summary", "archive_manifest", "benchmark")]
    floors, paths = rows("floors"), rows("paths")
    assert set(execution["source_hashes"]) == set(science.SOURCES)
    assert all(digest(p) == h for p, h in execution["source_hashes"].items())
    assert execution["widths"] == [7, 8] and execution["rules"] == list(range(256))
    assert execution["dimensions"] == [2, 3, 4] and execution["period"] == 6
    assert len(paths) == 512 and {(p["width"], p["rule"]) for p in paths} == {(w,r) for w in (7,8) for r in range(256)}
    indexed = {(r["width"], r["rule"], r["dimension"]): r for r in floors}
    assert len(indexed) == len(floors)
    for path in paths:
        assert path["status"] in ("passed", "failed", "censored")
        if path["status"] == "passed":
            assert path["last_floor"] == 4 and not path["later_floors_untested"]
            assert all(indexed[path["width"],path["rule"],d]["status"] == "passed" for d in (2,3,4))
            for c in path["cache_at_path_end"]:
                assert c["native_family_evaluations"] == 1 and c["physical_key_builds"] == 2
    passed = [r for r in floors if r["status"] == "passed"]
    for row in passed:
        w, d = row["width"], row["dimension"]
        assert row["source_states"] == 2**w and row["phase_count"] == 6**(d-1)
        assert row["constraint_cells"] == 2**w * w * 6**(d-1)
        assert row["radii_array_order"] == [3]*(d-1)+[2]
        for key in ("native", "uniform_parent_recovery"):
            assert row[key]["passes"] and row[key]["conflicting_keys"] == 0 and row[key]["witness"] is None
        for key in ("aligned_recovery", "native_replay", "parent_replay", "source_recovery", "parents_immutable"):
            assert row[key] is True
        assert row["direct_patch_checks"] == 15 and row["uncached_sample_states"] == 4
        f, p = row["features"], row["phase_analysis"]
        phases, count = 6**(d-1), 2**w
        assert p["truth_shape"] == [phases,count]
        assert len(p["phase_degrees"]) == len(p["phase_terms"]) == phases
        assert f["source_degree_fraction"] == sum(p["phase_degrees"])/phases/w
        assert f["source_term_fraction"] == sum(p["phase_terms"])/phases/count
        assert f["affine_phase_fraction"] == sum(x <= 1 for x in p["phase_degrees"])/phases
        assert f["source_rank_fraction"] == p["source_rank"]/min(phases,count)
        assert f["key_fraction"] == row["native"]["forced_keys"]/(phases*count)
        assert all(np.isfinite(x) and 0 <= x <= 1 for x in f.values())
    assert [r["partial_rule"] for r in passed] == manifest["members"]
    expected = {"paths":len(paths), "path_status":dict(Counter(p["status"] for p in paths)),
                "floors_recorded":len(floors), "passed_floors":len(passed),
                "constraint_cells":sum(r.get("constraint_cells",0) for r in floors),
                "direct_patch_checks":sum(r.get("direct_patch_checks",0) for r in floors),
                "archive_members":len(manifest["members"]), "archive_bytes":manifest["archive_size"],
                "native_failure_floors":sum(r.get("failure_kind")=="native" for r in floors),
                "uniform_decoder_failure_floors":sum(r.get("failure_kind")=="uniform_decoder" for r in floors),
                "stage_seconds":{k:sum(r.get(k,0) for r in floors) for k in summary["stage_seconds"]}}
    assert all(summary[k] == v for k,v in expected.items())
    assert json.loads(json.dumps(analysis.analyze(floors,paths))) == read("analysis")
    assert benchmark["status"] == "completed"
    records = benchmark["records"]
    assert len(records) == 24
    assert {(r["repeat"],r["mode"],r["rule"]) for r in records} == {(i,m,r) for i in range(3) for m in ("old4","jet6") for r in (0,30,90,110)}
    micro = {}
    for mode in ("old4","jet6"):
        selected = [r for r in records if r["mode"]==mode]
        assert all(r["path"]["status"]=="passed" for r in selected)
        by_rule = {str(r):float(np.median([x["path"]["wall_seconds"] for x in selected if x["rule"]==r])) for r in (0,30,90,110)}
        assert benchmark["medians"][mode] == {"per_rule_median_seconds":by_rule,"pooled_median_seconds":float(np.median(list(by_rule.values())))}
        measurements = []
        for item in selected:
            assert [r["dimension"] for r in item["rows"]] == [2,3,4]
            for row in item["rows"]:
                assert row["radii_array_order"] == list(science.radii(row["dimension"],mode))
                m = row["key_microbenchmark"]
                assert m["all_keys_equal"]
                for k in ("cached","uncached"):
                    assert len(m["seconds"][k])==3 and all(v>0 for v in m["seconds"][k])
                    assert m[k+"_median"]==float(np.median(m["seconds"][k]))
                measurements.append(m)
        micro[mode] = {"floor_cases":len(measurements),
                       "median_cached_seconds":float(np.median([m["cached_median"] for m in measurements])),
                       "median_uncached_seconds":float(np.median([m["uncached_median"] for m in measurements])),
                       "median_paired_speed_ratio":float(np.median([m["uncached_median"]/m["cached_median"] for m in measurements]))}
    old = json.loads((science.OLD_RUN/"summary.json").read_text())
    work_ratio = summary["constraint_cells"]/old["native_constraint_cells"]
    time_ratio = summary["wall_seconds"]/old["wall_seconds"]
    native_prediction = (False if any(r.get("failure_kind")=="native" for r in floors)
                         else True if len(passed)==1536 else "censored")
    uniform_prediction = (False if any(r.get("failure_kind")=="uniform_decoder" for r in floors)
                          else True if len(passed)==1536 else "censored")
    return {"schema_version":1, "date":"2026-09-14", "implementation_commit":execution["implementation_commit"],
            "baseline_commit":execution["baseline_commit"], "source_paths":SOURCES,
            "source_hashes":{k:digest(p) for k,p in SOURCES.items()}, "summary":summary,
            "historical_comparison":{"old_wall_seconds":old["wall_seconds"], "new_wall_seconds":summary["wall_seconds"],
                                     "time_ratio":time_ratio, "cell_constraint_ratio":work_ratio,
                                     "throughput_ratio":work_ratio/time_ratio,
                                     "archive_size_ratio":summary["archive_bytes"]/old["archive_bytes"],
                                     "peak_rss_ratio":summary["peak_rss_bytes"]/old["peak_rss_bytes"],
                                     "scope":"Different operator, period, radius, cache and export representation; engineering comparison, not causal attribution"},
            "matched_backend_comparison":benchmark["medians"], "key_microbenchmark":micro,
            "predictions":{"P1_native_through4D":native_prediction,
                           "P1_stronger_uniform_recovery":uniform_prediction,
                           "P2_cached_keys_faster":all(m["median_cached_seconds"]<m["median_uncached_seconds"] for m in micro.values()),
                           "P3_lower_time_per_cell":work_ratio/time_ratio>1},
            "archive":{"sha256":manifest["archive_sha256"], "bytes":manifest["archive_size"],
                       "preservation":"Exact bytes delivered privately to Myk; public reproduction code, raw metrics and full member/archive hashes in repository",
                       "ci":"No archive download or CA construction; provenance, accounting and fixed-analysis recomputation only"}}


def check_archive(path):
    from read_uniform_jet6_cache import CachedRule
    manifest = read("archive_manifest")
    assert path.stat().st_size == manifest["archive_size"] and digest(path) == manifest["archive_sha256"]
    floor_map = {r["partial_rule"]["path"]:r for r in rows("floors") if r["status"]=="passed"}
    with tarfile.open(path,"r|gz") as archive:
        for wanted in manifest["members"]:
            member = archive.next()
            assert member and member.isfile() and member.name==wanted["path"] and member.size==wanted["size"]
            data = archive.extractfile(member).read()
            assert hashlib.sha256(data).hexdigest()==wanted["sha256"]
            record, row = json.loads(data), floor_map[member.name]
            cache = CachedRule(record)
            assert cache._law is None
            w,d = row["width"],row["dimension"]
            assert record["rule"]==row["rule"] and record["width"]==w and record["dimension"]==d
            assert record["grid_shape"]==[2**w]+[6]*(d-1)+[w]
            assert record["mode"]=="jet6" and record["recipe"]=={"family":"uniform-six-field"}
            assert record["radii_array_order"]==row["radii_array_order"]
            assert cache.k==row["native"]["forced_keys"]
            assert record["unforced_derivative"]==record["unforced_decoder"]==0
            assert record["native_table_sha256"]==row["native_sha256"]==science.old.sha(cache.derivative.tobytes()+cache.decoder.tobytes())
            assert float(cache.derivative.mean())==row["features"]["forced_flip_fraction"]
            truth = science.unpacked(record["source_phase_derivative_bits_big"],record["source_phase_shape"])
            assert list(truth.shape)==row["phase_analysis"]["truth_shape"]
            coefficients = science.old.mobius(truth)
            weights = np.array([i.bit_count() for i in range(2**w)])
            assert np.where(coefficients,weights[None,:],0).max(axis=1).tolist()==row["phase_analysis"]["phase_degrees"]
            assert coefficients.sum(axis=1).tolist()==row["phase_analysis"]["phase_terms"]
            assert science.old.binary_rank(truth)==row["phase_analysis"]["source_rank"]
            assert float(truth.mean())==row["features"]["event_flip_fraction"]
            if row["rule"] in (0,30,90,110) and w==7:
                # Bounded native index reconstruction/reader execution; full hashes above cover all members.
                actual = cache.step(cache.grid[[0,1,42,85,127]])
                reference = science.Reference(row["rule"],w,"jet6",None)
                assert np.array_equal(actual,reference.get(d,1)[[0,1,42,85,127]])
                assert np.array_equal(cache.recover(cache.grid[[0,1,42,85,127]]),reference.get(d-1,0)[[0,1,42,85,127]])
        assert archive.next() is None
    return {"members_verified":len(manifest["members"]),"bounded_reader_floors":12,"sha256":manifest["archive_sha256"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write",action="store_true")
    parser.add_argument("--archive",type=Path)
    args = parser.parse_args()
    rendered = json.dumps(derive(),indent=2)+"\n"
    if args.write:
        (ROOT/RESULT).write_text(rendered)
    else:
        assert (ROOT/RESULT).read_text()==rendered
        import check_result_integrity as integrity
        assert not integrity.check(RESULT),integrity.check(RESULT)
    if args.archive:
        print(json.dumps(check_archive(args.archive.resolve())))
    print(json.dumps({"accounting":"passed","analysis_recomputed":True,"primary_science_rerun":False}))


if __name__=="__main__":
    main()
