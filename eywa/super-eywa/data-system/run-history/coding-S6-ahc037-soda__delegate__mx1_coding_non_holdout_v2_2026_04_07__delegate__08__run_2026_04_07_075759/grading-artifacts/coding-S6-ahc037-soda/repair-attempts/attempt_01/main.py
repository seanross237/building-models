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

    # Sort targets to ensure monotonicity is easier to satisfy.
    # Sorting by x then y ensures that for any target i, 
    # there might be a target j < i such that x_j <= x_i and y_j <= y_i.
    targets.sort()

    # existing_beverages stores (x, y) of beverages already created.
    # We start with (0, 0).
    existing_beverages = [(0, 0)]
    operations = []

    for tx, ty in targets:
        best_parent = None
        min_dist = float('inf')

        # Find the best existing beverage to create the current target.
        # The constraint is tx >= fx and ty >= fy.
        # To minimize cost (tx-fx) + (ty-fy), we want to maximize fx + fy
        # subject to fx <= tx and fy <= ty.
        for fx, fy in existing_beverages:
            if fx <= tx and fy <= ty:
                dist = (tx - fx) + (ty - fy)
                if dist < min_dist:
                    min_dist = dist
                    best_parent = (fx, fy)
                elif dist == min_dist:
                    # Tie-break: prefer parent with larger coordinates to help future targets
                    if fx + fy > best_parent[0] + best_parent[1]:
                        best_parent = (fx, fy)

        if best_parent:
            fx, fy = best_parent
            operations.append((fx, fy, tx, ty))
            existing_beverages.append((tx, ty))
        else:
            # This case should theoretically not happen if (0,0) is always available
            # and targets are non-negative, but for robustness:
            # If no parent found, we must connect from (0,0) if possible, 
            # but the problem implies tx, ty >= 0.
            # If tx, ty are both >= 0, (0,0) is always a valid parent.
            operations.append((0, 0, tx, ty))
            existing_beverages.append((tx, ty))

    # Output the number of operations
    print(len(operations))
    # Output each operation
    for op in operations:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == "__main__":
    solve()
