# Step 0+1 Goal: Orientation, Landscape Verification, and Pressure Term Dissection

## Mission Context

**Mission:** Determine whether the Vasseur pressure exponent gap (β = 4/3, need β > 3/2) can be closed using H^1 structure of the pressure from compensated compactness.

**Chain:** The planning loop selected a chain that exploits the divergence-free structure of u to show p ∈ H^1 (Hardy space), then attempts to convert this H^1 structure into improved De Giorgi iteration estimates. The chain has 5 steps (0-4). This strategizer execution covers Steps 0 and 1.

**Why H^1 matters:** Standard CZ estimates give p ∈ L^{4/3}, but for div-free u, compensated compactness (CLMS 1993) gives p ∈ H^1. H^1 is NOT a better L^p space (H^1 ⊂ L^1 ⊂ L^{4/3}), but it has additional structure: cancellation, atomic decomposition, and duality with BMO. The core question is whether this structure can be converted into something the De Giorgi machine can digest.

## Step 0: Orientation (1 exploration)

**Tasks:**
1. Confirm β = 4/3 is still the best known pressure exponent for De Giorgi NS regularity. Check Vasseur's publications 2014-2026, citing papers.
2. Search for prior work combining compensated compactness / H^1 pressure with De Giorgi iteration for NS. Key terms: "compensated compactness" + "De Giorgi" + "Navier-Stokes."
3. Check Tran-Yu (2014, AIHP) relevance — does it address the pressure exponent or a different question?
4. Verify the 3/2 threshold is correct for full regularity.

**Kill conditions:**
- (A) Someone already pushed past β = 4/3 → report who and how, pivot to understanding their method
- (B) H^1 + De Giorgi already tried and documented failure → report the obstruction
- (C) β = 4/3 proven sharp for ALL decompositions → report sharpness, mission complete

## Step 1: Pressure Term Dissection (1-2 explorations)

**Tasks:**
1. Write out the De Giorgi energy inequality for the Vasseur (2007) / Caffarelli-Vasseur (2010) framework with ALL terms explicit (dissipation, nonlinear transport, pressure, commutator/cutoff corrections).
2. For the pressure term, trace the chain of estimates producing 4/3. Identify each inequality (Hölder, CZ, Sobolev) and its exponent contribution.
3. **Caffarelli-Vasseur comparison:** In drift-diffusion (no pressure), De Giorgi reaches criticality. Map term-by-term which estimates succeed without pressure that fail with pressure. This isolates the exact gap.
4. **Bogovskii corrector scaling:** When pressure is localized via cutoff φ_k, compute ||u · ∇φ_k||_{L^p} on the annulus {k ≤ |u| ≤ k+1} using super-level set measure decay from L^{3,∞}. Determine whether the corrector grows faster than the De Giorgi energy.

**Output:**
- Annotated inequality chain: A → B → C → ... → β = 4/3
- Comparison table: drift-diffusion (succeeds) vs NS (fails at pressure term)
- Bogovskii corrector scaling computation

**Kill condition:** If the 4/3 exponent is proven to arise from a single sharp inequality AND the H^1 route cannot bypass it, document this as the obstruction. If the bottleneck is distributed, map the constraint surface with sensitivity analysis.

## What Feeds Into Step 2

Step 2 will test three routes for converting H^1 pressure into De Giorgi-compatible estimates:
- 2A: Interpolation (H^1, L^{4/3})_{θ,q}
- 2B: H^1-BMO duality (most promising — requires De Giorgi test functions to be BMO-bounded)
- 2C: Atomic decomposition

This step needs to deliver: (a) which specific inequality to target, (b) whether the Bogovskii corrector is manageable, and (c) the Caffarelli-Vasseur comparison showing exactly what pressure costs.

## Available Tools

- Python (numpy, scipy, sympy, mpmath)
- SageMath 10.8
- Lean 4 + Mathlib
- Web search for papers

## Validation Requirements

- Function spaces specified precisely (Sobolev, Lebesgue, Besov, Hardy, BMO)
- Domain stated for every result (T³ vs R³ vs bounded)
- Citations accurate (paper, authors, theorem/equation numbers)
- Every claim tagged: [VERIFIED], [COMPUTED], [CHECKED], or [CONJECTURED]
- Partial results valued — an incomplete dissection with 3 of 4 terms resolved is better than nothing
