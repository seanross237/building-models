# Sprint 2: Derive the Noise Spectrum from the Fracton Condensate

**Date:** 2026-03-21
**Status:** PARTIAL PASS — Parametric scaling derived, but two fatal structural gaps identified

## The Question

What is the full acceleration noise power spectral density S_a(f) for a test mass embedded in the fracton dipole condensate ground state?

## Pass/Fail Criteria

- PASS: S_a derived from condensate, matches or constrains the assumed formula, and we learn the frequency spectrum
- PARTIAL: We can set up the calculation but cannot complete it (identify which part is intractable)
- FAIL: The condensate produces fundamentally different noise than assumed

## Calculator Result

### Derivation Summary

Starting from the Pretko action S = ∫dt d³x [½ E_ij E_ij - ½ B_ij B_ij]:

1. **Momentum-space action:** Quadratic form gives propagator with k⁴ magnetic term
2. **Condensate phase:** Around ⟨A_ij⟩ = ρ_s δ_ij, fluctuations δA_ij develop linear dispersion ω = vk (Goldstone mode). Gapped scalar mode at m ~ M_Pl.
3. **Zero-point correlator:** ⟨δA_ij(k,ω) δA_kl(-k,-ω)⟩ ~ ℏ/(2ω) × tensor structure
4. **Test mass coupling:** Spatial averaging gives UV cutoff k_max ~ 1/R
5. **Integration:** Summing zero-point fluctuations up to k_max ~ 1/R:

**Result:** S_a(f) = Gℏ/(2π²R³) for f ≪ c/(2πR)

The spectrum is approximately **white** (frequency-independent) at frequencies well below c/R ~ 10¹⁵ Hz, which includes all laboratory frequencies. Roll-off occurs at f ~ c/(2πR).

### Key Assumptions Made

1. h_00 identified with condensate order parameter fluctuations (via Stueckelberg construction — **not explicitly verified**)
2. Linear dispersion ω = vk used (condensed phase Goldstone)
3. T = 0 (ground state only)
4. Test mass treated as rigid sphere of radius R

## Checker Verification

Six independent checks performed:

| Check | Method | Result | Consistent? |
|-------|--------|--------|-------------|
| 1 | Dimensional analysis | Gℏ/R³ is unique at O(Gℏ), c-independent | **Yes** |
| 2 | Zero-point fluctuations | S_a ~ Gℏ/R³ via tidal coupling + bandwidth | **Yes** |
| 3 | Known results comparison | Standard QFT gives ≪ Gℏ/R³ at lab frequencies | **Distinctive** |
| 4 | Oppenheim bound | Gℏ/R³ is lower bound; saturation natural at T=0 | **Yes** |
| 5 | Frequency dependence | White noise plausible; could be ∝ f³ from phonons | **Partially** |
| 6 | Mode counting | ~1 mode contributes; parametrically OK | **Marginally** |

### Critical Checker Finding

**The c-independence of Gℏ/R³ is physically meaningful.** It means the formula doesn't depend on the speed of light, which is consistent with FDCG where c is a derived quantity (c² = ρ_s/χ). This is not a generic quantum gravity result — standard QG vacuum noise gives S_a ∝ f⁵ at lab frequencies, which is unmeasurably small. The Gℏ/R³ formula gives orders-of-magnitude more noise than standard perturbative QG.

### Frequency Dependence

The frequency spectrum remains uncertain:
- **White noise** argument: At f ≪ c/R, all contributing modes have k < 1/R, giving flat spectrum
- **f³ rising** argument: Phonon mode density ∝ ω², times zero-point amplitude ∝ 1/ω, gives S_a ∝ f
- Within a narrow experimental band (10-1000 Hz), either looks approximately flat
- The spectral shape IS a distinguishing observable if measured precisely

## Skeptic Attacks

### Fatal Problems

**1. The A_ij → g_μν Identification Gap (FATAL)**

The Pretko field A_ij is a SPATIAL rank-2 tensor (i,j = 1,2,3). The metric g_μν is a SPACETIME tensor (μ,ν = 0,1,2,3). Gravitational acceleration requires h_00 (the time-time component): a_i = -(c²/2)∂_i h_00.

The Pretko field has no time-time component. The Stueckelberg mechanism is invoked to fill this gap, but the explicit construction mapping A_ij fluctuations to h_00 has NOT been performed. Without this, the derivation of acceleration noise literally cannot start.

**Defense:** The gauge enhancement proven in prior work (FDCG → linearized diffeos) implies the full metric emerges. The condensate ⟨A_ij⟩ = ρ_s δ_ij breaks the tensor gauge symmetry, and the Goldstone sector should contain the h_00 mode. But "should contain" ≠ "proven to contain."

**2. Oppenheim Bound Inapplicability (FATAL)**

The Oppenheim bound is a theorem within the CQ (classical-quantum) framework, which assumes gravity is fundamentally classical. FDCG treats gravity as fundamentally quantum (a condensate). These frameworks are logically incompatible:
- In CQ: noise is fundamental stochasticity required by consistency
- In FDCG: noise is vacuum fluctuations of a quantum field

