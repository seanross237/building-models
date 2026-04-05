# Factual Seed Knowledge — INDEX

These entries are seeded from the Atlas library's factual collection. They were selected for their relevance to the Navier-Stokes existence and smoothness problem through transferable mathematical techniques: spectral analysis, regularity structures, stochastic PDEs, multi-scale renormalization group methods, energy estimates, lattice-to-continuum limits, and proof strategy frameworks. The Yang-Mills mass gap problem shares deep structural parallels with Navier-Stokes — both require controlling nonlinear PDEs across scales, proving regularity or constructing solutions in the continuum limit, and establishing spectral gaps in infinite-dimensional operators.

## yang-mills/

- **balaban-uv-stability.md** — Balaban's multi-scale UV stability program for 4D Yang-Mills; the renormalization group framework for controlling UV divergences scale-by-scale transfers directly to multi-scale regularity analysis in Navier-Stokes.
- **shen-zhu-zhu-stochastic-analysis.md** — SZZ stochastic analysis approach to mass gap at strong coupling; stochastic PDE techniques and spectral gap methods applicable to stochastic Navier-Stokes formulations.
- **stochastic-quantization-chandra-hairer.md** — Chandra-Hairer-Chevyrev-Shen regularity structures construction; the regularity structures framework (Hairer's Fields Medal work) is the leading approach to singular stochastic PDEs including stochastic Navier-Stokes.
- **adhikari-cao-technique-and-obstruction.md** — Adhikari-Cao swapping map technique and finite-to-continuous obstruction; the lattice-to-continuum limit problem is structurally identical to discretization convergence questions in Navier-Stokes numerics.
- **completed-gauge-constructions.md** — Reference benchmarks for completed rigorous QFT constructions; demonstrates what "rigorous existence proof" looks like for infinite-dimensional nonlinear systems.
- **dimock-expository-program.md** — Dimock's pedagogical revisitation of Balaban's multi-scale methods; accessible entry point to the renormalization group techniques applicable to fluid PDE regularity.
- **gap-structure-overview.md** — Gap analysis of what remains unproven for the Yang-Mills Millennium Prize; maps the proof strategy landscape, useful as a template for analogous gap analysis on Navier-Stokes.
- **lattice-numerical-evidence.md** — Numerical lattice results for pure Yang-Mills theory; lattice discretization and extrapolation methods transfer to numerical evidence strategies for Navier-Stokes regularity.
- **hessian-analytical-formula-c-decomposition.md** — Analytical Hessian formula with curvature/commutator decomposition; second-variation analysis and operator spectral decomposition techniques applicable to stability analysis of Navier-Stokes solutions.
- **hessian-lambda-min-adversarial.md** — Adversarial characterization of minimum eigenvalue bounds via decoherence; adversarial stress-testing methodology for operator bounds transferable to energy estimate verification.
- **b-square-inequality-proof-progress.md** — Partial proofs, failed approaches, and remaining gap for a key operator inequality; detailed record of proof strategy attempts, pivots, and obstructions — a template for systematic proof attack on hard inequalities.
- **full-eigenspace-gap1-investigation.md** — Full eigenspace bound investigation with per-vertex reduction and numerical evidence; eigenvalue bounding techniques and reduction strategies applicable to spectral analysis of the Stokes operator.
- **weitzenbock-exact-formula.md** — Exact Weitzenbock formula for curvature eigenvalues; Bochner-Weitzenbock techniques connect curvature to Laplacian eigenvalues, directly relevant to geometric analysis of fluid operators.
- **szz-lemma-4-1-hessian-slack.md** — SZZ Lemma 4.1 Hessian bound is 12-170x loose due to plaquette cancellations; demonstrates how cancellation structure in nonlinear terms can make naive bounds extremely wasteful — a key lesson for Navier-Stokes energy estimates where the nonlinear term has similar hidden cancellations.
- **proof-strategies-comparison.md** — Comparative assessment of proof strategies for Yang-Mills existence and mass gap; multi-strategy comparison framework transferable to evaluating competing approaches to Navier-Stokes regularity.
- **cns-novelty-assessment.md** — Novelty assessment of the Cao-Nissim-Sheffield 2025 area law result; demonstrates rigorous novelty verification methodology for claimed mathematical results.
- **adversarial-review-proof-chain.md** — Adversarial review finding a critical flaw in a proof chain; demonstrates how systematic adversarial review catches errors that internal consistency checks miss — essential methodology for any proof attempt.

## riemann-hypothesis/

- **riemann-operator-constraints.md** — Constraints on the hypothetical Riemann operator from GUE statistics; spectral operator reconstruction constraints demonstrate how statistical properties constrain the underlying operator — analogous to constraining the Navier-Stokes solution operator from known regularity properties.
- **spectral-form-factor-gue.md** — Spectral form factor confirms GUE universality class; spectral universality analysis methods applicable to eigenvalue statistics of discretized Navier-Stokes operators.
- **li-coefficients-verified-n500.md** — Li's criterion verified for 500 coefficients; large-scale numerical verification methodology and convergence analysis transferable to numerical evidence programs for Navier-Stokes regularity.

## cross-cutting/

- **spectral-dimension-propagator-constraint.md** — Spectral dimension d_s=2 in the UV forces propagator ~ 1/p^4; demonstrates how dimensional flow constrains propagator structure — the propagator/Green's function approach is central to Navier-Stokes solution theory.
- **spectral-dimension-running.md** — Spectral dimension running from 4 to 2 across quantum gravity approaches; multi-scale dimensional analysis techniques applicable to understanding the scale-dependent behavior of Navier-Stokes solutions.
- **entanglement-area-law.md** — Entanglement entropy area law as a cross-cutting theme; area-law scaling for information content of boundary data is structurally related to boundary regularity estimates in PDE theory.

## emergent-gravity/

- **padmanabhan-program.md** — Padmanabhan's thermodynamic emergent gravity program showing Einstein field equations reduce to Navier-Stokes form on null surfaces; the most directly relevant entry — establishes a precise mathematical mapping between gravitational field equations and fluid dynamics equations, making all geometric/thermodynamic techniques from gravity potentially applicable to Navier-Stokes.
