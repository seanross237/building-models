# Exploration 002: Tao Filter for the Harmonic Far-Field Pressure Loophole

## 1. Executive verdict

- [VERIFIED] Tao's primary-source construction replaces the ordinary Navier-Stokes bilinear term

  ```text
  B(u,v) = -(1/2) P[(u·∇)v + (v·∇)u]
  ```

  by an averaged operator `\tilde B` built from rotations, dilations, and order-zero Fourier multipliers; see Tao (2016), equations (1.12)-(1.13) and Theorem 1.5.
- [VERIFIED] Tao also states a primitive-variable reformulation

  ```text
  ∂_t u + T(u,u) = Δu - ∇p,
  div u = 0,
  ```

  where `T` is an averaged version of `(u·∇)u`; see Tao (2016), Remark 1.6.
- [CHECKED] Taking divergence of Tao's Remark 1.6 formula gives the averaged pressure law

  ```text
  -Δp = div T(u,u),
  ```

  not the ordinary local tensor law `-Δp = ∂i∂j(u_i u_j)`.
- [CHECKED] A harmonic far-field pressure component still exists in a purely formal elliptic sense after one splits the source `div T` into near and far pieces. But the loophole needs more than that: it needs the source to come from the **local quadratic tensor in the physical velocity field**, so that "far field" means genuinely distant fluid.
- [CHECKED] Tao's averaging destroys exactly that locality by inserting order-zero pseudodifferential operators before the pressure solve.
- [VERIFIED] Verdict: **`Tao-incompatible`**.
- [CHECKED] The new bottleneck in the averaged setting is not a Vasseur-style local pressure slot such as `P_{k21}`. It is the already-nonlocal averaged convection/pressure package `T(u,u)` (equivalently `\tilde B(u,u)` after Leray projection). Any harmonic far-field split of `p` is then bookkeeping on top of a source that has already mixed near and far data.

## 2. Tao averaged equation and pressure law

### 2.1 Ordinary NS operator in Tao's setup

- [VERIFIED] Tao writes the Navier-Stokes dynamics abstractly as

  ```text
  ∂_t u = Δu + B(u,u).
  ```

- [VERIFIED] In the same source, Tao gives the unaveraged bilinear operator as

  ```text
  B(u,v) = -(1/2) P[(u·∇)v + (v·∇)u],
  ```

  where `P` is the Leray projection. Tao's blog announcement from February 4, 2014 reproduces the same formula, matching the paper.
- [VERIFIED] Tao also records the Leray projection componentwise as

  ```text
  (Pu)_i = u_i - Δ^{-1} ∂_i ∂_j u_j.
  ```

- [CHECKED] From this ordinary formula one recovers the standard primitive-variable law

  ```text
  ∂_t u + (u·∇)u = Δu - ∇p,
  div u = 0,
  -Δp = ∂i∂j(u_i u_j).
  ```

### 2.2 Tao's averaged operator

- [VERIFIED] Tao defines an averaged Euler bilinear operator `\tilde B` by duality as

  ```text
  <\tilde B(u,v), w>
    := E < B(m1(D) Rot_{R1} Dil_{λ1} u,
             m2(D) Rot_{R2} Dil_{λ2} v),
             m3(D) Rot_{R3} Dil_{λ3} w) >,
  ```

  where the `m_i(D)` are random real order-zero Fourier multipliers, `R_i` are random rotations, and `λ_i` are random dilations; see Tao (2016), equation (1.12).
- [VERIFIED] Tao then rewrites this in integral form as

  ```text
  <\tilde B(u,v), w>
    = ∫_Ω < B(m_{1,ω}(D) Rot_{R1,ω} Dil_{λ1,ω} u,
              m_{2,ω}(D) Rot_{R2,ω} Dil_{λ2,ω} v),
              m_{3,ω}(D) Rot_{R3,ω} Dil_{λ3,ω} w > dμ(ω),
  ```

  with bounded dilation range and integrable multiplier seminorms; see Tao (2016), equation (1.13).
- [VERIFIED] Tao's averaged Navier-Stokes equation is

  ```text
  ∂_t u = Δu + \tilde B(u,u),
  ```

  and mild solutions satisfy

  ```text
  u(t) = e^{tΔ} u_0 + ∫_0^t e^{(t-t')Δ} \tilde B(u(t'),u(t')) dt';
  ```

  see Tao (2016), equations (1.9) and (1.15), plus Theorem 1.5.

### 2.3 What replaces `-Δp = ∂i∂j(u_i u_j)`?

