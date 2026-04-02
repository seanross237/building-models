# Exploration 001: QD↔HQEC — Exhaustive Literature Search and Formal Mapping

## Mission Context

We are investigating whether the "classicality budget" — an upper bound on quantum Darwinism (QD) redundancy derived from holographic entropy bounds — is a novel contribution. Strategy-001 found a potentially major result: quantum Darwinism and holographic quantum error correction (HQEC) appear to be the same phenomenon viewed from different frameworks, with zero prior cross-citations between the two communities. This is currently the STRONGEST novel claim from the entire mission.

**Your job:** Verify this claim with exhaustive literature research, formalize the mapping mathematically, identify where it breaks, and deliver a definitive novelty verdict.

## Background: What Strategy-001 Found

The following dictionary was constructed in Exploration 007 of strategy-001:

| QD Concept | Holographic Translation | Prior status |
|------------|------------------------|--------------|
| System S | Bulk operator φ(x) at bulk point x | CONJECTURED |
| System entropy H_S = S_T | log₂(dim H_x), local bulk Hilbert space | CONJECTURED |
| Environment E | Boundary CFT Hilbert space H_CFT | Sourced (standard holography) |
| Fragment F_k | Boundary subregion R_k | CONJECTURED |
| "Fragment knows S" (I(S:F_k) ≥ (1−δ)H_S) | x ∈ W(R_k) (x in entanglement wedge of R_k) | Sourced (HQEC theorem) |
| Fragment entropy S(F_k) | S(R_k) = Area(γ_{R_k})/(4G_N) [RT formula] | Sourced (RT 2006) |
| Total environment entropy S_max | S(full boundary) ≈ log₂(dim H_CFT) | Sourced (holographic bound) |
| Redundancy R_δ | # disjoint boundary regions R_k with x ∈ W(R_k) | CONJECTURED |
| Classical fact | Bulk operator in multiple entanglement wedges | CONJECTURED |

The HaPPY code (Pastawski-Yoshida-Harlow-Preskill 2015, arXiv:1503.06237) achieves exactly 50% of the holographic classicality budget — which strategy-001 interpreted as HaPPY implementing quantum Darwinism in holographic language without using that terminology.

The structural formula is: **R_δ ≤ S_max/S_T** — derived holographically from boundary tensor product + HQEC + holographic entropy bound.

Previous literature search (strategy-001, exploration-007): 7 keyword queries, zero papers found connecting Zurek's R_δ to HQEC/RT formula. But 7 queries is NOT exhaustive. The mission explicitly requires checking specific papers.

## Your Goal

Do an exhaustive literature search to answer: **Has anyone published the QD↔HQEC connection before? And is the formal mapping correct?**

### Part 1: Exhaustive Literature Search

**CHECK EVERY ONE of these specific papers/groups:**

**QD (Quantum Darwinism) side:**
1. Zurek, W. H. (2003, 2009, 2022) — any mention of AdS/CFT, holography, error correction, or entanglement wedges
2. Riedel, J. F., Zurek, W. H., Zwolak, M. (2010, 2012, 2016) — same
3. Brandão, F. G. S. L., Piani, M., Horodecki, P. (2015, arXiv:1310.8999) — "Generic emergence of classical features in quantum Darwinism" — read for any connection to holography or QEC
4. Korbicz, J. K. and collaborators (2014, 2021) — spectrum broadcast structures (SBS) — check for any holographic context
5. Tank, C. (2025, arXiv:2509.17775) — check the full paper for any holographic or error-correction connections
6. Blume-Kohout, R. & Zurek, W. H. (2005, 2006) — check for holographic connections
7. Knott, P. A. et al. (2018, Physical Review Letters) — "Generic emergence of objectivity" — check for holographic connections

**HQEC (Holographic Quantum Error Correction) side:**
8. Almheiri, A., Dong, X., Harlow, D. (2015, arXiv:1411.7041) "Bulk locality and quantum error correction in AdS/CFT" — read the full paper, especially the characterization of when a boundary region can reconstruct a bulk operator. Does it ever mention decoherence, classicality, or environmental witnessing?
9. Pastawski, F., Yoshida, B., Harlow, D., Preskill, J. (2015, arXiv:1503.06237) "HaPPY code" — read for any mention of quantum Darwinism, redundancy, environmental witnesses, or classicality
10. Hayden, P., Penington, G. (2018, arXiv:1811.09895) "Learning the alpha-bits of black holes" — check for any QD connection
11. Cotler, J., Hayden, P., Penington, G., Salton, G., Swingle, B., Walter, M. (2019, arXiv:1905.04306) "Entanglement wedge reconstruction via universal recovery channels" — check for QD connection
12. Harlow, D. (2017, arXiv:1607.03901) "Jerusalem lectures on black holes and quantum information" — look for any discussion of environmental redundancy or quantum Darwinism
13. Qi, X.-L. (2018, arXiv:1801.09666) "Emergent quantum mechanics from holographic spacetime" — check whether this connection is mentioned
14. Verlinde, E. and collaborators on emergent spacetime — any mention of classicality or QD

