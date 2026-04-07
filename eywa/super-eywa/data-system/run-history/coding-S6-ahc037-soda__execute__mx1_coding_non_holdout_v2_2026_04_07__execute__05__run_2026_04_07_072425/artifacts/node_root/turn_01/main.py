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

    # Sort targets to process them in a way that respects the non-decreasing constraint
    # Sorting by x then y helps in finding valid predecessors easily.
    targets.sort()

    # existing_beverages stores (x, y) of beverages already created
    # We start with (0, 0)
    existing_beverages = [(0, 0)]
    operations = []

    for tx, ty in targets:
        # Check if (tx, ty) is already in existing_beverages (though targets are unique in problem usually)
        # But we must ensure we don't create a duplicate if it's already (0,0)
        if tx == 0 and ty == 0:
            continue
            
        best_dist = float('inf')
        best_source = None

        # Find the best source (fx, fy) such that fx <= tx and fy <= ty
        # to minimize (tx - fx) + (ty - fy)
        for fx, fy in existing_beverages:
            if fx <= tx and fy <= ty:
                dist = (tx - fx) + (ty - fy)
                if dist < best_dist:
                    best_dist = dist
                    best_source = (fx, fy)
        
        # If no valid source found (shouldn't happen as (0,0) is always valid),
        # we'd have a problem. But with (0,0) and tx, ty >= 0, (0,0) is always a candidate.
        if best_source is not None:
            fx, fy = best_source
            operations.append((fx, fy, tx, ty))
            existing_beverages.append((tx, ty))

    # Output the number of operations and each operation
    print(len(operations))
    for op in operations:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == "__main__":
    solve()