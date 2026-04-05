# Exploration 005 — SED Tunneling: Verify Γ Formula at 5+ λ Values

## Mission Context

You are verifying the key quantitative finding from Strategy-002 Exploration 001: a formula relating SED barrier-crossing rates to quantum tunneling rates in a double-well potential.

**This is a mathematical/computational verification. Everything you need is here. Reuse the code from Exploration 001.**

## What Was Found in E001 (Two Data Points)

The double-well potential is `V(x) = -½ω₀²x² + ¼λx⁴` with ω₀=m=ħ=1.

**Key insight from E004 (confirmed analytically):** The local oscillation frequency at the potential minimum x_min = 1/√λ is ALWAYS ω_local = √2, regardless of λ:
- V''(x_min) = -ω₀² + 3λx_min² = -1 + 3λ(1/λ) = 2
- ω_local = √(V''(x_min)/m) = √2 (universal constant for this potential family)

Therefore, the ZPF energy at the well bottom is: **E_zpf = ħω_local/2 = √2/2 ≈ 0.7071** (constant for all λ).

**Barrier height:** V_barrier = 1/(4λ). So V_barrier/E_zpf = √2/(4λ).

**Proposed formula (needs verification):**
```
Γ_SED/Γ_exact ≈ A × exp(S_WKB − V_barrier/E_zpf)
```
where S_WKB is the WKB action integral from the QM computation, V_barrier/E_zpf = √2/(4λ), and A is an unknown prefactor.

**E001 measurements (2 data points):**

| λ | S_WKB | V_barrier/E_zpf | Measured Γ_SED/Γ_exact | Predicted exp(S_WKB - V_b/E_zpf) | Implied A |
|---|-------|-----------------|-------------------------|-----------------------------------|-----------|
| 0.25 | 1.408 | 1.414 | 1.15 | exp(-0.006) ≈ 1.00 | 1.15 |
| 0.10 | 6.290 | 3.536 | 18.5 | exp(2.754) ≈ 15.7 | 1.18 |

The prefactor A ≈ 1.15–1.18 appears in both cases. **If A is universal, the formula becomes:**
```
Γ_SED/Γ_exact ≈ 1.17 × exp(S_WKB − √2/(4λ))
```

**Your goal:** Verify this formula at 5+ additional λ values spanning from deep barriers (λ=0.05) to near-transition (λ=0.30).

## The Code (Reuse Directly from E001)

**Key simulation loop (from E001 REPORT.md, verified):**

```python
import numpy as np

def run_sed_double_well(lam, omega0=1.0, tau=0.001, omega_max=10.0,
                         dt=0.05, N=200000, N_traj=100):
    """
    SED double-well simulation with ALD equation.
    Returns Gamma_SED (barrier-crossing rate in units of omega0).
    """
    m = 1.0; hbar = 1.0

    # FFT noise generation
    T = N * dt
    freqs = np.fft.rfftfreq(N, d=dt) * 2 * np.pi  # angular freq array
    S_F = 2.0 * tau * hbar * np.abs(freqs)**3 / m   # one-sided PSD
    A_k = np.sqrt(S_F * N / (2.0 * dt))              # FFT amplitude

    # Generate N_traj independent noise realizations
    phases = np.random.uniform(0, 2*np.pi, (N_traj, len(freqs)))
    noise_fft = A_k * np.exp(1j * phases)
    F_zpf_t = np.fft.irfft(noise_fft, n=N, axis=1)  # shape: (N_traj, N)

    # Time-derivative of noise (finite difference)
    dF_zpf_t = np.diff(F_zpf_t, axis=1, prepend=F_zpf_t[:, :1]) / dt

    # Initial conditions: x = +x_min, v = 0
    x_min_val = omega0 / np.sqrt(lam)
    x = np.full(N_traj, x_min_val)
    v = np.zeros(N_traj)

    # Burn-in: 1000 time units
    N_burnin = int(1000 / dt)
    N_measure = N - N_burnin

    sign_crossings = np.zeros(N_traj, dtype=int)
    x_prev_sign = np.sign(x)

    for i in range(N):
        # V'(x) = -omega0^2 * x + lam * x^3
        cons_force = omega0**2 * x - lam * x**3
        # V''(x) = -omega0^2 + 3*lam*x^2
        Vpp = -omega0**2 + 3.0 * lam * x**2
        damp_force = -tau * Vpp * v   # ALD damping
        zpf_drive = F_zpf_t[:, i] + tau * dF_zpf_t[:, i]

        force = cons_force + damp_force + zpf_drive
        v += force * dt   # Euler-Cromer
        x += v * dt

        # Count sign crossings (after burn-in)
        if i >= N_burnin:
            new_sign = np.sign(x)
            crossings = (new_sign != x_prev_sign) & (new_sign != 0)
            sign_crossings += crossings.astype(int)
            x_prev_sign = new_sign

    T_measure = N_measure * dt
    Gamma_SED = sign_crossings / T_measure  # per trajectory
    return Gamma_SED.mean(), Gamma_SED.std() / np.sqrt(N_traj)
```

**QM tunneling rate computation (from E001, verified):**

