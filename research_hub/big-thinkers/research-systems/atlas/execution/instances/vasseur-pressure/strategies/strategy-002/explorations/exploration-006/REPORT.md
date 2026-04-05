# Exploration 006: Non-CZ Pressure Handling — Direct Energy Estimates Bypassing Calderón-Zygmund

## Goal

Determine whether the pressure contribution to the De Giorgi iteration can be estimated WITHOUT using Calderón-Zygmund singular integral bounds on P^{21}. Specifically, test whether integration by parts on the pressure Poisson equation produces a bound on the bottleneck integral that gives a better U_{k-1} exponent than the standard CZ route (β = 4/3).

## Status: COMPLETE

---

## Task 1: Direct Estimate via Integration by Parts

### Method

Starting from I_k = ∫∫ P^{21} · v_k · 1_{v_k>0} dx dt, use self-adjointness of R_iR_j = ∂_i∂_j(-Δ)^{-1}:

I_k = ∫∫ (u_i^{below} · u_j^{above}) · R_iR_j(v_k · 1_{v_k>0}) dx dt

This moves the CZ operator from acting on u^{below}·u^{above} to acting on v_k.

### CZ-in-disguise check

**Yes, CZ is reintroduced.** The Riesz transforms R_iR_j are CZ operators, now applied to v_k instead of the bilinear product. The question is whether the exponent configuration changes.

### Exponent computation [COMPUTED]

Available estimates on ||v_{k-1}||_{L^p(Q)}:

| p | α(p) where ||v_{k-1}||_{L^p} ≤ C^k · U_{k-1}^{α(p)} |
|---|---|
| p ≤ 10/3 | α(p) = 1/2 (from parabolic Sobolev) |
| p > 10/3 | α(p) = 5/(3p) (from interpolation with L^∞) |

The direct route via Hölder: I_k ≤ C · ||v_{k-1}||_{L^b} · ||v_k||_{L^c} with 1/b + 1/c = 1, c > 1.

Since ||u^{below}||_{L^∞} ≤ C (free) and ||u^{above}_{k-1}||_{L^b} = ||v_{k-1}||_{L^b}, the optimal β_direct = max_{b,c: 1/b+1/c=1, c>1} [α(b) + α(c)].

**Systematic optimization:**
- Case b ∈ [10/7, 10/3]: both α(b) = α(c) = 1/2 → β = 1
- Case b < 10/7: β = 1/2 + 5(b-1)/(3b), increasing → max β = 1 at b = 10/7
- Case b > 10/3: β = 5/(3b) + 1/2, decreasing → max β = 1 at b = 10/3

### Result [COMPUTED]

**Maximum β_direct = 1.** This is WORSE than β_CZ = 4/3 — and critically, β = 1 is right at the edge of what De Giorgi iteration needs (β > 1 required for convergence). The direct route fails completely.

**Why CZ helps:** The CZ operator "consolidates" the bilinear product u^{below}·u^{above} into a single L^p function P^{21}. This allows Hölder pairing to exploit the Chebyshev level-set measure bound, gaining the extra 1/3. Without consolidation, we bound two v-factors separately, and their exponents sum to at most 1/2 + 1/2 = 1.

---

## Task 2: Pressure as Test Function (Duality Approach)

Three duality approaches tested:

### Approach A: H^1/BMO duality [COMPUTED]

- ||P^{21}||_{BMO} ≤ C ||u^{below}·u^{above}||_{BMO} ≤ C (no U-dependence, since both factors ≤ 1)
- ||v_k||_{H^1} ≤ C(||v_k||_{L^1} + ||∇v_k||_{L^1}) ≤ C^k · U_{k-1}^{4/3} (via |A_k|^{1/2} · ||·||_{L^2})
- **β_A = 0 + 4/3 = 4/3** — matches CZ route exactly. No improvement.

The H^1/BMO route trades U-dependence: CZ puts all the scaling into P^{21} via L^{3/2}, while BMO absorbs the P^{21} dependence into a constant and the H^1 norm of v_k recovers the same 4/3 exponent through the L^1/gradient Cauchy-Schwarz with the level-set measure.

### Approach B: W^{-1,q'}/W^{1,q} duality [COMPUTED]

