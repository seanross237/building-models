"""
Detailed test at Q=I to understand the Hessian structure.
At Q=I, all v_i are the same => B_□ = v1+v2-v3-v4 (the curl), and the
Hessian should be (β/2N)|B_□|² (the M-quadratic form).

With v1=v2=v3=v4=v, B_□ = v+v-v-v = 0 so Hessian = 0. That's why test 1 was 0!
Let's use different v's.
"""
import numpy as np
np.set_printoptions(precision=10, linewidth=120)

sigma = np.array([
    [[0, 1], [1, 0]],
    [[0, -1j], [1j, 0]],
    [[1, 0], [0, -1]],
], dtype=complex)
I2 = np.eye(2, dtype=complex)

def expm_su2(v):
    det_v = v[0,0]*v[1,1] - v[0,1]*v[1,0]
    theta_sq = -det_v
    theta = np.sqrt(np.abs(theta_sq.real))
    if theta < 1e-15:
        return I2 + v + 0.5 * v @ v
    return np.cos(theta) * I2 + (np.sin(theta) / theta) * v

def su2_basis():
    return [1j * sigma[a] for a in range(3)]

basis = su2_basis()

# Use DIFFERENT tangent vectors for each edge
v1 = 0.3*basis[0] + 0.1*basis[1]
v2 = 0.5*basis[1] - 0.2*basis[2]
v3 = 0.1*basis[0] + 0.4*basis[2]
v4 = -0.3*basis[1] + 0.2*basis[2]

# At Q=I: w1=v1, w2=v2, w3=-v3, w4=-v4
w1, w2, w3, w4 = v1, v2, -v3, -v4

# Analytical formula
Q3inv = I2.copy()
Q4inv = I2.copy()
L1 = I2.copy()
L12 = I2.copy()
L123 = I2.copy()
R1 = I2.copy()
R2 = I2.copy()
R3 = I2.copy()

self1 = np.trace(w1 @ w1)
self2 = np.trace(w2 @ w2)
self3 = np.trace(w3 @ w3)
self4 = np.trace(w4 @ w4)
self_sum = self1 + self2 + self3 + self4

c12 = np.trace(w1 @ w2)
c13 = np.trace(w1 @ w3)
c14 = np.trace(w1 @ w4)
c23 = np.trace(w2 @ w3)
c24 = np.trace(w2 @ w4)
c34 = np.trace(w3 @ w4)
cross_sum = c12 + c13 + c14 + c23 + c24 + c34

d2_trace = (self_sum + 2*cross_sum).real
hess_plaq = -(1.0/2) * d2_trace

print("At Q=I, analytical Hessian of one plaquette:")
print(f"  self_sum  = {self_sum.real:.6f}")
print(f"  cross_sum = {cross_sum.real:.6f}")
print(f"  d2 ReTr   = {d2_trace:.6f}")
print(f"  HessS_□   = {hess_plaq:.6f}")

# Now compare with (β/2N)|B_□|² where B_□ = w1 + w2 + w3 + w4
# Wait: at Q=I, B_□ = v1 + Ad_I(v2) - Ad_I(v3) - Ad_I(v4) = v1+v2-v3-v4
# And |B|² = -2 Tr(B²) for su(2) elements (since Tr(iσ_a · iσ_b) = -2δ_{ab})
B = v1 + v2 - v3 - v4
B_sq_trace = np.trace(B @ B).real  # this is -|B|² × 2 for su(2) (negative since B anti-hermitian)

# For su(2): Tr((iσ_a)(iσ_b)) = -Tr(σ_a σ_b) = -2δ_{ab}
# So if B = Σ b_a (iσ_a), Tr(B²) = Σ b_a b_b Tr(iσ_a iσ_b) = -2|b|²
# |B|² in the Euclidean metric = |b|² = -Tr(B²)/2

B_norm_sq = -np.trace(B @ B).real / 2
print(f"\nB_□ = v1+v2-v3-v4:")
print(f"  |B|² (Euclidean) = {B_norm_sq:.6f}")
print(f"  (β/2N)|B|² = {0.5*0.5*B_norm_sq:.6f}")

