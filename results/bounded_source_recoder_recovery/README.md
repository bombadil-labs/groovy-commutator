# Bounded source-recoder exact recovery checkpoints

This directory contains durable, resumable checkpoints for the eight bounded-source-recoder seed languages left unresolved by the original 1,200-second verification wall.

Files in this directory are operational state for the frozen exact-recovery protocol. `pending` means only that another infrastructure slice is required; it is not a scientific censoring outcome. The workflow resumes these checkpoints until each seed is exactly classified as either `bounded-recoder-certified` or `no-bounded-recoder-through-4`.

Scientific parameters remain frozen at `m <= 4` and `t <= 6`; restarting or resuming a batch does not enlarge the hypothesis.

Operational checkpoint: the first durable recovery batch was recorded at `ea08699`; this edit explicitly resumes from those persisted queues after enabling workflow-dispatch recursion.
