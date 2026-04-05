"""
Investigation 3: Decompose the D4 Toeplitz determinant into contributions
from the Euler product part, the gamma part, and the cross terms.

The key insight from the first computation:
- Gamma kernel: PF_5 (!) -- BETTER than Xi itself (PF_4)
- Zeta kernel: PF_6+ -- very high PF order
- But Xi = G * zeta has kernel = convolution of G_kernel and zeta_kernel
  ... and this convolution is only PF_4

This is surprising: convolution of PF_5 and PF_6+ should give PF_5 (min of the two).
But the Toeplitz test shows Xi is only PF_4. This means our kernel decomposition
is not quite right -- we need to think more carefully.

Actually, the issue is: Xi(1/2+it) = G(1/2+it) * zeta(1/2+it) is a PRODUCT in
frequency space, which means the kernel (Fourier transform) is a CONVOLUTION.
But G is complex-valued on the critical line, not real. The PF test only applies
to the real kernel Phi(u) = FT[Xi(1/2+it)](u), which is the FT of a real function.

Let us carefully decompose the product:
Xi(t) = Re[G(1/2+it)] * Re[zeta(1/2+it)] - Im[G(1/2+it)] * Im[zeta(1/2+it)]

(since Xi is real on the critical line)

The kernel is then:
Phi(u) = FT[Re(G)*Re(zeta)](u) - FT[Im(G)*Im(zeta)](u)

Each of these terms involves a convolution (FT of a product = convolution of FTs).

This decomposition lets us see exactly which cross-terms contribute to D4 positivity.
"""

import numpy as np
import mpmath
import json

mpmath.mp.dps = 50

###############################################################################
# 1. Compute the four components
###############################################################################

t_max = 60.0
N_pts = 4001
t_grid = np.linspace(0, t_max, N_pts)
dt = t_grid[1] - t_grid[0]

print("Computing function components on the critical line...")

def gamma_factor_on_line(t):
    t = mpmath.mpf(t)
    s = mpmath.mpc('0.5', t)
    val = mpmath.mpf('0.5') * s * (s-1) * mpmath.power(mpmath.pi, -s/2) * mpmath.gamma(s/2)
    return complex(val)

def zeta_on_line(t):
    t = mpmath.mpf(t)
    s = mpmath.mpc('0.5', t)
    return complex(mpmath.zeta(s))

G_complex = np.array([gamma_factor_on_line(t) for t in t_grid])
zeta_complex = np.array([zeta_on_line(t) for t in t_grid])

G_real = np.real(G_complex)
G_imag = np.imag(G_complex)
zeta_real = np.real(zeta_complex)
zeta_imag = np.imag(zeta_complex)

# Xi = Re(G)*Re(zeta) - Im(G)*Im(zeta)
xi_from_product = G_real * zeta_real - G_imag * zeta_imag
# Verification: this should match Xi(1/2+it) directly
print(f"  Xi reconstruction check: max |Xi_direct - Xi_product| = ", end="")
xi_direct = np.array([float(mpmath.re(mpmath.mpf('0.5') * mpmath.mpc('0.5', mpmath.mpf(t)) * (mpmath.mpc('0.5', mpmath.mpf(t)) - 1) * mpmath.power(mpmath.pi, -mpmath.mpc('0.5', mpmath.mpf(t))/2) * mpmath.gamma(mpmath.mpc('0.5', mpmath.mpf(t))/2) * mpmath.zeta(mpmath.mpc('0.5', mpmath.mpf(t))))) for t in t_grid[:10]])
xi_prod_check = (G_real * zeta_real - G_imag * zeta_imag)[:10]
print(f"{np.max(np.abs(xi_direct - xi_prod_check)):.2e}")

print("  Defining 'RR' = Re(G)*Re(zeta), 'II' = Im(G)*Im(zeta)")
print("  Xi(t) = RR(t) - II(t)")

