# Exploration 006: Hessian Slack Verification on 4D Lattice + Worst-Case Search

## Mission Context
This is a YANG-MILLS mission. Do not confuse with other missions.

## Background — Critical Context

From the previous exploration (E005), we found an unexpected major result:

**SZZ Lemma 4.1 Hessian bound is 12-45× loose on typical configurations.**

E005 measured H_normalized = |HessS(v,v)| / (8(d-1)Nβ|v|²) for SU(2) on a 4³ lattice (3D):
| β | max H_norm |
|---|---|
| 0.020 | **0.0224** (bound would be 1.0) |
| 0.100 | **0.0267** |
| 0.500 | **0.0358** |
| 1.000 | **0.0536** |
| 2.000 | **0.0840** |

**CRITICAL CAVEAT:** E005 used a 3D lattice. The Yang-Mills mass gap problem is in d=4. The bound 8(d-1)Nβ has an explicit d-dependence (factor (d-1)). In 4D: bound = 8×3×2×β = 48β. In 3D: bound = 8×2×2×β = 32β.

If the physical mechanism (cancellations between independent plaquettes) carries over to 4D, the slack factor should be LARGER in 4D (more plaquettes per edge = more cancellations).

**SECOND CAVEAT:** E005 only measured TYPICAL Gibbs configurations. The Lemma 4.1 bound must hold for ALL configurations. There may exist adversarial configurations (e.g., aligned plaquettes) that saturate the bound. If so, the bound IS tight and cannot be improved.

## Your Task

### Priority 1: 4D Lattice Measurement

Repeat E005 on a 4⁴ lattice (4D, L=4) at β = 0.02, 0.1, 0.5, 1.0:
- Use the same Kennedy-Pendleton heat bath code (from E003's code base)
- Measure H_normalized = |HessS(v,v)| / (8 × 3 × 2 × β × |v|²) (note: (d-1) = 3 for d=4)
- 10 configurations × 5 tangent vectors = 50 samples per β (faster than E005's 200)
- Report: mean, std, max(H_norm)

**Prior SU(2) code:** `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/yang-mills/strategies/strategy-001/explorations/exploration-003/code/su2_lattice.py`

**Prior E005 code (3D version):** `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/yang-mills/strategies/strategy-002/explorations/exploration-005/code/hessian_sharpness.py`

Adapt E005's code for d=4 (change lattice dimensions, update the bound formula).

### Priority 2: Worst-Case Configuration Search

The question: are there non-Gibbs configurations where H_norm approaches 1.0?

Design an adversarial search:
1. **Aligned configuration:** Set all U_e = I (identity). Compute H_norm. If the action has no plaquette contributions near I, this might be trivial; try U_e = exp(iε_e σ₃) for small random ε_e.
2. **Gradient ascent:** Starting from a random configuration, maximize H_norm(Q, v) over Q and v simultaneously using gradient ascent (finite-difference gradient w.r.t. Q). Run for 100 steps. What is the maximum H_norm found?
3. **Worst-case tangent:** For each configuration in Priority 1, find the tangent vector v that maximizes H_norm (eigenvalue of the per-link Hessian). Report the true max over optimal v (not just random v).

Report: max H_norm found by adversarial search, and which configurations are near-worst-case.

### Priority 3: Physical Interpretation

Based on Priority 1 and 2 results, assess:
1. **If 4D max H_norm ≤ 0.1:** The slack is robust and holds in 4D. This strongly suggests the analytic bound is improvable. Report: what analytic mechanism could explain the cancellations?
2. **If 4D max H_norm ≈ 0.5:** Significant slack but less extreme. Still improvable.
3. **If adversarial search finds H_norm → 1.0:** The bound is tight for non-Gibbs configurations. Report: what type of configuration nearly saturates the bound?

## Success Criteria

**Success:**
1. 4D measurement: max H_norm at β = 0.02 in 4D (with bound factor 48β, not 32β)
2. Adversarial search result: max H_norm found by gradient ascent or aligned config
3. Physical interpretation of the slack (or lack thereof)

**Failure:** If 4D simulation is too slow for the 10-exploration timeline. Fallback: run on 4⁴ × 4 lattice but only β = 0.02 and β = 0.5 (2 values instead of 4).

## Output Format

1. **code/** directory:
   - `hessian_4d.py` — 4D Hessian measurement
   - `worst_case_search.py` — adversarial configuration search
   - `results_4d.json` — 4D measurement results
   - `worst_case_results.json` — adversarial search results

2. **REPORT.md** covering:
   - 4D Hessian results table (comparison with E005 3D results)
   - Worst-case search results
   - Physical interpretation

3. **REPORT-SUMMARY.md** (1 page):
   - Is the 12-45× slack confirmed in 4D?
   - Is there an adversarial configuration that saturates the bound?
   - Implication for whether a tighter analytic Hessian bound is achievable

## Important Notes
- **Write code immediately.** Maximum 5 minutes of thinking before first line of code.
- **Print results as you get them** — don't wait for all β values.
- **Cross-check:** The 4D result should be consistent with d=4 physics (bound = 48β not 32β). Normalize correctly.
- **Save code to files before running.**
- **Fastest path:** Adapt the E005 code — change lattice dims from [4,4,4] to [4,4,4,4], update bound formula.
- Write REPORT.md section by section, not as one large block.
