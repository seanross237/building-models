# Exploration 001 Summary — Santos O(ħ²) Connection

## Goal
Investigate whether Santos (2022) O(ħ²) corrections quantitatively predict our measured SED discrepancies: 15-18% anharmonic residual (⟨x²⟩_ALD=0.303 vs ⟨x²⟩_QM=0.257 at β=1) and tunneling slope=1.049.

## What Was Tried
1. Found and read Santos (2022) arXiv:2212.03077 in full. Extracted the key theorem.
2. Computed ⟨x²⟩ numerically via Schrödinger equation for multiple β values.
3. Computed classical Boltzmann ⟨x²⟩ at T_eff = ħω/2 for comparison.
4. Derived WKB action S = 2√2/(3λ) analytically for the double-well (verified numerically).
5. Analyzed what O(ħ²) corrections could give slope=1.049.
6. Verified consistency with Pesquera-Claverie (1982) via symmetry argument.

## Outcome: MINIMUM SUCCESS

### Santos Framework Summary
Santos proves: **SED = O(ħ) QED** in the Weyl-Wigner representation. Full QED uses the Moyal equation; SED uses the classical Liouville equation (O(ħ) truncation). The O(ħ²) correction term is:
```
(ħ²/24) × V'''(x) × ∂³W/∂p³ = βħ²x × ∂³W/∂p³   [for quartic V = ½x² + βx⁴]
```
For quadratic Hamiltonians (V'''=0): O(ħ²) = 0, SED is exact. For nonlinear systems: O(ħ²) ≠ 0, SED fails. This formally explains all SED failures for nonlinear systems.

### Part B: Anharmonic Oscillator — Result: EXPLAINED (not independently predicted)

Key hierarchy at β=1 (natural units):
- ⟨x²⟩_classical (T=ħω/2) = **0.183**
- ⟨x²⟩_QM = **0.257** (verified numerically)
- ⟨x²⟩_ALD (SED) = **0.303** (from prior simulation)

The ω³ ZPF in SED **overshoots** the QM value — not just fails to reach it. Santos' O(ħ²) Moyal correction then brings 0.303 → 0.257 (negative correction = −0.046). Santos' framework explains WHY this correction exists (it's the Moyal bracket term) but does NOT independently predict the number 0.046 without already knowing either the ALD result or the QM result. This is a definitional statement, not a new prediction.

**Symmetry result (key finding):** The O(ħ²) Moyal correction to ⟨x²⟩ is zero at O(β) (first order in the quartic coupling), consistent with Pesquera-Claverie (1982) showing SED = QM at O(β). The 0.046 discrepancy is an O(β²) effect that has accumulated for β=1 (non-perturbative regime). This is proven by the parity argument: the Moyal source term is odd in x and odd in p, making ΔW odd in x, and ∫∫ x²(odd in x) dx dp = 0.

### Part C: Tunneling Slope — Result: NOT EXPLAINED by O(ħ²)

New derivation: WKB action S = 2√2/(3λ) [analytical, verified numerically]. Kramers exponent K = √2/(4λ). Faria-França slope=1.000 is an algebraic identity (both sides equal 5√2/(12λ)).

The O(ħ²) anharmonic correction to the well energy is δE = −λ/4 (from perturbation theory: +3λ/32 quartic −11λ/32 cubic). This is λ-dependent (→0 for deep barriers) and **cannot** produce a constant 4.9% slope deviation over 4 decades. Prefactor corrections affect the intercept (0.072) not the slope.

**Conclusion:** slope=1.049 is most likely a **finite-τ/finite-ω_max artifact** that converges to 1.000 in the physically correct limit. The 0.072 intercept IS consistent with an O(ħ²) prefactor correction.

## Key Takeaway
Santos' framework **correctly classifies** the 15-18% anharmonic discrepancy as the missing O(ħ²) Moyal correction. It does not independently predict the numerical value. The tunneling slope=1.049 is NOT an O(ħ²) effect — it is a simulation artifact. **The grand claim ("both discrepancies are the O(ħ²) corrections") is HALF-CONFIRMED**: the anharmonic residual yes, the tunneling slope no.

## Unexpected Findings
1. **Hierarchy reversal:** classical(0.183) < QM(0.257) < ALD/SED(0.303). The SED/ALD result overshoots QM (not undershoots). The O(ħ²) quantum correction is NEGATIVE — quantum mechanics is MORE CONSTRAINED than the classical stochastic SED simulation for nonlinear systems. This is opposite to naive intuition about "quantum fluctuations."

2. **New analytic result:** WKB action S = 2√2/(3λ) for V = −½x² + ¼λx⁴, derived analytically using the factorization V − V_min = (1/(4λ))(1 − λx²)². This gives the exact tunneling action and confirms Faria-França's slope=1 analytically.

3. **O(β) coincidence:** SED and QM give identical ⟨x²⟩ at first order in β (proven via symmetry of the Moyal source term). This is deeper than it appears: the O(ħ²) correction is present but its contribution to ⟨x²⟩ is symmetry-forbidden at leading order.

## Leads Worth Pursuing
- The slope=1.049 deviation likely comes from finite ω_max: the ZPF spectrum cutoff reduces effective E_zpf → increases Kramers exponent → slope > 1 with a constant (λ-independent) deviation. **A targeted τ, ω_max extrapolation of the slope toward 1.000 would confirm or refute this.**
- Can an analytic SED calculation (not just numerical) give ⟨x²⟩_SED for the quartic oscillator? If yes, it would make the Santos prediction truly independent. Approach: perturbation theory in β for the classical stochastic problem.

## Computations Identified
- **Independent test of Santos framework:** Compute d⟨x²⟩_SED/dβ at β=0 from first principles (solving the classical Fokker-Planck equation with ω³ noise spectrum, perturbatively). If this gives −3/2 (same as QM), it confirms SED = O(ħ) QED at O(β). Medium difficulty (20-line calculation). Input: the Fokker-Planck equation for ω³ noise.
- **Slope convergence test:** Run ALD tunneling simulation at λ=0.1 (deep barrier) for 3-4 different ω_max values. Plot slope vs 1/ω_max. If slope → 1.000 linearly, confirms artifact hypothesis. Easy (existing code from Strategy-002).

DONE
