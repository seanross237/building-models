"""Task 0: Setup and Data Loading — load zeros, unfold, compute parameters."""
import numpy as np
import pickle
import os

# Try to load cached zeros
cache_path = "../exploration-002/code/zeros_cache.pkl"
zeros_npz_path = "../exploration-002/code/zeros.npz"

if os.path.exists(cache_path):
    print(f"Loading cached zeros from {cache_path}")
    with open(cache_path, 'rb') as f:
        zeros_data = pickle.load(f)
    print(f"Type: {type(zeros_data)}")
    if isinstance(zeros_data, dict):
        print(f"Keys: {zeros_data.keys()}")
    elif isinstance(zeros_data, (list, np.ndarray)):
        print(f"Length: {len(zeros_data)}, first element type: {type(zeros_data[0])}")
        print(f"First 3 elements: {zeros_data[:3]}")

if os.path.exists(zeros_npz_path):
    print(f"\nLoading zeros.npz from {zeros_npz_path}")
    data = np.load(zeros_npz_path)
    print(f"Keys: {list(data.keys())}")
    for k in data.keys():
        v = data[k]
        if v.ndim > 0:
            print(f"  {k}: shape={v.shape}, first 3={v[:3]}")
        else:
            print(f"  {k}: scalar={v}")

# Load zeros — prefer the npz file
if os.path.exists(zeros_npz_path):
    data = np.load(zeros_npz_path)
    if 'zeros' in data:
        t_array = data['zeros']
    elif 'zero_imag_parts' in data:
        t_array = data['zero_imag_parts']
    elif 'imaginary_parts' in data:
        t_array = data['imaginary_parts']
    else:
        t_array = data[list(data.keys())[0]]
elif os.path.exists(cache_path):
    with open(cache_path, 'rb') as f:
        zeros_data = pickle.load(f)
    if isinstance(zeros_data, dict):
        t_array = np.array([float(v.imag) if hasattr(v, 'imag') else float(v) for v in zeros_data.values()])
    else:
        t_array = np.array([float(z.imag) if hasattr(z, 'imag') and not isinstance(z, (int, float)) else float(z) for z in zeros_data])
else:
    print("No cached data found, computing from mpmath...")
    from mpmath import zetazero
    zeros_list = []
    for n in range(1, 2001):
        z = zetazero(n)
        zeros_list.append(float(z.imag))
        if n % 200 == 0:
            print(f"  Computed {n}/2000 zeros")
    t_array = np.array(zeros_list)

print(f"\nLoaded {len(t_array)} zeros")
print(f"First 5: {t_array[:5]}")
print(f"Last 5: {t_array[-5:]}")
print(f"Min: {t_array.min():.4f}, Max: {t_array.max():.4f}")

# Sort
t_array = np.sort(t_array)
N = len(t_array)

# Geometric mean height
T_geo = np.exp(np.mean(np.log(t_array)))
print(f"\nT_geo (geometric mean): {T_geo:.4f}")

# Mean zero density
rho_bar = np.log(T_geo / (2 * np.pi)) / (2 * np.pi)
print(f"rho_bar = log(T_geo/(2π))/(2π) = {rho_bar:.6f}")

# Unfolding using Riemann-von Mangoldt: N̄(t) = (t/(2π))log(t/(2π)) - t/(2π) + 7/8
# This gives mean spacing ≈ 1
x_array = (t_array / (2 * np.pi)) * np.log(t_array / (2 * np.pi)) - t_array / (2 * np.pi) + 7.0/8.0
print(f"\nUnfolded zeros:")
print(f"  First 5: {x_array[:5]}")
print(f"  Last 5: {x_array[-5:]}")

# Check mean spacing
spacings = np.diff(x_array)
print(f"\nMean spacing of unfolded zeros: {np.mean(spacings):.6f} (should be ≈ 1)")
print(f"Std of spacings: {np.std(spacings):.6f}")

# Save
np.savez('data_zeros.npz', zeros=t_array, unfolded=x_array, T_geo=T_geo, rho_bar=rho_bar)
print(f"\nSaved data_zeros.npz")
print(f"  N = {N}")
print(f"  T_geo = {T_geo:.4f}")
print(f"  rho_bar = {rho_bar:.6f}")
print(f"  Mean unfolded spacing = {np.mean(spacings):.6f}")
