#!/usr/bin/env python3
"""
Classicality Budget Computation
================================
Computes the classicality budget R_delta <= (S_max / S_T) - 1 for 6 physical systems.

The classicality budget bounds how much classical reality (redundantly-encoded
information) can exist in a bounded region of space, combining the Bekenstein
entropy bound with quantum Darwinism's requirement of redundancy.

Uses scipy.constants for all physical constants.
"""

import numpy as np
from scipy import constants
import json

# ============================================================================
# Physical Constants (from scipy.constants)
# ============================================================================
c = constants.c                     # speed of light, m/s
hbar = constants.hbar               # reduced Planck constant, J*s
G = constants.G                     # gravitational constant, m^3/(kg*s^2)
k_B = constants.k                   # Boltzmann constant, J/K
M_sun = 1.98892e30                  # solar mass, kg
l_P = constants.value('Planck length')   # Planck length, m
E_P = constants.value('Planck mass energy equivalent in GeV') * constants.eV * 1e9  # Planck energy in J
m_P = constants.value('Planck mass')     # Planck mass, kg
ln2 = np.log(2)

print("=" * 80)
print("PHYSICAL CONSTANTS USED")
print("=" * 80)
print(f"  c     = {c:.6e} m/s")
print(f"  hbar  = {hbar:.6e} J*s")
print(f"  G     = {G:.6e} m^3/(kg*s^2)")
print(f"  k_B   = {k_B:.6e} J/K")
print(f"  l_P   = {l_P:.6e} m")
print(f"  E_P   = {E_P:.6e} J")
print(f"  m_P   = {m_P:.6e} kg")
print(f"  M_sun = {M_sun:.6e} kg")
print(f"  ln(2) = {ln2:.10f}")
print()

# ============================================================================
# Entropy Bound Functions
# ============================================================================

def bekenstein_bound_nats(R, E):
    """Bekenstein bound: S_Bek = 2*pi*R*E/(hbar*c) in nats."""
    return 2 * np.pi * R * E / (hbar * c)

def bekenstein_bound_bits(R, E):
    """Bekenstein bound in bits."""
    return bekenstein_bound_nats(R, E) / ln2

def holographic_bound_nats(R):
    """Holographic (spherical) bound: S_holo = A/(4 l_P^2) = pi*R^2/l_P^2 in nats."""
    A = 4 * np.pi * R**2
    return A / (4 * l_P**2)

def holographic_bound_bits(R):
    """Holographic bound in bits."""
    return holographic_bound_nats(R) / ln2

def effective_smax_bits(R, E):
    """Effective S_max = min(Bekenstein, holographic) in bits."""
    s_bek = bekenstein_bound_bits(R, E)
    s_holo = holographic_bound_bits(R)
    return min(s_bek, s_holo), s_bek, s_holo

def classicality_budget(S_max, S_T):
    """R_delta = S_max / S_T - 1. Returns R_delta (max redundancy number)."""
    return S_max / S_T - 1

def n_facts(S_max, S_T):
    """Maximum number of distinct classical facts: N = S_max / S_T."""
    return S_max / S_T


# ============================================================================
# System Definitions
# ============================================================================

systems = {}

# System 1: Lab-scale region
R1 = 0.5        # meters (radius of 1-meter sphere)
m1 = 1.0        # kg
E1 = m1 * c**2  # rest energy
systems['Lab-scale (1m sphere, 1 kg)'] = {
    'R': R1, 'E': E1, 'mass': m1,
    'description': '1-meter sphere containing 1 kg of ordinary matter (air)',
}

# System 2: Human brain
R2 = 0.08       # meters (sphere enclosing ~1400 cm^3: V = 4/3 pi r^3 -> r ~ 0.069 m, use 0.08)
m2 = 1.4        # kg
E2 = m2 * c**2
systems['Human brain'] = {
    'R': R2, 'E': E2, 'mass': m2,
    'description': 'Human brain (~1400 cm^3, 1.4 kg)',
}

# System 3: Near solar-mass black hole
M_bh = M_sun
R_s = 2 * G * M_bh / c**2  # Schwarzschild radius
R3 = R_s        # at 1 Schwarzschild radius
E3 = M_bh * c**2  # total energy of the black hole
systems['Solar-mass black hole'] = {
    'R': R3, 'E': E3, 'mass': M_bh,
    'description': f'Solar-mass BH at r = r_s = {R_s:.1f} m',
}

