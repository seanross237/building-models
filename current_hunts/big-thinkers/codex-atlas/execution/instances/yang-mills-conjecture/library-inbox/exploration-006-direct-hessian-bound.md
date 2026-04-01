# Exploration 006: Direct Hessian Bound — Per-Plaquette and Anti-Correlation

## Goal
Prove |λ(Hess S(Q))| ≤ 4d for all Q ∈ SU(2)^E on the d-dimensional hypercubic torus, completing the mass gap proof at β < 1/(2d). Three approaches tested: (B) D/C anti-correlation, (C) concavity, (A) per-plaquette.

## Approach B: D/C Anti-Correlation Bound

**Claim to test:** |D_min(Q)| + ||C(Q)||_op ≤ 4d = 16 for all Q.

### Random Survey (500 configs, d=4, L=2)

`[COMPUTED]` Over 500 random SU(2) configurations:
- max(|D_min| + ||C||) = 11.39, mean = 10.04
- max(D_max + ||C||) = 12.28, mean = 10.03
- Zero violations of the 4d=16 bound among random configs
- Actual eigenvalues: max λ_max = 8.86, max |λ_min| = 8.73 — well within bounds

### Structured Configs — CRITICAL NEGATIVE RESULT

`[COMPUTED]` **The combined bound |D_min| + ||C|| ≤ 4d is FALSE.**

| Config | |D_min| | ||C|| | sum_neg | sum_pos | λ_max | |λ_min| |
|--------|---------|-------|---------|---------|-------|--------|
| flat | 6.000 | 10.000 | **16.000** | **16.000** | 16.000 | 0.000 |
| uniform-θ=2.094 | 6.000 | 10.583 | **16.583** | **16.583** | 14.822 | 4.583 |
| uniform-θ=0.785 | 6.000 | 9.345 | 15.345 | 15.345 | 14.243 | 3.345 |
| anti-instanton | 6.000 | 8.093 | 14.093 | 6.093 | 4.758 | 13.768 |
| checker-I/iσ0 | 6.000 | 8.329 | 14.329 | 14.329 | 14.214 | 2.329 |

The uniform rotation at θ = 2π/3 gives |D_min| + ||C|| = 16.58 > 16 = 4d. **This exceeds the bound by 0.58.**

Crucially, the actual Hessian eigenvalues at this config are λ_max = 14.82 and |λ_min| = 4.58, both well below 16. So the Hessian bound |λ(H)| ≤ 4d still holds — the failure is that D and C do not anti-correlate tightly enough for the simple sum bound to work.

### Why Approach B Fails

`[CONJECTURED]` The issue is that |D_min| = 6 = 2(d-1) is achievable simultaneously with ||C|| > 10 = 2(d+1). At the uniform-θ=2π/3 config, all plaquettes have Re Tr(U_□) = -1 (not the extremal ±2), giving D = -6 uniformly. Meanwhile the cross-term norm ||C|| = 10.58 slightly exceeds the flat value of 10, because the color kernels partially align despite non-flat holonomies.

The actual Hessian eigenvalue is smaller because D and C act on different subspaces — the eigenvector of C with eigenvalue 10.58 doesn't align with the D = -6 direction. But capturing this algebraically requires more than the triangle inequality |λ(D+C)| ≤ |D| + ||C||.

### Gradient Ascent on |D_min| + ||C||

`[COMPUTED]` Stochastic ascent from random starts reached max ~13.4, well below the structured config's 16.58. The structured configs (uniform rotations) are harder to find by random search but represent the true extremal behavior.

### Dimension Scaling

`[COMPUTED]` Random survey (200 configs per dimension):
- d=2: max |D_min|+||C|| = 5.26 / 8 (ratio 0.66)
- d=3: max |D_min|+||C|| = 8.73 / 12 (ratio 0.73)
- d=4: max |D_min|+||C|| = 11.39 / 16 (ratio 0.71)

Random configs stay well below 4d, but structured configs can exceed it.

## Approach C: Concavity / Local Maximum (NOT RUN)

Due to time constraints, the concavity test along geodesics and gradient ascent on λ_max were not completed. Code is written and available in `code/approach_C_concavity.py` and `code/run_all_fast.py`.

The key question — whether λ_max(H(Q)) is concave on SU(2)^E — remains open. Prior exploration E003 showed flat is a strict local max (negative second derivative in all directions). If concavity held globally, this would immediately give the bound. This is the most promising remaining direction.

## Approach A: Per-Plaquette (NOT RUN)

Code written (`code/approach_A_per_plaquette.py`) but not executed due to time constraints.

The per-plaquette approach asks: is ||H_□|| ≤ 4 for every plaquette □ and every Q? If yes, aggregation via graph coloring (coloring plaquettes so same-color ones share no edges) would give ||H|| ≤ k × 4 where k is the chromatic number. If k ≤ d, this gives ||H|| ≤ 4d.

At flat, ||H_□|| = 4 exactly. Whether this is the maximum is unknown.

## Summary of Results

| Claim | Status | Result |
|-------|--------|--------|
| \|D_min\| + \|\|C\|\| ≤ 4d | `[COMPUTED]` | **FALSE** — violated at uniform θ=2π/3 (16.58 > 16) |
| \|λ(H)\| ≤ 4d for all Q | `[COMPUTED]` | Holds in all tested configs (max λ_max = 16.00 at flat) |
| Flat is global max of λ_max | `[COMPUTED]` | Consistent with all data — no config found with λ_max > 16 |
| Random configs satisfy \|D\|+\|\|C\|\| ≤ 12.3 | `[COMPUTED]` | True (500 configs, max = 12.28) |
| Anti-instanton: \|λ_min\| ≈ 13.77 | `[COMPUTED]` | Confirmed, well below 16 |

## Key Insight

The gap between |λ(H)| ≤ 4d (empirically true) and |D|+||C|| ≤ 4d (false) reveals that the proof CANNOT go through any bound of the form |λ(D+C)| ≤ |λ(D)| + ||C||. The cancellation between D and C is essential and operates at the eigenvector level, not just at the operator norm level.

Any successful proof must either:
1. **Prove concavity of λ_max** (Approach C) — making flat the unique global max
2. **Use per-plaquette structure** (Approach A) — bounding H_□ individually and aggregating via combinatorics
3. **Find a different decomposition** of H that admits tighter per-component bounds
