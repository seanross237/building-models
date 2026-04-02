---
topic: Vasseur beta — De Giorgi recurrence exponent definition
confidence: verified
date: 2026-03-30
source: "vasseur-pressure exploration-001; Vasseur 2007 (NoDEA 14:753-785)"
---

## Finding

**Beta (beta_p) is NOT a pressure integrability exponent. It is the nonlinear recurrence exponent in the De Giorgi iteration.**

Vasseur defines nested space-time cylinders Q_k = [T_k, 1] x B_k with level set truncations v_k = [|u| - (1 - 2^{-k})]_+ and aggregated energy quantities:

```
U_k = sup_{t in [T_k,1]} int_{B_k} |v_k(t,x)|^2 dx  +  int int_{Q_k} |d_k(t,x)|^2 dx dt
```

where d_k^2 = (v_k/|u|)|nabla|u||^2 + ((1-2^{-k}) 1_{|u| >= 1-2^{-k}}/|u|)|nabla u|^2. U_k contains NO pressure term.

**Proposition 3 (equation (5)):** For p > 1, there exist universal constants C_p, beta_p > 1 such that if U_0 <= 1 then for every k > 0:

```
U_k  <=  C_p^k * (1 + ||P||_{L^p(0,1; L^1(B_0))}) * U_{k-1}^{beta_p}
```

Beta_p is the power-law nonlinearity controlling whether the recurrence drives U_k -> 0. By Lemma 4: if beta > 1 and U_0 is small enough, then U_k -> 0, giving partial regularity (Theorem 1 -> Theorem 2 -> CKN result).

## Why This Matters

The entire Vasseur regularity program hinges on the value of beta. If beta > 3/2, all suitable weak solutions are regular. The current proof achieves beta < 4/3 (see beta-current-value-four-thirds.md).
