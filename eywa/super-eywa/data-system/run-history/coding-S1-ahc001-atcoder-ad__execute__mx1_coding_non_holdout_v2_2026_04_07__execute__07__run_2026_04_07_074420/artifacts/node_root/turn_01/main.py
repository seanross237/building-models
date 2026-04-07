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
        advertisers.append((x, y, r))
        idx += 3

    strip_height = 10000 // N
    
    for i in range(N):
        x, y, r = advertisers[i]
        y_min_strip = i * strip_height
        y_max_strip = (i + 1) * strip_height if i < N - 1 else 10000
        side = int(r**0.5)
        x1 = max(0, x - side // 2)
        x2 = min(10000, x + side // 2 + 1)
        if not (x1 <= x < x2):
            if x1 > x: x1 = x
            if x2 <= x: x2 = x + 1
        y1 = max(y_min_strip, y - side // 2)
        y2 = min(y_max_strip, y + side // 2 + 1)
        if not (y1 <= y < y2):
            if y1 > y: y1 = y
            if y2 <= y: y2 = y + 1
        if x1 >= x2: x2 = x1 + 1
        if y1 >= y2: y2 = y1 + 1
        if x2 > 10000: x2 = 10000
        if y2 > 10000: y2 = 10000
        print(f"{x1} {y1} {x2} {y2}")

solve()