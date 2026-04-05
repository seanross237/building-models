---
topic: Numerical lattice results for pure Yang-Mills theory
confidence: verified
date: 2026-03-27
source: "yang-mills strategy-001 exploration-004; Morningstar-Peardon 1999, Athenodorou-Teper 2021, Berg-Billoire 2015, Borsanyi et al. 2012, Luscher 2010"
---

## Overview

50 years of lattice Monte Carlo simulations have established an extraordinary body of numerical evidence for pure Yang-Mills properties. None constitute rigorous proofs — they are numerical experiments of extremely high quality. These benchmarks define what any rigorous construction must reproduce.

## Confinement and String Tension

Wilson loop expectation: ⟨W(R,T)⟩ ~ exp(-σ R T) for large R, T, where σ is the string tension.

- **SU(3):** √σ ≈ 420–440 MeV (one of the most precisely determined lattice quantities)
- **SU(2):** √σ ≈ 440 MeV (in appropriate physical units)
- **Large-N:** Athenodorou-Teper (2021, arXiv:2106.00364) confirmed Casimir scaling σ/g² ∝ N for N = 2,...,12, consistent with 't Hooft scaling

Extraction methods: Creutz ratios, Polyakov loop correlators, static quark potential V(R) ≈ σR + const − π/(12R) (Luscher term). Multi-level algorithm of Luscher-Weisz dramatically improved large-loop accuracy.

**Rigorous status: NUMERICAL ONLY.** Area law proved rigorously only at strong coupling (Osterwalder-Seiler 1978) and for finite gauge groups at weak coupling (Chatterjee 2020, Adhikari-Cao 2025). Not proved for continuous compact groups at weak coupling in 4D.

## Mass Gap and Glueball Spectrum

Glueball masses extracted from exponential decay of Euclidean correlators: ⟨O(t) O(0)⟩ ~ exp(-m₀ t).

**SU(3) glueball spectrum (quenched):**

| State (J^PC) | Mass (MeV) | Reference |
|:---|:---|:---|
| 0++ (scalar) | 1730 ± 80 | Morningstar-Peardon (1999) |
| 2++ (tensor) | 2400 ± 120 | Morningstar-Peardon (1999) |
| 0−+ (pseudoscalar) | 2590 ± 130 | Morningstar-Peardon (1999) |

Alternative: Bali et al. (1999) give m(0++) = 1648 ± 58 MeV, m(2++) = 2267 ± 104 MeV. Athenodorou-Teper (2021) extend to SU(N) with N up to 12, confirming large-N scaling.

**The mass gap itself:** m(0++) ≈ 1.7 GeV defines Δ > 0. Proving Δ > 0 rigorously is the core of the Millennium Prize Problem.

**Rigorous status: NUMERICAL ONLY.** No rigorous proof that m₀ > 0 for SU(2) or SU(3) in 4D.

## Asymptotic Scaling

Perturbative β-function predicts: a Λ_L = (β₀ g₀²)^{-β₁/(2β₀²)} exp(-1/(2β₀ g₀²)) × [1 + O(g₀²)]

where β₀ = 11N/(48π²), β₁ = 34N²/(3(16π²)²) for SU(N).

Berg-Billoire (2015, arXiv:1507.05555) tested SU(3) across β = 5.7 to 7.5, finding dimensionless ratios "well described by a power series of aΛ_L" using 2-3 loop approximations. Modern simulations work at a ≈ 0.04–0.12 fm, well within the asymptotic scaling window.

**Rigorous status: NUMERICAL ONLY.** Perturbative AF established (Gross-Wilczek, Politzer 1973), but the non-perturbative statement is unproved. Balaban's bounds are consistent but don't prove uniqueness.

## Universality Across Lattice Actions

Different discretizations (Wilson, Symanzik, Iwasaki, DBW2) give the same continuum physics after extrapolation. Gradient flow scales (w₀) agree at the per-mille level across different fermion actions (Borsanyi et al. 2012). PDG Lattice QCD Review (2024): "All actions lead to the same continuum theory."

Universality is the primary evidence that a unique continuum theory exists. It would be "miraculous" if different discretizations converged to the same answers without an underlying continuum limit.

**Rigorous status: NUMERICAL ONLY.** No proof for 4D. Trivially established in 2D (exactly solvable).

## Deconfinement Transition

At finite temperature T = 1/(N_t a), pure gauge theory undergoes a phase transition (Polyakov loop order parameter):

- **SU(3):** T_c ≈ 270 MeV (first-order transition)
- **SU(2):** T_c ≈ 300 MeV (second-order, Ising universality class)
- Dimensionless ratio: T_c/√σ ≈ 0.63 for SU(3)

**Rigorous status: PARTIALLY.** Borgs-Seiler (1983) proved deconfinement at high T for SU(2); full quantitative picture is numerical.

## Continuum Limit Procedure (How Practitioners Do It)

1. Compute observable Q̂(β) = a(β) × Q_phys at several values of β = 2N/g₀²
2. Set scale using a reference quantity (r₀ ≈ 0.5 fm from static potential, or gradient flow scales w₀, t₀)
3. Extrapolate dimensionless ratios to a → 0, fitting a² (or a⁴ for improved actions)

Scale setting: r₀ (Sommer parameter), w₀/t₀ (gradient flow, Luscher 2010 — computationally cheap, sub-percent precision), √σ (traditional).

Systematic errors controlled by simulations at 3–5 lattice spacings with continuum extrapolation: Q = Q_cont + c₁ a² + c₂ a⁴ + ...

**The entire procedure rests on the unproven assumption that a continuum limit exists and is unique.** Numerical results are consistent with this assumption to extraordinary precision.

## Atlas SU(2) Verification (Exploration 003)

An independent from-scratch SU(2) Wilson lattice gauge theory simulation (Kennedy-Pendleton heat bath, quaternion representation) on 4⁴-8⁴ lattices at β = 2.0-3.0 reproduced known results:

- **Plaquette values:** Match literature within 1-2σ (e.g., ⟨P⟩ = 0.5687(4) at β=2.2, L=8 vs. literature 0.5688)
- **Confinement:** Area law for Wilson loops with R² > 0.996 at all β; string tension σ = 0.13-0.59 lattice units
- **Polyakov loop:** Consistent with zero at L ≥ 6, confirming confinement
- **Creutz ratios:** Robustly positive, L=6 and L=8 mutually consistent

### Practical Lattice Size Requirements

| Observable | Minimum lattice | Notes |
|:---|:---|:---|
| Average plaquette | 4⁴ | Minimal finite-size effects; UV observable |
| Wilson loops / Creutz ratios | 6⁴-8⁴ | Adequate for basic area law and string tension |
| Glueball mass (0++) | ≥16⁴ | Direct plaquette correlator fails at L ≤ 8 (signal-to-noise ~ exp(-m₀) at t=1); requires smeared/variational operators (APE, GEVP), O(10⁵-10⁶) configurations |
| Asymptotic scaling (SU(2)) | ≥16⁴, β ≥ 2.4 | Physical string tension varies by factor ~50 across β = 2.0-3.0 on L ≤ 8; not yet in scaling window |

The glueball mass extraction failure on small lattices is itself informative: it is consistent with a LARGE mass gap (m₀ ~ 2 lattice units >> 1/L). Phenomenological estimate m₀ ≈ 4√σ ≈ 1.8-2.5 lattice units, consistent with known ratio m₀/√σ ≈ 3.5-4.5 for SU(2).
