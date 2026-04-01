# Strategy 001: Adversarial Proof Audit

## Objective

Determine whether the prior mission's central claim (mass gap for lattice SU(2) Yang-Mills at beta < 1/6) is correct, novel, and extensible. This is a validation strategy — the primary mode is adversarial verification, not discovery. Every exploration should be trying to find errors and gaps, not confirm what was claimed.

## Context: What to Validate

A prior Atlas mission (3 strategies, 30 explorations) claimed:

1. **beta < 1/6 proved** via tighter analysis of the SZZ Bakry-Emery Hessian bound
2. **Proof chain:** SZZ Theorem 1.3 gives mass gap for beta < 1/(48 * H_norm). They showed H_norm <= 1/8 via triangle inequality on lambda_max(M(Q)) <= 8(d-1) = 24. Then 1/(48 * 1/8) = 1/6.
3. **Conjecture 1:** lambda_max(M(Q)) <= 4d for all Q, which would give H_norm <= 1/12 and beta < 1/4
4. **Staggered mode** at Q=I is the tight Hessian maximizer: lambda_max(M(I)) = 4d
5. **Numerical evidence:** 500+ configs on L=2,4 with zero violations of Conjecture 1

### Key Prior Files (read these)

- `../../../yang-mills/MISSION-COMPLETE.md` — consolidated claims
- `../../../yang-mills/strategies/strategy-002/FINAL-REPORT.md` — proof details
- `../../../yang-mills/strategies/strategy-002/explorations/exploration-008/REPORT.md` — the actual proof
- `../../../yang-mills/strategies/strategy-002/explorations/exploration-009/REPORT.md` — eigenvalue verification
- `../../../yang-mills/strategies/strategy-003/FINAL-REPORT.md` — conjecture analysis, Weitzenbock

### CNS Papers to Check

- arXiv:2509.04688 (Cao-Nissim-Sheffield, September 2025) — improved SZZ to beta < 1/24
- arXiv:2505.16585 (CNS, May 2025) — different technique

### Known Convention Risk

The SZZ convention is S = -(beta/N) sum Re Tr(U_square), with the 1/N factor. The B_square formula was corrected once already during the prior mission (backward edges include own link in holonomy). Convention errors (factors of 2, N vs 2N, 1/N factors) are the most likely failure mode.

## Methodology: Three-Phase Adversarial Audit

**All explorations are mandatory.** No early stopping. Budget: 8-10 explorations.

### Phase 1: Proof Audit + Novelty Assessment (3 parallel explorations)

Launch all three simultaneously. Each is independent.

**E001 — Independent Proof Rederivation (Math Explorer):**
Starting from SZZ Theorem 1.3 (arXiv:2204.12737), independently derive the beta < 1/6 result. Do NOT read the prior mission's proof first — derive it yourself from the SZZ paper. Then compare with the claimed proof.

Specifically:
1. State the SZZ Bakry-Emery condition precisely, with all conventions (S = -(beta/N) sum Re Tr)
2. Compute the Hessian of the Wilson action for a single plaquette at general Q
3. Apply the triangle inequality to bound lambda_max(M(Q))
4. Derive the resulting threshold for beta
5. Compare: does YOUR derivation give beta < 1/6, or a different number?

If you get a different number, STOP and carefully identify where the discrepancy is. Convention errors are the most likely cause. Report the discrepancy precisely.

Computation is mandatory. Write out every step symbolically AND verify key formulas numerically on small lattices (e.g., L=2).

**E002 — CNS Paper Analysis (Standard Explorer):**
Read the actual CNS papers. This is NOT a literature survey — it's a targeted comparison.

For arXiv:2509.04688 (Sept 2025):
1. What technique do they use to prove beta < 1/24? Is it the same Bakry-Emery approach or something different?
2. Do they already prove beta < 1/6 or better anywhere in the paper?
3. What is their sharpest result for SU(2), d=4?
4. If they don't reach 1/6, what prevents their technique from getting there? Is it a fundamental limitation or could it be trivially extended?

For arXiv:2505.16585 (May 2025):
1. What technique? Same or different from the September paper?
2. What threshold do they reach?
3. Any overlap with the triangle inequality improvement?

Report format: For each paper, state their main theorem, their technique, their convention, and whether our beta < 1/6 result is (a) already in their paper, (b) trivially derivable from their paper, (c) requires genuinely new insight beyond their work.

**E003 — B-square Formula and Convention Verification (Math Explorer):**
The B_square formula was corrected once during the prior mission. Verify the corrected version is correct.

1. Read the prior mission's B_square formula from strategy-002 exploration-008 REPORT.md
2. Derive B_square independently from the Wilson action Hessian
3. Pay special attention to: backward edges including the link's own holonomy, the 1/N factor in the action convention, the Re Tr vs Tr convention
4. Compute B_square numerically for a specific small-lattice configuration and compare with the analytical formula
5. Compute lambda_max(M(Q)) for Q=I on L=2 using BOTH the formula and direct numerical Hessian computation. Do they agree?

If ANY discrepancy is found, this is the most important result of the entire strategy.

### Phase 1 Checkpoint

