# Exploration 003 Summary: Prior Art Search

## Goal
Determine whether the classicality budget R_δ ≤ S_max/S_T − 1 has been derived before, even under a different name.

## What Was Tried
Executed 25+ web searches across Google Scholar, arXiv, and general web. Examined 17+ papers. Checked all 8 named author groups (Zurek, Blume-Kohout, Riedel, Brandão/Piani/Horodecki, Korbicz, Bousso, Zwolak, and others including Tank, Hayden/Wang, Le/Olaya-Castro). Searched for direct term matches, cross-field combinations, and all identified conceptual neighbors (channel capacity, QEC bounds, broadcast channels, information bottleneck).

## Outcome: PARTIALLY KNOWN (Novel Synthesis)

**The structural form exists, but the physical content does not.** The bound R_δ ≤ (total environment capacity)/(per-fact entropy) is made explicit by Tank (2025, arXiv:2509.17775) as R_δ ≤ N·log₂(d_e)/((1−δ)·H_S), and was implicit in quantum Darwinism since Zurek (2009). What is **novel** is:

1. Connecting the abstract N·log₂(d_e) to the Bekenstein bound S_max = A/(4Gℏ)
2. The physical interpretation as a fundamental limit on classical reality from spacetime geometry
3. The conceptual framing as a budget/trade-off between richness and objectivity
4. All physical implications (black holes, labs, cosmology)
5. The bridging of two previously unconnected research communities

## Key Takeaway
After exhaustive search, **zero papers** were found that cite both quantum Darwinism and Bekenstein/holographic entropy bounds in connection with this question. The two communities — quantum Darwinism (Zurek school) and entropy bounds (Bousso/Bekenstein school) — have never intersected on this specific question. The classicality budget lives at precisely this gap. The formula is "trivially" obtainable by combining known results from both fields, but no one has done so because no one works in both. This is a genuine interdisciplinary insight.

## Leads Worth Pursuing
- Tank (2025) arXiv:2509.17775 should be cited as the closest structural precursor
- Hayden & Wang (2025) "What exactly does Bekenstein bound?" provides rigorous foundation for applying Bekenstein to information stored in a region — essential for the derivation
- The QD-encoding transition literature (2023-2024) may provide testable predictions where the budget becomes relevant
- Bousso's universal communication limit could provide an *alternative* derivation path via channel capacity rather than static entropy

## Unexpected Findings
The gap between these two research communities is strikingly clean — not a single cross-reference in 20+ years. This suggests the classicality budget has genuine novelty, but also that the derivation might face criticism as "merely combining existing results." The stress-testing phase should preemptively address this by showing the combination yields non-trivial physical predictions (e.g., near black holes).

## Computations Identified
- **Formal proof that N·log₂(d_e) ≤ S_max for physical environments:** This requires carefully applying the Bekenstein bound to the environment's Hilbert space in specific models. Difficulty: moderate (careful dimensional analysis and physics). Would definitively establish the classicality budget as a theorem rather than a conjecture.
- **Comparison with Bousso's channel capacity bound:** Compute whether the Bousso (2017) communication limit gives a tighter or looser constraint than Bekenstein when applied to environmental redundancy. Difficulty: moderate (need to map between static entropy and dynamic channel capacity).
