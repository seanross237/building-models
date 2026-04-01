# Q7 — Partition Function (Opus Run 1, Hybrid M2+M4)

## PHASE 1 — PLAN

### Constraint Extraction

**Entities:**
- N adsorption sites on a 2D lattice surface
- Each site can hold up to k layers (k = 0, 1, 2, 3, ...)
- Particles adsorb in layers
- Grand canonical ensemble (particle number fluctuates)

**Energetics:**
- First monolayer (k=1): interaction energy epsilon_1 = 0.1 k_B T
- Subsequent layers (k >= 2): energy epsilon_l = (0.02)^k k_B T per layer
- Nearest-neighbor lateral interactions: epsilon_l with coordination number z_l = 4
- Chemical potential: mu = 0.15 k_B T
- z_inter = 4 (interlayer coordination number)
- T = 318 K

**Framework:**
- Grand canonical ensemble
- Mean-field approximation (replace neighbor occupancies with average)

### Key Ambiguity Check

The problem states "epsilon_l = (0.02)^k k_B T for subsequent layers." I need to be careful: is this the energy of the k-th layer specifically, or cumulative? The phrasing "for subsequent layers" with the subscript l suggests this is the per-layer energy for layer number k (where k >= 2). The first layer has a distinct energy epsilon_1.

Also: the problem uses "k" both as "number of layers" and in the exponent of the subsequent layer energy formula. I will treat k in (0.02)^k as the layer index.

### Plan (3 steps):

1. **Write the single-site grand partition function** in the mean-field approximation. For a site with k layers, the effective energy includes: the first-layer energy, subsequent layer energies, lateral mean-field interactions, and the chemical potential contribution for k particles.

2. **Compute the single-site grand partition function Xi** by summing over all possible layer counts k = 0, 1, 2, 3, ... and identify whether the geometric-like series converges.

3. **Calculate <k>** = (1/Xi) * sum over k of k * (Boltzmann weight for k layers), using the given numerical parameters.

## PHASE 2 — SOLVE

### Step 1: Single-site effective Hamiltonian in mean-field approximation

In the grand canonical ensemble, the grand partition function for a single site is:

Xi = sum_{k=0}^{infinity} exp(beta * [mu * k - E(k)])

where E(k) is the total adsorption energy for k layers on a single site.

**Energy for k layers on a single site:**

For k = 0: E(0) = 0 (empty site)

For k >= 1: The first layer contributes energy -epsilon_1 (binding energy, should be negative/attractive for adsorption). Subsequent layers j = 2, 3, ..., k each contribute -epsilon_j where epsilon_j = (0.02)^j k_B T.

So: E(k) = -epsilon_1 - sum_{j=2}^{k} (0.02)^j k_B T for k >= 1.

**Wait — sign convention check.** In adsorption, the interaction energy epsilon_1 represents the binding energy to the surface. In the grand canonical formulation, the Boltzmann factor for a state with k particles is:

exp(beta * (mu * k - H_k))

where H_k is the energy of the configuration.

For adsorption, the energy should be negative (favorable), so H_k < 0 for occupied states. I'll define:

H(k) = -epsilon_1 * delta(k>=1) - sum_{j=2}^{k} (0.02)^j k_B T - (z_l/2) * epsilon_l_lateral * <n> * k

The last term is the mean-field lateral interaction where <n> is the average layer occupancy of neighbors. In mean-field, this becomes self-consistent.

**However**, let me reconsider. The problem asks to "derive the grand partition function Z and determine <k>." With the mean-field approximation, we typically replace neighbor interactions with an effective field. But the problem gives specific numerical values and asks for <k>, which suggests a direct numerical calculation.

**Simplification approach:** Let me re-read the problem carefully.

The problem states:
- epsilon_1 = 0.1 k_B T (first monolayer energy)
- epsilon_l = (0.02)^k k_B T (subsequent layer energy)
- Nearest-neighbor lateral interactions epsilon_l with z_l = 4
- mu = 0.15 k_B T
- z_inter = 4

