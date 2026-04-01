# Exploration Set — 22 Questions for Architecture Testing

These are questions where Sonnet baseline fails. Categorized by failure mode to predict which architecture components should help.

## Failure Mode Taxonomy

- **K = Knowledge Gap**: Model lacks specific domain expertise. Architecture won't help without retrieval.
- **R = Reasoning Error**: Model has knowledge but applies it incorrectly. Planning/critics may help.
- **C = Computation Error**: Model sets up correctly but makes arithmetic/algebraic mistakes. Verification may help.
- **D = Discrimination Error**: Model can't distinguish between plausible options. Adversarial elimination (D2) may help.
- **S = Systematic Error**: Model has principled but wrong understanding. No single-model architecture helps.

## Hard Set (13 questions — both Sonnet and Opus fail)

| ID | Question | Failure Mode | Why Both Fail | Architecture Prediction |
|----|----------|-------------|---------------|----------------------|
| SCI-01 | Tardigrade FTIR | K+D | Both say I (beta+alpha) not C (coiled-coils). Lack specialized FTIR coiled-coil knowledge | Retrieval needed |
| SCI-02 | Schaeffler Ferrite | K | Sonnet: 50, Opus: 20, correct: 10. Don't know the diagram well enough | Retrieval needed |
| SCI-03 | 2D Exciton Rydberg | C+R | Both get magnitude right but miss negative sign / wrong binding energy calc | Sign-explicit (C1) may help |
| SCI-04 | Polymer Adiabatic Force | C | Both derive wrong coefficient in F=... formula | C1 + verification may help |
| SCI-07 | Lattice Adsorption | K+C | Complex stat-mech derivation, wrong partition function setup | Retrieval + computation help |
| SCI-08 | Mean-Field Occupancy | S | Known systematic error — models disagree on 1/2 double-counting factor | No architecture fixes (from prior F8) |
| SCI-10 | Ceramic Sintering | K+D | Neither knows the specific mechanism well enough to identify C | Retrieval needed |
| SCI-14 | ReAl12 Polyhedra | K | Need to compute neighbor lists from CIF data — specialized knowledge | Retrieval + computation |
| LOGIC-05 | Pronoun Disambiguation | D | Both say B, answer is E (ambiguous). Models over-commit to one reading | D2 adversarial elimination |
| LOGIC-09 | Adjective Order | R | Both say CDH, answer is H. Over-generate valid orderings | Stricter verification |
| LOGIC-14 | Sarcasm Detection | D | Both say 1,0,1, answer is 0,0,1. First reply miscategorized | Multiple perspectives may help |
| MATH-06 | b-eautiful Numbers | ? | DISPUTED — both models say 211, key says 150 | Pending verification |
| MATH-10 | Counting Triples | ? | DISPUTED — both models say 889, key says 735 | Pending verification |

## Medium Set (9 questions — Opus fixes what Sonnet misses)

| ID | Question | Failure Mode | How Opus Fixes | Architecture Prediction |
|----|----------|-------------|----------------|----------------------|
| SCI-05 | Perovskite XRD | K | Opus knows rhombohedral splitting rules | Better model or retrieval |
| SCI-06 | Mossbauer Hyperfine | K | Opus knows about orbital angular momentum in linear Fe(II) | Better model or retrieval |
| SCI-11 | Perovskite A-site | K | Opus knows aziridinium literature | Better model or retrieval |
| SCI-12 | Beetle Optics | K+D | Opus correctly identifies Bouligand→unpolarized function | Better model or retrieval |
| LOGIC-06 | Dyck Brackets | C | Opus traces bracket stack more carefully | Verification loops |
| LOGIC-21 | Word Sorting | C | Opus identifies letter-indexing error at step 5 | Verification loops |
| MATH-03 | Fourth Power Div | C | Opus does Hensel lifting correctly | Verification or majority vote |
| MATH-08 | Random Chords | C | Opus computes intersection probabilities correctly | Verification or majority vote |
| MATH-13 | Binary Ones | R+C | Opus finds k(n)=3 achievable (Sonnet stopped at 4) | More thorough search |

## Architecture Components to Test

Based on failure mode analysis:

### 1. Planning Prompts (D2/C1) — Target: Reasoning + Computation errors
- D2 (adversarial elimination) → LOGIC-05, LOGIC-14, SCI-01
- C1 (sign-explicit) → SCI-03, SCI-04

### 2. Verification/Critic Loops — Target: Computation errors
- LOGIC-06, LOGIC-21, MATH-03, MATH-08, MATH-13
- Hypothesis: a critic pass catches arithmetic mistakes that Sonnet makes

### 3. Multi-Agent Majority Vote — Target: Variance-dominated errors
- Run 3 separate Sonnet agents on medium-set questions
- If answers vary across agents, vote. If unanimous wrong, vote doesn't help.

### 4. Retrieval-Augmented Hints — Target: Knowledge gaps
- SCI-01 (coiled-coil FTIR signatures), SCI-02 (Schaeffler diagram values)
- SCI-10 (ceramic sintering gas mechanisms), SCI-06 (linear Fe(II) orbital effects)

### Priority Order for Testing

Round 2 tests (highest information value first):
1. **Critic loops on computation errors** (5 questions) — easiest to test, clear predictions
2. **D2 on discrimination errors** (3 questions) — tests our best prior finding
3. **Majority vote on medium set** (9 questions) — tests variance hypothesis from F5
