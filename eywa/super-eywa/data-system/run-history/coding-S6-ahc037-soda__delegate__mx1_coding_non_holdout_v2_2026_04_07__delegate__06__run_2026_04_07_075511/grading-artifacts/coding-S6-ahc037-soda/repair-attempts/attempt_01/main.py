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

    # Sort targets by Manhattan distance (a + b) to ensure we process 
    # points closer to (0,0) first, which helps satisfy the monotonicity 
    # constraint (fx <= tx and fy <= ty) for subsequent points.
    targets.sort(key=lambda p: (p[0] + p[1]))

    # existing_beverages stores (x, y) of all beverages currently created.
    # We start with (0, 0).
    existing_beverages = [(0, 0)]
    operations = []

    for tx, ty in targets:
        best_dist = float('inf')
        best_source = None
        
        # For each target, find the existing beverage (fx, fy) that:
        # 1. Satisfies monotonicity: fx <= tx and fy <= ty
        # 2. Minimizes Manhattan distance: (tx - fx) + (ty - fy)
        for fx, fy in existing_beverages:
            if fx <= tx and fy <= ty:
                dist = (tx - fx) + (ty - fy)
                if dist < best_dist:
                    best_dist = dist
                    best_source = (fx, fy)
                # Optimization: if distance is 0, it's already there (though targets are usually unique)
                if dist == 0:
                    break
        
        # If a source is found, record the operation and add the target to the set.
        # Note: The problem implies targets are distinct from (0,0) or we just add them.
        # If best_source is None, it means the target cannot be reached under constraints,
        # but given the problem structure (0,0) is always a valid source for any (a,b) where a,b >= 0.
        if best_source is not None:
            if (tx, ty) != best_source:
                operations.append((best_source[0], best_source[1], tx, ty))
                existing_beverages.append((tx, ty))
            else:
                # If the target is already in existing_beverages, we don't need an operation.
                # However, the problem says "Every target beverage must eventually be created".
                # If the target is already (0,0), we don't add an operation.
                pass

    # Output the number of operations
    print(len(operations))
    # Output each operation: from_x from_y to_x to_y
    for op in operations:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == "__main__":
    solve()
