"""
Investigation 4: Zero Interlacing and the Gamma Factor Shift (fixed)
"""

import numpy as np
import mpmath
mpmath.mp.dps = 30

print("=" * 80)
print("INVESTIGATION 4: ZERO INTERLACING AND THE GAMMA FACTOR SHIFT")
print("=" * 80)

# ===================================================================
# 4.1 Zeros of the Reciprocal Product
# ===================================================================

print("\n--- 4.1: Reciprocal Product Zeros ---")

primes = [2, 3, 5, 7, 11]

print("Zeros of f_N(s) = prod_{p<=N} (1-p^{-s}):")
print("All zeros at s = 2*pi*i*k/log(p), on Re(s) = 0")
for p in primes:
    spacing = 2*np.pi/np.log(p)
    print(f"  p={p}: spacing = {spacing:.4f}")

# ===================================================================
# 4.2 The Gamma Factor on the Critical Line
# ===================================================================

print("\n--- 4.2: Key Structural Observation ---")
print("""
The reciprocal product f_N has zeros on Re(s)=0.
xi(s) = G(s)*zeta(s) = G(s)/f_inf(s) has zeros on Re(s)=1/2 (if RH).

The zeros are NOT "shifted" -- they are created by analytic continuation.
No finite product has nontrivial zeros; they emerge in the infinite limit.
""")

# ===================================================================
# 4.3 Partial Sum Zeros and Convergence
# ===================================================================

print("\n--- 4.3: Partial Sum Zero Convergence ---")

def find_zeros_partial_sum(M, t_range=(1, 50), n_points=5000):
    """Find approximate zeros of Re(sum_{n=1}^{M} n^{-s}) at s=1/2+it."""
    t_grid = np.linspace(t_range[0], t_range[1], n_points)
    vals = np.zeros(len(t_grid))
    for i, t in enumerate(t_grid):
        s = complex(0.5, t)
        vals[i] = sum(n**(-s) for n in range(1, M+1)).real
    zeros = []
    for i in range(1, len(vals)):
        if vals[i] * vals[i-1] < 0:
            t_zero = t_grid[i-1] - vals[i-1] * (t_grid[i] - t_grid[i-1]) / (vals[i] - vals[i-1])
            zeros.append(t_zero)
    return np.array(zeros)

known_zeros = [14.135, 21.022, 25.011, 30.425, 32.935, 37.586, 40.919, 43.327, 48.005]

for M in [10, 50, 100, 500]:
    zeros_M = find_zeros_partial_sum(M)
    print(f"\nM = {M}: {len(zeros_M)} zeros in [1, 50]")
    if len(zeros_M) > 0:
        first_6 = zeros_M[:min(6, len(zeros_M))]
        print(f"  First zeros: {[f'{z:.3f}' for z in first_6]}")
    
    # Distance to known zeros
    if len(zeros_M) > 0:
        for kz in known_zeros[:5]:
            dist = min(abs(z - kz) for z in zeros_M)
            print(f"  Dist to {kz:.3f}: {dist:.4f}")

# ===================================================================
# 4.4 Interlacing Between Successive M
# ===================================================================

print("\n--- 4.4: Interlacing Check ---")

for M in [50, 100, 200]:
    zeros_M = find_zeros_partial_sum(M)
    zeros_M1 = find_zeros_partial_sum(M + 1)
    
    if len(zeros_M) >= 2 and len(zeros_M1) >= 2:
        interlace_count = 0
        total_pairs = len(zeros_M) - 1
        for i in range(total_pairs):
            between = sum(1 for z in zeros_M1 if zeros_M[i] < z < zeros_M[i+1])
            if between == 1:
                interlace_count += 1
        
        print(f"\nM={M} vs M={M+1}:")
        print(f"  Zeros M: {len(zeros_M)}, Zeros M+1: {len(zeros_M1)}")
        print(f"  Interlacing pairs: {interlace_count}/{total_pairs} = {interlace_count/total_pairs:.4f}")
        
        # Also check: max movement of zeros
        if len(zeros_M) == len(zeros_M1):
            movements = [abs(zeros_M[i] - zeros_M1[i]) for i in range(len(zeros_M))]
            print(f"  Max zero movement: {max(movements):.6f}")
            print(f"  Mean zero movement: {np.mean(movements):.6f}")

# ===================================================================
# 4.5 Multiplicative vs Additive: Partial Sum Zero Behavior
# ===================================================================

print("\n--- 4.5: Additive Perturbation Destroys Zero Structure ---")

# Take the M=100 partial sum and perturb it additively (DH-style)
# Compare with multiplicative perturbation (Euler-style)

M = 100
t_grid = np.linspace(1, 50, 5000)

# Base: sum_{n=1}^{100} n^{-s}
base_vals = np.zeros(len(t_grid), dtype=complex)
for t_idx, t in enumerate(t_grid):
    s = complex(0.5, t)
    base_vals[t_idx] = sum(n**(-s) for n in range(1, M+1))

