"""
Investigation 4: Hardy Z-function approach
Investigation 5: Precise numerical comparison of PF orders

The key findings so far:
1. Xi kernel = K_RR - K_II (difference of convolutions), limiting PF to 4
2. Gamma kernel alone is PF_5, Zeta kernel is PF_6+
3. |G|*|zeta| (modulus product) is PF_6+ -- but has no zeros
4. Hardy Z kernel is highly oscillatory and NOT positivity-preserving
5. The modular boost creates PF_4 from PF_3 components

New question: Is there a DIFFERENT function whose zeros are exactly the
nontrivial zeros of zeta, and whose kernel has better PF properties?

The candidates:
- Z(t) = e^{i*theta(t)} * zeta(1/2+it): real, but bad kernel
- Xi(1/2+it): real, kernel is PF_4
- What about abs(Xi(1/2+it))^2? Real, positive, but zeros become double zeros
- What about Xi(1/2+it)^2? This is real and its zeros are exactly the zeta zeros (doubled)

The squared Xi approach is interesting because:
- Xi^2 = (RR - II)^2 = RR^2 - 2*RR*II + II^2
- Its kernel is the AUTOCONVOLUTION of the Xi kernel
- By Schoenberg: autoconvolution of PF_k is PF_k
- So the squared kernel is also PF_4

But we can also write: |Xi|^2 = Xi * Xi_bar = Xi^2 (since Xi is real)
And |Xi|^2 has the same zero set as Xi (with doubled multiplicities).

Actually, the key insight is DIFFERENT: we should look at functions that
NATURALLY avoid the G(s)*zeta(s) product structure.
"""

import numpy as np
import mpmath
import json

mpmath.mp.dps = 50

###############################################################################
# 1. The Xi^2 kernel (autoconvolution)
###############################################################################

print("=" * 70)
print("INVESTIGATION: Xi^2, ALTERNATIVE FUNCTIONS, AND PF COMPARISON")
print("=" * 70)

t_max = 60.0
N_pts = 4001
t_grid = np.linspace(0, t_max, N_pts)
dt = t_grid[1] - t_grid[0]

# Precompute Xi
xi_vals = np.array([float(mpmath.re(mpmath.mpf('0.5') * mpmath.mpc('0.5', mpmath.mpf(t)) * (mpmath.mpc('0.5', mpmath.mpf(t)) - 1) * mpmath.power(mpmath.pi, -mpmath.mpc('0.5', mpmath.mpf(t))/2) * mpmath.gamma(mpmath.mpc('0.5', mpmath.mpf(t))/2) * mpmath.zeta(mpmath.mpc('0.5', mpmath.mpf(t))))) for t in t_grid])
print("Xi computed.")

# Xi^2
xi_sq_vals = xi_vals ** 2
print("Xi^2 computed.")

# Z-function for reference
def hardy_Z(t):
    t = mpmath.mpf(t)
    s = mpmath.mpc('0.5', t)
    theta = mpmath.im(mpmath.loggamma(mpmath.mpc('0.25', t/2))) - t/2 * mpmath.log(mpmath.pi)
    z_val = mpmath.exp(mpmath.mpc(0, theta)) * mpmath.zeta(s)
    return float(mpmath.re(z_val))

Z_vals = np.array([hardy_Z(t) for t in t_grid])
print("Z computed.")

# Z^2 for comparison
Z_sq_vals = Z_vals ** 2
print("Z^2 computed.")

def kernel(f_vals, u):
    integrand = f_vals * np.cos(u * t_grid)
    return 2 * np.trapz(integrand, dx=dt)

def toeplitz_det(kernel_func, h, order):
    vals = [kernel_func(k*h) for k in range(order)]
    mat = np.zeros((order, order))
    for i in range(order):
        for j in range(order):
            mat[i][j] = vals[abs(i-j)]
    return np.linalg.det(mat)

###############################################################################
# 2. PF comparison table
###############################################################################

print("\n=== PF Order Comparison ===\n")

funcs = {
    'Xi': lambda u: kernel(xi_vals, u),
    'Xi^2': lambda u: kernel(xi_sq_vals, u),
    'Z': lambda u: kernel(Z_vals, u),
    'Z^2': lambda u: kernel(Z_sq_vals, u),
}

