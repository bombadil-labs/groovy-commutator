#!/usr/bin/env python3
"""Audit fresh composite counts/products with independent reviewer functions.

No scientific author imports, new trajectories, or graph replay. The imported
module is the independently authored first-stage audit, never the pilot runner.
Reviewer: Codex / OpenAI GPT-6 Astra, /root/discriminator_review, 2026-09-15.
"""
import hashlib
import json
from pathlib import Path
import time
import zipfile

import numpy as np

import class4_saved_counts_independent as independent

ROOT=Path(__file__).resolve().parents[1]
RESULT=ROOT/'results/class4_composite_20260915.json'
RUN=ROOT/'experiments/class4_composite_20260915/run'
BASELINE=ROOT/'results/class4_independent_20260915.json'
OUTPUT=ROOT/'review/class4_composite_saved_counts_independent.json'
CONFIGS=[dict(name='validation_384',n=384,burn=1536,steps=1024,
              seeds=[7001,7002,7003,7004,7005,7006]),
         dict(name='validation_768',n=768,burn=3072,steps=1024,
              seeds=[8001,8002,8003,8004,8005,8006])]


def products(record,alpha):
    retention=max(record['retention']['7']['retention'],0)
    growth=max(alpha,0)
    temporal=record['prediction']['8']['score']
    return dict(C=(retention*growth)*temporal,D=growth*temporal,
                A=retention*growth,B=temporal,R_times_B=retention*temporal)


def report(values,classes,positives=(54,110),exclude=(41,106)):
    r=independent.ranking(values,classes,positives,exclude)
    negatives=set(values)-set(positives)-set(exclude)
    r['separation_margin']=min(values[p] for p in positives)-max(values[n] for n in negatives)
    return r


