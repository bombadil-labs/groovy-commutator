"""Persist the fifth-cycle synthesis from actual census and audit outputs."""
import json,datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent;RUN=ROOT/'runs/universal_3d'
rows=list(map(json.loads,(RUN/'candidates.jsonl').read_text().splitlines()))
s=json.loads((RUN/'summary.json').read_text());v=json.loads((RUN/'verification.json').read_text())
assert s['status']=='complete' and v['status']=='passed'
prior=[]
for name in ('recursive_binary_3d_v2','recursive_binary_reflections','recursive_binary_centering_alternatives'):
    prior.extend(map(json.loads,(ROOT/f'runs/{name}/candidates.jsonl').read_text().splitlines()))
best={r['rule']:r for r in rows if r['recursive_G']['passes']}
for r in prior:
    if r['recursive_G']['passes'] and r['rule'] not in best:best[r['rule']]=r
extra=sorted(set(best)-set(s['recursive_G_rules']))
unresolved=sorted(set(s['G_eligible_rules'])-set(best))
s['best_known_G_rules']=sorted(best);s['earlier_alternative_G_rules']=extra
s['best_known_raw_G_rules']=sorted({r['rule'] for r in rows+prior if r['recursive_G'].get('mode')=='raw' and r['recursive_G']['passes']})
s['eligible_without_known_3d_G']=unresolved
(RUN/'summary.json').write_text(json.dumps(s,indent=2)+'\n')
(RUN/'best_known_G_paths.jsonl').write_text(''.join(json.dumps(best[r],separators=(',',':'))+'\n' for r in sorted(best)))
questions=[
 'Which exact native/probe collisions exclude every first-floor centered-G recipe for the36remaining source rules?',
 'For the14eligible rules with no known3DGpath, which forced-value distinctions must a reusable field relation preserve?',
 'Can the universal first-order repeat be characterized by a closed local invariant, including the two rank-one parent-completion constraints, rather than another finite-dimensional census?'
]
report=f'''# Universal first-floor family repeated into 3D

The same four-field recipe, selected once per ECA, gives **faithful native binary 1D → 2D → 3D paths for all 256 ECAs**, with native radius two at both lifted floors. This is a universal finite-depth dynamical result. A common nontrivial, indefinitely reusable G-preserving lift remains open.

| Gate | Selected first floor | Selected 3D paths |
|---|---:|---:|
| Uniform unlabeled native evolution | 256 | 256 |
| Local source recovery | 256 | 256 |
| Local parent recovery | 256 (same as source here) | 256 |
| Original-G route | 133 | 115 |
| Centered route selected when original unavailable | 87 | 85 |
| Combined selected G route | 220 | 200 |

The 85 centered successes are the successful **centered-only selections**, not a separate census of centered G on all 256 paths. Original-mode failures were not silently reclassified using centered G. The 36 rules without any first-floor carrier were tested for dynamics and both decoders, and were not submitted to an inapplicable recursive-G test.

Keeping six earlier successful alternative recipes—{', '.join(map(str,extra))}—raises **best-known 3D G coverage to 206 source rules: 121 original and 85 additional centered**. Rule 110 retains its earlier successful path; the new deterministic selection fails there. This distinction prevents a selection failure from erasing an existing result.

## Experiment and exact domain

Selection uses only the completed first-floor tables. In each two-element ECA reflection orbit, choose the smaller rule and prefer original G, then centered G, then the canonical P/D/M/Q order, symmetric Q, the right reference placement, positive P sign, then birth/death/stay-one/stay-zero. Reflect the entire recipe for the partner: rule, P sign and Q operand polarity/placement. No second-floor result influences selection, and there is no recipe rescue search.

For self-reflecting rules we fix an orientation convention; there cannot be a signed recipe invariant under reflection when its P sign must change. We claim an aligned selection on paired rules and a reflection-closed family, not a reflection-fixed selector at those fixed points. All measured rule-level gates are reflection-closed.

The reference family is:

- `S[i-2] AND S[i+1]` and `S[i-1] AND S[i+2]`;
- `S[i-2] AND NOT S[i+1]` and `S[i+2] AND NOT S[i-1]`.

Derivative convention is primitive: `D_r = table(r XOR 204)`, and `E_r(X) = X XOR D_r(X)`. Original `G = D(E(X)) XOR E(D(X))`; centered G is tracked separately. On recursion, apply the same mask, row order and Q coefficients diagonally across the newest old transverse axis. Q probes use the derivative of Q, including its polarity.

The census accounts for all 256 selected recipes: **53 exact prior cases reused, 203 new cases**, in {s['seconds']:.2f} seconds. Every new case exhausts 8,192 source words in its exact 13-cell dependency window and all 16 transverse phases: 131,072 local events per recipe. Sparse native neighborhoods have 80 distinct bits on this prepared family, corresponding to the full physical 5×5×5 neighborhood. No finite-ring sampling is used as evidence for the exhaustive conclusion.

Unspecified 2D native outputs remain GF(2) variables. Centered failures exhaust every admissible parent-zero and child-zero choice. No arbitrary zero completion creates a claimed obstruction. The child native rule remains unspecified outside the keys forced by native and commutator constraints; any consistent total extension exists as a finite binary local table.

## What failed, and what changed

Every native and decoder gate passes. The selected recursive-G test has 18 original-mode failures and two centered-mode failures:

`{', '.join(map(str,s['recursive_G_constraint_failures']))}`.

The centered failures are 173 and 229, both with all parent/child zero branches ruled out. These are exact failures of these particular recipes and diagnostic modes, not universal no-go theorems. After retaining older alternatives, the 14 eligible rules without any saved successful 3D G path are:

`{', '.join(map(str,unresolved))}`.

The distinct first-floor G gap consists of 36 rules:

`{', '.join(map(str,s['missing_first_floor_G']))}`.

The directed repair survives recursion: Rule 23 carries centered G and Rule 232 original G in 3D. The symmetric-family exceptions to the directed census also survive: Rule 77 carries centered G and Rule 178 original G.

Two successful paths, 157 and 199, impose a rank-one linear condition on still-free parent outputs. Consequently the earlier observation that successful paths never constrain the parent completion does **not** generalize to this expanded selection. Satisfying assignments were checked directly. The other successful selected paths have rank-zero extension constraints.

## Verification and costs

Independent verification uses interval-cropped source evolution, independently implemented directed Q, full 125-bit physical neighborhoods, and the opposite-pivot GF(2) solver. It checks all 36 directed selected paths, every newly computed G failure, representative new successful geometries/modes, both nonzero-rank successes, and all 36 no-carrier rules for native/source/parent gates. Cached paths retain their existing independent audits.

All checks passed: 64 eligible rules plus 36 no-carrier rules; **300 native/recovery decisions, {v['independent_GF2_branch_decisions']} symbolic branch decisions, and {v['direct_recursive_G_cells']:,} direct physical-G cells**. Verification took {v['seconds_total']:.2f} seconds, for about {s['seconds']+v['seconds_total']:.2f} seconds of primary plus targeted computation.

Alphabet: one bit per site. Source radius: one. Native radius: two in each lifted axis. Preparation: nonlinear distance-three pair references, repeated diagonally; all added axes have period four. There are four fields in 2D and sixteen in 3D per horizontal source coordinate. The prepared family still has only the source line's independent information. G is guaranteed on nested P/D layers, not every physical row or arbitrary off-image configuration. Faithfulness and G alone do not distinguish this from all copy/stripe mechanisms; independent higher-dimensional information and a general recursion theorem are unproved.

## Morning synthesis and next discriminating question

The obsolete three-row filter hid most of the first-floor coverage. Removing it exposed just two source-recovery holdouts, 23/232. Exact periodic complement witnesses showed that their symmetric-Q encodings erased a global color distinction; changing labels, row order or decoder radius could not repair the unchanged encoding. Directed mismatch Q preserved the missing distinction. Neither Q reflection orbit alone is universal, but their four-formula union is faithful for all 256 and now repeats faithfully once into 3D.

The remaining separation is between dynamical faithfulness and commutator closure: 220 first-floor carriers, 200 successes under the prescribed 3D selection, 206 with existing alternative paths. The earlier 4D baseline remains 113 faithful / 105 recursive-G paths, with no new 4D or 5D computation.

Ranked questions:

1. {questions[0]}
2. {questions[1]}
3. {questions[2]}

**Recommended next experiment:** classify the saved native/probe collision witnesses across all faithful first-floor recipes for those 36 rules. Seek a single missing relation that repairs the collision at the current alphabet and radius. Reuse the completed census; do not rerun it. A field proposal that leaves a whole-image collision unchanged is rejected before any recursive run.

The five planned cycles are complete. The continuation is stopped at this checkpoint; a later explicit research request can start from these questions. All unchanged exact no-gos remain retired.

Artifacts: `ca_lift_lab/runs/universal_3d/` contains the selected recipes, individual gates, symbolic completions, verification outputs, best-known G paths and manifests. The harness and verifier are `audit_universal_3d.py` and `verify_universal_3d.py`.
'''
(BASE/'universal-3d-results.md').write_text(report)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
statepath=BASE/'overnight_research/state.json';state=json.loads(statepath.read_text())
state.update({'updated_at':now,'cycle':5,'status':'completed_planned_cycles','latest_run':'ca_lift_lab/runs/universal_3d','three_dimensional_selected':{'paths':256,'native':256,'source_recovery':256,'parent_recovery':256,'G_eligible':220,'original_G':115,'centered_only_G':85,'recursive_G':200,'failed_selected_G':s['recursive_G_constraint_failures'],'reused':53,'new':203},'three_dimensional_best_known':{'recursive_G':206,'original_G':121,'centered_additional':85,'earlier_alternatives':extra,'eligible_unresolved':unresolved},'next_priority':questions[0],'automation_id':'6aa7a38968cc8191930cb342dea9e12d','automation_enabled':False,'stop_reason':'Completed five planned bounded cycles; do not launch further work without a new explicit research request','personal_context':'Search completed: no matching conversation, relevant saved-file context recovered; supplied conversation and durable context consistent'})
state['retired']+=['Repeated unchanged selected3D failures','First-floor-only selector as sufficient for universal recursiveG','Claim all successful Gextensions leave parent completion entirely free']
statepath.write_text(json.dumps(state,indent=2)+'\n')
entry={'cycle':5,'type':'experiment_and_synthesis','time':now,'goal':state['mission'],'last_lesson':'Four-reference reflection-closed union gives256faithful first floors,133originalG,220centeredG','ranked_before':['All256selected native/recovery into3D','RecursiveG for220eligible carriers','Structural failure causes'],'experiment':'One first-floor-selected recipe per reflection orbit, all256into3D; cache exact prior cases, symbolic parent completions','learned':state['three_dimensional_selected']|{'best_known':state['three_dimensional_best_known'],'missing_first_floor_G':36,'nonzero_parent_constraint_rank_rules':[157,199]},'verification':v,'seconds_census':s['seconds'],'costs':json.loads((RUN/'manifest.json').read_text()),'reassessment':'Universal finite-depth native/recovery repeat achieved; G and indefinite nontrivial recursive closure remain open; no4D/5Dclimb','retired':state['retired'][-3:],'top_questions':questions,'chosen_next':'Cached-witness classification for all36first-floorG holdouts, conditional on next explicit request','kill_conditions':['No repetition of unchanged exact failures','Any candidate must resolve its target witness before recursion','No universalG claim from200or206paths','No novelty claim from faithfulness alone'],'personal_context':state['personal_context'],'status':'completed_planned_cycles','artifacts':['universal-3d-results.md','ca_lift_lab/audit_universal_3d.py','ca_lift_lab/verify_universal_3d.py','ca_lift_lab/runs/universal_3d']}
with (BASE/'overnight_research/ledger.jsonl').open('a') as f:f.write(json.dumps(entry,separators=(',',':'))+'\n')
briefpath=BASE/'eca-overnight-brief.md';brief=briefpath.read_text()
brief=brief.replace('## Current state\n','## Current state\n\n- **Cycle5complete; planned continuation stopped.** All256selected paths retain native3D evolution and source/parent recovery. RecursiveG:200/220eligible (115original,85centered-only selection);36missing first-floor carriers are separate.53exact prior cases reused,203new;26.19s. Targeted independent verification:64eligible+36no-carrier rules,300first-order decisions,106GF2branches,5,636,096physicalGcells;34.03s. Earlier alternatives for14/84/110/124/206/220raise best-known3DG to206 (121original,85additional centered). Two new successes157/199require rank-one parent completion conditions. See `universal-3d-results.md` and `ca_lift_lab/runs/universal_3d/`.\n')
start=brief.index('## First experiment resolved; next question');end=brief.index('## Execution discipline',start)
brief=brief[:start]+'''## Completed sequence and next question

The five planned bounded cycles are complete and the continuation is disabled. Subsequent scheduled invocations should exit promptly. A new explicit user request may continue research from the saved state.

**Do not repeat the first-floor censuses or selected3D census.** Native evolution and both recovery gates now cover all256through3D. Universal G still has36first-floor gaps plus14eligible rules without a known3Dpath. Selected failures are recipe-specific; keep earlier successful alternatives, especially Rule110. Self-reflecting rules use an orientation convention, not a reflection-fixed signed recipe. Directed mismatch Q is not globally complement-odd in the strict Boolean sense; complement swaps the directed relation.

Ranked next questions:
1. Classify saved native/probe collisions across every faithful first-floor recipe for the36rules without centeredG carriers. Which missing relation must a repair preserve?
2. Classify forced constraints for the14eligible rules without any saved3DGpath, reusing exact results; no unchanged retry.
3. Find a local invariant sufficient for general recursion, accounting for the rank-one parent-completion constraints in157/199. Do not infer this from another higher-dimensional example.

Recommended next experiment, only on an explicit continuation: cached-witness classification for all36first-floorG holdouts. Keep alphabet/radius fixed, and reject any proposed relation that leaves its target collision unchanged.

'''+brief[end:]
briefpath.write_text(brief)
print(json.dumps({'report':str(BASE/'universal-3d-results.md'),'cycle':5,'status':state['status'],'best_known_G':206}))
