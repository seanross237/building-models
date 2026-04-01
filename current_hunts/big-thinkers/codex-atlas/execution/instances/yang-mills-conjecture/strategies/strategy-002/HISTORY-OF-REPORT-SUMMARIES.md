# Exploration History

## Exploration 001: SDP/SOS Certificate for 9D Eigenspace Bound

**Outcome:** Partial success — numerical confirmation at scale, clean decomposition formula found, no SOS proof.

Key findings:
- **[VERIFIED]** M_12(I) = 16 I_12 - 4(J_4 ⊗ I_3), eigenvalues {0(x3), 16(x9)}. Bound tight at Q=I.
- **[COMPUTED]** lambda_max(M_9(Q)) < 16 for 16,000+ configs. Adversarial max = 15.637.
- **[COMPUTED]** Per-plaquette SOS BLOCKED: single-plaquette lambda_max = 8 at Q=I (budget is 4). Ratio up to 7454x.
- **[VERIFIED]** Key algebraic identity: sum_{mu<nu} T_mu^T [(I-R_mu) + (I-R_nu^T)] T_nu = -sum_mu f(R_mu, T_mu) (error 7e-15)
- **[COMPUTED]** Exact decomposition: 16||T||^2 - F_x = f_same + 2*f_R - Term_C - Term_D (error 7e-14)
- **[COMPUTED]** Cross-term ratio 5.24% (better than claimed 8.2%)
- **[VERIFIED]** No uniform epsilon > 0: bound tight at Q=I. Gap ~ O(||Q-I||^2).
- **Remaining gap:** Proving Term_C + Term_D <= f_same + 2*f_R algebraically.

## Exploration 002: Block Extension of Combined Bound Lemma

**Outcome:** Structurally complete proof with one algebraic gap (LEMMA_D and LEMMA_RDR).

Key findings:
- **[VERIFIED]** Vector CBL (VCBL): f(A,p) + f(B,q) + p^T(I-A)D(I-B^T)q >= 0 for ALL p,q in R^3, A,B,D in SO(3). Proof: same C-S + AM-GM as scalar CBL. 0 violations in 200K tests.
- **[VERIFIED]** Per-plaquette identity confirmed (error 1e-13).
- **[VERIFIED]** Key decomposition via sum-to-zero trick: total_gap = 2*sum_mu f(R_mu, T_mu) + sum_S (error 5.7e-14).
- **[COMPUTED]** sum_S = LEMMA_D + LEMMA_RDR >= 0 in 200K tests (0 violations). Adversarial min sum_S = 0.587||T||^2.
- **[COMPUTED]** LEMMA_D: min = 0.41||T||^2, 4x safety margin. 0 violations in 200K tests.
- **[COMPUTED]** LEMMA_RDR: min = 0.62||T||^2, 6x safety margin. 0 violations in 200K tests.
- **[COMPUTED]** Both lemmas FAIL without constraint sum T_mu = 0 (942/200K violations).
- **[VERIFIED]** Identity ||(I-M^T)p||^2 = 2f(M,p) for M in O(n).
- **Remaining gap:** Proving LEMMA_D >= 0 and LEMMA_RDR >= 0 algebraically.

LEMMA_D: sum_{mu<nu} [f(R_mu D, T_mu) + f(D R_nu^T, T_nu) - 2 T_mu^T (I-D^T) T_nu] >= 0
LEMMA_RDR: sum_{mu<nu} [f(R_mu D, T_mu) + f(D R_nu^T, T_nu) - 2 T_mu^T (I-R_mu D R_nu^T) T_nu] >= 0

## Exploration 003: Prove LEMMA_D and LEMMA_RDR — CRITICAL DISCOVERY

**Outcome:** LEMMA_D and LEMMA_RDR are individually FALSE. Their SUM (sum_S) appears non-negative.

