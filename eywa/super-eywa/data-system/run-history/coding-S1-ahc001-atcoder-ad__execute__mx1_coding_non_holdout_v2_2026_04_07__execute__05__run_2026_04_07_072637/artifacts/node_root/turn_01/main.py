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

    sorted_indices = sorted(range(N), key=lambda i: advertisers[i][1])
    
    for i in range(N):
        idx_orig = sorted_indices[i]
        x, y, r = advertisers[idx_orig]
        print(f"{x} {x+1} {y} {y+1}")

if __name__ == "__main__":
    solve()