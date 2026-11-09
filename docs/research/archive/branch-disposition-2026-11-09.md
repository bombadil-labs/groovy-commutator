# Disposition of unmerged branches, 2026-11-09

On 2026-11-09 the remote held 105 branches that Git did not count as merged
into `main`, and one checkout held two commits that had never been pushed.
This record says what each contained and what was done, so that the branches
can be deleted without losing anything. **No branch had been deleted when this
was written.** Tips are full commit hashes.

## How each branch was classified

A branch counts as *fully represented* when every file version at its tip that
differs from the merge base already appears somewhere in the history of
`main`, as the identical blob. That test is exact and does not depend on how
the work was merged. Branches that fail it were inspected file by file.

## Integrated on 2026-11-09 (13 branches)

The October gathering branches. All thirteen open pull requests' head commits
are contained in the integration merge. See
[the review and integration record](../2026-11-09-october-integration-review.md).

| Branch | Last commit | Tip | Pull requests |
| --- | --- | --- | --- |
| `gather/cocycle-lift-20261006` | 2026-10-06 | `f073b636bfda655695a2688ea1890976b11d9f8f` | #316 open |
| `gather/asymptotic-closure-20261007` | 2026-10-07 | `e318132332eaeb41b0cf8272483ddb0a677035e0` | #318 open |
| `gather/asymptotic-closure-scaling-20261007` | 2026-10-07 | `ed4f776c1e0b83efef828c2579d5921bb0ac5779` | #320 open |
| `gather/asymptotic-closure-wedge-20261007` | 2026-10-07 | `41e57570054d6bf9a375cae0456ba7897472799a` | #319 open |
| `gather/commutator-jet-20261007` | 2026-10-07 | `7a257bd30bc2d131bcacb08d88d84be27a8e823e` | #324 open |
| `gather/commutator-jet-fibers-20261007` | 2026-10-07 | `68768df68849d9e649760ac8b17d7c014543325f` | #326 open |
| `gather/commutator-jet-language-20261007` | 2026-10-07 | `1059cd8d3e434bd3b52aa2b618fedbf8416986d5` | #325 open |
| `gather/jet-control-panel-20261007` | 2026-10-07 | `327489586320f06dec6fd9ac60e861a5727c055b` | #327 open |
| `gather/jet-gqr-256-fibonacci-20261007` | 2026-10-07 | `a57e7e6e08fa23e6452f2cc86f0eaf81796c94dc` | #328 open |
| `gather/matched-history-transport-20261007` | 2026-10-07 | `2a142541ff9bb5e5c6322fb1c7ed8bafd991ce36` | #321 open |
| `gather/rule110-latent-q-20261007` | 2026-10-07 | `953978e626c40673cc6646c318f1a9d63f0f700f` | #323 open |
| `gather/rule110-pg-closure-20261007` | 2026-10-07 | `6eab1fe4fb08648e405d3c7d3768e61276de4024` | #322 open |
| `gather/jet-full-line-autonomy-20261007` | 2026-10-08 | `ebffd1803044ae67c51b180b790105ff9a9c58dc` | #329 open |

## Recovered into `main` on 2026-11-09

