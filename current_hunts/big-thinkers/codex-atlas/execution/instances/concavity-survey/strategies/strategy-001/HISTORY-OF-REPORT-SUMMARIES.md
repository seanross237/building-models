# History of Report Summaries

## Exploration 001: Classical Eigenvalue Concavity/Convexity Theorems

**Outcome:** Succeeded — clear catalog of ≥8 major theorems with precise statements, domains, and applicability assessments.

**Key Takeaway:** The classical literature has a fundamental domain gap: all major theorems (Davis, Lewis, Ando, Löwner, Fan, Weyl) operate on H_n as a VECTOR SPACE or H_n^{++} as an open cone. None directly address λ_max(H(Q)) as a function on a compact group SU(N)^E. Moreover, λ_max is CONVEX on vector spaces (not concave). The two closest results (2024 unitary eigenvalue paper, Kostant/AGS convexity) give the wrong direction or wrong object.

**Best paths forward identified:**
1. Direct second-variation analysis of λ_max(H(Q)) at Q=I (computable, not covered by generic theory)
2. Schur-Horn/Kostant majorization: if λ(H(Q)) ≺ λ(H(I)) for all Q, then λ_max(H(Q)) ≤ λ_max(H(I)) directly
3. Restricted concavity along gauge orbits
4. Adaptable techniques from arXiv:2408.16906 (2024 unitary eigenvalue convexity paper)

**No applications to lattice gauge theory found** — genuine gap in the literature.

## Exploration 002: Geodesic Convexity on Riemannian Manifolds and Compact Lie Groups

**Outcome:** Succeeded — six frameworks for certifying local max = global max without full concavity.

**Key Takeaway:** Full geodesic concavity is IMPOSSIBLE by theorem on compact manifolds (superharmonic → constant by max principle). This is not a numerical accident — it's topology. The right question is "local max → global max," for which six frameworks exist:

**Top two frameworks:**
1. **Perfect Morse function** (★★★★★): On SU(2)^E ≅ (S³)^E, b_{3E} = 1. If λ_max(H(Q)) is a perfect Morse function, the unique top-index critical point IS the global max. Precedent: Atiyah-Bott (1983) proved the Yang-Mills functional is equivariantly perfect on Riemann surfaces.
2. **Trap-free landscape** (★★★★): Russell-Rabitz (2016) proved quantum control landscapes are trap-free under transversality. If dH is surjective at generic Q, no non-global local maxima exist. Checkable via rank computation.

Other frameworks: gauge symmetry + unique orbit (★★★★), Łojasiewicz + uniqueness (★★★), double bracket reformulation (★★★), SDP certificate (★★).

**Key computations identified:** (1) Rank of dH at non-flat configs (verifies trap-free), (2) Critical point count via gradient ascent sweep (evidence for Morse perfectness), (3) Convexity within injectivity radius ball.

## Exploration 003: Synthesis — Proof Strategy Assessment

**Outcome:** Succeeded — ranked list of 8 approaches with cross-references, critical path specified, failure modes analyzed.

**Key Takeaway:** A new highest-priority approach emerged: **direct matrix domination H(I) ≥ H(Q) (PSD)**. If H(I) - H(Q) is positive semidefinite for all Q, then λ_max(H(Q)) ≤ λ_max(H(I)) in two lines — no topology needed. The SZZ bound's 12-170x looseness (plaquette destructive interference) is circumstantial evidence this might hold. This appears to be a genuinely novel direction not found in the literature.

**Recommended critical path:**
1. FIRST: Numerical matrix domination test (~20 lines numpy, 1-2 days)
2. PARALLEL: Gradient ascent landscape survey (confirm unique attractor)
3. IF domination holds: Analytical proof via D+C Hessian decomposition
4. IF domination fails: Verify Rabitz transversality (rank of dH)
5. FALLBACK: Kirwan-type equivariant Morse theory (hard, 2-4 weeks, but precedent exists)

**Key connections found:** Majorization and Morse theory are independent paths (majorization makes Morse unnecessary). Matrix domination subsumes majorization. The 2024 unitary technique gives local concavity within the convexity ball, bridging to a landscape survey for global uniqueness.

