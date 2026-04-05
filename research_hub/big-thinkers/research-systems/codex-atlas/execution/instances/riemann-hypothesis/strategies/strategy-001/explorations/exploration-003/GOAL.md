# Exploration 003: Berry-Keating xp Operator — Spectrum Computation and Constraint Testing

## Mission Context

We are investigating the spectral approach to the Riemann Hypothesis. The Hilbert-Polya conjecture says the non-trivial zeta zeros are eigenvalues of an undiscovered self-adjoint operator. Berry and Keating (1999) conjectured that this operator is a quantization of the classical Hamiltonian H = xp (position times momentum).

In Phase 1 (explorations 001-002), we established a 10-point constraint catalog from numerical analysis of the first 2000 zeta zeros:

**Constraint Catalog:**
1. GUE symmetry class (beta=2) — no time-reversal symmetry
2. Pair correlation matches Montgomery R2 = 1 - (sin(pi*r)/(pi*r))^2 to 9%
3. NN spacing matches GUE Wigner surmise to 4%
4. Poisson, GOE definitively ruled out; GSE disfavored 1.2x
5. Quadratic level repulsion P(s) ~ s^2 for small s
6. Number variance Sigma^2(L) saturates at ~0.3-0.5 for L > 2
7. Spectral rigidity Delta_3(L) saturates at 0.156 for L > 15
8. Spectral form factor ramp slope = 1.010, plateau = 1.043
9. Super-rigidity: zeros 30-50% more rigid than finite-size GUE at large L
10. Periodic orbit structure related to primes (saturation encodes prime orbit sums)

## Your Task

**This is a COMPUTATION task. Write Python code, execute it, report numerical results. Do NOT do web research — all information you need is provided below.**

**Computation time budget: ~8 minutes total. You may need to compute new zeta zeros AND the operator spectrum.**

### Part 1: Berry-Keating xp Regularizations — Compute Spectra

The raw operator H = xp has continuous spectrum on the real line. To get a discrete spectrum comparable to zeta zeros, regularization is needed. Test the following approaches:

#### Approach A: Sierra-Townsend Regularization (2008)

Sierra and Townsend proposed the Hamiltonian:
H = (1/2)(xp + px) with the boundary condition that eigenfunctions vanish at x = l_p (a Planck-scale cutoff).

On the half-line x > 0, with boundary condition psi(l_p) = 0, the operator (1/2)(xp + px) = -i(x d/dx + 1/2) has eigenfunctions:
psi_E(x) = x^{-1/2 + iE} (unnormalized)

The boundary condition psi(l_p) = 0 gives: l_p^{-1/2 + iE} = 0, which has no solution.

Instead, Sierra-Townsend use a COMPACT space: x in [l_p, L] with boundary conditions at BOTH ends. The eigenvalue condition becomes:
L^{iE} = l_p^{iE}   →   E * ln(L/l_p) = 2*pi*n

So E_n = 2*pi*n / ln(L/l_p)

This gives EQUALLY SPACED eigenvalues, which is trivially NOT the zeta zeros. But it's the starting point — deviations from this regular spectrum are what matters.

**What to compute:**
1. Set ln(L/l_p) = 2*pi (so E_n = n, giving unit mean spacing)
2. Generate the first 2000 eigenvalues: E_n = n for n = 1, 2, ..., 2000
3. Compute pair correlation and NN spacing for these eigenvalues
4. Report: these are Poisson-like (equally spaced → delta function spacing distribution)
5. **Score against constraint catalog** — how many of the 10 constraints does this satisfy? (Answer: essentially none, since equally spaced is far from GUE)

#### Approach B: Bender-Brody-Mueller (BBM) PT-Symmetric Operator (2017)

BBM proposed:
H = (1 - e^{-ip})(xp + px)(1 - e^{ip})

They conjectured this has eigenvalues at the Riemann zeros (under certain conditions). However, this operator is PT-symmetric, not self-adjoint in the usual sense.

The BBM conjecture has been disputed. Rather than proving/disproving it, **compute the spectrum numerically by matrix approximation:**

1. Represent the operator in a truncated basis (e.g., harmonic oscillator basis |n>, n = 0, 1, ..., N-1)
2. Compute matrix elements <m|H|n> numerically (requires matrix elements of x, p, e^{ip})
3. In the harmonic oscillator basis:
   - x = sqrt(1/2) (a + a†),  p = i*sqrt(1/2) (a† - a)
   - xp = (i/2)(a†a† - aa + a†a - aa†) ... work out or use numerical integration
4. Diagonalize the truncated matrix
5. Examine the eigenvalues

**If this is too complex**, fall back to:

#### Approach C: Connes' Absorption Spectrum (1999, simplified numerical version)

Alain Connes proposed that the zeta zeros appear as an ABSORPTION spectrum: they are the missing eigenvalues of a larger operator. A simplified numerical model:

1. Consider the operator H acting on L^2(R+): (Hf)(x) = x*f(x)
2. The "trace formula" connects the spectrum to: sum_n h(E_n) = integral h(E) dN(E) + sum_p sum_m (log p) h(m*log p) / p^{m/2}
3. Instead of implementing the full Connes framework, test a SIMPLER question: if we construct a matrix whose eigenvalues ARE the first N zeta zeros, what are its matrix properties?

**Construct a zeta zero matrix:**
1. Compute the first 200 zeta zeros t_1, ..., t_200 using mpmath
2. Construct a diagonal matrix D = diag(t_1, ..., t_200) — this trivially has the right eigenvalues
3. Now randomize: apply random unitary rotations U*D*U† where U is drawn from GUE
4. This creates a matrix with the EXACT zeta zero spectrum but random eigenvectors
5. Compare the statistical properties of this matrix to a pure GUE matrix of the same size

### Part 2: Constraint Testing

For whichever approach(es) produce a nontrivial spectrum:

1. **Unfold the eigenvalues** (determine the smooth density and rescale to unit mean spacing)
2. **Compute pair correlation R2(r)** and compare to Montgomery's conjecture
3. **Compute NN spacing P(s)** and compare to GUE Wigner surmise
4. **If possible, compute number variance Sigma^2(L)**
5. **Score against the constraint catalog:** For each of the 10 constraints, report PASS/FAIL/PARTIAL with a quantitative measure of deviation

### Part 3: Assessment

Based on your results:
1. Which approach comes closest to matching the zeta zero statistics?
2. What are the SPECIFIC constraints that each approach fails, and by how much?
3. Is there a modification to any approach that could fix the failures?
4. What properties would a successful operator need that the tested candidates lack?

## Success Criteria
- At least two approaches attempted with numerical eigenvalue computation
- Each approach's spectrum tested against at least 3 constraints from the catalog
- A quantitative scorecard showing which constraints each approach passes/fails
- A clear statement of what's missing from the best candidate

## Failure Criteria
- If the BBM operator matrix elements are too hard to compute, skip to Approach C
- If any computation takes >5 minutes, abort and report partial results
- If mpmath is needed, `pip install mpmath numpy scipy` first

## Output
Write detailed report to:
`/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-001/explorations/exploration-003/REPORT.md`

Write summary (under 80 lines) to:
`/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/riemann-hypothesis/strategies/strategy-001/explorations/exploration-003/REPORT-SUMMARY.md`

Target report length: 300-500 lines.
