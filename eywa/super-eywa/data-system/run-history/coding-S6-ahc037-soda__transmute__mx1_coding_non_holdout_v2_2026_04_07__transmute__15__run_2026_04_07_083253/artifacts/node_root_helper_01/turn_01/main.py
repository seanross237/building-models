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

    # Sort targets to facilitate monotonic construction
    # Sorting by x then y helps in building a tree
    targets.sort()

    # We use a simple approach: connect each target to the origin
    # or to a previously added target that satisfies monotonicity.
    # To minimize cost, we want to reuse paths.
    
    # For this specific problem structure (Manhattan + Monotonicity),
    # the cost of an edge (x1, y1) -> (x2, y2) is (x2-x1) + (y2-y1).
    # Total cost is sum of edge costs.
    
    # Let's keep track of nodes currently in our tree
    nodes = [(0, 0)]
    edges = []

    for tx, ty in targets:
        best_dist = float('inf')
        best_node = None
        
        for fx, fy in nodes:
            if tx >= fx and ty >= fy:
                dist = (tx - fx) + (ty - fy)
                if dist < best_dist:
                    best_dist = dist
                    best_node = (fx, fy)
        
        # If no existing node can reach (tx, ty) monotonically,
        # we must connect from (0,0) or create an intermediate.
        # But (0,0) is always a valid source for any (tx, ty) where tx,ty >= 0.
        if best_node is None:
            best_node = (0, 0)
            best_dist = tx + ty
            
        edges.append((best_node[0], best_node[1], tx, ty))
        nodes.append((tx, ty))

    print(len(edges))
    for e in edges:
        print(f"{e[0]} {e[1]} {e[2]} {e[3]}")

if __name__ == "__main__":
    solve()