---
topic: emergent-gravity
confidence: verified
date: 2026-03-24
source: exploration-002-bianconi-entropic-action-assessment (strategy-002)
---

# Bianconi's "Gravity from Entropy" — Critical Assessment

## Paper Identity

- **Title:** "Gravity from entropy"
- **Author:** Ginestra Bianconi (Queen Mary University of London)
- **Published:** Physical Review D, Vol. 111, Article 066001 (March 2025)
- **arXiv:** 2408.14391 (v2)
- **DOI:** 10.1103/PhysRevD.111.066001

**Author background:** Professor of Applied Mathematics specializing in network science and complex systems — not primarily a QG researcher. Expertise in statistical mechanics of networks, algebraic topology of complex systems. This explains both the novel angle and the missing standard QG checks.

## Core Proposal

The gravitational action IS the quantum relative entropy S(ρ_metric || ρ_matter) between the spacetime metric and the metric induced by matter fields. Concretely:

- The metric tensor g_μν is reinterpreted as a "renormalizable effective density matrix"
- Matter fields are packaged as differential forms via the Dirac-Kähler formalism: |Φ⟩ = φ ⊕ ω_μ dx^μ ⊕ ζ_μν dx^μ ∧ dx^ν
- Two "topological metrics": g̃ (spacetime) and G̃ = g̃ + αM̃ − βR̃ (matter-induced)
- Lagrangian: ℒ = −Tr ln(G̃ g̃⁻¹), Action: S = (1/ℓ_P^d) ∫ √|−g| ℒ d^d x

**Critical observation:** The induced metric G̃ is **prescribed phenomenologically** (designed by hand to reproduce GR + scalar field at low coupling), NOT derived from first principles.

## Novelty Assessment

**Genuinely novel in form.** No one has previously proposed quantum relative entropy between two metrics as the gravitational action. The use of Dirac-Kähler formalism and treatment of metrics as density matrices is original.

**However, the novelty is in the packaging, not the output.** The theory is engineered to reproduce GR + scalar field in the low-coupling limit. Key comparisons:

| Program | Mechanism | Output |
|---------|-----------|--------|
| Jacobson (1995) | δQ = TdS at Rindler horizons | Einstein eqs (derivation) |
| Jacobson (2015) | Maximal vacuum entanglement | Einstein eqs (derivation) |
| Verlinde (2010) | Entropic force from holographic screens | Newton's law, MOND-like |
| Padmanabhan | TdS = dE + PdV on horizons | Einstein eqs + Λ |
| Sakharov (1967) | One-loop effective action | Einstein-Hilbert (Λ too large) |
| **Bianconi (2025)** | **Relative entropy as action** | **GR + scalar (by construction)** |

**Key difference from all above:** Bianconi gives a concrete, new action principle to vary — not just a derivation technique. But the action is constructed to give GR at low coupling.

## Tier 1 Validation: FAILS

| Check | Status | Details |
|-------|--------|---------|
| Spin-2 graviton | ❌ Not demonstrated | No linearization or propagator analysis |
| Unitarity | ❌ Not addressed | No quantum formulation exists |
| Ghost freedom | ⚠️ Serious concern | Fourth-order equations (B^μν tensor), no Ostrogradsky analysis |
| UV completion | ❌ No | Entirely classical, no quantum corrections |
| Diffeo invariance | ✅ Formally present | But no gauge-fixing or BRST analysis |
| Weinberg-Witten | ⚠️ Unclear | Likely evadable via GR limit, but not checked |