- [VERIFIED] Tao explicitly remarks that one can rewrite the averaged system in primitive-variable form as

  ```text
  ∂_t u + T(u,u) = Δu - ∇p,
  div u = 0,
  ```

  where `T = (1/2)(T_{12} + T_{21})` and

  ```text
  T_{ij}(u,u)
    := ∫_Ω Rot^{-1}_{R3,ω} m_{3,ω}(D)
         ((m_{i,ω}(D) Rot_{Ri,ω} u · ∇)
          m_{j,ω}(D) Rot_{Rj,ω} u) dμ(ω),
  ```

  for `ij = 12, 21`; see Tao (2016), Remark 1.6.
- [CHECKED] Taking divergence of Tao's primitive-form equation and using `div u = 0` gives

  ```text
  -Δp = div T(u,u).
  ```

  This is the averaged replacement for the ordinary NS pressure law.
- [CHECKED] The crucial difference is algebraic, not merely notational:

  ```text
  ordinary NS:  div T_NS(u,u) = div((u·∇)u) = ∂i∂j(u_i u_j),
  Tao averaged: div T(u,u) with T a bilinear pseudodifferential operator.
  ```

- [CHECKED] Remark 1.4 in Tao's paper notes that one rotation and one dilation can be eliminated by symmetry if desired. This explains why Tao's displayed `T_{ij}` formula is simpler than the fully general `\tilde B` definition without changing the locality conclusion.

### 2.4 Primary-source note

- [CHECKED] The repository did not contain the Tao paper text locally, and direct shell-network access failed with `URLError` on `arxiv.org`. The formulas above were fixed from AMS/JAMS primary-source snippets exposed through web search results, not from secondary summaries.

## 3. Harmonic far-field comparison

- [VERIFIED] Exploration 001 established that the surviving loophole is **not** Vasseur's literal harmonic term `P_{k1}`. It is the alternative idea that one may rewrite the dangerous pressure interaction using a near/far split

  ```text
  p = p_near + p_far,
  Δp_far = 0 on Q_k,
  ```

  with `p_far` carrying enough of the dangerous mass to beat the `P_{k21}` barrier.

### 3.1 Does a harmonic far-field piece still exist after averaging?

- [CHECKED] Yes, but only in a weak, generic sense. Once Tao's pressure satisfies

  ```text
  -Δp = div T(u,u),
  ```

  one may choose a spatial cutoff `χ` and define

  ```text
  p_near := -Δ^{-1} div(χ T(u,u)),
  p_far  := -Δ^{-1} div((1-χ) T(u,u)).
  ```

  On the region where `χ ≡ 1`, the source of `p_far` vanishes, hence `Δp_far = 0` there.
- [CHECKED] So formal harmonicity survives.

### 3.2 Why that does not save the loophole

- [CHECKED] The loophole needs more than post-Poisson harmonicity. It needs a split in which "far field" really means "generated by fluid outside the working cylinder or ball" so that the far piece can be estimated by harmonic tools while the dangerous local piece is correspondingly reduced.
- [CHECKED] In ordinary NS, this interpretation is available because the pressure source is the local tensor `u ⊗ u`; once one localizes `u_i u_j` in physical space, the corresponding far pressure really comes from exterior source support.
- [CHECKED] In Tao's averaged equation, `T(u,u)(x)` is already nonlocal in `u`: the order-zero multipliers `m_i(D)` have convolution kernels with long tails, so the value at `x` depends on velocity information from all over space before the pressure Poisson equation is even invoked.
- [CHECKED] Therefore a split of `div T(u,u)` into near and far source is **not** a split of the underlying fluid interaction into near and far regions. The averaged equation has already mixed those regions together at the level of the convection operator.
- [CHECKED] This is the specific ordinary-NS structure the loophole needs and Tao removes: the pressure source must be a local divergence/divergence of `u ⊗ u`, not a pseudodifferentially averaged bilinear expression.

### 3.3 Comparison table

