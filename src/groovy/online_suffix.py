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
    rebuilds: int = 0
    rebuild_windows: int = 0
    rebuild_key_symbols: int = 0
    rebuild_successor_insertions: int = 0


@dataclass(frozen=True)
class StorageAccount:
    retained_history_symbols: int
    table_keys: int
    table_key_symbols: int
    table_successor_entries: int


def _table_storage(table: Mapping[tuple[Obs, ...], object]) -> tuple[int, int]:
    key_symbols = sum(len(key) for key in table)
    successor_entries = sum(len(values) for values in table.values())  # type: ignore[arg-type]
    return key_symbols, successor_entries


@dataclass(frozen=True)
class FrozenSuffixModel(Generic[Obs]):
    h: int
    table: Mapping[tuple[Obs, ...], frozenset[Obs]]

    def __post_init__(self) -> None:
        if self.h < 1:
            raise ValueError("h must be >= 1")
        # Snapshot caller-owned mappings and values as well as attribute bindings.
        snapshot = {key: frozenset(values) for key, values in self.table.items()}
        object.__setattr__(self, "table", MappingProxyType(snapshot))

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

    def storage(self, held_out_history_symbols: int = 0) -> StorageAccount:
        key_symbols, successor_entries = _table_storage(self.table)
        return StorageAccount(
            retained_history_symbols=held_out_history_symbols,
            table_keys=len(self.table),
            table_key_symbols=key_symbols,
            table_successor_entries=successor_entries,
        )


@dataclass
class HeldOutResult(Generic[Obs]):
    stats: OutcomeStats
    work: WorkStats
    history: list[Obs]
    h_trace: list[int]
    storage: StorageAccount


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
    _pending_prediction: Prediction[Obs] | None = field(default=None, init=False, repr=False)
    _pending_key: tuple[Obs, ...] | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.h < 1:
            raise ValueError("h must be >= 1")

    def _predict_current(self) -> Prediction[Obs]:
        self.work.predictions += 1
        key = self._pending_key
        if key is None:
            return Prediction(ABSTAIN_UNSEEN)
        self.work.prediction_key_symbols += len(key)
        successors = self.table.get(key, set())
        if not successors:
            return Prediction(ABSTAIN_UNSEEN)
        if len(successors) > 1:
            return Prediction(ABSTAIN_CONFLICT)
        return Prediction(DEFINITE, next(iter(successors)))

    def begin_step(self, current: Obs) -> Prediction[Obs]:
        """Receive the current observation and predict before the outcome exists."""
        if self._pending_prediction is not None:
            raise RuntimeError("finish the pending step before beginning another")
        self.raw.append(current)
        # Construct the key once; prediction and recording use this same tuple.
        self._pending_key = tuple(self.raw[-self.h :]) if len(self.raw) >= self.h else None
        prediction = self._predict_current()
        self._pending_prediction = prediction
        return prediction

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
        key_symbols, successor_entries = _table_storage(self.table)
        return StorageAccount(
            retained_history_symbols=len(self.raw),
            table_keys=len(self.table),
            table_key_symbols=key_symbols,
            table_successor_entries=successor_entries,
        )

    def finish_step(self, successor: Obs) -> Prediction[Obs]:
        """Receive the successor, then score, record, and possibly refine."""
        if self._pending_prediction is None:
            raise RuntimeError("begin_step must be called before finish_step")
        prediction = self._pending_prediction
        pending_key = self._pending_key
        self.stats.score(prediction, successor)

        if pending_key is not None:
            self._record(pending_key, successor)

        wrong_definite = prediction.kind == DEFINITE and prediction.value != successor
        if wrong_definite:
            self.h += 1
            self.stats.rebuilds += 1
            self.work.rebuilds += 1
            # successor is available for re-keying now, but is not appended to
            # raw until it becomes the next current observation.
            self._rebuild(self.raw + [successor])

        self.h_trace.append(self.h)
        self.storage_trace.append(self.storage())
        self._pending_prediction = None
        self._pending_key = None
        return prediction

    def learn_transition(self, current: Obs, successor: Obs) -> Prediction[Obs]:
        """Convenience helper preserving the begin/finish ordering internally."""
        self.begin_step(current)
        return self.finish_step(successor)

    def freeze(self) -> FrozenSuffixModel[Obs]:
        if self._pending_prediction is not None:
            raise RuntimeError("cannot freeze with a pending prediction")
        table = {key: frozenset(values) for key, values in self.table.items()}
        return FrozenSuffixModel(self.h, table)

    def training_result(self) -> TrainingResult[Obs]:
        return TrainingResult(self.stats, self.work, list(self.h_trace), list(self.storage_trace))


def run_prequential(
    learner: ConservativeSuffixLearner[Obs],
    initial_state: State,
    transition: Callable[[State], State],
    observe: Callable[[State], Obs],
    steps: int,
) -> TrainingResult[Obs]:
    """Run a concrete harness; learner receives only observations in order."""
    if steps < 0:
        raise ValueError("steps must be non-negative")
    state = initial_state
    current = observe(state)
    for _ in range(steps):
        learner.begin_step(current)
        next_state = transition(state)
        successor = observe(next_state)
        learner.finish_step(successor)
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
    return HeldOutResult(
        stats=stats,
        work=work,
        history=history,
        h_trace=h_trace,
        storage=model.storage(held_out_history_symbols=len(history)),
    )
