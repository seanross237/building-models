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

    # Sort targets to build a monotonic tree
    # A simple greedy approach: connect each target to the closest existing node
    # that satisfies monotonicity. Since we start at (0,0), we can build a path.
    # To minimize total distance, we use a Steiner-like approach or simply
    # connect targets in a way that reuses edges.
    
    # For this specific problem structure (monotonicity), the minimum cost
    # is achieved by a tree. A simple way is to sort targets by x then y.
    targets.sort()
    
    edges = []
    visited = [(0, 0)]

    for tx, ty in targets:
        # Find a node (fx, fy) in visited such that fx <= tx and fy <= ty
        # and (tx-fx) + (ty-fy) is minimized.
        best_dist = float('inf')
        best_node = (0, 0)
        
        for fx, fy in visited:
            if fx <= tx and fy <= ty:
                dist = (tx - fx) + (ty - fy)
                if dist < best_dist:
                    best_dist = dist
                    best_node = (fx, fy)
        
        # If the best node is not the target itself, we might need intermediate steps
        # but the problem asks for edges. To minimize edges, we can go (fx, fy) -> (tx, fy) -> (tx, ty)
        # or (fx, fy) -> (fx, ty) -> (tx, ty). However, the problem allows any edge
        # satisfying monotonicity. A single edge (fx, fy) -> (tx, ty) is valid.
        
        if (tx, ty) not in visited:
            edges.append((best_node[0], best_node[1], tx, ty))
            visited.append((tx, ty))

    print(len(edges))
    for fx, fy, tx, ty in edges:
        print(f"{fx} {fy} {tx} {ty}")

if __name__ == "__main__":
    solve()