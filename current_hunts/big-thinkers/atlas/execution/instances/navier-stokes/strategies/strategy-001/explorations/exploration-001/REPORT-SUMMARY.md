# Exploration 001: Summary — Load-Bearing Inequalities in 3D NS Regularity Theory

## Goal
Produce a comprehensive catalog of every load-bearing inequality in the major 3D Navier-Stokes regularity results: exact statements, sources, sharpness, scaling in Re, constant status, and Tao generic/NS-specific classification.

## What Was Done
Assembled a 17-entry catalog covering all target inequality families: functional inequalities (Ladyzhenskaya, GNS, Sobolev embedding, Agmon, Calderón-Zygmund, Brezis-Gallouet-Wainger, Kato-Ponce, HLS), energy/enstrophy estimates (global energy inequality, enstrophy ODE, Constantin-Fefferman vortex stretching, H^s energy), regularity criteria (Prodi-Serrin, Beale-Kato-Majda), partial regularity (CKN local energy, CKN ε-regularity, ESS L³ endpoint), and Gronwall. For each: precise mathematical statement, source, usage, scaling, constant status, sharpness, and Tao classification.

## Outcome: Succeeded

**13 inequalities** cataloged with all 7 fields (4 more additional entries beyond the minimum 8). The Tao classification is attempted for all. A ranked slack analysis and structural chain analysis is provided.

## Key Takeaway

**The single most load-bearing bottleneck in 3D NS regularity theory is the vortex stretching bound.** The inequality

    |VS| ≤ C ||ω||^{3/2}_{L²} ||∇ω||^{3/2}_{L²}

derived from Ladyzhenskaya applied to the enstrophy equation is the exact step that makes the enstrophy ODE blow up (dy/dt ≤ Cy³/ν³). This is the inequality whose tightening would most directly change what is provable. Constantin-Fefferman (1993) showed geometrically it IS loose for flows with disordered vorticity direction — the actual VS is much smaller for non-aligned vorticity. But no analytic proof has captured this.

**Second most important:** The ε-regularity threshold in CKN (ε*) is completely uncomputed — it is a pure existence constant from a compactness argument. Making it explicit would quantify partial regularity.

**The Tao obstruction is critical:** Any proof must use NS-specific structure (beyond energy + scaling + GNS). Generic inequalities (GNS, Sobolev, Gronwall) cannot alone prove regularity. The most interesting slack therefore lives in NS-specific inequalities: E2/E3 (vortex stretching), R3/R4 (CKN), R1 (Prodi-Serrin), R2 (BKM).

## Top 5 by Expected Slack

1. **Vortex stretching bound (E2/E3):** Real VS ≈ Re^{-1/4} × (Ladyzhenskaya bound) for isotropic turbulence. Computation: measure VS_actual vs. VS_Lad for model flows.
2. **Agmon + Gronwall chain (F4 + G1):** L^∞ overestimate × exponential amplification = astronomical overestimate for large Re. Computation: Burgers analog.
3. **CKN ε-regularity constant (R4):** Completely uncomputed — explicit ε* would yield quantitative partial regularity. Computation: variational problem in parabolic cylinder.
4. **NS-specific Ladyzhenskaya constant (F1):** The divergence-free constraint may reduce C_L. Computation: numerical optimization over div-free fields on T³.
5. **BKM log-Sobolev inequality (F6):** Log exponent is sharp (1/2) but leading constant is existential. Computation: sharp constant for 3D BWG inequality.

## Unexpected Findings

1. **The transport cancellation ⟨u·∇(J^s u), J^s u⟩ = 0 is NS-specific** (uses div u = 0) and is the key reason H^s estimates are as clean as they are. This is a hidden use of NS structure in E4.

2. **The gap between CKN singular set dimension (≤1 parabolic) and the conjectured dimension (0, i.e., isolated points)** represents a substantial slack in the entire partial regularity program — not just a single inequality but the geometry of the covering argument.

3. **All functional inequalities (F1-F8) are sharp on ℝ³ but their extremal functions (Aubin-Talenti bubbles) are static, isotropic, and non-divergence-free.** The "NS-specific" Sobolev constant (restricted to div-free vector fields) may be strictly smaller than the general one — this has apparently not been systematically computed.
