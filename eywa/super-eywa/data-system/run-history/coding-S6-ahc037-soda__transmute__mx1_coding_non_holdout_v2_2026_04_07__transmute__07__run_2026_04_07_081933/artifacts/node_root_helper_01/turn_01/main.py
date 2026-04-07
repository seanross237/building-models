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

    # Sort targets to ensure monotonicity can be satisfied
    # A simple way is to sort by x then y
    targets.sort()

    edges = []
    current_nodes = [(0, 0)]
    
    # To ensure we can always reach targets monotonically,
    # we must ensure targets are reachable from existing nodes.
    # Since we sort by x and y, we can try to connect each target
    # to the 'closest' existing node that satisfies monotonicity.
    
    visited_targets = []
    
    # We use a simple greedy approach: connect each target to the
    # node in the current set that is closest and satisfies monotonicity.
    # If no such node exists, we must create intermediate nodes.
    
    for tx, ty in targets:
        best_node = None
        min_dist = float('inf')
        
        for nx, ny in current_nodes:
            if tx >= nx and ty >= ny:
                dist = (tx - nx) + (ty - ny)
                if dist < min_dist:
                    min_dist = dist
                    best_node = (nx, ny)
        
        if best_node:
            bx, by = best_node
            # If direct connection is not possible via single edge
            # (though Manhattan distance is additive), we just add the edge.
            # However, the problem asks for edges. A single edge (bx, by) -> (tx, ty)
            # is valid if tx >= bx and ty >= by.
            edges.append((bx, by, tx, ty))
            current_nodes.append((tx, ty))
        else:
            # This case shouldn't happen if targets are reachable from (0,0)
            # and we sort them correctly, but for safety:
            # Find the node with max x <= tx and max y <= ty
            # For this problem, we assume targets are in the first quadrant.
            # If a target is not reachable, we'd need to find a path.
            # Given the constraints, we'll just connect to (0,0) via a path.
            # But the problem implies a valid tree exists.
            pass

    print(len(edges))
    for e in edges:
        print(f"{e[0]} {e[1]} {e[2]} {e[3]}")

if __name__ == "__main__":
    solve()