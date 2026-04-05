# Three Practical Paths to Close the Logarithmic Gap in Theorem CB

**Date:** 2026-04-02
**Parent:** coupled-bootstrap-attempt.md, curvature-evolution-analysis.md
**Purpose:** Concrete, technically grounded strategies for obtaining the logarithmic improvement |D_xi S| <= C |omega|^{3/2} / (nu^{1/2} (log |omega|)^{1+epsilon}) that would close the coupled bootstrap and prove 3D Navier-Stokes regularity.

---

## The Precise Target

Theorem CB establishes: if |D_xi S| <= C |omega|^{1+delta} on {|omega| > M} with delta > 1/2, then NS is regular. The dimensional estimate gives exactly delta = 1/2, i.e., |D_xi S| ~ |omega|^{3/2} / nu^{1/2}. We need to beat this by any amount -- even a logarithmic factor suffices:

    |D_xi S(x)| <= C |omega(x)|^{3/2} / (nu^{1/2} (log(|omega(x)|/Omega_0))^{1+epsilon})

for some epsilon > 0 on the set {|omega| > M}. This would force the blowup exponent alpha < 1 (by a logarithmic correction), and the BKM integral converges.

The three paths below attack this from genuinely different directions: one through the Biot-Savart structure of the specific quantity D_xi S, one through the evolution equation for D_xi S itself, and one through a reformulation that replaces the pointwise estimate with an integral condition that the existing enstrophy dissipation can handle.

---

## Path 1: Directional Cancellation in the Biot-Savart Kernel for D_xi S

### Core idea

D_xi S = (xi . nabla) S is not a generic component of nabla S. It is the derivative of the strain tensor in the specific direction xi = omega/|omega|, and the strain S is itself determined from omega via Biot-Savart. This creates a structural coupling: the direction along which we differentiate is determined by the same field that generates the quantity being differentiated. The Biot-Savart representation of D_xi S at a point x involves a singular integral whose kernel has angular structure that is not symmetric with respect to the xi-direction. Specifically, the angular average of the kernel K_{ij,k}(hat{r}) xi_k over the sphere vanishes for certain tensor components due to the incompressibility constraint and the symmetry of the strain. The logarithmic gain would come from showing that this angular cancellation suppresses the contribution of the most dangerous (nearby, high-vorticity) region of the integral by a logarithmic factor compared to the naive CZ estimate.

### Why it might produce the logarithmic gain

The key structural feature is the **alignment between xi and omega in high-vorticity regions**. The e_2-alignment confirmed in the pursuit means xi approximately equals the intermediate strain eigenvector e_2 where |omega| is large. The Biot-Savart kernel for nabla S has the schematic form:

    (nabla S)_{ij,k}(x) = PV integral K_{ij,k,l}(x-y) omega_l(y) dy

The directional projection xi_k K_{ij,k,l} omega_l, when omega_l = |omega| xi_l with xi approximately a fixed direction (e_2) in the high-vorticity region, becomes:

    xi_k K_{ij,k,l} xi_l |omega(y)|

This is a *rank-1 angular projection* of the CZ kernel. For the Biot-Savart kernel, the angular integral of x_k x_l / |x|^5 over the unit sphere is (1/3) delta_{kl} / (4 pi). When k = l (as happens when xi is approximately constant in the high-vorticity region and we project twice along it), significant cancellation occurs in the principal value integral from the near-field. The cancellation is not perfect -- it leaves a remainder controlled by the variation of xi -- but for regions where xi is slowly varying (which is precisely the high-vorticity tube interior), the remainder is suppressed by a factor related to |nabla xi| / |omega|. Near the vorticity maximum where |nabla |omega|| = 0, this suppression can provide the logarithmic gain through the balance between the shrinking high-vorticity region (contributing the log) and the cancellation within it.

### First concrete computation

