"""Post-enumeration independent audit; primary protocol and data stay fixed.

Boolean truth sets replace NumPy gather operations. Direct reachability
replaces strongly connected components. The conveyor construction is a
deductive follow-up prompted by the radius-failure distinction.
"""
from collections import deque
from itertools import product
from pathlib import Path
import csv
import hashlib
import json
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from experiment_column_compatibility import bits,encode,step2

STEM=ROOT/'results/column_compatibility_20260908'


def truth_tags(k):
    w=2*k+1
    full=(1<<(2**w))-1
    variables=[sum(((z>>i)&1)<<z for z in range(2**w)) for i in range(w)]
    q=[4*((z>>(k-1))&1)+2*((z>>k)&1)+((z>>(k+1))&1) for z in range(2**w)]
    rule_for_truth={sum(((r>>j)&1)<<z for z,j in enumerate(q)):r for r in range(256)}
    tags=[]
    for word in range(4**w):
        types=[(word>>(2*y))&3 for y in range(w)]
        grid=[[0 if t==0 else full if t==3 else x if t==2 else full^x
               for x in variables] for t in types]
        for _ in range(k):
            out=[]
            for y in range(1,len(grid)-1):
                row=[]
                for x in range(1,len(grid[0])-1):
                    left,c,right=grid[y][x-1:x+2]
                    n0=(full^left)&(full^right)
                    n1=left^right
                    n2=left&right
                    above=(n0&grid[y-1][x-1])|(n1&grid[y-1][x])|(n2&grid[y-1][x+1])
                    below=(n0&grid[y+1][x-1])|(n1&grid[y+1][x])|(n2&grid[y+1][x+1])
                    row.append(((full^c)&above)|(c&below))
                out.append(row)
            grid=out
        output=grid[0][0]
        center=types[k]
        if center in [0,3]:
            tag=-2 if output==(full if center==3 else 0) else -1
        else:
            tag=rule_for_truth.get(output if center==2 else full^output,-1)
        tags.append(tag)
    return tags


def step_nd(field):
    """Literal d-dimensional count/ternary-address interpreter, vectorized."""
    d=field.ndim-1
    count=np.zeros_like(field,dtype=np.int64)
    axes=tuple(range(1,d+1))
    for offset in product([-1,0,1],repeat=d):
        if any(offset):count+=np.roll(field,offset,axis=axes)
    coordinates=np.indices(field.shape)
    coordinates[0]=(coordinates[0]+2*field.astype(np.int64)-1)%field.shape[0]
    remaining=count.copy()
    for axis in range(d,0,-1):
        digit=remaining%3;remaining//=3
        coordinates[axis]=(coordinates[axis]+digit-1)%field.shape[axis]
    assert np.all(remaining==0)
    return field[tuple(coordinates)]


def main():
    saved=json.loads(Path(str(STEM)+'_constraints.json').read_text())
    graph=list(csv.DictReader(Path(str(STEM)+'_graph.csv').open()))
    checked_words=checked_paths=checked_decisions=0
    for k in [1,2,3]:
        tags=truth_tags(k)
        assert tags==saved[str(k)]
        checked_words+=len(tags)
        size=4**(2*k)
        for r in range(256):
            edges=[i for i,t in enumerate(tags) if t in [-2,r]]
            variable=[e for e in edges if ((e>>(2*k))&3) in [1,2]]
            adj={}
            for e in edges:adj.setdefault(e%size,[]).append(e//4)
            admitted=False
            for e in variable:
                source,target=e%size,e//4
                reached={target};queue=deque([target])
                while queue:
                    for v in adj.get(queue.popleft(),[]):
                        if v not in reached:reached.add(v);queue.append(v)
                admitted=admitted or source in reached
                checked_paths+=1
            original=next(x for x in graph if int(x['k'])==k and int(x['rule'])==r)
            assert admitted==(original['admitted']=='True')
            checked_decisions+=1
        print('Independent truth sets and reachability k=',k,flush=True)
    # Deductive follow-up, all-height proof belongs in the note. Repeat a
    # logical row every m>=2 rows with zero rows between. It moves one row
    # down and one cell right per tick, returning after m ticks as shift^m.
    conveyor_checks=0
    for m in range(2,10):
        for n in [5,7]:
            states=bits(np.arange(2**n),n)
            initial=encode(states,m,0,1)
            field=initial.copy()
            for t in range(1,2*m+1):
                field=step2(field)
                expected=np.roll(np.roll(initial,t,axis=-2),t,axis=-1)
                assert np.array_equal(field,expected)
                conveyor_checks+=len(states)
    dimension_checks=0
    rng=np.random.default_rng(20260908)
    for d in [2,3]:
        for m in [2,3,4]:
            for _ in range(8):
                initial=np.zeros((m,)+(3,)*d,dtype=np.uint8)
                initial[0]=rng.integers(0,2,size=(3,)*d,dtype=np.uint8)
                field=initial.copy()
                for t in range(1,2*m+1):
                    field=step_nd(field)
                    expected=np.roll(initial,(t,)*(d+1),axis=tuple(range(d+1)))
                    assert np.array_equal(field,expected)
                    dimension_checks+=1
    out=dict(independent_vertical_truth_words=checked_words,
        independent_variable_edge_return_searches=checked_paths,
        independent_rule_cadence_decisions=checked_decisions,
        conveyor_finite_state_tick_checks=conveyor_checks,
        conveyor_scope='Deductive follow-up: all m>=2; finite checks m2..9, n5/7, two vertical laps.',
        higher_dimensional_conveyor_field_ticks=dimension_checks,
        higher_dimensional_scope='Proof for every positive lower dimension; checks d2/3, transverse m2/3/4, spatial side3, eight seeded fields, two laps.',
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    Path(str(STEM)+'_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
