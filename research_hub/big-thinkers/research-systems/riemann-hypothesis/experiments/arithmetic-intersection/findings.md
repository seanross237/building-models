# Arithmetic Intersection Pairing on the Arithmetic Square

**Date:** 2026-04-05
**Status:** Complete

## Claim Status

- `KNOWN:` established in published work I am relying on.
- `LITERATURE CONJECTURE:` proposed in published work, not proved there.
- `PROPOSAL:` my speculative construction or inference.

## Sources Used

Internal files read first, as requested:

1. `current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/weil-positivity-bridge/findings.md`
2. `current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/geometric-bridge/findings.md`

Primary mathematical sources used to ground the evaluation:

- Alain Connes, *Trace formula in noncommutative geometry and the zeros of the Riemann zeta function* (Selecta Math., 1999).
- Alain Connes and Caterina Consani, *Weil positivity and trace formula, the archimedean place* (Selecta Math., 2021).
- Alain Connes and Caterina Consani, *Quasi-inner functions and local factors* (J. Number Theory, 2021).
- Alain Connes, Caterina Consani, Henri Moscovici, *Zeta zeros and prolate wave operators: semilocal adelic operators* (Ann. Funct. Anal., 2024).
- Alain Connes and Caterina Consani, *The arithmetic site* (C. R. Math., 2014), *Geometry of the arithmetic site* (Adv. Math., 2016), *The scaling site* (C. R. Math., 2016), and *The Riemann-Roch strategy, Complex lift of the Scaling Site* (2019).
- Alain Connes and Caterina Consani, *Riemann-Roch for Spec Z* (Bull. Sci. Math., 2023).
- Gerd Faltings, *Calculus on arithmetic surfaces* (Ann. of Math., 1984).
- Henri Gillet and Christophe Soule, *Arithmetic intersection theory* (IHES Publ. Math., 1990) and *Arithmetic analogs of the standard conjectures* (1994).
- Xinyi Yuan and Shou-Wu Zhang, *The arithmetic Hodge index theorem for adelic line bundles* (2014).
- Stephen Kudla, *Special cycles and derivatives of Eisenstein series* (2004 survey/programmatic paper).
- Jan Bruinier, Benjamin Howard, Stephen Kudla, Michael Rapoport, Tonghai Yang, work on modularity of generating series of divisors on unitary Shimura varieties.
- Chao Li and Yifeng Liu, *Chow groups and L-derivatives of automorphic motives for unitary groups* (Ann. of Math., 2021).

## Executive Summary of the Proposed Construction

`KNOWN:` The exact obstruction is now fairly sharp. The semilocal Sonin spaces do **not** blow up as more places are added; Connes-Consani-Moscovici show they canonically stabilize. The instability sits in the **metrics** on that common space:

\[
dm_S(t)=\left|\prod_{v\in S}L_v\!\left(\tfrac12-it\right)\right|^2dt,
\]

and for \(S_N=\{\infty\}\cup\{p\le N\}\) these weights inherit the critical-line fluctuations of partial Euler products. The archimedean compensation mechanism in the quasi-inner proof is finite by construction, and Connes' 1999 analysis shows that weak limits of finite positive objects can land on a harmonic-measure balayage of the zeros rather than the raw Weil distribution. So the missing object must fix the problem **before** passing to the limit.

`PROPOSAL:` The most plausible global pairing is therefore **not** an infinite product of local inner products. It should be an **adelic, Arakelov-style, additive, regularized intersection pairing** on the square of the scaling site

\[
\mathscr S^{(2)}:=\mathscr S\times_{\mathbf F_1}\mathscr S,
\]

built on metrized Frobenius correspondences. The square comes from Connes-Consani's geometry; the additive regularization comes from Arakelov/adelic height theory; the positivity mechanism should come from a global theta package of Kudla-Siegel-Weil type.

`PROPOSAL:` Concretely, attach to a test function \(f\) in Connes' trace-formula class a primitive correspondence

