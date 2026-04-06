# Tropical/Adelic Deligne Pairing on the Scaling-Site Square

## Status

This note gives a rigorous research sketch with explicit failure points, not a completed construction.

- `KNOWN` means supported by the supplied context files or by published literature checked during this session.
- `PROPOSED` means a mathematically coherent definition or extension suggested by those sources, but not found in that exact form in the literature.
- `CONJECTURE` means a missing theorem or identification that is currently essential.

## Sources Actually Used

### Prior investigation files

1. `current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/arithmetic-intersection/findings.md`
   Key inputs: `A Synthesized Proposal Combining the Strongest Elements`, especially the additive globalization, primitive correspondences, and local-kernel blueprint.
2. `current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/weil-positivity-bridge/findings.md`
   Key input: the exact obstruction is instability of the `S`-dependent inner products, not instability of the semilocal Sonin spaces.
3. `current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/geometric-bridge/findings.md`
   Key input: the square/intersection/Hodge-index gap is the central unresolved step in the `F_1`-geometry strategy.

### Published literature checked

1. Alain Connes, `Trace formula in noncommutative geometry and the zeros of the Riemann zeta function`, Selecta Math. 5 (1999).
2. Alain Connes, Caterina Consani, `Geometry of the arithmetic site`, Adv. Math. 291 (2016).
3. Alain Connes, Caterina Consani, `Geometry of the scaling site`, Selecta Math. 23 (2017).
4. Alain Connes, Caterina Consani, `Weil positivity and trace formula, the archimedean place`, Selecta Math. 27 (2021).
5. Alain Connes, Caterina Consani, `Quasi-inner functions and local factors`, J. Number Theory 226 (2021).
6. Alain Connes, Caterina Consani, Henri Moscovici, `Zeta zeros and prolate wave operators`, Ann. Funct. Anal. 15 (2024).
7. Alain Connes, Caterina Consani, `Hochschild homology, trace map and zeta-cycles`, Proc. Sympos. Pure Math. 105 (2023).
8. Omid Amini, Matthew Baker, `Linear series on metrized complexes of algebraic curves`, arXiv:1204.3508 / Math. Ann.
9. Omid Amini, Matthew Baker, Erwan Brugalle, Joseph Rabinoff, `Lifting harmonic morphisms I: metrized complexes and Berkovich skeleta`, Res. Math. Sci. 2 (2015).
10. Lars Allermann, Johannes Rau, `First steps in tropical intersection theory`, Math. Z. 264 (2010).
11. Kristin Shaw, `A tropical intersection product in matroidal fans`, SIAM J. Discrete Math. 27 (2013).
12. Andreas Mihatsch, `On tropical intersection theory`, Selecta Math. 29 (2023).
13. Walter Gubler, Klaus Kunnemann, `A tropical approach to non-archimedean Arakelov geometry`, Algebra Number Theory 11 (2017).

### Two search-result caveats

- I did **not** locate a published paper with the exact title `Metrized complexes of curves and tropical Deligne pairing`. The nearest checked Amini-Baker sources are items 8 and 9 above, and they are genuinely 1-dimensional.
- I did **not** locate a published paper devoted specifically to the square of the scaling site. The checked square theory is for the arithmetic site, not for the scaling site.

## Executive Diagnosis

`KNOWN:` Connes-Consani construct the scaling site `S` as a semiringed topos with structure sheaf of convex piecewise affine functions with integral slopes, and show that the corresponding geometric space behaves like a tropical curve. They develop the sheaf of fractions and Cartier divisors on `S`, and a detailed divisor/Jacobian/Riemann-Roch theory on each periodic orbit `C_p`.

`KNOWN:` Connes-Consani construct the square of the arithmetic site and its Frobenius correspondences. The square is a semiringed topos whose reduced structure sheaf is described by convex Newton polygons, and the Frobenius objects are best viewed as congruences/correspondences on that square, not as ordinary subvarieties in the scheme-theoretic sense.

`KNOWN:` Allermann-Rau, Shaw, Mihatsch, and Gubler-Kunnemann provide strong tropical and non-archimedean intersection technology, but they work for tropical cycles, polyhedral spaces, matroidal fans, tropical spaces, or Berkovich analytic spaces. None of these papers proves that a Grothendieck topos like `S^(2)` automatically carries such a theory.

`KNOWN:` The supplied obstruction analysis is correct: the semilocal Sonin spaces stabilize, but the semilocal inner products are weighted by partial Euler products. A global additive geometric pairing is therefore the right structural target.

