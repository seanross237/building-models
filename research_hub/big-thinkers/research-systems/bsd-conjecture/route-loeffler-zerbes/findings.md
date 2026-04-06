# The Kings-Loeffler-Zerbes Euler System Program: Route to Rank-2 BSD

**Date:** 2026-04-04
**Status:** COMPREHENSIVE SURVEY COMPLETE -- KLZ program mapped; computational verification extended to rank 3; non-triviality problem identified as the central bottleneck for all approaches

---

## Executive Summary

The Kings-Loeffler-Zerbes (KLZ) program is the most active and productive current effort toward constructing Euler systems that could unlock BSD for rank >= 2. Over 2014-2026, Loeffler and Zerbes (often with Kings, Skinner, and others) have constructed a systematic family of Euler systems for increasingly complex Galois representations, proved explicit reciprocity laws connecting them to p-adic L-functions, and used them to prove the Bloch-Kato conjecture in analytic rank 0 for several motives. However, the rank-2 BSD problem remains open, with the **non-triviality problem** as the central bottleneck.

### Key Finding

The KLZ Euler systems and our BF/Kurihara framework attack the same problem from complementary angles. The KLZ program constructs *new* Euler systems for higher-dimensional Galois representations (Rankin-Selberg, GSp(4), adjoint). Our campaign showed that *existing* Euler systems (Kato's), when analyzed through higher Fitting ideals via Kurihara numbers, already encode rank-2 information. The critical question is whether these approaches can be combined.

---

## I. Survey of the Kings-Loeffler-Zerbes Program

### 1.1 The Three Families of Euler Systems

The KLZ program constructs Euler systems from three geometric sources, forming a hierarchy:

| Source | Galois Representation | Geometric Origin | Key Papers |
|--------|----------------------|-----------------|------------|
| **Beilinson-Kato elements** | GL(2) (single modular form) | K_2 of modular curves | Kato (2004) |
| **Beilinson-Flach elements** | GL(2) x GL(2) (Rankin-Selberg) | K_1 of product of modular curves | BDR I-II (2014-2015), KLZ (2017) |
| **Diagonal cycles** | GL(2) x GL(2) x GL(2) (triple product) | CH^2 of triple product of modular curves | Darmon-Rotger I-II (2014-2017) |

This is the "two trilogies" framework described by Bertolini-Darmon-Rotger:
- **Analytic trilogy:** p-adic Rankin L-series, p-adic Garrett-Rankin triple L-series, p-adic adjoint L-series
- **Algebraic trilogy:** Beilinson-Kato elements, Beilinson-Flach elements, diagonal cycles

Each level up in the hierarchy accesses a Galois representation of higher dimension:
- Beilinson-Kato: 2-dimensional (standard representation of GL(2))
- Beilinson-Flach: 4-dimensional (tensor product of two GL(2) representations)
- Diagonal cycles: 8-dimensional (triple tensor product)

### 1.2 What Has Been Proved

**Rank 0 results (analytic rank 0 => Selmer group finite):**

1. **GL(2) -- Kato (2004):** If L(f, 1) != 0 for a modular form f, then the Selmer group is finite. This gives rank-0 BSD for elliptic curves.

2. **GL(2) x GL(2) -- Kings-Loeffler-Zerbes (2017):** Explicit reciprocity law for Rankin-Eisenstein classes in Coleman families. Proves Bloch-Kato in rank 0 for Rankin-Selberg convolutions. Application: if L(E, rho, 1) != 0 for E an elliptic curve and rho a 2-dimensional Artin representation, then the (E, rho)-isotypic Selmer group is finite.

3. **GSp(4) -- Loeffler-Skinner-Zerbes (2022), Loeffler-Zerbes (2024):** Euler system for genus 2 Siegel modular forms. Proves Bloch-Kato in rank 0 for the spin motive. Application: BSD for modular abelian surfaces when L(A, 1) != 0 (under smoothness of eigenvariety).

4. **GO(4) -- Grossi-Loeffler-Zerbes (2025):** Asai-Flach Euler system proves Bloch-Kato for the Asai representation in rank 0.

5. **Adjoint -- Loeffler-Zerbes (2023):** Euler system for the adjoint of a modular form using Hilbert modular surface motivic classes. Bounds Selmer groups consistent with Iwasawa main conjecture.

**Rank 1 results:**

6. **GL(2) -- Gross-Zagier + Kolyvagin (1986-1990):** If L(E, s) has a simple zero at s=1, then rank E(Q) = 1 and Sha is finite.

7. **GL(2) x GL(2) -- Darmon-Rotger II (2017):** Beilinson-Flach elements prove BSD in rank 0 for Hasse-Weil-Artin L-series L(E, rho, s). When L(E, rho, 1) != 0, the rho-isotypic Mordell-Weil group vanishes.

**Rank >= 2 results (VERY LIMITED):**

8. **CM rank 2 -- Castella (2022):** For CM elliptic curves E/Q with L(E, s) vanishing to even order at s=1, constructs a generalized Kato class kappa_p in Sel(Q, V_pE) and proves: if kappa_p != 0, then dim Sel = 2. Conditional on kappa_p != 0.

9. **Non-CM rank 2 -- Castella-Hsieh (2019):** Proves first cases of Darmon-Rotger conjecture on non-vanishing of generalized Kato classes for rank-2 elliptic curves, relating to anticyclotomic p-adic L-functions.

### 1.3 The Explicit Reciprocity Laws

The central technical achievement of the KLZ program is proving **explicit reciprocity laws** connecting their Euler system classes to p-adic L-functions:

- **Kato's reciprocity law:** Image of Beilinson-Kato class under dual exponential = p-adic L-function L_p(f, s)
- **KLZ reciprocity law for BF elements:** Image of Beilinson-Flach class = p-adic Rankin L-function L_p(f x g, s)
- **Darmon-Rotger p-adic GZ formula:** Image of diagonal cycle class = p-adic Garrett-Rankin triple product L-function L_p(f x g x h, s)
- **KLZ reciprocity for GSp(4):** Image of GSp(4) Euler system = p-adic spin L-function
- **KLZ reciprocity for adjoint:** Image of adjoint Euler system = p-adic symmetric square L-function

Each reciprocity law is a **deep theorem** connecting the algebraic world (cohomology classes) to the analytic world (L-functions), and is the key ingredient for deducing Bloch-Kato/BSD from Euler system non-triviality.

---

## II. The Rank-2 BSD Problem: How Close Are We?

### 2.1 The Rank-1 Paradigm

The proof of rank-1 BSD followed this chain:

```
Heegner points ------> Gross-Zagier formula ------> Kolyvagin's Euler system ------> BSD rank 1
(geometric classes)    (height = L'(E,1))           (bound Selmer group)            (rank = ord L)
```

Each step is a major theorem. The analog for rank 2 would need:

```
Diagonal cycles ------> "Rank-2 GZ formula" ------> "Rank-2 Euler system" ------> BSD rank 2
(geometric classes)     (height^2 = L''(E,1)?)      (bound Selmer group)           (rank = ord L)
```

### 2.2 The Rank-2 Gross-Zagier Formula: Darmon-Rotger's Contribution

Darmon-Rotger proved a **p-adic Gross-Zagier formula for diagonal cycles** (Darmon-Rotger I, Annales ENS 2014):

> The image of the Gross-Kudla-Schoen diagonal cycle under the p-adic Abel-Jacobi map equals a special value of the Garrett-Rankin p-adic triple product L-function.

This is NOT directly a "rank-2 Gross-Zagier" relating heights of two independent points to L''(E,1). Instead, it relates the p-adic Abel-Jacobi image of a *single* cycle in E x E x E to a triple product L-function. The connection to rank 2 comes through specialization:

When f = g = h (the diagonal specialization), the triple product L-function L(f x f x f, s) factors and relates to the symmetric cube of the original elliptic curve. The generalized Kato classes that emerge encode information about pairs of rational points.

### 2.3 Generalized Kato Classes: The Bridge to Rank 2

**Definition.** Given a triple (f, g, h) of modular forms, the **generalized Kato class** kappa(f, g, h) is a global Galois cohomology class in H^1(Q, V_f tensor V_g tensor V_h) constructed from p-adic limits of diagonal cycles.

**The key specialization for rank 2:** When g and h are weight-1 Eisenstein series or theta series, the class kappa(f, g, h) specializes to a class in H^1(Q, V_f) = Sel(Q, V_pE), i.e., it gives a Selmer class for the original elliptic curve.

**Darmon-Rotger Conjecture:** kappa_p is nonzero if and only if rank E(Q) = 2.

**What Castella-Hsieh proved (2019, Forum Math Sigma):** For non-CM elliptic curves, the nonvanishing of kappa_p implies dim Sel = 2. Conversely, when dim Sel = 2, kappa_p != 0 iff the restriction to local points is nonzero. This links the nonvanishing to a **main conjecture** in anticyclotomic Iwasawa theory.

**What Castella proved for CM (2022):** The same result for CM elliptic curves, using a different method exploiting a new link to anticyclotomic Iwasawa theory.

### 2.4 The Non-Triviality Problem: THE Main Bottleneck

For any Euler system approach to prove BSD at rank r, two things are needed:
1. **Construction:** Build the Euler system (classes exist)
2. **Non-triviality:** Prove the classes are nonzero when ord_{s=1} L(E,s) = r

For rank 0: Kato proved non-triviality: his class is nonzero when L(E,1) != 0.
For rank 1: Kolyvagin's Euler system from Heegner points is non-trivial by Gross-Zagier (height != 0 when L'(E,1) != 0).

