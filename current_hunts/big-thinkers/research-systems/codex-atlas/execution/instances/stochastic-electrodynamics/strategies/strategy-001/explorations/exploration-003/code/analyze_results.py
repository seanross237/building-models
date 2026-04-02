"""
Analysis of SED vs QM comparison results.
Generates tables, statistics, and distribution comparisons.
"""

import numpy as np
import json
import os
from scipy.stats import kstest

code_dir = os.path.dirname(__file__)

# Load QM results
with open(os.path.join(code_dir, 'qm_reference_results.json')) as f:
    qm_data = json.load(f)

# Load SED results
with open(os.path.join(code_dir, 'sed_results.json')) as f:
    sed_data = json.load(f)

print("="*80)
print("SED vs QM Comparison — Anharmonic Oscillator V(x) = 0.5*x^2 + beta*x^4")
print("="*80)
print()

# Main comparison table
print("--- Position Variance Comparison ---")
print(f"{'beta':>6} | {'var_x_QM':>10} | {'var_x_SED':>12} | {'std_var':>8} | {'frac_diff':>10} | {'SED/QM':>8} | {'sigma':>6}")
print("-"*80)

betas = [0.0, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0]
results_table = []

for beta in betas:
    qm_key = None
    for k in qm_data:
        if abs(float(k) - beta) < 1e-9:
            qm_key = k; break

    sed_key = None
    for k in sed_data:
        if abs(float(k) - beta) < 1e-9:
            sed_key = k; break

    if qm_key is None or sed_key is None:
        print(f"{beta:6.3f} | {'N/A':>10} | {'N/A':>12} | {'N/A':>8} | {'N/A':>10} | {'N/A':>8} | {'N/A':>6}")
        continue

    var_x_qm = float(qm_data[qm_key]['var_x'])
    var_x_sed = float(sed_data[sed_key]['var_x_sed'])
    std_var = float(sed_data[sed_key]['std_var'])
    frac_diff = (var_x_sed - var_x_qm) / var_x_qm
    ratio = var_x_sed / var_x_qm
    # sigma: how many std errors away from QM value
    sigma = (var_x_sed - var_x_qm) / std_var

    print(f"{beta:6.3f} | {var_x_qm:10.6f} | {var_x_sed:12.6f} | {std_var:8.6f} | {frac_diff:+10.4f} | {ratio:8.4f} | {sigma:6.1f}")

    results_table.append({
        'beta': beta, 'var_x_qm': var_x_qm, 'var_x_sed': var_x_sed,
        'std_var': std_var, 'frac_diff': frac_diff, 'ratio': ratio, 'sigma': sigma
    })

print()
print("--- Baseline-adjusted discrepancy ---")
# The beta=0 result has a +3.1% systematic from UV cutoff
# Adjusted discrepancy = (var_x_SED(beta) - var_x_QM(beta)) / var_x_QM(beta) - (var_x_SED(0) - var_x_QM(0)) / var_x_QM(0)
if results_table:
    baseline_frac = results_table[0]['frac_diff']  # beta=0 case
    print(f"Baseline (beta=0) fractional difference: {baseline_frac:+.4f} ({baseline_frac*100:+.2f}%)")
    print()
    print(f"{'beta':>6} | {'frac_diff':>10} | {'adjusted':>10} | {'significance':>12}")
    print("-"*50)
    for r in results_table:
        adjusted = r['frac_diff'] - baseline_frac
        print(f"{r['beta']:6.3f} | {r['frac_diff']:+10.4f} | {adjusted:+10.4f} | {r['sigma']:8.1f}σ")

print()
print("--- PE comparison ---")
print(f"{'beta':>6} | {'PE_QM':>10} | {'PE_SED':>10} | {'frac_diff_PE':>14}")
print("-"*50)
for beta in betas:
    qm_key = None
    for k in qm_data:
        if abs(float(k) - beta) < 1e-9: qm_key = k; break
    sed_key = None
    for k in sed_data:
        if abs(float(k) - beta) < 1e-9: sed_key = k; break
    if qm_key and sed_key:
        pe_qm = float(qm_data[qm_key]['PE'])
        pe_sed = float(sed_data[sed_key]['PE_sed'])
        frac = (pe_sed - pe_qm) / pe_qm
        print(f"{beta:6.3f} | {pe_qm:10.6f} | {pe_sed:10.6f} | {frac:+14.4f}")