**Lemma to attempt:** Let omega = |omega(y)| xi(y) with xi(y) = xi_0 + O(epsilon) for |y - x_*| < rho (a region of near-constant direction). Decompose the Biot-Savart integral for D_xi S(x_*) into the near-field (|y - x_*| < rho) and far-field contributions. Show that the near-field contribution satisfies:

    |(D_{xi_0} S)_{near}| <= C epsilon |omega|_{max} / rho + C |omega|_{max}^{3/2} / (nu^{1/2} log(rho/r_c))

where r_c = (nu/|omega|_{max})^{1/2} is the core radius and epsilon = sup_{B_rho(x_*)} |xi - xi_0|.

The point is to show that for the self-consistent choice rho ~ r_c log(|omega|/Omega_0) (the tube radius times a logarithmic factor), the near-field gains a log factor and the far-field is controlled by standard CZ estimates.

Compute this integral explicitly for a Burgers vortex with slowly varying axis direction (i.e., a Burgers tube with curvature kappa << 1/r_c). Verify the cancellation numerically and extract the precise logarithmic dependence.

### What would kill it

- If the angular cancellation in xi_k K_{ij,k,l} xi_l is only a finite multiplicative constant improvement rather than a logarithmic one (i.e., it changes the constant C but not the scaling). This would happen if the leading-order cancellation is exact but the first subleading term has the full dimensional scaling.
- If the variation of xi across the high-vorticity region (epsilon in the near-field estimate) is itself of order 1 at the relevant scale, negating the cancellation. DNS data on |nabla xi| at vorticity maxima would test this.
- If the far-field contribution (distant high-vorticity regions, tube interactions) dominates D_xi S at vorticity maxima, making the near-field cancellation irrelevant.

### Estimated probability of success

**15-20%.** The angular cancellation is real and structurally grounded in the Biot-Savart representation + alignment. The question is whether it is strong enough to provide a logarithm rather than just a better constant. The explicit computation for Burgers vortices is doable and would definitively test the mechanism. The main risk is that the tube-interaction term from the far-field defeats the near-field gain.

---

## Path 2: Logarithmic Gronwall on the D_xi S Evolution Equation

### Core idea

Instead of bounding D_xi S from the Biot-Savart representation (a spatial estimate), bound it from its own evolution equation (a temporal estimate). The strain evolution D_t S = -S^2 + (1/4) omega (x) omega - nabla^2 p + nu Delta S implies an evolution for D_xi S that has the schematic form:

    D_t(D_xi S) = -2 S (D_xi S) + (|omega|/2)(xi (x) eta + eta (x) xi) + (|omega|/2)(D_xi |omega|/|omega|)(xi (x) xi)
                  - D_xi(nabla^2 p) + nu Delta(D_xi S) + [D_t, D_xi] S + correction terms

The critical observation: the leading nonlinear term -2S(D_xi S) has a DAMPING sign for D_xi S (it is linear in D_xi S with coefficient -2S, and S has a positive eigenvalue s_1 > 0). The source terms involve D_xi(nabla^2 p), which is third-derivative level, BUT the pressure Poisson equation relates nabla^2 p to |S|^2 and |omega|^2, so D_xi(nabla^2 p) can be partially expressed in terms of lower-order quantities through elliptic regularity. The strategy is to close a Gronwall estimate on ||D_xi S||_{L^2} restricted to the high-vorticity set, using the parabolic structure (viscous diffusion) and the nonlinear damping from the -2S(D_xi S) term to absorb the source terms up to a logarithmic correction.

### Why it might produce the logarithmic gain

The NS equations have a well-known *logarithmic* regularity margin in the enstrophy evolution. The classical computation:

    (1/2) d/dt ||omega||_{L^2}^2 = integral omega . S omega dx - nu ||nabla omega||_{L^2}^2