```python
import scipy.linalg

def compute_qm_tunneling_rate(lam, omega0=1.0, N_grid=2000, x_range=6.0):
    """
    Compute exact QM tunneling rate via finite-difference Schrödinger equation.
    Returns: E0, E1, Gamma_exact (= (E1-E0)/2), S_WKB, V_barrier/E_zpf
    """
    x = np.linspace(-x_range, x_range, N_grid)
    dx = x[1] - x[0]

    # Potential
    V = -0.5 * omega0**2 * x**2 + 0.25 * lam * x**4

    # Kinetic energy: -ħ²/(2m) d²/dx² using finite differences
    # Tridiagonal: diagonal = 1/(dx²) + V, off-diagonal = -1/(2dx²)
    diag = 1.0/dx**2 + V
    off_diag = -0.5/dx**2 * np.ones(N_grid-1)

    # Get lowest 4 eigenvalues
    eigenvalues = scipy.linalg.eigh_tridiagonal(diag, off_diag,
                                                 eigvals_only=True,
                                                 select='i',
                                                 select_range=(0, 3))
    E0, E1 = eigenvalues[0], eigenvalues[1]

    # Tunneling rate = splitting / 2 (energy oscillation frequency)
    Gamma_exact = (E1 - E0) / 2.0

    # WKB action integral
    x_min = omega0 / np.sqrt(lam)
    E_zpf = np.sqrt(2.0) / 2.0  # = omega_local/2 = sqrt(2)/2 (universal)
    V_barrier = 1.0 / (4.0 * lam)
    V_b_over_E_zpf = V_barrier / E_zpf  # = sqrt(2)/(4*lam)

    # WKB: integrate sqrt(2(V-E0)) over classically forbidden region
    mask = V > E0
    S_WKB = np.trapz(np.sqrt(2.0 * np.maximum(V - E0, 0)), x)  # approx

    return E0, E1, Gamma_exact, S_WKB, V_b_over_E_zpf
```

## λ Values to Test

Test these λ values in order (run one at a time — don't batch them all):

1. **λ = 0.30** (V_barrier=0.833, near transition to over-barrier — check if still tunneling)
2. **λ = 0.20** (V_barrier=1.25, between E001's two data points)
3. **λ = 0.15** (V_barrier=1.667)
4. **λ = 0.075** (V_barrier=3.33, deep barrier — need longer simulation or more trajectories)
5. **λ = 0.05** (V_barrier=5.0, very deep — rare crossings, need N=500,000 or N_traj=200)

For each λ:
- First run `compute_qm_tunneling_rate(lam)` to get E0, E1, Gamma_exact, S_WKB, V_b_E_zpf
- Check: is E0 < V_barrier? If E0 > V(0) = 0, skip (over-barrier regime)
- Then run `run_sed_double_well(lam, N_traj=100)` for λ ≥ 0.15
- For λ ≤ 0.075: increase N=400,000 or N_traj=200 (rare events need larger samples)
- Also optionally test λ=0.10 again to cross-check E001's result

**Stop early if the formula clearly breaks down** (report why).

## Primary Analysis: Plot and Test the Formula

For each λ in tunneling regime, compute:
- `S_WKB` from QM
- `V_b_E_zpf = sqrt(2)/(4*lambda)` from the analytical formula
- `exponent = S_WKB - V_b_E_zpf`
- `ln(Gamma_SED / Gamma_exact)`

Test: Is `ln(Gamma_SED/Gamma_exact)` linear in `exponent = S_WKB - V_b_E_zpf` with slope ≈ 1?
And: Is the intercept (when exponent=0) equal to `ln(A)` with A ≈ 1.15?

Report:
1. The data table: λ × [S_WKB, V_b/E_zpf, Γ_SED, Γ_exact, Γ_SED/Γ_exact, predicted ratio, residual]
2. Linear fit: slope and intercept of ln(Γ_SED/Γ_exact) vs (S_WKB - V_b/E_zpf)
3. The universal prefactor A = exp(intercept)

## Secondary Question: When Does the Formula Break Down?

For very deep barriers (small λ, large S_WKB), the crossing events are exponentially rare. At some point:
- Γ_SED may be dominated by numerical noise (sampling error)
- The ALD approximation may break down for very energetic rare events

Report: what is the deepest barrier (smallest λ) for which Γ_SED is measurable with N_traj=100?

## Sanity Check

At λ=0.10, you should recover Γ_SED/Γ_exact ≈ 18.5 (from E001). If your code gives something different, check:
1. Noise normalization: A_k formula
2. ALD equation signs (ALD adds energy at barrier top, removes at well bottom)
3. Initial conditions (start at x_min, not x=0)

## UV Divergence Warning

Don't compute total energy or velocity variance — they are UV-divergent. Report only position-based observables (barrier-crossing rate, mean |x|).

## Write Incrementally

After EACH λ value simulation, write the result to REPORT.md immediately. Include code, parameters, results, and the computed Γ_SED/Γ_exact ratio with error bars.

## Prior Art Search

After completing the simulations, do a quick web search for:
1. "stochastic tunneling classical rate theory" and "classical tunneling rate ZPF"
2. "Kramers rate theory ZPF zero-point field comparison"
3. "SED barrier crossing rate formula"

Note any papers that discuss the exp(S_WKB - ...) structure.

## Success Criteria

**Good success:** 4+ λ values computed with clear Γ_SED/Γ_exact ratios, linear fit of formula.

**Excellent success:** The formula ln(Γ_SED/Γ_exact) = ln(A) + (S_WKB - V_b/E_zpf) confirmed with slope ≈ 1 and A ≈ 1.15 across all data points.

**Acceptable negative:** The formula fails for deep barriers (λ < 0.075). Document when and why.

**Failure:** No quantitative results computed.

## Your Exploration Directory

`/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/stochastic-electrodynamics/strategies/strategy-002/explorations/exploration-005/`

The code from E001 is at: `/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/stochastic-electrodynamics/strategies/strategy-002/explorations/exploration-001/` (read the REPORT.md for the exact code).

Write REPORT.md and REPORT-SUMMARY.md here.