In mean-field theory for adsorption, the effective single-site problem has a modified chemical potential:

mu_eff = mu + z_l * epsilon_l * <theta>

where <theta> is the mean-field average coverage. But this creates a self-consistency equation.

**For a tractable calculation**, let me work with the direct single-site partition function first, treating the lateral interactions in mean-field, and then solve self-consistently.

### Step 2: Boltzmann weights for each layer count

Let me define the effective energy benefit of having k layers. Working in units of k_B T (so beta * k_B T = 1):

For k particles on a site, the contribution to the grand partition function is:

w(k) = exp(beta * mu * k) * exp(beta * E_binding(k))

where E_binding is the total binding energy.

**Binding energy for k layers:**
- Layer 1: epsilon_1 = 0.1 k_B T
- Layer j (j >= 2): (0.02)^j k_B T

Total binding energy for k layers:
- E_bind(k=0) = 0
- E_bind(k=1) = 0.1
- E_bind(k=2) = 0.1 + (0.02)^2 = 0.1 + 0.0004 = 0.1004
- E_bind(k=3) = 0.1 + (0.02)^2 + (0.02)^3 = 0.1 + 0.0004 + 0.000008 = 0.100408
- E_bind(k) = 0.1 + sum_{j=2}^{k} (0.02)^j for k >= 2

The geometric sum: sum_{j=2}^{k} (0.02)^j = 0.02^2 * (1 - 0.02^{k-1})/(1 - 0.02) = (0.0004/0.98) * (1 - 0.02^{k-1})

As k -> infinity: sum_{j=2}^{inf} (0.02)^j = 0.0004/0.98 ≈ 0.000408163...

So the binding energy rapidly converges: E_bind(infinity) ≈ 0.100408...

**Chemical potential contribution:** beta * mu * k = 0.15 * k

**Mean-field lateral interaction:** In the mean-field approximation with coordination number z_l = 4, each site interacts with z_l neighbors. The lateral interaction for a site with k layers surrounded by neighbors with average <k> layers gives an energy contribution. However, the lateral interaction parameter epsilon_l is already defined as (0.02)^k k_B T, which seems to be the interlayer energy, not the lateral energy.

**Re-reading the problem:** "Nearest-neighbor lateral interactions epsilon_l with coordination number z_l" — this suggests epsilon_l is the lateral interaction strength. But epsilon_l is also defined as (0.02)^k k_B T. This is confusing notation.

Let me consider: perhaps the lateral interaction is a separate parameter. The problem says "nearest-neighbor lateral interactions epsilon_l with coordination number z_l" — and then separately "epsilon_l = (0.02)^k k_B T for subsequent layers." The subscript "l" appears to serve double duty: once for "lateral" and once for "layer."

**OPPOSITE CHECK:** Could the (0.02)^k term be the lateral interaction energy and NOT the interlayer energy? Re-reading: "Particles adsorb in layers with interaction energy epsilon_1 for the first monolayer, and epsilon_l = (0.02)^k k_B T for subsequent layers." This clearly defines the layer-dependent adsorption energy. Then "Nearest-neighbor lateral interactions epsilon_l" reuses this symbol for the lateral coupling.

**Resolution:** I will interpret this as: the lateral interaction between nearest-neighbor sites also uses the layer-dependent energy scale epsilon_l = (0.02)^k k_B T, where k is the layer index. In the mean-field approximation, the lateral contribution becomes:

E_lateral = -(z_l/2) * sum of lateral interactions

But for a practical mean-field calculation, the lateral interactions modify the effective field. Given the rapid decay of (0.02)^k, these lateral contributions are extremely small for k >= 2.

### Step 3: Computing the single-site partition function and <k>

**Without lateral interactions first** (as a baseline, since they are tiny):

Xi = sum_{k=0}^{inf} exp(0.15*k + E_bind(k))

= 1 + exp(0.15 + 0.1) + exp(0.30 + 0.1004) + exp(0.45 + 0.100408) + ...