| Source | Tip | What was recovered |
| --- | --- | --- |
| `research/relational-source-recoder-20260909` (#55 closed) | `2ff683a217d1f163d2dd62ec213d83afa1bf4b7c` | Seventeen files that existed nowhere on `main`: the phase-splice note, the SAT recovery result and its summaries, the two-switch rail-selector protocols and their scripts. The pull request was closed as superseded by #231 with a comment that its content had been carried forward; #231 carried a different, later subset. `scripts/experiment_two_switch_rail_selector_sat.py` on `main` referred to a protocol file that only this branch held. Recovered verbatim at the original paths. **Unreviewed and unregistered**; the phase-splice note reports an exact negative on all 22 seed languages for one splice family, which is narrower than, and consistent with, the archived-incomplete status of the wider recoder search. |
| local `chore/adlc-bootstrap` (never pushed; its pull request #1 was closed) | `8ac434956dc31cf497fc85fcce31fa5f173fee5a` | The July finite-ring attractor unit: script, results and a rewritten account, [the commutator where a ring settles](../2026-11-09-g-on-attractor.md). The branch's edits to the old agent guide and notes were not carried over, because both files have since been replaced. |

## Holds content that is not on `main`, deliberately not migrated

| Branch | Tip | Content and reason |
| --- | --- | --- |
| `noop-should-not-exist` (no pull request) | `458a6ff867afba24afcee4d86be1f393287809fa` | A frozen protocol and control implementation for "symbolic defect normalization" (three files, four commits, 2026-09-09). Never evaluated, never opened as a pull request, and its own name says it was pushed by mistake. The question it posed was overtaken by the source-recoder line. |
| `gather/structured-nonclosure-20261007` (#317 closed) | `372b6c2db93a0e58768aebe4671b5ed0f9e7d586` | One frozen protocol, closed unevaluated when the question was sharpened into the asymptotic-closure unit. The pull request records that disposition. |

## Fully represented, pull request merged (58 branches)

Leftover heads of merged pull requests.

| Branch | Last commit | Tip | Pull requests |
| --- | --- | --- | --- |
| `research/closure-defect-20260908` | 2026-09-08 | `037fe45f79aab3792578077280fbd932a50615f9` | #19 merged |
| `research/fiber-visibility-20260908` | 2026-09-08 | `a226a866fce240700b3af695107342844c67061a` | #23 merged |
| `research/history-lift-closure-20260908` | 2026-09-08 | `80a76d231044f9fc11fbc35e9fbcaa99323b8997` | #20 merged |
| `research/observer-search-20260908` | 2026-09-08 | `a551fb89f139cf041bf8f16d3fc1f83dce84b370` | #22 merged |
| `research/possibility-frontier-20260908` | 2026-09-08 | `fbc9eeeb8717156f73d952091a0ff57760c1e149` | #25 merged |
| `research/pulse-scattering-20260908` | 2026-09-08 | `4acd5883c7f43a264711a066f2b5a5ad771cd11b` | #17 merged |
| `research/pulse-shape-scattering-20260908` | 2026-09-08 | `8fb5027dfe398a8e3ce29162b1da4904227d1dee` | #18 merged |
| `research/representation-design-main-20260908` | 2026-09-08 | `f1382ff69cfb3f25683db007571256458da98fdb` | #28 merged |
| `research/selector-shielding-20260908` | 2026-09-08 | `ec71d4ce14f7aa63a9e365e96e8e3c30e3d55041` | #21 merged |
| `site/research-program-20260908` | 2026-09-08 | `001606ce826dc51f62b2a40304896f1ec2b4a332` | #24 merged |
| `ci/contextual-quotient-validation` | 2026-09-09 | `a3e6d14c4959828da88ecff0f2a745024eae49c3` | #31 merged |
| `ci/remove-contextual-quotient-bootstrap` | 2026-09-09 | `d92d1b178507d07d7f3f300c7cef7d0a69faceca` | #32 merged |
| `feature/multiple-research-programs` | 2026-09-09 | `ef09583a7f9123a2275f26d2dec8fc6e2ba14dab` | #44 merged |
| `fix/research-index-order` | 2026-09-09 | `1fc1046ad4635e51070d43c90c77ccc06d1ccb6f` | #43 merged |
| `fix/research035-number-collision` | 2026-09-09 | `b635564947b77a4d3e730180663fbc5cc63ccae7` | #42 merged |
| `fix/sofic-note-036-identity` | 2026-09-09 | `ab4c5bdd486918ba22a1ae1f47dc7a01ad316165` | #48 merged |
| `research/astra-dimensional-closure-review-20260909` | 2026-09-09 | `1b367de8a23beb16fd21f0389728ac36f63b1706` | #45 merged |
| `research/block3-representation-design-20260908` | 2026-09-09 | `203dc0e162e3586054a440c54e6cfaa4be7c88e7` | #29 merged |
| `research/causal-witness-automaton-20260909` | 2026-09-09 | `d86debef469b7a407159bbfd6f6e71b90f3782da` | #37 merged |
| `research/causal-witness-horizon-20260909` | 2026-09-09 | `9ec8c38ed60b1a5d129d623190f58bcd5a4f8b6b` | #36 merged |
| `research/dimensional-intertwining-20260909` | 2026-09-09 | `67147e04f0163df311c392631ccebc1a2f812251` | #35 merged |
| `research/editable-routing-tables-20260909` | 2026-09-09 | `9d8279e5e522b937f3136bda3ad0983bf0471042` | #51 merged |
| `research/extension-freedom-20260910` | 2026-09-09 | `c5c380ecd80e53ff7ac1e8c64edcd267a8d61cd4` | #56 merged |
| `research/fatal-predictive-synergy-20260908` | 2026-09-09 | `037b28e971e6c2fbd82accb44c675e450a260894` | #30 merged, #33 closed |
| `research/finite-horizon-quotients-20260909` | 2026-09-09 | `6adbf519b97156ea809b46c5ca7ed35e2091e13a` | #34 merged |
| `research/finite-routing-boundaries-20260910` | 2026-09-09 | `1a012ae350e73f2091940aa79a47f9b036ed8fd3` | #52 merged |
| `research/guard-free-axial-lift` | 2026-09-09 | `923e777d5fb8c112b2bc0847af9343e476d9c9f7` | #57 merged |
| `research/local-correction-caps-20260910` | 2026-09-09 | `f65a63ea5a96824cbed850043b286ad0e5b7c3be` | #53 merged |
| `research/program-edit-locality-20260909` | 2026-09-09 | `43a3fa8e311e9c472f0abdf099c57a4607548d6b` | #47 merged |
| `research/reachable-context-invariants-20260909` | 2026-09-09 | `7e02234fd3b3b00c0653df7593615ea689183c92` | #39 merged |
| `research/rule32-physical-cap-20260910` | 2026-09-09 | `346f146b94df10c55b8488718c25fd88589fb269` | #54 merged |
| `research/sofic-defect-orbit-20260909` | 2026-09-09 | `826f367d90f395cffd36cb44e66e5440422b16a1` | #41 merged |
| `research/spatial-rail-programs-20260909` | 2026-09-09 | `4916f9d9ee4d58ba75f9126a13ae11ccb714722c` | #50 merged |
| `research/symbolic-sofic-image-20260909` | 2026-09-09 | `df2f20342f48e152be2301fe9ff60feef96a85d5` | #49 merged |
| `research/window3-reachable-language-20260909` | 2026-09-09 | `94f8336e653a496294c316f3869085a52883f627` | #40 merged |
| `docs/agreed-issue-burndown` | 2026-09-10 | `78d6f4883560b7606bacb4297bafd357e224fcfb` | #70 merged |
| `docs/issue67-second-lift-protocol` | 2026-09-10 | `a8550eb231cca259ac1bf2ce8b9f09b3c2976ddf` | #77 merged |
| `docs/issue68-resonance-concepts` | 2026-09-10 | `bdc758c5fbedbaf394cc8f7d869303cf7f49f9ed` | #76 merged |
| `docs/representation-empowerment-protocol` | 2026-09-10 | `541cbce91df324647b6cb2a2c1104dd85928ac10` | #72 merged |
| `docs/shared-closure-account` | 2026-09-10 | `ae4617fed499f87adaad96634c55709c679a901d` | #71 merged |
| `research/conservative-online-observer` | 2026-09-10 | `4847e6b8dc599d1c3405ab476a7f7a2337d197d3` | #78 merged |
| `research/full-gradient-closure` | 2026-09-10 | `2860f8f8709153a911d41faf44627b13d3f70d8b` | #59 merged |
| `research/gradient-intervention-costs` | 2026-09-10 | `6b8cb088aa4b33b1ac17543e067bfa15372bf612` | #69 merged |
| `research/gradient-loop-invariants` | 2026-09-10 | `dc56e51e159ab2d082acb243d041e460956e5a20` | #60 merged |
| `research/issue62-successor-archive` | 2026-09-10 | `9242750e3eb306fe03c842f6aeeca8b6720d5d1c` | #73 merged |
| `research/issue65-relabeling-archive` | 2026-09-10 | `47d9e9fa59d424498f5ab0c547d30a20fa5cd8e1` | #74 merged |
| `research/issue66-constructor-inventory` | 2026-09-10 | `9580b21f960f1541b0127dc46e3ed0484e9ce7fd` | #75 merged |
| `research/transverse-difference-closure` | 2026-09-10 | `6200ee0751e6a6793c50382622cf85a3bdddc5ed` | #58 merged |
| `docs/multi-agent-collaboration` | 2026-09-12 | `e92ccf84bb59e9d8b590644763cda3e1af16023f` | #133 merged |
| `records/binary-lift-gate2-accepted` | 2026-09-14 | `a1b099160302487f9ca53f2a2217a9c04e365425` | #234 merged |
| `gather/absential-claim-boundary` | 2026-09-22 | `7efdd9149a62006ba93551e8597fd1030ea6ba1b` | #291 merged |
| `gather/phase-free-consumer-audit` | 2026-09-22 | `e91e1dcdb1830ceeb4dd26f166fab53207b0964f` | #285 merged |
| `gather/public-status-stop` | 2026-09-22 | `a505a4d99affec59efcdb63fb01ea3e4f8633f12` | #290 merged |
| `gather/recursive-g-boundary` | 2026-09-22 | `931c69cb8125e1d4f9c7281537285320d775e90d` | #287 merged |
| `gather/representation-empowerment-disposition` | 2026-09-22 | `74aa9780a1840ad5bdb190e00f119652454843ec` | #288 merged |
| `gather/research-drive-integration-record` | 2026-09-22 | `4a0647c9b0e5e114107b88c5eb1bf3f8adfcc5af` | #286 merged |
| `gather/research-drive-synthesis` | 2026-09-22 | `0fee77e7a7346509d7a35a59055ce487ba5ea575` | #292 merged |
| `gather/second-lift-status-repair` | 2026-09-22 | `8736fcca22cbe75b4970453159d9951e39ce1b22` | #289 merged |

## Fully represented, pull request closed or absent (10 branches)

Every file version is in the history of `main`; the work reached it by another
route.

| Branch | Last commit | Tip | Pull requests |
| --- | --- | --- | --- |
| `chore/adlc-bootstrap` | 2026-07-12 | `f4a3a582b273ee87025167ec3d08b432ad2ae86e` | #1 closed |
| `chatgpt/access-check-20260909` | 2026-09-09 | `b2f8f28fc3d71358d3164f347cd513766aacb2c6` | none |
| `research/causal-witness-horizon-ci-20260909` | 2026-09-09 | `c784f586fd9d01b759616c2d6027cc3f3d5ddf21` | none |
| `research/dimensional-history-scaling-evaluation` | 2026-09-12 | `930ccffb2082003834bf71c971f13e5d805f802d` | #183 closed |
| `research/interface-history-cross-width-evaluation` | 2026-09-12 | `7876930649e9251af8e83865ceb02bb7861f34a6` | #167 closed |
| `research/predictive-assembly-support-evaluation` | 2026-09-12 | `8ef31cd8635a86b03060eddf035c0d4b625fcb51` | #182 closed |
| `work/ci-cost-boundary/policy` | 2026-09-12 | `bb3ffe9caf2f07c15985087c49521055b05c8e31` | none |
| `work/dimensional-resonance-response/reconcile-main` | 2026-09-12 | `71ba2f1c54204f7b26cba521463dd5b7245371c3` | #208 closed |
| `work/dimensional-resonance-response/reconcile-main-v2` | 2026-09-12 | `6677edbad491fd56d83a6f4856484f534fcf42cb` | none |
| `work/closed-violation-depth-three/evaluation-local` | 2026-09-13 | `f22410cd45e24bc36cac6d5d6a0029b0f8ac1165` | none |

## Superseded intermediate versions only (21 branches)

Each of these holds one or more file versions that never appeared on `main`,
at paths where `main` has a later version of the same file. They are drafts
that a later branch replaced, or duplicates of an edit that reached `main` by
another pull request. Two were inspected individually and are noted.

| Branch | Last commit | Tip | Pull requests | Files with a version not on `main` |
| --- | --- | --- | --- | --- |
| `claude/website-exploration-experiments-vrw9yf` | 2026-09-07 | `6aa5b091ab2d3ec16d657e13af712bc2dd5882bc` | none | `site/src/components/Concepts.jsx`; `site/src/components/Home.jsx`; `site/src/components/Questions.jsx` |
| `research/history-repairability-2026-09-07` | 2026-09-07 | `b752cfbf6239bc0094911d333810cfba73c2aaba` | #2 merged | `site/src/components/Concepts.jsx`; `site/src/components/Home.jsx`; `site/src/components/Questions.jsx` |
| `research/causal-shielding-20260908` | 2026-09-08 | `12db2c52d1061fe131a54a3ead8686a4457a03d5` | none | `docs/research/2026-09-08-pulse-shape-scattering.md` |
| `research/representation-design-20260908` | 2026-09-08 | `7700ea40826f3e47ea3c19f94f5e6a4772aab880` | #26 closed, #27 closed | `docs/research/2026-09-08-representation-design.md`; `docs/research/CI.md`; `docs/research/protocols/representation-design-20260908.md` and 2 more |
| `research/reachable-context-invariants-20260909-aaa` | 2026-09-09 | `d802d56d5827e2533d068cc0f8e0ee9eec8a313b` | none | `scripts/experiment_reachable_context_invariants.py` |
| `research/reachable-context-invariants-20260909-copycheck` | 2026-09-09 | `d802d56d5827e2533d068cc0f8e0ee9eec8a313b` | none | `scripts/experiment_reachable_context_invariants.py` |
| `research/reachable-context-invariants-20260909-final` | 2026-09-09 | `d802d56d5827e2533d068cc0f8e0ee9eec8a313b` | none | `scripts/experiment_reachable_context_invariants.py` |
| `research/reachable-context-invariants-20260909-pr` | 2026-09-09 | `d802d56d5827e2533d068cc0f8e0ee9eec8a313b` | none | `scripts/experiment_reachable_context_invariants.py` |
| `research/reachable-context-invariants-20260909-temp` | 2026-09-09 | `d802d56d5827e2533d068cc0f8e0ee9eec8a313b` | none | `scripts/experiment_reachable_context_invariants.py` |
| `research/selector-program-two-lift-20260909` | 2026-09-09 | `f4b49ed5b44f1f8f943337fc400fec23a329bcde` | #46 merged | `site/content/research-program.json` |
| `work/dimensional-interface-factor/implementation` | 2026-09-11 | `86946884f2ade706641ec8dbe93046edb9ab1055` | none | `scripts/verify_interface_factor.py` |
| `work/dimensional-intervention-axis/gate1-clarifications` | 2026-09-11 | `29ac5dde2041966e566d5e6332a533ff206e8e8b` | #115 closed | `docs/research/protocols/intervention-axis-20260911.md` |
| `work/dimensional-spatial-axis/gate1-clarifications` | 2026-09-11 | `25af3422a430d331c6fb1e3a80cccbcd051e51fa` | #105 closed | `docs/research/protocols/transverse-freedom-20260911.md`. An alternate wording of the same two gate clarifications; closed as a duplicate of #104, whose wording is on `main`. |
| `work/dimensional-spatial-axis/report` | 2026-09-11 | `a0cf57d9df594d1f13f37a60f08f3ebb637d81f7` | #109 closed | `docs/knowledge/transverse-freedom-criterion.md`; `docs/research/2026-09-11-transverse-freedom.md`; `site/content/research/transverse-freedom.json`. Its knowledge page `transverse-freedom-criterion.md` is on `main` under the name `transverse-freedom-capacity.md`. |
| `gather/dimensional-beam-resonance` | 2026-09-12 | `de5c26aa16f4cb22f1beee8b86368f84ed736827` | none | `docs/research/2026-09-09-dimensional-closure-program.md` |
| `work/dimensional-relational-rank/evaluation` | 2026-09-12 | `4f1e00d193557c7f65abe0c38815e2fb9c019c0b` | #150 closed | `results/relational_rank_20260912.json` |
| `work/dimensional-zero-base/current-account` | 2026-09-12 | `eaf56d13e2f518a1052ecbd537d151100dccada7` | none | `docs/research/checkpoints/dimensional-lift.md` |
| `work/dimensional-zero-base/reporting` | 2026-09-12 | `4b1873ae2fe36057362ea3caa0e15c80684df687` | #143 closed | `docs/knowledge/zero-dimensional-selector-overlap.md`; `docs/research/checkpoints/dimensional-lift.md` |
| `work/dimensional-zero-base/reporting-v2` | 2026-09-12 | `8c744d61502a77304b82b73b0b042672ff67bd1d` | #145 closed | `docs/research/checkpoints/dimensional-lift.md` |
| `work/interface-history-cross-width/reporting` | 2026-09-12 | `5681412cadf5c0f1397a8aa8457031eec507f982` | none | `docs/research/2026-09-09-dimensional-closure-program.md`; `docs/research/checkpoints/dimensional-lift.md` |
| `work/closed-violation-depth-three/reporting` | 2026-09-13 | `2d310c31688d1513f9bee22429d69dfe56b3a5b5` | #224 closed | `docs/research/2026-09-13-closed-violation-depth-three.md` |

## Local branch

`claude/website-exploration-experiments-vrw9yf` was the default branch before
`main` existed. Its remote copy is in the table above; nothing on it is absent
from `main`.

## If the branches are deleted

Every branch above that has a pull request can be restored from that pull
request on GitHub. The 17 branches with no pull request cannot, once
their commits are collected. Before deleting those, either keep
`noop-should-not-exist` or push its tip to a non-branch ref such as
`refs/archive/noop-should-not-exist`; the rest hold nothing that `main` lacks.