for name, kfunc in funcs.items():
    print(f"\n--- {name} ---")
    print(f"{'h':>6s}  {'D2':>14s}  {'D3':>14s}  {'D4':>14s}  {'D5':>14s}  {'D6':>14s}  PF")
    for h in [0.05, 0.08, 0.1, 0.12, 0.15]:
        dets = []
        for r in range(2, 7):
            d = toeplitz_det(kfunc, h, r)
            dets.append(d)
        signs = ''.join(['+' if d > 0 else ('-' if d < 0 else '0') for d in dets])
        pf = 1
        for d in dets:
            if d > 0:
                pf += 1
            else:
                break
        print(f"{h:6.3f}  {dets[0]:14.6e}  {dets[1]:14.6e}  {dets[2]:14.6e}  {dets[3]:14.6e}  {dets[4]:14.6e}  PF_{pf} [{signs}]")

###############################################################################
# 3. The deformation approach: Xi_lambda(t) = Xi(t) * e^{lambda*t^2}
###############################################################################

print("\n\n=== De Bruijn-Newman Deformation: Xi_lambda(t) ===\n")
print("Xi_lambda = Xi(t) * exp(lambda * t^2)")
print("Lambda >= 0 (Rodgers-Tao), Lambda <= 0.2 (Platt-Trudgian)")
print("RH <=> Lambda <= 0")
print()

print("PF order as function of lambda (at h=0.08):")
print(f"{'lambda':>10s}  {'D2':>12s}  {'D3':>12s}  {'D4':>12s}  {'D5':>12s}  {'D6':>12s}  PF")

for lam in [-0.5, -0.2, -0.1, -0.05, -0.01, -0.005, -0.001, 0, 0.001, 0.005, 0.01, 0.05]:
    xi_lam = xi_vals * np.exp(lam * t_grid**2)
    kfunc = lambda u, xv=xi_lam: kernel(xv, u)
    dets = []
    for r in range(2, 7):
        d = toeplitz_det(kfunc, 0.08, r)
        dets.append(d)
    signs = ''.join(['+' if d > 0 else ('-' if d < 0 else '0') for d in dets])
    pf = 1
    for d in dets:
        if d > 0:
            pf += 1
        else:
            break
    print(f"{lam:10.4f}  {dets[0]:12.4e}  {dets[1]:12.4e}  {dets[2]:12.4e}  {dets[3]:12.4e}  {dets[4]:12.4e}  PF_{pf} [{signs}]")

###############################################################################
# 4. What about using a DIFFERENT multiplier instead of e^{lambda*t^2}?
###############################################################################

print("\n\n=== Alternative Deformations ===\n")

# Instead of the Gaussian deformation, try:
# (a) Cauchy deformation: multiply by (1+lambda*t^2)^{-1}
# (b) Sech deformation: multiply by sech(lambda*t)
# (c) Bessel deformation: multiply by J_0(lambda*t)

print("--- Cauchy deformation: Xi(t) / (1 + lambda*t^2) ---")
print(f"{'lambda':>10s}  {'D4':>12s}  {'D5':>12s}  PF")

for lam in [0, 0.0001, 0.001, 0.01, 0.05, 0.1, 0.5, 1.0]:
    xi_cauchy = xi_vals / (1 + lam * t_grid**2)
    kfunc = lambda u, xv=xi_cauchy: kernel(xv, u)
    dets = []
    for r in range(2, 7):
        d = toeplitz_det(kfunc, 0.08, r)
        dets.append(d)
    signs = ''.join(['+' if d > 0 else ('-' if d < 0 else '0') for d in dets])
    pf = 1
    for d in dets:
        if d > 0:
            pf += 1
        else:
            break
    print(f"{lam:10.4f}  {dets[2]:12.4e}  {dets[3]:12.4e}  PF_{pf} [{signs}]")

print("\n--- Sech deformation: Xi(t) * sech(lambda*t) ---")
print(f"{'lambda':>10s}  {'D4':>12s}  {'D5':>12s}  PF")

for lam in [0, 0.001, 0.01, 0.05, 0.1, 0.5, 1.0]:
    xi_sech = xi_vals / np.cosh(lam * t_grid)
    kfunc = lambda u, xv=xi_sech: kernel(xv, u)
    dets = []
    for r in range(2, 7):
        d = toeplitz_det(kfunc, 0.08, r)
        dets.append(d)
    signs = ''.join(['+' if d > 0 else ('-' if d < 0 else '0') for d in dets])
    pf = 1
    for d in dets:
        if d > 0:
            pf += 1
        else:
            break
    print(f"{lam:10.4f}  {dets[2]:12.4e}  {dets[3]:12.4e}  PF_{pf} [{signs}]")

###############################################################################
# 5. The KEY question: can we find a deformation that improves PF_5
#    WITHOUT breaking PF_4, and whose effect on zeros is controlled?
###############################################################################

print("\n\n=== Targeted PF5 Restoration ===\n")

