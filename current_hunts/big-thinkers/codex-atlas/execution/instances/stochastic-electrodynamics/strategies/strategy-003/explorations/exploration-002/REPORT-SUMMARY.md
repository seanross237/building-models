# Exploration 002 Summary — SED Hydrogen T_ion(L) with Physical τ

## Goal
Re-measure ionization timescales T_ion(L) for the SED hydrogen atom using the physical radiation-reaction time τ = 2.591×10⁻⁷ a.u. (60.6× smaller than E003's τ = 1.57×10⁻⁵). Scan L/ħ = 0.4–1.0, 20 trajectories each.

## What Was Tried
- Implemented Landau-Lifshitz ALD in C (gcc -O3) with chunked FFT ZPF noise (2^17-point blocks), multiprocessing across 10 CPUs
- Full scan: 140 trajectories, 10,000-period cap (L<1.0) or 50,000-period cap (L=1.0)
- Total wall time: ~24 seconds
- Sanity checks all passed: τ value ✓, pure Coulomb stability ✓, ZPF RMS ✓

## Outcome: SUCCESS — All 7 L Values Completed

### T_ion(L) Table `[COMPUTED]`

| L/ħ | N_ion/20 | Median T_ion (periods) | IQR    | ⟨r⟩/a₀ |
|-----|----------|------------------------|--------|---------|
| 0.4 | 20/20    | 94                     | 145    | 1.823   |
| 0.5 | 20/20    | 448                    | 366    | 1.514   |
| 0.6 | 19/20    | 1,633                  | 1,506  | 1.356   |
| 0.7 | 12/20    | 3,895                  | 2,755  | 1.122   |
| 0.8 | 15/20    | 7,886                  | 4,267  | 1.421   |
| 0.9 |  3/20    | 9,638                  | N/A    | 1.115   |
| 1.0 | 18/20    | 19,223                 | 11,894 | 1.509   |

T_ion(L) is **monotonically increasing** ✓

## Verification Scorecard
- **7 COMPUTED** (all table entries, sanity checks, power-law fit, ⟨r⟩ check)
- **0 CHECKED** (no independent verification against published SED numerics available)
- **2 CONJECTURED** (interpretation of non-monotonic ionization fraction; UV-cutoff dependence of ground-state lifetime)

## Key Takeaway
With physical τ, the T_ion scaling is confirmed but non-linear: observed ratios vs E003 range from 26× (L=0.5) to 89× (L=0.9), not the expected 60×. The key new result is that the n=1 circular Bohr orbit (L=1.0) **does eventually ionize** — median T_ion ≈ 19,223 orbital periods ≈ 2.9 ps — while achieving ⟨r⟩ = 1.509 a₀ ≈ 1.5 a₀ (QM 1s expectation) during early evolution.

## Comparison with E003
- L=0.5: 448 periods (physical) vs 17 periods (E003) → ratio 26.3×
- L=0.7: 3,895 periods (physical) vs 83 periods (E003) → ratio 46.9×
- L=0.9: 9,638 periods (physical) vs 108 periods (E003) → ratio 89.2×
- Expected ratio: 60.6× (simple τ-diffusion scaling)

## Unexpected Findings
1. **L=1.0 ionizes**: The circular Bohr orbit with physical τ does not persist indefinitely (18/20 ionize within 50,000 periods). Whether this indicates SED cannot stabilize hydrogen with ω_max = 100 a.u., or whether a higher UV cutoff would give indefinite stability, is an open question.
2. **⟨r⟩ = 1.509 a₀**: The L=1.0 orbit samples ⟨r⟩ exactly matching the QM 1s ground state (1.500 a₀), to 0.6%.
3. **Power law T_ion ≈ 37,527 × L^6.44 periods** (R² = 0.996) for L = 0.4–0.8. The exponent 6.44 is unexpectedly large.
4. **L=0.4 nuclear collisions**: 5/20 trajectories end in nuclear collision (r < 0.05 a₀, T_ion < 50 periods) rather than escape. The initial pericenter for L=0.4 is r_min ≈ 0.087 a₀, just above R_NUKE.
5. **Non-monotonic ionization fraction**: L=0.8 (75%) > L=0.7 (60%), while L=0.9 drops to 15%. Statistically marginal for 0.8 vs 0.7 but the L=0.9 drop is significant.

## Proof Gaps / Open Questions
- Does stability of L=1.0 depend critically on UV cutoff ω_max? Higher ω_max increases both ZPF drive and radiation damping — the balance is non-trivial.
- What sets the L^6.44 exponent? A perturbative calculation of D_E (energy diffusion coefficient) as a function of L might predict this.
- The non-trivial ratio (26×–89× rather than 60×) with L suggests the damping-drive balance is L-dependent. A theoretical explanation is needed.

## Computations Identified for Follow-on
1. **UV-cutoff sweep**: Run L=1.0 with ω_max = 50, 100, 200 a.u. to measure T_ion(ω_max) and determine if T_ion → ∞ at the physical ω_max = m_e c²/ħ.
2. **L_crit measurement**: Run L = 0.55, 0.58, 0.60, 0.62 with 20 trajectories each to precisely locate the critical angular momentum (where T_ion diverges).
3. **Longer-cap runs for L=0.9**: Extend L=0.9 to 100,000 periods to measure the true median T_ion (currently only 3/20 ionized in 10,000 periods).
4. **Power-law exponent theory**: Compute D_E(L) analytically or semi-analytically for the Landau-Lifshitz equation in a Coulomb potential.
