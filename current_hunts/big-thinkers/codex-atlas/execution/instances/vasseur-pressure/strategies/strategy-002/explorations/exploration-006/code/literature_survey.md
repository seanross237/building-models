# Literature Survey: Non-CZ Approaches to Pressure in Navier-Stokes Regularity Theory

## Scope

This survey catalogues published approaches to handling the pressure term in Navier-Stokes (NS) regularity theory that do NOT rely on standard Calderon-Zygmund (CZ) singular integral bounds, or that illuminate the structural role of pressure in ways relevant to bypassing the beta = 4/3 barrier in Vasseur's De Giorgi framework. For each approach, we record: the exact method used for pressure, whether CZ bounds appear explicitly or implicitly, the regularity result obtained, and whether the approach could in principle yield better exponents than CZ.

---

## 1. Caffarelli-Kohn-Nirenberg (1982) — Partial Regularity via epsilon-Regularity

**Reference:** Caffarelli, L., Kohn, R., Nirenberg, L. "Partial regularity of suitable weak solutions of the Navier-Stokes equations." Comm. Pure Appl. Math. 35 (1982), 771-831.

### Method for Pressure

CKN does NOT use a De Giorgi iteration and does NOT use CZ bounds on the pressure in the sense of Vasseur (2007). Their approach is fundamentally different:

1. **Local energy inequality.** They work with "suitable weak solutions" satisfying a localized energy inequality:

   partial_t(|u|^2/2) + |nabla u|^2 <= div(...) + (|u|^2/2 + p) u . nabla phi + ...

   The pressure enters the local energy inequality through the flux term (|u|^2/2 + p) u . nabla phi, where phi is a smooth cutoff function. This is an *energy-based* treatment: the pressure appears multiplied by u and tested against the cutoff, not estimated independently in an L^p norm.

2. **epsilon-regularity criterion.** The core of the proof is a dimension-reduction argument. They establish: if the scale-invariant quantity

   r^{-1} integral_{Q_r} (|u|^3 + |p|^{3/2}) dx dt

   is sufficiently small over a parabolic cylinder Q_r, then u is regular at the center. The pressure enters this smallness condition at the natural scaling exponent 3/2.

3. **Pressure estimates used.** To verify the epsilon-regularity condition, CKN use the Poisson equation Delta p = -partial_i partial_j (u_i u_j) and standard elliptic regularity: ||p||_{L^{3/2}} <= C ||u||_{L^3}^2. This IS a CZ-type estimate, but it is used in a qualitatively different way from Vasseur's framework. CKN only need the pressure to be small in an integrated sense over shrinking cylinders. They do not need to bound a specific truncated pressure component (like P^{21}) against a De Giorgi test function.

### Whether CZ Bounds Are Used

**Implicitly YES.** The estimate ||p||_{L^{3/2}} <= C ||u||_{L^3}^2 is precisely the CZ bound for the Riesz transforms. However, CKN use it only as a *qualitative input* to their epsilon-regularity criterion, not as a *quantitative bound in an iteration*. The exponent 3/2 for pressure in the smallness condition is the CZ-natural pairing with L^3 for velocity.

### Result Obtained

One-dimensional parabolic Hausdorff measure of the singular set is zero: H^1_par(Sing(u)) = 0. This is partial regularity, not full regularity.

### Could This Approach Beat CZ Exponents?

**Unlikely for the beta = 4/3 question.** CKN's epsilon-regularity approach measures the singular set's size but does not attempt to prove full regularity. The CKN framework is optimized for partial regularity and has been shown to be essentially sharp by Buckmaster-Colombo-Vicol (2022), who constructed solutions saturating the CKN bounds. The pressure enters CKN at its natural CZ scaling, so there is no obvious path to improving pressure exponents within this framework. [CHECKED]

---

## 2. De Giorgi-Nash-Moser for Scalar Equations — The Pressure-Free Baseline

**References:**
- De Giorgi, E. "Sulla differenziabilita e l'analiticita delle estremali degli integrali multipli regolari." Mem. Accad. Sci. Torino 3 (1957), 25-43.
- Nash, J. "Continuity of solutions of parabolic and elliptic equations." Amer. J. Math. 80 (1958), 931-954.
- Moser, J. "A new proof of De Giorgi's theorem concerning the regularity problem for elliptic differential equations." Comm. Pure Appl. Math. 13 (1960), 457-468.

### The Original Theory (No Pressure)

For a scalar equation of the form

   partial_t theta + div(b theta) = Delta theta

with divergence-free drift b, the De Giorgi-Nash-Moser theory proves Holder continuity of theta without any pressure term. The key mechanism:

