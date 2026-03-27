# Adversarial Logic System — Experiment Configuration

## Parameters (toggleable per run)

| Parameter | Options | Description |
|-----------|---------|-------------|
| judge | yes / no | Whether a 3rd-party judge evaluates the adversary's attacks before sending to architect |
| format | structured / prose | Structured logical notation (premises → conclusions) vs. free prose |
| attack_taxonomy | yes / no | Whether adversary uses a fixed taxonomy of attack types |
| exploration_phase | yes / no | Whether architect first plans and researches before theorizing |

## Agent Roles

### Architect
Proposes and refines the theory. Produces structured arguments with explicit premises and logical steps.

### Adversary
Attacks the theory. Looks for any weakness: logical, empirical, conceptual.

### Judge
Evaluates each attack. Determines what landed, severity, and what the architect must address.
