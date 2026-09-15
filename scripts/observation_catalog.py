#!/usr/bin/env python3
"""Frozen observation atlas; all observations ride the same source dynamics.

The protocol, rather than this implementation, defines the scientific contract.
Scientific stages run locally. Raw arrays retain events, not just scores.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import itertools
import json
from pathlib import Path
import resource
import tarfile
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / 'experiments/observation_catalog_20260915'
NAMES = ['state','future1','future2','change1','change2','space_left',
         'space_right','space_two','move_left1','move_right1','move_left2',
         'move_right2','birth','death','sensitivity_left','sensitivity_center',
         'sensitivity_right','absential','commutator','motif000','motif010',
         'motif101','motif111','persistence']
CANDIDATES = [(i,) for i in range(24)] + list(itertools.combinations(range(24), 2))
METRICS = ['symbol_entropy','next_uncertainty','refinement_gain','spatial_information',
           'target_uncertainty','branching_mass','complementary_gain']
NATIVE = [i for i in range(24) if i not in (14,15,16,18)]
NATIVE_CANDIDATES = [c for c in CANDIDATES if all(i in NATIVE for i in c)]
PANEL = [0,4,18,30,54,90,110,124,126,137,147,193,204]
LONG_PANEL = [0,4,18,30,41,54,73,90,106,110,124,126,137,147,193,204,'radius2']
SEEDS = [2026091501,2026091502]
EPS = 1e-10


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def dump(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)+'\n')


def arrays(path, **items):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path, **items)


def budget(start):
    if time.monotonic()-start > 600:
        raise TimeoutError('600-second stage wall budget exhausted')
    if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss > 2*1024*1024:
        raise TimeoutError('2-GiB stage RSS budget exhausted')


def shift(x, offset):
    return np.roll(x, -offset, axis=-1)


def evolve(x, rule):
    if rule == 'radius2':
        return shift(x,2) ^ (shift(x,-2)&shift(x,-1)&x&shift(x,1))
    idx = 4*shift(x,-1)+2*x+shift(x,1)
    return ((int(rule) >> idx) & 1).astype(np.uint8)


def fields(x, rule=None, u=None, v=None, native=False):
    u = evolve(x,rule) if u is None else u
    v = evolve(u,rule) if v is None else v
    left,right = shift(x,-1),shift(x,1)
    out = [x,u,v,x^u,x^v,x^left,x^right,x^shift(x,2),
           x^shift(u,-1),x^shift(u,1),x^shift(v,-2),x^shift(v,2),
           (1^x)&u,x&(1^u)]
    if native:
        out += [np.zeros_like(x)]*3
    elif rule == 'radius2':
        five = [shift(x,j) for j in range(-2,3)]
        for j in (1,2,3):
            changed = [a.copy() if k==j else a for k,a in enumerate(five)]
            changed[j] ^= 1
            alt = changed[4] ^ (changed[0]&changed[1]&changed[2]&changed[3])
            out.append(u^alt)
    else:
        idx = 4*left+2*x+right
        for mask in (4,2,1):
            out.append(u ^ ((int(rule) >> (idx^mask))&1).astype(np.uint8))
    out.append((1^x)&(left|right))
    out.append(np.zeros_like(x) if native else u^v^evolve(x^u,rule))
    idx = 4*left+2*x+right
    out.extend((idx==k).astype(np.uint8) for k in (0,2,5,7))
    out.append(x&u)
    return np.stack(out)


def words(f):
    return shift(f,-1)+2*f+4*shift(f,1)


def states(width):
    return ((np.arange(1<<width,dtype=np.uint32)[:,None] >> np.arange(width))&1).astype(np.uint8)


def codes(x):
    return np.sum(x.astype(np.uint32) << np.arange(x.shape[-1]),axis=-1).astype(np.uint32)


def canon(z):
    _, first, inv = np.unique(z,return_index=True,return_inverse=True)
    order = np.argsort(first)
    remap = np.empty(len(order),np.uint16); remap[order]=np.arange(len(order))
    return remap[inv].astype(np.uint8)


def joint(w, candidate):
    return w[candidate[0]].astype(np.uint32) if len(candidate)==1 else (
        w[candidate[0]].astype(np.uint32)+8*w[candidate[1]].astype(np.uint32))


def entropy(z):
    counts = np.bincount(np.asarray(z,dtype=np.int64).ravel())
    counts = counts[counts>0]
    p = counts/counts.sum()
    return float(-np.sum(p*np.log2(p)))


def h_joint(*zs):
    combined = np.zeros(np.asarray(zs[0]).shape,np.int64)
    for z in zs:
        a = np.asarray(z,np.int64)
        combined = combined*(int(a.max())+1)+a
    return entropy(combined)


def measurements(z0,z1,z2,zright,target):
    h0,h1 = entropy(z0),entropy(z1)
    h01 = h_joint(z0,z1)
    refinement = h_joint(z1,z2)-h1-h_joint(z0,z1,z2)+h01
    pairs = np.unique(np.asarray(z0,np.int64)*64+z1)
    branches = np.bincount(pairs//64,minlength=64)>1
    return [h0,max(0.,h01-h0),max(0.,refinement),
            max(0.,h0+entropy(zright)-h_joint(z0,zright)),
            max(0.,h_joint(z0,target)-h0),float(np.mean(branches[z0])),None]


def table(w0,w1,w2,wr,target,which=None):
    which = list(range(300)) if which is None else sorted(set(which))
    required = sorted(set(which)|{i for k in which for i in CANDIDATES[k]})
    out = np.full((300,7),np.nan)
    for k in required:
        c=CANDIDATES[k]
        vals=measurements(*(joint(w,c).ravel() for w in (w0,w1,w2,wr)),target.ravel())
        out[k,:6]=vals[:6]
        if len(c)==2:
            out[k,6]=max(0.,min(out[c[0],4],out[c[1],4])-out[k,4])
    return out


def orbit(rule):
    def mirror(r):
        return sum(((r>>(((i&1)<<2)|(i&2)|((i&4)>>2)))&1)<<i for i in range(8))
    def complement(r):
        return sum((1-((r>>(7-i))&1))<<i for i in range(8))
    return sorted({rule,mirror(rule),complement(rule),mirror(complement(rule))})


def groups():
    lab=json.loads((ROOT/'experiments/on_beam_256_4d_20260914/labels.json').read_text())
    negative=sorted({min(orbit(r)) for k in ('1','2','3') for r in lab['representatives'][k]})
    return {'positive':[orbit(54),orbit(110)],'negative':[orbit(r) for r in negative],
            'disputed':[orbit(41),orbit(106)]}


def interval_report(values,lo,hi,g):
    inside=(values>=lo-EPS)&(values<=hi+EPS)
    if inside.ndim==1: inside=inside[None,:]
    return {'core_members_inside':int(inside[:,sum(g['positive'],[])].sum()),
            'core_members_total':int(inside.shape[0]*sum(map(len,g['positive']))),
            'negative_orbits_overlap':[min(o) for o in g['negative'] if np.any(inside[:,o])],
            'disputed_orbits_overlap':[min(o) for o in g['disputed'] if np.any(inside[:,o])]}


def select(metrics):
    g=groups(); positives=sum(g['positive'],[])
    rows=[]; selected=[]
    for m in range(7):
        ranks=[]
        for k in range(24 if m==6 else 0,300):
            a=metrics[:,:,k,m]
            lo,hi=float(a[:,positives].min()),float(a[:,positives].max())
            report=interval_report(a,lo,hi,g)
            spread=float(a.max()-a.min())
            normalized=round((hi-lo)/spread,12) if spread>EPS else 0.
            row={'candidate':k,'metric':m,'interval':[lo,hi],'normalized_width':normalized,**report}
            ranks.append((len(report['negative_orbits_overlap']),normalized,k,row))
            rows.append(row)
        ranks.sort(key=lambda z:z[:3]); selected.append(ranks[0][3])
    return {'groups':g,'attempted_slots':len(rows),'ranking':rows,'selected':selected}


def case(width,rule):
    x=states(width); nxt=codes(evolve(x,rule)); right=codes(shift(x,1))
    f=fields(x,rule); w=words(f)
    return table(w[:,:,0],w[:,nxt,0],w[:,nxt[nxt],0],w[:,:,1],words(evolve(x,rule))[:,0]),f,nxt,right


def alias_catalog(rule):
    # Center 5 has its complete -5..5 dependency window, independent of wrap.
    w=words(fields(states(11),rule))[:,:,5]
    by={}; aliases=[]
    for c in CANDIDATES:
        key=canon(joint(w,c)).tobytes()
        if key not in by: by[key]=len(by)
        aliases.append(by[key])
    return aliases


def discovery(unit,start):
    metrics=np.empty((2,256,300,7)); aliases=[]
    for wi,width in enumerate((7,8)):
        for rule in range(256):
            budget(start)
            m,f,nxt,right=case(width,rule); metrics[wi,rule]=m
            arrays(unit/'finite'/f'w{width}_r{rule:03d}.npz',fields=f,next_index=nxt,right_index=right)
            if wi==0: aliases.append(alias_catalog(rule))
            if rule%32==0: print('discovery',width,rule,round(time.monotonic()-start,2),flush=True)
    arrays(unit/'discovery-metrics.npz',metrics=metrics,widths=np.array([7,8]),aliases=np.array(aliases,np.uint16))
    selection=select(metrics)
    selection['input_hashes']={'discovery-metrics.npz':sha(unit/'discovery-metrics.npz')}
    selection['metric_names']=METRICS
    selection['candidate_names']=['+'.join(NAMES[i] for i in c) for c in CANDIDATES]
    dump(unit/'shortlist.json',selection)
    return {'cases':512,'nominal_observation_contracts':512*300,
            'distinct_partition_counts':[len(set(a)) for a in aliases],
            'selected':selection['selected'],'shortlist_sha256':sha(unit/'shortlist.json')}


def long_case(rule,seed,which,unit):
    rng=np.random.Generator(np.random.PCG64(seed))
    x=rng.integers(0,2,size=1021,dtype=np.uint8)
    initial=x.copy()
    for _ in range(1024): x=evolve(x,rule)
    trajectory=np.empty((1028,1021),np.uint8); trajectory[0]=x
    for t in range(1,len(trajectory)): trajectory[t]=evolve(trajectory[t-1],rule)
    f=fields(trajectory[:-2],rule,u=trajectory[1:-1],v=trajectory[2:])
    ww=words(f); sites=np.arange(8)*1021//8
    w=ww[:,:,sites]; wr=ww[:,:1024,(sites+1)%1021]
    target=words(trajectory[1:1025])[:,sites]
    out=table(w[:,:1024],w[:,1:1025],w[:,2:1026],wr,target,which)
    arrays(unit/'long'/f'r{rule}_s{seed}.npz',initial=initial,
           trajectory_bits=np.packbits(trajectory),trajectory_shape=np.array(trajectory.shape),
           words=w,right_words=wr,target=target,metrics=out,sites=sites)
    return out


def confirmation(unit,start):
    shortlist=json.loads((unit/'shortlist.json').read_text())
    seal=json.loads((unit/'confirmation-seal.json').read_text())
    assert seal['shortlist_sha256']==sha(unit/'shortlist.json')
    assert shortlist['input_hashes']['discovery-metrics.npz']==sha(unit/'discovery-metrics.npz')
    which=sorted({s['candidate'] for s in shortlist['selected']})
    metrics=np.full((256,300,7),np.nan)
    for rule in range(256):
        budget(start)
        m,f,nxt,right=case(9,rule); metrics[rule]=m
        arrays(unit/'finite'/f'w9_r{rule:03d}.npz',fields=f,next_index=nxt,right_index=right)
        if rule%32==0: print('confirmation width9',rule,round(time.monotonic()-start,2),flush=True)
    arrays(unit/'confirmation-metrics.npz',metrics=metrics)
    verdicts=[]
    for s in shortlist['selected']:
        k,m=s['candidate'],s['metric']; lo,hi=s['interval']
        verdicts.append({'candidate':k,'metric':m,'interval':[lo,hi],
                         **interval_report(metrics[:,k,m],lo,hi,shortlist['groups'])})
    longer=[]
    for rule in LONG_PANEL:
        for seed in SEEDS:
            budget(start); t=long_case(rule,seed,which,unit)
            vals=[]
            for s in shortlist['selected']:
                value=float(t[s['candidate'],s['metric']]);lo,hi=s['interval']
                vals.append({'candidate':s['candidate'],'metric':s['metric'],'value':value,
                             'inside':bool(lo-EPS<=value<=hi+EPS)})
            longer.append({'rule':rule,'seed':seed,'slots':vals})
            print('confirmation long',rule,seed,round(time.monotonic()-start,2),flush=True)
    return {'width9_cases':256,'width9':verdicts,'long_runs':longer,
            'shortlist_sha256':seal['shortlist_sha256'],'selection_commit':seal['selection_commit']}


def unpack(raw,shape):
    return np.unpackbits(np.frombuffer(base64.b64decode(raw),np.uint8))[:int(np.prod(shape))].reshape(shape)


def source_graph(x,rule):
    w=x.shape[1]; numeric=codes(x); to_order=np.empty(len(x),np.uint32)
    to_order[numeric]=np.arange(len(x)); nxt=to_order[codes(evolve(x,rule))]
    period=np.full(len(x),w,np.uint16)
    for p in range(w-1,0,-1):
        if w%p==0: period[np.all(x==shift(x,p),axis=1)]=p
    basin=np.full(len(x),-1,np.int32)
    for i in range(len(x)):
        path=[]; positions={}; j=i
        while basin[j]<0 and j not in positions:
            positions[j]=len(path);path.append(j);j=int(nxt[j])
        label=int(basin[j]) if basin[j]>=0 else min(path[positions[j]:])
        for j in path: basin[j]=label
    return nxt,period,basin


def choose2(n):
    n=np.asarray(n,np.int64); return int(np.sum(n*(n-1)//2))


def pair_groups(labels,attribute=None):
    if not len(labels): return 0
    z=labels.astype(np.int64)
    if attribute is not None: z=z*(int(attribute.max())+1)+attribute
    _,counts=np.unique(z,return_counts=True)
    return choose2(counts)


def lift_and_provenance(unit,start,archive,relation_dir):
    assert sha(archive)=='766e4db7083fbdb551bc4aee66abc554079c5d118905f6d65aa5e5372c9418d1'
    records=[]; provenance=[]
    with tarfile.open(archive,'r:gz') as tar:
        for member in tar:
            if not member.isfile() or not member.name.endswith('.json'): continue
            pieces=member.name.split('/')
            if len(pieces)!=3 or int(pieces[1][4:]) not in PANEL: continue
            d=json.load(tar.extractfile(member)); width,rule,dim=d['width'],d['rule'],d['dimension']
            if width not in (7,8) or dim not in (2,3,4): continue
            budget(start)
            grid=unpack(d['grid_bits_big'],d['grid_shape']); root=grid
            for _ in range(dim-1): root=root[:,4]^root[:,5]
            assert root.shape==(1<<width,width) and len(np.unique(codes(root)))==1<<width
            nxt,period,basin=source_graph(root,rule)
            u,v=grid[nxt],grid[nxt[nxt]]
            fw=words(fields(grid,u=u,v=v,native=True))
            rootw=words(fields(root,rule))[:,:,0]
            rootdict={}
            for k,c in enumerate(CANDIDATES):
                rootdict.setdefault(canon(joint(rootw,c)).tobytes(),[]).append(k)
            matched=[]; unmatched=0; witnesses=[]
            for phase in range(6):
                idx=(slice(None),slice(None),phase)+(0,)*(dim-2)+(0,)
                w=fw[idx]
                for c in NATIVE_CANDIDATES:
                    z=joint(w,c); key=canon(z).tobytes(); targets=rootdict.get(key,[])
                    if targets:
                        matched.append([phase,CANDIDATES.index(c),targets])
                        if len(witnesses)<4:
                            # Complete relabeling suffices to verify transition conjugacy.
                            rz=joint(rootw,CANDIDATES[targets[0]])
                            pairs=np.unique(np.stack([z,rz],axis=1),axis=0)
                            assert len(pairs)==len(np.unique(z))==len(np.unique(rz))
                            witnesses.append({'phase':phase,'native_candidate':CANDIDATES.index(c),
                                              'root_candidate':targets[0],'relabeling':pairs.tolist()})
                    else: unmatched+=1
            rr={'width':width,'rule':rule,'dimension':dim,'attempted_views':6*len(NATIVE_CANDIDATES),
                'matched_views':len(matched),'unmatched_views':unmatched,'matches':matched,
                'root_candidates_recovered':sorted({k for _,_,ks in matched for k in ks}),
                'transition_witnesses':witnesses}
            records.append(rr)
            path=relation_dir/f'w{width}_r{rule:03d}_d{dim}.npz'
            with np.load(path) as q:
                reps=q['orbit_representatives']; source=reps//(6**(dim-1))
                for contract in ('finite','full_input_d2') if dim==2 else ('finite',):
                    labels=q[contract+'_symbol'].ravel()[reps]; keep=labels>0
                    ll,ss=labels[keep],source[keep]
                    total=pair_groups(ll)
                    full=period[ss]==width
                    pr={'width':width,'rule':rule,'dimension':dim,'contract':contract,
                        'free_events':int(len(ll)),'free_pairs':total,'same_source':pair_groups(ll,ss),
                        'equal_successor':pair_groups(ll,nxt[ss]),'same_basin':pair_groups(ll,basin[ss]),
                        'both_full_period':pair_groups(ll[full]),
                        'status':'ok' if total else 'not_applicable'}
                    provenance.append(pr)
                arrays(unit/'lift'/f'w{width}_r{rule:03d}_d{dim}.npz',
                       root=root,next_index=nxt,spatial_period=period,basin=basin,
                       orbit_representatives=reps,event_source=source)
            dump(unit/'lift'/f'w{width}_r{rule:03d}_d{dim}.json',rr)
            print('lift',width,rule,dim,round(time.monotonic()-start,2),flush=True)
    assert len(records)==78 and len(provenance)==104
    return {'records':records,'provenance':provenance,'archive_sha256':sha(archive)}


def main():
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['discovery','confirmation','lift'])
    p.add_argument('--unit',type=Path,default=UNIT);p.add_argument('--archive',type=Path)
    p.add_argument('--relation-dir',type=Path)
    a=p.parse_args();start=time.monotonic();a.unit.mkdir(parents=True,exist_ok=True)
    try:
        if a.stage=='discovery': result=discovery(a.unit,start)
        elif a.stage=='confirmation': result=confirmation(a.unit,start)
        else: result=lift_and_provenance(a.unit,start,a.archive,a.relation_dir)
        budget(start);status='complete'
    except TimeoutError as e:
        result={'reason':str(e)};status='censored'
    result['status']=status
    result['source_hashes']={p:sha(ROOT/p) for p in
        ['scripts/observation_catalog.py','docs/research/protocols/observation-catalog-20260915.md',
         'experiments/on_beam_256_4d_20260914/labels.json']}
    dump(a.unit/(a.stage+'-result.json'),result)
    dump(a.unit/(a.stage+'-execution.json'),{'stage':a.stage,'status':status,
        'wall_seconds':time.monotonic()-start,'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'numpy':np.__version__,'result_sha256':sha(a.unit/(a.stage+'-result.json'))})
    print(json.dumps({'stage':a.stage,'status':status,'seconds':time.monotonic()-start}),flush=True)


if __name__=='__main__': main()