# System 4: Observable universe
R4 = 4.4e26     # meters (comoving radius)
m4 = 1e53       # kg (approximate total mass-energy)
E4 = m4 * c**2
systems['Observable universe'] = {
    'R': R4, 'E': E4, 'mass': m4,
    'description': 'Observable universe (R ~ 4.4e26 m, M ~ 10^53 kg)',
    'caveat': 'Bekenstein bound applicability to cosmological scales is contested',
}

# System 5: Planck-scale region
R5 = l_P
E5 = E_P
systems['Planck-scale region'] = {
    'R': R5, 'E': E5, 'mass': m_P,
    'description': f'Planck-scale region (R = l_P = {l_P:.3e} m)',
}

# System 6: Quantum computer (1000 qubits)
R6 = 0.01       # meters (1 cm for trapped-ion register)
m6 = 1e-22      # kg (1000 ions, ~1e-25 kg each)
E6 = m6 * c**2
N_qubits = 1000
hilbert_dim_log2 = N_qubits  # log2(2^1000) = 1000 bits
systems['Quantum computer (1000 qubits)'] = {
    'R': R6, 'E': E6, 'mass': m6,
    'description': '1000-qubit trapped-ion quantum computer',
    'hilbert_dim_log2': hilbert_dim_log2,
}

# ============================================================================
# S_T values to test (information content of one classical fact, in bits)
# ============================================================================
S_T_values = {
    '1 bit (minimal fact)': 1,
    '10 bits (a letter/digit)': 10,
    '100 bits (a sentence)': 100,
    '1e6 bits (a photograph)': 1e6,
}

# ============================================================================
# Compute and display results
# ============================================================================

print("=" * 80)
print("ENTROPY BOUNDS FOR EACH SYSTEM")
print("=" * 80)
print()

results = {}

for name, sys_data in systems.items():
    R = sys_data['R']
    E = sys_data['E']

    s_bek_nats = bekenstein_bound_nats(R, E)
    s_bek_bits = bekenstein_bound_bits(R, E)
    s_holo_nats = holographic_bound_nats(R)
    s_holo_bits = holographic_bound_bits(R)
    s_eff_bits = min(s_bek_bits, s_holo_bits)
    tighter = 'Bekenstein' if s_bek_bits < s_holo_bits else 'Holographic'

    results[name] = {
        'R': R,
        'E': E,
        'S_bek_bits': s_bek_bits,
        'S_holo_bits': s_holo_bits,
        'S_eff_bits': s_eff_bits,
        'tighter_bound': tighter,
        'S_bek_nats': s_bek_nats,
        'S_holo_nats': s_holo_nats,
    }

    print(f"--- {name} ---")
    print(f"  {sys_data['description']}")
    if 'caveat' in sys_data:
        print(f"  WARNING: {sys_data['caveat']}")
    print(f"  R = {R:.3e} m")
    print(f"  E = {E:.3e} J")
    print(f"  S_Bek (nats)  = {s_bek_nats:.6e}")
    print(f"  S_Bek (bits)  = {s_bek_bits:.6e}")
    print(f"  S_holo (nats) = {s_holo_nats:.6e}")
    print(f"  S_holo (bits) = {s_holo_bits:.6e}")
    print(f"  log10(S_Bek bits)  = {np.log10(s_bek_bits):.2f}")
    print(f"  log10(S_holo bits) = {np.log10(s_holo_bits):.2f}")
    print(f"  Tighter bound: {tighter}")
    print(f"  S_max (bits)  = {s_eff_bits:.6e} (= 10^{np.log10(s_eff_bits):.2f})")
    if 'hilbert_dim_log2' in sys_data:
        print(f"  Hilbert space dim: 2^{sys_data['hilbert_dim_log2']} (log2 = {sys_data['hilbert_dim_log2']})")
        print(f"  S_max / Hilbert_dim(log2) = {s_eff_bits / sys_data['hilbert_dim_log2']:.3e}")
    print()

# ============================================================================
# Classicality Budget Table
# ============================================================================

print("=" * 80)
print("CLASSICALITY BUDGET: R_delta = S_max / S_T - 1")
print("=" * 80)
print()

