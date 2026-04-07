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

    board_size = 10000
    strip_height = board_size // N
    
    for i in range(N):
        x, y, r = advertisers[i]
        y_min_strip = i * strip_height
        y_max_strip = (i + 1) * strip_height if i < N - 1 else board_size
        print(f'0 {y_min_strip} 10000 {y_max_strip}')