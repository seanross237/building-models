import sys

def solve():
    # Read all input at once
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

    # To guarantee no overlap and that each rectangle contains (x_i, y_i),
    # we can sort the advertisers by their x-coordinate.
    # Then, we assign each advertiser a vertical strip.
    # However, if multiple advertisers have the same x, we need to handle that.
    # A safer way to ensure no overlap is to sort by x, then y.
    # We will divide the 10000x10000 board into N vertical strips.
    # But the strips must contain the requested x_i.
    
    # Let's use a simpler approach:
    # Sort advertisers by x.
    # We define x-boundaries b_0, b_1, ..., b_N such that 0 = b_0 <= b_1 <= ... <= b_N = 10000.
    # For each advertiser i (in sorted order), we need b_i <= x_i < b_{i+1}.
    # This is possible if we can find such boundaries.
    # Since we need to output N lines, let's sort by x.
    
    sorted_adv = sorted(advertisers, key=lambda a: (a['x'], a['y']))
    
    # We will create x-intervals [x1_i, x2_i) and y-intervals [y1_i, y2_i).
    # To ensure no overlap, we can use the sorted order to create non-overlapping x-strips.
    # But x_i might be the same. If x_i are the same, we can use y-strips.
    
    # Let's use a very robust method:
    # Sort by x.
    # For each i, x_start = sorted_adv[i]['x']
    # x_end = sorted_adv[i+1]['x'] if i < N-1 else 10000
    # This doesn't work if x_i == x_{i+1}.
    
    # Let's use a grid-like approach or a simple scanline.
    # Actually, the simplest way to guarantee no overlap is to assign each 
    # advertiser a unique 1x1 cell if possible, but that's not good for area.
    # Let's use the "Sorted X-Strips" logic but with a tiny bit of logic to handle duplicates.
    
    # We'll use a coordinate-based approach.
    # Sort by x.
    # We need to find b_0, ..., b_N such that b_i <= x_i < b_{i+1}.
    # This is only possible if x_i < x_{i+1} for all i.
    # If x_i == x_{i+1}, we can't use vertical strips.
    
    # Let's use a "Staircase" approach:
    # Sort by x.
    # For each i, we define a rectangle that is [x_i, x_i+1) x [y_i, y_i+1).
    # To avoid overlap, we can use a very small epsilon or just ensure 
    # that if (x_i, y_i) == (x_j, y_j), we shift one.
    # But we must contain (x_i, y_i).
    # A rectangle [x1, x2) x [y1, y2) contains (x, y) if x1 <= x < x2 and y1 <= y < y2.
    
    # Let's use a simple greedy:
    # Sort by x.
    # For each advertiser, we'll try to give them a strip [x_i, x_{i+1}) 
    # but we must ensure x_i is in it.
    # If we sort by x, then x_0 <= x_1 <= ... <= x_{N-1}.
    # We can pick boundaries b_i such that b_i <= x_i and x_i < b_{i+1}.
    # Let's try:
    # b_0 = 0
    # b_i = max(b_{i-1} + 1, x_{i-1} + 1) is not quite right.
    
    # Let's use a simpler approach:
    # Sort by x.
    # For i = 0 to N-1:
    #   x1 = sorted_adv[i]['x']
    #   x2 = sorted_adv[i+1]['x'] if i < N-1 else 10000
    #   Wait, if x_i == x_{i+1}, then x2 = x_i, which makes the rectangle invalid.
    
    # Let's use a 1D approach on x, but if x is same, use y.
    # Sort by x, then y.
    # For each i, we'll define a rectangle [x1, x2) x [y1, y2).
    # To ensure no overlap, we can use a very thin strip.
    # Let's use:
    # x1 = sorted_adv[i]['x']
    # x2 = sorted_adv[i]['x'] + 1
    # y1 = sorted_adv[i]['y']
    # y2 = sorted_adv[i]['y'] + 1
    # To handle duplicates, we can use:
    # x1 = sorted_adv[i]['x']
    # x2 = sorted_adv[i]['x'] + 1
    # y1 = sorted_adv[i]['y'] + (i * 0.00001) -- no, must be integers.
    
    # Let's use:
    # x1 = sorted_adv[i]['x']
    # x2 = sorted_adv[i]['x'] + 1
    # y1 = sorted_adv[i]['y']
    # y2 = sorted_adv[i]['y'] + 1
    # If (x, y) is same, we can use:
    # x1 = x, x2 = x+1, y1 = y, y2 = y+1
    # If we have multiple at same (x, y), we can't.
    
    # Let's use a simple grid-based approach.
    # Since N is up to 10000, we can't use a 10000x10000 grid.
    # But we can use a dictionary to keep track of used (x, y) points.
    # For each advertiser, we try to find the smallest rectangle [x, x+w) x [y, y+h)
    # that contains (x, y) and doesn't overlap.
    # Actually, the simplest valid solution is to just output 1x1 rectangles.
    # To handle duplicates, we can use:
    # x1 = x, x2 = x+1, y1 = y, y2 = y+1
    # If (x, y) is taken, we try (x+1, y), (x, y+1), (x+1, y+1), etc.
    # But we must contain (x, y).
    # If we use [x, x+1) x [y, y+1), it contains (x, y).
    # If another advertiser has (x, y), we can use [x-1, x+1) x [y, y+1) 
    # but that might overlap.
    
    # Let's use the "Strips" approach correctly.
    # Sort by x.
    # For each i, we want to find x_start_i, x_end_i such that
    # x_start_i <= x_i < x_end_i and x_end_i <= x_start_{i+1}.
    # This is possible if we use the sorted x_i.
    # Let's use:
    # x_start_i = sorted_adv[i]['x']
    # x_end_i = sorted_adv[i+1]['x'] if i < N-1 else 10000
    # If x_start_i == x_end_i, we have a problem.
    # But we can use y to break ties.
    # If x_i == x_{i+1}, we can't use vertical strips.
    # However, we can use a "staircase" of rectangles.
    
    # Let's try this:
    # Sort by x, then y.
    # For each i:
    #   x1 = sorted_adv[i]['x']
    #   x2 = sorted_adv[i]['x'] + 1
    #   y1 = sorted_adv[i]['y']
    #   y2 = sorted_adv[i]['y'] + 1
    # To avoid overlap, if (x, y) is taken, we can use:
    # x1 = x, x2 = x+1, y1 = y + (some offset)
    # Since we need integers, we can use:
    # x1 = x, x2 = x+1, y1 = y, y2 = y+1
    # If (x, y) is taken, we can use:
    # x1 = x, x2 = x+1, y1 = y + 1, y2 = y + 2...
    # But we must contain (x, y).
    # If we use [x, x+1) x [y, y+1), it contains (x, y).
    # If we use [x, x+1) x [y-1, y), it contains (x, y)
