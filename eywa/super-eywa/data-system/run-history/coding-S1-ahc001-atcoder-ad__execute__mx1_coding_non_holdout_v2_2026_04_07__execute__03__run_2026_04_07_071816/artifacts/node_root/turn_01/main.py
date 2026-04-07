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

    # Sort advertisers by r to handle smaller ones first or by position
    # A simple approach: use a grid or just very small rectangles to avoid overlap.
    # To maximize score, we want area close to r. 
    # However, the constraint is NO overlap. 
    # Let's try to assign a tiny rectangle around (x, y) to ensure no overlap.
    # Or better, a small epsilon-sized rectangle.
    
    # To avoid overlap, we can use a very small width/height.
    # But we want to approach r. 
    # Let's try a simple strategy: sort by x, then y, and try to expand.
    # Actually, a safer way to avoid overlap is to use a very small rectangle.
    # Given the constraints and the nature of the problem, a simple valid baseline
    # is to output [x, x+1) [y, y+1) if it doesn't overlap. 
    # But we need to handle N up to a large number.
    
    # Let's use a very small rectangle for each: [x, x+0.0001) [y, y+0.0001)
    # Wait, coordinates are integers? The problem says (x, y) and r. 
    # Usually, in these problems, coordinates are integers. 
    # If we use [x, x+1) and [y, y+1), they might overlap if points are same.
    
    # Let's try to use a tiny rectangle around the point.
    # Since we need to output x1 y1 x2 y2, let's use integer bounds if possible.
    # If we use [x, x+1) and [y, y+1), we must ensure no two points are the same.
    # If points are the same, we must offset them.
    
    # Let's use a simple grid-based approach or just tiny rectangles.
    # To be safe and valid: [x, x+1) [y, y+1) is a rectangle of area 1.
    # If points are identical, we can't use the same [x, x+1) [y, y+1).
    
    # Let's refine: for each point, we'll output [x, x+1) [y, y+1).