**Explicit search queries you MUST run (using web search):**
- "quantum Darwinism holographic"
- "quantum Darwinism AdS/CFT"
- "quantum Darwinism entanglement wedge"
- "Zurek redundancy Ryu-Takayanagi"
- "quantum Darwinism error correction"
- "quantum objectivity holographic"
- "classicality budget holographic"
- "broadcast structure entanglement wedge"
- "spectrum broadcast holographic"
- "Zurek entanglement wedge"
- "environmental decoherence AdS/CFT"
- "QD HQEC"
- "quantum Darwinism black hole"
- "classicality AdS/CFT"
- "redundancy holographic quantum error correction"

**For each search:** note how many results appear, and quote any abstracts that look possibly relevant.

### Part 2: Formalize the Mapping

Produce a rigorous mathematical dictionary — not just words. For each pair in the translation table above:
- State the PRECISE holographic definition (with equations from the cited papers)
- State the PRECISE QD definition (with equations from Zurek/Riedel)
- Assess whether the identification is exact, approximate, or metaphorical

In particular, for the CONJECTURED entries:
- **S_T identification**: What IS the "local bulk Hilbert space dimension" dim(H_x)? Does such a thing exist rigorously? What does it depend on? Does it equal H_S = von Neumann entropy of the system?
- **Pointer states**: QD requires a preferred pointer basis (the einselected states). What is the holographic analogue? Does classical bulk geometry play the same role? Where precisely does this break?
- **Redundancy R_δ**: In HQEC, one counts the number of disjoint boundary subregions R_k such that x ∈ W(R_k). In QD, R_δ counts fragments with I(S:F_k) ≥ (1−δ)H_S. Show formally that these are equivalent given the QD↔HQEC identification.

### Part 3: Where the Mapping Breaks

Identify at least 3 places where the QD↔HQEC mapping is approximate, inapplicable, or strained:
1. What is the analogue of "pointer states" in holography? Does the need for a classical bulk geometry (semiclassical limit) map to the need for a preferred basis?
2. What happens to the mapping at the Planck scale (where neither bulk tensor product nor semiclassical geometry holds)?
3. What is the analogue of the "δ-distinguishability" condition in QD? Is there a precise holographic analogue?
4. Does the mapping require a specific vacuum state (the AdS vacuum)? What happens for excited states?

### Part 4: Novelty Verdict

Deliver a final verdict:
- **HIGH confidence novelty**: No paper found; the mapping is formally demonstrable and not in any existing work
- **MEDIUM confidence novelty**: No paper found, but the connection may be "well-known" to experts in both communities (folklore); or the mapping has gaps that weaken it
- **LOW confidence novelty**: Found papers that are adjacent/suggestive; or mapping is too imprecise to claim

Include: (a) list of all papers and searches that came up empty; (b) any papers that are ADJACENT (not the connection itself but in the neighborhood); (c) your honest assessment of whether this is the kind of thing that "experts already know" even if not published.

## Success Criteria

**SUCCESS:** Delivers a HIGH or MEDIUM novelty verdict with: (1) a complete list of all papers searched with their verdict, (2) a formal mathematical dictionary for at least 5 QD↔HQEC mappings, (3) at least 3 identified gaps or failure modes of the mapping.

**FAILURE:** Returns "I searched but couldn't find anything" without a documented search list; or fails to formalize any mappings.

## Output

Write your report to: `explorations/exploration-001/REPORT.md` (relative to this strategy directory: `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/classicality-budget/strategies/strategy-002/`)

Then write a concise summary (max 400 words) to: `explorations/exploration-001/REPORT-SUMMARY.md`

Write the report incrementally — complete each section and write it to the file before moving on to the next. Do NOT compose the entire report in memory and write it all at once.

## Strategy Directory

`/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/classicality-budget/strategies/strategy-002/`
