#!/usr/bin/env python3
"""Exact future fibers and equivariant binary complements; frozen protocol in docs.

No search over local features. The finite quotient is minimal by forward
observation refinement. The orbit allocator realizes it over its observation
if and only if each stabilizer orbit type has sufficient binary-word capacity.
This does not assert a size-independent or local full-line encoder.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from experiment_matched_history_transport import (  # noqa: E402
    state_map, block2_parity_map, centered_g_map, compress, entropy,
)

WIDTHS = (6, 8, 10, 12, 14, 16, 18)
ARMS = ("P", "G", "PG")
RADII = (0, 1, 2, 3)
PROTOCOL = "docs/research/protocols/rule110-latent-q-20261007.md"
SCRIPT = "scripts/experiment_rule110_latent_q.py"
INPUTS = (PROTOCOL, SCRIPT, "scripts/experiment_matched_history_transport.py")
OUT = ROOT / "results/rule110_latent_q_20261007.json"
CERT = ROOT / "results/rule110_latent_q_20261007"
DEADLINE = float("inf")


def budget():
    if time.monotonic() > DEADLINE:
        raise TimeoutError("600-second scientific budget")


def sha_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def array_sha(a):
    return hashlib.sha256(np.asarray(a, dtype="<u4").tobytes()).hexdigest()


def rotate(x, n, stride):
    """tau_stride X at site i equals X at i+stride, little-endian sites."""
    stride %= n
    if not stride:
        return x
    return (x >> stride) | ((x & ((1 << stride) - 1)) << (n - stride))


def representatives(labels):
    k = int(labels.max()) + 1
    reps = np.full(k, len(labels), dtype=np.uint32)
    np.minimum.at(reps, labels, np.arange(len(labels), dtype=np.uint32))
    return reps


def collision(keys, targets):
    order = np.argsort(keys, kind="stable")
    bad = np.flatnonzero((keys[order[1:]] == keys[order[:-1]]) &
                         (targets[order[1:]] != targets[order[:-1]]))
    if not len(bad):
        return None
    i = int(bad[0])
    return int(order[i]), int(order[i + 1])


def first_difference(x, y, obs, step, limit):
    for t in range(limit + 1):
        if obs[x] != obs[y]:
            return {"time": t, "observation_x": int(obs[x]),
                    "observation_y": int(obs[y]), "at_x": x, "at_y": y}
        x, y = int(step[x]), int(step[y])
    raise AssertionError("refinement witness did not separate")


def future_partition(obs, step):
    labels = compress(obs)
    counts, witnesses = [int(labels.max()) + 1], []
    for depth in range(129):
        budget()
        k = counts[-1]
        new = compress(labels.astype(np.uint64) * k + labels[step])
        knew = int(new.max()) + 1
        if knew == k:
            reps = representatives(labels)
            assert np.array_equal(obs, obs[reps][labels])
            assert np.array_equal(labels[step], labels[step[reps]][labels])
            return labels, {"status": "stable", "depth": depth,
                            "class_counts": counts, "split_witnesses": witnesses}
        if depth == 128:
            return None, {"status": "not_stable_within_cap", "class_counts": counts,
                          "split_witnesses": witnesses}
        x, y = collision(labels, labels[step])
        witnesses.append({"refinement": depth + 1, "x": x, "y": y,
                          "current_observation": int(obs[x]),
                          "first_difference": first_difference(x, y, obs, step, depth + 1)})
        labels = new
        counts.append(knew)
    raise AssertionError("unreachable")


def quotient_metrics(labels, obs, step, n):
    reps = representatives(labels)
    sizes = np.bincount(labels)
    hist = Counter(map(int, sizes))
    visible_labels = compress(obs)
    multiplicities = np.bincount(visible_labels[reps])
    max_mult = int(multiplicities.max())
    residual = float(np.sum(sizes * np.log2(sizes)) / len(labels))
    ho, hc = entropy(visible_labels), n - residual
    pair = None
    for c in np.flatnonzero(sizes > 1)[:1]:
        x, y = map(int, np.flatnonzero(labels == c)[:2])
        a, b, coalescence, seen = x, y, None, set()
        for t in range(129):
            if a == b:
                coalescence = t
                break
            if (a, b) in seen:
                break
            seen.add((a, b))
            a, b = int(step[a]), int(step[b])
        pair = {"x": x, "y": y, "class": int(c), "class_size": int(sizes[c]),
                "current_observation": int(obs[x]), "coalescence_epoch": coalescence,
                "coalescence_search_cap": 128}
    return {
        "classes": len(reps), "source_states": len(labels),
        "class_size_histogram": {str(s): hist[s] for s in sorted(hist)},
        "H_observation": ho, "H_quotient": hc,
        "latent_conditional_bits": hc - ho,
        "residual_source_bits": residual, "residual_per_site": residual / n,
        "max_future_classes_per_visible_fiber": max_mult,
        "worst_fiber_label_bits": (max_mult - 1).bit_length(),
        "merged_witness": pair,
    }


def binary_orbits(n, stride):
    """Orbit representatives grouped by exact period for one subgroup generator."""
    if stride % n == 0:
        return {1: np.arange(1 << n, dtype=np.uint32)}
    seen = np.zeros(1 << n, dtype=bool)
    catalogs = defaultdict(list)
    for q in range(1 << n):
        if q % 8192 == 0:
            budget()
        if seen[q]:
            continue
        x, length = q, 0
        while not seen[x]:
            seen[x] = True
            length += 1
            x = rotate(x, n, stride)
        assert x == q
        catalogs[length].append(q)
    return {d: np.array(v, dtype=np.uint32) for d, v in catalogs.items()}


def equivariant_q(labels, obs, step, n, stride, catalogs):
    reps = representatives(labels)
    k = len(reps)
    cobs = obs[reps]
    states = np.arange(1 << n, dtype=np.uint32)
    rot = labels[rotate(reps, n, stride)]
    assert np.array_equal(labels[rotate(states, n, stride)], rot[labels])
    assert np.all(cobs[:-1] <= cobs[1:])  # canonical labels refine visible ordering
    fibers = defaultdict(list)
    for c, o in enumerate(cobs):
        fibers[int(o)].append(c)
    qclass = np.full(k, -1, dtype=np.int64)
    rot_powers = {}
    visible_orbits, matched_orbits = 0, 0
    demand_by_stabilizer = defaultdict(Counter)
    for anchor in range(k):
        if anchor % 8192 == 0:
            budget()
        if qclass[anchor] >= 0:
            continue
        v = int(cobs[anchor])
        c, p = int(rot[anchor]), 1
        while cobs[c] != v:
            assert cobs[c] > v
            c, p = int(rot[c]), p + 1
        s = p * stride
        if p not in rot_powers:
            rp = np.arange(k, dtype=np.uint32)
            for _ in range(p):
                rp = rot[rp]
            rot_powers[p] = rp
        rp = rot_powers[p]
        if s not in catalogs:
            catalogs[s] = binary_orbits(n, s)
        catalog = catalogs[s]
        class_orbits, seen = [], set()
        for c0 in fibers[v]:
            if c0 in seen:
                continue
            orbit, c = [], c0
            while c not in seen:
                seen.add(c)
                orbit.append(c)
                c = int(rp[c])
            assert c == c0
            class_orbits.append(orbit)
        demands = Counter(map(len, class_orbits))
        for d, count in demands.items():
            demand_by_stabilizer[s][d] = max(demand_by_stabilizer[s][d], count)
            supply = len(catalog.get(d, []))
            if count > supply:
                return None, {"status": "orbit_capacity_obstruction", "visible": v,
                    "translation_stride": stride, "stabilizer_generator_sites": s,
                    "orbit_length": d, "demand": count, "supply": supply,
                    "class_source_representatives": [int(reps[o[0]]) for o in class_orbits if len(o) == d]}
        used = Counter()
        for orbit in class_orbits:
            d = len(orbit)
            q = int(catalog[d][used[d]])
            used[d] += 1
            for c in orbit:
                assert qclass[c] == -1
                qclass[c] = q
                q = rotate(q, n, s)
            assert q == int(qclass[orbit[0]])
        # Propagate the chosen visible fiber around its full translation orbit.
        for c0 in fibers[v]:
            c, q = c0, int(qclass[c0])
            for _ in range(1, p):
                c, q = int(rot[c]), rotate(q, n, stride)
                assert qclass[c] == -1
                qclass[c] = q
        visible_orbits += 1
        matched_orbits += len(class_orbits)
    assert np.all(qclass >= 0)
    qclass = qclass.astype(np.uint32)
    q = qclass[labels]
    augmented = (obs.astype(np.uint64) << n) | q
    assert len(np.unique(augmented)) == k
    assert np.array_equal(q[rotate(states, n, stride)], rotate(q, n, stride))
    assert np.array_equal(augmented[step], augmented[step[reps]][labels])
    return qclass, {
        "status": "constructed", "translation_stride": stride,
        "visible_orbits": visible_orbits, "matched_class_orbits": matched_orbits,
        "exact_partition": True, "translation_covariant": True, "autonomous": True,
        "H_Q": entropy(compress(q)), "Q_distinct_words": len(np.unique(q)),
        "max_orbit_demand_by_generator": {str(s): dict(sorted(d.items())) for s, d in sorted(demand_by_stabilizer.items())},
    }


def local_keys(g, parity, q, n, arm, radius):
    key = np.zeros(1 << n, dtype=np.uint64)
    def symbol(j):
        if arm == "G":
            return ((g >> (j % n)) & 1) | (((q >> (j % n)) & 1) << 1)
        a = (2 * j) % n
        return (((parity >> (j % (n // 2))) & 1) |
                (((g >> a) & 3) << 1) | (((q >> a) & 3) << 3))
    for j in range(-radius, radius + 1):
        key = (key << (2 if arm == "G" else 5)) | symbol(j)
    return key, symbol(0)


def local_result(key, target, widths=None):
    bad = collision(key, target)
    if bad is None:
        return {"status": "pass_finite_domain", "contexts": len(np.unique(key))}
    x, y = bad
    witness = {"x": x, "y": y, "context": int(key[x]),
               "target_x": int(target[x]), "target_y": int(target[y])}
    if widths is not None:
        ns, xs = widths
        witness.update(x=int(xs[x]), y=int(xs[y]), n_x=int(ns[x]), n_y=int(ns[y]))
    return {"status": "conflict", "witness": witness}


def tuple_step(x, n):
    cells = [(x >> i) & 1 for i in range(n)]
    return sum(((110 >> (4 * cells[(i - 1) % n] + 2 * cells[i] + cells[(i + 1) % n])) & 1) << i for i in range(n))


def tuple_observation(x, n, arm):
    h = tuple_step(x, n)
    g = h ^ tuple_step(h, n) ^ tuple_step(x ^ h, n)
    p = sum((((x >> (2 * j)) ^ (x >> (2 * j + 1))) & 1) << j for j in range(n // 2))
    return p if arm == "P" else g if arm == "G" else (p << n) | g


def semantic_checks(n, arm, labels, obs, step, row, qclass=None):
    # Independent causal arithmetic for every recorded temporal witness.
    for w in row["refinement"]["split_witnesses"]:
        x, y = w["x"], w["y"]
        for t in range(w["first_difference"]["time"] + 1):
            ox, oy = tuple_observation(x, n, arm), tuple_observation(y, n, arm)
            if t < w["first_difference"]["time"]:
                assert ox == oy
            else:
                assert ox == w["first_difference"]["observation_x"]
                assert oy == w["first_difference"]["observation_y"] and ox != oy
            x, y = tuple_step(tuple_step(x, n), n), tuple_step(tuple_step(y, n), n)
    w = row["metrics"]["merged_witness"]
    if w:
        assert labels[w["x"]] == labels[w["y"]]
        assert tuple_observation(w["x"], n, arm) == tuple_observation(w["y"], n, arm)
    if n <= 10:
        words = []
        for x0 in range(1 << n):
            x, word = x0, []
            for _ in range(row["refinement"]["depth"] + 1):
                word.append(tuple_observation(x, n, arm))
                x = tuple_step(tuple_step(x, n), n)
            assert tuple_observation(x0, n, arm) == obs[x0]
            assert tuple_step(tuple_step(x0, n), n) == step[x0]
            words.append(tuple(word))
        mapping, reverse = {}, {}
        for x, word in enumerate(words):
            c = int(labels[x])
            assert mapping.setdefault(word, c) == c
            assert reverse.setdefault(c, word) == word
    if qclass is not None:
        q = qclass[labels]
        for r in RADII:
            test = row["locality"][str(r)]
            if test["status"] == "conflict":
                w = test["witness"]
                assert w["target_x"] != w["target_y"]
                # target uses independently stepped source, then retained exact Q.
                for name in ("x", "y"):
                    x = w[name]
                    nx = tuple_step(tuple_step(x, n), n)
                    v = tuple_observation(nx, n, arm)
                    target = (v & 1) | ((int(q[nx]) & 1) << 1) if arm == "G" else (((v >> n) & 1) | ((v & 3) << 1) | ((int(q[nx]) & 3) << 3))
                    assert target == w["target_" + name]


def repeat_word(x, d, n):
    y = np.zeros_like(x)
    for offset in range(0, n, d):
        y |= x << offset
    return y


def run():
    global DEADLINE
    started = time.monotonic()
    DEADLINE = started + 600
    CERT.mkdir(exist_ok=True)
    report = {"schema": "rule110-latent-q-v1", "date": "2026-10-07", "rule": 110,
              "cadence": 2, "widths": list(WIDTHS), "prior": "uniform sources",
              "protocol": PROTOCOL, "source_hashes": {p: sha_file(ROOT / p) for p in INPUTS},
              "profiles": {}, "gates": {}, "repetition": {}, "joint_locality": {}}
    qcache, all_local = {}, defaultdict(list)
    for n in WIDTHS:
        report["profiles"][str(n)] = {}
        try:
            budget()
            h = state_map(110, n)
            step, g, p = h[h], centered_g_map(110, n, h), block2_parity_map(n)
            states = np.arange(1 << n, dtype=np.uint32)
            d = states ^ h
            assert np.array_equal((states & d) ^ (states & (~d & ((1 << n) - 1))), states)
            observations = {"P": p, "G": g, "PG": (p.astype(np.uint64) << n) | g}
            labels_by_arm, catalogs = {}, {}
            for arm in ARMS:
                budget()
                obs = observations[arm]
                labels, refinement = future_partition(obs, step)
                row = {"status": refinement["status"], "refinement": refinement}
                report["profiles"][str(n)][arm] = row
                if labels is None:
                    continue
                labels_by_arm[arm] = labels
                reps = representatives(labels)
                row["metrics"] = quotient_metrics(labels, obs, step, n)
                arrays = {"labels": labels, "representatives": reps, "successor": labels[step[reps]]}
                qclass = None
                if arm != "P":
                    qclass, row["encoding"] = equivariant_q(labels, obs, step, n, 1 if arm == "G" else 2, catalogs)
                    if qclass is not None:
                        arrays["qclass"] = qclass
                        q = qclass[labels]
                        qcache[n, arm] = q
                        row["locality"] = {}
                        for r in RADII:
                            key, symbols = local_keys(g, p, q, n, arm, r)
                            target = symbols[step]
                            row["locality"][str(r)] = local_result(key, target)
                            all_local[arm, r].append((n, key, target))
                semantic_checks(n, arm, labels, obs, step, row, qclass)
                cert_path = CERT / f"n{n}_{arm}.npz"
                np.savez_compressed(cert_path, **arrays)
                row["certificate"] = {"path": cert_path.relative_to(ROOT).as_posix(),
                                      "array_sha256": {k: array_sha(a) for k, a in arrays.items()}}
                row["checks"] = {"full_finite_closure": True, "lift_decoder": True,
                                 "tuple_witness_replay": True,
                                 "independent_explicit_future_partition": n <= 10}
                print(json.dumps({"n": n, "arm": arm, "depth": refinement["depth"],
                                  "classes": len(reps), "R": row["metrics"]["residual_source_bits"],
                                  "encoding": row.get("encoding", {}).get("status")}), flush=True)
                OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
            if len(labels_by_arm) == 3:
                fine = labels_by_arm["PG"]
                reps = representatives(fine)
                for arm in ("P", "G"):
                    assert np.array_equal(labels_by_arm[arm], labels_by_arm[arm][reps][fine])
        except TimeoutError as exc:
            report["budget_stop"] = str(exc)
            break
    for n in WIDTHS:
        rows = report["profiles"].setdefault(str(n), {})
        for arm in ARMS:
            rows.setdefault(arm, {"status": "not_evaluated_budget"})
    for arm in ("G", "PG"):
        report["repetition"][arm] = []
        for d in WIDTHS:
            for n in WIDTHS:
                if n <= d or n % d:
                    continue
                rec = {"d": d, "n": n, "status": "not_evaluated_encoder_missing"}
                if (d, arm) in qcache and (n, arm) in qcache:
                    words = np.arange(1 << d, dtype=np.uint32)
                    repeated = repeat_word(words, d, n)
                    expected = repeat_word(qcache[d, arm], d, n)
                    actual = qcache[n, arm][repeated]
                    bad = np.flatnonzero(expected != actual)
                    rec.update(status="conflict" if len(bad) else "pass", conflicts=len(bad))
                    if len(bad):
                        x = int(bad[0])
                        rec["witness"] = {"x": x, "repeated_x": int(repeated[x]),
                                          "repeated_Q_d": int(expected[x]), "Q_n": int(actual[x])}
                report["repetition"][arm].append(rec)
        report["joint_locality"][arm] = {}
        for r in RADII:
            parts = all_local[arm, r]
            if not parts:
                report["joint_locality"][arm][str(r)] = {"status": "not_evaluated_encoder_missing"}
                continue
            keys = np.concatenate([k for _, k, _ in parts])
            targets = np.concatenate([t for _, _, t in parts])
            ns = np.concatenate([np.full(len(k), n, dtype=np.uint8) for n, k, _ in parts])
            xs = np.concatenate([np.arange(len(k), dtype=np.uint32) for _, k, _ in parts])
            rec = local_result(keys, targets, (ns, xs))
            rec["widths"] = [n for n, _, _ in parts]
            report["joint_locality"][arm][str(r)] = rec
    for question, arm in (("P1", "PG"), ("P2", "G")):
        rows = [report["profiles"][str(n)][arm] for n in (14, 16, 18)]
        report["gates"][question] = {"question": f"{arm} optimal compression >= 1 percent at 14,16,18",
            "status": "not_evaluated" if not all("metrics" in r for r in rows) else
            "pass" if all(r["metrics"]["residual_per_site"] >= .01 for r in rows) else "fail"}
    encs = [report["profiles"][str(n)][a].get("encoding", {}).get("status") for n in WIDTHS for a in ("G", "PG")]
    report["gates"]["P3"] = {"question": "exact minimal equivariant binary encoders at every width",
        "status": "pass" if all(s == "constructed" for s in encs) else "fail" if "orbit_capacity_obstruction" in encs else "not_evaluated"}
    all_reps = [r for a in ("G", "PG") for r in report["repetition"][a]]
    local_pass = all(any(r["status"] == "pass_finite_domain" and r["widths"] == list(WIDTHS)
                         for r in report["joint_locality"][a].values()) for a in ("G", "PG"))
    report["gates"]["P4"] = {"question": "constructed Q repetition compatible and radius<=3 across widths",
        "status": "not_evaluated" if report["gates"]["P3"]["status"] != "pass" else
        "pass" if local_pass and all(r["status"] == "pass" for r in all_reps) else "fail"}
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    execution = {"implementation_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                 "runtime_seconds": time.monotonic() - started, "python": sys.version,
                 "numpy": np.__version__, "platform": platform.platform(),
                 "result_sha256": sha_file(OUT), "reviewed_by": "none",
                 "certificates_bytes": sum(p.stat().st_size for p in CERT.glob("*.npz"))}
    (CERT / "execution.json").write_text(json.dumps(execution, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"gates": report["gates"], "execution": execution}), flush=True)


def verify_saved():
    report = json.loads(OUT.read_text(encoding="utf-8"))
    for p, expected in report["source_hashes"].items():
        assert sha_file(ROOT / p) == expected, p
    for n in WIDTHS:
        h = state_map(110, n)
        step, g, p = h[h], centered_g_map(110, n, h), block2_parity_map(n)
        for arm in ARMS:
            row = report["profiles"][str(n)][arm]
            if "certificate" not in row:
                continue
            cert = row["certificate"]
            arrays = np.load(ROOT / cert["path"])
            for name, expected in cert["array_sha256"].items():
                assert array_sha(arrays[name]) == expected
            obs = p if arm == "P" else g if arm == "G" else (p.astype(np.uint64) << n) | g
            labels, ref = future_partition(obs, step)
            assert ref == row["refinement"]
            assert np.array_equal(labels, arrays["labels"])
            reps = arrays["representatives"]
            assert np.array_equal(reps, representatives(labels))
            assert np.array_equal(arrays["successor"], labels[step[reps]])
            assert quotient_metrics(labels, obs, step, n) == row["metrics"]
            qclass = arrays["qclass"] if "qclass" in arrays.files else None
            if qclass is not None:
                q = qclass[labels]
                states = np.arange(1 << n, dtype=np.uint32)
                stride = 1 if arm == "G" else 2
                assert np.array_equal(q[rotate(states, n, stride)], rotate(q, n, stride))
                aug = (obs.astype(np.uint64) << n) | q
                assert len(np.unique(aug)) == len(reps)
                assert np.array_equal(aug[step], aug[step[reps]][labels])
                for r in RADII:
                    key, symbols = local_keys(g, p, q, n, arm, r)
                    assert local_result(key, symbols[step]) == row["locality"][str(r)]
            semantic_checks(n, arm, labels, obs, step, row, qclass)
    print("Saved quotient certificates, finite closure, equivariance, metrics and witnesses verified.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true", help="verify existing certificates without rewriting")
    args = parser.parse_args()
    verify_saved() if args.verify else run()
