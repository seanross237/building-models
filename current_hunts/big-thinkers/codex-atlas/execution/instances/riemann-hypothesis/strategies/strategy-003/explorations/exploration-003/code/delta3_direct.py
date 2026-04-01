"""Direct Delta3 from unfolded zeros (independent cross-check)."""
import numpy as np

data = np.load('data_zeros.npz')
x = data['unfolded']
N = len(x)

def delta3_direct(x_unfolded, L, n_windows=200):
    """Compute Delta3(L) by sliding window over unfolded zeros."""
    x_min, x_max = x_unfolded[0], x_unfolded[-1]
    starts = np.linspace(x_min, x_max - L, n_windows)
    vals = []
    for a in starts:
        b = a + L
        mask = (x_unfolded >= a) & (x_unfolded < b)
        xi = x_unfolded[mask]
        n = len(xi)
        if n < 2:
            continue
        # Shift to [0, L]
        y = xi - a
        # Delta3 = min over (A,B) of (1/L) sum(y_i - A - B*y_i)^2... wait
        # Actually: Delta3(L) = min_{A,B} (1/L) int_a^{a+L} (N(x) - Ax - B)^2 dx
        # For discrete: use the staircase N(x) = #{x_i <= x}
        # Analytic formula for least-squares fit to staircase:
        # N_bar = n, mean_y = mean(y), mean_y2 = mean(y^2)
        S0 = n
        S1 = np.sum(y)
        S2 = np.sum(y**2)
        S3 = np.sum(y**3)
        S4 = np.sum(y**4)
        # Dyson-Mehta formula:
        # Delta3 = (n/L) - (1/L^3)(12*S1 - 6*n*L)^2/(12*n) ...
        # Simpler: use exact formula
        # Delta3 = n/L - (S1/L^2)^2*12/n... no, let me just do it properly

        # Standard formula: Delta3 = (1/L) * [sum_i (y_i - A - B*y_i)^2 integrated]
        # Actually the simplest correct formula for the staircase:
        # Let N(x) = #{i: x_i <= x} for x in [a, a+L]
        # Delta3(L) = min_{A,B} (1/L) int_0^L [N(x+a) - Ax - B]^2 dx
        #
        # Using the explicit solution:
        # A_opt, B_opt from least squares, then evaluate the integral

        # Easier: use the identity
        # Delta3 = (n^2 - 1)/(12*L) - ...
        # Let me use the exact Aurich-Steiner formula

        # Actually simplest: just do the least squares numerically
        # Sample N(x) on a grid
        x_grid = np.linspace(0, L, 500)
        N_grid = np.searchsorted(y, x_grid, side='right').astype(float)
        # Fit N(x) = A*x + B
        A_fit, B_fit = np.polyfit(x_grid, N_grid, 1)
        residuals = N_grid - (A_fit * x_grid + B_fit)
        d3 = np.mean(residuals**2) / 1.0  # 1/L * integral = mean of residuals^2
        vals.append(d3)
    return np.mean(vals) if vals else np.nan

L_list = [2, 5, 10, 15, 20, 25, 30]
print("=== Direct Delta3 from unfolded zeros ===")
print(f"{'L':>5} {'D3_direct':>10}")
d3_direct = {}
for L in L_list:
    d3 = delta3_direct(x, L)
    d3_direct[L] = d3
    print(f"{L:5d} {d3:10.4f}")

# Compare with R2-based
r2_d3 = np.load('delta3_results.npz')
L_r2 = r2_d3['L']
D3_r2 = r2_d3['Delta3_emp']
D3_gue_a = r2_d3['Delta3_GUE_analytic']

print(f"\n=== Comparison ===")
print(f"{'L':>5} {'D3_direct':>10} {'D3_R2':>10} {'D3_GUE_a':>10}")
for L in L_list:
    idx = np.argmin(np.abs(L_r2 - L))
    print(f"{L:5d} {d3_direct[L]:10.4f} {D3_r2[idx]:10.4f} {D3_gue_a[idx]:10.4f}")

sat_direct = np.mean([d3_direct[L] for L in [15, 20, 25]])
print(f"\nDelta3_sat direct (avg L=15,20,25): {sat_direct:.4f}")
print(f"Delta3_sat R2-based:                 {float(r2_d3['D3_sat_emp']):.4f}")
print(f"Delta3_sat GUE analytic:             {np.mean([D3_gue_a[np.argmin(np.abs(L_r2-L))] for L in [15,20,25]]):.4f}")
