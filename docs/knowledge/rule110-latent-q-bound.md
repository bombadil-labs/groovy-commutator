# Minimal latent Q restores finite autonomy while retaining almost the source

Status: exact on the seven full Rule-110 source rings n=6,8,...,18, under
F=H^2, with a uniform source prior. No infinite-line extension is claimed.

Future-equivalence refinement gives the coarsest autonomous representation
retaining a chosen current observer O. Every other autonomous refinement
retaining O must distinguish at least these classes. Consequently its
conditional source entropy is at most that of this quotient.

For O=(block-2 parity, entire G), the exact quotient has 2^n-2 classes at
every tested width. Only the uniform pair and alternating pair are merged.
The best possible forgotten information is 4/2^n bits on this finite list.
G-only also becomes nearly injective after refinement. Parity-only leaves
substantially more ambiguity; preserving G changes the information contract.

Minimal Q fields in {0,1}^n are constructed by matching stabilizer orbits
over the visible fibers. They commute with one-site translations for G and
two-site translations for blocked parity/G. Whole-field (O,Q) evolution is
autonomous on every tested ring, but the chosen construction has update
collisions at every tested radius 0--3 across those widths. Passing the three
repetition checks does not establish a single full-line encoder.

The aligned six-field lift is lossless because its last two rails XOR to
the source. The computed quotient therefore factors that sufficient lift.
This does not analyze its ambient native completions or minimize a spatial
automaton. At n=18, Q adds only 0.2514 conditional bits over parity/G, but
the joint state is almost microscopic. A small latent coordinate does not
imply large total compression.

The [research note](../research/2026-10-07-rule110-latent-q.md) preserves the
protocol, optimality argument, all failures, exact witnesses, array
certificates and provenance repair. The local-track negative is strengthened
to an encoding-independent finite-domain bound. A changed observer/domain
or a full-line proof would be a separate unit. Reviewed by: none.
