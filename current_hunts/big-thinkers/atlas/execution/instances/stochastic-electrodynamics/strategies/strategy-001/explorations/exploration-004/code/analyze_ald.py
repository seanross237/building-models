"""
Analysis of ALD simulation results vs QM and E003 Langevin.
Determines order of failure and physical interpretation.
"""
import json
import numpy as np
import os

code_dir = os.path.dirname(os.path.abspath(__file__))
results_path = os.path.join(code_dir, 'ald_results.json')

with open(results_path) as f:
    data = json.load(f)

# E003 Langevin results (extracted from REPORT-SUMMARY.md)
LANGEVIN = {
    0.0:  (0.515, 0.007),
    0.01: (0.529, 0.008),
    0.1:  (0.735, 0.014),
    1.0:  (2.411, 0.043),
}

betas = sorted([float(k) for k in data.keys()])
QM_EXACT = {
    0.0:  0.5000, 0.01: 0.4862, 0.05: 0.4458,
    0.1:  0.4125, 0.2:  0.3700, 0.5:  0.3058, 1.0:  0.2571
}

print("=" * 80)
print("3-WAY COMPARISON: ALD vs QM vs Langevin (E003)")
print("=" * 80)
print(f"{'β':>6} | {'var_x QM':>10} | {'var_x ALD':>12} | {'ALD err%':>9} | "
      f"{'ALD σ':>7} | {'var_x Lang':>12} | {'Lang err%':>10}")
print("-" * 85)

results = {}
for beta in betas:
    k = str(beta)
    v = data[k]
    qm = QM_EXACT[beta]
    ald = v['var_x_ald']
    std = v['std_var']
    ald_err_pct = (ald - qm) / qm * 100
    ald_sig = (ald - qm) / std

    lang_str = "---"
    lang_err_str = "---"
    if beta in LANGEVIN:
        lang_mu, lang_std = LANGEVIN[beta]
        lang_err = (lang_mu - qm) / qm * 100
        lang_str = f"{lang_mu:.3f}±{lang_std:.3f}"
        lang_err_str = f"{lang_err:+.1f}%"

    print(f"{beta:6.2f} | {qm:10.4f} | {ald:7.4f}±{std:.4f} | "
          f"{ald_err_pct:+8.2f}% | {ald_sig:+6.1f}σ | {lang_str:>12} | {lang_err_str:>10}")

    results[beta] = {
        'qm': qm, 'ald': ald, 'std': std,
        'err_abs': ald - qm,
        'err_pct': ald_err_pct,
        'err_sig': ald_sig,
    }

print()
print("=" * 80)
print("ORDER-OF-FAILURE ANALYSIS")
print("=" * 80)

# β=0 baseline error
err0 = results[0.0]['err_abs']
print(f"β=0 baseline error: {err0:+.4f} (from UV cutoff / finite τ effects)")
print()
print("β-dependent EXCESS error (err(β) - err(0)):")
print(f"{'β':>6} | {'Δe_β':>10} | {'Δe_β/std':>10} | {'Δe_β/β':>10} | {'Δe_β/β²':>10}")
print("-" * 60)

betas_nonzero = [b for b in betas if b > 0]
for beta in betas_nonzero:
    r = results[beta]
    excess = r['err_abs'] - err0
    n_sig = excess / r['std']
    print(f"{beta:6.3f} | {excess:+.4f}  | {n_sig:+.2f}σ    | "
          f"{excess/beta:+.4f}   | {excess/beta**2:+.4f}")

print()
print("Power-law fit to β-dependent excess (large-β regime: β=0.2, 0.5, 1.0):")
betas_fit = [0.2, 0.5, 1.0]
excesses_fit = [results[b]['err_abs'] - err0 for b in betas_fit]
log_b = np.log([b for b in betas_fit])
log_e = np.log([max(e, 1e-6) for e in excesses_fit])  # avoid log(0)
alpha, log_A = np.polyfit(log_b, log_e, 1)
A = np.exp(log_A)
print(f"  Δe(β) ≈ {A:.4f} × β^{alpha:.2f}")
print()

print("Comparison with expectations:")
print(f"  If O(β¹): ratio Δe(0.5)/Δe(0.2) expected = {0.5/0.2:.2f}, "
      f"observed = {excesses_fit[1]/excesses_fit[0]:.2f}")
print(f"  If O(β²): ratio Δe(0.5)/Δe(0.2) expected = {(0.5/0.2)**2:.2f}, "
      f"observed = {excesses_fit[1]/excesses_fit[0]:.2f}")
print(f"  If O(β^0.4): ratio Δe(0.5)/Δe(0.2) expected = {(0.5/0.2)**0.4:.2f}, "
      f"observed = {excesses_fit[1]/excesses_fit[0]:.2f}")
print()

print("=" * 80)
print("COMPARISON WITH LANGEVIN (E003) — KEY POINTS")
print("=" * 80)
print(f"β=0.01: ALD err = {results[0.01]['err_sig']:+.1f}σ  |  Langevin err = +5.4σ")
print(f"β=0.10: ALD err = {results[0.1]['err_sig']:+.1f}σ  |  Langevin err = +23.6σ")
print(f"β=1.00: ALD err = {results[1.0]['err_sig']:+.1f}σ  |  Langevin err = +50.5σ")
print()
print("Improvement factor (Langevin_err / ALD_err in σ):")
for beta, lang_sig in [(0.01, 5.4), (0.1, 23.6), (1.0, 50.5)]:
    ald_s = abs(results[beta]['err_sig'])
    print(f"  β={beta}: {lang_sig:.1f}σ → {ald_s:.1f}σ  (improvement: {lang_sig/ald_s:.0f}x)")

print()
print("=" * 80)
print("PHYSICAL INTERPRETATION")
print("=" * 80)
print("Effective damping at equilibrium:")
for beta in betas:
    r = results[beta]
    var_x = r['ald']
    # <Gamma_eff> = tau*(omega0^2 + 12*beta*<x^2>)
    # But <x^2> includes both position and fluctuations — use var_x as proxy
    x4 = data[str(beta)]['x4_ald']
    # <x^2> ≈ var_x (since <x>=0)
    gamma_eff = 0.01 * (1.0 + 12.0 * beta * var_x)
    gamma_const = 0.01
    print(f"  β={beta:.2f}: ⟨Γ_eff⟩ = τ(ω₀²+12β⟨x²⟩) = {gamma_eff:.5f}  "
          f"vs constant Γ = {gamma_const:.4f} "
          f"(ratio: {gamma_eff/gamma_const:.2f})")

print()
print("Comparison: ALD DECREASES with β (matches QM direction)")
print("Comparison: Langevin INCREASES with β (wrong direction)")
print()
dv_ald = results[1.0]['ald'] - results[0.0]['ald']
dv_qm = QM_EXACT[1.0] - QM_EXACT[0.0]
dv_lang = 2.411 - 0.515
print(f"Δvar_x from β=0 to β=1:")
print(f"  QM:       {dv_qm:+.3f}")
print(f"  ALD:      {dv_ald:+.3f}")
print(f"  Langevin: {dv_lang:+.3f}")
print()
print("Slope comparison: ALD / QM slope ratio = "
      f"{dv_ald/dv_qm:.2f} (should be 1 for perfect agreement)")
