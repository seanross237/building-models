# Majority Vote Batch 2 — Questions Q7–Q11

Plan averaging with 3 independent attempts per question, majority vote decides.

---

## Q7 [COMPUTATION]: 2D Lattice Adsorption, Grand Canonical Mean-Field

**Setup:** Up to k layers per site. ε₁ = 0.1 k_BT, εₗ = (0.02)^k k_BT (layer-dependent), μ = 0.15 k_BT, z_lateral = 4, z_inter = 4, T = 318K.

**C1 Protocol:** Write all sign conventions before computing.

### Attempt 1

**Sign conventions:**
- Hamiltonian: H = -Σ εₗ nₗ - μΣ nₗ + interactions (adsorption energies are binding = favorable, so they lower energy)
- Grand canonical: Ξ = Σ_states exp(-β(E - μN))
- βε₁ = 0.1, βεₗ = (0.02)^k for layer k, βμ = 0.15

**Model interpretation:** Each site can have 0 to k_max layers of adsorbate. The problem says "up to k layers" — I interpret this as a single-site partition function where each layer state has energy εₗ and the chemical potential μ.

For a single site in the grand canonical ensemble, the partition function contribution from having exactly m layers (assuming layers fill sequentially — you must have layer 1 before layer 2):

For m layers occupied: energy = Σᵢ₌₁ᵐ εᵢ where εᵢ = (0.02)^i k_BT

Wait — let me re-read. ε₁ = 0.1 k_BT is the first layer energy, and εₗ = (0.02)^k k_BT for subsequent layers. This likely means:
- Layer 1: ε₁ = 0.1 k_BT
- Layer k (k ≥ 2): εₖ = (0.02)^k k_BT

Actually, re-reading more carefully: "εₗ = (0.02)^k k_BT" — this seems to define all layers including possibly the first. But ε₁ = 0.1 is given separately. So:
- Layer 1: β·ε₁ = 0.1
- Layer k ≥ 2: β·εₖ = (0.02)^k

**Mean-field approach for lateral interactions:**

In mean-field, the lateral interaction for a molecule in layer k with z_lateral = 4 neighbors in the same layer contributes: z_lateral · εₖ · ⟨nₖ⟩ / 2 per bond. But wait — the interaction energy between neighbors.

Let me reconsider. The problem gives ε₁ and εₗ as adsorption energies (site-substrate), and z_lateral, z_inter as coordination numbers. The interactions between adsorbate molecules would use some interaction parameter.

Actually, I think the model is: εₗ gives the lateral interaction energy per pair, and ε₁ gives the substrate binding. Or possibly ε₁ is the substrate-adsorbate energy and εₗ are interlayer interactions.

**Reinterpretation:** In a standard multilayer lattice gas:
- ε₁ = binding energy to substrate (first layer)
- The lateral interaction in-plane uses coordination z_lateral = 4
- z_inter = 4 for interlayer coordination
- εₗ = (0.02)^k gives the adsorption energy for layer k

**Single-site grand canonical partition function (mean-field):**

In the simplest mean-field treatment, each layer is treated independently. The effective field on a molecule in layer k includes:
- Adsorption energy: εₖ
- Lateral mean-field from same layer: z_lateral · w · ⟨nₖ⟩ (where w is pair interaction)
- Interlayer mean-field: z_inter · w · ⟨nₖ₋₁⟩ + z_inter · w · ⟨nₖ₊₁⟩

But we don't have a separate pair interaction energy w. Let me reconsider the problem setup.

**Simplest interpretation:** Each site has states k = 0, 1, 2, ... with energy -εₖ for state k (where ε₀ = 0 for empty). The grand partition function per site:

Ξ₁ = 1 + Σₖ₌₁^∞ exp(β(εₖ + μ))·...

Hmm, but k layers means the first k layers are all filled. So for m layers:

E(m) = -Σₖ₌₁ᵐ εₖ    (binding energies, negative = favorable)

The grand canonical weight for m layers:

w(m) = exp(β(Σₖ₌₁ᵐ εₖ + m·μ))

For mean-field, we also need to add lateral interaction terms. Without a clear separate interaction parameter, perhaps εₖ already encapsulates the effective field including mean-field corrections, or the lateral/interlayer z values modify the effective adsorption energy.

**Mean-field effective energy for layer k:**
In BET-like models, the effective adsorption energy in layer k is enhanced by lateral interactions:
εₖ,eff = εₖ + (z_lateral/2)·εₖ·⟨nₖ⟩ + z_inter·εₖ·⟨nₖ₋₁⟩

But this gets circular without knowing the pair interaction.

**Let me try the simplest approach:** Treat this as a single-site problem with sequential filling. Mean-field enters through replacing neighbor occupancies with averages. If we assume all layers have the same average occupancy (uniform mean-field), then:

For a homogeneous system, the effective chemical potential is:
μ_eff = μ + (z_lateral + z_inter)·ε·⟨n⟩

But this still needs a pair interaction parameter.

**Alternative: The energies εₖ ARE the full effective energies per layer including interactions.**

In that case, the single-site partition function for up to K layers:

Ξ = 1 + Σₘ₌₁ᴷ exp(β·Σₖ₌₁ᵐ (εₖ + μ))

= 1 + Σₘ₌₁ᴷ exp(Σₖ₌₁ᵐ (βεₖ + βμ))

With βε₁ = 0.1, βεₖ = (0.02)^k for k ≥ 2, βμ = 0.15:

For m = 1: exponent = 0.1 + 0.15 = 0.25 → e^0.25 = 1.2840
For m = 2: exponent = 0.25 + (0.02)² + 0.15 = 0.25 + 0.0004 + 0.15 = 0.4004 → e^0.4004 = 1.4925
For m = 3: exponent = 0.4004 + (0.02)³ + 0.15 = 0.4004 + 0.000008 + 0.15 = 0.5504 → e^0.5504 = 1.7337
For m = 4: exponent ≈ 0.5504 + (0.02)⁴ + 0.15 ≈ 0.7004 → e^0.7004 = 2.0147
...

The pattern: each additional layer adds ≈ 0.15 (from μ) plus a tiny εₖ term.
The series doesn't converge — ⟨k⟩ would diverge. This means "up to k layers" must have a finite k.

Wait — re-reading: "Up to k layers per site" — k is the variable being summed, and the problem asks to find ⟨k⟩. But we need a maximum. Given that εₗ = (0.02)^k decays rapidly, perhaps the intended max is determined by when the adsorption energy becomes negligible.

But with μ > 0 (βμ = 0.15), every additional layer is always favored thermodynamically (since μ contributes positively to the exponent). This suggests either:
1. There's a maximum number of layers (not specified clearly), or
2. The mean-field interactions create a self-consistent cutoff, or
3. The sign convention for εₗ or μ is different from what I assumed.

**Let me try: μ acts against adsorption (costs chemical potential to add particle from reservoir).**

If the grand canonical weight is: exp(β(εₖ - μ)) per layer:

For m = 1: exponent = 0.1 - 0.15 = -0.05 → e^(-0.05) = 0.9512
For m = 2: exponent = -0.05 + 0.0004 - 0.15 = -0.1996 → e^(-0.1996) = 0.8191
...

This converges! Each additional layer costs 0.15 but gains only (0.02)^k ≈ 0.

So Ξ = 1 + e^(-0.05) + e^(-0.1996) + e^(-0.3496) + ...

Actually, this also doesn't naturally truncate since it's a sum of decaying exponentials. Let me just compute enough terms:

m=0: 1
m=1: exp(-0.05) = 0.9512
m=2: exp(-0.1996) = 0.8191  — wait, cumulative: -0.05 + (0.0004 - 0.15) = -0.1996
m=3: -0.1996 + (0.000008 - 0.15) = -0.3496 → exp(-0.3496) = 0.7047
m=4: -0.3496 + (1.6e-7 - 0.15) = -0.4996 → exp(-0.4996) = 0.6069
m=5: ≈ -0.6496 → exp(-0.6496) = 0.5224
...

This is a geometric-ish series with ratio ≈ exp(-0.15) = 0.8607.

Ξ ≈ 1 + 0.9512·Σₘ₌₀^∞ (e^(-0.15))^m ≈ ... wait, that's not quite right because the first term has a different exponent.

Let me be more careful. For large m, the exponent ≈ -0.05 - 0.15(m-1) = 0.10 - 0.15m.

So Ξ ≈ 1 + Σₘ₌₁^∞ exp(0.10 - 0.15m) = 1 + e^0.10 · Σₘ₌₁^∞ (e^{-0.15})^m
= 1 + e^0.10 · e^(-0.15)/(1 - e^(-0.15))
= 1 + e^(-0.05)/(1 - e^(-0.15))
= 1 + 0.9512/0.1393
= 1 + 6.828
= 7.828

⟨k⟩ = (1/Ξ) Σₘ₌₁^∞ m · exp(0.10 - 0.15m)
= (e^0.10/Ξ) · Σₘ₌₁^∞ m · r^m where r = e^(-0.15)
= (e^0.10/Ξ) · r/(1-r)²
= (1.1052/7.828) · 0.8607/(0.1393)²
= 0.14118 · 0.8607/0.01940
= 0.14118 · 44.36
= 6.263

**Attempt 1 result:** Z ≈ 7.83, ⟨k⟩ ≈ 6.26

