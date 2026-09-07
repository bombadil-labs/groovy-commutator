# Expanding a macro preserves its physical computation

Suppose every macro is a finite word in the primitive operations, all
primitive operations remain callable, and a macro pays the physical cost
of its expansion. Every macro program expands to a primitive program with
the same endpoint and physical cost. Every primitive program remains allowed.
Therefore adding macros leaves physical-budget reachability unchanged.

This argument does not assume a ring size or particular CA rule. Its
assumptions matter: new physical operators, changed execution costs, or
removing primitive actions would be different models.

A combined budget that also prices dispatch can change. In the
[costed experiment](../research/2026-09-07-costed-primitives.md), a four-tick
macro needs one dispatch instead of four. All execution costs coincide
across libraries when dispatch has zero price, as the argument requires.
