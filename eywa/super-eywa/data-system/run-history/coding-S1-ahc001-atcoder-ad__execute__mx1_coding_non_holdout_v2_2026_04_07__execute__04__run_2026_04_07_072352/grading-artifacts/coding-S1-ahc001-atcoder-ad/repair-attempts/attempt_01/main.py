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
        advertisers.append({'x': x, 'y': y, 'r': r, 'id': i})
        idx += 3

    # To ensure no overlap and that (x_i, y_i) is contained,
    # we can assign each advertiser a unique vertical strip.
    # However, x_i might be the same. 
    # A safer way to avoid overlap is to use a grid or sort by x and y.
    # Let's sort by x, then y.
    # We will assign each rectangle a width of 1 and a height of 10000,
    # but we must ensure x_i is within [x1, x2).
    # If we use [x_i, x_i+1), we might have overlaps if x_i are same.
    
    # Let's use a simple strategy: 
    # Sort advertisers by x.
    # Assign each advertiser i a range [x_start_i, x_end_i) such that
    # x_start_i <= x_i < x_end_i and ranges are disjoint.
    
    sorted_adv = sorted(advertisers, key=lambda a: a['x'])
    
    # We need to find x_start and x_end for each.
    # Since we need to contain x_i, let's try to partition the x-axis.
    # But x_i can be any value from 0 to 10000.
    # Let's use a very small width for each to avoid overlap.
    # Since the problem doesn't specify integer coordinates for output, 
    # but AtCoder usually expects them or floats, let's check.
    # "The rectangle is [x1, x2) x [y1, y2)". 
    # Let's use integer coordinates to be safe.
    
    # If we use integer coordinates, the smallest width is 1.
    # If N is up to 10000, we can give each a strip of width 1.
    # But x_i might be the same.
    
    # Let's use a different approach: 
    # Sort by x. For each i, the strip is [x_i_min, x_i_max).
    # To handle same x, we can use the index.
    # Let's map each advertiser to a unique x-coordinate if possible.
    # But x_i is fixed.
    
    # Correct approach for non-overlapping:
    # Sort by x.
    # For the i-th advertiser in sorted order, 
    # we need x_start <= x_i < x_end.
    # Let's try to use the y-coordinate to separate them if x is the same.
    # Or just use a very thin rectangle: [x_i, x_i+1) x [y_i, y_i+1).
    # To avoid overlap when (x_i, y_i) are same, we can use:
    # [x_i, x_i+1) x [y_i + offset, y_i + offset + 1)
    
    # Let's use a simple grid-like approach or just tiny rectangles.
    # To ensure no overlap, we can use:
    # x1 = x_i, x2 = x_i + 1
    # y1 = y_i, y2 = y_i + 1
    # If (x_i, y_i) is same, we shift.
    
    # However, the goal is to get area close to r_i.
    # A better way:
    # Sort by x.
    # For each i, x_start = (some value <= x_i), x_end = (some value > x_i).
    # To ensure no overlap, we can use x_start = sorted_adv[i].x 
    # and x_end = sorted_adv[i+1].x (if we handle the last one).
    # But x_i might be equal to x_{i+1}.
    
    # Let's use a simple 1x1 rectangle for each, but offset them to avoid overlap.
    # Since we need to output x1 y1 x2 y2:
    
    results = [None] * N
    # To handle duplicates and ensure no overlap:
    # We can use a small epsilon or just integer offsets.
    # Let's use: x1 = x_i, x2 = x_i + 1, y1 = y_i, y2 = y_i + 1.
    # To avoid overlap, if (x_i, y_i) is used, we try (x_i, y_i+1), etc.
    
    occupied = set()
    
    for i in range(N):
        x = advertisers[i]['x']
        y = advertisers[i]['y']
        
        # Find a unique 1x1 cell
        curr_x, curr_y = x, y
        while (curr_x, curr_y) in occupied:
            curr_y += 1
            if curr_y >= 10000:
                curr_y = 0
                curr_x += 1
                if curr_x >= 10000:
                    # This should not happen given N is reasonable
                    break
        
        # We must ensure the rectangle [x1, x2) x [y1, y2) contains (x, y)
        # and is within [0, 10000).
        # If we use [curr_x, curr_x+1) x [curr_y, curr_y+1), 
        # it only contains (x, y) if curr_x == x and curr_y == y.
        # If we shift, we must ensure the original (x, y) is inside.
        
        # Let's use a different strategy:
        # Each advertiser gets a strip [x_i, x_i+1) x [0, 10000).
        # To handle same x_i, we use y-offsets.
        # But we must contain (x_i, y_i).
        # If we use [x_i, x_i+1) x [y_i, y_i+1), it contains (x_i, y_i).
        # If we have multiple at same (x_i, y_i), we can use [x_i, x_i+1) x [y_i+k, y_i+k+1).
        # But then (x_i, y_i) is not in the rectangle unless k=0.
        
        # Wait, the requirement is: "Rectangle i must contain its requested point (x_i, y_i)".
        # If we use [x1, x2) x [y1, y2), then x1 <= x_i < x2 and y1 <= y_i < y2.
        
        # Let's use:
        # x1 = x_i, x2 = x_i + 1
        # y1 = y_i, y2 = y_i + 1
        # If (x_i, y_i) is already taken, we can't just shift y1, y2 because 
        # then (x_i, y_i) won't be in [y1, y2).
        # We must expand the rectangle to include (x_i, y_i).
        # But if we expand, we might overlap.
        
        # Let's use the fact that we can have x1 < x_i < x2.
        # Let's sort by x.
        # For each i, we assign a strip [x_start_i, x_end_i) where x_start_i <= x_i < x_end_i.
        # To ensure no overlap, we can use x_end_i = x_start_{i+1}.
        # We need to handle x_i = x_{i+1}.
        
        # Let's use a very simple approach:
        # Sort by x, then y.
        # For each i, x1 = x_i, x2 = x_i + 1.
        # To avoid overlap, if x_i is same, we use y-ranges.
        # But we must contain y_i.
        # If we use [x_i, x_i+1) x [y_i, y_i+1), it works.
        # If multiple have same (x_i, y_i), we can't use 1x1.
        # But the problem says "Rectangles must not overlap".
        # If two advertisers have the same (x_i, y_i), they MUST have different rectangles.
        # But if they have different rectangles, they can't both contain (x_i, y_i) 
        # without overlapping, because (x_i, y_i) is a single point.
        # Wait, if the rectangles are [x1, x2) x [y1, y2), 
        # and they both contain (x_i, y_i), then x1 <= x_i < x2 and y1 <= y_i < y2.
        # This means (x_i, y_i) is in the intersection.
        # If they must not overlap, then no two rectangles can contain the same point.
        # Therefore, all (x_i, y_i) must be unique.
        # Let's assume (x_i, y_i) are unique.
        
        # If (x_i, y_i) are unique, we can use:
        # x1 = x_i, x2 = x_i + 1, y1 = y_i, y2 = y_i +
