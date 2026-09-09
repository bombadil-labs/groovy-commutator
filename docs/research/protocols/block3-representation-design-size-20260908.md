# Fresh-size protocol: Rule-24 block-3 greedy counterexample — 2026-09-08

**Status:** frozen after the independent `n=12` audit passed and before evaluating the fresh size.  
**Discovery:** Rule 24, target `01000010`, `n=12`, `q=3`.  
**Fresh ring width:** `n=15`, still tiled by nonoverlapping three-cell blocks.

## Purpose

Research028 found the first exact failure of the greedy fixed-target Shannon closure-repair gradient. An independently implemented audit reproduced the complete `n=12` counterexample and identified a predictive-synergy mechanism: a zero-immediate-gain split `{1}|{6}` makes a later `{3,7}` split more than an order of magnitude more predictive.

This protocol asks whether that qualitative obstruction survives a fresh larger periodic ring without reselecting a rule or target.

## Frozen case

- fine ECA rule: **24**;
- local binary target: `01000010`;
- target classes: `{0,2,3,4,5,7}` and `{1,6}`;
- cadence: `q=3`;
- fresh periodic ring width: `n=15`;
- exact uniform ensemble over all `2^15` microstates;
- exact local target-refinement interval: `B_6 B_2 = 406` encoders.

The named bridge and same-split encoders remain:

- zero-gain discovery bridge: `01000020`, splitting `{1}|{6}`;
- `{3,7}` split directly from target: `01020012`;
- `{3,7}` split after the bridge: `01020032`.

## Frozen predictions

The fresh-size test passes only if both primary predictions hold:

1. **Greedy remains globally suboptimal.** Recompute the complete 406-node interval, the exact greedy repair under the frozen gain/tie-breaking rule, and the globally minimum added-information exact repair. Require
   
   \[
   A_{greedy}>A_T^*.
   \]

2. **The predictive-synergy ordering survives.** Let `g_direct` be the cost-normalized gain of the `{3,7}` split directly from the target and `g_conditioned` the gain of that same split after the `{1}|{6}` bridge. Require
   
   \[
   g_{conditioned}>g_{direct}.
   \]

The test does **not** require the exact `n=12` one-bit regret, greedy terminal encoder, or globally optimal terminal encoder to remain unchanged. Those are recorded descriptively if they do.

## Secondary measurements

Record:

- target `W` and stable future horizon;
- greedy and global added-information costs and regret;
- greedy path and every global optimum;
- immediate gain of the `{1}|{6}` bridge;
- direct and conditioned `{3,7}` gains and their ratio;
- whether the `n=12` global encoder `01230243` remains globally optimal;
- whether the `n=12` greedy terminal encoder `01230245` remains the greedy endpoint.

## Independent method

Use the direct explicit-future implementation introduced by `audit_block3_representation_design.py`, generalized only from `n=12` to `n=15`. Do not use the Research028 primary search implementation to decide the fresh-size result.

## Scope

A pass establishes robustness on one fresh finite ring size only. It does not prove the counterexample persists for all widths, nor that predictive synergy is the only obstruction to greedy optimality.