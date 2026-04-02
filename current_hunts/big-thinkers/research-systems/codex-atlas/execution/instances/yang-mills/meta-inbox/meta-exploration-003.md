# Meta-Learning: Exploration 003

## What worked well
- The Math Explorer successfully implemented a full lattice gauge theory simulation from scratch — quite impressive
- Kennedy-Pendleton heat bath algorithm + numba optimization made it fast enough to run on reasonable sizes
- Specifying exact β values and lattice sizes in the goal gave clear, comparable results
- The verification scorecard (VERIFIED/COMPUTED/CHECKED/CONJECTURED) is extremely useful for knowing what to trust

## What didn't work
- First attempt crashed (tmux session died). Required relaunch. Need explicit Enter after paste.
- Glueball mass extraction from correlators failed on small lattices — this was expected but should have been noted in the goal as a "likely failure mode"
- Scaling analysis couldn't be done on small lattices — goal should have set more realistic expectations or asked for larger lattices with numba

## Lessons
- Math Explorer can implement complex numerical simulations (lattice gauge theory is non-trivial). The key is being very specific about what to compute and what parameters to use.
- For lattice simulations, 4⁴-8⁴ is only good for basic observables (plaquette, Wilson loops, Creutz ratios). Glueball masses need ≥16⁴ which is borderline for pure Python.
- The negative connected correlator (finite-volume sum rule effect) was an unexpected and interesting finding. Future computational goals should ask for diagnostic outputs that might reveal such effects.
- Always send Enter after the text paste in tmux — this is now a known operational issue.
