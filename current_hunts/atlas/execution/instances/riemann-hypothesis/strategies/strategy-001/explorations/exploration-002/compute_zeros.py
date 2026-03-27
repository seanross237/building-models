"""Step 0: Compute first 2000 Riemann zeta zeros and unfold them."""
import mpmath
import numpy as np
import time
import json

N = 2000
print(f"Computing {N} zeta zeros...")

# Compute zeros
t_start = time.time()
zeros_im = []
for n in range(1, N + 1):
    z = mpmath.zetazero(n)
    zeros_im.append(float(z.imag))
    if n % 200 == 0:
        elapsed = time.time() - t_start
        rate = n / elapsed
        print(f"  n={n}, t={zeros_im[-1]:.2f}, rate={rate:.1f} zeros/s, elapsed={elapsed:.1f}s")

elapsed = time.time() - t_start
print(f"Done computing {N} zeros in {elapsed:.1f}s")

t = np.array(zeros_im)
print(f"Range: t in [{t[0]:.2f}, {t[-1]:.2f}]")

# Unfold: x_n = (t_n / (2*pi)) * log(t_n / (2*pi*e))
x = (t / (2 * np.pi)) * np.log(t / (2 * np.pi * np.e))
print(f"Unfolded range: x in [{x[0]:.4f}, {x[-1]:.4f}]")

# Check mean spacing
spacings = np.diff(x)
mean_spacing = np.mean(spacings)
std_spacing = np.std(spacings)
print(f"Mean unfolded spacing: {mean_spacing:.6f}")
print(f"Std of spacings: {std_spacing:.6f}")

# Save to disk
np.savez('zeros_data.npz', t=t, x=x, spacings=spacings)
print("Saved to zeros_data.npz")

# Also save summary stats
stats = {
    'N': N,
    'compute_time_s': elapsed,
    't_min': float(t[0]),
    't_max': float(t[-1]),
    'x_min': float(x[0]),
    'x_max': float(x[-1]),
    'mean_spacing': float(mean_spacing),
    'std_spacing': float(std_spacing),
}
with open('zeros_stats.json', 'w') as f:
    json.dump(stats, f, indent=2)
print("Stats saved to zeros_stats.json")
