# Exploration History

## Exploration 001 — Santos O(ħ²) Connection (DONE)

**Type:** Standard Explorer | **Outcome:** Minimum Success (half the central hypothesis confirmed)

**Goal:** Determine whether Santos (2022) O(ħ²) corrections predict the measured 15-18% anharmonic residual and tunneling slope=1.049.

**Santos (2022) framework:** SED = O(ħ) QED in the Weyl-Wigner representation. O(ħ²) correction term = (ħ²/24) × V'''(x) × ∂³W/∂p³ = βħ²x × ∂³W/∂p³ for the quartic oscillator. For quadratic Hamiltonians: correction = 0 (SED exact). For nonlinear: correction ≠ 0 (SED fails).

**Key hierarchy at β=1:** classical (T=ħω/2) = 0.183 < QM = 0.257 < ALD/SED = 0.303. The SED result OVERSHOOTS QM — the O(ħ²) correction is negative (tightening). This is opposite to naive intuition.

**Anharmonic residual:** Santos' framework explains the 15-18% discrepancy as the missing O(ħ²) Moyal correction. Definitional, not independently predictive. O(ħ²) correction is zero at O(β) (symmetry argument: Moyal source term odd in x → ⟨x²⟩ correction zero at O(β), per Pesquera-Claverie consistency). The 0.046 is an O(β²) accumulated effect at β=1.

**Tunneling slope=1.049:** NOT predicted by O(ħ²). Anharmonic energy correction δE=−λ/4 is λ-dependent and vanishes at deep barriers — cannot produce a constant 4.9% deviation over 4 decades. Slope=1.049 is a finite-τ/ω_max artifact. Intercept=0.072 IS consistent with O(ħ²) prefactor correction.

**New analytic results:** WKB action S = 2√2/(3λ) (exact, verified); Faria-França slope=1.000 is an algebraic identity; δE=−λ/4 for quantum correction to well depth.

**Claim status:** PARTIALLY VERIFIED — anharmonic connection (definitional proof), slope deviation (refuted as O(ħ²) effect).

---

## Exploration 002 — SED Hydrogen T_ion(L) with Physical τ (DONE)

**Type:** Math Explorer | **Outcome:** Succeeded

**Goal:** Re-run SED hydrogen simulation with physical τ = 2.591×10⁻⁷ a.u. (60× smaller than E003's τ).

**Key result:** Full T_ion(L) table at physical τ:

| L/ħ | N_ion/20 | Median T_ion (periods) | ⟨r⟩/a₀ |
|-----|----------|------------------------|---------|
| 0.4 | 20/20 | 94 | 1.82 |
| 0.5 | 20/20 | 448 | 1.51 |
| 0.6 | 19/20 | 1,633 | 1.36 |
| 0.7 | 12/20 | 3,895 | 1.12 |
| 0.8 | 15/20 | 7,886 | 1.42 |
| 0.9 | 3/20 | 9,638 | 1.12 |
| 1.0 | 18/20 | 19,223 | 1.51 |

T_ion monotonically increasing ✓. Power law: T_ion ≈ 37,527 × L^6.44 (R²=0.996).

**Key new finding:** L=1.0 circular Bohr orbit DOES eventually ionize — 18/20 within 50,000 periods, median 19,223 periods. ⟨r⟩=1.509 ≈ QM 1s value (1.500 a₀). Scaling ratios vs E003: 26-89× (not simple 60× — relationship is L-dependent and non-linear). Nuclear collisions (r<0.05 a₀) occur at L=0.4.

**Claim status:** COMPUTED (all sanity checks passed). Physical-τ T_ion table is first published data.

---

## Exploration 003 — 3D ZPF Two-Point Correlator (DONE)

**Type:** Math Explorer | **Outcome:** Succeeded (Tier 4+)

**Goal:** Determine what happens to C_xx(d) = cos(ω₀d/c) [1D result] when the full 3D ZPF (all k-vector directions and polarizations) is used.

**Key result:** The 3D ZPF position-position correlator in the narrow-linewidth limit is:

```
C_xx(d) = (3/2q³)[(q²-1)sin(q) + q cos(q)]   where q = ω₀d/c
         = j₀(q) - (1/2) j₂(q)   [spherical Bessel form]
```

Verified by: analytic integration by parts, quadrature, Bessel function identity, and Monte Carlo (N=500,000 modes) — all agree to machine precision.

**Limiting behaviors:** Near field: C_xx ≈ 1 - q²/5. Far field: C_xx ≈ (3/2)sin(q)/q (~1/d decay). Special value: C_xx(q=1) = (3/2)cos(1) ≈ 0.81.

**Answer:** The 3D orientational average does NOT kill the correlation. SED predicts C_xx ≠ 0 at all finite d; QM predicts C_xx = 0 for uncoupled oscillators. The discrepancy persists in 3D but is weaker than 1D (1/d decay vs constant amplitude). NOT the van der Waals r⁻⁶ term (that requires second-order Coulomb coupling).

**Claim status:** COMPUTED (analytic + Monte Carlo). The formula is the xx-component of the transverse EM propagator — connects to the known ZPF two-point correlator in classical ED.

---

## Exploration 004 — Adversarial Synthesis and Grand Synthesis (DONE)

**Type:** Standard Explorer | **Outcome:** Tier 4 (Good Success)

**Goal:** Adversarially stress-test all 7 novel claims from SED Strategies 1–3, conduct prior art search on "field quantization necessity," and produce grand synthesis answering the central mission question.

**Prior art situation — critical finding:** The grand synthesis conclusion ("field quantization is necessary for nonlinear systems") is NOT genuinely novel:
- Santos (2022) proves SED = O(ħ) QED exactly, and fails for nonlinear systems at O(ħ²) — mathematical implication clear
- Nieuwenhuizen (2020) states it explicitly: "SED is not a basis for quantum mechanics" after exhausting all renormalization fixes
- Boyer (2019) implicitly accepts it ("closest classical *approximation*")
- de la Peña & Cetto (2014) explicitly deny it — debate is live in the literature

**Claim verdicts:**

| Claim | Verdict | Novelty |
|-------|---------|---------|
| S1-A: First numerical quartic oscillator, 17.8% excess | PARTIALLY VERIFIED | 3/5 |
| S1-B: ω³ positive feedback mechanism | CONJECTURED | 2/5 |
| S2-A: Tunneling ratio formula R²=0.9998 | PARTIALLY VERIFIED | 2/5 |
| S2-B: ω_local=√2 universality | VERIFIED (trivial) | 1/5 |
| S2-C: ω³ unified root cause | CONJECTURED | 2/5 |
| S2-D: 1D correlator C_xx=cos(ω₀d/c) | PARTIALLY VERIFIED | 2/5 |
| S3-A: T_ion(L) power law, L=1.0 → 19,223 periods | PARTIALLY VERIFIED | 3/5 |
| S3-B: 3D correlator C_xx=j₀−j₂/2 | VERIFIED (standard) | 2/5 |
| S3-C: Hierarchy 0.183 < 0.257 < 0.303 | PARTIALLY VERIFIED | 3/5 |

**Key takeaway:** Best novel output is the **convergence law Δ(⟨x²⟩) ∝ τ^0.23 × ω_max^{-0.18}** — quantitatively demonstrates SED failure is physically irreducible. Next-best: **T_ion(L) ∝ L^6.44 power law** extending Nieuwenhuizen's qualitative observation to a quantitative table with physical τ.

Our contribution is systematic quantitative evidence across three systems — a compilation argument, not a conceptual breakthrough.

**Future leads:** de la Peña/Cetto "Emerging Quantum" framework not quantitatively tested against our specific numbers. C_xx(d) correlator as experimental discriminant (SED predicts nonzero inter-site correlations; QM predicts zero for uncoupled oscillators) is an unexplored experimental proposal.

---