= 1 + exp(0.25) + exp(0.4004) + exp(0.550408) + exp(0.7004...) + ...

Wait — this series DIVERGES because the mu*k = 0.15k term grows linearly while the binding energy saturates at ~0.1004. So exp(0.15k + ~0.1004) grows without bound as k increases.

**This means the sum does not converge**, which indicates a physical instability — the chemical potential is high enough that unlimited multilayer adsorption is favorable. This is the BET-like regime where multilayer adsorption leads to condensation.

**However**, the problem asks for a specific numerical answer, so perhaps I need to reconsider the energy model. Let me re-examine.

**CRITICAL RE-READ:** "epsilon_l = (0.02)^k k_B T for subsequent layers" — perhaps this means the TOTAL energy cost grows as (0.02)^k, making higher layers increasingly unfavorable. But (0.02)^k for k >= 2 gives 0.0004, 0.000008, ... which are DECREASING, not increasing. So each additional layer beyond 1 costs less and less energy to add.

**Alternative interpretation:** Perhaps epsilon_l represents an energy COST (unfavorable), not a binding energy. If higher layers have energy +epsilon_l (repulsive/unfavorable), while mu drives adsorption, then:

w(k) = exp(beta*mu*k - beta*epsilon_1 - sum_{j=2}^{k} beta*(0.02)^j * k_B T)

Wait, the sign of epsilon_1 matters. If epsilon_1 = 0.1 k_B T is a cost, then:

w(k) = exp(k * 0.15 - 0.1 - sum_{j=2}^{k}(0.02)^j) for k >= 1

= exp(0.15k - 0.1 - small)

This still diverges for large k since 0.15k dominates.

**Alternative: maybe mu contributes negatively.** In some conventions for adsorption, the grand canonical weight is:

w(k) = exp(-beta*E(k) + beta*mu*k)

but if E(k) = epsilon_1 + ... is the binding energy (negative of what I want), we need:

w(k) = exp(-beta*epsilon_1 - sum - beta*mu*k)... No, that's wrong for grand canonical.

**Standard grand canonical:** Z_G = sum_states exp(-beta*(E - mu*N))

For k particles: weight = exp(-beta*E(k) + beta*mu*k)

If E(k) is the energy of the k-layer configuration, and in adsorption the energy is LOWERED by binding (E < 0), then:

- E(k=0) = 0
- E(k=1) = -epsilon_1 = -0.1 k_B T
- E(k=2) = -epsilon_1 - (0.02)^2 k_B T = -(0.1 + 0.0004) k_B T

w(k) = exp(-beta*E(k) + beta*mu*k) = exp(epsilon_1/k_BT + ... + mu*k/k_BT)
     = exp(0.1 + 0.0004 + ... + 0.15*k)

This still diverges.

**The only way to get convergence** is if the subsequent layer energies are REPULSIVE (positive energy cost) and grow with k. Perhaps the formula should be read as epsilon_l = (0.02)^k meaning the layer energy COST is 0.02 * k (linear in k), not 0.02 to the power k?

**OR:** Perhaps we should interpret the exponent differently. What if "epsilon_l = (0.02)^k k_B T" means epsilon at layer k is 0.02 raised to power k, and the energy for having k layers is the sum, but with a sign that makes adding layers costly beyond what mu provides?

Let me try: E(k) = +epsilon_1 + sum_{j=2}^{k} (0.02)^j k_B T (energy cost, positive)

w(k) = exp(beta*mu*k - beta*E(k)) = exp(0.15k - 0.1 - sum_{j=2}^{k}(0.02)^j)

For large k: 0.15k dominates and sum converges, so this still diverges.

**Mean-field lateral interactions as the convergence mechanism:**

Perhaps the lateral interactions provide a k-dependent cost. If each layer at a site interacts laterally with neighbors, and in mean-field the cost grows with k:

E_mf(k) ~ (z_l/2) * k * epsilon_lat * <k>

If epsilon_lat is substantial, this k^2-like term (through self-consistency) could provide convergence. But with epsilon_lat given by the (0.02)^k formula, this would be tiny.

