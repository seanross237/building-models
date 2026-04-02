# Exploration 004: Island Formula and Page Transition — Classicality Budget

**Mission:** Classicality Budget — holographic bound on QD redundancy with implications for BH evaporation.

**Goal:** Use the island formula to compute R_δ(t) = S(R,t)/S_T − 1 through the evaporation, identify the classicality transition, and assess whether the Page transition is a new QD perspective or a restatement of known results.

---

## Part 1: Model Setup

### The Island Formula

S(R) = min_{islands I} { Area(∂I) / (4G_N) + S_bulk(R ∪ I) }

Implemented two models:

**Linear (simple) model:**
- Before Page time (t < t_Page = t_evap/2): S(R,t) = S_BH × t/t_evap  (grows)
- After Page time: S(R,t) = S_BH × (1 − (t − t_Page)/t_evap)  (decreases)
- Island formula: minimum of no-island (Hawking) and island (decreasing) branches

**CFT (log) model — JT gravity:**
- S_Hawking(t) = (c/3) × ln(t/β)
- Page time: t_Page = β × exp(3·S_BH / (2c))
- Total evaporation time: t_evap = β × exp(3·S_BH / c)
- Island formula: S(R) = min(S_Hawking(t), S_BH − S_Hawking(t))

Code: `code/island_formula.py`

---

## Part 2: Numerical Results — R_δ(t)  [COMPUTED]

**Definition:** R_δ(t) = S(R,t)/S_T − 1, where S_T = 1 bit.

**Linear model classicality transition table** — t_classical = time when R_δ first ≥ 0:

| S_BH (bits)  | t_class/t_Page | t_class/t_evap | R_δ(t_Page)  |
|:-------------|:---------------|:---------------|:-------------|
| 10^77        | 2.000e-77      | 1.000e-77      | 5.000e+76    |
| 10^50        | 2.000e-50      | 1.000e-50      | 5.000e+49    |
| 10^20        | 2.000e-20      | 1.000e-20      | 5.000e+19    |
| 10^10        | 2.000e-10      | 1.000e-10      | 5.000e+09    |
| 10^4         | 2.000e-04      | 1.000e-04      | 4.999e+03    |
| 100          | 2.000e-02      | 1.000e-02      | 4.900e+01    |
| 10           | 2.000e-01      | 1.000e-01      | 4.000e+00    |

**Key formula** [COMPUTED]: t_classical = t_Page × (2/S_BH)

This follows analytically from the linear model: S(R,t) = S_T → S_BH × t/t_evap = 1 → t = t_evap/S_BH = t_Page × 2/S_BH.

**Interpretation:** For a solar-mass black hole (S_BH ≈ 10^77), the classicality transition in the exterior radiation happens at t_classical/t_Page ≈ 2×10^{-77}. The first Hawking photon emitted already provides enough entropy to create a single-bit classical fact in the exterior — the exterior becomes classically informative almost immediately after evaporation begins.

---

## Part 3: Redundancy Level Thresholds  [COMPUTED]

Time to first achieve R_δ(t) = k (as fraction of t_Page), linear model:

| S_BH    | k=0       | k=1       | k=2       | k=10      | k=100     | k=1000    |
|:--------|:----------|:----------|:----------|:----------|:----------|:----------|
| 10^77   | 2.0e-77   | 4.0e-77   | 6.0e-77   | 2.2e-76   | 2.0e-75   | 2.0e-74   |
| 10^10   | 2.0e-10   | 4.0e-10   | 6.0e-10   | 2.2e-09   | 2.0e-08   | 2.0e-07   |
| 100     | 2.0e-02   | 4.0e-02   | 6.0e-02   | 2.2e-01   | NEVER     | NEVER     |
| 10      | 2.0e-01   | 4.0e-01   | 6.0e-01   | NEVER     | NEVER     | NEVER     |

**All entries are t_k/t_Page.** For macroscopic BHs, even massive redundancy (k=1000) appears vastly before the Page time. For tiny BHs (S_BH=10), only k ≤ 3 is achievable (since max R_δ = 10/2 − 1 = 4).

**Formula** [COMPUTED]: t_k = t_Page × 2(k+1)/S_BH. For large S_BH, t_k ≪ t_Page for any fixed k.

---

## Part 4: Interior vs Exterior Classicality Budget  [COMPUTED]

This is the most structurally important result.

### Exterior budget (Hawking radiation observer)
R_δ_ext(t) = S(R,t)/S_T − 1

- Grows from −1 at t=0 to S_BH/2 − 1 at the Page time
- Shrinks back to −1 at total evaporation
- Transition R_δ = 0 at t_classical ≪ t_Page
- At Page time: R_δ_ext = S_BH/2 − 1 ≈ 5×10^76 (solar mass)

### Interior budget (operators behind the horizon)

**Before Page time:** Entanglement wedge of radiation does NOT include the interior. Interior operators cannot be reconstructed from exterior radiation. → R_δ_int = −1 (or effectively 0 — no copies).

**After Page time:** Island appears. Interior IS in entanglement wedge. Interior operators CAN be reconstructed from exterior radiation. → R_δ_int = S_BH/2/S_T − 1 (same as exterior at that moment).

### The key discontinuity  [COMPUTED]