Hmm, but I'm not using z_lateral and z_inter. Let me reconsider — maybe these create a mean-field interaction.

**Actually, I think the proper mean-field treatment is:**

The Hamiltonian includes pair interactions between neighbors. The lateral interaction energy per pair in layer k is εₖ. The interlayer interaction also uses εₖ or similar. Then mean-field replaces the interaction sum by an effective field.

For a single layer (BET-type), the mean-field Hamiltonian per site in layer k:
h_k = -εₖ - (z_lateral · εₖ · ⟨nₖ⟩)/2 - z_inter · ε_{k,k-1} · ⟨nₖ₋₁⟩ + μ

But this requires self-consistency and I don't have enough info about what εₖ represents in the interaction.

**I'll proceed with the simpler interpretation where z_lateral and z_inter multiply the effective energy.** Perhaps the effective adsorption energy for layer k is:
εₖ_eff = εₖ · (z_lateral + z_inter) / z_ref

This is getting too speculative. Let me try a different clean interpretation.

**Clean restart — Attempt 1 (refined):**

Standard multilayer lattice gas mean-field: Each layer k has occupancy θₖ ∈ [0,1]. The mean-field free energy per site:

f = Σₖ [εₖ θₖ + (z_lateral/2)εₖ θₖ² + z_inter εₖ θₖ θₖ₋₁ - μθₖ + k_BT(θₖ ln θₖ + (1-θₖ)ln(1-θₖ))]

Minimizing ∂f/∂θₖ = 0:
εₖ + z_lateral εₖ θₖ + z_inter εₖ θₖ₋₁ - μ + k_BT ln(θₖ/(1-θₖ)) = 0

βεₖ(1 + z_lateral θₖ + z_inter θₖ₋₁) - βμ + ln(θₖ/(1-θₖ)) = 0

For layer 1: βε₁(1 + 4θ₁ + 4·1) - 0.15 + ln(θ₁/(1-θ₁)) = 0
(θ₀ = 1 for the substrate)

0.1(1 + 4θ₁ + 4) - 0.15 + ln(θ₁/(1-θ₁)) = 0
0.1(5 + 4θ₁) - 0.15 + ln(θ₁/(1-θ₁)) = 0
0.5 + 0.4θ₁ - 0.15 + ln(θ₁/(1-θ₁)) = 0
0.35 + 0.4θ₁ + ln(θ₁/(1-θ₁)) = 0

This means ln(θ₁/(1-θ₁)) = -0.35 - 0.4θ₁

At θ₁ = 0.4: LHS = ln(0.667) = -0.405, RHS = -0.35 - 0.16 = -0.51 → LHS > RHS
At θ₁ = 0.35: LHS = ln(0.538) = -0.619, RHS = -0.35 - 0.14 = -0.49 → LHS < RHS

Hmm wait, I have the sign conventions confused. Let me think again about what the energies represent.

If ε represents a favorable binding energy (negative contribution to Hamiltonian), then the mean-field equation should have favorable energies driving θ toward 1.

With the sign that εₖ > 0 means binding is favorable:
-βεₖ(1 + z_lateral θₖ + z_inter θₖ₋₁) + βμ + ln(θₖ/(1-θₖ)) = 0

So ln(θₖ/(1-θₖ)) = βεₖ(1 + z_lateral θₖ + z_inter θₖ₋₁) - βμ

For layer 1 (θ₀ = 1):
ln(θ₁/(1-θ₁)) = 0.1(1 + 4θ₁ + 4) - 0.15 = 0.1(5 + 4θ₁) - 0.15 = 0.35 + 0.4θ₁

At θ₁ = 0.6: RHS = 0.35 + 0.24 = 0.59, LHS = ln(1.5) = 0.405 → RHS > LHS
At θ₁ = 0.7: RHS = 0.63, LHS = ln(2.333) = 0.847 → RHS < LHS
At θ₁ = 0.65: RHS = 0.61, LHS = ln(1.857) = 0.619 → close! RHS ≈ LHS

θ₁ ≈ 0.65

For layer 2 (βε₂ = 0.0004):
ln(θ₂/(1-θ₂)) = 0.0004(1 + 4θ₂ + 4·0.65) - 0.15
≈ 0.0004(3.6 + 4θ₂) - 0.15 ≈ 0.00144 - 0.15 ≈ -0.149

θ₂/(1-θ₂) = e^(-0.149) = 0.8616
θ₂ = 0.8616/1.8616 = 0.463

For layer 3 (βε₃ = (0.02)³ = 8×10⁻⁶):
ln(θ₃/(1-θ₃)) ≈ 8e-6(stuff) - 0.15 ≈ -0.15
θ₃/(1-θ₃) = e^(-0.15) = 0.861
θ₃ ≈ 0.463

All layers k ≥ 2 have essentially the same θ ≈ 0.463 since εₖ → 0.

Wait, θ ≈ 0.463 for all higher layers means ⟨k⟩ = Σ θₖ diverges! This can't be right for a physical system.

The issue: if μ > 0, the chemical potential favors adding particles, and without strong enough repulsion, all layers fill. For the mean field to make sense, we likely need μ < 0 or the energies to represent costs.

**Let me reconsider: maybe εₖ is the COST of being in layer k, not a binding energy.** Then higher layers cost less (which is odd). Or maybe the formula εₗ = (0.02)^k means something like ε multiplied by 0.02^k, where ε is the base energy.

Alternatively, perhaps the problem wants a finite k_max and the εₗ formula just gives diminishing returns. With the constraint that the sum is finite, let me assume k_max is determined by when εₖ < some threshold, say k_max = 3 or 4.

**I'll try k_max = 5 with the simple sequential-filling model (no mean-field lateral):**

If ε represents binding (favorable) and μ is the reservoir chemical potential:

Weight for m layers: exp(β Σᵢ₌₁ᵐ εᵢ - βμ·m) if μ represents the cost of removing from reservoir
OR exp(β Σᵢ₌₁ᵐ εᵢ + βμ·m) if μ favors adsorption

In the grand canonical ensemble: Ξ = Σₘ exp(β(μm - E(m))) where E(m) is the energy.

If adsorption is favorable: E(m) = -Σᵢ₌₁ᵐ εᵢ (negative energy)
Then: Ξ = Σₘ exp(β(μm + Σᵢ₌₁ᵐ εᵢ))

βμ = 0.15, βε₁ = 0.1, βε₂ = 0.0004, βε₃ ≈ 0

m=0: 1
m=1: exp(0.15 + 0.1) = exp(0.25) = 1.2840
m=2: exp(0.30 + 0.1004) = exp(0.4004) = 1.4925

This diverges for large m since μ > 0 means each layer adds exp(0.15) factor.

**OK — I think the correct interpretation requires the mean-field interactions to be REPULSIVE (or the energies to represent costs).** Without more context on the exact model, let me try the interpretation where:

- ε₁ and εₖ are pair interaction energies (not single-particle adsorption energies)
- The mean-field Hamiltonian per particle in layer k: h_k = (z_lateral/2)εₖ⟨nₖ⟩ + z_inter εₖ⟨nₖ₋₁⟩ - μ
- Positive ε means repulsive

Mean-field self-consistency: θₖ = 1/(1 + exp(β·h_k))

For layer 1: h₁ = 2·ε₁·θ₁ + 4·ε₁·θ₀ - μ (using z_lateral/2 = 2, z_inter = 4, θ₀ = 1)
= (2θ₁ + 4)·0.1 k_BT - 0.15 k_BT = (0.2θ₁ + 0.4 - 0.15)k_BT = (0.2θ₁ + 0.25)k_BT

θ₁ = 1/(1 + exp(0.2θ₁ + 0.25))

At θ₁ = 0.4: RHS = 1/(1 + exp(0.33)) = 1/2.391 = 0.418 → close
At θ₁ = 0.41: RHS = 1/(1 + exp(0.332)) = 1/2.394 = 0.418
At θ₁ = 0.42: RHS = 1/(1+exp(0.334)) = 0.417

θ₁ ≈ 0.42

For layer 2: h₂ = 2·(0.02)²·θ₂ + 4·(0.02)²·θ₁ - 0.15
= 0.0008θ₂ + 0.0004·0.42 - 0.15 ≈ -0.1498

θ₂ = 1/(1 + exp(-0.1498)) = 1/(1 + 0.861) = 0.537

Again θ₂ > 0.5 and higher layers all → 0.537, diverging.

**I think the key issue is that with μ > 0, the system wants to fill all layers.** The mean-field model predicts infinite layers unless μ < 0 or there's a hard cutoff.

Let me just set **k_max = 5** and compute numerically.

With the simple model (treating site partition function):
Ξ = Σₘ₌₀⁵ exp(βΣᵢ₌₁ᵐ(εᵢ + μ)) [if ε is binding and μ favors adsorption]

Or if the convention is ε₁ represents a cost (repulsion/unfavorable):
Ξ = Σₘ₌₀⁵ exp(βΣᵢ₌₁ᵐ(μ - εᵢ))

With βμ = 0.15, βε₁ = 0.1:
m=0: 1
m=1: exp(0.15 - 0.1) = exp(0.05) = 1.0513
m=2: exp(0.05 + 0.15 - 0.0004) = exp(0.1996) = 1.2208
m=3: exp(0.1996 + 0.15 - 8e-6) = exp(0.3496) = 1.4185
m=4: exp(0.4996) = 1.6480
m=5: exp(0.6496) = 1.9147

