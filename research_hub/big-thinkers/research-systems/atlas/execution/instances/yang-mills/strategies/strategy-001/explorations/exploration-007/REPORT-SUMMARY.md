# Exploration 007 Summary: Novelty Search for Finite Group Convergence Results

## Goal
Determine whether the computational results from exploration 005 (finite subgroup approximation of SU(2) lattice gauge theory) are novel or already known. Specifically, assess four claims: (1) convergence rates |obs_G - obs_SU(2)| ~ |G|^{-α}, (2) β_c ~ |G|^{0.6} scaling, (3) hysteresis weakening 0.39→0.18→0.09, (4) <0.5% icosahedral accuracy.

## What Was Tried
- Comprehensive literature search across web databases, INSPIRE, arXiv
- Full text obtained for the key 2022 paper (Hartung et al., arXiv:2201.09625) with definitive β_c table
- Cross-checked β_c ~ |G|^{0.6} claim by fitting published data
- Searched specifically for convergence rate measurements, hysteresis jump sizes, and quantitative accuracy bounds

## Outcome: SUCCEEDED — Clear novelty assessment achieved

## Key Findings

### Prior Art Summary (5+ relevant papers identified)

1. **Petcher & Weingarten (1980)**, *Phys. Rev. D* **22**, 2465 — FOUNDATIONAL. Studied exactly T̄, Ō, Ī subgroups; found first-order transitions for all three; found icosahedral "agrees with SU(2) over wide coupling range." BUT: no power-law fits, no percent accuracy bounds, no hysteresis magnitudes.

2. **Hartung, Jakobs et al. (2022)**, *Eur. Phys. J. C* **82**, 237; arXiv:2201.09625 — COMPREHENSIVE MODERN STUDY. Tabulates exact β_c values: 2T→2.15(15), 2O→3.20(10), 2I→5.70(20). States these reproduce Petcher-Weingarten values. Provides analytic formula β_c(N) = ln(1+√2)/(1-cos(2π/N)) based on cyclic order N. Does NOT fit power law in group order |G|; does NOT measure hysteresis jump magnitudes; does NOT measure observable convergence rates.

3. **Jakobs et al. (2025)**, arXiv:2503.03397 — Hamiltonian formalism, finds N^{-0.88} convergence for partitionings. Different formalism (not Euclidean subgroup approach).

4. **Adhikari-Cao (2022/2024)**, arXiv:2202.10375 — Proves mass gap for finite gauge groups; threshold β ≥ (114 + 4log|G|)/Δ_G. Does not discuss |G|→∞ limit. Spectral gap Δ_G for binary polyhedral groups not computed.

5. **Stack (1983)**, *Phys. Rev. D* **27**, 412 — Used icosahedral approximation for heavy quark potential as practical substitute for SU(2). Confirming qualitative adequacy.

6. **Quantum gate papers (2022-2024)** — Binary tetrahedral, octahedral studied for quantum simulation; qualitative BT < BO < BI hierarchy confirmed but no convergence rates.

### Novelty Assessment

| Finding | Status | Details |
|---------|--------|---------|
| Convergence rates α ~ |G|^{-α} (α = 0.7–2.5) | **APPEARS NOVEL** | No prior paper measured power-law convergence of Euclidean LGT observables vs group order |
| β_c ~ \|G\|^{0.6} scaling | **PARTIALLY KNOWN** | β_c values known since 1980. Power-law fit is consistent with published data (exponent 0.589 from our fit) but never stated. Prior analytic formula uses cyclic order N, not group order |G|. |
| Hysteresis Δ⟨P⟩ = 0.39→0.18→0.09 | **APPEARS NOVEL** | Hartung (2022) measures β_c via hysteresis but never tabulates jump magnitudes |
| <0.5% icosahedral accuracy | **PARTIALLY KNOWN** | Qualitatively known since 1980. Specific 0.5% bound for all observables simultaneously is new |

## Key Takeaway

**The phase transition structure and qualitative convergence of binary icosahedral → SU(2) have been known since 1980.** However, two genuinely new quantitative contributions stand out: (1) the systematic measurement of convergence rates α ≈ 0.7–2.5 as power laws in group order for Euclidean lattice observables, and (2) the hysteresis jump size measurements. These fill a real gap — practitioners have used the icosahedral approximation since 1983 (Stack) but never formally quantified the errors.

The β_c ~ |G|^{0.6} description is a new parameterization of known data, derivable from Petcher-Weingarten/Hartung values, but no prior paper states it this way. The established analytic formula is β_c(N) based on cyclic order, giving a more precise description.

## Leads Worth Pursuing

- The Adhikari-Cao threshold for 2I is β ≥ ~133/Δ_I; if Δ_I is small, this could be MUCH larger than β_c = 5.7, meaning the Adhikari-Cao bounds are vacuous in the physical range
- Computing Δ_G for the binary polyhedral groups would quantify the fourth obstruction to extending Adhikari-Cao to SU(2)
- A systematic paper measuring convergence rates across observables + comparing to the Fibonacci spiral construction from Hartung (2022) would be publishable

## Unexpected Findings

- The 2022 Hartung paper has an **analytic formula** β_c(N) that our β_c ~ |G|^{0.6} is just a cruder version of. The formula shows the true dependence is on cyclic order N (which scales ~log|G|), not a simple power of group order. Our power-law description is numerically accurate (exponent 0.589) but lacks the physical interpretation.
- The binary icosahedral β_c = 5.70(20) from Hartung (2022) matches our measured ≈5.8 closely, confirming our simulation was correct.
- The quantum computing community (2022-2025) has extensively characterized the BT and BO groups but never systematically measured convergence rates — our work would be directly relevant to quantum error budgets.

## Computations Identified

1. **Spectral gap Δ_G for binary polyhedral groups** (easy, ~20 lines): Compute the second-largest eigenvalue of the normalized adjacency matrix of the Cayley graph on {T̄, Ō, Ī} with generators being the neighbors of identity. This directly enters the Adhikari-Cao bound and tells us whether their mass gap applies in the physical β range (below β_c).

2. **Convergence rate survey with larger lattices** (medium, ~200 lines): Repeat the exploration 005 measurements on 6⁴ lattices to check finite-volume corrections, and extend to compute explicit α exponents for each observable with error bars. This would be the core of a publishable paper.
