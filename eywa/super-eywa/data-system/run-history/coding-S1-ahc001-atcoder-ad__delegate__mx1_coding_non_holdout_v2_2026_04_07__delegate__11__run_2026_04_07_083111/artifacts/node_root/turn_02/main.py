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

    # Sort by area descending to give larger rectangles priority
    sorted_adv = sorted(advertisers, key=lambda a: a['r'], reverse=True)
    
    results = [None] * N
    placed_rects = []

    def intersects(r1, r2):
        # r = (x1, y1, x2, y2)
        return not (r1[2] <= r2[0] or r1[0] >= r2[2] or r1[3] <= r2[1] or r1[1] >= r2[3])

    for adv in sorted_adv:
        x, y, target_r = adv['x'], adv['y'], adv['r']
        
        # Start with a minimal rectangle containing the point
        # We use a small epsilon-like approach for integer bounds
        # [x, x+1) x [y, y+1)
        best_rect = (x, y, x + 1, y + 1)
        
        # Try to expand the rectangle to approach target_r
        # We'll use a simple greedy expansion: try to increase width/height
        # while checking for collisions and board boundaries.
        
        curr_x1, curr_y1, curr_x2, curr_y2 = x, y, x + 1, y + 1
        
        # Target side length if it were a square
        side = int(target_r**0.5)
        if side < 1: side = 1
        
        # Attempt to expand in 4 directions greedily
        # This is a simplified heuristic: expand to reach target area
        # while ensuring no overlap.
        
        # We'll try to grow the rectangle towards a square shape of area target_r
        # but we must keep the point (x, y) inside.
        
        # Heuristic: Try to find a bounding box that fits the area
        # and doesn't collide.
        
        # For simplicity in this baseline, we expand the current rect
        # in steps to find