---
topic: Always include a trivial control check in computation explorations
category: methodology
date: 2026-03-30
source: "thermal-time strategy-001 meta-exploration-003, riemann-hypothesis strategy-003 meta-exploration-006, yang-mills s003-meta-exploration-004, yang-mills s003-meta-exploration-s003-007, vasseur-pressure strategy-001 meta-exploration-007"
---

## Lesson

Every computation exploration should include at least one "trivial control check" — a comparison that should equal something exactly by construction. The control check serves three purposes: (1) validates that the code is correct; (2) confirms that the discrepancy found in the main result is physical, not numerical; (3) builds immediate trust in the computation for readers.

A good trivial control check costs almost nothing (no extra computation, often just a different path through the same data) and pays off enormously if there's a bug.

## Evidence

- **thermal-time strategy-001 exploration-003** — The goal included: C_global(τ) = Tr[ρ_AB · e^{i(K_AB/β)τ} x_A e^{−i(K_AB/β)τ} · x_A] as a control check against C_full(τ). Since K_AB = βH_AB + const·I for a Gibbs state, C_global and C_full are theoretically identical. Numerical result: max|C_global − C_full| = 0.00e+00 for ALL λ values (exactly machine zero). This check confirmed: (a) the eigendecomposition and spectral weight code are correct; (b) the 82.7% discrepancy between C_full and C_local is real physics, not a bug in the C_local path. Without this control, the large discrepancy might have been dismissed as a computational error.

## Design Pattern

**Structure:** For any computation that produces result Y ≠ expected_value, include a computation that should produce Z = expected_value by construction.

**Common forms:**

1. **Two paths to the same answer:** Compute X via method A and method B independently. They should agree exactly if both are correct. (Used in thermal-time E003: K_AB/β path vs. H_AB path for the same correlator.)

2. **Limit check:** At special limiting parameter value (λ=0, T→0, etc.), result should reduce to known analytic value. E.g., "At λ=0, C_full and C_local should both equal (coth(βω/2)/2ω)·cos(ωτ)."

3. **Symmetry check:** Physical symmetry constrains results (e.g., C(τ) is real-valued, C(0) = ⟨x²⟩, C(−τ) = C(τ)*). Violation = code bug.

4. **Conservation check:** A quantity that should be conserved (norm, energy expectation, trace of density matrix) should stay constant under time evolution.

**Placement in GOAL.md:** Include as a mandatory section: "Compute [control check]. This should equal [expected value] by [theoretical reason]. If it doesn't, stop and debug before proceeding."

## Why This Works

The control check converts "potentially wrong computation" into "verified computation." A large unexpected result (e.g., 82.7% discrepancy) is always suspect. The trivial control check provides independent corroboration: "If the code were buggy in a way that would explain the large discrepancy, it would also fail this control check — but it doesn't."

For physical theories, control checks are often free: global vs. local, limit case, symmetry — these don't require additional approximations.

## When to Apply

- Any exploration where the main result is a large discrepancy between two quantities
- Computation-heavy explorations where a code bug would be hard to detect from results alone
- Explorations where the main result is surprising — the more surprising, the more important the control check
- Anytime two computational paths exist that should give the same answer for different reasons

## Variant: Analytical Cross-Check Route for Multi-Step Integral Chains

When the primary computation involves a multi-step integral chain (e.g., K(τ) → Σ₂ → Δ₃), include an **independent analytical formula** as a parallel cross-check route — not just a control within the same chain, but a completely different path to the same answer.

- **riemann-hypothesis strategy-003 exploration-006** — The K(τ) → Σ₂ → Δ₃ integral chain had a systematic ~2× normalization error (GUE control gave 0.491 vs known 0.226 at L=10). Berry's closed-form formula Δ₃_sat = (1/π²)·log(log(T/(2π))) — included as Task 3 — gave a clean, well-defined result (0.154 at T=600, matching measured 0.155 within 1%) even though the integral route failed. Without the Berry formula cross-check, the exploration would have been inconclusive.

**Design pattern for integral chains:**
1. Compute via the integral chain (primary method)
2. Run the same chain with a **known-analytic input** (e.g., K_GUE = min(τ,1)) and verify the output matches the known-analytic result: "After computing Δ₃ from K_GUE, confirm Δ₃_GUE(L=10) ≈ 0.226. If not, stop and report the discrepancy."
3. Include an **independent formula** (if one exists) as a separate task that bypasses the chain entirely

Step 2 would have flagged the normalization issue immediately instead of after full computation. Step 3 salvaged the exploration when the primary route failed.

## Variant: Multiple Computation Variants for Relative Comparison

When absolute normalization might fail, design the exploration with **multiple variants** of the main quantity (e.g., nocap, cap, GUE control versions of K(τ)). Even if absolute values are broken, relative comparison between variants can produce valid findings.

- **riemann-hypothesis strategy-003 exploration-006** — Three K(τ) versions (nocap, cap, GUE) were fed through the same integral chain. Absolute Δ₃ values were all ~2× too large, but the relative comparison showed K_primes(cap) is only 3.3% above GUE — a genuine physical finding (tau<1 differences are negligible) extracted from a normalization-broken computation.