\[
\Gamma_0(f)=\Gamma(f)-\deg_1(f)H_1-\deg_2(f)H_2,
\]

where \(H_1,H_2\) are the two factor classes and \(\Gamma(f)\) is a weighted integral of Frobenius/scaling correspondences \(\Psi^\lambda\) on \(\mathscr S^{(2)}\). Equip \(\Gamma_0(f)\) with a family of local Green kernels \(g_v(f)\): at \(v=\infty\) the prolate/Toeplitz kernel of Connes-Consani, and at finite \(p\) the scattering/Hankel kernel attached to the local ratio \(\rho_p\). Then define the global intersection pairing by a **zeta-regularized sum of local energies**, not by a product:

\[
\langle \widehat\Gamma_0(f),\widehat\Gamma_0(g)\rangle_{\mathrm{glob}}
:=
(\Gamma_0(f)\cdot\Gamma_0(g))_{\mathrm{trop}}
+ \operatorname{CT}_{z=0}\sum_v N(v)^{-z}\,\mathcal E_v^{\mathrm{prim}}(f,g).
\]

Here `CT` denotes constant-term regularization, and \(\mathcal E_v^{\mathrm{prim}}\) is the primitive local energy after removing the trivial mode. The Weil quadratic form should then be

\[
Q_{\mathrm W}(f,g):=-\langle \widehat\Gamma_0(f),\widehat\Gamma_0(g)\rangle_{\mathrm{glob}}.
\]

`PROPOSAL:` The key additional conjecture is an **arithmetic theta/Siegel-Weil formula on the scaling-site square**:

\[
Q_{\mathrm W}(f,g)=\langle \Theta(f),\Theta(g)\rangle_{\mathrm{glob}},
\]

for a theta lift \(\Theta\) landing in primitive arithmetic correspondences on \(\mathscr S^{(2)}\). This is the step that would globalize the "modular boost": local pieces that are not positive termwise would combine by adelic theta symmetry into a globally positive height pairing.

This proposal does **not** solve RH. It isolates what the missing pairing should look like if it exists:

1. local restrictions reproduce the semilocal forms on the stabilized Sonin space;
2. the pairing is adelically normalized, so continuity under adding places is built in;
3. positivity is geometric from the start, so one never has to identify a weak limit of partial positive distributions with the unsmeared Weil distribution.

## Verification of the Exact Obstruction

`KNOWN:` The obstruction to globalizing Connes' positivity is not the absence of finite-stage objects.

- Connes proved the semilocal trace formula for finite sets of places.
- Connes-Consani proved the archimedean positivity theorem.
- Connes-Consani proved finite products of local factors are quasi-inner.
- Connes-Consani-Moscovici proved the semilocal Sonin spaces stabilize canonically across finite \(S\).

`KNOWN:` The obstruction is the combination of three failures in the all-place limit:

1. the common Sonin space carries \(S\)-dependent inner products weighted by partial Euler products, with critical-line fluctuations of size \(\log\log N\);
2. the archimedean compensation argument that repairs finitely many bad \(p\)-adic factors is inherently finite;
3. weak limits of positive finite-stage trace distributions may record harmonic measure of zeros rather than the actual Weil distribution.

`PROPOSAL:` Therefore any viable pairing must make the all-place object **adelically complete at the level of metrics/cycles**, not only at the level of vector spaces.

## Evaluation of the Six Approaches

### 1. Arakelov Intersection Theory

Core references: Arakelov; Faltings (1984); Gillet-Soule (1990, 1994); Yuan-Zhang and Liu-Zhang-Zhang on adelic Hodge index theorems.

`KNOWN:` `Does it produce the right local restrictions?` Partially yes, and this is its main strength. Arakelov intersection is already a global pairing assembled from finite local contributions plus an archimedean Green-energy term. In other words, it gives exactly the **additive** globalization pattern needed here, and it avoids the bad infinite-product format from the start.

