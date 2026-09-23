"""Finite observation grammar and exact prediction/control witnesses.

The controller is external, global, deterministic and acts once. No agency
or local-controller claim is encoded in these predicates.
"""
from collections import Counter
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
N, RULE, HORIZON = 12, 54, 4
FULL_ACTIONS = (1 << (N+1))-1
TASKS = ('predict', 'repair', 'joint')


def grammar():
    def grow(p):
        if len(p) == 8:
            yield tuple(p)
        else:
            for label in range(max(p)+2):
                yield from grow(p+[label])
    return sorted(grow([0]), key=lambda p: (len(set(p)), p))


def block_codes(s):
    return tuple((int(s) >> (3*i)) & 7 for i in range(4))


def view(p, s):
    return tuple(p[c] for c in block_codes(s))


def intersection(masks):
    common = FULL_ACTIONS
    for mask in masks:
        common &= int(mask)
    return common


def irreducible(indices, wins):
    """Inclusion-minimal empty intersection; not minimum-cardinality search."""
    kept = list(indices)
    if intersection(wins[i] for i in kept):
        raise ValueError('not a failing action intersection')
    for i in list(kept):
        rest = [j for j in kept if j != i]
        if not intersection(wins[j] for j in rest):
            kept = rest
    return kept


class Domain:
    def __init__(self):
        states = np.arange(1 << N, dtype=np.uint32)
        bits = ((states[:, None] >> np.arange(N)) & 1).astype(np.uint8)
        code = 4*np.roll(bits, 1, axis=1)+2*bits+np.roll(bits, -1, axis=1)
        out = ((RULE >> code) & 1).astype(np.uint32)
        self.step = (out * (1 << np.arange(N))).sum(1).astype(np.uint16)
        motif = np.array([0, 0, 1, 1]*3)
        self.viable = sorted({int((np.roll(motif, i)*(1 << np.arange(N))).sum())
                              for i in range(N)})
        self.member = np.isin(states, self.viable).astype(np.uint8)
        if len(self.viable) != 4 or not all(self.member[self.step[v]] for v in self.viable):
            raise AssertionError('declared organization is not invariant')
        self.actions = [0]+[1 << i for i in range(N)]
        self.states = sorted({v ^ a for v in self.viable for a in self.actions})
        self.index = {s: i for i, s in enumerate(self.states)}
        if len(self.states) != 52:
            raise AssertionError('unexpected initial domain')
        self.codes = np.array([block_codes(s) for s in self.states], dtype=np.uint8)
        future = self.member.copy()
        self.refinement_counts = [len(np.unique(future))]
        for _ in range(64):
            _, refined = np.unique(np.column_stack((future, future[self.step])),
                                   axis=0, return_inverse=True)
            count = len(np.unique(refined))
            self.refinement_counts.append(count)
            if count == self.refinement_counts[-2]:
                future = refined
                break
            future = refined
        else:
            raise TimeoutError('passive future partition did not stabilize in 64 rounds')
        _, first, inv = np.unique(future, return_index=True, return_inverse=True)
        reps = first[inv]
        if not (np.array_equal(self.member, self.member[reps]) and
                np.array_equal(future[self.step], future[self.step[reps]])):
            raise AssertionError('future partition is not forward-consistent')
        self.future = future
        evolved = states
        for _ in range(HORIZON):
            evolved = self.step[evolved]
        self.wins = [sum(1 << a for a, mask in enumerate(self.actions)
                         if self.member[evolved[s ^ mask]]) for s in self.states]
        if not all(self.wins):
            raise AssertionError('some initial state cannot be repaired with full information')

    def observations(self, p):
        labels = np.asarray(p, dtype=np.uint16)[self.codes]
        base = len(set(p))
        return (labels*np.array([base**i for i in range(4)], dtype=np.uint16)).sum(1)

    def groups(self, p):
        groups = {}
        for i, y in enumerate(self.observations(p)):
            groups.setdefault(int(y), []).append(i)
        return groups

    def first_difference(self, a, b):
        for t in range(65):
            if self.member[a] != self.member[b]:
                return t
            a, b = int(self.step[a]), int(self.step[b])
        raise AssertionError('different stable labels without bounded target witness')

    def oracle(self, p, task):
        groups = self.groups(p)
        if task in ('predict', 'joint'):
            for indices in groups.values():
                a = self.states[indices[0]]
                for i in indices[1:]:
                    b = self.states[i]
                    if self.future[a] != self.future[b]:
                        return {'kind': 'predict', 'states': [a, b],
                                'first_difference': self.first_difference(a, b)}
        if task in ('repair', 'joint'):
            for indices in groups.values():
                if not intersection(self.wins[i] for i in indices):
                    kept = irreducible(indices, self.wins)
                    return {'kind': 'repair', 'states': [self.states[i] for i in kept],
                            'winning_masks': [self.wins[i] for i in kept]}
        return None

    def validate(self, p, w):
        states = w['states']
        if len(states) < 2 or len(set(states)) != len(states) or any(s not in self.index for s in states):
            raise ValueError('invalid witness states')
        if len({view(p, s) for s in states}) != 1:
            raise ValueError('witness states are distinguishable')
        if w['kind'] == 'predict':
            if len(states) != 2 or self.future[states[0]] == self.future[states[1]]:
                raise ValueError('no passive future disagreement')
            if w['first_difference'] != self.first_difference(*states):
                raise ValueError('wrong first disagreement')
        elif w['kind'] == 'repair':
            masks = [self.wins[self.index[s]] for s in states]
            if masks != w['winning_masks'] or intersection(masks):
                raise ValueError('forged or compatible action sets')
            if any(not intersection(masks[:i]+masks[i+1:]) for i in range(len(masks))):
                raise ValueError('witness is not inclusion-minimal')
        else:
            raise ValueError('unknown witness kind')

    def policy(self, p):
        rows, flips = [], 0
        for indices in self.groups(p).values():
            common = intersection(self.wins[i] for i in indices)
            if not common:
                return None
            action = (common & -common).bit_length()-1
            rows.append({'observation': list(view(p, self.states[indices[0]])),
                         'action': action, 'states': [self.states[i] for i in indices]})
            flips += (action != 0)*len(indices)
        return {'entries': rows, 'flips_on_uniform_domain': flips,
                'state_count': len(self.states)}


