"""
Stage 1.1-1.2: Compute staggered signs for all plaquettes on (Z/2Z)^4, d=4.
Classify the effective coefficient patterns.

Lattice: (Z/2Z)^4, so coordinates are in {0,1}^4.
Directions: mu=0,1,2,3.
Edges: (x, mu) for x in {0,1}^4, mu in {0,1,2,3}. Total = 16*4 = 64 edges.
Plaquettes: For each x in {0,1}^4 and each pair (mu, nu) with mu < nu,
  one plaquette. Total = 16 * C(4,2) = 16*6 = 96 plaquettes.

For plaquette at (x, mu, nu):
  e1 = (x, mu)
  e2 = (x + mu_hat, nu)
  e3 = (x + nu_hat, mu)
  e4 = (x, nu)

B_sq formula:
  B_sq(Q, v) = v_{e1} + Ad_{Q_{e1}}(v_{e2}) - Ad_{Q_{e1}Q_{e2}Q_{e3}^{-1}}(v_{e3}) - Ad_{U_sq}(v_{e4})

For staggered mode: v_{x,mu} = (-1)^{|x| + mu} * n, where |x| = sum of coordinates.

So the staggered coefficient for edge (x, mu) is s(x, mu) = (-1)^{|x| + mu}.

Effective coefficients in B_sq for staggered mode:
  c1 = s(x, mu)       = (-1)^{|x| + mu}
  c2 = s(x+mu_hat, nu) = (-1)^{|x+mu_hat| + nu} = (-1)^{|x| + 1 + nu}
  c3 = -s(x+nu_hat, mu) = -(-1)^{|x+nu_hat| + mu} = -(-1)^{|x| + 1 + mu}
  c4 = -s(x, nu)       = -(-1)^{|x| + nu}

Note: |x + mu_hat| = |x| + 1 (mod 2) since adding mu_hat flips one coordinate.
Wait: |x + mu_hat| = sum of coords of (x + mu_hat mod 2). If x_mu = 0, then
(x+mu_hat)_mu = 1, so |x+mu_hat| = |x| + 1. If x_mu = 1, then (x+mu_hat)_mu = 0,
so |x+mu_hat| = |x| - 1. In both cases, |x+mu_hat| = |x| +/- 1, so
(-1)^{|x+mu_hat|} = -(-1)^{|x|}.

Similarly for nu_hat.

So:
  c1 = (-1)^{|x| + mu}
  c2 = (-1)^{|x| + 1 + nu}  = -(-1)^{|x| + nu}
  c3 = -(-1)^{|x| + 1 + mu} = (-1)^{|x| + mu}
  c4 = -(-1)^{|x| + nu}

So c3 = c1 and c4 = c2!

Let a = (-1)^{|x| + mu}, b = -(-1)^{|x| + nu} = (-1)^{|x| + nu + 1}.

Then the effective coefficients are (c1, c2, c3, c4) = (a, b, a, b).

B_sq(Q, v_stag) = a*n + b*Ad(Q_{e1})(n) - a*Ad(Q_{e1}Q_{e2}Q_{e3}^{-1})(n) - b*Ad(U_sq)(n)
                = a*[n - Ad(Q_{e1}Q_{e2}Q_{e3}^{-1})(n)] + b*[Ad(Q_{e1})(n) - Ad(U_sq)(n)]

Wait, let me be more careful. The B_sq formula has:
  B_sq = v_{e1} + Ad(Q_{e1})(v_{e2}) - Ad(Q_{e1}Q_{e2}Q_{e3}^{-1})(v_{e3}) - Ad(U_sq)(v_{e4})

With staggered mode:
  v_{e1} = s(x,mu) * n = c1 * n
  v_{e2} = s(x+mu_hat, nu) * n
  v_{e3} = s(x+nu_hat, mu) * n
  v_{e4} = s(x, nu) * n

So:
  B_sq = c1*n + s(x+mu_hat,nu)*Ad(Q_{e1})(n) - s(x+nu_hat,mu)*Ad(P23)(n) - s(x,nu)*Ad(U_sq)(n)

where P23 = Q_{e1}Q_{e2}Q_{e3}^{-1}.

The EFFECTIVE coefficients (including the minus signs from B_sq formula) are:
  eff_1 = s(x, mu)         = (-1)^{|x|+mu}
  eff_2 = s(x+mu_hat, nu)  = (-1)^{|x|+1+nu}
  eff_3 = -s(x+nu_hat, mu) = -(-1)^{|x|+1+mu} = (-1)^{|x|+mu}
  eff_4 = -s(x, nu)        = -(-1)^{|x|+nu}

So eff_1 = eff_3, and eff_2 = eff_4.

Let me verify: eff_2 = (-1)^{|x|+1+nu} and eff_4 = -(-1)^{|x|+nu} = (-1)^{|x|+nu+1}.
Yes, eff_2 = eff_4.

So B_sq = a*(n + Ad(P23)^{-1} ... wait let me redo this.

Actually, B_sq = eff_1*n + eff_2*Ad(R1)(n) + eff_3*Ad(R2)(n) + eff_4*Ad(R3)(n)
where:
  R0 = Id (no rotation on first edge)
  R1 = Ad(Q_{e1})
  R2 = Ad(Q_{e1}Q_{e2}Q_{e3}^{-1})   (this gets multiplied by -s(x+nu_hat,mu), i.e., eff_3)
  R3 = Ad(U_sq)                        (this gets multiplied by -s(x,nu), i.e., eff_4)

Let me just enumerate everything explicitly.
"""

