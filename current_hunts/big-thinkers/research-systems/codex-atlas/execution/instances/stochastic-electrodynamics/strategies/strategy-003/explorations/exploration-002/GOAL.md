# Exploration 002 — SED Hydrogen: Physical τ and T_ion(L) Measurements

## Mission Context

You are working on Stochastic Electrodynamics (SED) hydrogen simulations. The SED model simulates a classical electron in a Coulomb potential subjected to a stochastic zero-point field (ZPF) with spectral density S_F(ω) = 2τħω³/m (in atomic units, ħ=1, m=1).

**Prior work (Strategy-002 E003)** produced a T_ion(L) table — ionization timescales as a function of angular momentum L — but used τ = 1.57×10⁻⁵ atomic units, which is 60× too large. All T_ion values are therefore ~60× too short.

**Your job:** Re-run with physical τ = 2.6×10⁻⁷ atomic units.

## Physical Constants (VERIFY BEFORE CODING)

In atomic units (ħ = mₑ = e = 4πε₀ = 1):
- **τ = 2e²/(3mₑc³) = 2α³/3 where α = 1/137.036**
- **τ = 2/(3 × 137.036³) ≈ 2.6×10⁻⁷ atomic time units**
- **c = 137.036 atomic units** (inverse fine structure constant)
- **Orbital period for n=1 circular orbit: T_orb = 2π atomic time units ≈ 6.28 a.u.**

Sanity check: 2/(3 × 137.036³) = 2/(3 × 2,571,215) = 2/7,713,645 ≈ 2.59×10⁻⁷ ✓

The error in E003: they used τ = 1.57×10⁻⁵, which corresponds to roughly τ_SI/40 but computed incorrectly. The correct value is 2.6×10⁻⁷.

## L Values to Scan

Scan L/ħ = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0] (7 values)

The critical angular momentum is approximately L_crit ≈ 0.588ħ (Nieuwenhuizen 2015).

## Simulation Specifications

### Initial Conditions (same for all L values)
- Position: pos = [1.0, 0.0, 0.0] (Bohr radius = 1 a.u.)
- Velocity: vel = [0.0, L, 0.0] (tangential, so angular momentum = L at r=1)
- This gives a circular Bohr orbit at r=1 for L=1.0

### Run Parameters
- **20 trajectories per L value**
- **Cap at 10,000 orbital periods** for L < 1.0
- **Cap at 50,000 orbital periods for L = 1.0** (circular orbit may be stable long-term)
- Record r(t) every 100-500 orbital periods for diagnostics

### Ionization / Termination Criteria
- **Ionized:** r > 5.0 a₀ (ionization radius)
- **Nuclear collision:** r < 0.05 a₀ (treat as ionization)
- Cap reached without ionization → record as "not ionized"

### Equations of Motion

Use the Landau-Lifshitz reduction of the Abraham-Lorentz-Dirac (ALD) equation:

```
F_coulomb = -pos / |pos|³
d/dt(F_coulomb) = (-vel/|pos|³ + 3*pos*(pos·vel/|pos|²)/|pos|³)
a = F_coulomb + τ * d/dt(F_coulomb) + F_zpf
```

This is the Landau-Lifshitz form — the radiation reaction term is τ * dF_coulomb/dt, not the full Abraham-Lorentz jerk term. This avoids runaway solutions.

**DO NOT use the simple form** `a = F_coulomb + F_zpf - τ*(ω_local² * v)`. The position-dependent acceleration form above is correct.

### ZPF Spectral Density

One-sided ZPF force PSD per spatial component:
```
S_F(ω) = 2τω³   for 0 < ω ≤ ω_max
S_F(ω) = 0      otherwise
```

Use UV cutoff ω_max = 100 atomic units.

### CRITICAL: Memory Management for Long Runs

The prior code (E003) pre-generated the full ZPF array at initialization:
```python
F_zpf, dF_zpf = generate_zpf(N_steps, dt=DT, seed=seed)
```

For N_steps = 10,000 periods × 2π / 0.01 ≈ 6.28M steps, this is:
- F_zpf array: 6.28M × 3 × 8 bytes = 150 MB per trajectory
- dF_zpf array: another 150 MB
- **Total: ~300 MB per trajectory — marginal to too large**

**Solution: Generate ZPF in chunks.** Generate 100,000 steps at a time, process them, then generate the next chunk. This reduces memory to ~5 MB per trajectory while maintaining correct noise statistics.

```python
CHUNK_SIZE = 100_000  # steps per chunk

def generate_zpf_chunk(n_steps, dt, seed):
    """Generate n_steps of ZPF noise."""
    # Same FFT method as before, but for n_steps only
    ...

def run_full_sed_chunked(L, max_periods, seed, dt=0.01):
    N_max = int(max_periods * T_ORB / dt)
    pos = np.array([1.0, 0.0, 0.0])
    vel = np.array([0.0, float(L), 0.0])

    chunk_seed = seed
    for chunk_start in range(0, N_max, CHUNK_SIZE):
        n_in_chunk = min(CHUNK_SIZE, N_max - chunk_start)
        F_zpf, dF_zpf = generate_zpf_chunk(n_in_chunk, dt, seed=chunk_seed)
        chunk_seed += 1

        for n in range(n_in_chunk - 1):
            # ... integration loop using F_zpf[n], F_zpf[n+1], dF_zpf[n], dF_zpf[n+1]
            # check ionization condition
            ...
```

**Key**: Each chunk uses a DIFFERENT seed (chunk_seed += 1) so sequential chunks produce statistically independent noise. This is valid because we're targeting an equilibrium stationary process.

### Timestep
Use fixed dt = 0.01 atomic time units. This is ~1/628 of an orbital period — sufficient for the orbital dynamics.

