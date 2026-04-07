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

    # Sort targets to ensure monotonicity (x then y)
    # This helps in building a path-like or tree-like structure
    targets.sort()

    edges = []
    current_nodes = [(0, 0)]
    
    # To minimize total Manhattan distance while ensuring reachability
    # and monotonicity, we can connect each target to the origin
    # or to a previously placed node. 
    # However, the problem asks to minimize sum of (tx-fx) + (ty-fy).
    # For any target (xi, yi), the minimum cost to reach it from (0,0)
    # is xi + yi. If we connect (0,0) -> (xi, yi) directly,
    # the cost is xi + yi. If we use intermediate nodes, the sum 
    # of costs remains xi + yi due to monotonicity.
    
    # A simple valid solution is to connect each target directly from (0,0)
    # if we want to ensure every target is reached.
    # But we must ensure every source node has been previously generated.
    # (0,0) is the starting node.
    
    for tx, ty in targets:
        edges.append((0, 0, tx, ty))

    print(len(edges))
    for fx, fy, tx, ty in edges:
        print(f"{fx} {fy} {tx} {ty}")

if __name__ == "__main__":
    solve()