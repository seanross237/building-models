"""Compute zeta zeros 2001-5000 in batches and save."""
import numpy as np
from mpmath import zetazero, mp
import time

mp.dps = 25

# Load existing 2000 zeros
zeros_2k = np.load('t_zeros_2k.npy')
all_zeros = list(zeros_2k)

batch_size = 500
start_n = 2001
end_n = 5001

for batch_start in range(start_n, end_n, batch_size):
    batch_end = min(batch_start + batch_size, end_n)
    t0 = time.time()
    batch = []
    for n in range(batch_start, batch_end):
        t = float(zetazero(n).imag)
        batch.append(t)
    elapsed = time.time() - t0
    all_zeros.extend(batch)
    # Save progress after each batch
    arr = np.array(all_zeros)
    np.save('t_zeros_progress.npy', arr)
    print(f'Batch {batch_start}-{batch_end-1} done in {elapsed:.1f}s, total zeros: {len(all_zeros)}, last={batch[-1]:.4f}')

# Final save
final = np.array(all_zeros)
np.save('t_zeros_5k.npy', final)
print(f'DONE. Total zeros: {len(final)}, range: {final[0]:.4f} to {final[-1]:.4f}')
