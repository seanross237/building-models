"""
Task 3: Commutator mechanism analysis — SQG vs NS.

Analyzes:
1. What the SQG commutator estimate gives (Caffarelli-Vasseur 2010)
2. Whether an analogous commutator form exists for the NS bottleneck P^{21}
3. Whether Coifman-Rochberg-Weiss (1976) commutator bounds apply

Also includes numerical computation of the commutator [R_iR_j, u^{below}·]
to test whether it gains regularity on DNS data.
"""

import sys
import os
import numpy as np
from numpy.fft import fftn, ifftn

strat1_code = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', '..', '..',
    'strategy-001', 'explorations', 'exploration-002', 'code'))
sys.path.insert(0, strat1_code)

from ns_solver import NavierStokesSolver


def compute_commutator_RiRj_b(solver, b_phys, f_hat, i_idx, j_idx):
    """
    Compute [R_iR_j, b·]f = R_iR_j(b*f) - b*R_iR_j(f)

    where b is a scalar multiplier (in physical space) and f is in spectral space.

    R_iR_j(g) = F^{-1}[ -k_i k_j / |k|^2 * g_hat ]

    Returns the commutator in physical space.
    """
    K = [solver.KX, solver.KY, solver.KZ]
    ki = K[i_idx]
    kj = K[j_idx]

    # R_iR_j operator in spectral space: multiply by -ki*kj/|k|^2
    def apply_RiRj(g_hat):
        result = -ki * kj * g_hat / solver.K2_safe
        result[0, 0, 0] = 0
        return result

    f_phys = solver.to_physical(f_hat)

    # Term 1: R_iR_j(b * f)
    bf_hat = fftn(b_phys * f_phys)
    term1 = ifftn(apply_RiRj(bf_hat)).real

    # Term 2: b * R_iR_j(f)
    RiRj_f = ifftn(apply_RiRj(f_hat)).real
    term2 = b_phys * RiRj_f

    return term1 - term2


def compute_commutator_Ri_b(solver, b_phys, f_hat, i_idx):
    """
    Compute [R_i, b·]f = R_i(b*f) - b*R_i(f)

    This is the basic Coifman-Rochberg-Weiss commutator.

    R_i(g) = F^{-1}[ -i*k_i / |k| * g_hat ]
    """
    K = [solver.KX, solver.KY, solver.KZ]
    ki = K[i_idx]
    K_mag_safe = np.where(solver.K_mag > 0, solver.K_mag, 1.0)

    def apply_Ri(g_hat):
        result = -1j * ki * g_hat / K_mag_safe
        result[0, 0, 0] = 0
        return result

    f_phys = solver.to_physical(f_hat)

    # [R_i, b]f = R_i(bf) - b R_i(f)
    bf_hat = fftn(b_phys * f_phys)
    term1 = ifftn(apply_Ri(bf_hat)).real
    term2 = b_phys * ifftn(apply_Ri(f_hat)).real

    return term1 - term2