At the Page time, R_δ_int undergoes a **discontinuous jump**:
- R_δ_int(t_Page^−) = −1 (no interior access)
- R_δ_int(t_Page^+) = S_BH/(2·S_T) − 1 ≈ 5×10^76 (for solar mass BH)

Solar mass BH summary:
```
t_classical_ext / t_Page  = 2.000e-77   (exterior becomes classical almost instantly)
t_classical_int / t_Page  = 1.000       (interior classicality appears EXACTLY at Page time)
R_delta_ext at Page time  = 5.000e+76
R_delta_int just before   = -1 (no access)
R_delta_int just after    = 5.000e+76
```

**Two-stage structure:** There are two distinct classicality transitions:
1. **Exterior transition** at t_classical ≈ (2/S_BH) × t_Page — the Hawking radiation itself first becomes classically informative. Happens almost immediately after evaporation starts.
2. **Interior transition** at t_Page — the BH interior first becomes classically inferable from the exterior radiation. Happens at the Page time, due to the island formula.

---

## Part 5: CFT (Log) Model vs Linear Model  [COMPUTED]

Using JT gravity + 2D CFT parameters (c=12, β=1):

| S_BH | t_Page/t_evap (CFT) | t_Page/t_evap (linear) |
|:-----|:--------------------|:-----------------------|
| 10   | 0.2865              | 0.5000                 |
| 30   | 0.0235              | 0.5000                 |
| 50   | 0.0019              | 0.5000                 |
| 100  | ≈0                  | 0.5000                 |

**Critical insight from the CFT model:** The Page time in the CFT model satisfies:

t_Page/t_evap = exp(−3·S_BH / (2c))

For large S_BH (≫ c), this is **exponentially smaller than 1/2**. In the linear model the Page time is always at half-evaporation. In the CFT model, the Page time arrives much earlier in the evaporation timeline (as a fraction of total evaporation time). This reflects the fact that Hawking emission slows dramatically as the BH shrinks and cools, so the bulk of evaporation time is spent emitting very little entropy.

**For R_δ(t), the qualitative structure is the same in both models** — the interior classicality jump occurs at the Page time in both — but the quantitative location of that Page time is very different.

---

## Part 6: Novelty Assessment

### The conjecture
"The Page transition marks when the BH interior first becomes QD-classical from the exterior's perspective."

### Assessment: Restatement with new language  [CONJECTURED]

**What this says in QD terms:**
- Before Page time: R_δ_int = −1 → interior facts have zero redundancy in exterior radiation → interior is not QD-observable from outside.
- After Page time: R_δ_int > 0 → interior facts have positive redundancy in Hawking radiation → interior becomes QD-observable from outside.

**What HQEC/entanglement wedge reconstruction already says:**
- Before Page time: interior NOT in entanglement wedge of Hawking radiation → interior not reconstructable from R.
- After Page time: interior IS in entanglement wedge → interior is reconstructable from R.

**Conclusion:** The QD framing of "classicality transition at the Page time for interior operators" is a **restatement in QD language** of the standard entanglement wedge result. It adds:
- A quantitative budget (R_δ = S_BH/2 − 1 at the Page time), which is numerically trivially satisfied for macroscopic BHs.
- The concept of a jump from R_δ=−1 to R_δ=S_BH/2−1, which is the holographic version of what happens when you get "access" to a system.
- The two-stage structure (exterior becomes classical early, interior at Page time) which is genuinely a new way of organizing the result.

**What QD adds that HQEC doesn't:**
1. The distinction between "is reconstructable" and "has been copied redundantly enough to be classically observed" — HQEC says the interior is IN the entanglement wedge, QD says how many independent copies exist.
2. The explicit R_δ budget, bounding how many observers can simultaneously infer interior facts from Hawking radiation after the Page time.
3. The exterior transition time t_classical ≪ t_Page, which is not emphasized in HQEC discussions but which follows naturally from counting Hawking photons.

**Is there a distinguishable prediction?** The QD framework suggests that before the Page time, the Hawking radiation forms a classically observable record of the BH's *exterior* properties (mass, charge, angular momentum) but not interior properties. After the Page time, interior facts also become redundantly encoded. This matches what's known but provides a measurement-theoretic criterion: "at what radiation fraction does classical observability switch on?" The answer is t_classical ≈ 2/S_BH (exterior, nearly instantaneous) and t_Page (interior). No new physical prediction beyond entanglement wedge results.

---

## Summary of Key Results

| Result | Value | Status |
|:-------|:------|:-------|
| t_classical_ext (solar mass) | 2×10^{-77} × t_Page | [COMPUTED] |
| t_classical_int | t_Page (exactly) | [COMPUTED] |
| R_δ at Page time (solar mass) | 5×10^76 | [COMPUTED] |
| Discontinuity in R_δ_int at t_Page | from −1 to 5×10^76 | [COMPUTED] |
| CFT model Page time fraction (S=30, c=12) | 0.0235 of t_evap | [COMPUTED] |
| "Interior classicality at Page time" is new | No — restatement in QD language | [CONJECTURED] |
| Two-stage structure (exterior early, interior at Page) | Genuine organizing insight | [CONJECTURED] |

---

## Code

All computations: `code/island_formula.py`
Output plots: `code/page_curve_linear.png`, `code/page_curve_comparison.png`, `code/classicality_budget_summary.png`

