# Experiment 8: HLE Gauntlet — T5 Triple Fusion on Expert Questions (2026-03-28)

**Goal:** Test whether the T5 Triple Fusion system prompt (Exp 7 winner) transfers from reasoning benchmarks (BBEH) to expert domain-knowledge benchmarks (HLE).

**Models:** Claude Opus 4.6, Claude Sonnet 4.6
**Method:** All 14 HLE text-only questions, run with T5 system prompt, single-agent (no sub-agents). Both models see identical prompts.
**System Prompt:** "Default to EXCLUSION -- better to select too few. Ground every claim in specific cited evidence. Before committing, consider the OPPOSITE of your initial reading. Check if surface patterns are misleading you. Only include what survives all three checks."

**Question Set (14 HLE questions):**

| Q | Topic | Subject | Answer Type | Expected Answer |
|---|-------|---------|-------------|-----------------|
| Q1 | Tardigrade Protein FTIR Gelation | Biophysics | multipleChoice | C |
| Q2 | Stainless Steel Ferrite Level | Materials Science | exactMatch | 10 |
| Q3 | 2D Semiconductor Exciton Rydberg | Condensed Matter Physics | exactMatch | -0.08 |
| Q4 | Polymer Freely Jointed Chain Force Law | Polymer Physics | exactMatch | F(x) = 3E(0)x/(nℓ)² |
| Q5 | Perovskite XRD Bragg Reflections | Crystallography | exactMatch | 1, 2, 2 |
| Q6 | 57Fe Mössbauer Hyperfine Field | Chemistry / Spectroscopy | multipleChoice | C |
| Q7 | 2D Lattice Adsorption Partition Function | Thermodynamics | exactMatch | Z = 4.61, ⟨k⟩ = 1.66 |
| Q8 | 2D Lattice Gas Mean-Field Occupancy | Thermodynamics | exactMatch | 0.424 |
| Q9 | CARS Microscopy Broadband Pump | Physics / Spectroscopy | multipleChoice | B |
| Q10 | Coarsening Gas During Sintering | Materials Science | multipleChoice | C |
| Q11 | Organic A-Site Cations for Perovskites | Chemistry / Perovskites | multipleChoice | B |
| Q12 | Protaetia Cuprea Elytron Optics | Ecology / Biophysics | multipleChoice | G |
| Q13 | Mori-Tanaka Effective Elastic Moduli | Mechanical Engineering | exactMatch | C = (Vm·Cm + Vf·Cf·A)·(Vm·I + Vf·A)⁻¹ |
| Q14 | ReAl12 Crystal Coordination Polyhedra | Crystallography | exactMatch | Al, Re2Al13; Al, ReAl12; Al, Re2Al9 |

## Results

### Full Results Table

| Q | Topic | Expected | Opus Answer | Opus | Sonnet Answer | Sonnet |
|---|-------|----------|-------------|------|---------------|--------|
| Q1 | Tardigrade FTIR | C | F | ✗ | I | ✗ |
| Q2 | Ferrite Level | 10 | 50 | ✗ | 0 | ✗ |
| Q3 | Exciton Rydberg | -0.08 | -0.08 | ✓ | -0.08 | ✓ |
| Q4 | Polymer Force Law | 3E(0)x/(nℓ)² | 3E(0)x/(n²ℓ²) | ✓ | -3E(0)x/(n²ℓ²) | ✓* |
| Q5 | Perovskite XRD | 1, 2, 2 | 1, 2, 2 | ✓ | 1, 2, 2 | ✓ |
| Q6 | Mössbauer | C | C | ✓ | D | ✗ |
| Q7 | Lattice Adsorption | Z=4.61, ⟨k⟩=1.66 | Z=8.34, ⟨k⟩=6.32 | ✗ | Z=3.78, ⟨k⟩=1.13 | ✗ |
| Q8 | Lattice Gas | 0.424 | 0.358 | ✗ | 0.848 | ✗ |
| Q9 | CARS Microscopy | B | C | ✗ | C | ✗ |
| Q10 | Coarsening Gas | C | E | ✗ | F | ✗ |
| Q11 | A-Site Cations | B (incl. Aziridinium) | B | ✓ | A | ✗ |
| Q12 | Beetle Elytron | G | G | ✓ | K | ✗ |
| Q13 | Mori-Tanaka | formula | formula | ✓ | formula | ✓ |
| Q14 | ReAl12 Crystal | Al-centered polyhedra | Re-centered (wrong) | ✗ | Re, ReAl12 (wrong) | ✗ |

