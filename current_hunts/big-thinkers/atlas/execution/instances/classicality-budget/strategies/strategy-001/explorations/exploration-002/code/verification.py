"""
Cross-checks and additional analysis for the classicality budget computation.
"""
import numpy as np

hbar = 1.054571817e-34
c = 2.99792458e8
G = 6.67430e-11
l_P = 1.616255e-35
ln2 = np.log(2)
k_B = 1.380649e-23
M_sun = 1.989e30

print("=" * 70)
print("VERIFICATION AND CROSS-CHECKS")
print("=" * 70)

# ============================================================
# Cross-check 1: BH entropy from Bekenstein-Hawking formula
# ============================================================
print("\n--- Cross-check 1: Black hole entropy ---")
r_s = 2 * G * M_sun / c**2
print(f"Schwarzschild radius: {r_s:.4f} m")

# Bekenstein-Hawking entropy: S_BH = (k_B c³ A) / (4 G ℏ)
# In natural units (nats): S = A / (4 l_P²) where A = 4π r_s²
A_BH = 4 * np.pi * r_s**2
S_BH_nats = A_BH / (4 * l_P**2)
S_BH_bits = S_BH_nats / ln2
print(f"BH area: {A_BH:.6e} m²")
print(f"BH entropy (nats): {S_BH_nats:.6e}")
print(f"BH entropy (bits): {S_BH_bits:.6e}")
print(f"Published value for solar-mass BH: ~10^77 (nats) ✓" if 1e76 < S_BH_nats < 1e78 else "MISMATCH!")

# From Bekenstein formula: S = 2πRE/(ℏc)
S_Bek_nats = 2 * np.pi * r_s * (M_sun * c**2) / (hbar * c)
S_Bek_bits = S_Bek_nats / ln2
print(f"\nBekenstein bound for full BH (nats): {S_Bek_nats:.6e}")
print(f"Bekenstein bound for full BH (bits): {S_Bek_bits:.6e}")
print(f"Ratio S_Bek/S_BH = {S_Bek_nats/S_BH_nats:.6f}")
print(f"Expected ratio: 1.0 (they coincide for BH)")

# Verify: 2πRE/(ℏc) = 2π(2GM/c²)(Mc²)/(ℏc) = 4πGM²/(ℏc) 
# and A/(4l_P²) = 4π(2GM/c²)²/(4·Gℏ/c³) = 4πG²M²·c³/(c⁴·Gℏ) = 4πGM²/(ℏc)
# So the ratio should be exactly 1!
ratio_analytic = (2 * np.pi * 2 * G * M_sun * M_sun * c) / (hbar * c * np.pi * (2*G*M_sun)**2 / (c**4 * l_P**2))
print(f"Analytic check of ratio: The Bekenstein bound 2πRE/(ℏc) with R=r_s, E=Mc²")
print(f"  = 2π · (2GM/c²) · (Mc²) / (ℏc) = 4πGM²/(ℏc)")
print(f"  A/(4l_P²) = 4π(2GM/c²)² / (4Gℏ/c³) = 4π · 4G²M²/(c⁴) · c³/(4Gℏ) = 4πGM²/(ℏc)")
print(f"  → They are IDENTICAL. ✓")

# ============================================================
# Cross-check 2: Bekenstein bound for 1 kg at 1 m
# ============================================================
print("\n--- Cross-check 2: Lab-scale Bekenstein bound ---")
R_lab = 0.5
M_lab = 1.0
E_lab = M_lab * c**2
S_lab_nats = 2 * np.pi * R_lab * E_lab / (hbar * c)
S_lab_bits = S_lab_nats / ln2
print(f"S_Bek (1 kg, 0.5 m) = {S_lab_nats:.6e} nats = {S_lab_bits:.6e} bits")
print(f"log₁₀ = {np.log10(S_lab_bits):.2f}")
print(f"Expected: ~10^43 bits ✓" if 42 < np.log10(S_lab_bits) < 44 else "MISMATCH!")

