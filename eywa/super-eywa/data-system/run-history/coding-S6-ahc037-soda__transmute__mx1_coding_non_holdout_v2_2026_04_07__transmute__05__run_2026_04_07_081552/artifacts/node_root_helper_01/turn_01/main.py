import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    targets = []
    idx = 1
    for _ in range(n):
        x = int(input_data[idx])
        y = int(input_data[idx+1])
        targets.append((x, y))
        idx += 2

    # Sort targets to ensure monotonicity and minimize distance
    # Sorting by x then y helps in building a path-like structure
    targets.sort()

    existing = {(0, 0)}
    operations = []
    
    # To minimize cost, we try to connect each target to the
    # closest existing node that satisfies the monotonicity constraint.
    # Since we sort targets, we can often connect to the previous target.
    
    current_nodes = [(0, 0)]
    
    for tx, ty in targets:
        best_node = None
        min_dist = float('inf')
        
        for fx, fy in current_nodes:
            if tx >= fx and ty >= fy:
                dist = (tx - fx) + (ty - fy)
                if dist < min_dist:
                    min_dist = dist
                    best_node = (fx, fy)
        
        if best_node:
            fx, fy = best_node
            # If the target is not already reached by an existing node
            # (though in this specific problem, we just need to reach it)
            if (tx, ty) not in existing:
                # We might need intermediate steps if we want to be strictly monotonic
                # but the problem allows (fx, fy) -> (tx, ty) directly if tx >= fx and ty >= fy
                operations.append((fx, fy, tx, ty))
                existing.add((tx, ty))
                current_nodes.append((tx, ty))
        else:
            # This case shouldn't happen if targets are reachable from (0,0)
            # but if it does, we must find a way. Given constraints, 
            # we assume targets are in the first quadrant.
            # If no node satisfies monotonicity, we can't reach it under rules.
            pass

    print(len(operations))
    for op in operations:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == "__main__":
    solve()