"""Exact invariant-column search for the fixed Research-012 2D interpreter.

Protocol: docs/research/protocols/column-compatibility-20260908.md.
The all-height result uses a finite graph of local row-type constraints;
finite trajectories validate it and separately measure physical damage.
No Wolfram classes are loaded. All numeric counts are exhaustive, scoped
counts, not independent statistical samples.
"""
from collections import deque
from pathlib import Path
import csv
import hashlib
import json
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from groovy.ca import apply_rule
from verify_dimensional_lift import local as previous_local, step as previous_step

STEM = ROOT / "results/column_compatibility_20260908"
CHECKS = {}


def count(name, value=1):
    CHECKS[name] = CHECKS.get(name, 0) + int(value)


def bits(values, width):
    return ((np.asarray(values, dtype=np.uint64)[..., None]
             >> np.arange(width, dtype=np.uint64)) & 1).astype(np.uint8)


def column_bits(value, height):
    # Python integers also cover graph witnesses taller than 64 rows.
    return np.array([(value >> y) & 1 for y in range(height)], dtype=np.uint8)


def pack(values):
    return sum(int(v) << i for i, v in enumerate(values))


def step2(grid, shrink=False):
    """Batch synchronous 2D update; last axes are y,x. No per-cell Python loop."""
    m, n = grid.shape[-2:]
    if shrink:
        c = grid[..., 1:-1, 1:-1].astype(np.int64)
        population = grid[..., 1:-1, :-2] + grid[..., 1:-1, 2:]
        yy, xx = np.indices((m-2, n-2)) + 1
    else:
        c = grid.astype(np.int64)
        population = np.roll(grid, 1, axis=-1) + np.roll(grid, -1, axis=-1)
        yy, xx = np.indices((m, n))
    yi = (yy + 2*c - 1) % m
    xi = (xx + population.astype(np.int64) - 1) % n
    index = (yi*n + xi).reshape(grid.shape[:-2] + (-1,))
    return np.take_along_axis(grid.reshape(grid.shape[:-2] + (-1,)), index,
                              axis=-1).reshape(c.shape)


def step1(states, rule):
    q = 4*np.roll(states, 1, axis=-1) + 2*states + np.roll(states, -1, axis=-1)
    return ((rule >> q) & 1).astype(np.uint8)


def encode(states, m, a, b):
    zero, one = column_bits(a, m), column_bits(b, m)
    return np.where(states[..., None, :], one[:, None], zero[:, None]).astype(np.uint8)


