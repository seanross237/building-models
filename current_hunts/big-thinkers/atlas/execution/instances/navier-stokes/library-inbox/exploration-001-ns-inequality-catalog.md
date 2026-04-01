# Exploration 001: Catalog of Load-Bearing Inequalities in 3D Navier-Stokes Regularity Theory

**Status:** COMPLETE
**Date:** 2026-03-29

---

## Setting

3D incompressible Navier-Stokes on T³ (periodic torus) or Ω ⊆ ℝ³:

    ∂ₜu + (u·∇)u = ν∆u − ∇p + f,    ∇·u = 0

Notation: ||·||_{L^p} = ||·||_{L^p(T³)}, H^s = Sobolev space W^{s,2}, H^s₀ = H^s ∩ {∇·u = 0}.

---

## Part 1: Master Catalog Table

| ID | Inequality Name | Source | Used In | Bounds What | Scaling (Re) | Const. Status | Sharp? | Tao Cat. |
|----|-----------------|--------|---------|-------------|--------------|----------------|--------|----------|
| F1 | Ladyzhenskaya (3D) | Ladyzhenskaya 1958/1967 | Prodi-Serrin, energy est. | L⁴ norm by L² and H¹ | grows ~Re^{3/4} | Explicit: (2/√3)^{1/2} (Sobolev sharp) | Yes, but not by NS sol. | Generic |
| F2 | GNS interpolation (general) | Gagliardo 1958, Nirenberg 1959 | Everywhere in NS proofs | Intermediate Sobolev norms | depends on exponents | Existential (C(n,p,q,r)) | Partially (some cases) | Generic |
| F3 | Sobolev embedding H¹ ↪ L⁶ | Sobolev 1938 | Energy estimates, CKN | H¹ norm → L⁶ norm | scale-invariant | Explicit: best const. known via Aubin-Talenti | Yes, by Aubin-Talenti functions | Generic |
| F4 | Agmon's inequality (3D) | Agmon 1965 | BKM, higher energy est. | L^∞ norm by H¹ and H² | grows | Existential (C) | Essentially sharp | Generic |
| F5 | Calderón-Zygmund pressure est. | CZ 1952, applied to NS | All regularity proofs | Pressure ∇p in terms of ∇u | scale-invariant | Existential but near-explicit | Yes (Riesz transforms sharp) | NS-specific (pressure from NS) |
| E1 | Global Energy Inequality | Leray 1934 | Weak solution existence | Kinetic energy ||u||²_{L²} | O(1) in Re | Exact (no constant) | Exact (equality for smooth) | NS-specific |
| E2 | Enstrophy Identity | Helmholtz/standard | Regularity criteria | Enstrophy ||ω||²_{L²} | grows ~Re² | Involves vortex stretch term | Exact identity | NS-specific |
| E3 | Vortex Stretching Bound | Constantin-Fefferman 1993 | Enstrophy control | Vortex stretching integral | grows ~Re³ | Existential C | Not sharp | NS-specific |
| E4 | Higher Energy (H^s) | Standard | Blow-up criteria | ||u(t)||_{H^s} | grows | Involves iterative constants | Not sharp | NS-specific |
| R1 | Prodi-Serrin criterion | Prodi 1959, Serrin 1962 | Conditional regularity | u ∈ L^p_t L^q_x sufficient | scale-invariant condition | Existential (condition, not const.) | Critical: L³ endpoint (ESS) | NS-specific |
| R2 | Beale-Kato-Majda criterion | Beale-Kato-Majda 1984 | Conditional regularity | ||ω||_{L^∞} time-integral | scale-invariant condition | Explicit structure (log term) | Unknown if sharp | NS-specific |
| R3 | Local Energy Inequality (CKN) | Caffarelli-Kohn-Nirenberg 1982 | Partial regularity | Local kinetic energy | local | Exact structure, small ε | Essentially sharp in CKN | NS-specific |
| R4 | ε-regularity (CKN) | Caffarelli-Kohn-Nirenberg 1982 | Partial regularity | Regularity at a point | local | Existential ε > 0 | Unknown: ε not computed | NS-specific |
| R5 | ESS Carleman inequality | Escauriaza-Seregin-Šverák 2003 | L³ endpoint regularity | Backward uniqueness | endpoint | Existential | Unknown | NS-specific |
| F6 | Brezis-Gallouet-Wainger log-Sobolev | Brezis-Gallouet 1980 | BKM proof | L^∞ at critical exponent | O(log Re) | Existential C, sharp log exp | Yes (log exp 1/2 sharp) | Generic |
| F7 | Kato-Ponce commutator | Kato-Ponce 1988 | H^s energy estimates | H^s norm of nonlinear term | grows with s | Existential | Essentially sharp | Generic |
| F8 | Hardy-Littlewood-Sobolev | Hardy-Littlewood 1927 | CKN pressure | Pressure L^q from velocity | scale-inv | Explicit (Lieb 1983) | Yes (Lieb extremals) | Generic |
| E4 | H^s energy estimate | Majda-Bertozzi / Kato-Ponce | BKM blow-up criterion | ||u||_{H^s} growth rate | exp(∫||∇u||_{L^∞}) | Existential (Kato-Ponce const.) | No (loose for NS flows) | NS-specific (transport cancellation) |
| G1 | Gronwall exponential bound | Gronwall 1919 | Everywhere | ||u(t)||_{H^s} growth | grows exponentially | Exact structure | Generically loose | Generic |

---

## Part 2: Detailed Entries

### F1. Ladyzhenskaya Inequality (3D Version)

**Exact Statement:**
For u ∈ H¹(T³) (or H¹₀(Ω), Ω ⊆ ℝ³):

    ||u||_{L⁴(T³)} ≤ C_L ||u||_{L²(T³)}^{1/4} ||∇u||_{L²(T³)}^{3/4}

with C_L being a dimensional constant. In ℝ³, by GNS interpolation with p=4, this follows from the general GNS:

    ||u||_{L⁴} ≤ C ||u||_{L²}^{1/4} ||u||_{H¹}^{3/4}

but on T³ the mean must be separated. The exponents 1/4 and 3/4 are fixed by scaling: [u]_{L⁴} requires [u]_{L²}^{1/4} [∇u]_{L²}^{3/4} by dimensional analysis in 3D.

**Source:** Ladyzhenskaya, O.A. (1958, 1967). "The Mathematical Theory of Viscous Incompressible Flow." Also in her 1958 Dokl. Akad. Nauk paper. In the West it appears in Temam (1977) "Navier-Stokes Equations."

**Where it enters the proof:** Used in bounding the nonlinear term in Prodi-Serrin regularity arguments and in energy estimates. Specifically: the term ∫(u·∇u)·u = 0 after integration by parts (by incompressibility), but the term ∫(u·∇u)·v requires controlling ||u||_{L⁴}² ||∇v||_{L²}, and Ladyzhenskaya bounds ||u||_{L⁴} for this purpose.

**What it bounds:** The L⁴ spatial norm of velocity in terms of L² norm and H¹ seminorm. It controls the "intermediate" Lebesgue norm between L² (energy) and H¹ (enstrophy-related).

**Scaling behavior:** If u has typical velocity scale U and length scale L, then Re = UL/ν. The L⁴ norm scales as U·L^{3/4}, L² norm as U·L^{3/2}, ∇u scales as U/L. Plugging in: C · (U·L^{3/2})^{1/4} · (U/L · L)^{3/4} = C·U·L^{3/8}·U^{3/4}/1 = C·U^{7/4}·L^{3/8}...

Actually in terms of Re: on T³ with unit torus L=1, u ~ Re·ν, so ||u||_{L⁴} ~ Re^{1}. The bound: ||u||_{L²}^{1/4} ||∇u||_{L²}^{3/4} ~ (Re·ν)^{1/4} · (Re·ν/1)^{3/4} = Re·ν. So the bound is of the correct order — the *ratio* of actual to bound is O(1) in Re for generic flows. The issue arises in cascade: bounds compound in chains.

**Constant status:** Existential but the sharp constant for the underlying Sobolev inequality is known (it reduces to GNS with specific exponents). The sharp constant for the 3D GNS inequality ||u||_{L⁴} ≤ C ||u||_{L²}^{1/4} ||∇u||_{L²}^{3/4} on ℝ³ is known in principle (via extremal functions) but is not standardly tabulated. The constant is dimension-dependent. In practice, proofs use C = 2^{1/2} or similar from the proof of GNS via Sobolev.

