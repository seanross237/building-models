<!-- explorer-type: math -->

# Exploration 007: Beltrami Deficit of u_below + Hessian/Lamb Decomposition on DNS

## Goal

Two linked computational measurements on DNS data that determine whether the Beltrami conditional regularity mechanism survives the De Giorgi truncation:

**Task A:** Measure the Beltrami deficit of the truncated velocity u_below as a function of De Giorgi level k.
**Task B:** Decompose the P_k^{21} pressure source into its Hessian (CZ-lossless) and Lamb vector (CZ-lossy) pieces and measure their relative contributions.

## Background: Why This Is Critical

Exploration 006 identified the mechanism explaining why ABC (Beltrami) flows have beta_eff ≈ 1.0 in the De Giorgi iteration:

**For exact Beltrami flows (curl u = λu):**
- Lamb vector L = ω × u = 0
- Pressure p = −|u|²/2 (Bernoulli, no CZ inversion needed)
- The pressure Poisson source ∂_i∂_j(u_iu_j) = Δ(|u|²/2) is a pure Hessian
- CZ "loss" is zero because Riesz transforms acting on a Hessian give exact inversion

**For near-Beltrami flows (deficit ε):**
- Lamb vector L = δω × u = O(ε) where δω = curl u − λu
- Pressure source = Hessian part Δ(|u|²/2) + Lamb part div(L) where Lamb part is O(ε)
- CZ loss applies only to the O(ε) Lamb part → improvement is continuous in ε

**THE OBSTACLE:** The De Giorgi truncation u_below = u · min(1, λ_k/|u|) is NOT Beltrami even when u is. The bottleneck integral involves P_k^{21} which is the pressure from u_below, not from u. If the truncation destroys Beltrami structure, the mechanism is killed.

**This exploration answers:** Does B(u_below) stay small? How does the Hessian/Lamb ratio look for u_below on actual DNS data?

## Task A: Beltrami Deficit of u_below

### What to Compute

For ABC flow at Re = 100, 500, 1000 (N=64):

1. Run DNS to generate velocity snapshots (reuse exploration-002 infrastructure)
2. For each snapshot and each De Giorgi level k = 0, 1, ..., 8:
   - Compute λ_k = 1 − 2^{-k} (level set threshold)
   - Compute u_below = u · min(1, λ_k/|u|) at each grid point
   - Compute curl(u_below) using spectral differentiation
   - Compute the optimal Beltrami eigenvalue for u_below:
     λ_opt = ⟨curl(u_below), u_below⟩ / ||u_below||²
   - Compute the Beltrami deficit:
     B_k = ||curl(u_below) − λ_opt · u_below||_{L²} / ||u_below||_{L²}

3. Report table:

| IC | Re | k=0 | k=1 | k=2 | k=3 | k=4 | k=5 | k=6 | k=7 | k=8 | Trend |
|---|---|---|---|---|---|---|---|---|---|---|---|

4. Also compute B_k for the NON-Beltrami ICs (Taylor-Green, random Gaussian) as controls. These should have B_k ≈ const (no Beltrami structure to lose).

### Interpretation Guide
- If B_k ≈ 0 for all k on ABC: truncation preserves Beltrami structure → mechanism viable
- If B_k → 1 rapidly: truncation destroys structure → mechanism killed for De Giorgi
- If B_k increases slowly with k: partial preservation → mechanism partially viable, quantify

## Task B: Hessian/Lamb Decomposition of P_k^{21} Source

### What to Compute

The pressure Poisson source for P_k^{21} is:
```
S_{ij} = ∂_i∂_j(u_{below,i} · u_{below,j})
```

This can be decomposed as:
```
S_{ij} = H_{ij} + L_{ij}
```

where:
- **Hessian piece:** H_{ij} = ∂_i∂_j(|u_below|²/2) — this is CZ-lossless (a pure Hessian of a scalar)
- **Lamb piece:** L_{ij} = S_{ij} − H_{ij} = ∂_i∂_j(u_{below,i} u_{below,j}) − ∂_i∂_j(|u_below|²/2)

