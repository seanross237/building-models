#!/usr/bin/env python3
"""
Plot: R_delta vs S_T for each system on a log-log plot.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # non-interactive backend
import matplotlib.pyplot as plt
import json

# Load results
with open('results.json', 'r') as f:
    results = json.load(f)

# S_T range: 1 bit to 10^12 bits
S_T = np.logspace(0, 12, 500)

fig, ax = plt.subplots(1, 1, figsize=(12, 8))

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
linestyles = ['-', '--', '-.', ':', '-', '--']

for i, (name, res) in enumerate(results.items()):
    S_max = res['S_eff_bits']
    R_delta = S_max / S_T - 1
    # Only plot where R_delta > 0
    mask = R_delta > 0
    if np.any(mask):
        ax.loglog(S_T[mask], R_delta[mask], 
                  color=colors[i], linestyle=linestyles[i],
                  linewidth=2, label=f"{name} (S_max=10^{res['log10_S_eff']:.1f})")

# Reference lines
ax.axhline(y=1, color='gray', linestyle=':', alpha=0.5, label='R_delta = 1 (min for classicality)')
ax.axhline(y=1e11, color='gray', linestyle='--', alpha=0.3, label='~10^11 (number of neurons)')

ax.set_xlabel('S_T (bits per classical fact)', fontsize=14)
ax.set_ylabel('R_delta (max redundancy number)', fontsize=14)
ax.set_title('Classicality Budget: R_delta = S_max/S_T - 1', fontsize=16)
ax.legend(fontsize=9, loc='upper right')
ax.grid(True, alpha=0.3, which='both')
ax.set_xlim(1, 1e12)
ax.set_ylim(1e-1, 1e130)

plt.tight_layout()
plt.savefig('classicality_budget_plot.png', dpi=150, bbox_inches='tight')
print("Plot saved to classicality_budget_plot.png")

# ============================================================================
# Second plot: Bekenstein vs Holographic bound comparison
# ============================================================================

fig2, ax2 = plt.subplots(1, 1, figsize=(10, 6))

names = list(results.keys())
s_bek = [np.log10(results[n]['S_bek_bits']) for n in names]
s_holo = [np.log10(results[n]['S_holo_bits']) for n in names]
s_eff = [results[n]['log10_S_eff'] for n in names]

x = np.arange(len(names))
width = 0.3

bars1 = ax2.bar(x - width, s_bek, width, label='Bekenstein bound', color='#1f77b4', alpha=0.8)
bars2 = ax2.bar(x, s_holo, width, label='Holographic bound', color='#ff7f0e', alpha=0.8)
bars3 = ax2.bar(x + width, s_eff, width, label='Effective (min)', color='#2ca02c', alpha=0.8)

ax2.set_ylabel('log10(S_max) [bits]', fontsize=12)
ax2.set_title('Entropy Bounds Comparison Across Systems', fontsize=14)
ax2.set_xticks(x)
# Shorten names for x labels
short_names = ['Lab', 'Brain', 'BH', 'Universe', 'Planck', 'QC']
ax2.set_xticklabels(short_names, fontsize=11)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('entropy_bounds_comparison.png', dpi=150, bbox_inches='tight')
print("Plot saved to entropy_bounds_comparison.png")

# ============================================================================
# Third plot: The trade-off curve (R_delta vs N_facts for fixed S_max)
# ============================================================================

fig3, ax3 = plt.subplots(1, 1, figsize=(10, 8))

# For the lab system, show the fundamental trade-off
# If you have N facts each of S_T bits, replicated R times:
# N * R * S_T <= S_max  (approximate)
# So R = S_max / (N * S_T)
# For fixed S_T, R * N = S_max / S_T

for i, (name, res) in enumerate(results.items()):
    S_max = res['S_eff_bits']
    if S_max < 10:
        continue  # skip Planck
    # For S_T = 1 bit: R * N = S_max
    N_range = np.logspace(0, res['log10_S_eff'], 200)
    R_range = S_max / N_range  # this is the trade-off: R * N = S_max (for S_T=1)
    ax3.loglog(N_range, R_range,
               color=colors[i], linewidth=2,
               label=f"{name}")

ax3.set_xlabel('N_facts (number of distinct classical facts)', fontsize=14)
ax3.set_ylabel('R_delta (redundancy per fact)', fontsize=14)
ax3.set_title('Fundamental Trade-off: More Facts vs More Agreement\n(S_T = 1 bit)', fontsize=14)
ax3.legend(fontsize=9)
ax3.grid(True, alpha=0.3, which='both')

# Add annotation
ax3.annotate('More objective\n(fewer facts, more copies)',
             xy=(1e5, 1e35), fontsize=10, color='gray',
             ha='center')
ax3.annotate('Richer reality\n(more facts, fewer copies)',
             xy=(1e35, 1e5), fontsize=10, color='gray',
             ha='center')

plt.tight_layout()
plt.savefig('tradeoff_curve.png', dpi=150, bbox_inches='tight')
print("Plot saved to tradeoff_curve.png")