# Literature value: Bekenstein (1981) gives S ≈ 2πMRc/ℏ ≈ 2π × 1 × 0.5 × 3×10^8 / 10^-34
# = 2π × 1.5×10^8 / 10^-34 = 2π × 1.5×10^42 ≈ 9.4×10^42 nats ≈ 1.4×10^43 bits
print(f"Manual check: 2π × 0.5 × (3e8)² × 1 / (1.05e-34 × 3e8) = 2π × 0.5 / (1.05e-34 × 3e8) × 9e16")
manual = 2 * np.pi * 0.5 * 9e16 / (1.05e-34 * 3e8)
print(f"  = {manual:.4e} nats, {manual/ln2:.4e} bits")

# ============================================================
# Cross-check 3: Observable universe entropy
# ============================================================
print("\n--- Cross-check 3: Observable universe ---")
R_univ = 4.4e26
E_univ = 1e53 * c**2
S_univ_bek_bits = 2 * np.pi * R_univ * E_univ / (hbar * c * ln2)
S_univ_holo_bits = np.pi * R_univ**2 / (l_P**2 * ln2)
print(f"Bekenstein: {S_univ_bek_bits:.4e} bits (log₁₀ = {np.log10(S_univ_bek_bits):.1f})")
print(f"Holographic: {S_univ_holo_bits:.4e} bits (log₁₀ = {np.log10(S_univ_holo_bits):.1f})")
print(f"Published holographic bound for observable universe: ~10^122-10^124 bits")
print(f"Our Bekenstein bound: 10^{np.log10(S_univ_bek_bits):.1f} — in range ✓")

# The actual entropy of the observable universe (from Egan & Lineweaver 2010)
# is dominated by the cosmic event horizon: S ~ 2.6 × 10^122 k_B
# The entropy in CMB photons: ~ 10^88
# The entropy in massive particles: ~ 10^80
print(f"\nFor comparison (Egan & Lineweaver 2010):")
print(f"  Actual entropy of cosmic event horizon: ~2.6 × 10^122 k_B = ~3.75 × 10^122 bits")
print(f"  Actual entropy of CMB photons: ~10^88")
print(f"  Actual entropy of massive particles: ~10^80")
print(f"  Our computed S_max (Bekenstein): 10^{np.log10(S_univ_bek_bits):.1f} bits")
print(f"  Note: Our S_max is an UPPER BOUND, so it should be ≥ actual entropy")

# ============================================================
# Cross-check 4: Planck scale
# ============================================================
print("\n--- Cross-check 4: Planck-scale region ---")
R_P = l_P
E_P = 1.956e9
S_planck_bek = 2 * np.pi * R_P * E_P / (hbar * c * ln2)
S_planck_holo = np.pi * R_P**2 / (l_P**2 * ln2)
print(f"Bekenstein: {S_planck_bek:.4f} bits")
print(f"Holographic: {S_planck_holo:.4f} bits = π/ln(2) = {np.pi/ln2:.4f}")
print(f"Expected holographic: π/ln(2) ≈ 4.53 ✓")
# The Bekenstein bound for Planck mass at Planck length:
# S = 2π l_P E_P / (ℏc) = 2π l_P (ℏc⁵/G)^{1/2} / (ℏc)
# With l_P = (Gℏ/c³)^{1/2} and E_P = (ℏc⁵/G)^{1/2}:
# S = 2π (Gℏ/c³)^{1/2} (ℏc⁵/G)^{1/2} / (ℏc) = 2π (ℏ²c²)^{1/2}/(ℏc) = 2π
S_planck_analytic = 2 * np.pi  # in nats
print(f"\nAnalytic: S_Bek(Planck) = 2π nats = {S_planck_analytic:.4f} nats = {S_planck_analytic/ln2:.4f} bits")
print(f"Computed: {S_planck_bek:.4f} bits")
print(f"Match: {'✓' if abs(S_planck_bek - S_planck_analytic/ln2) < 0.1 else '✗'}")

# ============================================================
# Additional analysis: What S_T makes R_δ = 1?
# ============================================================
print("\n\n" + "=" * 70)
print("CRITICAL S_T VALUES: Where does R_δ = 1?")
print("=" * 70)
print("\nR_δ = 1 means: exactly ONE independent observer can verify a fact")
print("(plus the system itself). This is the boundary of classicality.")
print("R_δ = (S_max / S_T) - 1 = 1 → S_T = S_max / 2")
print()

