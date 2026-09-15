#!/usr/bin/env python3
"""Present saved atlas results; never refit selection or rerun discovery."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
UNIT=ROOT/'experiments/observation_catalog_20260915'


def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()


def read(p):return json.loads(p.read_text())


def save(p,value):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n')


def figure():
    import matplotlib
    matplotlib.use('Agg')
    matplotlib.rcParams['svg.fonttype']='none'
    matplotlib.rcParams['svg.hashsalt']='observation-catalog-20260915'
    import matplotlib.pyplot as plt
    from matplotlib.colors import Normalize
    d=np.load(UNIT/'discovery-metrics.npz')['metrics'][1]
    s=read(UNIT/'selected-shortlist.json'); names=s['candidate_names'][:24]
    short=['S','E','E2','D','D2','P−','P+','P2','M−1','M+1','M−2','M+2',
           'Birth','Death','A−','A0','A+','Abs','G','000','010','101','111','Stay']
    fig,axes=plt.subplots(1,3,figsize=(17,6.5),layout='constrained')
    import itertools
    pairs=list(itertools.combinations(range(24),2))
    matrices=[]
    for rule in (54,110,30):
        a=np.zeros((24,24))
        for k,(i,j) in enumerate(pairs,24):a[i,j]=a[j,i]=d[rule,k,6]
        matrices.append(a)
    norm=Normalize(vmin=0,vmax=max(float(a.max()) for a in matrices))
    for ax,rule,a in zip(axes,(54,110,30),matrices):
        im=ax.imshow(a,cmap='viridis',norm=norm,interpolation='nearest')
        ax.set_title(f'Rule {rule}',fontsize=14)
        ax.set_xticks(range(24),short,rotation=90,fontsize=7)
        ax.set_yticks(range(24),short,fontsize=7)
        ax.tick_params(length=0)
    fig.suptitle('Which pairs supply distinctions that either view alone loses?',fontsize=18)
    cb=fig.colorbar(im,ax=axes,shrink=.72,pad=.015)
    cb.set_label('Additional information about the same next-state patch (bits)',fontsize=10)
    fig.supxlabel('Width 8 · uniform source ensemble · 24 views and all 276 pairs\n'
                  'Larger pairs have a larger observation budget; this is not a Class-IV separation.',fontsize=10)
    out=ROOT/'results/observation_catalog_pairs_20260915.png'
    out.parent.mkdir(exist_ok=True)
    fig.savefig(out,dpi=160)
    fig.savefig(out.with_suffix('.svg'),metadata={'Date':None})
    plt.close(fig)


def summary():
    s=read(UNIT/'selected-shortlist.json');d=read(UNIT/'discovery-result.json')
    c=read(UNIT/'confirmation-result.json');l=read(UNIT/'lift-result.json')
    rows=[]
    core=[r for r in c['long_runs'] if r['rule'] in (54,110,124,137,147,193)]
    for i,(a,b) in enumerate(zip(s['selected'],c['width9'])):
        rows.append({'metric':s['metric_names'][i],'candidate':a['candidate'],
            'observation':s['candidate_names'][a['candidate']],
            'interval':a['interval'],'discovery_negative_orbits':a['negative_orbits_overlap'],
            'width9_core':[b['core_members_inside'],b['core_members_total']],
            'width9_negative_orbits':b['negative_orbits_overlap'],
            'long_core':[sum(r['slots'][i]['inside'] for r in core),len(core)],
            'long_canonical_core':[{'rule':r['rule'],'seed':r['seed'],**r['slots'][i]}
                                  for r in core if r['rule'] in (54,110)]})
    liftrows=[]
    for r in l['records']:
        liftrows.append({k:r[k] for k in ('width','rule','dimension','attempted_views',
                                        'matched_views','root_candidates_recovered')})
    paths=['scripts/observation_catalog.py','scripts/summarize_observation_catalog.py',
           'docs/research/protocols/observation-catalog-20260915.md',
           'experiments/on_beam_256_4d_20260914/labels.json',
           'review/catalog-gate1.md','review/catalog_oracle.py','review/catalog_compare.py',
           'review/catalog_period_witnesses.py','review/catalog_author_crossreview.py',
           'review/catalog-author-crossreview.json','review/catalog-verification.json',
           'review/catalog-independent-review.md']
    paths += ['experiments/observation_catalog_20260915/'+f for f in
              ('protocol-freeze.json','implementation-freeze.json','selected-shortlist.json',
               'confirmation-seal.json','discovery-result.json','discovery-execution.json',
               'confirmation-result.json','confirmation-execution.json','lift-execution.json',
               'lift-input-hashes.json','REPRODUCE.md','raw-archive.json')]
    absent=[p for p in paths if not (ROOT/p).is_file()]
    if absent:raise SystemExit('Missing review/preservation inputs: '+str(absent))
    result={'schema_version':1,'status':'complete','nominal_observations':300,
            'primitive_observations':24,'pairs':276,'attempted_measurement_slots':s['attempted_slots'],
            'negative_symmetry_families':len(s['groups']['negative']),
            'discovery_contracts':d['nominal_observation_contracts'],
            'distinct_partition_counts':d['distinct_partition_counts'],
            'slots':rows,'long_runs':c['long_runs'],'native_views':liftrows,
            'completion_provenance':l['provenance'],
            'execution':{stage:read(UNIT/(stage+'-execution.json')) for stage in ('discovery','confirmation','lift')},
            'raw_result_hashes':{stage:sha(UNIT/(stage+'-result.json')) for stage in ('discovery','confirmation','lift')},
            'source_hashes':{p:sha(ROOT/p) for p in paths}}
    save(ROOT/'results/observation_catalog_20260915.json',result)


def archive(out,source):
    assert sha(source)=='766e4db7083fbdb551bc4aee66abc554079c5d118905f6d65aa5e5372c9418d1'
    files={p.relative_to(ROOT).as_posix():p for p in UNIT.rglob('*') if p.is_file()
           and p.name!='raw-archive.json'}
    for relative in ('scripts/observation_catalog.py','scripts/summarize_observation_catalog.py',
                     'docs/research/protocols/observation-catalog-20260915.md',
                     'docs/research/2026-09-15-observation-catalog.md',
                     'experiments/on_beam_256_4d_20260914/labels.json',
                     'results/observation_catalog_pairs_20260915.png',
                     'results/observation_catalog_pairs_20260915.svg'):
        files[relative]=ROOT/relative
    for p in (ROOT/'review').glob('catalog*'):
        if p.is_file():files[p.relative_to(ROOT).as_posix()]=p
        elif p.is_dir():
            for q in p.rglob('*'):
                if q.is_file() and '__pycache__' not in q.parts:
                    files[q.relative_to(ROOT).as_posix()]=q
    files['experiments/observation_catalog_20260915/inputs/uniform_jet6_rules.tar.gz']=source
    manifest={name:{'sha256':sha(path),'bytes':path.stat().st_size} for name,path in sorted(files.items())}
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,path in sorted(files.items()):z.write(path,name)
        z.writestr('CONTENTS.json',json.dumps(manifest,sort_keys=True,indent=2)+'\n')
    record={'filename':out.name,'bytes':out.stat().st_size,'sha256':sha(out),
            'members':len(files)+1,'content_manifest_sha256':hashlib.sha256(
                (json.dumps(manifest,sort_keys=True,indent=2)+'\n').encode()).hexdigest()}
    save(UNIT/'raw-archive.json',record);print(json.dumps(record))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['figure','summary','archive'])
    p.add_argument('--out',type=Path);p.add_argument('--source',type=Path);a=p.parse_args()
    if a.mode=='figure':figure()
    elif a.mode=='summary':summary()
    else:archive(a.out,a.source)
