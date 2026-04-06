# Reframing u = 1 via Path B (Stark Systems) on a Clean Example

**Date:** 2026-04-04
**Status:** COMPLETE (main conclusions stable; one cross-check against Bullach-Burns Lambda-adic version flagged [QUESTIONABLE] for follow-up)
**Predecessors / context:**
- `../determine-unit-u/findings.md` -- the BROKEN version using 11a1/p=5 (a "double failure" curve/prime where MCS Theorem 3.4 does not even apply) and citing the dead "BF correlator = Kurihara" identity from `../route-bf-kolyvagin-system/`.
- `../verify-mcs-hypotheses/findings.md` -- catalogues which (E, p) pairs satisfy MCS Hypothesis 2.11 + 2.17. Flags 11a1/p=5 as anomalous AND residually reducible.
- `../lemma-tqft-kolyvagin-formal/findings.md` -- proves the BF -> Kolyvagin TQFT path is dead. The Park-Park paper has no observables, no determinantal Z, no Poitou-Tate-stated gluing. Recommends using Path B (MCS Theorem 3.4 directly) instead.
- `../final-audit/codex-audit.md` -- identifies the inconsistency.

This file does two jobs:
1. **Pick a curve/prime where ALL hypotheses hold cleanly** and where the MCS framework actually applies. (Done: see Section II.)
2. **Reframe the "u = 1" claim in Path B language** -- as an identity between two Stark systems (det^{-1}(SC) generator vs Kato Stark element under MCS), NOT between Kolyvagin systems via the (broken) BF correlator route.

---

## Executive Summary

**Curve picked: 11a1 at p = 7.** This is a deliberate rhetorical replacement of the broken main example: the SAME curve as the original (so all infrastructure ports over) but at a DIFFERENT prime where every MCS hypothesis is genuinely satisfied. ALL of the following hold for (11a1, 7), checked computationally in SageMath:

- Good ordinary reduction at p = 7 (a_7 = -2, |E(F_7)| = 10, both nonzero mod 7)
- Non-anomalous: 7 does not divide |E(F_7)| = 10
- rho_bar irreducible: the ONLY reducible prime for 11a1's mod-p Galois rep is p = 5 (the famous 5-isogeny). At p = 7, rho_bar is surjective (in fact the whole of GL_2(F_7)).
- p = 7 does not divide |E(Q)_tors| * Tam(E/Q) = 5 * 5 = 25
- Optimal, semistable, Manin constant = 1
- E has rank 0 and analytic order of Sha = 1, so L(E, 1) / Omega = 1/5 is a unit at p = 7
- Sha[7^infty] = 0 (bounded by p-descent; `E.sha().p_primary_bound(7) = 0`)
- Kato non-triviality is computationally verifiable (the trivial-character L-value alone witnesses non-vanishing of the core Kato class)

A backup curve **643a1 at p = 7** (rank 2, semistable, optimal, all hypotheses clean) is documented in Section II.4 in case the rank-2 setting is needed. The core u = 1 argument as written in Sections III-V works for 11a1/p=7.

**Headline result: u(0) = 1 is a THEOREM for 11a1 at p = 7.**

Specifically, combining:
- Bullach-Burns arXiv:2509.13894 Corollary 9.7 (applied to K = Q, non-CM case), which gives element-level equality between z_Q^{Kato} and a basis of det^{-1}(SC) **conditional on the p-part of BSD over Q**; AND
- Burungale-Castella-Skinner 2024 (arXiv [29] in Bullach-Burns), which proves the p-part of BSD for E/Q under p > 3, good ordinary, SL_2 in rho_bar image, analytic rank <= 1 -- **all of which hold for 11a1/p=7**,

**we obtain u(0) = 1 as a theorem** (not just a conjecture), resolving the element-level equality of epsilon^Stark(0) and epsilon^Kato(0) under the MCS isomorphism. Numerically verified: the Sage-computed Lp(E, 0) series constant term agrees with the interpolation formula (1 - 1/alpha_7)^2 * L(E,1)/Omega to full Sage precision, both being 7-adic units.

**The fuller claim "u = 1 in Lambda" remains [QUESTIONABLE].** Bullach-Burns Theorem 9.4 gives the one-sided inclusion z_{Q_inf}^{Kato} in im(Theta_{Q_inf}) at the Lambda-adic level. The reverse inclusion in the Lambda-adic setting (= u = 1 in Lambda for 11a1/p=7) plausibly extends from Cor 9.7's proof but is not literally written down in BB for K = Q at the Iwasawa level. The original campaign's claim of "u = 1 unconditionally" was predicated on the (dead) BF correlator framework; with the Path B reframe, u = 1 at the base level is now a theorem, but the Lambda-adic extension is a [QUESTIONABLE] or [GAP] depending on how one reads Bullach-Burns.

**Reframed claim (Path B language):**

Let T = T_p(E), p = 7, E = 11a1. By MCS Theorem 3.4 (whose hypotheses are verified), there is a canonical Z_p-module isomorphism

    varpi : det^{-1}_{Z_p}(SC(T)) -->  SS_1(T, F_can)

where SS_1 is the module of rank-1 Stark systems for the canonical Selmer structure F_can. The module SS_1 is FREE OF RANK 1 over Lambda = Z_p[[T]] (MCS Proposition 3.3). Pick:

- **epsilon^Stark := varpi(z_BF)**, where z_BF is any Lambda-basis of det^{-1}(SC). (For 11a1/p=7, z_BF can be taken to be the canonical generator coming from the Iwasawa Main Conjecture, i.e., a generator of Fitt_0(X) where X is the Pontryagin dual of the Selmer group over Q_cyc.)
- **epsilon^Kato := image under MCS of Kato's Euler system**, more precisely the rank-1 Stark system attached to Kato's zeta element via Burns-Sakamoto-Sano (BSS arXiv:1805.08448, Theorem 5.2 / Section 5).

Both live in the free rank-1 module SS_1, so

    epsilon^Stark = u * epsilon^Kato,    u in Lambda^x.

**The u = 1 argument (Path B version):**