def primitive(m, a, b):
    aa, bb = column_bits(a, m), column_bits(b, m)
    for p in range(1, m+1):
        if m % p == 0 and np.array_equal(aa, np.tile(aa[:p], m//p)) and np.array_equal(bb, np.tile(bb[:p], m//p)):
            return p, pack(aa[:p]), pack(bb[:p])
    raise AssertionError("Missing primitive period")


def rule_reflect(r):
    return sum(((r >> (4*(q&1) + (q&2) + (q>>2))) & 1) << q for q in range(8))


def rule_complement(r):
    return sum((1-((r >> (7-q)) & 1)) << q for q in range(8))


def rule_orbit(r):
    return min(r, rule_reflect(r), rule_complement(r), rule_reflect(rule_complement(r)))


def canonical(m, a, b, k, r):
    m, a, b = primitive(m, a, b)
    aa, bb = column_bits(a, m), column_bits(b, m)
    variants = []
    for transform in [False, True]:
        x, y = (1-aa[::-1], 1-bb[::-1]) if transform else (aa, bb)
        rr = rule_reflect(r) if transform else r
        for shift in range(m):
            xx, yy = pack(np.roll(x, shift)), pack(np.roll(y, shift))
            variants.extend([(m, xx, yy, k, rr), (m, yy, xx, k, rule_complement(rr))])
    return min(variants)


def classify_columns(m, a, b, k):
    width = 2*k+1
    windows = bits(np.arange(2**width), width)
    field = encode(windows, m, a, b)
    for _ in range(k):
        field = step2(field)
    out = field[..., k]
    is_a = (out == column_bits(a, m)).all(axis=-1)
    is_b = (out == column_bits(b, m)).all(axis=-1)
    bad = np.flatnonzero(~(is_a | is_b))
    record = dict(m=m, a=a, b=b, k=k, primitive_m=primitive(m,a,b)[0],
                  physical_flips=(a^b).bit_count(), rule=-1, off_code=int(len(bad)),
                  outer_conflicts=0, witness_input=-1, witness_other=-1, witness_output=-1)
    if len(bad):
        i = int(bad[0])
        record.update(witness_input=i, witness_output=pack(out[i]))
        return record
    q = 4*windows[:,k-1] + 2*windows[:,k] + windows[:,k+1]
    representatives = [int(np.flatnonzero(q==j)[0]) for j in range(8)]
    lut = is_b[representatives]
    conflicts = np.flatnonzero(is_b != lut[q])
    record['outer_conflicts'] = int(len(conflicts))
    if len(conflicts):
        i = int(conflicts[0])
        record.update(witness_input=i, witness_other=representatives[int(q[i])],
                      witness_output=pack(out[i]))
    else:
        record['rule'] = pack(lut)
    return record


def row_constraints(k):
    """tag=-2: constant row valid for any r; -1: impossible; otherwise unique r."""
    width = 2*k+1
    inputs = bits(np.arange(2**width), width)
    q = 4*inputs[:,k-1] + 2*inputs[:,k] + inputs[:,k+1]
    representatives = [int(np.flatnonzero(q==j)[0]) for j in range(8)]
    tags = np.full(4**width, -1, dtype=np.int16)
    for start in range(0, len(tags), 64):
        ids = np.arange(start, min(start+64, len(tags)), dtype=np.uint64)
        types = ((ids[:,None] >> (2*np.arange(width,dtype=np.uint64))) & 3).astype(np.uint8)
        field = (types[:,None,:,None] >> inputs[None,:,None,:]) & 1
        for _ in range(k):
            field = step2(field, shrink=True)
        response = field[:,:,0,0]
        for i, word in enumerate(ids):
            center = int(types[i,k])
            if center in [0,3]:
                if np.all(response[i] == center//3):
                    tags[int(word)] = -2
            else:
                decoded = response[i] ^ (center==1)
                lut = decoded[representatives]
                if np.array_equal(decoded, lut[q]):
                    tags[int(word)] = pack(lut)
        count('local_vertical_horizontal_windows', len(ids)*len(inputs))
    return tags


def components(adj, reverse):
    """Iterative Kosaraju, avoiding recursion limits for 4096 graph vertices."""
    seen = set()
    order = []
    for root in range(len(adj)):
        if root in seen:
            continue
        seen.add(root)
        stack = [(root,iter(adj[root]))]
        while stack:
            v, children = stack[-1]
            try:
                w = next(children)
            except StopIteration:
                order.append(v)
                stack.pop()
                continue
            if w not in seen:
                seen.add(w)
                stack.append((w,iter(adj[w])))
    labels = [-1]*len(adj)
    label = 0
    for root in reversed(order):
        if labels[root] >= 0:
            continue
        labels[root] = label
        stack = [root]
        while stack:
            for w in reverse[stack.pop()]:
                if labels[w] < 0:
                    labels[w] = label
                    stack.append(w)
        label += 1
    return labels


def graph_decision(tags, k, rule):
    size = 4**(2*k)
    words = np.flatnonzero((tags == -2) | (tags == rule)).tolist()
    variable = [e for e in words if ((e >> (2*k)) & 3) in [1,2]]
    record = dict(k=k, rule=rule, vertices=size, allowed_edges=len(words),
                  variable_edges=len(variable), admitted=False, cycle_m=0)
    if not variable:
        return record, None
    adj, rev = [[] for _ in range(size)], [[] for _ in range(size)]
    for e in words:
        source, target = e % size, e//4
        adj[source].append(target)
        rev[target].append(source)
    for neighbors in adj:
        neighbors.sort()
    labels = components(adj, rev)
    candidates = [e for e in variable if labels[e%size] == labels[e//4]]
    if not candidates:
        return record, None
    first = candidates[0]
    source, target = first % size, first//4
    parents = {target: None}
    todo = deque([target])
    while source not in parents:
        v = todo.popleft()
        for w in adj[v]:
            if labels[w] == labels[source] and w not in parents:
                parents[w] = v
                todo.append(w)
    path = [source]
    while path[-1] != target:
        path.append(parents[path[-1]])
    path.reverse()
    edges = [first]
    for v,w in zip(path,path[1:]):
        edge = v + (w//(size//4))*size
        assert edge//4 == w and (tags[edge] in [-2, rule])
        edges.append(edge)
    row_types = [(e >> (2*k)) & 3 for e in edges]
    a, b = pack([v&1 for v in row_types]), pack([v>>1 for v in row_types])
    m = len(row_types)
    assert a != b
    direct = classify_columns(m,a,b,k)
    assert direct['rule'] == rule, (record, row_types, direct)
    count('graph_cycle_direct_checks')
    record.update(admitted=True,cycle_m=m)
    return record, dict(m=m,a=a,b=b,k=k,rule=rule,row_types=row_types,cycle_edges=edges)


def graph_rule_for_code(m,a,b,k,tags):
    row_types = [((a>>y)&1) + 2*((b>>y)&1) for y in range(m)]
    forced = set()
    for y in range(m):
        word = sum(row_types[(y+i-k)%m] << (2*i) for i in range(2*k+1))
        tag = int(tags[word])
        if tag == -1:
            return -1
        if tag >= 0:
            forced.add(tag)
    return next(iter(forced)) if len(forced)==1 else -1


def verify_engines():
    for z in range(512):
        patch = bits(z,9).reshape(3,3)
        assert step2(patch)[1,1] == previous_local(patch)
        assert np.array_equal(step2(patch),previous_step(patch))
    count('previous_interpreter_local_patches',512)
    count('previous_interpreter_complete_grids',512)
    for n in [5,7]:
        states = bits(np.arange(2**n),n)
        for rule in range(256):
            expected = np.stack([apply_rule(s,rule) for s in states])
            assert np.array_equal(step1(states,rule),expected)
            count('package_eca_state_checks',len(states))


def probe_codes(selected):
    rows, witnesses = [], {}
    for index,(m,a,b,k,r) in enumerate(sorted(selected)):
        for n in [5,7]:
            states = bits(np.arange(2**n),n)
            natural, flipped = states.copy(), states.copy()
            flipped[:,0] ^= 1
            expected_natural, expected_flipped = [], []
            for _ in range(5):
                expected_natural.append(encode(natural,m,a,b))
                expected_flipped.append(encode(flipped,m,a,b))
                natural, flipped = step1(natural,r),step1(flipped,r)
            for expected in [expected_natural,expected_flipped]:
                field = expected[0].copy()
                for h in range(1,5):
                    for _ in range(k):
                        field = step2(field)
                    assert np.array_equal(field,expected[h])
                    count('matched_trajectory_state_checks',len(states))
            for y in range(m):
                damaged = expected_natural[0].copy()
                damaged[:,y,0] ^= 1
                initial_valid = None
                for h in range(5):
                    zero = (damaged == column_bits(a,m)[None,:,None]).all(axis=-2)
                    one = (damaged == column_bits(b,m)[None,:,None]).all(axis=-2)
                    valid = (zero|one).all(axis=-1)
                    same = (damaged == expected_natural[h]).all(axis=(-2,-1))
                    same_flip = (damaged == expected_flipped[h]).all(axis=(-2,-1))
                    if h==0:
                        initial_valid = valid.copy()
                    rows.append(dict(m=m,a=a,b=b,k=k,rule=r,n=n,damaged_row=y,h=h,
                                     states=len(states),valid=int(valid.sum()),
                                     same_natural=int(same.sum()),same_matched_flip=int(same_flip.sum()),
                                     reentered=int((valid & ~initial_valid).sum())))
                    key = 'reentered_changed' if np.any(valid & ~initial_valid & ~same) else 'reentered_undamaged'
                    mask = valid & ~initial_valid & (~same if key=='reentered_changed' else same)
                    if h and key not in witnesses and mask.any():
                        i = int(np.flatnonzero(mask)[0])
                        witnesses[key] = dict(m=m,a=a,b=b,k=k,rule=r,n=n,damaged_row=y,
                            h=h,initial=i,decoded=pack(one[i]),natural=pack((expected_natural[h][i]==column_bits(b,m)[:,None]).all(axis=0)),
                            damaged_rows=[pack(row) for row in damaged[i]])
                    if h<4:
                        for _ in range(k):
                            damaged = step2(damaged)
            if n==5:
                mask = column_bits(a^b,m)
                for word in range(8):
                    logical = states.copy()
                    physical = encode(logical,m,a,b)
                    for j in range(3):
                        if (word>>j)&1:
                            logical[:,0] ^= 1
                            physical[:,:,0] ^= mask
                        logical = step1(logical,r)
                        for _ in range(k):
                            physical = step2(physical)
                        assert np.array_equal(physical,encode(logical,m,a,b))
                        count('action_word_state_checks',len(states))
        if index % 25 == 0:
            print(f'Probes {index+1}/{len(selected)}',flush=True)
    return rows,witnesses


def write_json(suffix,obj):
    Path(str(STEM)+suffix+'.json').write_text(json.dumps(obj,indent=2)+'\n')


def write_csv(suffix,rows):
    with Path(str(STEM)+suffix+'.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)


def main():
    started = time.time()
    verify_engines()
    tags_by_k, graph_rows, graph_witnesses = {}, [], []
    for k in [1,2,3]:
        tags = row_constraints(k)
        tags_by_k[k] = tags
        for r in range(256):
            row,witness = graph_decision(tags,k,r)
            graph_rows.append(row)
            if witness:
                graph_witnesses.append(witness)
        admitted=[row['rule'] for row in graph_rows if row['k']==k and row['admitted']]
        print(f'All-height graph k={k}: {admitted}',flush=True)
    rows = []
    for m in range(1,7):
        for a in range(2**m):
            for b in range(2**m):
                if a==b:
                    continue
                for k in [1,2,3]:
                    row=classify_columns(m,a,b,k)
                    assert row['rule'] == graph_rule_for_code(m,a,b,k,tags_by_k[k])
                    count('finite_code_graph_agreements')
                    rows.append(row)
        print(f'Finite height {m} complete',flush=True)
    by_key={(v['m'],v['a'],v['b'],v['k']):v for v in rows}
    accepted=[v for v in rows if v['rule']>=0]
    for v in accepted:
        m,a,b,k,r=[v[key] for key in ['m','a','b','k','rule']]
        assert by_key[(m,b,a,k)]['rule']==rule_complement(r)
        aa,bb=column_bits(a,m),column_bits(b,m)
        for shift in range(m):
            assert by_key[(m,pack(np.roll(aa,shift)),pack(np.roll(bb,shift)),k)]['rule']==r
            assert by_key[(m,pack(np.roll(1-aa[::-1],shift)),pack(np.roll(1-bb[::-1],shift)),k)]['rule']==rule_reflect(r)
            count('encoding_symmetry_checks',2)
        count('encoding_symmetry_checks')
    assert by_key[(1,0,1,1)]['rule']==232
    selected={(v['m'],v['a'],v['b'],v['k'],v['rule']) for v in accepted if v['m']==v['primitive_m'] and v['m']<=3}
    for k in [1,2,3]:
        for r in range(256):
            choices=[v for v in accepted if v['k']==k and v['rule']==r]
            if choices:
                v=min(choices,key=lambda v:(v['m'],v['a'],v['b']))
                selected.add((v['m'],v['a'],v['b'],k,r))
            else:
                choices=[v for v in graph_witnesses if v['k']==k and v['rule']==r]
                if choices:
                    v=choices[0];selected.add((v['m'],v['a'],v['b'],k,r))
    damage, damage_witnesses=probe_codes(selected)
    census=[]
    for m in range(1,7):
        for k in [1,2,3]:
            group=[v for v in rows if v['m']==m and v['k']==k]
            good=[v for v in group if v['rule']>=0]
            census.append(dict(m=m,k=k,candidates=len(group),accepted=len(good),
                off_code=sum(v['off_code']>0 for v in group),
                outer_context=sum(v['off_code']==0 and v['rule']<0 for v in group),
                rules=sorted({v['rule'] for v in good}),
                primitive_codes=sum(v['primitive_m']==m for v in good)))
    minimal=[]
    for k in [1,2,3]:
        for r in sorted({v['rule'] for v in accepted if v['k']==k}):
            v=min((v for v in accepted if v['k']==k and v['rule']==r),key=lambda v:(v['m'],v['a'],v['b']))
            minimal.append(v)
    rejected={}
    for category,predicate in [('off_code',lambda v:v['off_code']>0),('outer_context',lambda v:v['off_code']==0 and v['rule']<0)]:
        choices=[v for v in rows if predicate(v)]
        if choices:rejected[category]=choices[0]
    summary=dict(census=census,total_candidates=len(rows),accepted=len(accepted),
        canonical_encodings=len({canonical(v['m'],v['a'],v['b'],v['k'],v['rule']) for v in accepted}),
        admitted_by_k={str(k):[v['rule'] for v in graph_rows if v['k']==k and v['admitted']] for k in [1,2,3]},
        rule_symmetry_orbits=sorted({rule_orbit(v['rule']) for v in graph_rows if v['admitted']}),
        minimal_codes=minimal,probe_codes=[list(v) for v in sorted(selected)],damage_rows=len(damage))
    write_csv('',rows);write_csv('_graph',graph_rows);write_csv('_damage',damage)
    write_json('_constraints',{str(k):tags.tolist() for k,tags in tags_by_k.items()})
    write_json('_witnesses',dict(graph_cycles=graph_witnesses,rejected=rejected,damage=damage_witnesses))
    write_json('_summary',summary)
    write_json('_metadata',dict(checks=CHECKS,seconds=round(time.time()-started,3),numpy=np.__version__,
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        protocol_sha256=hashlib.sha256((ROOT/'docs/research/protocols/column-compatibility-20260908.md').read_bytes()).hexdigest(),
        scope='All periodic column heights, cadences 1..3, fixed Research-012 interpreter; physical damage is finite n=5/7, four coarse steps.'))
    print(json.dumps(dict(admitted=summary['admitted_by_k'],candidates=len(rows),accepted=len(accepted),
        canonical=summary['canonical_encodings'],probe_codes=len(selected),checks=CHECKS),indent=2),flush=True)


if __name__=='__main__':
    main()
