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
import sys
import itertools
from math import comb

def litstr(lits):
    return " ".join(map(str, lits))

def random_subset(S):
    return list(itertools.compress(S, random.choices([False, True], k=len(S))))

def sample_subset(S, k=None, allow_empty=True):
    """
        sample a subset of S of size k uniformly
        if k is not given, sample a subset uniformly
    """
    if k != None:
        return random.sample(S, k)
    else:
        if allow_empty:
            return random_subset(S)
        else:
            pivot = random.randrange(len(S))
            return random_subset(S[:pivot]) + [S[pivot]] + random_subset(S[pivot+1:])

def sample_clause(U, v, X, w):
    """
        sample a clause uniformly at random with
            v variables from the set U
            w variables from the set X
        if v or w not given, sample a random susbet of variables
    """
    return frozenset(random.choice([-1, 1]) * var for var in
            sample_subset(U, v) + sample_subset(X, w, allow_empty=False))

def sample_param(p, s):
    return random.randint(int(p * (1-s)), int(p * (1+s)))

def main(args):
    u = sample_param(args.u, args.s)
    x = sample_param(args.x, args.s)
    m = sample_param(args.m, args.s)
    v = sample_param(args.v, args.s) if args.v != None else None
    w = sample_param(args.w, args.s) if args.w != None else None
    d = sample_param(args.d, args.s) if args.d != None else None

    U = range(1, u+1)
    X = range(u+1, u+x+1)
    S = {x : sample_subset(U, d) for x in X}
    F = set()

    # calculate the total number  p  of possible clauses
    # if m > p raise an error

    uni_clauses = 3**u   if v is None else comb(u, v) * 2**v
    exi_clauses = 3**x-1 if w is None else comb(x, w) * 2**w
    p = uni_clauses * exi_clauses

    if m > p:
        print(f"DQBFuzz ERROR: Cannot generate {m} different clauses with these parameters", file=sys.stderr)
        sys.exit()

    if m > p // 2:
        print(f"DQBFuzz WARNING: Requesting a large proportion of all possible clauses ({m} out of {p})", file=sys.stderr)

    while len(F) < m:
        F.add(sample_clause(U, v, X, w))

    # TODO: also determine if the prefix is a QBF
    indep_xvars = []
    print(f"p cnf {x+u} {m}")
    for xvar in X:
        if len(S[xvar]) == 0:
            indep_xvars.append(xvar)
    if len(indep_xvars) > 0 and len(indep_xvars) < x:
        print("e " + litstr(indep_xvars) + " 0")
    if u > 0 and len(indep_xvars) < x:
        print("a " + litstr(U) + " 0")
    for xvar in X:
        if len(S[xvar]) > 0:
            print(f"d {xvar} " + litstr(S[xvar]) + " 0")
    for C in F:
        print(litstr(sorted(C, key=abs)) + " 0")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", type=int, default=50, help="number of clauses")
    parser.add_argument("-w", type=int, default=None, help="existential clause width")
    parser.add_argument("-v", type=int, default=None, help="universal clause width")
    parser.add_argument("-x", type=int, default=12, help="number of existential variables")
    parser.add_argument("-u", type=int, default=6, help="number of universal variables")
    parser.add_argument("-d", type=int, default=None, help="size of each dependency set")
    parser.add_argument("-s", type=float, default=0, help="sample other parameters from uniform distributions on [p*(1+s), p*(1-s)]")
    args = parser.parse_args()

    if args.x <= 0:
        print(f"DQBFuzz ERROR: x must be positive (got {args.x})", file=sys.stderr)
        sys.exit(1)

    if args.u < 0:
        print(f"DQBFuzz ERROR: u must be non-negative (got {args.u})", file=sys.stderr)
        sys.exit(1)

    if args.m < 0:
        print(f"DQBFuzz ERROR: m must be non-negative (got {args.m})", file=sys.stderr)
        sys.exit(1)

    if args.v:
        if args.v > args.u:
            print(f"DQBFuzz ERROR: v must be no greater than u (got v={args.v}>{args.u}=u)", file=sys.stderr)
            sys.exit(1)
        if args.v < 0:
            print(f"DQBFuzz ERROR: v must be non-negative (got {args.v})", file=sys.stderr)
            sys.exit(1)

    if args.w:
        if args.w > args.x:
            print(f"DQBFuzz ERROR: w must be no greater than x (got w={args.w}>{args.x}=x)", file=sys.stderr)
            sys.exit(1)
        if args.w <= 0:
            print(f"DQBFuzz ERROR: w must be positive (got {args.w})", file=sys.stderr)
            sys.exit(1)

    if args.d:
        if args.d > args.u:
            print(f"DQBFuzz ERROR: d must be no greater than u (got d={args.d}>{args.u}=u)", file=sys.stderr)
            sys.exit(1)
        if args.d < 0:
            print(f"DQBFuzz ERROR: d must be non-negative (got {args.d})", file=sys.stderr)
            sys.exit(1)

    main(args)