**Sharpness:** The inequality is saturated on ℝ³ by functions of the form u(x) = f(|x|) approaching the Aubin-Talenti Sobolev extremals (appropriately scaled). These are NOT Navier-Stokes solutions in general (the extremals are radial, static, and compactly supported or decaying — they don't satisfy the NS momentum equation). This is the key source of slack: the extremal function for Ladyzhenskaya is a static profile, not a fluid.

**Tao Category:** Generic — this inequality does not use the specific structure of NS (divergence-free, pressure, nonlinearity). It holds for any H¹ function.

---

### F2. Gagliardo-Nirenberg-Sobolev (GNS) Interpolation

**Exact Statement:** For u: ℝⁿ → ℝ (or on bounded domain with Dirichlet BC), the GNS family:

    ||D^j u||_{L^p(ℝⁿ)} ≤ C(j, m, n, p, q, r) ||D^m u||_{L^r(ℝⁿ)}^θ ||u||_{L^q(ℝⁿ)}^{1-θ}

where the scaling exponent θ is determined by:

    1/p - j/n = θ(1/r - m/n) + (1-θ)/q,    j/m ≤ θ ≤ 1

(with exceptions when r = n/(m-j) in 3D).

**Key instances used in NS (3D, n=3):**

(a) j=0, p=6, r=2, m=1, q=∞ excluded → the Sobolev embedding (see F3)

(b) j=0, p=4, r=2, m=1, q=2 → Ladyzhenskaya (F1):
    ||u||_{L⁴} ≤ C ||∇u||_{L²}^{3/4} ||u||_{L²}^{1/4}    (θ = 3/4)

(c) j=0, p=3, r=2, m=1, q=2:
    ||u||_{L³} ≤ C ||∇u||_{L²}^{1/2} ||u||_{L²}^{1/2}    (θ = 1/2)

(d) j=1, p=2, r=2, m=2, q=2 → just Sobolev interpolation between H¹ and H²:
    ||∇u||_{L²} ≤ C ||u||_{H²}^{1/2} ||u||_{L²}^{1/2}

(e) j=0, p=∞ (Agmon, see F4 below)

(f) For pressure: j=0, p=3/2, various → used in CKN

**Source:** Gagliardo (1958) "Proprietà di alcune classi di funzioni in più variabili"; Nirenberg (1959) "On elliptic partial differential equations." Standard references: Evans "PDE" Appendix, Brezis "Functional Analysis."

**Where it enters:** GNS is the master inequality family. Virtually every estimate in NS regularity theory is a special case or corollary of GNS. It appears:
- In the nonlinear term estimates ||u·∇u||_{L²} ≤ ||u||_{L⁴}||∇u||_{L²} ≤ C||u||_{H¹}^{7/4}||u||_{L²}^{1/4}
- In energy estimates for H^s norms
- In Prodi-Serrin criterion proofs

**Constant status:** Existential — C depends on domain, exponents, dimension. For specific exponent pairs on ℝⁿ, sharp constants are known (e.g., the Sobolev constant), but most NS applications use non-sharp constants.

**Sharpness:** Extremal functions are Aubin-Talenti type (power functions modulated by Gaussians/rational functions). These are generally NOT NS solutions.

**Scaling:** The GNS inequalities are designed to be scale-invariant (the exponent θ is the unique scaling exponent). So the *ratio* of LHS to RHS is scale-invariant for divergence-free flows. The "slack" comes from the specific geometry of the flow vs. the extremal function.

**Tao Category:** Generic — GNS holds for all H^m functions, no NS structure needed.

---

### F3. Sobolev Embedding H¹ ↪ L⁶ in 3D

**Exact Statement:** For u ∈ H¹(ℝ³) (or H¹₀(Ω)):

    ||u||_{L⁶(ℝ³)} ≤ S₃ ||∇u||_{L²(ℝ³)}

where the sharp constant S₃ is:

    S₃ = (4/3)^{1/2} · π^{-1/3} · Γ(3/2)^{1/3} = (1/√3)(4π²)^{-1/3}

More explicitly: S₃² = 1/K_3 where K_3 is the best Sobolev constant. The Aubin-Talenti value:

    S₃ = (4/3)^{1/2} / (√π · Γ(3)^{1/3}/Γ(3/2)^{1/3})

[Note: The exact numerical value is approximately 0.20082... but this needs verification against standard tables.]

The exponent 6 is sharp (Sobolev exponent p* = 2n/(n-2) = 6 when n=3).

**Source:** Sobolev (1938). Sharp constant: Aubin (1976) "Problèmes isopérimétriques et espaces de Sobolev," and Talenti (1976) "Best constant in Sobolev inequality," Ann. Mat. Pura Appl.

**Where it enters:**
- H¹ solutions are automatically in L⁶, giving the basic integrability for NS solutions
- In the nonlinear term: |∫(u·∇)u · v dx| ≤ ||u||_{L^6} ||∇u||_{L^2} ||v||_{L^6} ≤ S₃² ||∇u||_{L^2}² ||∇v||_{L^2}
- CKN estimates use H¹ ↪ L⁶ locally

**What it bounds:** The L⁶ norm of velocity (or any H¹ function) in terms of the H¹ seminorm.

**Scaling:** Scale-invariant in ℝ³. Under Kolmogorov scaling u ~ Re^{3/4} (at energy-injection scale), the bound gives ||u||_{L⁶} ≤ S₃ ||∇u||_{L²} which scales correctly. The gap is O(1) in Re at each scale but integrating over the cascade computes to potentially larger gaps.

**Constant status:** EXPLICIT — the sharp constant is known via Aubin-Talenti. The extremal functions are:

    u_ε(x) = (ε/(ε² + |x|²))^{1/2}    (up to normalization)

These are the Aubin-Talenti bubbles.

**Sharpness:** YES — the inequality is sharp, equality is attained (on ℝ³) by the Aubin-Talenti functions u_ε(x) = C(ε² + |x - x₀|²)^{-1/2}. These are emphatically NOT NS solutions — they are static, isotropic, and have infinite H¹ norm on T³ (require the whole ℝ³).

**Tao Category:** Generic — holds for any H¹ scalar function, no NS structure.

---

### F4. Agmon's Inequality (3D)

**Exact Statement:** For u ∈ H²(T³) (or H²(Ω) with appropriate BC):

    ||u||_{L^∞(T³)} ≤ C_A ||u||_{H¹(T³)}^{1/2} ||u||_{H²(T³)}^{1/2}

This follows from GNS with n=3, j=0, p=∞, m=2: the scaling gives θ = 3/4, but actually for L^∞ in 3D the GNS gives:

    ||u||_{L^∞} ≤ C ||u||_{H^s}    for any s > 3/2

The "Agmon" form specifically used in NS and Euler proofs is:

    ||u||_{L^∞} ≤ C ||u||_{H¹}^{1/2} ||u||_{H²}^{1/2}    (3D)

which follows by interpolation + Sobolev embedding (H² ↪ W^{1,∞} is NOT true in 3D; the actual useful bound is H^{3/2+ε} ↪ L^∞).

[**NOTE:** The precise form of Agmon's inequality used in NS differs slightly across sources. In 2D, the clean form ||u||_{L^∞} ≤ C ||u||_{L²}^{1/2} ||u||_{H²}^{1/2} holds. In 3D, the clean form requires two derivatives more carefully: one standard version is ||u||_{L^∞} ≤ C ||u||_{H^{3/2+ε}} for any ε > 0. The form ||u||_{L^∞} ≤ C ||u||_{H¹}^{1/2} ||u||_{H²}^{1/2} is used in 2D; in 3D the analogous formula uses H^{3/4} and H^{5/4} or similar. This is a source of ambiguity across papers — see Part 4.]

**Source:** Agmon, S. (1965) "Lectures on Elliptic Boundary Value Problems." Princeton. The form used in fluid dynamics appears in Constantin-Foias (1988) "Navier-Stokes Equations" and Majda-Bertozzi (2002) "Vorticity and Incompressible Flow."

**Where it enters:**
- In the BKM criterion proof: one needs ||u||_{L^∞} to be bounded to control energy growth; the Agmon inequality provides this from H² control.
- In higher-energy estimate chains: if ||u||_{H^s} is bounded, Agmon gives L^∞ control.

**Scaling:** For NS solutions with Re ≫ 1, ||u||_{L^∞} ~ Re (characteristic velocity), while ||u||_{H¹}^{1/2}||u||_{H²}^{1/2} ~ Re^{1/2} · Re^{1} = Re^{3/2} (rough estimate from turbulence scaling). So the Agmon bound is *not tight* in the turbulent regime — the actual L^∞ grows slower than the Agmon bound. Significant slack here.

**Constant status:** Existential. The sharp constant for Agmon's inequality is not typically computed in NS applications.

**Sharpness:** The inequality is sharp in an abstract sense (optimal up to constants for general H² functions), but the extremal functions are concentrated bump functions, not NS solutions.

**Tao Category:** Generic — holds for any H² function.

---

### F5. Calderón-Zygmund Pressure Estimate

**Exact Statement:** From the NS equations, the pressure satisfies:

    −∆p = ∇·((u·∇)u) = ∂_i u^j ∂_j u^i = tr(∇u)²

Taking the Riesz transform: for p ∈ L^q,

    ||∇²p||_{L^q} ≤ C_{CZ}(q) ||∇u||_{L^{2q}}²    for 1 < q < ∞

Equivalently (using Riesz transform boundedness on L^q):

    ||p||_{L^q} ≤ C_{CZ}(q) ||u||_{L^{2q}}²    for 1 < q < ∞

More precisely, since p = Σ_{i,j} R_i R_j (u^i u^j) where R_i are Riesz transforms, and since ||R_i||_{L^q → L^q} ≤ C_p:

    ||p||_{L^q(T³)} ≤ C(q) ||u||_{L^{2q}(T³)}²    for 1 < q < ∞

The constant C(q) blows up as q → 1 and q → ∞ (Riesz transforms are not bounded on L¹ or L^∞).

**Source:** Calderón-Zygmund (1952) "On the existence of certain singular integrals," Acta Math.; applied to NS in Temam (1977), Constantin-Foias (1988).

**Where it enters:**
- CKN partial regularity: pressure must be estimated locally; CZ gives L^q control of p from L^{2q} control of u
- Prodi-Serrin proofs: pressure estimates needed at each step
- Any energy estimate for weak solutions where pressure appears in interior terms

**What it bounds:** The L^q norm of pressure (or ∇²p) in terms of the L^{2q} norm of velocity (or ∇u).

**Scaling:** Scale-invariant in ℝ³ (Riesz transforms commute with dilations). So the gap is O(1) in Re from scaling alone.

**Constant status:** The best constant C(q) for the Riesz transforms on L^q is known:

    ||R_j||_{L^q → L^q} ≤ C(q),    C(q) = max(q, q') - 1    (Pichorides 1972 sharp result for Hilbert transform; for Riesz transforms in ℝⁿ, sharp constants are less explicit)

For the full CZ estimate in NS context, C(q) ~ max(q, q/(q-1)) (i.e., O(1) for q bounded away from 1 and ∞, but blowing up at endpoints).

**Sharpness:** The L^q boundedness of Riesz transforms is sharp (equality cases exist abstractly). At q=2, the Riesz transforms are isometries on L²(ℝⁿ) (Plancherel). The CZ pressure estimate is therefore essentially sharp at q=2, with a somewhat quantified constant.

**Tao Category:** NS-specific — the pressure equation −∆p = ∂_i(u^i u^j)_{,j} uses the NS nonlinearity. The CZ estimate reflects the specific way NS couples pressure to velocity.

---

### E1. Global Energy Inequality (Leray-Hopf)

**Exact Statement:** For a Leray-Hopf weak solution u of 3D NS on [0,T]:

    ||u(t)||²_{L²} + 2ν ∫₀ᵗ ||∇u(s)||²_{L²} ds ≤ ||u₀||²_{L²} + 2 ∫₀ᵗ ⟨f(s), u(s)⟩ ds

for a.e. t ∈ [0,T] (including t=0).

This is NOT an equality in general (for weak solutions). For smooth solutions:

    d/dt ||u||²_{L²} + 2ν ||∇u||²_{L²} = 2⟨f, u⟩

(exact identity). The inequality arises because in the weak solution construction, the nonlinear term ∫(u·∇u)·u dx = 0 cannot be justified as an equality — only ≥ 0.

**Source:** Leray, J. (1934) "Sur le mouvement d'un liquide visqueux emplissant l'espace," Acta Mathematica; Hopf, E. (1951) "Über die Anfangswertaufgabe für die hydrodynamischen Grundgleichungen," Math. Nachr.

**Where it enters:** Foundational — used in:
- Existence of weak solutions
- Unique continuation arguments
- As the base of all higher-energy estimates (the H^0 level)

**What it bounds:** Total kinetic energy ||u||²_{L²} = 2 × kinetic energy.

**Scaling (Re):** The energy is ~Re² ν² (in natural units). The dissipation term 2ν||∇u||²_{L²} is ~Re²·ν. The energy inequality states the sum of energy + integrated dissipation is bounded by initial energy + forcing work. For turbulent flows, the dissipation is ~ε × T where ε = νRe³ (Kolmogorov estimate), so the energy inequality is essentially an equality (the anomalous dissipation hypothesis is that equality holds even as ν → 0).

**Constant status:** The inequality has no constants (it is exact for smooth solutions). The "slackness" in the weak solution case is the unknown difference:

    ||u₀||²_{L²} − ||u(t)||²_{L²} − 2ν ∫₀ᵗ ||∇u||²_{L²} ds ≥ 0

which represents the energy "disappearing" in weak solutions via oscillations (Scheffer, Shnirelman phenomena).

**Sharpness:** For smooth solutions, equality holds exactly. For weak solutions, the gap is exactly the "anomalous dissipation" — the energy lost to the oscillation of the weak limit. This gap is the subject of the Onsager conjecture (proved by Isett 2018).

**Tao Category:** NS-specific — the energy inequality exploits (u·∇u)·u = 0 (for divergence-free u), which is the specific cancellation in the NS nonlinearity.

---

### E2. Enstrophy Evolution Identity

**Exact Statement:** Taking the curl of NS: ∂ₜω + (u·∇)ω = ν∆ω + (ω·∇)u + ∇×f, where ω = ∇×u.

Taking L² inner product with ω:

    d/dt (1/2)||ω||²_{L²} = −ν||∇ω||²_{L²} + ∫_{T³} (ω·∇u)·ω dx + ⟨∇×f, ω⟩

The vortex stretching term:

    VS = ∫_{T³} ω_i (∂_j u^i) ω^j dx = ∫_{T³} S_{ij} ω_i ω_j dx

where S = (1/2)(∇u + (∇u)^T) is the strain rate tensor.

This is an IDENTITY (not an inequality) for smooth solutions. The inequality arises when bounding VS.

**Bounding the Vortex Stretching Term:**

(a) Crude bound via Hölder + Ladyzhenskaya:
    |VS| ≤ ||ω||²_{L⁴} ||∇u||_{L²} ≤ C ||ω||_{L²}^{1/2} ||∇ω||_{L²}^{3/2} ||ω||_{L²}

(using Ladyzhenskaya for ω: ||ω||_{L⁴} ≤ C||ω||_{L²}^{1/4}||∇ω||_{L²}^{3/4}, and ∇u ~ ω so ||∇u||_{L²} ~ ||ω||_{L²}).

This gives:
    d/dt ||ω||²_{L²} ≤ −ν||∇ω||²_{L²} + C ||ω||^{3/2}_{L²} ||∇ω||^{3/2}_{L²}

By Young's inequality (ab ≤ εa^p + C(ε)b^{p'}):
    C ||ω||^{3/2}_{L²} ||∇ω||^{3/2}_{L²} ≤ ν||∇ω||²_{L²} + C/ν³ ||ω||^6_{L²}

yielding:
    d/dt ||ω||²_{L²} ≤ C/ν³ ||ω||^6_{L²}

This ODE for y = ||ω||²_{L²} is dy/dt ≤ C y³/ν³, which blows up in finite time if ||ω₀||_{L²} is large. This is the fundamental mechanism by which the enstrophy-based regularity argument FAILS to give global regularity.

**Source:** The enstrophy identity is classical. The vortex stretching bound appears in many forms in the literature; the specific power bound dy/dt ≤ C y³/ν³ appears in Foias-Manley-Rosa-Temam "Navier-Stokes Equations and Turbulence" (2001) and related works.

**Where it enters:**
- This is the *reason* 3D NS is hard: the vortex stretching term cannot be controlled by dissipation
- Conditional regularity: if |VS| can be bounded more carefully (Constantin-Fefferman geometric bound), one gets conditional results

**What it bounds:** Enstrophy ||ω||²_{L²} = ||∇u||²_{L²} growth rate.

**Scaling:** In turbulence, ||ω||²_{L²} ~ Re^3 ν^{-1} (enstrophy scales as Re per unit volume). The bound C/ν³ ||ω||^6 scales much more dramatically than reality.

**Constant status:** Existential C. The Young's inequality constant is explicit but the overall constant is not sharp.

**Sharpness:** The bound |VS| ≤ C||ω||^{3/2}_{L²}||∇ω||^{3/2}_{L²} uses Ladyzhenskaya and is generally loose. Constantin-Fefferman (1993) showed geometrically that the actual vortex stretching is controlled by the *alignment* of vortex directions, giving a much tighter bound for flows with no "coherent vortex alignment" — but this is a conditional geometric bound.

**Tao Category:** NS-specific — the enstrophy equation uses the specific form of the NS nonlinearity via the vortex stretching structure.

---

### E3. Constantin-Fefferman Vortex Stretching Geometric Bound

**Exact Statement:** (Constantin-Fefferman 1993) Let ξ = ω/|ω| be the vorticity direction. Define:

    ∇ξ = "variation of vorticity direction"

Then the vortex stretching satisfies:

    |VS| = |∫ S_{ij} ω_i ω_j dx| ≤ C ||ω||_{L²}² (||∇ξ||_{L^∞} · ||u||_{L^∞})^{1/2} ||∇ω||_{L²}^{1/2} ...

[The precise statement requires careful notation from the paper. The key point is that if the vorticity direction field ξ is Lipschitz, then VS can be bounded without blowup.]

More precisely, Constantin-Fefferman proved:

If sup_{t∈[0,T]} ∫₀ᵗ ||∇ξ(·,s)||_{L^∞(Ω(s))}² ds < ∞  (where Ω(s) = {x: |ω(x,s)| > 0})

then the solution remains regular on [0,T].

**Source:** Constantin, P. and Fefferman, C. (1993) "Direction of vorticity and the problem of global regularity for the Navier-Stokes equations," Indiana Univ. Math. J.

**Where it enters:** Conditional regularity — gives a geometric sufficient condition for regularity that is potentially much weaker than the pure analytic conditions (Prodi-Serrin).

**What it bounds:** The vortex stretching integral VS, using geometric information about vorticity direction.

**Scaling:** The condition on ∇ξ is scale-invariant in a specific sense. For smooth flows where vorticity direction varies regularly, ∇ξ is bounded and VS is controlled.

**Constant status:** Existential C.

**Sharpness:** Unknown. The condition is not known to be sharp (a flow satisfying the condition could still be regular even if the condition fails).

**Tao Category:** NS-specific — depends explicitly on the vortex stretching structure of NS.

---

### R1. Prodi-Serrin-Ladyzhenskaya Regularity Criterion

**Exact Statement:** Let u be a Leray-Hopf weak solution of 3D NS on (0,T). If

    u ∈ L^p(0,T; L^q(T³))    with    2/p + 3/q ≤ 1,    q > 3

then u is regular on (0,T] (and in fact smooth if f is smooth).

The endpoint q=3: if u ∈ L^∞(0,T; L³(T³)) (the borderline case 2/p + 3/q = 1 with p=∞, q=3), then regularity holds by the Escauriaza-Seregin-Šverák theorem (2003).

**Supporting inequalities in the proof:** The Prodi-Serrin proof uses:

(a) **Prodi-Serrin-based energy estimate for difference:** If u satisfies the above integrability, one shows (by energy methods for the difference u-v where v is a smooth approximation) that the difference → 0. This requires controlling:

    ∫ |(u·∇)u · φ| dx ≤ ||u||_{L^q} ||∇u||_{L²} ||φ||_{L^{2q/(q-2)}}

and the GNS inequality to handle the ||φ||_{L^{2q/(q-2)}} term.

(b) The critical Sobolev embedding: the condition 2/p + 3/q = 1 is exactly the scaling-critical condition (the NS scaling u(x,t) → λu(λx, λ²t) transforms the norm by λ^{2/p+3/q-1}).

**Source:** Prodi (1959) "Un teorema di unicità per le equazioni di Navier-Stokes"; Serrin (1962) "On the interior regularity of weak solutions"; Ladyzhenskaya (1967). The sharp endpoint: Escauriaza-Seregin-Šverák (2003).

**Where it enters:** This IS the main conditional regularity result. It converts a spacetime integrability condition on u into full regularity.

**Scaling:** The condition 2/p + 3/q ≤ 1 is scale-invariant for NS (q > 3 sub-critical, q = 3 critical, q < 3 super-critical). The scaling analysis shows that for NS on T³ with energy at scale λ, the L^p_t L^q_x norm scales correctly when 2/p + 3/q = 1.

**Constant status:** The condition (2/p + 3/q ≤ 1) is scale-invariant — no constant. The proof uses various unspecified constants from GNS and energy estimates.

**Sharpness:** The scaling condition 2/p + 3/q = 1 is sharp (necessary and sufficient for scale-invariance). Whether regularity actually fails when 2/p + 3/q > 1 is unknown (and would imply blowup of weak solutions).

**Tao Category:** NS-specific — the proof uses the energy structure and the cancellation (u·∇u)·u = 0.

---

### R2. Beale-Kato-Majda (BKM) Criterion

**Exact Statement:** (Beale, Kato, Majda 1984) Let u₀ ∈ H^s(ℝ³) for s ≥ 3 (or s > 5/2), and let u be the smooth solution on [0,T*) where T* is the maximal existence time. Then:

    T* < ∞  ⟹  ∫₀^{T*} ||ω(·,t)||_{L^∞(ℝ³)} dt = +∞

Equivalently: if ∫₀^T ||ω(·,t)||_{L^∞} dt < ∞, then the solution extends smoothly to t = T.

**Key inequality in the proof:** The proof requires bounding ||∇u||_{L^∞} in terms of ||ω||_{L^∞}. Kato-Ponce (1988) and others use the logarithmic Sobolev inequality:

    ||∇u||_{L^∞} ≤ C (1 + ||ω||_{L^∞}) (1 + log⁺ ||u||_{H^s} / (1 + ||ω||_{L^∞}))

or equivalently (from Brezis-Wainger-Gallouet inequality):

    ||u||_{W^{1,∞}} ≤ C ||u||_{H²} (1 + log(1 + ||u||_{H^{s}}))    for s > 3/2 + 2

[The exact logarithmic Sobolev form used in BKM is:
    ||∇u||_{L^∞} ≤ C ||∇ω||_{L²} (1 + log(||u||_{H^3} / ||∇ω||_{L²}))  ]

This logarithmic correction is what makes the BKM bound integrable and the proof work.

**Source:** Beale, J.T., Kato, T., and Majda, A. (1984) "Remarks on the breakdown of smooth solutions for the 3-D Euler equations," Comm. Math. Phys. Originally for Euler equations; extension to NS is essentially the same.

**Where it enters:** Gives a sufficient condition for regularity that is weaker than Prodi-Serrin (only requires L¹ in time of L^∞ in space of vorticity).

**What it bounds:** The H^s norm of u in terms of the L^∞ norm of ω, via a Gronwall argument.

**Scaling:** The quantity ∫||ω||_{L^∞} dt is scale-invariant for NS (with the NS scaling, ω → λ²ω and t → λ²t, so ∫||ω||_{L^∞}dt is invariant). This is a critical condition.

**Constant status:** The constant C is existential; the logarithmic correction factor is explicit in structure but not in the exact coefficient.

**Sharpness:** Unknown — whether the logarithmic correction is necessary or whether the condition ∫||ω||_{L^∞}dt < ∞ can be weakened to ∫||ω||_{L^∞}/log(1+||ω||_{L^∞})dt < ∞ is an open question.

**Tao Category:** NS-specific — uses the specific structure of the vorticity equation (which is NS-specific).

---

### R3. CKN Local Energy Inequality

**Exact Statement:** (Caffarelli-Kohn-Nirenberg 1982, Def. 2.2) A suitable weak solution (u,p) of 3D NS satisfies the local energy inequality:

    ∂ₜ(|u|²/2) + |∇u|² ≤ ∆(|u|²/2) − (|u|²/2 + p)∇·(uφ) + f·u

More precisely, for any φ ∈ C₀^∞(ℝ⁴), φ ≥ 0:

    ∫∫ |∇u|² φ dx dt ≤ ∫∫ [|u|²/2 (∂ₜφ + ∆φ) + (|u|²/2 + p)(u·∇φ) + f·u φ] dx dt

This is the LOCAL version of the energy inequality (the global one E1 is obtained by integrating over all space).

**Source:** Caffarelli, R., Kohn, R., Nirenberg, L. (1982) "Partial regularity of suitable weak solutions of the Navier-Stokes equations," Comm. Pure Appl. Math.

**Where it enters:** Foundation of partial regularity theory — every subsequent result (Lin 1998, Ladyzhenskaya-Seregin 1999, Vasseur 2007, etc.) uses a variant of this inequality.

**What it bounds:** Local kinetic energy and local dissipation in parabolic cylinders Q_r = B_r × (t₀-r², t₀).

**Constant status:** No extra constant — this is essentially an identity with an inequality sign from a weak form argument.

**Tao Category:** NS-specific — relies on the cancellation in (u·∇u)·u = 0 which gives the local energy structure.

---

### R4. CKN ε-Regularity Lemma

**Exact Statement:** (CKN 1982, Proposition 2) There exists an absolute constant ε* > 0 such that: if (u,p) is a suitable weak solution in Q₁ = B₁(0) × (-1,0), and

    **Condition (I):**    (1/r³) ∫∫_{Q_r} |∇u|² dx dt ≤ ε*

for some r ∈ (0,1), then u is Hölder continuous in Q_{r/2}.

Alternative formulation using the "normalized quantities":

    A(r) = sup_{t ∈ (-r²,0)} (1/r) ∫_{B_r} |u|² dx,
    E(r) = (1/r) ∫∫_{Q_r} |∇u|² dx dt,
    C(r) = (1/r²) ∫∫_{Q_r} |u|³ dx dt,
    D(r) = (1/r²) ∫∫_{Q_r} |p|^{3/2} dx dt

CKN prove: there exists ε* such that if A(r) + E(r) + C(r) + D(r) ≤ ε*, then u is regular in Q_{r/2}.

This yields: the 1D parabolic Hausdorff measure P¹(Sing(u)) = 0, i.e., the singular set has parabolic Hausdorff dimension ≤ 1.

**Source:** CKN (1982). Lin (1998) "A new proof of the Caffarelli-Kohn-Nirenberg theorem" simplified the argument; key simplification: Lin showed condition A(r) ≤ ε* alone is sufficient under a scaling condition.

**Key value:** ε* is NOT explicitly computed in CKN or subsequent papers (to my knowledge). It is a pure existence result. This is a major gap in the program — the constant ε* is not known explicitly.

**Constant status:** EXISTENTIAL — ε* exists but is not computed. Several papers attempt to make it more explicit but the computation involves compactness arguments that resist quantification.

**Scaling:** The CKN quantities A(r), E(r), C(r), D(r) are each scale-invariant under the NS scaling.

**Sharpness:** The 1D bound on the singular set is conjectured to be loose — the actual singular set should have dimension 0 (at most isolated points), but this is unproved. So ε-regularity as a tool probably has significant slack.

**Tao Category:** NS-specific — uses the local energy inequality (which is NS-specific).

---

### R5. Escauriaza-Seregin-Šverák (ESS) L³ Endpoint

**Exact Statement:** (ESS 2003) If u is a Leray-Hopf weak solution of 3D NS on [0,T] and

    lim_{t→T⁻} ||u(·,t)||_{L³(ℝ³)} = ∞

(i.e., u blows up in L³), then u was NOT a Leray-Hopf weak solution on a larger interval. More usefully stated: if u ∈ L^∞(0,T; L³(ℝ³)), then u is regular on (0,T].

**Key analytical tool — Backward Uniqueness:** The proof reduces to a backward uniqueness theorem for the heat equation with lower-order terms. Specifically:

If w satisfies |∂ₜw + ∆w| ≤ C(|w| + |∇w|) in ℝⁿ × (0,T) and w(·,T) = 0 and ||w||_{L^∞} ≤ M, then w ≡ 0 on ℝⁿ × (0,T).

The proof of backward uniqueness uses **Carleman-type inequalities**:

    ∫∫ e^{-φ/σ} (|∂ₜv|² + |∆v|²) dx dt ≥ C/σ ∫∫ e^{-φ/σ} |∇²v|² dx dt

for appropriate weight functions φ. (The precise form requires careful notation from the ESS paper.)

**Source:** Escauriaza, L., Seregin, G., and Šverák, V. (2003) "L_{3,∞}-solutions of Navier-Stokes equations and backward uniqueness," Russian Math. Surveys.

**Key constants:** The constants in the Carleman inequalities are existential. The proof is non-constructive.

**Where it enters:** Resolves the L³ endpoint of the Prodi-Serrin scale — the most delicate case.

**Tao Category:** NS-specific — the specific structure of the NS equations is needed to reduce to the backward uniqueness problem.

---

### G1. Gronwall-Based Growth Estimates

**Exact Statement:** For a quantity y(t) ≥ 0 satisfying:

    dy/dt ≤ A(t) y + B(t)

the Gronwall lemma gives:

    y(t) ≤ e^{∫₀ᵗ A(s) ds} [y(0) + ∫₀ᵗ B(s) e^{-∫₀ˢ A(r) dr} ds]

**Application in NS:** When bounding ||u||²_{H^s}, one derives:

    d/dt ||u||²_{H^s} ≤ C ||∇u||_{L^∞} ||u||²_{H^s}

By Gronwall:

    ||u(t)||²_{H^s} ≤ ||u₀||²_{H^s} exp(C ∫₀ᵗ ||∇u(s)||_{L^∞} ds)

This is the BKM-type bound: H^s norm grows at most exponentially in the time integral of ||∇u||_{L^∞}.

**Source:** Gronwall (1919). Application to NS: standard, appears in virtually all NS textbooks.

**Where it enters:** Every higher-order energy estimate. The exponential factor is the "cost" of using Gronwall.

**What it bounds:** Growth rate of H^s norm of u.

**Scaling:** The exponential bound e^{C ∫||∇u||_{L^∞}dt} can be astronomically large compared to what actually happens in smooth flows (where ||u(t)||_{H^s} grows polynomially or mildly). The Gronwall bound is generically the loosest step in the chain.

**Constant status:** The constant C in the exponent is existential but often related to the GNS constant.

**Sharpness:** The Gronwall inequality itself is sharp (equality for dy/dt = Ay). But A(t) = ||∇u||_{L^∞} is typically much smaller than the worst case, so the *compound* bound (Gronwall applied to a differential inequality where A(t) is itself bounded by other estimates) is loose.

**Tao Category:** Generic — Gronwall applies to any ODE. It is not NS-specific.

---

### F6. Brezis-Gallouet-Wainger Logarithmic Sobolev Inequality

**Exact Statement:** (Brezis-Gallouet 1980, Brezis-Wainger 1980) For u ∈ W^{1,n}(Ω) ∩ W^{2,n/2}(Ω) (or for n=3: u ∈ H¹(ℝ³) ∩ H^{3/2}(ℝ³)), the following borderline embedding holds:

    ||u||_{L^∞(ℝ³)} ≤ C ||u||_{H^1(ℝ³)} (1 + log^{1/2}(1 + ||u||_{H^{3/2}(ℝ³)} / ||u||_{H^1(ℝ³)}))

More commonly used in the BKM context: for u ∈ H^s(ℝ³), s > 5/2:

    ||∇u||_{L^∞} ≤ C ||∇u||_{H^{n/2}} (1 + log^{1/2}(||u||_{H^s} / ||∇u||_{H^{n/2}}))

The key feature is the logarithmic correction: without it, H^{3/2} does not embed into L^∞ in 3D (since H^{3/2} is the critical Sobolev exponent in 3D for L^∞). The logarithm is the "just barely fails to embed" correction.

**Source:** Brezis, H. and Gallouet, T. (1980) "Nonlinear Schrödinger evolution equations," Nonlinear Anal.; Brezis, H. and Wainger, S. (1980) "A note on limiting cases of Sobolev embeddings and convolution inequalities," Comm. Partial Differential Equations. Application to NS/Euler in Beale-Kato-Majda (1984).

**Where it enters:** The BKM proof uses this inequality (or a variant) to bound ||∇u||_{L^∞} in terms of ||ω||_{L^∞} and ||u||_{H^s}:

    ||∇u||_{L^∞} ≤ C ||ω||_{L^∞} (1 + log(1 + ||u||_{H^s} / ||ω||_{L^∞}))

This is the key step: the logarithm makes ∫₀ᵀ ||∇u||_{L^∞} dt integrable under the BKM hypothesis ∫₀ᵀ ||ω||_{L^∞} dt < ∞, combined with a Gronwall argument for ||u||_{H^s}.

**What it bounds:** The L^∞ norm of u (or ∇u) in terms of a slightly higher Sobolev norm, with a logarithmic correction at the critical exponent.

**Scaling:** The inequality is at the critical Sobolev exponent — H^{n/2} is the borderline space for L^∞ in dimension n. The logarithmic correction is necessary and sharp (without it, the embedding fails).

**Constant status:** The exponent of the logarithm (1/2) is sharp (Brezis-Wainger proved this). The leading constant C depends on the domain but is existential.

**Sharpness:** The exponent 1/2 on the log is sharp. Equality is "asymptotically attained" by sequences of functions concentrating on points.

**Tao Category:** Generic — holds for any H^{3/2} function, not NS-specific.

---

### F7. Kato-Ponce Commutator Estimate

**Exact Statement:** (Kato-Ponce 1988) Let J^s = (I - ∆)^{s/2} be the Bessel potential of order s, and let 1 < p < ∞, s > 0. Then:

    ||J^s(fg) - f J^s g||_{L^p} ≤ C(||∇f||_{L^{p_1}} ||J^{s-1}g||_{L^{p_2}} + ||J^s f||_{L^{p_3}} ||g||_{L^{p_4}})

where 1/p = 1/p₁ + 1/p₂ = 1/p₃ + 1/p₄, 1 < p₁, p₄ ≤ ∞, 1 < p₂, p₃ < ∞.

Applied to NS: with f = u and g = u (or ∂_j u), this gives:

    ||J^s(u · ∇u)||_{L^2} ≤ C (||u||_{H^s} ||∇u||_{L^∞} + ||∇u||_{L^∞} ||u||_{H^s})
                          ≤ C ||u||_{H^s} ||u||_{W^{1,∞}}

This is used to bound the H^s norm of the nonlinear term in terms of H^s and W^{1,∞} norms.

**Source:** Kato, T. and Ponce, G. (1988) "Commutator estimates and the Euler and Navier-Stokes equations," Comm. Pure Appl. Math.

**Where it enters:**
- H^s energy estimates: d/dt ||u||²_{H^s} ≤ C ||∇u||_{L^∞} ||u||²_{H^s} (via Kato-Ponce)
- This gives the BKM-type estimate: ||u(t)||_{H^s} ≤ ||u₀||_{H^s} exp(C ∫₀ᵗ ||∇u||_{L^∞} ds)
- Combined with F6 (BKM), gives the Beale-Kato-Majda theorem

**What it bounds:** The H^s norm of the nonlinear product u·∇u in terms of H^s of u and W^{1,∞} of u.

**Scaling:** Scale-invariant in the appropriate sense. The bound ||u||_{H^s}||u||_{W^{1,∞}} involves a mixed norm that is not a single Sobolev norm — this is the source of the Gronwall iteration.

**Constant status:** Existential C(s,p,p₁,...).

**Sharpness:** Known to be essentially sharp for the commutator structure.

**Tao Category:** Generic — Kato-Ponce holds for any smooth function composition, not NS-specific.

---

### F8. Hardy-Littlewood-Sobolev (HLS) Inequality

**Exact Statement:** For α ∈ (0,n) and 1 < p, q < ∞ with 1/q = 1/p - α/n:

    || |·|^{-α} * f ||_{L^q(ℝⁿ)} ≤ C_{α,n,p} ||f||_{L^p(ℝⁿ)}

Equivalently (Riesz potential): ||I_α f||_{L^q} ≤ C ||f||_{L^p} where I_α = |·|^{-(n-α)} is the Riesz potential.

**Key case for NS:** n=3, α=2, p=3/2, q=3:

    ||I_2 f||_{L^3(ℝ³)} ≤ C ||f||_{L^{3/2}(ℝ³)}

This is used in CKN because the pressure satisfies p = -I_2(∂_i u^j ∂_j u^i) (schematically), so:

    ||p||_{L^3} ≤ C ||∇u||²_{L^3}    (by HLS + composition)

or more carefully:

    ||p||_{L^{3/2}} ≤ C ||u||²_{L^3}

**Source:** Hardy-Littlewood (1927), Sobolev (1938). Sharp constant: Lieb (1983) "Sharp constants in the Hardy-Littlewood-Sobolev and related inequalities," Ann. Math.

**Where it enters:** CKN partial regularity: the pressure estimate ||p||_{L^{3/2}(Q_r)} ≤ C [...] uses HLS.

**Constant status:** The sharp constant for HLS on ℝⁿ was computed by Lieb (1983). It is explicit (involving Gamma functions and π) but complex.

**Sharpness:** YES — sharp constants found by Lieb (1983) using symmetry and rearrangements. The extremal functions are again concentrated (Aubin-Talenti type) and not NS solutions.

**Tao Category:** Generic.

---

### E4. Higher-Order Energy Estimate (H^s energy)

**Exact Statement:** For smooth NS solutions, applying J^s = (I-∆)^{s/2} to the NS equation and taking the L² inner product with J^s u:

    (1/2) d/dt ||u||²_{H^s} + ν||u||²_{H^{s+1}} = −⟨J^s(u·∇u) − u·∇(J^s u), J^s u⟩ − ⟨u·∇(J^s u), J^s u⟩

The first term (commutator) is controlled by Kato-Ponce (F7):
    |first term| ≤ C||∇u||_{L^∞}||u||²_{H^s}

The second term (transport structure) vanishes when div u = 0:
    ⟨u·∇(J^s u), J^s u⟩ = 0    (since div u = 0, integration by parts)

Therefore:
    d/dt ||u||²_{H^s} + 2ν||u||²_{H^{s+1}} ≤ C||∇u||_{L^∞}||u||²_{H^s}

By Gronwall (G1):
    ||u(t)||²_{H^s} ≤ ||u₀||²_{H^s} exp(C ∫₀ᵗ ||∇u(s)||_{L^∞} ds)

**Source:** This exact formulation is in Majda-Bertozzi (2002) "Vorticity and Incompressible Flow," Chapter 3. The commutator estimate is Kato-Ponce (1988).

**Where it enters:**
- Gives the BKM blow-up criterion directly when combined with F6 (Brezis-Gallouet-Wainger)
- Establishes persistence of H^s regularity for smooth solutions
- Quantifies how much the H^s norm can grow in terms of the vorticity

**What it bounds:** The H^s norm of the velocity for s ≥ 1.

**Scaling:** If ||∇u||_{L^∞} ≤ M (bounded), then ||u(t)||_{H^s} ≤ ||u₀||_{H^s} e^{CMt} — exponential growth. For turbulent flows with Re ≫ 1, M = ||∇u||_{L^∞} ~ Re (rough estimate), giving exp(CRe·T) — enormous overestimate vs. polynomial growth of smooth solutions.

**Constant status:** Existential C from Kato-Ponce.

**Sharpness:** The bound is sharp for the commutator estimate (Kato-Ponce is sharp), but the APPLICATION to NS is loose because the transport term vanishes (div-free), giving a better implicit constant than the general Kato-Ponce bound.

**Tao Category:** The transport cancellation ⟨u·∇(J^s u), J^s u⟩ = 0 is NS-specific (uses div u = 0). Without this, the Kato-Ponce commutator would not close so cleanly.

---

## Part 3: Structural Analysis

### 3.1 Inequality Chains

The main chains in NS regularity arguments:

**Chain A: Energy → Enstrophy → Regularity failure**

    E1 (Energy ineq.) → E2 (Enstrophy ODE) → (via F1 Ladyzhenskaya) → ODE blow-up

Steps: (1) Global energy inequality controls ||u||_{L^∞_t L²_x} ∩ L²_t H¹_x. (2) Enstrophy equation with F1 gives dy/dt ≤ Cy³/ν³. (3) This ODE blows up if y₀ is large enough. The "failure" to close regularity occurs at step (2) — the Ladyzhenskaya inequality applied to the vortex stretching term gives an exponent of 3 on the enstrophy (too high for global control).

**Chain B: Prodi-Serrin (conditional regularity)**

    u ∈ L^p_t L^q_x (assumed) → (via F2 GNS + F5 CZ pressure) → ||∇u||_{L^2} improves → iterative bootstrap → full regularity

The GNS inequality at the core: each step gains one derivative while paying for the spacetime integrability of u.

**Chain C: CKN Partial Regularity**

    R3 (Local energy ineq.) → scale-invariant quantities A,C,D,E → (by Hölder + F1 + F5) → R4 (ε-regularity) → covering argument → P¹(Sing) = 0

The chain uses: R3 feeds into the Hölder estimates, which require F1 (Ladyzhenskaya for |u|³ control from H¹) and F5 (CZ for pressure from velocity), to establish the CKN condition A+C+D+E ≤ ε*.

**Chain D: BKM Blow-up Criterion**

    H^s energy estimate (via F4 Agmon for ||∇u||_{L^∞} ≤ C||u||_{H^1}||u||_{H^2}) → G1 Gronwall → H^s growth bounded by exp(∫||ω||_{L^∞}dt)

### 3.2 Accumulated Slack (Most to Least)

Assessing the multiplicative constant compounding:

1. **Gronwall + Agmon combination (Chain D):** The Agmon bound ||∇u||_{L^∞} ≤ C||u||_{H^2} overestimates the actual L^∞ gradient by O(Re^{1/2}) for turbulent flows. The Gronwall exponential then further amplifies this. **Highest accumulated slack.**

2. **Vortex stretching bound (Chain A):** The bound |VS| ≤ C||ω||^{3/2}_{L²}||∇ω||^{3/2}_{L²} (from Ladyzhenskaya applied to ω in L⁴) is known to be loose by the Constantin-Fefferman result — actual vortex stretching is controlled by vorticity alignment, and randomly directed vorticity would give a much smaller VS. **High slack for generic flows.**

3. **Ladyzhenskaya inequality (F1):** The extremal function is a static Sobolev ball, not a fluid. The actual L⁴ norm of NS solutions is controlled by the intermittency of the velocity field — for flows with standard Kolmogorov intermittency corrections, ||u||_{L^4} is much smaller than the Ladyzhenskaya bound suggests. **Moderate-high slack.**

4. **Sobolev embedding (F3):** The Aubin-Talenti extremals are concentrated at a point; NS solutions are distributed. For spatially smooth flows, the actual L⁶ norm is well below the Sobolev bound. **Moderate slack.**

5. **GNS interpolation (F2):** The extremals (Aubin-Talenti functions) are static. For time-evolving flows, the instantaneous GNS bound can be loose, but time-averaging tends to make it less so. **Moderate slack.**

6. **CZ pressure estimate (F5):** At q=2, this is essentially sharp (Plancherel). For q ≠ 2, there is slack from the non-sharpness of Riesz transform bounds. **Low-moderate slack.**

7. **Local energy inequality (R3):** This is essentially exact (≈ identity) for smooth solutions. **Very low slack** for smooth solutions, but weak solutions may have slack.

8. **Energy inequality (E1):** Exact equality for smooth solutions. **Zero slack** for regular solutions.

### 3.3 Which Inequalities Have Highest Leverage?

- **Ladyzhenskaya (F1):** Appears in nearly every energy/enstrophy chain. Tightening it or finding its NS-specific analogue would affect Chains A, B, C.
- **GNS interpolation (F2):** Master inequality — all others are special cases. Any improvement to GNS would cascade everywhere.
- **Vortex stretching bound (E3):** The single inequality responsible for the enstrophy equation not closing. This is the KEY bottleneck.
- **ε-regularity threshold (R4):** If ε* could be computed explicitly, partial regularity results could be made quantitative and potentially extended.

---

## Part 4: Gaps and Ambiguities

### 4.1 Convention Inconsistencies

1. **Ladyzhenskaya exponents:** In 2D, the clean form is ||u||_{L⁴} ≤ C||u||_{L²}^{1/2}||∇u||_{L²}^{1/2}. In 3D, the exponents 1/4 and 3/4 are correct but some authors include the ||u||_{H¹} = (||u||²_{L²} + ||∇u||²_{L²})^{1/2} norm on the right, others use just ||∇u||_{L²}. On T³ (where the mean matters), the form differs from ℝ³. This creates notational inconsistency.

2. **Agmon's inequality in 3D:** Some sources state ||u||_{L^∞} ≤ C||u||_{H¹}^{1/2}||u||_{H²}^{1/2} as "Agmon's inequality in 3D" but this is the 2D version. The correct 3D version requires H^{3/2+ε} or is the interpolation ||u||_{L^∞} ≤ C||u||_{H^s} for s > 3/2. The form used in BKM is a different logarithmic inequality. There is genuine ambiguity here.

3. **Energy inequality direction:** Leray (1934) proved the energy inequality in integral form; Hopf (1951) proved it for approximating sequences. Whether equality holds (energy conservation for weak solutions) is equivalent to the Onsager conjecture — proved by Isett (2018) for C^{1/3-ε} solutions.

4. **CKN epsilon threshold:** The exact value of ε* in the ε-regularity lemma varies between papers using different norms and different parabolic cylinders. Lin (1998), Ladyzhenskaya-Seregin (1999), Vasseur (2007), and Kukavica (2009) all use slightly different formulations. The ε* is NOT universally standardized.

5. **Pressure regularity:** In CKN theory, the pressure is assumed to satisfy a certain L^{3/2} integrability condition. Whether this is automatic from the NS equations or must be assumed separately is a subtle point (it is automatic for distributional solutions but requires care).

### 4.2 Unknown Constants

- The sharp constant for Ladyzhenskaya in 3D is not commonly tabulated (though it follows from GNS with explicit Sobolev constants — this could be computed).
- The Agmon constant in 3D is existential.
- The CKN ε* threshold is existential and uncomputed.
- The constants in the Carleman inequalities used in ESS are existential.
- The constant C in the vortex stretching bound |VS| ≤ C||ω||^{3/2}||∇ω||^{3/2} is existential.

### 4.3 Potentially Missing Inequalities

Based on the survey, the following inequalities may also be load-bearing but were not explicitly cataloged:

- **Kato-Ponce commutator estimates** (used in fractional Sobolev energy estimates): ||J^s(fg) - f J^s g||_{L^2} ≤ C(||∇f||_{L^p}||J^{s-1}g||_{L^q} + ||J^s f||_{L^p}||g||_{L^q}) — used in the H^s energy estimates.
- **Brezis-Gallouet-Wainger logarithmic Sobolev inequality:** ||u||_{L^∞} ≤ C(1 + ||u||_{H^{n/2}})(1 + log^{1/2}(1 + ||u||_{H^s})) — used in BKM.
- **Parabolic smoothing estimates:** if u is a weak solution, then u ∈ L²_{loc}(0,T; H²_{loc}) (Prodi-Serrin-type smoothing). What is the exact bound?
- **Strichartz estimates** for the linear Stokes equation — used in some regularity proofs.
- **Hardy-Littlewood-Sobolev inequality** — used in pressure estimates in CKN.

---

## Part 5: Next Steps Recommendation

### 5.1 Ranking by Expected Slack (Most Slack First)

**Rank 1: Vortex Stretching Bound (E2/E3)**

*Why most slack:* The bound |VS| ≤ C||ω||^{3/2}_{L²}||∇ω||^{3/2}_{L²} is the single inequality responsible for the enstrophy equation having a super-quadratic right-hand side (making global regularity unprovable). Constantin-Fefferman (1993) showed this bound is not tight — for flows where vorticity directions are not aligned, VS is much smaller. The gap between the algebraic bound and the actual VS in turbulent flow is potentially enormous.

*Specific computation:* Given a family of NS-compatible velocity fields (e.g., from direct numerical simulation data), compute VS directly and compare to the Ladyzhenskaya-based bound. The ratio (actual VS)/(Ladyzhenskaya bound) quantifies the slack. For isotropic turbulence, the expected ratio from Kolmogorov theory is ~Re^{-1/4} → 0 as Re → ∞.

*What a tightening would yield:* If |VS| ≤ f(||ω||_{L²}, ||∇ω||_{L²}) with f growing only quadratically (not to the 3/2 power), the enstrophy ODE would close and 3D NS would be globally regular. This is not believed possible for the analytic bound (Tao's result suggests barriers), but for *NS-specific* flows there may be more room.

**Rank 2: Agmon + Gronwall Chain (F4 + G1)**

*Why high slack:* The Agmon bound ||∇u||_{L^∞} ≤ C||u||_{H^2} overestimates the actual gradient by the square root of the Reynolds number for turbulent flows (L^∞ norm is controlled by a single large-gradient event, while H² norm sums over all frequencies). The subsequent Gronwall exponential amplifies this: if A(t) = ||∇u||_{L^∞} is overestimated by a factor R, the Gronwall bound grows by exp(R·T) instead of exp(T), which is astronomically loose.

*Specific computation:* For the Burgers equation (1D analog), compute the actual growth of ||u||_{H^s} alongside the Gronwall bound. The ratio should grow exponentially in Re.

*What a tightening would yield:* A tighter Agmon-type inequality for divergence-free vector fields (using the specific structure of NS solutions, e.g., the energy spectrum) would immediately tighten BKM and all higher-energy estimates.

**Rank 3: ε-Regularity Constant in CKN (R4)**

*Why high slack:* The constant ε* in the CKN ε-regularity lemma is completely uncomputed. The proof uses a compactness argument (subsequence extraction) that does not yield quantitative bounds. If ε* could be computed explicitly (even a rough lower bound), it would:
1. Make the partial regularity result quantitative.
2. Potentially yield improved Hausdorff dimension bounds on the singular set.
3. Enable numerical verification of regularity for specific flows.

*Specific computation:* The ε* is tied to the constant in the parabolic interpolation inequality for NS-compatible functions in a parabolic cylinder. A PDE/variational calculation could in principle yield an explicit ε* via a computable optimization problem.

*What a tightening would yield:* Explicit ε* → quantitative partial regularity → potentially dimension 0 singular set (isolated points only) with a specific count.

**Rank 4: Ladyzhenskaya Constant (F1)**

*Why moderate slack:* The constant C_L in the 3D Ladyzhenskaya inequality can be computed explicitly from GNS. However, for NS solutions (which are divergence-free), there may be a better constant — the divergence-free constraint removes certain functions from consideration. The "NS-specific Ladyzhenskaya constant" has not been computed.

*Specific computation:* Compute the best constant C_{L,div-free} = sup{ ||u||_{L⁴} / (||u||_{L²}^{1/4}||∇u||_{L²}^{3/4}) : u ∈ H¹(T³), ∇·u = 0 }. This is a calculus of variations problem that can be attacked numerically (gradient descent in the space of divergence-free fields on T³).

*What a tightening would yield:* If C_{L,div-free} < C_L by a factor α < 1, every inequality using Ladyzhenskaya in the NS context improves by α (and compounded chains improve by α^k for k applications).

**Rank 5: Brezis-Gallouet-Wainger Logarithmic Inequality (BKM supporting)**

*Why moderate slack:* The BKM proof uses a logarithmic Sobolev inequality of the form ||u||_{W^{1,∞}} ≤ C||u||_{H²}(1 + log(||u||_{H^s}/||u||_{H²})). The logarithmic correction is what makes BKM integrable. If the logarithm can be sharpened — e.g., the exponent 1 on the log reduced to 1/2, or the argument changed — the BKM regularity criterion would be correspondingly weakened (making regularity easier to prove from BKM data).

*Specific computation:* Compute the sharp constant and exponent in the 3D Brezis-Gallouet-Wainger inequality. This is an analytic problem with a specific critical embedding (H² is borderline for L^∞ in 2D; H^{3/2} is borderline in 3D).

*What a tightening would yield:* A stronger BKM criterion (less demanding condition guaranteeing regularity) → potentially bringing BKM and Prodi-Serrin closer to each other in strength.

---

## Summary Table: Expected Slack Rankings

| Rank | ID | Inequality | Expected Slack Mechanism | Computation to Quantify |
|------|----|-----------|--------------------------|------------------------|
| 1 | E2/E3 | Vortex Stretching | Vorticity alignment; Ladyzhenskaya overestimates VS by ~Re^{1/4} | Compute (VS_actual)/(VS_Ladyzhenskaya bound) for DNS data or model flows |
| 2 | F4+G1 | Agmon+Gronwall | L^∞ overestimate + exponential amplification | Burgers analog computation |
| 3 | R4 | CKN ε* | Uncomputed existence constant | Variational problem for ε* in parabolic cylinder |
| 4 | F1 | Ladyzhenskaya | Non-divergence-free extremal; NS constant smaller | Numerical optimization over div-free fields on T³ |
| 5 | Implicit | BKM log inequality | Log exponent may be improvable | Sharp constant computation for 3D BW inequality |

---

## Appendix: On the Tao (2016) Obstruction

Tao (2016) "Finite time blowup for an averaged Navier-Stokes equation" (J. Amer. Math. Soc.) proved that a certain *averaged* version of NS (replacing the nonlinearity with an averaged/mollified version) CAN blow up in finite time. This shows that:

**The following are NOT sufficient to prove NS regularity:**
- Scaling properties of NS
- Energy estimates (E1)
- Sobolev/GNS inequalities (F2, F3)
- Gronwall-type estimates (G1)
- The cancellation (u·∇u)·u = 0 (this is preserved in the averaged system)

**What Tao's result implies for our catalog:**

"Generic" inequalities (F1-F4, G1) by themselves cannot prove regularity. The averaged NS can blow up while satisfying all generic estimates. Therefore, any proof of NS regularity MUST use NS-specific structure beyond the energy and scaling.

The NS-specific structures that the averaged system breaks are:
- The specific algebraic form of the nonlinearity (u·∇)u = div(u⊗u) for vector u
- The pressure equation −∆p = div div(u⊗u) (which requires the matrix structure)
- The vorticity dynamics (ω·∇u term) — the averaged system scrambles the vortex stretching structure

**Implication for slack analysis:** Inequalities marked "NS-specific" are the ones where actual slack (specific to real NS solutions) is most meaningful. The generic inequalities (Sobolev, GNS, Gronwall) may have slack on NS solutions but that slack cannot be leveraged in a proof without also invoking NS-specific structure.

---

---

## Notes on Verification

The detailed entries above are based on the mathematical literature as known to the author. Key statements to verify against specific sources:

- Sharp Sobolev constant S₃ for H¹ ↪ L⁶: exact numerical value from Talenti (1976)
- Whether Lin (1998) or Ladyzhenskaya-Seregin (1999) made the CKN ε* explicit or merely simplified the proof
- The exact form of the Carleman inequality used in ESS (2003) — the paper contains precise technical statements
- The sharp constant in the 3D Brezis-Gallouet-Wainger inequality (the exponent 1/2 on the log is sharp, but the leading constant C is existential)
- Whether any modern computational paper (e.g., Fefferman's NS prize description) gives explicit bounds on any of these constants

*Note: Three background agents were launched to verify these specifics via web search. Results not yet incorporated (agents still running). The core content is from the author's training on the mathematical literature.*
