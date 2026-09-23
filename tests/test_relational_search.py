"""Small semantic rejection tests. No benchmark execution or external API calls."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    'relational_pilot', ROOT/'experiments/relational_search_20260923/run.py')
pilot = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pilot)


class CertificateRejections(unittest.TestCase):
    def test_missing_candidate_cannot_be_called_complete(self):
        reference = [(0, 0, 1), (0, 1, 2)]
        with self.assertRaisesRegex(ValueError, 'incomplete'):
            pilot.validate_stream(reference[:1], reference)
        with self.assertRaisesRegex(ValueError, 'duplicated'):
            pilot.validate_stream(reference+reference[:1], reference)

    def test_forged_future_disagreement_is_rejected(self):
        domain = pilot.Domain.__new__(pilot.Domain)
        domain.np = np
        domain.word = np.array([[0, 0], [0, 1], [0, 0]])
        p = (0,)*8
        witness = {'states': [0, 1], 'codes_a': pilot.codes(0),
                   'codes_b': pilot.codes(1), 'first_target_difference': 1}
        domain.validate_witness(p, witness)  # Genuine toy collision.
        witness.update(states=[0, 2], codes_b=pilot.codes(2))
        with self.assertRaisesRegex(ValueError, 'disagreement'):
            domain.validate_witness(p, witness)

    def test_witness_must_collide_under_failed_candidate(self):
        domain = pilot.Domain.__new__(pilot.Domain)
        domain.np = np
        domain.word = np.array([[0, 0], [0, 1]])
        witness = {'states': [0, 1], 'codes_a': pilot.codes(0),
                   'codes_b': pilot.codes(1), 'first_target_difference': 1}
        with self.assertRaisesRegex(ValueError, 'does not collide'):
            domain.validate_witness(tuple(range(8)), witness)

    def test_prolog_witness_filters_family_and_keeps_joint_repair(self):
        bridge = pilot.Bridge()
        try:
            generated = bridge.call('generate', target=[0, 0, 0])
            self.assertEqual(len(generated), 5)
            # One witness requires splitting 0/1; another requires 1/2.
            # Only their conjunction leaves these two possible repairs.
            ps = pilot.order(generated)
            bridge.call('install', rows=[[i, pilot.weight(p), p] for i, p in enumerate(ps)])
            bridge.call('witness', id=0, a=[0], b=[1])
            bridge.call('witness', id=1, a=[1], b=[2])
            offered = bridge.call('next', guided=True, limit=8)
            self.assertEqual([ps[i] for i in offered], [(0, 1, 0)])
            for i in offered:
                bridge.call('mark', index=i)
            self.assertEqual([ps[i] for i in bridge.call('next', guided=True, limit=1)],
                             [(0, 1, 2)])
            stats = bridge.call('stats')
            self.assertEqual(len(stats['rejections']), 3)
            for i, witness_id in stats['rejections']:
                pair = ([0], [1]) if witness_id == 0 else ([1], [2])
                self.assertTrue(pilot.collides(ps[i], *pair))
        finally:
            bridge.close()

    def test_jev_cannot_choose_outside_supplied_tier_or_exceed_cap(self):
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self): return b'{"answers":{"next":{"choice":"c999"}}}'
        ps = [(0, 1, 0, 0, 0, 0, 1, 0), tuple(range(8))]
        with patch.dict('os.environ', {'TYPESAFE_API_KEY': 'test-only'}), \
             patch.object(pilot.urllib.request, 'urlopen', return_value=Response()) as api:
            selected, attempts, record = pilot.choose_jev(ps, [0, 1], [], 0)
            self.assertEqual((selected, attempts), (0, 1))
            self.assertEqual(record['status'], 'api_or_choice_fallback')
            selected, attempts, record = pilot.choose_jev(ps, [0, 1], [], 6)
            self.assertEqual((selected, attempts), (0, 6))
            self.assertEqual(record['status'], 'budget_fallback')
            self.assertEqual(api.call_count, 1)


if __name__ == '__main__':
    unittest.main()
