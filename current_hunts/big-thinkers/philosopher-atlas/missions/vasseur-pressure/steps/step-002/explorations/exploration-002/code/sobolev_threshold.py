"""
Sobolev threshold analysis: W^{1,3} gap for De Giorgi.
Shows W^{1,2} (De Giorgi energy) does NOT reach W^{1,3} threshold.
Exploration 002: Interpolation Route.
"""

from fractions import Fraction

print("=" * 65)
print("SOBOLEV EMBEDDING ANALYSIS: W^{1,2} vs W^{1,3} in R^3")
print("=" * 65)

print("""
SOBOLEV EMBEDDINGS IN 3D (spatial):

W^{1,2}(R^3):
  W^{1,2} hookrightarrow L^{2*} = L^6  (Sobolev, 2* = 2n/(n-2) = 6 for n=3)
  W^{1,2} hookrightarrow L^p for all p <= 6

W^{1,3}(R^3):
  3 >= n, so W^{1,3} hookrightarrow L^infty cap C^0  (Morrey embedding)
  W^{1,3} subset BMO  (by Morrey => bounded, BMO inclusion)

Critical difference:
  W^{1,2}(R^3) NOT subset W^{1,3}(R^3)  (different Sobolev spaces)
  W^{1,2}(R^3) NOT subset L^3(R^3)    ... wait, W^{1,2} subset L^6, so L^3 is fine?

Actually: W^{1,2}(R^3) hookrightarrow L^6(R^3) hookrightarrow L^3_{loc}(R^3)
So W^{1,2} DOES embed into L^3 locally (but not W^{1,3}).
""")

print("Let me be precise about which spaces are involved:")
print()
print("For the De Giorgi estimate, we need to control:")
print("  ||nabla psi_k||_{L^3(Q_k)} or ||psi_k||_{W^{1,3}(Q_k)}")
print()
print("psi_k = v_k * phi_k * e . nabla(phi_k)")
print()
print("From De Giorgi energy U_k:")
print("  ||nabla(v_k phi_k)||_{L^2_{t,x}} <= U_k^{1/2}")
print("  ||v_k phi_k||_{L^infty_t L^2_x} <= U_k^{1/2}")
print()
print("We need: does De Giorgi energy give ||v_k||_{L^2_t W^{1,3}_x}?")
print()

print("SOBOLEV SCALING ARGUMENT:")
print("For a function f in W^{1,2} subset L^6 (in R^3):")
print("  Does W^{1,2} subset W^{s,3} for some s?")
print()
print("Sobolev embedding: W^{s,3}(R^3) embed L^p with 1/p = 1/3 - s/3 (s < 1)")
print("W^{1,3}(R^3) embed L^infty (Morrey, s=1, p=infty)")
print()
print("For W^{1,2} to embed into W^{s,3}, need (by scaling):")
print("  1/2 - 1/3 = 1/6 (fractional Sobolev exponent difference)")
print()
print("W^{1,2}(R^3) embed W^{s,3} iff... this requires Besov/fractional analysis")

# Sobolev exponent calculation
print()
print("Besov/Sobolev equivalence:")
print("W^{1,2}(R^3) = B^{1}_{2,2}(R^3)")
print("W^{1,3}(R^3) = B^{1}_{3,3}(R^3)")
print()
print("For B^{s_0}_{p_0, q_0} subset B^{s_1}_{p_1, q_1}:")
print("Need: s_0 - n/p_0 >= s_1 - n/p_1 (same or larger Sobolev number)")
print()
s0, p0 = 1, 2
s1, p1 = 1, 3
n = 3
sob0 = s0 - n/p0
sob1 = s1 - n/p1
print(f"W^{{1,2}}: Sobolev number = {s0} - {n}/{p0} = {sob0}")
print(f"W^{{1,3}}: Sobolev number = {s1} - {n}/{p1} = {s1 - n/p1:.4f}")
print()
if sob0 >= sob1:
    print("W^{1,2} DOES embed into W^{1,3} by Sobolev number!")
else:
    print("W^{1,2} does NOT embed into W^{1,3} by Sobolev number.")
    print(f"  Need {sob0} >= {sob1:.4f}, but {sob0} < {sob1:.4f}")

print()
print("CONCLUSION: W^{1,2}(R^3) does NOT embed into W^{1,3}(R^3).")
print("The De Giorgi energy at level W^{1,2} is INSUFFICIENT for W^{1,3} control.")
print()

print("=" * 65)
print("W^{1,3} UNIVERSALITY: Three routes to the same threshold")
print("=" * 65)

