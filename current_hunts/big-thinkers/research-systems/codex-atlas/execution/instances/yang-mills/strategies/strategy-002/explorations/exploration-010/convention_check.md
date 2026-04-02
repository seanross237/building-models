# SZZ Convention Check — arXiv:2204.12737

**Paper:** "A stochastic analysis approach to lattice Yang-Mills at strong coupling"
**Authors:** Hao Shen, Rongchan Zhu, Xiangchan Zhu
**Published:** Comm. Math. Phys. (2022), DOI: 10.1007/s00220-022-04609-1
**Source:** Full text extracted from arXiv PDF v1, 27 Apr 2022 (43 pages)

---

## 1. Wilson Action Formula

**Equation (1.2), page 4:**

The action (called S, not "Wilson action" explicitly) is:

```
S(Q) = Nβ Re Σ_{p ∈ P⁺_ΛL} Tr(Q_p)
```

where Q_p = Q_{e1} Q_{e2} Q_{e3} Q_{e4} is the ordered product around plaquette p = e1 e2 e3 e4.

The measure (Equation (1.1)) is:

```
dμ_{ΛL,N,β}(Q) = Z^{-1}_{ΛL,N,β} exp(S(Q)) Π_{e ∈ E⁺_ΛL} dσ_N(Q_e)
```

**Key conventions:**

- **Sign: POSITIVE.** The measure is exp(+S), and S = +Nβ Re Tr(Q_p). So higher Re Tr(Q_p) is energetically favored (plaquettes closer to identity are favored at positive β). This is the standard attractive convention.
- **Prefactor: Nβ (not β/N).** The 't Hooft scaling is explicit: the action is multiplied by Nβ, not β/N. This means β here is the 't Hooft coupling divided by N, i.e., their β corresponds to β_{physics}/N² in the standard lattice gauge theory convention where S = (β/2N) Σ Re Tr(U_□).
- **No 1/N inside the trace.** The trace Tr is the standard (unnormalized) matrix trace. The factor of N sits outside as a multiplier Nβ.
- **Sum over P⁺ only** (positively oriented plaquettes), not over all plaquettes. This avoids double-counting.
- **Re can be omitted for SO(N)** since all matrices are real.
- **Negatively oriented edges:** Q_e = Q^{-1}_{e^{-1}} for e ∈ E⁻, so Q_p = Q_{e1} Q_{e2} Q*_{e3} Q*_{e4} when e3, e4 are negatively oriented (since Q^{-1} = Q* for SO(N) and SU(N)).

**Comparison with standard physics convention:**

The standard Wilson action in lattice gauge theory is typically written:

```
S_{Wilson} = (β/N) Σ_□ Re Tr(U_□)        [physics convention]
```

or equivalently β Σ_□ (1/N) Re Tr(U_□). In SZZ, the action is Nβ_{SZZ} Σ Re Tr(Q_p).

So: **Nβ_{SZZ} = β_{physics}/N**, meaning **β_{SZZ} = β_{physics}/N²**.

When SZZ write β < 1/(16(d-1)), this translates to β_{physics} < N²/(16(d-1)). For SU(2) in d=4: β_{physics} < 4/48 = 1/12 ≈ 0.083. The SU(2) deconfinement transition is at β_{physics} ≈ 2.3, so the SZZ regime is far into strong coupling.

**WAIT — alternative reading:** SZZ explicitly say "t' Hooft scaling βN for the inverse coupling strength" (abstract). This means their convention is that the total coupling is βN, not β alone. If we identify βN with the standard lattice β_{std}/N (i.e., β_{std} = N²β_{SZZ}), then:

For SU(N): β_{SZZ} < 1/(16(d-1)) means β_{std} = N²β_{SZZ} < N²/(16(d-1)).

But another common convention sets S = β Σ Re Tr(U_□) (no 1/N), in which case β_{std} = Nβ_{SZZ} and β_{std} < N/(16(d-1)). For SU(2), d=4: β_{std} < 2/48 ≈ 0.042.

**The key point is that SZZ's β is NOT the standard lattice β.** Their total coupling prefactor is Nβ multiplying Re Tr(Q_p), where Tr is the unnormalized trace.

---

## 2. Inner Product on the Lie Algebra

**Equation (2.3), page 9:**

They endow M_N(C) with the Hilbert-Schmidt inner product:

```
⟨X, Y⟩ = Re Tr(XY*)       ∀ X, Y ∈ M_N(C)
```

Then (immediately following, same page):

