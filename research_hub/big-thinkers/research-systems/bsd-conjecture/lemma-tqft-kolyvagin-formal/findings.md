# Lemma: TQFT Gluing Implies Kolyvagin Recursion -- Formal Write-Up

**Date:** 2026-04-04
**Status:** IN PROGRESS -- preliminary verdict GAP (see Section IX). Most decisive finding: Park-Park's paper does NOT define observables, correlators, or insertion operators; their gluing theorem is purely a partition-function identity. The schematic write-up in route-bf-kolyvagin-system implicitly assumes the existence of objects that the cited source does not construct.
**Predecessors:**
- `../route-bf-kolyvagin-system/findings.md` (the schematic version)
- `../final-audit/codex-audit.md` (the audit identifying it as schematic)
- `../normalization-check/findings.md` (sign analysis: epsilon = +1, definitionally tautological)
- `../verify-mcs-hypotheses/findings.md` (MCS hypotheses verified for good ordinary)

**Sources verified by direct PDF inspection (this run):**
- arXiv:2603.23978 (Macias Castillo-Sano), `pdftotext` output saved to `/tmp/mcs.txt`
- arXiv:2602.19621 (Park-Park), `pdftotext` output saved to `/tmp/pp.txt`
- Mazur-Rubin Memoirs 168 #799 (via cornut.imj-prg.fr mirror), saved to `/tmp/mr.txt`

---

## Executive Summary

The schematic claim in `route-bf-kolyvagin-system/findings.md` is:

> "Park-Park BF theory has a TQFT gluing axiom (their Theorem 5.12). The Poitou-Tate exact sequence is a special case of this gluing. The connecting homomorphism delta gives the Kolyvagin recursion. Therefore the BF observables produce a Kolyvagin system."

After reading the actual sources, the situation is the following:

1. **Park-Park (arXiv:2602.19621) does NOT define BF observables, BF correlators, or insertion operators.** A keyword search on the verbatim text of the PDF for "observable", "insertion", "correlator", or "correlation" returns ZERO matches. Their Theorem 5.12 is a gluing identity for partition functions Z_X (Definition 5.7), where X is a "global field" and S, T are finite subsets of closed points. The gluing relates Z_{X_S} to a pairing of Z_{X_T} with Z_{∂X_{T∖S}^*}. There is no insertion of local data at a single Kolyvagin prime.

2. **The Park-Park "partition function" is a complex scalar, not a determinantal element of det(SC).** Definition 5.7 sets Z_X := Σ_ρ exp(2π i · BF_X(ρ)) ∈ C, summed over the (finite) set of "fields" F(X). Proposition 6.5 evaluates this to |π(Sel(M,W))| · |Sel(M_1^∨, W_1^⊥)|. This is a CARDINALITY, not a determinant module element. The bridge "Z_BF = τ(SC) ∈ det(SC)" repeated throughout `route-bf-kolyvagin-system` is not in the Park-Park paper.

3. **The "TQFT gluing = Poitou-Tate" identification is asserted but not literally proved in Park-Park.** Theorem 5.12 is proved via a pullback-square commutative-cube argument over the BF "field" sets F(X_S, α), F(X_T, α⊕γ). The proof identifies F(X_S, α) ≅ ⊔_γ F(X_T, α⊕γ) × BC(∂X_S, γ) (a fibration of finite sets) and uses the integral-formula structure of Definition 5.7. It is NOT phrased as a Poitou-Tate exact sequence statement. The Cassels-Tate connection appears only in Section 6 via Proposition 6.5 (counting argument).

4. **MCS Theorem 3.4 is a real, precise theorem -- but it lands in the wrong type for what the schematic argument claims.** Theorem 3.4 gives an isomorphism det⁻¹(RΓ̃_F(K,T))/π^n ≅ SS_χ(F)(A_n, F, P), where SS_r is a module of "Stark systems" defined as an inverse limit of exterior biduals ∧^{r+ν(n)} H¹_{F^n}(K,A_n) tensored with duals of the singular quotients (Definition 3.2). This is NOT a Kolyvagin system in the sense of Mazur-Rubin Definition 3.1.3. To get a Kolyvagin system one would need a separate Stark-to-Kolyvagin map (the Burns-Sakamoto-Sano "Kolyvagin derivative"), and that map is not exhibited in MCS.

5. **The Mazur-Rubin Kolyvagin recursion uses a SPECIFIC operator φ^fs_ℓ (the finite-singular comparison map), not just the Poitou-Tate connecting homomorphism.** Definition 1.2.2 of Mazur-Rubin defines φ^fs_ℓ as a composition involving Q(Fr⁻¹), where Q(x) is the polynomial with (x-1)Q(x) = det(1 - Fr · x | T). This Frobenius polynomial twist is what makes Kolyvagin classes work. The Poitou-Tate connecting map alone is not φ^fs_ℓ.

**Verdict:** [GAP]. The "TQFT gluing → Kolyvagin recursion" claim cannot be derived from the cited Park-Park theorem because Park-Park does not have the relevant input objects (no observables, no determinantal Z_BF, no Poitou-Tate-stated gluing). The argument as written conflates four distinct things: (a) Park-Park's complex-valued partition function gluing, (b) the conjectural extension of this to a determinantal observable theory, (c) the Poitou-Tate exact sequence, and (d) the Mazur-Rubin finite-singular comparison map. These are NOT the same and the equivalences are nontrivial. See Section IX for the precise obstruction list.

---

## I. Verbatim Statements of the Source Theorems

This section records the actual statements, with line references to the extracted PDF text files in `/tmp/`.

### I.1 Mazur-Rubin Definition 3.1.3 (Kolyvagin system) [/tmp/mr.txt:991-1001]

> **Definition 3.1.3.** A Kolyvagin system for (T, F, P) is a global section (over X(P)) of the Selmer sheaf H_{(T,F,P)}. We write KS(T, F, P) ... Concretely, a Kolyvagin system for (T, F, P) is a collection of cohomology classes
>
>     {κ_n ∈ H¹_{F(n)}(Q, T/I_n T) ⊗ G_n : n ∈ N}
>
> such that if ℓ is prime and nℓ ∈ N,
>
>     (κ_{nℓ})_{ℓ,s} = φ^fs_ℓ(κ_n)    in H¹_s(Q_ℓ, T/I_{nℓ}T) ⊗ G_{nℓ}.    (5)

**The Selmer sheaf** is defined at [/tmp/mr.txt:973-989]: H(n) := H¹_{F(n)}(Q, T/I_n T) ⊗ G_n, with the edge map ψ^e_n : H(n) → H¹_s(Q_ℓ, T/I_{nℓ}T) ⊗ G_{nℓ} given by **localization at ℓ followed by φ^fs_ℓ**.

So the Kolyvagin recursion is the equation:

  **loc^s_ℓ(κ_{nℓ}) = φ^fs_ℓ(loc_ℓ(κ_n))**

in H¹_s(Q_ℓ, T/I_{nℓ}T) ⊗ G_{nℓ}, where loc_ℓ on the right-hand side projects κ_n into H¹_f(Q_ℓ, T/I_{nℓ}T) ⊗ G_n (because κ_n ∈ H¹_{F(n)} which has the FINITE condition at ℓ since ℓ does not divide n).

