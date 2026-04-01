# Exploration 003: Vasseur (2007) Proof Architecture

## Objective

Analyze Alexis Vasseur's proof (2007) of partial regularity for Navier-Stokes using De Giorgi iteration. Extract the structural features that determine the dimension bound on the singular set, with particular attention to how Vasseur's approach differs from CKN (1982) and Lin (1998).

**Paper:** Alexis Vasseur, "A new proof of partial regularity of solutions to Navier-Stokes equations," *NoDEA: Nonlinear Differential Equations and Applications*, 14(5-6):753-785, 2007.

## What to Extract

For each item below, provide the **precise mathematical statement** from the paper, not just a verbal description. Include equation numbers or theorem numbers where possible.

### 1. Epsilon-Regularity Criterion
What scaled quantity must be small for regularity to follow? Write the precise inequality. Key questions:
- CKN and Lin use scaled energy quantities involving ∫|∇u|² and pressure terms over parabolic cylinders.
- Vasseur's De Giorgi approach works differently — what plays the role of the epsilon-regularity criterion?
- Is there a direct analogue, or does the De Giorgi iteration produce regularity through a fundamentally different mechanism?
- What is the scaling of Vasseur's criterion under parabolic rescaling?

### 2. Covering Argument
How does Vasseur estimate the size of the singular set? Key questions:
- Does Vasseur use the same Vitali covering / parabolic cylinder approach as CKN?
- Does the De Giorgi iteration change the geometry of the covering objects?
- Is the step from epsilon-regularity to the dimension-≤-1 bound the same as in CKN/Lin?

### 3. Localization Mechanism
This is the critical difference. De Giorgi iteration is a fundamentally different localization strategy:
- CKN uses cutoff functions; Lin uses compactness. What does De Giorgi iteration do instead?
- De Giorgi iteration works by controlling level sets of the solution on a decreasing sequence of domains. Describe this mechanism precisely.
- Does avoiding cutoff functions eliminate a source of loss present in CKN?
- What new estimates or inequalities does the De Giorgi approach require that CKN doesn't?
- Is the De Giorgi approach more or less lossy than CKN's cutoff approach?

### 4. Critical Scaling Exponents
What powers of the radius r appear in Vasseur's key estimates? Specifically:
- What scaling exponents appear in the De Giorgi iteration?
- Are these the same as CKN's scaling exponents?
- Does the De Giorgi approach produce the dimension ≤ 1 bound through the same scaling route as CKN, or through a genuinely different mechanism?
- What is the role of the parabolic metric dimension (5 = 3 + 2) in Vasseur's approach?

### 5. Free-Parameter vs. Fixed-Constant Estimates
- Does the De Giorgi iteration involve Young/absorption estimates with free epsilons?
- Where in the iteration does lossiness enter?
- Are the estimates in the De Giorgi approach "tighter" than CKN in any identifiable way?
- What is the role of Sobolev embedding in Vasseur vs. CKN — same exponents, different exponents?

## Success Criteria

A structured report containing:
- All five items above with precise mathematical content
- Clear identification of what the De Giorgi approach changes vs. what it preserves from the CKN framework
- An explicit assessment: does Vasseur's proof arrive at dimension ≤ 1 through the same scaling route as CKN, or through a different mechanism?
- Identification of any structural advantage (or disadvantage) of the De Giorgi approach for potential improvement beyond dimension ≤ 1

## Failure Criteria

- Treating Vasseur's proof as "just another proof of CKN" without extracting what the De Giorgi iteration specifically changes
- Failing to compare Vasseur's scaling exponents with CKN's
- Not addressing whether the De Giorgi approach offers a genuinely different path or converges on the same bottleneck

## Context

This is one of three parallel explorations. The other two analyze CKN (1982) and Lin (1998). The results will be compared to determine whether all three proof strategies converge on the same structural bottleneck or offer different routes. Your extraction must use the same 5-item template so results are directly comparable.

Vasseur's proof is the most structurally different of the three — it comes from the De Giorgi tradition in elliptic/parabolic regularity theory rather than the energy-estimate tradition. If any of the three proofs might avoid a constraint the others hit, Vasseur is the most likely candidate. The question is whether this structural difference changes the dimension bound on the singular set, or whether the parabolic scaling of Navier-Stokes forces all approaches through the same bottleneck.