## Variant: Q=I Sanity Check for Hessian/Eigenvalue Computations

For any exploration computing Hessian eigenvalues or spectral properties of lattice gauge theory operators, always start with a **Q=I baseline check**: compute λ_max at the identity configuration and verify it matches the known analytical value (e.g., λ_max = 4β for SU(2) d=4). This catches convention errors (missing 1/N factor), formula bugs, and code setup issues before the main scan begins.

- **yang-mills strategy-003 exploration-004** — The Q=I sanity check (λ_max = 4.000000 = 4β, H_norm = 1/12 exactly) immediately validated the setup and caught the convention. A prior exploration (E004 code) initially used S = −β Σ Re Tr (missing 1/N) which gave λ_max = 8β; the Q=I check detected this immediately.

**Template for GOAL.md:** "Task 0: Sanity check — compute λ_max(H) at Q=I. Expected: [analytical value]. If mismatch, stop and check conventions before proceeding."

## Variant: Numerical Sanity Check Before Proof Attempts

For proof explorations ("prove X"), always start with a numerical check of the claim itself: compute X for 3-5 random examples. If X fails in any example, X is false — pivot immediately rather than spending the entire exploration on a doomed proof.

- **yang-mills strategy-003 exploration-007** — Goal: prove M(Q) ≼ M(I). A 5-line Python check (compute eigenvalues of M(Q)−M(I) for 3 random Q) would have immediately shown positive eigenvalues, revealing the claim is false. Instead, the explorer spent significant effort on four proof approaches (A/B/C/D) before confirming falseness numerically.

**Template for GOAL.md:** "First: compute [claim] for 3-5 random configurations. If any counterexample is found, the claim is FALSE — do not attempt to prove it. Instead, characterize the failure and identify the correct (weaker) statement."

This is distinct from the Q=I sanity check (which validates code correctness) — this variant validates the **proof target** itself. Cost: ~5 minutes. Payoff: prevents entire exploration from being wasted on false target.

## Non-Trivial Control Variant (yang-mills-validation E003)

**Counterpoint:** For convention/formula verification tasks, a TRIVIAL control (Q=I, flat config) is USELESS because it hides errors. Different formula conventions produce identical results at the identity. Always include a NON-TRIVIAL control: a configuration with nontrivial parallel transport but predictable structure.

**Example:** U_all = iσ₃ is a perfect test case for B_□ formula verification — it has nontrivial adjoint transport (R = diag(-1,-1,+1)) but flat plaquettes (U_□ = I), so the eigenvalue structure is predictable (should equal Q=I if the formula handles transport correctly). Testing at Q=I cannot distinguish left from right perturbation formulas; testing at iσ₃ immediately reveals the difference (λ_max = 4β for LEFT, 6β for RIGHT).

**Rule:** For convention-sensitive computations, test at BOTH a trivial config (sanity) AND a non-trivial config (discrimination). The non-trivial config must satisfy: (a) nontrivial parameter values, (b) predictable output from independent reasoning.

## Variant: Known-Answer Validation at Exact-Solution Conditions

When building code on top of prior code or extending a computation to new regimes, always include a sanity check at conditions where the answer is known exactly (e.g., t=0 for an exact initial condition, exact Beltrami flow with known eigenvalue). This catches sign errors and formula bugs propagated from earlier code versions.

- **vasseur-pressure strategy-001 exploration-007** — The pressure decomposition code was built on prior E002/E004 code that had a sign error (missing minus sign in pressure Poisson solve). The t=0 sanity check for exact Beltrami (where R_frac should be 0, not 2.0) caught the error immediately. Without this check, all reported R_frac values would have been wrong. The explorer iterated through v1, v2, v3 of the code; only v3 passed the sanity check.

**Template for GOAL.md:** "Before reporting results, verify at [exact-solution condition] that [quantity] = [expected value]. If not, the code has a bug — debug before proceeding."

**When to apply:** Any exploration that extends or builds on prior code; any exploration measuring a quantity that has a known exact value in a limiting case. Especially important when code is reused across explorations (sign conventions, normalization factors, and index conventions are the most common error sources).

## Variant: Verify Mathematical Identity Before Building Measurements On It

When a goal prescribes a specific mathematical decomposition (e.g., Hessian/Lamb split), include a verification step: "confirm that the identity div(omega x u) = ... holds for u_below before computing the decomposition." If the identity requires assumptions (e.g., div u = 0) that the truncated quantity violates, the entire measurement is invalid.

- **vasseur-pressure strategy-001 exploration-007** — The goal prescribed a three-way Hessian/Lamb/compressibility decomposition, but div(u_below) != 0 invalidates the Lamb vector identity. The explorer correctly pivoted to a two-way Bernoulli/remainder decomposition. Had the identity verification been in the goal, the pivot would have happened at the design stage rather than during debugging.

**Template for GOAL.md:** "Task 0: Verify that [identity] holds for [quantity]. If it does not, explain why and use [fallback decomposition] instead."

## What NOT to Do

Do not use the main computation as its own check (circular). The control check must be genuinely independent — different code path, different limiting case, different theoretical argument.
