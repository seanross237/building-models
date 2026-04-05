# Mission

Find the loosest estimate in Navier-Stokes regularity theory. Take the key inequalities used in regularity proofs (Ladyzhenskaya, CKN energy estimates, interpolation bounds), run actual NS simulations, measure how tight each bound is. Find which one has the most slack. A tighter version of a loose estimate is a novel result and direct progress toward the regularity problem.

This is a stepping stone toward the Navier-Stokes Existence and Smoothness Millennium Prize Problem. The question behind the Prize: given smooth initial data, do solutions to the 3D incompressible Navier-Stokes equations

  ∂u/∂t + (u·∇)u = ν∆u − ∇p + f
  ∇·u = 0

remain smooth for all time? Nobody knows. But the proofs that get closest all rely on specific estimates, and those estimates may have slack — just as the SZZ spectral gap bound in Yang-Mills turned out to be 8× too conservative.

What is known:
- **Leray (1934):** Weak solutions exist globally but may not be smooth. If singularities occur, the singular set in time has Hausdorff dimension ≤ 1/2.
- **Caffarelli-Kohn-Nirenberg (1982):** The singular set in spacetime has 1-dimensional parabolic Hausdorff measure zero (partial regularity). Best result on the "yes" side.
- **Prodi-Serrin-Ladyzhenskaya criteria:** Regularity holds if u ∈ L^p_t L^q_x with 2/p + 3/q ≤ 1, q > 3. Endpoint cases remain open.
- **Escauriaza-Seregin-Šverák (2003):** Regularity holds if u ∈ L^∞_t L³_x.
- **Tao (2016):** Constructed blow-up solutions for an averaged Navier-Stokes, showing that any proof of regularity must use specific structural properties of the nonlinearity — not just energy estimates and scaling.
- **Numerical evidence:** Universally shows smooth behavior. No numerical blow-up candidate has survived scrutiny.

Concretely:
1. **Identify the key estimates.** Map which inequalities are load-bearing in the major regularity results (CKN, Prodi-Serrin, ESS). For each, write down the exact mathematical statement and where it enters the proof.
2. **Test them computationally.** Run NS simulations (pseudospectral on T³, a range of Reynolds numbers and initial conditions). For each estimate, measure the ratio of the bound to the actual value. Find the slack factor.
3. **Search for worst cases.** Don't just test typical flows — construct adversarial initial conditions designed to stress each estimate. Vortex tubes, vortex sheets, high-symmetry configurations, near-singular initial data.
4. **Rank by slack.** Which estimate is loosest? By how much? Is the slack robust across Reynolds numbers and initial conditions, or does it tighten as Re → ∞?
5. **Tighten the loosest one.** Once you've identified the target, try to prove a tighter version analytically. Even a constant-factor improvement is novel.

Explorers have full shell access and should compute rather than speculate. Run fluid simulations, measure scaling exponents, test bounds numerically. When a claim depends on a computation, do the computation.