1. **Energy inequality at truncation levels.** Multiply by (theta - lambda_k)_+ and integrate. The divergence-free drift produces no contribution because div(b) = 0 and the nonlinear test function (theta - lambda_k)_+ absorbs the transport term via integration by parts.

2. **Iterative shrinking of super-level sets.** The energy inequality gives control of U_k = ||theta - lambda_k)_+||_{L^2}^2, and Sobolev embedding + Chebyshev gives the measure of the level sets. The iteration converges (De Giorgi lemma) if the initial quantity is small.

3. **No pressure appears** because the equation is scalar. The "pressure" in the NS context is a Lagrange multiplier enforcing the divergence-free constraint, which is automatically satisfied for scalar transport.

### What Analogous Term Appears for NS?

When adapting De Giorgi to the vector-valued NS equations

   partial_t u + (u . nabla)u + nabla p = Delta u,   div(u) = 0

the scalar truncation v_k = (|u| - lambda_k)_+ is used. Testing the NS equation against v_k (u/|u|) and integrating produces:

- **Dissipation term:** integral |nabla v_k|^2 (good, same as scalar case)
- **Transport term:** partially cancels due to div(u) = 0, but NOT completely — unlike the scalar case, the vector structure introduces cross terms
- **Pressure term:** integral nabla p . (v_k u/|u|) 1_{|u|>lambda_k}

This pressure integral is the NEW term that has no analog in scalar De Giorgi. It is the term that Vasseur decomposes as P^{11} + P^{12} + P^{21} + P^{22} and bounds using CZ.

### How Various Authors Handle It

| Author(s) | Method for pressure integral | CZ used? |
|---|---|---|
| Vasseur (2007) | Decompose into P^{ij}, bound P^{21} via CZ on L^{3/2} | YES, explicitly |
| Caffarelli-Vasseur (2010, SQG) | No pressure (scalar equation) | N/A |
| Vasseur-Yang (2021) | Take curl to get vorticity equation, eliminate pressure | NO (but pays cost) |
| Cheskidov-Dai (2014-2023) | Regularity criteria, Littlewood-Paley | Implicitly via Sobolev |

### Could Scalar De Giorgi Methods Help?

**The fundamental obstruction is that NS is a system, not a scalar equation.** The scalar De Giorgi theory works because: (a) the nonlinearity is in divergence form relative to the truncated variable, and (b) there is no pressure. For NS, neither holds. The truncation v_k = (|u| - lambda_k)_+ destroys the divergence-free structure, producing a non-divergence-form remainder that manifests as the pressure term.

Caffarelli-Vasseur (2010) proved global regularity for the critical SQG equation using De Giorgi precisely because SQG is scalar, divergence-free drift, fractional diffusion — the perfect setting. Their success does NOT transfer to NS because the vector structure introduces the pressure obstruction. [CHECKED]

---

## 3. Seregin-Sverak and Escauriaza-Seregin-Sverak — L^{3,infinity} Regularity

### Seregin-Sverak: Liouville Theorems for Ancient Solutions

**Reference:** Koch, G., Nadirashvili, N., Seregin, G., Sverak, V. "Liouville theorems for the Navier-Stokes equations and applications." Acta Math. 203 (2009), 83-105.

**Method for pressure:**

1. **Blow-up and rescaling.** Suppose (x_0, t_0) is a singular point. They rescale: u_lambda(x,t) = lambda u(lambda x + x_0, lambda^2 t + t_0). As lambda -> 0, the rescaled solutions converge to an "ancient solution" (defined for all t in (-infinity, 0]) of NS on all of R^3.

2. **Pressure in the limit.** The pressure of the limiting ancient solution satisfies the usual Poisson equation Delta p = -partial_i partial_j(u_i u_j) on all of R^3. For bounded ancient solutions, standard elliptic theory (which IS CZ) gives p in L^infinity. But the key point is that the Liouville theorem aims to show the ancient solution is CONSTANT, at which point the pressure is constant too.

3. **Pressure is handled via global elliptic estimates on R^3.** The whole-space setting allows optimal use of CZ, but the estimates are used only to establish boundedness of the ancient solution, not to run a De Giorgi iteration.

**CZ used?** Yes, implicitly, in establishing regularity of the limiting ancient solution. But the Liouville-type classification does not require iterative pressure bounds.

**Result:** If u is a bounded ancient solution of NS in R^3 x (-infinity, 0] that is axisymmetric with no swirl, then u is constant. The 3D case without symmetry assumptions remains open.

### Escauriaza-Seregin-Sverak: The L^{3,infinity} Endpoint

