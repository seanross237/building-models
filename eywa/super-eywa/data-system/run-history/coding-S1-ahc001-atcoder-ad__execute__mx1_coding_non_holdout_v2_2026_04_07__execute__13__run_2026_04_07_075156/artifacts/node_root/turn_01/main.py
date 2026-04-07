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

    for i in range(N):
        x, y, r = advertisers[i]
        print(f"{x} {y} {x+1} {y+1}")

if __name__ == "__main__":
    solve()