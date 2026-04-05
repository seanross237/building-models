"""Tasks 2+4: K(tau) from empirical R2, then Delta3 via Sigma2 route."""
import numpy as np

# Load R2
d = np.load('r2_empirical.npz')
r = d['r_grid']
R2 = d['R2']
R2_GUE = d['R2_GUE']
dr = r[1] - r[0]

# ---- TASK 2: K(tau) ----
tau = np.linspace(0, 3, 301)
K_emp = np.zeros(len(tau))
K_gue_num = np.zeros(len(tau))
for i, t in enumerate(tau):
    integrand = (R2 - 1.0) * np.cos(2*np.pi*t*r)
    K_emp[i] = 1.0 + 2.0*np.trapz(integrand, r)
    integrand_g = (R2_GUE - 1.0) * np.cos(2*np.pi*t*r)
    K_gue_num[i] = 1.0 + 2.0*np.trapz(integrand_g, r)

K_gue_exact = np.minimum(np.abs(tau), 1.0)

print("=== TASK 2: K(tau) ===")
print(f"{'tau':>5} {'K_emp':>10} {'K_GUE_num':>10} {'K_GUE_exact':>12}")
for tv in [0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0]:
    idx = int(tv / (tau[1]-tau[0]))
    print(f"{tv:5.1f} {K_emp[idx]:10.4f} {K_gue_num[idx]:10.4f} {K_gue_exact[idx]:12.4f}")

np.savez('k_tau_empirical.npz', tau=tau, K_emp=K_emp, K_gue_num=K_gue_num, K_gue_exact=K_gue_exact)
print("Saved k_tau_empirical.npz")

# ---- TASK 4: Delta3 via Sigma2 ----
# Sigma2(L) = L + 2*int_0^L (L-s)*(R2(s)-1) ds
# We need R2 on a fine grid up to L_max ~ 30
# R2 is on r grid with dr=0.05 up to ~30

L_vals = np.linspace(0.1, 30, 300)
Sigma2 = np.zeros(len(L_vals))
Sigma2_GUE = np.zeros(len(L_vals))

for i, L in enumerate(L_vals):
    mask = r <= L
    if mask.sum() < 2:
        Sigma2[i] = L
        Sigma2_GUE[i] = L
        continue
    rr = r[mask]
    integrand = (L - rr) * (R2[mask] - 1.0)
    Sigma2[i] = L + 2.0*np.trapz(integrand, rr)
    integrand_g = (L - rr) * (R2_GUE[mask] - 1.0)
    Sigma2_GUE[i] = L + 2.0*np.trapz(integrand_g, rr)

print("\n=== Sigma2(L) ===")
print(f"{'L':>5} {'Sig2_emp':>10} {'Sig2_GUE':>10}")
for lv in [1, 2, 5, 10, 15, 20, 25]:
    idx = np.argmin(np.abs(L_vals - lv))
    print(f"{lv:5d} {Sigma2[idx]:10.4f} {Sigma2_GUE[idx]:10.4f}")

# Delta3(L) = (2/L^4) * int_0^L (L^3 - 2*L^2*s + s^3) * Sigma2(s) ds
# We interpolate Sigma2 onto L_vals
Delta3 = np.zeros(len(L_vals))
Delta3_GUE = np.zeros(len(L_vals))

for i, L in enumerate(L_vals):
    if i < 2:
        Delta3[i] = L/15.0
        Delta3_GUE[i] = L/15.0
        continue
    mask = L_vals[:i+1] <= L
    ss = L_vals[:i+1][mask]
    weight = L**3 - 2*L**2*ss + ss**3
    integrand = weight * Sigma2[:i+1][mask]
    integrand_g = weight * Sigma2_GUE[:i+1][mask]
    Delta3[i] = (2.0/L**4) * np.trapz(integrand, ss)
    Delta3_GUE[i] = (2.0/L**4) * np.trapz(integrand_g, ss)

# Analytic GUE: Delta3 ~ (1/pi^2)(log(L) - 0.0687)
Delta3_GUE_analytic = (1.0/np.pi**2) * (np.log(L_vals) - 0.0687)
Delta3_GUE_analytic[L_vals < 1] = L_vals[L_vals < 1] / 15.0

print("\n=== TASK 4: Delta3(L) ===")
print(f"{'L':>5} {'D3_emp':>10} {'D3_GUE_num':>11} {'D3_GUE_anal':>12}")
for lv in [1, 2, 5, 10, 15, 20, 25, 30]:
    idx = np.argmin(np.abs(L_vals - lv))
    print(f"{lv:5d} {Delta3[idx]:10.4f} {Delta3_GUE[idx]:11.4f} {Delta3_GUE_analytic[idx]:12.4f}")

# Saturation region
mask_sat = (L_vals >= 15) & (L_vals <= 25)
D3_sat_emp = np.mean(Delta3[mask_sat])
D3_sat_gue = np.mean(Delta3_GUE[mask_sat])
D3_sat_gue_a = np.mean(Delta3_GUE_analytic[mask_sat])

print(f"\n=== SATURATION (L=15-25 average) ===")
print(f"Delta3_sat (empirical from zeta zeros): {D3_sat_emp:.4f}")
print(f"Delta3_sat (GUE numerical from R2):     {D3_sat_gue:.4f}")
print(f"Delta3_sat (GUE analytic):              {D3_sat_gue_a:.4f}")
print(f"Target from prior work:                  0.155")
print(f"Ratio emp/GUE_analytic:                  {D3_sat_emp/D3_sat_gue_a:.4f}")

np.savez('delta3_results.npz', L=L_vals, Delta3_emp=Delta3, Delta3_GUE_num=Delta3_GUE,
         Delta3_GUE_analytic=Delta3_GUE_analytic, Sigma2_emp=Sigma2, Sigma2_GUE=Sigma2_GUE,
         D3_sat_emp=D3_sat_emp, D3_sat_gue=D3_sat_gue)
print("Saved delta3_results.npz")
