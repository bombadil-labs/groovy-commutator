"""Exact compatible-rule inference from complete periodic spacetime panels.

No class labels. A fixed rule generates each entire path. Future equivalence
uses all next rows, with optional single cell-0 flip before evolution.
"""
from pathlib import Path
from collections import Counter
import sys,json,csv,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from groovy.ca import apply_rule
PREFIX='spacetime_provenance_20260908'
CHECKS=Counter();NODES={};EDGES={};WITNESSES=[]

def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def node(obj):
    key=digest(obj);NODES[key]=dict(id=key,**obj);return key

def engine(n):
    size=1<<n;states=np.arange(size,dtype=np.int64);rules=np.arange(256,dtype=np.int64)
    bits=(states[:,None]>>np.arange(n))&1
    q=4*np.roll(bits,1,axis=1)+2*bits+np.roll(bits,-1,axis=1)
    seen=np.bitwise_or.reduce(1<<q,axis=1)
    e=((((rules[:,None,None]>>q[None,:,:])&1)<<np.arange(n)).sum(axis=2))
    seeds=states if n==6 else np.linspace(0,size-1,32,dtype=int)
    for r in rules:
        for s in seeds:
            assert e[r,s]==int(np.dot(apply_rule(bits[s].astype(np.uint8),int(r)),1<<np.arange(n)))
            CHECKS['engine_transitions']+=1
    return e,seen

def same_partition(a,b):
    na=len(np.unique(a));nb=len(np.unique(b))
    assert na==nb==len(np.unique(a.astype(np.int64)*(int(b.max())+1)+b))
    CHECKS['direct_partition_checks']+=1

def minbits(count):return np.array([(int(x)-1).bit_length() for x in count])

def witness(name,n,t,source,e,history,mask):
    size=1<<n;r=source//size;s=source%size;rows=[int(x[source]) for x in history[:t+1]]
    m=int(mask[source]);v=r&m
    candidates=[q for q in range(256) if q&m==v]
    panel=node(dict(kind='spacetime_panel',width=n,boundary='periodic',cadence=1,bit_order='LSB is cell 0',rows=rows))
    seed=node(dict(kind='configuration',width=n,boundary='periodic',bit_order='LSB is cell 0',state=s))
    continuations=[]
    for q in candidates:
        x=s;replayed=[x]
        for _ in range(t):x=int(e[q,x]);replayed.append(x)
        assert replayed==rows;CHECKS['witness_derivations']+=1
        edge=dict(source=seed,target=panel,relation='stack_evolution',rule=q,steps=t,
                  decoder='whole periodic rows, forward time',verification='performed exhaustive-candidate replay')
        key=digest(edge);EDGES[key]=dict(id=key,**edge)
        item={'rule':q}
        for mode,flip in [('autonomous',0),('flip_cell_0',1)]:
            x=rows[-1]^flip;future=[]
            for _ in range(4):x=int(e[q,x]);future.append(x)
            item[mode]=future
        continuations.append(item)
    WITNESSES.append(dict(name=name,panel=panel,visited_mask=m,observed_rule_outputs=v,
                         candidates=candidates,continuations=continuations))

