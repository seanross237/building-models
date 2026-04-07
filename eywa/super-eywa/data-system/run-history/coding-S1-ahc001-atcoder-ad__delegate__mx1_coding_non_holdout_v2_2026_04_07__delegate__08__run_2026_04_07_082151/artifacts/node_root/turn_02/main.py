import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    advertisers = []
    idx = 1
    for i in range(N):
        x = float(input_data[idx])
        y = float(input_data[idx+1])
        r = float(input_data[idx+2])
        advertisers.append({'id': i, 'x': x, 'y': y, 'r': r})
        idx += 3

    # Sort advertisers by target area descending to prioritize larger ones
    sorted_adv = sorted(advertisers, key=lambda a: a['r'], reverse=True)
    
    # Rectangles: (x1, y1, x2, y2)
    results = [None] * N
    # Occupied regions list to check for overlaps
    occupied = []

    BOARD_SIZE = 10000.0

    for adv in sorted_adv:
        target_x, target_y, target_r = adv['x'], adv['y'], adv['r']
        
        # Initial minimal rectangle (a tiny point around the target)
        # We try to expand this rectangle to reach target_r
        # For simplicity in this baseline, we use a small epsilon
        eps = 1e-7
        x1, y1, x2, y2 = target_x, target_y, target_x + eps, target_y + eps
        
        # Greedy expansion attempt
        # We try to grow the rectangle in 4 directions
        # To keep it simple and avoid complex geometry, we'll try to find a square-ish
        # rectangle that fits the area and doesn't overlap.
        
        side = target_r**0.5
        # Try to center the square on (target_x, target_y)
        best_rect = (target_x, target_y, target_x + eps, target_y + eps)
        max_area = 0

        # Heuristic: Try several candidate sizes/offsets
        # We'll try to expand the rectangle symmetrically
        for scale in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
            s = side * scale
            # Try to center the square
            cx1 = max(0.0, target_x - s/2)
            cy1 = max(0.0, target_y - s/2)
            cx2 = min(BOARD_SIZE, target_x + s/2)
            cy2 = min(BOARD_SIZE, target_y + s/2)