> "We restrict this inner product to our Lie algebra g, which is then invariant under the adjoint action. In particular for X, Y ∈ so(N) or su(N) we have ⟨X, Y⟩ = −Tr(XY). Note that Tr(XY) ∈ R since we have Tr((XY)*) = Tr(Y*X*) = Tr(XY), and Tr(A*) = Tr(A) for any A ∈ M_N(C)."

**So the inner product on g = su(N) or so(N) is:**

```
⟨X, Y⟩ = −Tr(XY)
```

**This means |X|² = −Tr(X²) for X ∈ su(N) or so(N).**

**Derivation:** For X ∈ su(N), we have X* = −X (skew-Hermitian). So:
Re Tr(XY*) = Re Tr(X(−Y)) = −Re Tr(XY) = −Tr(XY) (the last equality since Tr(XY) is real for skew-Hermitian X, Y).

**This is NOT the same as:**
- The Killing form: B(X,Y) = 2N Tr(XY) for su(N), which would give ⟨X,Y⟩_{Killing} = −2N Tr(XY) = 2N|X|²_{SZZ}.
- A normalized trace convention: (1/2) Tr(X†X) or similar.

**The SZZ inner product is the standard Hilbert-Schmidt inner product restricted to the Lie algebra.** It is proportional to the Killing form: ⟨X,Y⟩_{SZZ} = −Tr(XY) = (1/2N) B(X,Y) for su(N).

**The tangent space inner product** (page 9) is defined by right translation:

> "The inner product on g induces an inner product on the tangent space at every Q ∈ G via the right multiplication on G. Hence, for X, Y ∈ g, we have XQ, YQ ∈ T_Q G, and their inner product is given by Tr((XQ)(YQ)*) = Tr(XY*). This yields a bi-invariant Riemannian metric on G."

---

## 3. Lemma 4.1 — Hessian Bound

**Lemma 4.1, page 17 (equation (4.2)):**

> "**Lemma 4.1.** For v = XQ ∈ T_Q Q_L we have
>
> |HessS(v, v)| ≤ 8(d−1)N|β| |v|²."

**The coefficient is 8(d-1)N|β|.**

### Full Context and Proof Sketch

The text preceding Lemma 4.1 (page 17):

> "We first compute HessS(v,v) for v ∈ T_Q Q_L. Note that as a 'naive' guess, S defined in (1.2) would appear to be of order N², since the trace of the orthogonal or unitary matrix Q_p would be generally bounded by N and there is another factor N outside the summation. If the Hessian of S was indeed of order N², or N^p for any p > 1, then in Assumption 1.1 we would never be able to fix β small uniformly in N and ensure that K_S is strictly positive when N gets large. Fortunately in the next lemma by properly arranging terms and using Hölder inequalities we prove that the Hessian is actually at most of order N."

### Proof Structure

The proof (pages 17-19) proceeds as follows:

1. Write v = XQ with X ∈ q_L (the Lie algebra of Q_L).
2. Since ∇_v v = 0 for right-invariant vector fields, HessS(v,v) = v(v(S)) = Σ_{e,ē} (X_ē Q_ē)(X_e Q_e) S.
3. **Diagonal terms (e = ē):** For each edge e, the plaquette p contributes only if p contains e or e⁻¹. There are 2(d-1) such plaquettes. Each second derivative produces terms of the form Tr(Y₁ Q_{e1} Y₂ Q_{e2} Q*_{e3} Y₃* Q*_{e4} Y₄*) with one Y = X_e² and three Y = I_N. By Cauchy-Schwarz for the Hilbert-Schmidt inner product, each is bounded by |X_e|². Summing: diagonal contribution ≤ 2(d-1)|β| |v|².

4. **Off-diagonal terms (e ≠ ē):** There is at most one plaquette containing both e and ē. The second derivative produces Tr(...X_e...X_ē...). By Cauchy-Schwarz: each term ≤ |X_e||X_ē| ≤ (1/2)(|X_e|² + |X_ē|²). Combinatorial counting over plaquettes gives: off-diagonal contribution ≤ 6(d-1)|β| |v|².

5. **Total:** (1/N)·(diagonal + off-diagonal) ... wait, re-reading more carefully:

The actual accounting from the paper (page 18-19):

Diagonal part:
```
(1/N) Σ_{e∈E⁺} Σ_{p∈P_e} |β||X_e|² = 2|β|(d−1) Σ|X_e|² = 2(d−1)|β||v|²
```

Wait — the (1/N) factor is NOT present in the paper's accounting. Let me re-examine. The action is S = Nβ Re Σ Tr(Q_p). The factor N is part of S, so the Hessian of S inherits it. The proof bounds:

```
(1/N) Σ_{e=ē} |(X_ē Q_ē)(X_e Q_e)S| ≤ 2(d−1)|β||v|²
```