### I.2 Mazur-Rubin Definition 1.2.2 (the finite-singular comparison map φ^fs_ℓ) [/tmp/mr.txt:513-526]

> **Definition 1.2.2.** Suppose that T is free of finite rank as an R-module, and that det(1 − Fr | T) = 0. Define P(x) ∈ R[x] by
>
>     P(x) = det(1 − Fr · x | T).
>
> Since P(1) = 0, there is a unique polynomial Q(x) ∈ R[x] such that (x − 1)Q(x) = P(x) in R[x]. By the Cayley-Hamilton theorem, P(Fr) annihilates T, so Q(Fr⁻¹)T ⊂ T^{Fr=1}.
>
> We define the finite-singular comparison map φ^fs_ℓ on T to be the composition, using the isomorphisms of Lemma 1.2.1,
>
>     H¹_f(K, T) ≅ T/(Fr − 1)T --Q(Fr⁻¹)→ T^{Fr=1} ≅ H¹_s(K, T) ⊗ F^×.

**This is the load-bearing operator in the recursion.** It is NOT a connecting homomorphism in any obvious exact sequence; it is built explicitly from the Frobenius polynomial. The factor "⊗ G_ℓ = ⊗ F^×_ℓ = ⊗ Gal(Q(μ_ℓ)/Q)" in the target is essential -- this is the source of the "G_n" factor in the Selmer sheaf.

### I.3 Mazur-Rubin Theorem 5.2.10 (freeness) [/tmp/mr.txt:2867-2874]

> **Theorem 5.2.10.**
> (i) If χ(T) = 0 then KS(T) = 0.
> (ii) If χ(T) = 1 then KS(T) is a free R-module of rank one, generated by a κ ∈ KS(T) whose image in KS(T̄) is nonzero.

This is a freeness result for the **classical Mazur-Rubin Kolyvagin system module**, with the recursion as in Definition 3.1.3. To use this in the BF setting, one must first produce an honest element of KS(T) -- not of the MCS Stark system module SS_r.

### I.4 MCS Theorem 3.4 [/tmp/mcs.txt:1326-1333]

> **Theorem 3.4.** We fix the data F = (F_v)_{v∈Sp} ... and let RΓ̃_F(K,T) be the associated Selmer complex (see Definition 2.2). ... Assume Hypothesis 2.11 and that N contains a core vertex for F on A_n with χ(F) = χ(F) (so Hypothesis 2.17 is also satisfied). Then there is a canonical isomorphism
>
>     ϖ_n : det⁻¹_R(RΓ̃_F(K,T))/π^n = det⁻¹_{R_n}(O/π^n O ⊗^L_O RΓ̃_F(K,T)) →∼ SS_{χ(F)}(A_n, F, P).

**The target SS_{χ(F)} is the Stark system module of Definition 3.2** [/tmp/mcs.txt:1264-1273]:

> **Definition 3.2** (See [BSS25, §4.1]). Let r ≥ 0. The module of Stark systems of rank r for (A_n, F, P) is defined by
>
>     SS_r(A_n, F, P) := lim_{n∈N} ( ∧^{r+ν(n)}_{R_n} H¹_{F^n}(K, A_n) ⊗_{R_n} ⊗_{q|n} H¹_{/F}(K_q, A_n)* )

where ∧^k denotes the k-th exterior bidual (notation of Burns-Sakamoto), and the inverse limit is over m | n in N with maps v_{n,m}.

**This is NOT the same as the Kolyvagin system module KS(T, F, P).** Stark systems live in exterior powers; Kolyvagin systems live in H¹ ⊗ G_n. The maps φ^fs_ℓ that define a Kolyvagin system have NO direct counterpart in the Stark system definition (which uses inclusion-by-norms maps v_{n,m} instead).

### I.5 MCS Theorem 2.20 [/tmp/mcs.txt:759-789]

> **Theorem 2.20.** Assume Hypotheses 2.11 and 2.17. Let C_PT be the Poitou-Tate complex in Definition 2.7 (see also Remark 2.10). Then there exists a canonical quasi-isomorphism ϕ : C_PT → C_Nek/π^n such that the following diagrams are commutative:
>
>     [degree 1: H¹_F(K,A_n) → H¹(C_Nek)/π^n  via κ_1 (no sign), then to H¹(C_Nek/π^n) via H¹(ϕ)]
>     [degree 2: H¹_{F*}(K, A_n*(1))* → H²(C_Nek)/π^n via -κ_2 (NEGATIVE sign), then to H²(C_Nek/π^n) via H²(ϕ)]

The negative sign at degree 2 is the source of the −κ_2 cited in `normalization-check/findings.md`. It does not affect the Kolyvagin recursion (which is a degree-1 statement), but it does mean that **the comparison between Nekovar's Selmer complex and the Poitou-Tate complex is not just "the same object"** -- it is a quasi-isomorphism with a nontrivial degree-2 sign.

### I.6 MCS Hypothesis 2.11 [/tmp/mcs.txt:539-545]

> **Hypothesis 2.11.**
> (i) H⁰(K, A) = H⁰(K, T^∨(1)) = 0.
> (ii) H⁰(K_v, T_v^−) = 0 for any v ∈ S_p.
> (iii) H⁰(K_v, A_v^−) = H⁰(K_v, (T_v^+)^∨(1)) = 0 for any v ∈ S_p.
> (iv) H¹_ur(K_v, T) = H¹_f(K_v, T) for any finite place v with v ∉ S_p.

For T = T_p(E) with E/Q good ordinary at p, p odd, p non-anomalous, p ∤ #E(Q)_tors · Tam(E) · #Ẽ(F_p), and ρ̄ irreducible: SATISFIED (verified in `verify-mcs-hypotheses/findings.md`).

### I.7 MCS Definition 2.16 (core vertex) [/tmp/mcs.txt:679-693]

> **Definition 2.16.** Let n be a square-free product of places of K which do not belong to S_∞ ∪ S_p ∪ S_ram(T). We say that n is a core vertex for F on A_n if
> - H¹_{F^n}(K, A_n) is a free R_n-module,
> - H¹_{/F}(K_v, A_n) is a free R_n-module for every v | n, and
> - H¹_{(F^n)*}(K, A_n*(1)) = 0.

### I.8 Park-Park Definition 5.7 (BF partition function) [/tmp/pp.txt:1572-1577]

> **Definition 5.7.** We define
>
>     Z_X := Σ_{ρ∈F(X)} exp(2π i · BF_X(ρ)) ∈ C.
>
> Since F(X) is finite by Remark 5.6, this sum is finite.

**Note:** Z_X is a COMPLEX NUMBER, not an element of det(SC). It is defined as a finite sum of phase factors over the set F(X) of "fields" (in the BF-theory sense, i.e., a discrete set of fppf cohomology data). This is critical: the schematic write-up in `route-bf-kolyvagin-system` repeatedly identifies Z_BF with τ(SC(T)) ∈ det(SC). **Park-Park do not make this identification, anywhere in the paper.**