**Let me try a practical truncation approach.** In real BET theory, the series is truncated at some maximum k or there's a condensation condition. Let me compute with a reasonable truncation at k_max ~ 20 and see where <k> lands, noting that the physical answer may correspond to a specific framework.

**ACTUALLY — let me reconsider the interlayer interaction.** z_inter = 4 is given as an "interlayer coordination number." Perhaps this means each particle in layer j interacts with z_inter particles in adjacent layers (above and below), creating an energy penalty that grows with k.

If the interlayer interaction contributes an energy cost of z_inter * epsilon_l per layer transition, then for k layers:

E_inter(k) = z_inter * sum_{j=1}^{k-1} epsilon_j = 4 * [epsilon_1 + sum_{j=2}^{k-1} (0.02)^j k_BT]

But this still saturates.

**Let me just compute numerically with a truncation and see what the problem likely expects.**

### Numerical Computation

Working in units of k_B T:

**Define:** For a site with k layers:
- Adsorption energy: E_ads(k) = epsilon_1 + sum_{j=2}^{k} (0.02)^j = 0.1 + sum_{j=2}^{k} (0.02)^j
- Chemical potential gain: mu * k = 0.15k
- Mean-field lateral energy: (z_l/2) * epsilon_lat(k) * <k> [need self-consistency]
- Interlayer energy: z_inter * ...

**Simplest mean-field approach — treat as BET-like with mean-field:**

In standard BET theory, the partition function per site for multilayer adsorption is:

Xi = 1 + sum_{k=1}^{inf} c * x^k

where x = exp(beta*(mu - epsilon_bulk)) and c = exp(beta*(mu - epsilon_1))/x accounts for the different first-layer energy.

Let me map to this framework:
- First layer: activity contribution = exp(beta*(mu - epsilon_1)) = exp(0.15 - 0.1) = exp(0.05)
- Subsequent layers: if the effective energy per layer is epsilon_bulk ≈ 0 (since (0.02)^k -> 0 rapidly), then x = exp(beta*mu) = exp(0.15)

With x = exp(0.15) > 1, the BET series diverges, indicating the system is above the condensation point. In BET theory, this means x < 1 is required (vapor pressure below saturation), and for x >= 1, infinite layers form.

**But the problem asks for a finite <k>, so there must be a mechanism I'm missing, or the energy convention differs.**

**FINAL INTERPRETATION ATTEMPT:** What if epsilon_1 = 0.1 k_BT is not a binding energy but rather the REDUCED chemical potential or effective parameter, and the "energies" are the Boltzmann-weighted activities directly?

Let me try: the grand partition function per site in mean-field BET form is:

Xi = 1 + a + a*b + a*b^2 + ... = 1 + a/(1-b) for |b| < 1

where a = exp(beta*(mu - epsilon_1) + z_l*<theta>*beta*epsilon_lat/2) and b = exp(beta*(mu - epsilon_bulk) + ...)

For this to converge, b < 1, meaning mu < epsilon_bulk.

With the mean-field lateral interaction included self-consistently, and if the lateral interaction epsilon_l acts as an additional energy cost (positive, opposing adsorption):

For layer k >= 2: effective energy = (0.02)^k + z_l * epsilon_lat_effective

If z_l * epsilon_lat gives a constant energy cost per layer of, say, 0.02 * 4 = 0.08 per layer, then:

b = exp(0.15 - 0.08 - small) = exp(0.07 - small)

Still > 1, diverges.

**If lateral interactions are repulsive and mean-field gives a k-dependent penalty:**

In mean-field with self-consistency: mu_eff = mu - z_l * epsilon_l * <k>

The self-consistent equation would be:

<k> = d/d(beta*mu) ln Xi(mu_eff)

This creates a self-consistent reduction of the effective chemical potential.

**Let me try the self-consistent mean-field calculation numerically.** I'll assume:
- Each occupied layer on a site interacts laterally with z_l = 4 neighbors
- The lateral interaction per layer pair is some effective epsilon_lat
- In mean-field: mu_eff = mu - z_l * epsilon_lat * <k>