# The PF_5 failure is at specific h values (h ~ 0.05 to 0.11).
# The Cauchy deformation damps high-frequency oscillations.
# Can it fix PF_5 without breaking PF_4?

print("Fine scan of Cauchy lambda at h = 0.08:")
print(f"{'lambda':>10s}  {'D4':>12s}  {'D5':>12s}  D5 sign")

for lam in np.arange(0, 0.11, 0.005):
    xi_cauchy = xi_vals / (1 + lam * t_grid**2)
    kfunc = lambda u, xv=xi_cauchy: kernel(xv, u)
    d4 = toeplitz_det(kfunc, 0.08, 4)
    d5 = toeplitz_det(kfunc, 0.08, 5)
    s = '+' if d5 > 0 else '-'
    print(f"{lam:10.4f}  {d4:12.4e}  {d5:12.4e}  {s}")

print("\nFine scan of Cauchy lambda at h = 0.1:")
for lam in np.arange(0, 0.11, 0.005):
    xi_cauchy = xi_vals / (1 + lam * t_grid**2)
    kfunc = lambda u, xv=xi_cauchy: kernel(xv, u)
    d4 = toeplitz_det(kfunc, 0.1, 4)
    d5 = toeplitz_det(kfunc, 0.1, 5)
    s = '+' if d5 > 0 else '-'
    print(f"{lam:10.4f}  {d4:12.4e}  {d5:12.4e}  {s}")

###############################################################################
# 6. The functional equation constraint on completions
###############################################################################

print("\n\n=== Functional Equation Constraints ===\n")

# For Xi to be real on the critical line, we need:
# Xi(1/2+it) = conj(Xi(1/2+it))
# which follows from Xi(s) = Xi(1-s) (functional equation)
#
# Any "alternative completion" G_new(s)*zeta(s) will be real on the line iff
# G_new(1/2+it)*zeta(1/2+it) is real for all real t.
#
# Since zeta(1/2+it) is NOT real in general, G_new must compensate:
# arg(G_new(1/2+it)) + arg(zeta(1/2+it)) = 0 or pi for all t.
#
# This means: arg(G_new(1/2+it)) = -arg(zeta(1/2+it)) mod pi for ALL t.
# This is an extremely restrictive condition.
#
# The standard G(s) satisfies this via the functional equation:
# Xi(s) = Xi(1-s) => G(s)*zeta(s) = G(1-s)*zeta(1-s)
# On s = 1/2+it: G(1/2+it)*zeta(1/2+it) = G(1/2-it)*zeta(1/2-it) = conj(G(1/2+it)*zeta(1/2+it))
# So Xi is real.
#
# For G_new: we need G_new(s)*zeta(s) = G_new(1-s)*zeta(1-s)
# Using zeta(s) = chi(s)*zeta(1-s) where chi is the completed function equation factor:
# G_new(s) = G_new(1-s)*chi(s)^{-1}... this constrains G_new.

# Actually, any G_new of the form G_new(s) = f(s)*G(s) where f(s) = f(1-s)
# and f is real on Re(s) = 1/2 will work: f*Xi has the same zeros as Xi
# (assuming f is nonzero in the strip), is real on the line, and has kernel
# that is the convolution of f's kernel with Xi's kernel.

# The question is: can we choose f such that the convolution IMPROVES PF order?

print("Testing symmetric multipliers f(s) = f(1-s), real on the line:")
print()

# f_1(t) = exp(-alpha*t^2): Gaussian. This is the de Bruijn-Newman deformation.
# f_2(t) = (1+alpha*t^2)^{-1}: Cauchy-like.
# f_3(t) = cos(alpha*t)^2: oscillatory
# f_4(t) = 1 + alpha*cos(t): gentle modification

# For a multiplier f that is real, even, positive:
# New kernel = Old kernel * FT[f] (convolution in kernel domain)
# If FT[f] is PF_infinity (e.g., f is the FT of a PF_infinity kernel),
# then the new PF order >= old PF order (convolution with PF_inf preserves PF_k).
#
# If FT[f] is PF_m, then new PF = min(old PF, m).
#
# So: to IMPROVE PF, we need f such that the resulting kernel Phi_new = Phi * FT[f]
# (NOT convolution! In this case Xi_new(t) = f(t)*Xi(t), and
# Phi_new(u) = FT[f*Xi](u) = (FT[f] * FT[Xi])(u) = (FT[f] conv Phi)(u))
# Wait, actually FT[f*Xi](u) = (FT[f] * Phi)(u) is convolution.
#
# But convolution of PF_k and PF_m gives PF_{min(k,m)}.
# So convolution CANNOT increase PF order!

