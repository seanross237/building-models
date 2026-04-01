---
topic: Zurek spin models saturate the classicality budget; novelty assessment
confidence: verified
date: 2026-03-27
source: "classicality-budget strategy-001 exploration-001"
---

## Result

Zurek's standard spin-environment models (1 system qubit + N environment qubits) produce R_delta ~ N, which exactly saturates the classicality budget bound R_0 <= N. The bound is tight for this class of models.

## Saturation Proof

For 1 qubit system + N environment qubits:
- S_max = N + 1 bits (total Hilbert space is (N+1) qubits)
- H_S = 1 bit
- S_T = 1 bit (for delta = 0)
- R_0 <= S_max/S_T - 1 = (N+1)/1 - 1 = N

Zurek's dynamical models give R ~ N. Our bound gives R <= N. The bound is saturated.

## Novelty Assessment — PARTIALLY KNOWN (Novel Synthesis)

**Refined by prior art search (exploration-003).** See `prior-art-literature-search.md` for comprehensive details.

The **structural form** of the bound (redundancy <= total capacity / per-fact entropy) exists: explicit in Tank (2025) as R_delta <= N * log_2(d_e) / ((1 - delta) * H_S), and implicit in QD since Zurek (2009) as R ~ N/f. The **physical content** (connecting to the Bekenstein bound on a spatial region) is novel. Zero papers connect QD redundancy to Bekenstein/holographic entropy bounds (29 searches, 17 papers, 8 author groups checked).

### Known components (not novel):
- Quantum Darwinism and R_delta definition (Zurek 2003, 2009)
- Bekenstein bound (Bekenstein 1981)
- Holevo bound (Holevo 1973)
- R ~ N in spin models (Zurek, Blume-Kohout, Zwolak)
- Brandao-Piani-Horodecki generic emergence of objectivity (2015)
- **The structural form** R_delta <= capacity / per-fact-entropy (Tank 2025, arXiv:2509.17775)

### Novel in this work:
- **The Bekenstein connection** — identifying that N * log_2(d_e) is physically bounded above by S_max = A/(4Ghbar)
- **The universal, model-independent upper bound** with physical (not just Hilbert space) grounding
- **The multi-fact trade-off** M * (1 + R) <= S_max/S_T (the "budget hyperbola")
- **The physical interpretation** that classical reality has a finite budget with an explicit richness-objectivity trade-off
- **The observation** that Zurek's spin-model results saturate this bound
- **Bridging two disconnected communities** — QD and entropy bounds have zero cross-citations on this question

### What it is NOT:
- Not just the Bekenstein bound restated (it specifically connects to QD redundancy and adds trade-off structure)
- Not just quantum Darwinism restated (QD alone does not bound R_delta — the bound comes from combining QD with entropy bounds)
- Not just Tank's bound restated (Tank uses abstract Hilbert space capacity; the classicality budget uses physical spacetime-geometric capacity)

## Comparison with Brandao et al. (2015)

Brandao-Piani-Horodecki proved quantum Darwinism is generic: objectivity EMERGES for any quantum dynamics. But they do not bound TOTAL information capacity or relate redundancy to an entropy bound on the region. The classicality budget ADDS the constraint that the region has finite capacity, limiting how much objectivity can coexist with how many facts.

## Verdict

The classicality budget inequality is **not present** in Zurek's work or the broader quantum Darwinism literature as a Bekenstein-bounded physical limit. The structural form exists in Tank (2025) with abstract capacity; the novelty lies in connecting quantum Darwinism's information requirements to gravitational/holographic entropy bounds to obtain a physical constraint on classical reality. Verdict: **PARTIALLY KNOWN (Novel Synthesis).**
