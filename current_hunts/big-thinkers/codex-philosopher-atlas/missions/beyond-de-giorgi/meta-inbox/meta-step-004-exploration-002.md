# Meta-Learning: Step 4, Exploration 002 (Comparator Dynamic Audit)

## What Worked

- Auditing the direction-only and tube-only routes separately exposed two
  different failure types that would have blurred together inside the hybrid:
  prior-art collapse on the direction side and descriptive slippage on the tube
  side.
- Keeping the same fixed Eulerian package across both comparators made the
  comparison honest. It stopped the audit from giving each comparator its own
  friendliest localization story.
- Recording transport story, diffusion loss, and localization burden in the
  same table sharpened the ranking faster than another static observable table
  would have.

## What Could Be Improved

- The repository would benefit from a compact standing note on the difference
  between "Tao-sensitive intuition" and "estimate-level dynamic mechanism."
- Comparator audits should default to naming the first hidden stronger
  assumption explicitly, since that is often the real collapse point.

## Generalizable Lesson

When a hybrid survives because it combines two ideas, audit the halves
separately under the exact same package. If one half dies by prior-art overlap
and the other by missing transport law, the hybrid may still be the best route
available, but it is not yet dynamically plausible.