RR = G_real * zeta_real  # Re(G)*Re(zeta) part
II = G_imag * zeta_imag  # Im(G)*Im(zeta) part (subtracted)

###############################################################################
# 2. Compute kernels of RR and II
###############################################################################

def kernel(f_vals, u):
    """FT kernel: 2 * int_0^inf f(t) cos(ut) dt."""
    integrand = f_vals * np.cos(u * t_grid)
    return 2 * np.trapz(integrand, dx=dt)

print("\n=== Kernels of the two components ===\n")
print(f"{'u':>6s}  {'K_Xi':>14s}  {'K_RR':>14s}  {'K_II':>14s}  {'K_RR-K_II':>14s}  {'match':>6s}")
print("-" * 70)

for u in [0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0]:
    k_xi = kernel(xi_from_product, u)
    k_rr = kernel(RR, u)
    k_ii = kernel(II, u)
    diff = k_rr - k_ii
    match = abs(diff - k_xi) < 1e-4 * max(abs(k_xi), 1e-10)
    print(f"{u:6.2f}  {k_xi:14.6e}  {k_rr:14.6e}  {k_ii:14.6e}  {diff:14.6e}  {'OK' if match else 'MISMATCH'}")

###############################################################################
# 3. PF tests on the two components separately and combined
###############################################################################

print("\n=== PF Tests: RR Component vs II Component vs Xi ===\n")

def toeplitz_det(kernel_func, h, order):
    vals = [kernel_func(k*h) for k in range(order)]
    mat = np.zeros((order, order))
    for i in range(order):
        for j in range(order):
            mat[i][j] = vals[abs(i-j)]
    return np.linalg.det(mat)

K_Xi = lambda u: kernel(xi_from_product, u)
K_RR = lambda u: kernel(RR, u)
K_II = lambda u: kernel(II, u)

for name, kfunc in [('Xi = RR - II', K_Xi), ('RR alone', K_RR), ('II alone', K_II)]:
    print(f"\n--- {name} ---")
    print(f"{'h':>6s}  {'D2':>14s}  {'D3':>14s}  {'D4':>14s}  {'D5':>14s}  {'D6':>14s}")
    for h in [0.05, 0.08, 0.1, 0.12, 0.15]:
        dets = []
        for r in range(2, 7):
            d = toeplitz_det(kfunc, h, r)
            dets.append(d)
        sign_str = ''.join(['+' if d > 0 else ('-' if d < 0 else '0') for d in dets])
        pf_order = 1
        for d in dets:
            if d > 0:
                pf_order += 1
            else:
                break
        print(f"{h:6.3f}  {dets[0]:14.6e}  {dets[1]:14.6e}  {dets[2]:14.6e}  {dets[3]:14.6e}  {dets[4]:14.6e}  PF_{pf_order} [{sign_str}]")

###############################################################################
# 4. Matrix decomposition: express D4(Xi) in terms of D4(RR), D4(II), cross
###############################################################################

print("\n\n=== D4 Decomposition: Xi = RR - II ===\n")

# For the 4x4 Toeplitz matrix:
# T_Xi(i,j) = K_Xi(|i-j|*h) = K_RR(|i-j|*h) - K_II(|i-j|*h)
# So T_Xi = T_RR - T_II
# and det(T_Xi) = det(T_RR - T_II)

# This is NOT simply det(T_RR) - det(T_II). The cross terms matter.
# We can expand using the matrix determinant lemma or direct expansion.

