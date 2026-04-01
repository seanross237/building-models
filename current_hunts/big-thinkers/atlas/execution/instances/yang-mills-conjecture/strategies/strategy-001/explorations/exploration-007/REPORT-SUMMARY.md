# Exploration 007: ADVERSARIAL REVIEW — Summary

## Verdict: CONDITIONAL PASS

## What was the goal

Independently verify (or refute) every step of the proof claimed in Exploration 006 that lambda_max(M_total) <= 64 for all SO(3) configurations on the L=2 d=4 torus, which implies Conjecture 1 (lambda_max(M(Q)) <= 16).

## What was tried

Wrote all code from scratch (8 independent scripts, no code copied from E006). Tested:
- Lattice construction (L=2, L=3, L=4)
- Full 192×192 M(Q) eigenvalues (200+ configs)
- Per-vertex F_x bound (3200+ tests on L=2, 40,000+ on L=3)
- Sign structure enumeration (all vertices, L=2/3/4)
- Proof formula match against actual lattice computation (1600+ tests per L)
- Algebraic identity verification (100k tests each)
- Cauchy-Schwarz bound (200k tests)
- Combined Bound Lemma assembly (100k tests)
- Adversarial gradient descent (200 trials)
- Near-identity eigenvalue behavior
- Top eigenspace characterization at Q=I

## Outcome: Two gaps found, core proof correct

### Core proof: CORRECT

The algebraic proof of lambda_max(M_total) <= 64 via the Combined Bound Lemma is correct. All five steps verified:
- Sign structure (28+/8-, net 20) ✓
- Trace identity c+Tr(P) = 64 ✓
- Expansion 64I-M = 2×[groups] (error < 4.3e-14) ✓
- Combined Bound Lemma: algebraic identity (error < 2.7e-15), Cauchy-Schwarz (ratio < 1.0), AM-GM (trivially true) ✓
- Assembly (100k configs, 0 violations) ✓

### Gap 1: Full matrix vs staggered mode (MODERATE)

The proof bounds the staggered mode Rayleigh quotient but Conjecture 1 is about the full operator lambda_max. At Q=I (the tight case), the top eigenspace is 9-dimensional with staggered modes contributing only 3 dimensions. The proof does not show that non-staggered modes are also bounded by 16.

Numerically: 0 violations in 200 tests (max full lambda = 14.41).

### Gap 2: Odd L sign structures (MINOR)

The proof's M_total formula A = a(I+RD)+b(R+RDR^T) is valid for even L only. On L=3, vertices with coordinates = L-1 have a different formula (max discrepancy 31.8). The proof doesn't cover odd L.

For even L (sufficient for continuum limit): formula verified correct for L=2 and L=4. Even L numerically verified: 0 violations.

## Verification scorecard

- **13 VERIFIED** (machine-checked or algebraically proven)
- **5 COMPUTED** (numerically verified, no violations)
- **1 CONJECTURED** (full matrix reduction, numerically supported but not proven)

## Key takeaway

The core algebraic insight — the Combined Bound Lemma pairing base-link deficiency with inactive cross-link negativity via Cauchy-Schwarz + AM-GM — is correct and elegant. The proof fully establishes lambda_max(M_total) <= 64 for the L=2 per-vertex matrix with the standard sign structure. The remaining gaps are in the reductions connecting this local bound to the global Conjecture 1.

## Leads worth pursuing

1. **Close Gap 1**: Prove that lambda_max(M(Q)) is maximized at Q=I, where the staggered mode IS in the top eigenspace. Near-identity analysis shows lambda_max decreases monotonically from 16 — a convexity/concavity argument might close this.

2. **Close Gap 2**: For odd L, the sign structure at boundary vertices has 3-4 inactive planes instead of 2, but the trace identity gives c+Tr(P) <= 48 < 64. A variant of the Combined Bound with a tighter target might work, or simply observe that 48 < 64 provides extra slack.

3. **Operator inequality approach**: Instead of per-vertex, prove 16I - M(Q) >= 0 as an operator inequality on the full 192×192 space. This would close both gaps simultaneously.

## Proof gaps identified

- The factorization LHS = n^T(I-A)D(I-B^T)n + f(A) + f(B) is tight (equality at A·n = n, B·n = n). No room for improvement in the lemma itself.
- The 6 non-staggered modes in the top eigenspace at identity need characterization. They appear to be complex lattice modes, not simple Fourier modes.
- The base-link budget deficit on odd L (3+ inactive planes) means the current grouping strategy cannot be directly extended. A different grouping or a different proof technique is needed for odd L.

## Unexpected findings

- On L=3 at identity, the full matrix maximum is only 12 (not 16!). The staggered mode Rayleigh quotient is 13.33 (not 16!). This is because L=3 vertices with modified sign structures have F_x < 64 at identity (as low as 32), pulling down the global average.
- The full matrix spectrum at identity follows a clean pattern: eigenvalues {0, 4, 8, 12, 16} for L=2 and {0, 3, 6, 9, 12} for L=3, suggesting a formula lambda_k = 4k for L=2 and lambda_k = 3k for L=3.
