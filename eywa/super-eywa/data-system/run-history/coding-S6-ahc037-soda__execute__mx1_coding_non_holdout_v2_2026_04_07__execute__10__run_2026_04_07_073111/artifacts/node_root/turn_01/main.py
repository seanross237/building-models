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
        best_f = None
        min_dist = float('inf')

        for fx, fy in existing_beverages:
            if fx <= tx and fy <= ty:
                dist = (tx - fx) + (ty - fy)
                if dist < min_dist:
                    min_dist = dist
                    best_f = (fx, fy)
                elif dist == min_dist:
                    if best_f is None or (fx + fy > best_f[0] + best_f[1]):
                        best_f = (fx, fy)

        if best_f is not None:
            fx, fy = best_f
            operations.append((fx, fy, tx, ty))
            existing_beverages.append((tx, ty))

    print(len(operations))
    for op in operations:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == "__main__":
    solve()