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

    # Sort targets to process in a topological order (increasing x and y)
    # This ensures we can always find a valid ancestor among processed nodes
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
        
        if best_node is not None:
            edges.append((best_node[0], best_node[1], tx, ty))
            nodes.append((tx, ty))

    print(len(edges))
    for fx, fy, tx, ty in edges:
        print(f"{fx} {fy} {tx} {ty}")

if __name__ == "__main__":
    solve()