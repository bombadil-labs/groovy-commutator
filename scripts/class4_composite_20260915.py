#!/usr/bin/env python3
"""Prospectively fixed validation of the post-discovery C and D scores."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import platform
import resource
import signal
import time

import numpy as np
import class4_independent_20260915 as original

ROOT = original.ROOT
BASELINE = 'results/class4_independent_20260915.json'
EXPECTED_BASELINE = '30a48e9c58a28ebca45757c3467afbbb21aa7964325dbe69b71a3ef5f1b7d1a5'
EXPECTED_SCIENCE = '363c3bfa531712583a134d1056b085eaa286506ad653f4d46a8f196d6e0dc7d2'
PROTOCOL = 'docs/research/protocols/class4-composite-validation-20260915.md'
CONFIGS = (
    dict(name='validation_384', n=384, burn=1536, steps=1024,
         seeds=[7001,7002,7003,7004,7005,7006]),
    dict(name='validation_768', n=768, burn=3072, steps=1024,
         seeds=[8001,8002,8003,8004,8005,8006]),
)
SOURCES = tuple(original.SOURCE_PATHS) + (BASELINE, PROTOCOL,
                                        'scripts/class4_composite_20260915.py')


def baseline():
    assert original.sha256(ROOT/BASELINE) == EXPECTED_BASELINE
    assert original.sha256(ROOT/'scripts/class4_independent_20260915.py') == EXPECTED_SCIENCE
    return json.loads((ROOT/BASELINE).read_text())


def scores(record, alpha):
    r = max(0.0, record['retention']['7']['retention'])
    growth = max(0.0, alpha)
    b = record['prediction']['8']['score']
    a = record['retention']['7']['score']
    assert abs(a-r*growth) < 1e-12
    return dict(C=a*b, D=growth*b, A=a, B=b, R_times_B=r*b)


def self_test():
    original.self_test()
    record = dict(retention={'7':dict(retention=2.0,score=6.0)},
                  prediction={'8':dict(score=5.0)})
    assert scores(record,3.0) == dict(C=30.0,D=15.0,A=6.0,B=5.0,R_times_B=10.0)
    record['retention']['7'] = dict(retention=-2.0,score=0.0)
    assert scores(record,3.0)['C'] == 0
    assert scores(record,3.0)['D'] == 15
    baseline()
    return dict(original_controls=True, product_controls=True, pinned_inputs=True)


def run(out, implementation):
    out = Path(out)
    out.mkdir(parents=True,exist_ok=True)
    if (out/'execution.json').exists():
        raise RuntimeError('Refuse to overwrite an existing execution')
    started = time.monotonic()
    prior = baseline()
    parents = {r['rule']:r for r in prior['per_rule']}
    hashes = {p:original.sha256(ROOT/p) for p in SOURCES}
    execution = dict(status='running', implementation_commit=implementation,
                     protocol_commit='0a3639b15a1aea8d1e8f1637c0de0cc668914276',
                     source_hashes=hashes, budget_seconds=900, configurations=CONFIGS,
                     python=platform.python_version(), numpy=np.__version__, completed_rules=[])
    original.write_json(out/'execution.json',execution)
    original.write_json(out/'controls.json',self_test())
    # These products are explicitly post hoc on the original trajectory data.
    discovery = []
    for row in prior['per_rule']:
        discovery.append(dict(rule=row['rule'], configurations={
            name:scores(rec,row['alpha_shape']) for name,rec in row['configurations'].items()}))
    original.write_json(out/'discovery_products.json',discovery)
    def expired(signum,frame):
        raise TimeoutError('Composite validation hard wall expired')
    signal.signal(signal.SIGALRM,expired)
    signal.setitimer(signal.ITIMER_REAL,max(0.001,900-(time.monotonic()-started)))
    try:
        for index,r in enumerate(original.representatives()):
            tick = time.monotonic()
            alpha = parents[r]['alpha_shape']
            table = original.local_tables(r,7)
            row = dict(rule=r, orbit=original.orbit(r), alpha_shape=alpha, configurations={})
            for cfg in CONFIGS:
                series = original.trajectory(r,cfg)
                spatial = original.spatial_counts(series,cfg,7)
                temporal = original.history_counts(series,cfg,8)
                rec = dict(retention={'7':original.retention_metrics(spatial,table,alpha)},
                           prediction={'8':original.predictive_metrics(temporal)})
                rec['scores'] = scores(rec,alpha)
                raw = out/'counts'/f'r{r:03d}_{cfg["name"]}.npz'
                raw.parent.mkdir(exist_ok=True)
                np.savez_compressed(raw,spatial_w7=spatial,temporal_h8=temporal)
                rec['raw_counts'] = dict(path=str(raw.relative_to(out)),sha256=original.sha256(raw))
                row['configurations'][cfg['name']] = rec
            row['elapsed_seconds'] = time.monotonic()-tick
            original.write_json(out/'rules'/f'r{r:03d}.json',row)
            execution['completed_rules'].append(r)
            execution['elapsed_seconds'] = time.monotonic()-started
            original.write_json(out/'execution.json',execution)
            print(json.dumps(dict(completed=index+1,total=88,rule=r,
                                  elapsed=round(execution['elapsed_seconds'],2))),flush=True)
        execution['status'] = 'complete'
    except BaseException as exc:
        execution['status'] = 'censored_wall_budget' if isinstance(exc,TimeoutError) else 'failed'
        execution['error'] = dict(type=type(exc).__name__,message=str(exc))
        raise
    finally:
        signal.setitimer(signal.ITIMER_REAL,0)
        execution['elapsed_seconds'] = time.monotonic()-started
        execution['peak_rss_kib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        original.write_json(out/'execution.json',execution)


def report_one(values,classes,positives=(54,110),exclude=(41,106)):
    report = original.rank_report(values,classes,positives,exclude)
    negatives = [r for r in values if r not in positives and r not in exclude]
    report['separation_margin'] = min(values[p] for p in positives)-max(values[n] for n in negatives)
    return report


def summarize(out,result_path):
    out = Path(out)
    execution = json.loads((out/'execution.json').read_text())
    if execution['status'] != 'complete' or execution['completed_rules'] != original.representatives():
        raise RuntimeError('Refuse completed-population scoring of an incomplete run')
    for p,digest in execution['source_hashes'].items():
        assert original.sha256(ROOT/p) == digest,p
    prior = baseline()
    classes = {int(k):v for k,v in prior['class_by_representative'].items()}
    rows = [json.loads((out/'rules'/f'r{r:03d}.json').read_text()) for r in original.representatives()]
    discovery_rows = json.loads((out/'discovery_products.json').read_text())
    discovery_reports = {}
    for cfg in original.CONFIGS:
        discovery_reports[cfg['name']] = {}
        for score in ('C','D','A','B','R_times_B'):
            values = {r['rule']:r['configurations'][cfg['name']][score] for r in discovery_rows}
            discovery_reports[cfg['name']][score] = report_one(values,classes)
    reports,expanded,predictions = {},{},{}
    for cfg in CONFIGS:
        name=cfg['name']
        reports[name],expanded[name] = {},{}
        for score in ('C','D','A','B','R_times_B'):
            values = {r['rule']:r['configurations'][name]['scores'][score] for r in rows}
            reports[name][score] = report_one(values,classes)
            expanded[name][score] = report_one(values,classes,(41,54,106,110),())
        predictions[f'V1_{name}_C_clean'] = reports[name]['C']['clean_separation']
        predictions[f'V3_{name}_D_clean'] = reports[name]['D']['clean_separation']
        for score in ('C','D'):
            report = reports[name][score]
            predictions[f'V2_{name}_{score}_AUC'] = report['auc_all'] > .95 and report['auc_class3'] > .9
        positivity = []
        for row in rows:
            if row['rule'] in (54,110):
                rec = row['configurations'][name]
                positivity.append(row['alpha_shape'] > 0 and rec['retention']['7']['retention'] > 0
                    and all(d['predictive_gain'] > 0 for d in rec['prediction']['8']['directions']))
        predictions[f'V4_{name}_positivity'] = all(positivity)
    result = dict(schema_version=1,evidence='exploratory',status='complete',
                  source_hashes=execution['source_hashes'],implementation_commit=execution['implementation_commit'],
                  configurations=CONFIGS, independent_positive_families=2,
                  discovery_products_status='post_hoc',discovery_reports=discovery_reports,
                  reports=reports,expanded_iv_convention=expanded,predictions=predictions,
                  execution=execution,per_rule=rows,
                  controls=json.loads((out/'controls.json').read_text()))
    original.write_json(result_path,result)
    return result


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--self-test',action='store_true')
    ap.add_argument('--run',action='store_true')
    ap.add_argument('--summarize',action='store_true')
    ap.add_argument('--implementation-commit')
    ap.add_argument('--out',default=str(ROOT/'experiments/class4_composite_20260915/run'))
    ap.add_argument('--result',default=str(ROOT/'results/class4_composite_20260915.json'))
    args=ap.parse_args()
    if args.self_test:
        print(json.dumps(self_test(),sort_keys=True))
    if args.run:
        if not args.implementation_commit:
            ap.error('--run requires --implementation-commit')
        run(args.out,args.implementation_commit)
    if args.summarize:
        result=summarize(args.out,args.result)
        print(json.dumps(result['predictions'],sort_keys=True))
    if not (args.self_test or args.run or args.summarize):
        ap.error('select an action')


if __name__ == '__main__':
    main()
