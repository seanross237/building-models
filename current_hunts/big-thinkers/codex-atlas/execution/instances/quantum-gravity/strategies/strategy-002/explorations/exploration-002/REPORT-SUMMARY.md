# Exploration 002 Summary: Bianconi's Entropic Action Quantum Gravity

## Goal
Critically assess Bianconi's 2025 "Gravity from entropy" paper (Phys. Rev. D 111, 066001), which claims to derive gravity from the quantum relative entropy between spacetime's metric and the metric induced by matter fields.

## What Was Done
- Found and reconstructed the full mathematical proposal from the original paper and 4 follow-up papers
- Compared to Jacobson, Verlinde, Padmanabhan, and Sakharov programs
- Ran Tier 1 structural sanity checks (graviton DoF, unitarity, ghosts, UV completion, diffeo invariance, Weinberg-Witten)
- Assessed predictive claims (cosmological constant, G-field dark matter, inflation, BH entropy)

## Outcome: FAILS — Not a Viable Quantum Gravity Theory

**The proposal fails Tier 1 validation on multiple counts:**
1. **Not quantum at all.** The theory is entirely classical — no Hilbert space, no quantization, no quantum corrections. The author explicitly defers quantization to future work.
2. **Probable ghost problem.** The full equations of motion are fourth-order in the metric (via the B^μν tensor), triggering Ostrogradsky instability concerns. No ghost analysis is performed.
3. **No UV completion.** Despite press claims, this is a classical modified gravity theory, not a quantum gravity theory.
4. **Phenomenological construction.** The induced metric G̃ is designed by hand to reproduce GR at low coupling, undermining the "gravity emerges from entropy" narrative.

**Novelty assessment:** The specific idea (action = quantum relative entropy between two metrics) IS genuinely novel. But the output is a classical modified gravity theory that reduces to GR by construction.

**Inflationary predictions (from follow-up paper 2509.23987):** n_s ∈ [0.962, 0.964], r ∈ [0.010, 0.012] — within current bounds and potentially testable by CMB-S4. However, these come from unquantized modified Friedmann equations in the high-coupling regime where ghost stability is unverified.

## Key Takeaway
**Bianconi's work is a creative information-theoretic reformulation of classical gravity by a network scientist, not a quantum gravity theory.** It cannot compete with QG+F or other properly quantized approaches. The entire entropic gravity program (Jacobson, Verlinde, Padmanabhan, Bianconi) shares the same fundamental weakness: it derives classical Einstein equations from thermodynamic/information arguments but never provides UV completion.

**Recommendation: Move on.** Do not pursue this approach further. The information-theoretic framing (action = relative entropy) is an interesting idea worth remembering if it could be implemented within an actually quantized framework, but Bianconi's specific realization is not viable.

## Leads Worth Pursuing
- The inflation predictions (n_s, r) are worth tracking against CMB-S4 data, though many theories predict similar values
- The idea that gravitational action measures information divergence between geometry and matter could be explored within asymptotic safety or path-integral frameworks that ARE properly quantized
- The lesson: any serious information-theoretic approach to QG must address ghosts, unitarity, and UV completion from the start — not defer them
