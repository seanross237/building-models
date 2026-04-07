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

    used_points = set()
    for x, y, r in advertisers:
        curr_x, curr_y = x, y
        while (curr_x, curr_y) in used_points:
            curr_x += 1
            if curr_x >= 10000:
                curr_x = x
                curr_y += 1
        
        used_points.add((curr_x, curr_y))
        print(f"{curr_x} {curr_x+1} {curr_y} {curr_y+1}")