import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    targets = []
    for i in range(n):
        x = int(input_data[1 + 2*i])
        y = int(input_data[2 + 2*i])
        targets.append((x, y))

    # Sort targets to process them in a way that respects monotonicity
    # Sorting by x then y ensures we process nodes from bottom-left to top-right
    targets.sort()

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
        
        if best_node:
            edges.append((best_node[0], best_node[1], tx, ty))
            nodes.append((tx, ty))
        else:
            # This case shouldn't happen if (0,0) is always valid
            # but for robustness, connect to (0,0) if possible or skip
            # Given constraints, (0,0) is always a valid source if tx,ty >= 0
            edges.append((0, 0, tx, ty))
            nodes.append((tx, ty))

    print(len(edges))
    for edge in edges:
        print(f"{edge[0]} {edge[1]} {edge[2]} {edge[3]}")

if __name__ == "__main__":
    solve()