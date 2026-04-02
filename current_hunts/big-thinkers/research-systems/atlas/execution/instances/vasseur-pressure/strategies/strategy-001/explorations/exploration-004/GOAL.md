<!-- explorer-type: math -->

# Exploration 004: CZ Slack on the De Giorgi Pressure Decomposition

## Goal

Decompose the NS pressure into the De Giorgi pieces (P_k^1, P_k^{21}, P_k^{22}, P_k^{23}) on DNS data and measure the Calderón-Zygmund tightness ratio for each piece separately. Determine whether the previously observed CZ near-tightness (7.6-17.5× on full pressure) persists for the specific bottleneck piece P_k^{21}.

## Background: Why This Matters

In Vasseur (2007)'s De Giorgi iteration for NS regularity, the recurrence exponent β is limited by a SINGLE term involving the non-divergence local pressure P_k^{21}. The analytical bound gives β < 4/3 because:

1. CZ theory bounds ||P_k^{21}||_{L^q} ≤ C_q (a CONSTANT, independent of U_{k-1})
2. This constant bound contributes exponent 0 to the recurrence
3. Combined with the ||d_k||_{L²} ~ U_{k-1}^{1/2} and Chebyshev, total exponent is 4/3 - 5/(3q)

**Prior finding:** The CZ bound on the FULL NS pressure (Δp = -∂_i∂_j(u_iu_j)) has slack 7.6-17.5× across all tested ICs and Re values. This means ||p||_{L^q,actual} / ||p||_{L^q,CZ bound} ≈ 1/7.6 to 1/17.5.

**Key question:** Does this slack persist for P_k^{21} specifically? If ||P_k^{21}||_{L^q,actual} << C_q by a factor that DEPENDS ON U_{k-1}, then the effective β improves. This would be a direct path to β > 4/3.

## The Pressure Decomposition

From Vasseur (2007), the pressure is decomposed using a spatial cutoff φ_k (smooth, supported in B_k, = 1 on B_{k+1}). On periodic domains, adapt as follows:

### P_k^1 (Nonlocal pressure):
```
-ΔP_k^1 = Σ_{i,j} ∂_i∂_j [(1 - φ_k) u_i u_j]
```
This is the pressure from velocity OUTSIDE the level set region.

### P_k^{21} (Local pressure, bounded factors):
```
-ΔP_k^{21} = Σ_{i,j} ∂_i∂_j [φ_k · u_j(1 - v_k/|u|) · u_i(1 - v_k/|u|)]
```
Key property: the factors u_i(1 - v_k/|u|) are bounded by 1 (Vasseur, Lemma 10).
This is the BOTTLENECK TERM.

### P_k^{22} (Local pressure, cross term):
```
-ΔP_k^{22} = Σ_{i,j} ∂_i∂_j [φ_k · u_j(v_k/|u|) · u_i(1 - v_k/|u|)]
```

### P_k^{23} (Local pressure, level set term):
```
-ΔP_k^{23} = Σ_{i,j} ∂_i∂_j [φ_k · u_j(v_k/|u|) · u_i(v_k/|u|)]
```

**Periodic domain adaptation:** On T³, there are no spatial boundaries, so the cutoff φ_k is not needed for localization. Set φ_k = 1 everywhere (full domain). The decomposition becomes purely about the velocity magnitude truncation: splitting u = u·(1-v_k/|u|) + u·(v_k/|u|) where the first factor is bounded by 1 and the second is the "above threshold" part.

With φ_k = 1, P_k^1 = 0 (no nonlocal piece). The decomposition simplifies to P = P_k^{21} + P_k^{22} + P_k^{23}.

## Specific Tasks

### Task 1: Implement the Pressure Decomposition

For each DNS snapshot:
1. Compute |u| and v_k = [|u| - (1-2^{-k})]_+
2. Compute the "below" and "above" velocity projections:
   - u_below = u · min(1, (1-2^{-k})/|u|) (bounded by 1-2^{-k})
   - u_above = u - u_below = u · v_k/|u| (supported where |u| > 1-2^{-k})
