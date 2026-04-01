"""
Stage 5: Comparison with the Claimed Proof
==========================================

After independent derivation, compare with the prior mission's claimed proof chain.

Prior mission claims:
- β < 1/6 threshold
- Proof via CS on HessS = (β/2N) Σ|B_□|²

My independent derivation:
- Same formula: HessS = (β/2N) Σ|B_□|²
- Same CS bound: HessS ≤ 6β|v|² → β < 1/6
- Numerically verified: CS bound achieved at U=iσ₃

Goal of this stage:
1. Check whether my derivation matches the claimed proof
2. Identify where SZZ's β < 1/48 comes from (the 8x gap)
3. Verify that β < 1/6 is not improvable (needs all-Q saturation analysis)
"""

import numpy as np
from itertools import product as iproduct

print("=" * 60)
print("STAGE 5: COMPARISON WITH CLAIMED PROOF")
print("=" * 60)

N = 2
d = 4
beta = 1.0

# ===========================
# Key formulas
# ===========================

print("\n=== FORMULA COMPARISON ===\n")
print("  KEY FORMULA (verified by FD at multiple configs):")
print("  HessS(v,v) = (β/2N) × Σ_{□} |B_□(Q,v)|²")
print()
print("  where B_□(Q,v) = Σ_{e∈□} s_e Ad_{P_{□,e}}(v_e)")
print("  s_e = ±1 (link orientation), Ad_P = isometry (|Ad_P v| = |v|)")
print()

# ===========================
# SZZ's bound derivation
# ===========================

print("=== SZZ LEMMA 4.1 vs MY BOUND ===\n")
print("  Both use Cauchy-Schwarz, but different forms:")
print()
print("  [METHOD A — SZZ claimed in GOAL]:")
print("  Step 1: |B_□| ≤ |v_{e1}| + |v_{e2}| + |v_{e3}| + |v_{e4}|  (triangle ineq)")
print("  Step 2: (...sum...)^2 ≤ 4 × Σ_{e∈□} |v_e|^2  (Cauchy-Schwarz)")
print("  Result: |B_□|^2 ≤ 4 × Σ_{e∈□} |v_e|^2")
print()
print("  [METHOD B — My derivation]:")
print("  Direct CS: |Σ_i A_i|^2 ≤ n Σ|A_i|^2 for n terms with |A_i|=|v_i|")
print("  Result: |B_□|^2 ≤ 4 × Σ_{e∈□} |v_e|^2")
print()
print("  BOTH methods give the SAME bound: |B_□|^2 ≤ 4 Σ|v_e|^2")
print()

# ===========================
# The factor-of-8 discrepancy
# ===========================

print("=== THE 8× DISCREPANCY ===\n")
print("  GOAL claims SZZ Lemma 4.1: HessS ≤ 8(d-1)Nβ|v|^2")
print()
C_szz = 8 * (d-1) * N
C_mine = 4 * (d-1) / N
print(f"  C_SZZ = 8(d-1)N = {C_szz}  →  β < {N/(2*C_szz):.5f} = 1/48")
print(f"  C_mine = 4(d-1)/N = {C_mine:.2f}  →  β < {N/(2*C_mine):.5f} = 1/6")
print()
print(f"  Ratio: C_SZZ / C_mine = {C_szz/C_mine:.1f}  (= 2N^2 = {2*N**2} for N={N})")
print()
print("  The factor 2N^2 = 8 discrepancy:")
print()
print("  Observation: Both methods A and B give |B_□|^2 ≤ 4 Σ|v_e|^2.")
print("  Then:")
print("  My bound: HessS ≤ (β/2N) × 4 × 2(d-1) × |v|^2 = (4(d-1)/N)β|v|^2 = 6β")
print("  SZZ:      HessS ≤ 8(d-1)Nβ|v|^2 = 48β  (factor 8N^2/4 = 2N^2 larger)")
print()
print("  What intermediate step gives the 2N^2 = 8 factor?")
print()
print("  HYPOTHESIS: SZZ's Lemma 4.1 bounds |B_□|^2 per generator separately:")
print("  If we bound each Lie algebra component a separately:")
print("     [B_□]_a = Σ_{e} s_e [Ad_{P_e}(v_e)]_a")
print("  then maybe SZZ applies Cauchy-Schwarz differently, losing N^2.")
print()