def main():
    print("=" * 70)
    print("TASK 3: SQG Commutator Mechanism vs NS")
    print("=" * 70)

    print("""
3a. WHAT THE SQG COMMUTATOR GIVES
==================================

In Caffarelli-Vasseur (2010), SQG in the Caffarelli-Silvestre extension:
  dtheta/dt + u . grad theta = 0       in R^2
  u = R^perp theta = (-R_2, R_1) theta  (Riesz transforms)

The De Giorgi iteration for theta gives an energy estimate with the key term:

  I_k^{SQG} = int theta_k * (u . grad theta_k) dx   [schematic]

BUT u depends on theta, so u = R^perp theta. In the truncated setting:
  u = R^perp(theta^{below} + theta^{above})

The key insight: the theta^{below} contribution can be written as a COMMUTATOR:

  theta_k * (R^perp theta^{below}) . grad theta_k
  = theta_k * [R^perp, theta^{below}] . grad theta_k
    + theta_k * theta^{below} * (R^perp grad) theta_k

The second term vanishes after integration by parts (antisymmetry of R^perp grad).
So we're left with a COMMUTATOR:

  I_k^{SQG} ~ int theta_k * [R^perp, theta^{below}] . grad(theta_k) dx

The Coifman-Rochberg-Weiss (1976) theorem says:
  [R_i, b]f is bounded on L^p if b in BMO.

But more crucially, Caffarelli-Vasseur use a STRONGER commutator estimate
from Coifman-Meyer (1975) / Kato-Ponce (1988):

  ||[(-Delta)^{s/2}, b]f||_{L^p} <= C(||grad b||_{L^{p1}} ||f||_{L^{p2}}
                                       + ||b||_{L^{q1}} ||(-Delta)^{s/2}f||_{L^{q2}})

with 1/p = 1/p1 + 1/p2 = 1/q1 + 1/q2.

For SQG with s=1 (the fractional Laplacian order), this gives:
  ||[(-Delta)^{1/2}, theta^{below}]theta_k||_{L^2}
    <= C ||grad theta^{below}||_{L^p} ||theta_k||_{L^q}

The key gain: grad(theta^{below}) involves grad(theta * min(1,lambda/|theta|)),
which is bounded by lambda * |grad theta| / |theta| on the support. But since
theta is a SCALAR, the truncation theta^{below} = theta * min(1, lambda/|theta|)
preserves more structure than the vector case.

Specifically for SQG: the commutator structure provides an EXTRA POWER of U_{k-1}.
Instead of:
  |I_k| <= C^k U_{k-1}^{4/3}    (what standard Holder gives)

the commutator estimate gives:
  |I_k| <= C^k U_{k-1}^{3/2}    (the critical exponent!)

This extra 1/6 power (4/3 -> 3/2) comes from the regularity gain of the commutator:
[R^perp, theta^below] gains one derivative relative to the direct product, and this
derivative exactly compensates the Chebyshev loss.
""")

    print("""
3b. THE ANALOGOUS OBJECT FOR NS
================================

For NS, the bottleneck is P^{21} = R_iR_j(u_i^{above} u_j^{below}).

Can we write this as a commutator? Let's try:

  R_iR_j(u_i^{above} u_j^{below}) = R_iR_j(u_i^{above} * u_j^{below})

Using the identity R_iR_j(fg) = f * R_iR_j(g) + [R_iR_j, f]g:

  R_iR_j(u_i^{above} * u_j^{below}) = u_i^{above} * R_iR_j(u_j^{below})
                                        + [R_iR_j, u_i^{above}] * u_j^{below}

Hmm, but the sum over i makes this more complex. Let's sum:

  P^{21} = sum_{ij} R_iR_j(u_i^{above} u_j^{below})
         = sum_j R_j[ sum_i R_i(u_i^{above} u_j^{below}) ]

For the inner sum (fixing j):
  sum_i R_i(u_i^{above} u_j^{below}) = sum_i R_i(u_i^{above} * u_j^{below})
  = sum_i [u_j^{below} * R_i(u_i^{above}) + [R_i, u_j^{below}] u_i^{above}]
  = u_j^{below} * R . (u^{above}) + sum_i [R_i, u_j^{below}] u_i^{above}

Now R . (u^{above}) = (-Delta)^{-1/2} div(u^{above}).

If u^{above} were divergence-free, R . (u^{above}) = 0 and we'd be left with
pure commutator terms. BUT as computed in Task 2:

  div(u^{above}) = -div(u^{below}) = lambda * (u . grad|u|) / |u|^2  ≠ 0

So the decomposition is:

  P^{21} = sum_j R_j[u_j^{below} * (-Delta)^{-1/2} div(u^{above})]
         + sum_{ij} R_j[[R_i, u_j^{below}] u_i^{above}]

FIRST TERM: This is a "remainder" from the non-zero divergence.
  It involves (-Delta)^{-1/2} div(u^{above}) — a zeroth-order operator on u^{above}.
  This term has the SAME size as the original P^{21} in L^p norms.
  It is NOT a commutator and does NOT gain regularity.

SECOND TERM: These ARE commutators [R_i, u_j^{below}] u_i^{above}.
  By Coifman-Rochberg-Weiss (1976):
    [R_i, b]f in L^p for 1 < p < infty if b in BMO and f in L^p
    with ||[R_i, b]f||_p <= C ||b||_{BMO} ||f||_p

  Here b = u_j^{below} (bounded, so in BMO) and f = u_i^{above}.
  So [R_i, u_j^{below}]u_i^{above} in L^p for the same p as u^{above}.

  BUT: this gives the SAME L^p bound as the direct product estimate.
  CRW says ||[R_i, b]f||_p <= C ||b||_{BMO} ||f||_p, and for bounded b:
  ||b||_{BMO} <= 2||b||_{L^infty} <= 2*lambda.
  So ||[R_i, u_j^{below}]u_i^{above}||_p <= C*lambda*||u^{above}||_p.

  This is EXACTLY what CZ theory gives for R_i(u_j^{below} * u_i^{above}).
  No improvement.

The commutator does NOT gain a derivative here. WHY?

SQG vs NS — the structural difference:
  - In SQG: the drift u = R^perp(theta) is a ZEROTH-order operator on theta.
    The commutator [R^perp, theta^below] gains one derivative because R^perp
    is a zeroth-order CZ operator and the commutator of two zeroth-order operators
    can be a smoothing (-1 order) operator.

  - In NS: the pressure P^{21} involves R_iR_j, a ZEROTH-order operator, applied
    to a PRODUCT of velocity components. The commutator [R_i, u_j^{below}] is
    also zeroth order on L^p (by CRW), so it gives the same bounds.

    The fundamental issue: in SQG, the bilinear form is
      theta_k * (R^perp theta^{below} . grad theta_k)
    which has a NATURAL commutator structure because the operator R^perp and the
    multiplier theta^{below} can be separated by commutation.

    In NS, the bilinear form is
      d_k * P^{21} * 1_{v_k > 0}
    where P^{21} = R_iR_j(u^{above} tensor u^{below}).
    The double Riesz transform acts on a PRODUCT — there's no single multiplier
    to commute past because BOTH factors are dynamic (velocity-dependent).
""")

    print("""
3c. COIFMAN-ROCHBERG-WEISS APPLICABILITY
=========================================

CRW (1976) Theorem: If b in BMO(R^n) and T is a Calderon-Zygmund operator, then
  [T, b]f = T(bf) - b*T(f)
is bounded on L^p(R^n) for 1 < p < infty, with:
  ||[T, b]f||_p <= C_p ||b||_{BMO} ||f||_p

Applied to our setting with T = R_iR_j, b = u_j^{below}, f = u_i^{above}:

  ||[R_iR_j, u_j^{below}] u_i^{above}||_{L^p} <= C ||u_j^{below}||_{BMO} ||u_i^{above}||_{L^p}

Since u^{below} is bounded (|u^{below}| <= lambda_{k-1}), it is in BMO with
  ||u^{below}||_{BMO} <= 2 ||u^{below}||_{L^infty} <= 2 lambda_{k-1}

So: ||[R_iR_j, u_j^{below}] u_i^{above}||_{L^p} <= C lambda_{k-1} ||u^{above}||_{L^p}

This is the SAME bound we get from the direct estimate:
  ||R_iR_j(u_i^{above} u_j^{below})||_{L^p} <= C ||u^{above} u^{below}||_{L^p}
                                                <= C lambda_{k-1} ||u^{above}||_{L^p}

CONCLUSION: CRW applies but provides NO improvement. The commutator bound and
the direct CZ bound give identical exponents in the De Giorgi recurrence.

WHY CRW DOESN'T HELP: CRW trades ||b||_{L^infty} for ||b||_{BMO}, which for
bounded functions is the same (up to a factor 2). The "gain" in CRW is useful
when b is UNBOUNDED but in BMO (like log|x|). For our bounded u^{below},
the BMO norm is no better than L^infty.

COULD A HIGHER-ORDER COMMUTATOR HELP?

The Coifman-Meyer-Stein theory of paraproducts gives:
  T(fg) = T_f(g) + T_g(f) + R(f,g)

where T_f is a paraproduct and R is a remainder with better regularity.
But the regularity gain is in SOBOLEV regularity (R maps L^p x L^q -> W^{s,r}
for s > 0), not in the L^p exponent. This would help if the bottleneck were
a Sobolev regularity deficit, but our bottleneck is an INTEGRABILITY deficit
(L^{10/3} vs L^4). Sobolev gains don't help with this.
""")

    # Numerical verification
    print("=" * 70)
    print("NUMERICAL VERIFICATION: Commutator regularity test")
    print("=" * 70)

    N = 64
    nu = 0.01
    solver = NavierStokesSolver(N, nu)

    # Taylor-Green evolved
    ux0 = np.sin(solver.X) * np.cos(solver.Y) * np.cos(solver.Z)
    uy0 = -np.cos(solver.X) * np.sin(solver.Y) * np.cos(solver.Z)
    uz0 = np.zeros_like(solver.X)
    ux_hat, uy_hat, uz_hat = solver.project(
        solver.to_spectral(ux0), solver.to_spectral(uy0), solver.to_spectral(uz0))
    ux_hat, uy_hat, uz_hat = solver.run(ux_hat, uy_hat, uz_hat, T_final=2.0)

    ux = solver.to_physical(ux_hat)
    uy = solver.to_physical(uy_hat)
    uz = solver.to_physical(uz_hat)
    u_mag = np.sqrt(ux**2 + uy**2 + uz**2)
    u_max = np.max(u_mag)

    vol = (2 * np.pi)**3
    dV = vol / N**3

    lambda_k = 0.5 * u_max
    u_safe = np.where(u_mag > 1e-14, u_mag, 1.0)
    above = u_mag > lambda_k

    ratio_below = np.where(above, lambda_k / u_safe, 1.0)
    ratio_below[u_mag < 1e-14] = 0.0
    ratio_above = np.where(above, (u_mag - lambda_k) / u_safe, 0.0)
    ratio_above[u_mag < 1e-14] = 0.0

    u_below = [ux * ratio_below, uy * ratio_below, uz * ratio_below]
    u_above = [ux * ratio_above, uy * ratio_above, uz * ratio_above]
    u_above_hat = [fftn(u_above[i]) for i in range(3)]

    # Compute: direct P^{21} vs commutator decomposition
    K = [solver.KX, solver.KY, solver.KZ]

    # Direct: P^{21} = sum_{ij} R_iR_j(u_i^above * u_j^below)
    P21_hat = np.zeros((N, N, N), dtype=complex)
    for i in range(3):
        for j in range(3):
            prod_hat = fftn(u_above[i] * u_below[j])
            P21_hat += (-K[i] * K[j]) * prod_hat / solver.K2_safe
    P21_hat[0, 0, 0] = 0
    P21 = ifftn(P21_hat).real

    # Commutator part: sum_{ij} [R_iR_j, u_j^below] u_i^above
    comm_part = np.zeros((N, N, N))
    for i in range(3):
        for j in range(3):
            comm_ij = compute_commutator_RiRj_b(solver, u_below[j], u_above_hat[i], i, j)
            comm_part += comm_ij

    # Remainder: P^{21} - commutator part = sum_{ij} u_j^below * R_iR_j(u_i^above)
    remainder = P21 - comm_part

    # Check: remainder should equal sum_j u_j^below * R_j[sum_i R_i(u_i^above)]
    # = sum_j u_j^below * R_j[(-Delta)^{-1/2} div(u^above)]
    # This is the non-zero-divergence piece.

    P21_L2 = np.sqrt(np.sum(P21**2) * dV)
    comm_L2 = np.sqrt(np.sum(comm_part**2) * dV)
    rem_L2 = np.sqrt(np.sum(remainder**2) * dV)

    print(f"\n  lambda = {lambda_k:.4f} ({lambda_k/u_max:.0%} of max|u|)")
    print(f"  ||P^{{21}}||_L2 = {P21_L2:.6f}")
    print(f"  ||commutator part||_L2 = {comm_L2:.6f}")
    print(f"  ||remainder (div-error)||_L2 = {rem_L2:.6f}")
    print(f"  Ratio remainder/total = {rem_L2/max(P21_L2,1e-30):.4f}")
    print(f"  Ratio commutator/total = {comm_L2/max(P21_L2,1e-30):.4f}")

    # Check if commutator has better Sobolev regularity (higher spectral decay)
    P21_spectrum = np.zeros(N//3)
    comm_spectrum = np.zeros(N//3)
    rem_spectrum = np.zeros(N//3)

    P21_hat_check = fftn(P21)
    comm_hat = fftn(comm_part)
    rem_hat = fftn(remainder)

    for shell in range(1, N//3):
        mask = (solver.K_mag >= shell - 0.5) & (solver.K_mag < shell + 0.5)
        P21_spectrum[shell] = np.sum(np.abs(P21_hat_check[mask])**2)
        comm_spectrum[shell] = np.sum(np.abs(comm_hat[mask])**2)
        rem_spectrum[shell] = np.sum(np.abs(rem_hat[mask])**2)

    print(f"\n  Spectral decay comparison (energy in shell k):")
    print(f"  {'k':>4s}  {'|P21|^2':>12s}  {'|comm|^2':>12s}  {'|rem|^2':>12s}  {'comm/P21':>10s}")
    for shell in [1, 2, 4, 8, 12, 16, 20]:
        if shell < N//3 and P21_spectrum[shell] > 0:
            ratio = comm_spectrum[shell] / max(P21_spectrum[shell], 1e-30)
            print(f"  {shell:4d}  {P21_spectrum[shell]:12.4e}  {comm_spectrum[shell]:12.4e}  {rem_spectrum[shell]:12.4e}  {ratio:10.4f}")

    print("""
INTERPRETATION:
If the commutator part had better regularity than P^{21} overall, its spectrum
would decay FASTER at high k. If the ratio comm/P21 stays constant or grows,
there is NO regularity gain from the commutator decomposition.
""")

    # Also compute the single-Riesz commutator for comparison
    print("\nSingle Riesz commutator test: [R_i, u_1^below] u_1^above")
    single_comm = compute_commutator_Ri_b(solver, u_below[0], u_above_hat[0], 0)
    direct_Ri = ifftn(-1j * K[0] * fftn(u_above[0] * u_below[0]) /
                       np.where(solver.K_mag > 0, solver.K_mag, 1.0)).real

    sc_L2 = np.sqrt(np.sum(single_comm**2) * dV)
    dr_L2 = np.sqrt(np.sum(direct_Ri**2) * dV)
    print(f"  ||[R_1, u_1^below] u_1^above||_L2 = {sc_L2:.6f}")
    print(f"  ||R_1(u_1^above * u_1^below)||_L2 = {dr_L2:.6f}")
    print(f"  Ratio: {sc_L2/max(dr_L2, 1e-30):.4f}")
    print("  (CRW bound predicts this ratio ~ ||u^below||_BMO ~ lambda, which is O(1))")

    print("\n[TASK 3 COMPLETE]")


if __name__ == '__main__':
    main()
