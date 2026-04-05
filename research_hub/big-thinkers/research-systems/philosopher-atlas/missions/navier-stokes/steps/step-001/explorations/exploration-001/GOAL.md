# Exploration 001: CKN (1982) Proof Architecture

## Objective

Analyze the original Caffarelli-Kohn-Nirenberg (1982) proof of partial regularity for suitable weak solutions of the Navier-Stokes equations. Extract the structural features that determine the dimension bound on the singular set.

**Paper:** Caffarelli, Kohn, Nirenberg, "Partial regularity of suitable weak solutions of the Navier-Stokes equations," *Communications on Pure and Applied Mathematics*, 35(6):771-831, 1982.

Also consult Scheffer's earlier work (1976-1980) which established the first partial regularity results and introduced the dimensional reduction framework that CKN improved.

## What to Extract

For each item below, provide the **precise mathematical statement** from the paper, not just a verbal description. Include equation numbers or theorem numbers where possible.

### 1. Epsilon-Regularity Criterion
What scaled quantity must be small for regularity to follow? Write the precise inequality. What is the scaling of this quantity under parabolic rescaling (x → λx, t → λ²t)? Is the smallness threshold a universal constant or does it depend on parameters?

### 2. Covering Argument
How does the proof estimate the size of the singular set? Specifically:
- What geometric objects are used (parabolic cylinders Q_r, balls B_r, cubes)?
- What is the Vitali-type covering used?
- How does the dimension bound (Hausdorff dimension ≤ 1 in parabolic metric, equivalently ≤ 5/3 in Euclidean space-time) emerge from the covering?
- What is the precise role of parabolic scaling (space-time dimension 5 = 3 spatial + 2 temporal) in determining the dimension bound?

### 3. Localization Mechanism
How does the proof pass from global energy estimates to local regularity? Specifically:
- What cutoff functions are used?
- What terms arise from localizing the energy inequality?
- Are there "cross terms" or "error terms" from localization that must be controlled?
- How lossy is the localization step?

### 4. Critical Scaling Exponents
What powers of the radius r appear in the key estimates? For the central energy-type estimate, what is the scaling behavior? Write the key estimate schematically as:

  [local quantity at scale r] ≤ C · r^α · [global data] + ...

What is α? How does this α relate to the dimension bound on the singular set? Is this α sharp (saturated by known examples) or is there room?

### 5. Free-Parameter vs. Fixed-Constant Estimates
Which steps use Young's inequality with a free epsilon (ε-absorption, intentionally lossy) and which steps use estimates with optimal/fixed constants?
- List the Young/absorption steps and note the powers used
- For each, note whether the free epsilon is eventually chosen to optimize or just to close the estimate

## Success Criteria

A structured report containing:
- All five items above with precise mathematical content
- Clear identification of which step in the proof introduces the scaling that limits the singular set dimension to ≤ 1
- A clear statement of the proof's logical flow: [energy inequality] → [localization] → [epsilon-regularity] → [covering] → [dimension bound]

## Failure Criteria

- Giving only verbal/qualitative descriptions without mathematical content
- Failing to identify the specific step where the dimension bound originates
- Treating CKN as a monolithic result without decomposing the proof architecture

## Context

This is one of three parallel explorations. The other two analyze Lin (1998) and Vasseur (2007). The results will be compared to determine whether all three proof strategies converge on the same structural bottleneck or offer different routes. Your extraction must use the same 5-item template so results are directly comparable.

The dimension bound ≤ 1 (parabolic) for the singular set is the central qualitative result. The question driving this comparison is: does this bound arise from a universal feature of the Navier-Stokes energy structure, or from a proof-specific technique that could be improved?
