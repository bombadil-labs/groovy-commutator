"""Semantic controls, no scientific parameter sweep."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('repair_core', ROOT/'experiments/prediction_repair_20260923/core.py')
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)


class RepairTests(unittest.TestCase):
    def toy(self):
        d = core.Domain.__new__(core.Domain)
        d.states = [0, 1, 2]
        d.index = {s: s for s in d.states}
        d.codes = np.array([core.block_codes(s) for s in d.states])
        d.wins = [3, 6, 5]  # {a,b}, {b,c}, {a,c}
        return d

    def test_pairwise_compatible_actions_can_have_no_common_response(self):
        d = self.toy()
        self.assertTrue(all(d.wins[i] & d.wins[j] for i in range(3) for j in range(i)))
        p = (0,)*8
        w = d.oracle(p, 'repair')
        self.assertEqual(w['states'], [0, 1, 2])
        d.validate(p, w)
        self.assertIsNone(d.policy(p))

    def test_splitting_conflict_can_enable_a_policy(self):
        d = self.toy()
        p = (0, 0, 1, 0, 0, 0, 0, 0)
        self.assertIsNone(d.oracle(p, 'repair'))
        self.assertEqual(d.policy(p)['flips_on_uniform_domain'], 2)
        w = self.toy().oracle((0,)*8, 'repair')
        self.assertFalse(core.violates(p, w))

    def test_forged_winning_sets_are_rejected(self):
        d = self.toy()
        w = d.oracle((0,)*8, 'repair')
        w['winning_masks'][0] = 7
        with self.assertRaisesRegex(ValueError, 'forged'):
            d.validate((0,)*8, w)

    def test_nonminimal_witness_is_rejected(self):
        d = self.toy()
        d.wins = [1, 2, 3]
        w = {'kind': 'repair', 'states': [0, 1, 2], 'winning_masks': [1, 2, 3]}
        with self.assertRaisesRegex(ValueError, 'minimal'):
            d.validate((0,)*8, w)

    def test_refining_observation_does_not_violate_old_group_constraint(self):
        d = self.toy()
        w = d.oracle((0,)*8, 'repair')
        self.assertTrue(core.violates((0,)*8, w))
        self.assertFalse(core.violates(tuple(range(8)), w))


if __name__ == '__main__':
    unittest.main()