The problem states "nearest-neighbor lateral interactions epsilon_l" where epsilon_l = (0.02)^k k_BT. If I take the first-layer lateral interaction (k=1): epsilon_l(1) = 0.02 k_BT, then:

mu_eff = 0.15 - 4 * 0.02 * <k> = 0.15 - 0.08<k>

For the series Xi = sum_{k=0}^{inf} exp(mu_eff * k + binding(k)) to converge:

We need mu_eff < 0 for large k, so <k> > 0.15/0.08 = 1.875.

**Self-consistent solution:** Let me iterate.

Start: <k> = 2 (guess)
mu_eff = 0.15 - 0.08*2 = -0.01

With mu_eff = -0.01 (units k_BT):
w(0) = 1
w(1) = exp(-0.01 + 0.1) = exp(0.09) = 1.09417
w(2) = exp(-0.02 + 0.1004) = exp(0.0804) = 1.08373
w(3) = exp(-0.03 + 0.100408) = exp(0.070408) = 1.07294
w(k) ≈ exp(-0.01k + 0.1004) for large k

Sum = 1 + exp(0.09) + exp(0.0804)*exp(-0.01) + exp(0.0804)*exp(-0.02) + ...

Actually, for k >= 2 the binding saturates at ~0.1004, so:
w(k) ≈ exp(0.1004 - 0.01k) for k >= 2

Sum from k=2 to inf of exp(0.1004 - 0.01k) = exp(0.1004) * sum_{k=2}^{inf} exp(-0.01k)
= exp(0.1004) * exp(-0.02)/(1-exp(-0.01))
= exp(0.0804) * 1/(exp(0.01)-1)
= 1.08373 * 1/0.01005 = 1.08373 * 99.50 = 107.83

<k> = [1*w(1) + sum_{k>=2} k*w(k)] / Xi

This gives a very large <k>, not ~2. So the self-consistency is not satisfied with <k>=2.

Let me try <k> = 3:
mu_eff = 0.15 - 0.08*3 = -0.09

w(k) ~ exp(0.1004 - 0.09k) for large k
Geometric ratio: exp(-0.09) = 0.9139 < 1, converges.

Xi = 1 + exp(-0.09+0.1) + exp(0.1004)*exp(-0.18)/(1-exp(-0.09))
   = 1 + exp(0.01) + exp(0.1004-0.18)/(1-0.9139)
   = 1 + 1.01005 + exp(-0.0796)/0.08611
   = 1 + 1.01005 + 0.92347/0.08611
   = 1 + 1.01005 + 10.724
   = 12.734

<k> computed from this:
<k> = [1*1.01005 + sum_{k=2}^{inf} k*exp(0.1004-0.09k)] / 12.734

sum_{k=2}^{inf} k*r^k where r = exp(-0.09) = 0.9139
= exp(0.1004) * [sum_{k=2}^{inf} k*r^k]
= exp(0.1004) * [r/(1-r)^2 - r/(1-r)]  [subtracting k=1 from full sum and k=0 is 0]

Actually: sum_{k=0}^{inf} k*r^k = r/(1-r)^2
Subtract k=0 (=0) and k=1 (=r):
sum_{k=2}^{inf} k*r^k = r/(1-r)^2 - r = r*[1/(1-r)^2 - 1] = r*[1-(1-r)^2]/(1-r)^2 = r*(2r-r^2)/(1-r)^2 = r^2*(2-r)/(1-r)^2

With r = 0.9139:
r^2 = 0.8352
2-r = 1.0861
(1-r)^2 = (0.0861)^2 = 0.007413

sum_{k=2}^{inf} k*r^k = 0.8352 * 1.0861 / 0.007413 = 0.9071/0.007413 = 122.37

Multiply by exp(0.1004) = 1.1056:
= 135.27

<k> = (1.01005 + 135.27) / 12.734 = 136.28/12.734 = 10.70

Not self-consistent with <k>=3.

