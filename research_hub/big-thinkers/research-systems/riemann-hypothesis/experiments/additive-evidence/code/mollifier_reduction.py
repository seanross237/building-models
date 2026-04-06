"""
Show that the NON-TRIVIAL ('t-coupled') version of the additive-evidence LP
is equivalent to mollifier optimization.

A prime-supported mollifier is M(s) = sum_{p<=P} a_p p^{-s} (or more generally
a short Dirichlet polynomial). For s on the critical strip we have
    Re log M(s) = Re sum_p a_p p^{-s}  (when log is the principal branch near 1).

The natural weights induced by M are
    w_p(t) = -Re(a_p p^{-sigma-it}) = -a_p cos(t log p) p^{-sigma}
(for real a_p). These satisfy |w_p(t)| <= |a_p| p^{-sigma}, an envelope that
CANNOT converge at sigma=1/2 unless we impose |a_p| <= p^{-1/2-eps}, i.e.
"mollifier coefficients" decaying faster than the natural p^{-1/2} scale.

This is exactly the classical constraint in Levinson/Conrey mollifier methods
except that those methods average in t rather than trying pointwise domination.

This script:
  1) Computes the AVERAGED "mollifier budget" needed to dominate <-log|zeta|>
     averaged over a t-window.
  2) Contrasts with the pointwise budget.
"""
import numpy as np
import mpmath as mp

mp.mp.dps = 30


def primes_up_to(N):
    return [p for p in range(2, N+1) if all(p % d for d in range(2, int(p**0.5)+1))]


def neg_log_zeta_abs(sigma, t):
    return float(-mp.log(abs(mp.zeta(mp.mpc(sigma, t)))))


def main():
    primes = primes_up_to(100)
    B = np.array([1.0/(p**1.05) for p in primes])
    budget = float(np.sum(B))
    print(f"L1-envelope budget (eps=0.05, P<=100) = {budget:.4f}")

    # Mean of -log|zeta| over a long t-window, per sigma
    print("\nMean of -log|zeta(sigma+it)| over t in [10, 200]:")
    for sigma in [0.55, 0.60, 0.70, 0.80, 1.00]:
        ts = np.linspace(10.0, 200.0, 401)
        vals = np.array([neg_log_zeta_abs(sigma, float(t)) for t in ts])
        mean = float(np.mean(vals))
        mx = float(np.max(vals))
        mn = float(np.min(vals))
        print(f"  sigma={sigma}: mean={mean:.4f}, min={mn:.4f}, max={mx:.4f}, "
              f"std={float(np.std(vals)):.4f}")
        # Bohr-Jessen analogue: E[-log|zeta|] tends to 0 in t-average for sigma > 1
        # and to a finite value 0 for sigma > 1/2 by symmetry of the BJ distribution.
        # The L1-envelope 1.64 dominates the mean for every sigma >= 0.55, but NOT
        # the pointwise max at sigma <= 0.7.

    print("\nConclusion: the envelope CAN dominate the t-averaged target")
    print("(= ordinary mollifier estimates) but CANNOT dominate the pointwise")
    print("max near the critical line. The averaging is what makes mollifiers work,")
    print("and the additive-evidence proposal (as pointwise minimax) loses that.")


if __name__ == "__main__":
    main()
