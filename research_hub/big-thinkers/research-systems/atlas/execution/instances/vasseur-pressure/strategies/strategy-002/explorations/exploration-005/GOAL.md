<!-- explorer-type: math -->

# Exploration 005: Frequency-Localized De Giorgi via Littlewood-Paley Decomposition

## Goal

Determine whether a Littlewood-Paley (LP) frequency decomposition of the De Giorgi pressure P^{21} can bypass the β = 4/3 barrier by applying stronger (commutator-type) estimates on low-frequency modes and accepting standard CZ estimates on high-frequency modes. The key hypothesis: if the high-frequency contribution is subdominant in the De Giorgi recurrence, the improved low-frequency bound could raise the effective β.

## Background

### Why frequency localization might work

Strategy-002 exploration-004 (commutator analysis) found:

1. **The commutator part of P^{21} has genuinely better high-frequency regularity** — spectral ratio of commutator to full P^{21} drops from 0.67 at low Fourier modes to 0.09 at mode k=20. The commutator structure IS present; it's just negated by the divergence-error remainder.

2. **The divergence error concentrates at HIGH frequencies.** div(u^below) = -λ(u·∇|u|)/|u|², which involves ∇|u| — a derivative term that peaks at high frequencies. This means:
   - Low-frequency P^{21} ≈ commutator (good regularity)
   - High-frequency P^{21} ≈ divergence-error remainder (bad, but maybe small)

3. **β = 4/3 is sharp within energy+Sobolev+CZ+Chebyshev.** But LP decomposition goes BEYOND this class — it uses frequency-dependent estimates, which standard CZ does not.

### The idea

Split P^{21} using LP projectors: P^{21} = P^{21}_{lo} + P^{21}_{hi} where:
- P^{21}_{lo} = Σ_{j ≤ J} Δ_j P^{21} (low modes, frequency ≤ 2^J)
- P^{21}_{hi} = Σ_{j > J} Δ_j P^{21} (high modes, frequency > 2^J)

For P^{21}_{lo}: use commutator/Hardy space estimates (which E004 showed work at low frequencies)
For P^{21}_{hi}: use standard CZ (β = 4/3), but if the contribution is small enough (e.g., decays with J), the overall recurrence might improve.

The cutoff J may depend on the De Giorgi level k — this is allowed and potentially powerful.

### What could go wrong

1. The high-frequency contribution might NOT be subdominant — it could be O(1) for all J
2. The LP decomposition might not commute well with the De Giorgi truncation
3. The improved low-frequency estimate might not produce a better U_{k-1} exponent after Hölder pairing
4. Bernstein inequalities relating LP blocks to L^p norms might eat up any frequency-localized gain

## Specific Computation Tasks

### Task 1: Set up the LP decomposition of P^{21} analytically

Write P^{21} = R_iR_j(u_i^{below} · u_j^{above}) and apply standard LP decomposition:

Δ_j P^{21} = Δ_j R_iR_j(u_i^{below} · u_j^{above})

Using paraproduct decomposition (Bony 1981):
u_i^{below} · u_j^{above} = T_{u^{below}} u^{above} + T_{u^{above}} u^{below} + R(u^{below}, u^{above})

where T is the paraproduct and R is the remainder. Analyze each piece:
- T_{u^{below}} u^{above}: low-high interaction. u^{below} is smooth (below threshold), so this is well-controlled.
- T_{u^{above}} u^{below}: high-low interaction. u^{above} is rough (above threshold).
- R(u^{below}, u^{above}): resonance term.

For each piece, determine:
1. What LP-block estimates are available?
2. Does any piece have better regularity than CZ predicts?
3. Can the paraproduct structure give k-dependent improvement?

### Task 2: Estimate the bottleneck integral with LP splitting

The bottleneck integral is:
I_k = ∫∫ P^{21}_k · v_k · 1_{v_k > 0} dx dt

Split into:
I_k = I_k^{lo}(J) + I_k^{hi}(J)

For I_k^{lo}(J): Apply the best available estimate using commutator / paraproduct structure.
For I_k^{hi}(J): Apply standard CZ.