### I.9 Park-Park Theorem 5.12 (gluing formula) [/tmp/pp.txt:1695-1705]

> **Theorem 5.12 (Gluing formula).** Let S ⊆ T ⊆ Y^cl be finite subsets.
> (1) If S ≠ ∅, then the following equality holds in H_S:
>
>     Z_{X_S} = ⟨ Z_{X_T} , Z^{∂X_S}_{(T∖S)^*} ⟩.
>
> (2) If S = ∅, X∖Y ⊆ T, and the order of M is invertible on Y_T, then the following equality holds in C:
>
>     Z_X = ⟨ Z_{X_T} , Z^{∂X_T}_{T^*} ⟩.

The pairing ⟨·,·⟩ is defined just before [/tmp/pp.txt:1683-1692] via the canonical evaluation map H_T ⊗ H_{(T∖S)^*} → H_S, where H_S, H_T are Hilbert spaces of functions on the "boundary field" sets F_S, F_T.

**Crucial structural observation:** The gluing relates Z on X_S (the scheme cut along the LARGER set S) to Z on X_T (cut along T ⊃ S). It does NOT insert local data at a single prime ℓ. To "insert ℓ" you would set T = S ∪ {ℓ} and read the gluing as expressing Z_{X_S} in terms of Z_{X_{S∪{ℓ}}}. This gives a relation between two partition functions, but the resulting equation is between COMPLEX NUMBERS (or more precisely, sections of Hermitian line bundles on the "boundary field" spaces F_S, F_T). It does not, by itself, produce a cohomology class κ_{nℓ} ∈ H¹_{F(nℓ)}(Q, T/I_{nℓ}T).

### I.10 Park-Park Proposition 6.5 [/tmp/pp.txt:2058-2061]

> **Proposition 6.5.** Under the same assumption as Proposition 6.3, we have
>
>     Z_X = |π(Sel(M, W))| · |Sel(M_1^∨, W_1^⊥)|.

This is the punchline of the paper: the BF partition function counts (the relevant part of) the Selmer group. **Z_X is a positive integer** (a cardinality), not a Lambda-adic determinantal object. It carries no Iwasawa-theoretic information by itself; the schematic claim "Z_BF = char(X) under IMC" is not in Park-Park.

---

## II. The Type Mismatches the Schematic Argument Hides

I now spell out exactly where the chain in `route-bf-kolyvagin-system/findings.md` jumps types.

### II.1 Mismatch 1: Park-Park's Z is a scalar; det(SC) is a module

| Object | Lives in | Source |
|---|---|---|
| Park-Park Z_X (Def 5.7) | C | /tmp/pp.txt:1572 |
| Park-Park Z_X (Prop 6.5) | Z_{>0} (a cardinality) | /tmp/pp.txt:2061 |
| MCS det⁻¹(RΓ̃_F(K,T))/π^n | (free) R_n-module | /tmp/mcs.txt:1326 |
| MCS Stark system ε^BF | element of SS_{χ(F)}(A_n,F,P) | /tmp/mcs.txt:1264 |
| Mazur-Rubin κ_n | element of H¹_{F(n)}(Q,T/I_nT) ⊗ G_n | /tmp/mr.txt:996 |

The schematic argument writes Z_BF in det⁻¹(SC) and applies MCS Theorem 3.4 to get a Stark system. But:

- **Park-Park's Z_X is not in det⁻¹(SC).** It is a complex number (or a section of a Hermitian line bundle on F_S, in the relative version). There is no published or even sketched map "Park-Park Z → MCS det⁻¹(SC) basis."

- **What the schematic write-up needs is an UPGRADE of Z_X from a number to a determinant generator.** This upgrade would be a separate construction. It is not in either paper. It may be plausible (e.g., "the BF action exponentiates to give a section of the determinant line of cohomology, and Z_X is its trace") but it would have to be MADE precise. The Park-Park paper does not make it precise.

### II.2 Mismatch 2: MCS gives Stark systems, not Kolyvagin systems

The MCS isomorphism (Theorem 3.4) lands in SS_{χ(F)}(A_n, F, P), the module of Stark systems. A Stark system of rank r is, by Definition 3.2, an inverse system

   ε = (ε_n)_{n∈N},  ε_n ∈ ∧^{r+ν(n)}_{R_n} H¹_{F^n}(K, A_n) ⊗ ⊗_{q|n} H¹_{/F}(K_q, A_n)*

with the inclusion-by-norms compatibility. **Stark systems and Kolyvagin systems are different objects, with different transfer maps.** The Stark system uses the map v_{n,m} from Lemma 3.1 of MCS, which is a "norm/restriction" map on exterior powers, NOT the Mazur-Rubin finite-singular comparison φ^fs_ℓ.

To pass from Stark to Kolyvagin one needs the **Burns-Sakamoto-Sano "Kolyvagin derivative" map** D : ES_r → KS_r (Burns-Sakamoto-Sano arXiv:1805.08448). This map is itself nontrivial:

- For r = 1 it is essentially the higher rank generalization of the classical Kolyvagin "derivative" sum over G_n.
- It produces classes whose recursion is built from φ^fs_ℓ -- but the proof that the result satisfies (5) of Mazur-Rubin Definition 3.1.3 uses **the distribution relations of the Euler system**, which Stark systems do NOT automatically satisfy. (Stark systems satisfy a "norm relation in exterior powers," which is weaker.)

In fact, the Burns-Sakamoto-Sano construction goes Euler system → Stark system → Kolyvagin system, not Stark → Kolyvagin directly without an Euler system input. Whether the Stark system from MCS Theorem 3.4 (which is constructed abstractly from det(SC), not from an Euler system) can be fed into Burns-Sakamoto-Sano is **unestablished**. The MCS paper itself notes (Section 1.4 of MCS, see /tmp/mcs.txt:280-300) that they give an alternative path going directly from Stark to Fitting ideals **bypassing Kolyvagin systems**. This is explicit: MCS does not produce a Kolyvagin system.

### II.3 Mismatch 3: Poitou-Tate connecting map ≠ φ^fs_ℓ

The Mazur-Rubin Kolyvagin recursion is

   (κ_{nℓ})_{ℓ,s} = φ^fs_ℓ((κ_n)_ℓ)

where the right-hand side is `Q(Fr⁻¹)` applied to the finite localization of κ_n. The polynomial Q is defined by

   (x - 1) Q(x) = det(1 - Fr · x | T)

so Q(Fr⁻¹) is essentially "the rest of the Frobenius polynomial after dividing out (Fr − 1)". This is a SPECIFIC operator on T^{Fr=1}, NOT the abstract connecting homomorphism in the Poitou-Tate exact sequence.

The schematic argument identifies the Poitou-Tate connecting map δ : H¹_s(Q_ℓ, T/I_ℓT) → H²_F(Q, T/I_ℓT) with the Kolyvagin recursion. But:

- δ is a SECOND-ORDER cohomology object: source H¹_s, target H².
- φ^fs_ℓ is a first-order operator: source H¹_f, target H¹_s ⊗ G_ℓ.
- These have different source and target. They are not the same map.

