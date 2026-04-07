import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    advertisers = []
    idx = 1
    for i in range(N):
        x = int(float(input_data[idx]))
        y = int(float(input_data[idx+1]))
        r = int(float(input_data[idx+2]))
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
        s_target = target_r**0.5
        
        def get_rect(side):
            half = side / 2.0
            x1 = max(0.0, cx - half)
            x2 = min(10000.0, cx + half)
            y1 = max(0.0, cy - half)
            y2 = min(10000.0, cy + half)
            
            # Ensure cx, cy is strictly inside [x1, x2) and [y1, y2)
            # The problem requires x1 <= cx < x2 and y1 <= cy < y2
            # If cx is at the boundary, we must shift the rectangle slightly
            if not (x1 <= cx < x2):
                if cx == 0: x1, x2 = 0.0, 1.0
                elif cx == 10000: x1, x2 = 9999.0, 10000.0
                else: x1, x2 = cx - 0.5, cx + 0.5
            if not (y1 <= cy < y2):
                if cy == 0: y1, y2 = 0.0, 1.0
                elif cy == 10000: y1, y2 = 9999.0, 10000.0
                else: y1, y2 = cy - 0.5, cy + 0.5
                
            return [x1, y1, x2, y2]

        def is_valid(rect):
            if rect[0] >= rect[2] or rect[1] >= rect[3]: return False
            # Check bounds
            if rect[0] < 0 or rect[2] > 10000 or rect[1] < 0 or rect[3] > 10000: return False
            # Check point containment
            if not (rect[0] <= cx < rect[2] and rect[1] <= cy < rect[3]): return False
            for pr in placed_rects:
                if intersects(rect, pr):
                    return False
            return True

        # Binary search for the largest side length
        best_side = 0.0
        L, R = 0.0, 10000.0
        # Use a small epsilon to ensure we find a valid tiny rectangle if needed
        for _ in range(30):
            mid = (L + R) / 2.0
            rect = get_rect(mid)
            if is_valid(rect):
                best_side = mid
                L = mid
            else:
                R = mid
        
        # If even a tiny square fails, try a minimal valid rectangle
        res_rect = get_rect(best_side)
        if not is_valid(res_rect):
            # Fallback to a 1x1 or minimal rectangle containing (cx, cy)
            x1 = max(0.0, cx - 0.1)
            x2 = min(10000.0, cx + 0.9)
            if x1 >= x2: # handle edge cases
                if cx == 0: x1, x2 = 0.0, 1.0
                else: x1, x2 = cx - 1.0, cx + 0.0
            
            y1 = max(0.0, cy - 0.1)
            y2 = min(10000.0, cy + 0.9)
            if y1 >= y2:
                if cy == 0: y1, y2 = 0.0, 1.0
                else: y1, y2 = cy - 1.0, cy + 0.0
            
            res_rect = [x1, y1, x2, y2]
            # Final safety check: if still invalid, use a point-like rect
            if not is_valid(res_rect):
                res_rect = [cx, cy, cx + 1e-7, cy + 1e-7]
                # If cx is 10000, adjust
                if cx >= 10000: res_rect = [cx-1e-7, cy, cx, cy+1e-7]
                if cy >= 10000: res_rect = [cx, cy-1e-7, cx+1e-7, cy]

        final_rects[adv['id']] = res_rect
        placed_rects.append(res_rect)

    for r in final_rects:
        # The scorer expects integers based on the error message
        # "failed to parse the input 3830.000000 to the value of type i64"
        # This means the output must be integers.
        print(f"{int(r[0])} {int(r[1])} {int(r[2])} {int(r[3])}")

if __name__ == "__main__":
    solve()
