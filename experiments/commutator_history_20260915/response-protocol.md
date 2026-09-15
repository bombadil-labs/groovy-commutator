# Repeated perturbation: a bounded four-arm follow-up

2026-09-15, frozen after the commutator-history result and before this follow-up. Owner: Codex /root. Protocol review: none at freeze; run authorized by Myk's standing Gate 1 approval and new message proposing prior-perturbation modification of later responses. Independent review follows before integration.

## Claim and limit

The user proposes operational remembering through changed responsiveness. A deterministic autonomous CA cannot retain an effect of history outside its complete current state: identical full states, identical future interventions imply identical futures. This experiment tests causal response modulation by a first pulse, not learning, beneficial adaptation or a feedback mechanism driven by the derived commutator.

Use four arms: neither pulse (00), first pulse only (10), second only (01), both (11). Pulses XOR one cell. After the second pulse, define responses R0=S01 XOR S00 and R1=S11 XOR S10; the interaction I=R0 XOR R1. This cancels the direct lingering first disturbance. I[0]=0. An affine rule has I=0 for every input and pulse schedule. Nonzero I may simply be nonlinear state dependence; Class IV specificity is explicitly in question.

## Exact short-delay census

For all 256 ECAs, enumerate all 128 seven-cell source contexts. First pulse is at the center, wait one step, second pulse is at that same physical cell, then observe one step later. Score I on the three cells reachable by the second pulse. All source dependencies of those outputs lie in the seven-cell window. Report how many contexts admit nonzero interaction per rule and one explicit witness for rule 30 if any. This is an exact local census, not a long-time class test. Include an exhaustive 13-cell version (8192 inputs) for the radius-two correction family.

## Delayed native-trajectory probes

Use the first retained R6 state for rules 0,1,30,54,73,90,106,110,122,126,150,204 and seeds 6041512..6041514. Use the first retained R10 state for all six radius/correction families at seed 6041542. Earlier trajectory and G results are known; these response measurements are new and exploratory.

For each input, use 16 evenly spaced initial pulse locations, delays 16 and 64, and second-pulse offsets -r*delay, 0, +r*delay. Add a remote control at r*(delay+64)+1, too far for the two influence cones to overlap during the 32-step response horizon. Analyze h=1,8,32. Extract adequately padded initial windows and evolve by shrinking open-window steps. For ECAs, initial window extraction respects the archived ring. For R10 choose only origins with the full initial window inside its saved open strip. Half-padding is 2*r*(delay+32)+remote_offset; it includes the entire support of both responses through h=32.

Record changed-response indicators, I cell counts and XOR/union ratios. Before the second pulse, record whether the two worlds have identical radius-2r local neighborhoods at the probe and whether the first pulse has completely disappeared. Also record the 16 most recent causally available G bits in each world at the eventual probe location: times delay-17 through delay-2; for delay 16, use 0 through 14 (15 bits). Compute G from native frames only through the encounter time. Descriptive strata may use whether any of those local G bits differ; no predictor or class threshold is fitted to them.

## Checks and reporting

The remote interaction must vanish. If the first pulse has disappeared, every later interaction vanishes. Matching radius-2r probe neighborhoods imply I[1]=0. Known affine controls 90,150,204 must have zero interaction at every tested time; zero rules and pure shifts provide additional controls.

Report this finite geometry and the three effective local probes separately from the remote control. History-sensitive response in chaotic or periodic controls defeats the specificity of the bare modulation criterion; it does not refute a stronger theory involving selective retention, response quality or plasticity. Neither changing response nor observing G history alone proves that G causally feeds back into the update law. No analogy to immune or clinical phenomena is treated as a scientific result.

Local budget: five minutes; no automatic scientific evaluation in Actions. Preserve per-trial arrays, hashes, sources, results and independent review. Do not refit the previously frozen discriminator or memory threshold.
