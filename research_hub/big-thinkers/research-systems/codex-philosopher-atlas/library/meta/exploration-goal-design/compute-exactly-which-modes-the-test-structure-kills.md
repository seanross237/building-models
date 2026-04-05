# Compute Exactly Which Modes The Test Structure Kills

When a branch depends on quotienting out modes already killed by the test
structure, make the explorer compute the annihilated modes exactly.

Ask separately for "modes already killed" and "modes still live." Otherwise the
branch can overcount fake progress on constants or other components that were
never live in the first place.

Filed from:
- `missions/beyond-de-giorgi/meta-inbox/meta-exploration-001.md`
