# Computations for Later

## From Exploration 001 (Classical Eigenvalue Theorems)

### 1. Majorization test: λ(H(Q)) ≺ λ(H(I)) for all Q?
- **What:** Compute H(Q) for many random Q ∈ SU(2)^E and check whether eigenvalues are always majorized by those at Q=I
- **Why:** If majorization holds, then λ_max(H(Q)) ≤ λ_max(H(I)) directly — a complete proof
- **Difficulty:** Easy (numpy, random SU(2) sampling)
- **Inputs needed:** Explicit formula for H(Q) (Yang-Mills Hessian), available from library (D+C decomposition)
- **Source:** Exploration 001

### 2. Second-variation of λ_max(H(Q)) at Q=I
- **What:** Compute d²λ_max(H(Q(t)))/dt²|_{t=0} for all geodesics through I. If always negative, Q=I is local max.
- **Why:** Establishes local concavity at Q=I (already known numerically, but explicit formula useful)
- **Difficulty:** Moderate (10-30 lines scipy/sympy for SU(2))
- **Inputs needed:** Weitzenbock formula / D+C decomposition at Q=I
- **Source:** Exploration 001

## From Exploration 002 (Geodesic Convexity Alternatives)

### 3. Rank of dH on SU(N)^E (Rabitz transversality check)
- **What:** Compute rank of the differential of Q ↦ H(Q) at multiple non-flat configurations
- **Why:** If generically full rank, verifies the Rabitz-Russell transversality condition → trap-free landscape → no non-global local maxima. This would be a DECISIVE result.
- **Difficulty:** Moderate (50-100 line numpy script)
- **Inputs needed:** Explicit formula for H(Q)
- **Source:** Exploration 002
- **Priority:** HIGH — checkable and potentially decisive

### 4. Morse critical point count via gradient ascent sweep
- **What:** Gradient ascent on λ_max(H(Q)) from many random initializations on small lattices (E=2,3 for SU(2))
- **Why:** If only one local max found, strong numerical evidence for Morse perfectness
- **Difficulty:** Moderate
- **Source:** Exploration 002

### 5. Geodesic concavity within injectivity radius ball
- **What:** Check whether λ_max(H(Q)) is geodesically concave within the ball of radius π√2/2 around Q=I
- **Why:** Would give local-to-global result within the geodesically convex ball
- **Difficulty:** Low (modify existing second-derivative computation)
- **Source:** Exploration 002
