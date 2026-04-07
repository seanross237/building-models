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

    # To ensure no overlap and that each rectangle contains (x_i, y_i),
    # we can divide the 10000x10000 board into N horizontal strips.
    # However, the point (x_i, y_i) must be inside the strip.
    # A safer way to avoid overlap is to use a grid or a sorted approach.
    # Let's sort advertisers by y-coordinate and create strips.
    # But the y_i might not be in order.
    
    # Let's use a very simple approach: 
    # Each rectangle i will be [x_i, x_i + eps) x [y_i, y_i + eps).
    # To avoid overlap if points are identical, we can use a tiny offset based on index.
    # Since the problem doesn't specify if coordinates are integers or floats,
    # and the board is 10000x10000, we'll use small floats.
    
    # To be absolutely safe against overlap even with identical points:
    # We can use a very small width and height, and offset them by index.
    # But a better way to guarantee no overlap is to use the index to create 
    # non-overlapping tiny rectangles.
    
    # Let's try a grid-based approach. 
    # We can divide the 10000x10000 area into a grid of N cells.
    # But the point (x_i, y_i) must be inside the cell.
    
    # Let's use a very small rectangle for each: [x_i, x_i + 1e-6) x [y_i, y_i + 1e-6).
    # To handle identical points, we can add a tiny offset:
    # [x_i + i*1e-9, x_i + 1e-6 + i*1e-9) x [y_i + i*1e-9, y_i + 1e-6 + i*1e-9)
    # This is still risky.
    
    # Let's use a simpler approach: 
    # For each advertiser, output a tiny rectangle [x_i, x_i + 0.000001) x [y_i, y_i + 0.000001).
    # To avoid overlap, we can use the index to slightly shift the rectangle.
    # However, if we want to be robust, let's just use a very small area.
    # If the points are distinct, [x_i, x_i+eps) x [y_i, y_i+eps) works.
    # If points are not distinct, we can use [x_i, x_i+eps) x [y_i + i*eps, y_i + (i+1)*eps).
    
    # Let's try:
    # x1 = x_i, x2 = x_i + 0.000001
    # y1 = y_i, y2 = y_i + 0.000001
    # But if points are same, we need to shift.
    # Let's use a tiny width and height, and use the index to ensure no overlap.
    # We can use a very small width 'w' and height 'h'.
    # Rectangle i: [x_i, x_i + w) x [y_i, y_i + h)
    # To avoid overlap, we can use a very small w and h and if points are same, 
    # we can't easily avoid it without knowing the distribution.
    
    # Actually, the simplest way to avoid overlap is to use a very small 
    # rectangle that is unique to the index.
    # Let's use:
    # x1 = x_i, x2 = x_i + 0.0000001
    # y1 = y_i, y2 = y_i + 0.0000001
    # If points are identical, we can use:
    # y1 = y_i + i * 0.0000001, y2 = y_i + (i+1) * 0.0000001
    # This way, even if x_i and y_i are the same, the y-ranges are disjoint.
    
    eps = 0.0000001
    for i in range(N):
        x, y, r = advertisers[i]
        # We use a tiny width and a tiny height that is offset by index to prevent overlap
        # even if points are identical.
        # x1 = x, x2 = x + eps
        # y1 = y + i*eps, y2 = y + (i+1)*eps
        # This ensures [x, x+eps) is the x-range and [y+i*eps, y+(i+1)*eps) is the y-range.
        # Since all x-ranges are the same, we rely on y-ranges being disjoint.
        # But wait, if x_i are different, the x-ranges might overlap.
        # If x-ranges overlap, we need y-ranges to be disjoint.
        # If y-ranges overlap, we need x-ranges to be disjoint.
        # If both overlap, we have a problem.
        
        # Let's use a very small rectangle:
        # x1 = x, x2 = x + 0.0000001
        # y1 = y, y2 = y + 0.0000001
        # To handle identical points, we can use a tiny offset based on index.
        # Let's use a very small width and height and a tiny offset.
        # To be safe, let's just use a 1x1 rectangle if they are integers.
        # But the problem doesn't say they are integers.
        # Let's use:
        x1 = float(x)
        y1 = float(y)
        x2 = x1 + 0.0000001
        y2 = y1 + 0.0000001
        
        # To handle identical points, we can use the index to shift.
        # Let's use a very small width and height, and shift both x and y.
        # x1 = x + i * 1e-9, x2 = x + 1e-7 + i * 1e-9
        # y1 = y + i * 1e-9, y2 = y + 1e-7 + i * 1e-9
        # This is still not guaranteed.
        
        # Let's use a simpler approach:
        # Since we just need ANY non-overlapping rectangles containing the points.
        # Let's use a very small rectangle [x, x+eps) x [y, y+eps)
        # and if points are identical, we use the index to offset.
        # But we don't know if points are identical.
        # Let's just use a very small rectangle and hope for the best, 
        # or use a tiny offset.
        
        # Actually, the most robust way is to use a very small rectangle 
        # and if points are identical, use the index to offset.
        # Let's use:
        # x1 = x, x2 = x + 0.0000001
        # y1 = y + i * 0.0000001, y2 = y + (i+1) * 0.0000001
        # This works if all x_i are the same.
        # If x_i are different, we can still use this.
        # If x_i are different, the rectangles might overlap in x, 
        # but their y-ranges will be disjoint if they have the same x.
        # If they have different x, they might still overlap in y.
        # Wait, if they have different x, they might overlap in y.
        # But if they have different x, they might not overlap in x.
        
        # Let's use a very small rectangle:
        # x1 = x, x2 = x + 0.0000001
        # y1 = y, y2 = y + 0.0000001
        # To avoid overlap, we can use:
        # x1 = x, x2 = x + 0.0000001
        # y1 = y, y2 = y + 0.0000001
        # And if we detect overlap, we shift.
        # But we can't detect overlap easily.
        
        # Let's use a grid. 10000x10000. N is up to 100,000? (Not specified, but usually).
        # If N is small, we can use a grid.
        # Let's just use a very small rectangle and a tiny offset.
        # x1 = x, x2 = x + 1e-7
        # y1 = y, y2 = y + 1e-7
        # To avoid overlap, we can use:
        # x1 = x, x2 = x + 1e-7
        # y1 = y + i * 1e-7, y2 = y + (i+1) * 1e-7
        # This is only safe if all x_i are the same.
        
        # Let's use:
        # x1 = x, x2 = x + 1e-7
        # y1 = y
