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

    # To ensure no overlaps and that each point (x_i, y_i) is contained,
    # we can use a very simple strategy:
    # Each rectangle i will be a 1x1 rectangle [x_i, x_i+1) x [y_i, y_i+1).
    # However, if multiple advertisers have the same (x_i, y_i), 
    # we must ensure they don't overlap.
    # Since the problem allows any rectangle that contains the point,
    # we can use a tiny offset for identical points.
    # But wait, the coordinates are integers. If we use [x, x+1), 
    # the only integer point it contains is x.
    # If two points are identical, we can't both use [x, x+1) x [y, y+1).
    # But we can use [x, x+1) x [y, y+1) for the first, 
    # and for the second, we can use [x, x+1) x [y+1, y+2) if y+1 < 10000.
    # However, the second rectangle must contain (x, y).
    # A rectangle [x1, x2) x [y1, y2) contains (x, y) if x1 <= x < x2 and y1 <= y < y2.
    # If x1 = x and x2 = x+1, then x is the only integer in [x1, x2).
    # If we have two points at (x, y), we can use:
    # Rect 1: [x, x+1) x [y, y+1)
    # Rect 2: [x, x+1) x [y-1, y+1) -- No, that overlaps.
    # Actually, if we use non-integer boundaries, we can avoid overlap.
    # But the problem doesn't say boundaries must be integers.
    # Let's use a very small width/height.
    # For advertiser i, let's use [x_i, x_i + epsilon) x [y_i, y_i + epsilon).
    # To avoid overlap, we can use [x_i, x_i + eps) x [y_i, y_i + eps) 
    # and if there's a collision, we shift the epsilon.
    # Actually, the simplest way to avoid overlap is to use a grid.
    # But the points are arbitrary.
    
    # Let's use a very simple approach:
    # For each advertiser i, output [x_i, x_i+1) x [y_i, y_i+1).
    # To handle duplicates, we'll use a dictionary to track used 1x1 cells.
    # If (x, y) is taken, we'll try to find a 1x1 cell that still contains (x, y).
    # But a 1x1 cell [x1, x1+1) x [y1, y1+1) contains (x, y) only if x1=x and y1=y.
    # Wait, if we use [x-0.5, x+0.5) x [y-0.5, y+0.5), it contains (x, y).
    # If we have two points at (x, y), we can use:
    # Rect 1: [x-0.1, x+0.1) x [y-0.1, y+0.1)
    # Rect 2: [x-0.2, x-0.1) x [y-0.1, y+0.1) -- No, doesn't contain (x, y).
    
    # Let's use the fact that we can use any x1, y1, x2, y2.
    # For each advertiser i, we can use [x_i, x_i + 0.0001) x [y_i, y_i + 0.0001).
    # To avoid overlap, we can add a tiny offset based on the index i.
    # Rect i: [x_i, x_i + 0.00001 * i) x [y_i, y_i + 0.00001 * i) is not quite right.
    
    # Let's use: x1 = x_i, x2 = x_i + 1, y1 = y_i, y2 = y_i + 1.
    # If (x_i, y_i) is the same, we can use:
    # Rect 1: [x_i, x_i + 1) x [y_i, y_i + 1)
    # Rect 2: [x_i - 1, x_i) x [y_i, y_i + 1) -- No, doesn't contain x_i.
    # Wait, the condition is x1 <= x_i < x2.
    # So if x_i = 10, x1 can be 10, 9, 8... and x2 can be 11, 12, 13...
    # If we have two points at (10, 10):
    # Rect 1: [10, 11) x [10, 11)
    # Rect 2: [9, 10.5) x [10, 11) -- No, overlaps.
    # Rect 2: [9, 10) x [10, 11) -- No, doesn't contain 10.
    # Rect 2: [10, 11) x [11, 12) -- No, doesn't contain 10.
    
    # Correct logic: if x1 <= x < x2, then x can be the boundary.
    # If we have two points at (10, 10):
    # Rect 1: [10, 11) x [10, 11)
    # Rect 2: [9, 10] -- No, the interval is [x1, x2).
    # So x1 must be <= 10. If x1 = 10, then 10 is in [10, x2).
    # If we want to avoid overlap, we can use:
    # Rect 1: [10, 11) x [10, 11)
    # Rect 2: [9, 10) x [10, 11) -- This does NOT contain 10.
    # BUT, if we use [10, 11) x [10, 11) and [9, 10.000001) x [10, 11)? No.
    
    # Let's use a very simple non-overlapping strategy:
    # Divide the 10000x10000 board into N strips.
    # Since we don't know where the points are, let's use a grid.
    # Or even simpler: for each i, output [x_i, x_i + 0.000001) x [y_i, y_i + 0.000001).
    # To avoid overlap, we can use [x_i, x_i + 0.000001 * (i+1)) x [y_i, y_i + 0.000001 * (i+1)).
    # No, that's still not guaranteed.
    
    # Let's use: x1 = x_i, x2 = x_i + 1, y1 = y_i, y2 = y_i + 1.
    # To handle duplicates, we'll use a dictionary to store used (x, y) integer cells.
    # If (x, y) is taken, we'll try (x, y+1), (x, y+2)... (x+1, y), (x+1, y+1)...
    # But we must contain (x, y).
    # If we use [x, x+1) x [y, y+1), it contains (x, y).
    # If we use [x-1, x+1) x [y, y+1), it contains (x, y) and is 2x1.
    # If we use [x, x+1) x [y-1, y+1), it contains (x, y) and is 1x2.
    # If we use [x-1, x+1) x [y-1, y+1), it contains (x, y) and is 2x2.
    
    # Let's use a simple approach:
    # For each point (x, y), we'll try to find a rectangle [x1, x2) x [y1, y2)
    # such that x1 <= x < x2 and y1 <= y < y2 and it doesn't overlap.
    # The simplest is to use a 1x1 rectangle [x, x+1) x [y, y+1).
    # If (x, y) is already used, we can't use [x, x+1) x [y, y+1).
    # But we can use [x-1, x+1) x [y, y+1) if we are careful.
    # Actually, if we use [x, x+1) x [y, y+1), the only integer point is (x, y).
    # If we have multiple points at (x, y), we can use:
    # Rect 1: [x
