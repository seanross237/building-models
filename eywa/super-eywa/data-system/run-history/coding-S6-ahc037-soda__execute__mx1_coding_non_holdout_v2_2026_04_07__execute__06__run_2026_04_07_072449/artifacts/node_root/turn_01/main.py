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

    targets.sort(key=lambda p: (p[0] + p[1]))

    existing = [(0, 0)]
    operations = []

    for tx, ty in targets:
        best_parent = None
        min_dist = float('inf')

        for fx, fy in existing:
            if fx <= tx and fy <= ty:
                dist = (tx - fx) + (ty - fy)
                if dist < min_dist:
                    min_dist = dist
                    best_parent = (fx, fy)
        
        if best_parent is not None:
            fx, fy = best_parent
            if (tx, ty) != (fx, fy):
                operations.append((fx, fy, tx, ty))
                existing.append((tx, ty))
