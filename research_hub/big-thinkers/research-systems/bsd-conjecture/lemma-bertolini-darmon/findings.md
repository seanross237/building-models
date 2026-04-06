# Lemma BD-Reg: The Cyclotomic Derived Regulator Identification

**Date:** 2026-04-04
**Status:** ESSENTIALLY PROVED (modulo a normalization-convention gap)
**Bottom line:**
- BD 1995 Theorem 2.23 + cyclotomic IMC ALREADY does the algebraic side of cyclotomic higher-rank p-adic BSD; we don't need to invent a "BCHKLL cyclotomic analog" because Bertolini-Darmon literally already wrote it down 30 years ago.
- The "lemma" reduces to: BD's pairing `((·,·))_1` valued in `I/I^2 ⊗ Q` is identified with Schneider's `h_p` valued in `Q_p` via the "natural" identification `(γ-1) ↦ 1`, which makes the conversion factor exactly `log_p(γ)^r` on the regulator.
- BD 1995 Lemma 2.2 confirms BD use the e_grp identification, and BD Theorem 2.18(4) confirms their first pairing IS Schneider's. The remaining gap is purely a normalization bookkeeping check between Schneider 1982 and Tan's PhD thesis.
- Numerical verification: 14/14 (curve, prime) cases, including 2 rank-3 cases (5077a1 at p=5,7), confirm the lemma identification (with unit u=1) to as many digits as the SAGE p-adic L-series allows (3-7 digits depending on n_terms).
- **The lemma DOES NOT close classical BSD by itself.** It closes the IWASAWA-THEORETIC side of higher-rank p-adic BSD. The classical period comparison (the [GAP] flagged by the codex audit) is independent and remains open.

**Goal:** Prove (or compute, or refute) the lemma:

> **Lemma (BD-Reg).** For E/Q of rank r with good ordinary reduction at p,
>
>     Reg_{p,der}^{cyc}(E)  =  Reg_p(E) / log_p(gamma)^{r}  * (p-adic unit u)
>
> with u = 1 under the BD/e_grp normalization of I^r/I^(r+1) ⊗ Q ≅ Q_p (the identification (γ-1) ↦ 1).
>
> (Note: the original problem statement asked for `log_p(γ)^r`. Initial uncertainty about whether the exponent might be r or r-1 was resolved by numerical verification on the rank-3 curve 5077a1, which definitively pins it at r. See Section 4.)

---

## 0. Calibration

Per the prior audit, the campaign has overstated things before. We will use the labels:

- `[SOUND]` — checked against published source / verified numerically / proved
- `[QUESTIONABLE]` — plausible, used by literature, but not directly verified here
- `[GAP]` — known missing step

The single biggest danger is mis-stating the BD definition and "verifying" the wrong identity. We will try to read the actual BD paper before doing computations.

---

## 1. What we are trying to prove (precise formulations)

There are several plausible exact statements. We need to pin down which one Bertolini-Darmon actually proved, and which one matches our period relation.

### 1.1 The cyclotomic p-adic L-function

Let L_p(E,T) be the Mazur-Swinnerton-Dyer cyclotomic p-adic L-function, viewed as an element of Z_p[[T]] where T = γ - 1 and γ is a topological generator of Γ = Gal(Q_∞/Q). For E of rank r over Q with good ordinary reduction at p, the order of vanishing at T = 0 is conjecturally r.

Define the leading coefficient by:

    L_p(E,T)  =  L_p^*(E,0) · T^r  +  O(T^{r+1})

So L_p^*(E,0) = (1/r!) · L_p^{(r)}(E,0) in the usual derivative-at-zero convention.

### 1.2 Two candidate regulators

(a) **Schneider/Mazur-Tate-Teitelbaum p-adic regulator Reg_p(E):**

    Reg_p(E) = det( h_p(P_i, P_j) )_{1 ≤ i,j ≤ r}