and

```
(1/N) Σ_{e≠ē} |(X_ē Q_ē)(X_e Q_e)S| ≤ 6(d−1)|β||v|²
```

These are bounds on the Hessian divided by N (i.e., each individual trace term is O(1) after the Cauchy-Schwarz, and the Nβ prefactor in S gives an N|β| overall, but the proof extracts an N from the bound to get the form without explicit N). Then the total bound is:

```
|HessS(v,v)| ≤ N · [2(d−1)|β| + 6(d−1)|β|] · |v|² = 8(d−1)N|β| |v|²
```

**The crucial point:** Despite S having an Nβ prefactor (seemingly O(N²) for the Hessian since Tr(Q_p) ~ O(N)), the actual Hessian is only O(N) because the second derivatives of Tr(Q_p) via Cauchy-Schwarz produce terms bounded by |X_e||X_ē| (which is O(1) in N, not O(N)), and the only N factor comes from the Nβ prefactor in S.

### How This Feeds Into the Bakry-Emery Condition

**Equation (4.7), page 19:**

The Bakry-Emery condition requires:

```
Ric(v,v) − HessS(v,v) ≥ K_S |X|²
```

**Ricci curvature** (equation (4.8), citing [AGZ10, (F.6)]):

```
Ric(u,u) = (α(N+2)/4 − 1) |u|²
```

where α = 1 for SO(N), α = 2 for SU(N).

For SU(N): Ric(v,v) = ((2(N+2)/4) − 1)|v|² = (N/2)|v|²

**Combined (Assumption 1.1 for SU(N)):**

```
K_S = (N+2)/2 − 1 − 8N|β|(d−1) = N/2 − 8N(d−1)|β|
```

K_S > 0 requires |β| < 1/(16(d-1)).

In d = 4: |β| < 1/48.

---

## 4. Additional Conventions

### Trace Convention
- **Tr is the standard unnormalized matrix trace.** Not tr = (1/N)Tr.
- The normalized trace does not appear in the action formula.

### Orthonormal Basis of su(N)
SZZ use the standard basis (citing [AGZ10, Proposition E.15]):

For su(N), the orthonormal basis (w.r.t. ⟨X,Y⟩ = −Tr(XY)) consists of:
- D_k = (i/√2)(e_{kk} − e_{(k+1)(k+1)}) for 1 ≤ k < N
- E_{kn} = (1/√2)(e_{kn} − e_{nk}) for 1 ≤ k < n ≤ N
- F_{kn} = (i/√2)(e_{kn} + e_{nk}) for 1 ≤ k < n ≤ N

For so(N):
- E_{kn} = (1/√2)(e_{kn} − e_{nk}) for 1 ≤ k < n ≤ N

### Brownian Motion Convention
The Langevin SDE (equation (1.5)):

```
dQ = ∇S(Q) dt + √2 dB
```

where B = (B_e) are independent Brownian motions on G. The √2 factor is the standard convention for Langevin dynamics with invariant measure proportional to exp(S).

### Casimir Element
For SU(N): the drift has a term −((N²−1)/N) Q_e dt arising from the Casimir element (Ito correction from Brownian motion on the group manifold).

For SO(N): the corresponding term is −(1/2)(N−1) Q_e dt.

---

## 5. Summary Table

| Convention | SZZ Value | Notes |
|-----------|-----------|-------|
| Action sign | S = +Nβ Re Σ Tr(Q_p) | Positive; measure is exp(+S) |
| Coupling prefactor | Nβ (t'Hooft scaling) | NOT β/N; their β is NOT the standard lattice β |
| Inner product on g | ⟨X,Y⟩ = −Tr(XY) | = Re Tr(XY*) restricted to su(N)/so(N) |
| Norm on g | \|X\|² = −Tr(X²) | Standard Hilbert-Schmidt |
| Trace | Unnormalized Tr | Standard matrix trace |
| Ricci curvature (SU(N)) | N/2 per unit | Ric(u,u) = (N/2)\|u\|² |
| Ricci curvature (SO(N)) | (N-2)/4 per unit | Ric(u,u) = ((N+2)/4 − 1)\|u\|² |
| Hessian bound (Lemma 4.1) | \|HessS(v,v)\| ≤ 8(d−1)N\|β\|\|v\|² | Coefficient is 8(d−1)N\|β\| |
| Bakry-Emery threshold (SU(N)) | \|β\| < 1/(16(d−1)) | d=4: β < 1/48 |
| Bakry-Emery threshold (SO(N)) | \|β\| < (N−2)/(32(d−1)N) | Depends on N |
