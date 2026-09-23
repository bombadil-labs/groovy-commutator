"""Semantic guards for 1D recursion and its inherited/full-domain distinction."""
import copy
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from groovy_1d_second_generation import (  # noqa: E402
    Rule, closure, eca, groovy, verify_closure,
)


@pytest.mark.parametrize('bits', [(0, 0), (0, 1), (1, 0), (1, 1)])
def test_every_pointwise_binary_rule_has_constant_native_g(bits):
    result = groovy(Rule(0, bits))
    assert result == Rule(0, (bits[0], bits[0]))


def test_linear_two_cell_shift_has_zero_commutator():
    # A directed radius-two shift controls offset/orientation handling.
    rule = Rule(2, tuple((i >> 4) & 1 for i in range(32)))
    assert groovy(rule) == Rule(0, (0, 0))


def saved_case(source=2, fill=0):
    data = json.loads((ROOT/'results/groovy_1d_second_generation_20260923.json').read_text())['data']
    child = next(x for x in data['nonpointwise_descendants'] if x['source_rule'] == source)
    return child['variants'][fill]


def read_rule(d):
    return Rule(d['radius'], tuple(map(int, d['outputs_ascending'])))


def test_full_domain_negative_does_not_override_inherited_positive():
    case = saved_case()
    assert case['full_descendant_domain']['status'] == 'no_present_only_law'
    assert case['inherited_domain']['status'] == 'law'
    assert case['inherited_domain']['radius'] == 2


def test_tampered_positive_table_is_rejected_by_unpacked_replay():
    case = saved_case()
    cert = copy.deepcopy(case['inherited_domain'])
    bits = list(cert['forced_outputs_ascending'])
    index = next(i for i, b in enumerate(bits) if b != '?')
    bits[index] = str(1-int(bits[index]))
    cert['forced_outputs_ascending'] = ''.join(bits)
    with pytest.raises(AssertionError):
        verify_closure(read_rule(case['inherited_observation']), eca(2), cert)


def test_tampered_periodic_successor_is_rejected():
    case = saved_case(32)
    cert = copy.deepcopy(case['inherited_domain'])
    cert['witness']['successors'][0] = cert['witness']['successors'][1]
    with pytest.raises(AssertionError):
        verify_closure(read_rule(case['inherited_observation']), eca(32), cert)


def test_constant_positive_does_not_need_a_periodic_screen():
    cert = closure(Rule(0, (1, 1)), eca(30))
    assert cert['status'] == 'law' and cert['periods_screened'] == 0
    assert cert['observation_constant'] == 1