`KNOWN:` `Does it have a positivity mechanism?` Yes. Faltings' Hodge index theorem for arithmetic surfaces, together with later adelic Hodge index theorems, provides a genuine continuity/negativity statement on primitive classes. This is the closest existing template for the continuity property the missing pairing must satisfy under adding places.

`KNOWN:` `What breaks or remains open?` The ambient space is wrong. Classical Arakelov theory works for regular projective arithmetic surfaces over \(\operatorname{Spec}\mathcal O_K\), or more generally for projective varieties with adelic metrized line bundles. The desired square \(\operatorname{Spec}(\mathbf Z)\times_{\mathbf F_1}\operatorname{Spec}(\mathbf Z)\) or \(\mathscr S^{(2)}\) is not such a surface in the usual scheme-theoretic sense. There is no arithmetic Chow group, no Deligne pairing, and no theory of Green currents on the scaling-site square. So Arakelov gives the **formal blueprint** for normalization and continuity, but not the actual object.

Verdict: strongest template for how a global pairing should be normalized; insufficient as a direct construction.

### 2. Connes-Consani Scaling Site

Core references: Connes-Consani (2014, 2016, 2019, 2023).

`KNOWN:` `Does it produce the right local restrictions?` This is the best candidate for the ambient geometry. The arithmetic site and scaling site were built precisely to make \(\operatorname{Spec}(\mathbf Z)\) behave like a curve over \(\mathbf F_1\). Their points over \(\mathbf R^{\max}_+\) recover the adele class space quotient, the scaling action plays the Frobenius role, and the periodic orbits \(C_p\) encode primes. So if a square with an intersection pairing exists anywhere, it should be here.

`KNOWN:` `Does it have a positivity mechanism?` Only in embryo. The scaling site has a tropical curve structure, Frobenius correspondences, and a Riemann-Roch strategy. Connes-Consani's later *Riemann-Roch for Spec Z* shows there is real arithmetic content in the one-dimensional geometry, not just metaphor. But none of these papers gives a Hodge index theorem or an actual intersection pairing on the square.

`KNOWN:` `What breaks or remains open?` The square exists conceptually, but the cycle theory does not. There is no arithmetic Chow group of correspondences on \(\mathscr S^{(2)}\), no primitive decomposition, no Deligne pairing, and no positivity theorem. This is exactly the missing gap identified in the geometric-bridge investigation.

Verdict: best geometric recipient for the desired pairing; currently missing the algebraic geometry needed to define it.

### 3. Adelic Intersection Theory

Core references: Connes-Consani-Moscovici (2024); Gillet-Soule; Yuan-Zhang.

`KNOWN:` `Does it produce the right local restrictions?` In principle, yes. Since the semilocal Sonin spaces stabilize, the local data to be globalized lives in the changing inner products and correction operators, not in changing underlying vector spaces. That strongly suggests an adelic formalism where one sums renormalized local energies on a common primitive space.

`PROPOSAL:` The correct adelic format is additive:

\[
\langle \cdot,\cdot\rangle_{\mathrm{glob}}
\sim
\operatorname{CT}_{z=0}\sum_v N(v)^{-z}\,\langle \cdot,\cdot\rangle_v^{\mathrm{ren}},
\]

not multiplicative:

\[
\prod_v \langle \cdot,\cdot\rangle_v,
\]

because logarithms of local norms behave like intersection numbers, while raw products inherit the \(\log\log N\) divergence of the partial Euler product.

`KNOWN:` `Does it have a positivity mechanism?` Only abstractly. Adelic line-bundle theory shows that global positivity can survive infinite collections of local metrics once admissibility and semipositivity are built into the definition. That is exactly the continuity property we want.

`KNOWN:` `What breaks or remains open?` Three things. First, the finite-place local ratios \(\rho_p\) are not individually quasi-inner, so there is no placewise positivity to sum. Second, there is no canonical renormalization known that makes the local semilocal forms converge to the true Weil form rather than a smoothed one. Third, adelic continuity by itself does not eliminate Connes' harmonic-measure smearing. A bare adelic sum is therefore the right analytic **container**, but not a proof engine.

