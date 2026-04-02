# Exploration 005 Summary: Weitzenböck R(Q) Sign Analysis

**Mission:** Yang-Mills mass gap (strategy-003)
**Date:** 2026-03-28

## Goal
Extract the Weitzenböck decomposition M(Q) = M(I) + R(Q) from Jiang (2022) (arXiv:2211.17195) and SZZ (arXiv:2204.12737). Determine whether R(Q) ≼ 0 is provable.

## What Was Tried

1. **Literature search:** Found Jiang (2022) and read SZZ Section 4. Checked all related "discrete Weitzenböck" papers.
2. **Computation:** Full eigenspectrum of R(Q) = M(Q) − M(I) on L=2, d=4, SU(2) lattice (192 DOFs) for 20 configurations (random, perturbed, single-link).
3. **Top eigenspace restriction:** Projected R(Q) onto the 9-dimensional top eigenspace P of M(I) (eigenvalue 4d = 16).
4. **Single-link worked example:** Computed R(Q) for Q = exp(ε τ₁) on one link, ε ∈ {0, 0.1, 0.5, 1.0, π/2, π}.

## Outcome: PARTIAL SUCCESS — Key Structural Clarification

### Critical Correction to GOAL.MD Framing

**The full operator ordering M(Q) ≼ M(I) is FALSE for all Q ≠ I.** R(Q) = M(Q) − M(I) always has BOTH positive and negative eigenvalues. M(Q) ≼ M(I) as operators was 0/20 tested. The GOAL.MD statement "M(Q) ≼ M(I) confirmed numerically (E004)" was incorrect — E004 only tested λ_max(M(Q)) ≤ 4d (spectral radius), NOT the full operator ordering.

### The Correct Statement (Confirmed)

What IS true and numerically confirmed (20/20):
**R(Q) restricted to the top eigenspace P of M(I) is negative semidefinite (NSD).**

This is equivalent to λ_max(M(Q)) ≤ λ_max(M(I)) = 4d, which is the ACTUAL target inequality. Since M(I) has a spectral gap (2nd eigenvalue = 14 < 16), the P-restriction suffices.

Key data points:
- Random Q: max eigenvalue of R(Q)|_P ≈ −14 (deeply negative, never close to 0)
- Single-link ε=0.5: max R(Q)|_P = −0.016 (negative even for small excitations)
- Single-link ε=π: max R(Q)|_P = −0.342 (stays negative even at maximal excitation)

## Key Takeaway

**No paper proves R(Q)|_P ≼ 0.** The M(Q) = M(I) + R(Q) framework and the observation that the restriction to the staggered eigenspace is NSD are **original to this research program.**

Jiang (2022) proves ∆_A = B_A + Ric + F (Weitzenböck for graph connection Laplacians) with F = holonomy defect, but:
- Does NOT prove F ≼ 0
- Does NOT specialize to Yang-Mills Hessian
- The correspondence to our M(Q) is indirect (Jiang acts on k-forms on general graphs)

SZZ bounds |HessS| ≤ 8(d-1)Nβ|v|² by triangle inequality. The decomposition M(Q) = M(I) + R(Q) is COMPLETELY ABSENT from SZZ. The entire atlas approach of exploiting the spectral gap at 4d is not in SZZ.

## Unexpected Findings

1. **The full operator ordering M(Q) ≼ M(I) is FALSE** — prior explorations conflated "λ_max ≤ 4d" with full operator ordering. These are genuinely different. This is important: the target is weaker (spectral radius) than what was claimed.

2. **R(Q) has LARGE positive eigenvalues for random Q** (up to +6), but these are in sub-maximal eigenspaces. The gauge field redistributes spectral weight — decreasing the top eigenvalue while increasing some lower ones.

3. **The cos(ε/2) suppression** (not cos(ε)): For single-link excitation, Re Tr(U_P) = 2 cos(ε/2), not 2 cos(ε). This is the correct factor from the holonomy structure.

## Proof Gap

The remaining mathematical problem is:
```
Prove: v^T [M(Q) − M(I)] v ≤ 0 for all v ∈ P (staggered eigenspace) and all Q ∈ SU(2)^E
```

This requires:
1. Specializing Jiang's F formula to the hypercubic lattice with SU(2) = SO(3) in adjoint representation
2. Showing that ∑_□ ⟨v, [Ad(G_□) − I] v⟩ ≤ 0 for staggered modes v
3. This is a sum of rotation terms: Ad(G_□) ∈ SO(3) → ⟨v, Ad(G_□)v⟩ ≤ ⟨v, v⟩ = |v|² for all v... BUT the sign of the sum (which mixes adjacent contributions) needs more care

The bound has enormous numerical slack (margin ≈ 14 for random Q) suggesting a natural proof exists.

## Computations Identified

1. **Jiang F formula for our specific plaquette structure** (medium, 30-line algebra): Write F(i,j,k) for the standard Wilson plaquette with SU(2) = SO(3). Show ⟨v_stag, F v_stag⟩ ≤ 0 for the staggered mode. Requires working out the SU(2) representation theory for the holonomy terms.

2. **Verify R(Q)|_P ≼ 0 at L=4** (easy, existing code): Run the same eigensystem computation on L=4 (1024 links, 3072 DOFs). Requires full diagonalization of 3072×3072 matrix — about 30 seconds. Inputs: code from E004 + R(Q) computation added.

3. **Measure the spectral gap of R(Q)|_P** (easy): Compute min eigenvalue of R(Q)|_P as a function of |F_□|² (plaquette curvature magnitude). If min R(Q)|_P ≈ −c × ∑_□ |F_□|², this gives the precise Weitzenböck formula analogous to Ric ≥ −c × |Rm|² in differential geometry.

DONE