def main():
    started=time.monotonic()
    data=json.loads(RESULT.read_text()); prior=json.loads(BASELINE.read_text())
    old_audit=json.loads((ROOT/'review/class4_saved_counts_independent.json').read_text())
    assert old_audit['status']=='pass'
    assert independent.digest(BASELINE)==old_audit['result_sha256']
    assert independent.digest(ROOT/'review/class4_saved_counts_independent.py')==old_audit['verifier_sha256']
    expected_digest=independent.digest(RESULT)
    source_hashes={}
    for p,h in data['source_hashes'].items():
        assert independent.digest(ROOT/p)==h,p
        source_hashes[p]=h
    assert data['source_hashes']==data['execution']['source_hashes']
    assert data['status']==data['execution']['status']=='complete'
    assert data['implementation_commit']=='1d5b726d44db8ab089b9f0b6be81492a7ee8392f'
    assert data['execution']['protocol_commit']=='0a3639b15a1aea8d1e8f1637c0de0cc668914276'
    assert data['configurations']==data['execution']['configurations']==CONFIGS
    assert data['execution']['elapsed_seconds']<data['execution']['budget_seconds']==900
    independent.same(json.loads((RUN/'execution.json').read_text()),data['execution'],'execution')
    independent.same(json.loads((RUN/'controls.json').read_text()),data['controls'],'controls')
    parent_rows={r['rule']:r for r in prior['per_rule']}
    rows={r['rule']:r for r in data['per_rule']}
    assert list(rows)==list(parent_rows)==data['execution']['completed_rules']
    assert len(rows)==88
    archives=[]
    for r,row in rows.items():
        independent.same(json.loads((RUN/'rules'/f'r{r:03d}.json').read_text()),row,f'row/{r}')
        assert row['orbit']==parent_rows[r]['orbit']
        assert row['alpha_shape']==parent_rows[r]['alpha_shape']
        table=independent.local_map_tables(r,7)
        for cfg in CONFIGS:
            name=cfg['name']; record=row['configurations'][name]
            path=RUN/record['raw_counts']['path']
            archive_digest=independent.digest(path)
            assert archive_digest==record['raw_counts']['sha256'],path
            entry=dict(path=str(path.relative_to(ROOT)),sha256=archive_digest,members={})
            with zipfile.ZipFile(path) as z:
                assert set(z.namelist())=={'spatial_w7.npy','temporal_h8.npy'}
                assert z.testzip() is None
                for member in sorted(z.namelist()):
                    entry['members'][member]=hashlib.sha256(z.read(member)).hexdigest()
            with np.load(path,allow_pickle=False) as z:
                spatial=z['spatial_w7']; temporal=z['temporal_h8']
            assert spatial.shape==(6,512) and temporal.shape==(6,512,2)
            for array in (spatial,temporal):
                assert array.dtype==np.int64 and np.all(array>=0)
                assert np.all(array.reshape(6,-1).sum(axis=1)==cfg['n']*cfg['steps'])
            independent.same(independent.retention(spatial,table,row['alpha_shape']),
                             record['retention']['7'],f'retention/{r}/{name}')
            independent.checks['retention_records']+=1
            independent.same(independent.predictive(temporal),record['prediction']['8'],f'prediction/{r}/{name}')
            independent.checks['history_records']+=1
            spatial_ones=spatial[:,[(j>>4)&1==1 for j in range(512)]].sum(axis=1)
            temporal_ones=temporal[:,1::2,:].sum(axis=(1,2))
            assert np.array_equal(spatial_ones,temporal_ones),(r,name,'current-bit marginal')
            independent.checks['current_bit_marginals']+=1
            independent.same(products(record,row['alpha_shape']),record['scores'],f'products/{r}/{name}')
            independent.checks['product_records']+=1
            archives.append(entry)
    classes={int(k):v for k,v in prior['class_by_representative'].items()}
    discovery=json.loads((RUN/'discovery_products.json').read_text())
    assert data['discovery_products_status']=='post_hoc'
    expected_discovery=[dict(rule=r,configurations={name:products(rec,row['alpha_shape'])
               for name,rec in row['configurations'].items()}) for r,row in parent_rows.items()]
    independent.same(discovery,expected_discovery,'all discovery products')
    scores=('C','D','A','B','R_times_B')
    for cfg in prior['configurations']:
        name=cfg['name']
        for label in scores:
            values={r['rule']:r['configurations'][name][label] for r in expected_discovery}
            independent.same(report(values,classes),data['discovery_reports'][name][label],f'discovery report/{name}/{label}')
            independent.checks['rank_reports']+=1
    outcomes={}; v4=[]; primary={}
    for cfg in CONFIGS:
        name=cfg['name']; reconstructed={}
        for label in scores:
            # Metrics and products have already been independently reproduced.
            # Retain saved float values for the frozen exact-tie reporting rule.
            values={r:row['configurations'][name]['scores'][label] for r,row in rows.items()}
            reconstructed[label]=report(values,classes)
            independent.same(reconstructed[label],data['reports'][name][label],f'fresh/{name}/{label}')
            independent.same(report(values,classes,(41,54,106,110),()),data['expanded_iv_convention'][name][label],f'expanded/{name}/{label}')
            independent.checks['rank_reports']+=2
        outcomes[f'V1_{name}_C_clean']=reconstructed['C']['clean_separation']
        outcomes[f'V3_{name}_D_clean']=reconstructed['D']['clean_separation']
        for label in ('C','D'):
            rr=reconstructed[label]
            outcomes[f'V2_{name}_{label}_AUC']=rr['auc_all']>.95 and rr['auc_class3']>.9
        cases=[]
        for r in (54,110):
            row=rows[r]; rec=row['configurations'][name]
            gains=[d['predictive_gain'] for d in rec['prediction']['8']['directions']]
            passed=row['alpha_shape']>0 and rec['retention']['7']['retention']>0 and all(g>0 for g in gains)
            cases.append(passed)
            v4.append(dict(rule=r,configuration=name,passed=passed,alpha=row['alpha_shape'],
                           retention=rec['retention']['7']['retention'],directional_gains=gains))
        outcomes[f'V4_{name}_positivity']=all(cases)
        primary[name]={label:{k:reconstructed[label][k] for k in ('auc_all','auc_class3',
             'clean_separation','separation_margin','positive_ranks','negatives_at_or_above_lower_positive')}
                       for label in ('C','D')}
    independent.same(outcomes,data['predictions'],'all predictions')
    assert independent.digest(RESULT)==expected_digest
    output=dict(status='pass',reviewer='Codex / OpenAI GPT-6 Astra /root/discriminator_review',
                reviewed_implementation=data['implementation_commit'],result_sha256=expected_digest,
                verifier_sha256=independent.digest(__file__),
                independent_statistics_verifier_sha256=independent.digest(independent.__file__),
                original_audit_sha256=independent.digest(ROOT/'review/class4_saved_counts_independent.json'),
                source_hashes=source_hashes,archive_count=len(archives),archive_manifest=archives,
                counts=dict(independent.checks),numerical_absolute_tolerance=independent.ATOL,
                maximum_observed_numeric_difference=independent.max_numeric_difference,
                predictions=outcomes,v4_detailed=v4,primary_reports=primary,
                elapsed_seconds=time.monotonic()-started,
                limitations=['No author functions imported; reviewer statistics functions reused.',
                             'No new trajectories or graph replay; alpha matches the audited original result.',
                             'Exact ties/rankings use verified saved floating-point values.'])
    OUTPUT.write_text(json.dumps(output,sort_keys=True,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:output[k] for k in ('status','archive_count','counts','maximum_observed_numeric_difference','predictions','elapsed_seconds')},sort_keys=True))


if __name__=='__main__':
    main()