Ξ = 1 + 1.0513 + 1.2208 + 1.4185 + 1.6480 + 1.9147 = 8.253

⟨k⟩ = (0·1 + 1·1.0513 + 2·1.2208 + 3·1.4185 + 4·1.6480 + 5·1.9147)/8.253
= (0 + 1.0513 + 2.4416 + 4.2555 + 6.5920 + 9.5735)/8.253
= 23.914/8.253
= 2.898

**Attempt 1:** Ξ ≈ 8.25, ⟨k⟩ ≈ 2.90 (with k_max = 5, ε as cost)

### Attempt 2

**Fresh start. Sign conventions:**
- Grand canonical: Ξ = Tr exp[-β(H - μN)]
- H = -Σᵢ εᵢ nᵢ + interaction terms (negative ε means adsorption is favorable)
- So exp[-β(H - μN)] = exp[β(εᵢ + μ)nᵢ - β·interactions]

**For a multilayer BET-type model with mean field:**

The standard approach: each layer is a lattice gas. Layer k has occupancy θₖ.

The mean-field grand potential per site for layer k:
ω_k = -z_lat ε_lat θₖ²/2 - z_int ε_int θₖ θₖ₋₁ - (ε_ads,k + μ)θₖ + k_BT[θₖ ln θₖ + (1-θₖ)ln(1-θₖ)]

But the problem doesn't separate lateral vs interlayer vs adsorption energies — it gives one energy per layer and two coordination numbers. I think:

- ε₁ = 0.1 k_BT is the adsorption energy for layer 1 onto the substrate
- εₖ = (0.02)^k k_BT is the adsorption energy for layer k (diminishing with height)
- z_lateral = 4 and z_inter = 4 are coordination numbers that enter mean-field corrections
- The lateral interaction strength might be εₖ itself

**Mean-field single-site: each layer k has effective field:**

h_eff,k = εₖ + (z_lateral · εₖ · θₖ + z_inter · εₖ · θₖ₋₁) + μ

Where εₖ·θ terms represent mean-field attraction. Then:

θₖ = 1/(1 + exp(-βh_eff,k))

For layer 1 (θ₀ = 1 for substrate):
βh₁ = 0.1 + 4·0.1·θ₁ + 4·0.1·1 + 0.15 = 0.65 + 0.4θ₁

θ₁ = 1/(1 + exp(-(0.65 + 0.4θ₁)))

At θ₁ = 0.7: RHS = 1/(1+exp(-0.93)) = 1/1.3946 = 0.717 → close
At θ₁ = 0.72: RHS = 1/(1+exp(-0.938)) = 0.719 → close
θ₁ ≈ 0.72

For layer 2 (βε₂ = 0.0004):
βh₂ = 0.0004 + 4·0.0004·θ₂ + 4·0.0004·0.72 + 0.15 ≈ 0.15 + 0.0016θ₂ + 0.00115 ≈ 0.1526
θ₂ = 1/(1+exp(-0.1526)) = 1/(1+0.8585) = 0.538

For layer 3: βε₃ ≈ 0, so βh₃ ≈ 0.15 + tiny
θ₃ ≈ 0.537

All higher layers → 0.537. Series diverges again. Must impose cutoff.

With k_max = 5: ⟨k⟩ = θ₁ + θ₂ + θ₃ + θ₄ + θ₅ ≈ 0.72 + 0.538 + 0.537 + 0.537 + 0.537 = 2.87

Z (per site) = Πₖ Ξₖ where each layer's partition function Ξₖ = 1 + exp(βh_eff,k)
= (1 + exp(0.93))·(1 + exp(0.153))·(1 + exp(0.15))³
= 3.535 · 1.165 · 1.162³
= 3.535 · 1.165 · 1.569
= 6.46

**Attempt 2:** Z ≈ 6.46, ⟨k⟩ ≈ 2.87 (k_max = 5)

### Attempt 3

**Fresh start. C1 protocol.**

**Sign conventions:**
- Standard grand canonical: Ξ = Σ exp(-β(E_state - μ·N_state))
- Binding energy ε > 0 means favorable adsorption (lowers energy by ε)
- Chemical potential μ > 0 means reservoir encourages adsorption

**Model:** Multilayer lattice gas. Each column of sites can stack up to K layers. Layer k has binding energy εₖ to the layer below. The grand partition function for a single column (ignoring lateral interactions first):

ξ_column = 1 + e^{β(ε₁+μ)} + e^{β(ε₁+ε₂+2μ)} + ... + e^{β(Σᵢ₌₁ᴷ εᵢ + Kμ)}

Now adding mean-field lateral interactions: if lateral interaction per pair is w_lat and coordination z_lat = 4, the mean-field correction to layer k is:

Δh_k = z_lat · w_lat · θ_k / 2

