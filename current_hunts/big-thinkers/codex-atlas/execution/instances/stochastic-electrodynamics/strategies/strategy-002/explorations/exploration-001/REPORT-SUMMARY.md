# Exploration 001 — Summary: SED Double-Well Barrier Crossing vs WKB

## Goal
First numerical simulation of SED barrier crossing in `V(x) = -½ω₀²x² + ¼λx⁴` using the ALD equation with colored ZPF noise. Compare SED barrier-crossing rate to exact QM tunneling rate.

## What Was Tried
Symplectic Euler integration of ALD for 100 trajectories × 200,000 steps at λ=0.25, 0.10, 1.0. Exact QM rates from Schrödinger equation finite-difference diagonalization. WKB action computed numerically. Prior art search conducted.

## Key Quantitative Result

**λ=0.25 (V_barrier=1.0, S_WKB=1.41):** Γ_SED = **0.0663 ± 0.0035 ω₀** vs Γ_exact = **0.0578 ω₀** → **Γ_SED/Γ_exact = 1.15** (15% agreement — remarkable).

**λ=0.10 (V_barrier=2.5, S_WKB=6.29):** Γ_SED = **0.00790 ± 0.00137 ω₀** vs Γ_exact = **0.000428 ω₀** → **Γ_SED/Γ_exact = 18.5** (18× overestimate).

**λ=1.0 (V_barrier=0.25):** QM ground state is above barrier (E₀ > V_barrier) — over-barrier regime. Γ_SED = 0.204 ω₀, no WKB comparison.

## Verification Scorecard
4 [COMPUTED], 1 [CHECKED], 2 [CONJECTURED]

## Key Takeaway
SED agrees with QM tunneling to 15% when S_WKB ≈ V_barrier/E_zpf (both ≈ 1.41 for λ=0.25). For larger barriers, SED overestimates by ~exp(S_WKB − V_barrier/E_zpf), giving 18× for λ=0.1. Particles never escape — they show stable tunneling-like oscillation for moderate barriers, incoherent bursts for deep barriers. The ALD double-well is numerically stable throughout.

## Novelty
**This is the first numerical SED simulation of double-well barrier crossing compared to QM.** Prior work (Faria & Franca 2005) was analytical only. Drummond (1989) found truncated Wigner (SED-equivalent) fails for tunneling — confirmed here for large barriers.

## Leads Worth Pursuing
1. Test crossover condition S_WKB = V_barrier/E_zpf with other potential shapes
2. Measure phase coherence of SED crossings vs QM Rabi oscillation
3. Add thermal noise: does Γ_SED(T)/Γ_WKB(T) converge at high T?

## Unexpected Findings
The 15% agreement at λ=0.25 is surprisingly good. No numerical instability from negative-V'' anti-damping at barrier top — the ALD is well-behaved throughout.
