"""
Computation 6: Verify E[p^dim] = p+1 from Poonen-Rains random matrix model.

Model: Sel_p(E) ~ ker(A) where A is a random alternating matrix over F_p.

More precisely (Poonen-Rains):
Take V = F_p^{2n} with the standard symplectic form.
Let U, W be two random maximal isotropic subspaces (each of dimension n).
Then dim(U ∩ W) has a specific distribution.

E[p^{dim(U ∩ W)}] should equal p+1 as n -> infinity.

We verify this computationally.
"""

print("="*70)
print("COMPUTATION 6: POONEN-RAINS RANDOM MATRIX MODEL VERIFICATION")
print("="*70)

# Method 1: Random alternating matrices
# If A is a random 2n x 2n alternating matrix over F_p,
# then E[|ker(A)|] = p + 1 (conjectured/proved by Poonen-Rains)

def random_alt_matrix(n, p):
    """Generate a random 2n x 2n alternating matrix over F_p."""
    F = GF(p)
    M = matrix(F, 2*n, 2*n)
    for i in range(2*n):
        for j in range(i+1, 2*n):
            M[i,j] = F.random_element()
            M[j,i] = -M[i,j]
    return M

def test_alternating_kernel(p, n, num_trials=10000):
    """Average |ker(A)| for random alternating matrices A over F_p."""
    total = 0
    for _ in range(num_trials):
        A = random_alt_matrix(n, p)
        k = A.kernel().dimension()
        total += p^k
    return RR(total) / num_trials

# Test for small p and n
print("\nMethod 1: Random alternating matrices")
print(f"{'p':>4} | {'n':>4} | {'E[p^dim(ker)]':>14} | {'p+1':>6} | {'ratio':>8} | {'trials':>6}")
print("-"*60)

for p in [2, 3, 5, 7]:
    for n in [2, 4, 6, 8]:
        avg = test_alternating_kernel(p, n, num_trials=5000)
        pred = p + 1
        ratio = avg / pred
        print(f"{p:>4} | {n:>4} | {avg:>14.6f} | {pred:>6} | {ratio:>8.4f} | {5000:>6}")

# Method 2: Random isotropic subspace intersection
# Take F_p^{2n} with symplectic form J = [[0, I_n], [-I_n, 0]]
# Pick random maximal isotropic U (dimension n)
# Fix W = F_p^n x {0} (the standard maximal isotropic)
# Compute dim(U ∩ W)

def random_isotropic_intersection(p, n, num_trials=10000):
    """Average p^dim(U ∩ W) for random maximal isotropic U in F_p^{2n}."""
    F = GF(p)
    # Standard maximal isotropic: W = span of e_1, ..., e_n
    # Random maximal isotropic U = {(x, Sx) : x in F_p^n} for random symmetric S
    # (This parametrizes a dense open subset of the Lagrangian Grassmannian)

    total = 0
    for _ in range(num_trials):
        # Random symmetric n x n matrix S
        S = matrix(F, n, n)
        for i in range(n):
            for j in range(i, n):
                S[i,j] = F.random_element()
                S[j,i] = S[i,j]

        # U = {(x, Sx) : x in F_p^n}
        # W = {(x, 0) : x in F_p^n}
        # U ∩ W = {(x, 0) : Sx = 0} = ker(S) x {0}
        k = S.kernel().dimension()
        total += p^k
    return RR(total) / num_trials

print("\nMethod 2: Isotropic subspace intersections (symmetric matrix kernel)")
print(f"{'p':>4} | {'n':>4} | {'E[p^dim(ker S)]':>16} | {'p+1':>6} | {'ratio':>8}")
print("-"*55)

for p in [2, 3, 5, 7, 11]:
    for n in [3, 5, 8, 12]:
        avg = random_isotropic_intersection(p, n, num_trials=5000)
        pred = p + 1
        ratio = avg / pred
        print(f"{p:>4} | {n:>4} | {avg:>16.6f} | {pred:>6} | {ratio:>8.4f}")

# Method 3: Exact computation of the distribution for small n
print("\n\nMethod 3: Exact computation for small n and p")
print("="*50)

for p in [2, 3, 5, 7]:
    F = GF(p)
    for n in [2, 3, 4]:
        # Enumerate all symmetric n x n matrices over F_p
        total_size = 0
        total_count = 0
        dim_counts = {}

        # This is p^(n(n+1)/2) matrices total
        num_entries = n * (n + 1) // 2
        num_matrices = p^num_entries

        if num_matrices > 100000:
            print(f"  p={p}, n={n}: too many matrices ({num_matrices}), skipping exact")
            continue

        # Generate all symmetric matrices
        from itertools import product as iterproduct
        entries = list(F)

        # Generate upper triangle indices
        upper_triangle = [(i, j) for i in range(n) for j in range(i, n)]

        for vals in iterproduct(entries, repeat=len(upper_triangle)):
            S = matrix(F, n, n)
            for idx, (i, j) in enumerate(upper_triangle):
                S[i, j] = vals[idx]
                S[j, i] = vals[idx]

            k = S.kernel().dimension()
            total_size += p^k
            total_count += 1
            dim_counts[k] = dim_counts.get(k, 0) + 1

        avg = RR(total_size) / total_count
        pred = p + 1
        print(f"\n  p={p}, n={n}: EXACT E[p^dim(ker S)] = {avg:.6f}, p+1 = {pred}")
        print(f"    dim(ker) distribution: {dict(sorted(dim_counts.items()))}")
        print(f"    Total matrices: {total_count}")
        print(f"    Ratio to prediction: {avg/pred:.6f}")

# Key theoretical result:
print("""
THEORETICAL RESULT:
The Poonen-Rains paper proves that for a random alternating matrix A
over Z_p (p-adic integers), the expected value of |coker(A)| equals p+1.

More precisely: if A is a random alternating 2n x 2n matrix over Z_p
(entries chosen uniformly from Z_p), then as n -> infinity:
    E[|coker(A)_tors|] -> p + 1

where coker(A)_tors is the torsion part of the cokernel.

The analogous result for SYMMETRIC matrices over F_p (our Method 2) is:
    E[p^{dim ker(S)}] -> p + 1 as n -> infinity

for a random symmetric n x n matrix S over F_p.

This is equivalent to the statement: a random element of the
Lagrangian Grassmannian has expected |intersection with a fixed
Lagrangian| equal to p+1.

The connection to Selmer groups:
    Sel_p(E) = (global isotropic) ∩ (product of local isotropics)
    dim Sel_p(E) = dim of this intersection

The Poonen-Rains model: treat the global isotropic as random.
Then E[p^{dim Sel_p}] = p + 1 follows from the random matrix result.

The BF theory connection:
    The BF partition function Z_BF = |Sel_p| = p^{dim Sel_p}
    The BF measure on gauge configurations is related to the uniform
    measure on the Lagrangian Grassmannian
    AVERAGING Z_BF over "random" E is equivalent to computing
    E[p^{dim(random isotropic intersection)}] = p + 1
""")
