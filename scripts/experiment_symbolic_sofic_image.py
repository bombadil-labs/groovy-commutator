from __future__ import annotations
import argparse, hashlib, json, sys, time
from pathlib import Path
from itertools import product

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'scripts'))

from experiment_causal_witness_automaton import MDD, NodeBudgetExceeded, build_local_function, horizon_masks, PAIR_LIST, TARGETS
from experiment_causal_witness_horizon import macro_rule, FULL_CLASS
from experiment_window3_reachable_language import scan_rule as scan_research034

PROTOCOL = 'docs/research/protocols/symbolic-sofic-image-20260909.md'
HMAX = 6
NODE_BUDGET = 5_000_000
COMPARE_BUDGET = 5_000_000


class ComparisonBudgetExceeded(RuntimeError):
    pass


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def node_coord(mdd: MDD, node: int, horizon: int, delta: int) -> int | None:
    if node < 8:
        return None
    return delta + mdd.data[node][0] - horizon


def exact_equal_shifted(m1: MDD, r1: int, h1: int, m2: MDD, r2: int, h2: int, delta: int,
                        max_pairs: int = COMPARE_BUDGET):
    """Exact equality of F_h1 at 0 and F_h2 at translated site delta.

    Returns (equal, visited_pair_states, counterexample_assignment).
    Assignment keys are physical macro coordinates.
    """
    memo: dict[tuple[int, int], bool] = {}
    choice: dict[tuple[int, int], tuple[int, int, tuple[int, int]] | None] = {}

    def rec(a: int, b: int) -> bool:
        key = (a, b)
        if key in memo:
            return memo[key]
        if len(memo) >= max_pairs:
            raise ComparisonBudgetExceeded(f'comparison-state ceiling {max_pairs} exceeded')
        if a < 8 and b < 8:
            ok = a == b
            memo[key] = ok
            choice[key] = None
            return ok
        ca = node_coord(m1, a, h1, 0)
        cb = node_coord(m2, b, h2, delta)
        coord = cb if ca is None else ca if cb is None else min(ca, cb)
        ach = m1.data[a][1] if ca == coord else (a,) * 8
        bch = m2.data[b][1] if cb == coord else (b,) * 8
        for value in range(8):
            nxt = (ach[value], bch[value])
            if not rec(*nxt):
                memo[key] = False
                choice[key] = (coord, value, nxt)
                return False
        memo[key] = True
        choice[key] = None
        return True

    equal = rec(r1, r2)
    assignment = None
    if not equal:
        assignment = {}
        key = (r1, r2)
        while choice[key] is not None:
            coord, value, nxt = choice[key]
            assignment[coord] = value
            key = nxt
    return equal, len(memo), assignment


def build_h(rule: int, h: int, node_budget: int = NODE_BUDGET):
    return build_local_function(rule, h, node_budget)


def recurrence_search(rule: int, hmax: int = HMAX, node_budget: int = NODE_BUDGET,
                      compare_budget: int = COMPARE_BUDGET):
    built = {}
    records = []
    censored = None
    for h in range(hmax + 1):
        try:
            m, root, g, seconds = build_h(rule, h, node_budget)
        except NodeBudgetExceeded as exc:
            censored = {'stage': 'mdd-build', 'horizon': h, 'reason': str(exc), 'node_budget': node_budget}
            break
        built[h] = (m, root)
        records.append({'horizon': h, 'mdd_nodes': m.node_count, 'build_seconds': seconds})
        if h == 0:
            continue
        hits = []
        comparisons = []
        for j in range(h):
            m2, r2 = built[j]
            for delta in range(-(h + j), h + j + 1):
                try:
                    eq, states, assignment = exact_equal_shifted(m, root, h, m2, r2, j, delta, compare_budget)
                except ComparisonBudgetExceeded as exc:
                    censored = {'stage': 'comparison', 'horizon': h, 'j': j, 'delta': delta,
                                'reason': str(exc), 'compare_budget': compare_budget}
                    return {'rule': rule, 'wclass': FULL_CLASS[rule], 'horizons': records,
                            'recurrences': hits, 'censored': censored}
                rec = {'h': h, 'j': j, 'delta': delta, 'comparison_states': states, 'equal': eq}
                if not eq:
                    rec['counterexample_width'] = max(assignment) - min(assignment) + 1 if assignment else 0
                comparisons.append(rec)
                if eq:
                    hits.append({'h': h, 'j': j, 'delta': delta, 'comparison_states': states})
        records[-1]['comparisons'] = comparisons
        if hits:
            hits.sort(key=lambda x: (x['h'], x['j'], abs(x['delta']), x['delta']))
            return {'rule': rule, 'wclass': FULL_CLASS[rule], 'horizons': records,
                    'recurrences': hits, 'first_recurrence': hits[0], 'censored': None}
    return {'rule': rule, 'wclass': FULL_CLASS[rule], 'horizons': records,
            'recurrences': [], 'first_recurrence': None, 'censored': censored}


