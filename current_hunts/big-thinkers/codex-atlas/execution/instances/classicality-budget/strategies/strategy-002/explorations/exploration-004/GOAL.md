# Exploration 004: Island Formula and Page Transition — Classicality Budget Through BH Evaporation

## Mission Context

We are studying the "classicality budget" — an upper bound R_δ ≤ (S_max/S_T − 1)/(1−δ) on quantum Darwinism (QD) redundancy. Strategy-001 conjectured that the Page time in black hole evaporation marks a "classicality transition" — a moment when classical reality (in the QD sense) becomes possible for observers of the black hole interior. This is currently labeled CONJECTURED and requires explicit computation.

**What's established:**
- The holographic version: R_δ ≤ S_max/S_T where S_max = S(boundary) = RT area / (4G)
- Before Page time: entanglement wedge of Hawking radiation does NOT include BH interior → R_δ = 0 for interior operators
- After Page time: an "island" appears in the entanglement wedge → interior becomes reconstructable by exterior radiation
- The Ryu-Takayanagi formula (used in strategy-001) gives the entropy of boundary subregions in static AdS/CFT
- The **island formula** (quantum extremal surface) extends this to evaporating black holes

**The island formula:**
S(R) = min_{islands I} { Area(∂I) / (4G_N) + S_bulk(R ∪ I) }

Where:
- R = Hawking radiation region (collected exterior radiation)
- I = "island" (a bulk region whose boundary is extremized)
- S_bulk(R ∪ I) = bulk entanglement entropy of the combined region
- Before Page time: no island contributes; S(R) = S_bulk(R) = S_Hawking(t) (grows)
- After Page time: island is the BH interior; S(R) = S_BH − S_Hawking(t) (decreases, following Page curve)

## Your Goal

Compute R_δ(t) as a function of evaporation time t using the island formula, and determine whether the Page transition creates a "classicality transition."

## Part 1: Set Up the Model

Use the standard 2D model for the island formula computation. This is the doubly holographic setup or equivalently the JT gravity + 2D CFT model from Penington (arXiv:1905.08255) and Almheiri et al. (arXiv:1911.09536).

**The Page curve:**
- Before Page time t_Page: S(R,t) = S_Hawking(t) = (c/3) ln(t) + const (or use a simple linear model S(t) = α·t for evaporation)
- After Page time: S(R,t) = S_BH − (c/3) ln(t) + const (or simple: S(t) = S_BH − α·t)
- Page time: when S_Hawking(t) = S_BH/2 (half the original BH entropy has been emitted)

**Simplification for computation:** Use the "simple model" where:
- S_BH(t=0) = initial BH entropy (Bekenstein-Hawking) = A_BH / (4G)
- S_Hawking(t) = (S_BH/t_evap) × t for t < t_Page (linear growth)
- S_Hawking(t) = S_BH − (S_BH/t_evap) × (t − t_Page) for t > t_Page (linear decrease)
- t_Page = t_evap/2 (where t_evap = total evaporation time)
- For a solar-mass BH: S_BH ≈ 10^77 bits, t_evap ≈ 2×10^67 years

## Part 2: Compute R_δ(t)

The classicality budget for the exterior observer reading the Hawking radiation:

**R_δ(t) = S(R,t) / S_T − 1**

where:
- S(R,t) = Page curve entropy (from island formula)
- S_T = entropy per "fact" about the BH interior = 1 bit (assume the simplest case)

So:
- Before Page time: R_δ(t) = S_Hawking(t)/S_T − 1 (grows from −1 toward S_BH/S_T − 1)
- After Page time: R_δ(t) = [S_BH − S_Hawking(t)]/S_T − 1 (decreases back toward −1)

**Compute this numerically with Python and plot:**

```python
import numpy as np
import matplotlib.pyplot as plt

# Simple model
S_BH = 1e77  # BH entropy in bits (solar mass)
S_T = 1.0    # 1 bit per fact
t_evap = 1.0  # normalized evaporation time
t_page = 0.5 * t_evap  # Page time at half evaporation

t = np.linspace(0, t_evap, 1000)
# Page curve (simple piecewise linear model)
S_R = np.where(t < t_page,
               S_BH * t / t_evap,  # growing phase
               S_BH * (1 - (t - t_page) / t_evap))  # decreasing phase

R_delta = S_R / S_T - 1
```

