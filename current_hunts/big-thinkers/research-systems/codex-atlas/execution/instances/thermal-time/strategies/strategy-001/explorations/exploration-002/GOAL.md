# Exploration 002 — Normalization Resolution + Entangled-State Modular Hamiltonian

## Mission Context

You are working on a mission to derive a measurable prediction from the **Connes-Rovelli thermal time hypothesis (TTH)**. The mission asks: does TTH predict physical behavior at the interface of two entangled subsystems that differs from standard quantum thermodynamics?

This is **Exploration 002, Phase 1 (Foundation)**. Exploration 001 established the modular Hamiltonian toolkit for product states and found a candidate discriminating observable. Your job is to (A) resolve the normalization ambiguity that blocks interpreting that observable, and (B) compute the key quantity that exploration-001 identified but didn't compute: the modular Hamiltonian K_A for the ENTANGLED (globally coupled) thermal state.

---

## What Exploration 001 Found

Exploration-001 computed the position autocorrelation C(t) = ⟨x_A(t)x_A(0)⟩ for two oscillators in a **product state** ρ_{AB} = ρ_A(β_A) ⊗ ρ_B(β_B):

- **TTH prediction** (modular flow σ_t(x_A) = e^{iK_{AB}t} x_A e^{-iK_{AB}t} with K_{AB} = β_A H_A + β_B H_B): oscillation at **β_A ω_A**
- **Standard QM prediction** (Heisenberg under H_A): oscillation at **ω_A**
- **Difference:** factor of β_A (numerically verified, β_A = 2.0 → TTH oscillates twice as fast as QM)

The central unresolved question: **Is the β_A factor a genuine TTH prediction, or does TTH include a normalization τ = β·t that removes it?**

This normalization question is blocking. Until it's resolved, we cannot interpret whether future computations show TTH agreeing or disagreeing with standard QM.

---

## Your Goal

### Part A — Resolve the Normalization Ambiguity (Literature)

Read the original TTH papers and extract the EXACT statement about how modular time relates to physical time.

**The specific question:** When Connes & Rovelli say "physical time IS the modular flow," do they mean:
1. τ_physical = t_modular directly (no rescaling), OR
2. τ_physical = β · t_modular (time rate proportional to temperature), OR
3. Something else?

**Key constraint from Rindler/Bisognano-Wichmann:** For the Rindler wedge:
- K_BW = 2π · (boost generator) = 2π K_boost
- Rindler time η corresponds to boost rapidity
- The Unruh temperature is T_U = a/(2π) in natural units → β_U = 2π/a
- Modular flow parameter t and Rindler time η are related by: η = 2πt → physical proper time τ = η/a = (2π/a)t = β_U · t
- **Implication:** For Rindler, physical time = β_U × modular time (normalization (2) above)

Verify this interpretation by consulting:
1. **Connes & Rovelli (1994)** — "Von Neumann Algebra Automorphisms and Time-Thermodynamics Relation in Generally Covariant Quantum Theories," *Class. Quant. Grav.* 11, 2899. Look specifically for: how they define physical time from the modular parameter, and whether they include a β factor.
2. **Martinetti & Rovelli (2003)** — "Diamond's temperature: Unruh effect for bounded trajectories and the thermal time hypothesis," *Class. Quant. Grav.* 20, 4919. arXiv:gr-qc/0212074. This paper computes TTH predictions for different accelerated trajectories. If TTH = QM for these trajectories, the normalization must agree.
3. **Haggard & Rovelli (2013)** — "Death and resurrection of the zeroth principle of thermodynamics," arXiv:1302.0724. This derives the Tolman-Ehrenfest effect from TTH. **Key:** the T-E effect says clocks at higher temperature run faster (different rates at different heights in gravitational field). TTH predicts rate ∝ temperature. Does this imply time rate = T × (modular time rate), i.e., τ = T · t = t/β?

