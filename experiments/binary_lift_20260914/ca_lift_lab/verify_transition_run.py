"""Check first-floor regression and apply selected 3D tables to periodic grids.

The periodic reference is separate from the causal-window compiler and lift
plugin. It evaluates the specified transition-reference construction directly.
This is an in-session check, not an independent model/research review.
"""
import argparse, hashlib, itertools, json, sqlite3
from pathlib import Path
import numpy as np
from inspect_run import table

def words(n):return np.array([[int(b) for b in format(i,f'0{n}b')] for i in range(1<<n)],dtype=np.uint8)
def primitive(source,rule):
    w=source.shape[-1];index=4*source[:,(np.arange(w)-1)%w]+2*source+source[:,(np.arange(w)+1)%w]
    return np.array([((rule^204)>>i)&1 for i in range(8)],dtype=np.uint8)[index]
def periodic(source,rule,path):
    if not path:return source
    prefix=path[:-1];choice=path[-1]
    parent=periodic(source,rule,prefix)
    source_mask=primitive(source,rule)
    derivative=source_mask if not prefix else parent^periodic(source^source_mask,rule,prefix)
    neighbor=np.take(parent,(np.arange(parent.shape[-1])+choice['shift'])%parent.shape[-1],axis=-1)
    for axis,offset in enumerate(choice['offsets'],1):
        neighbor=np.take(neighbor,(np.arange(parent.shape[axis])+offset)%parent.shape[axis],axis=axis)
    a,b={'birth':(0,1),'death':(1,1),'stay_one':(1,0),'stay_zero':(0,0)}[choice['mask']]
    reference=((parent==a)&(derivative==b)).astype(np.uint8)
    return np.stack((parent^neighbor,derivative,reference),axis=1)