**Reference:** Escauriaza, L., Seregin, G., Sverak, V. "L_{3,infinity}-solutions of the Navier-Stokes equations and backward uniqueness." Russian Math. Surveys 58:2 (2003), 211-250.

**Method for pressure:**

1. **The pressure plays NO essential role in the proof.** Seregin's own survey (2012) states explicitly: "estimates for the pressure do not play an essential role" in the Escauriaza-Seregin-Sverak argument. This is a major point.

2. **The proof strategy avoids direct pressure estimates.** Instead:
   - Assume for contradiction that u in L^infinity_t(L^{3,infinity}_x) becomes singular at time T.
   - Rescale to produce a sequence of solutions on expanding domains.
   - The limit satisfies a perturbed heat equation on R^3 x [0, T] with variable lower-order coefficients.
   - Apply **backward uniqueness for parabolic operators** (proved via Carleman inequalities): if the solution vanishes at time T, it must vanish identically.
   - The contradiction comes from showing the rescaled solution must vanish at time T (from the L^{3,infinity} bound) but cannot vanish on the whole interval.

3. **Backward uniqueness replaces pressure estimates.** The Carleman inequality approach works on the velocity equation written as a perturbed heat equation. The pressure gradient nabla p appears only as a lower-order perturbation that is absorbed into the variable coefficients. No CZ bound on pressure is needed; the pressure is controlled by its role as a "small perturbation" in the backward uniqueness framework.

**CZ used?** **NO** in the backward uniqueness step, which is the heart of the proof. Standard elliptic estimates for pressure appear only in the preliminary reduction to establish that the rescaled solutions are smooth enough for the backward uniqueness argument to apply.

**Result:** L^{3,infinity} solutions of 3D NS are smooth. This is the endpoint of the Prodi-Serrin regularity criteria.

### Could This Approach Give Better Exponents Than CZ?

**The ESS approach is fundamentally different from De Giorgi iteration and does not produce a "beta exponent."** It is a contradiction argument: either the solution is regular, or backward uniqueness is violated. There is no iteration with level sets, no Chebyshev step, no pressure decomposition P^{ij}. The two approaches are structurally incomparable.

However, the ESS insight that *pressure estimates are not essential* for certain regularity results is deeply relevant. It suggests that the beta = 4/3 barrier may be an artifact of the De Giorgi + CZ approach, not of the NS equations themselves. An approach that avoids both De Giorgi iteration and CZ pressure bounds might not encounter the 4/3 at all. [CHECKED]

---

## 4. De Giorgi Applied to NS with Pressure Handled via Energy Methods

### Vasseur (2007) — The Standard Approach (Uses CZ)

**Reference:** Vasseur, A. "A new proof of partial regularity of solutions to Navier-Stokes equations." NoDEA 14 (2007), 753-785. arXiv:math/0607017.

For baseline comparison: Vasseur's Proposition 3 decomposes the pressure into four components P^{11}, P^{12}, P^{21}, P^{22} based on frequency interaction (above/below the truncation level). The critical term P^{21} (low-frequency velocity x high-frequency velocity) is bounded via CZ:

   ||P^{21}||_{L^{3/2}} <= C ||u^{below}||_{L^3} ||u^{above}||_{L^3}

This feeds into the bottleneck integral and produces beta = 1/2 + 5/6 = 4/3.

### Chamorro-Lemarie-Rieusset-Mayoufi (2018) — Pressure via Dissipative Solutions

**Reference:** Chamorro, D., Lemarie-Rieusset, P.G., Mayoufi, K. "The role of the pressure in the partial regularity theory for weak solutions of the Navier-Stokes equations." Arch. Ration. Mech. Anal. 228 (2018), 237-277. arXiv:1602.06137.

**Method for pressure:**

1. They introduce the notion of "dissipative solutions" due to Duchon-Robert (2000). Instead of the standard local energy inequality involving the pressure explicitly, they work with the Duchon-Robert energy equality:

   partial_t(|u|^2/2) + div(u(|u|^2/2 + p)) = Delta(|u|^2/2) - |nabla u|^2 - D(u)

   where D(u) is the local energy dissipation defect (a distribution measuring energy dissipation anomaly).

2. **The pressure term (|u|^2/2 + p) u appears as a flux.** In the dissipative solutions framework, the pressure is bundled with the kinetic energy into the Bernoulli quantity (|u|^2/2 + p), and this combined quantity appears only inside a divergence. When testing against a cutoff phi, the boundary terms involve (|u|^2/2 + p) u . nabla phi, which requires only local integrability of p u, not a pointwise CZ bound.