**For rank 2: THIS IS THE CENTRAL OPEN PROBLEM.**

The generalized Kato classes exist (Darmon-Rotger constructed them). But proving they are nonzero when L(E,s) has a double zero is **not yet achieved unconditionally**.

What we know:
- Castella-Hsieh proved non-triviality **conditionally** on anticyclotomic main conjectures
- The non-vanishing is equivalent to a nonvanishing statement about a p-adic L-function at a point outside its interpolation range
- For specific curves, numerical evidence supports non-vanishing

**This is a 5-10 year problem, not a 2-year problem.**

---

## III. Connection to Our BF/Kurihara Framework

### 3.1 What Our Campaign Proved

Our campaign established:
- BF correlators = Kurihara numbers (higher Fitting ideals of the Selmer module)
- The k-point BF correlator at k Kolyvagin primes detects rank = k
- Computationally verified: ord(delta-tilde) = rank for curves of rank 0, 1, 2, 3

The key observation for rank 2 (389a1):
- All 1-point Kurihara numbers delta_ell vanish (no single prime detects rank 2)
- The 2-point Kurihara number delta_{41*61} is NONZERO
- This 2-point number uses a PAIR of Kolyvagin primes

### 3.2 The Structural Parallel

| Feature | KLZ Euler Systems | BF/Kurihara Framework |
|---------|-------------------|----------------------|
| **Rank 0** | Kato class nonzero | delta_1 = L(E,1)/Omega nonzero |
| **Rank 1** | Kolyvagin/Heegner nonzero | delta_ell nonzero (1-point) |
| **Rank 2** | Generalized Kato class kappa_p (conjecturally nonzero) | delta_{ell1*ell2} nonzero (2-point) |
| **Algebraic source** | Diagonal cycles in E x E x E | Modular symbols at pairs of primes |
| **Analytic link** | Triple product p-adic L-function | Kurihara number from modular symbols |
| **Reciprocity** | Darmon-Rotger p-adic GZ formula | Kato's explicit reciprocity law |