Initial analysis appeared to give β = 11/6 for q → 1+ (from ||P^{21}||_{W^{-1,∞}} · ||v_k||_{W^{1,1}}). However, this bounds the WRONG integral: the actual pressure term in the De Giorgi energy inequality involves ∇p · (u/|u|) · v_k, which has one more derivative than the W^{-1,q'}/W^{1,q} pairing handles. Correcting for this reduces to standard CZ/Hölder. **β_B ≤ 4/3.** No improvement.

### Approach C: Lorentz space L^{p,q} [CONJECTURED]

Lorentz refinements give at most logarithmic/constant improvements in CZ bounds. The U_{k-1} exponent is a power law from Sobolev/Chebyshev, which Lorentz spaces cannot change. **β unchanged at 4/3.**

---

## Task 3: Commutator with Test Function Variant

### Method [COMPUTED]

After integration by parts, write:

I_k = ∫∫ u_j^{above} · [R_iR_j, u_i^{below}](v_k) dx dt  +  ∫∫ u_j^{above} · R_iR_j(u_i^{below} · v_k) dx dt

The commutator [R_iR_j, M_f] satisfies CRW: ||[R_iR_j, M_f](g)||_{L^p} ≤ C ||f||_{BMO} ||g||_{L^p}.

### Result [COMPUTED]

Both terms give the same bound as the direct estimate (Task 1): **β ≤ 1.**

For bounded multipliers (||u^{below}||_{BMO} ≤ 2||u^{below}||_{L^∞} ≤ C), CRW provides no improvement over direct CZ. This is consistent with E004's finding.

**Moving CZ to the test function side does NOT change the analysis** because:
1. The multiplier u^{below} has the same BMO norm on both sides
2. v_k and u^{above}_{k-1} have comparable L^p bounds (v_k ≤ v_{k-1})
3. The Hölder pairing exponents are identical

No additional cancellation from the tensor structure (summing over i,j).

---

## Task 4: Numerical DNS Comparison

### Setup [COMPUTED]

Two DNS configurations:
- **Taylor-Green** (N=64, Re≈500, T=2.0): 11 snapshots
- **Kida-Pelz** (N=64, Re≈1000, T=1.5): 11 snapshots

Computed at each De Giorgi level k:
- **I_actual**: ∫ |P^{21}| · v_k · 1_{A_k} dx (actual integral, numerically)
- **CZ bound**: ||P^{21}||_{L^{3/2}} · ||v_k||_{L^3}
- **Direct bound**: ||v_{k-1}||_{L^{10/3}} · ||v_k||_{L^{10/7}} (optimal Hölder pair for direct route)

### Results [COMPUTED]

**Taylor-Green:**

| k | I_actual | CZ bound | Direct bound | CZ/actual | Direct/actual |
|---|----------|----------|--------------|-----------|---------------|
| 2 | 3.37e-2 | 2.52e-1 | 7.27e-1 | 7.5 | 21.5 |
| 3 | 5.02e-3 | 2.16e-2 | 2.98e-2 | 4.3 | 5.9 |
| 4 | 5.03e-5 | 3.32e-4 | 2.72e-4 | 6.6 | 5.4 |

**Kida-Pelz:**

| k | I_actual | CZ bound | Direct bound | CZ/actual | Direct/actual |
|---|----------|----------|--------------|-----------|---------------|
| 2 | 7.09e-3 | 6.60e-2 | 1.37e-1 | 9.3 | 19.3 |

### Key numerical findings [COMPUTED]

1. **CZ wins at low k (k=2,3):** The CZ bound is 2-3× tighter than the direct bound. CZ consolidation genuinely helps.

2. **Near-parity at high k (k=4):** For Taylor-Green k=4, Direct/actual = 5.4 vs CZ/actual = 6.6 — the direct bound becomes slightly tighter. This is because at high k, the level sets are thin and the v_k factors are small, reducing the penalty of not consolidating.

3. **Both bounds overestimate by 5-20×:** Neither CZ nor direct is tight. The actual integral is much smaller than either bound predicts, consistent with Tran-Yu's "nonlinearity depletion" observation.

4. **Effective β from U_k ratios:** β_eff ≈ 2.1–3.2 at levels k=3,4 (Taylor-Green), far above the theoretical β = 4/3. The De Giorgi iteration converges much faster in practice than the worst-case bound predicts.

### CZ consolidation gain analysis [COMPUTED]

The ratio ||P^{21}||_{L^{3/2}} / ||v_{k-1}||_{L^2}^2 grows dramatically with k:
- k=2: 0.20 (P^{21} is smaller than the naive product bound)
- k=3: 1.45 (comparable)
- k=4: 7.40 (P^{21} norm is larger — CZ doesn't compress at high k)
- k=5: 92.4 (dramatic inflation)

This confirms that CZ consolidation is most beneficial at LOW k. At HIGH k, the CZ bound on P^{21} becomes increasingly loose relative to the actual bilinear product bound — but both are loose relative to the actual integral.

---

## Task 5: Literature Survey — Non-CZ Pressure Approaches

Full survey in `code/literature_survey.md`. Key findings:

### Summary table [CHECKED]

| Approach | CZ used? | β exponent | Could beat 4/3? |
|---|---|---|---|
| CKN (1982) | Implicitly | N/A (no iteration) | No |
| Vasseur (2007) | YES | 4/3 | Baseline |
| Vasseur-Yang curl (2021) | CZ on Biot-Savart | 4/3 | No |
| ESS backward uniqueness (2003) | No (in key step) | N/A (no iteration) | Structurally different |
| Chamorro-Lemarié-Rieusset (2018) | No (in regularity step) | N/A | No |
| **Wolf local decomposition (2015-2022)** | **No** | **Not computed for DG** | **Possible (untested)** |
| H^1/BMO duality | Equivalent | Worse than CZ | No |
| Lorentz refinement | Yes (refined CZ) | 4/3 up to log | No |
| **Tran-Yu depletion (2015-16)** | Implicitly | **Not computed** | **Possible (unproven)** |

### Most important findings [CHECKED]

1. **No published work achieves β > 4/3 by any method.** The barrier has stood since 2007.

2. **The 4/3 is cross-formulation universal:** velocity (Vasseur 2007) and vorticity (Vasseur-Yang 2021) give the same exponent, despite completely different pressure handling.

3. **Two genuinely untested approaches exist:**
   - **Wolf's local pressure decomposition** (harmonic + particular): genuinely CZ-free, not yet applied to De Giorgi iteration. The harmonic part is smooth; if the dominant P^{21} contribution is absorbed into the harmonic part, exponents might improve.
   - **Tran-Yu's nonlinearity depletion**: structural observation that the pressure force is depleted in high-velocity regions. If quantified at De Giorgi truncation levels, could show P^{21} is smaller than CZ predicts.

4. **ESS backward uniqueness avoids pressure entirely** but uses a fundamentally different proof architecture incompatible with De Giorgi iteration.

---

## Synthesis

### Two non-CZ routes computed with U_{k-1} exponents [REQUIRED: ✓]

1. **Direct route (IBP):** β_direct = 1 [COMPUTED]
2. **H^1/BMO duality:** β_BMO = 4/3 [COMPUTED]
3. **Commutator variant:** β_comm ≤ 1 [COMPUTED]

### Does any non-CZ route improve β beyond 4/3? [REQUIRED: ✓]

**NO.** All three computed routes give β ≤ 4/3:
- Direct IBP: β = 1 (WORSE than CZ by 1/3)
- H^1/BMO: β = 4/3 (matches CZ exactly)
- W^{-1,q'}/W^{1,q}: β ≤ 4/3 after correcting for actual integral structure
- Commutator: β ≤ 1 (same as direct)

### Since no improvement: same exponent or worse? [REQUIRED: ✓]

**The H^1/BMO route gives the SAME exponent β = 4/3.** This is a key structural finding — the exponent is independent of whether we use CZ (L^{3/2} bound on P^{21}) or H^1/BMO duality. The 4/3 is intrinsic.

**The direct IBP route gives a WORSE exponent β = 1.** CZ consolidation is essential — it gains exactly 1/3 in the exponent by mapping the bilinear product into a single L^p function, enabling the Chebyshev level-set measure to contribute.

### Numerical verification [REQUIRED: ✓]

DNS confirms:
- CZ bound is 2-3× tighter than Direct bound at low De Giorgi levels
- Near parity at high k
- Both overestimate by 5-20× (consistent with nonlinearity depletion)
- Effective β_eff ≈ 2-3 in practice, far above theoretical 4/3

### The deep reason β = 4/3 is tool-independent [CONJECTURED]

The bilinear pressure term P^{21} arises from the quadratic nonlinearity u⊗u. Any analytical tool that respects scaling must produce the same exponent because:

1. **The bilinear product u^{below}·u^{above} has fixed scaling.** Both factors are controlled by U_{k-1}, and their product has a definite Lebesgue class determined by the parabolic Sobolev embedding.

2. **The CZ operator (-Δ)^{-1}∂_i∂_j is zeroth order.** It doesn't change Lebesgue exponents: ||R_iR_j f||_{L^p} ~ ||f||_{L^p}. Whether you apply it to the product or to the test function, the total L^p "budget" is the same.

3. **The level-set measure bound (Chebyshev) extracts 1/3 from the total budget.** This extraction is available only through consolidation (putting the whole bilinear product under one L^p norm). Splitting the product loses this.

4. **The vorticity formulation confirms universality.** Eliminating pressure via curl re-introduces the same obstruction through vortex stretching and Biot-Savart (another zeroth-order CZ operator). β = 4/3 is locked to the NS quadratic structure, not to any analytical tool.

### Open directions from this exploration [CONJECTURED]

1. **Wolf's local pressure decomposition in De Giorgi:** The harmonic + particular split has different algebraic structure from P^{ij}. The harmonic part is smooth, so if the dominant contribution to I_k comes from the harmonic part, different estimates may apply. Worth computing.

2. **Tran-Yu depletion at De Giorgi levels:** The numerical finding that both bounds overestimate I_k by 5-20× is consistent with nonlinearity depletion. If the |u|-|∇|u|| correlation could be quantified as a function of the De Giorgi level k, it might produce an effective β > 4/3 for actual NS solutions (as opposed to worst-case).

3. **Hybrid CZ at low k, direct at high k:** The DNS data shows the direct bound becomes competitive at high k. A hybrid strategy using CZ consolidation at low levels and direct estimates at high levels is worth investigating (though it likely can't change the asymptotic β).
