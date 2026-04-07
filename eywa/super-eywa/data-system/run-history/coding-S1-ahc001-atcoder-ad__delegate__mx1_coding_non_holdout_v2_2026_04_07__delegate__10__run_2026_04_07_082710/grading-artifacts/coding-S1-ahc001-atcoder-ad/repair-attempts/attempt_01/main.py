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

    # Sort by target area descending to give larger ones more space
    sorted_adv = sorted(advertisers, key=lambda a: a['r'], reverse=True)
    
    final_rects = [None] * N
    placed_rects = []

    def intersects(r1, r2):
        # r = [x1, y1, x2, y2]
        return not (r1[2] <= r2[0] or r1[0] >= r2[2] or r1[3] <= r2[1] or r1[1] >= r2[3])

    for adv in sorted_adv:
        cx, cy = adv['x'], adv['y']
        target_r = adv['r']
        
        # Target side length for a square
        s = target_r**0.5
        
        # We try to find the largest possible square centered at (cx, cy)
        # that doesn't intersect existing rectangles and stays in bounds.
        # Since we want to maximize area, we'll try to expand a square.
        
        best_x1, best_y1, best_x2, best_y2 = cx, cy, cx + 1e-7, cy + 1e-7
        
        # Heuristic: Try to expand a square centered at (cx, cy)
        # We'll use a binary search or a simple step-based expansion to find max side length
        low = 0.0
        high = 10000.0
        
        # To ensure (cx, cy) is inside [x1, x2) and [y1, y2), 
        # we define the square as [cx - s/2, cx + s/2] but clipped to bounds.
        # However, the problem says (x, y) must be inside.
        # Let's try to build a square [cx - d, cx + d] x [cy - d, cy + d]
        # where d is the distance from center to edge.
        
        # Let's try a simpler approach: 
        # A square with side length 'side' centered at (cx, cy)
        # x1 = cx - side/2, x2 = cx + side/2, etc.
        # We must ensure 0 <= x1 < x2 <= 10000 and 0 <= y1 < y2 <= 10000
        
        def get_rect(side):
            half = side / 2.0
            x1 = max(0.0, cx - half)
            x2 = min(10000.0, cx + half)
            y1 = max(0.0, cy - half)
            y2 = min(10000.0, cy + half)
            # Ensure cx, cy is strictly inside
            if not (x1 <= cx < x2 and y1 <= cy < y2):
                # Adjust if cx or cy is on the boundary
                if x1 == cx: x1 = max(0.0, cx - 1e-7)
                if x2 == cx: x2 = min(10000.0, cx + 1e-7)
                if y1 == cy: y1 = max(0.0, cy - 1e-7)
                if y2 == cy: y2 = min(10000.0, cy + 1e-7)
            return [x1, y1, x2, y2]

        def is_valid(rect):
            if rect[0] >= rect[2] or rect[1] >= rect[3]: return False
            for pr in placed_rects:
                if intersects(rect, pr):
                    return False
            return True

        # Binary search for the largest side length
        best_side = 0.0
        L, R = 0.0, 10000.0
        for _ in range(40):
            mid = (L + R) / 2.0
            rect = get_rect(mid)
            if is_valid(rect):
                best_side = mid
                L = mid
            else:
                R = mid
        
        res_rect = get_rect(best_side)
        final_rects[adv['id']] = res_rect
        placed_rects.append(res_rect)

    for r in final_rects:
        print(f"{r[0]:.6f} {r[1]:.6f} {r[2]:.6f} {r[3]:.6f}")

if __name__ == "__main__":
    solve()