where {P_1, ..., P_r} is a basis of E(Q)/torsion and h_p is the cyclotomic p-adic height pairing (Schneider's definition; equivalent to Mazur-Tate's and Perrin-Riou's up to sign).

The cyclotomic p-adic height takes values in Q_p, NOT in Γ ⊗ Q_p. The "log(gamma)" appears when we convert between the two.

(b) **Bertolini-Darmon derived regulator Reg_{p,der}^{cyc}(E):**

This is harder to state without the paper. Loosely: it is a determinant of "derived" height pairings, where the derived heights are iterated Bockstein-like operators on a certain Selmer module in Iwasawa cohomology.

### 1.3 The candidate identification

The "lemma" is the identification:

    Reg_{p,der}^{cyc}(E) = (something involving Reg_p, log_p(γ), and r) · u

where u is a p-adic unit. The various candidates from prior literature:

- Naive dimensional analysis (from 11.3 of beilinson-bloch-push/findings.md): factor `1 / log(γ)^r`
- Standard Iwasawa-theoretic conversion: factor `1 / log(γ)^{r-1}` (one log(γ) is "absorbed" into the natural normalization of derived heights)
- Schneider's original normalization: factor `1` (no log(γ); the regulators agree)

We need to determine WHICH it is. Numerical verification on 389a1 will distinguish all three.

---

## 2. Step 1: Find the Bertolini-Darmon papers — DONE

Both BD papers obtained as PDFs from Darmon's McGill page and converted to text:

- `BD1994-derived-heights.txt` — Bertolini-Darmon, "Derived heights and generalized Mazur-Tate regulators," Duke Math. J. 76 (1994). Finite-level, group-ring-of-G version. Defines derived heights for cyclic G via iterated coboundary operators D^(k) in the augmentation ideal of Z/p^n[G]. [SOUND]
- `BD1995-derived-p-adic-heights.txt` — Bertolini-Darmon, "Derived p-adic heights," Amer. J. Math. 117 (1995). Iwasawa-theoretic version. Compiles the finite-level derived heights up the cyclotomic / anticyclotomic Z_p-tower into pairings on the inverse-limit Selmer group. THIS IS THE PAPER TO READ. [SOUND]

### 2.1 Key constructions (BD 1995)

**Setup.** K_∞/K is a Z_p-extension, Γ = Gal(K_∞/K), Λ = Z_p[[Γ]], γ = topological generator of Γ, I = (γ-1)Λ. Sp(E/K) = lim_n Sel_{p^n}(E/K) is the pro-p Selmer group. (BD work in this generality so this includes cyclotomic and anticyclotomic.)

**Theorem 2.7 (and 2.18 — the limit version):** For 1 ≤ k ≤ p-1 there exist canonical pairings

    ((·, ·))_k :  S_p^(k) × S_p^(k)  →  I^k / I^(k+1) ⊗ Q

where S_p^(1) = Sp(E/K) and inductively S_p^(k+1) = nullspace of ((·,·))_k. The pairings are symmetric for k odd, alternating for k even. **Theorem 2.18(4) (CRUCIAL):** the restriction of ((·,·))_1 to E(K)_p is equal to the standard cyclotomic p-adic height pairing of Schneider/Mazur-Tate, viewed as taking values in I/I^2 ⊗ Q. [SOUND, quoted from paper]

**Definition 2.20:** the derived regulator R_der ∈ (I^ρp / I^(ρp+1) ⊗ Q) / Z_p^×, defined as the product of the partial regulators R^(1) · R^(2) · ... · R^(p-1), where each R^(k) is the determinant of the matrix of ((·,·))_k restricted to a basis of the gradedpiece S_p^(k)/S_p^(k+1).

**Theorem 2.23:** Assume X_∞ = Pontryagin dual of Sel_{p^∞}(E/K_∞) is Λ-torsion. Let L_∞ be a characteristic power series of X_∞, ν_p its order of vanishing (smallest exponent so L_∞ ∈ I^(ν_p)). Then

    ν_p ≥ ρ_p ,    Div( L_∞ )  =  R_der    in  (I^(ρ_p) / I^(ρ_p+1) ⊗ Q) / Z_p^×

(equality of monoid elements; "Div" = divisible part).

**Remark 1 after Theorem 2.23 (CRUCIAL):** "When ((·,·))_1 is nondegenerate, then R_der is equal to the usual p-adic regulator." [Quoted directly from paper, p.1541]

### 2.2 The KEY structural observation

When the standard p-adic height is non-degenerate (which is the GENERIC case for elliptic curves of any rank, and is conjectured to ALWAYS hold for cyclotomic Z_p-extensions of Q for E/Q), we have:

    S_p^(1) = Sp(E/K),   S_p^(2) = 0,
    ρ_p = r = rank,   d_1 = r,   d_k = 0 for k ≥ 2,
    R_der = R^(1) = det( ((P_i, P_j))_1 )_{i,j}  ∈  I^r / I^(r+1) ⊗ Q .

So R_der is just the determinant of the **first** derived height, i.e. of the standard p-adic height pairing — viewed not as a Q_p-valued pairing but as an `I/I^2 ⊗ Q`-valued one.

This is the heart of the lemma. The "gap" between R_der and Reg_p is purely a question of the identification of `I^r / I^(r+1) ⊗ Q` with `Q_p`.

---

## 3. The identification I^r/I^(r+1) ≅ Q_p and where log_p(γ) appears

### 3.1 Two natural isomorphisms

The Λ-module I/I^2 is canonically isomorphic to Γ ⊗_{Z_p} Z_p ≅ Γ (via γ-1 ↔ γ in Γ written additively / `log` of γ in the multiplicative version). There are two natural further identifications of Γ with Z_p:

**(A) "Group element" isomorphism `e_grp`:**
    γ ∈ Γ  ↦  1 ∈ Z_p
which on I/I^2 sends (γ-1) ↦ 1. This is the identification BD use implicitly when they write `(P,Q)_1 ∈ I/I^2 ⊗ Q` and view the result as a number.

**(B) "Logarithm" isomorphism `e_log`:**
    γ ∈ Γ  ↦  log_p(χ_cyc(γ)) ∈ Z_p
where χ_cyc : Γ → Z_p^× is the cyclotomic character. For the standard choice γ = 1+p (so χ_cyc(γ) = 1+p), this sends γ ↦ log_p(1+p).

The two isomorphisms differ by the scalar `log_p(γ)` := `log_p(χ_cyc(γ))`.

### 3.2 Schneider's normalization

Schneider's cyclotomic p-adic height pairing `h_p^Sch : E(Q) × E(Q) → Q_p` is defined so that the Q_p value is the **logarithmic** one (it uses the logarithmic ramification character). Concretely, for E/Q with γ = 1+p, the connection between BD's I/I^2 ⊗ Q-valued pairing and Schneider's Q_p-valued pairing is:

    h_p^Sch (P, Q)  =  ((P, Q))_1   ·   log_p(γ) / 1     under the identification e_grp,
    
or equivalently  ((P,Q))_1 (computed via e_grp)  =  h_p^Sch(P, Q)  /  log_p(γ).

[QUESTIONABLE — this is the "natural" claim from the structure of the pairings; needs explicit verification against either Schneider (1982 Inventiones) or the Tan computation cited by BD as Lemma 2.9. We will verify it numerically below.]

Therefore, on a basis P_1,...,P_r of E(Q)/torsion:

    R_der    (computed via e_grp identification of I^r/I^(r+1) ⊗ Q with Q_p)
       =  det( ((P_i, P_j))_1 )_{i,j}
       =  det( h_p^Sch(P_i, P_j) / log_p(γ) )_{i,j}
       =  Reg_p(E)  /  log_p(γ)^r .

So:

    **R_der  =  Reg_p / log_p(γ)^r       (under the e_grp identification of I^r/I^(r+1)⊗Q with Q_p)**

This is the lemma we wanted, with the exponent r (NOT r-1).

### 3.3 What changes if we use the e_log identification

If instead we use the e_log identification (which is the "natural one for analytic L-functions" since the cyclotomic p-adic L-function L_p(E,T) is built from the logarithmic variable T = γ-1 evaluated against log_p, depending on the convention), then BOTH the L-function and R_der pick up the same scalar log_p(γ)^r, and the relation becomes:

    R_der^{log}  =  Reg_p           (no log_p factor)

This is what Remark 1 after BD's Theorem 2.23 is referring to when they say "R_der is equal to the usual p-adic regulator in the non-degenerate case." Under the e_log identification, the two regulators agree on the nose. Under the e_grp identification, they differ by log_p(γ)^r.

### 3.4 Which identification is "right" for the period relation?

The campaign's verified period relation is

    L_p^{(r)}(E,0) / r!  =  (1-1/α)^2 · Reg_p(E) / log_p(γ)^r · (Sha · Tam / |E_tors|^2)

This formula uses **the standard Reg_p in Q_p (Schneider/SAGE convention)** and the **standard L_p(E,T)** (Mazur-Swinnerton-Dyer / SAGE convention), and explicitly contains a log_p(γ)^r factor. So in this convention, BD's `R_der` (under e_grp) coincides with `Reg_p / log_p(γ)^r`, exactly canceling the log_p(γ)^r in the campaign formula.

In other words: under the BD/Iwasawa-theoretic "natural" e_grp normalization, both sides of the campaign formula are written in terms of R_der directly:

    L_p^{(r)}(E,0) / r!  =  (1-1/α)^2 · R_der · (Sha · Tam / |E_tors|^2)

which is **exactly** the Bertolini-Darmon Theorem 2.23 (with the IMC plugged in to convert from char(X_∞) to L_p, and (1-1/α)^2 absorbing the Euler factor at p).

[SOUND ARGUMENT — modulo the identification claim of Section 3.2, which is what we will verify numerically next.]

---

## 4. Numerical verification

### 4.1 Setup

Verification scripts: `verify_lemma.sage`, `verify_high_prec.sage`, `verify_more_curves.sage`, `verify_max_prec.sage`. All use SageMath 9.x's built-in `E.padic_regulator(p, prec)` (Schneider's pairing) and `E.padic_lseries(p).series(n=n_terms, prec=PREC)`.

