# Exploration 001: Extract the Precise Definition of Beta from Vasseur (2007)

## Status: COMPLETE

## Sources

Primary source: Vasseur, A.F. "A new proof of partial regularity of solutions to Navier Stokes equations." *NoDEA: Nonlinear Differential Equations and Applications*, 14(5-6):753-785, 2007. Preprint: https://web.ma.utexas.edu/users/vasseur/documents/preprints/NS2.pdf

Supporting sources:
- Vasseur, A.F. "The De Giorgi Method for Elliptic and Parabolic Equations and Some Applications." Lecture notes, https://web.ma.utexas.edu/users/vasseur/documents/preprints/DGPekin.pdf
- Lee, M. "The De Giorgi Method with Applications to Fluid Dynamics." REU 2024, U. Chicago, https://math.uchicago.edu/~may/REU2024/REUPapers/Lee,Michael.pdf

---

## 1. The Exact Mathematical Definition of Beta

**[VASSEUR] Beta (β_p) is NOT a pressure integrability exponent. It is the nonlinear recurrence exponent in the De Giorgi iteration.**

### The De Giorgi Level Set Framework

Vasseur defines a sequence of nested space-time cylinders and truncated energy functions:

**Sets:**
- `B_k = B(½(1 + 2^{-3k}))` (nested balls in R³)
- `T_k = ½(-1 - 2^{-k})` (increasing time cutoffs)
- `Q_k = [T_k, 1] × B_k` (nested space-time cylinders)

**Level set energy functions:**
- `v_k = [|u| - (1 - 2^{-k})]_+` (truncations of velocity magnitude)
- `d_k² = (v_k/|u|)|∇|u||² + ((1-2^{-k})1_{|u|≥1-2^{-k}}/|u|)|∇u|²`

**Aggregated energy quantity:**
```
U_k = sup_{t∈[T_k,1]} ∫_{B_k} |v_k(t,x)|² dx  +  ∫∫_{Q_k} |d_k(t,x)|² dx dt
```

Note: U_k contains NO pressure term. It combines an L^∞_t(L²_x) norm of v_k and an L²(Q_k) norm of d_k. The initial quantity U_0 corresponds to the first two terms of Theorem 1's smallness condition.

### The Key Inequality (Proposition 3, equation (5))

**[VASSEUR] Proposition 3:** Let p > 1. There exist universal constants C_p, β_p > 1 depending only on p such that for any suitable weak solution to NS in [-1,1] × B(1), if U_0 ≤ 1 then for every k > 0:

```
U_k  ≤  C_p^k · (1 + ||P||_{L^p(0,1; L¹(B_0))}) · U_{k-1}^{β_p}     (5)
```

**β_p is the exponent of U_{k-1} in this recurrence.** It is the power-law nonlinearity in the De Giorgi iteration. It is NOT a Lebesgue exponent of the pressure, NOT a ratio, and NOT a parameter in a functional space condition. It is the structural exponent that controls whether the nonlinear recurrence drives U_k → 0.

### Why β > 1 suffices for partial regularity

By Lemma 4 in Vasseur: if 0 ≤ W_{k+1} ≤ C^k W_k^β with β > 1, then there exists C_0* such that W_0 < C_0* implies W_k → 0. Since β_p > 1 for all p > 1, if U_0 is small enough, then U_k → 0, which means |u| ≤ 1 on [-½,1] × B(½). This gives partial regularity (Theorem 1 → Theorem 2 → CKN result).

---

## 2. What Does Beta > 3/2 Give You?

