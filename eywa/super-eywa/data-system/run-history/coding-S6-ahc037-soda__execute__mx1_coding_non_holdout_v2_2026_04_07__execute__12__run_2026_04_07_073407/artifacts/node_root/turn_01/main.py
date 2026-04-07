import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    targets = []
    idx = 1
    for _ in range(N):
        a = int(input_data[idx])
        b = int(input_data[idx+1])
        targets.append((a, b))
        idx += 2

    sorted_targets = sorted(targets, key=lambda p: (p[0], p[1]))
    existing = [(0, 0)]
    operations = []
    sorted_targets = sorted(targets, key=lambda p: (p[0], p[1]))