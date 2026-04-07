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
        
        # Start with a minimal rectangle containing the point [x, x+1) x [y, y+1)
        # Note: The problem says rectangle must contain (x, y). 
        # In [x1, x2) x [y1, y2), the point (x, y) is contained if x1 <= x < x2 and y1 <= y < y2.
        # To be safe and simple, we use [x, x+1) x [y, y+1).
        
        best_x1, best_y1, best_x2, best_y2 = x, y, x + 1, y + 1
        max_area_found = 0
        
        # Heuristic: Try to expand around the point (x, y)
        # We'll try to find a rectangle that maximizes area <= target_r without collision
        # Since N is small or time is limited, we use a simple greedy expansion.
        
        # Try to find a square-ish rectangle
        side = int(target_r**0.5)
        if side < 1: side = 1
        
        # We try several possible widths and heights to find a good fit
        # To keep it efficient, we'll just try to expand the current rect greedily
        curr_x1, curr_y1, curr_x2, curr_y2 = x, y, x + 1, y + 1
        
        # Greedy expansion: try to grow in 4 directions
        # Directions: Up, Down, Left, Right
        # We'll do a simple loop to expand
        for _ in range(200): # Limit iterations for speed
            expanded = False
            # Try expanding width or height
            # We check 4 directions: x1, x2, y1, y2
            # To keep it simple, let's try to expand the bounding box
            
            # Try expanding x2
            tx2 = curr_x2 + 1
            if tx2 <= 10000:
                nr = (curr_x1, curr_y1, tx2, curr_y2)
                if not any(intersects(nr, pr) for pr in placed_rects):
                    if (tx2 - curr_x1) * (curr_y2 - curr_y1) <= target_r * 1.5: # Allow some overshoot
                        curr_x2 = tx2
                        expanded = True
            
            # Try expanding x1
            tx1 = curr_x1 - 1
            if tx1 >= 0:
                nr = (tx1, curr_y1, curr_x2, curr_y2)
                if not any(intersects(nr, pr) for pr in placed_rects):
                    if (curr_x2 - tx1) * (curr_y2 - curr_y1) <= target_r * 1.5:
                        curr_x1 = tx1
                        expanded = True

            # Try expanding y2
            ty2 = curr_y2 + 1
            if ty2 <= 10000:
                nr = (curr_x1, curr_y1, curr_x2, ty2)
                if not any(intersects(nr, pr) for pr in placed_rects):
                    if (curr_x2 - curr_x1) * (ty2 - curr_y1) <= target_r * 1.5:
                        curr_y2 = ty2
                        expanded = True

            # Try expanding y1
            ty1 = curr_y1 - 1
            if ty1 >= 0:
                nr = (curr_x1, ty1, curr_x2, curr_y2)
                if not any(intersects(nr, pr) for pr in placed_rects):
                    if (curr_x2 - curr_x1) * (curr_y2 - ty1) <= target_r * 1.5:
                        curr_y1 = ty1
                        expanded = True
            
            if not expanded:
                break
        
        # Final check: ensure it contains (x,y) and is within bounds
        # (Already ensured by starting at x,y and expanding)
        res = (curr_x1, curr_y1, curr_x2, curr_y2)
        results[adv['id']] = res
        placed_rects.append(res)

    for r in results:
        print(f"{r[0]} {r[1]} {r[2]} {r[3]}")

if __name__ == "__main__":
    solve()