Verdict: analytically necessary, but not sufficient without an additional global positivity structure.

### 4. Modular Boost Globalization

Core references: metaplectic/prolate structure in Connes-Consani-Moscovici (2024); Kudla's program; classical Siegel-Weil and Rallis inner product formulas.

`KNOWN:` `Does it produce the right local restrictions?` Potentially yes. Adelic theta kernels and the Weil representation are designed to factor over all places. That is exactly what one wants if the semilocal forms are to appear as finite-place restrictions of a single global object.

`KNOWN:` `Does it have a positivity mechanism?` Yes, and this is why this approach matters. The whole point of Siegel-Weil/Rallis-type formulas is that a global norm or height of a theta lift equals an Eisenstein quantity built from local data. This is the cleanest existing mechanism by which individually non-positive local pieces can become globally positive after modular assembly. It is the natural way to globalize the archimedean "modular boost."

`KNOWN:` `What breaks or remains open?` The currently known theta/Siegel-Weil frameworks live on reductive groups and their Shimura varieties. Connes' scaling-site square is not yet inside that formalism. There is no known adelic theta kernel whose Fourier coefficients are the Frobenius correspondences on \(\mathscr S^{(2)}\), and no known arithmetic Siegel-Weil formula identifying its height pairing with the Weil distribution of Connes' trace formula.

Verdict: strongest available global positivity mechanism; missing the right geometric target.

### 5. Kudla's Arithmetic Theta Lifts

Core references: Kudla, Kudla-Rapoport-Yang, Bruinier-Howard-Kudla-Rapoport-Yang, Li-Liu (2021).

`KNOWN:` `Does it produce the right local restrictions?` Structurally, yes. This program already packages finite and archimedean local contributions into global arithmetic cycles and their height pairings. In Li-Liu's work, the arithmetic inner product formula explicitly relates heights of arithmetic theta lifts to central \(L\)-derivatives times local zeta integrals. This is very close in shape to what the desired RH pairing should do.

`KNOWN:` `Does it have a positivity mechanism?` Yes. Arithmetic theta lifts come with honest height pairings on arithmetic Chow groups. This is the best existing example of "modular symmetry turns into arithmetic intersection positivity."

`KNOWN:` `What breaks or remains open?` There is no version for \(\operatorname{Spec}(\mathbf Z)\) or for the scaling-site square. Kudla's cycles live on Shimura varieties attached to orthogonal/unitary groups. Even the closest one-dimensional cases are modular or Shimura curves, not the arithmetic site. So this program gives a powerful **analog**, not the desired object itself.

Verdict: closest working model of the missing theorem; wrong ambient geometry.

### 6. My Own Idea

`PROPOSAL:` The right construction is a hybrid:

1. use the scaling-site square as the ambient "surface";
2. import Arakelov/adelic normalization so the global pairing is a regularized sum of local energies;
3. import Kudla/Siegel-Weil as the positivity mechanism that assembles non-positive local data into a positive global height.

`PROPOSAL:` More precisely:

- `Ambient object.` Let \(\mathscr S\) be the Connes-Consani scaling site and \(\mathscr S^{(2)}=\mathscr S\times_{\mathbf F_1}\mathscr S\).
- `Cycles.` Let \(\mathrm{Corr}^{\mathrm{adm}}(\mathscr S^{(2)})\) be a conjectural arithmetic Chow group of **admissibly metrized correspondences**. Its basic generators are the diagonal \(\Delta\), the two factor classes \(H_1,H_2\), and Frobenius correspondences \(\Psi^\lambda\) coming from scaling.
- `Test-function correspondence.` For \(f\) in Connes' test-function space, define

\[
\Gamma(f):=\int_{\mathbf R_+^\ast} f(\lambda)\,\Psi^\lambda\,d^\ast\lambda,
\]

and primitive part

\[
\Gamma_0(f):=\Gamma(f)-\deg_1(f)H_1-\deg_2(f)H_2.
\]

