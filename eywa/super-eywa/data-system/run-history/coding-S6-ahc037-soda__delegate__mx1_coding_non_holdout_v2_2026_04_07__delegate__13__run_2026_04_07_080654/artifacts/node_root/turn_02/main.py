import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    targets = []
    for i in range(N):
        tx = int(input_data[1 + 2*i])
        ty = int(input_data[2 + 2*i])
        targets.append((tx, ty))
    
    # Sort targets primarily by x and secondarily by y to facilitate a greedy approach
    targets.sort()
    
    ops = []
    # The starting beverage is (0, 0)
    visited = [(0, 0)]
    
    for tx, ty in targets:
        best_dist = float('inf')
        best_prev = None
        
        # Find the existing beverage (vx, vy) that can produce (tx, ty)
        # such that tx >= vx and ty >= vy, minimizing Manhattan distance.
        # Since we want to minimize C = sum((tx-vx) + (ty-vy)), 
        # and (tx-vx) + (ty-vy) is the cost of one step.
        for vx, vy in visited:
            if vx <= tx and vy <= ty:
                dist = (tx - vx) + (ty - vy)
                if dist < best_dist:
                    best_dist = dist
                    best_prev = (vx, vy)
                elif dist == best_dist:
                    # Tie-breaking: prefer existing points closer to origin or specific order
                    pass
        
        # If no valid predecessor is found (should not happen if (0,0) is in visited and targets are >= 0)
        # we fallback to (0,0) if possible, though the problem implies targets are reachable.
        if best_prev is None:
            # This case handles if targets could be negative, but problem implies sweetness/carbonation increase
            # We use (0,0) as a fallback if the logic fails.
            best_prev = (0, 0)
            
        ops.append((best_prev[0], best_prev[1], tx, ty))
        visited.append((tx, ty))
    
    # Output the number of operations
    print(len(ops))
    # Output each operation
    for op in ops:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == "__main__":
    solve()