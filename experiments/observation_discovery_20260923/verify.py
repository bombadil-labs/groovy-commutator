#!/usr/bin/env python3
"""Same-author scalar certificate audit; does not import the producing runner."""
import hashlib
import itertools
import json
from pathlib import Path
import signal
import sys
import time

ROOT = Path(__file__).resolve().parents[2]


def step(row, rule):
    return {x: (rule >> (4*row[x-1]+2*row[x]+row[x+1])) & 1
            for x in sorted(row) if x-1 in row and x+1 in row}


def g(row, rule):
    nxt = step(row, rule)
    nxt2 = step(nxt, rule)
    d = {x: row[x] ^ nxt[x] for x in nxt}
    ed = step(d, rule)
    return {x: nxt[x] ^ nxt2[x] ^ ed[x] for x in nxt2}


def features():
    return ([[(0,x)] for x in range(-3,4)] +
            [[(0,x),(0,x+1)] for x in range(-3,3)] +
            [[(0,-1),(0,1)]] + [[(-1,x)] for x in range(-1,2)] +
            [[(-1,x),(0,x)] for x in range(-1,2)])


def rows_for(rule):
    out = []
    for n in range(512):
        past = {x: (n >> (x+4)) & 1 for x in range(-4,5)}
        now = step(past, rule)
        nxt = step(now, rule)
        fs = []
        for operands in features():
            value = 0
            for t,x in operands: value ^= (past if t == -1 else now)[x]
            fs.append(value)
        out.append({'seed': n, 'base': now[0] if rule == 90 else g(now,rule)[0],
                    'target': nxt[0] if rule == 90 else g(nxt,rule)[0],
                    'features': sum(v << i for i,v in enumerate(fs)),
                    'now': [now[x] for x in range(-3,4)]})
    return out


def ordered(raw=False):
    choices = tuple(range(7))+(14,15,16) if raw else tuple(range(20))
    fs = features()
    candidates = []
    for k in range(8):
        for ids in itertools.combinations(choices,k):
            operands = set(op for i in ids for op in fs[i])
            order = (k,len(operands),sum(t == -1 for t,x in operands),
                     sum(len(fs[i]) == 2 for i in ids),ids)
            candidates.append((order,sum(2**i for i in ids)))
    return sorted(candidates)


def conflict(rows,mask):
    seen = {}
    for a,row in enumerate(rows):
        key = (row['base'],row['features'] & mask)
        if key not in seen: seen[key] = a
        elif rows[seen[key]]['target'] != row['target']: return [seen[key],a]
    return None


def table(rows,ids):
    lut = {}
    for row in rows:
        address = row['base']
        for j,i in enumerate(ids): address |= ((row['features'] >> i) & 1) << (j+1)
        key = str(address)
        assert key not in lut or lut[key] == row['target']
        lut[key] = row['target']
    return lut


def check_costs(c,ids,rule,rows):
    fs = features()
    operands = set(op for i in ids for op in fs[i])
    all_ops = operands | ({(0,x) for x in range(-2,3)} if rule == 30 else {(0,0)})
    expected = {'selected_bits':len(ids),'retained_bits_including_base':1+len(ids),
                'feature_operands':[list(v) for v in sorted(operands)],
                'all_raw_operands':[list(v) for v in sorted(all_ops)],
                'raw_read_count_including_base':len(all_ops),
                'past_buffer_cells':sum(t == -1 for t,x in all_ops),
                'feature_xors':sum(len(fs[i]) == 2 for i in ids),
                'base_rule_evaluations':5 if rule == 30 else 0,
                'base_xors':5 if rule == 30 else 0,
                'reachable_lut_entries':len(table(rows,ids)),
                'dense_lut_address_capacity':2**(1+len(ids))}
    assert c == expected


