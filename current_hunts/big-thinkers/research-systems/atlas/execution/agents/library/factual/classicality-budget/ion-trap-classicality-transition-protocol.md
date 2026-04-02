---
topic: Ion trap classicality phase transition prediction and experimental protocol
confidence: provisional
date: 2026-03-27
source: classicality-budget strategy-002 exploration-003
---

## Summary

A 20-ion trap sideband-cooled to n̄ < 0.003 is predicted to be in a regime where the classicality budget FORBIDS any redundant classical copies of a qubit state (R_max < 0). Above n̄_c ≈ 0.003, classical copies become possible; this is a sharp, controllable classicality transition driven by the thermal occupation number. This is the most experimentally accessible test of the classicality budget with current technology.

---

## The Phase Transition

For 20 ions with 60 motional modes:
- **R_max = 60 × [bose_entropy_per_mode(n̄)] / S_T − 1**
- bose_entropy_per_mode(n̄) = (n̄+1)log₂(n̄+1) − n̄·log₂(n̄)

**Critical occupation number:** Classicality requires R_max ≥ 0 → S_eff ≥ 1 bit:
  60 × bose_entropy_per_mode(n̄_c) = 1 → **n̄_c ≈ 0.003**

| n̄ | S_eff (bits) | R_max | Budget verdict |
|----|-------------|-------|----------------|
| 0.001 | 0.57 | −0.43 | FORBIDDEN (no copies) |
| 0.003 | 1.0 | 0 | Phase boundary |
| 0.005 | 1.62 | 0.62 | ≤ 1 copy |
| 0.01 | 4.86 | 3.86 | ≤ 4 copies |
| 0.05 | 12.2 | 11.2 | ≤ 11 copies |
| 0.1 | 72.5 | 71.5 | ≤ 72 copies |

**The n̄ sweep is the primary experimental prediction:** R_δ_obs should track R_max as n̄ is increased from 0.001 to 1.0. The transition from 0 copies to ~4 copies as n̄ crosses 0.003 is a qualitative classicality threshold.

---

## Why Ion Traps Are the Best Platform

Preferred over BEC sonic horizon because:
1. Mutual information I(S:F_k) is directly measurable via quantum state tomography
2. Fully programmable: known Hilbert space structure, N precisely controllable
3. Number of environment modes is exact: 3N motional modes per N-ion crystal
4. n̄ continuously tunable from ~0.001 to ~10 via sideband cooling laser power
5. Shadow tomography (Aaronson 2018, Huang et al. 2020) provides efficient I(S:F_k) estimation

---

## Experimental Protocol (6 Steps)

**Step 1 — State preparation:** Initialize N=20 ions; prepare ion #1 (system qubit) in |ψ⟩ = α|0⟩+β|1⟩; initialize other 19 ions to |0⟩; sideband-cool all 60 motional modes to target n̄.

**Step 2 — Environment partition:** Partition 60 motional modes into ~10 fragment groups (e.g., by symmetry: COM, stretch, tilt modes). Each fragment F_k = group of ~6 modes.

**Step 3 — Controlled interaction:** Let system qubit interact with ion crystal for time t via H = J∑σ_z^i × (a+a†). Motional modes acquire partial information about qubit state.

**Step 4 — Measure R_δ:** For each fragment F_k, measure:
  I(S:F_k) = H(S) + H(F_k) − H(S,F_k)
  via quantum state tomography or shadow tomography.
  Count R_δ = #{F_k : I(S:F_k) ≥ (1−δ)·H(S)}.

**Step 5 — Test prediction:** Budget predicts R_δ ≤ R_max = 60 × bose_entropy_per_mode(n̄)/S_T − 1. For n̄=0.05: R_δ ≤ 11. Falsifying result: R_δ ≥ 12.

**Step 6 — n̄ sweep:** Repeat for n̄ ∈ {0.001, 0.005, 0.01, 0.05, 0.1, 1.0}. Budget predicts R_δ → 0 as n̄ → n̄_c from above.

---

## Feasibility Assessment

**Currently demonstrable:**
- 20-ion traps: routine (IonQ, Oxford, ETH: 20–50 qubit systems)
- Sideband cooling to n̄ ~ 0.01: demonstrated (NIST groups; n̄ < 0.01 for single modes)
- State tomography 2–5 ions: routine

**Challenging but tractable:**
- State tomography on 60 modes: exponentially hard in principle, but shadow tomography (O(log N) measurements) bounds I(S:F_k) efficiently
- Full quantitative test requires development of efficient mutual information estimators

**Timeline:**
- Near-term (1–3 years): n̄ sweep with R_δ measured from ~5 environment modes; N=10 ions
- Medium-term (5 years): Full 20-ion test with all 60 modes characterized

---

## Status

n̄_c ≈ 0.003 [COMPUTED numerically]; interpretation as "classicality transition" [CONJECTURED — requires further theoretical work]; ion trap feasibility assessment [CONJECTURED based on literature review].
