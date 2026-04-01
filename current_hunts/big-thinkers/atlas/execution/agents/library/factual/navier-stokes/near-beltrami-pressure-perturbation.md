---
topic: Near-Beltrami perturbation analysis — bad pressure is O(epsilon), continuous degradation
confidence: verified
date: 2026-03-30
source: "vasseur-pressure exploration-006"
---

## Finding

For flows epsilon-close to Beltrami (u = u_B + epsilon v), the pressure decomposes into a "Beltrami part" (CZ-lossless, -|u|^2/2) and a "deficit part" (CZ-lossy, O(epsilon)). The degradation from exact Beltrami is **continuous and linear in epsilon** — there is no threshold discontinuity.

### Perturbation Analysis

The Lamb vector at O(epsilon):
  L = epsilon [lambda u_B x v + (curl v) x u_B] + O(epsilon^2)

The pressure decomposes as:
  p = -|u|^2/2 + p_L + const

where p_L satisfies -Delta p_L = div(L) = O(epsilon). So ||p_L||_{L^2} = O(epsilon).

### Numerical Confirmation

Near-Beltrami perturbation (u = u_ABC + eps * v_random):

| eps | ||L||_rms | ||p - (-\|u\|^2/2)|| / ||p|| |
|---|---|---|
| 0.01 | 0.042 | 0.020 |
| 0.05 | 0.213 | 0.098 |
| 0.10 | 0.427 | 0.195 |
| 0.20 | 0.864 | 0.370 |
| 0.50 | 2.358 | 0.725 |

Both Lamb vector norm and pressure deviation scale linearly with eps.

### Implication for De Giorgi

The effective bottleneck integral decomposes: I_k <= I_k^{Hessian} + C_q epsilon I_k^{Lamb}. If epsilon is small enough that the Lamb term is subdominant, the effective beta could be improved toward the Beltrami value (beta ~ 1).

### Key Obstacle: Truncation Breaks Beltrami — RESOLVED (E007)

Even when u is Beltrami, the truncated velocity u_below = u min(1, threshold/|u|) is NOT Beltrami. curl(u_below) != lambda u_below. This means P_k^{21} does not enjoy the full Beltrami simplification.

**RESOLVED by E007:** The Beltrami deficit B_k = ||curl(u_below) - lambda_opt u_below||_{L^2} / ||u_below||_{L^2} scales as O(2^{-k}) for ABC flows. The truncation perturbation is confined to the shrinking set where |u| > lambda_k. The pressure remainder fraction R_frac = O(2^{-k}) and the bottleneck remainder I_r/I_t = O(2^{-k}). The mechanism survives truncation. See `vasseur-de-giorgi/beltrami-deficit-truncation-survival.md` and `vasseur-de-giorgi/pressure-bernoulli-dominance-truncated.md` for full measurements.

### Conditional Regularity Conjecture

Beltrami deficit B(u) = ||curl u - lambda u||_{L^2} / ||u||_{L^2}. Conjecture: there exists epsilon_0 > 0 such that if B(u(t)) <= epsilon_0 for all t, the solution is regular. Grade B (promising but needs work): mechanism is real, formalization is nontrivial because the Beltrami deficit is not preserved by NS evolution.

## E009 Adversarial Assessment

The mechanism has a **discontinuous character** at the analytical level: exact Beltrami gives full CZ improvement, but any perturbation gives zero improvement within current analytical tools. The interesting follow-up is whether ||L|| provides a QUANTITATIVE improvement to beta — this would require a novel analytical argument: "if ||L||_{L^p} / ||u||_{L^{2p}} < epsilon, then beta > 4/3 + delta(epsilon)." This is the most promising direction for a publishable mathematical result from Strategy-001.

**The key open analytical task** (recommended for Strategy-002): decompose the bottleneck integral into Bernoulli (exact) and Lamb (CZ-lossy) pieces at the ANALYTICAL level; show the Lamb piece in the De Giorgi recurrence is bounded by ||L||_{L^p} * U_{k-1}^{alpha}; derive beta as a function of the Lamb-to-pressure ratio. Consider the vorticity formulation (Vasseur-Yang 2021) where Beltrami connection is stronger (Lamb enters at O(eps^2) vs O(eps)).

## E010 Definitive Negative Result — Near-Beltrami Does NOT Work

**E010 DNS with perturbed-ABC flows confirms the E009 assessment is correct.** Key results:

- **B_k decay lost for any eps > 0:** Even at eps=0.01, B_k plateaus at ~0.063 rather than decaying. At eps>=0.05, B_k is flat.
- **beta_eff degrades smoothly:** 1.01 (exact) -> 0.89 (eps=0.05) -> 0.28 (eps=0.50). beta > 1 only for eps < ~0.02.
- **Viscosity helps but not enough:** Viscous dissipation reduces B_full by ~50% but cannot restore B_k decay.

**Physical reason:** For exact Beltrami, the non-Beltrami component exists only at the clipping boundary (measure -> 0). For perturbed flows, the non-Beltrami component exists at ALL velocity magnitudes, so truncation cannot remove it.

**Conditional regularity conjecture status:** The conjecture "if B(u(t)) <= epsilon_0, then regular" may still be true in principle, but epsilon_0 must be extremely small (~0.01 or less for beta > 1), and even 1% perturbation is sufficient to prevent the B_k decay mechanism from functioning. The mechanism is specific to a measure-zero set of initial conditions.

See `near-beltrami-negative-result.md` for the full perturbed-ABC data tables.