def audit(data):
    for path,digest in data['source_hashes'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == digest, path
    assert [c['rule'] for c in data['cases']] == [90,30]
    assert len(data['grammar']) == 20
    for i,item in enumerate(data['grammar']):
        assert item['id'] == i and item['operands'] == [list(op) for op in features()[i]]
    full, raw = ordered(), ordered(True)
    for case in data['cases']:
        rule = case['rule']; rows = rows_for(rule)
        assert rows == case['rows'], 'scalar cone disagrees with producer'
        arms = case['arms']; guided = arms['guided']; witnesses = guided['witnesses']
        for w in witnesses:
            a,b = w['pair']; mask = w['candidate_mask']
            assert 0 <= a < b < 512
            assert rows[a]['base'] == rows[b]['base']
            assert rows[a]['target'] != rows[b]['target']
            diff = rows[a]['features'] ^ rows[b]['features']
            assert diff == w['distinguish_mask'] and mask & diff == 0
            assert full[w['candidate_rank']][1] == mask
            assert conflict(rows,mask) == [a,b]
        # Replay guided decisions: every skipped candidate has an earlier exact
        # witness; every oracle call and the winner are accounted for in order.
        wi = calls = pruned = comparisons = 0
        stop = guided['winner']['rank'] if guided['winner'] else len(full)-1
        for rank,(cost,mask) in enumerate(full[:stop+1]):
            reject = False
            for w in witnesses[:wi]:
                comparisons += 1
                if not mask & w['distinguish_mask']:
                    reject = True; pruned += 1; break
            if reject: continue
            calls += 1
            if wi < len(witnesses) and witnesses[wi]['candidate_rank'] == rank:
                wi += 1
            else:
                assert rank == stop and guided['winner'] and conflict(rows,mask) is None
        assert wi == len(witnesses)
        assert (calls,pruned,comparisons) == (guided['full_oracle_calls'],guided['pruned'],guided['witness_comparisons'])
        assert arms['scan']['winner'] == guided['winner']
        for name,arm in arms.items():
            cs = raw if name == 'raw' else full
            assert arm['candidate_count'] == len(cs)
            winner = arm['winner']; end = winner['rank'] if winner else len(cs)-1
            assert arm['visited'] == end+1
            assert arm['status'] == ('success' if winner else 'bounded_exhaustion')
            if name != 'guided':
                assert arm['full_oracle_calls'] == end+1 and arm['pruned'] == 0
            if name == 'raw':
                assert all(conflict(rows,mask) is not None for _,mask in cs[:end if winner else end+1])
            # For scan, the guided replay already certifies every earlier
            # candidate insufficient; do not repeat the expensive scan.
            if winner:
                cost,mask = cs[end]
                assert winner['mask'] == mask and winner['features'] == list(cost[-1])
                assert winner['cost_order'] == list(cost[:4])
                assert conflict(rows,mask) is None
                assert winner['lookup'] == table(rows,winner['features'])
                check_costs(winner['costs'],winner['features'],rule,rows)
        assert len(case['raw_windows']) == 4
        for r,w in enumerate(case['raw_windows']):
            ids = list(range(3-r,4+r)); mask = sum(1 << i for i in ids)
            pair = conflict(rows,mask)
            assert w['radius'] == r and w['mask'] == mask and w['witness'] == pair
            assert w['sufficient'] == (pair is None)
            if pair is None: check_costs(w['costs'],ids,rule,rows)
    c,t = [x['arms'] for x in data['cases']]
    cw,cr,tw,tr = [x['winner'] for x in [c['guided'],c['raw'],t['guided'],t['raw']]]
    label = lambda b: 'supported' if b else 'failed'
    expected = {'P1':label(cw is not None and cr is not None and cw['features']==[13] and len(cr['features'])>=2),
                'P2':label(len(tw['features'])<len(tr['features'])) if tw and tr else 'not_evaluated',
                'P3':label(t['guided']['full_oracle_calls']<t['scan']['full_oracle_calls']),
                'P4':label(any(i>=14 for i in tw['features'])) if tw else 'not_evaluated',
                'P5':label(t['guided']['total_seconds']<t['scan']['total_seconds'])}
    assert data['predictions'] == expected
    return {'cases':2,'local_cones':1024,'witnesses':sum(len(c['arms']['guided']['witnesses']) for c in data['cases']),
            'predictions':expected}

if __name__ == '__main__':
    signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(TimeoutError('120-second audit cap')))
    signal.alarm(120)
    start=time.perf_counter()
    result=audit(json.loads(Path(sys.argv[1]).read_text()))
    result['audit_seconds']=time.perf_counter()-start
    print(json.dumps(result,indent=2))
