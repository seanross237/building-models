# Exploration 004: Adversarial Review of Strategy-002 Claims

## Mission Context

Strategy-002 has completed 3 explorations investigating the BKM enstrophy bypass for 3D Navier-Stokes regularity. The key claims are:

1. **BKM enstrophy advantage**: The BKM-based enstrophy ODE gives blow-up times 10^7 to 10^16 times later than the Ladyzhenskaya-based ODE for tested NS flows, with the advantage scaling as ~Re^3.

2. **BKM enstrophy theorem**: Proved in 4 steps (enstrophy equation → Holder → BGW → combined). The BKM closure gives dE/dt <= C*E*||omega||_{L^inf}*log(...) with no nu^-3 factor and linear (not cubic) enstrophy.

3. **One proof gap**: The BGW estimate ||S||_{L^inf} <= C*||omega||_{L^inf}*log(...) on T^3 with explicit constant C <= 0.81.

4. **C(F4) is dead**: The identity C_Leff^4 = F4*R^3 shows the Strategy-001 correlation was an artifact.

5. **Slack atlas is IC-robust for tight bounds**: F5 CZ (7.6-17.5x), F1 Lad (3.0-18.7x), F3 Sob (2.7-27.5x) across 4 ICs.

6. **From Strategy-001 (carried forward)**: The 237x vortex stretching slack, the 3-factor decomposition (63% Lad + 31% geom + 6% sym), and the spectral Ladyzhenskaya dead end.

## Goal

Adversarially review ALL claims from Strategy-002 (and key claims from Strategy-001 that haven't been revised). For each claim:

1. **Check the proof step by step.** Identify the weakest step.
2. **Search for the result in the literature.** Is this already known? Use exact search terms.
3. **Identify the strongest counterargument.** What is the best reason the claim might be wrong, trivial, or not novel?
4. **Assess novelty** on the scale: KNOWN / PARTIALLY KNOWN / NOVEL / GENUINELY NOVEL.

## Specific Claims to Review

### Claim 1: T_BKM/T_Lad ~ Re^3
**Source:** Exploration 001, formalized in Exploration 002 (Corollary 3)
**Claim:** The ratio of BKM to Ladyzhenskaya effective blow-up times scales as Re^3, because the Ladyzhenskaya closure introduces a nu^-3 factor that BKM avoids.
**Search terms for literature:** "enstrophy blow-up time comparison", "BKM vs Ladyzhenskaya regularity", "vortex stretching bound comparison", "enstrophy ODE closure comparison"

### Claim 2: BKM Enstrophy Theorem
**Source:** Exploration 002 (Theorem 1)
**Claim:** dE/dt <= C_{BGW} * E * ||omega||_{L^inf} * [1 + log^+(||grad omega||/||omega||)] - nu||grad omega||^2
**Strongest potential attack:** This may be a trivial corollary of the BKM criterion (1984). If so, it's KNOWN, not novel.
**Key question:** Has anyone explicitly written down this enstrophy-level version of BKM? Check BKM (1984), Constantin & Foias textbook (1988), Majda & Bertozzi (2001), Robinson/Rodrigo/Sadowski (2016).

### Claim 3: BGW estimate on T^3 with C <= 0.81
**Source:** Exploration 002 (empirical)
**Claim:** The Brezis-Gallouet-Wainger estimate holds on T^3 for the CZ strain operator with constant C <= 0.81.
**Key question:** Is this just the standard BGW estimate applied to the CZ operator? Or does the periodic domain require additional work?

### Claim 4: C(F4) identity kills the direction
**Source:** Exploration 003
**Claim:** C_Leff^4 = F4 * R^3 is an exact algebraic identity, making the C(F4) correlation an artifact.
**Key question:** Is this identity trivially obvious from the definitions? (It is algebraic, so it must be...)

### Claim 5: IC-robust slack atlas
**Source:** Exploration 003 (Task B)
**Claim:** F5 CZ, F1 Lad, F3 Sob have IC-robust single-digit-to-low-double-digit slacks across 4 ICs.
**Key question:** Is this a meaningful finding or just saying that classical inequalities are closer to tight for typical flows?

### Claim 6 (Strategy-001): 237x vortex stretching slack
**Source:** Strategy-001, validated in Strategy-002
**Key question:** Has anyone quantified the slack in vortex stretching bounds before? Check Protas group (JFM 2020), Doering group, Gibbon.

## Structure of Your Review

For EACH claim, write:
```
### Claim N: [title]
**Step-by-step check:** [verify the logic]
**Literature search:** [what you found]
**Strongest counterargument:** [best reason it fails]
**Novelty verdict:** KNOWN / PARTIALLY KNOWN / NOVEL / GENUINELY NOVEL
**Defensibility:** 1-5 (1=easily demolished, 5=rock solid)
```

At the end, provide:
- **Overall strategy assessment:** What survived adversarial review?
- **What to recommend for the FINAL-REPORT:** Which claims should be highlighted vs downplayed?

## Output

Write REPORT.md and REPORT-SUMMARY.md in this directory.
