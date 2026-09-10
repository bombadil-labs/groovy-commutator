#!/usr/bin/env python3
"""Deterministic implementation checks for the issue-64 suffix learner.

These are hand-checkable traces, not a research evaluation.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from groovy.online_suffix import (
    ABSTAIN_CONFLICT,
    ABSTAIN_UNSEEN,
    DEFINITE,
    ConservativeSuffixLearner,
    FrozenSuffixModel,
    WorkStats,
    run_held_out,
    run_prequential,
)


def check_predict_before_record_and_refine():
    learner = ConservativeSuffixLearner[str]()
    assert learner.begin_step("A").kind == ABSTAIN_UNSEEN
    learner.finish_step("B")
    assert learner.begin_step("B").kind == ABSTAIN_UNSEEN
    learner.finish_step("A")

    p = learner.begin_step("A")
    assert p.kind == DEFINITE and p.value == "B"
    learner.finish_step("C")
    assert learner.stats.wrong == 1
    assert learner.stats.rebuilds == 1
    assert learner.work.rebuilds == 1
    assert learner.h == 2
    assert learner.table == {("A", "B"): {"A"}, ("B", "A"): {"C"}}
    assert learner.raw == ["A", "B", "A"]
    assert learner.storage().retained_history_symbols == 3
    assert learner.storage().table_keys == 2
    assert learner.storage().table_key_symbols == 4
    assert learner.storage().table_successor_entries == 2
    assert learner.work.rebuild_windows == 2
    assert learner.work.rebuild_key_symbols == 4


def check_abstentions_do_not_refine():
    learner = ConservativeSuffixLearner[str]()
    learner.table[("X",)] = {"A", "B"}
    p = learner.begin_step("X")
    assert p.kind == ABSTAIN_CONFLICT
    learner.finish_step("C")
    assert learner.h == 1
    assert learner.stats.rebuilds == 0
    assert learner.stats.abstain_conflict == 1

    fresh = ConservativeSuffixLearner[str]()
    p = fresh.begin_step("U")
    assert p.kind == ABSTAIN_UNSEEN
    fresh.finish_step("V")
    assert fresh.h == 1
    assert fresh.stats.rebuilds == 0


def check_held_out_freeze_and_fresh_history():
    learner = ConservativeSuffixLearner[str]()
    for a, b in zip(["A", "B", "A"], ["B", "A", "C"]):
        learner.learn_transition(a, b)
    model = learner.freeze()
    frozen_table = dict(model.table)

    trace = ["A", "B", "A", "C"]
    calls = {"transition": 0}

    def transition(i: int) -> int:
        calls["transition"] += 1
        return i + 1

    result = run_held_out(model, 0, transition, lambda i: trace[i], 3)
    assert calls["transition"] == 3
    assert result.stats.abstain_unseen >= 1
    assert model.h == 2
    assert dict(model.table) == frozen_table
    assert result.history == ["A", "B", "A"]
    assert result.storage.retained_history_symbols == 3
    assert result.storage.table_keys == len(frozen_table)


def check_prequential_single_advance_and_accounting():
    trace = ["A", "B", "A", "C"]
    calls = {"transition": 0}

    def transition(i: int) -> int:
        calls["transition"] += 1
        return i + 1

    learner = ConservativeSuffixLearner[str]()
    result = run_prequential(learner, 0, transition, lambda i: trace[i], 3)
    assert calls["transition"] == 3
    assert result.work.predictions == 3
    assert result.work.record_operations == 3
    assert result.work.successor_insertions == 3
    assert result.work.rebuilds == 1
    assert result.work.rebuild_windows == 2
    assert result.work.rebuild_successor_insertions == 2
    assert result.h_trace == [1, 1, 2]


def check_conflict_prediction_from_frozen_model():
    work = WorkStats()
    model = FrozenSuffixModel(1, {("X",): frozenset({"A", "B"})})
    p = model.predict(["X"], work)
    assert p.kind == ABSTAIN_CONFLICT
    assert work.predictions == 1
    assert work.prediction_key_symbols == 1


def check_step_protocol_guards():
    learner = ConservativeSuffixLearner[str]()
    try:
        learner.finish_step("X")
    except RuntimeError:
        pass
    else:
        raise AssertionError("finish_step without begin_step should fail")
    learner.begin_step("A")
    try:
        learner.begin_step("B")
    except RuntimeError:
        pass
    else:
        raise AssertionError("double begin_step should fail")
    learner.finish_step("B")


def main():
    check_predict_before_record_and_refine()
    check_abstentions_do_not_refine()
    check_held_out_freeze_and_fresh_history()
    check_prequential_single_advance_and_accounting()
    check_conflict_prediction_from_frozen_model()
    check_step_protocol_guards()
    print("conservative-online-suffix checks: PASS")


if __name__ == "__main__":
    main()