def eval_word(g, word, steps):
    row = list(word)
    for _ in range(steps):
        row = [int(g[64 * row[i] + 8 * row[i + 1] + row[i + 2]]) for i in range(len(row) - 2)]
    return row


def rule5_exhaustive_control():
    g = macro_rule(5)
    checked = 0
    started = time.perf_counter()
    for word in product(range(8), repeat=7):
        h3 = eval_word(g, word, 3)[0]
        h1 = int(g[64 * word[2] + 8 * word[3] + word[4]])
        if h3 != h1:
            return {'ok': False, 'checked': checked + 1, 'counterexample': list(word), 'h3': h3, 'h1': h1}
        checked += 1
    return {'ok': True, 'checked': checked, 'seconds': time.perf_counter() - started}


def controls():
    r5 = recurrence_search(5, 3)
    hits = {(x['h'], x['j'], x['delta']) for x in r5.get('recurrences', [])}
    if (3, 1, 0) not in hits:
        raise AssertionError(('Rule5 missing G3=G recurrence', r5))
    exhaustive = rule5_exhaustive_control()
    if not exhaustive['ok']:
        raise AssertionError(('Rule5 exhaustive recurrence failure', exhaustive))

    r35 = recurrence_search(35, 3)
    if r35.get('recurrences'):
        raise AssertionError(('Rule35 unexpected early recurrence', r35['recurrences']))
    w = horizon_masks(35, 3, NODE_BUDGET)
    pidx = PAIR_LIST.index((2, 6))
    tid = list(TARGETS).index(tuple(map(int, '00000001')))
    if not ((w['masks'][pidx] >> tid) & 1):
        raise AssertionError('Rule35 h3 witness regression')

    return {
        'ok': True,
        'rule5': {'recurrence': r5['first_recurrence'], 'exhaustive': exhaustive},
        'rule35': {'recurrences': r35.get('recurrences', []), 'h3_witness': True},
    }


def scan_rule(rule: int):
    base = scan_research034(rule)
    langs = []
    questions = 0
    for lang in base['languages']:
        incoming = list(lang['width3_unresolved_target_ids'])
        if not incoming:
            continue
        questions += len(incoming)
        langs.append({
            'pair_index': lang['pair_index'],
            'pair': lang['pair'],
            'seed_symbol': lang['seed_symbol'],
            'incoming_target_ids': incoming,
            'is_r122_161_sentinel': lang['is_r122_161_sentinel'],
        })
    if not questions:
        return {'rule': rule, 'wclass': FULL_CLASS[rule], 'frontier_questions': 0,
                'frontier_seed_languages': 0, 'languages': [], 'recurrence': None}
    rr = recurrence_search(rule, HMAX)
    status = ('temporal-recurrence' if rr.get('first_recurrence') else
              'censored' if rr.get('censored') else 'no-recurrence-through-6')
    return {
        'rule': rule,
        'wclass': FULL_CLASS[rule],
        'frontier_questions': questions,
        'frontier_seed_languages': len(langs),
        'languages': langs,
        'status': status,
        'recurrence': rr,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rule-start', type=int, default=0)
    ap.add_argument('--rule-end', type=int, default=256)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--controls-only', action='store_true')
    args = ap.parse_args()
    source_hashes = {
        'scripts/experiment_symbolic_sofic_image.py': file_hash(Path(__file__)),
        PROTOCOL: file_hash(ROOT / PROTOCOL),
    }
    if args.controls_only:
        out = {'experiment': 'symbolic-sofic-image-controls', 'schema': 1,
               'source_hashes': source_hashes, 'controls': controls()}
    else:
        if not (0 <= args.rule_start < args.rule_end <= 256):
            raise SystemExit('bad rule range')
        rows = [scan_rule(r) for r in range(args.rule_start, args.rule_end)]
        out = {
            'experiment': 'symbolic-sofic-image',
            'schema': 1,
            'rule_start': args.rule_start,
            'rule_end': args.rule_end,
            'hmax': HMAX,
            'source_hashes': source_hashes,
            'resource_limits': {'mdd_nodes': NODE_BUDGET, 'comparison_states': COMPARE_BUDGET},
            'rows': rows,
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + '\n')
    if args.controls_only:
        summary = {'ok': True, 'controls': out['controls']['ok']}
    else:
        from collections import Counter
        summary = {
            'rules': args.rule_end - args.rule_start,
            'frontier_questions': sum(r['frontier_questions'] for r in out['rows']),
            'statuses': dict(Counter(r.get('status') for r in out['rows'] if r['frontier_questions'])),
        }
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
