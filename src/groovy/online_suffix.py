"""Conservative online suffix learner from issue #64.

This module is an implementation instrument only. It deliberately makes no
claim that suffix depth equals the future-visibility depth of Research023.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Callable, Generic, Hashable, Mapping, TypeVar

Obs = TypeVar("Obs", bound=Hashable)
State = TypeVar("State")

ABSTAIN_UNSEEN = "abstain_unseen"
ABSTAIN_CONFLICT = "abstain_conflict"
DEFINITE = "definite"


@dataclass(frozen=True)
class Prediction(Generic[Obs]):
    kind: str
    value: Obs | None = None


@dataclass
class OutcomeStats:
    abstain_unseen: int = 0
    abstain_conflict: int = 0
    correct: int = 0
    wrong: int = 0
    rebuilds: int = 0

    def score(self, prediction: Prediction[Obs], actual: Obs) -> None:
        if prediction.kind == ABSTAIN_UNSEEN:
            self.abstain_unseen += 1
        elif prediction.kind == ABSTAIN_CONFLICT:
            self.abstain_conflict += 1
        elif prediction.kind == DEFINITE:
            if prediction.value == actual:
                self.correct += 1
            else:
                self.wrong += 1
        else:  # pragma: no cover - internal invariant guard
            raise ValueError(f"unknown prediction kind {prediction.kind!r}")


@dataclass
class WorkStats:
    predictions: int = 0
    prediction_key_symbols: int = 0
    record_operations: int = 0
    successor_insertions: int = 0
    rebuild_windows: int = 0
    rebuild_key_symbols: int = 0
    rebuild_successor_insertions: int = 0


@dataclass(frozen=True)
class StorageAccount:
    retained_history_symbols: int
    table_keys: int
    table_key_symbols: int
    table_successor_entries: int


@dataclass(frozen=True)
class FrozenSuffixModel(Generic[Obs]):
    h: int
    table: Mapping[tuple[Obs, ...], frozenset[Obs]]

    def __post_init__(self) -> None:
        if self.h < 1:
            raise ValueError("h must be >= 1")

    def predict(self, history: list[Obs], work: WorkStats | None = None) -> Prediction[Obs]:
        if work is not None:
            work.predictions += 1
        if len(history) < self.h:
            return Prediction(ABSTAIN_UNSEEN)
        key = tuple(history[-self.h :])
        if work is not None:
            work.prediction_key_symbols += self.h
        successors = self.table.get(key, frozenset())
        if not successors:
            return Prediction(ABSTAIN_UNSEEN)
        if len(successors) > 1:
            return Prediction(ABSTAIN_CONFLICT)
        return Prediction(DEFINITE, next(iter(successors)))


@dataclass
class HeldOutResult(Generic[Obs]):
    stats: OutcomeStats
    work: WorkStats
    history: list[Obs]
    h_trace: list[int]


@dataclass
class TrainingResult(Generic[Obs]):
    stats: OutcomeStats
    work: WorkStats
    h_trace: list[int]
    storage_trace: list[StorageAccount]


@dataclass
class ConservativeSuffixLearner(Generic[Obs]):
    h: int = 1
    raw: list[Obs] = field(default_factory=list)
    table: dict[tuple[Obs, ...], set[Obs]] = field(default_factory=dict)
    stats: OutcomeStats = field(default_factory=OutcomeStats)
    work: WorkStats = field(default_factory=WorkStats)
    h_trace: list[int] = field(default_factory=list)
    storage_trace: list[StorageAccount] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.h < 1:
            raise ValueError("h must be >= 1")

    def _predict_current(self) -> Prediction[Obs]:
        self.work.predictions += 1
        if len(self.raw) < self.h:
            return Prediction(ABSTAIN_UNSEEN)
        key = tuple(self.raw[-self.h :])
        self.work.prediction_key_symbols += self.h
        successors = self.table.get(key, set())
        if not successors:
            return Prediction(ABSTAIN_UNSEEN)
        if len(successors) > 1:
            return Prediction(ABSTAIN_CONFLICT)
        return Prediction(DEFINITE, next(iter(successors)))

    def _record(self, key: tuple[Obs, ...], successor: Obs) -> None:
        self.work.record_operations += 1
        bucket = self.table.setdefault(key, set())
        before = len(bucket)
        bucket.add(successor)
        if len(bucket) != before:
            self.work.successor_insertions += 1

    def _rebuild(self, sequence: list[Obs]) -> None:
        rebuilt: dict[tuple[Obs, ...], set[Obs]] = {}
        windows = max(0, len(sequence) - self.h)
        for i in range(windows):
            key = tuple(sequence[i : i + self.h])
            successor = sequence[i + self.h]
            self.work.rebuild_windows += 1
            self.work.rebuild_key_symbols += self.h
            bucket = rebuilt.setdefault(key, set())
            before = len(bucket)
            bucket.add(successor)
            if len(bucket) != before:
                self.work.rebuild_successor_insertions += 1
        self.table = rebuilt

    def storage(self) -> StorageAccount:
        return StorageAccount(
            retained_history_symbols=len(self.raw),
            table_keys=len(self.table),
            table_key_symbols=sum(len(key) for key in self.table),
            table_successor_entries=sum(len(values) for values in self.table.values()),
        )

    def learn_transition(self, current: Obs, successor: Obs) -> Prediction[Obs]:
        """Predict, score, record, then refine on a wrong definite prediction."""
        self.raw.append(current)
        prediction = self._predict_current()
        self.stats.score(prediction, successor)

        if len(self.raw) >= self.h:
            key = tuple(self.raw[-self.h :])
            self._record(key, successor)

        wrong_definite = prediction.kind == DEFINITE and prediction.value != successor
        if wrong_definite:
            self.h += 1
            self.stats.rebuilds += 1
            # The new successor is available for re-keying, but is not appended
            # to raw until it becomes the next current observation.
            self._rebuild(self.raw + [successor])

        self.h_trace.append(self.h)
        self.storage_trace.append(self.storage())
        return prediction

    def freeze(self) -> FrozenSuffixModel[Obs]:
        table = {key: frozenset(values) for key, values in self.table.items()}
        return FrozenSuffixModel(self.h, MappingProxyType(table))

    def training_result(self) -> TrainingResult[Obs]:
        return TrainingResult(self.stats, self.work, list(self.h_trace), list(self.storage_trace))


def run_prequential(
    learner: ConservativeSuffixLearner[Obs],
    initial_state: State,
    transition: Callable[[State], State],
    observe: Callable[[State], Obs],
    steps: int,
) -> TrainingResult[Obs]:
    """Run a concrete harness; learner receives observations only."""
    if steps < 0:
        raise ValueError("steps must be non-negative")
    state = initial_state
    current = observe(state)
    for _ in range(steps):
        next_state = transition(state)
        successor = observe(next_state)
        learner.learn_transition(current, successor)
        state = next_state
        current = successor
    return learner.training_result()


def run_held_out(
    model: FrozenSuffixModel[Obs],
    initial_state: State,
    transition: Callable[[State], State],
    observe: Callable[[State], Obs],
    steps: int,
) -> HeldOutResult[Obs]:
    """Evaluate a frozen model with fresh history and no training mutation."""
    if steps < 0:
        raise ValueError("steps must be non-negative")
    history: list[Obs] = []
    stats = OutcomeStats()
    work = WorkStats()
    h_trace: list[int] = []
    state = initial_state
    current = observe(state)
    for _ in range(steps):
        history.append(current)
        prediction = model.predict(history, work)
        next_state = transition(state)
        successor = observe(next_state)
        stats.score(prediction, successor)
        h_trace.append(model.h)
        state = next_state
        current = successor
    return HeldOutResult(stats=stats, work=work, history=history, h_trace=h_trace)
