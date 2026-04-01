# Chain History — Vasseur Pressure Mission

## Planning Loop Run 1 — 2026-03-30

### Planner Output

4 chains produced:

- **Chain 1: Tran-Yu Verification and Extension** — Literature survey of Vasseur's program post-2014, audit of Tran-Yu techniques, extract Galilean boost mechanism in pressure estimates, produce 2-page improvement proposal.
- **Chain 2: Divergence-Free Pressure Improvement via H^1 Structure** — Exploit compensated compactness (p in H^1) within De Giorgi iteration. Three routes: interpolation, H^1-BMO duality, atomic decomposition.
- **Chain 3: DNS Numerical Exploration** — (Eliminated by selector as duplicating Atlas's parallel mission.)
- **Chain 4: The 3/2 Threshold — Structural Origin and Sharpness** — Ask the meta-question: is beta = 4/3 sharp? Compare pressure-free drift-diffusion (Caffarelli-Vasseur 2010) term-by-term with full NS. Fractional NS continuity test.

### Selector Decision

Selected **Chains 1, 2, and 4** for adversarial review. Chain 3 eliminated for Atlas overlap.

### Attacker Critiques (Key Points)

**Chain 1:**
- Solid floor but low ceiling — mostly literature survey
- Tran-Yu relevance is assumed, not verified
- "Produce 2-page proposal" is too vague for a concrete deliverable

**Chain 2:**
- CRITICAL: Compensated compactness gives p in H^1, NOT a better L^p exponent. H^1 subset L^1 subset L^{4/3}. The original chain confused H^1 with improved integrability.
- The reframed question is whether H^1 structure (cancellation, duality with BMO) can be converted into De Giorgi-compatible estimates
- H^1-BMO duality is the most promising route — but requires De Giorgi test functions to be BMO-bounded
- Bogovskii corrector growth rate is a concrete computation that could kill the approach early

**Chain 4:**
- Most likely outcome is "suggestive but inconclusive" (55%)
- Fractional NS continuity test is really a numerical experiment, overlaps with Atlas
- The Caffarelli-Vasseur comparison is genuinely useful but should be a step within another chain, not a standalone mission

### Judge Verdict: SELECT CHAIN 2, MODIFY, INCORPORATE ELEMENTS FROM 1 AND 4

**Probability assessments:**
- Chain 1: 85-90% presentable (but ceiling is "literature survey")
- Chain 2: 55-65% presentable (15-20% positive result)
- Chain 4: 65% presentable (55% "suggestive but inconclusive")

**Key modifications:**
- Chain 1's Step 0 (orientation/verification) prepended to Chain 2
- Chain 4's pressure dissection (Caffarelli-Vasseur comparison) added as Step 1
- H^1-BMO duality elevated to primary branch; interpolation and atomic decomposition as alternatives
- Three explicit kill conditions at Step 0
- Negative findings explicitly valued and structured

### Final Decider Selection: CHAIN 2 (with elements from Chains 1 and 4)

**Reasoning:**
1. **Complementarity:** Atlas runs DNS numerics. Chain 2 is purely analytical — zero overlap.
2. **Ceiling:** Only chain with nonzero probability of actual mathematical progress on a Millennium Problem.
3. **Floor:** Raised by incorporated elements — Step 0 (landscape) and Step 1 (dissection) produce useful output regardless. Three-branch failure at Step 2 documents specific obstruction mechanisms.
4. **Executability:** After the H^1/L^p reframing, each branch has concrete computations with explicit success/failure criteria.
5. **Architecture learning:** Most computation-heavy chain, correcting prior mission's over-correction away from computation.

### Refined Chain

See `CHAIN.md` for the refined 5-step chain (Steps 0-4).
