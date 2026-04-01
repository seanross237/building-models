# Exploration 003 — SED Hydrogen: Time to Self-Ionization and Stability Window

## Mission Context

You are exploring Stochastic Electrodynamics (SED) — classical electrodynamics augmented by a real, Lorentz-invariant zero-point field (ZPF). This exploration probes SED hydrogen: a classical electron in a Coulomb potential driven by SED zero-point noise.

**Background — this problem is effectively closed, but uncharacterized:**
- Cole & Zou (2003): 11 simulations, short runs, reported probability density agreeing with |ψ₁s|². Initial optimism.
- Nieuwenhuizen & Liska (2015): Extended to full 3D GPU simulations with much longer runs. Result: SELF-IONIZATION IN ALL SIMULATIONS when orbital angular momentum fell below ~0.588ħ. Mechanism: near-nucleus passes in eccentric orbits → high-frequency ZPF injects energy faster than radiation reaction dissipates it.
- Nieuwenhuizen (2020): All renormalization schemes tested (short-time, absolute value variants, fractional power) → ALL FAIL. Conclusion: "SED is not a basis for quantum mechanics."

**The gap:** No quantitative timescale data exists in our library. We don't know: How long does the ground state persist? Is there a stability window? Is there a critical angular momentum threshold below which ionization is rapid vs. slow?

## Specific Goal

Run a targeted SHORT computation: simulate a classical electron in a 3D Coulomb potential plus SED noise using the Abraham-Lorentz equation. Measure:
1. **Mean orbital radius** ⟨r⟩ vs QM Bohr radius a₀ = 1.0 (in atomic units)
2. **Time to self-ionization** T_ion (when r > 5a₀) as a function of initial angular momentum L
3. **Critical angular momentum** L_crit below which ionization is rapid (< 10² orbital periods)

## Units and Parameters

Use **atomic units**: ℏ = 1, m_e = 1, e = 1, a₀ = 1.

- Coulomb potential: V(r) = -1/r
- Bohr radius: a₀ = 1, circular orbit period T_orb = 2π for n=1 orbit
- τ = e²/(6πε₀m_ec³) in SI → in atomic units, τ ≈ 2/3 × α³/(m_e c²/ℏ) ≈ 1.57 × 10⁻⁵ (in units of 1/ω_Bohr)
  - Use τ = 1.57 × 10⁻⁵ atomic units for radiation reaction

**ZPF noise in 3D atomic units:**
```
S_F(ω) = 2τℏω³/m = 2τω³   [in atomic units where ℏ=m=1]
```

FFT amplitude: `A_k = sqrt(S_F(omega_k) * N / (2 * dt))`

## Simulation Setup

**3D equations of motion (ALD in Coulomb potential):**
```
r̈ = -r̂/r² - τ(V''_eff(r))ṙ + F_zpf + τṪ_zpf
```

More precisely, in Cartesian coordinates:
```
ẍ = -x/r³ + F_x_zpf(t) + [radiation reaction terms]
ÿ = -y/r³ + F_y_zpf(t) + [radiation reaction terms]
z̈ = -z/r³ + F_z_zpf(t) + [radiation reaction terms]
```

**Radiation reaction (Landau-Lifshitz):**
The full ALD in Cartesian form:
```
ẍᵢ = Fᵢ_Coulomb/m + τ·d(Fᵢ_Coulomb)/dt + F_zpf_i + τ·Ḟ_zpf_i
```
where `d(F_x)/dt = d(-x/r³)/dt = (-ẋr³ + 3xr²ṙ)/r⁶ = (-ẋ + 3x(r·ṙ/r²))/r³`

**Singularity handling:** Use adaptive timestep near the nucleus. When r < 0.1a₀, reduce dt by factor of 10. When r < 0.01a₀, by factor of 100.

**UV cutoff:** Use ω_max = 100 (in atomic units, 100× the characteristic Bohr frequency). dt = 0.01 atomic time units when not near nucleus.

## Initial Conditions

Start with a circular orbit at r = a₀ = 1 (ground state Bohr radius):
- Position: (x, y, z) = (1, 0, 0)
- Velocity: (ẋ, ẏ, ż) = (0, v_c, 0) where v_c = 1.0 for circular orbit at r=1

