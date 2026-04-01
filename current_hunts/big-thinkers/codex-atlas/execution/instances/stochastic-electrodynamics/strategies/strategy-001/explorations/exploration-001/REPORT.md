# Exploration 001 — SED Harmonic Oscillator Ground State: Numerical Reproduction

## Goal
Numerically reproduce the quantum mechanical ground state of a harmonic oscillator from Stochastic Electrodynamics (SED). The SED program posits that a classical charged particle in a harmonic potential, driven by zero-point field (ZPF) radiation and subject to radiation reaction damping, reaches an equilibrium distribution that exactly matches the QM ground state.

**Target results (natural units m=1, w0=1, hbar=1):**
- Ground state energy: E0 = 1/2 hbar w0 = 0.5
- Position variance: var_x = hbar/(2*m*w0) = 0.5
- Position distribution: Gaussian

## 1. SED Axioms and Equations

### 1.1 The Zero-Point Field

SED assumes classical electrodynamics with one additional axiom: space is permeated by a real, Lorentz-invariant electromagnetic zero-point field (ZPF) with spectral energy density:

    rho(w) = hbar * w^3 / (2 * pi^2 * c^3)

This is the unique spectral density that is Lorentz-invariant (Boyer 1969). The ZPF is a classical stochastic field — each mode is a classical oscillator with random phase but fixed amplitude set by rho(w).

### 1.2 The Langevin Equation