\* Q4 Sonnet: formula magnitude matches but includes a negative sign not in expected answer (sign convention ambiguity).

### Score Summary

| Model | Score | Percentage |
|-------|-------|------------|
| **Opus 4.6** | **7/14** | **50%** |
| **Sonnet 4.6** | **4/14** | **29%** |

### Opus-Only Correct (3 questions that distinguish Opus from Sonnet)

| Q | Topic | Why Opus Won |
|---|-------|-------------|
| Q6 | Mössbauer Hyperfine Field | Opus recognized that linear S=2 Fe(II) has orbital angular momentum (Lz=±2) contributing to hyperfine field beyond spin-only. Sonnet picked D (tetrahedral S=2 Fe(II)) — missed the orbital contribution unique to linear geometry. |
| Q11 | A-Site Cations | Opus knew about Aziridinium (AZ) forming 3D perovskites. Sonnet picked A (Cs, MA, FA only) — the documented AI failure mode where models overlook AZPbBr₃. |
| Q12 | Beetle Elytron Optics | Opus correctly identified Bouligand structures making cuticle appear unpolarized to insects (G). Sonnet picked K (Bouligand for mate attraction) — right structure, wrong ecological function. |

### Both Correct (4 questions — the "easy" tier for expert questions)

| Q | Topic | Why Both Got It |
|---|-------|----------------|
| Q3 | Exciton Rydberg | Standard 2D hydrogen model formula derivation — clean physics, no domain-specific traps |
| Q4 | Polymer Force Law | Statistical mechanics derivation from first principles — reasoning-heavy, knowledge-light |
| Q5 | Perovskite XRD | Symmetry group theory applied to d-spacing formula — mechanical, verifiable |
| Q13 | Mori-Tanaka | Known textbook result in composite materials theory |

### Both Wrong (7 questions — the "impossible" tier)

| Q | Topic | Failure Analysis |
|---|-------|-----------------|
| Q1 | Tardigrade FTIR | Requires specific knowledge: 1618+1652 dual rise without 1680 rise = coiled-coil signature. Both models know FTIR peak assignments but not this specific diagnostic pattern. Opus guessed F (disordered→β-sheet), Sonnet guessed I (disordered→β-sheet+helix). |
| Q2 | Ferrite Level | Requires reading a Schaeffler diagram from memory. Opus guessed 50, Sonnet guessed 0 — both have the wrong mental model of where (39 Cr_eq, 29 Ni_eq) lands. |
| Q7 | Lattice Adsorption | Complex numerical computation with ambiguous problem statement. Neither model set up the partition function correctly. |
| Q8 | Lattice Gas | Self-consistent mean-field equation — both attempt the right approach but converge to wrong fixed points. |
| Q9 | CARS Microscopy | Both chose C (anti-Stokes with distinguishable information) over B (anti-Stokes without distinguishable information). The distinction between "broadband pump" and "narrowband pump" for spectral resolution is a niche spectroscopy fact. |
| Q10 | Coarsening Gas | Both chose wrong — C is correct because gas-induced voids concentrate in the interior (not randomly distributed). This requires knowing the surface-shell densification effect during sintering. |
| Q14 | ReAl12 Crystal | Requires computing neighbor lists from CIF coordinates with space group symmetry — essentially a computational crystallography task, not a reasoning task. Both models attempted to reason from structure type knowledge rather than compute. |

