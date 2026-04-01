"""Task 1: Empirical R₂(r) from Zero Pairs."""
import numpy as np

# Load unfolded zeros
data = np.load('data_zeros.npz')
x = data['unfolded']
N = len(x)
print(f"Loaded {N} unfolded zeros")

# Compute all pair spacings |x_i - x_j| for i < j
# For efficiency, only keep spacings up to r_max = 30
r_max = 30.0
dr = 0.05
r_grid = np.linspace(0, r_max, int(r_max / dr) + 1)  # 601 points
n_bins = len(r_grid) - 1
counts = np.zeros(n_bins)

print(f"Computing pair spacings up to r_max={r_max}...")
for i in range(N):
    # Only look at j > i, and only spacings <= r_max
    for j in range(i+1, N):
        gap = x[j] - x[i]
        if gap > r_max:
            break  # sorted, so all further j will be bigger
        bin_idx = int(gap / dr)
        if bin_idx < n_bins:
            counts[bin_idx] += 1

# Use bin centers for r_grid
r_centers = (r_grid[:-1] + r_grid[1:]) / 2

# Normalization: for a point process with density ρ=1,
# the expected number of pairs (i<j) with x_j - x_i ∈ [r, r+dr] is:
#   (N - r) × R₂(r) × dr  ≈  N × R₂(r) × dr  for r << N
# We counted unordered pairs (i<j) with positive spacing, so:
R2 = counts / ((N - r_centers) * dr)  # with boundary correction

print(f"\nR₂ sanity checks:")
print(f"  R₂(0) region [0, 0.1]: {np.mean(R2[:2]):.4f} (should be ~0, level repulsion)")
print(f"  R₂(r≈1): {R2[int(1.0/dr)]:.4f}")
print(f"  R₂(r≈2): {R2[int(2.0/dr)]:.4f}")
print(f"  R₂(r≈5): {R2[int(5.0/dr)]:.4f}")
print(f"  R₂(r≈10): {R2[int(10.0/dr)]:.4f}")
print(f"  R₂(r≈20): {R2[int(20.0/dr)]:.4f}")
print(f"  R₂(r≈29): {R2[int(29.0/dr)]:.4f} (should be ~1)")

# GUE R₂ for comparison
r_gue = r_centers
R2_GUE = 1.0 - (np.sin(np.pi * r_gue) / (np.pi * r_gue + 1e-30))**2

print(f"\nComparison at key points:")
print(f"{'r':>5} {'R₂_emp':>10} {'R₂_GUE':>10} {'diff':>10}")
for r_val in [0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0, 20.0]:
    idx = int(r_val / dr)
    if idx < len(R2):
        print(f"{r_val:5.1f} {R2[idx]:10.4f} {R2_GUE[idx]:10.4f} {R2[idx]-R2_GUE[idx]:10.4f}")

# Check convergence to 1
print(f"\nConvergence check: mean R₂ for r ∈ [25, 30]: {np.mean(R2[int(25/dr):]):.4f}")

np.savez('r2_empirical.npz', r_grid=r_centers, R2=R2, R2_GUE=R2_GUE)
print("\nSaved r2_empirical.npz")