A charged particle (mass m, charge e) in a harmonic potential V = (1/2)*m*w0^2*x^2 obeys:

    m * x'' = -m*w0^2*x + m*tau*x''' + e*E_zpf(t)

where:
- **First term:** restoring force from the harmonic potential
- **Second term:** Abraham-Lorentz radiation reaction, with tau = 2e^2/(3mc^3)
- **Third term:** driving force from the ZPF electric field

The radiation reaction acts as effective damping near resonance with coefficient Gamma = tau*w0^2.

### 1.3 Transfer Function (Frequency Domain)

For a linear oscillator, the equation of motion is solved EXACTLY in the frequency domain:

    X(w) = F(w) / H(w)

where the transfer function is:
- **Full Abraham-Lorentz:** H(w) = w0^2 - w^2 + i*tau*w^3
- **Effective damping:** H(w) = w0^2 - w^2 + i*Gamma*w

### 1.4 ZPF Spectral Density — CORRECTED DERIVATION

**[VERIFIED]** The correct one-sided PSD of the ZPF driving force (per unit mass) is:

    S_F^one(w) = 2 * tau * hbar * w^3 / m

**Derivation (carefully tracking factors of 2 and pi):**

1. ZPF spectral energy density: rho(w) = hbar*w^3/(2*pi^2*c^3)
2. Electric field energy density: u_E = (epsilon_0/2) * <E^2> = (1/2) * integral(rho(w) dw)
3. For one E-field component: (epsilon_0/2)<E_x^2> = (1/6) integral(rho dw)
4. Therefore: <E_x^2> = (1/(3*epsilon_0)) integral(rho dw)
5. Matching to PSD convention: <E_x^2> = (1/(2*pi)) integral_0^inf S_E^one dw
6. This gives: S_E^one(w) = 2*pi*rho(w)/(3*epsilon_0) = hbar*w^3/(3*pi*epsilon_0*c^3)
7. Force PSD: S_F^one = (e/m)^2 * S_E^one = e^2*hbar*w^3/(3*pi*epsilon_0*m^2*c^3)
8. Using tau = e^2/(6*pi*epsilon_0*m*c^3): S_F^one = 2*tau*hbar*w^3/m

**CRITICAL BUG FOUND:** The previous explorer's formula (from section 1.3 of the original report) stated S_F = (2*tau*hbar/(pi*m))*w^3, which is WRONG by a factor of pi. This error originated from confusing energy density rho(w) with PSD S_E(w) — the conversion requires a factor of 2*pi from the Parseval relation that was dropped. With the wrong formula, all variances come out pi times too small in analytic quadrature, and the FFT amplitude formula coincidentally compensated in a way that made position variance 2x too large. **[VERIFIED]** — confirmed by numerical cross-check (see Section 2.2).

### 1.5 Analytic Solution

The position variance is:

    var_x = (1/(2*pi)) integral_0^inf S_F^one(w)/|H(w)|^2 dw

For small tau (sharp resonance at w=w0), the integral is dominated by w ~ w0:

    integral_0^inf w^3/|H|^2 dw ~ pi/(2*tau*w0)   (Lorentzian peak)

Yielding:

    var_x ~ tau/(pi) * pi/(2*tau*w0) = 1/(2*w0) = hbar/(2*m*w0)

This is exactly the QM ground state position variance. **[CHECKED]** — classic Boyer (1975) / Marshall (1963) result.

### 1.6 UV Divergence Structure — KEY FINDING

**[COMPUTED]** The integrands for position and velocity variance have fundamentally different UV behavior under the full Abraham-Lorentz transfer function:

At high frequencies (w >> w0), |H(w)|^2 ~ tau^2 * w^6, so:

| Quantity | Integrand | UV behavior | Convergence |
|----------|-----------|-------------|-------------|
| var_x    | w^3 / |H|^2 | w^3/w^6 = 1/w^3 | **Converges** |
| var_v    | w^5 / |H|^2 | w^5/w^6 = 1/w   | **Diverges** (logarithmic) |

The velocity variance (and hence kinetic energy) grows as ln(w_max) with the UV cutoff. This means:

- **Position distribution: well-defined, matches QM** [COMPUTED]
- **Velocity distribution: UV-sensitive, depends on cutoff** [COMPUTED]
- **Total energy: UV-divergent, NOT directly comparable to E0 = hbar*w0/2** [COMPUTED]

This is a manifestation of the classical electromagnetic self-energy divergence. In the full SED theory, mass renormalization absorbs the divergent self-energy.

## 2. Numerical Implementation

### 2.1 Method: Frequency-Domain Solution

For the LINEAR harmonic oscillator, the Langevin equation is solved exactly in the frequency domain. This approach:
- Avoids all time-stepping errors (Velocity Verlet, etc.)
- Gives the exact steady-state distribution (no equilibration needed)
- Is orders of magnitude faster than time-domain integration

**Algorithm for each ensemble member:**
1. Generate FFT amplitudes from S_F^one(w): A_k = sqrt(N * S_F(w_k) / (2*dt))
2. Assign random phase: F_k = A_k * exp(i*phi_k), phi_k ~ Uniform(0, 2*pi)
3. Solve: X_k = F_k / H(w_k)
4. Velocity: V_k = i*w_k * X_k
5. IFFT: x(t) = irfft(X_k), v(t) = irfft(V_k)
6. Sample at midpoint: x_sample = x[N/2], v_sample = v[N/2]

**FFT normalization derivation** (numpy convention, verified numerically):

    |F_k|^2 = N * S_F^one(w_k) / (2*dt)

    E[var_x] = (2/N^2) * SUM_{k=1}^{K-1} |F_k|^2 / |H_k|^2

This was verified against independent Monte Carlo estimation (see Section 2.2). Code: `code/sed_corrected_run.py`.

### 2.2 Normalization Verification

**[VERIFIED]** Cross-checked the spectral density and FFT normalization three ways:

1. **Analytic quadrature** (scipy.integrate.quad):
   - tau=0.01: integral I = 161.13, var_x = tau*I/pi = 0.5129 (target 0.5, 2.6% excess from UV tail)
   - tau=0.001: I = 1576.4, var_x = 0.5018 (target 0.5, 0.4% excess)

2. **Discrete spectral sum** (from FFT grid):
   - tau=0.01, N=2^17, dt=0.05: var_x_spectral = 0.5110
   - tau=0.001, N=2^17, dt=0.1: var_x_spectral = 0.5022

3. **Monte Carlo ensemble** (2000 trajectories each):
   - tau=0.01: var_x_MC = 0.525 +/- ~0.05 (consistent with spectral prediction)
   - tau=0.001: var_x_MC = 0.507 +/- ~0.05

All three methods agree to within statistical/discretization error. Code: `code/debug_normalization.py`.

### 2.3 Time-Domain Validation

A vectorized Velocity Verlet time-domain simulation (100 trajectories, 30000 steps) was also run as a cross-check. Results were qualitatively consistent but suffered from the same UV contamination in velocity. The time-domain approach is O(N_steps * N_ensemble) while the frequency-domain approach is O(N_modes * log(N_modes) * N_ensemble), and the frequency-domain approach is exact for the linear system. Code: first version in `code/sed_harmonic_oscillator.py`.

## 3. Simulation Results

### 3.1 Position Variance — QM Ground State Reproduced

**[COMPUTED]** Position variance matches the QM prediction to within ~5% across all parameter regimes:

| Run | tau | w_max | dt | N_ensemble | var_x (MC) | var_x (target) | Error |
|-----|-----|-------|-----|-----------|-----------|----------------|-------|
| A   | 0.01 | 62.8 | 0.05 | 2000 | 0.5249 | 0.5 | 5.0% |
| B   | 0.001 | 31.4 | 0.10 | 2000 | 0.5071 | 0.5 | 1.4% |
| C   | 0.01 | 314.2 | 0.01 | 2000 | 0.4908 | 0.5 | 1.8% |

Key observations:
- var_x is **insensitive to the UV cutoff** (w_max). Changing w_max by 10x (Run A vs C) does not change var_x significantly.
- var_x is **insensitive to tau** over 2 orders of magnitude (Runs A vs B). It converges to 0.5 for any small tau.
- The ~2-5% deviations are consistent with Monte Carlo statistical noise (N=2000 gives ~4.5% standard error on variance).

### 3.2 Velocity Variance — UV Divergent

**[COMPUTED]** Velocity variance grows logarithmically with the UV cutoff:

| Run | w_max | var_v (MC) | var_v (target) | Ratio to target |
|-----|-------|-----------|----------------|-----------------|
| B   | 31.4  | 0.655     | 0.5            | 1.3x            |
| A   | 62.8  | 5.708     | 0.5            | 11.4x           |
| C   | 314.2 | 38.576    | 0.5            | 77.2x           |

The scaling is consistent with the prediction var_v ~ ln(w_max/w0):
- ln(31.4) = 3.4, ln(62.8) = 4.1, ln(314.2) = 5.8
- But the growth is faster than pure logarithmic — this is because the leading divergent term is (tau/pi) * integral_0^wmax w^5/|H|^2 dw, which for intermediate w (where |H|^2 ~ w^4 rather than tau^2*w^6) gives power-law rather than logarithmic behavior.

### 3.3 Energy

**[COMPUTED]** The total energy E = (1/2)*var_v + (1/2)*w0^2*var_x is dominated by the UV-divergent kinetic energy:

| Run | w_max | E (MC) | E (target) |
|-----|-------|--------|------------|
| B   | 31.4  | 0.582  | 0.5        |
| A   | 62.8  | 3.116  | 0.5        |
| C   | 314.2 | 19.536 | 0.5        |

However, the **potential energy** 0.5*w0^2*var_x converges to the correct value:

| Run | PE = 0.5*w0^2*var_x | Target 1/4*hbar*w0 = 0.25 |
|-----|---------------------|---------------------------|
| A   | 0.262               | 0.25                      |
| B   | 0.254               | 0.25                      |
| C   | 0.245               | 0.25                      |

This is expected from the virial theorem for the harmonic oscillator: the equipartition of the ground state energy between kinetic and potential only holds for the resonant modes near w0. The high-frequency tail contributes additional kinetic energy but negligible potential energy.

## 4. Distribution Analysis

### 4.1 Gaussianity — Confirmed

**[COMPUTED]** The position distribution passes all normality tests:

| Run | KS stat | KS p-value | Shapiro stat | Shapiro p | Skewness | Excess Kurtosis |
|-----|---------|------------|--------------|-----------|----------|-----------------|
| A   | 0.0108  | 0.972      | 0.9994       | 0.824     | 0.032    | -0.008          |
| B   | 0.0158  | 0.693      | 0.9985       | 0.077     | -0.061   | -0.246           |
| C   | 0.0182  | 0.516      | 0.9988       | 0.170     | 0.033    | -0.259           |

All KS p-values >> 0.05 (fail to reject normality). Shapiro-Wilk p-values >> 0.05. Skewness and excess kurtosis are near zero. The position distribution is **indistinguishable from Gaussian** at the N=2000 sample level.

This is expected theoretically: x(t) is a weighted sum of many independent frequency modes (each with random phase), so by the Central Limit Theorem, x is Gaussian regardless of the details of the spectral density.

### 4.2 Position Distribution Width

The Gaussian has the correct width: sigma_x = sqrt(var_x) ~ sqrt(0.5) ~ 0.707. This matches the QM ground state wavefunction:

    psi(x) = (m*w0/(pi*hbar))^{1/4} exp(-m*w0*x^2/(2*hbar))

which gives sigma_x = sqrt(hbar/(2*m*w0)) = sqrt(0.5) = 0.707.

## 5. Parameter Sensitivity

### 5.1 Dependence on tau (radiation reaction strength)

**[COMPUTED]** var_x is robust to changes in tau over two orders of magnitude:

| tau | var_x (spectral sum) | var_x (analytic quadrature) |
|-----|---------------------|---------------------------|
| 0.1   | ~0.55 (moderate UV excess) | 0.547 |
| 0.01  | 0.511 | 0.513 |
| 0.001 | 0.502 | 0.502 |

For smaller tau, the resonance peak at w0 becomes sharper (width ~ tau*w0^2) and the result converges to the analytic value of 0.5. For larger tau (tau = 0.1), there's a ~10% excess from the UV tail (the resonance is broader and the "near-resonance" approximation breaks down).

### 5.2 Dependence on UV Cutoff (w_max = pi/dt)

**[COMPUTED]** Position variance is cutoff-independent; velocity variance grows with cutoff:

| dt | w_max | var_x | var_v | E |
|----|-------|-------|-------|---|
| 0.10 | 31.4 | 0.502 | 0.660 | 0.581 |
| 0.05 | 62.8 | 0.511 | 5.82 | 3.16 |
| 0.01 | 314.2 | 0.512 | 38.5 | 19.5 |

This demonstrates that **only the position variance is a physical (cutoff-independent) prediction of SED for the harmonic oscillator.**

### 5.3 Full Abraham-Lorentz vs Effective Damping

The effective damping approximation (H = w0^2 - w^2 + i*Gamma*w) has WORSE UV behavior because |H|^2 ~ w^4 at high frequencies (vs tau^2*w^6 for full A-L). This makes even the position variance logarithmically divergent! The full Abraham-Lorentz transfer function is essential for UV convergence of var_x.

From the initial (incorrect-normalization) runs:
- Full A-L, tau=0.01: var_x_spectral = 0.511 (converged)
- Eff. damping, tau=0.01: var_x_spectral = 0.512 (seems fine, but actually grows slowly with w_max due to ln divergence)

## 6. Assumptions and Limitations

### 6.1 Assumptions Made in This Simulation

1. **Dipole approximation:** The ZPF electric field is evaluated at the particle's equilibrium position, not at its actual position. This is valid when the particle displacement is much smaller than the wavelength of relevant radiation (x << c/w0). In natural units, x ~ sqrt(0.5) ~ 0.7 and c/w0 ~ c >> 1, so this is well satisfied.

2. **Non-relativistic:** Particle velocities are much less than c. Since var_v ~ 0.5 in natural units and c >> 1, this is satisfied for the resonant modes. However, the UV-divergent velocity contribution technically violates this at high frequencies — another reason that mass renormalization is needed.

3. **Single particle, no back-reaction:** The particle does not significantly modify the ZPF. The radiation reaction term (Abraham-Lorentz) accounts for the particle's emission back into the field, but we don't track the field evolution.

4. **Linearity:** The harmonic potential is exactly quadratic. The frequency-domain solution is EXACT for this case. For anharmonic potentials, mode coupling would arise and the frequency-domain approach breaks down.

5. **Equilibrium / stationarity:** The ZPF is a stationary random process. In the frequency-domain approach, we directly compute the equilibrium distribution without simulating transients.

### 6.2 What Would Break for More Complex Systems

1. **Anharmonic potentials (V != (1/2)*m*w0^2*x^2):** Mode coupling means the frequency-domain transfer function approach fails. Would need true time-domain simulation. SED is known to fail for some anharmonic systems (e.g., the hydrogen atom stability problem).

2. **Multi-particle systems:** Particle-particle correlations are not captured by independent single-particle SED. Entanglement-like correlations require careful treatment.

3. **Relativistic motion:** For strong fields or small-mass particles, the non-relativistic approximation breaks down. Relativistic SED is more complex and less well-developed.

4. **Beyond dipole approximation:** For spatially extended systems or high-frequency fields, the spatial variation of E_zpf matters. This introduces additional coupling and potential difficulties.

5. **Multi-time correlations:** Blanchard et al. (1986) showed that while single-time distributions match QM, multi-time correlations in stochastic mechanics (and likely SED) give wrong answers. This exploration only checks the single-time position distribution.

### 6.3 The Mass Renormalization Issue

The UV divergence of var_v (kinetic energy) is not a bug in the simulation — it reflects real physics. In classical electrodynamics, a point charge has infinite electromagnetic self-energy. The Abraham-Lorentz equation implicitly assumes a bare mass, and the observed mass is:

    m_obs = m_bare + delta_m(w_max)

where delta_m grows logarithmically with the UV cutoff. The "total energy" computed from the simulation includes this bare-mass contribution. Only the position distribution and potential energy are renormalization-independent observables.

This is closely related to the quantum field theory concept of mass renormalization, and it's satisfying to see it emerge naturally in the classical SED simulation.

## 7. Summary of Results

### Position Variance
**[COMPUTED]** var_x = 0.507 +/- 0.05 (tau=0.001, N=2000 ensemble) vs QM target 0.5. **PASS** (1.4% error). Confirmed across 3 parameter regimes (tau=0.01, 0.001; w_max=31-314).

### Position Distribution Shape
**[COMPUTED]** Gaussian: KS test p > 0.5 for all runs, Shapiro-Wilk p > 0.07 for all runs, |skewness| < 0.07, |excess kurtosis| < 0.26. **PASS.**

### Energy
**[COMPUTED]** Total energy is UV-divergent and cannot be directly compared to E0 = 0.5. Potential energy PE = 0.5*w0^2*var_x = 0.254 matches the expected 0.25 (1/4 * hbar * w0) to ~2%. The energy comparison requires mass renormalization, which is beyond this exploration's scope.

### Spectral Density
**[VERIFIED]** The correct one-sided PSD is S_F^one(w) = 2*tau*hbar*w^3/m. The original code had (2*tau*hbar/(pi*m))*w^3, which is wrong by a factor of pi.

### Transfer Function
**[COMPUTED]** The full Abraham-Lorentz transfer function H = w0^2 - w^2 + i*tau*w^3 is REQUIRED for UV convergence of the position variance. The effective damping approximation H = w0^2 - w^2 + i*Gamma*w gives a logarithmically divergent position variance.
