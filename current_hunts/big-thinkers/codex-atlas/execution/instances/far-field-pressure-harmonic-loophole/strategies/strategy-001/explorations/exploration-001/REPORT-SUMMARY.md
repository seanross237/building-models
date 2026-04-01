# Exploration 001 Summary: Reconstruct the Exact Far-Field Pressure Obstruction

- Goal: reconstruct, in equations, the exact pressure obstruction behind the mission's far-field harmonic loophole and isolate the statement needed for the Tao filter.
- What I tried: reconciled Vasseur's actual pressure decomposition with the later H^1/far-field framing, using the local library notes and the prior Vasseur strategy reports.
- Outcome: succeeded.
- Key takeaway: the literal `beta = 4/3` bottleneck in Vasseur is the **local non-divergence term `P_{k21}`**, while the mission's loophole language is about an **alternative harmonic far-field split**. The real question for the next exploration is whether such a harmonic far-field decomposition can absorb the dangerous contribution that Vasseur isolates as local.
- Exact obstruction recovered:  
  `I_k ≤ ||P_{k21}||_{L^q} ||d_k||_{L^2} ||1_{v_k>0}||_{L^{2q/(q-2)}}` with  
  `||P_{k21}||_{L^q} ≤ C_q`, `||d_k||_{L^2} ≤ U_{k-1}^{1/2}`, and `||1_{v_k>0}|| ≤ C^k U_{k-1}^{5(q-2)/(6q)}`, giving  
  `I_k ≤ C_q C^k U_{k-1}^{4/3 - 5/(3q)} -> U_{k-1}^{4/3}`.
- Leads worth pursuing: Tao-filter the **alternative harmonic far-field decomposition**, not the already-favorable Vasseur harmonic term `P_{k1}`.
- Unexpected finding: the H^1 dead-end note uses "far-field" language in a way that is not literally consistent with Vasseur's notation; this appears to be a conceptual shorthand rather than a literal identification of `P_{k21}` as a far-field term.
- Computations worth doing later: if the Tao filter leaves the loophole alive, compute the alternative far/near split explicitly in a Wolf-type local pressure framework and test whether any part of the Vasseur `P_{k21}` contribution is truly moved into a harmonic component.