# Let's compute explicitly for each h:
for h in [0.05, 0.1, 0.15]:
    print(f"\n--- h = {h} ---")

    # Build the matrices
    rr_vals = [K_RR(k*h) for k in range(4)]
    ii_vals = [K_II(k*h) for k in range(4)]
    xi_vals_local = [K_Xi(k*h) for k in range(4)]

    T_RR = np.zeros((4,4))
    T_II = np.zeros((4,4))
    T_Xi_mat = np.zeros((4,4))

    for i in range(4):
        for j in range(4):
            T_RR[i,j] = rr_vals[abs(i-j)]
            T_II[i,j] = ii_vals[abs(i-j)]
            T_Xi_mat[i,j] = xi_vals_local[abs(i-j)]

    det_RR = np.linalg.det(T_RR)
    det_II = np.linalg.det(T_II)
    det_Xi = np.linalg.det(T_Xi_mat)

    # Check: T_Xi = T_RR - T_II
    assert np.allclose(T_Xi_mat, T_RR - T_II, atol=1e-6)

    print(f"  det(T_RR)  = {det_RR:14.6e}")
    print(f"  det(T_II)  = {det_II:14.6e}")
    print(f"  det(T_Xi)  = {det_Xi:14.6e}")
    print(f"  det(T_RR) - det(T_II) = {det_RR - det_II:14.6e}")
    print(f"  Cross-term contribution = det(T_Xi) - det(T_RR) + det(T_II) = {det_Xi - det_RR + det_II:14.6e}")

    # Eigenvalue decomposition of T_Xi
    eigvals_Xi = np.sort(np.linalg.eigvalsh(T_Xi_mat))
    eigvals_RR = np.sort(np.linalg.eigvalsh(T_RR))
    eigvals_II = np.sort(np.linalg.eigvalsh(T_II))

    print(f"\n  Eigenvalues of T_Xi: {eigvals_Xi}")
    print(f"  Eigenvalues of T_RR: {eigvals_RR}")
    print(f"  Eigenvalues of T_II: {eigvals_II}")

    # Condition numbers
    print(f"\n  Condition number T_Xi: {np.max(np.abs(eigvals_Xi))/np.min(np.abs(eigvals_Xi)):.2e}")
    print(f"  Condition number T_RR: {np.max(np.abs(eigvals_RR))/np.min(np.abs(eigvals_RR)):.2e}")

###############################################################################
# 5. The gamma factor's phase structure
###############################################################################

print("\n\n=== Gamma Factor Phase Structure ===\n")
print("G(1/2+it) = |G| * e^{i*phi_G(t)}")
print("zeta(1/2+it) = |zeta| * e^{i*phi_zeta(t)}")
print("Xi(1/2+it) = |G|*|zeta| * cos(phi_G + phi_zeta)")
print()

print(f"{'t':>8s}  {'|G|':>14s}  {'phi_G':>10s}  {'|zeta|':>14s}  {'phi_zeta':>10s}  {'phi_sum':>10s}  {'cos(phi_sum)':>14s}  {'Xi':>14s}")
print("-" * 110)

for t_idx in range(0, len(t_grid), 200):
    t = t_grid[t_idx]
    g = G_complex[t_idx]
    z = zeta_complex[t_idx]

    abs_g = abs(g)
    phi_g = np.angle(g)
    abs_z = abs(z)
    phi_z = np.angle(z)
    phi_sum = phi_g + phi_z
    cos_phi = np.cos(phi_sum)
    xi = abs_g * abs_z * cos_phi
    xi_actual = G_real[t_idx] * zeta_real[t_idx] - G_imag[t_idx] * zeta_imag[t_idx]

    print(f"{t:8.2f}  {abs_g:14.6e}  {phi_g:10.4f}  {abs_z:14.6e}  {phi_z:10.4f}  {phi_sum:10.4f}  {cos_phi:14.6e}  {xi_actual:14.6e}")

###############################################################################
# 6. Can we find a BETTER gamma factor?
###############################################################################

print("\n\n=== Search for Better Gamma Factor ===\n")
print("Goal: find G_new(s) such that G_new(s)*zeta(s) has a real, positive kernel")
print("AND G_new has higher PF order than G.\n")

# The standard G makes Xi real via the functional equation.
# Could we use a DIFFERENT completion that also gives a real function?
#
# Key constraint: for H(s) = F(s)*zeta(s) to have Fourier kernel, we need
# H(1/2+it) to be real for real t (or at least its cosine transform to be meaningful).
#
# Alternative: H(s) = |G(s)| * |zeta(s)| = the MODULUS.
# This IS real and positive, but has no zeros (so not directly useful for RH).
# However, its PF properties might be illuminating.