- `Metrics.` Equip \(\Gamma_0(f)\) with local Green kernels \(g_v(f)\). At \(v=\infty\), \(g_\infty\) is the prolate/Toeplitz kernel from Connes-Consani. At finite \(p\), \(g_p\) is the local scattering kernel extracted from the Hankel part of multiplication by the local ratio \(\rho_p\). The admissibility condition is that the renormalized family \((g_v-g_v^{\mathrm{vac}})_v\) has finite adelic energy, exactly as in adelic line-bundle theory.

- `Global intersection.` Define

\[
\langle \widehat\Gamma_0(f),\widehat\Gamma_0(g)\rangle_{\mathscr S^{(2)}}
:=
(\Gamma_0(f)\cdot\Gamma_0(g))_{\mathrm{trop}}
+ \operatorname{CT}_{z=0}\sum_v N(v)^{-z}\,\mathcal E_v^{\mathrm{prim}}(f,g).
\]

Here \((\cdot)_{\mathrm{trop}}\) is the tropical/combinatorial intersection on the square, and \(\mathcal E_v^{\mathrm{prim}}\) is the local primitive energy from the chosen Green kernel. The constant-term regularization removes the universal \(\sum_p 1/p\) divergence.

- `Weil form.` Set

\[
Q_{\mathrm W}(f,g):=
-\langle \widehat\Gamma_0(f),\widehat\Gamma_0(g)\rangle_{\mathscr S^{(2)}}.
\]

This sign matches the usual Hodge-index convention on primitive classes.

`PROPOSAL:` This construction is designed to satisfy the two required properties:

`(a) Local restrictions.` If one truncates the local Green data to a finite set \(S\), then the pairing on \(\widehat\Gamma_0(f)\) should agree with Connes' semilocal quadratic form \(Q_S(f,g)\) after transporting all data to the stabilized Sonin space. The whole point of using local Hankel/prolate kernels is that the semilocal correction operator \(K_S\) is then literally the sum of the local energies over \(v\in S\).

`(b) Positivity continuous under adding places.` Because the pairing is defined on an adelic completion of metrized correspondences, adding places is no longer a weak limit of unrelated quadratic forms. It is just convergence in the completed metric space of admissible Green data. Positivity should then be a Hodge-index statement on that completed space.

`PROPOSAL:` The missing theorem would be:

### Conjectural Arithmetic Hodge-Siegel-Weil Principle

There exists a theta lift

\[
\Theta:\mathcal S(\mathbf A_\mathbf Q)\longrightarrow \mathrm{Corr}^{\mathrm{adm}}(\mathscr S^{(2)})_{\mathrm{prim}}
\]

such that:

1. for every finite \(S\), the \(S\)-truncated pairing of \(\Theta(f)\) with \(\Theta(g)\) equals the semilocal Connes form \(Q_S(f,g)\);
2. globally,

\[
Q_{\mathrm W}(f,g)=\langle \Theta(f),\Theta(g)\rangle_{\mathscr S^{(2)}};
\]

3. primitive classes satisfy the Hodge inequality

\[
\langle \xi,\xi\rangle_{\mathscr S^{(2)}}\le 0;
\]

4. the Lefschetz trace of \(\Theta(f)\) recovers the unsmeared Weil distribution.

If such a principle were proved, the finite-to-infinite gap in Connes' approach would close.

## A Synthesized Proposal Combining the Strongest Elements

The strongest pieces of the six approaches fit together cleanly:

- `From the scaling site:` the correct ambient square and the Frobenius correspondences.
- `From Arakelov/adelic theory:` the correct format for globalizing infinitely many local metrics, namely an additive regularized height/intersection pairing.
- `From Kudla/Siegel-Weil:` the only known mechanism that turns a global theta lift into a positive arithmetic height whose Fourier coefficients still factor locally.

That leads to the following synthesized construction.

### Step 1. Define the primitive arithmetic correspondences

