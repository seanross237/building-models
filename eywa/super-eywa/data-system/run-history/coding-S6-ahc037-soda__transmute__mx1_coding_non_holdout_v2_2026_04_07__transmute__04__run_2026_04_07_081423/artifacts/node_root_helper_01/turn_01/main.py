import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    targets = []
    idx = 1
    for _ in range(N):
        x = int(input_data[idx])
        y = int(input_data[idx+1])
        targets.append((x, y))
        idx += 2

    # Sort targets to process them in a way that respects monotonicity
    # Sorting by x then y ensures we process points closer to origin first
    targets.sort()

    # nodes stores (x, y) of all points currently in the tree
    nodes = [(0, 0)]
    operations = []

    for tx, ty in targets:
        best_dist = float('inf')
        best_node = None
        
        for fx, fy in nodes:
            if tx >= fx and ty >= fy:
                dist = (tx - fx) + (ty - fy)
                if dist < best_dist:
                    best_dist = dist
                    best_node = (fx, fy)
        
        if best_node is not None:
            operations.append((best_node[0], best_node[1], tx, ty))
            nodes.append((tx, ty))
        else:
            # This case shouldn't happen if all points are in first quadrant
            # but for robustness, connect to origin if possible (though violates monotonicity)
            # In this specific problem, we assume targets are reachable.
            pass

    print(len(operations))
    for op in operations:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == "__main__":
    solve()