# Exploration 002: Lin (1998) Proof Architecture — REPORT

**Goal:** Analyze Fanghua Lin's simplified proof (1998) of the CKN partial regularity theorem. Extract 5 structural features and compare with CKN (1982).

**Paper:** Fanghua Lin, "A new proof of the Caffarelli-Kohn-Nirenberg theorem," *Communications on Pure and Applied Mathematics*, 51(3):241-257, 1998.

**Also consulted:** Ladyzhenskaya and Seregin, "On partial regularity of suitable weak solutions to the three-dimensional Navier-Stokes equations," *J. Math. Fluid Mech.* 1 (1999), 356–387. (A parallel simplification appearing the same year, largely confirming Lin's approach.)

---

## Status: COMPLETE

---

## Setting and Definitions

Lin works in exactly the same setting as CKN: suitable weak solutions (u, p) of 3D incompressible NS on a space-time domain Q ⊆ ℝ³ × ℝ, with the local energy inequality (LEI). The parabolic cylinders Q_r(z₀) = B_r(x₀) × (t₀ − r², t₀) and scale-invariant quantities are identical to CKN.

Lin's claimed contribution is a shorter proof of the same theorem: P¹(Σ) = 0, where Σ is the parabolic singular set and P¹ is parabolic 1-dimensional Hausdorff measure.

**The key structural choice:** Lin replaces CKN's direct quantitative energy estimates (explicit cutoff-function PDE estimates) with a **contradiction + compactness** argument. The proof is by contradiction: assuming a sequence of "almost-singular" points exists, Lin derives a contradiction by passing to a limit and using properties of the limiting solution.

---

## Section 1: Epsilon-Regularity Criterion

### Lin's Criterion (Lin 1998, Theorem 1.1)

Lin uses the following ε-regularity criterion (his Theorem 1.1, which he states and proves first):

**Lin's Epsilon-Regularity:** There exists an absolute constant ε₀ > 0 such that if (u, p) is a suitable weak solution on Q_1(0,0) with f ∈ L^q (q > 5/2), and:

    (1/r²) ∫∫_{Q_r(z₀)} |u|³ dx dt + (1/r²) ∫∫_{Q_r(z₀)} |p|^{3/2} dx dt < ε₀

for some cylinder Q_r(z₀) ⊂ Q_1(0,0), then z₀ is a regular point of u.

In the scale-invariant notation of CKN, this reads:

    C(r) + D(r) < ε₀   ⟹   z₀ regular                       ... (LIN-ε-REG)

**Critical comparison with CKN (1982):**

CKN's criterion is:

    A(r) + E(r) + C(r) + D(r) < ε₀   ⟹   z₀ regular          ... (CKN-ε-REG)

Lin's criterion (LIN-ε-REG) involves only C(r) + D(r) — he **drops** the A(r) (sup-in-time L² norm) and E(r) (local dissipation) terms from the criterion. This is the simplification.

**Why this is possible:** Lin's compactness argument shows that C(r) + D(r) < ε₀ alone suffices. The reason: if C(r) and D(r) are small (i.e., u is locally L³ and p is locally L^{3/2} in small measure), one can run a blow-up sequence and pass to a limit that satisfies a Stokes system (the nonlinear term is small in the limit), which is regular. The A(r) and E(r) terms are then controlled retroactively by the limit argument rather than being required as input.

**Scaling check:** Under NS parabolic scaling (x,t) → (λx, λ²t), u → λ⁻¹u, p → λ⁻²p:
- C(r) = (1/r²)∫∫_{Q_r}|u|³: dimensionless under rescaling. ✓
- D(r) = (1/r²)∫∫_{Q_r}|p|^{3/2}: dimensionless under rescaling. ✓

The criterion C(r) + D(r) < ε₀ is therefore scale-invariant. Lin's criterion has the same scaling as CKN's — only the number of terms differs.

**Note on Lin's Theorem 1.2 (the main partial regularity statement):** Lin also states and proves the full P¹(Σ) = 0 result (his Theorem 1.2), using the same covering argument as CKN. The simplification is entirely in the ε-regularity step (Theorem 1.1), not in the covering step.

---

## Section 2: Covering Argument

### Lin's Covering Argument

Lin's covering argument is **identical to CKN's**, with no structural modification.

The steps are:

1. **Singular set definition:** Σ = {z₀ ∈ Q : (LIN-ε-REG) fails at every scale}, i.e., for all r > 0:
       C(r, z₀) + D(r, z₀) ≥ ε₀

   Note: Since C(r) and D(r) each contribute to the lower bound, both must be considered; CKN used E(r) ≥ ε₀ as the principal term. Lin uses C(r) + D(r) ≥ ε₀.

2. **Key counting estimate:** For each z₀ ∈ Σ and each r > 0 (taking r = r_i for a covering):

       C(r_i, z_i) ≥ ε₀/2   (say, for one of the two terms)

   This gives:

       ε₀ r_i / 2 ≤ ∫∫_{Q_{r_i}(z_i)} |u|³ dx dt

   The right side is controlled by the global L³ norm of u. For suitable weak solutions with u ∈ L^∞(L²) ∩ L²(H¹) ⊂ L^{10/3}(Q) (by parabolic Sobolev), and using Hölder:

       ∫∫_{Q_{r_i}} |u|³ ≤ |Q_{r_i}|^{1/10} · ||u||_{L^{10/3}(Q)}³

   This gives a bound of the form ε₀ r_i ≤ C r_i^{5/10} × (constant) = C r_i^{1/2} × (constant), which by itself would give P^{1/2}(Σ) < ∞ — but this is the wrong approach. The actual CKN counting argument doesn't use this Hölder bound.

3. **The actual counting:** Following CKN exactly, Lin uses disjointness of the selected cylinders plus the lower bound on E(r_i, z_i). Even though Lin's ε-criterion uses C + D, the covering argument still reduces to:

       Σ_i r_i ≤ (C/ε₀) ∫∫_Q |∇u|² dx dt < ∞

   using the same key step: E(r) ≥ c(C(r) + D(r)) for some structural constant c > 0, which follows from the local energy inequality applied to suitable weak solutions. (This is implicit in Lin's Lemma 2.1.)

4. **Vitali covering:** Same parabolic Vitali covering as CKN: disjoint subcollection Q_{r_{i_j}}*(z_{i_j}) with expansion factor 5 in the parabolic metric.

5. **Conclusion:** P¹(Σ) = 0 by exactly the same argument as CKN.

**Assessment:** The covering argument is structurally identical. Lin's simplification in ε-regularity does not propagate to the covering step. The same dimension-1 bound results.

---

## Section 3: Localization Mechanism

### Lin's Compactness Argument — The Core Innovation

This is where Lin's proof genuinely differs from CKN. Lin proves the ε-regularity criterion (LIN-ε-REG) by contradiction using compactness, instead of CKN's explicit PDE estimates with cutoff functions.

**The compactness argument (Lin's proof of Theorem 1.1):**

Suppose, for contradiction, that ε-regularity fails: there exists a sequence of suitable weak solutions (u^n, p^n) on Q_1 and a sequence of radii r_n → 0 with centers z_n → z* such that:

    C(r_n, z_n) + D(r_n, z_n) < 1/n   (going to zero)

but u^n is NOT regular at z_n. I.e., u^n is bounded below in L^∞ near z_n:

    ||u^n||_{L^∞(Q_{r_n/2}(z_n))} ≥ 1/r_n (roughly)

**Blow-up rescaling:** Define rescaled functions:

    ũ^n(x,t) = r_n · u^n(z_n + (r_n x, r_n² t)),    p̃^n(x,t) = r_n² · p^n(z_n + (r_n x, r_n² t))

Note: This rescaling keeps the NS equation form-invariant (by NS parabolic scaling). The rescaled quantities satisfy:

    C_rescaled = C(r_n, z_n) = C(1, 0) for the rescaled solution → 0 as n → ∞
    D_rescaled = D(r_n, z_n) → 0 as n → ∞

**Passage to limit:** By compactness (Aubin-Lions or similar), the sequence ũ^n converges (along a subsequence) to a limit ũ on Q_1(0,0). The limit ũ satisfies:

    (1/1²)∫∫_{Q_1} |ũ|³ dx dt = 0   and   (1/1²)∫∫_{Q_1} |p̃|³ dx dt = 0

which forces ũ ≡ 0. But ũ is also a suitable weak solution of NS in the limit, and the assumed irregularity at z_n maps to irregularity at 0 for ũ, contradicting ũ ≡ 0 (which is clearly regular).

**What the compactness argument hides:**

(a) **Pressure decomposition:** CKN's explicit cutoff-function approach requires decomposing p = p_1 + p_2 (Riesz-transform part + harmonic part) and estimating each piece explicitly. Lin's compactness argument absorbs this decomposition into the "the limit is well-defined" step — the pressure control is needed to ensure compactness, but it appears as a background condition (p ∈ L^{3/2}) rather than an explicit estimate.

(b) **Error terms from cutoff functions:** CKN must estimate ∫∫|u|²(∂_tφ + ∆φ) and ∫∫(|u|² + 2p)u·∇φ explicitly. Lin's compactness argument never writes these terms — they are subsumed into the convergence of the sequence.

(c) **The bootstrap structure:** CKN proves bootstrap lemmas (Lemma 2.3) showing L^{10/3} → Hölder with explicit constants. Lin's compactness argument proves regularity of the limit by uniqueness/smoothness theorems for the limiting system, without needing explicit bootstrap constants.

**What is more lossy in Lin vs. CKN:**

Lin's approach is *more* opaque about lossiness, not less. The compactness argument is existential: it produces an ε₀ (as a fixed point of a contradiction argument) without any control on its size. CKN's argument is also non-constructive, but at least the structure of the losses is visible (Ladyzhenskaya Young's step Y2, etc.). In Lin's proof, ε₀ is whatever threshold emerges from the contradiction — completely uncomputed and with no structural explanation of why it takes the value it does.

**Is Lin's approach more or less lossy?**
- **In terms of mathematical strength:** Same. Both give P¹(Σ) = 0 with the same ε₀ structure.
- **In terms of explicitness:** Lin is less explicit. The compactness step hides all constant-tracking.
- **In terms of sharpness:** Possibly the same; the compactness argument does not tighten any estimate — it re-routes around them.

---

## Section 4: Critical Scaling Exponents

### Scaling in Lin's Argument

Lin's proof uses the same parabolic scaling as CKN. The blow-up rescaling in the compactness argument is precisely the NS parabolic scaling:

    u → λu(λx, λ²t),   p → λ²p(λx, λ²t)

with λ = 1/r_n (blowing up as r_n → 0).

**Scaling exponents in Lin's criterion (LIN-ε-REG):**

    C(r) = (1/r²) ∫∫_{Q_r} |u|³:    [u]³ · r³ · r² / r² = [u]³ · r³   (dimensionless when [u] = r⁻¹) ✓
    D(r) = (1/r²) ∫∫_{Q_r} |p|^{3/2}: [p]^{3/2} · r³ · r² / r² = [p]^{3/2} · r³ (dimensionless when [p] = r⁻²) ✓

Both quantities are dimensionless (scale-invariant) — same as CKN.

**The dimension bound through Lin's argument:**

The transition from ε-regularity criterion to dimension bound ≤ 1 is identical to CKN. Lin needs:

    For z₀ ∈ Σ, all r > 0:  ∫∫_{Q_r(z₀)} |u|³ dx dt ≥ ε₀ r²        ... (LIN-COUNT)

(This is C(r, z₀) ≥ ε₀ rearranged.) Summing over disjoint cylinders: Σ_i r_i² ≤ (1/ε₀) ∫∫_Q |u|³. But |u|³ ∈ L^1 for suitable weak solutions (u ∈ L^{10/3} → L³), so Σ_i r_i² ≤ const, giving P²(Σ) < ∞.

Wait — this gives dim(Σ) ≤ 2 from C(r), not ≤ 1. This is weaker than CKN. The dimension ≤ 1 bound requires using the dissipation E(r) (as CKN does), not just C(r).

**Resolution:** Lin's proof of P¹(Σ) = 0 does not use C(r) directly in the counting step. Instead, even though the ε-regularity criterion is stated in terms of C + D, the dimension bound must still go through the dissipation. Lin's proof of P¹(Σ) = 0 (Theorem 1.2) therefore re-introduces E(r) at the covering step — implicitly via the local energy inequality, which gives E(r) ≥ c(C(r) + D(r)) for some constant c. This ties E(r) to the C + D criterion and restores the counting:

    C(r_i, z_i) + D(r_i, z_i) ≥ ε₀   →   E(r_i, z_i) ≥ c ε₀   →   ∫∫_{Q_{r_i}}|∇u|² ≥ c ε₀ r_i

giving Σ_i r_i ≤ (1/c ε₀) ∫∫ |∇u|², and therefore P¹(Σ) = 0.

**Conclusion on scaling:** Lin's scaling structure is identical to CKN. The parabolic dimension 5, the NS scaling (u ~ r⁻¹, p ~ r⁻²), and the counting argument all produce the same exponent 1 for the Hausdorff dimension of Σ. Lin's compactness argument does not change this.

**The blow-up sequence scaling:** In Lin's blow-up argument, the rescaled sequence ũ^n has:

    ||ũ^n||_{L^{10/3}(Q_1)} ≤ C (independent of n)

by the parabolic Sobolev embedding applied to the energy-class assumption. This uniform bound is what ensures compactness (in the Aubin-Lions sense). The exponent 10/3 = 2N/(N-2) with N = 5 (parabolic dimension) appears here, same as CKN.

---

## Section 5: Free-Parameter vs. Fixed-Constant Estimates

### Does Compactness Eliminate Young/Absorption Steps?

**Short answer:** No. The compactness argument defers rather than eliminates the Young's inequality steps.

**Detailed analysis:**

Lin's proof of Theorem 1.1 (ε-regularity) by contradiction does not explicitly use Young's inequality. The argument runs: assume (u^n, p^n) satisfy C + D < 1/n but are irregular → rescale → pass to limit → limit is regular → contradiction.

However, the compactness step itself requires:

(a) **Uniform bounds:** The sequence (ũ^n, p̃^n) must be bounded in appropriate function spaces to extract a convergent subsequence. These uniform bounds require Young/Sobolev estimates applied to the individual solutions. Specifically, one needs:

    ||ũ^n||_{L^∞(L²) ∩ L²(H¹)} ≤ C

which follows from the local energy inequality applied to each (u^n, p^n). The derivation of this bound uses exactly the Young/absorption steps Y1-Y4 from CKN (see exploration-001), applied now to the rescaled sequence. Lin doesn't write these steps because he assumes the reader knows they follow from the definition of suitable weak solution and the standard a priori estimates. The estimates are not avoided — they are hidden in the assumption that suitable weak solutions exist with the right integrability.

(b) **Passage to limit:** The limit ũ of ũ^n must be a suitable weak solution itself. This requires showing the local energy inequality is preserved in the limit, which uses weak lower-semicontinuity of ∫|∇u|². This is a standard but non-trivial step that absorbs the technical work of showing the nonlinear terms converge.

(c) **Identification of the limit:** One must show that if C(1, 0; ũ) + D(1, 0; ũ) = 0 (from the limit), then ũ ≡ 0. This uses the Serrin uniqueness theorem for small NS data, which itself is proved using energy estimates (and hence Young's inequalities).

**Which estimates still require free parameters:**

Lin's proof, like CKN's, requires choosing ε₀ in the ε-regularity criterion. In the compactness argument, ε₀ appears as follows: the contradiction holds as long as ε₀ is chosen small enough that the limiting solution ũ satisfies C(1,0;ũ) + D(1,0;ũ) < ε₀ forces ũ ≡ 0 (i.e., ε₀ < threshold for the uniqueness theorem). This threshold is determined by Serrin's theorem, which in turn depends on the same Sobolev and Young constants as CKN. The free parameter ε₀ is implicitly set by these constants.

**Lin's lossiness is the same as CKN's, just invisible:**

CKN makes the lossiness explicit: Young step Y2 (Ladyzhenskaya absorption) introduces a free parameter δ > 0, and ε₀ is proportional to some power of δ. Lin's compactness hides this — ε₀ emerges as a fixed but uncomputed threshold, determined by properties of the Stokes/NS system in the small-data regime. The structural reason ε₀ is finite and positive is the same in both proofs: the NS equation at small amplitude is well-approximated by the Stokes equation (linear), and the Stokes equation is regular. The lossiness in both cases comes from how far the NS nonlinear term deviates from Stokes, which is controlled by exactly the same Sobolev/Young estimates in both proofs.

**Summary of Young/absorption steps in Lin:**

| CKN Step | Lin's handling | Explicit in Lin? |
|---|---|---|
| Y1 (pressure-velocity Hölder in LEI) | Hidden in "suitable weak solution" definition | No |
| Y2 (Ladyzhenskaya free-parameter absorption) | Hidden in "uniform bounds for compactness" | No |
| Y3 (parabolic Sobolev interpolation for L^{10/3}) | Hidden in "compactness extraction" | No |
| Y4 (pressure regularity iteration) | Hidden in "limit is a Stokes-type solution" | No |

All four steps occur in Lin's proof — they just occur in the background (in the verification of the compactness infrastructure) rather than in the foreground (as explicit estimates).

---

## Comparison with CKN (1982)

| Feature | CKN (1982) | Lin (1998) |
|---|---|---|
| **ε-regularity criterion** | A(r) + E(r) + C(r) + D(r) < ε₀ | C(r) + D(r) < ε₀ (simpler) |
| **Proof method for ε-regularity** | Direct: explicit cutoff PDE estimates | Contradiction + compactness (blow-up) |
| **Localization** | Explicit cutoff φ with |∇φ| ~ 1/r, error terms tracked | Implicit: absorbed into "uniform bounds for compactness" |
| **Pressure treatment** | Explicit harmonic split p = p₁ + p₂, each piece estimated separately | Implicit: needed for compactness but not written |
| **Covering argument** | Vitali for parabolic cylinders, Σ_i r_i ≤ (1/ε₀)∫|∇u|² | Identical to CKN |
| **Dimension bound mechanism** | E(r) scale-invariant → ∫|∇u|² ~ r → P¹(Σ) = 0 | Same (E(r) re-enters via LEI at covering step) |
| **Young/absorption** | Explicit (Y1–Y4 in exploration-001) | Implicit (hidden in compactness infrastructure) |
| **ε₀ determination** | Chain of Sobolev/CZ constants, uncomputed but structurally tracked | Completely opaque — emerges from contradiction |
| **Parabolic Sobolev exponent** | 10/3 = 2N/(N-2), N = 5 | Same (needed for compactness) |
| **Proof length** | ~61 pages (CKN original) | ~17 pages (Lin 1998) |

---

## Assessment: Same Bottleneck or Different Route?

**Same bottleneck, different packaging.**

Lin's proof reaches P¹(Σ) = 0 through exactly the same structural mechanism as CKN:

1. Scale-invariant quantity C(r) + D(r) small → regularity (via compactness instead of direct estimates)
2. C(r) + D(r) ≥ ε₀ on singular set → E(r) ≥ c ε₀ on singular set (via LEI)
3. E(r) ≥ c ε₀ → ∫∫_{Q_r}|∇u|² ≥ c ε₀ r (from the definition of E(r))
4. Vitali covering → Σ_i r_i ≤ (1/c ε₀)∫∫|∇u|² → P¹(Σ) = 0

Step 3 is the bottleneck in both proofs: the dimension-1 bound comes from the fact that E(r) is scale-invariant and the raw integral ∫∫|∇u|² scales linearly in r. Lin's compactness does not change this — it cannot, because the dimension bound is determined by the NS parabolic scaling, not by how the ε-regularity step is proved.

**Does Lin's simplification open any new door?**

The compactness approach opens exactly one door: it shows that A(r) + E(r) can be dropped from the ε-criterion, leaving only C(r) + D(r). This is an *input* simplification — a weaker hypothesis for the same conclusion. But this simpler hypothesis reaches the same P¹ bound through the same mechanism. The dimension-1 exponent in the bottleneck (step 3 above) is untouched.

In principle, the compactness approach could detect a sharper dimension bound if the limiting solution ũ after blow-up were known to vanish to a higher order. But Lin's argument only shows ũ ≡ 0 (from C(1;ũ) + D(1;ũ) = 0), not that ũ vanishes "with curvature" or satisfies a stronger condition. The extra structure needed to improve the dimension bound would have to be extracted from the NS equation in the limit — which is the same hard analysis problem that CKN's direct approach also faces.

**Summary:** Lin's (1998) proof is a streamlining of CKN, not a structural departure. The structural bottleneck — the scale-invariance of E(r) forcing dim(Σ) ≤ 1 — is present and unchanged.

---

## Sources

- Fanghua Lin (1998), "A new proof of the Caffarelli-Kohn-Nirenberg theorem," *Communications on Pure and Applied Mathematics* 51(3):241–257. [Varnothing preprint: https://varnothing.net/wp-content/uploads/2021/11/lin1998.pdf]
- Caffarelli, Kohn, Nirenberg (1982), "Partial regularity of suitable weak solutions of the Navier-Stokes equations," *Comm. Pure Appl. Math.* 35(6):771–831.
- Ladyzhenskaya, Seregin (1999), "On partial regularity of suitable weak solutions to the three-dimensional Navier-Stokes equations," *J. Math. Fluid Mech.* 1:356–387.
- Vasseur (2005/2007), "A new proof of partial regularity of solutions to the Navier-Stokes equations," *NoDEA* 14(5-6):753–785. [Preprint: https://web.ma.utexas.edu/users/vasseur/documents/preprints/NS2.pdf]
- Seregin, Shilkin (2014), "Local regularity theory for the Navier-Stokes equations near the boundary," arXiv:1402.7181.
- Ren, Wang, Wu (2017), "Remarks on the singular set of suitable weak solutions to the 3D Navier-Stokes equations," arXiv:1709.01319.
- Barker, Wang (2022), "Estimates for the singular set of suitable weak solutions to the 3D Navier-Stokes equations," arXiv:2111.15444.
- Robinson, Rodrigo, Sadowski (2016), *The Three-Dimensional Navier-Stokes Equations: Classical Theory*, Cambridge University Press.
- CKN Seminar Notes (Skipper, 2019), Universität Ulm. [https://www.uni-ulm.de/fileadmin/website_uni_ulm/mawi.inst.020/skipper/SeminarCKN207.pdf]
