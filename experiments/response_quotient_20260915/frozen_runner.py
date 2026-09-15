#!/usr/bin/env python3
"""Exact one-step response counts and a fixed finite completion-bank experiment."""
from __future__ import annotations
import argparse
import base64
import hashlib
import itertools
import json
from pathlib import Path
import platform
import resource
import signal
import tarfile
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = 'docs/research/protocols/response-quotient-20260915.md'
LABELS = 'experiments/on_beam_256_4d_20260914/labels.json'
SOURCE_PATHS = (PROTOCOL, LABELS, 'scripts/response_quotient_20260915.py')
WIDTHS = (7,8)
TIMES = (1,2,4,8)
POLICIES = ('no_flip','flip','output_zero','output_one','hash1701','hash1702','hash1703','hash1704')
BANKS = {'all':tuple(range(8)), 'structured':tuple(range(4)), 'hash':tuple(range(4,8))}
POSITIVES = (54,110)
DISPUTED = (41,106)
MASK64 = (1<<64)-1
EXPECTED_ARCHIVE_SHA256 = '766e4db7083fbdb551bc4aee66abc554079c5d118905f6d65aa5e5372c9418d1'


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()


def write_json(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix(path.suffix+'.tmp')
    temp.write_text(json.dumps(data,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n')
    temp.replace(path)


def labels():
    data=json.loads((ROOT/LABELS).read_text())
    result={int(r):int(c) for c,rs in data['representatives'].items() for r in rs}
    assert len(result)==88
    return result


def unpack(text,shape):
    raw=base64.b64decode(text,validate=True)
    n=int(np.prod(shape));bits=np.unpackbits(np.frombuffer(raw,dtype=np.uint8),bitorder='big')
    assert len(raw)==(n+7)//8 and not np.any(bits[n:])
    return bits[:n].reshape(shape)


def keys(grid):
    """35 physical bits, no phase, source or policy identifier in the key."""
    line=np.zeros(grid.shape,dtype=np.uint64)
    for dx in range(-2,3):line=(line<<1)|np.roll(grid,-dx,axis=-1)
    out=np.zeros(grid.shape,dtype=np.uint64)
    for dy in range(-3,4):out=(out<<5)|np.roll(line,-dy,axis=-2)
    return out


def scalar_key(grid,row,col):
    value=0
    for dy in range(-3,4):
        for dx in range(-2,3):value=(value<<1)|int(grid[(row+dy)%grid.shape[0],(col+dx)%grid.shape[1]])
    return value


def pack_states(grid):
    flat=grid.reshape(*grid.shape[:-2],-1)
    raw=np.packbits(flat,axis=-1,bitorder='little')
    padded=np.zeros((*raw.shape[:-1],8),dtype=np.uint8)
    padded[...,:raw.shape[-1]]=raw
    return padded.view('<u8')[...,0]


def unpack_states(values,width):
    bits=(values[...,None]>>np.arange(6*width,dtype=np.uint64))&1
    return bits.astype(np.uint8).reshape(*values.shape,6,width)


def forced_lookup(q,table):
    ks,vs=table
    at=np.searchsorted(ks,q);safe=np.minimum(at,len(ks)-1)
    present=(at<len(ks))&(ks[safe]==q)
    return present,vs[safe]


def off_mask(q,policy):
    if policy<2:return np.full(q.shape,policy,dtype=np.uint8)
    center=((q>>17)&1).astype(np.uint8)
    if policy<4:return center ^ np.uint8(policy-2)
    with np.errstate(over='ignore'):
        z=q+np.uint64(1701+policy-4)+np.uint64(0x9e3779b97f4a7c15)
        z=(z^(z>>30))*np.uint64(0xbf58476d1ce4e5b9)
        z=(z^(z>>27))*np.uint64(0x94d049bb133111eb)
        z=z^(z>>31)
    return (z&1).astype(np.uint8)


def scalar_off(q,policy):
    if policy<2:return policy
    if policy<4:return ((q>>17)&1)^(policy-2)
    z=(q+1701+policy-4+0x9e3779b97f4a7c15)&MASK64
    z=((z^(z>>30))*0xbf58476d1ce4e5b9)&MASK64
    z=((z^(z>>27))*0x94d049bb133111eb)&MASK64
    return (z^(z>>31))&1


def advance(grid,table):
    q=keys(grid);present,forced=forced_lookup(q,table)
    masks=np.empty(grid.shape,dtype=np.uint8)
    for policy in range(8):masks[policy]=off_mask(q[policy],policy)
    return grid ^ np.where(present,forced,masks).astype(np.uint8)


def source_successors(rule,width):
    x=((np.arange(1<<width)[:,None]>>np.arange(width-1,-1,-1))&1).astype(np.uint8)
    pat=4*np.roll(x,1,axis=-1)+2*x+np.roll(x,-1,axis=-1)
    y=((rule>>pat.astype(np.uint16))&1).astype(np.uint8)
    return (y.astype(np.uint64)*(1<<np.arange(width-1,-1,-1))).sum(axis=-1).astype(np.int64)


def read_record(raw):
    d=json.loads(raw)
    assert d['dimension']==2 and d['mode']=='jet6' and d['radii_array_order']==[3,2]
    w=d['width'];n=1<<w
    assert d['grid_shape']==[n,6,w]
    grid=unpack(d['grid_bits_big'],(n,6,w))
    source=((np.arange(n)[:,None]>>np.arange(w-1,-1,-1))&1).astype(np.uint8)
    assert np.array_equal(grid[:,4]^grid[:,5],source)
    reps=np.frombuffer(base64.b64decode(d['representative_flat_indices_u32le'],validate=True),dtype='<u4')
    q=keys(grid);ids=q.ravel()[reps]
    vals=unpack(d['forced_derivative_bits_big'],(len(reps),))
    assert len(ids)==d['forced_root_count'] and len(np.unique(ids))==len(ids)
    order=np.argsort(ids);table=(ids[order],vals[order])
    assert np.array_equal(np.unique(q),table[0])
    present,forced=forced_lookup(q,table)
    assert np.all(present)
    target=grid[source_successors(d['rule'],w)]
    assert np.array_equal(grid^forced,target)
    for policy in range(8):
        actual=grid^np.where(present,forced,off_mask(q,policy)).astype(np.uint8)
        assert np.array_equal(actual,target)
    # Equality on the complete invariant family establishes all t, not just t=1.
    return d,grid,table


def entropy(values):
    _,counts=np.unique(values,return_counts=True)
    p=counts.astype(float)/counts.sum()
    return float(-np.sum(p*np.log2(p)))


def metrics(endpoint,width,bank):
    """endpoint[policy, known probe, source]; exact finite uniform ensembles."""
    original=endpoint[np.array(bank)]
    groups={}
    for idx,array in zip(bank,original):groups.setdefault(array.tobytes(),[]).append(idx)
    classes=list(groups.values());chosen=[v[0] for v in classes]
    y=endpoint[np.array(chosen)]
    k,j,n=y.shape;assert n==1<<width
    multiplicity=(y[:,None,:,:]==y[None,:,:,:]).sum(axis=0)
    f_each=np.log2(k)-np.log2(multiplicity).mean(axis=(0,2))
    h_each=np.array([entropy(y[:,probe,:]) for probe in range(j)])
    m_each=(h_each-f_each)/width
    assert np.min(m_each)>-1e-11 and np.max(m_each)<1+1e-11
    m=float(np.clip(m_each.mean(),0,1));f=float(max(0,f_each.mean()))
    by_policy={POLICIES[idx]:float(np.mean([entropy(endpoint[idx,probe,:])/width for probe in range(j)])) for idx in bank}
    known=float(np.mean([by_policy[POLICIES[idx]] for idx in chosen]))
    assert known+1e-11>=m and f<=np.log2(len(bank))+1e-11
    return dict(score=m*f/np.log2(len(bank)),retention=m,response_bits=f,
                known_completion_retention=known,quotient_classes=classes,
                quotient_count=k,bank_size=len(bank),retention_by_probe=m_each.tolist(),
                response_bits_by_probe=f_each.tolist(),retention_by_policy=by_policy)


def ranking(scores,class_by_rule):
    negatives=[r for r in scores if r not in POSITIVES+DISPUTED]
    c3=[r for r in negatives if class_by_rule[r]==3]
    def auc(ns):return float(np.mean([float(scores[p]>scores[n])+.5*float(scores[p]==scores[n]) for p in POSITIVES for n in ns]))
    lower=min(scores[p] for p in POSITIVES)
    offenders=sorted([r for r in negatives if scores[r]>=lower],key=lambda r:(-scores[r],r))
    included=list(POSITIVES)+negatives
    return dict(auc_all=auc(negatives),auc_class3=auc(c3),
                clean_separation=not offenders,separation_margin=lower-max(scores[n] for n in negatives),
                positive_scores={str(p):scores[p] for p in POSITIVES},
                positive_ranks={str(p):1+sum(scores[r]>scores[p] for r in included)+.5*(sum(scores[r]==scores[p] for r in included)-1) for p in POSITIVES},
                negatives_at_or_above_lower_positive=[dict(rule=r,class_label=class_by_rule[r],score=scores[r]) for r in offenders],
                disputed={str(r):scores[r] for r in DISPUTED})


def summarize(rows,class_by_rule):
    reports={};predictions={}
    controls=(0,1,15,51,60,90,105,150,170,204)
    for w in WIDTHS:
        selected={r['rule']:r for r in rows if r['width']==w};assert len(selected)==88
        wr={}
        for t in TIMES:
            tr={}
            for bank in BANKS:
                vals={r:v['metrics'][str(t)][bank] for r,v in selected.items()}
                tr[bank]={field:ranking({r:v[field] for r,v in vals.items()},class_by_rule) for field in ('score','retention','response_bits')}
            wr[str(t)]=tr
        reports[str(w)]=wr
        predictions[f'P1_w{w}_unperturbed']=all(r['on_beam_control'] for r in selected.values())
        predictions[f'P2_w{w}_clean']=wr['4']['all']['score']['clean_separation']
        for bank in ('structured','hash'):predictions[f'P4_w{w}_{bank}_clean']=wr['4'][bank]['score']['clean_separation']
        for p in POSITIVES:
            for c in controls:
                predictions[f'P3_w{w}_{p}_beats_{c}']=selected[p]['metrics']['4']['all']['score']>selected[c]['metrics']['4']['all']['score']
    return reports,predictions


def self_test():
    rng=np.random.default_rng(314159)
    grid=rng.integers(0,2,(3,6,7),dtype=np.uint8);q=keys(grid)
    for b,row,col in itertools.product(range(3),range(6),range(7)):
        assert int(q[b,row,col])==scalar_key(grid[b],row,col)
        assert int((q[b,row,col]>>np.uint64(17))&np.uint64(1))==int(grid[b,row,col])
    assert np.array_equal(unpack_states(pack_states(grid),7),grid)
    values=np.array([0,1,2,(1<<35)-1,123456789],dtype=np.uint64)
    for policy in range(8):assert off_mask(values,policy).tolist()==[scalar_off(int(v),policy) for v in values]
    small=np.tile(grid[:1],(8,1,1,1));table=(np.array([q[0,0,0]],dtype=np.uint64),np.array([1],dtype=np.uint8))
    stepped=advance(small,table)
    for c,row,col in itertools.product(range(8),range(6),range(7)):
        key=scalar_key(small[c,0],row,col)
        expected=int(small[c,0,row,col])^(1 if key==int(table[0][0]) else scalar_off(key,c))
        assert int(stepped[c,0,row,col])==expected
    toykeys=np.array([0,1,1,2,0,2]);initial=np.array([1,0,1,1,0,0])
    outputs=set()
    for a,b in itertools.product((0,1),repeat=2):outputs.add(tuple(initial^np.choose(toykeys,[0,a,b])))
    assert len(outputs)==1<<len(set(toykeys)-{0})
    ident=np.tile(np.array([[[0,1]]],dtype=np.uint64),(8,1,1))
    mi=metrics(ident,1,BANKS['all']);assert mi['retention']==1 and mi['response_bits']==0 and mi['quotient_count']==1
    erased=np.arange(8,dtype=np.uint64)[:,None,None]*np.ones((8,1,2),dtype=np.uint64)
    me=metrics(erased,1,BANKS['all']);assert me['retention']==0 and me['response_bits']==3
    xor=np.array([[[0,1]],[[1,0]]],dtype=np.uint64)
    mx=metrics(xor,1,(0,1));assert mx['retention']==0 and mx['known_completion_retention']==1 and mx['response_bits']==1
    return dict(packed_vs_tuple_keys=True,fixed_completion_vs_scalar=True,
                packed_states_roundtrip=True,exact_assignment_count=True,
                identity_erasure_xor_information_controls=True)


def run(archive,out):
    start=time.perf_counter()
    def alarm(*_):raise TimeoutError('900-second scientific cap')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(900)
    out.mkdir(parents=True,exist_ok=True)
    controls=self_test();class_by_rule=labels();selected={};input_hashes={}
    archive_sha=sha(archive)
    assert archive_sha==EXPECTED_ARCHIVE_SHA256, 'Archive differs from the preserved uniform six-field cache'
    with tarfile.open(archive,'r|gz') as tf:
        for member in tf:
            if not member.isfile() or not member.name.endswith('/d2.json'):continue
            parts=member.name.split('/');w=int(parts[0][1:]);r=int(parts[1][4:])
            if w not in WIDTHS or r not in class_by_rule:continue
            raw=tf.extractfile(member).read();selected[w,r]=raw
            input_hashes[member.name]=hashlib.sha256(raw).hexdigest()
            dest=out/'inputs'/member.name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
    assert len(selected)==176
    sources={p:sha(ROOT/p) for p in SOURCE_PATHS}
    provenance=dict(source_hashes=sources,archive_sha256=archive_sha,input_record_sha256=input_hashes,
                    widths=list(WIDTHS),times=list(TIMES),policies=list(POLICIES),bank_indices=BANKS,
                    protocol_review='none at local freeze; run authorized by Myk; independent review follows',
                    python=platform.python_version(),numpy=np.__version__,budget_seconds=900)
    write_json(out/'freeze.json',provenance)
    rows=[]
    for w,r in sorted(selected):
        tick=time.perf_counter();d,beam,table=read_record(selected[w,r]);n=1<<w
        grid=np.broadcast_to(beam,(8,6,n,6,w)).copy()
        for j in range(6):grid[:,j,:,j,0]^=1
        q=keys(grid[0]);present,_=forced_lookup(q,table)
        u=np.empty((6,n),dtype=np.uint8)
        for j,s in itertools.product(range(6),range(n)):u[j,s]=len(np.unique(q[j,s][~present[j,s]]))
        assert np.max(u)<=30, 'Only five horizontal by six vertical neighborhoods can change'
        arrays={'unforced_distinct_keys':u};scored={}
        for t in range(1,9):
            grid=advance(grid,table)
            if t in TIMES:
                endpoint=pack_states(grid);arrays[f'endpoint_t{t}']=endpoint
                scored[str(t)]={name:metrics(endpoint,w,bank) for name,bank in BANKS.items()}
        rawfile=out/'endpoints'/f'w{w}_r{r:03d}.npz';rawfile.parent.mkdir(parents=True,exist_ok=True)
        np.savez_compressed(rawfile,**arrays)
        row=dict(rule=r,width=w,on_beam_control=True,forced_keys=len(table[0]),
                 exact_one_step_response_bits=dict(mean=float(u.mean()),minimum=int(u.min()),maximum=int(u.max()),
                    median=float(np.median(u)),positive_fraction=float(np.mean(u>0))),metrics=scored,
                 endpoints=dict(path=str(rawfile.relative_to(out)),sha256=sha(rawfile)),
                 input_record=f'w{w}/rule{r}/d2.json',elapsed_seconds=time.perf_counter()-tick)
        rows.append(row);write_json(out/'rules'/f'w{w}_r{r:03d}.json',row)
        write_json(out/'execution.json',dict(status='running',completed=len(rows),elapsed_seconds=time.perf_counter()-start,**provenance))
        if len(rows)%4==0:print(json.dumps(dict(completed=len(rows),total=176,width=w,rule=r,elapsed_seconds=round(time.perf_counter()-start,2))),flush=True)
    signal.alarm(0)
    execution=dict(status='complete',completed=len(rows),elapsed_seconds=time.perf_counter()-start,
                   peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,**provenance)
    write_json(out/'execution.json',execution)
    reports,predictions=summarize(rows,class_by_rule)
    result=dict(schema_version=1,status='complete',evidence='exploratory',source_hashes=sources,
                execution=execution,controls=controls,per_rule=rows,reports=reports,predictions=predictions,
                class_by_representative={str(k):v for k,v in class_by_rule.items()},
                independent_positive_representatives=list(POSITIVES),disputed_representatives=list(DISPUTED))
    write_json(ROOT/'results/response_quotient_20260915.json',result)
    print(json.dumps(dict(status='complete',seconds=execution['elapsed_seconds'],peak_rss_kib=execution['peak_rss_kib'])),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--self-test',action='store_true')
    parser.add_argument('--run',action='store_true');parser.add_argument('--archive',type=Path)
    parser.add_argument('--out',type=Path,default=ROOT/'experiments/response_quotient_20260915/run')
    args=parser.parse_args()
    if args.self_test:print(json.dumps(self_test(),sort_keys=True))
    if args.run:
        if args.archive is None:parser.error('--run needs --archive')
        run(args.archive,args.out)
