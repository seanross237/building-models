"""
Analytical comparison: exact formulas for the post-quench correlators.

C_QM(t) = (2n+1)/(4w) [cos(w_+ t) + cos(w_- t)]
         = (2n+1)/(2w) cos(w_avg t) cos(delta_w t / 2)

C_global(t) = (2n+1)/(2w) cos(w t)

where n = 1/(e^{beta w} - 1), w_+ = sqrt(w^2+lam), w_- = sqrt(w^2-lam)
      w_avg = (w_+ + w_-)/2, delta_w = w_+ - w_-
"""

import numpy as np

omega = 1.0
beta = 2.0
n_bar = 1.0 / (np.exp(beta * omega) - 1)
amplitude = (2*n_bar + 1) / (2*omega)

print("=" * 70)
print("ANALYTICAL COMPARISON — Post-Quench Correlator Formulas")
print(f"omega={omega}, beta={beta}, n_bar={n_bar:.6f}")
print(f"Common amplitude: (2n+1)/(2w) = {amplitude:.6f}")
print("=" * 70)

print(f"\nFormulas:")
print(f"  C_QM(t)     = {amplitude:.4f}/2 * [cos(w_+ t) + cos(w_- t)]")
print(f"              = {amplitude:.4f} * cos(w_avg t) * cos(dw/2 t)")
print(f"  C_global(t) = {amplitude:.4f} * cos(w t)")
print(f"  C_local(t)  = C_global(t)  [for product state]")

print(f"\n{'='*70}")
print("Discrepancy Analysis")
print(f"{'='*70}")

for lam in [0.1, 0.2, 0.3, 0.5]:
    w_plus = np.sqrt(omega**2 + lam)
    w_minus = np.sqrt(omega**2 - lam)
    w_avg = (w_plus + w_minus) / 2
    delta_w = w_plus - w_minus

    print(f"\nlambda = {lam}:")
    print(f"  w_+ = {w_plus:.6f}, w_- = {w_minus:.6f}")
    print(f"  w_avg = {w_avg:.6f}, delta_w = {delta_w:.6f}")
    print(f"  w_avg - omega = {w_avg - omega:.6f}  (shift of carrier frequency)")

    # The discrepancy has two components:
    # 1. Carrier frequency shift: w_avg != omega (for finite lambda)
    # 2. Beat envelope: cos(delta_w/2 * t) modulates C_QM

    # Compute ||C_QM - C_global|| / ||C_QM|| analytically on [0, T] for large T
    # Using time-average: <cos^2(at)> = 1/2
    # ||C_QM||^2 = amplitude^2/4 * integral[cos(w_+t) + cos(w_-t)]^2 dt
    #            = amplitude^2/4 * integral[cos^2(w_+t) + 2cos(w_+t)cos(w_-t) + cos^2(w_-t)] dt
    #            = amplitude^2/4 * [T/2 + 0 + T/2]  (for large T, the cross term averages to 0)
    #            = amplitude^2 * T / 4
    # So <C_QM^2> = amplitude^2 / 4  (time-averaged squared value)

    # ||C_global||^2 = amplitude^2 * integral cos^2(wt) dt = amplitude^2 * T/2
    # <C_global^2> = amplitude^2 / 2

    # Cross term: <C_QM * C_global> = amplitude^2/2 * integral[cos(w_+t) + cos(w_-t)]cos(wt)/(2) dt
    # Wait: C_QM = amplitude/2 * [cos(w_+t) + cos(w_-t)]
    # C_global = amplitude * cos(wt)
    # <C_QM * C_global> = amplitude^2/2 * <[cos(w_+t) + cos(w_-t)] cos(wt)>
    # = amplitude^2/2 * [<cos(w_+t)cos(wt)> + <cos(w_-t)cos(wt)>]
    # For w_+ != w and w_- != w (which is true for lambda > 0):
    # <cos(at)cos(bt)> = 0 for a != b (time average over long T)
    # SO <C_QM * C_global> = 0 for large T!

    # Therefore: ||C_QM - C_global||^2 = ||C_QM||^2 + ||C_global||^2 - 2<C_QM, C_global>
    #            = amplitude^2 * T/4 + amplitude^2 * T/2 - 0
    #            = 3/4 * amplitude^2 * T

    # And: ||C_QM - C_global|| / ||C_QM|| = sqrt(3/4 * T / (T/4)) = sqrt(3)
    # Hmm that's not right, it's way too large. The issue is the T dependence should cancel in the ratio.

    # Let me redo more carefully.
    # For large T with uniform grid:
    # ||f||^2 ≈ (T/N) sum f(t_i)^2 ≈ T * <f^2>
    # So ||f-g||/||f|| = sqrt(<(f-g)^2>/<f^2>)

    # <C_QM^2> = amplitude^2/4 * <[cos(w_+t) + cos(w_-t)]^2>
    #           = amplitude^2/4 * [<cos^2(w_+t)> + 2<cos(w_+t)cos(w_-t)> + <cos^2(w_-t)>]
    #           = amplitude^2/4 * [1/2 + 0 + 1/2]  = amplitude^2/4

    # <C_global^2> = amplitude^2 * <cos^2(wt)> = amplitude^2/2

    # <C_QM * C_global> = amplitude^2/2 * <[cos(w_+t)+cos(w_-t)] cos(wt)> = 0

    # <(C_QM - C_global)^2> = <C_QM^2> - 2<C_QM C_global> + <C_global^2>
    #                       = amplitude^2/4 + amplitude^2/2 = 3*amplitude^2/4

    # ||C_QM - C_global||/||C_QM|| = sqrt(3/4 amplitude^2 / (amplitude^2/4)) = sqrt(3) ≈ 1.732

    # So for all lambda > 0, the asymptotic (large T) relative discrepancy is sqrt(3) ≈ 1.732!
    # This is because for ANY lambda > 0, the frequencies are incommensurate.

    # But our computation window is [0, 4*pi], not infinite. Let's compute numerically.
    N_tau = 500
    tau_arr = np.linspace(0, 4*np.pi, N_tau)
    C_QM_a = amplitude/2 * (np.cos(w_plus * tau_arr) + np.cos(w_minus * tau_arr))
    C_gl_a = amplitude * np.cos(omega * tau_arr)

    disc = np.linalg.norm(C_QM_a - C_gl_a) / np.linalg.norm(C_QM_a)
    print(f"  Analytical discrepancy (T=4pi): {disc:.8f}")

    # Also on [0, 16*pi]
    tau_long = np.linspace(0, 16*np.pi, 2000)
    C_QM_long = amplitude/2 * (np.cos(w_plus * tau_long) + np.cos(w_minus * tau_long))
    C_gl_long = amplitude * np.cos(omega * tau_long)
    disc_long = np.linalg.norm(C_QM_long - C_gl_long) / np.linalg.norm(C_QM_long)
    print(f"  Analytical discrepancy (T=16pi): {disc_long:.8f}")
    print(f"  Asymptotic (T->inf): sqrt(3) = {np.sqrt(3):.8f}")

    # Beat period
    T_beat = 2*np.pi / (delta_w/2) if delta_w > 0 else float('inf')
    print(f"  Beat period: T_beat = 2pi/(dw/2) = {T_beat:.4f}")
    print(f"  T_beat / T_window(4pi) = {T_beat/(4*np.pi):.2f}")
    print(f"  T_beat / T_window(16pi) = {T_beat/(16*np.pi):.2f}")


