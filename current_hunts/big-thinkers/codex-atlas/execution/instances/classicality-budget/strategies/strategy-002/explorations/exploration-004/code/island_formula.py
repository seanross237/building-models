"""
Island Formula and Page Transition — Classicality Budget Computation
Exploration 004, Strategy 002

Computes:
 1. Page curve S(R,t) using both linear and CFT (log) models
 2. R_delta(t) = S(R,t)/S_T - 1 through the full evaporation
 3. Classicality transition time t_classical for various BH sizes
 4. Interior vs. exterior classicality budget
 5. Comparison of simple vs JT-gravity CFT models

References:
 - Penington (2019) arXiv:1905.08255
 - Almheiri et al. (2019) arXiv:1911.09536
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────────────────────
# PART 1: LINEAR (SIMPLE) MODEL
# ─────────────────────────────────────────────────────────────────────────────

def page_curve_linear(t, S_BH, t_evap):
    """
    Simple piecewise-linear Page curve.
    Before Page time: S(R) = S_BH * t / t_evap
    After Page time:  S(R) = S_BH * (1 - (t - t_page)/t_evap)
    Page time = t_evap / 2
    """
    t_page = t_evap / 2.0
    S_hawking = S_BH * t / t_evap
    S_island = S_BH * (1.0 - (t - t_page) / t_evap)
    # Island formula: take the minimum (whichever phase applies)
    return np.where(t < t_page, S_hawking, S_island)


def r_delta_linear(t, S_BH, t_evap, S_T=1.0):
    """R_delta = S(R,t) / S_T - 1  for the linear model."""
    S_R = page_curve_linear(t, S_BH, t_evap)
    return S_R / S_T - 1.0


def t_classical_linear(S_BH, t_evap, S_T=1.0):
    """
    Time when R_delta first = 0, i.e., S(R,t) = S_T.
    In the linear (growing) phase: t_classical = t_evap * S_T / S_BH
    This is well before the Page time t_evap/2 for large S_BH.
    """
    return t_evap * S_T / S_BH


def t_for_redundancy_k_linear(S_BH, t_evap, k, S_T=1.0):
    """
    Time when R_delta first reaches k, i.e., S(R,t) = S_T * (k+1).
    R_delta = k  iff  S(R) = S_T*(k+1).
    Growing phase: t = t_evap * S_T*(k+1) / S_BH
    Only valid if S_T*(k+1) <= S_BH/2 (i.e., this happens before Page time).
    """
    target_S = S_T * (k + 1.0)
    t = t_evap * target_S / S_BH
    t_page = t_evap / 2.0
    if target_S > S_BH / 2.0:
        # This redundancy level is only reached at or after Page time
        # On the decreasing branch: S = S_BH*(1 - (t-t_page)/t_evap)
        # target_S = S_BH*(1 - (t-t_page)/t_evap)
        # (t-t_page)/t_evap = 1 - target_S/S_BH
        # t = t_page + t_evap*(1 - target_S/S_BH)
        # But this is the DECREASING branch - redundancy is SHRINKING after Page time
        # The max R_delta is at Page time: S_BH/2 / S_T - 1
        return None  # Never reached if max < k
    return t


# ─────────────────────────────────────────────────────────────────────────────
# PART 2: CFT (LOG) MODEL — JT Gravity
# ─────────────────────────────────────────────────────────────────────────────

def page_curve_cft(t, S_BH, c=12, beta=1.0, epsilon=1e-10):
    """
    CFT model (Penington 2019 / Almheiri et al.):
    S_Hawking(t) = (c/3) * ln(t/beta)   [for t > beta]
    Island formula: S(R) = min(S_Hawking(t), S_BH - S_Hawking(t))

    The Page time is when S_Hawking(t_Page) = S_BH/2:
      (c/3)*ln(t_Page/beta) = S_BH/2
      t_Page = beta * exp(3*S_BH / (2*c))

    Note: S_Hawking diverges for t->0; we clip at t=epsilon.
    """
    t_safe = np.maximum(t, epsilon)
    S_hawking = (c / 3.0) * np.log(t_safe / beta)
    # Clip to non-negative (we start emission at t=beta conceptually)
    S_hawking = np.maximum(S_hawking, 0.0)
    # After island appears: S(R) = S_BH - S_Hawking (but this also needs care)
    S_island = S_BH - S_hawking
    # Island formula: take minimum; but island only appears once it's smaller
    return np.minimum(S_hawking, np.maximum(S_island, 0.0))


def page_time_cft(S_BH, c=12, beta=1.0):
    """
    t_Page in CFT model: (c/3)*ln(t_Page/beta) = S_BH/2
    => t_Page = beta * exp(3*S_BH/(2*c))

    For large S_BH this is astronomically large — we work in normalized units.
    """
    return beta * np.exp(3.0 * S_BH / (2.0 * c))


def evap_time_cft(S_BH, c=12, beta=1.0):
    """
    Total evaporation time in CFT model: S_Hawking(t_evap) = S_BH
    => (c/3)*ln(t_evap/beta) = S_BH
    => t_evap = beta * exp(3*S_BH/c)
    """
    return beta * np.exp(3.0 * S_BH / c)


# ─────────────────────────────────────────────────────────────────────────────
# PART 3: COMPUTATIONS
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 70)
print("ISLAND FORMULA — CLASSICALITY BUDGET COMPUTATION")
print("=" * 70)

# ── 3A: Page curve and R_delta for various BH sizes (linear model) ──────────

print("\n--- Part 1: Page Curve and R_delta(t) [LINEAR MODEL] ---")

BH_cases = {
    "Solar mass (S_BH=1e77)": 1e77,
    "Intermediate (S_BH=1e10)": 1e10,
    "Small (S_BH=100)": 100,
    "Tiny (S_BH=10)": 10,
}

S_T = 1.0      # 1 bit per fact
t_evap = 1.0   # normalized
t_page = 0.5

t = np.linspace(0.0, t_evap, 10000)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Page Curve S(R,t) — Linear Model — Various BH Sizes", fontsize=14)

for ax, (label, S_BH) in zip(axes.flatten(), BH_cases.items()):
    S_R = page_curve_linear(t, S_BH, t_evap)
    R_d = r_delta_linear(t, S_BH, t_evap, S_T)

    ax2 = ax.twinx()
    ax.plot(t, S_R / S_BH, 'b-', lw=2, label='S(R)/S_BH')
    ax2.plot(t, R_d / S_BH, 'r-', lw=1.5, alpha=0.7, label='R_δ/S_BH')

    ax.axvline(t_page, color='k', ls='--', lw=1, alpha=0.7, label='Page time')
    t_cl = t_classical_linear(S_BH, t_evap, S_T)
    if t_cl < t_evap:
        ax.axvline(t_cl, color='g', ls=':', lw=1.5, label=f't_class={t_cl:.2e}')

    ax.set_xlabel('t / t_evap')
    ax.set_ylabel('S(R,t) / S_BH', color='b')
    ax2.set_ylabel('R_δ(t) / S_BH', color='r')
    ax.set_title(label)
    ax.legend(loc='upper left', fontsize=8)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.05, 1.05)

plt.tight_layout()
plt.savefig('page_curve_linear.png', dpi=120, bbox_inches='tight')
plt.close()
print("  Saved: page_curve_linear.png")

# ── 3B: Classicality transition table ───────────────────────────────────────

print("\n--- Part 2: Classicality Transition Times ---")
print("\nDefinition: t_classical = time when R_delta >= 0 (S(R) >= 1 bit)")
print("In linear model: t_classical = t_evap * S_T / S_BH = t_Page * 2/S_BH\n")

header = f"{'S_BH (bits)':>20} | {'t_cl/t_Page':>15} | {'t_cl/t_evap':>15} | {'R_delta(t_Page)':>20} | Note"
print(header)
print("-" * len(header))

table_data = {}
for S_BH in [1e77, 1e50, 1e20, 1e10, 1e6, 1e4, 1000, 100, 10]:
    t_cl = t_classical_linear(S_BH, t_evap=1.0, S_T=1.0)
    t_cl_over_tpage = t_cl / t_page
    R_at_tpage = S_BH / (2.0 * S_T) - 1.0

    if t_cl < t_page:
        note = "transition BEFORE Page time"
    elif t_cl < t_evap:
        note = "transition AFTER Page time (decreasing branch)"
    else:
        note = "BH evaporates before reaching R_delta=0"

    table_data[S_BH] = {
        't_cl': t_cl,
        't_cl_over_tpage': t_cl_over_tpage,
        'R_at_tpage': R_at_tpage
    }

    print(f"{S_BH:>20.2e} | {t_cl_over_tpage:>15.3e} | {t_cl:>15.3e} | {R_at_tpage:>20.3e} | {note}")

# ── 3C: Meaningful redundancy thresholds (k = 1, 2, 10, 100) ───────────────

print("\n--- Part 3: Time to Reach Various Redundancy Levels ---")
print("(t when R_delta first reaches k, as fraction of t_Page)\n")

ks = [0, 1, 2, 10, 100, 1000]
BH_masses = [1e77, 1e10, 100, 10]

print(f"{'S_BH':>12} | " + " | ".join(f"{'k='+str(k):>12}" for k in ks))
print("-" * (16 + 15 * len(ks)))

for S_BH in BH_masses:
    row = f"{S_BH:>12.2e} | "
    parts = []
    for k in ks:
        t_k = t_for_redundancy_k_linear(S_BH, t_evap=1.0, k=k, S_T=1.0)
        if t_k is None:
            # k exceeds max possible R_delta (= S_BH/2 - 1)
            max_R = S_BH / 2.0 - 1.0
            if max_R < k:
                parts.append(f"{'NEVER':>12}")
            else:
                parts.append(f"{'(dec.branch)':>12}")
        else:
            ratio = t_k / t_page
            parts.append(f"{ratio:>12.3e}")
    print(row + " | ".join(parts))

print("\nNote: All entries are t_k / t_Page (time to reach R_delta=k, divided by Page time)")

# ── 3D: Interior vs Exterior classicality budget ─────────────────────────────

print("\n--- Part 4: Interior vs Exterior Classicality Budget ---")
print("""
EXTERIOR (reading Hawking radiation):
  R_delta_ext(t) = S(R,t)/S_T - 1  [computed from island formula above]
  - Grows before Page time: S(R) increasing
  - Shrinks after Page time: S(R) decreasing (island appears)
  - Transition to R_delta >= 0 at t_classical << t_Page for large BH