def violates(p, witness):
    return len({view(p, s) for s in witness['states']}) == 1


def search(domain, ps, task):
    witnesses, rejections, queries = [], [], []
    comparisons = 0
    for i, p in enumerate(ps):
        rejection = None
        for wid, w in enumerate(witnesses):
            comparisons += 1
            if violates(p, w):
                rejection = wid
                break
        if rejection is not None:
            rejections.append([i, rejection])
            continue
        w = domain.oracle(p, task)
        queries.append(i)
        if w is None:
            return {'task': task, 'winner': i, 'encoder': list(p), 'alphabet': len(set(p)),
                    'queries': queries, 'full_oracle_calls': len(queries),
                    'witness_comparisons': comparisons, 'witnesses': witnesses,
                    'rejections': rejections, 'policy': domain.policy(p),
                    'representation': costs(domain, p)}
        domain.validate(p, w)
        w['candidate'] = i
        witnesses.append(w)
    raise AssertionError('identity did not satisfy the task')


def costs(domain, p):
    k = len(set(p))
    width = (k-1).bit_length()
    essential = [b for b in range(3) if any(p[x] != p[x ^ (1 << b)] for x in range(8))]
    policy = domain.policy(p)
    entries = len(policy['entries']) if policy else None
    return {'labels': k, 'fixed_width_observation_bits': 4*width,
            'encoder_table_bits': 8*width, 'essential_input_positions': essential,
            'straight_line_source_reads': 4*len(essential),
            'occupied_policy_entries': entries,
            'sparse_policy_key_and_action_bits': entries*(4*width+4) if policy else None,
            'controller_is_external': True, 'observation_count': 1,
            'source_cell_updates_until_endpoint': N*HORIZON}


def complete_table(domain, ps):
    flags, repair_sizes = [], Counter()
    for p in ps:
        pred = domain.oracle(p, 'predict')
        repair = domain.oracle(p, 'repair')
        flags.append([pred is None, repair is None])
        if repair is not None:
            repair_sizes[len(repair['states'])] += 1
    summary = {}
    for task in TASKS:
        accepted = [i for i, (p, r) in enumerate(flags)
                    if (p if task == 'predict' else r if task == 'repair' else p and r)]
        k = min(len(set(ps[i])) for i in accepted)
        minimum = [i for i in accepted if len(set(ps[i])) == k]
        summary[task] = {'sufficient_count': len(accepted), 'minimum_alphabet': k,
                         'all_minimum_indices': minimum}
    separation = next((i for i, (p, r) in enumerate(flags) if p and not r), None)
    lossy = next((i for i, (_, r) in enumerate(flags)
                  if r and len(domain.groups(ps[i])) < len(domain.states)), None)
    return {'encoders': [''.join(map(str, p)) for p in ps], 'flags_predict_repair': flags,
            'summary': summary,
            'prediction_without_repair': None if separation is None else {
                'index': separation, 'encoder': list(ps[separation]),
                'witness': domain.oracle(ps[separation], 'repair')},
            'lossy_repair': None if lossy is None else {
                'index': lossy, 'encoder': list(ps[lossy]), 'fiber_count': len(domain.groups(ps[lossy]))},
            'first_failing_repair_fiber_minimal_sizes': dict(sorted(repair_sizes.items()))}


def evaluate():
    domain, ps = Domain(), grammar()
    if len(ps) != 4140:
        raise AssertionError('incomplete grammar')
    searches = {task: search(domain, ps, task) for task in TASKS}
    table = complete_table(domain, ps)
    identity = tuple(range(8))
    checks = {'organization_invariant': all(domain.member[domain.step[v]] for v in domain.viable),
              'grammar_4140': len(ps) == 4140,
              'identity_predicts_and_repairs': domain.oracle(identity, 'joint') is None,
              'guided_answers_equal_full_scan': all(searches[t]['winner'] == table['summary'][t]['all_minimum_indices'][0]
                                                   for t in TASKS)}
    predictions = {
        'P1': all(checks.values()),
        'P2': table['prediction_without_repair'] is not None,
        'P3': table['summary']['joint']['minimum_alphabet'] > table['summary']['predict']['minimum_alphabet'],
        'P4': table['lossy_repair'] is not None,
        'P5': any(size > 2 for size in table['first_failing_repair_fiber_minimal_sizes'])}
    fixed = [sum(bool(w & (1 << a)) for w in domain.wins) for a in range(13)]
    return {'checks': checks, 'predictions': {k: 'supported' if v else 'failed' for k, v in predictions.items()},
            'viable_states': domain.viable, 'initial_states': domain.states,
            'successful_action_masks': domain.wins, 'refinement_class_counts': domain.refinement_counts,
            'controls': {'fixed_action_success_counts': fixed, 'best_fixed_success_count': max(fixed),
                         'noop_success_count': fixed[0], 'identity_policy': domain.policy(identity)},
            'searches': searches, 'complete_table': table}