**Key computation:** For a given J (possibly k-dependent), what is the resulting bound on I_k in terms of U_{k-1}? Specifically:
- I_k^{lo}(J) ≤ ? × U_{k-1}^{β_lo}
- I_k^{hi}(J) ≤ ? × U_{k-1}^{β_hi}

If β_lo > 4/3 and the β_hi = 4/3 term is subdominant, we win.

### Task 3: Numerical verification on DNS data

Using the Strategy-001 DNS infrastructure (`../strategy-001/explorations/exploration-002/code/`):

1. **Compute P^{21} in Fourier space** for Taylor-Green at Re = 500 or 1000:
   - Apply LP projectors (dyadic frequency shells) to P^{21}
   - Measure ||Δ_j P^{21}||_{L^2} as a function of j
   - Separately measure ||Δ_j (commutator part)||_{L^2} and ||Δ_j (div-error part)||_{L^2}

2. **Compute the bottleneck integral split:**
   - I_k^{lo}(J) and I_k^{hi}(J) for several values of J and De Giorgi levels k = 1,...,8
   - Determine the optimal J(k) that minimizes the total bound
   - Does I_k^{hi}(J(k)) / I_k decay with k? With J?

3. **Test the paraproduct decomposition numerically:**
   - Compute T_{u^{below}} u^{above}, T_{u^{above}} u^{below}, R(u^{below}, u^{above})
   - Which piece dominates? Does the dominant piece have better estimates?

### Task 4: Assess viability and compute β_eff

Based on Tasks 1-3:

1. **If improvement found:** Trace through the full De Giorgi chain. What β does the frequency-localized estimate give? Is it β > 4/3? If so, by how much? Does it depend on the choice of J? Is it uniform in k?

2. **If no improvement:** Identify precisely why. Options:
   - Bernstein inequalities eat up the frequency gain (LP blocks in L^p have Bernstein factors 2^{jn(1/2-1/p)})
   - The high-frequency contribution is NOT subdominant
   - The paraproduct structure doesn't give k-dependent improvement
   - The LP decomposition doesn't commute with De Giorgi truncation in a useful way

3. **Compare with known LP-based regularity results for NS.** Have Chemin, Bahouri-Chemin-Danchin, or others used LP-based De Giorgi methods? If so, what did they achieve? If not, is there a structural reason?

## Success Criteria

1. Analytical paraproduct decomposition of P^{21} with estimates for each piece [REQUIRED]
2. Numerical measurement of ||Δ_j P^{21}||_{L^2} spectrum and bottleneck integral split [REQUIRED]
3. Assessment of whether I_k^{hi}(J)/I_k decays with J or k [REQUIRED]
4. Clear verdict: does frequency localization improve β? If yes, by how much? If no, why exactly? [REQUIRED]

## Failure Criteria

- Only describing the LP decomposition without computing the actual estimates
- No numerical verification
- Missing the Bernstein inequality check (this is the most likely "poison pill")

## Key References

- Bony (1981): "Calcul symbolique et propagation des singularités" — paraproduct decomposition
- Bahouri, Chemin, Danchin: "Fourier Analysis and Nonlinear Partial Differential Equations" — LP techniques for fluid PDEs
- Caffarelli-Vasseur (2010): SQG success via frequency-aware methods
- Strategy-002 E004: commutator spectral analysis (spectral ratio data)
- Strategy-001 code: `../strategy-001/explorations/exploration-002/code/`

## Important Notes

- **Tag all results** with [VERIFIED], [COMPUTED], [CHECKED], [CONJECTURED].
- **Bernstein is the key check.** LP block estimates satisfy ||Δ_j f||_{L^p} ≤ C 2^{jn(1/q - 1/p)} ||Δ_j f||_{L^q} for p > q. This factor can negate any frequency-localized improvement. Compute it explicitly.
- **The cutoff J should be optimized.** Try J = k (matching LP scale to De Giorgi level), J = αk for various α, and fixed J. The optimal choice may be k-dependent.
- **Worst-case discipline.** Any improvement must work analytically, not just on DNS. DNS serves as a diagnostic tool to identify whether the frequency structure supports the analytical approach.
- **Reuse existing code.** Extend the Strategy-001 spectral solver. Computing LP projectors in Fourier space is trivial (frequency-shell masking).
