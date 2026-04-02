# Exploration 001 — Code

## Files

- `spinor_helicity.py` — Core infrastructure: spinors, brackets, momentum construction, kinematics generation
- `compute_amplitudes.py` — All three amplitude methods + comparison framework + timing benchmark

## Running

```bash
cd code/
python spinor_helicity.py    # Test spinor infrastructure
python compute_amplitudes.py  # Full three-method comparison and benchmark
```

## Dependencies

- Python 3.8+
- NumPy

## Quick test (inline)

```python
from spinor_helicity import *
import numpy as np

parts = make_kinematics_com(1.0, np.pi/3)
p1, p2, p3, p4 = parts

# Parke-Taylor
A = ab(p1,p2)**4 / (ab(p1,p2)*ab(p2,p3)*ab(p3,p4)*ab(p4,p1))
print(f"A_PT = {A}")  # 2.370370...
```
