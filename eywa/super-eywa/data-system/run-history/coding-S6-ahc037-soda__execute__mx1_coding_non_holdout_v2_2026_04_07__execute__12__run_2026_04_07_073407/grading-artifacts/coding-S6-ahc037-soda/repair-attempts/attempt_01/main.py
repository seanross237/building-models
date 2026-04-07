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

    # To minimize cost C = sum((tx-fx) + (ty-fy)), we want to reuse existing points.
    # A simple greedy approach:
    # Sort targets by x, then y.
    # For each target, find an existing point (fx, fy) such that fx <= tx and fy <= ty
    # and (tx-fx) + (ty-fy) is minimized.
    
    sorted_targets = sorted(targets, key=lambda p: (p[0], p[1]))
    
    existing_points = [(0, 0)]
    operations = []
    
    # We need to keep track of which targets are already "created"
    # Since we process sorted_targets, we ensure we don't create duplicates 
    # if multiple targets are the same, though the problem implies N distinct targets.
    # However, we must ensure every target is reached.
    
    for tx, ty in sorted_targets:
        # Check if this point is already in existing_points (e.g., (0,0) or a previous target)
        # But the problem says "Every target beverage must eventually be created".
        # If a target is (0,0), it's already there.
        if tx == 0 and ty == 0:
            continue
            
        best_dist = float('inf')
        best_source = None
        
        for fx, fy in existing_points:
            if fx <= tx and fy <= ty:
                dist = (tx - fx) + (ty - fy)
                if dist < best_dist:
                    best_dist = dist
                    best_source = (fx, fy)
                elif dist == best_dist:
                    # Tie-break: prefer point closer to origin or something? 
                    # Actually, any valid source works for the cost.
                    pass
        
        if best_source is not None:
            operations.append((best_source[0], best_source[1], tx, ty))
            existing_points.append((tx, ty))
        else:
            # This case shouldn't happen because (0,0) is always a valid source for any (tx, ty) where tx, ty >= 0
            # But if it did, we'd have to handle it.
            pass

    # Output the number of operations
    print(len(operations))
    for op in operations:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == "__main__":
    solve()