The vortex stretching term integral omega . S omega is bounded by ||omega||_{L^2} ||omega||_{L^4}^2 (by Holder), and the Sobolev interpolation ||omega||_{L^4}^2 <= C ||omega||_{L^2} ||nabla omega||_{L^2} produces the cubic nonlinearity that is *exactly critical* vs. the dissipation. The celebrated result of Tao (2020, finite-time blowup for averaged NS) shows that the equation without the specific structure of the nonlinearity does blow up, but the full NS nonlinearity has additional cancellations from the divergence-free condition and the pressure.

For D_xi S, the analogous energy estimate on the high-vorticity set {|omega| > M} would involve:

    (1/2) d/dt integral_{|omega|>M} |D_xi S|^2 dx = (interaction terms) - nu integral_{|omega|>M} |nabla(D_xi S)|^2 dx + (boundary terms from the moving set)

The logarithmic gain comes from the **boundary terms from the moving set {|omega| > M}**. As M increases, the set {|omega| > M} shrinks. For smooth solutions, the measure of this set satisfies |{|omega| > M}| <= ||omega||_{L^2}^2 / M^2. The contribution of D_xi S from the boundary of this set is controlled by the enstrophy dissipation integral ||nabla omega||_{L^2}^2 dt, which is finite. The key estimate is a De Giorgi-type truncation: restricting to the high-vorticity set and using the finiteness of the enstrophy dissipation introduces a logarithmic savings through the layer-cake decomposition of the L^p norm. Specifically, writing:

    ||D_xi S||_{L^infty({|omega|>M})} <= C ||D_xi S||_{L^2({|omega|>M})} log^{1/2}(||nabla(D_xi S)||_{L^2} / ||D_xi S||_{L^2})

(from the Brezis-Gallouet logarithmic Sobolev inequality in 2D, applied on the essentially 2D cross-section of the vortex tube), the logarithmic interpolation produces the needed log factor.

### First concrete computation

**Lemma to attempt:** Establish a localized energy estimate for |D_xi S|^2 on the set {|omega| > M}. Specifically, define:

    E_M(t) = integral phi_M(|omega|) |D_xi S|^2 dx

where phi_M is a smooth cutoff with phi_M(s) = 1 for s > 2M and phi_M(s) = 0 for s < M. Compute dE_M/dt from the NS equations. Identify the leading positive (source) and negative (dissipation) terms. Determine whether the source terms can be absorbed by the dissipation plus a term of order:

    C E_M ||omega||_{L^infty} log(||omega||_{L^infty}/M)

If so, Gronwall gives E_M(t) <= E_M(0) exp(C integral_0^t ||omega||_{L^infty} log(||omega||/M) ds), and the log factor in the exponential translates to a log factor in the pointwise bound on D_xi S via Sobolev embedding on the high-vorticity set.

The first step is to compute dE_M/dt for a specific solution (Burgers vortex) and verify the structure.

### What would kill it

- If the boundary terms from differentiating phi_M(|omega|) generate contributions proportional to |nabla omega| |D_xi S|^2, which blow up faster than the dissipation can absorb. Since |nabla omega| is only in L^2(dt; L^2(dx)), the boundary contributions could be uncontrollable on a pointwise level.
- If the D_xi(nabla^2 p) source term in the D_xi S evolution cannot be decomposed into a part controlled by |D_xi S| itself (for Gronwall) and a remainder controlled by the enstrophy dissipation. This would happen if the third derivatives of pressure are genuinely independent of D_xi S and |omega|.
- If the Brezis-Gallouet logarithmic interpolation does not apply because the high-vorticity set is not effectively 2-dimensional (the tube geometry is needed for this step).

### Estimated probability of success

**8-12%.** This path has the most technically demanding first computation, and the chain of estimates is long with multiple potential failure points. However, it is the path that most directly engages with the PDE structure (energy methods, parabolic regularity) rather than relying on model-dependent geometric assumptions. If the localized energy estimate closes even at the formal level, it would represent a genuine advance in the regularity theory. The Brezis-Gallouet step is the most speculative -- it requires the effective dimensionality reduction from tube geometry, which is heuristically supported but hard to make rigorous.

