#!/usr/bin/env python3
"""Independent scalar audit of Fable's Rule-54 period-four golden generator.

Bit 0 is the first (leftmost) site. No reuse of the compiled census or
vectorized commutator code. Also corrects an unverified handwritten value
for G(HX): its *even* sublattice is zero, not one.
"""
from __future__ import annotations

import sympy as sp

RULE = 54


def H(row):
    n = len(row)
    return tuple(
        (RULE >> (4 * row[(i-1) % n] + 2 * row[i] + row[(i+1) % n])) & 1
        for i in range(n)
    )


def xor(a, b):
    return tuple(x ^ y for x, y in zip(a, b))


def G(x):
    y = H(x)
    return xor(xor(y, H(y)), H(xor(x, y)))


def allowed(a):
    n = len(a)
    return all(not (a[i] == a[(i+1) % n] == a[(i+2) % n]) for i in range(n))


def word(row, start, length=13):
    return sum(row[(start+i) % len(row)] << i for i in range(length))


def main():
    macro = sp.zeros(4)
    for ab in range(4):
        a, b = (ab >> 1) & 1, ab & 1
        for c in (0, 1):
            if not (a == b == c):
                macro[ab, 2*b+c] = 1
    z = sp.Symbol("z")
    assert sp.factor(macro.charpoly(z).as_expr()) == (
        (z*z-z-1)*(z*z+z+1)
    )

    plus, minus = set(), set()
    checked = 0
    for source in range(1 << 14):
        a = tuple((source >> i) & 1 for i in range(14))
        if not allowed(a):
            continue
        x = tuple(bit for v in a for bit in (v, 0))
        h1 = H(x)
        h2 = H(h1)
        h3 = H(h2)
        assert H(h3) == x
        assert h2 == tuple(bit for v in a for bit in (1-v, 0))
        assert all(bit == 0 for bit in G(x))
        assert G(h1) == tuple(bit for i in range(len(a))
                             for bit in (0, a[i] ^ a[(i+1) % len(a)]))
        assert G(h2) == G(x) and G(h3) == G(h1)
        checked += 1
        for i in range(len(x)):
            plus.add((word(x,i), word(h2,i)))
            minus.add((word(h1,i), word(h3,i)))

    assert checked == 842
    assert (len(plus), len(minus)) == (68,110)
    print("PASS: 842 cyclic 14-block words; H^4X=X and sparse complement identity")
    print("PASS: G(X)=0; G(HX) even=0 and odd=a_i XOR a_{i+1}")
    print("PASS: exact 68/110 generated local source-pair edges")
    print("PASS: golden-mean adjacency characteristic polynomial")


if __name__ == "__main__":
    main()