`PROPOSED:` The right Step 1 object is not a literal classical Deligne pairing in the relative-curve sense. It is an Arakelov-style height/intersection pairing on primitive correspondence classes on a proposed scaling-site square

`S^(2) := S x_{F_1} S`,

defined as an extension of scalars of the reduced arithmetic-site square.

`CONJECTURE:` The missing theorem is a bivariant tropical/adelic intersection theory on that square, strong enough to make sense of `Delta`, `Psi^lambda`, local Green kernels, and a primitive Hodge index statement.

## Conventions

- `S` denotes the Connes-Consani scaling site.
- `S^(2)` denotes the **proposed** scaling-site square, obtained by scalar extension of the reduced arithmetic-site square to `R_+^max`.
- `H_1, H_2` denote the two factor directions.
- `Delta` denotes the diagonal correspondence.
- `Psi^lambda` denotes the scaling/Frobenius correspondence of ratio `lambda`.
- `CT_{z=0}` means constant-term regularization at `z=0`.

## A. Divisors / Correspondences on `S^(2)`

### KNOWN

- Connes-Consani prove that the scaling site is the semiringed topos `[0,\infty) \rtimes N^\times` with structure sheaf of convex piecewise affine functions with integral slopes, and that the adele-class quotient inherits a tropical-curve structure.
- In `Geometry of the scaling site`, Section `4.3` is explicitly titled `The sheaf of fractions and Cartier divisors`, so the 1-dimensional ambient site `S` itself does have a Cartier-divisor language.
- The same paper proves a genuine divisor theory on each periodic orbit `C_p = R_+^*/p^Z`, including `Div(C_p)/P`, theta functions, and a Riemann-Roch theorem.
- In `Geometry of the arithmetic site`, Connes-Consani construct the square of the arithmetic site, its reduced structure sheaf via convex Newton polygons, and Frobenius correspondences on that square.
- In that paper the Frobenius correspondences are naturally presented as congruences/correspondence objects on the square. This matters: the square theory is already more bivariant than ordinary cycle theory.
- `INFERENCE FROM CHECKED LITERATURE:` Connes-Consani 2023 use the scaling site as a parameter space for `zeta-cycles` and emphasize stability by coverings. This supports, but does not prove, the idea that correspondence-like data can live over the scaling site, though not yet on its square.

### PROPOSED

- Define

`S^(2) := (reduced arithmetic-site square) \otimes_B R_+^max`

as the natural square on which to tropicalize the arithmetic-site correspondences.

- Define `Delta` as the scalar extension of the diagonal correspondence on the reduced arithmetic-site square.
- Define `Psi^lambda` as the scalar extension of the Connes-Consani Frobenius correspondence of ratio `lambda`.
- Define `H_1` and `H_2` first as formal factor classes characterized by degree maps

`deg_i : Corr^1(S^(2)) -> R`,

rather than as honest fibers `S x {pt}` and `{pt} x S`; the literature does not yet supply a compact surface on which those fibers are actual Cartier divisors.
- For a correspondence `Gamma`, define its primitive projection by

`Gamma_0 := Gamma - deg_1(Gamma) H_1 - deg_2(Gamma) H_2`.

- On the periodic-orbit sector, the graph of scaling by `lambda = p^n` meets the diagonal along the whole orbit `C_p`, not at isolated points. So the correct analogue of `Gamma_{Frob^r} . Delta` is already suggesting an orbital/excess-intersection object, not a point count.

### CONJECTURE

- There is no published proof that `Delta` and `Psi^lambda` are Cartier divisors or codimension-one tropical cycles on `S^(2)`.
- There is no published Chow/Picard/bivariant theory on the scaling-site square into which these correspondences canonically fit.
- The specific mathematical gap is:

`Gap A1:` build a rigorous category `Corr^1(S^(2))` of codimension-one correspondence classes on the scaling-site square that contains `H_1`, `H_2`, `Delta`, and `Psi^lambda`, and is compatible with the arithmetic-site Frobenius correspondences after scalar extension.

## B. Tropical Intersection Theory on `S^(2)`

### KNOWN

- Allermann-Rau define tropical cycles, Cartier divisors, and divisor-cycle intersection products first on fans in `R^n` and then on abstract tropical cycles that are locally fan-like.
- Shaw constructs an intersection product for tropical cycles in matroidal fans, generalizing the Allermann-Rau product.
- Mihatsch develops a tropical intersection theory of `delta`-forms and currents that allows arbitrary, even non-rational, polyhedra with smooth coefficients, and proves that the wedge product can be computed both by Allermann-Rau diagonal intersection and by the fan displacement rule.
- Gubler-Kunnemann combine tropical intersection theory with `delta`-forms to build non-archimedean Green-current and local-height technology.

