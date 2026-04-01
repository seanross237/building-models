---
topic: Require total baryonic mass (gas + stars) in galaxy rotation curve goals
category: goal-design
date: 2026-03-27
source: "compton-unruh strategy-001 meta-exploration-006"
---

## Lesson

For galaxy rotation curve fits, always require **total baryonic mass** (stars + gas, with helium
correction), not just stellar mass. For gas-rich galaxies, the gas component can easily exceed the
stellar mass — in NGC 2403, the gas mass was ~85% of total baryonic mass. Using stellar mass only
produces systematically wrong fits and misleading chi-squared values.

## Evidence

- **compton-unruh strategy-001 exploration-006** — Initial NGC 2403 fit used only the stellar mass
  (2.5×10⁹ M_☉), missing ~85% of total baryonic mass (HI ×1.33 for He = ~9.3×10⁹ M_☉; total
  1.85×10¹⁰ M_☉). The initial fit gave misleading χ² results. Correcting to total baryonic mass
  (BTFR-consistent for v_flat = 131 km/s) changed the best-fit a₀ significantly and prevented a
  false positive on the model comparison. The explorer caught its own error because the goal included
  an "honest assessment" requirement.

## How to Apply

Include in the goal statement: **"Use total baryonic mass (stars + gas; apply ×1.33 helium factor
to HI mass). Check against the BTFR (v_flat⁴ = G × M_baryon × a₀) to verify mass is consistent
with the observed flat rotation velocity before fitting."**

This double-check catches missing gas components before they contaminate the fit. For dwarf galaxies
and irregular galaxies, gas is often the dominant baryonic component.

## Why This Matters

Galaxy rotation curve tests of MOND-type models are sensitive to the exact a₀ value. A factor-of-2
mass error (from missing gas) translates to a factor-of-2^{1/4} ≈ 1.2 error in v_flat predictions
and can shift the best-fit a₀ by 30–50%. The BTFR consistency check is a minimal sanity condition
that should appear in every rotation-curve exploration goal.

## Related Lesson

This pairs with `require-quantification-in-stress-tests.md` — use χ²/dof to make model comparisons
unambiguous. With correct mass accounting AND quantitative χ², the conclusion (cH₀ ruled out at
χ²/dof ~ 130; cH₀/6 fits at χ²/dof ~ 1) is decisive rather than impressionistic.
