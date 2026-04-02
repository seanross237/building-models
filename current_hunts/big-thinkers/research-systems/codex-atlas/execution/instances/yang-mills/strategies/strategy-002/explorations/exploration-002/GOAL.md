# Exploration 002: Poincaré Constant / Spectral Gap vs. β for SU(2) Lattice Yang-Mills

## Mission Context
This is a YANG-MILLS mission. We are attacking the Yang-Mills Millennium Prize Problem (existence and mass gap for 4D quantum Yang-Mills theory). This is strategy-002.

**Do not conflate with other missions in this repository** (there are also missions on the Riemann Hypothesis, amplituhedron, and other topics — ignore all of those).

## Background

The Shen-Zhu-Zhu (SZZ) theorem (CMP 400, 2023; arXiv:2204.12737) proves that the SU(N) lattice Yang-Mills Gibbs measure satisfies a Poincaré inequality at strong coupling (β < 1/48 in 4D). This Poincaré inequality guarantees:
- A positive spectral gap for the Langevin dynamics (Markov chain mixing rate)
- Exponential decay of correlations = mass gap

The SZZ bound (β < 1/48 ≈ 0.0208) is a SUFFICIENT condition from their proof. The physical question is: does the spectral gap (and hence the mass gap) actually persist for larger β?

**Key question for this exploration:**
How does the spectral gap of the SU(2) Gibbs measure (measured as MCMC autocorrelation time) vary across β = 0.02 to β = 3.0? Does it drop sharply at β ≈ 0.02 = 1/48, or does it decay smoothly? At β = 2.0-3.0 (the physical lattice QCD region), does a spectral gap still appear to exist?

## Strategy Context
- β < 1/48 ≈ 0.021: SZZ guarantees positive Poincaré constant
- β ≈ 2.0-2.5: physical lattice region for SU(2) confinement
- β_c ≈ 2.3: deconfinement transition for SU(2) on 4⁴ lattices

## Prior Code Available

**SU(2) lattice simulation code from exploration-003 is available at:**
`../../strategy-001/explorations/exploration-003/code/su2_lattice.py`
`../../strategy-001/explorations/exploration-003/code/su2_simulation.py`

This code implements:
- SU(2) gauge fields as unit quaternions
- Wilson action: S = -β Σ_plaq Re Tr(U_p)
- Kennedy-Pendleton heat bath algorithm for SU(2)
- Plaquette measurement, Creutz ratios, string tension

**Autocorrelation code from exploration-008 is available at:**
`../../strategy-001/explorations/exploration-008/code/autocorr_mass_gap_4d.py`

This code implements integrated autocorrelation time estimation (τ_int) but was written for finite groups. You will need to adapt it for continuous SU(2).

## Your Task: Computational (write code, run it, report numbers)

**IMPORTANT: Compute first, report second. Do NOT spend time planning — start coding immediately.**

### Step 1: Build the Measurement Setup (30 minutes max)

Extend the exploration-003 SU(2) code to measure:
1. **MCMC autocorrelation time τ_int** of the average plaquette P = (1/N_plaq) Σ_p Re Tr(U_p) / 2
2. The **spectral gap proxy**: γ ≈ 1 / (2 τ_int) (autocorrelation time is inversely proportional to the Markov chain spectral gap)
3. The **average plaquette** ⟨P⟩ at each β

Save all code to `code/` directory in this exploration folder as you write it.

### Step 2: Scan β Values (core measurement)

Run on a **4⁴ lattice** (for speed). Measure at β values:
`β = 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 3.0`

That is 8 values spanning the SZZ regime (β ≈ 0.02) through the physical lattice region (β = 2.0-3.0).

For each β:
- Thermalize for min(500, adaptive) sweeps
- Run 2000 measurement sweeps
- Measure plaquette every sweep
- Compute τ_int using the integrated autocorrelation time method

**Print results immediately** as you get them (do not wait for all β values before printing):
```
β = 0.02: ⟨P⟩ = X.XXXX, τ_int = X.X, γ ≈ X.XXXX
β = 0.05: ⟨P⟩ = X.XXXX, τ_int = X.X, γ ≈ X.XXXX
...
```

### Step 3: Interpret the Results

After running, answer:
1. Does γ ≈ 1/(2τ_int) decrease monotonically as β increases? Or is there a sharp drop?
2. Is there any evidence of a special behavior near β = 1/48 ≈ 0.021?
3. At β = 2.0, is τ_int finite (suggesting the Gibbs measure still mixes reasonably)?
4. Compare τ_int(β = 0.02) vs. τ_int(β = 2.0): how many orders of magnitude difference?

### Step 4: Physical Interpretation

Connect the measurements to theory:
- At β < 1/48: SZZ guarantees spectral gap. Does τ_int look "small" (fast mixing)?
- At β = 2.0-3.0: Near the physical region. If τ_int is finite (not diverging), this suggests the spectral gap/mass gap may persist numerically even where SZZ's proof doesn't apply.
- **Critical distinction:** τ_int measures the Markov chain mixing time (a computational property), not directly the physical mass gap. But they are related: both measure exponential decay of correlations under the Gibbs measure.

## Minimum Requirements (for success)

1. **8 data points** (β, τ_int, ⟨P⟩) — one for each β value above. MANDATORY: at least 5 must be successfully measured.
2. Code saved to `code/` directory in this exploration folder
3. A table of results with units and interpretation
4. A clear statement of what the results imply for extending the SZZ result

## Success Criteria

**Success:** You produce a table with ≥5 (β, τ_int, γ) measurements, showing how the spectral gap proxy varies. You give a clear statement about whether τ_int diverges before β = 2.0 (which would suggest a breakdown of the Gibbs measure's mixing property) or stays finite.

**Failure:** If you cannot run the SU(2) simulation for any reason, document exactly what failed and why. Partial success: 3-4 β values measured with clear interpretation.

## Technical Setup

- Use a 4⁴ lattice for all measurements (fast, sufficient for spectral gap proxy)
- SU(2) group elements as unit quaternions: (a₀, a₁, a₂, a₃) with a₀² + a₁² + a₂² + a₃² = 1
- Wilson action: S = -β Σ_{□} Re Tr(U_□) = -β Σ_{□} 2 a₀(U_□) [for SU(2) with Tr(U) = 2 a₀]
- Kennedy-Pendleton heat bath for SU(2) (already in exploration-003 code)
- Integrated autocorrelation time: τ_int = 1/2 + Σ_{t≥1} C(t)/C(0) [stop when C(t) < 0 or t > 6*τ_int]

## Output Format

1. **code/** directory with:
   - `spectral_gap_scan.py` — main script
   - `su2_utils.py` — SU(2) group operations (adapted from E003 if needed)
   - `results.json` — all numerical results

2. **REPORT.md** covering:
   - Results table (β, ⟨P⟩, τ_int, γ)
   - Plot description (or actual plot if matplotlib available)
   - Physical interpretation
   - Implications for SZZ extension strategies

3. **REPORT-SUMMARY.md** (1 page max):
   - Main result: does spectral gap appear to persist past β = 1/48?
   - Key numbers
   - Implication for the RG+Bakry-Émery idea

## Important Notes

- **Write code to files immediately** (don't run inline). Save to `code/` before running.
- **Print results as you go** — don't wait for all computations to finish before printing.
- If a particular β takes too long, skip it and note "timeout" in the results table — still report the others.
- The 4⁴ lattice is small — each β value should run in under 5 minutes total.
- **Do not spend more than 10 minutes debugging any single issue** — work around it and note the issue.