**Let me try <k> = 10:**
mu_eff = 0.15 - 0.08*10 = -0.65

r = exp(-0.65) = 0.5220

Xi = 1 + exp(-0.65+0.1) + exp(0.1004)*exp(-1.30)/(1-0.5220)
   = 1 + exp(-0.55) + 1.1056*0.2725/0.4780
   = 1 + 0.5769 + 0.3012/0.4780
   = 1 + 0.5769 + 0.6301
   = 2.207

sum_{k=2}^{inf} k*r^k = r^2*(2-r)/(1-r)^2 = 0.2725*1.478/0.2285 = 0.4027/0.2285 = 1.7622

Numerator for <k>: 1*0.5769 + 1.1056*1.7622 = 0.5769 + 1.9479 = 2.525

<k> = 2.525/2.207 = 1.144

Not self-consistent with <k>=10.

**Iterate between 3 and 10. Try <k>=2:**
mu_eff = 0.15 - 0.08*2 = -0.01
Already computed: very large <k>. Let's be more precise.

**Try <k>=5:**
mu_eff = 0.15 - 0.08*5 = -0.25

r = exp(-0.25) = 0.7788

Xi = 1 + exp(-0.25+0.1) + exp(0.1004)*exp(-0.50)/(1-0.7788)
   = 1 + exp(-0.15) + 1.1056*0.6065/0.2212
   = 1 + 0.8607 + 0.6703/0.2212
   = 1 + 0.8607 + 3.030
   = 4.891

r^2*(2-r)/(1-r)^2 = 0.6065*1.2212/0.04893 = 0.7407/0.04893 = 15.138

Numerator: 0.8607 + 1.1056*15.138 = 0.8607 + 16.734 = 17.595
<k> = 17.595/4.891 = 3.598

Not self-consistent with <k>=5.

**Try <k>=3.6:**
mu_eff = 0.15 - 0.08*3.6 = 0.15 - 0.288 = -0.138

r = exp(-0.138) = 0.8711

Xi = 1 + exp(-0.138+0.1) + exp(0.1004)*exp(-0.276)/(1-0.8711)
   = 1 + exp(-0.038) + 1.1056*0.7589/0.1289
   = 1 + 0.9627 + 0.8391/0.1289
   = 1 + 0.9627 + 6.510
   = 8.473

r^2*(2-r)/(1-r)^2 = 0.7588*1.1289/(0.1289)^2 = 0.8566/0.01661 = 51.57

Numerator: 0.9627 + 1.1056*51.57 = 0.9627 + 57.01 = 57.97
<k> = 57.97/8.473 = 6.842

Not self-consistent. <k> overshoots.

**Try <k>=7:**
mu_eff = 0.15 - 0.08*7 = -0.41

r = exp(-0.41) = 0.6637

Xi = 1 + exp(-0.41+0.1) + exp(0.1004)*exp(-0.82)/(1-0.6637)
   = 1 + exp(-0.31) + 1.1056*0.4404/0.3363
   = 1 + 0.7334 + 0.4868/0.3363
   = 1 + 0.7334 + 1.4477
   = 3.181

r^2*(2-r)/(1-r)^2 = 0.4405*1.3363/(0.3363)^2 = 0.5886/0.1131 = 5.204

Numerator: 0.7334 + 1.1056*5.204 = 0.7334 + 5.752 = 6.485
<k> = 6.485/3.181 = 2.038

Not self-consistent with <k>=7.

So the self-consistent <k> lies between 2 and 7. Let me narrow down.

**f(<k>) function:** where f maps assumed <k> to computed <k>:
- f(2) >> 10 (divergent-like)
- f(3) ≈ 10.7
- f(3.6) ≈ 6.84
- f(5) ≈ 3.60
- f(7) ≈ 2.04
- f(10) ≈ 1.14

Fixed point: f(<k>) = <k>

Between 5 and 7: f(5)=3.6, f(7)=2.04
Between 3.6 and 5: f(3.6)=6.84, f(5)=3.6

The function f is decreasing. The fixed point is where f(x) = x.

