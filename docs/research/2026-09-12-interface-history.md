# Finite interface history does not close the frozen touching-strip representation

**Evidence:** exact within the frozen finite domain.  
**Authored by:** Codex / OpenAI GPT-5.6 Sol. **Reviewed by:** none yet; independent Gate 2 is pending on gathering PR #131.  
**Protocol:** `docs/research/protocols/interface-history-20260911.md`. Claude Code / Fable 5.1 approved Gate 1 on protocol-only gathering head `36f20aa89889bb884af4ec07785d1611158d6b28` with the K8 causal-patch clarification recorded before implementation.  
**Canonical result:** `results/interface_history_20260911.json`.

## Question

The accepted touching-strip interface-factor unit found that the memoryless six-bit observation `(A,B,E0,E1,E2,E3)` and every frozen interface subset fail local closure through longitudinal radius two on the declared reachable family. Can one or two lags of those **same already-frozen symbols** retain enough erased information to restore bounded local autonomy?

## Answer

No, within the frozen finite family.

Every one of the 288 scientific budgets across `D0/D1/D2`, allowed history depths, all 16 interface masks and radii `R=0,1,2` conflicts. The primary one-lag constructive bet fails, and the independently frozen two-lag extension fails too. There is no Pareto-minimal passing budget because there is no passing budget at all.

This result does not show that temporal history is useless in general. It says that **up to two lags of this specific six-bit interface representation**, on the declared rings, time window, masks and radii, do not recover the causally relevant distinctions that the memoryless representation erased.

## Frozen family

The protocol keeps the accepted touching-strip physical system fixed:

- adjacent encoded strips under the same physical law;
- rings `n=6,7`;
- current six-bit symbol `(A,B,E0,E1,E2,E3)`;
- interface masks `m=0..15`;
- history depths `h=0,1,2`;
- longitudinal radii `R=0,1,2`;
- coarse transition domains `D0=t0..6`, `D1=t1..6`, `D2=t2..6`;
- shallower histories rescored on the same transition domain whenever history depth is compared;
- the accepted `P0=t0..3` memoryless primary replay as a regression control.

The same-domain rule matters. A one-lag history begins only at `t=1`, so comparing it against a memoryless factor on a larger domain could make a false improvement by merely dropping warm-up transitions. The protocol instead compares `h=0` and `h=1` on `D1`, and all `h=0,1,2` on `D2`.

## Exact outcome

### K1–K3 controls pass

The accepted memoryless primary/stress verdicts and canonical conflicts replay exactly. History lag coordinates shift deterministically as specified. Refinement monotonicity has no violation: within a fixed domain, mask and radius, adding a retained lag never turns a passing shallower factor into a conflicting deeper one.

### K4: the one-lag constructive bet fails

On `D1`, the full interface observation with one lag, `H_{15,1}`, conflicts at every frozen radius:

`R = 0, 1, 2`.

The memoryless `H_{15,0}` also conflicts at all three radii, as already implied by the accepted memoryless witness. Thus one lag does not restore local autonomy in the frozen family.

### K5: the two-lag extension also fails

On `D2`, both `H_{15,1}` and `H_{15,2}` conflict at every frozen radius. The recorded K5 outcome is therefore

`both conflict`.

Depth two was frozen before evaluation; it is not a post-result rescue.

### K6: no Pareto-minimal passing budget exists

Across the scientific `D0`, `D1` and `D2` cells, all 288 combinations conflict. The 48 `P0` cells are accepted-result regression controls and are not included in that 288 count.

Because the passing set is empty, there is no minimum over interface-bit count, history depth and radius to interpret.

### K8: hidden causes remain in the current physical causal patch

Every canonical full-state conflict is independently replayed using the exact Gate-1-frozen current causal patch: rows `-2..5` relative to the observation band and columns `2i-2..2i+3` relative to logical block `i`.

For each retained conflict, the two records have no differences in the retained symbolic neighborhood, yet their complete current causal patches differ in unretained physical cells that can affect the next observation. A conflict with identical complete causal patches would be an implementation failure; none occurs.

Two max-radius examples retained during the evaluation lineage make the mechanism concrete:

- `D1, h=1, P15, R=2`: equal five-site current-plus-one-lag histories lead to next symbols differing first at `E0`; the current physical replay exposes one differing unretained in-band cell plus exterior differences.
- `D2, h=2, P15, R=2`: equal five-site three-symbol histories lead to a next symbol differing at `B`; replay again finds unretained current physical differences.

These are bounded witnesses, not a proof against every possible history representation.

### K9: no dependency audit is promoted from a failed factor

Predictive history/cross-interface dependency edges are audited only for a passing `D1` or `D2` factor. Since none passes, the dependency-audit record is empty. This prevents a failed local factor from being redescribed as a successful interacting representation.

### K10: independent physical replay passes

The imported scalar/vector replay checks complete physical-field equality through `t+1` for deterministic controls, accepted memoryless conflict records and every canonical full-state history conflict. This is stronger than checking only the observation or causal-patch cells.

The permanent dedicated workflow replays the entire canonical JSON byte for byte and verifies recorded source hashes for the history verifier, protocol, accepted interface-factor result and imported interface-factor executable dependency.

## What this changes

The result narrows one tempting rescue of the touching-strip obstruction. The memoryless six-bit coordinate failed because relevant current distinctions escaped the retained local state. Simply appending a short temporal stack of that **same coordinate** does not retrieve those distinctions within `h<=2` and `R<=2` on the frozen reachable family.

This is useful negative information: history depth, spatial radius and retained-coordinate choice remain separate resources. Failure of short history is not permission to silently widen radius, add a moving front description, invent a new coordinate, or reintroduce raw physical bands after seeing the result. Each would require its own frozen protocol.

## Evaluation history and reproducibility

Gate 1 was completed before implementation, with the K8 geometry clarification recorded first. Implementation-only PR #134 then pinned the verifier, permanent replay workflow, complete K8/K10 coverage, imported executable provenance and canonical-result integrity mapping with no result present.

A provisional draft run had occurred earlier under an explicit no-merge exception while review tooling was unavailable; it remained non-canonical branch evidence and did not change the frozen budgets or implementation corrections. After normal workflow resumed and #134 integrated, evaluation PR #149 ran the unchanged integrated verifier and committed the canonical result. Temporary one-shot and inspection artifacts were removed; the final evaluation diff contained only `results/interface_history_20260911.json`. All five exact-head checks passed, including byte-for-byte `interface-history` replay.

Reproduce from the repository root:

```bash
python scripts/check_result_integrity.py results/interface_history_20260911.json
python scripts/verify_interface_history.py
```

## Boundaries

This result is bounded to rings `n=6,7`, the declared reachable family, coarse transitions through `t=6`, history depth `h<=2`, radius `R<=2`, the frozen 16 masks and the existing six-bit interface coordinate.

It does **not** exclude deeper temporal history, larger spatial radius, moving or support-tracking state, alternative symbolic coordinates, nonlocal factors, arbitrary-width descriptions, recursive `2D→3D` lifting, intrinsic dimension, self-assembly, endogenous control, Class IV, universality, or all-time closure. It also supplies no physics, metaphysical, spacetime, or prime/`8n+1` claim.