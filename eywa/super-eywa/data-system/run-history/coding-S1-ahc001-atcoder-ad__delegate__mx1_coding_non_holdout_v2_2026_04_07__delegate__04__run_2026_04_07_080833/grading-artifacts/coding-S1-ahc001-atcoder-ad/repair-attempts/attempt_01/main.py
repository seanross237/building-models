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

    # Sort by target area descending to prioritize larger ones
    sorted_adv = sorted(advertisers, key=lambda a: a['r'], reverse=True)
    
    # rects[i] will store (x1, y1, x2, y2) for advertiser i
    rects = [None] * N
    # List of already placed rectangles to check for overlaps
    placed_rects = []

    def intersects(r1, r2):
        # r = (x1, y1, x2, y2)
        # Check if rectangles [x1, x2) x [y1, y2) overlap
        return not (r1[2] <= r2[0] or r1[0] >= r2[2] or r1[3] <= r2[1] or r1[1] >= r2[3])

    for adv in sorted_adv:
        target_area = adv['r']
        px, py = adv['x'], adv['y']
        
        # We want to find a rectangle [x1, x2) x [y1, y2) such that:
        # 0 <= x1 <= px < x2 <= 10000
        # 0 <= y1 <= py < y2 <= 10000
        # (x2-x1)*(y2-y1) is close to target_area
        # No overlap with placed_rects
        
        # Start with a tiny rectangle around the point
        # Using a very small epsilon to ensure the point is strictly inside [x1, x2)
        eps = 1e-7
        best_x1, best_y1, best_x2, best_y2 = px, py, px + eps, py + eps
        best_area = 0.0
        
        # Heuristic: Try to expand in a grid-like search or simple expansion
        # Since we need a valid solution, let's try to grow a square-ish rectangle
        # We'll try to find the largest side 's' such that a square [px-s/2, px+s/2] works
        # But the point must be inside, so we use a simpler approach:
        # Try to find a rectangle that is as close to target_area as possible.
        
        # Let's try a simple greedy expansion:
        # We'll try to find the largest possible square centered at (px, py)
        # that doesn't overlap and stays in bounds.
        
        # To make it faster and more robust, we'll try to find the largest s
        # such that [px-s, px+s] x [py-s, py+s] is valid.
        # But the problem allows any rectangle. Let's try to expand x and y.
        
        # Simple approach: Try to find a rectangle [x1, x2] x [y1, y2]
        # where x1=px, x2=px+s, y1=py, y2=py+s.
        # We'll try different side lengths.
        
        # Binary search for side length s
        low = 0.0
        high = 10000.0
        for _ in range(40):
            mid = (low + high) / 2
            # Try a square [px-mid, px+mid] x [py-mid, py+mid]
            # But we must ensure px is in [x1, x2) and py is in [y1, y2)
            # and bounds are [0, 10000]
            x1 = max(0.0, px - mid)
            x2 = min(10000.0, px + mid)
            y1 = max(0.0, py - mid)
            y2 = min(10000.0, py + mid)
            
            # Ensure point is strictly inside
            if x1 == px: x1 -= eps
            if x2 == px: x2 += eps
            if y1 == py: y1 -= eps
            if y2 == py: y2 += eps
            
            # Clamp to bounds
            x1 = max(0.0, x1)
            x2 = min(10000.0, x2)
            y1 = max(0.0, y1)
            y2 = min(10000.0, y2)
            
            if x1 >= x2 or y1 >= y2:
                high = mid
                continue

            current_rect = (x1, y1, x2, y2)
            overlap = False
            for pr in placed_rects:
                if intersects(current_rect, pr):
                    overlap = True
                    break
            
            if not overlap:
                low = mid
                best_x1, best_y1, best_x2, best_y2 = x1, y1, x2, y2
                best_area = (x2 - x1) * (y2 - y1)
            else:
                high = mid
        
        # If the square approach is too restrictive, we just use the tiny rect
        # to ensure we always output something valid.
        rects[adv['id']] = (best_x1, best_y1, best_x2, best_y2)
        placed_rects.append((best_x1, best_y1, best_x2, best_y2))

    for r in rects:
        print(f"{r[0]:.10f} {r[1]:.10f} {r[2]:.10f} {r[3]:.10f}")

if __name__ == "__main__":
    solve()