# Wait, let me think about the normalization.
# M(Q) is defined by v^T M v = Σ_□ |B_□|² (Euclidean norm on su(2) ~ R^3)
# HessS should equal (β/2N) × v^T M v at Q=I
# s_□ = -(β/N) Re Tr(U_□), so HessS_□ = -(β/N) d² Re Tr(U_□)/dε²
#
# For Q=I: U_□ = I, perturbed:
# d² Re Tr(U_□(ε))/dε² = Re Tr[(w1+w2+w3+w4)² + ...]
#
# Actually let me just verify: (w1+w2+w3+w4) = v1+v2-v3-v4 = B
# At Q=I, the product of exponentials to O(ε²) is:
# (I+εw1+ε²w1²/2)(I+εw2+ε²w2²/2)(I+εw3+ε²w3²/2)(I+εw4+ε²w4²/2) × I
# ≈ I + ε(w1+w2+w3+w4) + ε²[(w1²+w2²+w3²+w4²)/2 + w1w2+w1w3+w1w4+w2w3+w2w4+w3w4]
# = I + εB + ε²[Σwi²/2 + Σ_{i<j}wi wj]
# = I + εB + ε²/2 · B² + ε²/2 · Σ_{i<j}[wi,wj]
# Wait: (Σwi)² = Σwi² + 2Σ_{i<j}wi wj (when non-commutative, this is the ORDERED sum)
# Actually (w1+w2+w3+w4)² = Σwi² + Σ_{i≠j}wi wj
# But in the expansion we have Σwi²/2 + Σ_{i<j}wi wj
# = Σwi²/2 + (1/2)Σ_{i≠j}wi wj + (1/2)Σ_{i<j}[wi,wj]... no.
# Σ_{i<j}wi wj is ordered (w_i before w_j where i<j). It's NOT symmetric.
# (Σwi)² = Σwi² + Σ_{i<j}(wi wj + wj wi) = Σwi² + 2Σ_{i<j}(wi wj) - Σ_{i<j}[wi,wj]
# Hmm, this is: Σwi² + Σ_{i≠j}wi wj = Σwi² + Σ_{i<j}(wi wj + wj wi)
# So our ε² coefficient = Σwi²/2 + Σ_{i<j}wi wj
# And B² = Σwi² + Σ_{i<j}(wi wj + wj wi)
# So ε² coeff = B²/2 + (1/2)Σ_{i<j}[wi, wj]
#
# d² Re Tr(U)/dε² = Re Tr[2 × ε² coeff] = Re Tr[B² + Σ_{i<j}[wi,wj]]
# For su(2), [wi,wj] is anti-hermitian traceless => Tr([wi,wj]) = 0
# And Re Tr(X) = 0 for anti-hermitian X... wait, [wi,wj] IS anti-hermitian if wi,wj are.
# Tr([wi,wj]) = 0 always. So Σ_{i<j}Tr([wi,wj]) = 0.
# Therefore: d² Re Tr(U)/dε² = Re Tr(B²) = Tr(B²) (since B anti-herm => B² herm => Tr real)

print(f"\n  Tr(B²) = {np.trace(B @ B).real:.6f}")
print(f"  d²ReTr should be Tr(B²) = {np.trace(B @ B).real:.6f}")
print(f"  Our d²ReTr = {d2_trace:.6f}")

# But wait, the cross terms also include wi·wj where the wi pass through Q's at Q=I.
# At Q=I all Q's are I, so the insertions are just multiplied.
# The ε² terms are: Σwi²/2 + w1w2 + w1w3 + w1w4 + w2w3 + w2w4 + w3w4
# But w2 and w3 are at the SAME insertion point (between Q2 and Q3^{-1}).
# So the expansion is actually:
# Q1(I+εw1+ε²w1²/2)Q2(I+εw2+ε²w2²/2)(I+εw3+ε²w3²/2)Q3^{-1}(I+εw4+ε²w4²/2)Q4^{-1}
#
# At Q=I, this becomes:
# (I+εw1+ε²w1²/2)(I+εw2+ε²w2²/2)(I+εw3+ε²w3²/2)(I+εw4+ε²w4²/2)
# But there are 4 separate exponentials, not 4 insertions. So to O(ε²):
# ≈ I + ε(w1+w2+w3+w4) + ε²[w1²/2+w2²/2+w3²/2+w4²/2 + w1w2+w1w3+w1w4+w2w3+w2w4+w3w4]
# This is EXACTLY what our formula computes (self + 2*cross = 2 × [self/2 + cross]).
# Note: d²/dε² [ε²×(self/2 + cross)]|_0 = 2(self/2 + cross) = self + 2*cross. Yes.
#
# And this equals B² + Σ_{i<j}[wi,wj] where the commutator sum involves ordering.
# Re Tr of the commutator sum = 0 (since Tr([A,B])=0).
# So d² Re Tr/dε² = Re Tr(B²) = Tr(B²).real

