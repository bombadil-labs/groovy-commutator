# Protocol: dimensional rule closure as a Class-IV discriminator

Date: 2026-09-09
Status: preregistered before outcome-directed search

## Motivation

Two earlier constructions suggest that a lower-dimensional rule table can become literal spatial data one dimension higher:

1. an unrestricted ECA has eight output bits, which can be placed on the eight-cell ring around the center of a 3x3 Moore patch; the resulting local selector reads a three-bit address and copies the corresponding ring value;
2. for binary outer-totalistic radius-one Moore rules, a d-dimensional rule has 2*3^d bits, exactly the capacity of the two outer 3^d-cell layers in a (d+1)-dimensional radius-one neighborhood, with the central layer carrying the lower-dimensional input neighborhood.

The present question is stronger than arbitrary CA simulation or embedding. We ask whether a lower-dimensional rule can be promoted by one of these *specific rule-as-geometry constructions* so that the promoted object is itself describable by a native rule in the higher-dimensional representation family, allowing dimensional promotion to continue.

## User-supplied strong hypothesis

The deliberately optimistic hypothesis is:

> Dimensional rule closure is present for Wolfram Class IV elementary cellular automata and absent for Classes I-III.

This is a hypothesis to try to falsify, not an assumption used to select a representation.

## Anti-overfitting rule

No Class-IV labels may be used to choose among candidate lift geometries, decoder conventions, closure tolerances, or search objectives.

Candidate constructions and success criteria must be frozen first. Class labels are joined only after the structural measurements have been produced.

If several equally natural conventions exist (for example rotations/reflections, ring permutations, address axes, or transverse orientations), report the full distribution over the frozen convention family rather than selecting the convention that best separates classes.

## Class labels

The primary ECA analysis will use a frozen repository labeling if one already exists and will preserve symmetry equivalence explicitly. Because Wolfram classes are qualitative and published ECA tables differ on boundary rules, two reports are required:

1. the frozen primary labels used by this repository;
2. a sensitivity report over at least one published alternative labeling, with no retuning of the dimensional criterion.

The strong claim passes only if exclusivity survives the primary labeling. Alternative-label sensitivity is descriptive, not a rescue criterion.

## What counts as dimensional rule closure

A useful criterion must distinguish rules. Merely storing a truth table in a higher-dimensional patch, or applying the already-defined universal selector/interpreter, does not count because those properties hold by construction for every admitted rule.

We will evaluate increasingly strong closure levels.

### Level 0: local storage fit

The lower-dimensional rule bits occupy the prescribed higher-dimensional boundary/layers. This is a construction check only and cannot support the hypothesis.

### Level 1: local native-rule closure

After promotion, the induced higher-dimensional local input/output relation belongs to a frozen higher-dimensional native rule family without carrying an external decoder state that is not itself represented in the promoted patch.

Equivalently, the promoted relation must be compressible into the declared next-dimensional rule representation and reproduce the promoted update on every local patch in the tested domain.

### Level 2: overlap-consistent spatial closure

The promoted rule representation can be realized on an extended periodic lattice with overlapping neighborhoods satisfying the same local encoding constraints simultaneously. This eliminates constructions that fit in one isolated patch but cannot coexist spatially.

### Level 3: persistent closure under evolution

Starting from an overlap-consistent promoted encoding, at least one full update under the native higher-dimensional rule leaves the configuration inside the same decodable representation family, so a higher-dimensional rule can be decoded again after evolution.

For bounded finite systems we record persistence depth before first exit, with `infinity` only when exact graph analysis proves invariant closure.

### Level 4: recursive dimensional closure

The decoded higher-dimensional rule itself admits the same kind of promotion to dimension d+2 under the frozen construction. The first practical target is a verified 1D -> 2D -> 3D chain.

A rule satisfying a weaker level is not promoted to a stronger claim.

## Candidate construction families to freeze before evaluation

### A. Eight-bit Moore-ring construction

Use the existing unrestricted ECA eight-bit ring encoding from `2026-09-08-shared-state-rule.md`.

Freeze all geometric degrees of freedom already present in that construction:

- all 8! rule-entry-to-ring assignments, or a symmetry-reduced enumeration with exact multiplicities;
- horizontal and vertical three-bit address axes;
- rotations/reflections treated as equivalences rather than independent evidence.

The first task is not to search these encodings for Class-IV separation. It is to derive which higher-dimensional native rule representations, if any, can be decoded from the induced relation without referring back to the lower-dimensional rule table externally.

### B. Layered outer-totalistic construction

Use the existing `2*3^d` storage fit from `2026-09-08-dimensional-lift.md` as a control family. Its known failure of automatic recursive closure must be reproduced before extending it.

Because it admits only 64 reflection-symmetric ECAs at d=1, it cannot by itself test the unrestricted 'Class IV and only Class IV' hypothesis. It is a mechanism control for the meaning of closure and its obstructions.

## Primary structural outputs

For each ECA rule and each frozen construction/equivalence class, record without class labels:

- strongest closure level reached;
- number/fraction of geometric encodings reaching each level;
- minimal representation cost of a native higher-dimensional rule, if one exists;
- persistence depth under higher-dimensional evolution;
- whether failure is local representability, overlap consistency, persistence, or recursive promotion;
- symmetry orbit identifiers so conjugate/reflected rules are not counted as independent replications.

Only after this table is frozen are Wolfram labels attached.

## Primary tests

The strongest preregistered prediction is exact exclusivity:

- every primary-labeled Class-IV ECA reaches a nontrivial closure level chosen before labels are joined;
- no primary-labeled Class-I, II, or III ECA reaches that level.

Because it is not yet known which of Levels 1-4 is nonempty, the first outcome-independent milestone is to identify the highest level with at least one ECA witness under the frozen construction. The class test is then applied at that level without changing the representation or score.

Secondary analyses may test enrichment rather than exclusivity, but must be labeled exploratory if the strong hypothesis fails.

## Immediate falsifiers / warnings

- If all or almost all rules close, the property is architectural rather than Class-IV selective.
- If closure depends strongly on arbitrary ring permutations and only a post-hoc chosen encoding isolates Class IV, the hypothesis is unsupported.
- If only reflection-symmetric rules can enter the test, apparent class separation is confounded by representation admissibility.
- If a rule closes only because an off-manifold decoder or hidden program layer is supplied externally, it does not count.
- If closure is visible only after class-aware tuning of tolerance, scale, block size, or orientation, it does not count as preregistered evidence.

## Interpretation if the strong hypothesis succeeds

A success would not prove that Wolfram Class IV *is* dimensional closure. It would establish, in the tested finite rule space and frozen representation family, that a static property of rule-as-geometry exactly separates the independently assigned dynamical class. That would warrant fresh-size/fresh-family confirmation and a search for an analytic characterization.

## Interpretation if it fails

Failure is informative. Record whether dimensional closure tracks:

- symmetry or algebraic properties of the truth table;
- Class-II/Class-III boundary behavior;
- known localized-structure / long-transient rules;
- universality candidates;
- an entirely different partition of ECA rule space.

Do not redesign the construction to recover Class IV in the same research checkpoint.
