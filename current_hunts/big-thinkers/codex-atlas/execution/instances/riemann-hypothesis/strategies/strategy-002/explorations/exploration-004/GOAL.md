# Exploration 004 — Mandatory Berry Saturation: Quantitative Comparison

## Mission Context

We are investigating the Riemann Hypothesis through random matrix theory. Previous explorations established:

1. **Spectral rigidity saturates:** Δ₃(L) for zeta zeros saturates at Δ₃ = 0.156 for L > 15 (strategy-001, exploration-002). This "super-rigidity" means zeta zeros are 30–50% more rigid than finite-size GUE random matrices at large scales.

2. **Berry (1985) predicted this:** The saturation happens because the zeta zeros come from an operator with periodic orbits associated with prime numbers. Berry gave an **explicit formula** for the predicted saturation level in terms of sums over primes.

3. **The computation was never done:** Strategy-001 confirmed saturation qualitatively but never compared the **quantitative** saturation level to Berry's prediction. The strategy-002 mandate calls this "a clean, high-value computation" and makes it mandatory.

## Your Task

**Quantitatively test Berry's prediction** for the spectral rigidity saturation level of zeta zeros.

There are two independent computations:
1. **Measure** the actual Δ₃ saturation level from zeta zeros
2. **Compute** Berry's theoretical prediction from prime sums
3. **Compare** them: do they match?

## Berry's Theory (Background)

### What is spectral rigidity?

Δ₃(L) = minimum over (a,b) of: (1/L) × ∫₀^L [N(E + x) - ax - b]² dx

where N(E) is the eigenvalue counting function (staircase). It measures how much the eigenvalue positions deviate from a perfectly equally-spaced ladder.

- **GUE (random matrix theory):** Δ₃(L) grows logarithmically: Δ₃_GUE(L) ≈ (1/π²) × [log(2πL) + γ + 1 - 8/π²] for large L
- **Poisson:** Δ₃(L) = L/15 (grows linearly)
- **Zeta zeros:** Δ₃(L) grows logarithmically at small L like GUE, but **saturates** at Δ₃_sat ≈ 0.156 for L > 15

### Berry's prediction for the saturation level

Berry (1985, "Semiclassical theory of spectral rigidity") showed that for a quantum chaotic system with classical periodic orbits, the spectral rigidity saturates at:

**Δ₃_sat = Δ₃_GUE(L_max) ≈ (1/π²) × log(L_max)**

where L_max is the scale at which the shortest periodic orbit starts contributing. For the Riemann zeros:

**L_max ∝ (1/log(2)) × (T / (2π))^{1/2}**

where T is the height of the zeros being analyzed (approximately 14 for the first zero, up to ~1500 for the first 2000 zeros).

The explicit formula involves a sum over prime powers:

**Δ₃_sat ~ (1/π²) × log(T/(2π)) + corrections from prime periodic orbits**

More precisely, Berry's eq. (3.15) or the Bogomolny-Keating (1996) formula:

**Δ₃_sat = (1/π²) × [log(L_max) + C]**

where C is a constant involving sums of the form Σ_p (log p)² / p × (...)

**Important:** The exact form of Berry's formula is in his 1985 paper. Your job is to:
1. Look up Berry's exact formula (web search for "Berry 1985 spectral rigidity saturation formula prime")
2. Implement it
3. Compare it to measured Δ₃ = 0.156

### The measured value to compare against

From strategy-001 exploration-002:
- **Δ₃ = 0.156 ± ~0.005** for L > 15 (using the first 2000 zeta zeros)
- Measurement used the Dyson-Mehta Δ₃ formula correctly in that exploration

## What to Compute

### Part 1: Accurate Δ₃ from Zeta Zeros

Compute Δ₃(L) correctly for the first 2000 zeta zeros.

**Correct Dyson-Mehta formula:**

For a set of unfolded eigenvalues {x₁, ..., x_N}, to compute Δ₃(L) at scale L:
1. Choose a window [E, E+L]
2. Count eigenvalues in window: n = number of x_i in window
3. Fit a straight line to {x_i} in the window: find a, b minimizing Σᵢ (x_i - (a·rank_i + b))²
4. Δ₃(L) = (1/L) × min_{a,b} Σᵢ_{xᵢ∈[E,E+L]} [N(xᵢ) - a·xᵢ - b]²

where the sum is over eigenvalues in the window and N(x) is the counting function (= rank of x).

**Equivalently** (and more computationally stable): For eigenvalues {y₁, ..., yₙ} in window [0, L] (shifted and sorted), the minimum least-squares fit gives:

Δ₃(L) = (n+1)/4 - (1/3n(n+1)) × Σᵢ (2i - n - 1)² × (yᵢ - ȳ)² / (Σᵢ (yᵢ - ȳ)²)

Wait — this is getting complicated. Use the direct implementation:

```python
def delta3(unfolded, L, E_start):
    """Compute Δ₃(L) starting from E_start in unfolded coordinates."""
    # Select eigenvalues in window [E_start, E_start + L]
    mask = (unfolded >= E_start) & (unfolded < E_start + L)
    ys = unfolded[mask]
    n = len(ys)
    if n < 2:
        return np.nan

    # The staircase function N(E) counts eigenvalues ≤ E
    # In the window, N(E) = number of eigenvalues in [E_start, E]
    # Rank of eigenvalue ys[i] = i+1 (1-indexed counting)
    ranks = np.arange(1, n+1)  # N(ys[i]) in the window

    # Fit: N(E) ≈ a*E + b (minimize over a, b)
    # Shifted: let x_i = ys[i] - E_start, count c_i = i
    xs = ys - E_start  # positions in [0, L]
    cs = ranks.astype(float)  # counts 1, 2, ..., n

    # Least-squares fit: minimize sum_i (c_i - a*x_i - b)^2
    A = np.column_stack([xs, np.ones(n)])
    result, _, _, _ = np.linalg.lstsq(A, cs, rcond=None)
    a, b = result

    # Residuals
    residuals = cs - (a * xs + b)

    # Δ₃(L) = (1/L) * sum of squared residuals (NOT divided by n again)
    # This is the correct Dyson-Mehta formula
    return np.sum(residuals**2) / L
```

Average over many windows (100+) starting at different E_start values.

### Part 2: Berry's Theoretical Prediction

Search for and implement Berry's (1985) formula for Δ₃_sat.

Key facts from Berry's paper (as best understood from the literature):

The saturation level is reached at L_max ~ T/(2π) where T is the characteristic height of the zeros. For the GUE, the form factor K(τ) transitions from ramp (K = τ) to plateau (K = 1) at τ = 1 (or time t = 1). For the Riemann zeros, the transition happens earlier due to the discrete prime orbit structure.

Berry's key result (equation to look up): The spectral rigidity saturates at a value:

**Δ₃_sat = (1/π²) × log(T/(2π)) × (some constant)**

or more precisely, involving the prime sum:

**Δ₃_sat = Δ₃_GUE(L_max) where L_max ≈ T^{1/2}/(2π)**

The exact formula depends on whether we're looking at the "universal" part or the "non-universal" corrections from short orbits.

**What to do:**
1. Web search: "Berry 1985 Proc Royal Soc spectral rigidity Riemann zeros saturation formula"
2. Find the exact formula for Δ₃_sat in terms of T (height of zeros)
3. Compute for T ≈ geometric mean of first 2000 zeros (T_geo ≈ exp((1/N) Σ log t_n))
4. Compare to measured Δ₃ = 0.156

### Part 3: Height-Resolved Analysis

Split the 2000 zeros into height bins and compute Δ₃ separately for each bin:
- Bin 1: zeros 1-500 (heights 14–307)
- Bin 2: zeros 501-1000 (heights 307–631)
- Bin 3: zeros 1001-1500 (heights 631–989)
- Bin 4: zeros 1501-2000 (heights 989–1378)

For each bin:
- Compute geometric mean height T_bin
- Compute measured Δ₃ saturation value
- Compute Berry's predicted saturation for that T_bin

Does the saturation level INCREASE with height as Berry predicts?

### Part 4: Numerical Form Factor (connection to Berry's prediction)

Berry's saturation result follows from the form factor K(τ):
- Δ₃(L) = (4/π⁴) ∫ sin²(πLτ)/(τ²) × [1 - K(τ)] dτ + (log 2πL)/(π²) + ...

Computing K(τ) from actual zeros was done in strategy-001 (K(τ) ≈ min(τ,1) to within 1-4%).

Use this form factor formula to compute Δ₃_predicted_from_K(τ) and compare to directly computed Δ₃.

This tests whether the form factor and rigidity are consistent (they should be).

## Verification Protocol

Tag all results:
- [COMPUTED]: numerical result from code
- [CHECKED]: cross-checked against published value (strategy-001 says Δ₃ = 0.156)
- [CONJECTURED]: interpretation without direct verification

## Success Criteria

**Primary success:** Berry's formula predicts Δ₃_sat within 20% of the measured 0.156.
**Secondary success:** The height-resolved analysis shows Δ₃_sat increasing with height (consistent with Berry's T^{1/2} prediction).
**Interesting failure:** Berry's formula significantly disagrees with measured values — this would mean either the formula is approximate or our N=2000 zeros aren't asymptotic enough.

## Reuse of Prior Data

Strategy-001 exploration-002 already computed 2000 zeta zeros. Check if they're saved:
- Try: `np.load('code/zeta_zeros_2000.npy')` in the exploration-003 code directory
  Path: `/Users/seanross/.../strategies/strategy-002/explorations/exploration-003/code/zeta_zeros_2000.npy`

If not available, compute 2000 zeros with mpmath (~6 minutes).

## Exploration Directory

Your exploration directory is:
`/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/riemann-hypothesis/strategies/strategy-002/explorations/exploration-004/`

Write all scripts to `code/` subdirectory. Write REPORT.md incrementally as you complete each part. Write REPORT-SUMMARY.md **last** — this signals you are finished.

## Computation Time Budget

~15-20 minutes total. Break down:
- Zero computation (if needed): 6 minutes for 2000 zeros
- Δ₃ computation from zeros: 3 minutes
- Berry formula lookup + implementation: 5 minutes
- Height-resolved analysis: 3 minutes
- Report writing: 5 minutes
