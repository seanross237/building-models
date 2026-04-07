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
    
    # To avoid overlaps, we divide the board into N horizontal strips.
    # Each strip i will cover y in [y_start, y_end).
    # We must ensure the requested point (x_i, y_i) is inside the strip.
    # However, the problem doesn't guarantee y_i is in a specific strip.
    # A safer way to avoid overlap is to sort by y and create strips, 
    # but since we must contain (x_i, y_i), we can use a simple 
    # non-overlapping strategy: divide the board into N horizontal strips 
    # based on the y-coordinates of the points.
    
    # Let's try a simpler approach: 
    # Sort advertisers by y_i.
    # Assign each advertiser a strip [y_low, y_high) such that y_i is inside.
    
    sorted_indices = sorted(range(N), key=lambda i: advertisers[i][1])
    
    # We will define y boundaries. 
    # y_bounds[i] is the boundary between sorted_indices[i-1] and sorted_indices[i]
    y_bounds = [0] * (N + 1)
    y_bounds[0] = 0
    y_bounds[N] = board_size
    
    # To ensure no overlap and that each point is contained:
    # We can set boundaries between y_i and y_{i+1}
    for i in range(1, N):
        idx_curr = sorted_indices[i-1]
        idx_next = sorted_indices[i]
        y_curr = advertisers[idx_curr][1]
        y_next = advertisers[idx_next][1]
        # Boundary must be between y_curr and y_next. 
        # If they are equal, we need a tiny epsilon or just handle it.
        # Since coordinates are integers, we can use (y_curr + y_next) // 2
        # But we must ensure y_curr <= boundary < y_next is not strictly required,
        # just that y_curr is in [y_low, y_high).
        # Let's use: boundary = y_curr + 1 if y_curr < y_next else y_curr
        # Actually, a simpler way:
        # The strip for sorted_indices[i] is [y_bounds[i], y_bounds[i+1])
        # We need y_bounds[i] <= y_{sorted_indices[i]} < y_bounds[i+1]
        # Let's just use a very simple partition:
        # y_bounds[i] = y_{sorted_indices[i-1]} + 1 (if possible)
        # This is tricky if points have same y.
        pass

    # Let's use a more robust approach:
    # Divide the 10000 height into N strips. 
    # But we must ensure y_i is in the strip.
    # If we can't guarantee that, we can't use fixed strips.
    # Let's use the sorted y approach properly.
    
    # Correct approach for non-overlapping rectangles:
    # Sort by y.
    # For each i, rectangle is [0, 10000) x [y_low_i, y_high_i)
    # where y_low_0 = 0, y_high_N = 10000, and y_high_i = y_low_{i+1}
    # and y_low_i <= y_i < y_high_i.
    
    # To make this work, we need to pick y_bounds such that 
    # y_{sorted_indices[i-1]} < y_bounds[i] <= y_{sorted_indices[i]}
    # This is only possible if y values are strictly increasing.
    # If y values are not strictly increasing, we can't use horizontal strips 
    # that cover the whole width.
    
    # Let's use a very simple strategy: 
    # Each rectangle i is just the point (x_i, y_i) as a 1x1 rectangle.
    # [x_i, x_i+1) x [y_i, y_i+1)
    # But we need to avoid overlaps. If two points are the same, we shift.
    # However, the problem asks for area close to r_i.
    # Let's try to give each advertiser a unique x-coordinate strip.
    # Strip i: [i * (10000/N), (i+1) * (10000/N)) x [0, 10000)
    # This only works if x_i is in the strip.
    
    # Let's use a grid-based approach or just tiny rectangles.
    # Since we need to pass, let's output 1x1 rectangles that are guaranteed 
    # not to overlap.
    # We can use [x_i, x_i+1) x [y_i, y_i+1) but if they overlap, we shift.
    # A better way: use a very small width for each.
    # But the simplest valid output is a 1x1 rectangle for each point.
    # To avoid overlap, we can use [x_i, x_i+1) x [y_i, y_i+1) and if 
    # (x_i, y_i) is same, we use (x_i, y_i + offset).
    # But the problem says (x_i, y_i) must be contained.
    # A 1x1 rectangle [x_i, x_i+1) x [y_i, y_i+1) contains (x_i, y_i).
    
    # Let's use a simple scanline/grid approach.
    # We'll use 1x1 rectangles. To avoid overlap, we can use 
    # [x_i, x_i+1) x [y_i, y_i+1) and if there's a collision, 
    # we can't easily fix it without knowing all points.
    # Wait, the simplest way to avoid overlap is to use 
    # [x_i, x_i+1) x [y_i, y_i+1) and if they overlap, 
    # we can use a very small area.
    # Actually, the most robust way to avoid overlap is to 
    # assign each advertiser a unique integer coordinate.
    # But we must contain (x_i, y_i).
    
    # Let's use: x1=x_i, x2=x_i+1, y1=y_i, y2=y_i+1.
    # To handle overlaps, we can use a dictionary to track used (x, y) cells.
    used_cells = set()
    results = []
    for i in range(N):
        x, y, r = advertisers[i]
        # Try to find the nearest available 1x1 cell
        found = False
        for dx in range(0, 100):
            for dy in range(0, 100):
                # Check (x+dx, y+dy)
                if (x + dx, y + dy) not in used_cells:
                    # Check if this cell contains (x, y)
                    # A cell [cx, cx+1) x [cy, cy+1) contains (x, y) 
                    # only if cx <= x < cx+1 and cy <= y < cy+1
                    # which means cx = x and cy = y.
                    # So we can only use (x, y) if it's not used.
                    # If (x, y) is used, we must expand the rectangle 
                    # to include (x, y) but not overlap.
                    pass
        
        # Let's try a different approach: 
        # Every rectangle is [x_i, x_i+1) x [y_i, y_i+1).
        # If (x_i, y_i) is the same for multiple i, we can use 
        # [x_i, x_i+1) x [y_i, y_i+1), [x_i, x_i+1) x [y_i+1, y_i+2), etc.
        # But we must contain (x_i, y_i).
        # A rectangle [x1, x2) x [y1, y2) contains (x, y) if x1 <= x < x2 and y1 <= y < y2.
        # If we have multiple points at (x, y), we can use:
        # Rect 1: [x, x+1) x [y, y+1)
        # Rect 2: [x-1, x+1) x [y, y+1) -- NO, this overlaps.
        # Rect 2: [x, x+1) x [y-1, y+1) -- NO.
        # If points are identical, we can use:
        # Rect 1: [x, x+1) x [y, y+1)
        # Rect 2: [x-1, x) x [y, y+1) -- NO, doesn't contain (x, y).
        # Wait, if x1 <= x < x2, then x can be x1.
        # So if we have two points at (x, y):
        # Rect 1: [x, x+1) x [y, y+1)
        # Rect 2: [x-
