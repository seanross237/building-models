---
topic: Li's criterion — phase cancellation convergence mechanism
confidence: verified
date: 2026-03-27
source: "riemann-hypothesis strategy-003 exploration-002"
---

## Finding

For any zero rho = 1/2 + it on the critical line:

    |1 - 1/rho| = |(−1/2 + it)/(1/2 + it)| = sqrt((1/4 + t^2)/(1/4 + t^2)) = 1 exactly

This means (1 - 1/rho)^n lies on the unit circle for ALL n and ALL critical-line zeros. **The Li series converges by phase cancellation (like a Fourier series), not by amplitude decay.** `[VERIFIED by direct computation]`

## Interpretation

Each zero's contribution to lambda_n can be written as:

    2(1 - cos(n * theta_k))

where theta_k = arg((rho_k - 1)/rho_k) ~= 1/t_k for large t_k. The Li coefficient thus measures how much the phases theta_k fail to cancel when raised to the n-th power.

**Li's criterion (lambda_n >= 0 for all n) is equivalent to:** for every n, the sum of cosines Sum cos(n * theta_k) <= K (the number of zero pairs). This is a statement about the Fourier transform of the zero phase distribution. `[CONJECTURED]`

## Connection to RH

If a zero were off the critical line (Re(rho) != 1/2), then |1 - 1/rho| != 1, breaking the pure phase structure. Off-line zeros contribute terms that grow exponentially in n, potentially driving lambda_n negative for large n. This is the mechanism by which Li's criterion detects violations of RH. `[CONJECTURED]`

## Note on Novelty

The fact that |1 - 1/rho| = 1 for Re(rho) = 1/2 is algebraically trivial (follows immediately from the conjugate symmetry). The interpretation as "convergence by phase cancellation" is a useful framing, not a new mathematical result. Future explorations should distinguish algebraic identities from physical/mathematical mechanisms.

## Cross-References

- See `li-coefficients-verified-n500.md` for the primary computational verification
- See `li-gue-comparison-super-rigidity.md` for how super-rigid spacing enhances phase cancellation
- See `riemann-operator-constraints.md` for spectral constraints on the hypothetical Riemann operator