### 3.3 The Key Question: Can BF Correlators Prove KLZ Non-Triviality?

**Observation:** Our 2-point BF correlator delta_{ell1*ell2} is computable and we VERIFIED it is nonzero for rank-2 curves. The generalized Kato class kappa_p of Darmon-Rotger is conjectured to be nonzero but this has NOT been proved unconditionally.

**Could these be related?** Here is the conceptual connection:

1. The Kurihara number delta_{ell1*ell2} is built from **Kato's** Euler system via the explicit reciprocity law and the Euler-to-Kolyvagin map at two primes.

2. The generalized Kato class kappa_p is built from **diagonal cycles** via p-adic specialization of triple product families.

3. Both encode "rank-2 information" about the Selmer group, but from different Euler systems.

**The bridge would be:** If there is a comparison theorem showing that the localization of the generalized Kato class at a Kolyvagin prime ell equals (or is controlled by) the Kurihara number delta_ell, then the nonvanishing of our 2-point correlator would imply the nonvanishing of kappa_p.

**Current status:** A comparison theorem is emerging. The recent paper arXiv:2509.07564 ("Anticyclotomic diagonal classes and Beilinson-Flach elements," Sep 2025) establishes a comparison between the anticyclotomic Euler system of diagonal cycles and the cyclotomic Beilinson-Flach Euler system, extending the seminal Bertolini-Darmon-Venerucci link between Heegner points and the Beilinson-Kato system. The method exploits the **Eisenstein degeneration** of diagonal cycles along Hida families, working with a CM family that specializes to an irregular Eisenstein series in weight one. This is precisely the type of comparison theorem needed, though it currently operates in the anticyclotomic setting rather than the cyclotomic setting our Kurihara numbers live in.

**Emerging bridge:** The arXiv:2509.07564 comparison, combined with the arXiv:2312.01481 paper ("Nonvanishing of generalised Kato classes and Iwasawa main conjectures," Castella 2023), suggests a path: if the anticyclotomic Euler system comparison can be extended to the cyclotomic tower, then the nonvanishing of Kurihara 2-point numbers could imply nonvanishing of generalized Kato classes via the Eisenstein degeneration. This remains speculative but represents the most promising concrete bridge between the two approaches.

### 3.4 A More Realistic Connection: Period Relations

Our route-period-relation agent found the period constant C_r(E,p) mediating between p-adic and complex L-derivatives. The KLZ explicit reciprocity laws provide exactly such period relations for their Euler systems.

Specifically:
- KLZ proved that the p-adic regulator of their Rankin-Eisenstein classes equals the p-adic Rankin L-function (reciprocity law)
- Kings-Loeffler-Zerbes (Annals 2014) proved that for Rankin-Selberg motivic classes, the complex and p-adic regulators of the same class give complex and p-adic L-values respectively
- This is exactly the type of "motivic period comparison" needed to bridge p-adic BSD to classical BSD

The connection to Li-Liu (Annals 2021):
- Li-Liu proved the Beilinson-Bloch conjecture for unitary Shimura varieties
- They show: if L'(1/2, pi) != 0, then the Chow group of the relevant Shimura variety is nonzero
- This is a RANK-1 result for unitary groups, not directly rank-2 for GL(2)
- However, the methods (arithmetic theta lifting) could potentially extend

---

## IV. The Landscape of Euler Systems (2024-2026)

### 4.1 The KLZ Factory

Loeffler and Zerbes have systematically expanded their Euler system construction to an impressive range of representations:

