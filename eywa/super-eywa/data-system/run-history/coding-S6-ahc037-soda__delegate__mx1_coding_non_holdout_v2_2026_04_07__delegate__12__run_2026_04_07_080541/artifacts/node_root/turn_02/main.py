import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    targets = []
    idx = 1
    for _ in range(N):
        tx = int(input_data[idx])
        ty = int(input_data[idx+1])
        targets.append((tx, ty))
        idx += 2
    
    # Sort targets to facilitate finding valid predecessors.
    # Sorting by x then y helps ensure that for a target (tx, ty),
    # many previously processed targets (fx, fy) will satisfy fx <= tx.
    targets.sort()
    
    ops = []
    # current_beverages stores all beverages currently available to be used as sources.
    # We start with the initial beverage (0, 0).
    current_beverages = [(0, 0)]
    
    for i in range(N):
        tx, ty = targets[i]
        found = False
        
        # To satisfy the problem constraints, we must find an existing beverage (fx, fy)
        # such that fx <= tx and fy <= ty.
        # We iterate backwards through current_beverages to find a recent one,
        # which often helps in keeping the cost (tx-fx) + (ty-fy) lower.
        for j in range(len(current_beverages) - 1, -1, -1):
            fx, fy = current_beverages[j]
            if fx <= tx and fy <= ty:
                ops.append((fx, fy, tx, ty))
                current_beverages.append((tx, ty))
                found = True
                break
        
        if not found:
            # If no valid source is found, we fallback to the origin (0,0).
            # In a valid problem instance where targets are non-negative, (0,0) is always valid.
            ops.append((0, 0, tx, ty))
            current_beverages.append((tx, ty))

    # Output the number of operations
    print(len(ops))
    # Output each operation: from_x from_y to_x to_y
    for op in ops:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == "__main__":
    solve()