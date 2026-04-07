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
        advertisers.append((x, y, r))
        idx += 3

    board_size = 10000
    
    # To ensure no overlap and that each rectangle contains its point (x, y),
    # we divide the board into N horizontal strips.
    # Each strip i will cover y in [y_start, y_end).
    # We must ensure y_start <= y_i < y_end.
    
    # A simple way to avoid overlap and ensure point containment:
    # Sort advertisers by y coordinate to assign strips.
    # However, the problem asks for output in the original order.
    
    # Let's use a simple vertical striping based on the index, 
    # but we must ensure the point (x_i, y_i) is inside.
    # Since we can't guarantee y_i is in a specific strip if we use fixed strips,
    # let's use a different approach: 
    # Divide the board into N vertical strips [x_start, x_end).
    # But x_i might not be in the strip.
    
    # Correct approach: 
    # The simplest way to guarantee no overlap and point containment is to 
    # use the y-coordinate to define strips, but we must sort them.
    
    # 1. Store original index
    indexed_adv = []
    for i in range(N):
        indexed_adv.append((advertisers[i][1], i)) # (y, original_index)
    
    # 2. Sort by y
    indexed_adv.sort()
    
    # 3. Create strips based on sorted y
    # To ensure y_i is inside, we can use the sorted y values as boundaries.
    # But we need N rectangles. Let's use the sorted y values to define boundaries.
    # Boundaries: y_0 = 0, y_1, y_2, ..., y_{N-1}, y_N = 10000
    # This doesn't work because we need N rectangles.
    
    # Let's use a simpler approach: 
    # Divide the 10000 height into N equal parts. 
    # This only works if we can guarantee y_i is in the i-th part.
    # Since we can't, let's sort the advertisers by y and assign them strips.
    
    results = [None] * N
    
    # Sort advertisers by y to assign non-overlapping y-ranges
    sorted_indices = sorted(range(N), key=lambda i: advertisers[i][1])
    
    # We will create N strips. The i-th sorted advertiser gets a strip.
    # To ensure the strip contains y_i, we can use the sorted y values.
    # Let's define boundaries:
    # b[0] = 0
    # b[1] = y of sorted_indices[0] (but we need to be careful)
    # Actually, let's just use the sorted y values as boundaries.
    # Boundaries: 0, sorted_y[0], sorted_y[1]... is not enough.
    
    # Let's use:
    # Strip 0: [0, sorted_y[0] + epsilon] -> No, that's not right.
    
    # Let's use the sorted y values to create N intervals.
    # The i-th interval (in sorted order) will be [y_low, y_high]
    # where y_low is the y of the (i-1)-th sorted advertiser and y_high is the y of the i-th.
    # This is still tricky.
    
    # Simplest valid approach:
    # Sort advertisers by y.
    # The i-th advertiser (in sorted order) gets the range:
    # [y_of_prev_sorted_advertiser, y_of_current_sorted_advertiser] is too small.
    # Let's use:
    # y_boundary[0] = 0
    # y_boundary[i] = sorted_y[i-1] for i=1..N
    # y_boundary[N] = 10000
    # This gives N intervals: [y_boundary[i], y_boundary[i+1]]
    # But we need to ensure y_i is in the interval.
    # If we sort by y, then y_sorted[i] is definitely >= y_sorted[i-1].
    # So the interval [y_sorted[i-1], y_sorted[i]] contains y_sorted[i-1] and y_sorted[i].
    # Wait, the interval [y_sorted[i-1], y_sorted[i]] contains y_sorted[i] only if we use it as the upper bound.
    
    # Let's use:
    # For sorted index i (0 to N-1):
    # If i < N-1: y_min = sorted_y[i], y_max = sorted_y[i+1]
    # This doesn't work because the interval [y_i, y_{i+1}] might not contain y_i if we are not careful.
    # Actually, if we sort by y, then y_0 <= y_1 <= ... <= y_{N-1}.
    # The interval [y_i, y_{i+1}] contains y_i and y_{i+1}.
    # But we need N intervals.
    # Let's use:
    # Interval 0: [0, y_0] (if y_0 > 0)
    # Interval 1: [y_0, y_1]
    # ...
    # Interval N-1: [y_{N-2}, 10000]
    # This only works if N is small.
    
    # Let's use a very safe approach:
    # Divide the board into N horizontal strips: [i * 10000/N, (i+1) * 10000/N)
    # This only works if we can guarantee y_i is in the strip.
    # We can't.
    
    # Let's use the sorted y-coordinates to define the strips.
    # Sorted y: y'_0, y'_1, ..., y'_{N-1}
    # We need N rectangles.
    # Rectangle 0: [0, y'_0] (if y'_0 > 0) - but this might not contain y'_0 if we use [0, y'_0).
    # Let's use:
    # Rectangle 0: [0, y'_0]
    # Rectangle 1: [y'_0, y'_1]
    # ...
    # Rectangle N-1: [y'_{N-2}, 10000]
    # This is N rectangles. Let's check if they contain the points.
    # Rectangle i (for i > 0) is [y'_{i-1}, y'_i]. It contains y'_i.
    # Rectangle 0 is [0, y'_0]. It contains y'_0.
    # This works!
    # To avoid zero-width rectangles if y'_i == y'_{i-1}, we can use:
    # Rectangle i: [y'_{i-1}, y'_i] if i > 0 else [0, y'_0]
    # But if y'_i == y'_{i-1}, the area is 0. That's fine for a valid solution.
    # However, the problem says [x1, x2) x [y1, y2).
    # If y1 == y2, the rectangle is empty. An empty rectangle contains its point? 
    # "Rectangle i must contain its requested point (x_i, y_i)".
    # An empty rectangle cannot contain a point.
    # So we need y1 < y2.
    
    # Let's refine:
    # We have N points with y-coordinates y'_0 <= y'_1 <= ... <= y'_{N-1}.
    # We need N non-overlapping intervals [y1_i, y2_i) such that y'_i is in [y1_i, y2_i).
    # Let's use:
    # y_boundary[0] = 0
    # y_boundary[1] = y'_0
    # y_boundary[2] = y'_1
    # ...
    # y_boundary[N] = 10000
    # This is not working because we need y'_i to be in the interval.
    
    # Let's use:
    # y_boundary[0] = 0
    # y_boundary[1] = y'_0 + 0.000001 (not integer)
    # Let's use integers.
    # y_boundary[0] = 0
    # y_boundary[1] = y'_0
    # y_boundary[2] = y'_1
    # ...
    # This is still not working.
    
    # Let's try this:
    # Sort advertisers by y: (y'_0, idx_0), (y'_1, idx_1), ..., (y'_{N-1}, idx_{N-1})
    # For i = 0: y_min = 0, y_max = y'_0 + 1 (if y'_0 < 10000)
    # This is getting complicated.
    
    # Let's use a simpler approach:
    # The y-coordinates are in [0, 10000].
    # There are N advertisers.
    # Let's use the sorted y-coordinates to create N strips.
    # The i-th sorted advertiser gets the strip [y'_{i-1}, y'_i]? No.
    # Let's use:
