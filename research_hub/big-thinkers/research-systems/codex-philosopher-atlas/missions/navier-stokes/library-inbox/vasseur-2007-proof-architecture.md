# Exploration 003: Vasseur (2007) Proof Architecture — De Giorgi Iteration for Navier-Stokes Partial Regularity

## Goal

Analyze Alexis Vasseur's 2007 proof of partial regularity for Navier-Stokes equations using De Giorgi iteration. Extract five structural features and compare with CKN (1982).

**Paper:** Alexis Vasseur, "A new proof of partial regularity of solutions to Navier-Stokes equations," *NoDEA: Nonlinear Differential Equations and Applications*, 14(5-6):753-785, 2007. Preprint: web.ma.utexas.edu/users/vasseur/documents/preprints/NS2.pdf

**Sources consulted:** Vasseur 2007 preprint; Vasseur lecture notes (DGPekin.pdf); CKN Seminar Notes Ulm 2019 (Skipper); Seregin-Shilkin survey arXiv:1402.7181; Lee REU paper 2024 (De Giorgi for fluids).

---

## Section 1: Epsilon-Regularity Criterion

### Vasseur's Criterion — Theorem 1 (the Core Result)

Vasseur's Theorem 1 is the epsilon-regularity result, and it is stated differently from CKN. It reads:

> **Theorem 1.** For every p > 1, there exists a universal constant C*, such that any suitable weak solution (u, P) to (NSE) in [−1,1]×B(1) with no external force verifying
>
>   sup_{t ∈ [−1,1]} ∫_{B(1)} |u|² dx  +  ∫∫_{[−1,1]×B(1)} |∇u|² dx dt  +  (∫_{−1}^{1} (∫_{B(1)} |P| dx)^p dt)^{2/p}  ≤  C*
>
> satisfies ||u||_{L∞([−1/2,1]×B(1/2))} ≤ 1 (u is bounded, hence regular, on the inner half-cylinder).

**Key differences from CKN's criterion:**

1. **No pressure L^{3/2} norm.** The pressure P enters only via P ∈ L^p_t(L¹_x) for any p > 1. This is weaker than CKN's P ∈ L^{3/2} (in space-time) and weaker than L^p(L^{5/3}) used elsewhere. The L¹ spatial integrability is much weaker — only the time Sobolev regularity (p > 1) is needed.

2. **Fixed scale, not shrinking.** The domain [−1,1]×B(1) does not shrink as the proof proceeds. The De Giorgi cylinders Q_k converge to [−1/2,1]×B(1/2) from the outside. This is the fundamental structural departure from CKN, where the epsilon-regularity criterion is stated as a condition at every radius r → 0.

3. **Direct L∞ bound.** The conclusion is u ∈ L∞, not just u ∈ L^p for some high p. The De Giorgi iteration is specifically designed to produce L∞ bounds via level-set energy estimates.

### Recovery of the CKN Criterion — Theorem 2 and Proposition 5

The standard CKN epsilon-regularity criterion is recovered as Theorem 2 via parabolic rescaling (Proposition 5):

> **Theorem 2.** There exists δ* > 0 such that if (u, P) is a suitable weak solution near (x₀, t₀) and
>
>   limsup_{ε→0} (1/ε) ∫∫_{Q_ε(x₀,t₀)} |∇u|² dx dt  ≤  δ*
>
> then u is bounded (hence regular) near (x₀, t₀).

This is exactly the CKN ε-regularity criterion using E(u,r) = (r^{−1} ∫∫_{Q_r} |∇u|²)^{1/2}. The proof uses NS parabolic rescaling: u_λ(t,x) = λu(t₀+λ²t, x₀+λx), P_λ(t,x) = λ²P(t₀+λ²t, x₀+λx). Under this scaling:
- ||u_λ||_{L∞(L²)} + ||∇u_λ||_{L²} = λ^{−1}(||u||²+||∇u||² on Q_λ)^{1/2} → 0 as λ → 0, provided limsup_{r→0} r^{−1}∫∫_{Q_r}|∇u|² ≤ δ*
- ||P_λ||_{L^p(L¹)} scales as λ^{2-5/p}||P||_{L^p(L^1)} → 0 for any p > 1

So for small enough r, the conditions of Theorem 1 hold for u_λ, giving the regularity conclusion. Vasseur does not claim novelty in this step.

**Scaling analysis.** The CKN dimensionless quantities are:
- A(u,r) = (1/r) sup_{t} ∫_{B_r} |u|² dx — scaling exponent 0
- E(u,r) = (1/r) ∫∫_{Q_r} |∇u|² dx dt — scaling exponent 0
- C(u,r)³ = (1/r²) ∫∫_{Q_r} |u|³ dx dt — scaling exponent 0
- D(p,r)^{3/2} = (1/r²) ∫∫_{Q_r} |p|^{3/2} dx dt — scaling exponent 0

Each uses the parabolic measure dx dt ~ r⁵ (= r³ spatial × r² temporal). Vasseur's criterion, in scale-invariant form, is equivalent to requiring E(u,r) + (scaled pressure in L^p(L¹)) ≤ C* for some fixed r = 1.

---

## Section 2: Covering Argument

### How the Singular Set Bound Works

The covering argument in Vasseur is **identical to CKN's**. Vasseur explicitly states: "It is well known since [CKN] that, using classical covering lemmas, this result gives the partial regularity result." He does not claim any novelty in the covering step.

The argument proceeds:
1. Theorem 2 gives: if (x₀,t₀) is singular, then limsup_{r→0} E(u,r)² > δ*.
2. For each singular point, parabolic balls Q_{r_i}(x_i,t_i) with r^{−1}_i ∫∫_{Q_{r_i}} |∇u|² ≥ δ*/2.
3. By the Vitali covering lemma applied to the **parabolic metric** d((x,t),(y,s)) = max(|x-y|, |t-s|^{1/2}) (not the Euclidean metric), one extracts a disjoint subcollection.
4. Then: Σ r_i ≤ (2/δ*) Σ ∫∫_{Q_{r_i}} |∇u|² ≤ (2/δ*) ∫∫ |∇u|² < ∞.

Since the sum Σ r_i can be made arbitrarily small (via fine covers), H¹_{parabolic}(singular set) = 0.

### Why Parabolic Dimension Matters for the Bound

The key is that Σ r_i (not Σ r_i^α for some α > 1) is bounded. This gives zero **1-dimensional** parabolic Hausdorff measure, not zero higher-dimensional measure. The "1" comes from the fact that the energy inequality gives a bound on ∫∫|∇u|², which has parabolic homogeneity r^{5-2} = r³ (integrating |∇u|² ~ r^{-2} over a parabolic ball of radius r gives ~ r^3, not r). So the natural counting gives:

  r_i · (something ~ 1) ≤ r_i^{-1} ∫∫_{Q_{r_i}} |∇u|²

and summing: Σ r_i ≤ C ∫∫ |∇u|² < ∞.

In Euclidean space-time (R^3 × R), this parabolic 1-dimensional Hausdorff measure zero corresponds to Euclidean (1+2/2) = 2-dimensional Hausdorff measure zero, i.e., the singular set has **Hausdorff dimension at most 1** in parabolic metric, equivalently at most 5/3 in Euclidean space-time.

The covering argument is entirely at the level of Theorem 2 — the De Giorgi iteration (Theorem 1) is used only to establish Theorem 2, after which the CKN covering machinery runs unchanged.

---

## Section 3: Localization Mechanism — De Giorgi Iteration

**Vasseur's own assessment:** "All the novelty of this paper lies in the proof of Theorem 1."

### The Level Set Sequence

Vasseur defines a simultaneous **decreasing sequence of cylinders** and **increasing sequence of cut levels**:

- **Spatial balls:** B_k = B(½(1 + 2^{−3k}))  →  B(1/2) as k → ∞
- **Time intervals:** [T_k, 1] where T_k = ½(−1 − 2^{−k})  →  [−1/2, 1] as k → ∞
- **Parabolic cylinders:** Q_k = [T_k, 1] × B_k (shrinking toward the inner half-cylinder)
- **Levels:** C_k = 1 − 2^{−k}  →  1 as k → ∞
- **Level-set function:** v_k(t,x) = [|u(t,x)| − C_k]₊  (positive part of |u| above level C_k)

As k → ∞: the domain stabilizes to [−1/2,1]×B(1/2) and the level rises to 1. The iteration proves U_k → 0, which means eventually |u| ≤ 1 on the inner half-cylinder.

**Tracked quantity:**
  U_k = sup_{t ∈ [T_k,1]} ∫_{B_k} |v_k|² dx  +  ∫∫_{Q_k} d_k² dx dt

where d_k is a modified gradient defined as:
  d_k² = (1 − 2^{-k}) · 1_{|u| ≥ 1−2^{−k}} · |∇|u||²/|u|  +  (v_k/|u|)|∇u|²

The key property: d_k ≥ |∇v_k|, and d_k ~ |∇u| in the region where |u| is large.

Note: U₀ = ||u||²_{L∞(L²)} + ||∇u||²_{L²} — this is just the global kinetic energy, with **no pressure term**. Pressure enters only as an additive correction in Proposition 3.

### The Key De Giorgi Lemma

**Lemma 4** (standard De Giorgi iteration lemma): For C > 1 and β > 1, there exists C₀* such that if W₀ ≤ C₀* and for every k ≥ 1:

  W_k ≤ C^k · W_{k-1}^β

then lim_{k→∞} W_k = 0.

The proof is elementary: if W₀ < C₀* = C^{−1/(β−1)} then induction gives W_k ≤ C^{−k/(β−1)} → 0. The crucial feature is **superlinearity** (β > 1), not any particular value of β.

### Proposition 3 — The Main Recursive Estimate

**Proposition 3.** For any p > 1, there exist constants C_p and β_p > 1 such that for any suitable weak solution (u,P) in [−1,1]×B(1) with U₀ ≤ 1:

  U_k ≤ C_p^k · (1 + ||P||_{L^p(L¹)}) · U_{k-1}^{β_p}

Proposition 3 + Lemma 4 → Theorem 1: if U₀ ≤ min(1, C₀*/(1+||P||_{L^p(L¹)})), the recursion converges to 0.

The superlinearity β_p > 1 holds for **all p > 1**. Moreover:
- For p > 10: β_p > 3/2 (all terms exceed the natural scaling; see Section 4)
- For p ≤ 10: β_p ∈ (1, 4/3) (the "bad" local pressure term limits β)

### Local Energy Inequality for Level Sets — Lemma 11

**Lemma 11** (the core localization). Multiplying the NS equation by u·v_k/|u| and combining with the global energy inequality for |u|²/2, Vasseur derives a local energy inequality for v_k²/2:

  ∂_t(v_k²/2) + div(u·v_k²/2) + d_k² − Δ(v_k²/2) + div(u·P) + ((v_k/|u|) − 1)·u·∇P ≤ 0

This is an *inequality* (not equality), analogous to the local energy inequality for the full solution, but restricted to the level-set region {|u| > C_k}. The last two terms are the **pressure localization terms** — Vasseur must control div(uP) and the remaining pressure term.

### Integration Against Cutoff and Master Inequality (Equation 13)

Integrating Lemma 11 against a spatial cutoff η_k (= 1 on B_k, = 0 off B_{k−1/3}, |∇η_k| ≤ C·2^{3k}, |Δη_k| ≤ C·2^{6k}) and averaging over initial times σ ∈ [T_{k−1}, T_k]:

  U_k ≤ C·2^{6k} ∫∫_{Q_{k−1}} |v_k|² dx dt
      + C·2^{3k} ∫∫_{Q_{k−1}} |v_k|³ dx dt
      + |pressure terms|

The factors 2^{6k} and 2^{3k} arise from Δη_k and ∇η_k respectively — these are the "cutoff localization costs."

### Pressure Localization — How Vasseur Avoids the CKN Difficulty

**CKN's pressure difficulty.** In CKN, the pressure P satisfies −ΔP = ∂_i∂_j(u_iu_j) globally. Localizing this to a parabolic cylinder Q_r requires Riesz transform estimates, generating error terms of the form ∫|u|² (on larger balls). This introduces a nonlocal term that is hard to control at each scale and requires P ∈ L^{3/2}(Q_r) explicitly.

**Vasseur's decomposition.** Since the Q_k domains do NOT shrink to 0 (they converge to a fixed inner domain), Vasseur can decompose the pressure using the Newtonian potential with cutoff φ_k supported in B_{k−1}:

  P = P_k^1  +  P_k^2   on [T_{k−1},1]×B_{k−2/3}

