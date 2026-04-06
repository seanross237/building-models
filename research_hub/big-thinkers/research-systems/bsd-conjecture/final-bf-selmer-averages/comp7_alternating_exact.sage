"""
Computation 7: The ALTERNATING matrix model gives E[p^dim] = p+1 exactly.

The key formula (Poonen-Rains):
For a random alternating 2n x 2n matrix over F_p,
    Pr[dim ker = 2k] = C(n,k,p) * product formula

where the probabilities depend on the Gaussian binomial coefficients.

Let's verify:
1. E[p^dim(ker A)] = p+1 for alternating matrices over F_p
2. E[p^dim(ker S)] = 2 for symmetric matrices over F_p (different!)
3. The alternating structure is essential

This explains WHY the BF theory (which encodes the alternating Cassels-Tate
pairing) gives the correct Selmer average, while a naive approach without
the alternating structure would give the wrong answer.
"""

print("="*70)
print("COMPUTATION 7: ALTERNATING vs SYMMETRIC - THE CRITICAL DISTINCTION")
print("="*70)

# Exact computation for alternating matrices
def random_alt_matrix_Fp(n, p):
    """Random alternating 2n x 2n matrix over F_p."""
    F = GF(p)
    M = matrix(F, 2*n, 2*n)
    for i in range(2*n):
        for j in range(i+1, 2*n):
            M[i,j] = F.random_element()
            M[j,i] = -M[i,j]
    return M

# More trials for higher precision
print("\nAlternating matrices: E[p^{dim ker}]")
print(f"{'p':>4} | {'n':>4} | {'E[p^dim(ker)]':>14} | {'p+1':>6} | {'error':>10} | {'trials':>6}")
print("-"*65)

for p in [2, 3, 5, 7, 11, 13]:
    for n in [4, 8, 12]:
        trials = 10000 if n <= 8 else 5000
        total = 0
        for _ in range(trials):
            A = random_alt_matrix_Fp(n, p)
            k = A.kernel().dimension()
            total += p^k
        avg = RR(total) / trials
        error = abs(avg - (p + 1))
        print(f"{p:>4} | {n:>4} | {avg:>14.6f} | {p+1:>6} | {error:>10.6f} | {trials:>6}")

# Now verify: for SYMMETRIC matrices, the average is 2
print("\nSymmetric matrices: E[p^{dim ker}]")
print(f"{'p':>4} | {'n':>4} | {'E[p^dim(ker)]':>14} | {'predicted':>10} | {'error':>10}")
print("-"*60)

for p in [2, 3, 5, 7, 11]:
    F = GF(p)
    for n in [4, 8, 12]:
        trials = 10000 if n <= 8 else 5000
        total = 0
        for _ in range(trials):
            S = matrix(F, n, n)
            for i in range(n):
                for j in range(i, n):
                    S[i,j] = F.random_element()
                    S[j,i] = S[i,j]
            k = S.kernel().dimension()
            total += p^k
        avg = RR(total) / trials
        error = abs(avg - 2)
        print(f"{p:>4} | {n:>4} | {avg:>14.6f} | {'2':>10} | {error:>10.6f}")

# Exact computation for p=2, small n
print("\n\nExact results for p=2:")
print("="*50)

F = GF(2)

for size in [4, 6, 8]:
    # Enumerate all alternating size x size matrices
    # Alternating: M^T = -M and diagonal = 0
    # Over F_2: -1 = 1, so M^T = M with 0 diagonal = symmetric with 0 diagonal
    num_entries = size * (size - 1) // 2
    total_k_pow = 0
    count = 0
    dim_counts = {}

    if 2^num_entries > 200000:
        print(f"\n  Alternating {size}x{size} over F_2: too many ({2^num_entries}), using random sample")
        trials = 50000
        for _ in range(trials):
            M = matrix(F, size, size)
            for i in range(size):
                for j in range(i+1, size):
                    M[i,j] = F.random_element()
                    M[j,i] = M[i,j]  # Over F_2, -1 = 1
            k = M.kernel().dimension()
            total_k_pow += 2^k
            count += 1
            dim_counts[k] = dim_counts.get(k, 0) + 1
        avg = RR(total_k_pow) / count
        print(f"  Average (random, {trials} trials): {avg:.6f}, p+1 = 3")
    else:
        from itertools import product as iterproduct
        entries = list(F)
        upper_pairs = [(i, j) for i in range(size) for j in range(i+1, size)]

        for vals in iterproduct(entries, repeat=len(upper_pairs)):
            M = matrix(F, size, size)
            for idx, (i, j) in enumerate(upper_pairs):
                M[i, j] = vals[idx]
                M[j, i] = vals[idx]
            k = M.kernel().dimension()
            total_k_pow += 2^k
            count += 1
            dim_counts[k] = dim_counts.get(k, 0) + 1

        avg = RR(total_k_pow) / count
        print(f"\n  Alternating {size}x{size} over F_2:")
        print(f"    EXACT E[2^dim(ker)] = {avg:.6f}, target = 3")
        print(f"    dim distribution: {dict(sorted(dim_counts.items()))}")
        print(f"    Total matrices: {count}")

# The formula for E[p^dim(ker A)] for alternating matrices
print("\n\nTheoretical formula:")
print("="*50)
print("""
For alternating 2n x 2n matrices over F_p:

Pr[dim ker = 0] = prod_{i=1}^{n} (1 - p^{-(2i-1)})
Pr[dim ker = 2] = [Gaussian binomial (n choose 1)_p] * specific factor
...

The key identity (proved by Poonen-Rains):
    sum_{k=0}^{n} p^{2k} * Pr[dim ker = 2k] = p + 1

Note: the kernel of an alternating matrix always has EVEN dimension.
This is because the alternating form has even rank.

For the BF theory:
    The BF partition function Z_BF involves an alternating pairing
    (the Cassels-Tate pairing), and the Selmer group is the kernel
    of this alternating form.

    The ALTERNATING nature of the Cassels-Tate pairing is what ensures
    E[|Sel_p|] = p + 1 rather than E[|Sel_p|] = 2.

    In other words: the BF theory's use of an ALTERNATING action
    (B-field paired with A-field) encodes the correct random matrix
    model, and this is what gives the right Selmer average.
""")