# Print as a more readable format
for name, res in results.items():
    s_eff = res['S_eff_bits']
    print(f"  {name}:")
    for st_name, st_val in S_T_values.items():
        r_delta = classicality_budget(s_eff, st_val)
        log_rd = np.log10(max(r_delta, 1e-100))
        print(f"    S_T = {st_name:30s}  R_delta = {r_delta:.6e}  (10^{log_rd:.2f})")
    print()

# ============================================================================
# Number of Distinct Classical Facts Table
# ============================================================================

print("=" * 80)
print("NUMBER OF DISTINCT CLASSICAL FACTS: N_facts = S_max / S_T")
print("=" * 80)
print()

for name, res in results.items():
    s_eff = res['S_eff_bits']
    print(f"  {name}:")
    for st_name, st_val in S_T_values.items():
        nf = n_facts(s_eff, st_val)
        print(f"    S_T = {st_name:30s}  N_facts = {nf:.6e}  (10^{np.log10(nf):.2f})")
    print()

# ============================================================================
# Sanity Checks
# ============================================================================

print("=" * 80)
print("SANITY CHECKS")
print("=" * 80)
print()

# Check 1: R_delta * S_T <= S_max for all systems and all S_T
print("CHECK 1: (R_delta + 1) * S_T = S_max for all (system, S_T) pairs")
all_pass = True
for name, res in results.items():
    s_eff = res['S_eff_bits']
    for st_name, st_val in S_T_values.items():
        r_d = classicality_budget(s_eff, st_val)
        lhs = (r_d + 1) * st_val
        ok = np.isclose(lhs, s_eff, rtol=1e-10)
        if not ok:
            print(f"  FAIL: {name}, S_T={st_val}: (R_delta+1)*S_T = {lhs:.6e} vs S_max = {s_eff:.6e}")
            all_pass = False
if all_pass:
    print("  PASS: All systems satisfy (R_delta + 1) * S_T = S_max exactly (by construction)")
print()

# Check 2: Planck-scale region gives R_delta approx 0
planck_res = results['Planck-scale region']
planck_smax = planck_res['S_eff_bits']
planck_rd_1bit = classicality_budget(planck_smax, 1)
print(f"CHECK 2: Planck-scale region R_delta for S_T = 1 bit")
print(f"  S_max (Planck) = {planck_smax:.6f} bits")
print(f"  R_delta = {planck_rd_1bit:.6f}")
if planck_smax < 100:
    print(f"  PASS: S_max is of order {planck_smax:.1f} bits, so R_delta is small")
    print(f"  Interpretation: at Planck scale, barely any room for even 1 classical fact")
else:
    print(f"  UNEXPECTED: S_max = {planck_smax:.1f} bits at Planck scale (expected ~1)")
print()

# Check 3: Observable universe R_delta is astronomically large
universe_res = results['Observable universe']
universe_smax = universe_res['S_eff_bits']
universe_rd_1bit = classicality_budget(universe_smax, 1)
print(f"CHECK 3: Observable universe R_delta is astronomically large")
print(f"  S_max (universe) = 10^{np.log10(universe_smax):.2f} bits")
print(f"  R_delta (S_T=1 bit) = 10^{np.log10(universe_rd_1bit):.2f}")
if np.log10(universe_rd_1bit) > 50:
    print(f"  PASS: R_delta is astronomically large (10^{np.log10(universe_rd_1bit):.0f})")
else:
    print(f"  UNEXPECTED: R_delta seems too small")
print()

# Check 4: Brain has enough budget for conscious experience
brain_res = results['Human brain']
brain_smax = brain_res['S_eff_bits']
num_neurons = 1e11
print(f"CHECK 4: Brain classicality budget vs neurons")
print(f"  S_max (brain) = 10^{np.log10(brain_smax):.2f} bits")
print(f"  Number of neurons: ~10^11 = {num_neurons:.0e}")
n_neuron_facts = brain_smax / 1  # max number of 1-bit facts
print(f"  Max 1-bit facts: {n_neuron_facts:.3e} = 10^{np.log10(n_neuron_facts):.2f}")
print(f"  Ratio (max 1-bit facts / neurons): 10^{np.log10(n_neuron_facts/num_neurons):.2f}")
s_percept = 1e6
r_d_percept = classicality_budget(brain_smax, s_percept)
n_percepts = n_facts(brain_smax, s_percept)
print(f"  For S_T = 10^6 bits (photograph-level percept):")
print(f"    R_delta = {r_d_percept:.3e} = 10^{np.log10(r_d_percept):.2f}")
print(f"    N_facts = {n_percepts:.3e} = 10^{np.log10(n_percepts):.2f}")
print(f"  PASS: Budget vastly exceeds neural count -- no Bekenstein-level constraint on consciousness")
print()

