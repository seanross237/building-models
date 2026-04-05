"""
Fast kernel comparison: zeta Xi vs DH Xi on the critical line.

Instead of computing the full Fourier transform (expensive), we compare
the Xi functions directly on the critical line and analyze their properties.
"""

import mpmath
import numpy as np
import json

mpmath.mp.dps = 25

###############################################################################
# 1. Compute Xi_zeta(1/2+it) and Xi_DH(1/2+it) on the critical line
###############################################################################

def xi_zeta(t):
    """Xi(1/2+it) for the Riemann zeta function. Should be real for real t."""
    s = mpmath.mpc(0.5, t)
    val = 0.5 * s * (s-1) * mpmath.power(mpmath.pi, -s/2) * mpmath.gamma(s/2) * mpmath.zeta(s)
    return val

# DH setup
sqrt5 = mpmath.sqrt(5)
kappa = (mpmath.sqrt(10 - 2*sqrt5) - 2) / (sqrt5 - 1)
c1 = (1 - mpmath.mpc(0,1)*kappa) / 2
c2 = (1 + mpmath.mpc(0,1)*kappa) / 2

chi1_table = {0: mpmath.mpc(0), 1: mpmath.mpc(1), 2: mpmath.mpc(0,1), 3: mpmath.mpc(0,-1), 4: mpmath.mpc(-1)}

def L_chi(s, chi_func, N=5000):
    result = mpmath.mpc(0)
    for n in range(1, N+1):
        c = chi_func(n % 5)
        if c != 0:
            result += c * mpmath.power(n, -s)
    return result

def xi_dh(t):
    """Xi_DH(1/2+it). Uses completed form for chi mod 5 (odd character, a=1)."""
    s = mpmath.mpc(0.5, t)
    # Completed L-function for odd character mod 5:
    # Lambda(s, chi) = (5/pi)^{(s+1)/2} * Gamma((s+1)/2) * L(s, chi)
    factor = mpmath.power(5/mpmath.pi, (s+1)/2) * mpmath.gamma((s+1)/2)

    L1 = L_chi(s, lambda r: chi1_table[r], 3000)
    L2 = L_chi(s, lambda r: mpmath.conj(chi1_table[r]), 3000)

    dh_val = c1 * L1 + c2 * L2
    return factor * dh_val

###############################################################################
# 2. Sample Xi on the critical line
###############################################################################

print("=== Xi functions on the critical line ===\n")
print(f"{'t':>6s}  {'Xi_zeta (real)':>14s}  {'Re(Xi_DH)':>12s}  {'Im(Xi_DH)':>12s}  {'|Xi_DH|':>10s}")
print("-" * 60)

t_vals = np.linspace(0.1, 40, 80)
xi_z_vals = []
xi_dh_re_vals = []
xi_dh_im_vals = []

for t in t_vals:
    xz = xi_zeta(t)
    xdh = xi_dh(t)
    xi_z_vals.append(float(mpmath.re(xz)))
    xi_dh_re_vals.append(float(mpmath.re(xdh)))
    xi_dh_im_vals.append(float(mpmath.im(xdh)))
    if t < 5 or t > 35 or abs(t - 14.1) < 0.5 or abs(t - 21.0) < 0.5:
        print(f"{t:6.2f}  {float(mpmath.re(xz)):14.6f}  {float(mpmath.re(xdh)):12.6f}  {float(mpmath.im(xdh)):12.6f}  {float(abs(xdh)):10.6f}")

###############################################################################
# 3. Zero structure comparison
###############################################################################

print("\n=== Zeros of Xi_zeta on the critical line ===")
print("(These are the nontrivial zeta zeros)\n")

# Find sign changes of Xi_zeta (which is real on the critical line)
zeta_zeros = []
for i in range(len(t_vals)-1):
    if xi_z_vals[i] * xi_z_vals[i+1] < 0:
        # Bisect to find zero
        a, b = t_vals[i], t_vals[i+1]
        for _ in range(50):
            mid = (a+b)/2
            if float(mpmath.re(xi_zeta(mid))) * xi_z_vals[i] > 0:
                a = mid
            else:
                b = mid
        zeta_zeros.append((a+b)/2)

print("Zeta zeros found:")
for z in zeta_zeros:
    print(f"  t = {z:.6f}")

print(f"\n(Known first zeros: 14.1347, 21.0220, 25.0109, 30.4249, 32.9351, 37.5862)")

###############################################################################
# 4. Zero structure of Xi_DH
###############################################################################

print("\n=== Zeros of |Xi_DH| on the critical line ===")
print("(The DH function has zeros both ON and OFF the critical line)\n")

# For DH, Xi_DH(1/2+it) is complex, so we look for |Xi_DH| minima
dh_zeros_online = []
xi_dh_abs = [np.sqrt(r**2 + im**2) for r, im in zip(xi_dh_re_vals, xi_dh_im_vals)]

for i in range(1, len(t_vals)-1):
    if xi_dh_abs[i] < 0.5 and xi_dh_abs[i] < xi_dh_abs[i-1] and xi_dh_abs[i] < xi_dh_abs[i+1]:
        dh_zeros_online.append((t_vals[i], xi_dh_abs[i]))