**The Tolman-Ehrenfest test:**
Tolman-Ehrenfest (classical GR): at heights z₁ and z₂ in gravitational field, T₁ √g₁₁ = T₂ √g₂₂ (temperatures scale inversely with gravitational redshift). For weak field at height z: T(z) = T₀ / (1 + gz/c²) ≈ T₀(1 - gz/c²). Clocks at height z run at rate (1 + gz/c²) relative to ground (gravitational time dilation).

TTH derivation: a system at temperature T has modular flow rate proportional to T. If physical time = β · t_modular = t/T, then a hotter system's clock runs faster (t = Tτ → for same τ, higher T gives larger t). This IS the Tolman-Ehrenfest effect: hotter = runs faster = higher gravitational potential.

Extract the exact normalization from these papers. If the Rindler/T-E analysis pins down the normalization uniquely, state which option (1), (2), or (3) is correct and cite the exact passage.

**Deliverable for Part A:** A clear statement of the normalization convention, with citation and argument for why it's unambiguous (or an honest account of remaining ambiguity if it persists).

---

### Part B — The Entangled-State Modular Hamiltonian (Computation)

This is the most important computation in this exploration. Exploration-001 computed K_A for a **product state** and got K_A = β_A H_A (trivial result). Now compute K_A for the **coupled thermal state** — the state where A and B are entangled by their interaction.

**Setup:**
- Two harmonic oscillators: H_A = ω_A a†a, H_B = ω_B b†b
- Bilinear coupling: H_int = λ q_A q_B where q_A = (a + a†)/√2, q_B = (b + b†)/√2
- GLOBAL Hamiltonian: H_AB = H_A + H_B + H_int
- GLOBAL thermal state at single inverse temperature β: ρ_{AB} = e^{-β H_AB} / Z
- Subsystem A's reduced state: ρ_A = Tr_B[ρ_{AB}]

**What to compute:**

1. **ρ_A explicitly** (Python, truncated Fock space):
   - Construct H_AB as an (N×N)⊗(N×N) matrix in truncated Fock space (N=20 per mode)
   - Compute ρ_{AB} = expm(-β H_AB) / trace
   - Compute ρ_A = partial_trace(ρ_{AB}, system B)
   - Verify: ρ_A > 0, Tr[ρ_A] = 1

2. **K_A = -log ρ_A** (via matrix logarithm):
   - Compute K_A = -logm(ρ_A)
   - Compare K_A to β H_A numerically
   - Compute the DIFFERENCE: ΔK_A = K_A - β H_A - (constant×I) [subtract the scalar offset to isolate non-trivial content]
   - Report: ||ΔK_A||_F (Frobenius norm), eigenvalue spectrum of ΔK_A, and whether ΔK_A is proportional to some simple operator or is genuinely non-local

3. **Parameter sweep:**
   - Fix β = 2.0, ω_A = ω_B = 1.0
   - Vary λ from 0 to 0.5 in steps of 0.05
   - For each λ: compute ||ΔK_A(λ)||_F
   - Does ||ΔK_A|| grow as λ² (perturbative) or faster?
   - Plot: ||ΔK_A|| vs λ

4. **Modular flow comparison:**
   - For λ = 0.3 and β = 2.0: compute σ_t^{ρ_A}(q_A) = e^{iK_A t} q_A e^{-iK_A t} for t ∈ [0, π]
   - Also compute the standard QM Heisenberg evolution: U_t q_A U_t† = e^{iH_A t} q_A e^{-iH_A t}
   - Also compute the TTH with CORRECTED normalization (if Part A resolves the β factor): σ_τ = σ_{τ/β}
   - Plot all three trajectories for q_A

5. **The entanglement correction formula:**
   - For small λ, use perturbation theory to derive an analytic formula for ΔK_A(λ)
   - First-order perturbation theory for the modular Hamiltonian: ΔK_A ≈ λ · [something involving H_int, K_A^{(0)}, and the thermal 2-point functions]
   - Reference: Araki's perturbation theory of KMS states (Araki 1973, Commun. Math. Phys. 32, 245), or more accessible: "First law of entanglement entropy" papers (Blanco et al. 2013, arXiv:1301.7081)
   - Even if you can't derive it fully, compute it numerically and check if it scales as expected