3. Form the RHS tensors:
   - For P_k^{21}: f^{21}_{ij} = u_{below,j} · u_{below,i}
   - For P_k^{22}: f^{22}_{ij} = u_{above,j} · u_{below,i} (or symmetric)
   - For P_k^{23}: f^{23}_{ij} = u_{above,j} · u_{above,i}
4. Solve each Poisson equation spectrally: P_k^{mn}_hat = -k_i k_j f^{mn}_{ij,hat} / |k|²
5. Verify: P_k^{21} + P_k^{22} + P_k^{23} ≈ full pressure (to numerical precision)

### Task 2: Measure CZ Tightness for Each Piece

For each piece P_k^{mn} and each q ∈ {2, 3, 4, 6, 8}:
- **Actual:** ||P_k^{mn}||_{L^q} (computed from DNS)
- **CZ bound:** C_q · ||f^{mn}||_{L^q} where f^{mn} is the RHS tensor and C_q is the CZ constant for second-order Riesz transforms
- **Tightness ratio:** actual / CZ bound

The CZ constant C_q for the operator ∂_i∂_j Δ^{-1} on T³ can be estimated as:
- C_2 = 1 (exact, by Parseval)
- C_q ≈ max(q, q/(q-1)) - 1 for q ≠ 2 (Iwaniec conjecture gives C_q = q* - 1 where q* = max(q, q/(q-1)))

Use the best known rigorous constant or compute it on the grid.

### Task 3: Critical Measurement — Does P_k^{21} Slack Depend on k?

THIS IS THE KEY MEASUREMENT. For each k = 0, 1, ..., 8:
- Compute ||P_k^{21}||_{L^q,actual}
- Compute the CZ bound C_q
- Report the ratio

**If the ratio DECREASES with k** (i.e., P_k^{21} gets further from saturating the CZ bound as the level set narrows), then the CZ bound has slack that depends on U_{k-1}. This would directly improve β.

**If the ratio is CONSTANT with k**, the CZ bound is equally (near-)tight at every level, and improving β requires something other than CZ slack.

### Task 4: Run Across ICs and Re

**Minimum:**
- 3 ICs: Taylor-Green, anti-parallel tubes, random Gaussian
- 3 Re: 100, 500, 1000
- N = 64 primary, one convergence check at N = 128

**Output tables:**

Table A — CZ tightness by pressure piece:
| IC | Re | Piece | q=2 | q=4 | q=6 | q=8 |
|---|---|---|---|---|---|---|

Table B — P_k^{21} tightness vs k:
| IC | Re | k=0 | k=2 | k=4 | k=6 | k=8 | Trend |
|---|---|---|---|---|---|---|---|

## Prior DNS Code

A pseudospectral NS solver exists at:
`/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/navier-stokes/strategies/strategy-001/explorations/exploration-002/code/ns_solver.py`

This is a fully working 3D spectral solver on T³ with RK4, 2/3 dealiasing, and adaptive CFL.

## Success Criteria

✅ **Success:**
- Pressure decomposition verified (sum = full pressure)
- CZ tightness ratios measured for all 4 pieces × ≥ 3 q values × ≥ 3 ICs
- P_k^{21} tightness vs k measured for k = 0,...,8
- Clear determination: does the bottleneck piece's CZ slack depend on k (level set depth)?
- All values tagged [VERIFIED]

❌ **Failure modes:**
- Decomposition doesn't sum to full pressure → debug the implementation
- P_k^{21} is numerically zero for large k → level sets are empty; reduce K_max or increase Re
- CZ constant estimation is unreliable → use C_2 = 1 (exact) as the anchor and report relative ratios

## Output Format

Implementation Details → Decomposition Verification → CZ Tightness Tables → k-Dependence Analysis → Interpretation. Include ALL code. Tag every numerical value as [VERIFIED], [COMPUTED], or [CONJECTURED].
