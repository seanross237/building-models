import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    targets = []
    idx = 1
    for _ in range(n):
        x = int(input_data[idx])
        y = int(input_data[idx+1])
        targets.append((x, y))
        idx += 2
    
    # A simple valid baseline: create each target directly from (0,0)
    # This ensures every 'from' coordinate (0,0) is valid.
    print(n)
    for tx, ty in targets:
        print(f"0 0 {tx} {ty}")

if __name__ == "__main__":
    solve()