After all three Phase 1 explorations complete, evaluate:
- If a proof ERROR is found: Phase 2 becomes error diagnosis. Characterize the error, determine if it's fixable, and compute the corrected threshold.
- If CNS already prove 1/6: the novelty claim dies but correctness may still stand. Redirect Phase 2 to understand exactly what (if anything) remains novel.
- If proof is correct AND novel: proceed to Phase 2 extensions.

### Phase 2: Numerical Extension (3 parallel explorations)

**E004 — Large Lattice Verification (Math Explorer):**
Test H_norm <= 1/12 on lattices beyond the prior mission's L=2,4:

- L=8: 4096 links, Hessian 12288x12288. Use sparse power iteration or Lanczos for lambda_max.
- L=16 if tractable: use ARPACK/scipy.sparse.linalg.eigsh
- For each size, test at least 20 configurations: 5 random Haar, 5 Gibbs at beta=0.1, 5 Gibbs at beta=0.15, 5 adversarial gradient ascent (maximize lambda_max by gradient ascent on Q)
- Report: maximum H_norm observed, trend with lattice size, any violations

The gradient ascent is critical: use the gradient of lambda_max(M(Q)) with respect to Q to search for counterexamples. Run for at least 1000 steps.

**E005 — SU(3) Extension (Math Explorer):**
The conjecture for SU(N) predicts H_norm <= d/(4(d-1)N) = 1/18 for N=3, d=4.

1. Implement M(Q) for SU(3) (N^2-1 = 8 Lie algebra dimensions per link)
2. Compute lambda_max(M(Q)) on L=2 for 20+ SU(3) configurations
3. Does H_norm <= 1/18 hold? What is the maximum observed?
4. Check: does the triangle inequality proof of H_norm <= 1/8 generalize to SU(N)? What threshold does it give for N=3?
5. If H_norm <= 1/18 fails for SU(3), find the tight bound

**E006 — d=5 Anomaly Resolution (Math Explorer):**
The prior mission found that for d=5, the staggered mode is NOT the maximum eigenvector of M(I). The true lambda_max = 5*beta > 4.8*beta (staggered value).

1. Compute lambda_max(M(I)) for d=3,4,5,6 by exact Fourier analysis
2. For d=5: identify the maximum eigenvector. What is its structure? Why does the staggered mode fail?
3. Is there a dimension-dependent transition in the structure of the maximizer?
4. Does the triangle inequality bound lambda_max(M(Q)) <= 8(d-1) still hold for d=5?
5. What does this say about the d=4 result — is there something special about d=4, or does the proof carry through for all d?

### Phase 3: Adversarial Synthesis (2 mandatory explorations)

**E007 — Devil's Advocate Review:**
Your job is to ATTACK every claim from Phases 1 and 2. You have all the reports. For each claim:
1. State the strongest counterargument
2. Check: is the evidence sufficient? What would a skeptical mathematician say?
3. For the proof: is there a step that relies on a lemma that wasn't verified?
4. For the numerics: is the parameter space adequately covered? Could there be a counterexample in a regime not tested?
5. For the novelty: could any of this be in an unpublished preprint or PhD thesis?

Focus especially on convention errors. Recheck: does 48 * (1/8) = 6, giving beta < 1/6? Or is the 48 really a 24 or 96 in SZZ's notation?

**E008 — Final Synthesis and Verdict:**
Write the definitive validation report:
1. For each of the 5 MISSION.md items, give a verdict: CONFIRMED / REFUTED / PARTIALLY CONFIRMED / INCONCLUSIVE
2. If the proof is correct: state the theorem precisely with all conventions
3. If the proof has an error: state exactly where and whether it's fixable
4. For novelty: state the relationship to CNS precisely
5. For extensions: summarize SU(3), large lattice, d=5 findings
6. Novel claims section: which claims from the prior mission survive validation?

## Validation Criteria

### Success Indicators
- Every step of the beta < 1/6 proof chain independently verified OR a specific error identified
- CNS comparison based on reading actual papers, not summaries
- Numerical tests on L=8+ with 20+ configurations
- Clear yes/no verdict on SU(3) H_norm conjecture
- d=5 anomaly explained

### Exhaustion Indicators
- All 5 MISSION.md items have clear verdicts
- Adversarial review found no unchecked assumptions
- Remaining uncertainties are clearly identified and scoped

### What Would Indicate a Second Strategy Is Needed
- A fixable error that changes the threshold but not the approach
- CNS overlap that requires reframing the novelty claim
- SU(3) results that open a new research direction

## Methodology Rules

1. **Computation is mandatory in every Math Explorer exploration.** Symbolic derivation must be accompanied by numerical verification on small lattices. No exploration passes without runnable code.

2. **Write incrementally.** Write each derivation step as you complete it. If 10 minutes pass with no file writes, output what you have so far.

3. **Report discrepancies immediately.** If any computation disagrees with a claimed result, state the discrepancy clearly and diagnose the cause before moving on.

4. **Adversarial posture.** Every exploration should be trying to find errors, not confirm claims. "I verified this is correct" is a weaker conclusion than "I tried to break this 5 ways and all failed."

5. **Convention precision.** In every derivation, state the convention being used (S = -(beta/N) sum Re Tr or S = -(beta/2) sum Re Tr, etc.) and track it through every step.
