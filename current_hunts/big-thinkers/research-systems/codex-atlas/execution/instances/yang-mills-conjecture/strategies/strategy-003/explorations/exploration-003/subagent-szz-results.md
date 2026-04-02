# SZZ Bakry-Emery Threshold: Full Derivation

**Paper:** Hao Shen, Rongchan Zhu, Xiangchan Zhu, "A stochastic analysis approach to lattice Yang-Mills at strong coupling," Commun. Math. Phys. 400, 805-851 (2023). arXiv:2204.12737.

**Published DOI:** 10.1007/s00220-022-04609-1

---

## 1. Normalization Conventions (Section 2 of SZZ)

### Inner product on su(N)

SZZ use the Hilbert-Schmidt inner product restricted to the Lie algebra:

```
<X, Y> = -Tr(XY)    for X, Y in su(N)
```

where Tr is the trace in the **fundamental representation** (N x N matrices). Since elements of su(N) are skew-Hermitian (X* = -X), this gives:

```
|X|^2 = <X, X> = -Tr(X^2) = Tr(X X*) >= 0
```

This is the **unscaled** inner product (no factor of N in front).

### The Wilson action

SZZ use **t'Hooft scaling**. Their action is:

```
S(Q) = N beta Re sum_{p in P+} Tr(Q_p)
```

where Q_p = Q_{e1} Q_{e2} Q_{e3}^{-1} Q_{e4}^{-1} is the plaquette holonomy, and P+ is the set of positively-oriented plaquettes.

**IMPORTANT:** This is **not** the same as the standard lattice convention. The relationship is:
- SZZ: S = N*beta * sum Re Tr(Q_p)
- Standard lattice: S_lat = (beta/N) * sum Re Tr(U_p)

These are the same when we identify beta_SZZ = beta_lat / N^2. The t'Hooft parameter is beta*N (the combination that stays fixed as N -> infinity). In the SZZ convention, beta is already the t'Hooft coupling divided by N, so the action coupling is N*beta = beta_tHooft.

**For SU(2):** N=2, so S = 2*beta * sum Re Tr(Q_p). The standard lattice coupling beta_lat = 4*beta_SZZ. (In standard notation, one often writes S = beta_lat sum (1/N) Re Tr(U_p).)

### Configuration space

The configuration space is the product manifold G^{E+} where E+ is the set of positively-oriented edges. Each factor G = SU(N) is equipped with the bi-invariant metric from <,> = -Tr.

---

## 2. Ricci Curvature of SU(N) with <X,Y> = -Tr(XY)

### General formula for bi-invariant metrics

For a compact Lie group G with bi-invariant metric, the curvature tensor is:

```
R(X,Y)Z = -(1/4) [[X,Y], Z]
```

The sectional curvature of the plane spanned by orthonormal X, Y is:

```
K(X,Y) = (1/4) |[X,Y]|^2
```

The Ricci curvature is obtained by tracing over an orthonormal basis {e_i}:

```
Ric(X,X) = sum_i K(X, e_i) = (1/4) sum_i |[X, e_i]|^2
```

### Connection to the Killing form

By definition of the Killing form:

```
B(X,Y) = Tr(ad_X . ad_Y) = sum_i <[X,[Y,e_i]], e_i>
```

For a bi-invariant metric, this simplifies to:

```
B(X,X) = -sum_i |[X, e_i]|^2
```

Therefore:

```
Ric(X,X) = -(1/4) B(X,X)
```

### Killing form of su(N)

For the Lie algebra su(N) (traceless skew-Hermitian N x N matrices):

```
B(X,Y) = 2N Tr(XY)
```