INTERIOR (operators behind the horizon):
  BEFORE Page time: Entanglement wedge of radiation does NOT include interior.
    => Interior operators cannot be reconstructed from exterior radiation.
    => R_delta_int = 0 (no copies of interior facts in exterior)
    => Interior is NOT QD-classical from exterior perspective.

  AFTER Page time: Island appears. Interior IS in entanglement wedge.
    => Interior operators CAN be reconstructed from exterior radiation.
    => R_delta_int > 0: interior facts have "copies" in Hawking radiation.
    => Interior BECOMES QD-classical from exterior perspective.

KEY ASYMMETRY:
  t_classical_ext << t_Page  (exterior radiation becomes classical long before Page time)
  t_classical_int = t_Page   (interior classicality appears EXACTLY at Page time)

This is a genuine two-stage structure.
""")

S_BH = 1e77
R_at_tpage = S_BH / (2.0 * S_T) - 1.0
t_cl_ext = t_classical_linear(S_BH, 1.0, S_T)

print(f"Solar mass BH (S_BH = {S_BH:.2e} bits):")
print(f"  t_classical_ext / t_Page  = {t_cl_ext/t_page:.3e}")
print(f"  t_classical_int / t_Page  = 1.000 (exactly at Page time by island formula)")
print(f"  R_delta_ext at Page time  = {R_at_tpage:.3e}")
print(f"  R_delta_int just before Page time = 0 (no island)")
print(f"  R_delta_int just after  Page time = {R_at_tpage:.3e} (island fully present)")

# ── 3E: CFT log model ─────────────────────────────────────────────────────────

print("\n--- Part 5: CFT (Log) Model Comparison ---")

S_BH_small = 30.0   # small enough for manageable numbers in log model
c = 12              # central charge (standard choice)
beta = 1.0          # inverse Hawking temperature (normalized)

t_page_cft = page_time_cft(S_BH_small, c, beta)
t_evap_cft = evap_time_cft(S_BH_small, c, beta)

print(f"\nParameters: S_BH={S_BH_small}, c={c}, beta={beta}")
print(f"  t_Page (CFT)  = beta * exp(3*S_BH/(2c)) = {t_page_cft:.4f}")
print(f"  t_evap (CFT)  = beta * exp(3*S_BH/c)    = {t_evap_cft:.4f}")
print(f"  t_Page/t_evap = {t_page_cft/t_evap_cft:.4f}  (should be ~0.5 for symmetric model)")

# Verify: in log model, t_Page/t_evap = exp(3*S_BH/(2c)) / exp(3*S_BH/c)
#       = exp(-3*S_BH/(2c))  ≠ 0.5 in general — the log model is NOT symmetric!
t_ratio_cft = t_page_cft / t_evap_cft
print(f"\n  NOTE: In the CFT model, t_Page/t_evap = exp(-3*S_BH/(2c)) = {t_ratio_cft:.4f}")
print(f"  This is << 0.5 for large S_BH — the Page time is early in the evaporation!")

# Plot CFT model
t_cft = np.linspace(beta * 0.01, t_evap_cft * 1.0, 5000)
S_R_cft = page_curve_cft(t_cft, S_BH_small, c, beta)
S_hawking_cft = (c / 3.0) * np.log(np.maximum(t_cft, 1e-10) / beta)
S_hawking_cft = np.maximum(S_hawking_cft, 0.0)
R_delta_cft = S_R_cft / S_T - 1.0

t_cft_lin = np.linspace(0, 1.0, 5000)
S_R_lin = page_curve_linear(t_cft_lin, S_BH_small, 1.0)
R_delta_lin = r_delta_linear(t_cft_lin, S_BH_small, 1.0, S_T)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

ax = axes[0]
ax.plot(t_cft / t_evap_cft, S_R_cft, 'b-', lw=2, label='CFT/island formula')
ax.plot(t_cft / t_evap_cft, S_hawking_cft, 'b--', lw=1.5, alpha=0.5, label='S_Hawking (no island)')
ax.plot(t_cft_lin, S_R_lin, 'r-', lw=2, alpha=0.7, label='Linear model')
ax.axvline(t_page_cft / t_evap_cft, color='b', ls=':', lw=1.5, label=f'CFT Page time ({t_page_cft/t_evap_cft:.3f})')
ax.axvline(0.5, color='r', ls=':', lw=1.5, alpha=0.7, label='Linear Page time (0.5)')
ax.set_xlabel('t / t_evap')
ax.set_ylabel('S(R,t) in bits')
ax.set_title(f'Page Curve: Linear vs CFT  [S_BH={S_BH_small}, c={c}]')
ax.legend(fontsize=8)
ax.set_xlim(0, 1)

ax = axes[1]
ax.plot(t_cft / t_evap_cft, R_delta_cft, 'b-', lw=2, label='R_δ(t) CFT')
ax.plot(t_cft_lin, R_delta_lin, 'r-', lw=2, alpha=0.7, label='R_δ(t) linear')
ax.axhline(0, color='k', ls='-', lw=0.8)
ax.axvline(t_page_cft / t_evap_cft, color='b', ls=':', lw=1.5, label='CFT Page time')
ax.axvline(0.5, color='r', ls=':', lw=1.5, alpha=0.7, label='Linear Page time')
ax.set_xlabel('t / t_evap')
ax.set_ylabel('R_δ(t) = S(R,t)/S_T - 1')
ax.set_title(f'Classicality Budget R_δ(t)')
ax.legend(fontsize=8)
ax.set_xlim(0, 1)

plt.tight_layout()
plt.savefig('page_curve_comparison.png', dpi=120, bbox_inches='tight')
plt.close()
print("\n  Saved: page_curve_comparison.png")

# ── 3F: Main summary figure ───────────────────────────────────────────────────

print("\n--- Generating Main Summary Figure ---")

fig = plt.figure(figsize=(16, 12))
gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.3)

# Panel 1: Page curve (small BH = 100 bits, to see structure clearly)
ax1 = fig.add_subplot(gs[0, 0])
S_BH_demo = 100.0
t = np.linspace(0, 1.0, 10000)
S_R_demo = page_curve_linear(t, S_BH_demo, 1.0)
R_d_demo = r_delta_linear(t, S_BH_demo, 1.0, S_T)
ax1.plot(t, S_R_demo, 'b-', lw=2.5, label='S(R,t) — Page curve')
ax1.axvline(0.5, color='k', ls='--', lw=1.5, label='Page time (t=0.5)')
ax1.axhline(S_T, color='g', ls=':', lw=1.5, label=f'S_T = {S_T} bit')
t_cl_demo = t_classical_linear(S_BH_demo, 1.0, S_T)
ax1.axvline(t_cl_demo, color='g', ls='-', lw=1.5, label=f't_class={t_cl_demo:.3f}')
ax1.fill_between(t, 0, S_R_demo, alpha=0.12, color='blue')
ax1.set_xlabel('t / t_evap', fontsize=11)
ax1.set_ylabel('S(R,t) [bits]', fontsize=11)
ax1.set_title(f'Page Curve [S_BH={int(S_BH_demo)}]', fontsize=12)
ax1.legend(fontsize=8)
ax1.set_xlim(0, 1)
ax1.set_ylim(-2, S_BH_demo * 0.6)

# Panel 2: R_delta(t) small BH
ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(t, R_d_demo, 'r-', lw=2.5, label='R_δ(t)')
ax2.axhline(0, color='k', ls='-', lw=1)
ax2.axvline(0.5, color='k', ls='--', lw=1.5, label='Page time')
ax2.axvline(t_cl_demo, color='g', ls='-', lw=1.5, label=f't_class={t_cl_demo:.3f}')
ax2.fill_between(t, 0, R_d_demo, where=(R_d_demo >= 0), alpha=0.15, color='green',
                 label='Classical region (R_δ≥0)')
ax2.fill_between(t, R_d_demo, 0, where=(R_d_demo < 0), alpha=0.15, color='red',
                 label='Subclassical (R_δ<0)')
ax2.set_xlabel('t / t_evap', fontsize=11)
ax2.set_ylabel('R_δ(t) = S(R,t)/S_T - 1', fontsize=11)
ax2.set_title(f'Classicality Budget R_δ(t) [S_BH={int(S_BH_demo)}]', fontsize=12)
ax2.legend(fontsize=8)
ax2.set_xlim(0, 1)

# Panel 3: t_classical / t_Page vs S_BH
ax3 = fig.add_subplot(gs[1, 0])
S_BH_range = np.logspace(1, 80, 500)
t_cl_ratio = t_classical_linear(S_BH_range, 1.0, S_T) / t_page
ax3.loglog(S_BH_range, t_cl_ratio, 'b-', lw=2.5, label='t_class/t_Page')
ax3.axhline(1.0, color='k', ls='--', lw=1.5, label='= Page time')
ax3.axhline(0.01, color='gray', ls=':', lw=1, label='1% of Page time')
ax3.fill_between(S_BH_range, t_cl_ratio, 1.0, alpha=0.12, color='blue')
# Mark key cases
for S_BH_mark, label_mark in [(1e77, 'Solar'), (1e10, '10^10'), (100, '100')]:
    t_mark = t_classical_linear(S_BH_mark, 1.0, S_T) / t_page
    ax3.plot(S_BH_mark, t_mark, 'ro', ms=8)
    ax3.annotate(label_mark, (S_BH_mark, t_mark), textcoords='offset points',
                 xytext=(5, 5), fontsize=8)
ax3.set_xlabel('S_BH (bits)', fontsize=11)
ax3.set_ylabel('t_classical / t_Page', fontsize=11)
ax3.set_title('How Early is the Classicality Transition?', fontsize=12)
ax3.legend(fontsize=8)
ax3.set_xlim(S_BH_range[0], S_BH_range[-1])

# Panel 4: Interior vs Exterior budget — schematic
ax4 = fig.add_subplot(gs[1, 1])
t = np.linspace(0, 1.0, 10000)
S_BH_panel = 100.0
t_cl_p4 = t_classical_linear(S_BH_panel, 1.0, S_T)

# Exterior budget
R_d_ext = r_delta_linear(t, S_BH_panel, 1.0, S_T)
# Interior budget: 0 before Page time, then jumps
R_d_int = np.where(t < 0.5,
                   -1.0,  # no interior facts accessible
                   r_delta_linear(np.minimum(t, 1.0), S_BH_panel, 1.0, S_T))

ax4.plot(t, R_d_ext, 'b-', lw=2.5, label='R_δ exterior (Hawking radiation)')
ax4.plot(t, R_d_int, 'r-', lw=2.5, label='R_δ interior (behind horizon)')
ax4.axhline(0, color='k', ls='-', lw=0.8)
ax4.axvline(0.5, color='k', ls='--', lw=1.5, label='Page time')
ax4.axvline(t_cl_p4, color='b', ls=':', lw=1.5, label=f't_class_ext={t_cl_p4:.3f}')
ax4.set_xlabel('t / t_evap', fontsize=11)
ax4.set_ylabel('R_δ(t)', fontsize=11)
ax4.set_title('Interior vs Exterior Classicality Budget', fontsize=12)
ax4.legend(fontsize=8)
ax4.set_xlim(0, 1)

plt.savefig('classicality_budget_summary.png', dpi=120, bbox_inches='tight')
plt.close()
print("  Saved: classicality_budget_summary.png")

# ── 3G: Detailed numerical summary ───────────────────────────────────────────

print("\n" + "=" * 70)
print("FINAL NUMERICAL SUMMARY")
print("=" * 70)

print("\n1. t_classical for specific BH masses:")
for S_BH, name in [(1e77, "Solar mass"), (1e10, "Microscopic"), (100, "100-bit"), (10, "10-bit")]:
    t_cl = t_classical_linear(S_BH, 1.0, S_T)
    ratio = t_cl / t_page
    R_max = S_BH / 2.0 / S_T - 1.0
    print(f"  {name:20s}: t_class/t_Page = {ratio:.3e}, R_delta(t_Page) = {R_max:.3e}")

print("\n2. R_delta at the Page time (S_BH/2 - 1):")
for S_BH in [1e77, 1e10, 100, 10]:
    print(f"  S_BH={S_BH:.2e}: R_delta(t_Page) = {S_BH/2 - 1:.3e}")

print("\n3. CFT model Page time ratio:")
for S_BH_cft in [10, 30, 50, 100]:
    tp = page_time_cft(S_BH_cft, c=12)
    te = evap_time_cft(S_BH_cft, c=12)
    print(f"  S_BH={S_BH_cft:5.0f}: t_Page/t_evap = {tp/te:.5f}  (lin: 0.5)")

print("\n4. Key structural result:")
print("   R_delta_interior has a DISCONTINUOUS jump at t_Page:")
print("   R_delta_int(t_Page^-) = -1  (no interior access)")
print("   R_delta_int(t_Page^+) = S_BH/2/S_T - 1  (full island, interior accessible)")
print("\n   R_delta_exterior transitions smoothly through 0 at t_classical << t_Page")
print("\n   => TWO distinct classicality transitions: exterior (early) and interior (at Page time)")

print("\nAll plots saved. Computation complete.")