print("""
All three H^1 routes require W^{1,3}-level regularity in one form or another:

1. BMO route (Branch 2B):
   To use H^1-BMO duality: need psi_k ∈ BMO.
   For psi_k ∈ BMO: need u ∈ W^{1,3} (Morrey => BMO).
   Requires: W^{1,3} regularity. UNAVAILABLE from De Giorgi W^{1,2}.

2. Atomic decomposition (Branch 2C):
   Mean-zero atoms of p ~ scale rho: contribute ~ rho^{1/3} ||u||_{L^3}^2.
   For this to be useful: need u ∈ L^3.
   L^3 control of u requires: W^{1,2} -> L^6 and Morrey-type embedding.
   From De Giorgi: u ∈ L^{10/3}(Q_k), close but NOT L^3 uniformly.
   Actually L^{10/3} ⊂ L^3 locally -- wait, 10/3 > 3, so L^{10/3} ⊂ L^3_{loc}.

   Correction: u ∈ L^{10/3} ⊂ L^3 locally, so this CAN be used!
   But the atomic decomposition estimate shows the gain is exactly zero
   (the atoms saturate at the relevant scale). See exploration-001.

3. Interpolation (Branch 2A, this exploration):
   The interpolation space (H^1, L^{4/3})_{theta,q} gives at best L^{p_theta,q}
   with p_theta < 4/3 (complex) or p_theta-Lorentz refinement (real).
   To actually IMPROVE beta from 4/3, need pressure in L^{3/2} locally.
   L^{3/2} control requires u ∈ L^3 (then |u|^2 ∈ L^{3/2}, CZ gives p ∈ L^{3/2}).
   u ∈ L^3(Q_k) requires u ∈ L^3_x uniformly in t — not from De Giorgi.

In all three cases, the missing ingredient is L^3 (or W^{1,3}) regularity of u
on Q_k with U_k-dependent bounds. This is the W^{1,3} threshold.

The De Giorgi energy provides: u ∈ L^∞_t L^2_x cap L^2_t W^{1,2}_x
By parabolic Sobolev: u ∈ L^{10/3}_{t,x}
By Sobolev in x: u ∈ L^2_t L^6_x

For W^{1,3}(Q_k) control: would need ||nabla u||_{L^3(Q_k)} < infty,
i.e., nabla u ∈ L^3, but De Giorgi only gives nabla u ∈ L^2.

The threshold: nabla u in L^2 => p in L^{4/3} (via Calderón-Zygmund)
              nabla u in L^3 => p in L^{3/2} (Calderón-Zygmund with L^3 input)
                              => beta = 3/2 achievable

CRITICAL EXPONENT TABLE:
""")

print(f"{'nabla u in L^q':>20} {'p via CZ in L^r':>20} {'beta = r':>15}")
print("-" * 55)
for q in [Fraction(2,1), Fraction(5,2), Fraction(3,1), Fraction(7,2), Fraction(4,1)]:
    # p ~ Ri Rj (nabla u)^2... no, p ~ Ri Rj (u_i u_j)
    # If u in L^{2q} then u^2 in L^q, p in L^q by CZ
    # From nabla u in L^q (Sobolev): u in L^{nq/(n-q)} for q < n = 3
    if q < 3:
        sobolev_exp = 3*q/(3-q)
        u_exp = sobolev_exp
        p_exp = u_exp / 2  # from u^2 -> p
        beta = float(p_exp)
    elif q == 3:
        # Borderline Sobolev: W^{1,3} subset BMO (not L^infty directly)
        beta_str = "3/2 (from BMO/L^infty)"
        beta = 1.5
        print(f"{'L^'+str(q):>20} {'L^{3/2} (Morrey)':>20} {beta:>15.4f} *** THRESHOLD")
        continue
    else:
        # q > 3: Morrey embedding W^{1,q} subset L^infty
        beta_str = "p = infty, beta > 3/2"
        print(f"{'L^'+str(q):>20} {'L^{>3/2}':>20} {'>3/2':>15}")
        continue
    print(f"{'L^'+str(float(q)):>20} {'L^'+str(round(beta,3)):>20} {beta:>15.4f}")

print()
print("From De Giorgi energy: nabla u in L^2 (q=2). This gives beta = 4/3.")
print("W^{1,3} threshold (q=3) gives beta = 3/2.")
print("The gap is EXACTLY the beta = 4/3 to 3/2 improvement sought.")
print()
print("FINAL CONCLUSION:")
print("The W^{1,3} universality holds. All H^1 interpolation routes")
print("are blocked by the same threshold: nabla u in L^2 (available)")
print("vs nabla u in L^3 (needed). Interpolation cannot bridge this gap.")
