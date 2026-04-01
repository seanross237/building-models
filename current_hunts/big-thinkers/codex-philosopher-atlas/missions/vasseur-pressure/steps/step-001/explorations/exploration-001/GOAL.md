# Exploration 001: Orientation and Landscape Verification

## Goal

Verify that the premises of the Vasseur pressure exponent mission are current and that the H^1/De Giorgi route has not been explored before.

## Specific Tasks

### Task 1: Confirm beta = 4/3 is still the best known pressure exponent

Search for the current state of the art in the De Giorgi approach to Navier-Stokes regularity, specifically regarding the pressure integrability exponent.

- **Vasseur (2007)** "A new proof of partial regularity of solutions to Navier-Stokes equations" — introduced the De Giorgi approach. Confirm this uses beta = 4/3.
- **Caffarelli-Vasseur (2010)** "Drift diffusion equations with fractional diffusion and the quasi-geostrophic equation" — the drift-diffusion comparison case (no pressure). Confirm this reaches criticality.
- Check Vasseur's publications from 2014-2026 for any improvements to the pressure exponent.
- Search for any citing papers that improve the 4/3 exponent. Key search: "De Giorgi" + "Navier-Stokes" + "pressure" + "regularity".

### Task 2: Search for prior H^1 + De Giorgi work

Has anyone combined compensated compactness / Hardy space H^1 estimates for the pressure with a De Giorgi iteration scheme?

Key search terms:
- "compensated compactness" + "De Giorgi" + "Navier-Stokes"
- "Hardy space" + "pressure" + "De Giorgi" + "Navier-Stokes"
- "H^1" + "pressure" + "regularity" + "iteration"
- "div-curl lemma" + "De Giorgi" + "Navier-Stokes"

Also check: Coifman-Lions-Meyer-Semmes (1993) citing papers that mention De Giorgi or regularity iteration.

### Task 3: Check Tran-Yu relevance

Tran-Yu (2014) paper in Annales de l'IHP. Does it:
- Address the pressure exponent in the De Giorgi framework?
- Or address a different aspect (e.g., different scaling, epsilon-regularity, partial regularity)?

Clarify what their contribution is and whether it's relevant to the beta = 4/3 question.

### Task 4: Verify the 3/2 threshold

The claim is that De Giorgi regularity for NS requires the pressure to be in L^{beta} with beta > 3/2.

- Where does 3/2 come from? Trace the scaling argument.
- Is 3/2 the threshold for full regularity (L^infinity bound on u), or for a weaker result (partial regularity, epsilon-regularity)?
- Is 3/2 tight (meaning beta = 3/2 exactly fails), or is there slack?

## Success Criteria

- Confirmed or corrected: beta = 4/3 is current best (with citation)
- Confirmed or corrected: beta > 3/2 is the threshold for full regularity (with derivation)
- Literature search for H^1 + De Giorgi yields either: (a) nothing found (green light), or (b) specific papers to examine
- Tran-Yu relevance clarified

## Failure Criteria

- Unable to find Vasseur (2007) or determine current state of art
- Contradictory information with no resolution

## Kill Conditions (report immediately if triggered)

- (A) Someone pushed past beta = 4/3 using ANY method. Report who, how, what exponent they achieved.
- (B) H^1 + De Giorgi combination already tried and failure documented. Report the obstruction.
- (C) beta = 4/3 proven sharp for ALL decompositions. Report the sharpness result.

## Output Format

Write a structured report with:
1. **State of the art summary** (1 paragraph)
2. **Paper-by-paper findings** (for each relevant paper: authors, year, venue, one-sentence contribution, relevance to our mission)
3. **Kill condition assessment** (for each of A/B/C: triggered? evidence?)
4. **Verdict** on mission premises (confirmed/corrected/uncertain)
5. **Implications for next steps**
