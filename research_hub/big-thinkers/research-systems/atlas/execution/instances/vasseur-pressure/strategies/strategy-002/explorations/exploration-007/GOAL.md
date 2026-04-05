<!-- explorer-type: standard -->

# Exploration 007: Adversarial Review of the β = 4/3 Obstruction and Novel Claims

## Goal

Stress-test the comprehensive obstruction result accumulated across Strategy-002 explorations 001-005 and evaluate the novel claims for correctness, novelty, and publishability. This exploration is the devil's advocate.

## Background

Strategy-002 has produced a systematic negative result: β = 4/3 cannot be improved by standard analytical tools. Seven approaches were tried and all closed:

1. **Modified energy functional** (E001): 1/2 is definitional — immovable
2. **Improved Sobolev for div-free** (E001): H¹→L⁶ is sharp even for div-free
3. **Optimized truncation** (E001): truncation shape irrelevant to β
4. **Direct Chebyshev analytical** (E003): circular with the regularity problem; β = 1+s/n
5. **Direct Chebyshev computational** (E002): constant slack ~3-5×, k-independent, no U_{k-1}^{-δ}
6. **Commutator/compensated compactness** (E004): 3 independent obstructions (no div-curl, div-error dominates, CRW no gain)
7. **Frequency-localized LP** (E005): Bernstein penalty, CZ optimal freq-by-freq, spectral peak shifts to high j

### Novel claims to evaluate

**Claim 1: Universal formula β = 1 + s/n**
- For De Giorgi iteration on dissipative PDEs with H^s diffusion in n dimensions, the recurrence exponent is β = 1 + s/n.
- Evidence: Confirmed across 3D NS (s=1,n=3→4/3), 1D Burgers (s=1,n=1→2), 2D NS (s=1,n=2→3/2), SQG, MHD, fractional NS.
- Source: E003

**Claim 2: SQG-NS structural gap**
- SQG succeeds via commutator coupling, not by beating the Chebyshev/CZ chain.
- The gap has 3 dimensions: scalar vs vector (div-free preservation), linear vs quadratic coupling, first-order vs second-order cancellation.
- Source: E003, E004

**Claim 3: β = 4/3 sharp within energy+Sobolev+CZ+Chebyshev**
- An informal sharpness theorem: no technique using only these four ingredients can improve β.
- Source: E001 (sensitivity audit), E003-E005 (systematic closure of improvements)
- Note: This is informal — a rigorous version would require constructing an adversarial example.

**Claim 4: Div-free level-set open question**
- "Does div(u) = 0 improve the level-set distribution |{|u| > λ}|?" is genuinely open — no paper addresses it.
- Publishable as a question regardless of the answer.
- Source: E003

**Claim 5: Paraproduct transition**
- In the De Giorgi iteration, the resonance term R(u^below, u^above) dominates P^{21} at low k, while the paraproduct T_{u^below}u^above dominates at high k.
- Source: E005

## Specific Tasks

### Task 1: Literature search for published β improvements

Search systematically for any publication since Vasseur (2007) that claims to improve the De Giorgi recurrence exponent for 3D NS. Check:
- ArXiv searches: "De Giorgi" + "Navier-Stokes" + "partial regularity" post-2007
- Vasseur's own subsequent papers (Vasseur-Yang 2021 uses vorticity but same β)
- Choi-Vasseur (2017) alternative decomposition papers
- Any Chinese or Eastern European literature (NS regularity has active communities there)
- Tao's work on NS regularity
- Recent work by Albritton, Barker, Seregin, Kwon, or other NS regularity researchers

If ANY paper claims β > 4/3, report it with full citation and assess validity.

### Task 2: Attack the seven closure arguments

For each of the seven closed routes, try to find a weakness:

1. **Modified energy functional:** Is the 1/2 REALLY definitional? Could a non-standard functional (e.g., involving vorticity rather than velocity, or a nonlinear functional of U_k) give a different exponent?
2. **Improved Sobolev:** Is H¹→L⁶ sharp for div-free fields with ADDITIONAL NS structure (e.g., pressure equilibrium, energy decay)?
3. **Optimized truncation:** What about non-monotone or multi-scale truncations?
4. **Chebyshev circularity:** Is the β = 1+s/n formula EXACTLY correct or an approximation? Does it hold for s non-integer? Is there a loophole in the circularity argument?
5. **Chebyshev computational:** The DNS is smooth — could near-singular solutions have different distributional properties?
6. **Commutator:** Could a DIFFERENT commutator (not CRW-type) work? What about commutators with fractional derivatives?
7. **LP/Bernstein:** Could anisotropic LP (different in x₁,x₂,x₃) circumvent the isotropic Bernstein penalty?

### Task 3: Test combination attacks

Could any COMBINATION of the closed routes work? Specifically:
- Commutator + LP: E004 showed commutator works at low freq, E005 showed LP works at low k. Could a combined approach work at low k AND low freq?
- Modified functional + improved embedding: if the functional were changed, would different Sobolev exponents be relevant?
- Truncation + compensated compactness: could a different truncation (not amplitude-based) preserve more div-free structure?

### Task 4: Evaluate novel claims

For each of Claims 1-5:
1. **Correctness:** Is the claim mathematically correct? Any counterexamples?
2. **Novelty:** Has it been published before? Search specifically.
3. **Significance:** Would it be interesting to the NS/PDE community?
4. **Publishability:** Is there enough content for a paper (or a section of a paper)?
5. **Strongest counterargument:** What's the best objection?

### Task 5: Identify missing directions

Are there approaches to improving β that Strategy-002 hasn't considered? Specifically:
- Probabilistic methods (stochastic NS, Girsanov transform)
- Geometric methods (differential geometry of level sets)
- Microlocal analysis (beyond standard LP)
- Machine learning / computer-assisted proofs
- Approaches from other fields (turbulence theory, statistical mechanics)

## Success Criteria

1. Literature search covering ≥ 10 relevant post-2007 papers on De Giorgi for NS [REQUIRED]
2. At least one genuine weakness identified in the closure arguments (or an explicit statement that none were found after systematic search) [REQUIRED]
3. Assessment of ≥ 1 combination attack [REQUIRED]
4. Evaluation of all 5 novel claims with correctness/novelty/significance ratings [REQUIRED]
5. Identification of ≥ 2 unexplored directions [REQUIRED]

## Failure Criteria

- Rubber-stamping the existing results without genuine adversarial effort
- Missing obvious published improvements to β
- Not attempting combination attacks
- Vague assessments of novel claims without specific literature searches

## Key References

- Vasseur (2007): arXiv:0607017
- Vasseur-Yang (2021): vorticity De Giorgi
- Choi-Vasseur (2017): alternative decomposition
- Caffarelli-Vasseur (2010): SQG via De Giorgi
- Tao (various): NS regularity work
- Strategy-002 explorations 001-005 REPORT-SUMMARIES (summarized above)

## Notes

- **Be adversarial.** Your job is to find weaknesses, not to confirm. If you can't find any, that strengthens the result — but you must genuinely try.
- **Don't confuse "I can't think of a counterargument" with "no counterargument exists."** Search the literature actively.
- **For the novel claims:** The β = 1+s/n formula is the most likely to be either known or wrong. Check carefully whether this exact formula appears in Bahouri-Chemin-Danchin, in Vasseur's papers, or in the De Giorgi iteration literature for fractional diffusion.
- **Flag any claim where the "strongest counterargument" is strong enough to be fatal.** Better to identify a fatal flaw now than in peer review.
