#!/usr/bin/env python3

"""
    params:
        m = number of clauses
        x = number of existentials
        u = number of universals
        d = number of deps
        w = existential clause width
        v = universal clause width
"""

import argparse
import random


def sample_param(p, s):
    return random.randint(int(p * (1-s)), int(p * (1+s)))

def main(args):
    u = sample_param(args.u, args.s)
    x = sample_param(args.x, args.s)
    m = sample_param(args.m, args.s)
    v = sample_param(args.v, args.s)
    w = sample_param(args.w, args.s)
    d = sample_param(args.d, args.s)

    U = range(1, u+1)
    X = range(u+1, u+x+1)
    S = {x : random.sample(U, d) for x in X}
    F = set()
    while len(F) < m:
        C = frozenset(var * pol for var, pol in zip(
            random.sample(U, v) + random.sample(X, w),
            random.choices([-1, 1], k=v+w)
            ))
        F.add(C)

    print(f"p cnf {x+u} {m}")
    print("a " + " ".join(map(str, U)) + " 0")
    for xvar in X:
        print(f"d {x} " + " ".join(map(str, S[xvar])) + " 0")
    for C in F:
        print(" ".join(map(str, C)) + " 0")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", type=int, default=50, help="number of clauses")
    parser.add_argument("-w", type=int, default=4, help="existential clause width")
    parser.add_argument("-v", type=int, default=3, help="universal clause width")
    parser.add_argument("-x", type=int, default=12, help="number of existential variables")
    parser.add_argument("-u", type=int, default=6, help="number of universal variables")
    parser.add_argument("-d", type=int, default=3, help="size of each dependency set")
    parser.add_argument("-s", type=float, default=0, help="sample other parameters from uniform distributions on [p*(1+s), p*(1-s)]")
    args = parser.parse_args()
    main(args)
