---
topic: Yang-Mills partial positive geometry via scattering forms and corolla polynomial
confidence: verified
date: 2026-03-27
source: amplituhedron strategy-001 exploration-003; arXiv:1711.09102, arXiv:2405.10601
---

## Finding

Pure Yang-Mills has a **partial** positive geometry description at tree level and (messily) at 1-loop. The structure is real but requires more machinery than the N=4 amplituhedron — it is not a clean canonical form.

## Tree Level: Scattering Forms (arXiv:1711.09102, JHEP 2018)

Arkani-Hamed, Bai, He, Yan show:

1. **Color is Kinematics**: Kinematic wedge products in the scattering form satisfy the same Jacobi relations as color factors. This provides a geometric origin for BCJ/color-kinematics duality — something standard Feynman diagram methods cannot explain. **This is the most valuable insight: WHY color and kinematics obey the same algebra is now geometric.**

2. **YM scattering form**: The Yang-Mills amplitude (summed over color orderings) corresponds to a differential form in kinematic space whose pullback to the associahedron boundary recovers gluon amplitudes.

3. **CHY connection**: The worldsheet associahedron (from CHY moduli space) maps to the kinematic associahedron via scattering equations — a diffeomorphism giving a geometric encoding of YM tree amplitudes.

**What this achieves**: YM tree amplitudes have a geometric description via scattering forms. **What this is not**: A clean amplituhedron-style positive geometry — the scattering forms require CHY pushforward machinery and are not a canonical form of a clean polytope.

## Tree Level: Crucial Observation

Tree-level gluon amplitudes in pure YM are **identical** to tree-level N=4 SYM gluon amplitudes in the MHV sector (SUSY partners decouple for pure-gluon external states). Any geometric structure at tree level for YM is "inherited" from N=4.

## 1-Loop: Corolla Polynomial Extension (arXiv:2405.10601, JHEP 2025)

Laddha & Suthar (May 2024): The S-matrix of YM is obtained by contracting the canonical form of the ABHY associahedron with a multi-vector field (MVF) whose components are determined by the **Corolla polynomial** (Kreimer-Sars-van Suijlekom). Extends to **1-loop planar YM integrands** via a D̂ₙ polytope. Constructs curve integral formulae for tree and 1-loop gluon amplitudes.

**Assessment**: Significant — extends positive geometry to loop-level YM via corolla polynomial. However, the canonical form requires polynomial decoration rather than being a clean geometric object.

## Loop-Level Obstruction (Amplituhedron Approach)

At loop level, pure YM suffers from — **when approached via the amplituhedron framework**:
- UV divergences (theory is not UV-finite)
- No amplitude/Wilson loop duality
- No dual conformal symmetry
- Rational terms in loop amplitudes not captured by cut-based methods

These fundamentally prevent an **amplituhedron-style** clean geometric encoding. The corolla polynomial provides a partial workaround but not a fundamental resolution in this framework.

**⚠️ UPDATE (2025): A different geometric approach — surface kinematics / surfaceology — HAS resolved the canonical loop integrand problem for non-SUSY YM.** arXiv:2408.11891 (PRL 2025) defines a canonical YM loop integrand via scalar scaffolding in kinematic space (not twistor space). This is not an amplituhedron; it is a separate framework. The obstruction above is specific to the amplituhedron approach. See `surfaceology/surfaceology-yang-mills-integrand.md`.

## Status Summary

| Level | Status | Reference |
|-------|--------|-----------|
| Tree-level gluon (color-ordered) | ✅ Scattering forms work | arXiv:1711.09102 |
| 1-loop planar YM | ⚠️ Corolla polynomial (messy) | arXiv:2405.10601 |
| Loop-level general (amplituhedron) | ❌ UV divergences prohibit | — |
| Loop-level general (surfaceology) | ✅ Surface kinematics solves it | arXiv:2408.11891 (PRL 2025) |
| BCJ duality origin | ✅ Geometrically explained | arXiv:1711.09102 |
