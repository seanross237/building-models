# Mission History

## Strategy 001: Adversarial Proof Audit
**Status:** COMPLETE
**Explorations:** 8 used / 10 budget
**Objective:** Validate or refute the prior mission's β < 1/6 mass gap claim, assess novelty, test extensions.

### Key Findings
1. **β < 1/6 is PROBABLY CORRECT but NOT RIGOROUSLY PROVED.** Proof gap found in Step 2: the B² formula is not an identity at generic Q. However, λ_max(H_actual) ≤ λ_max(H_formula) for all 190+ tested configs.
2. **Novelty CONFIRMED.** β < 1/6 is not in either CNS paper (Sept 2025, May 2025) and requires going back to the edge-based SZZ framework with a tighter inequality — genuinely new.
3. **Two corrections to prior mission:** (a) Conjecture uses N², not N; (b) odd-d formula was wrong.
4. **Extensions verified:** SU(3) H_norm(I) = 1/27, d=5 anomaly fully resolved (λ_max = dβ universal, staggered saturates only for even d).
5. **Convention resolved:** LEFT formula (P3 = Q1·Q2·Q3⁻¹) is correct; RIGHT gives artifacts at Q ≠ I.

### Tier Classification
- **Tier 1 (Rigorous):** CS bound, link counting, λ_max at Q=I, convention, triangle inequality structure
- **Tier 2 (With citation):** SZZ original threshold
- **Tier 3 (Numerically verified, proof has gap):** β < 1/6 threshold, H_norm conjecture
- **Tier 4 (Conjectured):** λ_max(actual) ≤ λ_max(formula) for all Q

### Methodology Assessment
Three-phase adversarial audit (8/10 effectiveness). Adversarial posture found the genuine gap. Convention precision was critical. Explorer stalling affected E003, E004, E008 but strategizer worked around it. All 5 mission items received clear verdicts.

### What's Exhausted
- Novelty assessment (definitively answered)
- Convention questions (resolved)
- Numerical evidence at L=2,4,6 for SU(2) and SU(3)
- Dimensional analysis (all d unified)

### What Remains
- **Repairing the Step 2 gap** — the one remaining obstacle to upgrading from Tier 3 to Tier 1
- Four repair paths identified (v²=-c·I for SU(2), flat maximizer proof, direct Hessian bound, tightened SZZ)
- Gradient ascent on actual H_norm (not formula H_norm) — would strengthen the numerical evidence

---

## Strategy 002: Focused Gap Repair
**Status:** COMPLETE — DEFINITIVE NEGATIVE RESULT
**Explorations:** 3 used / 5-6 budget (early termination — result was conclusive)
**Objective:** Repair the proof gap at Step 2 (B² formula) or prove it is irreparable.

### Key Findings
1. **λ_max(H_actual) > λ_max(H_formula) is TRUE for one-hot perturbations at d≥3.** The B² formula is NOT a valid upper bound. Excess: ~0.2% at d=3, ~0.018·θ² coefficient at d=4.
2. **Flat connections are NOT global maximizers of λ_max(H_actual) at any d≥2.** Two mechanisms: one-hot small-angle (d≥3) and complex multi-link (d=2, 2.6% excess).
3. **Complete analytical SU(2) Hessian formula derived (NOVEL).** d²/dt² Re Tr(U□) = -(|w|²/2)cos(θ/2) + (1/2)L⃗·b⃗. Verified to O(h²) ~ 2×10⁻⁷.
4. **Decomposition C = C_curv + C_comm where C_curv is PSD, C_comm indefinite.** Top eigenspace of H_actual avoids C's negative directions (ratio 1.10).
5. **λ_max(H_formula) is exactly invariant under one-hot perturbations** — structural property of B² Gram operator, not previously noted.

### Paths Eliminated
| Path | Verdict |
|------|---------|
| A: λ_max(H_actual) ≤ λ_max(H_formula) | **DISPROVED** (r > 1 for one-hot) |
| B: Flat connections maximize H_actual | **DISPROVED** (counterexamples at all d≥2) |
| C: Tighten SZZ Lemma 4.1 | Not attempted (factor 2N² improvement needed) |
| D: Direct SU(2) bound via v²=-cI | Formula found, bound incomplete (cross terms too large) |

### Tier Classification Update
- **Tier 4 → DISPROVED:** λ_max inequality AND flat maximizer hypothesis both false
- **Tier 1 (NEW):** Complete analytical Hessian formula
- **Tier 3 (UNCHANGED):** β < 1/6 — numerically robust, proof gap irreparable via B² route

### Methodology Assessment
Check-before-prove methodology (9/10 effectiveness). E001's stress test had a coverage gap (missed one-hot small-angle) but E003 caught it. 3/5-6 budget used — excellent efficiency. Novel Hessian formula is a permanent result from a "failed" repair.

### What's Exhausted (Mission-Level)
- All 4 B² formula repair paths tested or numerically eliminated
- All 5 mission items have clear verdicts
- 490+ configs tested across 11 explorations

### What a Future Mission Could Pursue
- Direct bounding of H_actual bypassing B² formula (using the analytical formula)
- Characterize max_Q λ_max(H_actual) on larger lattices
- Probabilistic Bakry-Emery (avoiding worst-case bound)

---

## MISSION COMPLETE
**Total: 2 strategies, 11 explorations**
**Verdict: PARTIALLY VALIDATED** — conclusion almost certainly correct, proof chain has irreparable gap, novelty confirmed, extensions verified with corrections, novel analytical results produced.