`PROPOSAL:` Build a category of admissible metrized correspondences on \(\mathscr S^{(2)}\). The primitive part is the orthogonal complement of the span of \(H_1,H_2\). This is the arithmetic analog of degree-zero divisors in Weil's proof and of primitive Neron-Severi classes in Hodge index theory.

### Step 2. Identify the local kernels with Connes' semilocal correction terms

`PROPOSAL:` At each place \(v\), the local metric is not an arbitrary Green function. It is the logarithmic kernel of the local correction operator in Connes' framework:

- at \(v=\infty\), the prolate/Toeplitz kernel from the 2021 archimedean positivity theorem;
- at finite \(p\), the local scattering/Hankel kernel encoded by \(\rho_p\) from the quasi-inner analysis.

This is what forces the finite \(S\) truncations to reproduce the semilocal forms already in the literature.

### Step 3. Globalize additively, not multiplicatively

`PROPOSAL:` The global pairing is the constant term at \(z=0\) of the Dirichlet-weighted sum of local primitive energies. This is the exact analogue of passing from local metrics to an adelic metrized line bundle. It also explains why the product ansatz fails: products remember the raw partial Euler product, while intersections are logarithmic in the metrics.

### Step 4. Use theta lifting to package the local data into a globally positive object

`PROPOSAL:` Introduce a theta kernel on the scaling-site square whose local components are the Weil-representation kernels already latent in the metaplectic/prolate formalism. The global theta lift should turn a test function \(f\) into \(\Theta(f)\in\mathrm{Corr}^{\mathrm{adm}}(\mathscr S^{(2)})_{\mathrm{prim}}\).

Then one seeks an arithmetic Siegel-Weil formula

\[
\langle \Theta(f),\Theta(g)\rangle
=
\text{Eisenstein/Weil term}(f,g),
\]

with the right-hand side identified with Connes' Weil distribution.

### Step 5. Eliminate harmonic smearing geometrically

`KNOWN:` Harmonic smearing appears when one tries to identify a weak limit of finite positive distributions with the global spectral distribution.

`PROPOSAL:` In the geometric pairing above, one never takes that weak limit. The zero distribution is recovered from the arithmetic Lefschetz trace of a **globally defined correspondence**. In other words, the no-smearing statement is not an auxiliary convergence theorem; it is built into the global intersection object itself. This is exactly why a geometric pairing is the right bridge.

## What Remains Conjectural vs. What Follows from Known Results

### What follows from known results

`KNOWN:` Connes reduced RH to positivity of the Weil distribution.

`KNOWN:` Connes-Consani proved the archimedean positivity theorem.

`KNOWN:` Connes-Consani proved quasi-innerity for finite products of local factors and Connes-Consani-Moscovici proved the stabilized semilocal Sonin-space picture.

`KNOWN:` The arithmetic site and scaling site provide a serious candidate for \(\operatorname{Spec}(\mathbf Z)\) as a curve over \(\mathbf F_1\), with Frobenius correspondences and tropical curve structure.

`KNOWN:` Connes-Consani's later *Riemann-Roch for Spec Z* shows that one-dimensional "absolute" geometry over \(\operatorname{Spec}(\mathbf Z)\) can support genuine cohomological and Euler-characteristic statements.

`KNOWN:` Arakelov/Faltings/Gillet-Soule/Yuan-Zhang show that a global arithmetic intersection pairing over all places can exist and can satisfy a Hodge index theorem, provided one has the right category of metrized cycles.

`KNOWN:` Kudla's program and Li-Liu's arithmetic inner product formula show that theta lifting can convert modular symmetry into a positive arithmetic height pairing with explicitly factorized local terms.

### What is still conjectural

`PROPOSAL:` The existence of an arithmetic Chow group of admissible correspondences on \(\mathscr S^{(2)}\).

`PROPOSAL:` The existence of local Green kernels on \(\mathscr S^{(2)}\) matching the prolate/Toeplitz and quasi-inner/Hankel correction operators place by place.

