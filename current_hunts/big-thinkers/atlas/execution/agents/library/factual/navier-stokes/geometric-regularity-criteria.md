---
topic: Geometric regularity criteria for NS via velocity-vorticity alignment
confidence: verified
date: 2026-03-30
source: "vasseur-pressure exploration-006"
---

## Finding

A family of conditional regularity results for 3D Navier-Stokes based on the smoothness of the vorticity or velocity direction field. These results show that regularity holds when the flow has sufficient geometric coherence — directly relevant to Beltrami-near flows where velocity and vorticity are aligned.

### Key Results

| Condition | Authors | Year | Controlled quantity |
|---|---|---|---|
| Lipschitz direction of omega | Constantin-Fefferman | 1993 | vorticity direction |
| Holder-1/2 direction of omega | Beirao da Veiga-Berselli | 2002 | vorticity direction |
| Integrability of single component | Chae-Lee | 2002 | vorticity/velocity component |
| Direction of velocity | Vasseur | 2007 | velocity direction |
| Localized vorticity coherence | Grujic-Guberovic | 2010 | local vorticity direction coherence |

### Constantin-Fefferman Mechanism

The vortex stretching term (omega . nabla)u can be written as |omega|^2 (xi . S . xi) where xi = omega/|omega| is the vorticity direction and S is the strain rate tensor. If xi varies slowly (Lipschitz or Holder-1/2), the amplification rate of |omega| is bounded, preventing blow-up.

### Beirao da Veiga-Berselli Improvement

Weakened to Holder-1/2: |xi(x) - xi(y)| <= C|x-y|^{1/2} in regions where |omega| > Omega_0. This is the best exponent known. Equivalently: if |nabla xi|^2 / (1 + log(1+|omega|)) is integrable in space-time, regularity holds.

### Beltrami Connection

For exact Beltrami flows (curl u = lambda u), the vorticity direction xi = u/|u| (the velocity direction). The Constantin-Fefferman and Vasseur criteria become identical — both reduce to smoothness of the velocity direction field. This links geometric regularity to Beltrami structure.
