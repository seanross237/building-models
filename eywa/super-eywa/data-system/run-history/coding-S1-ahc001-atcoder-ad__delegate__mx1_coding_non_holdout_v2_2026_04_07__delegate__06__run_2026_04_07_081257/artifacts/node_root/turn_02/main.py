import sys
import heapq

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
    
    # To prevent overlaps, we keep track of occupied regions.
    # Since N is relatively small (implied by typical AHC problems), 
    # we can check against existing rectangles.
    # However, a simple greedy approach: 
    # 1. Start with a tiny rectangle around (x, y).
    # 2. Expand it to reach target area r while checking for collisions.
    
    occupied_rects = []

    # Sort advertisers by target area descending to give larger ones priority
    sorted_indices = sorted(range(N), key=lambda i: advertisers[i]['r'], reverse=True)

    for i in sorted_indices:
        adv = advertisers[i]
        tx, ty, tr = adv['x'], adv['y'], adv['r']
        
        # Initial tiny rectangle: [x, x+1) x [y, y+1)
        # We must ensure x+1 <= 10000 and y+1 <= 10000
        x1, y1 = tx, ty
        x2, y2 = tx + 1, ty + 1
        
        # Clamp to board
        if x2 > 10000: x2 = 10000; x1 = max(0, x2-1)
        if y2 > 10000: y2 = 10000; y1 = max(0, y2-1)
        if x1 < 0: x1 = 0
        if y1 < 0: y1 = 0

        # Greedy expansion
        # We try to expand in 4 directions to reach area tr
        # To keep it simple and robust, we expand in steps.
        current_area = (x2 - x1) * (y2 - y1)
        
        # Directions: Right, Left, Down, Up
        # We use a simple heuristic: expand the dimension that is currently smaller