print(f"\n  Verification: self_sum + 2*cross_sum = {(self_sum + 2*cross_sum).real:.6f}")
print(f"  Tr(B²) = {np.trace(B@B).real:.6f}")
print(f"  Match: {abs((self_sum + 2*cross_sum).real - np.trace(B@B).real) < 1e-12}")

# So HessS_□ at Q=I = -(β/N) Tr(B²)
# And since Tr(B²) = -2|b|² where |b|² is the Euclidean norm, we get:
# HessS_□ = -(β/N)(-2|b|²) = (2β/N)|b|² = (β/2N) × 4|b|²... hmm
# Wait: -Tr(B²)/2 = |b|², so Tr(B²) = -2|b|²
# HessS_□ = -(β/N) × (-2|b|²) = 2β|b|²/N = (β/N) × 2|b|²
# And (β/2N) × |B|²_M where |B|²_M is the M-norm...
# Actually the M(Q) quadratic form for ONE plaquette at Q=I is:
# v^T M v = |B|² = Σ_a b_a² = |b|² (Euclidean in the iσ_a basis)
# HessS_□ = (β/2N) × v^T M v requires (β/2N) |b|² = (2β/N)|b|²
# => 1/(2N) = 2/N => 1/2 = 2, which is wrong!

# Let me re-check the normalization. The issue is:
# What is the inner product on su(2)?
# If we use Tr(X†Y) = -Tr(XY) for anti-hermitian X,Y
# then <iσ_a, iσ_b> = Tr((iσ_a)†(iσ_b)) = Tr(-iσ_a · iσ_b) = Tr(σ_aσ_b) = 2δ_{ab}
# So |B|² = <B,B> = -Tr(B²) ... no wait:
# <B,B> = Tr(B†B) = Tr(-B·B) = -Tr(B²) (since B†=-B)
# If B = Σ b_a (iσ_a), then -Tr(B²) = -Σ b_a b_b Tr(iσ_a iσ_b) = -Σ b_a² × (-2) = 2Σb_a²

# Standard physics normalization: Killing form on su(N) is Tr(ad_X ad_Y).
# For SU(2), the standard normalization of generators T_a = σ_a/2:
# Tr(T_a T_b) = δ_{ab}/2
# If v = Σ c_a T_a, then |v|² in Killing metric ∝ Tr(v²) (but sign depends on convention)

# Let me just check numerically what the GOAL says.
# GOAL says M(Q) is defined by v^T M v = Σ_□ |B_□|² where
# B_□ is a vector in su(2) ≅ R³.
# The R³ identification uses the basis {iσ_a} with the Euclidean norm.
# So |B|² = Σ b_a² where B = Σ b_a (iσ_a).
# We have -Tr(B²)/2 = Σ b_a² (from above). So |B|² = -Tr(B²)/2.

# HessS_□ = -(β/N) Tr(B²) = -(β/N)(-2|B|²) = (2β/N)|B|²
# But the claim is HessS = (β/2N) × v^T M v = (β/2N)|B|²
# So (2β/N)|B|² ≠ (β/2N)|B|² unless 2/N = 1/2N, i.e. 4=1. CONTRADICTION.

# There must be a normalization issue. Let me re-check the GOAL's formula.
# The GOAL says HessS should equal (β/2N)M at Q=I. Let me verify numerically.

print("\n" + "="*70)
print("Detailed normalization check at Q=I")
print("="*70)

# FD Hessian at Q=I
def full_action_fd(Q1, Q2, Q3, Q4, v1, v2, v3, v4, beta=1.0, N=2, eps=1e-5):
    def action(e):
        U = (Q1 @ expm_su2(e*v1)) @ (Q2 @ expm_su2(e*v2)) @ \
            (expm_su2(-e*v3) @ Q3.conj().T) @ (expm_su2(-e*v4) @ Q4.conj().T)
        return -(beta/N) * np.trace(U).real
    fp = action(eps)
    fm = action(-eps)
    f0 = action(0)
    return (fp + fm - 2*f0) / eps**2