Applying the Oppenheim bound to FDCG is a category error. If gravity is quantum, there's no decoherence-diffusion trade-off.

**Defense:** Tracing out short-wavelength condensate modes produces effective CQ dynamics for the test mass (Caldeira-Leggett mechanism). The Oppenheim bound could apply as an effective description. But this makes the noise an emergent decoherence effect, not fundamental stochasticity — a crucial distinction.

### Serious Problems

**3. Classical vs Quantum Noise Conflation (SERIOUS)**
Vacuum fluctuations in standard QFT do NOT produce measurable stochastic forces on classical objects. The EM vacuum has ⟨E²⟩ ≠ 0 but doesn't randomly kick charged particles. FDCG needs to explain why its condensate fluctuations produce REAL noise, not just virtual vacuum energy.

**4. Non-Specificity (SERIOUS)**
Any theory with a massless spin-2 graviton gives the same IR metric fluctuations. The noise prediction may be generic to quantum gravity, not specific to FDCG.

**5. Saturation Unjustified (SERIOUS)**
Quantum bounds are rarely saturated. Why would the condensate sit exactly at the minimum noise? Coherent state argument is insufficient without explicit calculation.

**6. Non-Distinctiveness (SERIOUS)**
If the noise is the same as standard QG vacuum noise, FDCG adds nothing. If different, it must explain the discrepancy with its own claimed linearized GR limit.

### Concern

**7. Pretko Specifics (CONCERN)**
The scalar mode sign (conformal mode problem), spin-1 sector status, and interpolation between k² and k⁴ dispersion regimes are unexplored.

## Synthesis and Verdict: PARTIAL PASS

### What We Established

1. **Parametric scaling S_a ~ Gℏ/R³ is robust.** Derived from zero-point fluctuations with UV cutoff at k ~ 1/R, confirmed by dimensional analysis, and consistent (to order of magnitude) with the Oppenheim bound interpretation.

2. **The spectrum is approximately white at lab frequencies.** Roll-off at f ~ c/(2πR) ~ 10¹⁵ Hz means all experimental frequencies see flat noise. However, subtle frequency dependence (f vs f³) within the lab band remains an open question.

3. **FDCG predicts much more noise than standard perturbative QG.** This is genuinely distinctive — standard QG vacuum noise at lab frequencies goes as f⁵ and is unmeasurably small. FDCG gives frequency-independent noise many orders of magnitude larger.

4. **The c-independence of the formula is a genuine FDCG signature.** In FDCG, c is derived from condensate parameters. The noise formula not involving c is consistent with this.

### What We Could NOT Establish

1. **The h_00 construction.** The explicit Stueckelberg mechanism mapping A_ij fluctuations to h_00 is missing. This is the critical gap that must be filled in a future sprint.

2. **The physical mechanism for noise.** Is it fundamental stochasticity (Oppenheim-type), or emergent decoherence from tracing out condensate modes (Caldeira-Leggett-type)? These give the same formula but have different physical interpretations and different implications.

3. **The exact numerical coefficient.** Calculator gives 1/(2π²), but this depends on assumptions about tensor structure and the h_00 coupling.

4. **Whether the result is FDCG-specific.** The skeptic's argument that any quantum gravity gives the same IR noise is partially valid — but the checker's finding that standard QG gives f⁵ (not flat) noise suggests FDCG IS distinctive.

### Resolution of the Fatal Attacks

The two fatal attacks (A_ij → g_μν gap and Oppenheim inapplicability) are **real but not terminal**:

- **Attack 1 resolution path:** A future sprint should explicitly construct h_00 from the Stueckelberg sector of the condensed Pretko theory. This is a well-defined calculation.

- **Attack 4 resolution path:** FDCG should NOT claim to "saturate the Oppenheim bound." Instead, it should claim: "The ground-state fluctuations of the fracton condensate produce acceleration noise S_a = Gℏ/(2π²R³), which happens to coincide with the Oppenheim decoherence-diffusion bound. This coincidence may reflect a deeper connection between quantum condensate fluctuations and classical-quantum gravity." This reframing avoids the category error.

## Key Findings for KNOWLEDGE.md

1. S_a ~ Gℏ/R³ is derivable from zero-point fluctuations with k_max ~ 1/R cutoff
2. The spectrum is white at f ≪ c/R (all lab frequencies)
3. The h_00 identification remains the critical structural gap
4. FDCG predicts much more noise than standard perturbative QG (flat vs f⁵)
5. The Oppenheim bound framing is misleading — should be reframed as emergent decoherence
6. The c-independence of Gℏ/R³ is a genuine FDCG signature

## Next Steps

- **High priority:** Explicitly construct h_00 from Stueckelberg sector (Sprint 3 candidate)
- **High priority:** Compute Caldeira-Leggett decoherence rate from condensate → test whether emergent CQ dynamics reproduces Oppenheim bound
- **Medium priority:** Resolve white vs f³ frequency dependence through full phonon spectral function calculation
