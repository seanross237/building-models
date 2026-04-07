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

    # Sort targets to process them in an order that respects monotonicity
    # Sorting by x then y helps in building a chain or tree.
    targets.sort()

    # existing_beverages stores (x, y) coordinates of beverages already created
    existing_beverages = [(0, 0)]
    operations = []

    for tx, ty in targets:
        # Check if this target is already created (e.g., if (0,0) is a target)
        if (tx, ty) in existing_beverages:
            continue
            
        # Find the best existing beverage (fx, fy) such that fx <= tx and fy <= ty
        # and (tx - fx) + (ty - fy) is minimized.
        best_f = None
        min_dist = float('inf')

        for fx, fy in existing_beverages:
            if fx <= tx and fy <= ty:
                dist = (tx - fx) + (ty - fy)
                if dist < min_dist:
                    min_dist = dist
                    best_f = (fx, fy)
        
        # If no such beverage is found (shouldn't happen because (0,0) is always there and tx,ty >= 0)
        # but for robustness, we handle it.
        if best_f is None:
            # This case shouldn't be reachable given problem constraints (tx, ty >= 0)
            # but we'll just use (0,0) if needed.
            best_f = (0, 0)
            min_dist = tx + ty

        operations.append((best_f[0], best_f[1], tx, ty))
        existing_beverages.append((tx, ty))

    # Output the number of operations and each operation
    print(len(operations))
    for op in operations:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == "__main__":
    solve()