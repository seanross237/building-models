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

        best_source = None
        min_cost = float('inf')

        for fx, fy in existing_beverages:
            if fx <= tx and fy <= ty:
                cost = (tx - fx) + (ty - fy)
                if cost < min_cost:
                    min_cost = cost
                    best_source = (fx, fy)
        
        if best_source:
            fx, fy = best_source
            operations.append((fx, fy, tx, ty))
            existing_beverages.append((tx, ty))

    total_cost = sum(op[2]-op[0] + op[3]-op[1] for op in operations)
    print(total_cost)