**[VASSEUR] If β_p > 3/2 for some p > 1, then ALL suitable weak solutions to the Navier-Stokes equations in ]0,∞[ × R³ are locally bounded (and therefore regular).**

This is stated in the introduction (lines following Proposition 3) and proved rigorously in the **Appendix** of the paper.

### The Precise Statement: Conjecture 14 + Appendix Theorem

The Appendix introduces a rescaled NS equation for ε < 1:

```
∂_t u + (1/ε) div(u⊗u) + (1/ε) ∇P - Δu = 0,    div u = 0     (30)
```

with the associated local energy inequality (31).

**[VASSEUR] Conjecture 14:** There exist universal constants p > 1, C, β > 3/2 such that for any solution to (30)-(31) in [-1,1] × B(1), for every k > 0:

```
U_k  ≤  (C^k / ε) · (1 + ||P||_{L^p(0,1; L¹(B(1)))}) · U_{k-1}^β
```

**[VASSEUR] Appendix Theorem (unnumbered):** This conjecture implies that all solutions to NS in L^∞(L²) ∩ L²(H¹_0) are locally bounded.

### Proof sketch (from the Appendix)

Given any solution u and any point (t_0, x_0), define the rescaled family:
```
u_ε(t,x) = ελu(t_0 + λ²t, x_0 + λx)
P_ε(t,x) = ε²λ²P(t_0 + λ²t, x_0 + λx)
```

Then U_{ε,0} = O(ε²/λ). The condition for U_{ε,k} → 0 is:
```
U_{ε,0}  ≤  ε^{1/(β-1)}  =  ε²  ·  ε^{-(2β-3)/(β-1)}
```

Since (2β-3)/(β-1) > 0 when β > 3/2, for ε small enough this is satisfied, and U_{ε,k} → 0. This means |u_ε| ≤ 1 on [-½,½] × B(½), hence |u| is bounded near (t_0, x_0).

### The Critical Threshold 3/2

**[VASSEUR]** "Notice that 3/2 corresponds to the scale of the equation." The exponent 3/2 is the critical value because the NS scaling symmetry u_λ(t,x) = λu(λ²t, λx) gives a specific relationship between the ε and the energy. If β < 3/2, the factor ε^{-(2β-3)/(β-1)} diverges as ε → 0 in the wrong direction, and the argument fails. If β > 3/2, it converges and the argument works.

**[INTERPRETATION]** The value 3/2 is the "natural scale" of 3D Navier-Stokes in the De Giorgi framework, analogous to how (d+2)/d = 5/3 is the natural Sobolev gain exponent for d=3. The De Giorgi method's power lies in using Sobolev embedding + Chebyshev inequality to push the recurrence exponent above the natural scale. For NS, this works for ALL terms except one.

---

## 3. What is the Current Value Beta = 4/3?

### Where 4/3 comes from: The non-divergence local pressure term

**[VASSEUR]** "For p big enough, the only term for which the exponent is below the rod is the part of the local pressure term which cannot be written in a divergence form. [...] This term has an exponent strictly smaller than 4/3."

The proof of Proposition 3 (Section 4, Steps 3-6) proceeds by bounding each term on the right-hand side of the master inequality (13) with powers of U_{k-1}. Each term contributes a different exponent:

| Term | Source | Exponent of U_{k-1} | vs 3/2? |
|------|--------|---------------------|---------|
| Transport: ∫|v_k|² | Sobolev + Chebyshev | **5/3** | ✅ > 3/2 |
| Transport: ∫|v_k|³ | Sobolev + Chebyshev | **5/3** | ✅ > 3/2 |
| Nonlocal pressure P_k^1 | Harmonic regularity + Chebyshev | **5/3(1-1/p)** → 5/3 as p→∞ | ✅ > 3/2 for p > 10 |
| Local pressure P_k^{21} (divergence part) | CZ + Chebyshev | **5/3(1-1/q)** → 5/3 as q→∞ | ✅ > 3/2 for large q |
| **Local pressure P_k^{21} (non-divergence part)** | **CZ + L² of d_k** | **4/3 - 5/(3q)** → **4/3** as q→∞ | ❌ **< 3/2** |
| Local pressure P_k^{22}, P_k^{23} | CZ + Sobolev | **5/3** | ✅ > 3/2 |

**The bottleneck is a single term.** All other terms beat the 3/2 threshold. The bad term has exponent **strictly less than 4/3** (approaching 4/3 from below as q → ∞).

### The specific bad inequality

The bad term is isolated in equation (20) of the paper. The pressure P_k^{21} satisfies:

```
-ΔP_k^{21} = Σ_{i,j} ∂_i∂_j [φ_k u_j(1 - v_k/|u|) u_i(1 - v_k/|u|)]
```

By the Calderón-Zygmund / Riesz theorem: `||P_k^{21}||_{L^q} ≤ C_q` for all 1 < q < ∞. The key identity (19) is:

```
div(u P_k^{21}) + u(v_k/|u| - 1)∇P_k^{21}  =  div(v_k P_k^{21} · (uv_k/|u|))  -  P_k^{21} div(uv_k/|u|)
```

The first term (divergence form) integrates against ∇η_k and yields exponent 5/3(1-1/q) > 3/2 for large q.

**The second term** (non-divergence form) gives:
```
∫∫ |P_k^{21}| · |div(uv_k/|u|)| dx dt  ≤  ||P_k^{21}||_{L^q} · ||d_k||_{L²} · ||1_{v_k>0}||_{L^{2q/(q-2)}}
```

Using:
- ||P_k^{21}||_{L^q} ≤ C_q (CZ bound)
- ||d_k||_{L²} ~ U_{k-1}^{1/2}
- ||1_{v_k>0}||_{L^{2q/(q-2)}} ~ 2^{kα} U_{k-1}^{(d+2)/(2d) · (q-2)/q} (Chebyshev via Lemma 12)

Combined exponent of U_{k-1}: **1/2 + 5(q-2)/(6q) = 4/3 - 5/(3q)**, which approaches **4/3** from below as q → ∞.

### Connection to Calderón-Zygmund

**[INTERPRETATION]** The 4/3 exponent does NOT come directly from the standard pressure CZ bound Δp = -∂_i∂_j(u_iu_j) → ||p||_{L^q} ≤ C_q ||u||²_{L^{2q}}. Rather, it comes from the CZ bound applied to a specific piece of the decomposed pressure (P_k^{21}), combined with the L² norm of the velocity gradient proxy d_k.

However, both are intimately related. The underlying CZ structure gives P_k^{21} ∈ L^q for all q < ∞ but with bounds C_q that grow as q → ∞ (standard CZ constant growth). If one could show P_k^{21} ∈ L^∞ or even just show it has better integrability in an anisotropic sense, the exponent could be improved.

**[VASSEUR]** The 4/3 bound is NOT tight. It comes from worst-case Hölder pairings. But improving it requires either:
1. A better estimate on the non-divergence pressure term (beyond what CZ gives), OR
2. A structural cancellation that makes the non-divergence term smaller than the generic bound.

---

## 4. What is Conjecture 14?

### Precise Statement

**[VASSEUR] Conjecture 14** (p. 29 of preprint):

> There exist universal constants p > 1, C, β > 3/2 such that for any solution to the rescaled Navier-Stokes equations (30)-(31) in [-1,1] × B(1), we have for every k > 0:
>
> U_k ≤ (C^k / ε)(1 + ||P||_{L^p(0,1; L¹(B(1)))}) U_{k-1}^β

**[VASSEUR]** "Notice that after proper scaling, Proposition 3 is the equivalent to this conjecture but with a β < 3/2."

### Nature of the Conjecture

**[VASSEUR]** This is a conjecture, NOT a conditional theorem in the "if X holds then Y" sense. It is an unconditional statement about the De Giorgi iteration that, if proved, would resolve the NS regularity problem.

**[INTERPRETATION]** The conjecture is a precise quantitative strengthening of Proposition 3. It asserts that the single bad term (the non-divergence part of the local pressure) can actually be controlled with a better exponent than what the current proof achieves. The gap from β < 4/3 to β > 3/2 is the exact obstruction to proving NS regularity via this approach.

### What Would Need to Be Proved to Close the Gap

**[INTERPRETATION]** To go from 4/3 to > 3/2, one would need to improve the estimate on:

```
∫∫ |P_k^{21}| · |d_k| · 1_{v_k > 0} dx dt
```

Specifically, one needs the exponent of U_{k-1} in the bound on this integral to exceed 3/2. Currently it is 4/3 - 5/(3q) for the best available q.

Possible routes:
1. **Better pressure regularity:** Show P_k^{21} has better integrability than L^q (perhaps using the divergence-free structure of u more fully).
2. **Cancellation in the non-divergence term:** Show that -P_k^{21} div(uv_k/|u|) has a sign property or cancellation that the absolute value estimate misses.
3. **Modified iteration:** Use a different function than v_k or a different decomposition that shifts the non-divergence term into a better-controlled piece.
4. **Exploit the specific structure of P_k^{21}:** The RHS of -ΔP_k^{21} involves products u_i(1-v_k/|u|) u_j(1-v_k/|u|), which are bounded functions. This specific structure might give better estimates than generic CZ.

**[INTERPRETATION]** The gap is 1/6 = 3/2 - 4/3. This is NOT a "small" gap in the sense of perturbation theory. It represents a qualitative failure: the current method cannot extract enough nonlinearity from the pressure's interaction with the level sets.

---

## 5. The De Giorgi Iteration Structure

### Overview

The De Giorgi iteration for NS proceeds as follows:

1. **Define level sets** v_k = [|u| - (1-2^{-k})]_+ on nested cylinders Q_k.
2. **Derive the evolution equation for v_k²** (Lemma 11, equation (11)):
   ```
   ∂_t(v_k²/2) + div(u v_k²/2) + d_k² - Δ(v_k²/2) + div(uP) + (v_k/|u| - 1)u·∇P  ≤  0
   ```
3. **Multiply by cutoff η_k, integrate** to get the master inequality (13) for U_k.
4. **Bound each RHS term** with powers of U_{k-1} using Sobolev embedding + Chebyshev inequality.
5. **The bottleneck:** Step 5 (local pressure in non-divergence form) gives the worst exponent.
6. **Conclude** the nonlinear recurrence U_k ≤ C^k · U_{k-1}^β.
7. **Apply Lemma 4** (convergence of nonlinear sequences) to get U_k → 0 if U_0 small.

### Where Beta Enters

**β enters at Step 4** (the "Raise of the power exponents" step). The De Giorgi trick is:

**Chebyshev inequality on level sets:**
```
||1_{v_k > 0}||_{L^q(Q_{k-1})}  ≤  C · 2^{10k/(3q)} · U_{k-1}^{5/(3q)}
```

This comes from v_{k-1} > 2^{-k} wherever v_k > 0, so:
```
|{v_k > 0} ∩ Q_{k-1}|  ≤  2^{10k/3} ||v_{k-1}||^{10/3}_{L^{10/3}}  ≤  2^{10k/3} U_{k-1}^{5/3}
```

**Sobolev embedding + interpolation:**
```
||v_{k-1}||_{L^{10/3}(Q_{k-1})}  ≤  C · U_{k-1}^{1/2}
```

When bounding a term like ∫|v_k|^a |f| dx dt, one writes:
```
∫ |v_k|^a |f| dx dt  ≤  ||v_k||^a · ||f|| · ||1_{v_k>0}||
```

The exponent of U_{k-1} is: (contribution from ||v_k||^a) + (contribution from ||f||) + (contribution from ||1_{v_k>0}||).

The specific contributions from each term in the master inequality:
- **Transport terms** (∫v_k², ∫v_k³): Sobolev gives ||v_k||^2_{L^{10/3}} ≤ CU_{k-1}, and Chebyshev gives ||1_{v_k>0}|| ~ U_{k-1}^{2/3}. Combined: U_{k-1}^{5/3}.
- **Non-divergence pressure term:** ||P_k^{21}||_{L^q} ≤ C_q (a constant, independent of U_{k-1}!), ||d_k||_{L²} ~ U_{k-1}^{1/2}, ||1_{v_k>0}||_{L^{2q/(q-2)}} ~ U_{k-1}^{5(q-2)/(6q)}. Combined: U_{k-1}^{4/3 - 5/(3q)}.

**β_p is the MINIMUM over all such exponents** (across all terms). For p > 10:
```
β_p  =  min(5/3, 5/3(1-1/p), 4/3 - 5/(3q), ...)  =  4/3 - 5/(3q)  <  4/3
```

### Why the Non-Divergence Term is Special

The pressure P_k^{21} is bounded in L^q by CZ, but this bound is a CONSTANT (C_q), not a power of U_{k-1}. All other terms contribute at least U_{k-1}^{1/2} from their own norm, but P_k^{21} contributes U_{k-1}^0 = 1. This is because:

```
-ΔP_k^{21} = Σ ∂_i∂_j [φ_k u_j(1-v_k/|u|) u_i(1-v_k/|u|)]
```

The factors u(1-v_k/|u|) are BOUNDED BY 1 (Lemma 10), so the RHS is bounded independently of U_{k-1}. By CZ/Riesz: ||P_k^{21}||_{L^q} ≤ C_q. No additional power of U_{k-1} can be extracted.

This is the fundamental obstruction: **the pressure is not small even when the velocity is close to its level set truncation.**

---

## 6. Computable Specification of Beta_effective

### Mathematical Framework for Measurement

Given the De Giorgi iteration structure, there are two natural ways to define a "beta_effective" from DNS data:

### Approach A: Direct Iteration Measurement

Compute the sequence U_k for k = 0, 1, 2, ..., K and fit the recurrence.

```python
import numpy as np
from scipy.fft import fftn, ifftn

def compute_beta_effective_iteration(u, p, dx, dt, K_max=10):
    """
    Compute beta_effective by measuring the De Giorgi recurrence exponent
    from DNS velocity field u and pressure p.

    Parameters:
    -----------
    u : ndarray, shape (Nt, 3, Nx, Ny, Nz) — velocity field time series
    p : ndarray, shape (Nt, Nx, Ny, Nz) — pressure field time series
    dx : float — grid spacing (assumed uniform)
    dt : float — time step between snapshots
    K_max : int — number of De Giorgi levels to compute

    Returns:
    --------
    beta_eff : float — fitted recurrence exponent
    U_k_values : list — sequence of U_k values

    Notes:
    ------
    ADAPTATION FOR PERIODIC DOMAINS:
    The original De Giorgi iteration uses nested balls B_k.
    On a periodic domain, we use the full domain for all k
    (no spatial nesting). This is valid because on a periodic
    domain with finite volume, all B_k = full domain.
    The time nesting T_k = ½(-1 - 2^{-k}) is adapted to the
    available time window.
    """
    Nt, _, Nx, Ny, Nz = u.shape
    vol = (Nx * Ny * Nz) * dx**3

    # Compute |u| at each grid point and time
    u_mag = np.sqrt(np.sum(u**2, axis=1))  # shape (Nt, Nx, Ny, Nz)

    # Normalize so that the L^infty_t(L^2_x) + L^2_t(H^1_x) ≤ 1
    # (required for De Giorgi iteration to apply)
    energy_sup = np.max([np.sum(u_mag[t]**2) * dx**3 for t in range(Nt)])
    grad_u = compute_gradient(u, dx)  # shape (Nt, 3, 3, Nx, Ny, Nz)
    grad_energy = np.sum(np.sum(grad_u**2, axis=(1,2)) * dx**3 * dt)
    normalization = np.sqrt(energy_sup + grad_energy)
    u_normalized = u / normalization
    u_mag_norm = u_mag / normalization

    U_k_values = []

    for k in range(K_max + 1):
        C_k = 1.0 - 2.0**(-k)  # level set threshold

        # v_k = [|u| - C_k]_+
        v_k = np.maximum(u_mag_norm - C_k, 0.0)  # shape (Nt, Nx, Ny, Nz)

        # d_k^2 ≈ |∇|u||^2 on {|u| ≥ C_k}  (simplified)
        # More precisely: d_k^2 = (v_k/|u|)|∇|u||^2 + (C_k 1_{|u|≥C_k}/|u|)|∇u|^2
        grad_u_mag = compute_scalar_gradient(u_mag_norm, dx)  # (Nt, 3, Nx, Ny, Nz)
        grad_u_mag_sq = np.sum(grad_u_mag**2, axis=1)  # (Nt, Nx, Ny, Nz)

        mask = (u_mag_norm > 1e-10)
        d_k_sq = np.where(mask,
            (v_k / u_mag_norm) * grad_u_mag_sq +
            (C_k * (u_mag_norm >= C_k).astype(float) / u_mag_norm) *
            np.sum(np.sum(compute_gradient(u_normalized, dx)**2, axis=1), axis=1),
            0.0
        )

        # U_k = sup_t ∫ v_k^2 dx  +  ∫∫ d_k^2 dx dt
        v_k_sq_integral = np.array([np.sum(v_k[t]**2) * dx**3 for t in range(Nt)])
        sup_v_k = np.max(v_k_sq_integral)

        d_k_sq_integral = np.sum(d_k_sq) * dx**3 * dt

        U_k = sup_v_k + d_k_sq_integral
        U_k_values.append(U_k)

    # Fit beta: log(U_k) ≈ k*log(C_p) + beta * log(U_{k-1})
    # For k = 1, ..., K_max
    log_U = np.log(np.array(U_k_values) + 1e-300)

    # Linear regression: log(U_k) = a*k + beta * log(U_{k-1})
    # Using k = 2, ..., K_max (skip k=0,1 for stability)
    k_vals = np.arange(2, K_max + 1)
    Y = log_U[2:]
    X = np.column_stack([k_vals, log_U[1:-1]])

    # Least squares fit
    coeffs = np.linalg.lstsq(X, Y, rcond=None)[0]
    beta_eff = coeffs[1]

    return beta_eff, U_k_values


def compute_scalar_gradient(f, dx):
    """Compute gradient of scalar field using spectral methods."""
    # Spectral differentiation on periodic domain
    Nt = f.shape[0]
    Nx, Ny, Nz = f.shape[1], f.shape[2], f.shape[3]
    kx = np.fft.fftfreq(Nx, d=dx/(2*np.pi))
    ky = np.fft.fftfreq(Ny, d=dx/(2*np.pi))
    kz = np.fft.fftfreq(Nz, d=dx/(2*np.pi))
    KX, KY, KZ = np.meshgrid(kx, ky, kz, indexing='ij')

    grad = np.zeros((Nt, 3, Nx, Ny, Nz))
    for t in range(Nt):
        f_hat = fftn(f[t])
        grad[t, 0] = np.real(ifftn(1j * KX * f_hat))
        grad[t, 1] = np.real(ifftn(1j * KY * f_hat))
        grad[t, 2] = np.real(ifftn(1j * KZ * f_hat))
    return grad


def compute_gradient(u, dx):
    """Compute gradient tensor of vector field."""
    Nt, nc, Nx, Ny, Nz = u.shape
    grad = np.zeros((Nt, nc, 3, Nx, Ny, Nz))
    for i in range(nc):
        grad[:, i, :, :, :, :] = compute_scalar_gradient(u[:, i], dx)
    return grad
```

### Approach B: Bottleneck Term Measurement

Directly measure the exponent of U_{k-1} in the non-divergence pressure term that is the sole bottleneck.

```python
def compute_beta_bottleneck(u, p, dx, dt, K_max=10, q_CZ=4.0):
    """
    Compute the exponent of U_{k-1} in the non-divergence pressure term.

    This measures the specific term that limits beta:
    I_k = ∫∫ |P_k^{21}| · |d_k| · 1_{v_k > 0} dx dt

    Theoretical prediction: I_k ~ U_{k-1}^{4/3 - 5/(3q)}

    Parameters:
    -----------
    u, p, dx, dt : as above
    K_max : int
    q_CZ : float — Lebesgue exponent for CZ estimate (default 4)

    Returns:
    --------
    beta_bottleneck : float — empirical exponent of the bottleneck term
    I_k_values : list — measured integrals
    U_k_values : list — energy sequence

    Notes:
    ------
    P_k^{21} requires solving: -ΔP_k^{21} = Σ ∂_i∂_j[φ_k u_j(1-v_k/|u|) u_i(1-v_k/|u|)]
    On a periodic domain, this is done spectrally.
    The theoretical beta = 4/3 - 5/(3q) ≈ 0.917 for q=4.
    If empirical beta_bottleneck > 1.5, it suggests the CZ bound
    has massive slack in the De Giorgi context.
    """
    # [Implementation would compute P_k^{21} via spectral Poisson solve
    #  with the specific RHS, then measure the integral I_k for each k,
    #  and fit log(I_k) vs log(U_{k-1}) to extract the exponent]
    pass
```

### Approach C: CZ Slack as Proxy

**[INTERPRETATION]** A simpler and more robust proxy: measure the ratio between the theoretical CZ bound on P_k^{21} and its actual value. If the CZ bound has slack factor S, the effective β is modified:

```
β_effective ≈ 4/3 - 5/(3q) + (contribution from CZ slack)
```

This connects to the prior finding that CZ bounds on the full pressure have slack 7.6–17.5×. If similar slack exists for P_k^{21}, it might effectively increase β.

---

## 7. DNS Computability Assessment

### Verdict: **PARTIALLY** computable

### What CAN Be Computed from DNS

1. **U_k for finite k:** The energy quantities U_k = sup_t ∫ v_k² dx + ∫∫ d_k² dx dt are standard L^p norms computable on any grid. ✅

2. **The recurrence exponent via regression:** Given U_0, U_1, ..., U_K, one can fit log(U_k) vs log(U_{k-1}) to extract an empirical β. ✅

3. **The pressure decomposition P = P_k^1 + P_k^2:** This requires solving Poisson equations with specific RHS, which is standard on periodic domains via FFT. ✅

4. **The specific bottleneck integral I_k:** The integral ∫∫ |P_k^{21}| |d_k| 1_{v_k>0} dx dt involves only pointwise operations and spatial integration. ✅

5. **CZ slack in the De Giorgi context:** Compare ||P_k^{21}||_{L^q} with C_q for specific q values. ✅

### What CANNOT Be Computed (or is problematic)

1. **The limit k → ∞:** The De Giorgi method requires k → ∞. On a finite grid with resolution N, the level sets v_k become trivial (empty) for k large enough that 2^{-k} is below the grid resolution δx·U_∞. The iteration cannot be pushed beyond k ~ log₂(||u||_∞ / δx · ||u||_{min}). This gives maybe 10-15 useful levels on a 512³ grid. **Partially limiting but workable.**

2. **The nested ball geometry:** The original De Giorgi iteration uses nested balls B_k = B(½(1+2^{-3k})) that shrink to B(½). On a periodic domain, there are no boundaries, so one natural adaptation is to use the full domain for all k (the spatial nesting becomes trivial). This changes the geometric constants but not the structural exponent. **Adaptable.**

3. **The ε → 0 limit in the Appendix argument:** The Appendix proof of "β > 3/2 implies regularity" sends ε → 0 in the rescaled equations. This is an analytical limit, not a computational one. DNS cannot directly probe this limit. **Not computable—but not needed for measuring β itself.**

4. **Universality:** A single DNS run measures β for one specific flow. The theorem requires β to hold for ALL solutions. DNS can provide evidence but not proof. **Fundamental limitation.**

### Practical Assessment

**For measuring β_effective, DNS is well-suited.** The key quantities (U_k, the pressure decomposition, the bottleneck integral) are all computable on a periodic grid. The main adaptations needed:

1. Replace nested balls with full periodic domain (or use windowed sub-domains as an analogue).
2. Normalize so U_0 ≤ 1 (simple rescaling).
3. Compute for k = 0, 1, ..., K_max where K_max ~ 10-15 for typical resolutions.
4. Use spectral methods for the Poisson solves in the pressure decomposition.

**Key question for DNS:** Does the empirical β exceed 4/3? If so, the CZ bound has exploitable slack in the De Giorgi context. Does it exceed 3/2? That would be dramatic evidence for regularity.

### Obstacles Summary

| Obstacle | Severity | Workaround |
|----------|----------|------------|
| Finite k | Low | ~10-15 levels suffice for fitting |
| No nested balls | Low | Use full periodic domain or windowed sub-domains |
| Resolution limits on v_k | Medium | Limits K_max; use highest resolution available |
| Single-flow non-universality | High | Run multiple ICs (Taylor-Green, anti-parallel, random) |
| Cannot prove β > 3/2 | Fundamental | DNS provides evidence, not proof |

---

## Key Distinctions

### Beta (De Giorgi exponent) vs CZ Slack

- **β_p** is a structural exponent in the De Giorgi iteration: it measures the nonlinear gain per iteration step.
- **CZ slack** is the ratio ||p||_{L^q} / (C_q ||u||²_{L^{2q}}) — how tight the CZ bound is on the full pressure.
- **They are related but distinct.** CZ slack enters the β calculation through the bound on P_k^{21}, but β also depends on the Sobolev gain, the Chebyshev inequality structure, and the geometric constants of the nested sets. **It is theoretically possible for CZ slack to be large but β to remain < 3/2** (if the slack doesn't occur in the right place), and vice versa.

### Worst-Case vs Typical-Case

- **[VASSEUR]** β < 4/3 is a worst-case analytical bound. The proof uses Hölder inequality at every step, which can introduce significant slack.
- **[INTERPRETATION]** The empirical β from DNS might be much larger than 4/3, because the worst-case Hölder pairings may never be saturated for actual NS flows. The 7.6-17.5× CZ tightness suggests there IS slack, and the De Giorgi iteration might exploit it.
- **[INTERPRETATION]** The value 4/3 is NOT tight. It is the limit of 4/3 - 5/(3q) as q → ∞, and one never takes q = ∞ (the CZ constant diverges). The actual β for any finite q used in the proof is strictly less than 4/3.