**Most dangerous issue:** The full modified Einstein equations (Eq. 45) contain fourth-order derivatives through the B^μν tensor. By the Ostrogradsky theorem, this generically produces a massive spin-2 ghost (as in Stelle's quadratic gravity). The G-field is claimed to reduce equations to second order, but the G-field's own degrees of freedom are unanalyzed for ghostliness.

**The theory is entirely classical.** Author explicitly states "canonical quantization could bring new insights" — acknowledging quantization is future work. Calling the metric a "renormalizable effective density matrix" is a naming convention, not a demonstration of renormalizability.

## Tier 2: Known Physics Recovery (Partial)

- **Newton's law:** ✅ In low-coupling limit (because it reduces to GR)
- **GR reduction:** ✅ By construction: ℒ ≈ 3βR − α|∇φ|² − α(m² + ξR)|φ|²
- **PPN parameters:** ❌ Not computed
- **GW speed:** ❌ Not computed

## Predictive Claims Assessment

### Emergent Cosmological Constant — MOSTLY EMPTY
Λ is parameterized through the G-field, not predicted. The VALUE of Λ_G depends on the G-field configuration, which is itself undetermined. Not a solution to the CC problem — just moves the parameter.

### G-Field as Dark Matter — PURELY SPECULATIVE
No mass, no SM coupling, no production mechanism, no density profiles, no rotation curves. The G-field is an auxiliary (Lagrangian multiplier) — generically non-dynamical without additional mechanism.

### Inflationary Predictions (arXiv: 2509.23987) — MOST INTERESTING BUT CAVEATED

| Observable | Bianconi | QG+F | Planck |
|-----------|----------|------|--------|
| n_s | 0.962–0.964 | ~0.967 | 0.9649 ± 0.0042 |
| r | 0.010–0.012 | 0.0004–0.0035 | < 0.036 |

Inflation without inflaton from the entropic action's nonlinear structure. Both n_s and r are within current bounds and testable by Simons Observatory / CMB-S4. However: perturbation theory is incomplete, the high-entropy regime where inflation occurs is where the low-coupling approximation breaks down, and no stability/ghost analysis exists for this regime.

### Black Hole Entropy — ENCOURAGING BUT CIRCULAR
Gets S ∝ A/(4G) for Schwarzschild at large radii, but: Schwarzschild is only an approximate solution (low-coupling limit), proportionality constant involves free parameters, and a correction/erratum was needed.

## Follow-Up Papers (all by Bianconi)

1. **BH entropy** (arXiv: 2501.09491, Entropy 27(3), 266, 2025) — area law at large radii; erratum published
2. **Anisotropic diffusion** (arXiv: 2503.14048) — Perona-Malik from GfE in 2D Euclidean; not relevant to QG
3. **Inflation from entropy** (arXiv: 2509.23987) — modified Friedmann equations, geometric inflation, n_s and r predictions
4. **Thermodynamics of GfE** (arXiv: 2510.22545) — thermodynamic aspects

**Community response:** Minimal. Only known external citation is an unpublished preprint by J. O. Obidi. No engagement from Jacobson, Verlinde, Padmanabhan, or the QG community apparent.

## Overall Verdict: NOT VIABLE — MOVE ON

This is a classical modified gravity theory, not a quantum gravity theory. The fatal flaws:
1. **Not quantum** — no Hilbert space, no S-matrix, no quantization
2. **Fourth-order equations → probable ghosts** — potentially fatal even classically
3. **Phenomenological construction** — G̃ is built by hand to give GR, undermining the "emergence" claim
4. **Incomplete matter sector** — only scalar/topological bosonic fields; no fermions or gauge fields

**Worth remembering:** The idea of gravitational action = quantum relative entropy could be powerful if implemented within a properly quantized framework (e.g., as a UV completion mechanism within asymptotic safety). The inflationary predictions (r ∈ [0.010, 0.012]) are worth tracking against CMB-S4 data.

## Generalizable Lessons

Bianconi's failure mode is shared by the entire entropic gravity program (Jacobson, Verlinde, Padmanabhan): all derive classical Einstein equations from thermodynamic/information arguments but none provides UV completion. The hard problem of QG is not "how to derive Einstein's equations" — it's "how to quantize them consistently." Classical information theory is necessary but not sufficient.

Sources:
- Phys. Rev. D 111, 066001 (2025) — arXiv: 2408.14391
- arXiv: 2501.09491, 2503.14048, 2509.23987, 2510.22545
- Erratum: Entropy 27(7), 724