### PROPOSED

- Treat the reduced arithmetic-site square as supplying local polyhedral models via its Newton-polygon semiring. Then regard `S^(2)` as a tropical space only **after** choosing a polyhedral atlas extracted from that reduced square.
- On each chart, represent a divisor by a piecewise affine support function `phi`, define its tropical first Chern current by `dd'' phi`, and define

`(D_1 . D_2)_trop := integral_{S^(2)} c_1(D_1) ^ c_1(D_2)`

in the sense of tropical `delta`-forms.
- Normalize the factor classes so that

`(H_1 . H_2)_trop = 1`

if and only if the projection formula identifies each factor direction as degree one against the opposite factor. This is a normalization choice, not a theorem from the literature.
- The diagonal self-intersection should not be assigned a number by analogy alone. The right guess is an adjunction-type formula

`(Delta . Delta)_trop = - chi_trop(S)`

after a suitable compactification or boundary formalism, but neither `chi_trop(S)` nor the needed compactification theory is currently available for the full scaling site.
- For `Delta . Psi^lambda`, the periodic-orbit geometry forces a Lefschetz-density interpretation:
  generic `lambda` should have no resonant periodic-orbit contribution;
  `lambda = p^n` should contribute an excess-intersection term supported on `C_p`;
  boundary or non-periodic sectors may contribute separate archimedean/continuous terms.

### CONJECTURE

- Standard tropical intersection theory does **not** automatically apply because `S^(2)` is not a standard tropical variety, fan, or Berkovich skeleton; it is a semiringed topos.
- There is no published excess-intersection formalism for a 1-dimensional fixed locus like `C_p` inside the would-be surface `S^(2)`.
- The specific mathematical gaps are:

`Gap B1:` produce a polyhedral/tropical atlas for `S^(2)` compatible with the topos structure and with the arithmetic-site Newton-polygon model.

`Gap B2:` prove an excess-intersection or Lefschetz-index formula for `Delta` against `Psi^lambda`, where the resonant fixed locus is an orbit, not a finite set of points.

`Gap B3:` define and compute `Delta^2` in a compactified or renormalized tropical surface theory adapted to the scaling site.

## C. Line Bundles and Metrized Line Bundles

### KNOWN

- On the scaling site `S`, Connes-Consani explicitly develop the sheaf of fractions and Cartier divisors.
- In tropical geometry, Cartier-divisor data are encoded by piecewise affine transition functions/support functions, and Mihatsch/Gubler-Kunnemann provide a `delta`-form language for first Chern classes.
- Gubler-Kunnemann prove a non-archimedean Poincare-Lelong formula representing the first Chern current of a formally metrized line bundle by a `delta`-form, and construct Green-current star-products for divisors.
- `INFERENCE FROM CHECKED LITERATURE:` Amini-Baker's metrized-complex framework is genuinely useful for the **1-dimensional** pieces: metric-graph geometry enhanced by algebraic-curve data, divisor theory, harmonic morphisms, and specialization/lifting. It is relevant to the periodic orbits `C_p` and their coverings, but this relevance is analogical/orbitwise rather than a published identification.

### PROPOSED

- Define `Pic_trop(S^(2))` as Cartier divisor classes on the proposed tropical/topos square, locally modeled by piecewise affine support functions on the polyhedral charts coming from the reduced arithmetic-site square.
- Define an adelically metrized tropical line bundle as

`Lhat = (L, {g_v}_v)`,

where `L` is a class in `Pic_trop(S^(2))` and `g_v` is a local Green object for the place `v`.
- Define degrees by the factor classes:
  `deg_1(L) := (L . H_2)_trop`,
  `deg_2(L) := (H_1 . L)_trop`,
  whenever the tropical product exists.
- Use the primitive subgroup

`Pic_trop(S^(2))_0 := ker(deg_1) cap ker(deg_2)`

as the analogue of the primitive Neron-Severi part.
- Use the Amini-Baker framework only orbitwise: it can model the local 1-dimensional pieces `C_p`, coverings of `C_p`, and divisor/harmonic data on those pieces, but not the full square.

### CONJECTURE

- There is no published Picard group, Neron-Severi group, or metrized-line-bundle theory for `S^(2)`.
- There is no published 2-dimensional analogue of the metrized-complex formalism that would naturally produce a tropical Deligne pairing on a square of hybrid objects.
- The specific mathematical gaps are:

`Gap C1:` construct `Pic_trop(S^(2))` and show that `H_1`, `H_2`, `Delta`, and `Psi^lambda` define classes in it.

`Gap C2:` define a notion of admissible metric on a line bundle over a semiringed topos/tropical space like `S^(2)`.

`Gap C3:` build a 2-dimensional replacement for the Amini-Baker metrized-complex formalism, since the checked Amini-Baker literature is only 1-dimensional.

## D. Local Green Kernels

### KNOWN

- Connes-Consani 2021 prove the archimedean positivity statement and express the difference between the Weil distribution and the compressed scaling trace in terms of prolate spheroidal functions and Hermitian Toeplitz matrices.
- Connes-Consani 2021 also prove that no individual non-archimedean ratio `rho_p` is quasi-inner; quasi-innerity is recovered only for finite products after splitting the archimedean factor via Gauss multiplication.
- Connes-Consani-Moscovici 2024 prove that semilocal Sonin spaces stabilize as vector spaces while the Hilbert structure depends on the weighted measure

`dm_S(s) = |prod_{v in S} L_v(1/2 - i s)|^2 ds`.

- Gubler-Kunnemann provide the exact local-height technology one would want abstractly: first Chern `delta`-forms, Green currents, star-products, and local heights for divisors.

### PROPOSED

- At `v = infinity`, define a primitive Green kernel `g_infty^prim` by extracting from the Connes-Consani archimedean operator the kernel representing

`(Weil distribution) - (compressed scaling trace)`,

then removing the factor-class directions `H_1` and `H_2`.
- At a finite prime `p`, define `g_p^prim` from the Hankel/scattering defect of multiplication by `rho_p`, again after primitive/vacuum subtraction.
- For primitive correspondences `D_0, D_1`, define local energies

`E_v^prim(D_0, D_1) := <D_0, g_v^prim D_1>_ren`.

- Interpret the archimedean Toeplitz/prolate term and the non-archimedean Hankel/scattering terms as the metrics of an adelically metrized object only **after** primitive renormalization. This matches the supplied obstruction analysis: the bad divergence lies in the factor directions and in the multiplicative assembly, not in the stabilized primitive vector space itself.

### CONJECTURE

- None of the checked papers constructs these kernels as Green functions on `S^(2)`.
- The finite-prime kernels are especially problematic: the literature proves quasi-innerity only after finite archimedean compensation, so a placewise positive metric `g_p` is not actually available.
- The specific mathematical gaps are:

`Gap D1:` extract the archimedean prolate/Toeplitz correction as an honest Green kernel on a geometric realization of `S^(2)`.

`Gap D2:` define a renormalized finite-prime Green kernel `g_p^prim` despite the fact that `rho_p` is not quasi-inner by itself.

`Gap D3:` prove summable or zeta-regularizable asymptotics for `E_p^prim` as `p -> infinity`.

## E. The Global Tropical/Adelic Deligne Pairing

### KNOWN

- The right globalization must be additive, not multiplicative. This is the main lesson of the supplied obstruction analysis and it matches the architecture of Arakelov intersection theory.
- Gubler-Kunnemann show that tropical/non-archimedean local heights can be assembled from Green-current star-products, at least in the divisor setting.
- Classical Deligne pairing is a relative-dimension-one construction. The requested formula on `S^(2)` is therefore closer in spirit to an Arakelov height/intersection pairing on a surface than to a published literal Deligne pairing.

### PROPOSED

- Let `CH^1_trop,ad(S^(2))` denote admissibly metrized codimension-one correspondence classes on the proposed square.
- For primitive metrized classes `Lhat_0, Lhat_1`, define

`<Lhat_0, Lhat_1> := (L_0 . L_1)_trop + CT_{z=0} Sum_v N(v)^(-z) E_v^prim(Lhat_0, Lhat_1).`

- Here the admissibility conditions should be:
  almost all finite primes contribute a trivial or asymptotically controlled primitive correction;
  the Dirichlet-regularized sum has a well-defined constant term at `z=0`;
  principal divisors pair trivially after combining tropical and local terms.
- This is the exact place where the tropical and adelic pieces meet:
  the tropical term supplies the geometric intersection on the would-be surface;
  the local energies supply the metrized correction;
  constant-term regularization replaces the divergent multiplicative Euler-product weighting.

### CONJECTURE

- There is no published proof that this formula is well defined on a completed primitive Chow group of `S^(2)`.
- There is no published proof of bilinearity, symmetry, independence of regularization scheme, or compatibility with principal correspondences.
- The specific mathematical gaps are:

`Gap E1:` define `CH^1_trop,ad(S^(2))` rigorously enough that the pairing descends to classes.