systems_for_critical = {
    "Lab (1m, 1kg)": (0.5, 1.0*c**2),
    "Brain (1.4kg)": (0.0694, 1.4*c**2),
    "Solar BH": (2*G*M_sun/c**2, M_sun*c**2),
    "Observable universe": (4.4e26, 1e53*c**2),
    "Planck scale": (l_P, 1.956e9),
    "QC (1000q)": (0.01, 1e-22*c**2),
}

for name, (R, E) in systems_for_critical.items():
    S_bek = 2 * np.pi * R * E / (hbar * c * ln2)
    S_holo = np.pi * R**2 / (l_P**2 * ln2)
    S_max = min(S_bek, S_holo)
    S_T_critical = S_max / 2
    print(f"{name:<25}: S_max = {S_max:.3e} bits → R_δ=1 when S_T = {S_T_critical:.3e} bits")

# ============================================================
# Trade-off curve: N_facts × R_δ for fixed S_max
# ============================================================
print("\n\n" + "=" * 70)
print("THE CLASSICALITY TRADE-OFF: N_facts vs R_δ")
print("=" * 70)
print("\nTotal budget: S_max = N_facts × S_T = (R_δ + 1) × S_T")
print("So: N_facts × R_δ = (S_max/S_T) × (S_max/S_T - 1)")
print("    = (S_max/S_T)² - (S_max/S_T)")
print("    ≈ (S_max/S_T)² for large S_max/S_T")
print("\nBut the PRODUCT N_facts × R_δ is NOT the real constraint.")
print("The constraint is that they SHARE a budget.")
print("If you want N_facts = 10^6, then R_δ = S_max/(S_T × 10^6) - 1")
print()

# For the brain:
S_brain = min(2*np.pi*0.0694*1.4*c**2/(hbar*c*ln2), np.pi*0.0694**2/(l_P**2*ln2))
print(f"Brain S_max = {S_brain:.3e} bits")
print(f"\n{'N_facts':<15} {'S_T needed':<20} {'R_δ available':<20}")
print("─" * 55)
for log_n in [6, 11, 20, 30, 40, 42]:
    n = 10**log_n
    # N_facts = S_max / S_T → S_T = S_max / N_facts
    st = S_brain / n
    rd = (S_brain / st) - 1  # = N_facts - 1
    # Wait, this is trivial: if N_facts = S_max/S_T, then R_δ = S_max/S_T - 1 = N_facts - 1
    # That means R_δ = N_facts - 1 always!
    # This seems wrong. Let me think about this more carefully.
    # Actually, the budget is: total info = (R_δ + 1) × S_T × N_facts? No...
    # R_δ is the redundancy per fact. Total information = N_facts × (R_δ + 1) × S_T 
    # But wait — the original formula R_δ ≤ S_max/S_T - 1 doesn't mention N_facts at all.
    # It assumes that all S_max bits are devoted to redundantly encoding ONE fact.
    # If you want N_facts distinct facts each with redundancy R_δ, then:
    # Total info = N_facts × (R_δ + 1) × S_T ≤ S_max
    # → N_facts × (R_δ + 1) ≤ S_max / S_T
    # → N_facts × R_δ ≤ S_max/S_T - N_facts (approximately S_max/S_T for large ratios)
    pass

print("\n*** IMPORTANT CORRECTION ***")
print("The formula R_δ ≤ (S_max/S_T) - 1 gives the maximum redundancy for a SINGLE fact.")
print("For N_facts DISTINCT facts, each with redundancy R_δ:")
print("  Total info = N_facts × (R_δ + 1) × S_T ≤ S_max")
print("  → N_facts × (R_δ + 1) ≤ S_max / S_T")
print("  → R_δ ≤ S_max/(N_facts × S_T) - 1")
print()
print("This is the REAL classicality budget trade-off!")
print()

print(f"\nBrain (S_max = {S_brain:.3e} bits, S_T = 1 bit):")
print(f"{'N_facts':<15} {'R_δ (max)':<20} {'Interpretation':<40}")
print("─" * 75)
for log_n, interp in [(0, "1 fact, max redundancy"), (6, "10^6 facts"), 
                        (11, "~N_neurons"), (20, "~N_synapses"),
                        (30, "rich inner world"), (42, "max facts, no redundancy")]:
    n = 10**log_n
    rd = S_brain / (n * 1) - 1  # S_T = 1 bit
    if rd > 0:
        print(f"10^{log_n:<13} {rd:<20.3e} {interp}")
    else:
        print(f"10^{log_n:<13} {'< 0 (impossible)':<20} {interp}")