**Key question for Part B:** For the globally coupled thermal state (λ ≠ 0), is ΔK_A ≠ 0? If yes, then the modular flow for A (TTH's predicted time evolution) differs from Heisenberg evolution under H_A (standard QM). This is the genuine novel TTH prediction. Characterize the magnitude and structure of ΔK_A.

**Python computation template:**
```python
import numpy as np
from scipy.linalg import expm, logm
from numpy.linalg import norm

# Parameters
N = 20  # Fock space truncation per mode
hbar = 1.0
omega_A, omega_B = 1.0, 1.0
beta = 2.0
lambda_vals = np.arange(0, 0.55, 0.05)

# Fock space operators for single mode (N×N matrices)
n_op = np.diag(np.arange(N))  # number operator
a_op = np.diag(np.sqrt(np.arange(1, N)), 1)  # lowering
ad_op = a_op.T  # raising
q_op = (a_op + ad_op) / np.sqrt(2)  # position

# Two-mode operators (tensor products)
I_N = np.eye(N)
# H_A = omega_A (a†a ⊗ I)
H_A = np.kron(omega_A * n_op, I_N)
# H_B = omega_B (I ⊗ b†b)
H_B = np.kron(I_N, omega_B * n_op)
# H_int = lambda * q_A ⊗ q_B
q_A = np.kron(q_op, I_N)
q_B = np.kron(I_N, q_op)

for lam in lambda_vals:
    H_AB = H_A + H_B + lam * q_A @ q_B  # wait, q_A * q_B as operator product
    # Actually H_int = lambda * (q_A tensor q_B), meaning lambda * kron(q_op, q_op)
    H_int = lam * np.kron(q_op, q_op)
    H_AB = H_A + H_B + H_int

    # Global thermal state
    rho_AB = expm(-beta * H_AB)
    Z = np.trace(rho_AB)
    rho_AB /= Z

    # Partial trace over B to get rho_A
    rho_A = partial_trace(rho_AB, N, N, system=0)  # implement this

    # Modular Hamiltonian
    K_A = -logm(rho_A)

    # Comparison with beta * H_A_reduced
    H_A_red = omega_A * n_op  # H_A in the A subspace
    delta_K = K_A - beta * H_A_red - np.trace(K_A - beta * H_A_red) / N * np.eye(N)
    print(f"lambda={lam:.2f}, ||delta_K||_F = {norm(delta_K, 'fro'):.4f}")
```

Implement the partial trace function carefully: ρ_A_{ij} = Σ_k ρ_{AB}_{(i*N+k, j*N+k)} for A being the first mode.

---

### Part C — Does ΔK_A = 0 at First Order? (Optional But Important)

There's a theorem lurking here: for a product state ρ_A ⊗ ρ_B, K_A = β H_A trivially. For the coupled state e^{-β H_AB}/Z with H_AB = H_A + H_B + λ H_int, what is K_A to first order in λ?

Using Araki's perturbation theory or the "first law of entanglement entropy":
ΔK_A = -Tr_B[δρ_{AB} · log ρ_A^{(0)} ⊗ ρ_B^{(0)}] - Tr_B[ρ_{AB}^{(0)} · Δlog_A]

where the first term involves the first-order change in the global state. Compute whether this is zero or non-zero. If it's non-zero at O(λ), TTH's correction is first-order in coupling. If it's zero at O(λ), the correction starts at O(λ²).

---

## Rigor Requirements

- **Normalization resolution:** Give the exact passage from Connes-Rovelli or Haggard-Rovelli that pins down the normalization. Do not infer from context — find the explicit statement.
- **ΔK_A computation:** Report both the Frobenius norm and the eigenvalue spectrum. Verify that ρ_A has all eigenvalues positive and sums to 1 before computing K_A. Verify the matrix log is well-defined (no zero eigenvalues).
- **Perturbative order:** State explicitly whether ΔK_A is O(λ), O(λ²), or higher order based on your numerical results.

---

## Prior Findings From Exploration 001 (Pre-Loaded Context)

**From exploration-001 code (verified numerically):**
- β_A = 2.0, ω_A = ω_B = 1.0, λ = 0.1 (weak coupling, product state)
- K_A = β_A · diag(0, 1, 2, ..., N-1) + log(Z_A)·I (verified to machine precision)
- ⟨n̄_A⟩ = 0.1565, ⟨x_A²⟩ = 0.6565
- C_TTH(t) = 0.6565·cos(2t), C_QM(t) = 0.6565·cos(t)·e^{-0.020t}
- Lindblad decay rate Γ = 0.041, timescale τ_D = 24.5

**From exploration-001 literature survey:**
- Bisognano-Wichmann: K = 2π K_boost (modular = 2π × boost generator)
- KMS condition: ω(σ_{t+iβ}(A)B) = ω(BA) satisfied by modular flow of thermal state
- CFT interval: K = 2π ∫₀ᴸ [(L-x)x/L] T₀₀ dx (non-local, Casini-Huerta)
- Modular flow of CFT interval = Möbius transformation on interval

**Library context:**
- Modular flow unitarity (K self-adjoint, bounded below) is established fact
- Rindler horizon temperature T_U = ℏa/(2πck_B) verified
- De Sitter/Rindler thermal spectrum is exactly Planckian (no resonances)

---

## Failure Paths

If you encounter these, report explicitly:

1. **If Connes-Rovelli don't give an explicit normalization:** Document the ambiguity, state the two interpretations, and note which is consistent with Bisognano-Wichmann. Mark the question UNRESOLVED and suggest what additional evidence would settle it.

2. **If K_A = βH_A + (constant) for ALL λ** (no ΔK_A): This would mean TTH and QM agree for ALL equilibrium coupled oscillator states. Report this as a finding — it would mean TTH's new content must be sought in non-equilibrium or non-Gibbs states.

3. **If the matrix log fails** (ρ_A has near-zero eigenvalues due to Fock truncation): Increase N or use a regularized log (add ε·I to ρ_A before taking log). Report what regularization was needed and whether the result is stable.

4. **If you find a paper that directly computes modular Hamiltonians for coupled oscillators:** Cite it and compare with your numerical result. If it gives ΔK_A analytically, extract the formula.

---

## Output

**Write to:** `/Users/seanross/kingdom_of_god/home-base/current_hunts/big-thinkers/research-systems/atlas/execution/instances/thermal-time/strategies/strategy-001/explorations/exploration-002/`

1. **`REPORT.md`** — sections: (1) Normalization Resolution, (2) Entangled-State K_A Computation, (3) ΔK_A Parameter Sweep, (4) Modular Flow Comparison, (5) Interpretation — Are TTH and QM Different?
2. **`REPORT-SUMMARY.md`** — tight summary written LAST (signals completion)
3. Save Python scripts to `code/`

**IMPORTANT:** Write REPORT.md incrementally — write the skeleton first, then fill sections. REPORT-SUMMARY.md is written LAST.

---

## The Core Question You Are Answering

**For the globally coupled thermal state of two oscillators at a single temperature β, does the modular Hamiltonian K_A of subsystem A equal βH_A, or does the coupling λ generate a correction ΔK_A = K_A - βH_A that is genuinely non-zero?**

If ΔK_A ≠ 0: this is the TTH prediction. The time flow for A under TTH is NOT the same as Heisenberg evolution under H_A. Strategy Phase 2 would then compute the observable consequences of this difference.

If ΔK_A = 0: TTH agrees with QM for equilibrium coupled oscillators. Phase 2 would need to look at non-equilibrium states or more exotic systems.

Either outcome advances the mission — but we need the number.
