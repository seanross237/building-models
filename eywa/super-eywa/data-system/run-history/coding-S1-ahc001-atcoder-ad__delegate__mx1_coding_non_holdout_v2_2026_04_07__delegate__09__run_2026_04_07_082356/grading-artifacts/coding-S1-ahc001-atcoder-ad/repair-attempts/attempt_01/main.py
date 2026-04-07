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

    # Sort advertisers by target area descending to prioritize larger ones
    # This helps in placing larger rectangles first.
    sorted_advs = sorted(advertisers, key=lambda a: a['r'], reverse=True)

    results = [None] * N
    placed_rects = [] # List of (x1, y1, x2, y2)

    BOARD_SIZE = 10000

    for adv in sorted_advs:
        target_x, target_y, target_r = adv['x'], adv['y'], adv['r']
        
        # Start with a minimal 1x1 rectangle containing the point
        # The point (x, y) must be inside [x1, x2) x [y1, y2)
        # So x1 <= x < x2 and y1 <= y < y2.
        # Let's use x1=x, x2=x+1, y1=y, y2=y+1.
        
        best_x1, best_y1, best_x2, best_y2 = target_x, target_y, target_x + 1, target_y + 1
        
        # Try to expand the rectangle greedily
        # We'll try to expand the width and height to approach target_r
        # while checking for collisions with already placed rectangles.
        
        curr_x1, curr_y1, curr_x2, curr_y2 = target_x, target_y, target_x + 1, target_y + 1
        
        # Simple greedy expansion: try to expand in 4 directions
        # We'll try to increase the area by expanding boundaries
        # To keep it simple and avoid infinite loops, we use a step-based approach
        
        # We'll try to find a rectangle that maximizes area <= target_r
        # and doesn't overlap.
        
        # Heuristic: Try to grow a square-ish rectangle
        side = 1
        max_side = int(target_r**0.5) + 1
        
        # We'll use a simpler approach: 
        # Start with 1x1. Try to expand the rectangle by 1 unit at a time.
        # To avoid O(N * Area) complexity, we'll try to expand in larger steps or 
        # just stick to a safe small rectangle if expansion is too hard.
        
        # Let's try to expand the current rectangle [curr_x1, curr_x2) x [curr_y1, curr_y2)
        # in a way that keeps (target_x, target_y) inside.
        
        # For this specific problem, a very safe approach is to just output the 1x1.
        # But to get a score, we need to expand.
        
        # Let's try to expand the rectangle to a larger size.
        # We'll try to find the largest side 's' such that a square of side 's'
        # centered at (target_x, target_y) is valid.
        
        low = 1
        high = BOARD_SIZE
        best_s = 1
        
        # Binary search for the largest side length of a square centered at (target_x, target_y)
        # Note: "centered" means the point is inside.
        # Let's define the square as [target_x - dx, target_x + dx + 1)
        # But we must ensure target_x is within [x1, x2).
        
        # Let's try a simpler expansion:
        # Try to expand x1, x2, y1, y2 one by one.
        
        # To ensure we don't exceed time, we'll just try to expand the 1x1 
        # to a slightly larger rectangle if possible.
        
        # Let's try to expand the rectangle to reach target_r
        # We'll try to grow the rectangle by increasing x2, then x1, then y2, then y1.
        
        def is_valid(x1, y1, x2, y2):
            if x1 < 0 or y1 < 0 or x2 > BOARD_SIZE or y2 > BOARD_SIZE:
                return False
            if x1 >= x2 or y1 >= y2:
                return False
            if not (x1 <= target_x < x2 and y1 <= target_y < y2):
                return False
            for (rx1, ry1, rx2, ry2) in placed_rects:
                # Check for overlap: not (rect1.x2 <= rect2.x1 or rect1.x1 >= rect2.x2 or ...)
                if not (x2 <= rx1 or x1 >= rx2 or y2 <= ry1 or y1 >= ry2):
                    return False
            return True

        # Try to expand the rectangle greedily
        # We'll try to increase the area by expanding boundaries.
        # To keep it efficient, we'll try to expand in steps.
        
        cx1, cy1, cx2, cy2 = target_x, target_y, target_x + 1, target_y + 1
        if is_valid(cx1, cy1, cx2, cy2):
            # Try to expand
            # We'll try to expand the rectangle to reach target_r
            # We'll use a simple greedy: try to expand x2, then x1, then y2, then y1
            # in steps of 1.
            
            # To avoid TLE, we limit the number of expansion attempts.
            # Since N is up to 1000, we can't do too many.
            # Let's try to expand in larger steps.
            
            step = 1
            while True:
                expanded = False
                # Try expanding each side
                # Order: x2, x1, y2, y1
                for dx1, dy1, dx2, dy2 in [(0,0,step,0), (-step,0,0,0), (0,0,0,step), (0,-step,0,0)]:
                    nx1, ny1, nx2, ny2 = cx1 + dx1, cy1 + dy1, cx2 + dx2, cy2 + dy2
                    if is_valid(nx1, ny1, nx2, ny2):
                        # Check if this expansion is "good" (doesn't overshoot area too much)
                        # Actually, just expand if it's valid and doesn't exceed target_r too much.
                        # But the problem says "close to r_i", so larger is better.
                        # However, we must not overlap.
                        cx1, cy1, cx2, cy2 = nx1, ny1, nx2, ny2
                        expanded = True
                        break
                if not expanded:
                    # If we can't expand by 'step', try smaller steps or stop
                    if step > 1:
                        step //= 2
                        continue
                    else:
                        break
                # If we expanded, try to increase step size to grow faster
                if step < 100:
                    step += 1
                else:
                    step += 10
            
            best_x1, best_y1, best_x2, best_y2 = cx1, cy1, cx2, cy2
        
        results[adv['id']] = (best_x1, best_y1, best_x2, best_y2)
        placed_rects.append((best_x1, best_y1, best_x2, best_y2))

    for res in results:
        print(f"{res[0]} {res[1]} {res[2]} {res[3]}")

if __name__ == "__main__":
    solve()