For close approaches (r < 0.1 a₀), you may optionally use adaptive timestep: dt_local = min(0.01, 0.01 * r), but this requires matching the ZPF noise spectral density to the local timestep. For simplicity, use fixed dt=0.01 with the softened Coulomb potential (r_eff = max(r, 0.02)).

### Integrator

Use RK4 (4th-order Runge-Kutta) as in E003. For each step, you need forces at t_n, t_{n+1/2}, and t_{n+1}. Linearly interpolate for the half-step forces:
```
F_h = 0.5 * (F[n] + F[n+1])
dF_h = 0.5 * (dF[n] + dF[n+1])
```

## Sanity Check Before Full Run

Before running all 7 L values × 20 trajectories, verify:

1. **Pure Coulomb orbit**: with τ=0 and F_zpf=0, L=1.0 orbit should stay at r≈1.0 indefinitely (energy drift < 0.01% per 100 periods)
2. **Physical τ sanity**: print τ = 2/(3 × 137.036³) and confirm ≈ 2.6×10⁻⁷
3. **ZPF noise amplitude**: For τ=2.6×10⁻⁷ and ω_max=100, RMS force per component ≈ sqrt(τ × ω_max⁴ / (4π)) = sqrt(2.6×10⁻⁷ × 10⁸ / (4π)) ≈ sqrt(2.06×10⁻⁰) ≈ **1.44 atomic units**. Verify numerically.
4. **Short trial run**: Run L=0.5, 5 trajectories, 100-period cap, confirm ionization (should mostly ionize within 100 periods even with physical τ based on qualitative pattern)

## Run Order and Time Estimates

Run L values in order from most likely to ionize quickly (lowest L) to least:
1. L=0.4 (should ionize almost immediately)
2. L=0.5 (should ionize quickly)
3. L=0.6 (near critical, may or may not ionize in 1,000 periods)
4. L=0.7
5. L=0.8
6. L=0.9
7. L=1.0 (probably won't ionize in 10,000 periods, extend to 50,000)

Time estimate per trajectory at dt=0.01:
- 1,000 periods: ~63K steps → ~0.1 seconds (estimate)
- 10,000 periods: ~628K steps → ~1-2 seconds
- 50,000 periods: ~3.14M steps → ~5-10 seconds

For 20 trajectories × 7 L values = 140 trajectories at the cap: estimated total time 20-30 minutes.

## Output Requirements

For each L value, record:
- Fraction ionized (n/20)
- Median T_ion in orbital periods (for ionized trajectories)
- IQR of T_ion (25th to 75th percentile)
- ⟨r⟩ during early periods (sanity check vs QM expected value)
- Whether cap was reached

**Sanity check for L=1.0:** In atomic units, ⟨r⟩ for the circular n=1 orbit = 1.5 × (3/2) a₀ ... wait, actually for circular orbit at r=1 with L=1, the mean radius should be ≈ 1.0 a₀ initially (it IS at r=1). The QM expectation value ⟨r⟩ = 1.5 a₀ for the 1s state; for the circular orbit initial condition, ⟨r⟩ ≈ 1.0 early, then drifting toward 1.5 if the ZPF establishes the QM distribution. Report this.

## Key Results Table

Produce this table format:

```
L/ħ | N_ion/20 | Median T_ion (periods) | IQR | ⟨r⟩/a₀ | Notes
----|----------|------------------------|-----|---------|------
0.4 | ?/20     | ?                      | ?   | ?       |
0.5 | ?/20     | ?                      | ?   | ?       |
...
1.0 | ?/20     | ? (or >cap)            | ?   | ?       | Extended to 50k if no ionization
```

## Success Criteria

**Minimum success:**
- Ran at least 5 L values with 20 trajectories, physical τ = 2.6×10⁻⁷
- T_ion table produced (even if many entries are "< cap, no ionization")
- ⟨r⟩ sanity check for L=1.0 passes (⟨r⟩ ≈ 1.0-1.5 a₀)

**Good success:**
- All 7 L values completed
- T_ion(L) shows monotonic increase with L (confirming qualitative pattern)
- L=1.0 either: (a) shows no ionization up to cap → confirms stability, or (b) shows eventual ionization → quantifies T_ion
- Clear statement: "With physical τ, T_ion(L=0.5) ≈ X periods vs 17 periods in E003"

## Prior T_ion Data (for Comparison)

From Strategy-002 E003 (τ = 1.57×10⁻⁵ = 60× too large):

| L/ħ | Frac ionized (200 period cap) | Median T_ion (periods) |
|-----|-------------------------------|------------------------|
| 1.0 | 10% (2/20)                    | >200 (cap)             |
| 0.9 | 35% (7/20)                    | ~108                   |
| 0.7 | 75% (15/20)                   | ~83                    |
| 0.5 | 95% (19/20)                   | ~17                    |

With physical τ (60× smaller), expect T_ion to be ~60× longer, so L=0.5 median ≈ 1,000 periods, L=1.0 ≈ >>10,000 periods.

## Prior Code Reference

The E003 hydrogen simulation code is at:
`/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/stochastic-electrodynamics/strategies/strategy-002/explorations/exploration-003/code/sed_hydrogen_sim.py`

You may adapt this code. Key change required: `TAU = 1.57e-5` → `TAU = 2.6e-7`.

Also add chunked ZPF generation to handle long runs. The rest of the physics (Landau-Lifshitz ALD, RK4 integrator, ZPF spectral density) is correct.

## Output Files

Write REPORT.md (with results as you go — incremental writing), then REPORT-SUMMARY.md at the end.

Your exploration directory:
`/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/stochastic-electrodynamics/strategies/strategy-003/explorations/exploration-002/`

Save all code to a `code/` subdirectory within your exploration directory.