| Setting | Pressure object | Harmonic on local cylinder? | Load-bearing bottleneck |
|---|---|---|---|
| Ordinary NS / Vasseur split | `-Δp = ∂i∂j(u_i u_j)` with `p = P_{k1} + P_{k2}` and bad local part `P_{k21}` | `P_{k1}` yes; `P_{k21}` no | [VERIFIED] Vasseur's bad non-divergence term involving `P_{k21}` at exponent `4/3 - 5/(3q)` |
| Alternative harmonic far-field loophole picture | `p = p_near + p_far`, with `Δp_far = 0` on `Q_k` and hoped-for mass transfer from the dangerous piece into `p_far` | yes by construction | [CHECKED] Whether the dangerous `P_{k21}`-type interaction can genuinely be recaptured by `p_far` and gain `U_k`-dependence |
| Tao averaged NS | `-Δp = div T(u,u)` with `T` an averaged pseudodifferential bilinear convection operator | [CHECKED] yes after an arbitrary source split of `div T`; but this no longer tracks distant fluid sources | [VERIFIED] The averaged nonlocal operator `T(u,u)` / `\tilde B(u,u)` itself; pressure harmonicity no longer isolates the dangerous interaction |

## 4. Bottleneck replacement analysis

- [VERIFIED] Exploration 001 isolated the ordinary-NS bottleneck as the slot

  ```text
  I_k ≤ ||P_{k21}||_{L^q} ||d_k||_{L^2} ||1_{v_k>0}||_{L^{2q/(q-2)}}.
  ```

- [CHECKED] Tao's construction shows that any argument using only the energy identity and generic harmonic-analysis estimates cannot distinguish the true NS bilinear form from `\tilde B`. Therefore a loophole that genuinely survives Tao must rely on a piece of structure absent from `\tilde B`.
- [CHECKED] The harmonic far-field loophole does rely on such a structure: it needs the source of the pressure to be generated by the local tensor `u ⊗ u`, so that one can talk about far-field source support in physical space before solving for pressure.
- [CHECKED] Tao's averaged system destroys exactly this locality. The pressure source is no longer `∂i∂j(u_i u_j)` but `div T(u,u)`, where `T(u,u)` already contains nonlocal order-zero multipliers applied to `u`.
- [CHECKED] Hence the old pressure bottleneck is not replaced by a better harmonic far-field term. It is replaced by a more basic obstacle: the decomposition no longer separates the physically local dangerous interaction from a genuinely exterior harmonic remainder.
- [CHECKED] In short:

  ```text
  ordinary NS loophole candidate:
    local tensor source --> Poisson solve --> harmonic far-field candidate

  Tao averaged NS:
    nonlocal averaged source already mixed --> Poisson solve --> harmonic remainder exists only formally
  ```

- [CHECKED] This makes the loophole Tao-incompatible for a falsification-first reason: if the mechanism depended only on post-Poisson harmonicity, Tao would not kill it; but the mechanism actually needs pre-Poisson locality of the source, and Tao removes that.

## 5. Verdict table

| Verdict | Status | Reason |
|---|---|---|
| `Tao-incompatible` | [VERIFIED] | Tao replaces the local pressure source `∂i∂j(u_i u_j)` by `div T(u,u)` with `T` a nonlocal averaged pseudodifferential bilinear operator. A harmonic far-field pressure split still exists formally, but it no longer corresponds to genuinely far fluid sources and thus cannot play the loophole's intended role. |

## 6. Recommended next move

- [CHECKED] Exploration 003 should not keep testing the loophole against Tao in the abstract. The decisive remaining computation is to model the locality failure explicitly.
- [CHECKED] Recommended task for exploration 003:

  1. Pick a concrete toy averaged operator by choosing one or two explicit order-zero multipliers, e.g. Riesz-transform or smooth annular-multiplier examples compatible with Tao's framework.
  2. For a compactly supported or sharply localized divergence-free velocity field `u`, compute or numerically sample both

     ```text
     ordinary source:  S_NS := ∂i∂j(u_i u_j),
     averaged source:  S_avg := div T(u,u).
     ```

  3. Quantify how much of `S_avg` is already present inside a local ball even when the physical velocity support that generates it lies outside that ball.
  4. Use that model to state the sharper claim:
     "the harmonic far-field loophole requires source locality of `u ⊗ u`, which fails for any nontrivial Tao-type averaging with order-zero multipliers."

- [CHECKED] If that computation succeeds, the mission should drop the Tao filter and return to ordinary NS-specific decompositions only.

## Running notes / dead ends

- [VERIFIED] Exploration 001 established that Vasseur's `beta = 4/3` bottleneck is the local non-divergence pressure piece `P_{k21}`, while the harmonic nonlocal piece `P_{k1}` is already favorable.
- [CHECKED] The local repository contained secondary summaries of Tao's result, but not the primary-source formulas in enough detail.
- [CHECKED] Direct shell-network retrieval of the arXiv source failed because the execution environment has no working DNS/network path. The AMS/JAMS primary-source snippets available through the web tool were sufficient to fix the needed formulas anyway.
