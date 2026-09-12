from pathlib import Path
import re

program_path = Path('docs/research/2026-09-09-dimensional-closure-program.md')
program = program_path.read_text()
section_heading = '## Frozen resonance-response bet fails on primary ring seven'
if section_heading not in program:
    anchor = '## Relational rank separates available directions from law-used directions'
    if anchor not in program:
        raise SystemExit('program insertion anchor not found')
    section = '''## Frozen resonance-response bet fails on primary ring seven

The [transformed-homologue response audit](2026-09-12-dimensional-resonance-response.md) executes the beam refinement's first frozen operational response test without redefining success after seeing the result. In the accepted touching Rule90 strip substrate, nonliteral cyclic-shift/reflected-shift homologues are compared with controls matched on source weight, transition counts, Hamming distance and XOR-transition count. The response variables and signs were frozen as whole-field validity, residual mass, residual span and return-by-horizon in a **mutual-transparency** direction.

The primary ring-7 bet fails at every genuinely dynamical horizon `k=2,3,4` (and at the `k=1` predecessor-control horizon). This is not a no-effect result: residual mass and span contrasts vary across the 18 matched classes, but their signs are heterogeneous, while validity and return contrasts are zero in every scored class. The predeclared requirement that every class move weakly in the same mutual-transparency direction is therefore false. The symmetry-preserving placebo condition is not applicable because the actual strict predicate never passes; descriptively none of the 503 orbit-preserving placebo assignments strict-passes either. Ring 6 strict-passes at `k=4`, but its two scored classes were frozen as a small-family control and are not promoted over the primary ring-7 result.

This narrows the resonance direction rather than establishing a general absence theorem. Analyst-declared structural homology alone does not yield the frozen uniform response in this substrate. Other preregistered observables, transform-specific responses, interaction laws, or a response transported through an actual dimensional lift remain separate questions. Nothing here establishes semantic self-recognition, consciousness, endogenous control, self-assembly, intrinsic dimension, recursive beam resonance, spacetime/physics, metaphysics, Class IV/universality, or any prime/`8n+1` connection.

'''
    program = program.replace(anchor, section + anchor, 1)

exact_start = program.find('## What is exact now')
open_start = program.find('## What remains open')
if exact_start < 0 or open_start < 0 or open_start <= exact_start:
    raise SystemExit('exact/open section anchors not found')
exact_slice = program[exact_start:open_start]
exact_phrase = 'Transformed-homologue mutual transparency fails as a uniform primary response.'
if exact_phrase not in exact_slice:
    nums = [int(x) for x in re.findall(r'(?m)^(\d+)\. \*\*', exact_slice)]
    if not nums:
        raise SystemExit('no numbered exact claims found')
    n = max(nums) + 1
    item = f'''{n}. **{exact_phrase}** In the frozen touching Rule90 response audit, the primary ring-7 strict predicate fails at `k=2,3,4`: residual mass/span class signs are mixed and validity/return contrasts are all zero. The orbit-preserving placebo criterion is inapplicable because the actual strict predicate never passes. Ring-6 `k=4` is a declared small-family control only. This is an exact finite negative for one operational response hypothesis, not an absence theorem for all homology-sensitive dynamics.\n\n'''
    program = program[:open_start] + item + program[open_start:]
program_path.write_text(program)

checkpoint_path = Path('docs/research/checkpoints/dimensional-lift.md')
checkpoint = checkpoint_path.read_text()
checkpoint_heading = '## Checkpoint 2026-09-12: transformed-homologue mutual-transparency bet fails on primary ring seven; Gate 2 pending'
if checkpoint_heading not in checkpoint:
    anchor = 'Program page: `docs/research/2026-09-09-dimensional-closure-program.md`\n'
    if anchor not in checkpoint:
        raise SystemExit('checkpoint insertion anchor not found')
    block = '''\n## Checkpoint 2026-09-12: transformed-homologue mutual-transparency bet fails on primary ring seven; Gate 2 pending

Read `docs/research/2026-09-12-dimensional-resonance-response.md`. This unit operationalizes one narrow part of the accepted beam refinement: whether an analyst-declared nonliteral structural homology relation changes the touching-strip dynamics in one preregistered mutual-transparency direction.

- Protocol history stayed ahead of evidence. The original Gate 1 was blocked on a matching defect; the refreeze made nonliteral transformed homologues primary, froze the source-only matched census and exact V/M/S/R response semantics, and a final protocol-only clarification replaced the anti-conservative pair-level placebo with joint-shift-orbit label rotation and pinned inclusive span. Claude/Fable approved exact protocol head `15787fa8a2671f899e1d974aff8753386e423cfc` before implementation.
- Source-only implementation #196 and physical-verifier implementation #204 were integrated with no frozen physical-response result. The verifier independently agrees between packed and scalar paths, reproduces the exact `17/64` predecessor table at `k=1`, preserves the frozen ring-6/ring-7 matched census, and keeps the orbit-preserving placebo and complement/literal descriptive controls separate.
- Canonical evaluation #207 produced `results/dimensional_resonance_response_20260912.json` from the unchanged verifier; all bounded exact-head checks were green. Reporting #209 then recorded the result without a post-hoc rescue, and preservation-only #210 reconciled the gathering branch with current accepted `main` while preserving both result-integrity registries.
- **Primary R2 fails.** On ring 7 the strict transformed-homologue mutual-transparency predicate passes at none of `k=2,3,4` (nor at `k=1`). Residual mass/span contrasts exist but class signs are mixed; validity and return contrasts are zero for every scored class at every horizon.
- R4 is correctly not applicable because the actual ring-7 predicate never passes. Descriptively, none of the 503 joint-shift-orbit placebo assignments strict-passes either; this does not rescue R2. R5 independent return-witness replay passes.
- Ring 6 strict-passes at `k=4`, but ring 6 has only two scored classes and was frozen as a small-family control/descriptive cohort, not the primary claim. Do not promote that control over the preregistered ring-7 result.
- Exact scope is the exhaustive declared `n=6,7` touching-strip family, horizons `k=1..4`, frozen matching, causal window, observables and sign convention. Do not infer absence of every homology-sensitive statistic, semantic self-recognition, consciousness, endogenous control, self-assembly, intrinsic dimension, recursive beam resonance, physics/spacetime, metaphysics, Class IV/universality, or primes/`8n+1`.
- **Review state:** evaluation, reporting, latest-main reconciliation and this current-account update are complete on the gathering lineage. Exact-head independent Claude/Fable Gate 2 and reviewer merge remain required before acceptance on `main`.
'''
    checkpoint = checkpoint.replace(anchor, anchor + block, 1)
checkpoint_path.write_text(checkpoint)