where Tr is the trace in the fundamental representation. (This is a standard result; see e.g. Wikipedia "Killing form" or Knapp's "Representation Theory of Semisimple Groups.")

### The Ricci curvature constant

Combining:

```
Ric(X,X) = -(1/4) B(X,X) = -(1/4)(2N Tr(X^2)) = (N/2)(-Tr(X^2)) = (N/2)|X|^2
```

Therefore:

```
Ric(X,X) / |X|^2 = N/2     for SU(N) with metric <X,Y> = -Tr(XY)
```

**For SU(2): Ric(X,X)/|X|^2 = 1.**

### Product manifold

On the product manifold G^{E+}, the Ricci curvature of a tangent vector v = (v_e)_{e in E+} is:

```
Ric(v,v) = sum_{e in E+} Ric_G(v_e, v_e) = (N/2) sum_e |v_e|^2 = (N/2)|v|^2
```

---

## 3. The Bakry-Emery Condition (Assumption 1.1)

### The condition

The Bakry-Emery condition for a measure mu = exp(-S) * vol on a Riemannian manifold M requires:

```
Gamma_2(f) >= K * Gamma_1(f)     for all smooth f
```

where Gamma_1(f) = |grad f|^2 and Gamma_2(f) = (1/2) L(Gamma_1(f)) - Gamma_1(f, Lf) with L the generator of the Langevin dynamics.

On the product manifold G^{E+} with potential S, this reduces to:

```
Ric(v,v) - Hess_S(v,v) >= K_S |v|^2     for all tangent vectors v
```

where Hess_S is the Riemannian Hessian of the potential S.

### SZZ Assumption 1.1 (exact statement)

For **SU(N)**:

```
K_S = (N+2)/2 - 1 - 8N|beta|(d-1) > 0
```

Note: **(N+2)/2 - 1 = N/2**. The peculiar decomposition (N+2)/2 - 1 comes from writing the Ricci curvature of SU(N) as (N+2)/2 - 1, which separates the Casimir eigenvalue ((N+2)/2 for the defining representation) from an offset. Regardless:

```
K_S = N/2 - 8N|beta|(d-1)
```

**K_S > 0** if and only if:

```
|beta| < 1/(16(d-1))
```

Note this is **independent of N** because both Ric and Hess S scale as N.

For **SO(N)**:

```
K_S = (N+2)/4 - 1 - 8N|beta|(d-1)
```

giving |beta| < (N-2)/(32N(d-1)).

---

## 4. Lemma 4.1: The Hessian Bound

### Statement (Lemma 4.1 of SZZ)

For the Wilson action S(Q) = N*beta * Re sum Tr(Q_p):

```
|Hess_e S(v,v)| <= 8(d-1) N |beta| |v|^2
```

where Hess_e denotes the Hessian with respect to the edge variable Q_e.

### Derivation of the 8(d-1) factor

Each edge e participates in 2(d-1) plaquettes on the d-dimensional lattice. The Hessian has two types of contributions:

**Diagonal terms** (both derivatives act on the same edge e within the same plaquette):
- Each of the 2(d-1) plaquettes contributes at most |beta|*N to the diagonal
- Total diagonal contribution: 2(d-1) N|beta|

**Off-diagonal terms** (derivatives act on different edges e, e' sharing a plaquette):
- For each pair of edges (e, e') sharing a plaquette, the cross-Hessian is bounded by N|beta|
- Careful counting of all such pairs, combined with Cauchy-Schwarz / Holder inequalities
- Total off-diagonal contribution: at most 6(d-1) N|beta|

**Combined:**

```
|Hess S(v,v)| <= (2 + 6)(d-1) N|beta| |v|^2 = 8(d-1) N|beta| |v|^2
```

### How this gives the threshold

```
K_S = Ric_min - sup|Hess S|
    = N/2 - 8(d-1) N|beta|
    > 0
```

if and only if:

```
|beta| < N / (2 * 8(d-1) * N) = 1 / (16(d-1))
```

---

## 5. Mass Gap from K_S > 0

### Poincare inequality (Theorem 1.4 / Corollary)

When K_S > 0, the infinite-volume Yang-Mills measure mu satisfies the Poincare inequality:

```
Var_mu(F) <= (1/K_S) sum_{e in E+} mu(|grad_e F|^2)
```

### Log-Sobolev inequality (Theorem 1.4)

```
mu(F^2 log F^2) <= (2/K_S) sum_{e in E+} mu(|grad_e F|^2) + mu(F^2) log mu(F^2)
```

### Mass gap (exponential decay of correlations)

The Poincare inequality with constant 1/K_S implies that correlations decay exponentially:

```
|Cov_mu(f, g)| <= C * exp(-K_S * dist(supp f, supp g))
```

The **mass gap** (inverse correlation length) is at least K_S:

```
m >= K_S = N/2 - 8N(d-1)|beta| > 0
```

### Exponential ergodicity of Langevin dynamics (Theorem 1.2)

The Langevin dynamics converges exponentially to the unique invariant measure mu:

```
W_2(nu P_t, mu) <= C(a) exp(-K_S_tilde * t)
```

where K_S_tilde is a modified constant related to K_S.

---

## 6. Specific Values for SU(2) in d=4

### Threshold

```
|beta| < 1/(16 * 3) = 1/48 ~ 0.0208
```

### Ricci curvature per edge

```
Ric = N/2 = 1     (for SU(2))
```

### Hessian bound per edge

```
|Hess S| <= 8 * 3 * 2 * |beta| = 48 |beta|
```

### Curvature constant

```
K_S = 1 - 48|beta|
```

K_S > 0 iff beta < 1/48.

### At beta = 1/48

```
K_S = 1 - 48/48 = 0     (marginal, Bakry-Emery just fails)
```

### Mass gap at beta = 0.02 (within regime)

```
K_S = 1 - 48 * 0.02 = 0.04
```

So the mass gap is at least 0.04 (in units of the lattice spacing).

---

## 7. CNS Improvement: Vertex Formulation

Cao-Nissim-Sheffield (arXiv:2509.04688, Sept 2025) improved the threshold by applying Bakry-Emery to a **sigma-model on vertices** instead of Yang-Mills on edges:

### CNS Hessian bound (vertex formulation)

```
|Hess_x S(v,v)| <= 4(d-1) N |beta| |v|^2
```

The factor is **4(d-1)** instead of 8(d-1) because:
- Each vertex has 2(d-1) adjacent edges (not 2(d-1) plaquettes per edge)
- Diagonal: 2(d-1)N|beta|
- Off-diagonal: 2(d-1)N|beta| (simpler geometry)
- Total: 4(d-1)N|beta| (half of SZZ)

### CNS threshold

```
K_S^{CNS} = N/2 - 4N(d-1)|beta| > 0  iff  |beta| < 1/(8(d-1))
```

**For d=4: beta < 1/24 ~ 0.0417** (exactly double the SZZ threshold).

### For SU(2), d=4 (CNS)

```
K_S^{CNS} = 1 - 24|beta|
```

beta < 1/24.

---

## 8. Connection to the Exploration's Conjecture

### The exploration's conjecture

```
lambda_max(Hess S(Q)) <= 4d * (beta/N)    for all Q in SU(2)^E
```

### Translating to H_norm

Define H_norm = lambda_max(Hess S) / (N/2) (the Hessian relative to the Ricci curvature).

- **SZZ Lemma 4.1 bound:** H_norm <= 8(d-1)N|beta| / (N/2) = 16(d-1)|beta|. For d=4: H_norm <= 48|beta|.
- **CNS vertex bound:** H_norm <= 4(d-1)N|beta| / (N/2) = 8(d-1)|beta|. For d=4: H_norm <= 24|beta|.
- **The exploration's conjecture:** H_norm <= 4d(beta/N) / (N/2) = 8d*beta/N^2. For N=2, d=4: H_norm <= 8|beta|.

If the exploration's conjecture lambda_max(Hess S) <= 4d(beta/N) holds, then:

```
K_S = N/2 - 4d(beta/N)
    = N/2 - 4d*beta/N
```

K_S > 0 iff beta < N^2/(8d).

**For SU(2), d=4:**

```
K_S = 1 - 4*beta > 0  iff  beta < 1/4  (= 0.25)
```

This would be a **12x improvement** over the SZZ threshold (1/48) and a **6x improvement** over the CNS threshold (1/24).

### Summary comparison (SU(2), d=4)

| Method | Hess bound | H_norm bound | beta threshold |
|--------|-----------|-------------|---------------|
| SZZ Lemma 4.1 | 48*beta | 48*beta | beta < 1/48 ~ 0.021 |
| CNS vertex | 24*beta | 24*beta | beta < 1/24 ~ 0.042 |
| **Conjecture** | **8*beta** | **8*beta** | **beta < 1/4 = 0.25** |
| SU(2) deconfinement | -- | -- | beta_c ~ 2.3 |

The conjecture beta < 1/4 pushes into physically relevant territory but is still far from the deconfinement transition at beta_c ~ 2.3 (in standard lattice normalization beta_lat = 4*beta_SZZ, so the SZZ regime beta_SZZ < 1/48 corresponds to beta_lat < 4/48 = 1/12; the conjecture beta_SZZ < 1/4 corresponds to beta_lat < 1).

### NORMALIZATION WARNING

The above table uses SZZ's t'Hooft convention. In standard lattice notation (S = beta_lat/N * sum Re Tr), the thresholds are:

| Method | Standard lattice beta threshold (d=4) |
|--------|--------------------------------------|
| SZZ | beta_lat < 4/48 = 1/12 ~ 0.083 |
| CNS | beta_lat < 4/24 = 1/6 ~ 0.167 |
| Conjecture | beta_lat < 4/4 = 1.0 |
| SU(2) deconfinement | beta_lat ~ 2.3 |

---

## 9. Key Formulas at a Glance

```
Metric on su(N):     <X,Y> = -Tr(XY)
Killing form:        B(X,Y) = 2N Tr(XY)
Ricci curvature:     Ric(X,X) = -(1/4)B(X,X) = (N/2)|X|^2
SZZ Hess bound:      |Hess S| <= 8(d-1)N|beta| |v|^2
SZZ curvature:       K_S = N/2 - 8(d-1)N|beta|
SZZ threshold:       |beta| < 1/(16(d-1))
SZZ threshold d=4:   |beta| < 1/48
Mass gap:            m >= K_S > 0
Poincare constant:   C_P = 1/K_S
```

---

## Sources

- Shen, Zhu, Zhu (2023), arXiv:2204.12737 [primary]
- Cao, Nissim, Sheffield (2025), arXiv:2509.04688 [vertex improvement]
- Atlas library: `shen-zhu-zhu-stochastic-analysis.md` [verified summary]
- Atlas library: `szz-lemma-4-1-hessian-slack.md` [numerical Hessian measurements]
- Atlas library: `szz-spectral-gap-numerical-evidence.md` [spectral gap persistence]
- Atlas library: `cao-nissim-sheffield-area-law-extension.md` [CNS improvement]
- Atlas library: `fourier-hessian-proof-q-identity.md` [H_norm = 1/12 at Q=I]
- Wikipedia "Killing form" [B(X,Y) = 2N Tr(XY) for su(N)]
- CUHK math blog [R(X,Y)Z = -(1/4)[[X,Y],Z] for bi-invariant metrics]