print(f"\n{'='*70}")
print("KEY INSIGHT: Structural vs Quantitative Discrepancy")
print(f"{'='*70}")
print(f"""
The discrepancy between C_QM and C_global_TTH for the post-quench state is STRUCTURAL:

  C_QM(t)     has frequencies: w_+ = sqrt(w^2+lam), w_- = sqrt(w^2-lam)
  C_global(t) has frequency:   w = {omega}

These are completely different frequency contents. The modular flow generates
evolution under the PRE-QUENCH Hamiltonian (uncoupled), while actual dynamics
use the POST-QUENCH Hamiltonian (coupled, with normal modes).

Using sum-to-product:
  C_QM(t) = A * cos(w_avg * t) * cos(dw/2 * t)

The beating pattern cos(dw/2 * t) is completely absent from C_global_TTH.
The carrier frequency w_avg ≈ w - lam^2/(8*w^3) + ... is also shifted.

For the modular flow to be physically correct, it would need to "know" about
the coupling that was turned on during the quench. But the modular Hamiltonian
is determined purely by the STATE, which was prepared before the quench.

This is the fundamental limitation of TTH for non-equilibrium states:
the modular time evolution is determined by the state's preparation history,
not by the actual Hamiltonian governing the dynamics.
""")

# Comparison: Gibbs vs post-quench discrepancies
print(f"\n{'='*70}")
print("COMPARISON TABLE: Gibbs State vs Post-Quench State")
print(f"{'='*70}")
print(f"{'lam':>5}  {'Gibbs: global':>16}  {'Quench: global':>16}  {'Quench: local':>16}")
print("-" * 65)
for lam in [0.0, 0.1, 0.2, 0.3, 0.5]:
    gibbs_disc = 0.0  # always zero for Gibbs state
    w_plus = np.sqrt(omega**2 + lam)
    w_minus = np.sqrt(omega**2 - lam) if omega**2 > lam else 0.0

    tau_arr = np.linspace(0, 4*np.pi, 500)
    C_QM_a = amplitude/2 * (np.cos(w_plus * tau_arr) + np.cos(w_minus * tau_arr))
    C_gl_a = amplitude * np.cos(omega * tau_arr)

    quench_disc = np.linalg.norm(C_QM_a - C_gl_a) / np.linalg.norm(C_QM_a) if lam > 0 else 0.0
    # For product state, local = global
    print(f"{lam:5.2f}  {gibbs_disc:16.10f}  {quench_disc:16.10f}  {quench_disc:16.10f}")

print(f"\nFor Gibbs state: C_global = C_QM always (modular flow = Hamiltonian flow)")
print(f"For post-quench: C_global != C_QM for lambda > 0 (different frequencies)")
print(f"For post-quench product state: C_global = C_local (no entanglement correction)")

print("\nDONE — analytical comparison")