where:
- **P_k^1 is harmonic:** −ΔP_k^1 = 0 in [T_{k−1},1]×B_{k−2/3}. This is the "non-local" part carrying global pressure information. It is controlled by Lemma 7 using the *global* ||P||_{L^p(L¹)} norm:

    ||P_k^1||_{L^p(T_{k−1},1; L∞(B_{k−1/3}))} ≤ C·2^{12k}·(||P||_{L^p(L¹)} + ||u||²_{L∞(L²)})

  This works because the harmonic function P_k^1 is controlled by boundary values, which are bounded using the L¹ spatial norm of the full P.

- **P_k^2 is local:** −ΔP_k^2 = ∂_i∂_j[φ_k u_i u_j] on R³. This depends only on u inside B_{k−1}. The local pressure is further decomposed into three pieces P_k^{21}, P_k^{22}, P_k^{23} based on splitting u = u·(1 − v_k/|u|) + u·v_k/|u|, where the first factor is bounded by 1 (since |u|·(1−v_k/|u|) ≤ C_k ≤ 1) and the second depends on the level-set energy.

**Why this works at fixed scale but not at shrinking scale:** The key insight is that ||P||_{L^p(L¹)} is a *single global number* that doesn't scale with k. In CKN, you would need ||P||_{L^{3/2}(Q_{r_k})} at each level r_k → 0, which requires the full pressure integrability. Here, the single global norm suffices because Q_k → Q_∞ ≠ 0.

### The Obstruction: Local Pressure Term P_k^{21}

The P_k^{21} piece (harmonic component estimated via the bounded part of u) produces the estimate (Step 5, eq. (20)):

  |P_k^{21} terms| ≤ C_q·2^{kα_q}·U_{k-1}^{4/3 − 5/(3q)}

The minimum over q of 4/3 − 5/(3q) as q → ∞ approaches **4/3**. This is the fundamental obstruction:
- The exponent 4/3 > 1, so β_p > 1 still holds: partial regularity follows.
- But 4/3 < 3/2, so Vaseur **cannot** achieve β_p > 3/2 for all p.

Vasseur writes explicitly: "the only bad terms (with exponent smaller than 3/2) comes from the local pressure term which cannot be written in a divergence form."

### Comparison with CKN/Lin Localization

| Feature | CKN (1982) | Lin (1998) | Vasseur (2007) |
|---|---|---|---|
| Localization method | Explicit cutoff η_r, generates error terms via Riesz | Compactness/contradiction: no explicit ε formula | Fixed-scale De Giorgi iteration: level sets on Q_k → Q_∞ |
| Pressure localization | Must bound P at each scale r, requires P ∈ L^{3/2}(Q_r) | Compactness absorbs pressure implicitly | P_k = P_k^1 (harmonic) + P_k^2 (local); controlled by global ||P||_{L^p(L¹)} |
| Nonlocal terms | Yes: Riesz transform of localized pressure | Yes: implicit in compactness (info lost) | Yes: P_k^1 harmonic, controlled by global norm |
| Main lossiness source | Cutoff ∇η terms + pressure L^{3/2} → 3/2 scaling | Same (but obscured by contradiction) | P_k^{21} local pressure → exponent 4/3 |
| Does it change the bottleneck? | No | No | No (still 4/3 < 3/2; only partial regularity) |

---

## Section 4: Critical Scaling Exponents

### Parabolic Sobolev Embedding — Lemma 6

The core interpolation tool is Lemma 6, the parabolic Sobolev embedding:

  ||F||_{L^{10/3}(Q_k)} ≤ C·||F||_{L∞(L²)}^{2/5} · (||F||_{L∞(L²)} + ||∇F||_{L²})^{3/5}

This follows from: (i) spatial Sobolev in R³: H¹(B_k) ↪ L⁶(B_k), giving ||F||_{L²(L⁶)} ≲ ||F||_{L∞(L²)}^{1/2}·||∇F||_{L²}^{1/2}; (ii) time Hölder interpolation L∞(L²) × L²(L⁶) → L^{10/3}(Q_k) (since 2/5 + 3/5 = 1 and 1/(10/3) = 2/5·(1/2)^{... } works by Hölder in time).