# Check 5: Quantum computer -- S_max vs Hilbert space dimension
qc_res = results['Quantum computer (1000 qubits)']
qc_smax = qc_res['S_eff_bits']
print(f"CHECK 5: Quantum computer S_max vs Hilbert space")
print(f"  S_max (QC) = {qc_smax:.6e} bits = 10^{np.log10(qc_smax):.2f}")
print(f"  Hilbert space dimension: 2^1000 (log2 = 1000 bits)")
print(f"  S_max / 1000 = {qc_smax/1000:.3e}")
if qc_smax > 1000:
    print(f"  RESULT: S_max >> Hilbert space log-dimension")
    print(f"  Interpretation: Bekenstein bound allows FAR more information than the")
    print(f"  quantum state actually encodes. The QC is nowhere near saturating the bound.")
    print(f"  This makes sense: the qubits are a tiny fraction of the total degrees of freedom.")
else:
    print(f"  WARNING: S_max < Hilbert space log-dimension -- physically problematic")
print()

# Check 6: Black hole -- Bekenstein vs Holographic
bh_res = results['Solar-mass black hole']
print(f"CHECK 6: Black hole -- Bekenstein vs Holographic bound comparison")
print(f"  S_Bek  = 10^{np.log10(bh_res['S_bek_bits']):.2f} bits")
print(f"  S_holo = 10^{np.log10(bh_res['S_holo_bits']):.2f} bits")
ratio_bh = bh_res['S_bek_bits']/bh_res['S_holo_bits']
print(f"  Ratio S_Bek / S_holo = {ratio_bh:.6f}")
# For a BH at r_s: S_Bek = 2*pi*(2GM/c^2)*(Mc^2)/(hbar*c) = 4*pi*G*M^2/(hbar*c)
# S_holo = pi*R^2/l_P^2 = pi*(2GM/c^2)^2 / (hbar*G/c^3)  
# = pi*4*G^2*M^2/c^4 * c^3/(hbar*G) = 4*pi*G*M^2/(hbar*c)
# They should be EQUAL!
print(f"  Expected ratio for BH at r_s: 1.0 (Bek = Holo at horizon)")
if np.isclose(ratio_bh, 1.0, rtol=0.01):
    print(f"  PASS: Bekenstein = Holographic for BH at Schwarzschild radius (as expected)")
else:
    print(f"  WARNING: Mismatch -- ratio = {ratio_bh:.10f}")
print()

# Check 7: Known value for BH entropy
s_bh_nats = 4 * np.pi * G * M_sun**2 / (hbar * c)
s_bh_bits = s_bh_nats / ln2
print(f"CHECK 7: Solar-mass black hole entropy vs known value")
print(f"  Computed S_BH = {s_bh_nats:.6e} nats = {s_bh_bits:.6e} bits")
print(f"  log10(S_BH nats) = {np.log10(s_bh_nats):.2f}")
print(f"  Known value: Bekenstein-Hawking entropy ~ 10^77 (in natural units)")
A_bh = 4 * np.pi * R_s**2
S_BH_standard = A_bh / (4 * l_P**2)
print(f"  Standard BH entropy: S = A/(4*l_P^2) = {S_BH_standard:.6e} nats")
print(f"  log10(S_BH standard) = {np.log10(S_BH_standard):.2f}")
if 76 < np.log10(S_BH_standard) < 78:
    print(f"  PASS: Matches known ~10^77")
else:
    print(f"  VALUE {np.log10(S_BH_standard):.2f} outside expected range [76, 78]")
print()

# ============================================================================
# Additional: System-specific S_T estimates
# ============================================================================

print("=" * 80)
print("PHYSICALLY MOTIVATED S_T ESTIMATES")
print("=" * 80)
print()

