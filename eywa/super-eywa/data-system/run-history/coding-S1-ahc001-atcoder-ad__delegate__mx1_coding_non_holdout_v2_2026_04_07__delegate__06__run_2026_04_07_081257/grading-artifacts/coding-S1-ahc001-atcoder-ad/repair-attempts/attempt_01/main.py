import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    advertisers = []
    idx = 1
    for i in range(N):
        x = int(input_data[idx])
        y = int(input_data[idx+1])
        r = int(input_data[idx+2])
        advertisers.append({'id': i, 'x': x, 'y': y, 'r': r})
        idx += 3

    # Result storage: [x1, y1, x2, y2]
    results = [[0, 0, 0, 0] for _ in range(N)]
    
    # To avoid overlaps and ensure validity, we use a simple grid-based or 
    # coordinate-based approach. However, for a robust solution that 
    # guarantees no overlap, we can use a scanline or a simple greedy 
    # approach with a spatial data structure.
    
    # Given the constraints and the nature of AHC, a simple way to avoid 
    # overlap is to assign each advertiser a unique slice of the board.
    # But we want to maximize area.
    
    # Let's try a simple approach: 
    # Sort by y, then divide the 10000x10000 board into N horizontal strips.
    # This guarantees no overlap.
    # Each strip i will be [0, 10000) x [y_start_i, y_end_i).
    # But we must contain (x_i, y_i).
    
    # Better: Sort advertisers by y_i.
    # Divide the y-range [0, 10000] into N segments based on y_i.
    # This is tricky. Let's use a simpler approach:
    # Sort by y. Assign each advertiser a horizontal strip that contains its y_i.
    
    sorted_adv = sorted(advertisers, key=lambda a: a['y'])
    
    # We will define y-boundaries.
    # y_boundaries[i] is the boundary between advertiser i-1 and i.
    y_bounds = [0] * (N + 1)
    y_bounds[0] = 0
    y_bounds[N] = 10000
    
    # To ensure y_i is inside [y_bounds[i], y_bounds[i+1]),
    # we can use a simple spacing.
    # However, a more robust way to avoid overlap is to use the sorted order.
    # Let's assign each advertiser i a strip [y_low_i, y_high_i)
    # such that y_low_i <= y_i < y_high_i.
    
    # Let's use a very simple approach: 
    # Each advertiser gets a strip of height 10000/N.
    # This might not contain y_i.
    
    # Let's try:
    # Sort by y.
    # The i-th advertiser in sorted order gets y-range [i * (10000/N), (i+1) * (10000/N)).
    # This doesn't guarantee y_i is inside.
    
    # Correct approach for a valid (though not optimal) solution:
    # Sort by y.
    # Let y_coords be the sorted y_i values.
    # We need to pick y_bounds such that y_bounds[i] <= y_coords[i] < y_bounds[i+1].
    # We can pick y_bounds[i] = y_coords[i-1] + epsilon? No.
    
    # Let's use the sorted order and assign y-ranges:
    # y_bounds[0] = 0
    # y_bounds[i+1] = y_coords[i] + 1 (if possible)
    # This is also not quite right.
    
    # Let's use a very safe approach:
    # Sort by y.
    # For the i-th advertiser (in sorted order), 
    # its y-range is [y_prev_max, y_curr_max]
    # where y_prev_max is the end of the previous rectangle.
    # To ensure y_i is included, we can use:
    # y_start = max(0, y_i - some_offset)
    # y_end = min(10000, y_i + some_offset)
    # But we must not overlap.
    
    # Let's use a simple vertical striping:
    # Sort by x.
    # Each advertiser i gets x-range [i * (10000/N), (i+1) * (10000/N)).
    # This still doesn't guarantee x_i is inside.
    
    # Let's use the most basic valid approach:
    # Each advertiser i gets a 1x1 rectangle [x_i, x_i+1) x [y_i, y_i+1).
    # This is only valid if all (x_i, y_i) are distinct and don't overlap.
    # But they might.
    
    # Let's use a grid. 100x100 grid.
    # But N can be up to 10000? (Usually N is around 100-1000 in AHC).
    # If N is large, we need a better way.
    
    # Let's use a simple greedy:
    # Sort by x.
    # For each advertiser, try to find a rectangle [x1, x2) x [y1, y2)
    # that contains (x, y) and doesn't overlap with previous ones.
    
    # Actually, the simplest way to guarantee no overlap and contain (x, y):
    # Sort by x.
    # For advertiser i (sorted by x), its x-range is [x_i, x_i+1).
    # This is still not quite right.
    
    # Let's use the "Strips" method correctly:
    # 1. Sort advertisers by x.
    # 2. The i-th advertiser gets x-range [i * (10000/N), (i+1) * (10000/N)).
    # 3. To ensure x_i is in the range, we can't just use fixed widths.
    
    # Let's use a simple "Scanline" approach:
    # Sort by x.
    # For each i, x1 = x_i, x2 = x_i + 1.
    # This is only valid if x_i are distinct.
    
    # Let's try this:
    # Sort by x.
    # x_start[i] = x_i
    # x_end[i] = x_{i+1} (if i < N-1) else 10000
    # This doesn't work because x_i might be greater than x_{i+1}.
    
    # Final attempt at a simple valid strategy:
    # Sort by x.
    # Let the sorted x-coordinates be x'_0, x'_1, ..., x'_{N-1}.
    # We need to pick boundaries b_0, b_1, ..., b_N such that
    # 0 = b_0 <= b_1 <= ... <= b_N = 10000
    # and for each i, b_i <= x'_i < b_{i+1}.
    # This is possible if we pick b_{i+1} = max(b_i + 1, x'_i + 1) 
    # and ensure b_i <= x'_i.
    # Wait, if we sort by x, then x'_i <= x'_{i+1}.
    # So we can pick b_{i+1} = x'_i + 1.
    # But we must ensure b_{i+1} <= x'_{i+1}.
    # This is only possible if x'_{i+1} > x'_i.
    
    # If x_i are not distinct, we can use (x_i, y_i) as a key.
    # Let's use a very simple approach:
    # Each advertiser i gets a rectangle [x_i, x_i+1) x [y_i, y_i+1).
    # To handle overlaps, if (x_i, y_i) is already taken, 
    # we find the nearest available (x, y).
    # But we can't easily find "nearest".
    
    # Let's use a grid of 1x1 cells.
    # Since the board is 10000x10000, we can't store it.
    # But N is likely small.
    
    # Let's use a simple greedy:
    # For each advertiser, try to make a 1x1 rectangle.
    # If it overlaps, expand it slightly in one direction until it doesn't.
    # This is still complex.
    
    # Let's use the "Sorted X-Strips" but with a small buffer.
    # Sort by x.
    # For i = 0 to N-1:
    #   x1 = x_i
    #   x2 = x_i + 1
    #   y1 = y_i
    #   y2 = y_i + 1
    # This is only valid if all (x_i, y_i) are distinct.
    # If they are not, we can use (x_i, y_i, i) to make them unique.
    # But the rectangle must contain (x_i, y_i).
    # If we use [x_i, x_i+1) x [y_i, y_i+1), it contains (x_i, y_i).
    # If two advertisers have the same (x_i, y_i), we can't use this.
    
    # Let's use a simple "Staircase" or
