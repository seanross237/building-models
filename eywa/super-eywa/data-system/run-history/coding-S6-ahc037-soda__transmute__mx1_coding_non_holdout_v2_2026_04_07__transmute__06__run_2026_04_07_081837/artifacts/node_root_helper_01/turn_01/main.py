import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    points = []
    idx = 1
    for _ in range(n):
        x = int(input_data[idx])
        y = int(input_data[idx+1])
        points.append((x, y))
        idx += 2

    # Sort points to ensure monotonicity can be satisfied
    # A simple way is to sort by x then y
    points.sort()

    edges = []
    current_nodes = [(0, 0)]

    for px, py in points:
        # Find the best existing node to connect to
        # Best node (fx, fy) must have fx <= px and fy <= py
        best_dist = float('inf')
        best_node = None

        for nx, ny in current_nodes:
            if nx <= px and ny <= py:
                dist = (px - nx) + (py - ny)
                if dist < best_dist:
                    best_dist = dist
                    best_node = (nx, ny)
        
        if best_node:
            edges.append((best_node[0], best_node[1], px, py))
            current_nodes.append((px, py))
        else:
            # If no node satisfies monotonicity, we must use (0,0)
            # but the problem implies a valid construction exists.
            # In a grid with tx >= fx and ty >= fy, (0,0) is always valid
            # if all points are in the first quadrant.
            edges.append((0, 0, px, py))
            current_nodes.append((px, py))

    print(len(edges))
    for e in edges:
        print(f"{e[0]} {e[1]} {e[2]} {e[3]}")

if __name__ == "__main__":
    solve()