# Jev Class-IV independent-signal probe

This directory is a local execution package for the frozen 2026-09-16 protocol.

## Scientific boundary

The semantic primary run is blind to rule IDs/classes and deliberately withholds the previously successful recurrence/spreading and quotient-cycle-growth channels. `truth_private.json` is used only by the evaluator after inference.

The current feature table contains 49 label-free primitive summaries from three families:

- F1: selective retention + local predictive-history gain + residual uncertainty;
- F2: commutator-history predictive gain, independently reconstructed from saved count tables;
- F3: pooled partial-rule/cohabitation geometry.

The optional observation-catalog family F4 is omitted because the available compact result is entangled with label-selected slots and the 133 MB raw atlas was not required for this first run.

## Install

Use the official SDK:

```bash
uv add typesafe-sdk
# or: pip install typesafe-sdk
```

Then set the key in your shell (do not put it in this directory):

```bash
export TYPESAFE_API_KEY='...'
```

## Validate without an API call

```bash
python run_jev_probe.py --dry-run --mode semantic
```

## Primary run

```bash
python run_jev_probe.py --mode semantic --attempts 3
python evaluate_jev_probe.py jev_raw_responses.jsonl
```

The runner is resumable: successful `(mode, alias, attempt)` records already present in the JSONL are skipped.

## Opaque-name diagnostic

Only after preserving the semantic primary responses:

```bash
python run_jev_probe.py --mode opaque --attempts 3 --output jev_opaque_responses.jsonl
```

Known-signal restoration and rule-ID contamination controls are intentionally not implemented in the primary runner yet; run them only after the primary result is sealed.