# Pick specific v's with nonzero curl
v1 = 1.0*basis[0]  # pure iσ_1 on edge 1
v2 = np.zeros((2,2), dtype=complex)
v3 = np.zeros((2,2), dtype=complex)
v4 = np.zeros((2,2), dtype=complex)

# B = v1 + v2 - v3 - v4 = v1
# |B|² = 1.0 (coefficient of iσ_1 is 1)
# (β/2N)|B|² = 0.5 * 0.5 * 1.0 = 0.25
# Our formula: -(β/N)Tr(B²) = -(1/2)Tr((iσ_1)²) = -(1/2)(-2) = 1.0
h_fd_I = full_action_fd(I2, I2, I2, I2, v1, v2, v3, v4)
print(f"\nv1 = iσ_1, v2=v3=v4=0:")
print(f"  FD HessS = {h_fd_I:.6f}")
print(f"  |B|² = 1.0, (β/2N)|B|² = {0.25:.6f}")
print(f"  -(β/N)Tr(B²) = {-(1/2)*np.trace(basis[0]@basis[0]).real:.6f}")

# So the Hessian is 1.0 but (β/2N)|B|² = 0.25. Factor of 4 off!
# This means HessS_□ = (2β/N)|B|² = 4 × (β/2N)|B|²
# OR the normalization of M is different.
# Let me check: maybe |B|² uses Killing form Tr(XY) not the Euclidean norm.
# In that case |B|²_Kill = -Tr(B²) = -Tr((iσ_1)²) = 2
# (β/2N)|B|²_Kill = 0.25 × 2 = 0.5, still not 1.0.

# Or maybe there's an extra factor of 2 from the definition.
# Let me read the GOAL more carefully...
# "v^T M(Q) v = Σ_□ |B_□(Q, v)|²"
# "B_□(Q,v) = v_{e₁} + Ad(v_{e₂}) − Ad(v_{e₃}) − Ad(v_{e₄})"
#
# The norm |B|² — in what metric? The GOAL says su(2) ≅ ℝ³.
# Standard identification: v = Σ c_a (iσ_a) ↔ (c_1, c_2, c_3) ∈ ℝ³
# Euclidean norm: |v|² = Σ c_a² = -Tr(v²)/2
#
# So |B|² = -Tr(B²)/2, and v^T M v = -Tr(B²)/2 for one plaquette.
# HessS_□ = -(β/N) Tr(B²) = (2β/N)(−Tr(B²)/2) = (2β/N)|B|²
# = (2β/N) × v^T M_□ v

# So HessS = (2β/N) × v^T M v, NOT (β/2N) × v^T M v.
# That's a factor of 4N² off! With N=2: (2β/N)/(β/2N) = 4/1 × N²/N² = 4. Hmm wait:
# (2β/N) / (β/(2N)) = 2β/N × 2N/β = 4. Yes, factor of 4.

# BUT WAIT. The GOAL says E001 found that at Q=I the Hessian matches (β/2N)M.
# So either E001's M has a different normalization, or I have an error.

# Actually, let me re-examine. The GOAL says:
# s_□ = -(β/N) Re Tr(U_□)
# And the M operator comes from expanding Re Tr to second order.
# Re Tr(U_□) at Q=I, perturbed: Re Tr(I + εB + ε²C + ...) = 2 + ε²/2 · Tr(B²) + ...
# Wait: Re Tr(I + εB + ...) = Re[Tr(I)] + ε Re Tr(B) + ε² Re Tr(C) + ...
# Tr(I) = 2, Tr(B) = 0 (traceless), C = (B² + commutator_stuff)/2
# Re Tr(C) = Tr(B²)/2 (the commutator is traceless)
# Hmm no. Let me be precise.

# U(ε) ≈ I + εB + ε²[B²/2 + Σ_{i<j}[w_i,w_j]/2] + ...  (schematic)
# Actually from our expansion:
# coeff of ε² = Σw_i²/2 + Σ_{i<j}w_iw_j
# = (Σw_i)²/2 + Σ_{i<j}[w_i,w_j]/2
# = B²/2 + commutator_stuff

# Tr of ε² coeff = Tr(B²)/2 + 0 = Tr(B²)/2
# d²/dε² Re Tr(U)|_0 = 2 × Re[Tr(B²)/2] = Tr(B²)  (B² hermitian => Tr real)
# d²/dε² s_□|_0 = -(β/N) Tr(B²)

