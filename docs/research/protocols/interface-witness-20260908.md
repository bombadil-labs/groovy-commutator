# Follow-up protocol: a finite witness of interface escape

Selected after the completed interface-state census, not preregistered with it.
The first reachable failure at t=4 has upper a_-1=1 and lower b_-2=1;
all other causal input bits are zero. Translate by two logical cells and
extend both logical rows by zeros: a_1=1, b_0=1. This defines exactly four
physical toggles of alternating B at (0,3),(1,2),(2,1),(3,0).

Track this one finite perturbation for 32 fine ticks, including every phase.
Use initial rows -64..67 and columns -64..67, shrink once per tick, and
compare the complete remaining field with an independently written scalar
coordinate update. No torus, random seeds, fitted velocity, or sample search.
At every tick compare with B XOR (t mod 2), record all changed coordinates,
mass and bounding box, and the changed coordinates on the highest and lowest
affected rows. The retained window covers the whole perturbation light cone.

Plot selected even-tick fields and the support envelope to make the exact
finite failure legible. This is a bounded witness, not evidence by itself
for indefinite propagation, a recurrent isolated object, or a minimal repair.
Any subsequent all-time claim needs a separate local argument.
