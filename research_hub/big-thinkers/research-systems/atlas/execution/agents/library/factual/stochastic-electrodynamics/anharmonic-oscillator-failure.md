---
topic: SED anharmonic oscillator failure
confidence: verified
date: 2026-03-27
source: "SED strategy-001 exploration-002 (Pesquera & Claverie 1982); numerically confirmed SED strategy-001 exploration-003"
---

## Key Results

Pesquera & Claverie (1982) proved perturbatively that SED disagrees with QM at O(beta^2) for the quartic anharmonic oscillator V(x) = 1/2 m omega_0^2 x^2 + beta x^4 via the full ALD radiation reaction equation.

**Numerically confirmed (exploration-003, 2026-03-27):** Direct Langevin simulation revealed failure that is actually O(beta) — one order earlier than P-C's analytical result — due to the Langevin approximation used in practice (see `anharmonic-langevin-o-beta-failure.md` for the approximation comparison). Qualitative trends are **opposite**: QM var_x decreases with beta (confinement); SED var_x increases with beta (destabilization). Already at beta=0.01, excess above baseline is 5.4 sigma.

## Three Independent Signatures of Failure (P-C 1982)

1. **Energy correction:** SED stationary mean energy agrees with QM at first order in beta but gives a **different coefficient at O(beta^2)**. QM ground-state energy: E_0 = 1/2 hbar omega_0 + 3/4 (hbar/m omega_0) beta - (21/8)(hbar/m omega_0)^2 beta^2 / hbar omega_0 + ... SED matches the first-order correction but diverges at second order.

2. **Absorption frequencies:** SED maximum absorption frequencies (via Kubo linear response) **do not coincide with QM transition frequencies** when beta != 0. QM has discrete transitions at omega_nm = (E_n - E_m)/hbar; SED absorption peaks shift differently with beta.

3. **Radiation balance:** The equilibrium radiation balance (energy absorbed from ZPF = energy emitted via radiation reaction) is **not exactly satisfied** when beta != 0. In QM this balance holds exactly at all orders; in SED it breaks, meaning the anharmonic oscillator does not reach true equilibrium with the ZPF.

## QM Reference Values (exact; matrix diagonalization N_max=80, convergence <2e-11)

| beta  | E_0 (exact)  | var_x_QM | <x^4>_QM | PE_QM    |
|-------|--------------|----------|----------|----------|
| 0.00  | 0.50000000   | 0.500000 | 0.750000 | 0.250000 |
| 0.01  | 0.50725620   | 0.486168 | 0.702927 | 0.250113 |
| 0.05  | 0.53264275   | 0.445822 | 0.578803 | 0.251851 |
| 0.10  | 0.55914633   | 0.412525 | 0.488737 | 0.255136 |
| 0.20  | 0.60240516   | 0.369964 | 0.387403 | 0.262462 |
| 0.50  | 0.69617582   | 0.305814 | 0.260241 | 0.283028 |
| 1.00  | 0.80377065   | 0.257150 | 0.182207 | 0.310782 |

QM trend: var_x DECREASES with beta. The quartic term confines the ground state.

## Numerical SED vs QM Comparison (Langevin simulation; 10,000 samples per beta)

| beta  | var_x_QM  | var_x_SED       | Frac diff | Adj. excess | Significance |
|-------|-----------|-----------------|-----------|-------------|--------------|
| 0.000 | 0.500000  | 0.5155 ± 0.0074 | +3.1%     | 0% baseline | 2.1 sigma    |
| 0.010 | 0.486168  | 0.5292 ± 0.0079 | +8.9%     | +5.8%       | **5.4 sigma**|
| 0.050 | 0.445822  | 0.6098 ± 0.0101 | +36.8%    | +33.7%      | **16.3 sigma**|
| 0.100 | 0.412525  | 0.7353 ± 0.0137 | +78.2%    | +75.2%      | **23.6 sigma**|
| 0.200 | 0.369964  | 1.0360 ± 0.0202 | +180.1%   | +177.0%     | **35.1 sigma**|
| 0.500 | 0.305814  | 1.6667 ± 0.0295 | +445.0%   | +442.0%     | **46.2 sigma**|
| 1.000 | 0.257150  | 2.4108 ± 0.0426 | +837.5%   | +834.4%     | **50.5 sigma**|

SED trend: var_x INCREASES with beta. Qualitatively opposite to QM. At beta=1, SED overestimates var_x by a factor of 9.4x.

## Distribution Shape

- beta=0: Both SED and QM produce Gaussian distributions (SED KS vs Gaussian: p=0.84). Agreement.
- beta=0.1: SED is super-Gaussian (excess kurtosis = 0.44); QM ground state is sub-Gaussian (quartic term squeezes tails). Qualitatively **opposite** shapes.

## Linearity Boundary (Quantified)

The linearity boundary (excess >2 sigma above baseline): 6*beta > 3% → beta > 0.005.
At beta=0.01, failure is already 5.4 sigma. At beta >= 0.05, failure is catastrophic (>16 sigma, var_x ratio >1.4x).

## Significance

- Demonstrates SED's success with the harmonic oscillator is **specific to linearity**
- Failure is not just quantitative — the trend direction is qualitatively opposite to QM
- P-C's analytical O(beta^2) result confirmed; Langevin approximation fails even harder at O(beta) — see `anharmonic-langevin-o-beta-failure.md`
- **UPDATE (exploration-004):** The O(beta) Langevin failure is an approximation artifact. Full ALD with Landau-Lifshitz order reduction **eliminates the O(beta) excess** for beta ≤ 0.1 (ALD error indistinguishable from beta=0 baseline). Residual β^0.40 failure emerges at beta > 0.2. P-C's O(beta^2) prediction for full ALD is approximately supported. See `anharmonic-ald-landau-lifshitz.md`.
- **UPDATE (exploration-005):** The β^0.40 residual is NOT a UV-cutoff artifact (parameter scan confirmed). Error scales as τ^0.23 × ω_max^(-0.18) — extremely slow convergence.
- **Significance correction (exploration-006 adversarial review):** The 5.4σ at β=0.01 correctly measures absolute SED-QM discrepancy. However, for the O(β) trend specifically, the baseline-adjusted significance is ~2.5σ (subtracting β=0 offset). At β ≥ 0.1, both measures agree: failure is >20σ regardless.

## References

- Pesquera, L. & Claverie, P. (1982). "The quartic anharmonic oscillator in stochastic electrodynamics." J. Math. Phys. 23(7), 1315-1322.
- Bender, C.M. & Wu, T.T. (1969). Anharmonic oscillator perturbation theory.
- SED strategy-001 exploration-003 (2026-03-27): direct numerical verification.
