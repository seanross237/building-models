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

    targets.sort()

    existing_beverages = [(0, 0)]
    operations = []

    for tx, ty in targets:
        if tx == 0 and ty == 0:
            continue

        best_dist = float('inf')
        best_prev = None

        for fx, fy in existing_beverages:
            if fx <= tx and fy <= ty:
                dist = (tx - fx) + (ty - fy)
                if dist < best_dist:
                    best_dist = dist
                    best_prev = (fx, fy)
        
        if best_prev is not None:
            operations.append((best_prev[0], best_prev[1], tx, ty))
            existing_beverages.append((tx, ty))

    print(len(operations))
    for op in operations:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

solve()