# So HessS_□ = -(β/N)Tr(B²) = -(1/2)(-2) = 1.0 for our test case. Verified!

# Now, (β/2N)v^T M_□ v = (β/2N)|B|² = (1/4)(1.0) = 0.25 if |B|² = -Tr(B²)/2 = 1.

# So HessS_□ = -(β/N)Tr(B²) = (2β/N)(-Tr(B²)/2) = (2β/N)|B|²
# but (β/2N)|B|² = (β/2N)(-Tr(B²)/2) = -(β/4N)Tr(B²)

# Factor: HessS / [(β/2N)|B|²] = (2β/N) / (β/2N) = 4.

# So the GOAL's claim that HessS = (β/2N)M at Q=I seems wrong by a factor of 4,
# UNLESS the norm is defined differently. Perhaps they use:
# |B|² = -2Tr(B²) (the Killing form for SU(2) is -2Tr)
# Then |B|²_Kill = -2Tr(B²) = 4 for our test, and (β/2N)|B|²_Kill = 1.0. YES!

# Killing form normalization: <X,Y>_Kill = -2Tr(XY) for su(2)
# Then |B|²_Kill = -2Tr(B²), and
# (β/2N)|B|²_Kill = (β/2N)(-2Tr(B²)) = -(β/N)Tr(B²) = HessS_□. BINGO!

# So v^T M v should use the Killing norm: |B|² = -2Tr(B²).
# Or equivalently, the ℝ³ norm uses basis T_a = σ_a/2 (standard physicist convention),
# so v = Σ c_a (iσ_a/2), |v|² = Σ c_a²/4... no that changes things differently.

# Actually: if v_e = Σ_a c_{e,a} (iσ_a), then in ℝ³ with Euclidean norm, |v|² = Σ c_a².
# We showed |B|² = -Tr(B²)/2 in this convention, and HessS = (2β/N)|B|².
# If we instead use |B|²_alt = -2Tr(B²) = 4|B|², then HessS = (β/2N)|B|²_alt.

# So the GOAL likely defines |B|² with the Killing form or factor 4 convention.
# OR: the GOAL uses generators T_a = σ_a/2 and |v|² with that normalization.
# If v = Σ a_k (iσ_k/2) then c_k = a_k/2, and |B|² = Σ(a_k/2)² = Σa_k²/4.
# In "physicist" convention: |v|² = Σ a_k² (coordinates w.r.t. T_a), and
# -2Tr(v²) = -2Σ a_k a_l Tr(T_k T_l) = -2Σ a_k² (-1/4)×2 = Σa_k².
# Wait: Tr((iT_a)(iT_b)) = -Tr(T_aT_b) = -δ_{ab}/2
# v² = (Σ a_k iT_k)² = Σ a_k a_l (iT_k)(iT_l), Tr(v²) = Σa_k a_l(-δ_{kl}/2) = -Σa_k²/2
# -2Tr(v²) = Σa_k². Yes!

# So: the convention is that M uses the norm induced by -2Tr(XY) on su(2),
# which equals the standard Euclidean norm on the coordinates {a_k} when
# v = Σ a_k (iσ_k/2).

# In our code we parametrize v = Σ c_k (iσ_k), so a_k = 2c_k.
# |v|²_Kill = -2Tr(v²) = -2(-2Σc_k²) = 4Σc_k².
# So our HessS_□ = (β/2N)|B|²_Kill = (β/2N) × 4|B|²_Euclidean = (2β/N)|B|²_Euclidean.

print(f"\n  |B|²_Killing = -2Tr(B²) = {-2*np.trace(basis[0]@basis[0]).real:.6f}")
print(f"  (β/2N)|B|²_Kill = {0.25 * (-2*np.trace(basis[0]@basis[0]).real):.6f}")
print(f"  HessS_□ = {h_fd_I:.6f}")
print(f"  MATCH: {abs(0.25 * (-2*np.trace(basis[0]@basis[0]).real) - h_fd_I) < 1e-6}")

# CONCLUSION: HessS_□(v,v;Q=I) = (β/2N) × |B|²_Kill where |B|²_Kill = -2Tr(B²)
# This IS the (β/2N)M relationship, with the correct normalization.
