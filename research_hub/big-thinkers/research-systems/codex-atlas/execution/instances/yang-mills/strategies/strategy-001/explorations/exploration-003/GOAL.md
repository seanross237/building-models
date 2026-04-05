# Exploration 003: SU(2) Lattice Gauge Theory — Mass Gap Observables

## Mission Context

This is a YANG-MILLS mission investigating the Millennium Prize Problem on Yang-Mills existence and mass gap. Prior explorations established:
- UV stability of 4D lattice YM is achieved (Balaban's program)
- The UV problem for 4D YM is solved (Magnen-Rivasseau-Sénéor 1993)
- The entire difficulty is in the IR: confinement, mass gap, infinite volume
- The constructive QFT toolkit breaks at d=4 due to dimensionless coupling
- Asymptotic freedom should prevent triviality but no rigorous proof exists

## Your Task

**Implement SU(2) Wilson lattice gauge theory in 4D from scratch and compute mass gap observables.** This is a computational exploration — you MUST write and execute code. No reasoning-only work.

## Specific Deliverables

### 1. Lattice gauge theory implementation
Implement a Monte Carlo simulation of SU(2) lattice gauge theory in 4D with:
- Wilson plaquette action: S = β Σ_P (1 - (1/2)Re Tr U_P) where U_P is the plaquette
- SU(2) gauge links represented as 2×2 unitary matrices
- Heat bath or Metropolis algorithm for updates
- Parameters: lattice sizes from 4⁴ to at least 12⁴ (or 16⁴ if feasible), β values from 1.5 to 3.0

Use Python with numpy/scipy. Focus on correctness and reproducibility over speed.

### 2. Wilson loop measurements (confinement test)
Compute rectangular Wilson loops W(R,T) for various R and T:
- Extract the static quark potential V(R) from W(R,T) ~ exp(-V(R)T) at large T
- Test for area law vs. perimeter law: V(R) ~ σR (confinement) vs. V(R) → const (screening)
- Compute the string tension σ from the slope of V(R)
- Compute Creutz ratios χ(R,T) = -ln(W(R,T)W(R-1,T-1)/(W(R-1,T)W(R,T-1))) which give σ in the confined phase

### 3. Glueball mass estimate
From the correlation function of gauge-invariant operators:
- Measure the plaquette-plaquette correlator at different Euclidean time separations
- Extract the mass of the lightest glueball from exponential decay: C(t) ~ exp(-m₀t)
- The glueball mass m₀ IS the mass gap
- Report m₀ in lattice units for several β values
- If possible, estimate how m₀ scales with β (related to continuum limit)

### 4. Scaling analysis
- Plot observables vs. β (inverse coupling)
- Check for scaling behavior consistent with asymptotic freedom: a(β) ~ exp(-β/(4b₀)) for SU(2) where b₀ = 11/(12π²) × 2 for SU(2)
- The mass gap in physical units should remain finite as β → ∞ (continuum limit) if the mass gap exists

### 5. Connection to the rigorous problem
For each numerical result, state:
- What this computation demonstrates about the mass gap
- What would need to be proved rigorously to turn this into a mathematical theorem
- Where the gap is between the numerical evidence and a proof

## Success Criteria
- Working lattice gauge theory code that runs and produces results
- Wilson loop measurements showing area law (confinement) for at least 2 β values
- A glueball mass estimate for at least 2 β values
- Creutz ratios computed and showing approach to a constant (string tension)
- All results with error estimates
- Clear statement of what the computation proves vs. what it merely suggests

## Failure Criteria
- Code doesn't run or produces nonsensical results
- No error estimates
- No connection made between numerical results and the rigorous problem

## Technical Notes
- For SU(2), you can parameterize group elements as a₀I + i(a₁σ₁ + a₂σ₂ + a₃σ₃) with a₀² + a₁² + a₂² + a₃² = 1
- Heat bath for SU(2) is well-known (Creutz/Kennedy-Pendleton algorithm)
- Start with small lattices (4⁴) for debugging, then go larger for physics
- Use at least 1000 thermalization sweeps and 5000+ measurement sweeps
- Typical β values for SU(2) in 4D: β = 2.0-3.0 for confined phase near continuum

## Output
Write results to:
- `REPORT.md` in this directory (target 400-600 lines, include code snippets and numerical tables)
- `REPORT-SUMMARY.md` — concise summary (50-100 lines)
- Save complete runnable code in a `code/` subdirectory

Write REPORT-SUMMARY.md as your FINAL action.
