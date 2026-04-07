import sys

def solve():
    line = sys.stdin.readline()
    if not line:
        return
    try:
        n = int(line.strip())
    except ValueError:
        return

    targets = []
    for _ in range(n):
        line = sys.stdin.readline()
        if not line:
            break
        targets.append(list(map(int, line.split())))

    targets.sort(key=lambda p: (p[0] + p[1], p[0], p[1]))

    current_x, current_y = 0, 0
    operations = []
    created_beverages = [(0, 0)]

    for tx, ty in targets:
        best_f = None
        min_dist = float('inf')

        for fx, fy in created_beverages:
            if fx <= tx and fy <= ty:
                dist = (tx - fx) + (ty - fy)
                if dist < min_dist:
                    min_dist = dist
                    best_f = (fx, fy)
        
        if best_f is not None:
            fx, fy = best_f
            if fx == tx and fy == ty:
                continue
            operations.append((fx, fy, tx, ty))
            created_beverages.append((tx, ty))

    for op in operations:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == '__main__':
    solve()