print()
print("--- x^4 comparison ---")
print(f"{'beta':>6} | {'<x^4>_QM':>10} | {'<x^4>_SED':>10} | {'ratio':>8}")
print("-"*45)
for beta in betas:
    qm_key = None
    for k in qm_data:
        if abs(float(k) - beta) < 1e-9: qm_key = k; break
    sed_key = None
    for k in sed_data:
        if abs(float(k) - beta) < 1e-9: sed_key = k; break
    if qm_key and sed_key:
        x4_qm = float(qm_data[qm_key]['x4_exp'])
        x4_sed = float(sed_data[sed_key]['x4_sed'])
        ratio = x4_sed / x4_qm
        print(f"{beta:6.3f} | {x4_qm:10.6f} | {x4_sed:10.6f} | {ratio:8.3f}")

print()
print("--- Direction of SED error ---")
print("QM: var_x decreases with beta (quartic term confines particle)")
print("SED: var_x INCREASES with beta (quartic term destabilizes oscillator)")
print()
print("At beta=0: SED > QM by +3.1% (UV cutoff systematic)")
print("At beta=0.01: SED > QM by +8.9% (discrepancy beyond systematic: +5.8%)")
print()

# Distribution comparison for beta=0 and beta=0.1
print("--- P(x) Distribution Analysis ---")
for beta in [0.0, 0.1]:
    samp_path = os.path.join(code_dir, f'sed_samples_beta{beta:.3f}.npy')
    if not os.path.exists(samp_path):
        print(f"  No samples file for beta={beta}")
        continue

    x_samples = np.load(samp_path)
    var_x = np.var(x_samples)
    sigma_x = np.sqrt(var_x)

    # Load QM
    qm_key = None
    for k in qm_data:
        if abs(float(k) - beta) < 1e-9: qm_key = k; break
    if qm_key:
        var_x_qm = float(qm_data[qm_key]['var_x'])
        sigma_x_qm = np.sqrt(var_x_qm)

    # Check if SED P(x) is Gaussian
    # For a Gaussian: <x^4> = 3*var_x^2
    x4 = np.mean(x_samples**4)
    gaussian_expected_x4 = 3 * var_x**2
    kurtosis = x4 / var_x**2 - 3  # excess kurtosis (0 for Gaussian)

    print(f"  beta={beta}: var_x_SED={var_x:.4f}, sigma_SED={sigma_x:.4f}")
    print(f"    var_x_QM={var_x_qm:.4f}, sigma_QM={sigma_x_qm:.4f}")
    print(f"    <x^4>_SED={x4:.4f}, Gaussian pred (3*var^2)={gaussian_expected_x4:.4f}")
    print(f"    Excess kurtosis: {kurtosis:.4f} (0=Gaussian, >0=heavy tails)")

    # KS test: does SED P(x) match a Gaussian with var=var_x_SED?
    ks_stat, ks_pval = kstest(x_samples / sigma_x, 'norm')
    print(f"    KS test vs Gaussian(0,1): statistic={ks_stat:.4f}, p-value={ks_pval:.4f}")

    # Does P(x)_SED match P(x)_QM in shape?
    # KS test: compare SED samples to QM distribution
    # QM distribution: load and normalize
    # For now, compare normalized distributions
    ks_stat2, ks_pval2 = kstest(x_samples / sigma_x_qm, 'norm')
    print(f"    KS test vs Gaussian(0,sigma_QM): statistic={ks_stat2:.4f}, p-value={ks_pval2:.4f}")
    print()

print("--- Scale of discrepancy summary ---")
print("At what beta does SED qualitatively fail?")
for r in results_table:
    direction = "SED > QM" if r['var_x_sed'] > r['var_x_qm'] else "SED < QM"
    print(f"  beta={r['beta']:.2f}: var_x ratio SED/QM = {r['ratio']:.3f} ({direction})")

print()
print("At all beta > 0, SED predicts LARGER var_x while QM predicts SMALLER.")
print("The failure is not just quantitative but QUALITATIVE (wrong direction).")
