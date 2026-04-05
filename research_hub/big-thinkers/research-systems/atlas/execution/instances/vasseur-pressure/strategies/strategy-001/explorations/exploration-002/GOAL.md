<!-- explorer-type: math -->

# Exploration 002: Measure Empirical Beta from DNS via De Giorgi Iteration

## Goal

Implement the De Giorgi level-set iteration on 3D Navier-Stokes DNS data and measure the empirical recurrence exponent β_effective. This is the central measurement of the mission.

## Background: What Beta Is

From Vasseur (2007, NoDEA), Proposition 3: the De Giorgi iteration for NS gives a recurrence:

```
U_k ≤ C_p^k · (1 + ||P||_{L^p(L^1)}) · U_{k-1}^{β_p}
```

where:
- `U_k = sup_t ∫ v_k² dx + ∫∫ d_k² dx dt` (energy on level sets)
- `v_k = [|u| - (1 - 2^{-k})]_+` (truncated velocity magnitude)
- `d_k² = (v_k/|u|)|∇|u||² + ((1-2^{-k})·1_{|u|≥1-2^{-k}}/|u|)|∇u|²`
- β_p is the RECURRENCE EXPONENT — the minimum over all terms' exponents of U_{k-1}

**Current analytical bound:** β < 4/3 (strictly), limited by a SINGLE term — the non-divergence part of the local pressure P_k^{21}.

**Target:** If β > 3/2, ALL suitable weak solutions are regular (Conjecture 14 + Appendix proof).

**Key question:** What is β_effective on actual NS solutions? The analytical bound is worst-case. If DNS shows β_effective >> 4/3, there is exploitable slack.

## Specific Tasks

### Task 1: Implement the De Giorgi Level-Set Computation

Adapt for periodic domain T³ = [0, 2π]³ (no nested balls — use full domain):

1. Run pseudospectral DNS to generate velocity and pressure fields at multiple time snapshots
2. Normalize so that U_0 ≤ 1 (rescale by energy + gradient norm)
3. For k = 0, 1, ..., K_max (aim for K_max = 10-12):
   - Compute v_k = [|u_normalized| - (1 - 2^{-k})]_+
   - Compute d_k² with the full formula (both terms, including the gradient of |u| and the gradient of u)
   - Compute U_k = sup_t ∫ v_k² dx + ∫∫ d_k² dx dt
4. Fit: log(U_k) = a·k + β · log(U_{k-1}) via linear regression for k = 2, ..., K_max
5. Report β_effective with error bars (from regression)

### Task 2: Run Across Multiple ICs and Reynolds Numbers

**Initial conditions (minimum 5):**
- Taylor-Green vortex: u = (sin(x)cos(y)cos(z), -cos(x)sin(y)cos(z), 0)
- Anti-parallel vortex tubes: two counter-rotating tubes with Gaussian core
- Random Gaussian: random Fourier modes with k^{-5/3} spectrum, projected to div-free
- Kida vortex: symmetric vortex in T³
- Arnold-Beltrami-Childress flow: u = (B·sin(y) + C·cos(z), C·sin(z) + A·cos(x), A·sin(x) + B·cos(y)) with A=B=C=1

**Reynolds numbers (minimum 3):** Re = 100, 500, 1000 (use Re = 2000, 5000 if computational budget allows)

**Resolution:** N = 64 primary, with at least one convergence check at N = 128

**Output table format:**
| IC | Re | N | β_effective | std_err | K_max used | U_0 | U_{K_max} | Converged? |
|---|---|---|---|---|---|---|---|---|

### Task 3: Measure the Bottleneck Integral Separately

For each DNS run, also compute the bottleneck integral that limits β:

```
I_k = ∫∫ |P_k^{21}| · |d_k| · 1_{v_k > 0} dx dt
```

where P_k^{21} is the local non-divergence pressure piece:
```
-ΔP_k^{21} = Σ_{i,j} ∂_i∂_j [u_j(1-v_k/|u|) · u_i(1-v_k/|u|)]
```

Note: On a periodic domain, solve this Poisson equation spectrally. The factors u_i(1-v_k/|u|) are bounded by 1 (this is key — Vasseur's Lemma 10).

Fit: log(I_k) vs log(U_{k-1}) to extract the bottleneck exponent. The theoretical prediction is 4/3 - 5/(3q) → 4/3. If the empirical exponent exceeds 4/3, the bottleneck has exploitable slack.

### Task 4: Convergence and Sanity Checks

- Verify U_0 ≤ 1 after normalization
- Verify U_k is monotonically decreasing (should be for well-behaved DNS)
- Plot log(U_k) vs k for each IC/Re combination — it should be approximately linear with slope related to β
- Compare N=64 and N=128 results: β_effective should be consistent within error bars
- Cross-check: the energy equality (dissipation = -dE/dt for viscous flows) should hold

## Prior DNS Code

A pseudospectral NS solver exists at:
`/Users/seanross/kingdom_of_god/home-base/research_hub/big-thinkers/research-systems/atlas/execution/instances/navier-stokes/strategies/strategy-001/explorations/exploration-002/code/ns_solver.py`

This is a fully working 3D spectral solver on T³ with RK4, 2/3 dealiasing, and adaptive CFL. You may reuse or rewrite it. The solver class is `NavierStokesSolver` with methods: `to_spectral`, `to_physical`, `compute_rhs`, `step`, `run`.

## Success Criteria

✅ **Success:**
- β_effective measured for ≥ 5 ICs × ≥ 3 Re values
- Convergence check (N=64 vs N=128) on at least 2 ICs
- Bottleneck integral exponent measured separately
- Clear determination: β_effective < 4/3 (tight) or β_effective > 4/3 (slack exists) or β_effective > 3/2 (dramatic)
- All values tagged [VERIFIED] with code that produced them

❌ **Failure modes:**
- U_k doesn't decrease monotonically → check normalization, check that DNS is resolved
- β_effective varies wildly across ICs → report the distribution, identify which IC property matters
- Can't fit a clean recurrence → U_k might not follow a power-law; report the raw U_k sequences

## Output Format

Structure report as: Implementation Details → Results Table → Bottleneck Analysis → Convergence Checks → Interpretation. Include ALL code. Tag every numerical value as [VERIFIED] (code ran and produced it), [COMPUTED] (derived from verified values), or [CONJECTURED].