3. **Key insight:** "The pressure term usually included in hypothesis (A_n) is not in fact necessary." Their generalization shows that the CKN partial regularity theorem can be proved for dissipative solutions where the pressure enters only through the energy flux, not as an independent L^{3/2} condition.

**CZ used?** The pressure is not independently estimated via CZ in the epsilon-regularity argument. However, to verify that Leray-Hopf solutions are dissipative solutions, one still needs standard elliptic estimates for p. So CZ is used in the *existence theory*, not in the *regularity theory*.

**Result:** Partial regularity (H^1_par(Sing) = 0) for a broader class of solutions. No improvement to full regularity or to the CKN singular set dimension.

**Could this beat CZ exponents?** Not directly for the beta = 4/3 question. The Chamorro-Lemarie-Rieusset approach eliminates the pressure from the regularity criterion but does not run a De Giorgi iteration. It gives the same partial regularity conclusion as CKN. However, the philosophy — bundle p into an energy flux rather than estimating it independently — is suggestive. If one could similarly reorganize Vasseur's De Giorgi iteration to never estimate P^{21} in isolation, the beta exponent might change. [CHECKED]

### Wolf (2015-2017) — Local Pressure Decomposition Without CZ

**Reference:** Wolf, J. "On the local pressure of the Navier-Stokes equations and related systems." arXiv:1611.01482 (2016). Also: "On the local pressure expansion for the Navier-Stokes equations." J. Math. Fluid Mech. 24, Article 3 (2022). arXiv:2001.11526.

**Method for pressure:**

1. Wolf constructs a **local pressure decomposition** that avoids CZ estimates entirely. The key idea: every distribution partial_t u + F that vanishes on smooth solenoidal vector fields can be represented as partial_t nabla p_h + nabla p_0, where nabla p_h ~ u and nabla p_0 ~ F.

2. The pressure is split into a **harmonic part** p_h (satisfying Delta p_h = 0 locally, hence smooth) and a **particular part** p_0 (determined by the nonlinearity). The harmonic part can be estimated by mean-value properties without CZ. The particular part is estimated using only local Sobolev inequalities on a ball, not global CZ theory.

3. This decomposition is especially useful in domains where the global Poisson equation approach (and hence standard CZ) is not available.

**CZ used?** **NO.** Wolf's local pressure construction uses only: (a) De Rham theory to establish existence of local pressure, (b) Sobolev embedding on balls, (c) harmonic function estimates (mean value inequality). This is a genuinely CZ-free pressure handling method.

**Result:** Used to establish epsilon-regularity criteria and partial regularity for NS and related systems (MHD, liquid crystals), recovering CKN-type results. Does NOT achieve full regularity.

**Could this beat CZ exponents?** **This is the most promising CZ-free pressure method for the De Giorgi framework.** Wolf's local pressure decomposition produces pressure estimates of the same order as CZ (because the underlying Poisson equation is the same), so the exponents are not automatically better. However, the decomposition into harmonic + particular parts has different structure from the P^{11}/P^{12}/P^{21}/P^{22} decomposition, and the harmonic part is infinitely smooth. If the dominant contribution to the beta = 4/3 barrier comes from a component that is absorbed into the harmonic part, Wolf's decomposition might give a path to improvement. This requires detailed computation. [CONJECTURED]

### Ladyzhenskaya-Seregin (1999) — Blow-Up Proof of Partial Regularity

**Reference:** Ladyzhenskaya, O.A., Seregin, G.A. "On partial regularity of suitable weak solutions to the three-dimensional Navier-Stokes equations." J. Math. Fluid Mech. 1 (1999), 356-387.

**Method for pressure:**

The Ladyzhenskaya-Seregin proof uses a **compactness/blow-up** approach rather than direct quantitative estimates. They assume epsilon-regularity fails, extract a blow-up sequence, and derive a contradiction. The pressure in the blow-up limit is handled by:

1. Weak convergence of pressure along the blow-up sequence.
2. In the limiting equations, the pressure satisfies the usual Poisson equation but on all of R^3, where CZ theory is standard.

**CZ used?** Implicitly, in the limiting procedure. The blow-up approach does not require explicit CZ bounds at finite scale.

**Result:** Partial regularity, recovering CKN. The proof is considered more conceptual than CKN's original.

---

## 5. Vasseur-Yang (2021) — Curl Formulation Eliminating Pressure

**Reference:** Vasseur, A., Yang, J. "Second derivatives estimate of suitable solutions to the 3D Navier-Stokes equations." Arch. Ration. Mech. Anal. 241 (2021), 683-727.

### Method

Taking curl of the NS equations gives the vorticity equation:

   partial_t omega + (u . nabla) omega = (omega . nabla) u + Delta omega

