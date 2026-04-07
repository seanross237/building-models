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

    targets.sort()
    existing = [(0, 0)]
    total_cost = 0

    for tx, ty in targets:
        best_source = None
        min_dist = float('inf')
        for fx, fy in existing:
            if tx >= fx and ty >= fy:
                dist = (tx - fx) + (ty - fy)
                if dist < min_dist:
                    min_dist = dist
                    best_source = (fx, fy)
        
        if best_source:
            total_cost += min_dist
            existing.append((tx, ty))

    print(total_cost)

if __name__ == '__main__':
    solve()