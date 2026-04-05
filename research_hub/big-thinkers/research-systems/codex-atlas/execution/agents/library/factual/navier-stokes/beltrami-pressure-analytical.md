---
topic: Exact Beltrami flows have p = -|u|^2/2, zero CZ loss, trivial regularity
confidence: verified
date: 2026-03-30
source: "vasseur-pressure exploration-006"
---

## Finding

For exact Beltrami flows (curl u = lambda u) on T^3, the pressure is completely determined by the local velocity magnitude: **p = -|u|^2/2 + const**. No Calderon-Zygmund operator is needed. The CZ "loss" is exactly zero. The solution is trivially regular for all time.

### Derivation Chain

1. **Lamb vector vanishes:** L = omega x u = lambda(u x u) = 0. Therefore u . nabla u = nabla(|u|^2/2).

2. **Pressure is Bernoulli:** Taking divergence of NS with div u = 0 gives -Delta p = Delta(|u|^2/2), so p + |u|^2/2 is harmonic. On T^3, the only harmonic functions are constants.

3. **Beltrami = eigenfunction of Stokes operator:** curl(curl u) = -Delta u = lambda^2 u, so Delta u = -lambda^2 u.

4. **Exact exponential decay:** u(x,t) = u_0(x) exp(-nu lambda^2 t). Spatial structure frozen, only amplitude decreases. Trivially regular.

5. **Pressure Poisson source simplifies:** -Delta p = |S|^2 - lambda^2|u|^2/2, dramatically simpler than general tr((nabla u)^T nabla u).

### Why CZ Loss Is Zero

The pressure Poisson source for Beltrami flows is a pure Hessian: partial_i partial_j(u_i u_j) = partial_i partial_j(|u|^2/2). The CZ operator R_i R_j acting on a pure Hessian of a scalar is trivial — the Riesz transform inversion is exact. CZ loss occurs only when the source tensor has non-Hessian components (components in the kernel of the trace projection). For Beltrami flows, these components vanish because the Lamb vector is zero.

### ABC Flow Verification

For ABC flow (A=B=C=1, lambda=1), numerical verification on N=32 grid: ||L||_rms = 5.4e-16 (machine zero), p vs -|u|^2/2 relative error = 4.2e-16 (machine zero). Both core claims verified to machine precision.

## E009 Adversarial Assessment

**The analytical mechanism is correct; practical significance is genuinely uncertain.** Exact Beltrami flows on T^3 are trivially regular — they decay as u(t) = u_0 exp(-nu lambda^2 t), preserving spatial structure with exponential amplitude decay. Proving regularity for Beltrami flows requires no De Giorgi machinery at all. The mechanism is only interesting for near-Beltrami flows, but the Lamb vector enters at O(epsilon) — so for ANY finite departure from exact Beltrami, the full CZ loss returns. The mechanism gives zero-vs-full improvement, with no middle ground within the existing analytical framework. The DNS beta_eff ~ 1.0 for ABC is a correlation, not a causal verification.

**Corrected framing:** "For exact Beltrami flows, L=0 eliminates CZ loss in the De Giorgi pressure term — a valid analytical observation. DNS shows ABC flows have the highest beta_eff (~1.0), consistent with this mechanism. However, exact Beltrami flows are trivially regular, and the mechanism's utility for near-Beltrami flows requires a quantitative bound on how ||L|| controls the CZ loss contribution to beta — this remains an open analytical problem." Grade: B+ (strong analytically, limited practical scope). **Partially novel** — Lamb vector decomposition and Bernoulli pressure for Beltrami flows are known; the connection to De Giorgi CZ loss is new.

## E010 Update — Near-Beltrami Extension Fails

E010 tested perturbed-ABC flows and confirmed the mechanism does NOT extend: even 1% perturbation (eps=0.01) destroys the B_k = O(2^{-k}) decay, and beta_eff drops below 1 for eps >= 0.05. The mechanism is specific to exact eigenstates of curl — a measure-zero set. The analytical observation (L=0 => no CZ loss) remains valid but its practical significance for regularity theory is limited. See `near-beltrami-negative-result.md`.
