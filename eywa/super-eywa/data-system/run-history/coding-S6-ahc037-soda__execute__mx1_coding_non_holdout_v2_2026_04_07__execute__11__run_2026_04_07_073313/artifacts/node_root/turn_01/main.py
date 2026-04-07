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

    existing = [(0, 0)]
    sorted_targets = sorted(targets)
    
    operations = []
    available = [(0, 0)]
    
    for tx, ty in sorted_targets:
        best_dist = float('inf')
        best_source = None
        
        for fx, fy in available:
            if fx <= tx and fy <= ty:
                dist = (tx - fx) + (ty - fy)
                if dist < best_dist:
                    best_dist = dist
                    best_source = (fx, fy)
        
        if best_source is not None:
            operations.append((best_source[0], best_source[1], tx, ty))
            available.append((tx, ty))

    print(len(operations))
    for op in operations:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

solve()