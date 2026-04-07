import sys
from random import shuffle, seed

def main():
    input_data = sys.stdin.buffer.read().decode()
    tokens = input_data.split()
    idx = 0
    N = int(tokens[idx]); idx += 1

    pts = []
    for i in range(N):
        x = int(tokens[idx]); idx += 1
        y = int(tokens[idx]); idx += 1
        r = int(tokens[idx]); idx += 1
        pts.append((x, y, r))

    # Initialize each rectangle as a 1x1 box containing the point
    rects = []
    for i in range(N):
        x, y, r = pts[i]
        x1 = x
        y1 = y
        x2 = x + 1
        y2 = y + 1
        rects.append([x1, y1, x2, y2])

    def overlaps(a, b):
        if a[0] >= b[2] or b[0] >= a[2]:
            return False
        if a[1] >= b[3] or b[1] >= a[3]:
            return False
        return True

    def rect_area(r):
        return (r[2] - r[0]) * (r[3] - r[1])

    def can_expand(i, new_rect):
        if new_rect[0] < 0 or new_rect[1] < 0 or new_rect[2] > 10000 or new_rect[3] > 10000:
            return False
        for j in range(N):
            if j == i:
                continue
            if overlaps(new_rect, rects[j]):
                return False
        return True

    seed(42)
    
    # Build spatial index for faster overlap checking
    # But for simplicity with N likely <= 200, brute force should work
    
    for iteration in range(300):
        order = list(range(N))
        shuffle(order)
        any_changed = False
        for i in order:
            x, y, r = pts[i]
            cur_area = rect_area(rects[i])
            if cur_area >= r:
                continue
            
            # Try expanding in each of 4 directions
            directions = [0, 1, 2, 3]
            shuffle(directions)
            
            for d in directions:
                cur_area = rect_area(rects[i])
                if cur_area >= r:
                    break
                
                new_rect = rects[i][:]
                if d == 0:  # expand left
                    new_rect[0] -= 1
                    if new_rect[0] < 0:
                        continue
                elif d == 1:  # expand up (decrease y1)
                    new_rect[1] -= 1
                    if new_rect[1] < 0:
                        continue
                elif d == 2:  # expand right
                    new_rect[2] += 1
                    if new_rect[2] > 10000:
                        continue
                elif d == 3:  # expand down (increase y2)
                    new_rect[3] += 1
                    if new_rect[3] > 10000:
                        continue
                
                # Must still contain the point
                if new_rect[0] > x or new_rect[2] <= x:
                    continue
                if new_rect[1] > y or new_rect[3] <= y:
                    continue
                
                if can_expand(i, new_rect):
                    rects[i] = new_rect
                    any_changed = True
        
        # Also try larger expansions for efficiency
        if iteration >= 50:
            for i in order:
                x, y, r = pts[i]
                cur_area = rect_area(rects[i])
                if cur_area >= r:
                    continue
                
                # Try expanding by larger steps
                step = max(1, int((r - cur_area) ** 0.5) // 4)
                if step <= 1:
                    continue
                
                for d in range(4):
                    new_rect = rects[i][:]
                    if d == 0:
                        new_rect[0] = max(0, new_rect[0] - step)
                    elif d == 1:
                        new_rect[1] = max(0, new_rect[1] - step)
                    elif d == 2:
                        new_rect[2] = min(10000, new_rect[2] + step)
                    elif d == 3:
                        new_rect[3] = min(10000, new_rect[3] + step)
                    
                    if new_rect[0] > x or new_rect[2] <= x:
                        continue
                    if new_rect[1] > y or new_rect[3] <= y:
                        continue
                    
                    if can_expand(i, new_rect):
                        rects[i] = new_rect
                        any_changed = True

        if not any_changed and iteration > 100:
            break

    out = []
    for i in range(N):
        out.append(f"{rects[i][0]} {rects[i][1]} {rects[i][2]} {rects[i][3]}")
    sys.stdout.write("\n".join(out) + "\n")

main()
