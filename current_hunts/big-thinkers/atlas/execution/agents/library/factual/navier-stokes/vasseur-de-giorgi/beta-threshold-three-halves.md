---
topic: Vasseur beta > 3/2 implies NS regularity
confidence: verified
date: 2026-03-30
source: "vasseur-pressure exploration-001; Vasseur 2007 Appendix"
---

## Finding

**If beta_p > 3/2 for some p > 1, then ALL suitable weak solutions to the Navier-Stokes equations in ]0,inf[ x R^3 are locally bounded (and therefore regular).**

The Appendix introduces rescaled NS equations for epsilon < 1:

```
partial_t u + (1/epsilon) div(u tensor u) + (1/epsilon) nabla P - Delta u = 0,    div u = 0
```

**Conjecture 14:** There exist universal constants p > 1, C, beta > 3/2 such that for any solution to the rescaled NS:

```
U_k  <=  (C^k / epsilon) * (1 + ||P||_{L^p(0,1; L^1(B(1)))}) * U_{k-1}^beta
```

The proof that this implies regularity uses rescaling: given any solution u and any point (t_0, x_0), define u_epsilon(t,x) = epsilon*lambda*u(t_0 + lambda^2*t, x_0 + lambda*x). Then U_{epsilon,0} = O(epsilon^2/lambda). The condition for convergence U_{epsilon,k} -> 0 requires:

```
U_{epsilon,0}  <=  epsilon^{1/(beta-1)}  =  epsilon^2 * epsilon^{-(2*beta-3)/(beta-1)}
```

Since (2*beta-3)/(beta-1) > 0 when beta > 3/2, for epsilon small enough this is satisfied. The value 3/2 is the "natural scale" of 3D NS in the De Giorgi framework, analogous to how (d+2)/d = 5/3 is the natural Sobolev gain exponent for d=3.

## Nature of Conjecture 14

This is an unconditional conjecture, NOT a conditional theorem. It asserts that the single bad term (non-divergence part of local pressure) can be controlled with a better exponent. The gap from beta < 4/3 to beta > 3/2 is the exact obstruction to proving NS regularity via this approach.