(a) **At T = 0 (trivial character):** Both sides specialize to the same explicit value:
        epsilon^Stark(0) = (1 - 1/alpha_7)^2 * L(E,1)/Omega_E^+   (from the IMC determinantal generator)
        epsilon^Kato(0) = (1 - 1/alpha_7)^2 * L(E,1)/Omega_E^+   (from Kato's reciprocity, Asterisque 295 Thm 12.5)
   These are LITERALLY equal because L_p(E) is constructed by interpolation against this exact formula. So u(0) = 1 (and both sides are nonzero for 11a1/p=7 since L(E,1)/Omega = 1/5 is a 7-unit).

(b) **At finite-order characters:** For each character chi of Gal(Q(zeta_{p^n})/Q), specializing the identity epsilon^Stark = u * epsilon^Kato at T = chi(gamma) - 1 gives a comparison of Stark elements at level p^n. The interpolation property of L_p(E) at T = chi(gamma) - 1 is the same on both sides (this is Kato's explicit reciprocity law combined with the IMC).

(c) **Density / Weierstrass preparation:** The set { chi(gamma) - 1 : chi finite order character } is Zariski-dense in the open p-adic disk. A power series u in Z_p[[T]] with u(zeta_{p^n} - 1) = 1 for all n must be u = 1 identically (Weierstrass preparation: the difference u - 1 has only finitely many zeros in any closed disk, so cannot vanish on a Zariski-dense set unless it is zero).

**Verdict on u = 1:** [SOUND at T = 0] for 11a1/p=7, via Bullach-Burns (arXiv:2509.13894) Corollary 9.7 combined with the known p-part of BSD for 11a1 at p = 7. **[QUESTIONABLE / GAP at positive layers]** for non-CM rational curves in general, because the Lambda-adic element-level equality is only a one-sided inclusion in Bullach-Burns Theorem 9.4.

Specifically:

1. **At the base level (K = Q, T = 0):** Bullach-Burns Corollary 9.7 says the inclusion Z_p · z_Q^Kato ⊆ im(Theta_Q) is an EQUALITY when the p-part of BSD for E/Q is valid. For 11a1 at p = 7 the p-part of BSD IS known (by Burungale-Castella-Skinner 2024 + the direct computation that Sha[7^infty] = 0, Tam = 5, tors = 5, L(E,1)/Omega = 1/5 all line up as 7-units). So **u(0) = 1 is unconditionally a theorem for 11a1/p=7**, via Bullach-Burns Cor 9.7.

2. **At the Lambda-adic level (K_infty = Q_cyc):** Bullach-Burns Theorem 9.4 gives ONE inclusion: z_{Q_infty}^Kato in im(Theta_{Q_infty, S}). The REVERSE inclusion (= full element-level equality, = u = 1 in Lambda) is what Corollary 9.7's second assertion proves, but the precise statement requires p-BSD over every intermediate field F of K/Q with [F:Q] prime-to-p. For K = Q, K_infty = Q_cyc, the intermediate fields are Q_n with [Q_n:Q] = p^n, so the ONLY prime-to-p-degree subfield of K_infty = Q_cyc is K = Q itself. Hence the condition reduces to p-BSD over Q, which we have for 11a1/p=7.

**So in fact, for 11a1 at p = 7, Bullach-Burns Corollary 9.7 (applied to the Lambda-adic setting via the remark that prime-to-p subfields of Q_cyc are just {Q}) appears to give u = 1 as an equality in Lambda, unconditionally.** This is actually STRONGER than I originally expected. The only published-theorem gaps remaining are:

(a) Bullach-Burns is itself a recent paper (September 2025, arXiv:2509.13894) that uses machinery from Sakamoto et al.; its correctness as a published theorem is subject to peer review.
(b) The cited result depends on Burungale-Castella-Skinner 2024 (arXiv reference [29] in BB) for the p-part of BSD for rank-0 non-CM curves with good ordinary reduction, surjective rho_bar, and analytic rank <= 1. For 11a1/p=7 all conditions hold, so this is fine.
(c) The "condition that prime-to-p subfields of K_infty/Q are just Q" applied to Corollary 9.7 second assertion -- I have to be slightly careful here because Corollary 9.7 is stated for finite K, not K_infty. The Lambda-adic version (Theorem 9.4) only gives the inclusion, not equality; the equality at the Lambda-adic level is deduced in the proof of Corollary 9.7's second assertion and may or may not apply directly to K = Q. **This is the main subtlety and I mark it [QUESTIONABLE] until I can verify it against the Bullach-Burns paper directly.**

So the honest status is:

> **u(0) = 1 is unconditionally a theorem for 11a1 at p = 7**, via Bullach-Burns Corollary 9.7 + the known p-part of BSD for 11a1/p=7 (Burungale-Castella-Skinner 2024 + direct Sha = 0 computation). [SOUND]
>
> **u = 1 as an equality in Lambda for 11a1 at p = 7** is very likely true by extending the argument in Bullach-Burns Corollary 9.7 to the Lambda-adic setting, but I have NOT fully verified this from primary sources in this run. The ingredient is there (Theorem 9.4 gives the inclusion; the Rohrlich-based argument in Cor 9.7's proof plausibly gives the reverse inclusion at K = Q), but I have not read the precise Lambda-adic statement. **[QUESTIONABLE until verified]**.
>
> Unconditionally, the IMC of Kato + Skinner-Urban (which is a 2014 theorem) gives (u) = (1) as ideals in Lambda, i.e., u is a unit. This is [SOUND].

This is a substantially more honest (and more precisely sourced) claim than the original `determine-unit-u/findings.md`, which asserted u = 1 via the broken BF correlator framework.

---

## I. What changed and why

### I.1 The original claim (broken)

`../determine-unit-u/findings.md` claimed:

> **u = 1** for all optimal elliptic curves E/Q with Manin constant c_E = 1 (which includes all semistable optimal curves, by Mazur/Cesnavicius).

The "proof" used 11a1/p=5 as the worked example and went through the BF correlator formalism: it computed Kurihara numbers, used the Kim identity exp*(kappa^Kato_ell) = delta_ell, and argued that exp*(kappa^BF_ell) = delta_ell ALSO, hence u acts as 1 on the Kolyvagin recursion, hence u = 1 in Lambda by density.

**Two breakages:**

1. **The example was double-broken.** From `../verify-mcs-hypotheses/findings.md` Section IV.2: "11a1 at p = 5: a_5 = 1, so 5 | |E~(F_5)| = 5. Also rho_bar is REDUCIBLE at 5 (E(Q) has 5-torsion). Double failure." So MCS Theorem 3.4 does not apply to 11a1/p=5 at all. The hypothesis check was published right next to the unit-u argument and they disagree on whether the example works.

2. **The proof used a dead identity.** From `../lemma-tqft-kolyvagin-formal/findings.md`: Park-Park's paper (arXiv:2602.19621) does NOT define BF observables, BF correlators, or insertion operators. Verbatim word-search of the PDF returns ZERO matches for "observable", "insertion", "correlator". The "BF correlator = Kurihara number" identity that the unit-u argument leans on (`exp*(kappa^BF_ell) = delta_ell`) has no source. Park-Park's Z_X is a complex number (Definition 5.7), not an element of det^{-1}(SC). The MCS theorem produces a Stark system, not a Kolyvagin system; there is no published Stark -> Kolyvagin map that would recover kappa^BF.

The fix: drop both the broken example AND the broken framework.

### I.2 What survives

The "salvageable" Path B from `../lemma-tqft-kolyvagin-formal/findings.md` Section VII.1:

- MCS Theorem 3.4 IS a real theorem. It produces a **Stark system** epsilon^BF in SS_1 from a generator of det^{-1}(SC).
- MCS Proposition 3.3 + Corollary 3.5 give the Fitting-ideal application of this Stark system.
- The Burns-Sano cyclotomic Stark system attached to Kato's Euler system gives a SECOND Stark system epsilon^Kato in SS_1.
- Both are generators of the free rank-1 module SS_1, so they differ by a unit u.

The **u = 1 question** is the question of equality of these two specific Stark generators. It is the "ETNC unit" question, not the "BF correlator vs Kato class" question.

**This is conceptually cleaner but technically less ambitious.** It does not give a Kolyvagin system, does not use the (nonexistent) BF correlator framework, and does not get equality of ELEMENTS in KS_1 -- only equality of elements in SS_1. For the BSD application that is enough (MCS Corollary 3.5 gets Fitting ideals from SS_1 directly, bypassing KS_1).

### I.3 Why 11a1/p=7 (not 389a1/p=5)

The task brief proposed 389a1/p=5 as the strong candidate. I checked it: rank 2, semistable, optimal, all MCS hypotheses satisfied. **However**, for rank-2 curves, BOTH sides of the comparison vanish at T = 0:

   epsilon^Stark(0) = 0,  epsilon^Kato(0) = 0  (because L(E,1) = 0 for rank >= 1).

So the T = 0 comparison gives 0 = u * 0, which determines NOTHING about u. To pin down u for rank 2, one would need to specialize at finite-order characters AND find a specific character chi for which neither side vanishes, then use that. This is more delicate -- by Rohrlich's nonvanishing theorem, the twisted L-values L(E, chi, 1) are nonzero for almost all chi, so SOME chi works, but specifying which one and computing both sides at it is much harder than the rank-0 case.

**The cleanest u(0) = 1 statement requires rank 0.** That is why I switched to 11a1/p=7. The infrastructure built for 11a1/p=5 (modular symbols, p-adic L-function, Kurihara number computations) ports to p = 7 with no changes other than the prime.

For completeness I document 643a1/p=7 (rank 2, all hypotheses satisfied) as a backup in Section II.4, but the main worked example below is 11a1/p=7.

### I.4 Summary table of fixes

| Original (broken) | Replacement (clean) |
|---|---|
| Curve: 11a1 at p = 5 (anomalous, reducible rho_bar -- DOUBLE FAILURE) | Curve: 11a1 at p = 7 (rho_bar surjective, non-anomalous, all MCS hyps hold) |
| Framework: BF correlator = Kurihara number (DEAD: no observables in Park-Park) | Framework: epsilon^Stark = u * epsilon^Kato in SS_1 (Path B via MCS Theorem 3.4) |
| Conclusion: u = 1 unconditionally | Conclusion: u = 1 conditional on ETNC at p; unconditionally u in Lambda^x by IMC (Kato + Skinner-Urban) |
| Key step: density of Kolyvagin primes giving u mod p^k -> 0 in Lambda | Key step: u(0) = 1 from interpolation of L_p(E,0); higher u(zeta_{p^n}-1) values from twisted L-values; Weierstrass preparation |

---

## II. The Clean Example: 11a1 at p = 7

### II.1 The curve

E = 11a1 = "Cremona's first": y^2 + y = x^3 - x^2 - 10x - 20. Conductor N = 11.

```
Rank = 0
|E(Q)_tors| = 5  (the unique 5-torsion point P = (5, 5) and its multiples)
Tamagawa product = 5  (one bad prime, q = 11, with c_11 = 5)
Optimal? YES (it is the unique curve in its isogeny class up to isogeny choice; Cremona labels 11a1 as the optimal one)
Semistable? YES (only bad prime is q = 11, multiplicative)
Manin constant = 1  (proved by Mazur/Cesnavicius for semistable optimal curves)
L(E, 1) / Omega_E = 1/5  (verified by Sage)
Analytic order of Sha = 1
```

### II.2 Verification of all MCS hypotheses at p = 7

I checked these in Sage:

| Condition | Value | Hypothesis met? |
|---|---|---|
| p = 7 odd | True | YES (S1 from MCS standing) |
| Good reduction at 7 | True (only bad prime is 11) | YES (S3 / Panchishkin filtration exists) |
| Ordinary at 7 (a_7 not divisible by p) | a_7 = -2, |a_7| = 2 < 7 | YES |
| Non-anomalous: p does not divide |E~(F_7)| | |E~(F_7)| = 10, 10 mod 7 = 3 != 0 | YES (Hyp 2.11(iii)) |
| rho_bar irreducible at p = 7 | reducible primes for 11a1's mod-p rep are exactly {5}; 7 not in {5} | YES (Hyp 2.17 input) |
| rho_bar surjective at p = 7 | True (verified by Sage `is_surjective(7)`) | YES (gives core vertex existence by MR Thm 4.1.7) |
| p does not divide |E(Q)_tors| | tors = 5, 5 mod 7 != 0 | YES (Hyp 2.11(i) / Remark 2.12) |
| p does not divide Tam(E/Q) | Tam = 5, 5 mod 7 != 0 | YES (Remark 2.12) |
| Remark 2.12 product: p does not divide tors * Tam * |E~(F_p)| = 5 * 5 * 10 = 250 | 250 mod 7 = 5 != 0 | YES |
| H^0(Q_p, T_p^-) = 0 (alpha_7 != 1) | alpha_7 has |alpha_7|_p = 1, alpha_7 != 1 (since a_7 = -2, p = 7 means alpha is the unit root of x^2 + 2x + 7) | YES (Hyp 2.11(ii)) |
| H^0(Q_p, A_p^-) = 0 | Equivalent to non-anomalous, already checked | YES (Hyp 2.11(iii) part 1) |
| H^0(Q_p, (T_p^+)^vee(1)) = 0 | Equivalent to alpha_7 != 1 | YES (Hyp 2.11(iii) part 2) |
| Sakamoto p >= 5 condition (Mazur-Rubin H.4) | p = 7 >= 5 | YES |
| mu = 0 for X | Kato + Skinner-Urban under surjective rho_bar | YES |

**Conclusion: ALL MCS hypotheses hold.** Theorem 3.4 applies and gives the canonical isomorphism det^{-1}(SC(T_p(E)))/p^n -> SS_1(A_n, F_can, P) for all n.

### II.3 What L(E, 1) / Omega looks like at p = 7

```
L(E, 1) / Omega_E^+ = 1/5     (computed exactly by Sage)
v_7(1/5) = 0                  (since 7 does not divide 5)
```

So the trivial-character L-value is a 7-adic UNIT. Multiplying by the Euler factor (1 - 1/alpha_7)^2:

```
alpha_7 = unit root of x^2 + 2x + 7
       = -1 + sqrt(-6)  (computed in Q_7)
1 - 1/alpha_7 = 1 - 1/alpha_7

In Q_7: alpha_7 = a_7 - 7/alpha_7^* (where alpha_7^* is the other root)
v_7(alpha_7) = 0 (unit root by definition)
v_7(1 - 1/alpha_7): need to check whether alpha_7 = 1 mod 7
   a_7 mod 7 = -2 mod 7 = 5
   alpha_7 mod 7 = unit root of x^2 + 2x = x(x+2) over F_7, i.e., 0 or -2 = 5
   So alpha_7 mod 7 = 5 (the unit root, NOT zero), so alpha_7 != 1 mod 7
   Hence v_7(1 - 1/alpha_7) = 0 (the Euler factor is a unit)
```

So **(1 - 1/alpha_7)^2 * L(E,1)/Omega is a 7-adic UNIT** for 11a1 at p = 7. Both the BF (Stark) generator and Kato's class evaluate at T = 0 to this same unit. Both are NONZERO at T = 0 -- this is what makes 11a1/p=7 a clean witness.

### II.4 Backup: 643a1 at p = 7 (rank 2, all hypotheses clean)

For completeness, I also verified:

```
E = 643a1, p = 7
Rank = 2, Semistable = True, Optimal = True, Manin = 1
|E(Q)_tors| = 1, Tamagawa = 1
a_7 = -3, |E~(F_7)| = 11, non-anomalous (11 mod 7 != 0)
Reducible primes for rho_bar: [] (irreducible at every p)
Surjective at p = 7: True
```

This satisfies all MCS hypotheses. The catch is that for rank 2, both sides of u = u * 0 = 0 vanish at T = 0, so the trivial character does not pin down u(0). The argument for u = 1 in this case requires twisted L-values L(E, chi, 1) and is more delicate. I do NOT carry this through in the present file; it would require a separate analysis. 11a1/p=7 remains the clean main example.

---

## III. Reframed Claim in Path B Language

### III.1 The setup (Stark systems via MCS)

Let T = T_p(E) for E = 11a1, p = 7. Let R = Z_p, Lambda = R[[T]] (the cyclotomic Iwasawa algebra). Let F = F_can be the canonical (Greenberg / Bloch-Kato) Selmer structure on T:

- At v = 7: F_v = image of H^1(Q_7, T_7^+) -> H^1(Q_7, T)
- At v = 11 (bad prime): F_v = unramified condition (Bloch-Kato finite part)
- At all other v: F_v = unramified condition

The Selmer complex SC(T) = R Gamma_F~(Q, T) (Nekovar's notation) is a perfect complex of Lambda-modules of Euler characteristic 0 (because chi(F) = 1 for the canonical structure on a rank-2 representation -- the "core rank" is 1 since both H^0 and the H^2-based dual contribute 0 to the alternating sum once Hyp 2.11 is in force).

By **MCS Theorem 3.4** (whose hypotheses hold for our (E, p) -- see Section II.2):

    varpi : det^{-1}_{Lambda}(SC(T))  -->  SS_1(T, F_can)

is a canonical isomorphism, where

    SS_1(T, F_can) := lim_{n in N} ( wedge^{1+nu(n)} H^1_{F^n}(Q, T) (x) (x)_{q | n} H^1_{/F}(Q_q, T)^* )

(Definition 3.2 of MCS, with R replaced by Lambda; the Lambda-adic version is established in MCS Section 4 / Bullach-Burns arXiv:2509.13894 Theorem 4.20.)

By **MCS Proposition 3.3**, SS_1(T, F_can) is a free Lambda-module of rank 1.

### III.2 Two specific generators of SS_1

**Generator 1: epsilon^Stark = epsilon^{MSD} from the BF/det side.**

**This is exactly the construction in MCS Remark 3.14** (arXiv:2603.23978, line 1504-1546 of the extracted PDF text at `/tmp/mcs.txt`). MCS Remark 3.14 states (paraphrasing):

> Let Q_∞/Q be the cyclotomic Z_p-extension and Lambda = Z_p[[Gamma]] the Iwasawa algebra. Let T = T_p(E) ⊗_{Z_p} Lambda be the cyclotomic deformation. Let L^{MSD} in Q(Lambda) be the Mazur-Swinnerton-Dyer p-adic L-function. Then Mazur's cyclotomic Iwasawa main conjecture is equivalent to: Q(Lambda) ⊗^L_Lambda R Gamma_F~(Q, T) is acyclic, and there is a **unique** Lambda-basis
>
>     z_∞^{MSD} in det^{-1}_Lambda(R Gamma_F~(Q, T))
>
> such that the canonical isomorphism Q(Lambda) ⊗ det^{-1} → Q(Lambda) sends z_∞^{MSD} to L^{MSD}.
>
> Using this element, MCS define a Stark system
>
>     epsilon_{n,m}^{MSD} := varpi_{n,m}^{cyc}(z_m^{MSD})  in SS_0(A_{n,m})
>
> and note that Fitt^i(Sel_{p^n}(E/Q_m)^*) = I_i(epsilon_{n,m}^{MSD}), giving Kurihara's structure theorem as a direct consequence.

So **epsilon^Stark in our notation IS epsilon^{MSD} of MCS Remark 3.14.** It is defined as the unique element whose image under the determinant-to-Q(Lambda) isomorphism is L_p(E). Its existence requires the IMC of Kato + Skinner-Urban (to force the acyclicity of Q(Lambda) ⊗ R Gamma_F~), which holds under the hypotheses we verified for 11a1/p=7. This is published as a remark in the March 2026 MCS paper but is essentially a direct consequence of Theorem 3.4 once the IMC is in place.

Set:

    epsilon^Stark := varpi(z_∞^{MSD})  in SS_0(A_{n,m}) for each (n,m), assembling to a Lambda-Stark system.

Note: MCS write SS_0 (rank-0 Stark systems) in Remark 3.14, because for the cyclotomic tower the core rank is 0 once you take Lambda-coefficients. The "rank 1" SS_1 statement I used in Section III.1 becomes SS_0 in the Lambda-adic cyclotomic formulation. I'll treat the two as interchangeable at the level of this document; the key fact is that both are free of rank 1 over the appropriate base ring (Z_p or Lambda).

**Generator 2: epsilon^Kato from Kato's Euler system.**

Kato's zeta element z_Kato in H^1_Iw(Q_cyc, T) is the canonical Iwasawa cohomology class characterized by

    Perrin-Riou(z_Kato) = L_p(E) (up to an explicit normalization)

(Kato Asterisque 295 Thm 12.5.) The Burns-Sakamoto-Sano construction (arXiv:1805.08448, Section 5) takes z_Kato to a Stark system epsilon^Kato in SS_1. (This is the upgrade of the classical Kolyvagin derivative to a Stark system. For r = 1 -- i.e., core rank 1, our setting -- it specializes to a single Iwasawa cohomology class twisted by the wedge-power formalism of MCS Definition 3.2.)

**Both generators live in the free rank-1 module SS_1.** Therefore there exists a unique u in Lambda^x such that

    epsilon^Stark = u * epsilon^Kato.    (*)

This is the "u" of our reframed claim.

### III.3 What u encodes

The unit u is precisely the discrepancy between two generators of det^{-1}(SC): the IMC-canonical one (Z_BF) and the Kato/PR-canonical one (L_p(E) up to the BSS Stark upgrade). Equivalently:

    u = Z_BF / L_p(E)   in Lambda^x

By the IMC, (Z_BF) = (L_p(E)) as IDEALS, so u is a UNIT. The question "u = 1" is the question of whether they are equal as ELEMENTS, not just as ideals. This is the "ETNC at the prime p" question, sometimes called the "p-part of ETNC for h^1(E)(1)/Q with cyclotomic coefficients."

**Known cases of "u = 1":**
- CM elliptic curves with good ordinary p: PROVED by Bullach-Burns 2025 (arXiv:2509.13894).
- Tate motives over Q: PROVED by Burns-Greither 2003 (the original equivariant ETNC for cyclotomic units).
- Non-CM elliptic curves over Q: OPEN in general; conjecturally u = 1 for all optimal curves.

So u = 1 for non-CM curves like 11a1 is a CONJECTURE, not a theorem. The original `determine-unit-u/findings.md` claimed it as a theorem, justified by an argument that did not actually work (Path A via Kolyvagin systems through nonexistent BF observables).

---

## IV. The u(0) = 1 Calculation at the Trivial Character (Rigorous)

This calculation IS rigorous. It does not require BF observables, TQFT gluing, or Kolyvagin systems. It only requires:

(a) MCS Theorem 3.4 (verified to apply for 11a1/p=7 in Section II.2).
(b) Kato's explicit reciprocity at the trivial character (Asterisque 295 Thm 12.5).
(c) The interpolation property of L_p(E).

### IV.1 Specialization at T = 0

Specializing the identity (*) at T = 0 (the trivial character of Gamma):

    epsilon^Stark(0) = u(0) * epsilon^Kato(0)   in SS_1(A_0, F_can, P)

where A_0 = T / (gamma - 1) T = T modulo the augmentation ideal of Lambda. For T = T_p(E), A_0 is the p-adic Tate module of E modulo "cyclotomic minus identity", which under Kummer / Bloch-Kato becomes the part of H^1(Q, T) "captured at the trivial character".

For the rank-1 setting we are in (chi(F) = 1, rank-0 elliptic curve, Kato class nonzero at T=0), the Stark system specializes to a single class in H^1_F(Q, T_p(E)) under the natural map SS_1 -> H^1_F. The image is given by the dual exponential applied to the relevant L-value.

### IV.2 Both sides equal (1 - 1/alpha_p)^2 * L(E,1) / Omega

**Kato side (epsilon^Kato(0)):** From Kato Asterisque 295 Theorem 12.5 (the explicit reciprocity law),

    exp*(z_Kato(trivial char)) = (1 - 1/alpha_p)^2 * L(E,1) / Omega_E^+

The BSS Stark system epsilon^Kato is built from z_Kato and its specialization at T = 0 is, under the natural map SS_1 -> H^1_F, equal to z_Kato(trivial char). So

    exp*(epsilon^Kato(0)) = (1 - 1/alpha_p)^2 * L(E,1) / Omega_E^+

**BF side (epsilon^Stark(0)):** By MCS Theorem 3.4 + the IMC, the basis z_BF of det^{-1}(SC) corresponds under varpi to a Stark system epsilon^Stark whose specialization at T = 0 is determined by the value L_p(E)(0) under the specialization map for det^{-1}(SC). And L_p(E)(0) is, by the very definition of the p-adic L-function via interpolation against modular symbols,

    L_p(E)(0) = (1 - 1/alpha_p)^2 * L(E,1) / Omega_E^+

(This is the standard interpolation formula at the trivial character; see e.g. Greenberg-Stevens or the original Mazur-Tate-Teitelbaum.)

### IV.3 Conclusion: u(0) = 1

Both sides give literally the same value (the same explicit formula). Both are nonzero for 11a1/p=7 (since L(E,1)/Omega = 1/5 is a 7-adic unit and the Euler factor is a 7-adic unit).

So in (*) specialized at T = 0:

    nonzero unit = u(0) * (same nonzero unit)

forcing **u(0) = 1** in Z_p.

**[SOUND]** This calculation is rigorous. It uses only MCS Theorem 3.4 (whose hypotheses we verified) and Kato's explicit reciprocity (which is a 20-year-old published theorem). No BF correlator framework, no TQFT gluing, no Kolyvagin systems are involved.

**Caveat [QUESTIONABLE]:** The argument requires identifying epsilon^Stark with the IMC-canonical generator of det^{-1}(SC). This identification is done via the IMC of Kato + Skinner-Urban -- which gives the IDEAL equality (Z_BF) = (L_p(E)) -- AND a choice of generator. The choice of generator on the BF side is "the unique element of det^{-1}(SC) whose image under the Fitting-ideal map is L_p(E) on the nose, not just up to a unit." Whether this generator agrees with the BSS-Stark generator at T = 0 (i.e., not merely up to a unit) is essentially the ETNC at T = 0. **It is a theorem in the rank-0 case** because the rank-0 case of ETNC at the trivial character reduces to the BSD formula at p, and Skinner-Urban's IMC + Kato's bound give Sha[p^infty] = 1 for 11a1 at p = 7 (since the analytic Sha is 1 and the IMC gives the algebraic = analytic order). So at T = 0, in this specific case, the equality of ELEMENTS u(0) = 1 follows from the p-part of BSD for 11a1/p=7, which IS a theorem (Sha[7^infty] = 1, all factors line up, both sides = 1/5 as a 7-unit).

**So u(0) = 1 is indeed [SOUND] for 11a1/p = 7.** I'll re-examine this claim more carefully in Section V.

---

## V. The u(zeta_{p^n} - 1) = 1 Step (Honest Status)

For u = 1 in Lambda (not just at T = 0), the argument needs equality at all finite-order character specializations. This is where the argument gets [QUESTIONABLE].

### V.1 What we need

For each n >= 1 and each character chi : Gal(Q(zeta_{p^n})/Q) -> C_p^x, specializing (*) at T_chi := chi(gamma) - 1 gives:

    epsilon^Stark(T_chi) = u(T_chi) * epsilon^Kato(T_chi)   in SS_1(A_n, F_can^chi)

We want u(T_chi) = 1 for all such chi. By Weierstrass preparation, this would force u = 1 in Lambda.

### V.2 Kato's reciprocity at chi

For each chi of conductor p^n:

    exp*(z_Kato(chi)) = (1 - chi(p)/alpha_p)(1 - chi^{-1}(p)/beta_p) * L(E, chi^{-1}, 1) / (Omega^+ * tau(chi))

(Kato Asterisque 295 Thm 12.5; the precise constants depend on conventions for Gauss sums.)

### V.3 BF-side interpolation at chi

For epsilon^Stark, the analogous specialization gives:

    [some explicit value at chi]  =  u(T_chi) * [the Kato value at chi]

The "BF side" is the value of L_p(E) at T_chi, which by the very INTERPOLATION definition of L_p(E) is

    L_p(E)(T_chi) = (1 - chi(p)/alpha_p)(1 - chi^{-1}(p)/beta_p) * L(E, chi^{-1}, 1) / (Omega^+ * tau(chi))

i.e., the same formula. So at the LEVEL OF L-VALUES, both sides give the same number, and u(T_chi) = 1 follows -- but only if we are willing to identify "epsilon^Stark(T_chi) = L_p(E)(T_chi)" and "epsilon^Kato(T_chi) = (Kato's L-value at chi)" as exact equalities, not equalities up to a unit.

### V.4 Where the gap is

The issue is exactly the same as at T = 0, but harder. At T = 0, the rank-0 case of ETNC reduces to BSD at p, which is known for 11a1/p=7. But at finite-order characters chi of CONDUCTOR p^n with n >= 1, the analogous "ETNC at chi" reduces to a Sha-type statement for E twisted by chi over Q(zeta_{p^n}) -- and these higher-cyclotomic-twist Sha statements are NOT all proven.

Specifically, the equality

    epsilon^Stark(T_chi) = "L_p(E)(T_chi) on the nose"

requires that the IMC generator z_BF in det^{-1}(SC) specializes to L_p(E)(T_chi) at T_chi WITHOUT a correction unit. This is the "exact element-level IMC at the chi-twist", which is the "p-part of ETNC for h^1(E)(1) tensored with the chi-twist." For chi = trivial this is BSD-at-p (known here). For chi nontrivial, **this is what u(T_chi) = 1 IS asking** -- so the argument is essentially circular: "u(T_chi) = 1 because the two sides agree on the nose, which is what u(T_chi) = 1 means."

### V.5 What can be honestly asserted

**[SOUND]** For 11a1 at p = 7:
- u in Lambda^x (i.e., u is a unit in the Iwasawa algebra) -- this is the ideal IMC of Kato + Skinner-Urban (2014), holding under the surjective rho_bar + good ordinary + mu = 0 hypotheses we verified in Section II.
- **u(0) = 1**: this is the ELEMENT-LEVEL p-part of BSD for 11a1 at p = 7. It holds by Bullach-Burns arXiv:2509.13894 Corollary 9.7 applied at K = Q (the finite base field), combined with the known p-part of BSD at p = 7 for 11a1:
  - Analytic side: L(E,1)/Omega = 1/5, v_7 = 0
  - Algebraic side: |Sha[7^infty]| * Tam / |tors|^2 = 1 * 5 / 25 = 1/5, v_7 = 0 (and Sha[7^infty] = 0 is forced by p-descent via `E.sha().p_primary_bound(7) = 0` in Sage; see Section IX.5)
  - The p-part of BSD is also the main theorem of Burungale-Castella-Skinner 2024 ([29] in Bullach-Burns; the hypotheses are: p > 3, good ordinary, SL_2 in rho_bar image, analytic rank <= 1. ALL hold for 11a1/p=7.)
  Together these give u(0) = 1 as a **theorem**, not a conjecture.

**[QUESTIONABLE]** For 11a1 at p = 7:
- **u = 1 in Lambda (full Iwasawa-level equality)** is in the spirit of Bullach-Burns Theorem 9.4 + the Rohrlich-based argument in Corollary 9.7's proof. Theorem 9.4 gives the INCLUSION z_{Q_infty}^Kato in im(Theta_{Q_infty, S(K)}). The reverse inclusion (giving equality) is deduced in Cor 9.7 for a finite K using p-BSD at prime-to-p subfields.
  For K = Q (our case), the prime-to-p subfields of K_infty = Q_cyc are just {Q} (since [Q_n : Q] = p^n > 1 for n >= 1), so the condition in Cor 9.7 reduces to p-BSD over Q, which holds for 11a1/p=7.
  **However**, Corollary 9.7 as literally stated is for finite K; to extend its conclusion to the Lambda-adic setting K_infty would require a separate limiting argument. Bullach-Burns do give the limiting argument in the PROOF of Corollary 9.7 (lines 14263-14283 of the extracted PDF text at `/tmp/bb.txt`), arguing that im(Theta_{K_infty})/(Lambda_K * z_{K_infty}^Kato) has no nontrivial invariants -- so the argument SHOULD extend. But I have NOT fully verified that the Rohrlich-based part of the proof applies to K = Q with Q_infty = Q_cyc.
  **My honest status: very likely true but not fully verified from primary sources in this run.**

**[GAP]** If it turns out Bullach-Burns' argument does NOT give Lambda-adic element-level equality for non-CM rational elliptic curves in the rank-0 case, then u = 1 in Lambda remains the "equivariant Tamagawa number conjecture" for h^1(E)(1) over Q_cyc with Lambda coefficients, which is conjectural for non-CM curves. In that scenario the honest status is: u(0) = 1 is a theorem (Section IV), u = 1 is a conjecture.

### V.6 The "density of Kolyvagin primes" argument from the original findings

The original `determine-unit-u/findings.md` Sections III.5-III.7 had a different argument: instead of going through finite-order characters and Weierstrass, it used Kolyvagin primes ell with v_p(I_ell) = k and showed u ≡ 1 mod p^k for all k via the (broken) BF correlator = Kurihara identity. **That argument is not rescuable** for two reasons:

1. **The BF correlator identity exp*(kappa^BF_ell) = delta_ell does not exist.** It comes from the schematic Section VIII of `route-bf-kolyvagin-system/findings.md`, which is exactly the section that `lemma-tqft-kolyvagin-formal/findings.md` shows is unsupported by Park-Park.

2. **Even if you replaced kappa^BF with epsilon^Stark (the genuine MCS Stark system), there is no analog of "exp* applied at Kolyvagin prime ell".** The Stark system formalism uses wedge-power transfer maps v_{n,m}, not the Mazur-Rubin finite-singular comparison phi^fs_ell. So the per-Kolyvagin-prime congruence "u ≡ 1 mod I_ell" does not have a Path B analog. The Kim Kurihara-number theorem is about Mazur-Rubin Kolyvagin systems, not Stark systems.

So the rescue here LOSES the per-prime density argument and replaces it with the (genuine) interpolation argument at finite-order characters -- which then runs into the ETNC gap described above.

**Net effect:** The reframe gives u(0) = 1 rigorously and "u in Lambda^x" rigorously, but does NOT give u = 1 in Lambda unconditionally. The unconditional claim was an artifact of the broken BF correlator framework.

---

## VI. Numerical Verification (SageMath)

I ran the following verifications. (See Section IX for the full Sage transcripts.)

### VI.1 All MCS hypotheses for 11a1/p=7

```
sage: E = EllipticCurve('11a1')
sage: p = 7
sage: E.has_good_reduction(p)
True
sage: E.ap(p)
-2
sage: E.change_ring(GF(p)).cardinality()
10
sage: 10 % 7
3                                  # nonzero, so non-anomalous
sage: E.galois_representation().is_surjective(7)
True                               # rho_bar surjective at 7
sage: E.galois_representation().reducible_primes()
[5]                                # only 5 is reducible; 7 is fine
sage: E.torsion_subgroup().order()
5
sage: E.tamagawa_product()
5
sage: 5 * 5 * 10 % 7
5                                  # nonzero, Remark 2.12 condition holds
sage: E.is_semistable()
True
sage: E.optimal_curve() == E
True
sage: E.manin_constant()
1
sage: E.lseries().L_ratio()
1/5                                # L(E,1)/Omega; 7-unit
sage: E.sha().an()
1                                  # analytic order of Sha = 1
```

ALL MCS hypotheses verified.

### VI.2 The p-adic L-function at T = 0

```
sage: Lp = E.padic_lseries(p)      # 11a1 p-adic L-fn at p=7
sage: Lp.series(prec=8, n=4)       # 8 terms, accuracy O(7^4)
[ ... output below ... ]
```

I record the actual Sage output in Section IX. The relevant fact is that **L_p(E, 0) is a 7-adic unit** (because v_7(L(E,1)/Omega) = 0 and v_7((1 - 1/alpha_7)^2) = 0). This matches the value of (1 - 1/alpha_7)^2 * (1/5) computed independently from a_7 = -2.

### VI.3 Comparison with the original 11a1/p=5 example

For contrast, at p = 5:

```
sage: Lp5 = E.padic_lseries(5)
sage: v_5( (1 - 1/alpha_5)^2 ) = 2     (because alpha_5 = 1 mod 5 -- this is the "anomalous" condition!)
sage: v_5(1/5) = -1
sage: v_5(L_p(E,0)) = 2 - 1 = 1
```

So the trivial-character value at p = 5 has v_5 = 1, NOT 0. Combined with the reducibility of rho_bar at p = 5, this is exactly why MCS Hypothesis 2.11(iii) FAILS at (11a1, 5). At p = 7, both factors are units and the hypothesis is fine.

### VI.4 Sha for 11a1 at p = 7

By Skinner-Urban + analytic Sha = 1, **Sha[7^infty] = 0** for 11a1. This means the p-part of BSD at p = 7 holds with both sides equal to 1 (no Sha contribution, Tam factor 5 is a 7-unit, tors 5 is a 7-unit). So u(0) = 1 is INDEED a theorem at the trivial character for 11a1/p=7.

---

## VII. What This Means for the Campaign

### VII.1 Corrections to make in `../determine-unit-u/findings.md`

The original file is largely WRONG in its main claims and needs the following changes:

**[CORRECTION 1]** Replace the main worked example throughout. Every reference to "11a1 at p = 5" should become "11a1 at p = 7" (or be removed). The original p = 5 example is invalid because:
- 5 | |E~(F_5)| = 5 (anomalous)
- rho_bar is reducible at 5 (E has a 5-isogeny)
- Both failures are flagged in `verify-mcs-hypotheses/findings.md` Section IV.2 as "DOUBLE FAILURE"

**[CORRECTION 2]** Strike the entire BF correlator framework. Sections III.3 through III.7 of `determine-unit-u/findings.md` use the identity exp*(kappa^BF_ell) = delta_ell, which has no source: see `lemma-tqft-kolyvagin-formal/findings.md` Sections I.8-I.10 and IX. Park-Park does not define BF observables, so kappa^BF_ell is not constructed.

**[CORRECTION 3]** Restate the conclusion. Replace "u = 1 in Lambda for all optimal semistable curves" with the more honest pair:
- "u in Lambda^x by IMC of Kato + Skinner-Urban (a unit)"
- "u(0) = 1 conditional on the p-part of BSD at the trivial character (theorem for 11a1/p=7 because Sha[7^infty] = 1 by Sha analytic = 1 + IMC)"
- "u = 1 in Lambda for all T is the ETNC at p, currently a CONJECTURE for non-CM curves, theorem only for CM curves (Bullach-Burns 2025)"

**[CORRECTION 4]** The Section II "u(0) = 1 at the trivial character" calculation is essentially correct for any rank-0 curve where the hypotheses hold -- but the reasoning for WHY both sides give the same explicit value should be cited differently. Currently it cites Park-Park-derived BF interpolation. Replace this with the standard p-adic L-function interpolation formula (Mazur-Tate-Teitelbaum, Greenberg-Stevens) for L_p(E)(0), and Kato's Asterisque 295 Theorem 12.5 for the Kato side.

**[CORRECTION 5]** The Section III.5 "Numerical Data for 11a1 at p=5" table cannot stand. The Kolyvagin primes listed (31, 41, 61, 251, 751, 1301, 1801, 21001) are all computed with respect to the WRONG prime where MCS does not apply. They should be re-run for 11a1/p=7 OR removed. The Kim identity exp*(kappa^Kato_ell) = delta_ell is true on its own as a theorem about Kato's CLASSICAL Kolyvagin system (not the BF version), so the per-prime computations have meaning -- but only on the Kato side, and only for showing things about kappa^Kato, not about a comparison with kappa^BF (which does not exist).

**[CORRECTION 6]** Section VII.1 (Detailed Computations: 11a1 at p = 5) should be REPLACED with the analogous computations for 11a1 at p = 7, OR it should be clearly labeled as "the broken example, kept for archival purposes." The current section gives mu = 1 for L_p(E) at p = 5, which is CONSISTENT with the anomalous nature of the prime (mu can be nonzero when the prime is anomalous). At p = 7, mu = 0 by Kato's theorem, consistent with the rest of the chain.

**[CORRECTION 7]** Section IV.2 ("Known Cases" table) overstates "Semistable, rank 0, Sha[p] = 0: PROVED (our argument)." Replace with: "PROVED via IMC + p-part of BSD at the trivial character only (i.e., u(0) = 1, not u = 1 in Lambda)." The Lambda-adic statement is conjectural (= ETNC).

### VII.2 What survives from `determine-unit-u/findings.md`

- The general framing that u is a Lambda-adic unit (this is the IMC and is rigorous).
- The observation u(0) = 1 for rank-0 curves where the trivial-character L-value is a p-unit (this is rigorous for 11a1/p=7).
- The Bullach-Burns CM case: u = 1 PROVED for CM curves with good ordinary p (theorem of Bullach-Burns, NOT something we proved).

### VII.3 What the campaign loses

- The CLAIM of u = 1 unconditionally for non-CM rank-0 semistable curves over Q. This was overreach. Drop it.
- The "BF correlator" framework altogether. Use Path B (Stark systems via MCS) instead.
- The rhetorical "11a1 at p = 5" example. Replace with "11a1 at p = 7" (rank 0) or "643a1 at p = 7" (rank 2).

### VII.4 What the campaign gains

- An honest, calibrated assessment of which steps are theorems vs conjectures.
- A clean worked example (11a1/p=7) where every cited hypothesis genuinely holds.
- A clear identification of the remaining gap: equality of generators in det^{-1}(SC) between the IMC-canonical and Kato-canonical sides at finite-order characters of conductor p^n with n >= 1 (= the ETNC refinement of the IMC).

---

## VIII. Self-Assessment

| Step | Label | Why |
|---|---|---|
| All MCS hypotheses for 11a1/p=7 | [SOUND] | Verified in Sage (Section II.2 + IX.1); matches Section IV.2 of `verify-mcs-hypotheses/findings.md`. |
| MCS Theorem 3.4 applies | [SOUND] | Hypotheses verified. MCS is a March 2026 preprint, but accepted as the working framework. |
| MCS Remark 3.14 gives the cyclotomic Lambda-adic version | [SOUND] | Direct quote from `/tmp/mcs.txt` lines 1504-1546; construction of epsilon^{MSD} := varpi(z_infty^{MSD}) where z_infty^{MSD} is the unique element mapping to L_p(E). |
| SS_0(A_{n,m}) free of rank 1 over Lambda, epsilon^{MSD} generator | [SOUND] | MCS Proposition 3.3 + Remark 3.14. |
| Kato Stark system epsilon^Kato exists | [SOUND] | BSS arXiv:1805.08448 + Bullach-Burns Section 9 explicitly construct the Stark/determinantal image of Kato's Euler system. |
| Both live in det^{-1}(SC), so they differ by u in Lambda^x | [SOUND] | Free rank 1 module fact + IMC ideal equality (Kato + Skinner-Urban 2014). |
| **u(0) = 1** for 11a1/p=7 | **[SOUND]** | Bullach-Burns Corollary 9.7 (K = Q) + known p-part of BSD at p=7 for 11a1 (Burungale-Castella-Skinner 2024 + Sha[7^inf] = 0 via `E.sha().p_primary_bound(7) = 0`). |
| **u = 1 in Lambda** for 11a1/p=7 | [QUESTIONABLE] | Bullach-Burns Theorem 9.4 gives the one-sided inclusion z_{Q_inf}^Kato in im(Theta_{Q_inf}). The Rohrlich-based argument in the proof of Cor 9.7 sketches the reverse inclusion at K = Q but I have not fully verified the Lambda-adic version applies directly. Plausible but unverified in this run. |
| At finite-order characters chi of conductor p^n | [QUESTIONABLE] | Would follow from u = 1 in Lambda, or from a chi-by-chi version of Cor 9.7. |
| Numerical interpolation check Lp(E, 0) = (1-1/alpha)^2 * L(E,1)/Omega for 11a1/p=7 | [SOUND at O(7^6)] | Direct Sage computation; agreement with Lp.series(prec=6, n=4) to all computed digits. |
| 11a1/p=5 is BROKEN (double failure) | [SOUND] | Sage: 5 | |E(F_5)| = 5 (anomalous); 5 in reducible primes; MCS Hyp 2.11(iii) and Hyp 2.17 both fail. |
| Replacement of `determine-unit-u/findings.md` claims | [SOUND] | The CORRECTIONS in Section VII.1 are well-supported by this document. |

---

## IX. SageMath Verification Transcripts

The Sage script and output are in this section. (Computations done in Sage 10.8 on macOS.)

### IX.1 Hypothesis verification

```python
sage: E = EllipticCurve('11a1')
sage: p = 7
sage: print(f"Conductor: {E.conductor()}")
Conductor: 11
sage: print(f"Rank: {E.rank()}")
Rank: 0
sage: print(f"Torsion order: {E.torsion_subgroup().order()}")
Torsion order: 5
sage: print(f"Tamagawa product: {E.tamagawa_product()}")
Tamagawa product: 5
sage: print(f"Semistable: {E.is_semistable()}")
Semistable: True
sage: print(f"Optimal: {E.optimal_curve() == E}")
Optimal: True
sage: print(f"Manin constant: {E.manin_constant()}")
Manin constant: 1
sage: print(f"Good reduction at p: {E.has_good_reduction(p)}")
Good reduction at p: True
sage: print(f"a_p: {E.ap(p)}")
a_p: -2
sage: Ebar = E.change_ring(GF(p))
sage: print(f"|E(F_p)|: {Ebar.cardinality()}")
|E(F_p)|: 10
sage: print(f"Non-anomalous (p does not divide |E(F_p)|): {Ebar.cardinality() % p != 0}")
Non-anomalous (p does not divide |E(F_p)|): True
sage: rp = E.galois_representation().reducible_primes()
sage: print(f"Reducible primes for rho_bar: {rp}")
Reducible primes for rho_bar: [5]
sage: print(f"rho_bar irreducible at p: {p not in rp}")
rho_bar irreducible at p: True
sage: print(f"rho_bar surjective at p: {E.galois_representation().is_surjective(p)}")
rho_bar surjective at p: True
sage: print(f"L(E,1)/Omega: {E.lseries().L_ratio()}")
L(E,1)/Omega: 1/5
sage: print(f"Analytic order of Sha: {E.sha().an()}")
Analytic order of Sha: 1
```

### IX.2 The p-adic L-function at T=0

```python
sage: Lp = E.padic_lseries(7)
sage: Lp.series(prec=6, n=4)
5 + 7 + 5*7^2 + 4*7^3 + 7^4 + 2*7^5 + O(7^6)
 + (5 + 7 + 3*7^2 + O(7^3))*T
 + (6 + 3*7 + 4*7^2 + O(7^3))*T^2
 + (4*7^2 + O(7^3))*T^3
 + (4 + 7 + 6*7^2 + O(7^3))*T^4
 + (3 + 5*7 + 2*7^2 + O(7^3))*T^5
 + O(T^6)
```

**The constant term is `5 + 7 + 5*7^2 + 4*7^3 + 7^4 + 2*7^5 + O(7^6)`, which has v_7 = 0 (a 7-adic unit).**

### IX.3 Interpolation formula check

The interpolation formula predicts Lp(E, 0) = (1 - 1/alpha_7)^2 * L(E,1)/Omega.
Computing in Q_7 with prec=20:

- Characteristic polynomial of Frobenius: x^2 + 2x + 7
- Unit root alpha_7 = 5 + 3*7 + 4*7^2 + 6*7^3 + 2*7^4 + 5*7^5 + O(7^6) + ... (v_7 = 0)
- (1 - 1/alpha_7)^2 = 4 + 7 + 5*7^2 + 2*7^3 + 7^4 + 4*7^5 + O(7^6) + ... (v_7 = 0)
- L(E,1)/Omega = 1/5 = 3 + 7 + 4*7^2 + 5*7^3 + 2*7^4 + 7^5 + O(7^6) + ... (v_7 = 0)
- Product = (1 - 1/alpha_7)^2 * (1/5) = **5 + 7 + 5*7^2 + 4*7^3 + 7^4 + 2*7^5 + O(7^6) + ...**

**This matches the constant term of `Lp.series(prec=6, n=4)` EXACTLY.** Numerical
verification of the interpolation formula at T = 0, and confirmation that the
trivial-character value is a 7-adic unit. **[SOUND numerical check at O(7^6)].**

### IX.4 Comparison with the broken p=5 example

```
--- p = 5 (BROKEN) ---
a_p = 1
|E(F_p)| = 5
Anomalous (p divides |E(F_p)|): True  [FAIL Hyp 2.11(iii)]
rho_bar reducible at p: True  [FAIL Hyp 2.17]
rho_bar surjective at p: False
v_p(alpha) = 0, v_p((1-1/alpha)^2) = 2  (positive -- because alpha_5 = 1 mod 5)
v_p(L(E,1)/Omega) = v_p(1/5) = -1
v_p(interpolation value) = 1  (positive -- anomalous behavior)
MCS verdict: FAILS

--- p = 7 (CLEAN) ---
a_p = -2
|E(F_p)| = 10
Anomalous (p divides |E(F_p)|): False  [OK]
rho_bar reducible at p: False  [OK]
rho_bar surjective at p: True
v_p(alpha) = 0, v_p((1-1/alpha)^2) = 0
v_p(L(E,1)/Omega) = 0
v_p(interpolation value) = 0  (a unit -- clean trivial-character)
MCS verdict: APPLIES
```

### IX.5 Sha bound at p = 7

```python
sage: E.sha().an()
1                                   # analytic order = 1
sage: E.sha().p_primary_bound(7)
0                                   # p-descent forces Sha[7^infty] = 0
sage: E.sha().p_primary_bound(5)
0                                   # also at p = 5, via p-descent
```

**Sha[7^infty] = 0 is RIGOROUS for 11a1 (bound from p-descent, not just analytic).**
Combined with tors = 5 and Tam = 5 (both 7-units), the **p-part of BSD at p = 7 is
unconditionally established for 11a1**: both the analytic and algebraic sides equal
1/5 as 7-adic units. This is what makes u(0) = 1 a THEOREM (not a conjecture) for
this specific (E, p).

### IX.6 All Sage outputs

The Sage scripts `compute.sage`, `compare_broken.sage`, `sha_check.sage`,
`pbsd_check.sage`, and `final_lp_check.sage` are saved in this directory
alongside this findings file. They can be re-run on any Sage 10.x installation
to regenerate the numerical data.

### IX.7 Precise Lp(E,0) = interpolation formula numerical check

```python
sage: Lp = E.padic_lseries(7)
sage: series = Lp.series(prec=8, n=5)
sage: zero_coeff = series[0]           # constant term in T
sage: zero_coeff
5 + 7 + 5*7^2 + 4*7^3 + 7^4 + 2*7^5 + 4*7^6 + O(7^7)

sage: Zp_7 = Zp(7, prec=25)
sage: R = PolynomialRing(Zp_7, 'x')
sage: f = R.gen()**2 + 2*R.gen() + 7       # x^2 - a_7*x + 7, a_7 = -2
sage: alpha = [r for r,_ in f.roots() if r.valuation() == 0][0]
sage: interp = (1 - 1/alpha)^2 * (Zp_7(1)/Zp_7(5))
sage: interp
5 + 7 + 5*7^2 + 4*7^3 + 7^4 + 2*7^5 + 4*7^6 + 4*7^7 + 2*7^8 + ... + O(7^25)

sage: (zero_coeff - interp).valuation()
7                                          # agreement to full Sage precision
```

**Verdict:** Sage's p-adic L-function constant term agrees with
`(1 - 1/alpha_7)^2 * L(E,1)/Omega` to the full precision Sage can compute (O(7^7)).
The interpolation formula is numerically verified. Both sides are 7-adic units
(v_7 = 0), confirming that the "u(0) = 1" comparison is happening between two
NONZERO elements. **[SOUND numerical check.]**

---

## X. References

1. **Macias Castillo, D. and Sano, T.** "On Selmer complexes, Stark systems and derived p-adic heights." arXiv:2603.23978 (March 2026). Theorem 3.4: det^{-1}(SC) = SS_chi(F).

2. **Bullach, D. and Burns, D.** "On Euler systems and Nekovar-Selmer complexes." arXiv:2509.13894 (Sept 2025). Lambda-adic version of MCS, plus proof of u = 1 for CM elliptic curves.

3. **Burns, D., Sakamoto, R., and Sano, T.** "On the theory of higher rank Euler, Kolyvagin and Stark systems." arXiv:1805.08448 (2018). The Stark system attached to an Euler system (Section 5).

4. **Kato, K.** "p-adic Hodge theory and values of zeta functions of modular forms." Asterisque 295 (2004), 117-290. Theorem 12.5: Kato's zeta element and explicit reciprocity.

5. **Skinner, C. and Urban, E.** "The Iwasawa main conjectures for GL_2." Inventiones Math. 195(1) (2014), 1-277. IMC (= ideal equality).

6. **Cesnavicius, K.** "The Manin constant in the semistable case." Compositio Math. 158(6) (2022), 1143-1170. c_E = 1 for semistable optimal.

7. **Mazur-Rubin.** "Kolyvagin systems." Memoirs AMS 168(799) (2004). Theorem 5.2.10 (KS_1 free), Theorem 4.1.7 (core vertices exist when E[p] irreducible).

8. **Kim, C.-H.** "Kolyvagin's conjecture and Kurihara numbers." arXiv:1709.05780 (2020). Used in the BROKEN argument; not used in this reframe.

9. **Park-Park** "Arithmetic BF theory and the BSD conjecture." arXiv:2602.19621 (Feb 2026). NOT used in this reframe (the BF correlator framework is dead per `lemma-tqft-kolyvagin-formal/findings.md`).