`Gap E2:` prove that the constant-term prescription is canonical and independent of ordering/truncation of places.

`Gap E3:` prove a Hodge-index-type negativity statement on the primitive part of this pairing.

## F. The Critical Test: Recovering Connes' Trace Formula and the Semilocal Forms

### KNOWN

- In the function-field case, Weil's proof uses the intersection number `Gamma_{Frob^r} . Delta`.
- `INFERENCE FROM CONNES 1999 + CONNES-CONSANI:` In the number-field framework, the geometric side should be read as a trace formula over periodic prime orbits plus archimedean terms, not as a fixed-point count on a finite set.
- The supplied obstruction analysis shows that the finite semilocal quadratic forms exist and are positive, but their all-place limit is not controlled because the inner products are weighted by partial Euler products and weak limits can retain only harmonic-measure smearing.

### PROPOSED

- Define the correspondence-valued distribution

`Gamma(f) := integral_{R_+^*} f(lambda) Psi^lambda d^*lambda`

and its primitive part

`Gamma_0(f) := Gamma(f) - deg_1(f) H_1 - deg_2(f) H_2`.

- The key expected identity is not a pointwise formula for every `lambda`, but a distributional one:

`<Psi^lambda_hat, Delta_hat>`

should be a Lefschetz/intersection distribution in `lambda`, supported on resonant values `lambda = p^n` together with the needed boundary/archimedean correction terms.
- After integrating against a test function `f`, the result should reproduce the geometric side of Connes' trace formula.
- For a finite place set `S`, truncating the local-energy sum in the global pairing should recover the semilocal positive forms from Connes/Connes-Consani/Connes-Consani-Moscovici.
- Then define

`Q_W(f,g) := - <Gammahat_0(f), Gammahat_0(g)>`.

If a primitive Hodge index theorem held for this pairing, `Q_W` would be the sought-after Weil form.

### CONJECTURE

- No checked paper proves that `<Psi^lambda_hat, Delta_hat>` equals the prime-orbit distribution in Connes' trace formula.
- No checked paper proves that finite truncations of the proposed pairing recover the semilocal forms exactly.
- No checked paper proves that the resulting distribution is the **unsmeared** Weil distribution rather than its harmonic extension.
- The specific mathematical gaps are:

`Gap F1:` prove a Lefschetz trace theorem on `S^(2)` identifying `Delta . Psi^lambda` with Connes' orbital trace terms.

`Gap F2:` prove semilocal compatibility: finite truncations of the adelic pairing must match the existing semilocal positive forms.

`Gap F3:` prove that the global pairing recovers the unsmeared Weil distribution, thereby bypassing the harmonic-measure-smearing obstruction rather than merely repackaging it.

## Bottom Line

`INFERENCE FROM CHECKED LITERATURE:` There is enough published structure to justify the **ambient idea**:
the scaling site gives the right 1-dimensional tropical object,
the arithmetic-site square gives the right correspondence template,
and tropical/non-archimedean intersection theory explains what a metrized additive pairing should look like.

`PROPOSED:` A mathematically coherent Step 1 object is:

`<Lhat_0, Lhat_1> = (L_0 . L_1)_trop + CT_{z=0} Sum_v N(v)^(-z) E_v^prim(Lhat_0, Lhat_1),`

with primitive correspondence classes on a proposed scaling-site square.

`CONJECTURE:` The construction is not yet rigorous because the literature still lacks:
1. a bona fide square `S^(2)` with usable codimension-one correspondence theory,
2. a local Green-kernel interpretation of the Connes corrections on that square,
3. a Lefschetz/Hodge-index formalism strong enough to turn the pairing into Weil positivity.

## Hardest Open Problems

1. Construct a rigorous bivariant Chow/Picard theory for the scaling-site square itself, not just for the periodic orbits `C_p` or for the arithmetic-site square before scalar extension.
2. Build an excess-intersection/Lefschetz-index formalism for `Delta` against `Psi^lambda`, where resonant fixed loci are whole periodic orbits and not isolated points.
3. Extract the archimedean Toeplitz/prolate correction and the finite-prime Hankel/scattering corrections as genuine local Green kernels on `S^(2)`, with a place-by-place primitive renormalization that is canonically summable.
4. Prove that the regularized additive pairing recovers the existing semilocal positive forms at finite level and the unsmeared Weil distribution globally.
5. Prove a primitive Hodge index theorem for the resulting adelically metrized correspondence classes, since that is the point where RH would finally enter as a positivity theorem rather than as a hidden convergence assumption.
