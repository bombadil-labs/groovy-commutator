#!/usr/bin/env python3
"""Exact resource costs of frozen, replaceable, and revisable CA macros.

This is an oracle planning/accounting model, not a learning experiment.
The protocol is frozen in docs/research/protocols/revisable-primitives-20260907.json.
Every macro expands into primitive operations and pays their physical cost.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import itertools
import json
import platform
import sys
from collections import defaultdict
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from groovy.ca import apply_rule, apply_rule_int  # noqa: E402

ARMS = ('uncompiled', 'frozen', 'replace', 'revisable')
MACROS = [''.join(w) for w in itertools.product('AB', repeat=4)]
WORDS = [''.join(w) for h in range(9) for w in itertools.product('AB', repeat=h)]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def vector_map(n, a, b, word):
    result = []
    for s in range(1 << n):
        bits = np.array([(s >> i) & 1 for i in range(n)], dtype=np.uint8)
        for letter in word:
            bits = apply_rule(bits, a if letter == 'A' else b)
        result.append(sum(int(bit) << i for i, bit in enumerate(bits)))
    return np.array(result, dtype=np.uint16)


def encode(word, macro=None):
    """Minimum dispatch count and a tokenization; @ expands to the macro."""
    costs = [999] * (len(word) + 1)
    previous = [None] * len(costs)
    costs[0] = 0
    for i in range(len(word)):
        for token, expansion in [(word[i], word[i])] + ([('@', macro)] if macro else []):
            if word.startswith(expansion, i):
                j = i + len(expansion)
                if costs[i] + 1 < costs[j]:
                    costs[j] = costs[i] + 1
                    previous[j] = (i, token)
    tokens, j = [], len(word)
    while j:
        i, token = previous[j]
        tokens.append(token); j = i
    tokens.reverse()
    assert ''.join(macro if t == '@' else t for t in tokens) == word
    return costs[-1], tokens


def check_encoders():
    checks = 0
    for macro in MACROS:
        direct = {}
        def visit(expanded, count):
            direct[expanded] = min(count, direct.get(expanded, 999))
            for suffix in ('A', 'B', macro):
                if len(expanded) + len(suffix) <= 8:
                    visit(expanded + suffix, count + 1)
        visit('', 0)
        for word in WORDS:
            assert encode(word, macro)[0] == direct[word]
            checks += 1
    return checks


def fee(current, new, revisable):
    if current == new:
        return 0
    if not revisable:
        return 8
    return min(8, 1 + 2 * sum(x != y for x, y in zip(current, new)))


def make_kernel(n, a, b, dispatches, checks):
    states = np.arange(1 << n, dtype=np.uint16)
    maps = {letter: np.fromiter((apply_rule_int(s, n, rule) for s in states),
                                dtype=np.uint16, count=len(states))
            for letter, rule in [('A', a), ('B', b)]}
    if n == 6:
        for letter in 'AB':
            assert np.array_equal(maps[letter], vector_map(n, a, b, letter))
            checks['engine_transitions'] += len(states)
    transforms = {'': states}
    groups = defaultdict(list)
    for i, word in enumerate(WORDS):
        if word:
            transforms[word] = maps[word[-1]][transforms[word[:-1]]]
            assert np.array_equal(transforms[word], transforms[word[1:]][maps[word[0]]])
            checks['prefix_suffix_maps'] += 1
        groups[transforms[word].tobytes()].append(i)
    targets = [transforms[v + v].tobytes() for v in MACROS]
    classes = [targets.index(t) for t in targets]
    lengths = np.array([len(w) for w in WORDS], dtype=np.int16)
    issued = np.array([[encode(w, macro)[0] for w in WORDS] for macro in [None] + MACROS])
    output = []
    for d in dispatches:
        all_costs = lengths[None, :] + d * issued
        costs = np.zeros((17, 16), dtype=np.int16)
        realizations = np.zeros((17, 16), dtype=np.int16)
        for v, target in enumerate(targets):
            candidates = np.array(groups[target])
            indices = candidates[np.argmin(all_costs[:, candidates], axis=1)]
            costs[:, v] = all_costs[np.arange(17), indices]
            realizations[:, v] = indices
            assert np.all(costs[:, v] <= costs[0, v])
            if d == 0:
                assert np.all(costs[:, v] == costs[0, v])
                checks['physical_only_library_costs'] += 17
        output.append({'n': n, 'A': a, 'B': b, 'dispatch': d,
                       'target_classes': classes, 'costs': costs.tolist(),
                       'realizations': realizations.tolist()})
    return output


def comparison_totals(kernel, w, v, k, trace, pre=8):
    c = np.array(kernel['costs'])
    old = 8 + pre * int(c[w + 1, w])
    replace = np.array([fee(MACROS[w], u, False) + k * c[j + 1, v]
                        for j, u in enumerate(MACROS)])
    revise = np.array([fee(MACROS[w], u, True) + k * c[j + 1, v]
                       for j, u in enumerate(MACROS)])
    p, r = int(replace.argmin()), int(revise.argmin())
    values = {'uncompiled': pre * int(c[0, w]) + k * int(c[0, v]),
              'frozen': old + k * int(c[w + 1, v]),
              'replace': old + int(replace[p]),
              'revisable': old + trace + int(revise[r])}
    assert values['replace'] <= values['frozen']
    if trace == 0:
        assert values['revisable'] <= values['replace']
    if kernel['dispatch'] == 0:
        assert values['frozen'] == values['uncompiled'] + 8
        assert values['replace'] == values['frozen']
        assert values['revisable'] == values['frozen'] + trace
    return values, {'uncompiled': None, 'frozen': w, 'replace': p, 'revisable': r}


def plan_record(kernel, library, target):
    row = 0 if library is None else library + 1
    word = WORDS[kernel['realizations'][row][target]]
    macro = None if library is None else MACROS[library]
    dispatches, tokens = encode(word, macro)
    cost = len(word) + kernel['dispatch'] * dispatches
    assert cost == kernel['costs'][row][target]
    return {'macro': macro, 'target_word': MACROS[target] * 2,
            'expanded_word': word, 'tokens': tokens, 'physical_ticks': len(word),
            'dispatches': dispatches, 'execution_cost': cost}


def witness(kernel, w, v, k, trace, category, values, chosen):
    return {'category': category, **{key: kernel[key] for key in ('n', 'A', 'B', 'dispatch')},
            'trace': trace, 'K': k, 'W': MACROS[w], 'V': MACROS[v],
            'totals': values,
            'old_plan': plan_record(kernel, w, w),
            'new_plans': {arm: plan_record(kernel, chosen[arm], v) for arm in ARMS}}


def replay_witness(record):
    n, a, b = (record[key] for key in ('n', 'A', 'B'))
    plans = [record['old_plan']] + list(record['new_plans'].values())
    for plan in plans:
        expanded = ''.join(plan['macro'] if t == '@' else t for t in plan['tokens'])
        assert expanded == plan['expanded_word']
        assert np.array_equal(vector_map(n, a, b, expanded), vector_map(n, a, b, plan['target_word']))
        assert plan['execution_cost'] == len(expanded) + record['dispatch'] * len(plan['tokens'])
    v = record['totals']
    category = record['category']
    if category == 'revision_beats_all':
        assert all(v['revisable'] < v[x] for x in ARMS if x != 'revisable')
    if category == 'revision_loses_frozen': assert v['revisable'] > v['frozen']
    if category == 'revision_loses_replacement': assert v['revisable'] > v['replace']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--protocol', type=Path, default=ROOT / 'docs/research/protocols/revisable-primitives-20260907.json')
    parser.add_argument('--output-prefix', type=Path, default=ROOT / 'results/revisable_primitives_20260907')
    args = parser.parse_args()
    protocol = json.loads(args.protocol.read_text())
    assert protocol['macro_length'] == 4 and protocol['max_physical_ticks_per_job'] == 8
    assert protocol['compile_cost'] == protocol['replace_cost'] == protocol['prechange_jobs'] == 8
    checks = {'encodings': check_encoders(), 'engine_transitions': 0,
              'prefix_suffix_maps': 0, 'physical_only_library_costs': 0}
    kernels = []
    for n in protocol['ring_widths']:
        for a, b in protocol['rule_pairs']:
            kernels.extend(make_kernel(n, a, b, protocol['dispatch_costs'], checks))
        print(f'Kernels complete for n={n}', flush=True)
    aggregate, witnesses = {}, {}
    cases = 0
    primary = protocol['primary']
    for kernel in kernels:
        n, a, b, d = (kernel[key] for key in ('n', 'A', 'B', 'dispatch'))
        for trace in protocol['trace_reserves']:
            for k in protocol['postchange_jobs']:
                for w, old in enumerate(MACROS):
                    useful = 8 + 8 * kernel['costs'][w + 1][w] < 8 * kernel['costs'][0][w]
                    for v, new in enumerate(MACROS):
                        distance = sum(x != y for x, y in zip(old, new))
                        shift = ['unchanged', 'one_edit', 'far'][min(distance, 2)]
                        key = (n, a, b, d, trace, k, shift, int(useful))
                        if key not in aggregate:
                            aggregate[key] = dict(zip(('n','A','B','dispatch','trace','K','shift','useful_inheritance'), key))
                            row = aggregate[key]
                            row.update(cases=0, same_task_map=0, revision_changed_macro=0, replacement_changed_macro=0)
                            for arm in ARMS: row['sum_' + arm] = 0
                            for baseline in ('uncompiled','frozen','replace'):
                                for relation in ('win','tie','loss'): row[f'revision_{relation}_{baseline}'] = 0
                                row['max_saving_' + baseline] = -10**9
                                row['max_excess_' + baseline] = -10**9
                        row = aggregate[key]
                        values, chosen = comparison_totals(kernel,w,v,k,trace)
                        row['cases'] += 1; cases += 1
                        row['same_task_map'] += int(kernel['target_classes'][w] == kernel['target_classes'][v])
                        row['revision_changed_macro'] += int(chosen['revisable'] != w)
                        row['replacement_changed_macro'] += int(chosen['replace'] != w)
                        for arm in ARMS: row['sum_' + arm] += values[arm]
                        for baseline in ('uncompiled','frozen','replace'):
                            difference = values[baseline] - values['revisable']
                            relation = 'win' if difference > 0 else 'loss' if difference < 0 else 'tie'
                            row[f'revision_{relation}_{baseline}'] += 1
                            row['max_saving_' + baseline] = max(row['max_saving_' + baseline], difference)
                            row['max_excess_' + baseline] = max(row['max_excess_' + baseline], -difference)
                        if useful and (d,trace,k) == (primary['dispatch_cost'],primary['trace_reserve'],primary['postchange_jobs']):
                            categories = {
                                'revision_beats_all': all(values['revisable'] < values[arm] for arm in ARMS if arm != 'revisable'),
                                'revision_loses_frozen': values['revisable'] > values['frozen'],
                                'revision_loses_replacement': values['revisable'] > values['replace'],
                            }
                            for category, selected in categories.items():
                                if selected and category not in witnesses:
                                    witnesses[category] = witness(kernel,w,v,k,trace,category,values,chosen)
                        if d == 0 and trace == 4 and k == 4 and 'physical_only' not in witnesses:
                            witnesses['physical_only'] = witness(kernel,w,v,k,trace,'physical_only',values,chosen)
    for record in witnesses.values(): replay_witness(record)
    checks.update(witnesses_replayed=len(witnesses), policy_cases=cases, all_passed=True)
    prefix = args.output_prefix; prefix.parent.mkdir(parents=True,exist_ok=True)
    rows = list(aggregate.values())
    with prefix.with_suffix('.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    Path(str(prefix)+'_kernels.json').write_text(json.dumps({'macros':MACROS,'primitive_words':WORDS,'records':kernels},separators=(',',':'))+'\n')
    Path(str(prefix)+'_witnesses.json').write_text(json.dumps(list(witnesses.values()),indent=2)+'\n')
    metadata = {'protocol':protocol,'protocol_sha256':sha(args.protocol),'script_sha256':sha(__file__),
                'ca_engine_sha256':sha(ROOT/'src/groovy/ca.py'),'python':platform.python_version(),'numpy':np.__version__,
                'aggregate_rows':len(rows),'checks':checks,
                'interpretation':'Exact finite oracle cost model. Shared configurations are not independent statistical replicates.'}
    Path(str(prefix)+'_metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print(json.dumps({'rows':len(rows),'checks':checks},indent=2))

if __name__ == '__main__':
    main()