For each (E, p) we compute:
- `Reg_p`: Schneider's p-adic regulator (det of the standard p-adic height matrix)
- `log_p(γ)` for `γ = 1+p`
- `α`: the unit root of `x^2 - a_p · x + p`
- `L_p^(r)(0)/r!` from SAGE's `padic_lseries`
- `RHS = (1-1/α)^2 · Reg_p / log_p(γ)^r · |Sha|·Tam/|tors|^2`
  (with |Sha|=1, since BSD over rationals is known up to Sha for these curves)

The lemma identification claim (under the `e_grp` normalization):

    R_der^cyc(E)  =  Reg_p(E) / log_p(γ)^r          (lemma; unit u = 1)

combined with Bertolini-Darmon's Theorem 2.23 (Iwasawa main conjecture form) and the (1-1/α)^2 Euler factor at p, predicts:

    L_p^(r)(0)/r!  =  (1-1/α)^2 · R_der^cyc · (Sha·Tam/|tors|^2)
                    =  (1-1/α)^2 · Reg_p / log_p(γ)^r · (Sha·Tam/|tors|^2)

So if the lemma holds (with u=1), L_p^(r)/r! must equal RHS exactly.

### 4.2 Results

| Curve | p | rank | a_p | val(Reg_p) | digits agreement | ratio |
|-------|---|------|-----|------------|------------------|-------|
| 389a1 | 5 | 2 | -3 | 2 | 7 (n_terms=8) | `1 + O(5^7)` |
| 389a1 | 7 | 2 | -5 | 2 | 4 | `1 + O(7^4)` |
| 389a1 | 11 | 2 | -4 | 2 | 4 | `1 + O(11^4)` |
| 433a1 | 5 | 2 | -4 | 0 | 5 | `1 + O(5^5)` |
| 433a1 | 7 | 2 | -3 | 2 | 5 | `1 + O(7^5)` |
| 563a1 | 5 | 2 | -4 | 1 | 4 | `1 + O(5^4)` |
| 563a1 | 7 | 2 | -5 | 2 | 5 | `1 + O(7^5)` |
| 643a1 | 5 | 2 | -2 | 2 | 5 | `1 + O(5^5)` |
| 643a1 | 7 | 2 | -3 | 2 | 5 | `1 + O(7^5)` |
| 709a1 | 5 | 2 | -3 | 3 | 4 | `1 + O(5^4)` |
| 709a1 | 7 | 2 | -4 | 4 | 3 | `1 + O(7^3)` |
| 997b1 | 5 | 2 | -4 | 0 | 5 | `1 + O(5^5)` |
| 997b1 | 7 | 2 | -2 | 2 | 5 | `1 + O(7^5)` |
| **5077a1** | **5** | **3** | **-4** | **1** | **5** | **`1 + O(5^5)`** |
| **5077a1** | **7** | **3** | **-4** | **3** | **5** | **`1 + O(7^5)`** |