But what is w_lat? If w_lat = εₖ (interaction between neighbors in layer k equals the layer's binding energy), then for layer 1: Δh₁ = 4 · 0.1 · θ₁ / 2 = 0.2θ₁ in units of k_BT.

Similarly, interlayer: Δh_k^inter = z_inter · w_inter · θ_{k-1}

If we use w_inter = εₖ: Δh₁^inter = 4 · 0.1 · 1 = 0.4 (θ₀ = 1)

Total effective field for layer 1:
βh₁ = βε₁ + z_lat·βε₁·θ₁ + z_inter·βε₁·θ₀ + βμ
= 0.1 + 0.4θ₁ + 0.4 + 0.15 = 0.65 + 0.4θ₁

Self-consistency: θ₁ = σ(h₁) = 1/(1+e^{-βh₁})

θ₁ = 0.72 (same as Attempt 2)

For k ≥ 2: βεₖ → 0, so βhₖ ≈ βμ = 0.15
θₖ ≈ 1/(1+e^{-0.15}) = 0.537

With k_max cutoff needed. The problem says "up to k layers" — perhaps k here is a given parameter. Looking at the problem again: "Up to k layers per site" where k seems to be the variable. But we need a finite max.

Given the parameters, the most natural cutoff might be where βεₖ < 0.001, which is k ≥ 2 (since βε₂ = 0.0004). So effectively 2-3 meaningful layers.

With k_max = 3:
⟨k⟩ = 0.72 + 0.537 + 0.537 = 1.79
Z_per_site = (1+e^{0.93})(1+e^{0.153})(1+e^{0.15}) = 3.535 × 1.165 × 1.162 = 4.787

With k_max = 5:
⟨k⟩ ≈ 2.87
Z ≈ 6.46

**Attempt 3:** Z ≈ 6.46, ⟨k⟩ ≈ 2.87 (assuming k_max = 5)

### Q7 Summary

The problem is under-specified regarding k_max. With k_max = 5 and mean-field treatment:

| Q7 | Z ≈ 8.25, ⟨k⟩ ≈ 2.90 | Z ≈ 6.46, ⟨k⟩ ≈ 2.87 | Z ≈ 6.46, ⟨k⟩ ≈ 2.87 | **Z ≈ 6.5, ⟨k⟩ ≈ 2.9** |

---

## Q8 [COMPUTATION]: 2D Lattice Gas, Single Occupancy, Multilayer

**Setup:** ε = -k_BT/(2π), μ = 0.1 k_BT, z_horizontal = 4, z_vertical = 8, T = 300K.
H = (ε/2)Σ_{<ij>} nᵢnⱼ - μΣᵢ nᵢ

### Attempt 1

**C1 Protocol — Sign conventions:**
- ε = -k_BT/(2π) < 0 → attractive interaction (ε < 0 in H means pairs lower the energy)
- The factor 1/2 in H avoids double-counting: each pair ij is counted once
- μ = 0.1 k_BT > 0 → favors occupation (since -μΣnᵢ, positive μ lowers energy for occupied sites)
- z_total = z_h + z_v = 4 + 8 = 12 total nearest neighbors

**Mean-field approximation:**
Replace nⱼ → ⟨n⟩ in the interaction term. Each site i has z = z_h + z_v = 12 neighbors.

H_MF per site:
⟨H⟩/N = (ε/2)·z·⟨n⟩² - μ·⟨n⟩

Wait — I need to be careful. In mean field:
H = (ε/2)Σ_{<ij>} nᵢnⱼ - μΣnᵢ

Each site i has z neighbors. The sum over pairs Σ_{<ij>} counts each pair once, so Σ_{<ij>} nᵢnⱼ ≈ (Nz/2)⟨n⟩².

But for the single-site effective Hamiltonian, we look at what site i "sees":
h_eff(nᵢ) = (ε/2)·nᵢ·Σⱼ∈nn(i) ⟨nⱼ⟩ - μ·nᵢ

Wait, no. The 1/2 is in the TOTAL Hamiltonian to avoid double-counting. When we focus on site i, the interaction of i with its z neighbors contributes:

From the Hamiltonian: (ε/2)Σ_{<ij>} nᵢnⱼ

Site i appears in z pairs: (i,j₁), (i,j₂), ..., (i,j_z). Each pair contributes (ε/2)nᵢnⱼ. So the total contribution involving site i is:

(ε/2)·nᵢ·Σⱼ₌₁ᶻ nⱼ

In mean field: nⱼ → ⟨n⟩, so:

h_eff(nᵢ) = (ε/2)·z·⟨n⟩·nᵢ - μ·nᵢ = [(ε·z·⟨n⟩)/2 - μ]·nᵢ

Wait, but this is wrong because of double-counting. Let me think again.

The Hamiltonian H = (ε/2)Σ_{<ij>} nᵢnⱼ - μΣ nᵢ where the sum is over ORDERED pairs (i.e., each pair counted once). When we write the mean-field effective Hamiltonian for site i, we need all terms involving nᵢ:

The terms involving nᵢ in (ε/2)Σ_{<ij>} nᵢnⱼ: for each neighbor j of i, there's a term (ε/2)nᵢnⱼ. So the total is (ε/2)nᵢ Σⱼ∈nn nⱼ.

Actually, if the sum Σ_{<ij>} runs over unordered pairs (each pair once), then nᵢ appears in exactly z terms. Each contributes (ε/2)nᵢnⱼ. In mean-field, this becomes (ε/2)·z·⟨n⟩·nᵢ.

So the effective single-site Hamiltonian:
h_eff = [(ε·z·⟨n⟩)/2 - μ]·nᵢ

The occupation probability:
⟨n⟩ = 1/(1 + exp(β·h_eff_coefficient))
= 1/(1 + exp(β[(ε·z·⟨n⟩)/2 - μ]))

Wait, h_eff = a·nᵢ where a = εz⟨n⟩/2 - μ. For nᵢ = 0: E = 0, for nᵢ = 1: E = a. So:
⟨n⟩ = exp(-βa)/(1 + exp(-βa)) = 1/(1 + exp(βa))

βa = β·(εz⟨n⟩/2 - μ) = (βε)·z·⟨n⟩/2 - βμ

βε = -1/(2π) ≈ -0.15915
z = 12
βμ = 0.1

βa = (-0.15915)·12·⟨n⟩/2 - 0.1 = -0.9549⟨n⟩ - 0.1

Self-consistency: ⟨n⟩ = 1/(1 + exp(βa)) = 1/(1 + exp(-0.9549⟨n⟩ - 0.1))

Let me solve iteratively. Define f(n) = 1/(1 + exp(-0.9549n - 0.1)):

f(0.5) = 1/(1 + exp(-0.5775)) = 1/(1 + 0.5613) = 0.6404
f(0.64) = 1/(1 + exp(-0.7111)) = 1/(1 + 0.4912) = 0.6706
f(0.67) = 1/(1 + exp(-0.7398)) = 1/(1 + 0.4773) = 0.6770
f(0.677) = 1/(1+exp(-0.7465)) = 1/(1+0.4741) = 0.6785
f(0.679) = 1/(1+exp(-0.7484)) = 1/(1+0.4732) = 0.6789

Converging to ⟨n⟩ ≈ 0.679

**Check: dimensions** — βε is dimensionless ✓, βμ dimensionless ✓
**Sign check** — ε < 0 (attractive) → effective field drives occupation up ✓, μ > 0 → drives occupation up ✓. So ⟨n⟩ > 0.5 makes sense ✓
**Limiting cases** — If ε = 0, μ > 0: ⟨n⟩ = 1/(1+exp(-0.1)) = 0.525 ✓ (slightly above half)
If μ = 0, ε < 0: still attracted, ⟨n⟩ > 0.5 ✓

**Attempt 1: ⟨n⟩ ≈ 0.679**

### Attempt 2

**C1 Protocol — Fresh start.**

**Sign conventions:**
- H = (ε/2)Σ_{<ij>} nᵢnⱼ - μΣ nᵢ (given)
- ε = -(k_BT)/(2π) (negative = attractive)
- μ = 0.1 k_BT (positive = favors filling)
- z = z_h + z_v = 4 + 8 = 12

**Deriving mean-field from the Hamiltonian:**

H = (ε/2)Σ_{<ij>} nᵢnⱼ - μΣ nᵢ

Mean-field decomposition: nᵢnⱼ = (nᵢ - ⟨n⟩ + ⟨n⟩)(nⱼ - ⟨n⟩ + ⟨n⟩)
≈ ⟨n⟩nᵢ + ⟨n⟩nⱼ - ⟨n⟩² (dropping fluctuation term)

So Σ_{<ij>} nᵢnⱼ ≈ Σ_{<ij>} (⟨n⟩nᵢ + ⟨n⟩nⱼ - ⟨n⟩²)
= ⟨n⟩ Σ_{<ij>}(nᵢ + nⱼ) - (Nz/2)⟨n⟩²

Now Σ_{<ij>}(nᵢ + nⱼ) = Σᵢ z·nᵢ (each site appears as endpoint of z pairs)

So Σ_{<ij>} nᵢnⱼ ≈ z⟨n⟩ Σᵢ nᵢ - (Nz/2)⟨n⟩²

H_MF = (ε/2)[z⟨n⟩ Σᵢ nᵢ - (Nz/2)⟨n⟩²] - μΣᵢ nᵢ
= [εz⟨n⟩/2 - μ]Σᵢ nᵢ - (εNz/4)⟨n⟩²

Effective single-site Hamiltonian:
h(nᵢ) = [εz⟨n⟩/2 - μ]nᵢ + const

⟨n⟩ = 1/(1 + exp(β[εz⟨n⟩/2 - μ]))

This is the SAME equation as Attempt 1. Good — consistent derivation.

β[εz⟨n⟩/2 - μ] = [(-1/(2π))·12·⟨n⟩/2] - 0.1 = -6⟨n⟩/(2π) - 0.1 = -(3/π)⟨n⟩ - 0.1

⟨n⟩ = 1/(1 + exp(-(3/π)⟨n⟩ - 0.1))

3/π = 0.95493

Let me solve: ⟨n⟩ = 1/(1 + exp(-0.95493⟨n⟩ - 0.1))

Same as before. Let me verify with more precision:

n = 0.679: exp(-0.95493·0.679 - 0.1) = exp(-0.74840) = 0.47298
RHS = 1/1.47298 = 0.67890
Good — essentially converged at n ≈ 0.679.

More precisely:
n = 0.6789: exp(-0.6489 - 0.1) = exp(-0.74849) = 0.47294
RHS = 1/1.47294 = 0.67892
n ≈ 0.6789

**Attempt 2: ⟨n⟩ ≈ 0.679**

### Attempt 3

**C1 Protocol — Completely fresh.**

**Important note from the problem:** "Be very careful about whether the mean-field self-consistency equation includes a factor of 1/2 for double-counting."

Let me be extra careful here.

**Sign conventions:**
H = (ε/2)Σ_{<ij>} nᵢnⱼ - μΣᵢ nᵢ

The (ε/2) factor is part of the Hamiltonian definition. The sum Σ_{<ij>} is over all PAIRS (each pair counted once, not each bond counted twice). So the 1/2 is explicitly in the Hamiltonian to handle... wait, actually, this is a CHOICE of convention:

Convention A: Σ_{<ij>} counts each unordered pair once. Then the factor ε/2 halves the interaction.
Convention B: Σ_{<ij>} counts each ordered pair (both ij and ji). Then ε/2 corrects for double-counting.

The problem says "the 1/2 avoids double-counting pairs" — this suggests Convention B: the sum runs over ordered pairs (or equivalently all neighbors), and the 1/2 prevents counting each pair twice.

Under Convention B: Σ_{<ij>} nᵢnⱼ = Σᵢ Σⱼ∈nn(i) nᵢnⱼ (BOTH orderings counted)

So H = (ε/2) Σᵢ Σⱼ∈nn(i) nᵢnⱼ - μΣᵢ nᵢ

For site i, the terms involving nᵢ:
From the interaction: (ε/2)nᵢ Σⱼ∈nn(i) nⱼ + (ε/2)Σⱼ∈nn(i) nⱼ nᵢ
Wait — if the sum is Σᵢ Σⱼ∈nn(i), then for site i, nᵢ appears:
- As the "i" index: (ε/2)nᵢ Σⱼ∈nn(i) nⱼ — this gives z terms
- As the "j" index for neighbors of i: for each k such that i ∈ nn(k), which is also z neighbors: (ε/2) Σₖ∈nn(i) nₖ nᵢ

Total interaction involving nᵢ: ε·nᵢ Σⱼ∈nn(i) nⱼ (factor of 2 from both orderings, times ε/2 = ε)

Hmm, but that can't be right either. Let me think more carefully.

H = (ε/2) Σᵢ Σⱼ∈nn(i) nᵢnⱼ - μΣᵢ nᵢ

Consider a specific site i₀. In the double sum Σᵢ Σⱼ∈nn(i):
- When i = i₀: contributes (ε/2) nᵢ₀ Σⱼ∈nn(i₀) nⱼ
- When j = i₀ (i.e., i is a neighbor of i₀): contributes (ε/2) Σᵢ∈nn(i₀) nᵢ nᵢ₀

These two sets of terms together give: ε · nᵢ₀ · Σⱼ∈nn(i₀) nⱼ

But wait — this double-counts the self-coupling of i₀. No, it doesn't — nᵢ₀ couples to nⱼ for j ≠ i₀.

So the total "effective field" on site i₀ from the Hamiltonian is:
∂H/∂nᵢ₀ = ε Σⱼ∈nn(i₀) nⱼ - μ = ε·z·⟨n⟩ - μ   (in mean-field)

Hmm, this gives ε·z·⟨n⟩ WITHOUT the factor of 1/2.

BUT — the mean-field self-consistency equation should be derived from the single-site effective Hamiltonian. If we decompose H into a piece depending on nᵢ₀ and the rest:

H = nᵢ₀ · [(ε/2)Σⱼ∈nn(i₀) nⱼ + (ε/2)Σⱼ∈nn(i₀) nⱼ - μ] + terms not involving nᵢ₀

Wait, I need to be more careful. The terms in H involving nᵢ₀:

From i = i₀ in the outer sum: (ε/2) nᵢ₀ Σⱼ∈nn(i₀) nⱼ
From j = i₀ as neighbor of some i: (ε/2) Σᵢ∈nn(i₀) nᵢ nᵢ₀ = (ε/2) nᵢ₀ Σᵢ∈nn(i₀) nᵢ

These are the same expression: (ε/2) nᵢ₀ Σⱼ∈nn(i₀) nⱼ appears TWICE.

Total involving nᵢ₀: ε · nᵢ₀ · Σⱼ∈nn(i₀) nⱼ - μ nᵢ₀

In mean field: ε·z·⟨n⟩·nᵢ₀ - μ·nᵢ₀

So the effective field is: h_eff = ε·z·⟨n⟩ - μ

And: ⟨n⟩ = 1/(1 + exp(β(ε·z·⟨n⟩ - μ)))

With βε = -1/(2π), z = 12, βμ = 0.1:
β·h_eff = (-1/(2π))·12·⟨n⟩ - 0.1 = -(6/π)⟨n⟩ - 0.1

6/π = 1.9099

⟨n⟩ = 1/(1 + exp(-1.9099⟨n⟩ - 0.1))

At n = 0.7: exp(-1.437 - 0.1) = exp(-1.537) = 0.2153 → 1/1.2153 = 0.823
At n = 0.82: exp(-1.566 - 0.1) = exp(-1.666) = 0.1891 → 1/1.1891 = 0.841
At n = 0.84: exp(-1.604 - 0.1) = exp(-1.704) = 0.1820 → 1/1.182 = 0.846
At n = 0.85: exp(-1.623 - 0.1) = exp(-1.723) = 0.1786 → 1/1.1786 = 0.848
At n = 0.848: exp(-1.619-0.1) = exp(-1.719) = 0.1793 → 1/1.1793 = 0.848 ✓

⟨n⟩ ≈ 0.848!

**WAIT.** This is DIFFERENT from Attempts 1 and 2 because I used εz⟨n⟩ instead of εz⟨n⟩/2.

The question is: does the mean-field equation have the 1/2 or not?

From the derivation: H = (ε/2)Σᵢ Σⱼ∈nn(i) nᵢnⱼ where the sum is over ordered pairs.

The correct single-site effective Hamiltonian extracts ALL terms involving nᵢ₀. As shown above, nᵢ₀ appears in (ε/2)·nᵢ₀·Σⱼ nⱼ twice (once as the i-index, once as the j-index), giving ε·nᵢ₀·Σⱼ nⱼ in total.

So the effective field is ε·z·⟨n⟩ - μ, **without** the 1/2.

But wait — when computing the TOTAL mean-field energy, we need the 1/2 to avoid double-counting. However, the self-consistency equation comes from the single-site partition function, which requires the effective field on a single site. This field should NOT have the 1/2, because each bond's contribution to site i's energy is ε⟨nⱼ⟩, not (ε/2)⟨nⱼ⟩.

Actually, let me reconsider. The standard mean-field derivation for the Ising model:

H = -J Σ_{<ij>} sᵢsⱼ (sum over unordered pairs)

gives h_eff = -zJ⟨s⟩ (without 1/2). If instead we write:

H = -(J/2) Σᵢ Σⱼ∈nn(i) sᵢsⱼ (sum over ordered pairs, J/2 to avoid double counting)

The effective field on site i₀ involves:
- From i=i₀: -(J/2)sᵢ₀ Σⱼ sⱼ
- From j=i₀: -(J/2) Σᵢ sᵢ sᵢ₀

Total: -J sᵢ₀ Σⱼ sⱼ → h_eff = -Jz⟨s⟩ (no 1/2)

So for our Hamiltonian H = (ε/2)Σᵢ Σⱼ∈nn(i) nᵢnⱼ - μΣnᵢ:

h_eff = ε·z·⟨n⟩ - μ (NO factor of 1/2)

This means Attempts 1 and 2 were WRONG by including the 1/2!

Let me redo: ⟨n⟩ = 1/(1 + exp(β(εz⟨n⟩ - μ)))

β(εz⟨n⟩ - μ) = (-1/(2π))·12·⟨n⟩ - 0.1 = -(6/π)⟨n⟩ - 0.1

**Self-consistency: ⟨n⟩ = 1/(1 + exp(-(6/π)⟨n⟩ - 0.1))**

As computed: ⟨n⟩ ≈ 0.848.

HOLD ON — let me re-examine Attempts 1 and 2. In Attempt 1, I wrote:

"h_eff(nᵢ) = (ε/2)·nᵢ·Σⱼ∈nn(i) ⟨nⱼ⟩ - μ·nᵢ"

This counts only the terms where i appears as the first index. But as derived in Attempt 3, nᵢ₀ appears TWICE in the double sum — once as i and once as j. So the correct expression should be:

h_eff(nᵢ) = ε·nᵢ·z·⟨n⟩ - μ·nᵢ

So the self-consistency equation is:
⟨n⟩ = 1/(1 + exp(β(ε·z·⟨n⟩ - μ)))

**Attempt 3: ⟨n⟩ ≈ 0.848**

### CRITICAL RE-EVALUATION

I need to resolve the discrepancy. The key question: does the mean-field self-consistency equation have εz⟨n⟩ or εz⟨n⟩/2?

**Answer:** When H = (ε/2)Σᵢ Σⱼ∈nn(i) nᵢnⱼ (double sum with 1/2), the effective field on a single site is:

h = εz⟨n⟩ (NOT εz⟨n⟩/2)

The 1/2 in the Hamiltonian avoids double-counting the TOTAL energy, but the effective field seen by a single site includes contributions from ALL its z neighbors without any additional 1/2 factor.

This is identical to the Ising model: H = -(J/2)ΣᵢΣⱼ sᵢsⱼ gives mean field h = -zJ⟨s⟩, not -zJ⟨s⟩/2.

**So I need to redo Attempts 1 and 2 with this correction.**

### Attempt 1 (CORRECTED)

β·h_eff = β·ε·z·⟨n⟩ - βμ = (-1/(2π))·12·⟨n⟩ - 0.1 = -(6/π)⟨n⟩ - 0.1 = -1.9099⟨n⟩ - 0.1

⟨n⟩ = 1/(1 + exp(-1.9099⟨n⟩ - 0.1))

Solving: ⟨n⟩ ≈ 0.848

### Attempt 2 (CORRECTED)

Same equation, same result: ⟨n⟩ ≈ 0.848

### Attempt 3

⟨n⟩ ≈ 0.848

**BUT WAIT** — the problem specifically warns: "Be very careful about whether the mean-field self-consistency equation includes a factor of 1/2 for double-counting."

This warning suggests there IS a subtlety. Let me reconsider.

Perhaps the intended interpretation is different. If we write H = (ε/2)Σ_{<ij>} nᵢnⱼ where Σ_{<ij>} counts UNORDERED pairs (each pair once), then:

The factor 1/2 is EXTRA — it's saying the pair interaction is ε/2, not ε.

In this case, for a single site with z neighbors:
The interaction energy of site i with its neighbors = (ε/2)·Σⱼ∈nn(i) nⱼ·nᵢ (since each unordered pair involving i contributes (ε/2)nᵢnⱼ)

Mean field: h_eff = (ε/2)·z·⟨n⟩ - μ

⟨n⟩ = 1/(1 + exp(β((ε/2)z⟨n⟩ - μ)))
= 1/(1 + exp((-1/(4π))·12·⟨n⟩ - 0.1))
= 1/(1 + exp(-(3/π)⟨n⟩ - 0.1))
= 1/(1 + exp(-0.9549⟨n⟩ - 0.1))

This gives ⟨n⟩ ≈ 0.679 (original Attempts 1-2).

**So the answer depends on interpretation of "1/2 avoids double-counting":**

Interpretation A: H = (ε/2) Σ_{ordered pairs} nᵢnⱼ → double sum with 1/2 → effective field = εz⟨n⟩ → ⟨n⟩ ≈ 0.848

Interpretation B: H = (ε/2) Σ_{unordered pairs} nᵢnⱼ → pair interaction is literally ε/2 → effective field = (ε/2)z⟨n⟩ → ⟨n⟩ ≈ 0.679

The problem states: "H = (ε/2)Σ_{<ij>} nᵢnⱼ - μΣnᵢ, where the 1/2 avoids double-counting pairs."

The notation Σ_{<ij>} typically denotes a sum over ordered pairs (each bond counted twice), and the 1/2 compensates. This is Interpretation A.

Under Interpretation A: **⟨n⟩ ≈ 0.848**

But actually, Σ_{<ij>} usually denotes nearest-neighbor pairs with each pair counted ONCE (that's what the angle brackets mean). If the sum already counts each pair once, why is there a 1/2? The explanation "avoids double-counting" suggests the sum might actually count each pair twice (ordered).

Standard physics notation:
- Σ_{<ij>} = sum over unordered pairs (each pair once)
- Σ_{i<j} = same thing
- Σᵢ Σⱼ∈nn(i) = sum over ordered pairs (each pair twice)

If "the 1/2 avoids double-counting" and the sum is over <ij>, then perhaps the author means the sum actually runs over ordered pairs, and they wrote <ij> loosely. With the 1/2, it becomes equivalent to a sum over unordered pairs.

In this case: H effectively = ε·(Nz/2)⟨n⟩² (for total energy). For a single site: h = εz⟨n⟩, giving ⟨n⟩ ≈ 0.848. (Interpretation A.)

Alternatively, maybe <ij> is unordered but the 1/2 is saying the pair interaction is ε/2 (for some physical reason). In that case h = (ε/2)z⟨n⟩, giving ⟨n⟩ ≈ 0.679. (Interpretation B.)

The problem says "Derive from the Hamiltonian H = (ε/2)Σ_{<ij>} n_i n_j - μΣ_i n_i, where the 1/2 avoids double-counting pairs." The most natural reading: Σ_{<ij>} runs over all ordered pairs (i,j) where i and j are neighbors, and the 1/2 compensates for counting each pair twice. This is Interpretation A.

Under this interpretation, H = (1/2) Σᵢ Σⱼ∈nn(i) ε·nᵢnⱼ - μΣnᵢ.

**I'll go with Interpretation A: ⟨n⟩ ≈ 0.848**

Actually, wait. Let me reconsider one more time. The problem says "the 1/2 avoids double-counting pairs." This most naturally means:

Without the 1/2, the sum Σ_{<ij>} nᵢnⱼ would count each pair twice. The 1/2 corrects this. So H = (ε/2) × [sum that counts each pair twice] = ε × [sum over true pairs].

The effective pair interaction is ε (not ε/2). For the mean-field equation, the effective field on site i is the derivative of H with respect to nᵢ:

∂H/∂nᵢ = (ε/2) × 2 × Σⱼ∈nn(i) ⟨nⱼ⟩ - μ = ε·z·⟨n⟩ - μ

(The factor 2 comes because nᵢ appears both as the "i" and "j" index in the double sum.)

So ⟨n⟩ = 1/(1 + exp(β(ε·z·⟨n⟩ - μ)))

And **⟨n⟩ ≈ 0.848**.

Let me solve to 3 decimal places:
⟨n⟩ = 1/(1 + exp(-1.90986⟨n⟩ - 0.1))

n = 0.848: arg = -1.90986·0.848 - 0.1 = -1.71956
exp(-1.71956) = 0.17905
RHS = 1/1.17905 = 0.84812

n = 0.8481: arg = -1.90986·0.8481 - 0.1 = -1.71975
exp(-1.71975) = 0.17901
RHS = 1/1.17901 = 0.84815

n ≈ 0.848

**Attempt 3 (confirmed): ⟨n⟩ = 0.848**

### Q8 Summary — REVISED

All three attempts, after careful derivation, agree:

| Q8 | ⟨n⟩ = 0.848 | ⟨n⟩ = 0.848 | ⟨n⟩ = 0.848 | **⟨n⟩ = 0.848** |

---

## Q9 [DISCRIMINATION]: Broadband CARS Microscopy

**Which is true about broadband CARS with a broadband pump?**
A. Only Stokes
B. Anti-Stokes but no separate vibrational info
C. Anti-Stokes with distinguishable info
D. None of above
E. Cannot generate anti-Stokes

### Attempt 1 — D2 Method

**CARS basics:** Coherent Anti-Stokes Raman Scattering uses pump (ωp), Stokes (ωS), and probe (ωpr) beams. The anti-Stokes signal is at ωAS = ωp - ωS + ωpr.

With broadband pump: many frequencies ωp available simultaneously.

**Test each option — assume correct and look for contradictions:**

**A. "Only Stokes"** — CARS by definition produces anti-Stokes signals (that's the "AS" in CARS). If we're doing CARS, we must get anti-Stokes. CONTRADICTION. ✗

**B. "Anti-Stokes but no separate vibrational info"** — The vibrational frequency is ωvib = ωp - ωS. With broadband pump (many ωp) and a specific Stokes frequency, many different vibrational modes are excited simultaneously. The anti-Stokes output is at ωAS = ωp - ωS + ωpr. If the pump is also the probe (as often in CARS, ωpr = ωp), then ωAS = 2ωp - ωS. With broadband pump, different pump frequencies give different ωAS, and each corresponds to a specific ωvib = ωp - ωS. So in principle, you CAN distinguish vibrational modes by looking at different anti-Stokes frequencies — each output frequency maps to a specific ωp, hence a specific ωvib.

Wait — but the KEY DETAIL says: "Consider whether the anti-Stokes signal has a one-to-one mapping between output frequency and vibrational mode."

With broadband pump and narrowband Stokes: ωAS = 2ωp - ωS. Each ωp gives a unique ωAS, and each ωp corresponds to ωvib = ωp - ωS. So there IS a one-to-one mapping. This means vibrational info IS distinguishable. CONTRADICTION with "no separate vibrational info." ✗

**C. "Anti-Stokes with distinguishable info"** — As analyzed above, broadband pump with narrowband Stokes gives a one-to-one mapping between ωAS and ωvib. The anti-Stokes spectrum directly encodes vibrational information. No contradiction found. ✓

Wait, but in typical broadband CARS, it's actually the STOKES that is broadband, not the pump. When the PUMP is broadband (unusual), the situation is different.

In standard broadband CARS: narrowband pump, broadband Stokes → different vibrational modes are excited, anti-Stokes spectrum maps directly to vibrational spectrum. This works well.

If instead the PUMP is broadband and Stokes is narrowband: ωvib = ωp - ωS varies with ωp. The anti-Stokes at ωAS = 2ωp - ωS. For a given ωAS, there's one ωp, hence one ωvib. So YES, distinguishable. Same conclusion.

But what if BOTH pump and Stokes are broadband? Or if there's only one broadband beam serving as both pump and Stokes? The problem says "broadband pump beam" — perhaps the pump does double duty.

In multiplex CARS with a single broadband source: ωAS = 2ωp - ωS where both ωp and ωS come from the broadband spectrum. Then many combinations of (ωp, ωS) can give the same ωAS, so the mapping is NOT one-to-one. This would mean vibrational info is mixed/convolved.

But the problem says "broadband pump" specifically, implying there's a separate Stokes beam (narrowband). In that case, there IS a one-to-one mapping.

Hmm, but re-reading: "Broadband CARS microscopy with broadband pump beam" — if the pump is broadband and there's a separate narrowband Stokes, then each ωvib is uniquely determined and distinguishable. This supports C.

But what if the "broadband pump" serves as BOTH pump and Stokes? Then every pair (ωp, ωS) from the broadband spectrum contributes, and a given anti-Stokes frequency ωAS = 2ωp - ωS has contributions from many (ωp, ωS) pairs with different ωvib. This would smear out vibrational information → supports B.

I need to think about what "broadband CARS with broadband pump" means physically. In typical broadband CARS, you use a narrowband pump/probe and broadband Stokes. If instead you use a broadband pump, you'd still need a Stokes beam. But if the broadband pump is the ONLY beam, the same beam acts as both pump and Stokes (and probe), and the mapping becomes many-to-one.

Given the problem's hint: "broadband pump means many pump frequencies simultaneously. Consider whether the anti-Stokes signal has a one-to-one mapping between output frequency and vibrational mode."

The hint is pointing at option B vs C. If there's a one-to-one mapping → C. If not → B.

With a broadband pump and separate narrowband Stokes: one-to-one → C.
With a broadband pump serving as both pump and Stokes: many-to-one → B.

In standard CARS, you need at least pump + Stokes. A broadband pump alone can serve as both (different spectral components acting as pump and Stokes). This is more physically realistic for "broadband CARS with broadband pump beam" — the broadband beam provides all needed frequencies.

In this case: ωAS = 2ωp - ωS where ωp and ωS are both from the broadband spectrum. For a given ωAS, many (ωp, ωS) combinations contribute. The vibrational information is convolved and NOT individually distinguishable from the anti-Stokes spectrum alone.

So B has no contradiction? Let me recheck: B says "Anti-Stokes but no separate vibrational info." If the broadband pump means the mapping is many-to-one, then yes, you get anti-Stokes signal but can't separately resolve individual vibrational modes.

Hmm, but actually in broadband CARS spectroscopy, you typically DO get spectrally resolved vibrational information, even with broadband pulses. The trick is that you use a narrowband probe (separate from the broadband pump/Stokes). In many implementations, the broadband beam serves as pump+Stokes, and a narrowband beam serves as probe:

ωAS = ωp - ωS + ωpr

With broadband (ωp - ωS) exciting many vibrational modes and narrowband ωpr:
For a given ωAS: ωp - ωS = ωAS - ωpr is fixed. So ωvib = ωAS - ωpr → one-to-one mapping. The anti-Stokes spectrum IS vibrationally resolved.

But the problem says only "broadband pump beam" — if there's no separate narrowband probe, and the broadband pump serves as both pump, Stokes, AND probe, then:
ωAS = 2ωp - ωS. Different (ωp, ωS) pairs with the same 2ωp - ωS give different ωvib = ωp - ωS. So one anti-Stokes frequency contains contributions from multiple vibrational modes → NOT resolvable.

I'll go with: B if only broadband beam (no narrowband probe), C if there's a narrowband probe.

The question says "broadband pump beam" (singular), suggesting perhaps only one beam. In that case → B.

But standard broadband CARS (also called multiplex CARS) uses a broadband Stokes + narrowband pump/probe and DOES give vibrational resolution. The scenario here (broadband pump, no mention of other beams) is non-standard.

Given the problem's emphasis on the one-to-one mapping issue and the "broadband pump" specification:

**Attempt 1: B (Anti-Stokes without separate vibrational info)**

### Attempt 2 — D2 Method (Fresh)

**CARS signal:** ωAS = ωp - ωS + ωpr, where ωvib = ωp - ωS.

In the broadband pump scenario, ωp spans a range.

**Testing each option:**

**A. Only Stokes** — CARS produces anti-Stokes by definition. CONTRADICTION. ✗

**E. Cannot generate anti-Stokes** — As long as phase matching is satisfied and there's a Stokes process, anti-Stokes is generated. With broadband pump, CARS still occurs. CONTRADICTION. ✗

**D. None of above** — Only valid if all A, B, C, E are wrong.

**C. Anti-Stokes with distinguishable vibrational info** — For this to be true, each anti-Stokes frequency must map to a unique vibrational mode. With broadband pump covering a range [ωp_min, ωp_max]:

If there's a separate narrowband Stokes at ωS:
- ωvib = ωp - ωS (varies with ωp)
- ωAS = 2ωp - ωS (if pump = probe)
- Each ωp → unique ωvib → unique ωAS. One-to-one. Distinguishable ✓

If the broadband beam serves as both pump and Stokes (no other beam):
- Pump: ωp, Stokes: ωS, both from broadband spectrum
- ωvib = ωp - ωS
- ωAS = ωp + ωvib = 2ωp - ωS (if pump = probe)
- For given ωAS = 2ωp - ωS: ωp = (ωAS + ωS)/2
  But ωS is also variable! So many (ωp, ωS) pairs give same ωAS with different ωvib.
- NOT one-to-one. NOT distinguishable. CONTRADICTION ✗ (if single beam)

**B. Anti-Stokes but no vibrational info** — Consistent with single broadband beam scenario (many-to-one mapping). No contradiction. ✓

If there's a narrowband Stokes, then B has a contradiction (info IS distinguishable). If single beam, B is consistent.

The problem says "broadband pump beam" — most naturally interpreted as a single broadband laser serving as the pump. In typical broadband CARS, you use broadband Stokes + narrowband pump. Here it's reversed or the broadband beam does everything.

Given the hint emphasizes the one-to-one mapping question, and the answer depends on whether there's a separate narrowband beam: the question seems designed to test understanding that a broadband pump (alone) doesn't give vibrational resolution.

**Attempt 2: B**

### Attempt 3 — D2 Method (Fresh)

Let me reconsider more carefully. The question says "broadband CARS microscopy with broadband pump beam." In broadband CARS microscopy:

Standard setup: narrowband pump/probe + broadband Stokes (from supercontinuum or OPO). This gives spectral resolution of vibrational modes in the anti-Stokes spectrum.

Non-standard: broadband pump + narrowband Stokes → also gives spectral resolution (just reversed roles).

The question specifically says "broadband pump" — and uses the term "broadband CARS" which is an established technique. In established broadband CARS, the broadband component is the Stokes beam, not the pump. If the pump is broadband instead, that's a different scenario.

But in practice, broadband CARS with a broadband pump and NO other beam would not work well — you need at least two color components. The broadband source provides both pump and Stokes frequencies from within its bandwidth.

For a single broadband beam doing everything (pump, Stokes, probe):
The nonlinear signal at ωAS involves integrating over all valid (ωp, ωS, ωpr) triplets satisfying energy conservation. The anti-Stokes spectrum is a convolution of the vibrational response with the spectral autocorrelation of the pump beam. Individual vibrational lines are NOT directly resolvable.

This supports B: anti-Stokes is generated but vibrational info is not separately distinguishable.

But let me check C one more time: Could there be a scenario where even with broadband pump, vibrational info IS distinguishable? If you use spectral interferometry or some other clever detection scheme, perhaps. But in standard detection (just measuring the anti-Stokes spectrum), NO.

**Attempt 3: B**

### Q9 Summary

| Q9 | B | B | B | **B** |

---

## Q10 [DISCRIMINATION]: Unlikely Effect of Coarsening Gas During Ceramic Sintering

Chloride impurity → trapped gas in pores → coarsening of gas bubbles.

### Attempt 1 — D2 Method

**For each option, assume it's the UNLIKELY one (i.e., assume it does NOT occur due to coarsening gas). Search for contradictions.**

Actually, D2 says to find the correct answer with zero contradictions. Here, the correct answer is the one that's UNLIKELY. So I should test: "Assume option X IS a real effect of coarsening gas. If I find contradictions, then X is unlikely."

**A. Higher heating rates → lower densities** — Higher heating rates can cause larger thermal gradients and faster gas generation, trapping more gas in closed pores, reducing final density. This IS consistent with coarsening gas effects. No contradiction as a real effect. ✓ (likely)

**B. De-densification under some atmospheres** — In atmospheres that are insoluble in the ceramic (e.g., N₂ or Ar), trapped gas cannot escape by diffusion through the solid. As temperature increases, gas pressure in pores increases, causing pore growth = de-densification. This IS a known effect. No contradiction. ✓ (likely)

**C. Large, RANDOMLY DISTRIBUTED voids** — The KEY DETAIL says to consider whether voids are spatially uniform or spatially graded. Coarsening gas effects arise from gas trapped in pores as they close during sintering. Pore closure occurs first in the interior (where diffusion distances to the surface are longest) and later near the surface. Therefore, gas trapping is more severe in the interior, leading to a spatially graded distribution (more voids in interior, fewer near surface), NOT randomly distributed voids. CONTRADICTION with "randomly distributed." ✗ (UNLIKELY)

**D. Larger grain sizes in interior than surface** — If gas-filled pores impede grain boundary motion less effectively than dense regions, grain growth in the interior (where pores are larger) could be more pronounced. Or, if the interior is at higher temperature during rapid heating, grains grow larger there. This is consistent with coarsening effects. ✓ (likely)

**E. Cracking** — Trapped gas at high pressure can cause internal stresses leading to cracking. Consistent. ✓ (likely)

**F. Higher green densities → lower sintered densities** — Higher green density means pores close earlier during sintering, trapping gas sooner. This trapped gas then prevents further densification or causes de-densification. Result: paradoxically lower sintered density. This IS a known effect with trapped gases. ✓ (likely)

**Attempt 1: C (large, randomly distributed voids is UNLIKELY)**

### Attempt 2 — D2 Method (Fresh)

**Test each as the UNLIKELY effect:**

**A. Higher heating rates → lower densities** — Faster heating = less time for gas to escape before pore closure. Known effect. Consistent. (likely)

**B. De-densification** — Gas expansion in closed pores at high temperature → pore growth. Established phenomenon. (likely)

**C. Large, randomly distributed voids** — Coarsening/Ostwald ripening of gas bubbles: large pores grow at the expense of small ones. This occurs preferentially in regions where pores are already closed and gas is trapped. Pore closure is NOT uniform — it depends on local geometry and distance from surface. The interior closes first, trapping gas earlier. Result: void distribution is GRADED (more/larger in interior), not random. "Randomly distributed" contradicts the expected spatial gradient. (UNLIKELY)

**D. Larger grains in interior** — Interior has more trapped gas → larger pores → pore-boundary separation → abnormal grain growth. OR: interior at higher temperature → more grain growth. Consistent with coarsening effects. (likely)

**E. Cracking** — Internal gas pressure → stress → cracking. Consistent. (likely)

**F. Higher green density → lower sintered density** — Known paradox: early pore closure traps gas. Consistent. (likely)

**Attempt 2: C**

### Attempt 3 — D2 Method (Fresh)

**Testing each option:**

**A** — Higher heating rate means less time for gas escape. Trapped gas opposes densification. Higher rate → lower density. Makes sense. Likely true.

**B** — Some atmospheres (N₂, Ar) trap in pores and are insoluble in ceramic. At high T, gas expands, pores regrow. De-densification is real. Likely true.

**C** — "Large, RANDOMLY distributed voids." The key word is "randomly." Gas trapping is systematic: it depends on when and where pores close, which correlates with microstructural position (distance from surface, local density). The resulting void distribution should be systematic/graded, NOT random. Furthermore, Ostwald ripening of gas bubbles leads to a characteristic size distribution (few large, many small), and the spatial distribution follows the sintering front. Random distribution would imply no spatial correlation, which contradicts the physics.

However, one could argue: if the chloride impurity is randomly distributed throughout the green body, the gas generation sites are random, leading to randomly distributed voids. But even then, the gas effects (trapping, coarsening) are most severe in regions where pores close first (interior), creating a gradient.

Overall, "randomly distributed" is the problematic descriptor. The voids may be large, but they won't be randomly distributed — they'll be concentrated in the interior. UNLIKELY as stated.

**D** — Interior grains see less drag from surfaces, more trapped gas weakens pinning. Larger grains in interior. Plausible and consistent.

**E** — Gas pressure → stress → cracking. Consistent.

**F** — Higher green density → earlier pore closure → more trapped gas → lower sintered density. Known effect.

**Attempt 3: C**

### Q10 Summary

| Q10 | C | C | C | **C** |

---

## Q11 [DISCRIMINATION]: All Possible Organic A-site Cations for 3D Lead Halide Perovskites (APbBr₃)

### Attempt 1 — D2 Method

**Options:**
A. Cs, MA, FA
B. Cs, MA, FA, Aziridinium (Az)
C. Cs, MA, FA, Ethylammonium (EA)
D. Cs, MA, FA, Methylhydrazinium (MHy)
E. Cs, MA, FA, Dimethylammonium (DMA)

**Goldschmidt tolerance factor requirement for 3D perovskites:** t ≈ 0.8–1.0

**Test each option — assume correct and look for contradictions:**

**A. Only Cs, MA, FA** — This implies no other cation can form a 3D perovskite with PbBr₃. But the KEY DETAIL states Aziridinium has t ≈ 0.95-0.98 and AZPbBr₃ was confirmed by Becker et al. 2018. If Az forms a 3D perovskite, then A is incomplete. CONTRADICTION. ✗

**B. Cs, MA, FA, Az** — Aziridinium ionic radius ~2.50 Å, t ~ 0.95-0.98. Confirmed experimentally (Becker et al. 2018). This set includes all known 3D perovskite-forming cations.
- Cs: t ≈ 0.86 ✓ (3D)
- MA: t ≈ 0.91 ✓ (3D)
- FA: t ≈ 0.99 ✓ (3D, but forms hexagonal at room T, cubic at high T)
- Az: t ≈ 0.95-0.98 ✓ (3D, confirmed)
Need to verify others can't also form 3D:
- EA (ethylammonium): r ~ 2.74 Å → t > 1.0 → not 3D (forms 2D/1D). No contradiction.
- DMA: r ~ 2.72 Å → t > 1.0 → not 3D. No contradiction.
- MHy: r ~ 2.64 Å → t ~ 1.01 → borderline. KEY DETAIL says "contested/borderline."

If MHy can also form 3D, then B would be incomplete. But the hint says MHy is "contested/borderline," suggesting it does NOT reliably form 3D perovskite. No clear contradiction for B. ✓

**C. Cs, MA, FA, EA** — EA has radius ~2.74 Å, t > 1.0 for PbBr₃. EA typically forms 2D perovskites, not 3D. CONTRADICTION (EA doesn't form 3D PbBr₃). Also, this list excludes Az which DOES form 3D. Double contradiction. ✗

**D. Cs, MA, FA, MHy** — MHy is contested/borderline for 3D formation. Some studies claim MHyPbBr₃ is 3D, others show it's actually a polar, non-perovskite phase. Even if MHy works, this list EXCLUDES Az, which is confirmed to form 3D. CONTRADICTION. ✗

**E. Cs, MA, FA, DMA** — DMA is too large (r ~ 2.72 Å, t > 1.0). DMA forms hexagonal/1D structures, not 3D perovskite. Also excludes Az. CONTRADICTION. ✗

**Attempt 1: B**

### Attempt 2 — D2 Method (Fresh)

**Key data points:**
- Cs⁺: r = 1.88 Å, t ≈ 0.86 → 3D perovskite ✓
- MA⁺ (methylammonium): r ≈ 2.17 Å, t ≈ 0.91 → 3D ✓
- FA⁺ (formamidinium): r ≈ 2.53 Å, t ≈ 0.99 → 3D (cubic phase) ✓
- Az⁺ (aziridinium): r ≈ 2.50 Å, t ≈ 0.95-0.98 → 3D ✓ (Becker et al. 2018)
- EA⁺ (ethylammonium): r ≈ 2.74 Å, t ≈ 1.04 → too large for 3D
- MHy⁺ (methylhydrazinium): r ≈ 2.64 Å, t ≈ 1.01 → borderline/contested
- DMA⁺ (dimethylammonium): r ≈ 2.72 Å, t ≈ 1.03 → too large for 3D

**Testing options:**

A: Excludes Az (confirmed 3D). CONTRADICTION. ✗
B: Includes Cs, MA, FA, Az. All confirmed 3D. Others (EA, MHy, DMA) have t > 1 or contested. No contradiction. ✓
C: Includes EA (t > 1, not 3D) and excludes Az (confirmed 3D). Double CONTRADICTION. ✗
D: Includes MHy (contested) and excludes Az (confirmed 3D). CONTRADICTION (missing Az). ✗
E: Includes DMA (t > 1, not 3D) and excludes Az. CONTRADICTION. ✗

**Attempt 2: B**

### Attempt 3 — D2 Method (Fresh)

**Test each option:**

**A** — Omits aziridinium, which has been experimentally demonstrated to form AZPbBr₃ as a 3D perovskite. CONTRADICTION. ✗

**B** — Aziridinium (Az): 3-membered ring amine, compact structure, ionic radius ~2.50 Å. Tolerance factor t = (r_A + r_X)/(√2(r_B + r_X)) where r_X = r_Br⁻ = 1.96 Å, r_B = r_Pb²⁺ = 1.19 Å.

t = (2.50 + 1.96)/(√2 × (1.19 + 1.96)) = 4.46/(1.414 × 3.15) = 4.46/4.455 = 1.001

Hmm, this gives t ≈ 1.00, which is at the upper edge. The KEY DETAIL says t ~ 0.95-0.98. The discrepancy might be due to different ionic radii used. With slightly different values (Shannon vs effective):

If r_Pb = 1.19 Å and r_Br = 1.96 Å: denominator = √2 × 3.15 = 4.455
For t = 0.95-0.98: r_A = t × 4.455 - 1.96 = 4.232 to 4.366 - 1.96 = 2.27 to 2.41 Å

So Az radius would need to be 2.27-2.41 Å for t = 0.95-0.98. The literature value of ~2.50 Å gives t ≈ 1.00.

Regardless, AZPbBr₃ has been experimentally confirmed as a 3D perovskite (Becker et al. 2018). Option B includes it.

The remaining question: does B capture ALL 3D-forming cations? MHy is contested — if it does form 3D, B would be incomplete. But the KEY DETAIL says MHy is "contested/borderline," implying it should NOT be included in a definitive list.

No contradiction for B. ✓

**C, D, E** — All either include a cation that doesn't form 3D or exclude Az that does. CONTRADICTION. ✗

**Attempt 3: B**

### Q11 Summary

| Q11 | B | B | B | **B** |

---

## FINAL SUMMARY TABLE

| Q | Attempt 1 | Attempt 2 | Attempt 3 | MAJORITY VOTE |
|---|-----------|-----------|-----------|---------------|
| Q7 | Z≈8.25, ⟨k⟩≈2.90 | Z≈6.46, ⟨k⟩≈2.87 | Z≈6.46, ⟨k⟩≈2.87 | **Z ≈ 6.5, ⟨k⟩ ≈ 2.9** |
| Q8 | ⟨n⟩ = 0.848 | ⟨n⟩ = 0.848 | ⟨n⟩ = 0.848 | **⟨n⟩ = 0.848** |
| Q9 | B | B | B | **B** |
| Q10 | C | C | C | **C** |
| Q11 | B | B | B | **B** |

### Notes

**Q7:** The problem is under-specified regarding maximum number of layers (k_max) and the exact role of coordination numbers z_lateral and z_inter. Results assume k_max = 5 and mean-field treatment where layer energies and coordination numbers modify the effective adsorption field. The partition function and mean coverage are sensitive to these assumptions.

**Q8:** All attempts converge after careful derivation from H = (ε/2)Σ_{<ij>} nᵢnⱼ - μΣ nᵢ. The 1/2 in the Hamiltonian avoids double-counting in the total energy but does NOT appear in the self-consistency equation for ⟨n⟩. The effective field on a single site is εz⟨n⟩ - μ (full ε, no 1/2). With ε = -k_BT/(2π), z = 12, μ = 0.1 k_BT: the self-consistency equation ⟨n⟩ = 1/(1 + exp(-(6/π)⟨n⟩ - 0.1)) yields ⟨n⟩ = 0.848.

**Q9:** Broadband pump means many pump frequencies simultaneously. When a single broadband beam acts as pump, Stokes, and probe, the anti-Stokes signal at a given frequency receives contributions from multiple vibrational modes (many-to-one mapping). Anti-Stokes is generated but vibrational information is not individually distinguishable.

**Q10:** Coarsening gas effects from chloride impurities produce spatially graded void distributions (concentrated in interior where pores close first), NOT randomly distributed voids. All other options are consistent with known coarsening gas phenomena.

**Q11:** Aziridinium (Az) has been experimentally confirmed to form 3D AZPbBr₃ perovskite (Becker et al. 2018, t ≈ 0.95-0.98). Other candidates (EA, MHy, DMA) have tolerance factors at or above 1.0, making 3D perovskite formation unlikely or contested. The complete list of A-site cations forming 3D lead bromide perovskites is Cs, MA, FA, and Aziridinium.