`PROPOSAL:` The constant-term regularized adelic sum formula for the global intersection pairing.

`PROPOSAL:` The theta lift \(\Theta\) from Connes' test functions to primitive correspondences on \(\mathscr S^{(2)}\).

`PROPOSAL:` An arithmetic Siegel-Weil formula on the scaling-site square identifying that height pairing with the Weil distribution.

`PROPOSAL:` A Hodge index theorem on \(\mathscr S^{(2)}\) strong enough to imply \(Q_{\mathrm W}(f,f)\ge 0\).

`PROPOSAL:` The claim that this geometric construction automatically removes Connes' harmonic-measure smearing. It is conceptually plausible, but not proved.

### What I think is the mathematically honest status

`PROPOSAL:` Approaches 1-5 do not separately solve the problem. But they isolate three indispensable ingredients:

1. a geometric square carrying Frobenius correspondences;
2. an adelic height/intersection formalism that is continuous in the all-place topology;
3. a theta/Siegel-Weil mechanism that manufactures positivity globally rather than placewise.

My proposal is simply the minimal hybrid that contains all three.

## Feasibility and Next Steps

### Feasibility assessment

- `Most plausible ambient object:` the scaling-site square.
- `Most plausible normalization technology:` adelic Arakelov intersection, especially in its metrized-line-bundle form.
- `Most plausible positivity engine:` arithmetic theta lifting and Siegel-Weil.
- `Main difficulty:` nobody has yet put those three pieces into the same category.

`PROPOSAL:` I would rate the proposal as mathematically coherent but very speculative. It is substantially more concrete than saying "there should be an arithmetic Hodge index theorem," because it specifies:

1. what the cycles should be;
2. what the local metrics should be;
3. why the globalization must be additive and regularized;
4. how modular/metaplectic symmetry could become a height pairing;
5. where the no-smearing statement is supposed to enter.

The hard part is that every genuinely decisive step is still conjectural.

### Immediate next steps

1. Formulate a precise candidate category \(\mathrm{Corr}^{\mathrm{adm}}(\mathscr S^{(2)})\) of metrized correspondences on the scaling-site square.
2. Show that finite truncations of the proposed local Green kernels recover the known semilocal correction operators \(K_S\) on the stabilized Sonin space.
3. Define the regularized adelic sum of local primitive energies and test whether it is independent of truncation order.
4. Construct the simplest nontrivial theta kernel on \(\mathscr S^{(2)}\) from the metaplectic/prolate representation already present in Connes-Consani-Moscovici.
5. Prove a toy arithmetic Siegel-Weil formula first for a single periodic orbit \(C_p\) or for a finite union of periodic orbits before attempting the full adele class space.
6. Formulate the primitive Hodge-index statement on \(\mathscr S^{(2)}\) in a way that makes sense even before full cycle theory exists.

### Best near-term research program

`PROPOSAL:` The most realistic path is not "prove RH from this tomorrow." It is:

1. build a tropical/adelic Deligne-pairing formalism on the scaling-site square;
2. identify Connes' semilocal forms as truncations of that pairing;
3. search for a metaplectic theta kernel whose height pairing matches those truncations;
4. only then ask for a Hodge index theorem.

If that program fails, it will likely fail for a precise reason. If it succeeds, it would finally produce the arithmetic object that all 28 investigations were circling: a global intersection pairing whose local shadows are Connes' semilocal positive forms and whose positivity survives the all-place limit.

## Bottom Line

`PROPOSAL:` The missing pairing should be an **adelically regularized, theta-theoretic, Arakelov-style intersection pairing on the square of the scaling site**. The square provides the Frobenius correspondences, adelic intersection theory supplies convergence under adding places, and theta/Siegel-Weil machinery is the best available explanation for how global positivity could emerge from local pieces that are not individually positive. I do not know a published construction of this object. But among the available ideas, this hybrid is the most plausible candidate for the arithmetic Hodge index theorem that Connes' Weil positivity program is still missing.