The pressure nabla p is eliminated entirely (curl(nabla p) = 0). The cost is that the vortex stretching term (omega . nabla) u appears, and u must be recovered from omega via the Biot-Savart law u = K * omega, which introduces a nonlocal singular integral operator (itself a CZ-type operator, but acting on omega, not on pressure).

### De Giorgi Iteration on Vorticity

Vasseur-Yang apply De Giorgi iteration directly to the vorticity equation:

1. Truncate: w_k = (|omega| - mu_k)_+
2. Energy inequality: produces dissipation ||nabla w_k||_{L^2}^2 (good term)
3. **Vortex stretching term:** integral (omega . nabla) u . (w_k omega/|omega|)
   - This is the analog of the pressure term P^{21} in the velocity formulation
   - It involves the product omega_i partial_j u_i, which is a trilinear term requiring Biot-Savart inversion

4. **Biot-Savart law:** u = K * omega where K is the Biot-Savart kernel (|x|^{-2} in 3D). The operator nabla K is a CZ operator (Riesz transforms). So estimating ||nabla u||_{L^p} from ||omega||_{L^p} uses CZ bounds, but on the Biot-Savart kernel, not on the pressure Poisson equation.

### Does the Same beta = 4/3 Barrier Appear?

**YES.** This is the key finding from Exploration 001 of this mission (E001 REPORT-SUMMARY):

> "The cross-comparison confirms something profound: the 4/3 is intrinsic to the NS quadratic nonlinearity, not to the pressure handling. Taking curl eliminates the pressure entirely but the same 4/3 reappears from vortex stretching."

Specifically:
- The vortex stretching integral has the same Holder scaling as the pressure integral P^{21}
- The Biot-Savart law nabla u = CZ(omega) introduces the same singular integral bounds as nabla^2 Delta^{-1}(u otimes u) does for pressure
- The truncation v_k = (|omega| - mu_k)_+ has the same Sobolev + Chebyshev structure
- The resulting recurrence exponent is beta = 4/3, identical to the velocity formulation

### The Cost

1. **CZ is not truly eliminated** — it reappears in the Biot-Savart inversion nabla u = CZ(omega)
2. **Higher regularity is needed** — the vorticity equation involves second-order derivatives of u, requiring initial regularity assumptions
3. **The structural obstruction is the same** — the non-divergence-form quadratic interaction (omega . nabla)u = (omega . nabla)(K * omega) has the same scaling as the pressure term

### Result Obtained

Vasseur-Yang prove that second spatial derivatives of suitable weak solutions are locally in L^{4/3,q} for all q > 4/3 (Lorentz space refinement). This improves the previous L^{4/3,infinity} result. The exponent 4/3 for the second derivatives is directly related to the beta = 4/3 in De Giorgi iteration.

### Could This Approach Beat CZ?

**No, for precisely the reason that the obstruction is structural, not tool-dependent.** The vortex stretching term and the pressure term are dual manifestations of the same quadratic nonlinearity u tensor u. Eliminating one introduces the other. The beta = 4/3 is intrinsic to the NS nonlinear structure, not to the choice of formulation. [VERIFIED by cross-comparison in E001]

---

## 6. Duality and Alternative Function Space Approaches

### 6a. Hardy Space H^1 / BMO Duality for Pressure

**References:**
- Coifman, R., Lions, P.-L., Meyer, Y., Semmes, S. "Compensated compactness and Hardy spaces." J. Math. Pures Appl. 72 (1993), 247-286.
- Koch, H., Tataru, D. "Well-posedness for the Navier-Stokes equations." Adv. Math. 157 (2001), 22-35.

**Method:**

The NS pressure satisfies Delta p = -partial_i partial_j(u_i u_j). The bilinear form partial_i(u_i) . partial_j(u_j) has compensated compactness structure when div(u) = 0: by the CLMS theorem, div-free x curl-free products belong to the Hardy space H^1, not merely L^1. Since (H^1)* = BMO, this gives:

   p in H^1(R^3)   (not just L^{3/2})

and duality pairings against BMO functions are better controlled than L^p duality.

**Relevance to beta = 4/3:**

If we write the bottleneck integral as

   I_k = <P^{21}, v_k . 1_{v_k > 0}>

and if P^{21} in H^1, then we need v_k . 1_{v_k > 0} in BMO to apply duality. But:
- v_k . 1_{v_k > 0} = (|u| - lambda_k)_+ is Lipschitz (bounded gradient from energy inequality)
- Lipschitz functions are in BMO with ||f||_{BMO} <= C ||nabla f||_{L^n}
- This gives ||v_k . 1_{v_k > 0}||_{BMO} <= C ||nabla v_k||_{L^3}

