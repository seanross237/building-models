# Exploration 005: Finite Group Approximation of SU(2) — Mass Gap Convergence

## Mission Context

This is a YANG-MILLS Millennium Prize Problem mission. We've established:
- UV stability solved (Balaban, MRS 1993). The difficulty is entirely IR (confinement, mass gap).
- Adhikari-Cao (2025) proved mass gap for FINITE gauge groups at weak coupling.
- The finite-to-continuous gauge group transition is the single most important bottleneck.
- SU(2) lattice gauge theory numerically confirms confinement and mass gap at all couplings studied (our exploration 003).

## Your Task

**Computationally test whether mass gap properties converge as finite subgroups of SU(2) approach SU(2) itself.** This is a Math Explorer task — you MUST write and run code.

## Background

SU(2) has a sequence of finite subgroups with increasing size:
- **Z_n** (cyclic groups, order n) — abelian, simplest
- **Binary dihedral groups** 2D_n (order 4n)
- **Binary tetrahedral group** 2T (order 24)
- **Binary octahedral group** 2O (order 48)
- **Binary icosahedral group** 2I (order 120) — the largest exceptional finite subgroup of SU(2)

For larger groups: the *point groups* of regular lattices in SU(2) can approximate SU(2) arbitrarily well. For practical computation, one can also use subgroups of SU(2) defined by discretizing the 3-sphere into N equally-spaced points (ZN subgroups don't work well, but there are constructions based on Fibonacci lattices on S³ that give better approximations).

Adhikari-Cao's theorem applies to lattice gauge theories with finite gauge groups. If the mass gap they prove converges to a positive value as the finite group → SU(2), this would provide evidence that the continuous mass gap should exist.

## Specific Deliverables

### 1. Implement lattice gauge theory for finite subgroups of SU(2)

Using the code structure from our exploration 003 as reference, implement:
- Lattice gauge theory with gauge group G where G is a finite subgroup of SU(2)
- Links are elements of G (finite set → can enumerate exactly)
- Wilson plaquette action: S = β Σ_P (1 - (1/2)Re Tr U_P) — same as SU(2) but with U_P ∈ G
- Heat bath algorithm adapted for finite groups (can do exact sampling from discrete distribution)
- Measure: average plaquette, Wilson loops, string tension, Polyakov loop

Start with:
- **2T** (order 24): the binary tetrahedral group
- **2O** (order 48): the binary octahedral group
- **2I** (order 120): the binary icosahedral group
- **SU(2)** (continuous): for comparison

### 2. Mass gap observables for each group

For each finite group, at multiple β values:
- Compute the string tension σ(G, β) from Creutz ratios
- Compute the average plaquette ⟨P⟩(G, β)
- Check for confinement (area law in Wilson loops)
- If possible, estimate glueball mass from correlators

### 3. Convergence analysis

The key question: **As |G| → ∞ (groups approximating SU(2) better), do the mass gap observables converge to the SU(2) values?**

Plot:
- σ(G, β) vs. 1/|G| at fixed β — does it extrapolate to σ(SU(2), β)?
- ⟨P⟩(G, β) vs. 1/|G| — does it converge to the SU(2) value?
- Phase structure: is there a deconfinement transition for each G? If so, does the critical β converge?

### 4. Connection to Adhikari-Cao

State (even if you haven't read their paper):
- What this computation implies about extending finite-group mass gap proofs to SU(2)
- Whether the convergence pattern suggests the barrier is fundamental or technical
- What rate of convergence would be needed for a rigorous argument

## Success Criteria
- Working code for at least 2 finite subgroups (2O and 2I minimum)
- Quantitative comparison of mass gap observables between finite groups and SU(2)
- A convergence plot or table showing how observables evolve with group size
- Error estimates on all numerical results
- Clear statement about what the convergence (or lack thereof) implies

## Failure Criteria
- Code doesn't run
- Only one finite group studied (need at least 2 for convergence analysis)
- No comparison to SU(2)

## Technical Notes
- For a finite group G ⊂ SU(2), represent elements as 2×2 matrices. Precompute and store the multiplication table.
- Heat bath for finite groups is simpler than for SU(2): compute the local Boltzmann weight for each group element and sample from the discrete distribution.
- Use lattice size 4⁴ or 6⁴ (finite groups make the computation faster since there's no rejection).
- β values: 1.0 to 4.0 to explore the full phase diagram.

## Output
- `REPORT.md` (target 400-600 lines)
- `REPORT-SUMMARY.md` (50-100 lines)
- Save code in `code/` subdirectory
- Tag all claims as VERIFIED/COMPUTED/CHECKED/CONJECTURED

Write REPORT-SUMMARY.md as your FINAL action.