def run(n):
    size=1<<n;e,seen=engine(n);rules=np.repeat(np.arange(256),size);initial=np.tile(np.arange(size),256)
    total=len(rules);history=[initial.copy()]
    for _ in range(10):history.append(e[rules,history[-1]])
    mask=np.zeros(total,dtype=np.int64);pop=np.array([i.bit_count() for i in range(256)])
    subsets=np.arange(total) if n==6 else np.flatnonzero(np.isin(initial,[0,1,size//3,size//2,size-1]))
    rows_out=[];hist_out=[]
    for t in range(7):
        if t:
            old=mask.copy();mask|=seen[history[t-1]]
            assert np.all((mask&old)==old);CHECKS['nested_mask_cases']+=total
        values=rules&mask;key=(initial<<16)|(mask<<8)|values
        _,rep,groups,multiplicity=np.unique(key,return_index=True,return_inverse=True,return_counts=True)
        candidates=1<<(8-pop[mask[rep]])
        assert np.array_equal(candidates,multiplicity)
        assert np.all((rules&mask)==values)
        CHECKS['candidate_multiplicity_panels']+=len(rep)
        raw=np.stack(history[:t+1],axis=1)
        _,raw_labels=np.unique(raw[subsets],axis=0,return_inverse=True)
        same_partition(groups[subsets],raw_labels)
        maskbits=8-pop[mask[rep]]
        all_counts={};all_ref={};futures={}
        for mode,flip in [('autonomous',0),('flip_cell_0',1)]:
            labels=groups.copy();x=history[t]^flip;future=[]
            for h in range(1,5):
                x=e[rules,x];future.append(x.copy())
                _,child_reps,labels=np.unique((labels<<n)|x,return_index=True,return_inverse=True)
                counts=np.bincount(groups[child_reps],minlength=len(rep))
                assert np.all(counts<=candidates) and np.all(counts[candidates==1]==1)
                bits=minbits(counts);assert np.all(bits<=maskbits)
                CHECKS['future_bound_panels']+=len(rep)
                joined=np.concatenate((raw[subsets],np.stack(future,axis=1)[subsets]),axis=1)
                _,direct=np.unique(joined,axis=0,return_inverse=True)
                same_partition(labels[subsets],direct)
                all_counts[(mode,h)]=counts
                stat=dict(width=n,observed_steps=t,future_steps=h,mode=mode,source_pairs=total,panels=len(rep),
                    unique_rule_panels=int(np.sum(candidates==1)),
                    ambiguous_rule_one_future=int(np.sum((candidates>1)&(counts==1))),
                    multiple_future_panels=int(np.sum(counts>1)),
                    source_weighted_multiple_future_fraction=float(multiplicity[counts>1].sum()/total),
                    mean_candidate_rules=float(candidates.mean()),mean_rule_bits=float(maskbits.mean()),
                    mean_continuations=float(counts.mean()),max_continuations=int(counts.max()),
                    mean_future_bits=float(bits.mean()),max_future_bits=int(bits.max()),
                    more_futures_than_autonomous=0,fewer_futures_than_autonomous=0)
                if mode=='flip_cell_0':
                    reference=all_counts[('autonomous',h)]
                    stat['more_futures_than_autonomous']=int(np.sum(counts>reference))
                    stat['fewer_futures_than_autonomous']=int(np.sum(counts<reference))
                rows_out.append(stat)
                hist_out.append(dict(width=n,observed_steps=t,future_steps=h,mode=mode,
                    histogram=[dict(candidate_rules=int(a),continuations=int(b),panels=int(c))
                      for (a,b),c in sorted(Counter(zip(candidates,counts)).items())]))
        if n==6 and t==2:
            witness('zero_panel',n,t,0,e,history,mask)
            for name,predicate in [
                ('autonomous_ambiguity',all_counts[('autonomous',4)]>1),
                ('delayed_ambiguity',(all_counts[('autonomous',1)]==1)&(all_counts[('autonomous',4)]>1))]:
                choices=np.flatnonzero(predicate)
                if len(choices):witness(name,n,t,int(rep[choices[0]]),e,history,mask)
                else:WITNESSES.append(dict(name=name,absent=True))
        if n==8 and t==1:
            seed=int(np.flatnonzero(seen==255)[0]);witness('one_step_full_identification_rule_0',n,t,seed,e,history,mask)
        print('width',n,'observed',t,'panels',len(rep),flush=True)
    return rows_out,hist_out

def main():
    rows=[];hist=[]
    for n in [6,8,10]:
        a,b=run(n);rows+=a;hist+=b
    zero=next(w for w in WITNESSES if w['name']=='zero_panel')
    assert 0 in zero['candidates'] and 204 in zero['candidates']
    cont={x['rule']:x for x in zero['continuations']}
    assert cont[0]['autonomous']==cont[204]['autonomous']==[0]*4
    assert cont[0]['flip_cell_0']!=cont[204]['flip_cell_0']
    out=ROOT/'results'
    with (out/(PREFIX+'.csv')).open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    artifacts={'_histograms':hist,'_provenance':dict(schema_version=1,scope='selected witness subset; all listed derivations replayed',
               nodes=list(NODES.values()),edges=list(EDGES.values()),witnesses=WITNESSES),
               '_metadata':dict(checks=dict(CHECKS),widths=[6,8,10],observed_steps=list(range(7)),future_steps=[1,2,3,4],
                    modes=['autonomous','flip_cell_0'],aggregate_rows=len(rows),numpy=np.__version__,
                    protocol_commit='80639b11948ca39766c7a0c998f60ea885a33045',
                    protocol_sha256=hashlib.sha256((ROOT/'docs/research/protocols/spacetime-provenance-20260908.md').read_bytes()).hexdigest(),
                    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())}
    for suffix,obj in artifacts.items():(out/(PREFIX+suffix+'.json')).write_text(json.dumps(obj,indent=2)+'\n')
    print(json.dumps(artifacts['_metadata'],indent=2))
if __name__=='__main__':main()