Key findings:
- **[VERIFIED]** LEMMA_D is FALSE: min eigenvalue = -2.13. Genuine SO(3) counterexample found via adversarial optimization. 20 independent optimizations converge to same minimum.
- **[VERIFIED]** LEMMA_RDR is FALSE: min eigenvalue = -1.45.
- **[COMPUTED]** sum_S = LEMMA_D + LEMMA_RDR >= 0: 200 adversarial optimizations ALL converge to min eigenvalue = 0 (TIGHT). The two lemmas always compensate.
- **[COMPUTED]** sum_S = 0 iff D = I (for ANY R, ANY T in V). The zero set is parameterized by R alone when D = I.
- **[VERIFIED]** At R = I: sum_S = 2*sum VCBL(D,D,-I,...) >= 0 (proved via C-S + AM-GM).
- **[COMPUTED]** Per-plaquette VCBL can't close the gap: cross term is rank 3, VCBL product rank <= 2.
- **[COMPUTED]** Near Q=I, sum_S ~ O(eps^2) with positive coefficient ~2.96.
- **[COMPUTED]** max |harmful cross|/budget ≈ 0.28 for random Q,T. Approaches 1.0 only at D=I.

**Revised proof target:** Prove sum_S >= 0 directly (not via individual LEMMA_D + LEMMA_RDR).

**Total proof structure:**
16||T||^2 - F_x = 2*sum f(R_mu, T_mu) [PROVED >= 0] + sum_S [CONJECTURED >= 0, tight at D=I]

## Exploration 004: Prove sum_S >= 0 — Significant Partial Success

**Outcome:** Critical T theorem PROVED. D=I identity corrected and proved. Full algebraic proof still open.

Key findings:
- **[VERIFIED+PROVED]** sum_S(D=I) = 6*sum f(R_mu, T_mu) + |sum R_mu^T T_mu|^2 >= 0. Manifestly non-negative. CORRECTS E003's claim that sum_S(D=I) = 0 for all T — it's 0 only for T on axes (null eigenvalue, multiplicity 1).
- **[VERIFIED]** Delta factoring: sum_S(D) = baseline + sum_{mu<nu} 2*u^T*(I-D)*v where u = R_mu^T T_mu - T_nu, v = T_mu - R_nu^T T_nu. Error < 7.1e-14.
- **[VERIFIED+PROVED]** Critical T theorem: For T on rotation axes (T_mu = c_mu*axis(R_mu) with sum c_mu*axis = 0), u = v, so Delta = sum 2f(D,u) >= 0. This proves sum_S >= 0 for the MOST DANGEROUS direction (null eigenvector of M9 at D=I).
- **[COMPUTED]** 67K adversarial tests: min eigenvalue = 3.9e-13 ≈ 0 (at D=I). Every perturbation from D=I increases min eigenvalue.
- **Dead ends identified:** Convexity in D (FAILS), per-plaquette VCBL (IMPOSSIBLE, rank obstruction), eigenvalue perturbation (FAILS), Gershgorin (FAILS), M12 PSD directly (FAILS — 2 negative eigenvalues).
- **Key structural observation:** u - v = -(I-R_mu^T)T_mu - (I-R_nu^T)T_nu, controlled by f(R) terms. The correction from "on axes" to "off axes" is bounded by rotation deficiency.

## Exploration 005: Close sum_S >= 0 — PROOF COMPLETE

**Outcome: SUCCESS — sum_S >= 0 PROVED. Full proof chain complete.**

Key findings:
- **[PROVED]** Crude polarization approach FAILS (correction/baseline > 10). Wrong approach.
- **[VERIFIED]** M9 is AFFINE in D (error < 3.5e-15). Critical structural property — enables per-pair minimization.
- **[PROVED]** Per-pair Cauchy-Schwarz: u^T D v <= ||u||*||v|| for orthogonal D. Independent minimization over D gives D-free lower bound.
- **[VERIFIED]** Key computation: sum||u-v||^2 = 4*sum f(R,T) + |sum R^T T|^2. Error < 1.1e-13.
- **[PROVED]** Beautiful cancellation: F = (6*sum f + |sum a|^2) - (4*sum f + |sum a|^2) + sum(||u||-||v||)^2 = 2*sum f + sum squares >= 0.
- **[VERIFIED]** sum_S >= F >= 0 for 25K random + adversarial tests, 0 violations. Min gap (sum_S - F) = 6.1.
- **Stronger result**: Proof works for ALL contractions ||D|| <= 1, not just SO(3).
- **Tight**: F = 0 iff T on rotation axes (matching null eigenvector from E004).