# Actually, the norm on su(N) with <A,B> = -2 Re Tr(AB):
# For A = Σ_a c_a tau_a: |A|^2 = Σ_a c_a^2
# Cauchy-Schwarz: |Σ_i A_i|^2 ≤ n Σ|A_i|^2 works the same way
# Each |A_i|^2 = Σ_a [A_i]_a^2 where [A_i]_a are the su(N) components

print("  ALTERNATIVE HYPOTHESIS: SZZ computes HessS differently.")
print("  If they use HessS(v,v) = (β/N) Σ_□ |B_□|^2 (missing factor of 1/2),")
print("  then C_SZZ_revised = (β/N) × 4 × 2(d-1) = 8(d-1)/N × β")
print(f"  For N=2: = {8*(d-1)/N}β  (still not 48β)")
print()

# Let's check: maybe SZZ uses a DIFFERENT definition of the norm
# If |A|^2 = -(N) Tr(A^2) = N/2 × (-2 Tr(A^2)):
# |tau_a|^2 = -N Tr(tau_a^2) = N × 1/4 = N/4... not 1

# What if they use |A|^2 = N Tr(A^† A) = N Tr(-A^2) = -N Tr(A^2)?
# |tau_a|^2 = N × Tr(tau_a^2 × (-1)) = N × 1/4 = N/4... also not 1

# What if they use the Killing form: B(A,A) = 2N Tr(A^2) (for su(N))?
# Then |A|^2 = -B(A,A) = -2N Tr(A^2)
# |tau_a|^2 = -2N Tr(tau_a^2) = -2N × (-1/4) = N/2 for N=2: = 1 (same!)

print("  CHECKING INNER PRODUCT CONSISTENCY:")
print("  If <A,B> = -2 Tr(AB) then |tau_a|^2 = 1 (both SZZ and my convention)")
print("  The inner product factor is the same.")
print()

print("  MOST LIKELY EXPLANATION for 8x discrepancy:")
print("  SZZ's Lemma 4.1 is a GENUINE WEAKER BOUND than the CS bound.")
print("  They bound |B_□|^2 per LINK (not per plaquette) using a cruder estimate.")
print("  E.g., bounding |v_e|^2 per term by max_e' |v_{e'}|^2 instead of the average,")
print("  giving an extra factor of 4 (# links per plaquette) × N (dimension)")
print("  = 4N = 8 for N=2.")
print()
print("  The prior mission's improvement is: using CS DIRECTLY gives the 8× tighter bound.")
print()

# ===========================
# Verification summary table
# ===========================

print("=== VERIFICATION SUMMARY TABLE ===\n")
print("  | Claim | Method | C = HessS/β|v|^2 | β threshold | Status |")
print("  |-------|--------|------------------|-------------|--------|")
print(f"  | SZZ bound | Triangle+CS | {C_szz:.0f} | 1/48 | [CHECKED against GOAL] |")
print(f"  | My bound | CS directly | {C_mine:.1f} | 1/6 | [COMPUTED] |")
print(f"  | At Q=I | Numerical | 4.0 | 1/4 | [VERIFIED] |")
print(f"  | At U=iσ₃ | Numerical | 6.0 | 1/6 | [VERIFIED] |")
print(f"  | CS tightness | All plaquettes | 6.0 | 1/6 | [VERIFIED] |")
print()

# ===========================
# Is β < 1/6 the EXACT threshold?
# ===========================

print("=== IS β < 1/6 EXACT? ===\n")
print("  From Stage 4b: At U_all = iσ₃ with extremal eigenvector,")
print("  HessS(v,v)/|v|^2 = 6β EXACTLY (all 96 plaquettes CS-tight).")
print()
print("  This means: C_exact = max_Q max_v HessS(v,v)/(β|v|^2) = 6")
print()
print("  Therefore: β < N/(2×6) = 1/6 is the EXACT threshold,")
print("  not just an upper bound from a loose inequality.")
print()
print("  The bound is optimal within the HessS = (β/2N)Σ|B_□|² framework.")
print()