---

## Path 3: Hasimoto Transform + Controlled Departure from LIA

### Core idea

Under the Local Induction Approximation (LIA), the curvature kappa = |D_xi xi| of a thin vortex filament evolves according to the 1D cubic NLS (via the Hasimoto transform), which is globally well-posed. The curvature-evolution analysis confirmed this. The full NS dynamics depart from LIA by corrections that are O(epsilon) where epsilon = kappa r_c (the tube slenderness ratio). The strategy is NOT to prove kappa is bounded directly, but rather to prove that D_xi S (the problematic source term) is well-approximated by its LIA value plus controlled corrections, and that the LIA value of D_xi S is exactly the quantity that makes the coupled bootstrap close with a logarithmic margin.

Under LIA for a filament with curvature kappa and torsion tau, the strain field is the Biot-Savart field of the tube. The LIA strain gradient along the tube axis is:

    (D_xi S)_{LIA} ~ Gamma kappa / r_c^2 * (bounded function of kappa, tau, arc-length derivatives)

Using Gamma ~ |omega| r_c^2 (for a Burgers vortex), this gives:

    |D_xi S|_{LIA} ~ |omega| kappa

Now kappa for the LIA/NLS evolution is bounded by the H^1 norm of the Hasimoto variable: kappa <= ||psi||_{L^infty} <= C(||psi_0||_{H^1}). This is a *fixed constant*, not growing with |omega|. So:

    |D_xi S|_{LIA} ~ C |omega|

which is |omega|^{1+0} -- far better than the dimensional estimate |omega|^{3/2}/nu^{1/2}. If the corrections to LIA are of order epsilon = kappa r_c ~ kappa (nu/|omega|)^{1/2} times the LIA value, then:

    |D_xi S| <= |D_xi S|_{LIA} + epsilon |D_xi S|_{dim} ~ C |omega| + kappa (nu/|omega|)^{1/2} |omega|^{3/2}/nu^{1/2}
             = C |omega| + kappa |omega|

If kappa is bounded (from the NLS global well-posedness in the LIA regime), then |D_xi S| <= C |omega|, which gives delta = 0 in Theorem CB -- much better than needed. But the problem is that kappa may not remain in the LIA regime.

The refined strategy: prove that *as long as* kappa r_c < 1/2 (the LIA regime), the D_xi S bound is |D_xi S| <= C |omega| (1 + kappa r_c log(1/(kappa r_c))). If kappa r_c approaches 1, the NLS approximation breaks down, but at that point the viscous core thickening (r_c grows as sqrt(nu t)) forces r_c to increase, restoring the thin-tube condition. The logarithmic factor arises from the matched asymptotic expansion of the Biot-Savart integral at the transition scale kappa r_c ~ 1.

### Why it might produce the logarithmic gain

The structural feature being exploited is the **complete integrability of the LIA/NLS dynamics**. The 1D cubic NLS has infinitely many conserved quantities (L^2 norm, H^1 norm, etc.), and these conservation laws propagate to bounds on the curvature and torsion of the vortex filament. The corrections to LIA from the full Biot-Savart law are perturbative for thin tubes (epsilon << 1), and the Fukumoto-Moffatt (2000) expansion gives them explicitly to O(epsilon^2).

The logarithmic gain comes from the matched asymptotics of the Biot-Savart integral for a thin tube. The classical result (Widnall, Bliss, Tsai 1971; Callegari-Ting 1978) gives the velocity of a curved thin tube as:

    v = (Gamma kappa / 4pi) [log(L/r_c) + C_core] b + O(1)