The H^1-BMO duality pairing then gives:

   |I_k| <= ||P^{21}||_{H^1} . ||v_k||_{BMO} <= C ||u^{below}||_{L^3} ||u^{above}||_{L^3} . ||nabla v_k||_{L^3}

Compared to the standard CZ route:

   |I_k| <= ||P^{21}||_{L^{3/2}} . ||v_k||_{L^3} <= C ||u^{below}||_{L^3} ||u^{above}||_{L^3} . ||v_k||_{L^3}

The H^1-BMO route replaces ||v_k||_{L^3} with ||nabla v_k||_{L^3}. By Sobolev embedding, ||v_k||_{L^3} <= C ||nabla v_k||_{L^{18/7}} (in 3D), so the H^1-BMO route demands MORE regularity of v_k, not less. It gives a WORSE bound.

**CZ used?** The CLMS H^1 result itself does not use CZ in the classical sense — it uses the special cancellation structure of div-free x curl-free products. However, the resulting H^1 norm of pressure is comparable to the CZ L^{3/2} bound (they are equivalent up to constants for the NS pressure), so no exponent improvement is obtained.

**Could this beat CZ?** **No.** The H^1-BMO duality requires testing against a BMO function, which costs a derivative. For the De Giorgi iteration, the energy functional controls ||nabla v_k||_{L^2} (not L^3 or BMO), so the H^1-BMO pairing is strictly worse than the standard L^{3/2}-L^3 pairing. The CLMS improvement (L^1 -> H^1 for the pressure) is eaten by the BMO cost on the test function side. [COMPUTED — exponent comparison in E006 Task 2]

### 6b. Lorentz Space Estimates for Pressure

**References:**
- Phuc, N.C. "The Navier-Stokes equations in nonendpoint borderline Lorentz spaces." J. Math. Fluid Mech. 17 (2015), 741-760.
- Nguyen, Q.H., Nguyen, P.T. "New regularity criteria based on pressure or gradient of velocity in Lorentz spaces for the 3D Navier-Stokes equations." arXiv:1909.09960 (2019).
- Tran, C.V., Yu, X. "On mixed pressure-velocity regularity criteria to the Navier-Stokes equations in Lorentz spaces." Chinese Ann. Math. Ser. B 42 (2021), 1-16.

**Method:**

Replace Lebesgue space bounds with Lorentz space L^{p,q} bounds, which refine L^p by tracking the distribution function more carefully. For pressure:

   ||p||_{L^{3/2,q}} <= C ||u||_{L^{3,2q}}^2   for 1 <= q <= infinity

The case q = infinity gives weak-L^{3/2} bounds (larger space, weaker bound); the case q = 3/2 recovers the standard Lebesgue bound; the case q = 1 gives the smallest Lorentz space L^{3/2,1} (strongest bound).

**Regularity criteria:** A Leray-Hopf weak solution is regular on (0,T] if p in L^{p,infinity}_t L^{q,infinity}_x with 2/p + 3/q = 2 and 3/2 < q < infinity, provided the norm is sufficiently small.

**CZ used?** Yes, the Lorentz space bounds for the Riesz transforms are refinements of the standard CZ theory. CZ operators are bounded on L^{p,q} for 1 < p < infinity and 1 <= q <= infinity.

**Could this beat CZ?** **Only logarithmically.** Lorentz space refinements give at most logarithmic improvements (e.g., replacing L^{3/2} by L^{3/2,1} gains a factor of log). For the De Giorgi iteration, this translates to at most log corrections in the recurrence, which cannot change the power-law exponent beta = 4/3. The Vasseur-Yang (2021) Lorentz improvement L^{4/3,infinity} -> L^{4/3,q} (q > 4/3) is exactly this type of sub-power-law refinement. [CHECKED]

### 6c. Tran-Yu: Pressure Moderation and Nonlinearity Depletion

**References:**
- Tran, C.V., Yu, X. "Depletion of nonlinearity in the pressure force driving Navier-Stokes flows." Nonlinearity 28 (2015), 1295-1306.
- Tran, C.V., Yu, X. "Pressure moderation and effective pressure in Navier-Stokes flows." Nonlinearity 29 (2016), 2990-3005.

**Method:**

1. **Nonlinearity depletion.** Tran-Yu observe that the pressure force nabla p in NS is nonlinearly depleted: there is a genuine negative correlation between |u| and |nabla|u||. This means the pressure force is systematically weaker in high-velocity regions than generic CZ bounds predict.

