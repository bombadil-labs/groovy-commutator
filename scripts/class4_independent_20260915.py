#!/usr/bin/env python3
"""Frozen exploratory Class-IV pilot; see the committed protocol.

All scientific choices are constants below. No external discriminator code.
--self-test executes bounded semantic controls only, never the source-domain
pilot. --run writes per-rule checkpoints and raw sufficient-statistic arrays.
--summarize reads those saved checkpoints and joins labels only afterwards.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import platform
import resource
import signal
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from groovy.ca import apply_rule

WIDTHS = (5, 7, 9)
HISTORIES = (4, 8, 12)
RINGS = tuple(range(9, 15))
CONFIGS = (
    dict(name="primary", n=256, burn=256, steps=512,
         seeds=[101, 202, 303, 404, 505, 606]),
    dict(name="replication", n=512, burn=512, steps=512,
         seeds=[1101, 1202, 1303, 1404, 1505, 1606]),
)
PROTOCOL = "docs/research/protocols/class4-independent-20260915.md"
CLARIFICATIONS = "docs/research/protocols/class4-independent-20260915-clarifications.md"
LABELS = "experiments/on_beam_256_4d_20260914/labels.json"
SOURCE_PATHS = ("scripts/class4_independent_20260915.py", "src/groovy/ca.py",
                PROTOCOL, CLARIFICATIONS, LABELS)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, sort_keys=True, separators=(",", ":"),
                              allow_nan=False) + "\n")
    tmp.replace(path)


def reflect_rule(r):
    return sum(((r >> (4*c+b*2+a)) & 1) << (4*a+b*2+c)
               for a in (0, 1) for b in (0, 1) for c in (0, 1))


def complement_rule(r):
    return sum((1 ^ ((r >> (7-i)) & 1)) << i for i in range(8))


def orbit(r):
    return sorted({r, reflect_rule(r), complement_rule(r),
                   reflect_rule(complement_rule(r))})


def representatives():
    reps = sorted({min(orbit(r)) for r in range(256)})
    assert len(reps) == 88
    return reps


def step_rows(x, r):
    # apply_rule rolls flattened arrays. These explicit periodic guard cells
    # make every retained interior cell use neighbors from its own row.
    padded = np.concatenate((x[:, -1:], x, x[:, :1]), axis=1)
    return apply_rule(padded, r)[:, 1:-1]


def scalar_step(bits, r):
    n = len(bits)
    return [int((r >> (4*bits[(i-1) % n] + 2*bits[i] + bits[(i+1) % n])) & 1)
            for i in range(n)]


def local_tables(r, w):
    """Arrays indexed by bits [external-left, core..., external-right]."""
    cores = np.arange(1 << w, dtype=np.int64)
    bits = ((cores[:, None] >> np.arange(w)) & 1).astype(np.uint8)
    q = bits[:, 0] + 2*bits[:, 1] + 4*bits[:, -2] + 8*bits[:, -1]
    qcounts = np.bincount(q, minlength=16)
    losses = np.zeros((4, 1 << w))
    residuals = np.zeros_like(losses)
    outputs = np.zeros((4, 1 << w), dtype=np.int64)
    lut = np.array([(r >> i) & 1 for i in range(8)], dtype=np.uint8)
    for e in range(4):
        ext = np.column_stack((np.full(1 << w, e & 1, dtype=np.uint8),
                               bits, np.full(1 << w, e >> 1, dtype=np.uint8)))
        out = lut[4*ext[:, :-2] + 2*ext[:, 1:-1] + ext[:, 2:]]
        y = (out.astype(np.int64) * (1 << np.arange(w))).sum(axis=1)
        outputs[e] = y
        counts = np.bincount(y, minlength=1 << w)
        losses[e] = np.log2(counts[y])
        means = np.bincount(q, weights=losses[e], minlength=16) / qcounts
        residuals[e] = means[q] - losses[e]
        group_sums = np.bincount(q, weights=residuals[e], minlength=16)
        assert np.max(np.abs(group_sums)) < 1e-9
    distinct = 1 + np.count_nonzero(np.diff(np.sort(outputs, axis=0), axis=0), axis=0)
    capacity = np.log2(distinct)
    sigma = float(residuals.std())
    words = np.arange(1 << (w+2), dtype=np.int64)
    b = (words >> 1) & ((1 << w)-1)
    e = (words & 1) + 2*(words >> (w+1))
    return dict(loss=losses[e, b], residual=residuals[e, b],
                incoming=capacity[b], sigma=sigma, degenerate=sigma < 1e-12)


def reverse_words(words, width):
    out = np.zeros_like(words)
    for i in range(width):
        out |= ((words >> i) & 1) << (width-1-i)
    return out


def successors(r, n):
    x = np.arange(1 << n, dtype=np.int64)
    mask = (1 << n)-1
    left = ((x << 1) & mask) | (x >> (n-1))
    right = (x >> 1) | ((x & 1) << (n-1))
    result = np.zeros_like(x)
    for pattern in range(8):
        if (r >> pattern) & 1:
            term = (left if pattern & 4 else left ^ mask).copy()
            term &= (x if pattern & 2 else x ^ mask)
            term &= (right if pattern & 1 else right ^ mask)
            result |= term
    return result


def rotation_quotient(n):
    x = np.arange(1 << n, dtype=np.int64)
    least = x.copy()
    rot = x.copy()
    for _ in range(1, n):
        rot = (rot >> 1) | ((rot & 1) << (n-1))
        np.minimum(least, rot, out=least)
    nodes, inverse = np.unique(least, return_inverse=True)
    return nodes, inverse


def cycle_spectrum(nxt):
    """Peel trees, then traverse the remaining disjoint directed cycles."""
    n = len(nxt)
    indegree = np.bincount(nxt, minlength=n)
    queue = list(np.flatnonzero(indegree == 0))
    pos = 0
    while pos < len(queue):
        node = queue[pos]
        pos += 1
        target = int(nxt[node])
        indegree[target] -= 1
        if indegree[target] == 0:
            queue.append(target)
    spectrum = Counter()
    for start in np.flatnonzero(indegree):
        if not indegree[start]:
            continue
        node, length = int(start), 0
        while indegree[node]:
            indegree[node] = 0
            node = int(nxt[node])
            length += 1
        spectrum[length] += 1
    assert spectrum
    return {str(k): int(v) for k, v in sorted(spectrum.items())}


def graph_metrics(r, n, quotient):
    nxt = successors(r, n)
    nodes, inverse = quotient
    qnext = inverse[nxt[nodes]]
    assert np.array_equal(inverse[nxt], qnext[inverse])
    p = cycle_spectrum(nxt)
    q = cycle_spectrum(qnext)
    return dict(n=n, maximum_period=max(map(int, p)),
                maximum_shape_period=max(map(int, q)),
                ordinary_spectrum=p, shape_spectrum=q,
                states=1 << n, rotation_classes=len(nodes))


def slope(values):
    x = np.array(RINGS, dtype=float)
    y = np.log2(np.asarray(values, dtype=float))
    return float(np.dot(x-x.mean(), y-y.mean()) / np.dot(x-x.mean(), x-x.mean()))


def trajectory(r, config):
    states = np.stack([np.random.Generator(np.random.PCG64(seed)).integers(
        0, 2, size=config['n'], dtype=np.uint8) for seed in config['seeds']])
    result = np.empty((config['burn']+config['steps']+1, *states.shape), dtype=np.uint8)
    result[0] = states
    for t in range(1, len(result)):
        states = step_rows(states, r)
        result[t] = states
    return result


def spatial_counts(series, config, w):
    frames = series[config['burn']:config['burn']+config['steps']]
    words = np.zeros(frames.shape, dtype=np.uint16)
    half = w // 2
    for j, offset in enumerate(range(-half-1, half+2)):
        words |= np.roll(frames, -offset, axis=2).astype(np.uint16) << j
    counts = np.stack([np.bincount(words[:, s].ravel(), minlength=1 << (w+2))
                       for s in range(6)])
    assert np.all(counts.sum(axis=1) == config['n']*config['steps'])
    return counts


def history_counts(series, config, h):
    burn, steps = config['burn'], config['steps']
    words = np.zeros(series[burn:burn+steps].shape, dtype=np.uint16)
    for lag in range(h+1):
        words |= series[burn-lag:burn+steps-lag].astype(np.uint16) << lag
    joint = (words << 1) | series[burn+1:burn+steps+1]
    counts = np.stack([np.bincount(joint[:, s].ravel(), minlength=1 << (h+2))
                       .reshape(1 << (h+1), 2) for s in range(6)])
    assert np.all(counts.sum(axis=(1, 2)) == config['n']*steps)
    return counts


def conditional_entropy(counts):
    total = counts.sum()
    totals = counts.sum(axis=1, keepdims=True)
    p = np.divide(counts, totals, out=np.ones_like(counts, dtype=float), where=totals != 0)
    mask = counts > 0
    return float(-np.sum(counts[mask] * np.log2(p[mask])) / total)


def current_counts(counts):
    return np.stack((counts[::2].sum(axis=0), counts[1::2].sum(axis=0)))


def predictive_metrics(counts):
    directions = []
    for train_idx, test_idx in ((slice(0, 3), slice(3, 6)), (slice(3, 6), slice(0, 3))):
        train, test = counts[train_idx].sum(axis=0), counts[test_idx].sum(axis=0)
        train_c, test_c = current_counts(train), current_counts(test)
        prob_h = (train + 0.5) / (train.sum(axis=1, keepdims=True) + 1.0)
        prob_c = (train_c + 0.5) / (train_c.sum(axis=1, keepdims=True) + 1.0)
        ce_h = float(-np.sum(test*np.log2(prob_h)) / test.sum())
        ce_c = float(-np.sum(test_c*np.log2(prob_c)) / test.sum())
        gain = ce_c-ce_h
        innovation = conditional_entropy(test)
        directions.append(dict(cross_entropy_current=ce_c, cross_entropy_history=ce_h,
                               predictive_gain=gain, innovation=innovation,
                               plugin_conditional_mi=conditional_entropy(test_c)-innovation,
                               score=4*max(0.0, gain)*innovation,
                               train_samples=int(train.sum()), test_samples=int(test.sum()),
                               train_occupied_contexts=int(np.count_nonzero(train.sum(axis=1))),
                               test_occupied_contexts=int(np.count_nonzero(test.sum(axis=1)))))
    return dict(score=float(np.mean([d['score'] for d in directions])), directions=directions,
                occupied_contexts_by_seed=[int(np.count_nonzero(x.sum(axis=1))) for x in counts])


def retention_metrics(counts, table, alpha):
    totals = counts.sum(axis=1)
    numerator = counts @ table['residual'] / totals
    r = np.zeros(6) if table['degenerate'] else numerator/table['sigma']
    mean_r = float(r.mean())
    return dict(retention=mean_r, retention_by_seed=r.tolist(),
                residual_mean=float(numerator.mean()), reference_sd=table['sigma'],
                degenerate=bool(table['degenerate']),
                incoming_capacity=float(np.mean(counts @ table['incoming']/totals)),
                ambiguity=float(np.mean(counts @ table['loss']/totals)),
                score=max(0.0, mean_r)*max(0.0, alpha), sample_count=int(totals.sum()))


def self_test():
    checks = {}
    states = ((np.arange(32)[:, None] >> np.arange(5)) & 1).astype(np.uint8)
    for r in range(256):
        expected = np.asarray([scalar_step(s.tolist(), r) for s in states], dtype=np.uint8)
        assert np.array_equal(step_rows(states, r), expected), r
        packed = (expected.astype(np.int64)*(1 << np.arange(5))).sum(axis=1)
        assert np.array_equal(successors(r, 5), packed), r
    checks['all_256_scalar_batch_and_packed_step'] = True
    for w in WIDTHS:
        for r, value in ((204, 0), (170, 1), (240, 1)):
            tab = local_tables(r, w)
            assert np.allclose(tab['loss'], value)
            assert np.allclose(tab['incoming'], value)
            assert tab['degenerate']
    checks['same_window_identity_and_shifts'] = True
    words = np.arange(1 << 7, dtype=np.int64)
    rev = reverse_words(words, 7)
    for r in range(256):
        tab = local_tables(r, 5)
        reflect = local_tables(reflect_rule(r), 5)
        comp = local_tables(complement_rule(r), 5)
        for key in ('loss', 'residual', 'incoming'):
            assert np.allclose(tab[key], reflect[key][rev], atol=1e-10), (r, key, 'reflection')
            assert np.allclose(tab[key], comp[key][127 ^ words], atol=1e-10), (r, key, 'complement')
    checks['all_256_local_covariance'] = True
    for r in (0, 30, 54, 110, 122, 126, 204):
        tab = local_tables(r, 5)
        outs = {}
        for e in range(4):
            es = []
            for b in range(32):
                seq = [e & 1] + [(b >> j) & 1 for j in range(5)] + [e >> 1]
                es.append(tuple((r >> (4*seq[j]+2*seq[j+1]+seq[j+2])) & 1 for j in range(5)))
            outs[e] = es
            ct = Counter(es)
            for b in range(32):
                idx = (e & 1) | (b << 1) | ((e >> 1) << 6)
                assert abs(tab['loss'][idx]-math.log2(ct[es[b]])) < 1e-12
        for b in range(32):
            assert abs(tab['incoming'][b << 1]-math.log2(len({outs[e][b] for e in range(4)}))) < 1e-12
    checks['independent_direct_local_counts'] = True
    for n in (5, 6):
        quo = rotation_quotient(n)
        for r in (0, 204, 170):
            g = graph_metrics(r, n, quo)
            assert g['maximum_shape_period'] == 1
            assert g['maximum_period'] == (n if r == 170 else 1)
    checks['constant_identity_shift_quotient'] = True
    cfg = dict(n=16, burn=16, steps=16, seeds=[1, 2, 3, 4, 5, 6])
    series = trajectory(54, cfg)
    for w in (5, 7):
        observed = spatial_counts(series, cfg, w)
        reference = np.zeros_like(observed)
        for t in range(16, 32):
            for s in range(6):
                for i in range(16):
                    code = sum(int(series[t, s, (i+j-w//2-1) % 16]) << j for j in range(w+2))
                    reference[s, code] += 1
        assert np.array_equal(observed, reference)
    for h in (4, 8, 12):
        observed = history_counts(series, cfg, h)
        reference = np.zeros_like(observed)
        for t in range(16, 32):
            for s in range(6):
                for i in range(16):
                    code = sum(int(series[t-j, s, i]) << j for j in range(h+1))
                    reference[s, code, series[t+1, s, i]] += 1
        assert np.array_equal(observed, reference)
    checks['independent_spatial_and_temporal_indexing'] = True
    for r in (0, 204, 51):
        series = trajectory(r, cfg)
        for h in HISTORIES:
            assert predictive_metrics(history_counts(series, cfg, h))['score'] == 0
    checks['constant_identity_blinker_temporal_zero'] = True
    # Exact count controls: independent outcomes, and a process where an older
    # bit predicts a noisy output (Bayes error 1/4), while C carries no signal.
    independent = np.full((6, 32, 2), 50, dtype=np.int64)
    assert predictive_metrics(independent)['score'] == 0
    useful = independent.copy()
    for k in range(32):
        older = (k >> 1) & 1
        useful[:, k, older] = 75
        useful[:, k, 1-older] = 25
    assert predictive_metrics(useful)['score'] > 0.5
    checks['synthetic_independence_and_useful_history'] = True
    assert len(representatives()) == 88
    checks['symmetry_families'] = 88
    return checks


def run(out, implementation, budget):
    started = time.monotonic()
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    if (out/'execution.json').exists():
        raise RuntimeError('Refuse to overwrite an existing execution; preserve it explicitly.')
    hashes = {p: sha256(ROOT/p) for p in SOURCE_PATHS}
    execution = dict(status='running', implementation_commit=implementation,
                     source_hashes=hashes, protocol_commit='2302fa9ad03ccfeae2020adbfcbb62e32f0255e6',
                     python=platform.python_version(), numpy=np.__version__,
                     budget_seconds=budget, configurations=CONFIGS, rings=RINGS,
                     widths=WIDTHS, histories=HISTORIES, completed_rules=[])
    write_json(out/'execution.json', execution)
    controls = self_test()
    write_json(out/'controls.json', controls)
    quotients = {n: rotation_quotient(n) for n in RINGS}
    rules = representatives()
    def wall_expired(signum, frame):
        raise TimeoutError('Frozen total evaluation budget exceeded')
    signal.signal(signal.SIGALRM, wall_expired)
    signal.setitimer(signal.ITIMER_REAL, max(0.001, budget-(time.monotonic()-started)))
    try:
        for index, r in enumerate(rules):
            if time.monotonic()-started > budget:
                execution['status'] = 'censored_wall_budget'
                break
            rule_start = time.monotonic()
            graphs = [graph_metrics(r, n, quotients[n]) for n in RINGS]
            alpha_q = slope([g['maximum_shape_period'] for g in graphs])
            alpha_p = slope([g['maximum_period'] for g in graphs])
            tables = {w: local_tables(r, w) for w in WIDTHS}
            row = dict(rule=r, orbit=orbit(r), graphs=graphs,
                       alpha_shape=alpha_q, alpha_ordinary=alpha_p, configurations={})
            for cfg in CONFIGS:
                if time.monotonic()-started > budget:
                    raise TimeoutError('Frozen total evaluation budget exceeded')
                series = trajectory(r, cfg)
                arrays = {}
                record = dict(retention={}, prediction={})
                for w in WIDTHS:
                    ct = spatial_counts(series, cfg, w)
                    arrays[f'spatial_w{w}'] = ct
                    record['retention'][str(w)] = retention_metrics(ct, tables[w], alpha_q)
                for h in HISTORIES:
                    ct = history_counts(series, cfg, h)
                    arrays[f'temporal_h{h}'] = ct
                    record['prediction'][str(h)] = predictive_metrics(ct)
                raw = out/'counts'/f'r{r:03d}_{cfg["name"]}.npz'
                raw.parent.mkdir(exist_ok=True)
                np.savez_compressed(raw, **arrays)
                record['raw_counts'] = dict(path=str(raw.relative_to(out)), sha256=sha256(raw))
                row['configurations'][cfg['name']] = record
            if r == 54:
                assert row['graphs'][-1]['maximum_period'] == 112
            if r == 110:
                assert row['graphs'][-1]['maximum_period'] == 91
            row['elapsed_seconds'] = time.monotonic()-rule_start
            write_json(out/'rules'/f'r{r:03d}.json', row)
            execution['completed_rules'].append(r)
            execution['elapsed_seconds'] = time.monotonic()-started
            write_json(out/'execution.json', execution)
            print(json.dumps(dict(completed=index+1, total=88, rule=r,
                                  elapsed=round(execution['elapsed_seconds'], 2))), flush=True)
        else:
            execution['status'] = 'complete'
    except BaseException as exc:
        execution['status'] = 'censored_wall_budget' if isinstance(exc, TimeoutError) else 'failed'
        execution['error'] = dict(type=type(exc).__name__, message=str(exc))
        raise
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        execution['elapsed_seconds'] = time.monotonic()-started
        execution['peak_rss_kib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        write_json(out/'execution.json', execution)
    return execution


def auc(positive, negative):
    if not positive or not negative:
        return None
    return float(np.mean([float(p > n)+0.5*float(p == n) for p in positive for n in negative]))


def rank_report(scores, classes, positives=(54, 110), exclude=(41, 106)):
    negatives = sorted(r for r in scores if r not in positives and r not in exclude)
    class3 = sorted(r for r in negatives if classes[r] == 3)
    lower = min(scores[r] for r in positives)
    population = sorted(r for r in scores if r not in exclude)
    ranks = {}
    for r in positives:
        greater = sum(scores[s] > scores[r] for s in population)
        ties = sum(scores[s] == scores[r] for s in population)
        ranks[str(r)] = 1+greater+(ties-1)/2
    return dict(auc_all=auc([scores[r] for r in positives], [scores[r] for r in negatives]),
                auc_class3=auc([scores[r] for r in positives], [scores[r] for r in class3]),
                positive_scores={str(r): scores[r] for r in positives}, positive_ranks=ranks,
                negatives_at_or_above_lower_positive=[dict(rule=r, score=scores[r], class_label=classes[r])
                    for r in sorted(negatives, key=lambda s: (-scores[s], s)) if scores[r] >= lower],
                clean_separation=all(scores[r] < lower for r in negatives),
                beats_122_and_126=all(scores[p] > scores[n] for p in positives for n in (122, 126)),
                disputed={str(r): scores[r] for r in (41, 106)},
                top20=[dict(rule=r, score=scores[r], class_label=classes[r])
                       for r in sorted(scores, key=lambda s: (-scores[s], s))[:20]])


def summarize(out, result_path):
    out = Path(out)
    execution = json.loads((out/'execution.json').read_text())
    if execution['status'] != 'complete' or execution['completed_rules'] != representatives():
        raise RuntimeError('Incomplete population: refuse complete-classifier scoring')
    for p, digest in execution['source_hashes'].items():
        assert sha256(ROOT/p) == digest, p
    rows = [json.loads((out/'rules'/f'r{r:03d}.json').read_text()) for r in representatives()]
    # First use of class labels in the scientific pipeline.
    labels = json.loads((ROOT/LABELS).read_text())
    classes = {min(orbit(r)): int(k) for k, rules in labels['representatives'].items() for r in rules}
    assert set(classes) == set(representatives())
    reports, ablations, predictions = {}, {}, {}
    for cfg in CONFIGS:
        name = cfg['name']
        reports[name], ablations[name] = {}, {}
        for w in WIDTHS:
            scores = {row['rule']: row['configurations'][name]['retention'][str(w)]['score'] for row in rows}
            reports[name][f'A_W{w}'] = rank_report(scores, classes)
            if w == 7:
                comp = {row['rule']: row['configurations'][name]['retention']['7']['retention'] for row in rows}
                ablations[name]['retention_only'] = rank_report(comp, classes)
        for h in HISTORIES:
            scores = {row['rule']: row['configurations'][name]['prediction'][str(h)]['score'] for row in rows}
            reports[name][f'B_h{h}'] = rank_report(scores, classes)
            if h == 8:
                for key in ('predictive_gain', 'innovation'):
                    comp = {row['rule']: float(np.mean([d[key] for d in row['configurations'][name]['prediction']['8']['directions']]))
                            for row in rows}
                    ablations[name][key] = rank_report(comp, classes)
        for key in ('alpha_shape', 'alpha_ordinary'):
            ablations[name][key] = rank_report({row['rule']: row[key] for row in rows}, classes)
        for candidate in ('A_W7', 'B_h8'):
            report = reports[name][candidate]
            predictions[f'P2_{name}_{candidate}'] = report['auc_all'] > 0.9 and report['auc_class3'] > 0.75
            predictions[f'P3_{name}_{candidate}'] = report['beats_122_and_126']
    p4 = []
    for row in rows:
        if row['rule'] not in (54, 110):
            continue
        for cfg in CONFIGS:
            rec = row['configurations'][cfg['name']]
            for w in WIDTHS:
                p4.append(rec['retention'][str(w)]['retention'] > 0 and rec['retention'][str(w)]['score'] > 0)
            for h in HISTORIES:
                pred = rec['prediction'][str(h)]
                p4.append(pred['score'] > 0 and all(d['predictive_gain'] > 0 for d in pred['directions']))
    predictions['P4_all_prespecified_positivity'] = all(p4)
    expanded = {}
    for cfg in CONFIGS:
        name = cfg['name']
        expanded[name] = {}
        for label, key, param in [('A_W7','retention','7'), ('B_h8','prediction','8')]:
            scores = {row['rule']: row['configurations'][name][key][param]['score'] for row in rows}
            expanded[name][label] = rank_report(scores, classes, positives=(41,54,106,110), exclude=())
    result = dict(schema_version=1, status='complete', evidence='exploratory',
                  implementation_commit=execution['implementation_commit'], source_hashes=execution['source_hashes'],
                  configurations=CONFIGS, widths=WIDTHS, histories=HISTORIES, rings=RINGS,
                  independent_positive_families=2, symmetry_families=88,
                  labels=labels, class_by_representative={str(k):v for k,v in classes.items()},
                  reports=reports, component_ablations=ablations, predictions=predictions,
                  expanded_iv_convention=expanded, controls=json.loads((out/'controls.json').read_text()),
                  execution=execution, per_rule=rows)
    write_json(result_path, result)
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--self-test', action='store_true')
    ap.add_argument('--run', action='store_true')
    ap.add_argument('--summarize', action='store_true')
    ap.add_argument('--out', default=str(ROOT/'experiments/class4_independent_20260915/run'))
    ap.add_argument('--result', default=str(ROOT/'results/class4_independent_20260915.json'))
    ap.add_argument('--implementation-commit')
    ap.add_argument('--wall-seconds', type=int, default=1800)
    args = ap.parse_args()
    if args.self_test:
        print(json.dumps(self_test(), sort_keys=True))
    if args.run:
        if not args.implementation_commit:
            ap.error('--run requires --implementation-commit')
        run(args.out, args.implementation_commit, args.wall_seconds)
    if args.summarize:
        result = summarize(args.out, args.result)
        print(json.dumps(dict(reports=result['reports'], predictions=result['predictions']), sort_keys=True))
    if not (args.self_test or args.run or args.summarize):
        ap.error('select --self-test, --run, or --summarize')


if __name__ == '__main__':
    main()