The exponent **10/3** is the **parabolic critical Sobolev exponent** for L²-energy data in R³×R:
- Spatial dimension d = 3, time dimension 1 (but parabolic weight 2), so parabolic dimension n = d + 2 = 5
- Critical Sobolev exponent for W^{1,0}_2(R^n) → L^q: q = 2n/(n−2) with n = 5 gives q = 10/3
- This is exactly where L² energy → L^{10/3} via the parabolic Sobolev inequality

**The parabolic dimension 5 directly produces the exponent 10/3, which is central to the De Giorgi superlinearity.**

### Level Set Measure — Lemma 12 (The De Giorgi Mechanism)

**Lemma 12.** For q > 1 and k > 1:

  ||1_{{v_k>0}}||_{L^q(Q_{k−1})} ≤ C·2^{10k/(3q)}·U_{k−1}^{5/(3q)}

Proof sketch: v_k > 0 implies v_{k−1} ≥ 2^{−k} (since consecutive levels differ by 2^{−k}). By Chebyshev:

  |{v_{k−1} > 2^{−k}} ∩ Q_{k−1}| ≤ 2^{10k/3} · ||v_{k−1}||^{10/3}_{L^{10/3}(Q_{k−1})} ≤ C·2^{10k/3}·U_{k−1}^{5/3}

The exponent **5/3 in U_{k−1}^{5/3}** is superlinear (> 1), so this contributes to β > 1 in the recursion.

### Bounding Transport Terms — Equation (14)

Using Lemma 12 with Hölder:
  ∫∫ |v_k|² dx dt ≤ ||v_k||²_{L^{10/3}} · ||1_{{v_k>0}}||_{L^{5/3}}
  ∫∫ |v_k|³ dx dt ≤ ||v_k||³_{L^{10/3}} · ||1_{{v_k>0}}||_{L^{5/2}}

Combining with 2^{6k} and 2^{3k} factors from the master inequality:

  C·2^{6k}∫∫|v_k|² dx dt + C·2^{3k}∫∫|v_k|³ dx dt ≤ C·2^{6k+4k/3}·U_{k−1}^{5/3}

The exponent **5/3 > 3/2** — Vasseur's comment: "We have succeeded to overtake the scale of the equation." The natural scaling of NS corresponds to exponent exactly 3/2 (from Sobolev embedding of |u|³). The De Giorgi mechanism gives 5/3 for these transport terms, which is better than the NS critical scaling.

### The Critical Exponent Structure

| Term | Exponent in U_{k−1}^β | Source |
|---|---|---|
| ∫∫|v_k|² and ∫∫|v_k|³ (transport) | β = 5/3 | Parabolic Sobolev (L^{10/3}) + Chebyshev |
| Local pressure P_k^{22}, P_k^{23} (large-|u| part) | β = 5/3 | Same mechanism via CZ/Riesz on level sets |
| Local pressure P_k^{21} (bounded-|u| part) | β → 4/3 (as q → ∞) | Calderón-Zygmund on bounded×v_k terms |
| Non-local pressure P_k^1 (harmonic part) | β > 1 (any p > 1) | Mean value inequality for harmonic functions |

**Minimum exponent = 4/3 > 1.** Partial regularity follows (β_p > 1 for all p > 1).
**Maximum exponent = 5/3 < 2.** No "full regularity from a single term" possible.

### Comparison with CKN Scaling Exponents

In CKN and Lin's reformulation, the key estimate has the form (using scale-invariant quantities Φ(r) ~ r^{−1}∫∫_{Q_r}|∇u|²):

  Φ(r) ≤ C(r/R)²Φ(R) + C·Φ(R)^{3/2}

The **3/2 exponent** comes from: ||u||³_{L³(Q_r)} ≲ ||∇u||³_{L²} (by Sobolev in R³+time) ∼ Φ(r)^{3/2}. This is the **natural NS scaling exponent** — exactly critical.

Vasseur's transport terms give **5/3 > 3/2** (better than CKN), but the local pressure term gives **4/3 < 3/2** (worse, in the sense of being farther from full regularity). So:
- **Where De Giorgi is better:** transport/nonlinear terms (5/3 vs 3/2)
- **Where De Giorgi hits a new wall:** local pressure (4/3 — a new obstruction not visible in CKN)
- **Net:** β_p > 1 is achievable but β_p ≥ 3/2 is not, so only partial regularity is proved