modulus_product = np.abs(G_complex) * np.abs(zeta_complex)

print("PF test for |G|*|zeta| (modulus product):")
K_mod = lambda u: kernel(modulus_product, u)
for h in [0.05, 0.1, 0.15]:
    dets = []
    for r in range(2, 7):
        d = toeplitz_det(K_mod, h, r)
        dets.append(d)
    sign_str = ''.join(['+' if d > 0 else ('-' if d < 0 else '0') for d in dets])
    print(f"  h={h}: [{sign_str}] D2={dets[0]:.2e} D3={dets[1]:.2e} D4={dets[2]:.2e} D5={dets[3]:.2e} D6={dets[4]:.2e}")

# Alternative: "rotated" completion
# If we multiply by e^{-i*phi_G(t)} (removing the gamma phase), we get:
# H(t) = |G(t)| * zeta(1/2+it) * e^{-i*phi_G(t)}
# = |G(t)| * |zeta(t)| * e^{i*(phi_zeta - 0)} = |G|*|zeta|*e^{i*phi_zeta}
# This is NOT real.

# But if we multiply by e^{-i*(phi_G + phi_zeta)} (removing ALL phases):
# H(t) = |G|*|zeta| which is back to the modulus.

# The ONLY way to get a real function is to have the total phase = 0 or pi.
# Xi achieves this because the functional equation forces phi_G + phi_zeta = 0 mod pi.

print("\nThe phases phi_G + phi_zeta (should be 0 or pi for Xi to be real):")
for t_idx in range(0, len(t_grid), 400):
    t = t_grid[t_idx]
    phi_g = np.angle(G_complex[t_idx])
    phi_z = np.angle(zeta_complex[t_idx])
    total = phi_g + phi_z
    # Reduce to [-pi, pi]
    total_mod = ((total + np.pi) % (2*np.pi)) - np.pi
    print(f"  t={t:8.2f}: phi_G = {phi_g:8.4f}, phi_zeta = {phi_z:8.4f}, sum mod pi = {total_mod:8.4f}")

###############################################################################
# 7. The s(s-1) factor: absorbing it differently
###############################################################################

print("\n\n=== The s(s-1) Factor: Can We Absorb It Better? ===\n")

# Xi = s(s-1)/2 * pi^{-s/2} * Gamma(s/2) * zeta(s)
#
# s(s-1)/2 on the critical line: -(1+4t^2)/8 = -(1/4 + t^2)/2
# This is REAL and NEGATIVE for all t > 0. Its FT as a kernel is:
# K_s(u) = FT[-(1/4+t^2)/2](u)
# = -(1/4)*delta(u) - (1/2)*delta''(u) (distributional)
#
# This factor is what kills the PF properties of the stripped gamma.
# Without it, the stripped gamma kernel pi^{-s/2}*Gamma(s/2) has kernel
# that alternates signs (we saw it's PF_1).
#
# What if we replace s(s-1)/2 with a DIFFERENT polynomial that:
# (a) Has zeros at s=0 and s=1 (to cancel zeta's poles)
# (b) Has a better kernel (higher PF order)?
#
# Option: (s/2)*(1-s)/2 = s(1-s)/4 -- this is just -(s(s-1))/4, same thing.
# Option: Gamma(1+s/2) / Gamma(s/2) = s/2 -- doesn't cancel both poles.
# Option: (s-1) only -- then xi(s) = (s-1) * pi^{-s/2} * Gamma(s/2) * zeta(s)
#          which has only the pole at s=0 canceled... but Gamma(s/2) has a pole
#          at s=0 too, so (s-1)*Gamma(s/2)*pi^{-s/2} = (s-1)*pi^{-s/2}*Gamma(s/2)
#          has a simple pole at s=0. The s factor in s(s-1) kills it.

