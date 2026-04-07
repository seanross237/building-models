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

    existing = [(0, 0)]
    operations = []

    for tx, ty in targets:
        best_f = None
        min_dist = float('inf')

        for fx, fy in existing:
            if fx <= tx and fy <= ty:
                dist = (tx - fx) + (ty - fy)
                if dist < min_dist:
                    min_dist = dist
                    best_f = (fx, fy)
        
        if best_f is None:
            best_f = (0, 0)
            min_dist = tx + ty

        if not (tx == 0 and ty == 0):
            operations.append((best_f, (tx, ty)))
            existing.append((tx, ty))

    print(sum(op[1][0] - op[0][0] + op[1][1] - op[0][1] for op in operations))

solve()