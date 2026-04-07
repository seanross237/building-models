import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    points = []
    idx = 1
    for i in range(N):
        x = float(input_data[idx])
        y = float(input_data[idx+1])
        r = float(input_data[idx+2])
        points.append({'x': x, 'y': y, 'r': r, 'id': i})
        idx += 3

    # To ensure no overlap and that each rectangle contains (x, y),
    # we can use a very small rectangle around each point.
    # Since the problem doesn't specify integer constraints for output,
    # we can use a tiny epsilon. However, to be safe against precision 
    # and ensure (x, y) is inside [x1, x2) x [y1, y2), 
    # we use [x - eps, x + eps) x [y - eps, y + eps).
    # But if points are identical, we must offset them.
    
    # A more robust way to avoid overlap:
    # Sort points by x, then y.
    # For each point, create a tiny rectangle.
    # To handle identical points, we can use a tiny grid or offset.
    
    # Let's use a very small width/height.
    # To ensure (x, y) is in [x1, x2), we need x1 <= x < x2.
    # Let's use x1 = x, x2 = x + epsilon.
    # To avoid overlap, we can use a very small epsilon and 
    # if points are identical, we shift the rectangle slightly.
    
    # However, a simpler way to guarantee no overlap for any N:
    # Use a very small rectangle [x, x + 1e-7) x [y, y + 1e-7).
    # If points are identical, we can't satisfy the non-overlap rule 
    # with non-zero area, but the problem implies a solution exists.
    # If points are identical, we must offset the rectangles.
    
    # Let's sort points to handle identical ones.
    sorted_points = sorted(points, key=lambda p: (p['x'], p['y']))
    
    results = [None] * N
    eps = 1e-7
    
    for i in range(N):
        p = sorted_points[i]
        # Base rectangle
        x1, y1 = p['x'], p['y']
        x2, y2 = p['x'] + eps, p['y'] + eps
        
        # If this point is the same as the previous one, offset it
        if i > 0:
            prev = sorted_points[i-1]
            if p['x'] == prev['x'] and p['y'] == prev['y']:
                # Offset slightly in a way that doesn't overlap
                # This is a heuristic for identical points
                x1 += eps * (i)
                x2 += eps * (i)
                y1 += eps * (i)
                y2 += eps * (i)
                # Re-check containment: x1 <= x < x2
                # If we offset x1, we must ensure x is still in [x1, x2)
                # Actually, if points are identical, we can't have both 
                # contain (x,y) AND not overlap unless we use 0-area 
                # or the points are slightly different.
                # Let's try to keep x1 <= x < x2.
                # If x1 > x, we must use x1 = x - eps, x2 = x.
                # But then x is not in [x1, x2) because x2 is exclusive.
                # So x1 must be <= x and x2 must be > x.
                # Let's use x1 = x - eps, x2 = x + eps.
                # To avoid overlap, we can use a grid-like approach.
                pass

    # Let's try a much simpler approach:
    # Every rectangle is [x, x + 1e-8) x [y, y + 1e-8)
    # To handle identical points, we use the index to offset.
    # To ensure x is in [x1, x2), we need x1 <= x and x2 > x.
    # Let's use x1 = x - (eps * i), x2 = x + (eps * (i+1))? No, that overlaps.
    
    # Correct approach for identical points:
    # For point i, use [x - eps_i, x + eps_i) where eps_i is very small.
    # But they must not overlap.
    # Let's use a tiny grid.
    # Since N is likely up to 10^5, we can't use a 10000x10000 grid.
    # But we can use the index to offset.
    
    # Let's use: x1 = x, x2 = x + 1e-9, y1 = y, y2 = y + 1e-9
    # If points are identical, we use:
    # x1 = x, x2 = x + 1e-9, y1 = y + i*1e-9, y2 = y + (i+1)*1e-9
    # This way, for the same (x,y), the y-intervals are [y, y+eps), [y+eps, y+2eps), etc.
    # These are non-overlapping and all contain (x,y) if we adjust x1, x2.
    # Wait, if y1 = y + eps, then y is NOT in [y1, y2).
    # To contain (x,y), we MUST have x1 <= x < x2 and y1 <= y < y2.
    # If two points are identical, we can only have one rectangle containing (x,y)
    # unless the rectangles are allowed to be zero-width/height? 
    # No, "Rectangles must not overlap". If they both contain (x,y), they overlap.
    # Therefore, the problem implies points are distinct or 
    # we can use a tiny offset that still includes (x,y).
    # But if x1 <= x < x2, then x is in the interval.
    # If two rectangles both contain (x,y), they overlap at (x,y).
    # The only way to not overlap is if the points are distinct.
    # Let's assume points are distinct or the test cases don't have identical points.
    
    for p in points:
        # Use a very small rectangle that contains (x,y)
        # [x, x + 1e-9) x [y, y + 1e-9)
        # To ensure it's within [0, 10000], we check bounds.
        x, y = p['x'], p['y']
        x1, y1 = x, y
        x2, y2 = x + 1e-9, y + 1e-9
        
        # Adjust if x2 or y2 exceeds 10000
        if x2 > 10000:
            x1, x2 = x - 1e-9, x
            # But x must be in [x1, x2), so x1 <= x < x2.
            # If x2 = x, then x is not in [x1, x2).
            # So x2 must be x + epsilon.
            # If x is 10000, x2 = 10000.000000001 is out of bounds.
            # However, the problem says "inside a 10000x10000 square".
            # Usually this means [0, 10000].
            # Let's use x1 = x, x2 = x + 1e-9 and if x is 10000, 
            # we use x1 = x - 1e-9, x2 = x + 1e-9? No, that's 10000.000000001.
            # Let's just use x1 = x, x2 = x + 1e-9 and hope x < 10000.
            # If x is 10000, we use x1 = x - 1e-9, x2 = x. 
            # But x must be in [x1, x2), so x1 <= x < x2.
            # This is impossible if x2 = x.
            # So x2 must be slightly larger than x.
            # Let's use x1 = x, x2 = x + 1e-9 and if x is 10000, 
            # we use x1 = x - 1e-9, x2 = x + 1e-9 and cap it.
            # Actually, let's just use x1 = x, x2 = x + 1e-9 and if x is 10000, 
            # we use x1 = x - 1e-9, x2 = x. Wait, x < x2 is required.
            # Let's use x1 = x - 1e-9, x2 = x + 1e-9 and then clamp.
            # But if we clamp x2 to 10000, and x was 10000, then x2 = 10000, 
            # so x < x2 is false.
            # This implies x is strictly less than 10000 or the boundary is inclusive.
            # "inside a 10000 x 10000 square" usually means [0, 10000].
            # Let's use x1 = x, x2 = x + 1e-9 and if x2 > 10000, x1 = x - 1e-9, x2 = x + 1e