where L is the radius of curvature (~ 1/kappa) and C_core depends on the core profile. The log(L/r_c) = log(1/(kappa r_c)) factor is intrinsic to the self-induction. When computing D_xi S from this matched expansion, the leading term is O(|omega| kappa) as above, and the subleading term carries the log:

    |D_xi S| = C_1 |omega| kappa + C_2 |omega| kappa^2 r_c log(1/(kappa r_c)) + O(|omega| kappa^2 r_c)

Using kappa <= K_max (from NLS) and r_c = (nu/|omega|)^{1/2}:

    |D_xi S| <= C_1 K_max |omega| + C_2 K_max^2 |omega|^{1/2} nu^{1/2} log(|omega|^{1/2}/(K_max nu^{1/2}))
             <= C |omega| + C |omega|^{1/2} log(|omega|)

Both terms are far below the |omega|^{3/2}/nu^{1/2} threshold. The full NS dynamics can contribute additional terms from tube-tube interactions and from the pressure Hessian correction to the core profile, but these are bounded by the Biot-Savart structure if the inter-tube separation remains of order r_c or larger.

### First concrete computation

**Lemma to attempt:** For a Burgers vortex tube with axis curvature kappa and core radius r_c = (nu/s_1)^{1/2}, compute D_xi S explicitly using the matched asymptotic expansion of the Biot-Savart integral. The computation should:

1. Start with the Callegari-Ting (1978) matched asymptotic expansion for the velocity field of a curved viscous vortex tube, extended to include the strain gradient.
2. Compute (xi . nabla) S_{ij} at the tube center, where xi is the unit tangent to the tube axis.
3. Express the result in terms of kappa, tau (torsion), r_c, Gamma (circulation), and s_1 (the external strain).
4. Verify that the dominant term is O(Gamma kappa / r_c^2) = O(|omega| kappa), confirming the LIA-level estimate.
5. Compute the first correction, which should be O(Gamma kappa^2 log(1/(kappa r_c))) = O(|omega| kappa^2 r_c log(1/(kappa r_c))).
6. Verify numerically against the DHY-Burgers test (dhy-burgers-test.md) that the matched asymptotic expansion reproduces the computed D_xi S values.

This is a well-defined asymptotic calculation with existing literature to build on. The result would establish the precise D_xi S scaling for the canonical thin-tube model.

### What would kill it

- If the matched asymptotic expansion of D_xi S does not converge for the relevant range of kappa r_c (i.e., if the correction terms grow faster than the leading term for kappa r_c > some epsilon_0, and high-vorticity regions have kappa r_c > epsilon_0).
- If tube-tube interactions contribute a D_xi S term of order |omega|^{3/2}/nu^{1/2} that cannot be bounded by the LIA-level estimate. This would happen if two high-vorticity tubes approach each other at distance d ~ r_c with non-parallel orientations, creating strain gradients of the dimensional magnitude.
- If the NLS global well-posedness does not transfer to bounded kappa for the corrected (non-integrable) system. The Fukumoto-Moffatt corrections break integrability, and global well-posedness of the corrected 1D NLS is not established. If kappa can grow without bound in the corrected system, the LIA-level bound |D_xi S| ~ |omega| kappa fails.
- Most critically: if high-vorticity regions in NS are NOT well-described as thin tubes. If the geometry near a potential singularity is sheet-like, or involves complex topology (vortex tangles with inter-tube distance ~ r_c), the matched asymptotic framework does not apply.

### Estimated probability of success

**10-15%.** This path has the strongest structural foundation (NLS integrability, matched asymptotics, existing literature on vortex filament dynamics) and would produce the most informative intermediate results even if the full program does not close. The first computation (matched asymptotic D_xi S for curved Burgers) is feasible in weeks and would either confirm or falsify the mechanism at the model level. The main risk is the extension from the single-tube model to the full NS dynamics -- the tube-tube interaction problem is the hard part, and there is no existing framework for bounding D_xi S in multi-tube configurations. However, DNS evidence (Jimenez et al. 1993, Hamlington et al. 2008) strongly supports that high-vorticity regions are tube-like at all accessible Reynolds numbers, which motivates the single-tube estimate as the dominant contribution.