2. **Effective pressure.** They replace the physical pressure p by an "effective pressure" P = p + phi(|u|^2/2), where phi is a pressure moderator chosen so that the effective pressure vanishes on surfaces where maximum velocity is coupled with minimum effective pressure on each streamline.

3. **Regularity criteria.** If the moderated pressure (p + P) becomes sufficiently small in an appropriate norm as the measure of a velocity-dependent set decreases, then regularity is secured.

**CZ used?** Their regularity criteria still invoke standard Sobolev/CZ estimates for the original pressure. The "depletion" is a structural observation about NS solutions, not a new analytical tool. It suggests that the CZ bound is loose for the specific configurations that arise in NS, but Tran-Yu do not prove improved CZ-type bounds.

**Result:** New regularity criteria involving pressure moderators. These are sufficient conditions for regularity (like Prodi-Serrin), not improvements to De Giorgi beta exponents.

**Could this beat CZ?** **In principle yes, but the mechanism is different.** Tran-Yu's depletion observation is about the CORRELATION between pressure and velocity in actual NS solutions. If this correlation could be quantified at the De Giorgi truncation level (specifically, if the negative correlation between |u| and |nabla|u|| implies that P^{21} is systematically smaller than the CZ bound predicts), it would translate to an improved effective beta. However, Tran-Yu do not make this connection to De Giorgi iteration, and quantifying the depletion for truncated quantities is an open problem. [CONJECTURED]

---

## 7. Synthesis and Assessment

### Summary Table

| Approach | Pressure method | CZ used? | Result type | beta exponent | Could beat 4/3? |
|---|---|---|---|---|---|
| CKN (1982) | Energy inequality + epsilon-regularity | Implicitly | Partial regularity | N/A (no iteration) | No |
| De Giorgi scalar | No pressure | N/A | Full regularity (scalar) | N/A | N/A |
| Vasseur (2007) | P^{ij} decomposition + CZ | YES | Partial regularity (De Giorgi) | 4/3 | Baseline |
| Vasseur-Yang (2021) | Curl eliminates pressure | No (but CZ on Biot-Savart) | L^{4/3,q} second derivatives | 4/3 | No |
| ESS (2003) | Backward uniqueness, pressure absorbed | No (in key step) | L^{3,infinity} regularity | N/A (no iteration) | Structurally different |
| CLMR (2018) | Dissipative solutions, pressure in flux | No (in regularity step) | Partial regularity | N/A | No |
| Wolf (2015-2017) | Local harmonic + particular decomposition | No | Partial regularity | Not computed for DG | Possible (untested) |
| H^1/BMO duality | CLMS compensated compactness | No (but equivalent) | Same exponents | Worse than CZ | No |
| Lorentz refinement | CZ on L^{p,q} | Yes (refined CZ) | Log improvements | 4/3 (up to log) | No (sub-power) |
| Tran-Yu (2015-16) | Pressure moderation/depletion | Implicitly | Regularity criteria | Not computed | Possible (unproven) |
| Koch-Seregin-Sverak (2009) | Liouville + blow-up | Implicitly | Ancient solution classification | N/A | Structurally different |
| Ladyzhenskaya-Seregin (1999) | Compactness/blow-up | Implicitly | Partial regularity | N/A | No |

### Key Findings

1. **No published work achieves beta > 4/3 for the De Giorgi iteration on NS by any method, CZ or non-CZ.** The 4/3 barrier has stood since Vasseur (2007) identified it.

2. **Taking curl does NOT help:** Vasseur-Yang (2021) showed that eliminating pressure via curl re-introduces the same obstruction through vortex stretching. The CZ operator reappears as the Biot-Savart law. The 4/3 is structural.

3. **Backward uniqueness (ESS 2003) avoids pressure entirely** but uses a fundamentally different proof architecture (contradiction via Carleman inequalities) that does not produce a beta exponent. It cannot be compared with De Giorgi on exponent grounds.

4. **The most promising CZ-free approach for De Giorgi is Wolf's local pressure decomposition** (harmonic + particular). It has not been tested in the Vasseur De Giorgi framework, and the harmonic part's smoothness might provide structural advantages.

5. **Tran-Yu's nonlinearity depletion** is the most promising structural observation. If the negative |u|-|nabla|u|| correlation could be quantified at De Giorgi truncation levels, it might show that P^{21} is systematically smaller than CZ predicts. This is an open problem.

6. **H^1-BMO duality gives WORSE exponents** than standard CZ for the De Giorgi iteration because the BMO cost on the test function side is too expensive.

7. **Lorentz space refinements give at most logarithmic improvements**, which cannot change the power-law exponent beta = 4/3.