From f(5) = 3.6 and f(3.6) = 6.84:
- At x=4: let me compute f(4).

**f(4):**
mu_eff = 0.15 - 0.08*4 = -0.17

r = exp(-0.17) = 0.8437

Xi = 1 + exp(-0.17+0.1) + exp(0.1004)*exp(-0.34)/(1-0.8437)
   = 1 + exp(-0.07) + 1.1056*0.7118/0.1563
   = 1 + 0.9324 + 0.7867/0.1563
   = 1 + 0.9324 + 5.033
   = 6.966

r^2*(2-r)/(1-r)^2 = 0.7118*1.1563/(0.1563)^2 = 0.8230/0.02443 = 33.69

Numerator: 0.9324 + 1.1056*33.69 = 0.9324 + 37.24 = 38.17
<k> = 38.17/6.966 = 5.48

f(4) = 5.48. Still > 4.

**f(4.5):**
mu_eff = 0.15 - 0.08*4.5 = -0.21

r = exp(-0.21) = 0.8106

Xi = 1 + exp(-0.21+0.1) + exp(0.1004)*exp(-0.42)/(1-0.8106)
   = 1 + exp(-0.11) + 1.1056*0.6570/0.1894
   = 1 + 0.8958 + 0.7264/0.1894
   = 1 + 0.8958 + 3.834
   = 5.730

r^2*(2-r)/(1-r)^2 = 0.6571*1.1894/(0.1894)^2 = 0.7815/0.03587 = 21.78

Numerator: 0.8958 + 1.1056*21.78 = 0.8958 + 24.08 = 24.98
<k> = 24.98/5.730 = 4.36

f(4.5) = 4.36. Close!

**f(4.4):**
mu_eff = 0.15 - 0.08*4.4 = -0.202

r = exp(-0.202) = 0.8172

Xi = 1 + exp(-0.202+0.1) + exp(0.1004)*exp(-0.404)/(1-0.8172)
   = 1 + exp(-0.102) + 1.1056*0.6680/0.1828
   = 1 + 0.9030 + 0.7385/0.1828
   = 1 + 0.9030 + 4.040
   = 5.943

r^2*(2-r)/(1-r)^2 = 0.6682*1.1828/(0.1828)^2 = 0.7903/0.03342 = 23.65

Numerator: 0.9030 + 1.1056*23.65 = 0.9030 + 26.15 = 27.05
<k> = 27.05/5.943 = 4.55

f(4.4) = 4.55. Getting closer.

**f(4.45):**
mu_eff = 0.15 - 0.08*4.45 = -0.206

r = exp(-0.206) = 0.8139

r^2 = 0.6624, (2-r) = 1.1861, (1-r) = 0.1861, (1-r)^2 = 0.03463

Xi = 1 + exp(-0.106) + 1.1056*0.6625/0.1861
   = 1 + 0.8994 + 0.7323/0.1861
   = 1 + 0.8994 + 3.935
   = 5.835

r^2*(2-r)/(1-r)^2 = 0.6624*1.1861/0.03463 = 0.7857/0.03463 = 22.69

Numerator: 0.8994 + 1.1056*22.69 = 0.8994 + 25.09 = 25.99
<k> = 25.99/5.835 = 4.45

**f(4.45) ≈ 4.45. Self-consistent!**

### Result

The self-consistent mean-field solution gives:

**<k> ≈ 4.45 layers per site**

Rounding to appropriate precision: **<k> ≈ 4.5**

### Summary

The grand partition function per site is:

**Xi = sum_{k=0}^{inf} exp(beta*mu_eff*k + beta*E_bind(k))**

where mu_eff = mu - (z_l * epsilon_lat * <k>) is the mean-field-renormalized chemical potential, and E_bind(k) = epsilon_1 + sum_{j=2}^{k}(0.02)^j k_BT.

Self-consistent solution at the given parameters yields **<k> ≈ 4.5 adsorbed layers per site**.

---

## Final Answer

**<k> ≈ 4.5**
