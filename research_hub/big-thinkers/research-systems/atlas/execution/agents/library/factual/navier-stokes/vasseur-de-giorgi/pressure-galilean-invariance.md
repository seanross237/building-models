---
topic: Pressure Poisson equation is Galilean-invariant for incompressible flow
confidence: verified
date: 2026-03-30
source: vasseur-pressure exploration-003
---

## Finding

The pressure Poisson equation for incompressible NS is **exactly Galilean-invariant**: under u -> u - u_0 (constant u_0), the source term is unchanged. This means the CZ bound ||p||_{L^q} <= C_q ||u||_{L^{2q}}^2 cannot be improved by any constant-velocity frame shift.

## Proof

For incompressible flow (div u = 0), the pressure solves:
```
-Delta p = sum_{i,j} partial_i partial_j (u_i u_j)
```

Under u -> u - u_0:
```
-Delta p' = sum partial_i partial_j ((u_i - u_{0,i})(u_j - u_{0,j}))
          = sum partial_i partial_j (u_i u_j) - 2 sum u_{0,i} partial_i (partial_j u_j) + ...
          = sum partial_i partial_j (u_i u_j)
```
The cross-terms vanish because div u = 0, and the constant terms vanish because second derivatives of constants are zero.

## Consequence for Beta Improvement

This invariance is the fundamental reason why Galilean boosts cannot improve the CZ bound on the bottleneck term P_k^{21} in the De Giorgi iteration. The source term u(1 - v_k/|u|) changes under the boost, but remains bounded by 1 on the support of the truncation. The CZ constant C_q is unchanged.