import numpy as np
from itertools import product

# Lattice setup: (Z/2Z)^4
L = 2
d = 4
coords = list(product(range(L), repeat=d))  # 16 vertices

def parity(x):
    """Sum of coordinates mod 2"""
    return sum(x) % 2

def add_mod(x, mu):
    """x + e_mu mod L"""
    y = list(x)
    y[mu] = (y[mu] + 1) % L
    return tuple(y)

def staggered_sign(x, mu):
    """(-1)^{|x| + mu}"""
    return (-1) ** (sum(x) + mu)

# Enumerate all plaquettes and compute effective signs
plaquettes = []
for x in coords:
    for mu in range(d):
        for nu in range(mu+1, d):
            # Plaquette edges
            e1 = (x, mu)
            x_plus_mu = add_mod(x, mu)
            e2 = (x_plus_mu, nu)
            x_plus_nu = add_mod(x, nu)
            e3 = (x_plus_nu, mu)
            e4 = (x, nu)

            # Staggered signs for each edge variable
            s1 = staggered_sign(x, mu)
            s2 = staggered_sign(x_plus_mu, nu)
            s3 = staggered_sign(x_plus_nu, mu)
            s4 = staggered_sign(x, nu)

            # Effective coefficients in B_sq
            # B_sq = v_{e1} + Ad(Q_{e1})(v_{e2}) - Ad(P23)(v_{e3}) - Ad(U_sq)(v_{e4})
            # v_{ei} = s_i * n
            # So effective = (s1, s2, -s3, -s4)
            eff = (s1, s2, -s3, -s4)

            # Active orientation: mu + nu odd
            active = (mu + nu) % 2 == 1

            plaquettes.append({
                'x': x, 'mu': mu, 'nu': nu,
                'edges': (e1, e2, e3, e4),
                'stag_signs': (s1, s2, s3, s4),
                'eff_coeffs': eff,
                'active': active,
                'parity_x': parity(x),
                'mu_plus_nu_mod2': (mu + nu) % 2
            })

print(f"Total plaquettes: {len(plaquettes)}")

# Classify effective coefficient patterns
from collections import Counter
pattern_counter = Counter()
active_pattern_counter = Counter()
inactive_pattern_counter = Counter()

for p in plaquettes:
    pat = p['eff_coeffs']
    pattern_counter[pat] += 1
    if p['active']:
        active_pattern_counter[pat] += 1
    else:
        inactive_pattern_counter[pat] += 1

print("\n=== Effective Coefficient Patterns ===")
print(f"Distinct patterns: {len(pattern_counter)}")
for pat, count in sorted(pattern_counter.items()):
    print(f"  {pat}: {count} plaquettes")

print(f"\n=== Active Plaquettes (mu+nu odd) ===")
print(f"Total active: {sum(active_pattern_counter.values())}")
for pat, count in sorted(active_pattern_counter.items()):
    print(f"  {pat}: {count} plaquettes")

print(f"\n=== Inactive Plaquettes (mu+nu even) ===")
print(f"Total inactive: {sum(inactive_pattern_counter.values())}")
for pat, count in sorted(inactive_pattern_counter.items()):
    print(f"  {pat}: {count} plaquettes")

# Verify the algebraic prediction: eff_1 = eff_3, eff_2 = eff_4
print("\n=== Verification: eff_1 == eff_3 and eff_2 == eff_4? ===")
all_match = True
for p in plaquettes:
    c1, c2, c3, c4 = p['eff_coeffs']
    if c1 != c3 or c2 != c4:
        all_match = False
        print(f"  MISMATCH at {p['x']}, ({p['mu']},{p['nu']}): {p['eff_coeffs']}")
