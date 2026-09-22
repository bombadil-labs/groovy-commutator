"""Fast regression tests for the Groovy-field closure decider and certificates."""
import pytest

np = pytest.importorskip("numpy")
from groovy.groovy_field import (decide, witness, verify_witness,  # noqa: E402
                                 certify_law, ring_collision)


def verdict(rule, tracks, k, t=0):
    v = decide(rule, tracks, k, t)
    if v.status == "counterexample":
        assert verify_witness(rule, tracks, k, t, witness(v))["verified"]
    elif v.status == "law":
        assert certify_law(rule, tracks, k, t, r_max=8)["status"] == "certified"
    return v.status


@pytest.mark.parametrize("rule,tracks,k,t,expected", [
    (32, (), 1, 0, "law"),            # G_32 E_32 = E_128 G_32 (known)
    (90, (), 1, 0, "law"),            # G_90 = 0
    (110, (), 1, 0, "counterexample"),  # PR #293
    (110, (), 3, 0, "counterexample"),  # line-only memory-3 failure
    (110, (), 2, 1, "counterexample"),  # burn-in does not rescue memory 2
    (110, (128,), 1, 0, "counterexample"),
    (110, (128,), 2, 0, "law"),       # G + run-of-three-ones marker
    (110, (1,), 3, 0, "counterexample"),  # run-of-zeros marker misses phase
    (110, (204,), 1, 0, "law"),       # retaining the source always closes
    (30, (), 3, 0, "law"),            # Rule 30's G is third-order autonomous
])
def test_known_verdicts(rule, tracks, k, t, expected):
    assert verdict(rule, tracks, k, t) == expected


def test_memory3_110_is_invisible_to_every_ring():
    # the infinite-line counterexample has no periodic realisation up to n=10
    assert not any(ring_collision(110, (), 3, 0, n) for n in range(1, 11))


def test_ring_collision_implies_decider_counterexample():
    for rule in (18, 54, 110, 150, 106):
        for k in (1, 2):
            if any(ring_collision(rule, (), k, 0, n) for n in range(1, 8)):
                assert decide(rule, (), k, 0).status == "counterexample"