The identity is:
```
∂_i∂_j(u_i u_j) = Δ(|u|²/2) + ∂_i(ω × u)_i = Δ(|u|²/2) + div(L)
```

where L = ω × u is the Lamb vector and ω = curl(u). So the Lamb piece is:
```
L_{ij} = [terms involving curl(u_below) × u_below]
```

For each DNS snapshot and k = 0, ..., 8:
1. Compute u_below, ω_below = curl(u_below)
2. Compute Lamb vector L_below = ω_below × u_below
3. Solve Poisson equations spectrally:
   - P_Hessian: from source Δ(|u_below|²/2)
   - P_Lamb: from source div(L_below)
   - P_k^{21}: from full source (should equal P_Hessian + P_Lamb to numerical precision)
4. Measure the bottleneck integral contributions:
   - I_k^{total} = ∫∫ |P_k^{21}| · |d_k| · 1_{v_k>0} dx dt
   - I_k^{Hessian} = ∫∫ |P_Hessian| · |d_k| · 1_{v_k>0} dx dt
   - I_k^{Lamb} = ∫∫ |P_Lamb| · |d_k| · 1_{v_k>0} dx dt
5. Report the ratio I_k^{Lamb} / I_k^{total} — the fraction of the bottleneck due to the CZ-lossy Lamb piece

### Output Tables

Table B1 — Lamb fraction by IC and k:
| IC | Re | k=0 | k=2 | k=4 | k=6 | k=8 | Interpretation |
|---|---|---|---|---|---|---|---|

Table B2 — Absolute bottleneck integrals:
| IC | Re | k | I_total | I_Hessian | I_Lamb | Lamb/Total |
|---|---|---|---|---|---|---|

### Interpretation Guide
- If Lamb/Total → 0 for ABC and stays ~1 for non-Beltrami ICs: confirms mechanism, Beltrami structure provides real leverage
- If Lamb/Total ≈ 1 even for ABC: truncation destroys structure completely, mechanism dead
- If Lamb/Total is intermediate: partial improvement, quantify how much beta could gain

## Prior Code

DNS solver and De Giorgi infrastructure from exploration 002:
`/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/vasseur-pressure/strategies/strategy-001/explorations/exploration-002/code/`

- `ns_solver.py` — pseudospectral 3D NS solver
- `degiorgi_measure.py` — De Giorgi level-set computation, normalization

Pressure decomposition code from exploration 004:
`/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/vasseur-pressure/strategies/strategy-001/explorations/exploration-004/code/`

## ICs and Parameters

- **Primary ICs:** ABC (A=B=C=1), Taylor-Green, Random Gaussian (as control)
- **Re:** 100, 500, 1000
- **N:** 64 primary, one convergence check at N=128 for ABC Re=500
- **K_max:** 8 (matching exploration 004)
- **Normalization:** L^∞ normalization (max|u| = 1), matching exploration 002

## Success Criteria

✅ **Success:**
- B_k measured for ABC + 2 control ICs × 3 Re × 9 k-values
- Hessian/Lamb decomposition verified (P_Hessian + P_Lamb = P_k^{21} to numerical precision)
- Lamb fraction measured for ABC + 2 control ICs across k
- Clear determination: does truncation preserve or destroy Beltrami structure?
- All values tagged [VERIFIED]/[COMPUTED]

❌ **Failure modes:**
- u_below has numerical issues (division by zero near |u|=0) → use safe division with epsilon floor
- Hessian + Lamb ≠ P_k^{21} → debug decomposition identity
- B_k is ill-defined at high k (empty level sets) → reduce K_max

## Output Format

Task A Results → Task B Results → Decomposition Verification → Combined Interpretation → Implications for Conditional Regularity. Include ALL code. Tag every value.