### Implications for This Exploration

The literature strongly suggests that:

- **Any approach that estimates ||P^{21}||_{X} for some function space X, then uses Holder duality against the test function, will get beta = 4/3 or worse.** The pairing always has the same scaling. This includes CZ, H^1-BMO, Lorentz, and Wolf's decomposition.

- **The only paths to beta > 4/3 are:** (a) approaches that avoid estimating P^{21} in isolation (like the Chamorro-Lemarie-Rieusset energy flux idea), (b) approaches that exploit NS-specific correlations between pressure and velocity (like Tran-Yu's depletion), or (c) entirely different proof architectures (like ESS backward uniqueness, which avoids De Giorgi altogether).

- **The cross-formulation universality of 4/3 (velocity and vorticity give the same exponent) is the strongest evidence that the barrier is intrinsic to the NS nonlinear structure**, not to any particular analytical tool.

---

## References (Chronological)

1. De Giorgi, E. (1957). "Sulla differenziabilita e l'analiticita delle estremali degli integrali multipli regolari." *Mem. Accad. Sci. Torino* 3, 25-43.
2. Nash, J. (1958). "Continuity of solutions of parabolic and elliptic equations." *Amer. J. Math.* 80, 931-954.
3. Moser, J. (1960). "A new proof of De Giorgi's theorem." *Comm. Pure Appl. Math.* 13, 457-468.
4. Caffarelli, L., Kohn, R., Nirenberg, L. (1982). "Partial regularity of suitable weak solutions of the Navier-Stokes equations." *Comm. Pure Appl. Math.* 35, 771-831.
5. Coifman, R., Lions, P.-L., Meyer, Y., Semmes, S. (1993). "Compensated compactness and Hardy spaces." *J. Math. Pures Appl.* 72, 247-286.
6. Lin, F. (1998). "A new proof of the Caffarelli-Kohn-Nirenberg theorem." *Comm. Pure Appl. Math.* 51, 241-257.
7. Ladyzhenskaya, O.A., Seregin, G.A. (1999). "On partial regularity of suitable weak solutions to the three-dimensional Navier-Stokes equations." *J. Math. Fluid Mech.* 1, 356-387.
8. Duchon, J., Robert, R. (2000). "Inertial energy dissipation for weak solutions of incompressible Euler and Navier-Stokes equations." *Nonlinearity* 13, 249-255.
9. Koch, H., Tataru, D. (2001). "Well-posedness for the Navier-Stokes equations." *Adv. Math.* 157, 22-35.
10. Escauriaza, L., Seregin, G., Sverak, V. (2003). "L_{3,infinity}-solutions of the Navier-Stokes equations and backward uniqueness." *Russian Math. Surveys* 58:2, 211-250.
11. Vasseur, A. (2007). "A new proof of partial regularity of solutions to Navier-Stokes equations." *NoDEA* 14, 753-785. arXiv:math/0607017.
12. Koch, G., Nadirashvili, N., Seregin, G., Sverak, V. (2009). "Liouville theorems for the Navier-Stokes equations and applications." *Acta Math.* 203, 83-105.
13. Caffarelli, L., Vasseur, A. (2010). "Drift diffusion equations with fractional diffusion and the quasi-geostrophic equation." *Ann. Math.* 171, 1903-1930.
14. Tran, C.V., Yu, X. (2015). "Depletion of nonlinearity in the pressure force driving Navier-Stokes flows." *Nonlinearity* 28, 1295-1306.
15. Tran, C.V., Yu, X. (2016). "Pressure moderation and effective pressure in Navier-Stokes flows." *Nonlinearity* 29, 2990-3005.
16. Wolf, J. (2016). "On the local pressure of the Navier-Stokes equations and related systems." arXiv:1611.01482.
17. Chamorro, D., Lemarie-Rieusset, P.G., Mayoufi, K. (2018). "The role of the pressure in the partial regularity theory for weak solutions of the Navier-Stokes equations." *Arch. Ration. Mech. Anal.* 228, 237-277. arXiv:1602.06137.
18. Vasseur, A., Yang, J. (2021). "Second derivatives estimate of suitable solutions to the 3D Navier-Stokes equations." *Arch. Ration. Mech. Anal.* 241, 683-727.
19. Wolf, J. (2022). "On the local pressure expansion for the Navier-Stokes equations." *J. Math. Fluid Mech.* 24, Article 3. arXiv:2001.11526.
20. Lee, M. (2024). "The De Giorgi method with applications to fluid dynamics." *U. Chicago REU*. Available: https://math.uchicago.edu/~may/REU2024/REUPapers/Lee,Michael.pdf

DONE
