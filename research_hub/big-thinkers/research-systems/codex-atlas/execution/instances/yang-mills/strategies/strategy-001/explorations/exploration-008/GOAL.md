# Exploration 008: Transfer Matrix Spectral Gap and Adhikari-Cao Bound Analysis

## Mission Context

This is a YANG-MILLS Millennium Prize Problem mission. We have:
- SU(2) lattice gauge theory code that confirms confinement numerically (exploration 003)
- Finite group convergence data showing 2I (120 elements) matches SU(2) to <0.5% (exploration 005)
- Adhikari-Cao (2025) proves mass gap for finite gauge groups with bound β ≥ (114 + 4log|G|)/Δ_G
- The spectral gap Δ_G of the Laplacian on the finite group matters critically

## Your Task

**Two computational tasks:**

### Task A: Transfer Matrix Spectral Gap

The mass gap in lattice gauge theory is mathematically equivalent to the spectral gap of the transfer matrix. For small lattices, the transfer matrix can be explicitly constructed and its eigenvalues computed.

**Compute the spectral gap of the transfer matrix for SU(2) lattice gauge theory on small spatial volumes.**

Specifically:
1. For a 2³ or 3³ spatial lattice with gauge group SU(2) (or a finite subgroup for tractability):
   - Construct the transfer matrix T (or approximate it using stochastic methods)
   - Compute the ratio λ₂/λ₁ (second-largest to largest eigenvalue)
   - The mass gap is m = -ln(λ₂/λ₁)
2. Do this for multiple β values (1.0, 2.0, 2.5, 3.0)
3. For finite groups, the Hilbert space is finite → exact diagonalization may be feasible
4. Even for 2³ spatial volume with 2T (24 elements), the state space is 24^{3×2³} = 24^24 which is too large for exact diag. So use Monte Carlo estimation of the spectral gap via autocorrelation time (τ_int ≈ 1/mass_gap) or correlation function decay.

### Task B: Adhikari-Cao Bound Analysis

Quantitatively analyze how the Adhikari-Cao mass gap bound degenerates as the finite group approaches SU(2):

1. **Compute the spectral gap Δ_G** for the Laplacian on each binary polyhedral subgroup:
   - 2T (24 elements)
   - 2O (48 elements)
   - 2I (120 elements)

   The Laplacian on a finite group G ⊂ SU(2) can be defined via the character-theoretic distance. For matrix groups: L f(g) = Σ_{g' ∈ S} (f(g) - f(g')) where S is a generating set. The spectral gap is the smallest nonzero eigenvalue.

2. **Plug Δ_G into the Adhikari-Cao bound**: β_min = (114 + 4log|G|)/Δ_G. How does β_min scale with |G|?

3. **Compare β_min to our measured β_c**: Is Adhikari-Cao's bound consistent with where we see confinement/mass gap?

4. **Extrapolate**: As |G| → ∞ (approaching SU(2)), does β_min → ∞ (bound becomes vacuous) or does it converge to a finite value?

## Success Criteria
- Spectral gap Δ_G computed for at least 2 finite subgroups
- Adhikari-Cao β_min bound computed for each group
- Scaling of β_min with |G| characterized
- Mass gap estimate from autocorrelation time or correlation decay for at least 2 β values
- All numerical results with error estimates
- Tag all claims as VERIFIED/COMPUTED/CHECKED/CONJECTURED

## Failure Criteria
- Code doesn't run
- No connection made between Adhikari-Cao bounds and our data
- No error estimates

## Output
- `REPORT.md` (target 300-500 lines)
- `REPORT-SUMMARY.md` (50-100 lines)
- Save code in `code/` subdirectory

Write REPORT-SUMMARY.md as your FINAL action.
