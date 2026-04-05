# Computations for Later

## 1. Fully Resolved Re=1000 Simulation (N=256 or N=512)
- **What:** Run Taylor-Green vortex at Re=1000 with N=256 (and ideally N=512) to get fully resolved turbulent DNS
- **Why:** N=128 at Re=1000 is likely still underresolved (η ≈ 0.006 vs grid scale 0.15). Accurate β measurement requires fully resolved pressure fields
- **Source:** Task 001
- **Difficulty:** Medium (computational cost: ~100× N=64. Might need hours of wall time.)
- **Inputs:** Existing ns_solver.py with scipy.fft optimization

## 2. Direct Vasseur Exponent β Measurement
- **What:** Compute ∫p |u|^q dx as function of q, measure scaling relationship to extract effective β
- **Why:** This is THE key measurement of the entire mission — determines the mission's branching
- **Source:** Task 001 leads
- **Difficulty:** Medium-High (requires understanding Vasseur's De Giorgi iteration levels and computing super-level set integrals)
- **Inputs:** Working solver with pressure output, De Giorgi iteration theory (Vasseur 2007)

## 3. Pressure Field Verification Against Analytic TGV Solution
- **What:** At t=0, the TGV pressure is analytically known: p = -(cos 2x + cos 2y + cos 2z)/16. Verify solver matches.
- **Why:** Confirms the Poisson solver is correct to machine precision
- **Source:** Task 001 deferred
- **Difficulty:** Easy
- **Inputs:** ns_solver.py compute_pressure()
