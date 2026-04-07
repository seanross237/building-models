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
        advertisers.append({'x': x, 'y': y, 'r': r, 'id': i})
        idx += 3

    # Sort advertisers by area descending to place larger ones first
    # This is a common heuristic for packing problems.
    sorted_advs = sorted(advertisers, key=lambda a: a['r'], reverse=True)

    results = [None] * N
    # We use a simple grid-based or list-based collision check.
    # Since N is not explicitly bounded but the board is 10000x10000,
    # we'll store placed rectangles and check against them.
    placed_rects = []

    for adv in sorted_advs:
        x, y, r = adv['x'], adv['y'], adv['r']
        target_side = int(r**0.5)
        if target_side < 1: target_side = 1
        
        # We want to find [x1, x2) x [y1, y2) such that:
        # 1. 0 <= x1 <= x < x2 <= 10000
        # 2. 0 <= y1 <= y < y2 <= 10000
        # 3. (x2-x1)*(y2-y1) is close to r
        # 4. No overlap with placed_rects
        
        found = False
        # Try to find a valid rectangle by expanding from the point (x, y)
        # We try different side lengths and offsets.
        # To keep it simple and fast, we try to find the largest possible square 
        # centered around (x, y) that doesn't collide.
        
        # Strategy: Start with a 1x1 rectangle containing (x,y) and expand.
        # Or more simply: try to fit a square of side 'target_side'.
        # We'll try a few candidate rectangles.
        
        candidates = []
        # Candidate 1: Smallest possible square containing (x,y)
        # [x, x+1) x [y, y+1)
        candidates.append((x, y, x + 1, y + 1))
        
        # Candidate 2: Target square centered at (x,y)
        half = target_side // 2
        x1_c = max(0, x - half)
        x2_c = min(10000, x1_c + target_side)
        if x2_c <= x: # adjust if x is at the edge
            x1_c = max(0, x2_c - target_side)
            x2_c = min(10000, x1_c + target_side)
        if x1_c > x: # ensure x is inside
            x1_c = x
            x2_c = min(10000, x1_c + target_side)
            
        y1_c = max(0, y - half)
        y2_c = min(10000, y1_c + target_side)
        if y2_c <= y:
            y1_c = max(0, y2_c - target_side)
            y2_c = min(10000, y1_c + target_side)
        if y1_c > y:
            y1_c = y
            y2_c = min(10000, y1_c + target_side)
            
        # Ensure x and y are strictly inside [x1, x2) and [y1, y2)
        # The problem says "contains its requested point (x_i, y_i)".
        # Usually this means x1 <= x < x2.
        if x1_c <= x < x2_c and y1_c <= y < y2_c:
            candidates.append((x1_c, y1_c, x2_c, y2_c))

        # Candidate 3: A very small rectangle to guarantee something fits
        candidates.append((x, y, x + 1, y + 1))

        best_rect = None
        max_score = -1
        
        for cx1, cy1, cx2, cy2 in candidates:
            # Check bounds
            if not (0 <= cx1 <= x < cx2 <= 10000 and 0 <= cy1 <= y < cy2 <= 10000):
                continue
            
            # Check overlap
            overlap = False
            for rx1, ry1, rx2, ry2 in placed_rects:
                if not (cx2 <= rx1 or cx1 >= rx2 or cy2 <= ry1 or cy1 >= ry2):
                    overlap = True
                    break
            
            if not overlap:
                # Score is how close area is to r
                area = (cx2 - cx1) * (cy2 - cy1)
                score = -abs(area - r)
                if score > max_score:
                    max_score = score
                    best_rect = (cx1, cy1, cx2, cy2)
        
        # If no candidate works, try to find ANY valid tiny rectangle
        if best_rect is None:
            # Try to find a 1x1 that doesn't overlap
            # We check a small neighborhood around (x,y)
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    tx1, ty1 = x + dx, y + dy
                    tx2, ty2 = tx1 + 1, ty1 + 1
                    if 0 <= tx1 <= x < tx2 <= 10000 and 0 <= ty1 <= y < ty2 <= 10000:
                        overlap = False
                        for rx1, ry1, rx2, ry2 in placed_rects:
                            if not (tx2 <= rx1 or tx1 >= rx2 or ty2 <= ry1 or ty1 >= ry2):
                                overlap = True
                                break
                        if not overlap:
                            best_rect = (tx1, ty1, tx2, ty2)
                            break
                if best_rect: break

        if best_rect:
            results[adv['id']] = best_rect
            placed_rects.append(best_rect)
        else:
            # Fallback: a 1x1 rectangle that must contain (x,y)
            # If even this overlaps, we have to output something valid but potentially 0 score
            # The problem says "overlapping rectangles make the score collapse to zero".
            # To avoid zero score, we must not overlap.
            # If we can't find a non-overlapping one, we'll just output a 1x1 at (x,y) 
            # and accept the penalty, but we must ensure it's within bounds.
            tx1, ty1 = max(0, min(x, 9999)), max(0, min(y, 9999))
            tx2, ty2 = tx1 + 1, ty1 + 1
            results[adv['id']] = (tx1, ty1, tx2, ty2)

    for res in results:
        print(f"{res[0]} {res[1]} {res[2]} {res[3]}")

if __name__ == "__main__":
    solve()