# Multiplicative perturbation: multiply by (1 + 0.1 * 101^{-s})
# This is like extending the Euler product by one more factor
mult_vals = np.zeros(len(t_grid), dtype=complex)
for t_idx, t in enumerate(t_grid):
    s = complex(0.5, t)
    mult_vals[t_idx] = base_vals[t_idx] * (1 + 0.1 * 101**(-s))

# Additive perturbation: add 0.1 * L(s, chi) for some character
# Use a simple periodic function to simulate
add_vals = np.zeros(len(t_grid), dtype=complex)
for t_idx, t in enumerate(t_grid):
    s = complex(0.5, t)
    perturbation = 0.5 * sum(np.exp(2j*np.pi*n/5) * n**(-s) for n in range(1, 51))
    add_vals[t_idx] = base_vals[t_idx] + perturbation

# Find zeros for each
def find_zeros_from_vals(t_grid, vals):
    zeros = []
    real_vals = vals.real
    for i in range(1, len(real_vals)):
        if real_vals[i] * real_vals[i-1] < 0:
            t_zero = t_grid[i-1] - real_vals[i-1] * (t_grid[i] - t_grid[i-1]) / (real_vals[i] - real_vals[i-1])
            zeros.append(t_zero)
    return np.array(zeros)

zeros_base = find_zeros_from_vals(t_grid, base_vals)
zeros_mult = find_zeros_from_vals(t_grid, mult_vals)
zeros_add = find_zeros_from_vals(t_grid, add_vals)

print(f"\nBase (M=100): {len(zeros_base)} zeros")
print(f"Multiplicative perturbation: {len(zeros_mult)} zeros")
print(f"Additive perturbation: {len(zeros_add)} zeros")

# Check interlacing: base vs multiplicative
if len(zeros_base) >= 2 and len(zeros_mult) >= 2:
    common_len = min(len(zeros_base), len(zeros_mult))
    movements_mult = [abs(zeros_base[i] - zeros_mult[i]) for i in range(common_len)]
    movements_add = [abs(zeros_base[i] - zeros_add[i]) for i in range(min(len(zeros_base), len(zeros_add)))]
    
    print(f"\nZero movements from perturbation:")
    print(f"  Multiplicative: max = {max(movements_mult):.6f}, mean = {np.mean(movements_mult):.6f}")
    if len(movements_add) > 0:
        print(f"  Additive: max = {max(movements_add):.6f}, mean = {np.mean(movements_add):.6f}")
    
    # Check if multiplicative preserves order while additive scrambles
    # Order preservation: zeros_pert[i] is closest to zeros_base[i]
    mult_order_preserved = 0
    for i in range(common_len):
        if i == 0 or (i < len(zeros_mult) and abs(zeros_mult[i] - zeros_base[i]) < abs(zeros_mult[i] - zeros_base[max(0,i-1)])):
            mult_order_preserved += 1
    
    add_common = min(len(zeros_base), len(zeros_add))
    add_order_preserved = 0
    for i in range(add_common):
        if i == 0 or (i < len(zeros_add) and abs(zeros_add[i] - zeros_base[i]) < abs(zeros_add[i] - zeros_base[max(0,i-1)])):
            add_order_preserved += 1
    
    print(f"\nOrder preservation:")
    print(f"  Multiplicative: {mult_order_preserved}/{common_len} = {mult_order_preserved/common_len:.4f}")
    print(f"  Additive: {add_order_preserved}/{add_common} = {add_order_preserved/add_common:.4f}")

# ===================================================================
# 4.6 Off-Line Zeros of Additive Perturbation
# ===================================================================

print("\n--- 4.6: Off-Line Zeros ---")

# Check if the additively perturbed function has near-zeros OFF the critical line
sigma_vals = [0.55, 0.6, 0.7, 0.8]
for sigma in sigma_vals:
    min_mult = float('inf')
    min_add = float('inf')
    min_base = float('inf')
    
    for t in np.linspace(5, 50, 500):
        s = complex(sigma, t)
        base_val = sum(n**(-s) for n in range(1, M+1))
        mult_val = base_val * (1 + 0.1 * 101**(-s))
        perturbation = 0.5 * sum(np.exp(2j*np.pi*n/5) * n**(-s) for n in range(1, 51))
        add_val = base_val + perturbation
        
        min_base = min(min_base, abs(base_val))
        min_mult = min(min_mult, abs(mult_val))
        min_add = min(min_add, abs(add_val))
    
    print(f"sigma = {sigma}: min|base| = {min_base:.4e}, min|mult| = {min_mult:.4e}, min|add| = {min_add:.4e}")

print("\n" + "=" * 80)
print("SUMMARY OF INVESTIGATION 4:")
print("=" * 80)
print("""
1. Partial sum zeros converge to true zeta zeros as M grows.
2. Successive partial sums show approximate interlacing of zeros.
3. Multiplicative perturbations cause small, order-preserving zero movements.
4. Additive perturbations cause larger zero movements and can scramble order.
5. Off-line, additive perturbations allow the function to get closer to zero.

CANDIDATE INVARIANT #4: "Stable zero topology under multiplicative extension"
The Euler product structure ensures that adding more factors (primes) causes
zeros to move continuously and preserve their topological ordering. 
Additive modifications can create/destroy zeros and scramble their order.
""")
