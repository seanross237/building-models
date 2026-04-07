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

    sorted_targets = sorted(targets, key=lambda p: (p[0] + p[1]))
    
    existing = [(0, 0)]
    operations = []
    
    for tx, ty in sorted_targets:
        best_dist = float('inf')
        best_source = None
        
        for fx, fy in existing:
            if fx <= tx and fy <= ty:
                dist = (tx - fx) + (ty - fy)
                if dist < best_dist:
                    best_dist = dist
                    best_source = (fx, fy)
        
        if best_source is not None:
            fx, fy = best_source
            operations.append((fx, fy, tx, ty))
            existing.append((tx, ty))