Circular orbit angular momentum: L = m_e × r × v_c = 1.0 ħ (n=1 ground state).

Also test:
- L = 0.9ħ (slightly eccentric)
- L = 0.7ħ (moderately eccentric)
- L = 0.5ħ (Nieuwenhuizen's critical value ~ 0.588ħ, expect rapid ionization)

For each L value, run N_traj = 20 independent ZPF realizations. 20 is enough to get a rough distribution of T_ion.

## What to Measure

### Primary: Time to Ionization

For each trajectory, record T_ion = first time r > 5a₀ (or r > 10a₀ as secondary criterion). Report:
- Mean T_ion in units of orbital periods T_orb = 2π
- Standard deviation
- Fraction that ionize within the simulation cap (10⁴ orbital periods = 2π × 10⁴ ≈ 62,832 atomic time units)

Cap simulation at 10⁴ orbital periods per trajectory. If the electron hasn't ionized by then, report as "stable within simulation."

### Secondary: Mean Orbital Radius

Before ionization, compute ⟨r⟩ averaged over the first 100 orbital periods. Compare to Bohr a₀ = 1.

### Tertiary: Ionization Mechanism

For one trajectory at each L value, plot r(t) and log energy E(t) = ½v² - 1/r over the first 1000 periods. This reveals whether:
(a) Energy gradually increases (slow energy injection)
(b) Rapid energy injection near nucleus (Nieuwenhuizen mechanism)
(c) Sudden instability

## Sanity Checks

1. At t=0 with no ZPF noise (τ=0, F_zpf=0): the orbit should be stable indefinitely. Verify circular orbit at r=1 remains circular.
2. With ZPF only (no radiation reaction, τ=0): trajectories should gain energy and ionize FAST (ZPF pumps energy with no damping).
3. Full ALD: some balance between ZPF energy injection and radiation damping. Report the timescale.

## Run Explorations Sequentially

Run L=1.0 first, check output, then L=0.9, L=0.7, L=0.5. Each L value: 20 trajectories. Don't try to run all 80 trajectories at once.

## Prior Art Search

Before writing your report, web search for:
1. "SED hydrogen self-ionization timescale" and "Cole Zou 2003 stochastic electrodynamics hydrogen"
2. "Nieuwenhuizen Liska 2015 SED hydrogen simulation" — how long did stable orbits last in their simulations?
3. "critical angular momentum SED hydrogen"

## Success Criteria

**Positive result:** You obtain T_ion values with error bars as a function of L. Even if ALL trajectories self-ionize quickly, that's a clear result: "SED hydrogen self-ionizes within X orbital periods for L ≥ L_c."

**Interesting result:** A clear critical angular momentum threshold — above L_crit = 0.7ħ, T_ion > 10³ periods; below L_crit, T_ion < 100 periods. This quantifies the Nieuwenhuizen finding numerically.

**Negative result:** Numerical instability from Coulomb singularity even with adaptive timestepping. If so, document precisely when (at what r) instability occurs and suggest what smaller dt would be needed.

**Failure:** No quantitative results computed.

## Output Format

Write REPORT.md with:
1. Simulation code (key loop and ALD implementation)
2. Sanity check results (no-ZPF orbit stability)
3. T_ion table: L × [mean T_ion/T_orb, std, fraction ionized, ⟨r⟩/a₀]
4. Energy plot description (or inline ASCII plot) for one trajectory at each L
5. Ionization mechanism description
6. Prior art search results
7. Overall verdict: Does SED hydrogen have a stability window? What is T_ion for ground-state circular orbit?

Write REPORT-SUMMARY.md (max 300 words) with:
- Key quantitative result (T_ion for L=1.0ħ, critical L value)
- Whether Cole & Zou's optimism was warranted (short-run stability) or Nieuwenhuizen's pessimism (long-run ionization)
- Any novel quantitative finding not in Nieuwenhuizen (2015, 2020)

**Write incrementally — write to REPORT.md after each L value run.**

## Your exploration directory

`/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/stochastic-electrodynamics/strategies/strategy-002/explorations/exploration-003/`

Save all code, REPORT.md, and REPORT-SUMMARY.md here.