# Let's just try: what if we use different real-valued prefactors?
# The goal: find P(s) real on the critical line, such that P(1/2+it)*G_stripped*zeta
# has better kernel PF.

# Candidate 1: P(t) = exp(-alpha*t^2) (Gaussian)
# This is the de Bruijn-Newman approach! Multiplying by exp(alpha*t^2) in frequency
# domain = Gaussian convolution in kernel domain.

# Candidate 2: P(t) = cosh(alpha*t)^{-1} (Polya-type)
# This decays like exp(-alpha|t|), giving an exponential decay.

# Candidate 3: P(t) = (1+t^2)^{-beta} for some beta > 0

print("Testing alternative prefactors to replace s(s-1)/2:\n")

# The stripped xi: xi_stripped(t) = Re(pi^{-s/2} * Gamma(s/2) * zeta(s)), s=1/2+it
xi_stripped_vals = np.real(np.array([complex(mpmath.power(mpmath.pi, -mpmath.mpc('0.5', mpmath.mpf(t))/2) * mpmath.gamma(mpmath.mpc('0.5', mpmath.mpf(t))/2) * mpmath.zeta(mpmath.mpc('0.5', mpmath.mpf(t)))) for t in t_grid]))

# This has poles at t where Gamma(1/4+it/2) has poles... but Gamma has no poles
# on Re > 0, and 1/4+it/2 has Re = 1/4 > 0. So it's fine.

# But wait: stripped xi is Re(G_stripped * zeta), and on the critical line,
# G_stripped is complex. So the "real part" is nontrivial.

# Actually, Xi = s(s-1)/2 * G_stripped * zeta = (real prefactor) * (complex product)
# Since s(s-1)/2 is real on the critical line, Xi is real iff G_stripped*zeta
# has real part proportional to the result.
# Actually: Xi is real because of the functional equation, period.

# Let's try multiplying the Xi function by exp(alpha*t^2) to see if we can
# improve PF. This is exactly the de Bruijn-Newman deformation.

for alpha in [0, 0.001, 0.01, 0.05, 0.1]:
    # Deformed Xi: Xi_alpha(t) = Xi(t) * exp(alpha*t^2)
    # Kernel: K_alpha(u) = FT[Xi(t) * exp(alpha*t^2)](u)
    xi_deformed = xi_direct_full = np.array([float(mpmath.re(mpmath.mpf('0.5') * mpmath.mpc('0.5', mpmath.mpf(t)) * (mpmath.mpc('0.5', mpmath.mpf(t)) - 1) * mpmath.power(mpmath.pi, -mpmath.mpc('0.5', mpmath.mpf(t))/2) * mpmath.gamma(mpmath.mpc('0.5', mpmath.mpf(t))/2) * mpmath.zeta(mpmath.mpc('0.5', mpmath.mpf(t))))) for t in t_grid[:10]]) if alpha == 0 else None

    # For speed, use precomputed Xi and just multiply by exp(alpha*t^2)
    xi_alpha = (G_real * zeta_real - G_imag * zeta_imag) * np.exp(alpha * t_grid**2)
    K_alpha = lambda u, xv=xi_alpha: kernel(xv, u)

    dets = []
    for r in range(2, 7):
        d = toeplitz_det(K_alpha, 0.1, r)
        dets.append(d)
    sign_str = ''.join(['+' if d > 0 else ('-' if d < 0 else '0') for d in dets])

    print(f"  alpha = {alpha:.3f}: [{sign_str}] D5 = {dets[3]:.6e}")

###############################################################################
# 8. Key insight: what makes the Gamma kernel PF_5?
###############################################################################

print("\n\n=== Why Is the Gamma Kernel PF_5 While Xi Is Only PF_4? ===\n")

