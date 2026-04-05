# Exploration 008 — Adversarial Stress Test of the T_U/T_dS Modified Inertia Approach

## Mission Context

We have developed the following framework over 6 previous explorations:

**THE MODEL**: Inertial mass is modified as m_i = m × μ(g_N/a₀) where:
- μ(x) = x/√(1+x²) is the STANDARD MOND interpolation function
- g_N is the Newtonian gravitational acceleration
- a₀ ≈ cH₀/6 ≈ 1.1×10⁻¹⁰ m/s² (with Verlinde's correction factor)
- The formula arises from the ratio T_U(a)/T_dS(a) of Unruh to de Sitter temperatures

**WHAT WORKS**: Exact standard MOND interpolation function shape. Galaxy rotation curves (NGC 3198, NGC 2403) with χ²/dof ~ 0.5-1.3. Baryonic Tully-Fisher relation. Solar system consistency (deviation < 10⁻¹⁴ at Earth orbit).

**KNOWN WEAKNESSES**:
1. No first-principles derivation of m_i = m × T_U/T_dS (FDT route closed)
2. Free-fall objection (unresolved — being investigated in parallel exploration 007)
3. The factor of 1/6 is imported from Verlinde, not derived internally

## Your Task

This is an **adversarial analysis** task. Your job is to ATTACK this model — find its weaknesses, test it against the hardest observations, and determine what would falsify it. You are working on the COMPTON-UNRUH MISSION. Write ALL output to explorations/exploration-008/.

### Part 1: The Hardest Observational Tests

Test the model against observations that have killed or severely constrained other modified gravity/inertia proposals:

1. **Bullet Cluster (1E 0657-558)**
   - The Bullet Cluster shows gravitational lensing centered on the dark matter distribution, not the baryonic gas.
   - In a modified-inertia framework, there IS no dark matter. How does the model explain gravitational lensing being offset from the visible baryonic gas?
   - Key question: Does modified INERTIA (not modified gravity) affect gravitational lensing? Photons are massless — do they experience the modified dynamics?
   - If not (photons follow standard GR geodesics), lensing should trace the TOTAL mass including any missing mass. What IS the missing mass in this model?

2. **CMB Third Acoustic Peak**
   - The CMB power spectrum, particularly the ratio of the first to third peaks, is sensitive to the matter content of the universe.
   - Standard ΛCDM explains all peaks with ~27% dark matter.
   - Can modified inertia at a ~ a₀ affect the acoustic oscillations at recombination? (a₀ corresponds to spatial scales of ~100 Mpc — much larger than the sound horizon.)
   - Does the modification even apply at z ~ 1100? (H was much larger then, so a₀ was much larger too.)

3. **Gravitational Lensing Without Dark Matter**
   - Strong and weak gravitational lensing measurements consistently require more mass than the visible baryonic component.
   - In the T_U/T_dS framework, is lensing modified? If inertial mass ≠ gravitational mass (m_i ≠ m_g), does the gravitational mass (which determines lensing) remain unmodified?
   - If so, how does the model explain the observed lensing-mass discrepancy?

4. **Galaxy Cluster Dynamics**
   - MOND famously fails at cluster scales — it reduces the dark matter requirement but doesn't eliminate it (still needs ~2× more mass than baryons in clusters).
   - Does the T_U/T_dS model inherit this MOND failure?
   - Specific test: Coma cluster mass discrepancy.

5. **External Field Effect (EFE)**
   - MOND predicts that the internal dynamics of a system are affected by the external gravitational field it's embedded in (violating the strong equivalence principle).
   - Does the T_U/T_dS model predict an EFE? (Answer: probably yes, since μ depends on the total g_N.)
   - Is the predicted EFE consistent with observations? (Dwarf galaxies in clusters, wide binaries near galactic plane.)

6. **Solar System Precision Tests**
   - At a = g_sun(Earth) ~ 6×10⁻³ m/s², the model gives μ ≈ 1 − 10⁻¹⁴. This is tiny.
   - But the MOND EFE from the Milky Way at the Sun's position (g_MW ~ 2×10⁻¹⁰ m/s² ~ a₀) may be more relevant.
   - What does the model predict for: perihelion precession of outer planets, Pioneer anomaly bounds, lunar laser ranging residuals?

### Part 2: Theoretical Consistency

1. **Equivalence Principle Violation**
   - If m_i ≠ m_g, the weak equivalence principle is violated. Quantify: by how much at different acceleration scales? Is this ruled out by Eötvös experiments?
   - Key distinction: if ALL particles have the same m_i/m_g ratio (depending only on local g_N), the universality of free fall is preserved even though m_i ≠ m_g. Is this the case?

2. **Conservation Laws**
   - If inertial mass depends on acceleration, is momentum conserved? Is energy conserved?
   - In MOND, the modified Poisson equation ensures conservation. What ensures it in modified inertia?

3. **Causality and Stability**
   - Variable inertial mass can lead to pathological behavior. Are there negative-energy modes? Superluminal propagation? Ghost instabilities?
   - What does the modified dispersion relation look like?

4. **Cosmological Consistency**
   - If a₀ = cH₀/6, then a₀ evolves with cosmic time (as H changes). Does this create problems for structure formation, BBN, or recombination-era physics?
   - At z ~ 1100, H ~ 10⁶ H₀, so a₀(z=1100) ~ 10⁶ × a₀(today) ~ 10⁻⁴ m/s². This means almost ALL accelerations in the early universe were below a₀. What does the model predict for the early universe?

### Part 3: What Would Falsify It?

1. Identify the single most decisive test that would falsify the T_U/T_dS model.
2. Identify a test that would CONFIRM it (distinguish it from ΛCDM + dark matter).
3. Rate the model on a scale of 1-10 for theoretical viability and observational viability.

## Success Criteria
- At least 4 of the 6 observational tests evaluated with specific arguments
- At least 2 of the 4 theoretical consistency checks addressed
- A clear falsification test identified
- Honest overall viability assessment

## Deliverables
Write to:
- `explorations/exploration-008/REPORT.md` — full report (300-500 lines)
- `explorations/exploration-008/REPORT-SUMMARY.md` — concise summary (30-50 lines, WRITE THIS LAST)