The actual relationship between φ^fs_ℓ and Poitou-Tate is more subtle. Mazur-Rubin Lemma 1.2.4 [/tmp/mr.txt:558-576] uses the existence of a "transverse" subgroup H¹_{tr}(K_v, T) ⊂ H¹(K_v, T) which projects isomorphically onto H¹_s, giving a SPLITTING H¹ = H¹_f ⊕ H¹_{tr}. This splitting depends on a choice of totally tamely ramified extension L/K (taken to be K(μ_ℓ) for K = Q_ℓ). The map φ^fs_ℓ then identifies H¹_f with H¹_{tr} ⊗ G_ℓ via a Frobenius-polynomial twist.

**This is structural data not present in the Poitou-Tate exact sequence.** Poitou-Tate gives the existence of a long exact sequence; it does NOT give the splitting H¹ = H¹_f ⊕ H¹_{tr} or the map Q(Fr⁻¹). Those come from local Galois cohomology of unramified representations.

So even granting all the upstream type matches, "the TQFT gluing axiom IS the Poitou-Tate exact sequence" still does not give "the gluing axiom IS the Kolyvagin recursion." It gives at most an exact sequence; the Kolyvagin recursion adds the φ^fs_ℓ structure on top.

### II.4 Mismatch 4: TQFT inserting "an observable at ℓ" has no source meaning

In the schematic write-up, "BF observable insertion at ℓ" is the central construct. It is supposed to be a map that, given a Selmer complex, modifies it by relaxing the local condition at ℓ.

**The phrase does not appear in Park-Park.** Their Theorem 5.12 relates Z_{X_S} to Z_{X_T} for two SETS of cut points S ⊂ T, via a bilinear pairing of partition functions. There is no notion of "observable", "insertion", "n-point function", or "correlator" anywhere in the paper. (Verified by literal grep.)

The ANALOGY with QFT observables is suggestive: in a TQFT one can insert local operators at points, and the partition function with insertions is the n-point function. In Park-Park's arithmetic BF theory the "points" would be primes, and an "observable at ℓ" would be a local operator. But the paper never defines this. To make it precise one would need to:

1. Specify the algebra of observables at ℓ. Candidate: H¹(Q_ℓ, T/I_ℓT) or its singular quotient.
2. Specify what "inserting an observable" means at the level of the partition function. Candidate: replace Z_{X_S} by a "weighted sum" Z_{X_S, O_ℓ} that depends on the observable O_ℓ.
3. Prove a gluing axiom for the weighted partition function: Z_{X_S, O_ℓ} = ⟨Z_{X_{S∪ℓ}}, ev_{O_ℓ}⟩.

None of (1)-(3) is in Park-Park. The schematic write-up presupposes them.

---

## III. What Would Be Needed to Make the Argument Rigorous

I list the missing pieces, in increasing order of difficulty.

### III.1 Easy: redefine "BF correlator" to be the MCS Stark system (= bypass observables)

The cleanest fix is to drop the "observable" language and use MCS Theorem 3.4 directly. Then:

- Define ε^BF := ϖ_n(z), where z is some chosen R-basis of det⁻¹(RΓ̃_F(K,T)). [This is well-defined modulo R^×.]
- Use MCS Corollary 3.5 to extract Fitting ideals: Fitt^i(H¹_{F*}(K, A_n*(1))*) = I_i(ε^BF), where I_i(ε) = sum of im(ε_n) over n with ν(n) = i.
- This gives the same Fitting ideal information as Kolyvagin systems would, WITHOUT going through Mazur-Rubin's KS_1 module.

**The price of this fix:** the resulting object is a Stark system, NOT a Kolyvagin system. The Codex audit explicitly asked for a Kolyvagin system construction. If the goal is to produce κ^BF ∈ KS_1 and apply Mazur-Rubin freeness Theorem 5.2.10, this fix is insufficient.

**The benefit:** It IS a fully rigorous bridge from the BF/det side to Fitting ideals. The MCS paper ALREADY does this (Theorem 1.7 / Corollary 3.5). The only thing missing for application to BSD is identifying the Stark system ε^BF with the cyclotomic Stark system attached to Kato's Euler system (which BSS25 = Burns-Sakamoto-Sano give a Stark-system version of), so that ε^BF and ε^Kato can be compared via the freeness of SS_χ(F) (which MCS shows is free of rank 1, [/tmp/mcs.txt:1281]).

### III.2 Medium: produce a literal Kolyvagin system from MCS

To get an honest Kolyvagin system, one needs the Stark-to-Kolyvagin map from Burns-Sakamoto-Sano. The relevant statement is:

> (BSS25, Theorem ...) Let ε ∈ SS_r(A_n, F, P) be a Stark system. Then there is a "regulator" or "evaluation" map Reg : SS_r → KS_r, ε ↦ κ(ε), such that κ(ε) is a Kolyvagin system for (T, F, P).

The map Reg is constructed from the projection ∧^{r+ν(n)} → H¹_{F^n} ⊗ ∧^{r+ν(n)-1}(complementary) via the choice of a basis of the quotient pieces H¹_{/F}(K_q, A_n). The key property -- that the resulting collection satisfies (5) of MR Definition 3.1.3 with the φ^fs_ℓ -- requires a NONTRIVIAL compatibility check between the Stark system v_{n,m} maps and the Mazur-Rubin finite-singular maps.

**Status of this -- UPDATED 2026-04-04 after checking BSS abstract directly:** Burns-Sakamoto-Sano (arXiv:1805.08448) constructs a "canonical higher Kolyvagin derivative homomorphism" from higher rank **Euler systems** to higher rank **Kolyvagin systems**. The map is ES_r → KS_r, NOT SS_r → KS_r. (I verified this against the published abstract.) So the cited reference in the schematic write-up does not give what is needed: it gives a map FROM Euler systems, but the BF/MCS data is a Stark system, not an Euler system.

To use the BSS Kolyvagin derivative, one would need to upgrade the MCS Stark system ε^BF to a full Euler system (with norm relations along all cyclotomic Z_p-extensions, not just the inverse limit appearing in MCS Definition 3.2). MCS does not produce an Euler system; their construction takes det⁻¹(SC) directly to a Stark system, skipping the Euler system layer.

**This is a real gap.** The schematic write-up names the map "Burns-Sakamoto-Sano Kolyvagin derivative" but uses it as if it ran from Stark systems to Kolyvagin systems. The actual BSS map runs from Euler systems to Kolyvagin systems. The MCS paper itself notes (Section 1.4) that they go directly from SS to Fitting ideals BYPASSING Kolyvagin systems, precisely because there is no canonical SS → KS map.

### III.3 Hard: prove the TQFT gluing axiom for an OBSERVABLE-extended BF theory

To make the TQFT analogy literal, one would need to:

(a) Construct a BF theory in which observables can be inserted at primes. This means defining, for each finite set S of primes and each "observable" O_ℓ at ℓ ∈ S, a quantity Z_{X_S}(O_{ℓ_1}, ..., O_{ℓ_k}) ∈ (some space), and showing it satisfies a gluing axiom analogous to Theorem 5.12.

(b) Identify the Z with insertions with the determinantal data of Selmer complexes with relaxed conditions: Z_{X_S}(O_ℓ) should be a generator of det⁻¹(RΓ̃_{F^ℓ}(K,T)/π^n), where F^ℓ is the relaxation of F at ℓ.