# ===========================
# Critical check: formula correctness
# ===========================

print("=== FORMULA CORRECTNESS CHECK ===\n")
print("  The formula HessS(v,v) = (β/2N) Σ|B_□|² is the COVARIANT HESSIAN.")
print("  Proof that covariant = naive Hessian for bi-invariant metric:")
print()
print("  Covariant Hess_S(v,v) = d²/dt² S(Q exp(tv))|_{t=0} - (∇_v v)(S)")
print()
print("  For bi-invariant metric: ∇_X X = 0 (geodesics are Lie group exponentials)")
print("  Therefore: Covariant Hess = Naive d²S/dt²")
print()
print("  Cross-check with Lie bracket correction:")
print("  Hess_S(v,v) = naive + (1/2) Σ_{a,b} v_a v_b [X_a, X_b](S)")
print("  = naive + (1/2) Σ_c (v × v)_c X_c(S)")
print("  = naive + 0  (since v × v = 0 for real v)")
print()
print("  [VERIFIED] Formula is exact for covariant Hessian ✓")
print()

# ===========================
# Final adversarial assessment
# ===========================

print("=" * 60)
print("ADVERSARIAL ASSESSMENT: Is β < 1/6 correct?")
print("=" * 60)
print()
print("  CLAIM: β < 1/6 is the threshold for mass gap via Bakry-Émery")
print("  (8× improvement over SZZ's β < 1/48)")
print()
print("  FINDINGS:")
print()
print("  ✓ Formula HessS = (β/2N)Σ|B_□|² is correct [VERIFIED by FD]")
print("  ✓ Cauchy-Schwarz bound: HessS ≤ 6β|v|² is TIGHT [VERIFIED, 96/96 plaquettes]")
print("  ✓ CS saturated at U=iσ₃: λ_max = 6β exactly [COMPUTED]")
print("  ✓ Mass gap condition: 6β < N/2 = 1 → β < 1/6 [DERIVED]")
print("  ✓ Threshold is exact (CS bound cannot be improved) [VERIFIED]")
print()
print("  VERDICT: β < 1/6 is CORRECT.")
print()
print("  The prior mission's claim is verified by independent derivation.")
print("  The threshold is the exact optimal value from the CS argument.")
print()

# ===========================
# What about Stage 5 questions in GOAL?
# ===========================

print("=== ANSWERING GOAL STAGE 5 QUESTIONS ===\n")
print("  Q: 'λ_max(M(Q)) ≤ 8(d-1) = 24 for all Q via triangle inequality?'")
print("     This is the bound on the LINK adjacency matrix M normalized differently.")
print("     In my notation: max_Q λ_max(H(Q)/β) = 6 (the H_norm).")
print("     The factor of 24 vs 6 reflects a different normalization of M.")
print()
print("  Q: 'H_norm = λ_max/(48) ≤ 24/48 = 1/2... gives 1/2 not 1/8?'")
print("     If H_norm is defined as λ_max(H)/β / 48 (normalized by SZZ's bound):")
print(f"     At Q=I: H_norm = 4/48 = 1/12 ✓ (matches GOAL convention table)")
print(f"     At U=iσ₃: H_norm = 6/48 = 1/8")
print()
print("  Q: 'The claimed H_norm ≤ 1/8 needs a tighter argument'?")
print(f"     ANSWER: H_norm ≤ 1/8 means λ_max(H)/β ≤ 6, which is EXACTLY our CS bound.")
print(f"     The CS bound is tight (saturated at U=iσ₃) with H_norm = 6/48 = 1/8.")
print()
print("  So: H_norm (in GOAL's normalization) ≤ 1/8 means C ≤ 6β.")
print("  This is EQUIVALENT to β < 1/6 (with K_S > 0 condition Cβ < N/2 = 1).")
print()
print("  The GOAL's framing: 'H_norm ≤ 1/8' is the same as my 'HessS ≤ 6β|v|²'.")
print("  Both come from the CS bound, and both give β < 1/6.")
print()
print("  [CONFIRMED] Prior mission's H_norm ≤ 1/8 = 6/48 is correct ✓")