### Vasseur's Appendix: The Full Regularity Gap

Vasseur shows (Appendix, Conjecture 14): **if** Proposition 3 held with β_p > 3/2, then ALL suitable weak solutions would be globally bounded (full regularity). The proof rescales u_ε(t,x) = ελu(t₀+λ²t, x₀+λx); the rescaled initial energy U_{ε,0} ~ ε^{2−5/λ}·(global energy)·λ → 0 as λ → 0 when 2β − 3 > 0 ↔ β > 3/2. So the threshold β = 3/2 is **precisely the boundary between partial and full regularity** in the De Giorgi framework. The current proof achieves β = 4/3 (limited by local pressure), which falls short.

---

## Section 5: Free-Parameter vs. Fixed-Constant Estimates

### Where Lossiness Enters

**No ε-absorption in the main iteration.** Unlike CKN (which uses Young's inequality with free ε to absorb gradient error terms from cutoffs), Vasseur's De Giorgi iteration uses **no free parameters in the core Proposition 3**. Every estimate is done with fixed universal constants. The only source of lossiness is:

1. **The 2^{Ck} geometric growth** in the cutoff cost (|∇η_k| ~ 2^{3k}, |Δη_k| ~ 2^{6k}). These enter as the C^k factor in Proposition 3. This is absorbed into the De Giorgi lemma: even with C^k growth, convergence follows if β > 1.

2. **The exponent 4/3 from P_k^{21}** (see above). This is a fundamental loss — the pressure cannot be written in divergence form, so the Riesz transform estimate loses a factor. No ε-absorption can recover this. It is a **hard structural bound**, not a proof-technique artifact.

3. **One free parameter choice in Proposition 5.** When deriving Theorem 2 from Theorem 1 via rescaling, Vasseur must choose λ small enough so that C(λ² + λ^{6−4/p}) < 1/8. This is a one-time constant choice, not a per-step Young ε.

### Comparison with CKN's ε-Absorption

CKN's localization generates cutoff error terms like:

  ∫ |u|²|∇η|² ≤ ε∫|∇u|²η² + ε^{−1}∫|u|²|∇η|⁴/η²

where ε is freely chosen to make the first term small and absorbed into the left side. This is classic ε-absorption. It introduces no fundamental loss (ε is eventually chosen optimally), but it creates explicit "interaction terms" that must be controlled by the pressure estimate.

**Vasseur avoids this ε-absorption entirely** for the level-set energy estimates, replacing it with the De Giorgi mechanism (Lemma 12 + superlinear recursion). However, the pressure localization still requires Calderón-Zygmund estimates with **fixed L^q constants** (not optimal, but existential), which is where the 4/3 exponent arises.

### Sobolev Inequalities: Optimal vs. Existential

Vasseur uses:
- **Spatial Sobolev H¹(B_k) ↪ L⁶(B_k):** Standard embedding with constant independent of k (since B(1/2) ⊂ B_k ⊂ B(1)). Not optimal constant, but the same Sobolev exponent (6 in 3D) as CKN.
- **Calderón-Zygmund (Riesz transform) in L^q:** Used for pressure decomposition (Lemma 13). Standard L^q boundedness for 1 < q < ∞. Not sharp constants.
- **Mean value inequality for harmonic functions (Lemma 7):** Used for P_k^1 control. Classical, sharp up to constants.

The **same Sobolev exponent** (L^6 in 3D, L^{10/3} in parabolic space-time) appears in both CKN and Vasseur, because both rely on the same 5-dimensional parabolic geometry. The critical exponent 10/3 (= 2·5/3) is universal to the parabolic Navier-Stokes system in R³×R and is not specific to either proof method.

### Does De Giorgi Produce Tighter Estimates?

| Estimate type | CKN | Vasseur |
|---|---|---|
| Velocity nonlinear term | 3/2 (Sobolev L³→L^{3/2}) | 5/3 (De Giorgi level sets; tighter) |
| Pressure local term | 3/2 (L^{3/2} pressure directly) | 4/3 (harmonic/CZ; *looser* than CKN for this term) |
| Pressure condition | P ∈ L^{3/2}(Q_r) | P ∈ L^p(L¹), any p>1 (weaker assumption) |
| ε-absorption | Yes (explicit per-step) | No (De Giorgi mechanism) |
| Free parameters | Many (one per scale level in iteration) | One (the scaling parameter λ in Prop 5) |

**Conclusion:** De Giorgi produces tighter estimates for the velocity/transport terms (5/3 vs 3/2), but the pressure localization in Vasseur's approach produces a new obstruction at exponent 4/3. The proof is less lossy on the nonlinear terms but encounters a new pressure bottleneck. Both proofs reach the same conclusion (partial regularity, H¹(S) = 0) but via different "weakest links."

---

## Synthesis: CKN vs. Vasseur — Does De Giorgi Offer a Different Path?

### What De Giorgi Changes

1. **Mechanism of regularity propagation:** CKN/Lin iterate on a scale-invariant quantity Φ(r) at shrinking scales. Vasseur iterates on level-set energies U_k at a fixed scale, with shrinking levels. These are genuinely different mathematical objects.

2. **Pressure condition:** Vasseur requires only P ∈ L^p(L¹) (any p > 1), weaker than CKN's L^{3/2} condition. This is an actual improvement in the assumptions.

3. **Velocity nonlinear term:** Vasseur achieves exponent 5/3 > 3/2, which is better than CKN's critical 3/2 exponent. The De Giorgi level-set mechanism "beats" the natural NS scaling for the velocity term.

4. **No ε-absorption:** Vasseur's proof is cleaner in structure, with convergence guaranteed by Lemma 4 (superlinear recursion) rather than explicit smallness conditions at each scale.

### What De Giorgi Preserves (Same Bottleneck)

1. **The singular set bound is identical:** H¹_parabolic(S) = 0, proved by exactly the same Vitali covering argument applied to the same ε-regularity criterion.

2. **The critical Sobolev exponent 10/3 is the same:** Both proofs ultimately use the parabolic Sobolev embedding W^{1,0}_2 → L^{10/3} in 5-dimensional parabolic space-time. This is a universal property of the NS system, not a proof artifact.

3. **The dimension bound ≤ 1 arises through the same route:** Global energy bound ∫∫|∇u|² < ∞ → Vitali cover → Σ r_i ≤ C||∇u||²_{L²} → H¹(S) = 0. The De Giorgi iteration is used to establish the epsilon-regularity criterion; once established, the covering argument is identical to CKN.

4. **Full regularity is not achieved:** Both proofs face an exponent barrier. In CKN, it is the natural NS scaling (3/2 exponent for the nonlinear term). In Vasseur, the barrier is at exponent 4/3 from the local pressure term — actually a *harder* obstruction (lower exponent), though still > 1.

### The Key Negative Finding

Vasseur's proof does NOT offer a new route around the dimension ≤ 1 bottleneck. The De Giorgi mechanism achieves superlinear feedback (β > 1) via a different algebraic route, but the covering argument reduces to the same inequality Σ r_i ≤ C∫|∇u|² that CKN uses. The dimension bound is not a consequence of the particular proof technique; it is a consequence of the global energy bound and the ε-regularity structure — which are shared by all three proofs.

**What Vasseur's proof does offer** is a structural identification of the obstruction to full regularity: the local pressure term P_k^{21} gives exponent 4/3, and Vasseur proves (Appendix) that β > 3/2 would imply full regularity. So Vasseur's framework converts the question "can we prove full regularity?" into "can we control the local pressure term with exponent > 3/2?" — a more precise formulation than CKN provides.

---

## What Could Not Be Resolved

1. **Exact form of P_k^{22}, P_k^{23} decomposition:** The three-way split of the local pressure is described in general terms by Vasseur; extracting the exact exponents (5/3 for P_k^{22,23}) requires working through Lemmas 9-10 in detail, which are only summarized here.

2. **The p > 10 threshold for β_p > 3/2:** Vasseur states this exists but the exact calculation of the crossover value p = 10 requires tracing through the Calderón-Zygmund constants in Lemma 13. This is reported as a stated result.

3. **Whether any subsequent work has improved the exponent 4/3 for the local pressure:** A search of post-2007 literature found Caffarelli-Vasseur (2010, SQG equation, different PDE) and Tran-Yu (2014, Galilean invariance argument) but did not fully verify whether Tran-Yu's approach achieves β > 3/2 for NS itself.
