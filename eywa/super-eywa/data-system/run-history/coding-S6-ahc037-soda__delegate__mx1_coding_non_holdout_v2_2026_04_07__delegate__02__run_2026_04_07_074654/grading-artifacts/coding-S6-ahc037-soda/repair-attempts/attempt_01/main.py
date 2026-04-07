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

    # We need to reach all (a_i, b_i) starting from (0, 0).
    # Constraint: (fx, fy) -> (tx, ty) requires tx >= fx and ty >= fy.
    # Cost: (tx - fx) + (ty - fy).
    # To minimize total cost, we want to connect each target to a point 
    # that is already "created" and minimizes the Manhattan distance.
    
    # Sort targets to ensure we process them in a way that respects monotonicity.
    # Sorting by x then y ensures that if we pick a predecessor (fx, fy) 
    # from the already processed set, we are more likely to satisfy fx <= tx.
    # However, we also need fy <= ty.
    
    # Let's use a greedy approach:
    # 1. Start with the set of created points S = {(0, 0)}.
    # 2. Sort all targets by x + y (Manhattan distance from origin).
    # 3. For each target, find a point (fx, fy) in S such that fx <= tx and fy <= ty
    #    and (tx - fx) + (ty - fy) is minimized.
    # 4. Add target to S and record the operation.

    targets.sort(key=lambda p: (p[0] + p[1]))
    
    created = [(0, 0)]
    operations = []
    
    for tx, ty in targets:
        best_dist = float('inf')
        best_prev = None
        
        for fx, fy in created:
            if fx <= tx and fy <= ty:
                dist = (tx - fx) + (ty - fy)
                if dist < best_dist:
                    best_dist = dist
                    best_prev = (fx, fy)
                elif dist == best_dist:
                    # Tie-break: prefer points closer to origin or with smaller x
                    if best_prev is None or (fx + fy < best_prev[0] + best_prev[1]):
                        best_prev = (fx, fy)
        
        # If no valid predecessor found (shouldn't happen as (0,0) is always valid),
        # we must connect to (0,0) or handle error.
        if best_prev is None:
            best_prev = (0, 0)
            
        operations.append((best_prev[0], best_prev[1], tx, ty))
        created.append((tx, ty))

    print(len(operations))
    for op in operations:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == "__main__":
    solve()