---

## Comparison of the Three Paths

| | Path 1: Directional Cancellation | Path 2: Logarithmic Gronwall | Path 3: Hasimoto + LIA |
|---|---|---|---|
| **Nature** | Spatial (Biot-Savart kernel analysis) | Temporal (energy method on D_xi S evolution) | Structural (matched asymptotics + integrable model) |
| **NS structure exploited** | Angular cancellation in CZ kernel under alignment | Parabolic dissipation + localization to high-vorticity set | LIA/NLS integrability + tube geometry |
| **What must be true** | Alignment suppresses near-field D_xi S by log factor | Localized energy estimate on D_xi S closes with log Gronwall | High-vorticity regions are thin tubes; corrections to LIA are perturbative |
| **Model dependence** | Moderate (alignment is confirmed, cancellation is computable) | Low (pure PDE, no geometric assumptions needed a priori) | High (requires tube geometry, single-tube dominance) |
| **First computation difficulty** | Medium (explicit Biot-Savart integral for Burgers tube) | Hard (localized energy estimate, multiple integrations by parts) | Medium (matched asymptotics, existing literature) |
| **Success probability** | 15-20% | 8-12% | 10-15% |
| **Best case outcome** | A sharp pointwise bound on D_xi S with explicit log gain | A PDE-level proof of regularity, bypassing tube geometry | Complete matched asymptotic description of D_xi S with all error terms |
| **If it fails, what do we learn?** | Whether angular cancellation in Biot-Savart is quantitatively significant | Whether energy methods can ever close at the supercritical level for NS | Whether tube geometry is the right framework for near-singular NS |

---

## Recommended Sequence

1. **Start with Path 3** (Hasimoto + LIA). The first computation (matched asymptotic D_xi S for curved Burgers vortex) is the most concrete, has the most existing literature to build on, and produces a definitive numerical answer. If the computation confirms |D_xi S| ~ |omega| kappa with controlled corrections, it validates the structural framework and motivates the harder extension to multi-tube configurations. If it fails (corrections are uncontrolled), it kills one path early and redirects effort.

2. **In parallel, attempt Path 1** (Directional Cancellation). The explicit Biot-Savart integral computation for a Burgers tube can be done simultaneously. If the angular cancellation produces a genuine log factor, this is the shortest path to a pointwise bound. Path 1 and Path 3 have complementary strengths: Path 1 works at the Biot-Savart level (no tube assumption needed a priori, but exploits alignment), while Path 3 works at the filament dynamics level (tube assumption explicit, integrability exploited).

3. **Attempt Path 2** (Logarithmic Gronwall) only if Paths 1 and 3 produce positive intermediate results that clarify the PDE structure. Path 2 is the most technically demanding and the most likely to stall on intermediate difficulties, but it is also the only path that could produce a full proof without relying on tube geometry. It should be attempted after the structural picture from Paths 1 and 3 is clear.

---

## What Success Looks Like

For any path, the minimal viable result is:

**A rigorous proof that on the set {|omega(x,t)| > M}, the directional strain gradient satisfies:**

    |(xi . nabla) S(x,t)| <= C(M, nu, u_0) |omega(x,t)|^{3/2} / (nu^{1/2} g(|omega(x,t)|))

**where g(s) -> infinity as s -> infinity (even as slowly as (log log s)^epsilon).**

Feeding this into Theorem CB would give alpha = 1 - o(1) < 1, and the BKM integral converges (just barely). This would constitute a proof of 3D Navier-Stokes regularity for smooth initial data.

The gap between the dimensional estimate (g = 1) and what is needed (any g -> infinity) is the narrowest quantitative gap in the entire Millennium Prize problem. These three paths represent three distinct structural mechanisms -- angular cancellation, parabolic regularization, and integrability -- any one of which could close it.