## Timing Data

### Opus — Per-Question Breakdown
| Q | Topic | Time (s) | Tokens | Result |
|---|-------|----------|--------|--------|
| Q1 | Tardigrade FTIR | 4.2 | 16,227 | ✗ |
| Q2 | Ferrite Level | 2.7 | 15,948 | ✗ |
| Q3 | Exciton Rydberg | 8.6 | 16,383 | ✓ |
| Q4 | Polymer Force Law | 20.7 | 16,970 | ✓ |
| Q5 | Perovskite XRD | 25.0 | 17,147 | ✓ |
| Q6 | Mössbauer | 2.3 | 16,020 | ✓ |
| Q7 | Lattice Adsorption | 1284.1 | 105,783 | ✗ |
| Q8 | Lattice Gas | 51.0 | 19,782 | ✗ |
| Q9 | CARS Microscopy | 3.4 | 16,002 | ✗ |
| Q10 | Coarsening Gas | 2.3 | 16,055 | ✗ |
| Q11 | A-Site Cations | 2.4 | 16,068 | ✓ |
| Q12 | Beetle Elytron | 2.1 | 16,243 | ✓ |
| Q13 | Mori-Tanaka | 3.4 | 16,077 | ✓ |
| Q14 | ReAl12 Crystal | 306.2 | 43,477 | ✗ |
| **Total** | | **~1718** | **~348,182** | **7/14** |

**Note:** Q7 and Q14 were extreme outliers — Q7 ran for 21 minutes attempting iterative computation, Q14 for 5 minutes trying to build neighbor lists. All other questions completed in under 1 minute. Multiple-choice questions averaged ~3s; exact-match derivations averaged ~15s.

## Key Findings

### 1. T5 Triple Fusion does NOT transfer well from BBEH to HLE
- On BBEH (reasoning): 8/9 (89%) — near-ceiling performance
- On HLE (domain knowledge): 7/14 (50%) — exactly matches the benchmark average
- The prompt's power is in catching reasoning errors (consider the OPPOSITE, check for surface patterns). On expert domain questions, the bottleneck is knowledge, not reasoning strategy.

### 2. Opus vs Sonnet gap is larger on HLE than BBEH
- BBEH: Opus 13/14, Sonnet 12/14 — 1 question difference (geometric_shapes only)
- HLE: Opus 7/14, Sonnet 4/14 — 3 question difference (Mössbauer, A-site cations, beetle optics)
- Expert knowledge questions amplify the model capability gap. Opus has strictly more domain knowledge than Sonnet.

### 3. The 7 "impossible" questions reveal a clear failure taxonomy
- **Niche diagnostic patterns** (Q1, Q9): Model knows the domain but not the specific diagnostic. T5's inversion instruction can't help — you can't "consider the opposite" if you don't know the relevant fact.
- **Diagram/lookup recall** (Q2): Requires memorizing a specific chart. No reasoning strategy compensates.
- **Numerical computation** (Q7, Q8): Self-consistent equations, iterative solutions. Models attempt the right approach but converge to wrong values. Tool use (actual computation) might help.
- **Implicit knowledge** (Q10): Requires knowing a non-obvious physical mechanism (surface-shell densification). The "randomly distributed" trap is exactly what T5 should catch, but without the mechanism knowledge, the model can't identify the trap.
- **Computational crystallography** (Q14): Fundamentally a computation task disguised as a knowledge question. Requires neighbor-list algorithms, not reasoning.

### 4. Q11 (A-site cations) is a documented AI failure mode — and Opus dodges it
- HLE notes this as a known AI failure: models consistently overlook Aziridinium
- Opus picked B (including Aziridinium) — it has this knowledge. Sonnet picked A (the standard three) — it doesn't.
- This is pure knowledge retrieval, not reasoning. T5 played no role here.

### 5. Q12 (beetle optics) shows the subtlety gap between Opus and Sonnet
- Both identified Bouligand structures as the key optical mechanism (correct)
- Opus correctly chose G: "make cuticle appear unpolarized to most insects" (the anti-predator function)
- Sonnet chose K: "circular polarization for mate attraction" (the wrong ecological function)
- The distinction requires knowing that P. cuprea is uniformly colored (ruling out predator-distraction) and that the ecological function is predator evasion, not mate signaling

### 6. The "easy" tier (Q3, Q4, Q5, Q13) shares a common pattern
- All are derivation or formula-recall questions with clear mathematical structure
- Q3 and Q4: physics derivations from well-known models (2D hydrogen, freely jointed chain)
- Q5: mechanical application of symmetry rules to d-spacing formula
- Q13: textbook result (Benveniste 1987)
- These are "reasoning questions wearing domain costumes" — the domain knowledge needed is standard graduate-level, and the challenge is applying it correctly

### 7. Numerical computation questions (Q7, Q8) are fundamentally different from reasoning questions
- Q7: Opus spent 21 minutes and 105K tokens trying to compute iteratively — and still got wrong values
- Q8: Both models set up the right self-consistent equation but converge to wrong fixed points
- These questions would benefit from tool use (Python/calculator) more than better prompting
- **Implication for architecture:** A "math-explorer" agent pattern with actual computation tools might solve these

### 8. T5's "consider the OPPOSITE" instruction has no effect on knowledge-gap failures
- On BBEH, inversion caught category confusions (sport vs activity), CWA errors, surface pattern traps
- On HLE, the failures are all knowledge-first: you need to know the fact before you can reason about it
- The prompt's three checks (exclusion, evidence, inversion) all require having evidence to check against
- **Conclusion:** T5 is a reasoning amplifier, not a knowledge amplifier

## Architecture Design Principles (Updated from Experiments 3-8)

1. **T5 Triple Fusion is the best single system prompt for reasoning tasks.** 8/9 on BBEH, but only 7/14 on HLE — it hits ceiling on knowledge questions.
2. **Opus outperforms Sonnet more on knowledge than reasoning.** 1-question gap on BBEH, 3-question gap on HLE.
3. **Expert domain questions have three difficulty tiers:**
   - Easy (both models correct): Standard derivations with clear mathematical structure
   - Medium (Opus-only): Requires niche domain knowledge that Opus has and Sonnet doesn't
   - Hard (both wrong): Niche diagnostics, diagram recall, or computational tasks
4. **The "hard" tier failures suggest two architecture improvements:**
   - Tool-augmented agents for numerical computation (Q7, Q8, Q14)
   - RAG or retrieval for niche diagnostic patterns (Q1, Q2, Q9, Q10)
5. **System prompts cannot compensate for knowledge gaps.** T5's reasoning improvements don't transfer to knowledge-bottlenecked questions.
6. **HLE is a better discriminator than BBEH for comparing models.** Three distinguishing questions vs one on BBEH.

## Next Steps

- **Experiment 9 candidate:** Tool-augmented agent on Q7, Q8, Q14 — give the model Python/computation tools and re-test
- **Experiment 10 candidate:** Multi-agent architecture on HLE — can a critic/verifier help on the "both wrong" questions?
- **Expand HLE question set:** 14 questions is small; the public subset has 106 — load more to increase statistical power
- **Test ARC-AGI-2:** 4 questions loaded, never tested — tests pattern abstraction rather than knowledge

## Total Experiment Stats
- **Total agent calls:** 28 (14 Opus + 14 Sonnet) + 1 retry
- **Total wall-clock time:** ~50 minutes (dominated by Q7 Opus at 21 min)
- **Total tokens consumed:** ~700K (Opus ~348K + Sonnet ~350K est.)