Also compute for a SMALL BH where S_BH is small enough to see the transition clearly (say S_BH = 100 bits for illustration).

## Part 3: Identify the Classicality Transition

Define: **"classicality transition"** = the moment when R_δ first becomes ≥ 0 (i.e., when there is at least 1 bit available for redundancy, meaning a single independent witness of 1 fact is possible).

From the formula:
- R_δ ≥ 0 iff S(R,t) ≥ S_T = 1 bit
- Before Page time: this happens at t_classical = t_evap × S_T/S_BH ≪ t_Page
- The classicality transition occurs LONG BEFORE the Page time

**Compute t_classical / t_Page for various values of S_BH:**

| S_BH (bits) | t_classical / t_Page | Interpretation |
|-------------|---------------------|----------------|
| 10^77 (solar mass) | ? | ? |
| 10^10 | ? | ? |
| 100 | ? | ? |
| 10 | ? | ? |

**The key question:** When does MEANINGFUL redundancy (R_δ ≥ k for k = 2, 10, 100) appear relative to the Page time?

## Part 4: What Happens at the Page Time

At the Page time, S(R) = S_BH/2 (maximum entropy collected). This means:
- R_δ(t_Page) = S_BH/(2·S_T) − 1

For a solar mass BH with S_BH = 10^77, R_δ(t_Page) ≈ 5×10^76 — still enormous, trivially not constraining.

**But what about the quantum information content?** After the Page time, the island formula says the interior IS reconstructable from the exterior radiation. From the QD perspective, this means:

- Before Page time: exterior Hawking radiation does NOT know about the interior (R_δ = 0 from RT formula, no island)
- After Page time: exterior radiation DOES know about the interior (R_δ ≥ 1, island present)

This IS a classicality transition in the strict sense — but it happens at the Page time (when half the BH has evaporated), not at t_classical (when first 1 bit has been emitted).

**Compute the budget separately for the INTERIOR vs the EXTERIOR:**
- For exterior observers reading Hawking radiation: R_δ_exterior(t) = S(R,t)/S_T − 1
- For interior facts (operators behind the horizon): R_δ_interior(t) = 0 before Page time, > 0 after Page time

## Part 5: Connection to Information Paradox

The conjecture is: "The Page transition marks when the BH interior first becomes QD-classical from the exterior's perspective."

Assess this conjecture:
1. Is it new? Or is it just a restatement of "after the Page time, the interior is reconstructable"?
2. What does QD add here that HQEC/entanglement wedge reconstruction doesn't already say?
3. Is there a physically distinguishable prediction from this framework?

## Part 6: The JT Gravity Model (More Rigorous)

For the more rigorous version, use the JT gravity + 2D CFT result from Penington (2019):

```
S(R) = min(S_Hawking(t), S_BH - S_Hawking(t) + O(1))
```

where S_Hawking(t) = (c/3) ln(t/β) in the conformal field theory (c = central charge, β = inverse temperature).

The island transition happens at t_Page where S_Hawking(t_Page) = S_BH/2.

Implement this more precise version and compare with the simple linear model above.

## Success Criteria

**SUCCESS:**
1. Python code produces the Page curve and R_δ(t) plot
2. The classicality transition time t_classical is computed as a fraction of t_Page for several BH masses
3. A clear verdict on whether the "Page-time classicality transition" is a new perspective or a restatement of known results
4. All numbers are computed (not just formulas)

**FAILURE:** Returns the formulas without running code; or hedges on the "new perspective vs. restatement" question.

## Output

Write code to: `explorations/exploration-004/code/island_formula.py`
Write your report to: `explorations/exploration-004/REPORT.md`
Write a concise summary (max 400 words) to: `explorations/exploration-004/REPORT-SUMMARY.md`

Write the report incrementally — complete each section and write it to the file before moving on to the next.

## Strategy Directory

`/Users/seanross/kingdom_of_god/building_models/current_hunts/atlas/execution/instances/classicality-budget/strategies/strategy-002/`