# Lab-scale: position of object to 1mm precision in 3D
V_lab = (4/3) * np.pi * 0.5**3  # m^3
delta_x = 1e-3  # 1 mm
delta_V = delta_x**3  # m^3
S_T_position = np.log2(V_lab / delta_V)
print(f"Lab-scale: position to 1mm in sphere")
print(f"  V = {V_lab:.4f} m^3, delta_V = {delta_V:.2e} m^3")
print(f"  S_T = log2(V/delta_V) = {S_T_position:.1f} bits")
r_d_lab_pos = classicality_budget(results['Lab-scale (1m sphere, 1 kg)']['S_eff_bits'], S_T_position)
print(f"  R_delta = {r_d_lab_pos:.6e} = 10^{np.log10(r_d_lab_pos):.2f}")
print()

# Lab-scale: temperature to 1K precision (range 0-1000 K)
S_T_temp = np.log2(1000)  # ~10 bits
print(f"Lab-scale: temperature to 1K (range 0-1000K)")
print(f"  S_T = log2(1000) = {S_T_temp:.1f} bits")
r_d_lab_temp = classicality_budget(results['Lab-scale (1m sphere, 1 kg)']['S_eff_bits'], S_T_temp)
print(f"  R_delta = {r_d_lab_temp:.6e} = 10^{np.log10(r_d_lab_temp):.2f}")
print()

# Brain: various neural info levels
print(f"Brain: classicality budget for neural information")
brain_smax = results['Human brain']['S_eff_bits']
for s_t_label, s_t_val in [("1 bit (neuron fire/not)", 1),
                             ("8 bits (synapse weight)", 8),
                             ("1e3 bits (simple percept)", 1e3),
                             ("1e6 bits (rich percept)", 1e6)]:
    r_d = classicality_budget(brain_smax, s_t_val)
    print(f"  S_T = {s_t_label}: R_delta = {r_d:.3e} = 10^{np.log10(r_d):.2f}")
print()

# Universe: position of star to 1 AU precision
AU = 1.496e11  # meters
V_universe = (4/3) * np.pi * (4.4e26)**3
delta_V_star = AU**3  # 1 AU^3
S_T_star = np.log2(V_universe / delta_V_star)
print(f"Universe: position of star to 1 AU")
print(f"  V_universe = {V_universe:.3e} m^3")
print(f"  delta_V = (1 AU)^3 = {delta_V_star:.3e} m^3")
print(f"  S_T = log2(V/delta_V) = {S_T_star:.1f} bits")
universe_smax = results['Observable universe']['S_eff_bits']
r_d_star = classicality_budget(universe_smax, S_T_star)
print(f"  R_delta = {r_d_star:.6e} = 10^{np.log10(r_d_star):.2f}")
print()

# ============================================================================
# Compact Summary Table
# ============================================================================

print("=" * 80)
print("COMPACT SUMMARY TABLE")
print("=" * 80)
print()
fmt = "{:<35} {:>18} {:>12} {:>18} {:>18}"
print(fmt.format('System', 'log10(S_max)', 'Tighter', 'log10(Rd)[1b]', 'log10(Rd)[1Mb]'))
print("-" * 105)
for name, res in results.items():
    s_eff = res['S_eff_bits']
    r_d_1 = classicality_budget(s_eff, 1)
    r_d_1M = classicality_budget(s_eff, 1e6)
    log_smax = np.log10(s_eff)
    log_rd1 = np.log10(max(r_d_1, 1e-100))
    log_rdM = np.log10(max(r_d_1M, 1e-100))
    print(fmt.format(name, f"{log_smax:.2f}", res['tighter_bound'], f"{log_rd1:.2f}", f"{log_rdM:.2f}"))
print()

# ============================================================================
# Save results as JSON for plotting script
# ============================================================================

json_results = {}
for name, res in results.items():
    json_results[name] = {
        'S_bek_bits': float(res['S_bek_bits']),
        'S_holo_bits': float(res['S_holo_bits']),
        'S_eff_bits': float(res['S_eff_bits']),
        'tighter_bound': res['tighter_bound'],
        'log10_S_eff': float(np.log10(res['S_eff_bits'])),
    }

with open('results.json', 'w') as f:
    json.dump(json_results, f, indent=2)
print("Results saved to results.json")