print("DH near-zeros on critical line:")
for z, v in dh_zeros_online:
    print(f"  t = {z:.4f}, |Xi_DH| = {v:.6f}")

###############################################################################
# 5. Compare the oscillation structure
###############################################################################

print("\n=== Oscillation Structure Comparison ===")

# Count zero crossings of Re(Xi_zeta) and Re(Xi_DH) in the range
zeta_crossings = sum(1 for i in range(len(t_vals)-1) if xi_z_vals[i] * xi_z_vals[i+1] < 0)
dh_re_crossings = sum(1 for i in range(len(t_vals)-1) if xi_dh_re_vals[i] * xi_dh_re_vals[i+1] < 0)

print(f"In [0.1, 40]:")
print(f"  Xi_zeta sign changes: {zeta_crossings}")
print(f"  Re(Xi_DH) sign changes: {dh_re_crossings}")
print(f"  Expected zeta zeros: ~6 (N(40) ~ (40/2pi)*log(40/2pi) - 40/(2pi) ~ 6.4)")

###############################################################################
# 6. Key test: is Xi_zeta log-concave on the critical line?
###############################################################################

print("\n=== Log-concavity test for |Xi| on the critical line ===\n")

# Xi_zeta(1/2+it) is real, but it changes sign. |Xi_zeta| is not meaningful for log-concavity
# between zeros. Instead, we test Xi_zeta itself in the positive lobes.

# For the Polya kernel Phi(u), recall Phi is the cosine transform of Xi:
# Phi(u) = 2 integral_0^inf Xi(1/2+it) cos(ut) dt
# The PF2 property of Phi is NOT the same as log-concavity of Xi.
# But the shape of Xi on the critical line reveals the "envelope" structure.

# Let's look at the positive envelope of |Xi|
print("Envelope of |Xi_zeta| at local maxima:")
for i in range(1, len(t_vals)-1):
    if abs(xi_z_vals[i]) > abs(xi_z_vals[i-1]) and abs(xi_z_vals[i]) > abs(xi_z_vals[i+1]):
        if abs(xi_z_vals[i]) > 0.1:
            print(f"  t = {t_vals[i]:.2f}, |Xi_zeta| = {abs(xi_z_vals[i]):.4f}")

###############################################################################
# 7. The "amplitude mismatch" between zeta and DH
###############################################################################

print("\n=== Amplitude comparison: Xi_zeta vs Xi_DH ===\n")

# The key to the Euler product argument is that |Xi_zeta| grows in a controlled way
# while |Xi_DH| has irregular amplitude fluctuations

z_amplitudes = np.array([abs(v) for v in xi_z_vals])
dh_amplitudes = np.array(xi_dh_abs)

print(f"Xi_zeta: mean |Xi| = {np.mean(z_amplitudes):.4f}, std = {np.std(z_amplitudes):.4f}, max = {np.max(z_amplitudes):.4f}")
print(f"Xi_DH:   mean |Xi| = {np.mean(dh_amplitudes):.4f}, std = {np.std(dh_amplitudes):.4f}, max = {np.max(dh_amplitudes):.4f}")
print(f"\nCoeff of variation (std/mean):")
print(f"  Xi_zeta: {np.std(z_amplitudes)/np.mean(z_amplitudes):.4f}")
print(f"  Xi_DH:   {np.std(dh_amplitudes)/np.mean(dh_amplitudes):.4f}")

# Compute the ratio of successive maxima (growth rate)
z_maxima = []
dh_maxima = []
for i in range(1, len(t_vals)-1):
    if abs(xi_z_vals[i]) > abs(xi_z_vals[i-1]) and abs(xi_z_vals[i]) > abs(xi_z_vals[i+1]):
        z_maxima.append((t_vals[i], abs(xi_z_vals[i])))
    if xi_dh_abs[i] > xi_dh_abs[i-1] and xi_dh_abs[i] > xi_dh_abs[i+1]:
        dh_maxima.append((t_vals[i], xi_dh_abs[i]))

if len(z_maxima) >= 2:
    print(f"\nZeta maxima growth:")
    for i in range(1, min(6, len(z_maxima))):
        ratio = z_maxima[i][1] / z_maxima[i-1][1]
        print(f"  t={z_maxima[i][0]:.1f}: |Xi|={z_maxima[i][1]:.4f}, ratio to prev = {ratio:.4f}")

if len(dh_maxima) >= 2:
    print(f"\nDH maxima growth:")
    for i in range(1, min(6, len(dh_maxima))):
        ratio = dh_maxima[i][1] / dh_maxima[i-1][1]
        print(f"  t={dh_maxima[i][0]:.1f}: |Xi|={dh_maxima[i][1]:.4f}, ratio to prev = {ratio:.4f}")

###############################################################################
# 8. Save results
###############################################################################

results = {
    "t_values": t_vals.tolist(),
    "xi_zeta_real": xi_z_vals,
    "xi_dh_real": xi_dh_re_vals,
    "xi_dh_imag": xi_dh_im_vals,
    "xi_dh_abs": xi_dh_abs,
    "zeta_zeros_found": zeta_zeros,
    "dh_zeros_online": [(float(z), float(v)) for z, v in dh_zeros_online],
}

with open("/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/euler-product-repulsion/xi_comparison_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nResults saved.")
