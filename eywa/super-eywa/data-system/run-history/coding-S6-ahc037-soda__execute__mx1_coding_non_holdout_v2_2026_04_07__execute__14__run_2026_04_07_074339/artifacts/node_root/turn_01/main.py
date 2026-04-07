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
    sorted_targets = sorted(targets, key=lambda p: (p[0] + p[1]))
    
    for tx, ty in sorted_targets:
        if tx == 0 and ty == 0:
            continue
        best_parent = (0, 0)
        min_dist = tx + ty
        for ex, ey in existing_beverages:
            if ex <= tx and ey <= ty:
                dist = (tx - ex) + (ty - ey)
                if dist < min_dist:
                    min_dist = dist
                    best_parent = (ex, ey)
        operations.append((best_parent, (tx, ty)))
        existing_beverages.append((tx, ty))
    
    print(sum(op[1][0] - op[0][0] + op[1][1] - op[0][1] for op in operations))

solve()