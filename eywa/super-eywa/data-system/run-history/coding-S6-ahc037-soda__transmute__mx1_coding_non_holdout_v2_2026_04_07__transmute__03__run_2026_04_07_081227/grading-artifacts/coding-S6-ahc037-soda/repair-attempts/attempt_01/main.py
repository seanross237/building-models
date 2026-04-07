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

    # Sort targets primarily by x, then by y.
    # This ensures that when we process a target, we can potentially 
    # use a previously created beverage that has smaller or equal x and y.
    targets.sort()
    
    # nodes stores (x, y) of beverages already created.
    # We start with (0, 0).
    nodes = [(0, 0)]
    ops = []
    
    for tx, ty in targets:
        # If the target is already (0,0), we don't need an operation.
        # However, the problem says "Every target beverage must eventually be created".
        # If (0,0) is a target, it's already there.
        if tx == 0 and ty == 0:
            continue
            
        best_node = None
        min_dist = float('inf')
        
        # Find an existing node (fx, fy) such that fx <= tx and fy <= ty
        # and the cost (tx-fx) + (ty-fy) is minimized.
        # Minimizing (tx-fx) + (ty-fy) is equivalent to maximizing fx + fy.
        for fx, fy in nodes:
            if fx <= tx and fy <= ty:
                dist = (tx - fx) + (ty - fy)
                if dist < min_dist:
                    min_dist = dist
                    best_node = (fx, fy)
                elif dist == min_dist:
                    # Tie-break: prefer nodes that might be more useful later
                    # (though in this simple greedy, it doesn't matter much)
                    pass
        
        if best_node is not None:
            ops.append((best_node[0], best_node[1], tx, ty))
            nodes.append((tx, ty))
        else:
            # This case should not happen because (0,0) is always in nodes
            # and tx, ty >= 0 is implied by the problem context.
            pass

    # Output the number of operations
    print(len(ops))
    # Output each operation
    for op in ops:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == '__main__':
    solve()
