#!/usr/bin/env python3
"""Independent saved-count audit. No author imports, trajectories or graph replay.

Reviewer: Codex / OpenAI GPT-6 Astra, /root/discriminator_review, 2026-09-15.
Reconstruct local maps by tuple enumeration; recompute statistics using scalar
log-count expressions. Verify exact archive digests and member identities,
cross-window marginals, sources, reporting, and every original prediction.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import itertools
import json
import math
from pathlib import Path
import time
import zipfile

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "results/class4_independent_20260915.json"
RUN = ROOT / "experiments/class4_independent_20260915/run"
OUTPUT = ROOT / "review/class4_saved_counts_independent.json"
ATOL = 2e-10
checks = Counter()
max_numeric_difference = 0.0


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def same(got, expected, label):
    global max_numeric_difference
    if isinstance(expected, dict):
        assert set(got) == set(expected), (label, set(got), set(expected))
        for key, value in expected.items():
            same(got[key], value, f"{label}/{key}")
    elif isinstance(expected, list):
        assert len(got) == len(expected), label
        for index, value in enumerate(expected):
            same(got[index], value, f"{label}/{index}")
    elif isinstance(expected, (float, np.floating)):
        difference = abs(float(got) - float(expected))
        max_numeric_difference = max(max_numeric_difference, difference)
        assert math.isclose(got, expected, rel_tol=1e-11, abs_tol=ATOL), (label, got, expected)
        checks['numeric_values'] += 1
    else:
        assert got == expected, (label, got, expected)
        checks['exact_values'] += 1


def local_map_tables(rule, width):
    """Literal same-window truth maps grouped by tuple-valued endpoints."""
    blocks = list(itertools.product((0, 1), repeat=width))
    images = {}
    for left, right in itertools.product((0, 1), repeat=2):
        image = {}
        for block in blocks:
            extended = (left,) + block + (right,)
            image[block] = tuple((rule >> (4*extended[j] + 2*extended[j+1]
                                          + extended[j+2])) & 1
                                 for j in range(width))
        images[left, right] = image
    loss = [0.0] * 2**(width+2)
    residual = loss.copy()
    capacity = loss.copy()
    for external, image in images.items():
        multiplicities = Counter(image.values())
        costs = {b: math.log2(multiplicities[y]) for b, y in image.items()}
        groups = defaultdict(list)
        for block, value in costs.items():
            groups[block[:2] + block[-2:]].append(value)
        means = {q: math.fsum(v)/len(v) for q, v in groups.items()}
        sums = defaultdict(list)
        for block, value in costs.items():
            seq = (external[0],) + block + (external[1],)
            word = sum(bit * 2**j for j, bit in enumerate(seq))
            q = block[:2] + block[-2:]
            loss[word] = value
            residual[word] = means[q] - value
            capacity[word] = math.log2(len({mapping[block] for mapping in images.values()}))
            sums[q].append(residual[word])
        assert all(abs(math.fsum(v)) < 1e-10 for v in sums.values())
    mean = math.fsum(residual)/len(residual)
    sd = math.sqrt(math.fsum((x-mean)**2 for x in residual)/len(residual))
    checks['independent_local_tables'] += 1
    return loss, residual, capacity, sd


def retention(counts, table, alpha):
    loss, residual, capacity, sd = table
    total = [int(sum(row)) for row in counts]
    numerators = [math.fsum(int(c)*a for c, a in zip(row, residual))/n
                  for row, n in zip(counts, total)]
    by_seed = [0.0 if sd < 1e-12 else a/sd for a in numerators]
    mean = math.fsum(by_seed)/6
    incoming = [math.fsum(int(c)*a for c, a in zip(row, capacity))/n
                for row, n in zip(counts, total)]
    ambiguity = [math.fsum(int(c)*a for c, a in zip(row, loss))/n
                 for row, n in zip(counts, total)]
    return dict(retention=mean, retention_by_seed=by_seed,
                residual_mean=math.fsum(numerators)/6, reference_sd=sd,
                degenerate=sd < 1e-12, incoming_capacity=math.fsum(incoming)/6,
                ambiguity=math.fsum(ambiguity)/6,
                score=max(0.0, mean)*max(0.0, alpha), sample_count=sum(total))


def conditional_entropy(counts):
    # H(Y|context) = [sum n_context log n_context - sum n_joint log n_joint]/N.
    terms = []
    for row in counts:
        n = sum(map(int, row))
        if n:
            terms.append(n*math.log2(n))
        for value in row:
            c = int(value)
            if c:
                terms.append(-c*math.log2(c))
    return math.fsum(terms)/int(counts.sum())


def current_totals(counts):
    result = np.zeros((2, 2), dtype=np.int64)
    for context, row in enumerate(counts):
        result[context % 2] += row
    return result


def cross_entropy(train, test):
    terms = []
    for a, b in zip(train, test):
        log_denominator = math.log2(sum(map(int, a)) + 1)
        for x, y in zip(a, b):
            if y:
                terms.append(int(y)*(log_denominator - math.log2(int(x) + .5)))
    return math.fsum(terms)/int(test.sum())


def predictive(counts):
    directions = []
    for train_seeds, test_seeds in (([0,1,2], [3,4,5]), ([3,4,5], [0,1,2])):
        train = np.sum(counts[train_seeds], axis=0)
        test = np.sum(counts[test_seeds], axis=0)
        train_c, test_c = current_totals(train), current_totals(test)
        ce_c, ce_h = cross_entropy(train_c, test_c), cross_entropy(train, test)
        gain = ce_c-ce_h
        entropy = conditional_entropy(test)
        directions.append(dict(cross_entropy_current=ce_c, cross_entropy_history=ce_h,
                               predictive_gain=gain, innovation=entropy,
                               plugin_conditional_mi=conditional_entropy(test_c)-entropy,
                               score=4*max(0.0, gain)*entropy,
                               train_samples=int(train.sum()), test_samples=int(test.sum()),
                               train_occupied_contexts=int(sum(np.sum(train, axis=1)>0)),
                               test_occupied_contexts=int(sum(np.sum(test, axis=1)>0))))
    return dict(score=math.fsum(d['score'] for d in directions)/2,
                directions=directions,
                occupied_contexts_by_seed=[int(sum(np.sum(s, axis=1)>0)) for s in counts])


def graph_slope(graphs, maximum):
    xs = [g['n'] for g in graphs]
    ys = [math.log2(g[maximum]) for g in graphs]
    n = len(xs)
    # Algebraically equivalent OLS using uncentered scalar sufficient statistics.
    return ((n*math.fsum(x*y for x,y in zip(xs,ys)) - sum(xs)*math.fsum(ys)) /
            (n*sum(x*x for x in xs) - sum(xs)**2))


def auc(positives, negatives):
    return sum(1 if p > n else .5 if p == n else 0
               for p in positives for n in negatives)/(len(positives)*len(negatives))


def ranking(scores, classes, positives=(54,110), exclude=(41,106)):
    negatives = sorted(set(scores)-set(positives)-set(exclude))
    class3 = [r for r in negatives if classes[r] == 3]
    floor = min(scores[r] for r in positives)
    ordered = sorted(scores, key=lambda r: (-scores[r],r))
    included = [r for r in ordered if r not in exclude]
    positions = {r:i+1 for i,r in enumerate(included)}
    ranks = {str(r): math.fsum(positions[s] for s in included if scores[s]==scores[r]) /
             sum(scores[s]==scores[r] for s in included) for r in positives}
    return dict(auc_all=auc([scores[r] for r in positives], [scores[r] for r in negatives]),
                auc_class3=auc([scores[r] for r in positives], [scores[r] for r in class3]),
                positive_scores={str(r):scores[r] for r in positives}, positive_ranks=ranks,
                negatives_at_or_above_lower_positive=[dict(rule=r,score=scores[r],class_label=classes[r])
                   for r in ordered if r in negatives and scores[r]>=floor],
                clean_separation=all(scores[r]<floor for r in negatives),
                beats_122_and_126=all(scores[p]>scores[n] for p in positives for n in (122,126)),
                disputed={str(r):scores[r] for r in (41,106)},
                top20=[dict(rule=r,score=scores[r],class_label=classes[r]) for r in ordered[:20]])


def main():
    started = time.monotonic()
    original_digest = digest(RESULT)
    data = json.loads(RESULT.read_text())
    source_manifest = {}
    for path, expected in data['source_hashes'].items():
        actual = digest(ROOT/path)
        assert actual == expected, path
        source_manifest[path] = actual
    assert data['source_hashes'] == data['execution']['source_hashes']
    assert data['status'] == data['execution']['status'] == 'complete'
    same(json.loads((RUN/'execution.json').read_text()), data['execution'], 'execution')
    same(json.loads((RUN/'controls.json').read_text()), data['controls'], 'controls')
    rows = data['per_rule']
    assert [r['rule'] for r in rows] == data['execution']['completed_rules']
    assert len(rows) == 88
    assert sorted(r for row in rows for r in row['orbit']) == list(range(256))
    members = {f'spatial_w{w}' for w in (5,7,9)} | {f'temporal_h{h}' for h in (4,8,12)}
    archives = []
    by_rule = {r['rule']:r for r in rows}
    for row in rows:
        r = row['rule']
        same(json.loads((RUN/'rules'/f'r{r:03d}.json').read_text()), row, f'rulefile/{r}')
        assert [g['n'] for g in row['graphs']] == list(range(9,15))
        for g in row['graphs']:
            assert g['maximum_period'] == max(map(int,g['ordinary_spectrum']))
            assert g['maximum_shape_period'] == max(map(int,g['shape_spectrum']))
            assert sum(int(k)*v for k,v in g['ordinary_spectrum'].items()) <= g['states']
            assert sum(int(k)*v for k,v in g['shape_spectrum'].items()) <= g['rotation_classes']
            if r in (0,170,204):
                assert g['maximum_shape_period'] == 1
                assert g['maximum_period'] == (g['n'] if r == 170 else 1)
        same(graph_slope(row['graphs'],'maximum_period'),row['alpha_ordinary'],f'alphaP/{r}')
        same(graph_slope(row['graphs'],'maximum_shape_period'),row['alpha_shape'],f'alphaQ/{r}')
        tables = {w:local_map_tables(r,w) for w in (5,7,9)}
        for cfg in data['configurations']:
            name = cfg['name']; record = row['configurations'][name]
            archive = RUN/record['raw_counts']['path']
            assert digest(archive) == record['raw_counts']['sha256'], archive
            entry = dict(path=str(archive.relative_to(ROOT)), sha256=digest(archive), members={})
            with zipfile.ZipFile(archive) as z:
                assert set(z.namelist()) == {m+'.npy' for m in members}
                assert z.testzip() is None
                for member in sorted(z.namelist()):
                    entry['members'][member] = hashlib.sha256(z.read(member)).hexdigest()
            with np.load(archive,allow_pickle=False) as z:
                arrays = {k:z[k] for k in z.files}
            for key,array in arrays.items():
                assert array.dtype == np.int64 and np.all(array>=0), (r,name,key)
                assert np.all(array.reshape(6,-1).sum(axis=1)==cfg['n']*cfg['steps'])
            for w in (5,7,9):
                array=arrays[f'spatial_w{w}']
                assert array.shape == (6,2**(w+2))
                same(retention(array,tables[w],row['alpha_shape']),record['retention'][str(w)],f'R/{r}/{name}/{w}')
                checks['retention_records'] += 1
            for h in (4,8,12):
                array=arrays[f'temporal_h{h}']
                assert array.shape == (6,2**(h+1),2)
                same(predictive(array),record['prediction'][str(h)],f'B/{r}/{name}/{h}')
                checks['history_records'] += 1
            for small,large in ((5,7),(7,9)):
                source=arrays[f'spatial_w{large}']; target=arrays[f'spatial_w{small}']
                marginal=np.zeros_like(target)
                for code in range(source.shape[1]):
                    marginal[:,(code>>1)&(2**(small+2)-1)] += source[:,code]
                assert np.array_equal(marginal,target),(r,name,'spatial marginal',small)
                checks['cross_window_marginals'] += 1
            for small,large in ((4,8),(8,12)):
                source=arrays[f'temporal_h{large}']; target=arrays[f'temporal_h{small}']
                marginal=np.zeros_like(target)
                for context in range(source.shape[1]):
                    marginal[:,context%(2**(small+1)),:] += source[:,context,:]
                assert np.array_equal(marginal,target),(r,name,'temporal marginal',small)
                checks['cross_window_marginals'] += 1
            spatial=arrays['spatial_w7']; temporal=arrays['temporal_h8']
            spatial_ones=spatial[:,[(j>>4)&1==1 for j in range(512)]].sum(axis=1)
            temporal_ones=temporal[:,1::2,:].sum(axis=(1,2))
            assert np.array_equal(spatial_ones,temporal_ones),(r,name,'current-bit marginal')
            checks['cross_window_marginals'] += 1
            archives.append(entry)
    assert by_rule[54]['graphs'][-1]['maximum_period']==112
    assert by_rule[110]['graphs'][-1]['maximum_period']==91

    # Metrics agree above; use saved floating-point scores for exact ties in the
    # publication, preventing harmless roundoff in independent formulas changing
    # the finite-precision tie convention.
    classes={int(k):v for k,v in data['class_by_representative'].items()}
    outcomes={}; primary={}; detailed_p4=[]
    for cfg in data['configurations']:
        name=cfg['name']; primary[name]={}
        ablations={}
        for branch,params,prefix in (('retention',(5,7,9),'A_W'),('prediction',(4,8,12),'B_h')):
            for param in params:
                label=prefix+str(param)
                values={r:row['configurations'][name][branch][str(param)]['score'] for r,row in by_rule.items()}
                report=ranking(values,classes)
                same(report,data['reports'][name][label],f'report/{name}/{label}')
                checks['rank_reports']+=1
                if label in ('A_W7','B_h8'):
                    outcomes[f'P2_{name}_{label}']=report['auc_all']>.9 and report['auc_class3']>.75
                    outcomes[f'P3_{name}_{label}']=report['beats_122_and_126']
                    primary[name][label]={k:report[k] for k in ('auc_all','auc_class3','clean_separation','beats_122_and_126','negatives_at_or_above_lower_positive')}
                    same(ranking(values,classes,(41,54,106,110),()),data['expanded_iv_convention'][name][label],f'expanded/{name}/{label}')
                    checks['rank_reports']+=1
        ablations['retention_only']={r:row['configurations'][name]['retention']['7']['retention'] for r,row in by_rule.items()}
        for key in ('predictive_gain','innovation'):
            ablations[key]={r:sum(d[key] for d in row['configurations'][name]['prediction']['8']['directions'])/2 for r,row in by_rule.items()}
        for key in ('alpha_shape','alpha_ordinary'):
            ablations[key]={r:row[key] for r,row in by_rule.items()}
        for label,values in ablations.items():
            same(ranking(values,classes),data['component_ablations'][name][label],f'ablation/{name}/{label}')
            checks['rank_reports']+=1
        for r in (54,110):
            rec=by_rule[r]['configurations'][name]
            for w in (5,7,9):
                a=rec['retention'][str(w)]
                detailed_p4.append(dict(rule=r,configuration=name,candidate=f'A_W{w}',passed=a['retention']>0 and a['score']>0))
            for h in (4,8,12):
                b=rec['prediction'][str(h)]
                detailed_p4.append(dict(rule=r,configuration=name,candidate=f'B_h{h}',passed=b['score']>0 and all(d['predictive_gain']>0 for d in b['directions'])))
    outcomes['P4_all_prespecified_positivity']=all(x['passed'] for x in detailed_p4)
    same(outcomes,data['predictions'],'all predictions')
    assert digest(RESULT)==original_digest
    output=dict(status='pass',reviewer='Codex / OpenAI GPT-6 Astra /root/discriminator_review',
                reviewed_implementation=data['implementation_commit'],result_sha256=original_digest,
                verifier_sha256=digest(__file__),source_hashes=source_manifest,
                numerical_absolute_tolerance=ATOL,maximum_observed_numeric_difference=max_numeric_difference,
                counts=dict(checks),archive_count=len(archives),archive_manifest=archives,
                primary_reports=primary,predictions=outcomes,p4_detailed=detailed_p4,
                limitations=['No new trajectories or full-graph replay.',
                             'Graph spectra accepted as saved; maxima, controls and OLS slopes checked.',
                             'Exact ranking uses verified saved numeric values, retaining published float ties.'],
                elapsed_seconds=time.monotonic()-started)
    OUTPUT.write_text(json.dumps(output,sort_keys=True,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:output[k] for k in ('status','counts','archive_count','maximum_observed_numeric_difference','predictions','elapsed_seconds')},sort_keys=True))


if __name__=='__main__':
    main()