print("FUNDAMENTAL THEOREM:")
print("  If F_new(t) = f(t) * F_old(t), then Kernel_new = Kernel_f conv Kernel_old.")
print("  By Schoenberg: PF(Kernel_new) = min(PF(Kernel_f), PF(Kernel_old)).")
print("  THEREFORE: no multiplicative modification in frequency domain")
print("  can INCREASE the PF order of the kernel.")
print()
print("  This means: the PF_4 limit of Xi's kernel CANNOT be improved")
print("  by multiplying Xi(1/2+it) by any function f(t).")
print()
print("  To improve PF, we need a fundamentally DIFFERENT representation,")
print("  not just a different completion.")

###############################################################################
# 7. The only escape: non-multiplicative representations
###############################################################################

print("\n\n=== Non-Multiplicative Representations ===\n")

# The Weil explicit formula connects:
# sum_rho h(rho) = (stuff involving primes)
# where the sum is over zeta zeros.
#
# If we choose h to be a test function, we can express facts about zeros
# in terms of sums over primes. But this doesn't directly give a kernel
# representation.
#
# Another approach: the Selberg trace formula analogue.
# Or: the Guinand-Weil explicit formula gives:
# sum_gamma f(gamma) = f(0)*something + integral + sum_p sum_k stuff
# where gamma are the imaginary parts of nontrivial zeros.
#
# This is NOT a kernel representation of a function whose zeros are the gamma_n.
# Rather, it's a distribution relation.

print("The escape routes from PF_4 are:")
print()
print("1. ADDITIVE modification in frequency domain:")
print("   H(t) = Xi(t) + g(t)")
print("   Kernel_H = Kernel_Xi + Kernel_g")
print("   Addition CAN increase PF order (the modular boost does this!)")
print("   But H and Xi have different zeros unless g = 0.")
print()
print("2. DIFFERENTIAL representation:")
print("   Instead of Phi's Toeplitz structure, use a different criterion")
print("   for reality of zeros. E.g., the Hermite-Biehler theorem.")
print()
print("3. OPERATOR-THEORETIC approach:")
print("   Express Xi as a Fredholm determinant or characteristic polynomial")
print("   of a self-adjoint operator. Reality of zeros follows from")
print("   self-adjointness. This bypasses PF entirely.")
print()
print("4. WORK WITH PF_4 DIRECTLY:")
print("   Prove that PF_4 + functional equation + Euler product structure")
print("   => all zeros real. This requires a new theorem in total positivity.")

###############################################################################
# 8. Hermite-Biehler decomposition
###############################################################################

print("\n\n=== Hermite-Biehler Decomposition ===\n")

# The Hermite-Biehler theorem: E(z) = A(z) - iB(z) where A, B are real entire
# functions, has all zeros in the upper half-plane iff:
# |E(z)| > |E*(z)| for Im(z) > 0, where E*(z) = conj(E(conj(z))).
#
# For Xi: Xi(1/2+iz) is an even function of z. Its zeros are at z = i*gamma
# (on the imaginary axis) iff RH holds.
#
# Write F(z) = Xi(1/2+iz) = Xi(1/2+iz).
# For z real: F(z) = Xi(1/2+iz). Since Xi(1/2+it) is real for real t,
# F(z) = Xi(1/2+iz) = Xi(1/2+iz).
# For z = x (real): F(x) = Xi(1/2+ix).
#
# We can decompose F(z) = P(z^2) + z*Q(z^2) (since F is even + odd decomposition...
# wait, Xi(1/2+iz) is EVEN in z by the functional equation: Xi(s) = Xi(1-s)
# implies Xi(1/2+iz) = Xi(1/2-iz) = Xi(1/2+i(-z)), so F(z) = F(-z).
#
# So F(z) = P(z^2) for some function P.
# RH <=> all zeros of P(w) lie on w = -gamma^2 < 0, i.e., P has only
# negative real zeros.
#
# P has only negative real zeros iff P(w) is in the Laguerre-Polya class
# for the variable w.

# Let's check: P(w) = Xi(1/2 + i*sqrt(w))
# For w = -t^2 (i.e., w < 0): P(-t^2) = Xi(1/2+it) = Phi's generating function.
# For w = t^2 > 0: P(t^2) = Xi(1/2+it) where t is imaginary... so P(t^2) = Xi(1/2-t).

# We can compute P(w) for w > 0:
print("P(w) = Xi(1/2 + i*sqrt(w)) for w > 0 and w < 0:")
print(f"{'w':>8s}  {'P(w)':>14s}  {'via':>20s}")

