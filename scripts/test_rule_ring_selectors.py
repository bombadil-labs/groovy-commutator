#!/usr/bin/env python3
"""Software checks using constructed data, not a new scientific evaluation."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from rule_ring_selectors import (Case, arithmetic, compare, correlations, default_registry,
                                 divisibility, eca_features, eca_orbit, factorization,
                                 features, pearson, valuation)


def fixture(rings=(8, 12, 18), rules=('54', '110'), context=None):
    context = {'ensemble': 'synthetic', 'replicate': 1} if context is None else context
    return [Case(r, n, 'fixture', n * i, context, f'synthetic:{r}:{n}')
            for n in rings for i, r in enumerate(rules)]


class SelectorsTest(unittest.TestCase):
    def test_arithmetic_distinguishes_support_and_multiplicity(self):
        self.assertEqual(factorization(1), ())
        self.assertEqual(factorization(12), ((2, 2), (3, 1)))
        f = arithmetic(12, 18)
        self.assertEqual((f['gcd'], f['lcm'], f['same_prime_support'], f['exponent_l1']), (6, 36, 1, 2))
        self.assertEqual((f['n_divides_m'], f['m_divides_n']), (0, 0))
        self.assertEqual(valuation(12, 18, prime=2)['gap'], -1)
        self.assertEqual(valuation(12, 18, prime=3)['gap'], 1)
        self.assertEqual(arithmetic(8, 12)['prime_support_jaccard'], .5)
        self.assertEqual(divisibility(8, 12, divisor=4)['both'], 1)
        self.assertEqual(arithmetic(1, 8)['n_divides_m'], 1)
        with self.assertRaises(ValueError):
            valuation(12, 18, prime=4)
        for bad in (0, -1, 3.5, True):
            with self.assertRaises(ValueError):
                factorization(bad)

    def test_rule_symmetries_are_descriptors(self):
        self.assertEqual(eca_orbit(54), {54, 147})
        self.assertEqual(eca_orbit(110), {110, 124, 137, 193})
        self.assertEqual(eca_features('54', '110')['truth_table_hamming'], 3)

    def test_rectangles_and_context_isolation(self):
        cases = fixture() + fixture(context={'ensemble': 'synthetic', 'replicate': 2})
        report = compare(reversed(cases))
        self.assertEqual(report['comparison_count'], 6)
        first = report['rows'][0]
        self.assertEqual(first['rules'], ['54', '110'])
        self.assertEqual(first['rings'], [8, 12])
        self.assertEqual(first['relation_values'], [8, 12])
        self.assertEqual(first['scores']['change'], 4)
        self.assertEqual(first['sources'], ['synthetic:54:8', 'synthetic:110:8', 'synthetic:54:12', 'synthetic:110:12'])
        self.assertEqual(compare(cases), report)
        scan = correlations(report)
        self.assertTrue(all(e['distinct_ring_pairs'] == 3 for e in scan['entries']))
        self.assertEqual(len({json.dumps(e['context'], sort_keys=True) for e in scan['entries']}), 2)

    def test_missing_null_and_duplicate_cases(self):
        cases = fixture()
        report = compare(cases[:-1])
        self.assertEqual(report['comparison_count'], 1)
        self.assertEqual(report['coverage'][0]['missing_rectangles'], 2)
        last = cases[-1]
        cases[-1] = Case(last.rule, last.ring, last.observation, None, last.context, last.source)
        report = compare(cases)
        self.assertEqual(report['comparison_count'], 3)
        self.assertIsNone(report['rows'][-1]['scores']['change'])
        with self.assertRaises(ValueError):
            compare(cases + cases[:1])
        with self.assertRaises(ValueError):
            Case('54', 8, 'bad', float('nan'), {'ensemble': 'synthetic'}, 'fixture')

    def test_extensions_accept_structures_and_many_selectors(self):
        registry = default_registry()
        registry.add('relation', 'intersection', lambda a, b: sorted(set(a) & set(b)), version='test-1')
        registry.add('comparison', 'set_change', lambda a, b: {'symmetric_difference': len(set(a) ^ set(b))})
        registry.add('ring', 'residue', lambda n, m, modulus: {'equal': int(n % modulus == m % modulus)})
        cases = [Case(c.rule, c.ring, c.observation, [c.ring, 1], c.context, c.source) for c in fixture()]
        query = {'relation': [{'name': 'intersection'}], 'comparison': [{'name': 'set_change'}],
                 'ring': [{'name': 'residue', 'id': f'mod{k}', 'params': {'modulus': k}} for k in range(1, 151)]}
        report = compare(cases, query, registry)
        self.assertEqual(len(report['rows'][0]['ring_features']), 150)
        self.assertEqual(report['rows'][0]['relation_values'], [[1, 8], [1, 12]])
        self.assertEqual(report['rows'][0]['scores']['symmetric_difference'], 2)
        self.assertEqual(report['resolved_selectors']['relation'][0]['version'], 'test-1')

    def test_budget_precedes_user_relation(self):
        calls = []
        registry = default_registry()
        registry.add('relation', 'probe', lambda a, b: calls.append(1))
        with self.assertRaisesRegex(ValueError, 'budget exceeded'):
            compare(fixture(), {'max_comparisons': 2, 'relation': [{'name': 'probe'}]}, registry)
        self.assertEqual(calls, [])

    def test_version_and_name_collisions_are_errors(self):
        registry = default_registry()
        with self.assertRaises(ValueError):
            registry.add('ring', 'arithmetic', lambda a, b: {})
        with self.assertRaises(ValueError):
            compare(fixture(), {'ring': [{'name': 'arithmetic', 'version': 'wrong'}]})
        with self.assertRaises(ValueError):
            compare(fixture(), {'ring': [{'name': 'arithmetic'}, {'name': 'arithmetic'}]})
        registry.add('ring', 'one', lambda a, b: {'b.c': 1})
        registry.add('ring', 'two', lambda a, b: {'c': 2})
        resolved = registry.resolve('ring', [{'name': 'one', 'id': 'a'}, {'name': 'two', 'id': 'a.b'}])
        with self.assertRaises(ValueError):
            features(resolved, 8, 12)

    def test_descriptive_pearson_undefined_cases(self):
        self.assertEqual(pearson([(1, 2), (2, 4), (3, 6)]), (1., None))
        self.assertEqual(pearson([(1, 3), (2, 2), (3, 1)]), (-1., None))
        self.assertEqual(pearson([(1, 2)]), (None, 'fewer_than_three_rows'))
        self.assertEqual(pearson([(1, 2)] * 3), (None, 'constant_input'))

    def test_cli_plugin_and_atomic_failure(self):
        from dataclasses import asdict
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory)
            (p/'cases.jsonl').write_text(''.join(json.dumps(asdict(c)) + '\n' for c in fixture()))
            (p/'plugin.py').write_text("def register(registry):\n    registry.add('ring', 'custom', lambda a, b: {'gap': b-a}, version='2')\n")
            (p/'query.json').write_text(json.dumps({'ring': [{'name': 'custom'}]}))
            cmd = [sys.executable, str(Path(__file__).with_name('rule_ring_selectors.py')),
                   '--cases', str(p/'cases.jsonl'), '--query', str(p/'query.json'),
                   '--plugin', str(p/'plugin.py'), '--output', str(p/'out.json'), '--correlations']
            subprocess.run(cmd, check=True, capture_output=True)
            report = json.loads((p/'out.json').read_text())
            self.assertEqual(report['comparison_count'], 3)
            self.assertEqual(len(report['input_sha256']), 4)
            before = (p/'out.json').read_bytes()
            (p/'query.json').write_text('{"max_comparisons": 1}')
            failed = subprocess.run(cmd, capture_output=True)
            self.assertNotEqual(failed.returncode, 0)
            self.assertEqual((p/'out.json').read_bytes(), before)

    def test_catalog_adapter_preserves_indices_and_undefined_values(self):
        # Synthetic arrays with the archived schema; these are not CA results.
        import shutil
        import numpy as np
        from import_observation_catalog import catalog_cases
        definition = Path(__file__).with_name('observation_catalog.py')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'scripts').mkdir()
            shutil.copyfile(definition, root/'scripts/observation_catalog.py')
            unit = root/'experiments/observation_catalog_20260915'
            unit.mkdir(parents=True)
            discovery = np.arange(2*256*300*7, dtype=float).reshape(2, 256, 300, 7)
            confirmation = np.arange(256*300*7, dtype=float).reshape(256, 300, 7)
            discovery[:, :, :24, 6] = np.nan
            confirmation[:, :24, 6] = np.nan
            np.savez(unit/'discovery-metrics.npz', metrics=discovery, widths=[7, 8])
            np.savez(unit/'confirmation-metrics.npz', metrics=confirmation)
            cases = list(catalog_cases(root, rules=[110, 54], candidates=[3, 27], metrics=[2, 6], widths=[9, 7, 8]))
            self.assertEqual(len(cases), 24)
            self.assertEqual(len({json.dumps(c.context, sort_keys=True) for c in cases}), 1)
            for case in cases:
                candidate = 3 if case.observation.startswith('change1/') else 27
                metric = 2 if case.observation.endswith('/refinement_gain') else 6
                expected = (confirmation if case.ring == 9 else discovery[case.ring-7])[int(case.rule), candidate, metric]
                if np.isnan(expected):
                    self.assertIsNone(case.payload)
                else:
                    self.assertEqual(case.payload, expected)
                self.assertIn('sha256=', case.source)
                self.assertIn(f'{int(case.rule)}, {candidate}, {metric}', case.source)
            with self.assertRaises(ValueError):
                list(catalog_cases(root, rules=[54], candidates=[3], metrics=[2], widths=[1021]))


if __name__ == '__main__':
    unittest.main()