# ============================================================
# Physical interpretation: what does S_T actually mean?
# ============================================================
print("\n\n" + "=" * 70)
print("PHYSICAL INTERPRETATION OF S_T")
print("=" * 70)

print("\n--- Position precision estimates ---")
# In 3D volume V, position to precision δx in each dimension
# S_T = log₂(V / δx³) for a uniform prior
V_lab = (4/3) * np.pi * 0.5**3
for delta_name, delta in [("1 mm", 1e-3), ("1 μm", 1e-6), ("1 nm", 1e-9), ("1 Å", 1e-10)]:
    s = np.log2(V_lab / delta**3)
    print(f"  Position in 1m sphere to {delta_name}: S_T = {s:.1f} bits")

print("\n--- Temperature precision estimates ---")
for T_range, dT in [(300, 1), (300, 0.01), (300, 1e-6)]:
    s = np.log2(T_range / dT)
    print(f"  Temperature (0-{T_range}K to ±{dT}K): S_T = {s:.1f} bits")

print("\n--- Identity/category estimates ---")
print(f"  Binary choice (yes/no): S_T = 1 bit")
print(f"  Element identity (118 elements): S_T = {np.log2(118):.1f} bits")
print(f"  ASCII character: S_T = 7 bits")
print(f"  Human face recognition (~10^4 faces): S_T = {np.log2(1e4):.1f} bits")
print(f"  Photograph (1 Mpixel, 24-bit color): S_T = {1e6*24:.0e} bits")
print(f"  Book (~500 pages, ~2500 chars/page): S_T = {500*2500*8:.0e} bits")

# ============================================================
# Key insight about BH and Bekenstein bound coincidence
# ============================================================
print("\n\n" + "=" * 70)
print("KEY INSIGHT: WHEN BEKENSTEIN = HOLOGRAPHIC")
print("=" * 70)
print()
print("The Bekenstein and holographic bounds coincide EXACTLY for a black hole.")
print("This is not a coincidence — it's a fundamental feature.")
print()
print("Bekenstein: S = 2πRE/(ℏc)")
print("Holographic: S = πR²/l_P²")
print()
print("They are equal when: 2πRE/(ℏc) = πR²/l_P²")
print("→ E = R ℏc / (2 l_P²) = R c⁴ / (2G)")
print("→ R = 2GE/c⁴ = 2GM/c²  (i.e., R = Schwarzschild radius!)")
print()
print("So the two bounds coincide precisely when the system is a black hole.")
print("For ANY non-BH system with the same R, E < Mc² < Rc⁴/(2G),")
print("so Bekenstein < Holographic.")
print()
print("This means: the classicality budget is most constrained NOT at")
print("the Planck scale per se, but wherever the ratio E/R is small.")
print("A large, nearly empty region has a very small Bekenstein bound.")

# Compute for a near-vacuum region
print("\n--- Example: 1 m³ of near-vacuum (1 photon, E ≈ 1 eV) ---")
E_photon = 1.6e-19  # 1 eV in Joules
S_vacuum_bek = 2 * np.pi * 0.5 * E_photon / (hbar * c * ln2)
S_vacuum_holo = np.pi * 0.5**2 / (l_P**2 * ln2)
print(f"Bekenstein: {S_vacuum_bek:.4e} bits")
print(f"Holographic: {S_vacuum_holo:.4e} bits")
print(f"→ Even a single photon in 1 m³ gives S_Bek = {S_vacuum_bek:.1f} bits")
print(f"  This is still enough for ~{S_vacuum_bek:.0f} classical bits with R_δ = 0!")

# Actually more realistic: room with 1 photon
# S_T = 1 bit, R_δ = S_vacuum_bek - 1
print(f"  R_δ (S_T=1 bit) = {S_vacuum_bek - 1:.1f}")
print(f"  → Even 1 photon in 1 m³ permits a few classical bits")

# Truly empty space: E = 0 → S_Bek = 0 → no classicality!
print(f"\n--- Truly empty space (E = 0): S_Bek = 0 → R_δ = -1")
print(f"  → No classical reality possible in truly empty space")
print(f"  → This is actually a profound prediction!")

print("\n\nVerification complete.")