## Exploration 006: Adversarial Review — CONDITIONAL PASS

**Outcome:** All per-vertex identities (B1-B9) VERIFIED from scratch. Per-vertex bound correct with large margin. LOGICAL GAP in upstream connection: staggered bound does NOT imply full lambda_max bound.

Key findings:
- **[VERIFIED]** All 11 identity claims (B1-B9 + no double counting + lattice formula). Fresh code. Errors < 3e-12.
- **[VERIFIED]** Per-vertex F_x <= 16||T||^2 with 0 violations in 1800+ tests. Adversarial max = 14.36.
- **[VERIFIED]** No double counting in per-vertex to global sum reduction.
- **[FAILED]** The claim "staggered bound => full lambda_max bound" is INVALID. For random Q, the top eigenvector is predominantly NON-staggered (staggered projection < 0.5). Non-staggered eigenvalue reaches 14.6 (from 12 at Q=I).
- **[COMPUTED]** Full lambda_max(M(Q)) <= 16 in 700+ tests (L=2 and L=3), 0 violations. But proof doesn't cover non-staggered modes.
- **[COMPUTED]** L=3: lambda_max(M(I)) = 12 (not 16). Staggered bound of 16 is slack. lambda_max for random Q reaches ~14.1.
- **[CONJECTURED]** SZZ normalization needs exact specification.

**Status of proof:**
- PROVED: Staggered Rayleigh quotient ≤ 16 (complete, adversarial-verified)
- NOT PROVED: Non-staggered eigenvalues ≤ 16 (spectral gap of 4, max observed 14.6)
- COMPUTED: Full lambda_max ≤ 16 (700+ tests, 0 violations)

## Exploration 007: Non-Staggered Eigenvalue Bound — CRITICAL NEGATIVE

**Outcome:** lambda_max(M(Q)) > 16 appears achievable via targeted optimization (~16.08). But M(Q) may differ from the Hessian operator used in SZZ.

Key findings:
- **[COMPUTED]** Edge-by-edge gradient ascent: lambda_max ≈ 16.08 in 5 independent trials. Verified with PSD check, trace = 1152, Rayleigh quotient confirmation.
- **[COMPUTED]** Random Q (2000+): max 14.64, 0 violations. Violations require targeted optimization.
- **[VERIFIED]** Uniform Q: lambda_max = 16 exactly for ALL angles (Fourier block analysis + K_4 Laplacian proof).
- **[VERIFIED]** B-field formula verified against numerical differentiation.
- **[COMPUTED]** M(Q) ≠ Wilson action Hessian. Hessian = M(Q) - C(Q) where C(Q) involves curvature correction. Tr(C) ≈ -1148 (large).
- **[COMPUTED]** For L=3 and L=4 random tests: 0 violations of 16.
- **CRITICAL QUESTION**: Does the SZZ framework use M(Q) = sum B^T B directly, or the Hessian H(Q) = M(Q) - C(Q)?
- **CAUTION**: E007 used B_p formula Q_1 a_1 + Q_1 Q_2 a_2 - ... which may use fundamental representation rather than adjoint. If adjoint is the correct convention, the counterexample needs re-verification.

**The 6-step proof:**
1. Master identity: sum_S = baseline + sum 2u^T(I-D)v [E004]
2. Cauchy-Schwarz: u^T Dv <= ||u||*||v|| [Proved]
3. Independent minimization over D [Proved]
4. Algebraic identity: 2(||u||*||v|| - u*v) = ||u-v||^2 - (||u||-||v||)^2 [Verified]
5. Key cancellation: sum||u-v||^2 = 4*sum f + |sum a|^2 [Verified]
6. Assembly: F = 2*sum f + sum(||u||-||v||)^2 >= 0 [Proved]

