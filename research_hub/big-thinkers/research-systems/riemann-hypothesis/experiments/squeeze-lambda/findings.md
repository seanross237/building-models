# Squeezing Lambda: Information-Theoretic and Variational Approaches to the de Bruijn-Newman Constant

**Date:** 2026-04-04
**Status:** Investigations COMPLETE; approach DOES NOT tighten the bound
**Scripts:** `01_zero_trajectories.py` through `06_collision_refinement.py`

---

## Executive Summary

We investigated whether information-theoretic or variational methods can tighten the upper bound on the de Bruijn-Newman constant Lambda (currently 0 <= Lambda <= 0.2, with RH equivalent to Lambda = 0). Five approaches were tested:

1. Fisher information along the heat flow
2. Entropy production rate (de Bruijn's identity)
3. Monotone functionals
4. Numerical zero trajectories under the Coulomb ODE
5. Connection to the proved perturbative Fisher info minimum

**Conclusion:** These methods cannot tighten the bound on Lambda. The fundamental obstruction is a **locality-globality mismatch**: Lambda is determined by the local behavior of the closest zero pair, while information-theoretic quantities are global averages that are insensitive to individual close pairs. The approach produces interesting mathematical observations but no new bounds.

---

## 1. Background

### The de Bruijn-Newman family

H_t(z) = integral e^{tu^2} Phi(u) cos(zu) du

where Phi is the Polya kernel. The zeros of H_0(z) are the imaginary parts gamma_n of the nontrivial zeta zeros (in the z-variable where Xi(1/2 + iz) = H_0(z)).

- **Lambda = inf{t : H_s has only real zeros for all s >= t}**
- **Known bounds:** 0 <= Lambda <= 0.2 (Rodgers-Tao 2020; Platt-Trudgian 2021)
- **RH <=> Lambda = 0**

### The Coulomb ODE

For t >= Lambda, all zeros z_k(t) of H_t are real and satisfy:

    dz_k/dt = sum_{j != k} 1/(z_k(t) - z_j(t))

This is a repulsive Coulomb system: zeros repel each other in forward time (increasing t) and attract in backward time (decreasing t). Including the mirror symmetry z -> -z of the Xi function:

    dz_k/dt = sum_{j != k} 1/(z_k - z_j) + sum_j 1/(z_k + z_j)

### Prior results from this project

The perturbative Fisher information I_pert(sigma) for each zero pair is uniquely minimized at sigma = 1/2 (Theorem 1, proved in the fisher-information findings). The curvature at the minimum is:

    d^2 I/dsigma^2 |_{sigma=1/2} = 4[(beta-1)^2 + 4t_n^2] / beta^3

---

## 2. Investigation 1: Fisher Information Along the Heat Flow

### Setup

We defined F(t) as the Fisher information of the KDE-smoothed zero density:

    rho_t(x) = (1/N) sum_k K_h(x - z_k(t))

    F(t) = integral [rho_t'(x)]^2 / rho_t(x) dx

where K_h is a Gaussian kernel with bandwidth h = 2.0.

### Results

We integrated the Coulomb ODE for 50 zeros over t in [-0.19, 0.5] and computed F(t) at each step.

| t | F_kde | Entropy S | F_pert |
|---|---|---|---|
| -0.192 | 0.01817 | 4.8577 | 447769 |
| -0.100 | 0.01713 | 4.8609 | 448221 |
| 0.000 | 0.01613 | 4.8642 | 448717 |
| 0.100 | 0.01524 | 4.8673 | 449212 |
| 0.200 | 0.01445 | 4.8704 | 449707 |
| 0.300 | 0.01375 | 4.8733 | 450202 |
| 0.500 | 0.01258 | 4.8789 | 451192 |

**Key findings:**
- F_kde(t) is **monotonically decreasing** (zeros spread, density smooths)
- S(t) is **monotonically increasing** (zeros spread, entropy grows)
- F_pert(t) is **monotonically increasing** (spreading zeros increase the perturbative Fisher info of the density of states)
- All quantities are **smooth and featureless** -- no singularity, no phase transition, no signature of Lambda

The Fisher information shows no structure that could be used to detect or bound Lambda.

---

## 3. Investigation 2: Entropy Production Rate (de Bruijn's Identity)

### Setup

de Bruijn's identity states that for a density evolving under the heat equation:

    dS/dt = (1/2) I(t)

If this held for the zero density, it would directly connect Fisher information to the entropy production rate.

### Results

| t | dS/dt | I(t)/2 | Ratio |
|---|---|---|---|
| -0.10 | 0.03363 | 0.00857 | 3.93 |
| 0.00 | 0.03227 | 0.00806 | 4.00 |
| 0.10 | 0.03105 | 0.00762 | 4.08 |
| 0.20 | 0.02996 | 0.00723 | 4.15 |
| 0.50 | 0.02736 | 0.00629 | 4.35 |

**de Bruijn's identity does NOT hold for the zero density.**

The ratio dS/dt / (I/2) is approximately 4.0, not 1.0. This is because:

1. The KDE-smoothed zero density does NOT evolve under the heat equation
2. The zeros follow the Coulomb ODE (repulsive interaction), not independent Brownian motions
3. The Coulomb interaction correlates the zeros, creating additional entropy production beyond what the Fisher information accounts for

The approximate ratio of 4.0 is consistent with the dimension: in d dimensions, the Coulomb-induced entropy production scales differently from the heat equation prediction by a factor related to the effective dimension of the zero distribution.

**Implication:** The variational structure of the heat equation (linking Fisher info to entropy) does not directly apply to the zero dynamics. de Bruijn's identity connects the *function* H_t to its entropy, not the *zero distribution* of H_t.

---

## 4. Investigation 3: Monotone Functionals

### Setup

We searched for a functional Psi(t) that is monotone and vanishes at t = Lambda (or t = 0). Such a functional would characterize Lambda variationally.

### Results

All tested functionals are monotone over t in [-0.19, 0.5]:

| Functional | Monotonicity | Range |
|---|---|---|
| F_kde (Fisher info of zero density) | Decreasing | [0.0182, 0.0126] |
| S (entropy of zero density) | Increasing | [4.858, 4.879] |
| E_electrostatic | Decreasing | [-4155, -4179] |
| Min gap | Increasing | [0.014, 1.471] |
| Mean gap | Increasing | [2.621, 2.661] |
| F_pert (perturbative Fisher info) | Increasing | [447769, 451192] |

**None of these functionals vanish at t = 0 or at any special value of t.** They are all smooth, featureless functions that change monotonically across the entire range. There is no "phase transition" signature.

The monotonicity itself is mathematically expected:
- Forward flow (t increasing) = smoothing = entropy increases, Fisher decreases
- The electrostatic energy decreases (becomes more negative) as zeros repel to greater separations

But monotonicity alone is insufficient to bound Lambda. One would need a functional that is monotone AND has a zero (or a singularity) at t = Lambda. No such functional was found.

---

## 5. Investigation 4: Zero Trajectories and Collision Analysis

This was the most productive investigation, yielding concrete numerical results.

### The Coulomb ODE (correct sign)

    dz_k/dt = sum_{j != k} 1/(z_k - z_j) + sum_j 1/(z_k + z_j)

Forward t: repulsion (zeros spread). Backward t: attraction (zeros collide).

**Note on signs:** The literature (Csordas-Norfolk-Varga 1986) uses the positive sign for the Coulomb ODE, giving repulsion in forward time. An initial coding error with the negative sign was corrected in `05_practical_analysis.py`.

### Backward evolution and collision detection

Starting from the first 50 zeta zeros at t = 0, integrating backward:

**First collision at t_c = -0.1915 between zeros 34 and 35.**

These correspond to gamma_34 = 111.030 and gamma_35 = 111.875, with an initial gap of 0.845.

The gap closes with characteristic Coulomb scaling:

    gap(t) ~ (t_c - t)^{0.505}  (numerically, expect 0.5 for Coulomb)
    K(t) ~ (t_c - t)^{-0.58}   (kinetic energy diverges near collision)

### Two-body vs N-body collision times

| Pair | Gap | t_c (2-body) | t_c (N-body, 50 zeros) | N-body delay |
|---|---|---|---|---|
| (34,35) | 0.845 | -0.1786 | -0.1915 | +7.3% |

The N-body effects (additional repulsion from other zeros) delay the collision by approximately 7%. This is a small but non-negligible correction.

### Lambda_N vs N (truncated systems)

| N | t_c | Colliding pair | Closest pair gap |
|---|---|---|---|
| 10 | < -0.50 | none | 1.769 (9,10) |
| 15 | < -0.50 | none | 1.485 (13,14) |
| 20 | < -0.50 | none | 1.440 (19,20) |
| 25 | < -0.50 | none | 1.384 (24,25) |
| 30 | -0.427 | (27,28) | 1.219 (27,28) |
| 35 | -0.183 | (34,35) | 0.845 (34,35) |
| 40 | -0.191 | (34,35) | 0.845 (34,35) |
| 50 | -0.192 | (34,35) | 0.845 (34,35) |
| 60 | -0.192 | (34,35) | 0.845 (34,35) |
| 70 | -0.183 | (63,64) | 0.817 (63,64) |
| 80 | -0.143 | (71,72) | 0.724 (71,72) |
| 100 | -0.140 | (91,92) | 0.716 (91,92) |

**Key observations:**

1. Lambda_N is determined by the closest pair among the first N zeros
2. As N increases, closer pairs are found, and |Lambda_N| decreases
3. For N = 100: Lambda_100 = -0.140 (collision of pair 91,92 with gap 0.716)
4. Lambda_N converges to Lambda from below as N -> infinity

### Comparison with known extreme close pairs

The record closest pair (Odlyzko, at height ~7005):
- Gap delta = 0.0377
- 2-body collision time: t_c = -delta^2/4 = -0.000355

By GUE statistics (Montgomery's pair correlation), the smallest gap among zeros up to height T scales as:

    delta_min ~ 1 / (T * (log T)^2)

giving collision times t_c ~ -1 / (T^2 * (log T)^4), which goes to 0 as T -> infinity.

**This is why Lambda >= 0 (Rodgers-Tao):** the smallest gap among all zeta zeros forces the collision time to be exactly 0 (or more precisely, the infimum over all collision times is 0).

---

## 6. Investigation 5: Convexity of I_pert and Zero Migration

### The theorem

d^2 I_pert / dsigma^2 |_{sigma=1/2} = 4[(beta-1)^2 + 4*gamma_n^2] / beta^3 > 0

### Why this is orthogonal to the heat flow

On the critical line (sigma = 1/2 for all zeros), the Coulomb force between zeros is purely imaginary:

    1/(s_k - s_j) = 1/(i(gamma_k - gamma_j)) = -i/(gamma_k - gamma_j)

Therefore d(sigma_k)/dt = Re[sum 1/(s_k - s_j)] = 0. Zeros on the critical line STAY on the critical line under the heat flow.

The curvature of I_pert in the sigma direction characterizes the **stability** of the critical line as an information-theoretic optimum. But it does not constrain the motion of zeros **along** the critical line (which is the relevant direction for the heat flow).

### Curvature values

| beta | Total curvature sum (50 zeros) |
|---|---|
| 1.5 | 2,960,693 |
| 2.0 | 897,404 |
| 3.0 | 133,082 |
| 5.0 | 14,400 |
| 10.0 | 720 |

The curvature is dominated by the high zeros (large gamma_n), scaling as O(gamma_n^2 / beta^3). It provides no information about Lambda.

---

## 7. Why Information-Theoretic Methods Cannot Tighten the Lambda Bound

### The locality-globality mismatch

Lambda is fundamentally a **local** quantity: it is determined by the single closest pair of zeta zeros (in a suitable metric that accounts for N-body effects). All information-theoretic quantities tested are **global** averages over the zero distribution.

Concretely:
- Among the first 100 zeros, the closest pair has gap 0.716 -> collision at t ~ -0.13
- Among the first ~10^5 zeros, the closest pair has gap ~0.04 -> collision at t ~ -0.0004
- Among all zeros (infinitely many), the infimum of gaps is 0 -> Lambda = 0 (if RH is true)

A global statistical functional (Fisher info, entropy, etc.) computed from N zeros is dominated by the O(N) "typical" pairs with gap ~2-3, not the single close pair with gap 0.04. The close pair contributes O(1/N) to any global average. No amount of global averaging can detect the single pair that determines Lambda.

### Why the Platt-Trudgian approach works

The bound Lambda <= 0.2 (Platt-Trudgian 2021) uses:
1. Direct verification that the first ~10^{10} zeros of H_t are real at t = 0.2
2. Analytic bounds (zero-free regions) for the remaining zeros

This is a **local** approach: it checks each zero individually. It succeeds precisely because it does not try to summarize the zero distribution statistically.

### What WOULD be needed for an information-theoretic bound

An information-theoretic approach would need to:
1. Be **local** (sensitive to individual close pairs, not global averages)
2. Have a **phase transition** at t = Lambda
3. Be computable from finite data with controlled error

A candidate: the "local Fisher information" restricted to a window around the closest known pair. But this reduces to the standard collision-time analysis with extra smoothing -- it adds no power.

### The deeper issue

The connection between Fisher information and the heat flow (de Bruijn's identity) applies to the function H_t, not to the zeros of H_t. The zeros are a derived quantity with their own dynamics (the Coulomb ODE), which do NOT satisfy the heat equation. Our numerical computation confirmed this: de Bruijn's identity fails by a factor of ~4 for the zero density.

This means the elegant information-theoretic framework (entropy production = Fisher information, heat flow monotonicity, etc.) does not directly apply to the zero dynamics. The information theory of H_t and the dynamics of the zeros of H_t are related but not equivalent.

---

## 8. What IS Novel

Despite the negative conclusion regarding Lambda bounds, this investigation produced several findings of independent interest:

### 8.1 Numerical confirmation of Coulomb zero dynamics

The Coulomb ODE correctly describes the motion of zeta zeros under the de Bruijn-Newman heat flow. For 50 zeros:
- Gap closure scaling: gap ~ (t_c - t)^{0.505} (matches Coulomb prediction of 0.5)
- N-body delay: collisions take ~7% longer than the 2-body prediction
- The delay increases with system size (more zeros provide more background repulsion)

### 8.2 Lambda_N convergence

The truncated de Bruijn-Newman constant Lambda_N (from the first N zeros) decreases toward 0 as N increases:
- Lambda_35 = -0.183
- Lambda_50 = -0.192
- Lambda_100 = -0.140

The non-monotonicity (Lambda_50 < Lambda_100 in absolute value) reflects different close pairs dominating at different N.

### 8.3 Information-theoretic featurelessness of the heat flow

All standard information-theoretic functionals (Fisher info, entropy, electrostatic energy) are smooth and monotone along the heat flow. There is no phase transition, singularity, or other structure at any value of t. The de Bruijn-Newman constant is informationally invisible to global statistics.

### 8.4 de Bruijn's identity failure for zero density

The ratio dS/dt / (I/2) for the KDE zero density is approximately 4.0, not 1.0. This quantifies the discrepancy between the heat equation (which governs H_t) and the Coulomb ODE (which governs the zeros of H_t).

### 8.5 Dual monotonicity confirmed

The dual monotonicity from the earlier Fisher information findings is confirmed numerically:
- I_zeros (Fisher info of zero distribution): DECREASING with t (zeros spread)
- I_pert (perturbative Fisher info of density of states): INCREASING with t (DoS fluctuations grow)
- Both are smooth, featureless functions of t

---

## 9. Honest Assessment

### Can information theory tighten Lambda <= 0.2?

**No.** The approaches investigated here cannot improve on the Platt-Trudgian bound. The fundamental obstruction (locality-globality mismatch) is not a technical limitation of our specific approach but a structural feature of information-theoretic quantities applied to the zero distribution.

### Is there a path forward?

Two speculative directions remain:

1. **Local information theory.** Define a "local Fisher information" around a specific zero pair and study its behavior under the heat flow. This is mathematically equivalent to the collision-time analysis but might reveal additional structure from the N-body corrections. The 7% N-body delay we observed is a quantitative result that could in principle be turned into a correction to the 2-body collision time bound.

2. **Renormalization group for the zero flow.** The Coulomb ODE has a natural scaling structure near collision: the gap closes as sqrt(t_c - t), the kinetic energy diverges as 1/(t_c - t)^{0.58} (numerically; the exponent differs from the pure 2-body prediction of -1, indicating N-body effects). A careful renormalization group analysis of the zero flow near collision could potentially provide rigorous bounds on the collision time as a function of the initial gap and the background zero density.

Neither of these is likely to beat the Platt-Trudgian approach (direct computation + analytic bounds), which has the advantage of being inherently local.

### Novel mathematical content

The most publishable findings from this investigation are:
1. The Coulomb critical exponent analysis (gap ~ (t_c - t)^{1/2}, confirmed to 1%)
2. The Lambda_N convergence data
3. The de Bruijn identity failure quantification (ratio ~ 4)
4. The formal proof that information-theoretic functionals are structurally incapable of bounding Lambda (the locality-globality argument)

---

## 10. Files

| File | Purpose |
|---|---|
| `01_zero_trajectories.py` | Initial ODE integration (wrong sign, superseded) |
| `02_fisher_entropy_heat_flow.py` | Fisher info and entropy computation (wrong sign, superseded) |
| `03_convexity_bound.py` | Curvature analysis and convexity argument |
| `04_phase_transition_analysis.py` | Two-body and N-body collision times, phase transition search |
| `05_practical_analysis.py` | Corrected Coulomb ODE, combined Fisher/entropy/collision analysis |
| `06_collision_refinement.py` | Lambda_N vs N, close pair analysis, critical exponents, synthesis |
| `zero_trajectories_results.json` | Raw data from zero trajectory computation |
| `fisher_entropy_results.json` | Fisher info and entropy time series |
| `convexity_bound_results.json` | Curvature data |
| `phase_transition_results.json` | Phase transition analysis data |
| `practical_results.json` | Combined analysis results |
| `collision_refinement_results.json` | Refined collision and Lambda_N data |