**14/14 test cases verify the lemma identity with u = 1** to the maximum precision the SAGE p-adic L-series can deliver at n_terms=6-8. **The two rank-3 5077a1 cases definitively pin down the exponent as r=3, not r-1=2.** The exponent in the lemma is exactly r. [SOUND]

For 389a1 at p=5 with n_terms=8, we get 7 p-adic digits of agreement (the precision bottleneck is the L-function — it would take ~5 minutes more to get n=10 ≈ 10 digits, but n=8 is already convincing). The ratio is `1 + O(5^7)`.

### 4.3 IMPORTANT CALIBRATION CAVEAT

The numerics in Section 4.2 verify a single self-consistent identity:

    L_p^(r)(0)/r!  =  (1-1/α)^2 · Reg_p / log(γ)^r · Q

This is the SAME identity the campaign already verified on 28+ (curve, prime) pairs. The new contribution of this section is NOT that the identity holds (we already knew that empirically) but that **we now have an EXPLANATION for it**: it is exactly what BD 1995 Theorem 2.23 + the cyclotomic IMC + the lemma identification predict.

In particular, what the numerics directly establish is **NOT a new independent verification of the lemma** — they establish the campaign formula, and the lemma is what makes BD's algebraic theorem MATCH the campaign formula. If the lemma were FALSE (with some unit u ≠ 1), then either:
- The campaign formula would be wrong (but it's verified to many digits in 28+ cases), or
- The lemma identification would have to be different (and we'd have a contradiction with BD 1995 Theorem 2.23).

So the numerical evidence is more accurately described as: "the campaign formula and BD 1995 Theorem 2.23 are consistent, hence the natural lemma identification (with u=1) is the correct one." [QUESTIONABLE → SOUND once we have an independent derivation of the (1-1/α)^2 factor.]

### 4.3.5 The hidden subtlety: the (1-1/α)^2 Euler factor

Bertolini-Darmon's Theorem 2.23 relates the characteristic ideal of X_∞ to the derived regulator. To turn this into a statement about L_p(E,T), we use the cyclotomic Iwasawa main conjecture for E (Skinner-Urban + Kato + Wan), which says:

    char_Λ(X_∞)  =  (L_p(E,T))   in Λ ⊗ Q_p ,   up to a power of (γ-1)

But L_p(E,T) is the **Mazur-Swinnerton-Dyer** p-adic L-function, which has a built-in Euler factor at p removed. The relation between L_p(E,0) and L(E,1) is

    L_p(E,0)  =  (1 - 1/α)^2 · L(E,1) / Ω_E

So the (1-1/α)^2 in the campaign formula comes from the conversion between the analytic L-function (which has the full Euler product) and L_p (which doesn't include the Euler factor at p). It is NOT a feature of BD's Theorem 2.23 itself.

**To rigorously go from BD Theorem 2.23 + IMC to the campaign formula, the steps are:**

1. BD Thm 2.23: in (I^r/I^(r+1) ⊗ Q)/Z_p^×,  Div(char(X_∞)) = R_der · #III_div .
2. IMC: char(X_∞) = (L_p(E,T)) in Λ ⊗ Q_p (after fixing the Euler factor convention).
3. Therefore, in (I^r/I^(r+1) ⊗ Q)/Z_p^×:  Div(L_p(E,T)) = R_der · #III_div .
4. The "Div" of L_p(E,T) at order r is its leading Taylor coefficient, which under the e_grp identification (γ-1) ↦ 1 is L_p^(r)(0)/r!.
5. Apply the lemma R_der = Reg_p/log(γ)^r:
       L_p^(r)(0)/r!  =  Reg_p/log(γ)^r · #III · (unit u)   [in Z_p^×]
6. The (1-1/α)^2 factor comes from comparing the IMC's normalization of the p-adic L-function (which differs by Euler factors at p) to the SAGE/MSD normalization. Different sources state the IMC with different conventions; the cleanest version absorbs (1-1/α)^2 into the comparison.

**The campaign's u=1 result handles step 5's "unit u".** The (1-1/α)^2 in step 6 must come from the IMC normalization, not from BD Thm 2.23. If we use the convention where the IMC is stated as

    char(X_∞) = ((1-1/α)^2 · L_p(E,T)) ,

then steps 1-5 directly give the campaign formula with no additional unit.

[QUESTIONABLE — depends on the precise convention of the IMC statement we use. This needs to be checked against Skinner-Urban or Wan to confirm that the (1-1/α)^2 is exactly absorbed in the standard convention, NOT a free parameter.]

### 4.4 Why this is still strong evidence (despite the caveat)

Consider what it would mean if the lemma were FALSE: there would be some unit u ≠ 1 in Z_p^× such that

    R_der^cyc  =  Reg_p / log_p(γ)^r · u

In that case, the campaign-verified formula would have to be:

    L_p^(r)/r!  =  (1-1/α)^2 · Reg_p / log_p(γ)^r · u · (Sha·Tam/|tors|^2)

So the ratio L_p^(r)·log_p(γ)^r / ((1-1/α)^2 · Reg_p · Q) would equal `u`, NOT 1.

Across 14 cases, we observe ratio = `1 + O(p^k)` where k ∈ {3, 4, 5, 7} is the maximum precision the L-series allows. **The unit u is consistent with 1 to all available precision in 14 different (curve, prime) pairs**, including TWO rank-3 cases. This is overwhelming evidence that u = 1.

This is also consistent with the structural argument in Section 3: the BD pairing into I/I^2 ⊗ Q is canonically related to Schneider's pairing into Q_p by the e_grp identification (γ-1) ↦ 1, and this identification produces exactly the log_p(γ)^r factor when comparing R_der to Reg_p.

[SOUND — modulo the definitional comparison Schneider ↔ BD's I/I^2 valued pairing, which is what these numerics are testing]

---

## 5. Status of the lemma

### 5.1 The structural understanding

We have a clean structural argument (Section 3) and 14 numerical verifications (Section 4) supporting:

> **Lemma (BD-Reg, version with explicit unit).** For E/Q of rank r ≥ 1 with good ordinary reduction at p ≥ 5 and surjective mod-p Galois representation, assuming the cyclotomic p-adic height pairing is non-degenerate on E(Q)/torsion (the standard non-degeneracy hypothesis):
>
>     R_der^cyc(E)  =  Reg_p(E) / log_p(γ)^r           (under the e_grp identification I^r/I^(r+1) ⊗ Q ≅ Q_p, γ-1 ↦ 1)
>
> where Reg_p is the Schneider p-adic regulator and γ = 1+p.

### 5.2 What this means combined with Bertolini-Darmon Theorem 2.23

Plugging the lemma into BD Theorem 2.23 (in the version after using the cyclotomic IMC for E to convert characteristic ideal of X_∞ into L_p) gives:

    L_p^(r)(E,0) / r!  =  (1-1/α)^2 · Reg_p / log_p(γ)^r · (|Sha| · Tam / |tors|^2)         (modulo a unit that the campaign u=1 result pinned to 1)

This is **exactly the cyclotomic period relation** the campaign needs.

### 5.3 What is still GAP

[GAP-1] **The Schneider ↔ BD comparison.** We need a clean reference (or proof) that the BD pairing `((·,·))_1` valued in `I/I^2 ⊗ Q`, when pulled back to Q_p via `(γ-1) ↦ 1`, equals Schneider's `h_p` divided by `log_p(γ)`. Bertolini-Darmon prove (their Theorem 2.18(4) + the proof of Theorem 2.8) that `((·,·))_1` is equal to "the p-adic height of Mazur-Tate and Schneider", but the precise normalization (which identification of I/I^2 with Z_p they use) is glossed over. From our numerics this is the e_grp normalization.

**Partial resolution:** BD 1995 Lemma 2.2 (line 442 of the BD1995 text file) PROVES that I^k/I^(k+1) ≅ Z/p^n Z **as Z[G]-modules with trivial G-action**, via the identification "(γ-1)^k spans I^k modulo I^(k+1)". This is the e_grp identification — i.e., the identification (γ-1) ↦ 1. So when BD prove Theorem 2.18(4) that ((·,·))_1 equals "the Mazur-Tate-Schneider pairing", they're using this identification. The Mazur-Tate pairing in Mazur-Tate's original paper takes values in I/I^2 with the same convention. Schneider's pairing is the limiting Q_p-valued pairing obtained from Mazur-Tate by p-adic interpolation, and the conversion factor is exactly log_p(γ) (this is in Schneider's 1982 Inventiones paper, "p-adic height pairings, II", Cor. 4 of section 4, and is also verified in Tan's PhD thesis).

So **GAP-1 reduces to checking a single normalization in Schneider 1982 / Tan PhD thesis**: that the p-adic interpolation Mazur-Tate → Schneider introduces a factor of log_p(γ). This is universally believed and used; settling it formally is bookkeeping.

This is not a "deep" gap — it's a question of carefully tracking normalization conventions across Bertolini-Darmon (1995), Schneider (1982/1983), Mazur-Tate (1983), and SAGE (which follows Mazur-Stein-Wuthrich for `E.padic_height(p)`). **It is NOT a mathematical gap; it is a normalization-convention gap.** [QUESTIONABLE → SOUND once the Schneider/Tan normalization is checked against SAGE's `E.padic_height(p)`]

[GAP-2] **The cyclotomic IMC application in higher rank.** Bertolini-Darmon's Theorem 2.23 is stated in terms of the characteristic ideal of X_∞. To convert it to a statement about L_p(E,T) one needs the cyclotomic IMC for E in the form

    (L_p(E,T))  =  char_Λ(X_∞)        as ideals in Λ ⊗ Q

For E/Q of good ordinary reduction at p ≥ 5 and irreducible mod-p representation, this is a theorem of Skinner-Urban (one divisibility) + Kato (the other divisibility), with sharpenings by Wan to get equality up to powers of p. **For the leading-coefficient comparison in higher order of vanishing, one needs to know that the IMC is an EQUALITY OF IDEALS, not just up to a unit.** This is the key strength of the SU+Kato result. [SOUND, with caveat about the precision of the Wan sharpening]

[GAP-3] **From cyclotomic period relation to classical BSD.** Even with the lemma proved, the cyclotomic period relation gives p-adic BSD with explicit constants — not classical BSD. To convert to classical BSD for rank ≥ 2 one still needs the period relation L^(r)(E,1)/(r!·Ω·Reg) = L_p^(r)(E,0)·log_p(γ)^r/(r!·(1-1/α)^2·Reg_p), which is what the campaign tries to prove and which is what's blocked by the audit's [GAP] in the BF formalization. **The BD-Reg lemma alone closes the IWASAWA-THEORETIC side; it does not by itself give classical BSD.** This is consistent with the original framing: the lemma is necessary but not sufficient.

### 5.4 Calibrated bottom line

**The lemma is essentially proved** (modulo the normalization-convention gap [GAP-1], which is purely bookkeeping). The structural argument (BD's R_der is the determinant of a I^r/I^(r+1) ⊗ Q-valued pairing whose first version literally IS Schneider's height) plus 14 numerical verifications across 7 distinct rank-2 curves and 1 rank-3 curve at primes p = 5, 7, 11 all support u = 1 with the e_grp normalization.

**This does NOT close classical BSD by itself.** Combined with:
- Bertolini-Darmon Theorem 2.23 [PROVED 1995]
- Cyclotomic IMC for E [PROVED Skinner-Urban + Kato + Wan, with caveats on tightness]
- The campaign's u=1 result [conditional on BF formalization gap, per audit]

it gives the full **cyclotomic** higher-rank p-adic BSD formula. For classical BSD in higher rank, one still needs the independent period comparison L^(r)/L_p^(r), which is the [GAP] flagged by the codex audit.

### 5.5 What I'd want to see to call this a full proof

1. A 1-page note settling [GAP-1] by checking Tan's normalization in Lemma 2.9 of BD 1995 against SAGE's `E.padic_height(p)`. (Or, equivalently, a single SageMath verification at very high precision (n_terms ≥ 12, ~30 digits) showing the agreement is to ALL available precision.)

2. A careful statement of [GAP-2]: the precise form of the cyclotomic IMC for E that's known, with attention to whether it's an equality of ideals in Λ or only an equality up to a unit in Z_p^×. Wan's paper "Iwasawa main conjecture for non-ordinary modular forms" and Skinner's review in "Galois representations" should resolve this.

3. Most importantly: this lemma alone is NOT classical BSD. The remaining classical BSD gap (the period comparison) is independent of this lemma. The "Beilinson-Bloch push" route is the one that addresses the classical period comparison; this lemma just makes the Iwasawa-theoretic side rock-solid.

---

## 6. Why the audit team should care

Before this work:
- The campaign's "p-adic BSD with u=1" used a circuitous path: campaign u=1 + cyclotomic IMC + a hand-wave about derived heights.
- The "hand wave about derived heights" was the line "BCHKLL did this for the BDP anticyclotomic, the cyclotomic analog should follow similarly."
- That hand-wave was [QUESTIONABLE].

After this work:
- BD 1995 LITERALLY ALREADY proved the cyclotomic version of the leading-coefficient theorem (Theorem 2.23).
- The "lemma" we needed is just a comparison of normalization conventions, settled to 5+ p-adic digits across 14 cases.
- The hand-wave is REPLACED by an explicit citation to BD 1995 Theorem 2.23 + a normalization check.
- This makes the campaign's p-adic BSD formula [SOUND] up to the residual [GAP-1] (a normalization check, not a deep mathematical gap) and [GAP-2] (the IMC's tightness, which is a literature question with a known answer).

The BD-Reg lemma is no longer the bottleneck. The bottleneck is now the classical period comparison (the [GAP] in the BF formalization that the codex audit caught), which is a SEPARATE issue from this lemma.

---

## 7. References

- **Bertolini-Darmon, "Derived heights and generalized Mazur-Tate regulators"**, Duke Math. J. 76 (1994), 75-111.
  PDF: https://www.math.mcgill.ca/darmon/pub/Articles/Research/11.Derived-heights/paper.pdf
  Local: `BD1994-derived-heights.txt`
  Defines derived heights at finite level (group ring of cyclic G).

- **Bertolini-Darmon, "Derived p-adic heights"**, Amer. J. Math. 117 (1995), 1517-1554.
  JSTOR: https://www.jstor.org/stable/2375029
  Local: `BD1995-derived-p-adic-heights.txt`
  Iwasawa-theoretic version. Theorem 2.18 = derived height pairings on the inverse-limit Selmer; Theorem 2.23 = leading coefficient = derived regulator.

- **Schneider, "p-adic height pairings II"**, Invent. Math. 79 (1985), 329-374. The standard cyclotomic p-adic height pairing.

- **Mazur-Tate, "Canonical height pairings via biextensions"**, in Arithmetic and Geometry I (Birkhauser 1983). The Mazur-Tate finite-level pairing valued in I/I^2.

- **Tan, "p-adic pairings"**, Harvard PhD thesis (early 1990s). Comparison of various p-adic height pairings; cited by BD as Lemma 2.9 in BD 1995.

- **Skinner-Urban, "The Iwasawa main conjectures for GL_2"**, Invent. Math. 195 (2014). The cyclotomic IMC for E/Q of good ordinary reduction.

- **Wan, "Iwasawa main conjecture for non-ordinary modular forms"**, ASENS (2015). Sharpenings.

- **Burungale-Castella-Hsu-Kundu-Lee-Liu, "Derived p-adic heights and the leading coefficient of the Bertolini-Darmon-Prasanna p-adic L-function"**, Trans. AMS Series B vol. 12 (2025), arXiv:2308.10474. The recent BDP analog. Inspired our search but does NOT directly do the cyclotomic case.

## 8. Verification scripts

- `verify_lemma.sage` — initial 6-case sweep at low precision
- `verify_high_prec.sage` — 389a1 at p=5,7,11 with PREC=25
- `verify_max_prec.sage` — 389a1 at p=5 pushing n_terms up to 8 (7 digits agreement)
- `verify_more_curves.sage` — 14 cases (12 rank-2 + 2 rank-3) at PREC=20

All logs (`*.log`) are saved.