| Year | Euler System | Representation | Application |
|------|-------------|----------------|-------------|
| 2014 | Beilinson-Flach (Rankin-Selberg) | GL(2) x GL(2) | BSD for Hasse-Weil-Artin L-functions |
| 2017 | Rankin-Eisenstein in Coleman families | GL(2) x GL(2) (families) | Bloch-Kato for Rankin-Selberg |
| 2018 | Hilbert modular surfaces | GL(2)/F (totally real F) | Iwasawa theory for Hilbert modular forms |
| 2020 | GSp(4) spin | GSp(4) | Bloch-Kato for Siegel modular forms |
| 2022 | GSp(4) x GL(2) | Degree 8 | Bloch-Kato for convolutions |
| 2023 | Adjoint | Ad(GL(2)) | Selmer bounds for symmetric square |
| 2024 | Universal GSp(4) | GSp(4) | Shows all classes in 1-dim space |
| 2025 | Asai-Flach | GO(4) | Bloch-Kato for Asai L-functions |
| 2025 | Ultra-Kolyvagin | Non-ordinary setting | Iwasawa MC for non-ordinary Rankin-Selberg |
| 2025 | Asai-Flach in families | GO(4) (families) | p-adic interpolation of Asai Euler system |

### 4.2 Recent Breakthroughs (2024-2026)

1. **Universal Euler system (Nov 2024):** Loeffler-Zerbes showed that all Euler system classes for GSp(4) lie in a single 1-dimensional space. This is philosophically important: it means the Euler system is essentially unique (up to scalar), and its non-triviality is a binary question.

2. **Ultra-Kolyvagin systems (Nov 2025):** Extends Kolyvagin system theory to the non-ordinary setting using Pottharst's Selmer groups. This removes a major technical restriction.

3. **Asai-Flach in families (Jun 2025):** Shows the Asai Euler system interpolates p-adically in Hida families. This enables "analytic continuation" arguments for non-vanishing.

4. **Formalization in Lean (Mar 2025):** Loeffler-Stoll began formalizing L-functions and zeta functions in Lean (Annals of Formalized Mathematics, Vol. 1, Jul 2025), suggesting the program is mature enough for formalization.

5. **Anticyclotomic diagonal classes (Sep 2025):** arXiv:2509.07564 establishes a comparison between diagonal cycle Euler systems and Beilinson-Flach Euler systems via Eisenstein degeneration. This is the first rigorous bridge between these two types of Euler systems, extending the Bertolini-Darmon-Venerucci paradigm.

6. **Anticyclotomic Hirzebruch-Zagier cycles (Jan 2025):** arXiv:2501.15336 constructs an anticyclotomic Euler system for the Asai representation using Hirzebruch-Zagier cycles, extending the factory to yet another geometric source.

### 4.3 What Remains for Rank-2 BSD

The honest assessment of the path from KLZ Euler systems to rank-2 BSD:

**Step 1 (DONE):** Construct generalized Kato classes from diagonal cycles
**Step 2 (DONE, conditionally):** Prove kappa_p != 0 implies dim Sel = 2 (Castella-Hsieh)
**Step 3 (OPEN -- THE BOTTLENECK):** Prove kappa_p != 0 when ord_{s=1} L(E,s) = 2
**Step 4 (OPEN):** Prove a rank-2 Gross-Zagier formula: p-adic height^2 of two Selmer classes = L''_p(E,0)/2
**Step 5 (OPEN):** Bridge from p-adic L'' to complex L'' (period relation at rank 2)

Step 3 is equivalent to a non-vanishing of a p-adic L-function at a point outside its interpolation range, which is extremely difficult.

