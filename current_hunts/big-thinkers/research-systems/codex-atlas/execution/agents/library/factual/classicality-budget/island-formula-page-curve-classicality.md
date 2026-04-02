---
topic: Island formula and QD classicality budget through BH evaporation — quantitative analysis
confidence: provisional
date: 2026-03-27
source: classicality-budget strategy-002 exploration-004
---

## Summary

Using the island formula, R_δ(t) = S(R,t)/S_T − 1 is computed throughout BH evaporation. There are two distinct classicality transitions: (1) the **exterior transition** at t_classical ≈ (2/S_BH) × t_Page — exterior Hawking radiation becomes classically informative almost immediately after evaporation begins; (2) the **interior transition** at exactly t_Page — R_δ_int undergoes a discontinuous jump from −1 to S_BH/2 − 1 as the island appears. The "Page-time interior classicality" claim is a **restatement in QD language** of the standard HQEC/entanglement wedge result, not new physics.

---

## R_δ(t) Formula

**Definition:** R_δ(t) = S(R,t)/S_T − 1 where S(R,t) is the entropy of the Hawking radiation R at time t, given by the island formula:

  S(R,t) = min_{islands I} { Area(∂I)/(4G_N) + S_bulk(R ∪ I) }

**Linear model (simple):**
- Before Page time: S(R,t) = S_BH × t/t_evap (grows)
- After Page time: S(R,t) = S_BH × (1 − (t − t_Page)/t_evap) (decreases)
- Page time = t_evap/2 in linear model

**CFT (log) model — JT gravity:**
- S_Hawking(t) = (c/3) × ln(t/β)
- t_Page = β × exp(3·S_BH/(2c)); t_evap = β × exp(3·S_BH/c)
- t_Page/t_evap = exp(−3·S_BH/(2c)) → exponentially small for large S_BH

---

## Two-Stage Classicality Structure

### Exterior transition (Hawking radiation observer)

**Formula:** t_classical_ext = t_Page × 2/S_BH (linear model)

| S_BH | t_class/t_Page |
|------|----------------|
| 10^77 | 2×10^{-77} |
| 10^10 | 2×10^{-10} |
| 100 | 0.02 |
| 10 | 0.2 |

For a solar-mass BH (S_BH ≈ 10^77): t_classical/t_Page ≈ 2×10^{-77}. The first Hawking photon emitted provides enough entropy for one classical bit in the exterior — the exterior becomes classically informative almost immediately after evaporation begins.

**Formula for reaching redundancy R_k (exterior):** t_k = t_Page × 2(k+1)/S_BH

### Interior transition (operators behind the horizon)

- **Before Page time:** Entanglement wedge of radiation does NOT include interior. R_δ_int = −1 (no copies).
- **After Page time:** Island appears. R_δ_int = S_BH/(2·S_T) − 1.
- **Transition is exactly at t_Page**, not gradual.

**Discontinuous jump at the Page time (solar mass BH):**
- R_δ_int(t_Page^−) = −1
- R_δ_int(t_Page^+) = 5×10^76
- The interior goes from "inaccessible to any observer" to "redundantly encodable 5×10^76 times" at a single moment.

### Solar mass summary
```
t_classical_ext / t_Page  = 2.0×10^{-77}
t_classical_int / t_Page  = 1.000  (exactly)
R_δ_ext at Page time      = 5×10^76
R_δ_int just before       = −1
R_δ_int just after        = 5×10^76
```

---

## CFT vs Linear Model Comparison

| S_BH | t_Page/t_evap (CFT, c=12) | t_Page/t_evap (linear) |
|------|--------------------------|------------------------|
| 10 | 0.287 | 0.500 |
| 30 | 0.024 | 0.500 |
| 50 | 0.002 | 0.500 |
| 100 | ≈0 | 0.500 |

**Key insight from CFT model:** For large S_BH, the Page time arrives exponentially earlier than half-evaporation — the bulk of evaporation time is spent emitting very little entropy as the BH cools. The qualitative two-stage structure is the same in both models.

---

## Novelty Assessment

**The conjecture:** "The Page transition marks when the BH interior first becomes QD-classical from the exterior's perspective."

**Verdict: RESTATEMENT IN QD LANGUAGE — not new physics [CONJECTURED]**

What HQEC/entanglement wedge reconstruction already says:
- Before Page time: interior NOT in entanglement wedge of Hawking radiation → not reconstructable
- After Page time: interior IS in entanglement wedge → reconstructable from R

What QD adds (genuine contributions):
1. The quantitative R_δ budget at the Page time (R_δ = S_BH/2 − 1), bounding how many independent observers can simultaneously infer interior facts
2. The exterior classicality time t_classical ≪ t_Page, which is not emphasized in HQEC literature but follows naturally from counting Hawking photons
3. The **two-stage structure** (exterior becomes classical early, interior at Page time) as a genuine organizing insight — not anticipated in HQEC discussions
4. A measurement-theoretic criterion for observability: "at what radiation fraction does classical observability switch on?"

**What QD does NOT add beyond HQEC:** No new physical prediction beyond entanglement wedge results. The fact that the interior is "classically observable" after the Page time is exactly what HQEC already establishes via entanglement wedge inclusion.

---

## Connection to Prior Findings

This analysis confirms and extends the conjecture in `holographic-classicality-budget.md` (E007), which said:
- "Before Page time: R = 0 for all interior operators" ✓
- "After Page time: collective verification possible (R_collective ≥ 1)" — now UPGRADED: the jump is to R_δ = S_BH/2 − 1 ≈ 5×10^76, not just barely ≥ 1

The discrepancy: E007 said "true redundancy remains R ≈ 0 — the interior just barely enters the entanglement wedge." E004 shows this was WRONG: after the Page time, R_δ_int = S_BH/2 − 1 is astronomical. The island formula gives exactly the same S_max as the Bekenstein entropy; the entire S_BH budget is suddenly available for interior reconstruction.

---

## Status

All R_δ(t) values [COMPUTED] via `code/island_formula.py`. Two-stage structure [COMPUTED]. CFT vs linear comparison [COMPUTED]. Novelty verdict [CONJECTURED].
