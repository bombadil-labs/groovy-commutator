"""Semantic guards for streamed closure and direct third-G verification."""
import copy
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import groovy_1d_second_generation as prior  # noqa: E402
from groovy_1d_third_generation import (  # noqa: E402
    from_record, stream_factor, verify_result,
)


@pytest.mark.parametrize('r', [2, 16])
def test_identity_observation_recovers_original_radius_one_rule(r):
    identity = prior.Rule(0, (0, 1))
    zero = stream_factor(identity, prior.eca(r), 0)
    one = stream_factor(identity, prior.eca(r), 1)
    assert zero['status'] == 'local_conflict'
    assert one['status'] == 'law' and one['source_words'] == 8
    assert one['forced_outputs_ascending'] == prior.eca(r).record()['outputs_ascending']


def saved_case(first_fill, second_fill):
    result = json.loads((ROOT/'results/groovy_1d_third_generation_20260923.json').read_text())
    return next(c for c in result['data']['cases'] if
                (c['source_rule'], c['first_fill'], c['second_fill']) == (2, first_fill, second_fill))


def recover_observation(case):
    second = json.loads((ROOT/'results/groovy_1d_second_generation_20260923.json').read_text())
    child = next(c for c in second['data']['nonpointwise_descendants'] if c['source_rule'] == 2)
    variant = child['variants'][case['first_fill']]
    return prior.compose(prior.groovy(from_record(case['second_update'])),
                         from_record(variant['inherited_observation']))


def test_tampered_witness_rejected_by_direct_nested_g():
    case = saved_case(0, 0)
    cert = copy.deepcopy(case['inherited_domain'])
    cert['witness']['successors'][0] = cert['witness']['successors'][1]
    with pytest.raises(AssertionError):
        verify_result(prior.eca(2), from_record(case['first_update']),
                      from_record(case['second_update']), None, cert)


def test_tampered_positive_rejected_by_unpacked_replay():
    case = saved_case(1, 0)
    cert = copy.deepcopy(case['inherited_domain'])
    outputs = list(cert['forced_outputs_ascending'])
    assert outputs[0] == '0'
    outputs[0] = '1'
    cert['forced_outputs_ascending'] = ''.join(outputs)
    with pytest.raises(AssertionError):
        verify_result(prior.eca(2), from_record(case['first_update']),
                      from_record(case['second_update']), recover_observation(case), cert)


def test_unresolved_record_is_not_accepted_as_a_certificate():
    case = saved_case(1, 1)
    verdict = verify_result(prior.eca(2), from_record(case['first_update']),
                            from_record(case['second_update']), None,
                            case['inherited_domain'])
    assert verdict['verified'] is False
    assert 'unresolved' in verdict['reason']
