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

    # Sort targets primarily by x, then by y.
    # This ensures that when we process a target, we have already processed
    # potential "predecessor" targets with smaller x and y.
    targets.sort()

    # We start with (0, 0)
    existing_beverages = [(0, 0)]
    operations = []

    for tx, ty in targets:
        # If the target is (0,0), it's already "created" by the start condition.
        if tx == 0 and ty == 0:
            continue

        best_dist = float('inf')
        best_prev = None

        # Find the existing beverage (fx, fy) that minimizes (tx-fx) + (ty-fy)
        # subject to fx <= tx and fy <= ty.
        # This is equivalent to maximizing (fx + fy).
        for fx, fy in existing_beverages:
            if fx <= tx and fy <= ty:
                dist = (tx - fx) + (ty - fy)
                if dist < best_dist:
                    best_dist = dist
                    best_prev = (fx, fy)
                elif dist == best_dist:
                    # Tie-break: pick the one with larger coordinates to keep the tree "dense"
                    if best_prev is None or (fx + fy > best_prev[0] + best_prev[1]):
                        best_prev = (fx, fy)

        if best_prev is not None:
            fx, fy = best_prev
            operations.append((fx, fy, tx, ty))
            existing_beverages.append((tx, ty))
        else:
            # This case should not be reachable given (0,0) is always in existing_beverages
            # and targets are non-negative.
            pass

    # Output the number of operations
    print(len(operations))
    # Output each operation
    for op in operations:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == "__main__":
    solve()