if all_match:
    print("  YES: eff_1 = eff_3 and eff_2 = eff_4 for ALL plaquettes")

# For each pattern, what are a = eff_1, b = eff_2?
print("\n=== Simplified: B_sq = a*(n - R2*n) + b*(R1*n - R3*n) ===")
print("where R1 = Ad(Q_{e1}), R2 = Ad(Q_{e1}Q_{e2}Q_{e3}^{-1}), R3 = Ad(U_sq)")
for pat, count in sorted(pattern_counter.items()):
    a, b = pat[0], pat[1]
    print(f"  (a,b) = ({a:+d},{b:+d}): {count} plaquettes")

# B_sq at Q=I (all R_k = Id):
# B_sq = a*(n - n) + b*(n - n) = 0 for ALL plaquettes.
# So |B_sq|^2 = 0 at Q=I for staggered mode? That can't be right.
# Let me recheck: at Q=I, all Ad = Id.
# B_sq(I, v_stag) = s1*n + s2*n - s3*n - s4*n = (s1 + s2 - s3 - s4)*n
print("\n=== B_sq at Q=I for each plaquette ===")
for p in plaquettes[:20]:  # first 20
    c1, c2, c3, c4 = p['eff_coeffs']
    coeff_sum = c1 + c2 + c3 + c4  # Since these already include the -signs
    # Wait: eff_coeffs = (s1, s2, -s3, -s4)
    # B_sq(I) = s1*n + s2*n + (-s3)*n + (-s4)*n = (s1+s2-s3-s4)*n = (eff1+eff2+eff3+eff4)*n
    total = c1 + c2 + c3 + c4
    print(f"  x={p['x']}, (mu,nu)=({p['mu']},{p['nu']}), eff={p['eff_coeffs']}, sum={total}")

# Let's compute B_sq(I) properly for all:
print("\n=== Sum of |B_sq(I, v_stag)|^2 over all plaquettes ===")
total_bsq_I = 0
pattern_bsq = {}
for p in plaquettes:
    c1, c2, c3, c4 = p['eff_coeffs']
    coeff = c1 + c2 + c3 + c4
    bsq_I = coeff**2  # |coeff*n|^2 = coeff^2 * |n|^2
    total_bsq_I += bsq_I
    pat = p['eff_coeffs']
    if pat not in pattern_bsq:
        pattern_bsq[pat] = {'coeff_sum': coeff, 'bsq_coeff': coeff**2, 'count': 0}
    pattern_bsq[pat]['count'] += 1

print(f"Sum |B_sq(I)|^2 = {total_bsq_I} * |n|^2")
print(f"Expected: 4d * |v|^2 = 16 * (16*|n|^2) = 256 * |n|^2")
print(f"  [since |v|^2 = 16 sites * |n|^2 for staggered mode on (Z/2Z)^4 with 4 edge directions...]")

# Actually |v|^2 = sum over all edges |v_{x,mu}|^2 = 64 * |n|^2 (64 edges, each |n|^2)
print(f"  |v|^2 = 64 * |n|^2 (64 edges)")
print(f"  4d * |v|^2 = 16 * 64 = {16*64} * |n|^2")
print(f"  Ratio: {total_bsq_I} / {16*64} = {total_bsq_I / (16*64)}")

# Something's off. Let me reconsider.
# The staggered mode: which edges?
# v = (v_{x,mu}) for all edges (x, mu).
# v_{x,mu} = (-1)^{|x|+mu} * n
# |v|^2 = sum_{x,mu} |v_{x,mu}|^2 = sum_{x,mu} |n|^2 = 64 * |n|^2
# Sum_sq |B_sq(I,v)|^2 should = sum of eigenvalues of M(I) dotted with v...
# Actually at Q=I, M(I) has eigenvalue 4d=16 on the staggered subspace.
# So v^T M(I) v = 16 * |v|^2 = 16 * 64 * |n|^2 = 1024 * |n|^2
# And Sum_sq |B_sq(I,v)|^2 = v^T M(I) v = 1024 * |n|^2
# But we computed Sum_sq (c1+c2+c3+c4)^2 = total_bsq_I.
# Let me check...

print("\n=== Detailed check ===")
for pat, info in sorted(pattern_bsq.items()):
    print(f"  Pattern {pat}: coeff_sum = {info['coeff_sum']}, "
          f"|B_sq(I)|^2 = {info['bsq_coeff']}*|n|^2, count = {info['count']}")