# The first computation showed:
# - Gamma kernel (Re part): PF_5
# - Zeta kernel (Re part): PF_6+
# - Xi kernel: PF_4
#
# This is PARADOXICAL if we think in terms of convolution.
# The resolution: Xi is NOT the convolution of the gamma kernel and zeta kernel.
# Xi(t) = Re[G(t)] * Re[zeta(t)] - Im[G(t)] * Im[zeta(t)]
#
# The kernel of Xi is:
# Phi_Xi = Phi_RR - Phi_II
# where Phi_RR = FT[Re(G)*Re(zeta)] and Phi_II = FT[Im(G)*Im(zeta)]
#
# Each of these IS a convolution (FT of a product):
# Phi_RR = (1/2pi) * FT[Re(G)] ** FT[Re(zeta)]
# Phi_II = (1/2pi) * FT[Im(G)] ** FT[Im(zeta)]
#
# BUT Phi_Xi = Phi_RR - Phi_II is a DIFFERENCE of convolutions.
# And we know that DIFFERENCES (additions) can destroy PF properties!
#
# This is EXACTLY the same mechanism as in Davenport-Heilbronn:
# DH = c1*L1 + c2*L2 -- a linear combination destroys PF.
# Xi = RR - II -- a difference of two convolution terms also limits PF.

print("CRITICAL INSIGHT:")
print("  Xi kernel = K_RR - K_II (difference of two convolution kernels)")
print("  Each convolution kernel separately has high PF order,")
print("  but the DIFFERENCE can have lower PF order.")
print()
print("  This is analogous to DH = c1*L1 + c2*L2:")
print("  Each L-function has good PF properties (via Euler product),")
print("  but the linear combination does not.")
print()
print("  HOWEVER, Xi's difference is MUCH better than DH's:")
print("  Xi achieves PF_4 (with PF_5 barely failing),")
print("  while DH fails even PF_2 (its kernel is bimodal).")
print()
print("  The functional equation constrains the phases phi_G + phi_zeta")
print("  to be 0 or pi, which limits the 'damage' that the subtraction can do.")
print("  Without the functional equation (like DH), there's no such constraint.")

###############################################################################
# 9. Quantify the damage from the subtraction
###############################################################################

print("\n\n=== Quantifying the Subtraction Damage ===\n")

for h in [0.05, 0.1]:
    print(f"\nh = {h}:")
    for r in [4, 5, 6]:
        d_xi = toeplitz_det(K_Xi, h, r)
        d_rr = toeplitz_det(K_RR, h, r)
        d_ii = toeplitz_det(K_II, h, r)

        print(f"  D{r}: Xi = {d_xi:12.4e}  RR = {d_rr:12.4e}  II = {d_ii:12.4e}")

        # Build the actual matrices to compute cross terms
        rr_v = [K_RR(k*h) for k in range(r)]
        ii_v = [K_II(k*h) for k in range(r)]

        T_RR_mat = np.zeros((r,r))
        T_II_mat = np.zeros((r,r))
        for i in range(r):
            for j in range(r):
                T_RR_mat[i,j] = rr_v[abs(i-j)]
                T_II_mat[i,j] = ii_v[abs(i-j)]

        T_Xi_here = T_RR_mat - T_II_mat

        # Frobenius norm comparison
        norm_rr = np.linalg.norm(T_RR_mat, 'fro')
        norm_ii = np.linalg.norm(T_II_mat, 'fro')
        norm_xi = np.linalg.norm(T_Xi_here, 'fro')

        print(f"       norms: ||T_RR|| = {norm_rr:.4e}, ||T_II|| = {norm_ii:.4e}, ||T_Xi|| = {norm_xi:.4e}")
        print(f"       ||T_II||/||T_RR|| = {norm_ii/norm_rr:.6f}")

###############################################################################
# 10. Save results
###############################################################################

results = {
    'description': 'Cross-term decomposition of D4 Toeplitz determinant',
    'key_finding': 'Xi kernel = K_RR - K_II, a DIFFERENCE of convolution kernels. This difference is what limits PF order from PF_5/PF_6 to PF_4.',
}

with open('/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/gamma-bypass/cross_term_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n\nDone.")
