---
topic: De Giorgi iteration structure for Navier-Stokes
confidence: verified
date: 2026-03-30
source: "vasseur-pressure exploration-001; Vasseur 2007 Section 4, Lemma 11-12"
---

## Finding

The De Giorgi iteration for NS proceeds through 7 steps:

1. **Define level sets** v_k = [|u| - (1-2^{-k})]_+ on nested cylinders Q_k.
2. **Derive evolution equation for v_k^2** (Lemma 11, eq. (11)):
   ```
   partial_t(v_k^2/2) + div(u v_k^2/2) + d_k^2 - Delta(v_k^2/2) + div(uP) + (v_k/|u| - 1)u*nabla P  <=  0
   ```
3. **Multiply by cutoff eta_k, integrate** to get master inequality (13) for U_k.
4. **Bound each RHS term** with powers of U_{k-1} using Sobolev + Chebyshev. This is where beta enters ("Raise of the power exponents").
5. **The bottleneck:** Local pressure in non-divergence form gives worst exponent (Step 5 of Section 4).
6. **Conclude** the nonlinear recurrence U_k <= C^k * U_{k-1}^beta.
7. **Apply Lemma 4** (convergence of nonlinear sequences) to get U_k -> 0 if U_0 small.

### The De Giorgi trick (Step 4)

**Chebyshev inequality on level sets:**
```
||1_{v_k > 0}||_{L^q(Q_{k-1})}  <=  C * 2^{10k/(3q)} * U_{k-1}^{5/(3q)}
```

This comes from v_{k-1} > 2^{-k} wherever v_k > 0, combined with Sobolev embedding:
```
||v_{k-1}||_{L^{10/3}(Q_{k-1})}  <=  C * U_{k-1}^{1/2}
```

For each term int|v_k|^a |f| dx dt, the exponent of U_{k-1} is the sum of contributions from ||v_k||^a, ||f||, and ||1_{v_k>0}||.

### beta_p as minimum

beta_p = min over all term exponents. For p > 10, the minimum is 4/3 - 5/(3q), achieved by the non-divergence pressure term (see beta-current-value-four-thirds.md).
