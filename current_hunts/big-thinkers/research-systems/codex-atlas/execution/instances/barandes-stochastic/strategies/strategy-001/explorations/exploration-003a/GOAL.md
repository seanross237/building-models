# Exploration 003a — Phase Freedom vs. Realm Selection: Computational Test (Math Explorer)

## Mission Context

We are investigating Barandes' indivisible stochastic dynamics reformulation of QM. Our prior explorations established:
- Barandes' framework is a Level 2 reformulation (re-expresses QM in stochastic language, no new predictions)
- Phase degrees of freedom are NOT determined by stochastic data (multiple Theta matrices for same Gamma)
- Consistent Histories (CH) has a structurally analogous problem: multiple consistent families for the same quantum system (realm selection problem)
- A potentially novel observation: these two non-uniqueness problems may be the same mathematical structure seen from different angles

## Your Task

For a qubit system (N=2), explicitly construct and compare:
1. The space of all valid Theta matrices consistent with a given transition kernel Gamma (Barandes' phase freedom)
2. The space of all consistent history families for the same quantum system (CH's realm selection)

Then determine if these spaces have the same dimension and structure.

## Stage 1: Construct the Phase Freedom Space (Barandes side)

### Setup
Consider a qubit (N=2) evolving under Hamiltonian H = (omega/2) sigma_z for time t.

The quantum evolution operator is U(t) = exp(-iHt/hbar). The transition kernel Gamma is defined by:
```
Gamma_ij(t) = |<i|U(t)|j>|^2
```
where |i>, |j> are computational basis states |0>, |1>.

**Concrete parameters:** Use omega = 1, hbar = 1, t = pi/4. This gives:
```
U = [[cos(pi/4), -i*sin(pi/4)], [-i*sin(pi/4), cos(pi/4)]]
Gamma = [[cos^2(pi/4), sin^2(pi/4)], [sin^2(pi/4), cos^2(pi/4)]] = [[1/2, 1/2], [1/2, 1/2]]
```

### Task
Find ALL matrices Theta such that:
1. |Theta_ij|^2 = Gamma_ij for all i,j (phase freedom)
2. Theta defines a valid quantum channel (the map rho -> Theta rho Theta^dagger is CPTP)

Characterize the space:
- How many free parameters (real dimensions)?
- What is the topology? (Torus? Manifold? Disconnected components?)
- What constraints does CPTP impose beyond |Theta_ij|^2 = Gamma_ij?

### Verification
- For each constructed Theta, verify |Theta_ij|^2 = Gamma_ij exactly
- Verify the resulting channel is CPTP (trace-preserving, completely positive)
- Check: when Gamma = identity (no evolution), the phase freedom space should reduce to diagonal phase matrices (pure gauges)

## Stage 2: Construct the Consistent History Families (CH side)

### Setup
Same qubit system: initial state rho_0 = |+><+| = (1/2)[[1,1],[1,1]], Hamiltonian H = (omega/2) sigma_z.

Consider 3-time histories: t_0 = 0, t_1 = pi/4, t_2 = pi/2.

A history family at time t_1 is a set of projection operators {P_alpha} that form a complete decomposition of identity: Sum_alpha P_alpha = I. For a qubit, each family is a choice of orthonormal basis.

### Task
Find ALL families of projectors {P_alpha(t_1)} such that the decoherence functional satisfies the consistency condition:
```
D(alpha, alpha') = Tr(P_{alpha_2}(t_2) P_{alpha_1}(t_1) rho_0 P_{alpha_1'}(t_1) P_{alpha_2'}(t_2)) = 0
for alpha != alpha'
```
where P(t) = U(t) P U(t)^dagger (Heisenberg picture).

Note: For 3-time histories, we need consistency for the full set of projection sequences at t_1 and t_2.

Characterize the space:
- How many free parameters?
- What is the topology?
- How does the space depend on the initial state rho_0?

### Verification
- For each consistent family, verify D(alpha,alpha) >= 0 and Sum_alpha D(alpha,alpha) = 1
- For each consistent family, verify D(alpha,alpha') = 0 for alpha != alpha' (or Re[D] = 0 for weak consistency)
- Check: for trivial evolution (H=0), the consistent families should be any basis (all bases consistent)

## Stage 3: Compare

After completing Stages 1 and 2:
1. **Dimension comparison:** Do both spaces have the same number of free real parameters?
2. **Structure comparison:** Do they have the same topology? Is there a natural map between them?
3. **Dependence comparison:** How does each space depend on the system parameters (H, t, rho_0)?

## Success Criteria
- Both spaces are explicitly constructed with all free parameters identified [COMPUTED]
- Dimensions of both spaces are determined [COMPUTED]
- A definitive answer: same dimension or different dimension [VERIFIED]
- If same: a candidate map between the spaces, or proof no map exists [COMPUTED or CONJECTURED]
- If different: structural explanation for the discrepancy [COMPUTED]

## Failure Criteria
- Only constructing one of the two spaces
- Not verifying CPTP constraints (Stage 1) or consistency conditions (Stage 2)
- Claiming dimensional equality/inequality without explicit construction
- Not running the trivial control checks (Gamma=identity, H=0)

## Output
Write REPORT.md and REPORT-SUMMARY.md in your exploration directory (current directory). Include all code in a code/ subdirectory. Tag every claim as [VERIFIED], [COMPUTED], [CHECKED], or [CONJECTURED].