(c) Prove that the gluing axiom for Z with insertions implies the recursion for the corresponding Stark system or Kolyvagin system. This requires the gluing to interact correctly with the v_{n,m} or φ^fs_ℓ transfer maps.

**Status:** None of (a)-(c) is in the literature, to my knowledge. The schematic write-up presupposes (a) and asserts (b)-(c) without proof. Constructing an "observable-extended BF theory" is essentially the work that the Park-Park paper would need to do to actually have observables -- and they don't.

### III.4 Hardest: prove that the connecting map of relaxation IS φ^fs_ℓ

Even granting (a)-(c) above, the relaxation map

   res_ℓ : det⁻¹(RΓ̃_F(K,T)) → det⁻¹(RΓ̃_{F^ℓ}(K,T)) ⊗ det H¹_s(Q_ℓ, T/I_ℓT)⁻¹

derived from the exact triangle SC(T) → SC(T,ℓ) → H¹_s(Q_ℓ,T/I_ℓT)[-1] gives a connecting map at the level of det functors. The schematic argument identifies this with the Kolyvagin recursion. But **this connecting map is not literally φ^fs_ℓ** for the same reason as in §II.3: it is a Poitou-Tate connecting map, which is a δ in a long exact sequence, while φ^fs_ℓ is the Frobenius-polynomial map Q(Fr⁻¹).

To bridge these one would need a separate lemma:

> **Conjectured lemma:** The connecting map res_ℓ in the exact triangle, transported under MCS Theorem 3.4, agrees with the Mazur-Rubin transfer map v_{n,nℓ} on Stark systems (or, alternatively, with φ^fs_ℓ ⊗ id on Kolyvagin systems).

I have not found this lemma stated or proved anywhere. The MCS paper does not address the question (its v_{n,m} maps are defined directly on exterior powers, not via Poitou-Tate connecting maps). Burns-Sakamoto-Sano may address the analogous question for Euler systems, but I have not been able to verify this claim from primary sources in this run.

---

## IV. The Sign Compatibility (Already Resolved)

This is the one piece of the schematic argument that IS rigorous, by `normalization-check/findings.md`. The Cassels-Tate pairing is DEFINED as a sum of local Tate pairings (Milne ADT I.6.13), and the Poitou-Tate connecting map sends a local class c_ℓ ∈ H¹_s(Q_ℓ) to the functional b ↦ inv_ℓ(c_ℓ ∪ b_ℓ), which is local Tate duality at ℓ by definition. So the sign ε(ℓ) = +1 with no further analysis needed. This was confirmed numerically (22/22 prime pairs across 5 character twists, plus 60/60 distribution relation tests).

But: **the sign compatibility is necessary but not sufficient.** It says that IF you have a Kolyvagin system, the Poitou-Tate-induced operators give the right local pairing structure. It does not say that the Poitou-Tate-induced operators ARE the φ^fs_ℓ of the Kolyvagin recursion. That is the gap of §II.3 / §III.4.

---

## V. The Hidden Issue: det vs H¹ Compatibility

The user's task description correctly identifies the load-bearing subtlety:

> The Mazur-Rubin Kolyvagin systems live in H^1, not in det(SC). The BF correlators (as defined in the schematic version) live in det(SC). Converting between H^1 and det(SC) requires:
> - A canonical isomorphism det(SC(T)) ≅ Λ (which holds when SC is a perfect complex of trivial Euler characteristic)
> - The Macias Castillo-Sano comparison det ≅ Stark system module
> But these are MODULE isomorphisms, not natural transformations of FUNCTORS. So the "BF correlator with insertions" must be defined at the level of det(SC) AND it must commute with the MCS isomorphism.

This is exactly right. Specifically:

**MCS Theorem 3.4 provides one isomorphism per choice of (T, F, n).** The diagrams that make these isomorphisms compatible across n (or across different F obtained by relaxing local conditions at primes) are constructed in MCS Theorem 2.20 + Proposition 3.3, and they are NOT described in the schematic write-up.

To define a "Stark system at level n" via the BF/det side AND have it transform correctly under v_{n,m}, the BF data Z_{X_S} for varying S must form a coherent system across S = (subsets of primes). This means:

(i) For each n, Z must produce a Stark system at level n via MCS Theorem 3.4.
(ii) For m | n, the corresponding map v_{n,m} on Stark systems must agree with the "natural" transfer map on the BF side.

**Park-Park Theorem 5.12 is consistent with (ii) on its face**: it gives a relation between Z_{X_S} and Z_{X_T} for S ⊂ T. But the schematic write-up asserts that this relation, transported through MCS, gives v_{n,m}. **This compatibility is the missing rigor.** Either it must be proven, or the construction must be redesigned to make it tautological.

The user's task description explicitly asks me to either prove this or identify the obstruction. **The obstruction is precisely: Park-Park's gluing relates COMPLEX-VALUED partition functions on H_S, not generators of det⁻¹ modules. The MCS isomorphism ϖ_n does not act on Park-Park's H_S.** The two formalisms live in different categories. To make them talk to each other you would need a "categorification" of Park-Park's BF theory in which Z is upgraded from a number to a determinant element, and Park-Park's gluing (Theorem 5.12) is upgraded from a complex equation to a determinant-module equation. **This upgrade is exactly the work that has not been done.**

---

## VI. Attempted Direct Proof of the Recursion (and Where It Fails)

For completeness, I tried to push through the schematic argument step by step and identify the precise breakage. Let me record the attempt.

### VI.1 The setup

Let T = T_p(E) for E/Q with good ordinary reduction at p ≥ 5, p non-anomalous, ρ̄ irreducible, p ∤ #E(Q)_tors · Tam(E) · #Ẽ(F_p). Then MCS Hypothesis 2.11 holds and core vertices exist (Hypothesis 2.17 holds). Fix n ≥ 1 and the MCS isomorphism

   ϖ_n : det⁻¹_{R_n}(RΓ̃_F(Q,T)/π^n) →∼ SS_χ(F)(A_n, F, P).

For E with good ordinary reduction at p, the core rank χ(F) = 1.

### VI.2 The hypothetical BF generator

Suppose -- and this is the FIRST unjustified step -- that there is a "BF generator" z_BF ∈ det⁻¹(RΓ̃_F(Q,T)) coming from the Park-Park theory in some way. By Park-Park's actual theorems, z_BF is at most a complex number (Z_X) or a section of a Hermitian line bundle on F_S; it is NOT a det generator. So already the construction stops here.

Suppose nonetheless we postulate z_BF as a basis. Then ε^BF := ϖ_n(z_BF) is a Stark system of rank χ(F) = 1.

### VI.3 The hypothetical Kolyvagin system

Apply (the conjectural) Stark-to-Kolyvagin map Reg : SS_1 → KS_1 to ε^BF. Then κ^BF := Reg(ε^BF) ∈ KS_1(T, F, P) is a Kolyvagin system, and by Mazur-Rubin Theorem 5.2.10 it equals u · κ^Kato for some u ∈ R^× (or u ∈ Λ^× in the Λ-adic version).