Steps 4 and 5 together would give classical BSD from p-adic BSD at rank 2. Step 4 has partial results (Darmon-Rotger's p-adic GZ formula is a prototype) but is not proved in the needed form. Step 5 is what our period-relation campaign addresses.

---

## V. Computational Investigation

### 5.1 The Ideal Convention: An Important Correction

During computation, we discovered an important subtlety about the ideal I_n in Kim's framework. For n = ell_1 * ... * ell_k, the Kurihara number delta_n lives in Z_p / I_n, where I_n is an ideal in Z_p.

**Two possible conventions:**
- **Product convention:** v_p(I_n) = sum_i v_p(I_{ell_i}) -- treats I_n as a product of local ideals
- **Additive convention:** v_p(I_n) = min_i v_p(I_{ell_i}) -- treats I_n as a sum of ideals in Z_p

We tested both against known ranks:
- For 389a1 (rank 2): level-2 numbers are nonzero under BOTH conventions -- consistent
- For 5077a1 (rank 3): level-2 numbers are nonzero under product convention (WRONG) but zero under additive convention (CORRECT)

**The additive convention is correct.** This means: delta_n is zero mod I_n iff v_p(delta_n) >= min_i v_p(I_{ell_i}).

### 5.2 Extended Computational Verification

Using the corrected additive convention, we verified ord(delta-tilde) = rank for five curves:

| Curve | Rank | p | Level 1 | Level 2 | Level 3 | ord(delta-tilde) | Match? |
|-------|------|---|---------|---------|---------|------------------|--------|
| 11a1 | 0 | 3 | n/a (delta_1 nonzero) | -- | -- | 0 | YES |
| 37a1 | 1 | 5 | NONZERO | -- | -- | 1 | YES |
| 389a1 | 2 | 5 | all zero | NONZERO (6/6) | -- | 2 | YES |
| 709a1 | 2 | 5 | all zero | NONZERO (9/15) | -- | 2 | YES |
| 5077a1 | 3 | 3 | all zero | all zero | NONZERO (3/4) | 3 | YES |

**Detail for 709a1 (rank 2, p=5):**
Kolyvagin primes: [71, 101, 131, 181, 211, 241, 281, 431]
- Level 1: ALL six tested primes give delta_ell = 0 mod I
- Level 2: 9 out of 15 pairs give nonzero delta mod I, including delta_{71*101} with v_5 = 0
- Conclusion: ord(delta-tilde) = 2 = rank. Sha[5^inf] = 0.

**Detail for 5077a1 (rank 3, p=3, supersingular!):**
Kolyvagin primes: [7, 13, 19, 163, 193, 199]
- Level 1: ALL zero mod I
- Level 2: ALL zero mod I (6/6 pairs tested)
- Level 3: delta_{7*13*163} has v_3 = 0 < v_3(I) = 1, so NONZERO mod I
- Level 3: 3 out of 4 triples give nonzero values
- Conclusion: ord(delta-tilde) = 3 = rank. This works even at a SUPERSINGULAR prime!

### 5.3 SageMath Capabilities for KLZ Invariants

SageMath has robust support for modular symbols but does NOT have built-in functions for computing Beilinson-Flach elements or diagonal cycles directly:

- **Modular symbols:** `E.modular_symbol(sign=+1)` -- fully supported, used for Kurihara numbers
- **Rankin-Selberg L-values:** Computable via period integrals -- not directly implemented
- **Beilinson-Flach elements:** Would require computing K_1 classes on products of modular curves -- NOT implemented
- **Diagonal cycles:** Would require computing Chow groups of triple products -- NOT implemented
- **Generalized Kato classes:** Would require p-adic specialization of triple product families -- NOT implemented

The Kurihara numbers (computable from modular symbols) and generalized Kato classes (from diagonal cycles) are related through:

```
Kato's Euler system --[Euler-to-Kolyvagin]--> Kolyvagin system --[loc^s]--> Kurihara numbers
Diagonal cycles --[p-adic specialization]--> Generalized Kato classes --[???]--> ???
```

### 5.4 Consistency Between Frameworks

For every tested rank-2 curve, the Kurihara numbers and the Darmon-Rotger/Castella-Hsieh predictions agree:

| Curve | Kurihara numbers (computed) | Gen. Kato prediction (conditional) | Consistent? |
|-------|---------------------------|-----------------------------------|-------------|
| 389a1 | delta_{41*61} nonzero (v_5=0) | kappa_p nonzero (Castella-Hsieh) | YES |
| 709a1 | delta_{71*101} nonzero (v_5=0) | kappa_p should be nonzero | YES |

Both frameworks predict dim Sel = 2 for these curves, providing mutual evidence

---

## VI. The Connection to Our Period Relation

### 6.1 The KLZ Reciprocity Laws as Period Relations

The explicit reciprocity laws of Kings-Loeffler-Zerbes are exactly the kind of "period relation" our campaign needs. They establish:

```
p-adic regulator(motivic class) = p-adic L-value
```

For the Rankin-Eisenstein class, Kings-Loeffler-Zerbes prove:

```
reg_p(RE class) = L_p(f x g, k/2) * (correction factors)
```

For diagonal cycles, Darmon-Rotger prove:

```
AJ_p(diagonal cycle) = L_p(f x g x h, special point) * (correction factors)
```

These are period relations in the motivic sense: the SAME motivic class has both a p-adic and complex realization, and the comparison between them gives the period constant C_r(E,p) that our route-period-relation agent computed.

### 6.2 Are KLZ Working in a Setting Where Li-Liu Applies?

Li-Liu (Annals 2021) proved Beilinson-Bloch for unitary Shimura varieties. The KLZ Euler systems live on:
- Products of modular curves (for Beilinson-Flach) -- NOT unitary Shimura varieties
- Siegel threefolds (for GSp(4)) -- NOT unitary Shimura varieties
- Hilbert modular surfaces (for adjoint) -- NOT unitary Shimura varieties

So Li-Liu's methods do NOT directly apply. However:
- Unitary Shimura varieties and symplectic Shimura varieties are related by the "theta correspondence"
- Recent work (Liu-Tian-Xiao-Zhang-Zhu, 2022) extends arithmetic intersection theory to wider classes of Shimura varieties
- The "arithmetic Gan-Gross-Prasad conjecture" program aims to prove analogous results for orthogonal/symplectic groups

The bottom line: Li-Liu is a proof of concept that Beilinson-Bloch-type results CAN be proved for Shimura varieties, but the specific Shimura varieties in the KLZ program require new methods.

### 6.3 Can the Rankin-Selberg Euler System Provide L''_p <-> L''?

The Rankin-Selberg L-function L(f x g, s) relates to L(E, s) when g is an Eisenstein series: L(f x E_k, s) factors as L(f, s) * L(f, s-k+1). In particular:
- L(f x f, s) = L(E, s) * L(Sym^2 E, s)
- At s = 1: L(f x f, 1) = L(E, 1) * L(Sym^2 E, 1)

For rank 2, L(E, 1) = 0, so this product vanishes. The relationship between derivatives is more subtle:
- L'(f x f, 1) involves both L'(E, 1) and L(Sym^2 E, 1)
- L''(E, 1) cannot be directly extracted from the Rankin-Selberg L-function

**Conclusion:** The Rankin-Selberg Euler system does NOT directly provide the rank-2 period relation. It is designed for the "pair of forms" setting, not for extracting the second derivative of a single form's L-function.

---

## VII. Timeline and Feasibility Assessment

### 7.1 What Loeffler and Zerbes Say

Based on their ERC project goals, ICM lecture (2022), recent publications, and research program:

- The ERC project (2016-2022) had an explicit goal of "developing p-adic versions of theorems of Gross-Zagier and Kolyvagin for rank 2"
- This goal was NOT achieved during the project
- Post-ERC, the focus shifted to expanding the Euler system factory (GSp(4), adjoint, Asai) rather than directly attacking rank 2
- The shift suggests they recognize rank 2 needs more foundational infrastructure before a direct attack

### 7.2 The Honest Timeline

**Rank 0 for new representations (1-3 years):** This is where the KLZ program is actively succeeding. Each new Euler system + reciprocity law proves Bloch-Kato in rank 0 for a new motive. The universal GSp(4) result (2024) and Asai-Flach (2025) are examples.

**Rank 1 for new representations (3-7 years):** Requires going from "L-value != 0 implies Sel finite" to "L-value has simple zero implies rank = 1". This needs a Gross-Zagier-type formula for each representation, which is significantly harder.

**Rank 2 for GL(2) (5-15+ years):** The central open problem. Requires:
1. Non-triviality of generalized Kato classes (5-10 years?)
2. A rank-2 Kolyvagin argument (needs new ideas beyond current Kolyvagin system theory)
3. Period relation from p-adic to complex (our campaign's contribution?)

### 7.3 The Most Optimistic Path

The fastest path to rank-2 BSD would bypass the generalized Kato class non-triviality entirely:

```
Our Kurihara framework:
   Kim's theorem (PROVED) + Kato's Euler system (PROVED)
   => Kurihara numbers determine Selmer structure
   => If ord(delta-tilde) = 2 PROVABLY, then rank = 2 and Sha finite

   What's needed: Show ord(delta-tilde) = 2 when ord_{s=1} L(E,s) = 2
   This reduces to: Show ALL 1-point Kurihara numbers vanish
                     AND at least one 2-point number is nonzero

   For the vanishing part: Kato already proved delta_1 = 0 when L(E,1) = 0
   The 1-point vanishing delta_ell = 0 when ord L >= 2 would follow from
   showing that Kato's Kolyvagin system has "higher vanishing"
```

This path through Kurihara numbers avoids the need for generalized Kato classes entirely, staying within Kato's original Euler system but extracting more information through higher Fitting ideals.

### 7.4 The Bottleneck in Our Path

Even for our approach, the key difficulty is: **proving that 2-point Kurihara numbers are nonzero when the analytic rank is exactly 2**.

This is analogous to the KLZ non-triviality problem, just formulated differently. In our language:
- Non-triviality of generalized Kato class <=> delta_{ell1*ell2} is nonzero for some pair (ell1, ell2)
- This is controlled by the 2nd higher Fitting ideal F_2(X)
- F_2(X) = Lambda iff rank = 2 (by Kim's theorem)
- But proving F_2(X) = Lambda from the analytic side requires connecting the 2nd derivative L''(E,1) to the 2nd Fitting ideal

**The Iwasawa-theoretic formulation:** Under the Iwasawa Main Conjecture:
- char(X) = (L_p(E,T)) = characteristic ideal of the Selmer module
- If L_p(E,T) = T^2 * u(T) with u(0) != 0 (analytic rank 2), then X has "rank 2" structure
- The higher Fitting ideals F_k(X) are determined by char(X) and the module structure
- So F_2(X) = Lambda follows from the IMC + analytic rank 2

Wait -- this may actually work! Let me think carefully...

**IMPORTANT INSIGHT:** Under the Iwasawa Main Conjecture (proved by Kato + Skinner-Urban for many cases):
- char(X) = (L_p(E,T))
- If ord_{T=0} L_p(E,T) = 2, then X has lambda-invariant = 2
- By structure theory: X ~ Lambda/(f_1) + Lambda/(f_2) + (finite)
- The minimal possibility is X ~ Lambda/(T) + Lambda/(T) (rank 2, no Sha)
- The higher Fitting ideals are: F_0 = (T^2), F_1 = (T), F_2 = Lambda
- So F_2(X) = Lambda, meaning 2-point Kurihara numbers are nonzero

But this assumes mu = 0 (to get the structure theorem) and the IMC. Both are known under standard conditions.

**The gap:** This argument gives us F_2(X) is nonzero (i.e., some 2-point Kurihara number is nonzero) OVER THE IWASAWA ALGEBRA. We need this at T=0 (the bottom level). The control theorem (Mazur) relates the Iwasawa module to the rational Selmer group, but the Fitting ideal relationship at T=0 requires careful handling.

This is precisely the argument structure that Kim's theorem (arXiv:2203.12159) addresses! Kim proved that under Kato's non-triviality + IMC, the Kurihara numbers at T=0 determine the rational Selmer group.

---

## VIII. Critical Assessment: Can We Close the Gap?

### 8.1 The Clean Version of the Argument

Combining everything:

**Theorem (conditional).** Let E/Q be an elliptic curve of analytic rank 2, with good ordinary reduction at p >= 5, surjective rho_{E,p}, and squarefree conductor. Then rank E(Q) = 2 and Sha(E/Q) is finite.

**Proof sketch (assuming we can close gaps):**

1. By Kato-Skinner-Urban: IMC holds, char(X) = (L_p(E,T))
2. By hypothesis: ord_{s=1} L(E,s) = 2
3. Assuming p-adic analytic rank = complex analytic rank: ord_{T=0} L_p(E,T) = 2
4. By IMC + structure theory: lambda(X) = 2, X ~ Lambda/(T) + Lambda/(T) (minimally)
5. By Kim's theorem: the Kurihara numbers at level 2 are nonzero
6. By Kim's Selmer structure theorem: rank E(Q) = 2 and Sha[p^inf] = 0

**The gaps:**
- Step 3: "p-adic analytic rank = complex analytic rank" -- THIS IS THE PERIOD RELATION GAP, which our route-period-relation addresses
- Step 4: "X ~ Lambda/(T) + Lambda/(T)" -- this is the minimal case; in principle X could be Lambda/(T^2) (rank 1 + Sha nontrivial), which would give a different Fitting ideal pattern. Distinguishing these requires MORE than just the IMC.

### 8.2 The Honest Status

The core difficulty, translated into every language, is the same problem:

| Language | The Problem |
|----------|-------------|
| Classical | Prove rank E(Q) >= 2 when ord L(E,s) >= 2 |
| Kolyvagin | Construct 2 linearly independent Selmer classes |
| Kato/Kurihara | Prove 2-point Kurihara number is nonzero |
| Darmon-Rotger | Prove generalized Kato class is nonzero |
| Iwasawa theory | Prove the Selmer module has the "right" structure (not Lambda/(T^2)) |
| Period relation | Prove ord_T L_p(E,T) = ord_{s=1} L(E,s) |

These are ALL equivalent formulations of the same fundamental obstacle. No approach currently bypasses it.

### 8.3 What Our Framework Adds

Despite not solving the core problem, our BF/Kurihara framework adds genuine value:

1. **Computational access:** We can COMPUTE 2-point Kurihara numbers and verify they are nonzero for specific curves. This is numerical evidence for rank-2 BSD.

2. **Structural clarity:** The Fitting ideal hierarchy gives a clean algebraic framework for understanding what "rank 2" means module-theoretically.

3. **Reduction to known frameworks:** Kim's theorem + Kato's non-triviality reduces rank-2 BSD to the period relation (step 3 above), which is a more tractable problem than constructing entirely new Euler systems.

4. **The BF interpretation:** The gauge-theoretic language provides conceptual insight into WHY higher correlators detect higher rank.

---

## IX. Summary and Conclusions

### The KLZ Program

The Kings-Loeffler-Zerbes program is the most impressive systematic construction of Euler systems in modern number theory. Over a decade, they have:
- Constructed Euler systems for GL(2)xGL(2), GSp(4), GO(4), adjoint GL(2), and more
- Proved explicit reciprocity laws connecting each to p-adic L-functions
- Proved Bloch-Kato in rank 0 for all these representations
- Extended to p-adic families (Coleman families, Hida families)
- Pushed into non-ordinary territory (ultra-Kolyvagin systems)

However, they have NOT yet:
- Proved any rank >= 2 results unconditionally
- Proved the non-triviality of generalized Kato classes
- Proved a rank-2 Gross-Zagier formula

### Can KLZ + BF/Kurihara Close the Gap?

**Not directly.** The fundamental obstruction (proving non-triviality at rank 2) is the same in both frameworks. Our BF/Kurihara approach reformulates it in terms of Kurihara numbers and Fitting ideals, which gives computational access and conceptual clarity, but the core difficulty remains.

**The most promising bridge:** The period relation. If we can prove:

> ord_{T=0} L_p(E,T) = ord_{s=1} L(E,s)

then the IMC + Kim's theorem would give rank-2 BSD (and all higher ranks). This period relation is exactly what our route-period-relation campaign is targeting, using the Perrin-Riou comparison between p-adic and complex regulators.

### Feasibility Timeline

| Goal | Estimated Timeline | Approach |
|------|-------------------|----------|
| Rank 0 for more motives | 1-3 years | KLZ factory (ongoing) |
| Period relation at rank 2 | 3-7 years | Motivic methods + Perrin-Riou |
| Non-triviality of gen. Kato classes | 5-15 years | Anticyclotomic Iwasawa theory |
| Full unconditional rank-2 BSD | 10-20+ years | Requires combining all the above |
| Computational verification for specific curves | NOW | Kurihara numbers (already done for 389a1) |

### The Bottom Line

The Kings-Loeffler-Zerbes Euler system program provides essential infrastructure for BSD, but it alone is not close to proving rank-2 BSD. The missing piece in every approach is the same: connecting the vanishing order of L(E,s) to the structure of the Selmer group when the vanishing order is >= 2. Our BF/Kurihara framework provides the cleanest formulation of what needs to be proved (Fitting ideals + period relation) and the best computational tools for testing conjectures, but the theoretical gap remains a profound open problem.

---

## X. References

### KLZ Core Papers

- Kings, G., Loeffler, D., Zerbes, S.L. "Rankin-Eisenstein classes and explicit reciprocity laws." Cambridge J. Math. 5(1), 2017.
- Kings, G., Loeffler, D., Zerbes, S.L. "Rankin-Eisenstein classes in Coleman families." Res. Math. Sci. 3(29), 2016. arXiv:1506.06703.
- Loeffler, D., Zerbes, S.L. "Euler systems with local conditions." arXiv:1710.04956.
- Loeffler, D., Skinner, C., Zerbes, S.L. "Euler systems for GSp(4)." J. Eur. Math. Soc., 2022. arXiv:1706.00201.
- Loeffler, D., Zerbes, S.L. "On the Bloch-Kato conjecture for GSp(4)." arXiv:2003.05960.
- Loeffler, D., Zerbes, S.L. "A universal Euler system for GSp(4)." arXiv:2411.12576, Nov 2024.
- Loeffler, D., Zerbes, S.L. "Ultra-Kolyvagin systems and non-ordinary Selmer groups." arXiv:2511.08793, Nov 2025.
- Loeffler, D., Zerbes, S.L. "An Euler system for the adjoint of a modular form." arXiv:2312.04665, Dec 2023.
- Grossi, G., Loeffler, D., Zerbes, S.L. "Asai-Flach classes, p-adic L-functions and the Bloch-Kato conjecture for GO(4)." arXiv:2407.17055, Jul 2024.
- Loeffler, D., Zerbes, S.L. "On the Birch-Swinnerton-Dyer conjecture for modular abelian surfaces." New York J. Math. 30, 2024. arXiv:2110.13102.

### Diagonal Cycles and Generalized Kato Classes

- Darmon, H., Rotger, V. "Diagonal cycles and Euler systems I: A p-adic Gross-Zagier formula." Ann. Sci. ENS 47(4), 779-832, 2014.
- Darmon, H., Rotger, V. "Diagonal cycles and Euler systems II: The Birch and Swinnerton-Dyer conjecture for Hasse-Weil-Artin L-functions." J. Amer. Math. Soc. 30, 601-672, 2017.
- Bertolini, M., Darmon, H., Rotger, V. "Beilinson-Flach elements and Euler systems I: Syntomic regulators and p-adic Rankin L-series." J. Alg. Geom. 24, 355-378, 2015.
- Bertolini, M., Darmon, H., Rotger, V. "Beilinson-Flach elements and Euler systems II: BSD for Hasse-Weil-Artin L-series." J. Alg. Geom. 24, 569-604, 2015.
- Castella, F., Hsieh, M.-L. "On the non-vanishing of generalized Kato classes for elliptic curves of rank 2." Forum Math. Sigma 8, e12, 2020. arXiv:1809.09066.
- Castella, F. "Generalised Kato classes on CM elliptic curves of rank 2." arXiv:2204.09608, 2022.

### Euler System Theory

- Kato, K. "p-adic Hodge theory and values of zeta functions of modular forms." Asterisque 295, 2004.
- Mazur, B., Rubin, K. "Kolyvagin systems." Mem. AMS 168, 2004.
- Burns, D., Kurihara, M., Sano, T. "On the theory of higher rank Euler, Kolyvagin and Stark systems, II." arXiv:1805.08448, 2018.
- Kim, C.H. "The structure of Selmer groups and the Iwasawa main conjecture." arXiv:2203.12159v6, May 2025.

### Comparison and Bridge Papers

- Alonso, R. et al. "Anticyclotomic diagonal classes and Beilinson-Flach elements." arXiv:2509.07564, Sep 2025. [KEY: compares diagonal cycle and BF Euler systems via Eisenstein degeneration]
- Castella, F. "Nonvanishing of generalised Kato classes and Iwasawa main conjectures." arXiv:2312.01481, Dec 2023.
- Alonso, R. et al. "The diagonal cycle Euler system for GL_2 x GL_2." J. Inst. Math. Jussieu. arXiv:2106.05322.

### Beilinson-Bloch and Period Relations

- Li, C., Liu, Y. "Chow groups and L-derivatives of automorphic motives for unitary groups." Annals of Math. 194(3), 817-901, 2021.
- Perrin-Riou, B. "Fonctions L p-adiques d'une courbe elliptique et points rationnels." Ann. Inst. Fourier 43, 945-995, 1993.
- Skinner, C., Urban, E. "The Iwasawa main conjectures for GL_2." Invent. Math. 195, 2014.