def verify_periodic(db,candidate,rule,record):
    width=record['source_width'];source=words(width);path=record['recipe']
    grid=periodic(source,rule,path);source_mask=primitive(source,rule)
    following=periodic(source^source_mask,rule,path)
    parent=periodic(source,rule,path[:-1])
    parent_derivative=source_mask if len(path)==1 else parent^periodic(source^source_mask,rule,path[:-1])
    dimension=record['dimension'];neighbors=[]
    for offsets in itertools.product((0,1,-1),repeat=dimension-1):
        shifted=grid
        for axis,offset in enumerate(offsets,1):
            shifted=np.take(shifted,(np.arange(grid.shape[axis])+offset)%grid.shape[axis],axis=axis)
        for dx in (-1,0,1):
            neighbors.append(np.take(shifted,(np.arange(width)+dx)%width,axis=-1))
    observations=np.stack(neighbors,axis=-1).reshape(-1,3**dimension)
    packed=np.ascontiguousarray(np.packbits(observations,axis=1,bitorder='big'))
    keys,masks,_,names=table(db,candidate)
    dtype=np.dtype((np.void,keys.shape[1]));old=keys.view(dtype).ravel();new=packed.view(dtype).ravel()
    position=np.searchsorted(old,new)
    assert np.all(position<len(old)) and np.array_equal(old[position],new),(candidate,'unknown neighborhood')
    chosen=masks[position]
    want_source=np.broadcast_to(source.reshape((len(source),)+(1,)*(dimension-1)+(width,)),grid.shape).ravel()
    want_parent=np.broadcast_to(parent[:,None,...],grid.shape).ravel()
    want_parent_mask=np.broadcast_to(parent_derivative[:,None,...],grid.shape).ravel()
    expected={'derivative':(grid^following).ravel(),'source':want_source,'parent':want_parent,'parent_derivative':want_parent_mask}
    tasks=names if record['all_four_pass'] else ['derivative','source','parent']
    for name in tasks:
        assert np.array_equal(chosen[:,names.index(name)],1<<expected[name]),(candidate,name)
    return len(position),len(tasks)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',required=True);ap.add_argument('--baseline')
    args=ap.parse_args();root=Path(args.run);db=sqlite3.connect(root/'constraints.sqlite3')
    result={'baseline_conflict_counts':0,'periodic_candidates':0,'periodic_cells':0,'periodic_task_checks':0}
    if args.baseline:
        baseline=json.loads(Path(args.baseline).read_text())['rules']
        lookup={(r['rule'],c['sign'],c['mask']):c for r in baseline for c in r['candidates'] if c['rows'][1]=='D'}
        for rule,text in db.execute('SELECT rule,record_json FROM candidates WHERE dimension=2'):
            record=json.loads(text);choice=record['recipe'][0];old=lookup[(rule,choice['shift'],choice['mask'])]
            for mode in ('unmarked','tagged'):
                for name in ('derivative','source'):
                    assert record[mode]['tasks'][name]['conflicts']==old[mode]['tasks'][name]['conflicts']
                    result['baseline_conflict_counts']+=1
    chosen=[]
    for rule in range(256):
        for dimension in (2,3):
            candidates=db.execute('SELECT id,record_json FROM candidates WHERE rule=? AND dimension=? AND strict_pass=1 ORDER BY id',(rule,dimension)).fetchall()
            if not candidates:continue
            # For 3D check the unchanged-mask, positive transverse policy that passed all parents.
            if dimension==3:
                candidates=[(cid,text) for cid,text in candidates if (lambda p:p[-1]['geometry']=='transverse_plus' and p[-1]['mask']==p[0]['mask'])(json.loads(text)['recipe'])]
            assert candidates,rule
            cid,text=candidates[0];record=json.loads(text)
            cells,task_count=verify_periodic(db,cid,rule,record)
            result['periodic_candidates']+=1;result['periodic_cells']+=cells
            result['periodic_task_checks']+=cells*task_count
            chosen.append({'rule':rule,'dimension':dimension,'candidate_id':cid,'recipe':record['recipe']})
    policies={};strict_parents=set();parents_with_child=set()
    for cid,rule,ok,text in db.execute('SELECT id,rule,strict_pass,record_json FROM candidates WHERE dimension=2'):
        if ok:strict_parents.add(cid)
    for pid,rule,ok,text in db.execute('SELECT parent_id,rule,strict_pass,record_json FROM candidates WHERE dimension=3'):
        record=json.loads(text);first,last=record['recipe']
        if ok:parents_with_child.add(pid)
        for name,condition in [('unchanged_mask',first['mask']==last['mask']),('fixed_stay_one',last['mask']=='stay_one'),('fixed_stay_zero',last['mask']=='stay_zero')]:
            if condition:
                key=f'{name}/{last["geometry"]}';value=policies.setdefault(key,{'parents_tested':0,'parents_pass':0,'rules':set()})
                value['parents_tested']+=1;value['parents_pass']+=int(ok)
                if ok:value['rules'].add(rule)
    for value in policies.values():value['rules']=sorted(value['rules']);value['rule_count']=len(value['rules'])
    result['successful_parents']=len(strict_parents);result['parents_with_continuation']=len(parents_with_child)
    assert strict_parents==parents_with_child
    for sign in ('plus','minus'):
        p=policies[f'unchanged_mask/transverse_{sign}']
        assert p['parents_tested']==p['parents_pass']==len(strict_parents)
    manifest=json.loads((root/'manifest.json').read_text())
    for name,key in [('source_harness.py','harness_sha256'),('source_lift.py','lift_sha256')]:
        assert hashlib.sha256((root/name).read_bytes()).hexdigest()==manifest[key]
    result['run_source_hashes_match']=True
    (root/'checks.json').write_text(json.dumps(result,indent=2)+'\n')
    (root/'policies.json').write_text(json.dumps(policies,indent=2)+'\n')
    (root/'verified_candidates.json').write_text(json.dumps(chosen,indent=2)+'\n')
    print(json.dumps(result))

if __name__=='__main__':main()