**Where this fails:** As §III.2 explains, the map Reg is not in the literature I can access. The schematic write-up names it "Burns-Sakamoto-Sano Kolyvagin derivative", but the BSS Kolyvagin derivative goes from Euler systems (or from the abstract module ES_r) to Kolyvagin systems, not from the abstract Stark system module SS_r. The MCS paper itself BYPASSES Kolyvagin systems precisely because there is no canonical Reg.

### VI.4 The hypothetical recursion proof

Suppose nonetheless Reg exists. Then we want to prove that κ^BF satisfies the Mazur-Rubin recursion (κ^BF_{nℓ})_{ℓ,s} = φ^fs_ℓ((κ^BF_n)_ℓ).

The schematic argument's strategy is:

(a) The exact triangle SC(T,n/ℓ) → SC(T,n) → H¹_s(Q_ℓ, T/I_ℓT)[-1] gives a connecting map δ in cohomology.
(b) Identify δ with the Mazur-Rubin transfer maps.
(c) Use TQFT gluing to identify δ with the Park-Park gluing pairing.

**Step (a)** is correct if the exact triangle exists. Constructing this triangle requires a careful definition of "Selmer complex with relaxed condition at ℓ" -- this is in Nekovar Asterisque 310 §6, so it's published. OK.

**Step (b)** is the gap. The connecting map δ in the long exact sequence of the exact triangle is a degree-shifting map H¹ → H², not a degree-preserving map H¹_f → H¹_s ⊗ G_ℓ. The Mazur-Rubin transfer map ψ^e_n in the Selmer sheaf [/tmp/mr.txt:984-989] is degree-preserving, going H¹_{F(n)}(Q,T/I_n T) ⊗ G_n → H¹_s(Q_ℓ,T/I_{nℓ}T) ⊗ G_{nℓ} via "localization at ℓ then φ^fs_ℓ". These are not the same map. They are not even of the same homological degree.

**The schematic argument confuses two different maps:**
- δ_PT : H¹_s(Q_ℓ, T/I_ℓT) → H²_F(Q, T/I_ℓT) (Poitou-Tate connecting hom, increases degree by 1)
- ψ^e_n : H¹_{F(n)}(Q, T/I_n T) ⊗ G_n → H¹_s(Q_ℓ, T/I_{nℓ}T) ⊗ G_{nℓ} (Selmer sheaf edge map, same degree, twists by Q(Fr_ℓ⁻¹) and tensors with G_ℓ)

These cannot be identified. Step (b) is FALSE as stated.

The CORRECT relationship is that the Poitou-Tate exact sequence places constraints on the Mazur-Rubin classes -- specifically, the existence of κ^BF_{nℓ} satisfying the recursion is constrained by the long exact sequence -- but the recursion itself involves the FROBENIUS POLYNOMIAL Q, which is local-arithmetic data not appearing in any cohomological exact sequence.

**Step (c)** never gets to be executed because step (b) fails.

### VI.5 The corrected statement

What CAN be derived from the TQFT gluing axiom (granting the categorification):

**(Hypothetical) Lemma.** Let z_BF ∈ det⁻¹(RΓ̃_F(Q,T)) be a hypothetical BF generator coming from a categorified Park-Park theory satisfying gluing in det⁻¹. Then the Stark systems ε^BF_n at varying n form a coherent system in SS_1(A_n, F, P) (i.e., satisfy the v_{n,m} compatibility).

**This lemma might be true, given a suitably-constructed categorified BF theory.** It would follow from the gluing axiom transported through MCS Theorem 3.4 -- IF you can show that Park-Park's gluing pairing on H_S corresponds to MCS's v_{n,m} on SS_1 under the (conjectural) categorification + ϖ_n. This is a NONTRIVIAL compatibility statement, not a tautology, but it has a chance of being true.

**What does NOT follow** from any version of the TQFT gluing axiom: the Mazur-Rubin Kolyvagin recursion (κ_{nℓ})_{ℓ,s} = φ^fs_ℓ((κ_n)_ℓ) for the corresponding Kolyvagin system κ. This is because:
1. The Kolyvagin system module KS is not the target of MCS Theorem 3.4 (Stark systems are).
2. The transfer maps in KS use φ^fs_ℓ (Frobenius-polynomial), while the transfer maps in SS use v_{n,m} (norm/inclusion in exterior powers). These are NOT the same operations.
3. To get from SS to KS one needs an additional Stark-to-Kolyvagin map whose existence is unestablished in the cited literature.

---

## VII. What Is Salvageable

Despite the gap, several pieces of the schematic write-up survive direct scrutiny:

### VII.1 Path B (Stark → Fitting ideals directly) IS rigorous, modulo MCS

If we drop the Kolyvagin system goal entirely and pursue MCS Corollary 3.5:

   Fitt^i_{R_n}(H¹_{F*}(K, A_n*(1))*) = I_i(ε)

where I_i(ε) is the ideal generated by im(ε_n) for n with ν(n) = i.

This is a published theorem of MCS. To use it for BSD it suffices to:

1. Verify MCS Hypotheses 2.11 + 2.17 for T_p(E) (DONE in `verify-mcs-hypotheses`).
2. Identify the Stark system ε arising from MCS with a known generator of SS_1 (e.g., the Burns-Sano cyclotomic Stark system attached to Kato's element, or whatever).
3. Compute the I_i(ε) and compare with Kurihara numbers.

**Path B does not need TQFT gluing, observables, or Kolyvagin recursions.** It is a pure application of MCS Theorem 3.4 / Corollary 3.5. The user should be aware that the SCHEMATIC write-up's claim of having two paths (A via Kolyvagin systems, B via Stark systems) is overstated: only Path B is supportable from the cited sources, and Path A is essentially missing.

### VII.2 The sign compatibility (epsilon = +1) is rigorous

`normalization-check/findings.md` correctly establishes that, in any setting where the relevant structures DO exist, the local-global pairing comparison is sign-+1 because the Cassels-Tate pairing IS the sum of local Tate pairings. This is a tautology of definitions and is correct.

### VII.3 The MCS hypothesis verification is rigorous

`verify-mcs-hypotheses/findings.md` correctly checks Hypotheses 2.11 and 2.17 for T_p(E), good ordinary, p odd, etc. This is rigorous. However the verification only covers the GOOD ORDINARY case; the multiplicative case (681b1 at p=3) was flagged as failing Hypothesis 2.11(iii) and is not covered.

### VII.4 The numerical Kolyvagin recursion verification is rigorous

The CRT decomposition computations in route-bf-kolyvagin-system Section VIII (and the sign verification in normalization-check Section IV) are rigorous numerical evidence that:

   δ_{ℓ_1 ℓ_2} (direct sum) = δ_{ℓ_1 ℓ_2} (CRT decomposition)

across 22+ prime pairs. This confirms that the Kolyvagin recursion holds for the Kurihara/modular-symbol classes -- which are KNOWN to satisfy the recursion by Kim's published theorem. So this is consistency with Kim, not new evidence about the BF side.

---

## VIII. The Honest Status of the "TQFT → Kolyvagin" Theorem

I now state explicitly what is and is not established.

### VIII.1 What IS established (and is genuinely new, modulo MCS being correct)

**Theorem (Honest version).** Let E/Q be an elliptic curve with good ordinary reduction at p ≥ 5, p non-anomalous, ρ̄ irreducible, p ∤ #E(Q)_tors · Tam(E) · #Ẽ(F_p). Let T = T_p(E). Assume Macias Castillo-Sano (arXiv:2603.23978) is correct. Then:

(i) det⁻¹(RΓ̃_F(Q,T))/π^n ≅ SS_1(A_n, F, P) by MCS Theorem 3.4.
(ii) Any R-basis z of det⁻¹(RΓ̃_F(Q,T)) gives a Stark system ε := ϖ_n(z) ∈ SS_1.
(iii) Fitt^i(H¹_{F*}(Q, A_n*(1))*) = I_i(ε) by MCS Corollary 3.5.
(iv) The local Tate compatibility ε(ℓ) = +1 holds tautologically.

**This is genuinely new IF z can be identified with something canonical from the BF theory or from Kato's Euler system.** Identifying z with "Kato's element" requires further work (the comparison between det⁻¹(RΓ̃_F) and Kato's L-value, which is related to the Iwasawa Main Conjecture of Kato + Skinner-Urban). This is plausible but requires its own write-up.

### VIII.2 What is NOT established (the actual content of the lemma the task asked for)

**Theorem A (the schematic claim).** Park-Park's BF theory gives a Kolyvagin system κ^BF ∈ KS_1(T, F_can) via TQFT gluing.

**Status: GAP.** The argument requires:

1. (Missing) An "observable-extended" Park-Park BF theory in which Z_{X_S}(O_{ℓ_1},...,O_{ℓ_k}) is defined as a determinant module element. Park-Park does not define observables; their Z_X is a complex number.

2. (Missing) A categorification of Park-Park's gluing axiom (Theorem 5.12) at the level of det⁻¹(SC). Park-Park's gluing is between Hilbert spaces of functions on F_S; MCS's transfer maps are between exterior biduals of cohomology. These do not literally match.

3. (Missing) A Stark-to-Kolyvagin map "Reg : SS_r → KS_r" in the literature. Burns-Sakamoto-Sano constructs ES → KS via Kolyvagin derivatives, not SS → KS. MCS itself bypasses Kolyvagin systems.

4. (Wrong) The identification of the Poitou-Tate connecting map δ with the Mazur-Rubin finite-singular comparison φ^fs_ℓ. These are maps of different homological degrees and CANNOT be identified.

### VIII.3 What can be rescued

**Reformulated theorem A*.** Under the same hypotheses, MCS Theorem 3.4 produces a Stark system ε^BF ∈ SS_1 for any choice of basis of det⁻¹(SC). This Stark system has the right Fitting ideals to imply p-adic BSD via Path B. (No Kolyvagin system is constructed, no TQFT gluing is needed, no observables are inserted. The TQFT story is window dressing on top of a direct application of MCS Theorem 3.4.)

This rescue:
- Eliminates the dependence on a "TQFT-extended" Park-Park theory.
- Does not need the Mazur-Rubin freeness theorem (since it works in SS_1, not KS_1).
- Still resolves the Codex audit's concern about "type-changing assertion" -- not by constructing a Kolyvagin system, but by showing that no Kolyvagin system is needed if you use MCS's direct Stark → Fitting bridge.
- Does not satisfy the audit's literal demand for "the BF-to-Kolyvagin theorem in full detail," because the answer is "we don't need it; we have a Stark system, which is enough."

---

## IX. Verdict

**[GAP]** The "TQFT gluing implies Kolyvagin recursion" theorem of `route-bf-kolyvagin-system/findings.md` is NOT supported by the cited sources. The proof fails for the following PRECISE reasons:

1. **Park-Park (arXiv:2602.19621) does not define observables, correlators, or insertion operators.** Their partition function Z_X is a complex number, not a determinant module element. Their gluing theorem (Theorem 5.12) is between complex-valued partition functions on H_S, not between determinants of Selmer complexes. The schematic write-up's repeated identifications "Z_BF = τ(SC)", "BF observable insertion at ℓ = relaxing local condition at ℓ", "TQFT gluing at ℓ = Poitou-Tate at ℓ" are NOT in the Park-Park paper.

2. **MCS Theorem 3.4 lands in the wrong category.** It produces a Stark system, not a Kolyvagin system. The schematic write-up needs the Stark-to-Kolyvagin map "Reg : SS_r → KS_r" but this map is not in the cited Burns-Sakamoto-Sano literature. The MCS paper itself notes that they BYPASS Kolyvagin systems; this is a structural fact, not a presentation choice.

3. **The Poitou-Tate connecting map δ is NOT the Mazur-Rubin finite-singular comparison φ^fs_ℓ.** They are maps of different homological degrees and use different inputs (one is an exact-sequence δ, the other is the Frobenius polynomial Q(Fr⁻¹) acting on T^{Fr=1}). The schematic argument's identification of these is wrong as stated.

4. **The "categorification" of Park-Park's BF theory needed for the argument has not been written down** anywhere in the literature, as far as I can find. This is the main missing piece. Without it, "TQFT gluing" remains an analogy rather than a theorem.

**However**, the argument is RESCUABLE in a weakened form:

5. **MCS Theorem 3.4 alone (without TQFT gluing) suffices for p-adic BSD via Path B.** It produces a Stark system from det⁻¹(SC) and gives Fitting ideals via Corollary 3.5. To complete the BSD application one needs to identify this Stark system with the Burns-Sakamoto-Sano cyclotomic Stark system attached to Kato's Euler system -- this is a SEPARATE and substantial task, but it is cleaner than the TQFT story and uses only published machinery.

6. **The sign compatibility (epsilon = +1)** of `normalization-check/findings.md` is correct and is a definitional tautology, not a deep theorem.

7. **The MCS hypothesis verification** of `verify-mcs-hypotheses/findings.md` is correct for the good ordinary, non-anomalous, irreducible, p-coprime-to-torsion case.

**Bottom-line recommendation:** Drop the TQFT gluing language. Replace "Theorem A: TQFT gluing produces a Kolyvagin system" with "Theorem A* (clean version): MCS Theorem 3.4 produces a Stark system from det⁻¹(SC), and MCS Corollary 3.5 gives the Fitting ideals." This loses the (alleged) general theorem about arithmetic TQFTs producing Kolyvagin systems -- but that alleged general theorem was not actually proved, and the rescue suffices for BSD.

**The rest of the proof chain (Mazur-Rubin freeness, comparison with Kato, u = 1, Kim's Kurihara theorem, Schneider/Perrin-Riou) is downstream of either Theorem A or Theorem A***. Under Theorem A* the dependence is cleaner: no Kolyvagin system is involved, so Mazur-Rubin freeness is replaced by the freeness of SS_1 (which MCS Proposition 3.3 establishes), and the comparison with Kato is at the Stark-system level rather than the Kolyvagin-system level.

---

## X. What This Means for the Overall p-adic BSD Proof Architecture

The user's task description says: "This is the load-bearing theorem of the entire p-adic BSD proof architecture." The honest assessment:

- The TQFT gluing → Kolyvagin recursion theorem (Theorem A as stated) **does not have a proof in the cited literature**. The schematic version of route-bf-kolyvagin-system Section IV is not a proof, and the obstructions (§II, §VI) are not minor "fiddly normalizations" but type-mismatches that change what kind of theorem is being proved.

- The MCS-based replacement (Theorem A*) **may suffice for BSD if** one can identify the BF-side determinantal data with Kato's Stark system. This identification has not been written down but is plausible. It would require: (a) a precise definition of Z_BF as a det⁻¹(SC) generator (NOT in Park-Park); (b) a comparison Z_BF = (Kato's element) under the IMC. Neither (a) nor (b) is in the campaign's findings files.

- **The campaign's claim that "any arithmetic TQFT produces a Kolyvagin system" is a slogan, not a theorem.** Park-Park's BF theory is one specific construction, and even for it the categorification needed to make TQFT gluing into a determinantal-module statement is missing. For a "general arithmetic TQFT" the statement is even more aspirational.

- **The sound parts of the proof chain** (sign analysis, MCS hypothesis verification, numerical recursion checks) are real progress but they do not fill the central gap.

**Recommendation:** The campaign's BSD proof should be reframed as conditional on Path B (MCS-based, no Kolyvagin system, no TQFT gluing) rather than Path A (TQFT-based). The "new theorem about arithmetic TQFTs producing Kolyvagin systems" should be DELETED from the proof outline -- it is not proved and the gap is not the kind that can be filled with a few weeks of careful checking. It is a missing categorification of a paper that hasn't been written.

If the campaign is committed to Theorem A specifically (e.g., for independent interest beyond BSD), it would need to be rewritten as a CONJECTURE: "Conjecture (TQFT → Kolyvagin). If a categorified arithmetic BF theory exists in which the partition function takes values in det⁻¹(SC) and the gluing axiom holds at the level of det⁻¹, then the resulting Stark systems form a coherent system that maps to a Kolyvagin system via the (conjectural) Stark-to-Kolyvagin map." This is a precise conjecture, but it is not currently a theorem.

---

## XI. References

**Used in this analysis (verified by direct PDF inspection):**

1. **Mazur, B. and Rubin, K.** "Kolyvagin systems." Memoirs AMS 168(799), 2004. PDF saved to `/tmp/mr.txt`. Definition 1.2.2 (φ^fs_ℓ), Definition 3.1.3 (Kolyvagin system), Theorem 5.2.10 (freeness).

2. **Macias Castillo, D. and Sano, T.** "On Selmer complexes, Stark systems and derived p-adic heights." arXiv:2603.23978, March 2026. PDF saved to `/tmp/mcs.txt`. Hypothesis 2.11, Definition 2.16, Theorem 2.20, Definition 3.2, Proposition 3.3, Theorem 3.4, Corollary 3.5.

3. **Park, J. and Park, J.** "Arithmetic BF theory and the Cassels-Tate pairing." arXiv:2602.19621, February 2026. PDF saved to `/tmp/pp.txt`. Definition 5.7 (Z_X), Definition 5.8 (Z_{X_S}), Theorem 5.12 (gluing), Proposition 6.5 (Z_X = cardinality).

**Used by upstream campaign (assumed; not re-verified in this run):**

4. **Burns, D., Sakamoto, R., and Sano, T.** "On the theory of higher rank Euler, Kolyvagin and Stark systems, II." arXiv:1805.08448, 2018. (The schematic write-up cites this for "Stark-to-Kolyvagin derivative," but I have not been able to confirm this map exists in this paper. The classical Kolyvagin derivative goes ES → KS, not SS → KS.)

5. **Bullach, D. and Burns, D.** arXiv:2509.13894, September 2025. (Cited for Λ-adic / Gorenstein refinements; not consulted in this run.)

6. **Kim, C.H.** "The refined Tamagawa number conjectures for GL_2." arXiv:2505.09121. (Cited for exp* identifying Kolyvagin classes with Kurihara numbers.)

7. **Nekovar, J.** "Selmer complexes." Asterisque 310, 2006. (Cited for the Selmer complex formalism.)

---

## XII. Self-Assessment

I tried, throughout this analysis, to err on the side of MAKING the schematic argument work rather than against it. The conclusions above are forced by the literal content of the cited papers, not by an aggressive reading.

What I am highly confident about:

- Park-Park does not define observables or correlators with insertions. (I literally grepped for these terms.)
- Park-Park's Z_X is a complex number (Definition 5.7) and a cardinality (Proposition 6.5), not a determinant module element. (Direct quotation.)
- MCS Theorem 3.4 produces a Stark system, not a Kolyvagin system. (Direct quotation of Definition 3.2 and Theorem 3.4.)
- Mazur-Rubin Kolyvagin recursion uses φ^fs_ℓ (Definition 1.2.2), which is the Frobenius-polynomial map Q(Fr⁻¹), and is NOT a Poitou-Tate connecting homomorphism. (Direct quotation.)
- The sign compatibility ε = +1 is correct and tautological. (Verified in normalization-check.)

What I am less confident about:

- ~~Whether BSS gives a Stark-to-Kolyvagin map.~~ **CONFIRMED DOES NOT.** Burns-Sakamoto-Sano arXiv:1805.08448 gives Euler-to-Kolyvagin, not Stark-to-Kolyvagin. The schematic write-up's reference is incorrect.
- Whether the Park-Park gluing CAN be categorified to det⁻¹(SC) by additional work that the campaign could do. (My guess: maybe, but this would be a substantial paper, not a "few weeks of normalization checking.")
- ~~Whether Bullach-Burns (arXiv:2509.13894) bypasses the problem.~~ **CHECKED ABSTRACT: it does NOT.** Bullach-Burns develops "a theory of Euler and Kolyvagin systems relative to the Nekovář-Selmer complexes" but the construction takes EULER SYSTEMS as input ("given appropriate Euler systems, it allows one to study Selmer groups"). It does not produce Kolyvagin systems from a Selmer complex alone. So Bullach-Burns does NOT solve the problem of getting from det⁻¹(SC) to a Kolyvagin system without an Euler system input -- it just provides a refined Mazur-Rubin-style theory ONCE you already have an Euler system.

If any of the above uncertain points turns out to favor the schematic argument (e.g., if BSS25 really does have a clean SS → KS map), the verdict moves from [GAP] to [QUESTIONABLE]. But the most fundamental issue -- that Park-Park does not define observables and the categorification is missing -- is robust to these uncertainties.

The honest one-line summary: **The TQFT slogan "any arithmetic TQFT produces a Kolyvagin system via Poitou-Tate" is suggestive but not a theorem. Park-Park's actual paper does not give the inputs that the slogan needs, and the bridge to Mazur-Rubin Kolyvagin systems is missing both an upstream type match (Stark vs Kolyvagin) and a downstream operator identification (Poitou-Tate δ vs φ^fs_ℓ). The good news is that MCS Theorem 3.4 already gives enough Fitting ideal information for BSD via the Stark-system route, without needing the TQFT story at all.**
