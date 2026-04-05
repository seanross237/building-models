# Reasoning Log

## Exploration 001 + 002 (Parallel Launch)

### Options Considered
1. Sequential: classical results first, then Riemannian setting, then synthesis
2. Parallel: run classical (001) and Riemannian (002) simultaneously, then synthesize in 003

### Decision
Parallel launch of 001 and 002. These are independent literature surveys in different mathematical areas. Running them simultaneously saves time and the results feed jointly into the synthesis in 003.

### Key Prior Knowledge
The library search revealed a CRITICAL prior result: **global geodesic concavity of λ_max(M(Q)) has been numerically falsified** (E002 from b-square-inequality-proof-progress.md). F''(Q, W) > 0 was found at Q ≠ I. This means the survey isn't asking "is λ_max concave?" (answer: no, globally). Instead, the right questions are:
- Under what conditions IS λ_max concave?
- What restricted/conditional concavity results exist?
- Can concavity along specific paths (e.g., gauge orbits, geodesics from flat connections) be established?
- Are there alternatives to full concavity that still yield the global max result?

Both exploration goals are designed with this falsification pre-loaded so the explorers focus on what's actually viable.

### Exploration 001 Reflection (post-completion)
The explorer delivered exactly what was asked — a thorough catalog with honest applicability assessments. The key finding is a negative result: classical eigenvalue theorems live in the wrong domain (vector spaces, not compact groups) and give the wrong direction (convexity, not concavity). This is extremely valuable because it rules out the "just apply a known theorem" path. The most promising leads are: (1) majorization/Schur-Horn argument, (2) direct second-variation computation at Q=I, (3) the 2024 unitary eigenvalue paper's proof techniques. Scope was right — one exploration for the classical survey was sufficient.

### Exploration 002 Reflection (post-completion)
Excellent results. The explorer found the impossibility theorem immediately (geodesic concavity → superharmonic → constant on compact manifolds) which reframes the entire problem. It then identified six alternative frameworks, with two standouts: Morse perfectness (using Betti numbers of (S³)^E) and trap-free landscapes (Rabitz-Russell transversality). Both are genuinely applicable to our setting. The Atiyah-Bott precedent for Yang-Mills on Riemann surfaces is particularly promising. Scope was perfect — broad enough to find multiple alternatives, focused enough to assess each one meaningfully.

## Exploration 003 (Synthesis)

### Options Considered
1. Deep dive on Morse perfectness specifically — explore whether Atiyah-Bott applies to lattice YM
2. Deep dive on Rabitz trap-free landscape — verify the controllability condition
3. Synthesis: combine findings from 001 + 002 into a ranked assessment of all viable approaches

### Decision
Synthesis (option 3). With only 3 explorations budgeted, the most valuable use of the last one is to cross-reference the classical matrix analysis findings (001) with the Riemannian/topological frameworks (002) and produce a ranked list of proof strategies with concrete next steps. Deep dives on individual approaches belong in a follow-up mission or can be picked up by the Yang-Mills strategizer.

### Key Insight Driving the Goal Design
The two explorations revealed a clean split:
- Classical matrix analysis can't help directly (domain gap — wrong space)
- Riemannian/topological frameworks CAN help but need specific verification (Morse perfectness, trap-free transversality)
- There's a potential BRIDGE: the majorization idea from 001 + the Morse/topological structure from 002 might combine. The synthesis should explore these connections.

### Exploration 003 Reflection (post-completion)
The synthesis delivered exactly what was needed — and more. The emergent finding (matrix domination H(I) ≥ H(Q) as PSD) was the most valuable output of the entire mission. Neither survey named it; it emerged from cross-referencing the "plaquette destructive interference" observation with the "what direct conditions imply λ_max bound" question. The ranked list is clean and actionable. The critical path is well-ordered by expected value. No wasted exploration in this mission — 3/3 delivered.

### Librarian Query Summary
- **Factual library:** Rich on Yang-Mills Hessian eigenstructure (D+C decomposition, Weitzenbock formula, H_norm conjecture, SZZ bounds). Complete gap on matrix analysis theorems (Davis-Lewis, Ando, matrix convexity).
- **Meta library:** Useful lessons — name specific authors, pre-load context, use divergent survey pattern, ask forward-looking questions, prioritize novelty assessment.
- **Meta-inbox:** Empty (new mission).
- **Usefulness:** Very high. The geodesic concavity falsification result fundamentally shapes the exploration goals.