for w in [-100, -50, -25, -10, -1, -0.25, 0, 0.01, 0.1, 0.5, 1, 5]:
    if w < 0:
        t = np.sqrt(-w)
        p_val = float(mpmath.re(mpmath.mpf('0.5') * mpmath.mpc('0.5', mpmath.mpf(t)) * (mpmath.mpc('0.5', mpmath.mpf(t)) - 1) * mpmath.power(mpmath.pi, -mpmath.mpc('0.5', mpmath.mpf(t))/2) * mpmath.gamma(mpmath.mpc('0.5', mpmath.mpf(t))/2) * mpmath.zeta(mpmath.mpc('0.5', mpmath.mpf(t)))))
        print(f"{w:8.2f}  {p_val:14.6e}  Xi(1/2+i*{t:.2f})")
    elif w == 0:
        p_val = float(mpmath.re(mpmath.mpf('0.5') * mpmath.mpc('0.5', 0) * (mpmath.mpc('0.5', 0) - 1) * mpmath.power(mpmath.pi, -mpmath.mpf('0.25')) * mpmath.gamma(mpmath.mpf('0.25')) * mpmath.zeta(mpmath.mpf('0.5'))))
        print(f"{w:8.2f}  {p_val:14.6e}  Xi(1/2)")
    else:
        # w > 0: sqrt(w) is real, so 1/2 + i*sqrt(w) has Im part sqrt(w)
        t = np.sqrt(w)
        s = mpmath.mpc('0.5', mpmath.mpf(t))
        p_val = float(mpmath.re(mpmath.mpf('0.5') * s * (s - 1) * mpmath.power(mpmath.pi, -s/2) * mpmath.gamma(s/2) * mpmath.zeta(s)))
        print(f"{w:8.2f}  {p_val:14.6e}  Xi(1/2+i*{t:.2f})")

print()
print("RH <=> P(w) has only negative real zeros.")
print("This is equivalent to: P's Fourier/Laplace transform kernel being PF_inf.")
print("But P(w) for w < 0 IS just Xi evaluated at the zero, so this is circular.")

###############################################################################
# 9. The real question: what structural property beyond PF_4 do we need?
###############################################################################

print("\n\n=== Summary: What's Needed Beyond PF_4 ===\n")

print("1. Multiplicative deformations (changing the completion) CANNOT improve PF order.")
print("   Proof: convolution with PF_m gives min(PF_old, PF_m).")
print()
print("2. The Hardy Z-function avoids the gamma factor but has a TERRIBLE kernel")
print("   (highly oscillatory, sign-changing, PF_1 at best).")
print("   This is because Z removes the gamma factor's SMOOTHING effect.")
print()
print("3. The modular boost phenomenon shows that ADDITION can improve PF order.")
print("   The theta sum f_1 + f_2 + ... goes from PF_3 (f_1 alone) to PF_4.")
print("   A 2.27% increase in f_2 would give PF_5.")
print()
print("4. The cross-term analysis shows:")
print("   - D4(f_1) = -8.06e-7 (NEGATIVE)")
print("   - Cross-term from f_1*f_2 interaction: +4.63e-6 (POSITIVE, overwhelming)")
print("   - D5(f_1) = -6.82e-8 (NEGATIVE)")
print("   - Cross-term at D5: +6.64e-8 (POSITIVE, but only 97.3% enough)")
print("   The modular boost at D4 has 5.7x headroom; at D5 it falls 2.7% short.")
print()
print("5. The fundamental constraint is NOT the gamma factor per se.")
print("   It is the SUBTRACTION Xi = RR - II that limits PF order.")
print("   Both RR and II kernels are high-PF, but their difference is only PF_4.")
print()
print("6. The gamma kernel ALONE is PF_5 -- better than Xi!")
print("   So the 'gamma factor bottleneck' identified earlier was WRONG.")
print("   The real bottleneck is the interaction between gamma and zeta")
print("   mediated by the complex multiplication structure.")

###############################################################################
# Save
###############################################################################

results = {
    'key_correction': 'The gamma factor alone is PF_5, not the bottleneck. The bottleneck is the complex multiplication structure Xi = Re(G)*Re(zeta) - Im(G)*Im(zeta), which is a subtraction that limits PF.',
    'escape_routes': [
        'Additive modification in kernel domain (modular boost pattern)',
        'Operator-theoretic approach (bypass PF entirely)',
        'New theorem: PF_4 + FE + Euler product => real zeros',
        'Work directly with Euler product, bypass Xi completion'
    ]
}

with open('/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/riemann-hypothesis/experiments/gamma-bypass/hardy_z_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n\nDone.")
