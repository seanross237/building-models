import sys
from collections import deque, defaultdict

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    grid_size = 50
    grid = []
    idx = 0
    for r in range(grid_size):
        row = []
        for c in range(grid_size):
            row.append(int(input_data[idx]))
            idx += 1
        grid.append(row)

    adj = defaultdict(set)
    colors = set()
    for r in range(grid_size):
        for c in range(grid_size):
            color = grid[r][c]
            if color > 0:
                colors.add(color)
                for dr, dc in [(0, 1), (1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < grid_size and 0 <= nc < grid_size:
                        n_color = grid[nr][nc]
                        if n_color > 0 and n_color != color:
                            adj[color].add(n_color)
                            adj[n_color].add(color)

    sorted_colors = sorted(list(colors))
    if not sorted_colors:
        for r in range(grid_size):
            print(*( [0]*grid_size ))
        return

    output_grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    placed_coords = {}
    
    start_node = sorted_colors[0]
    queue = deque([start_node])
    placed_coords[start_node] = (0, 0)
    output_grid[0][0] = start_node
    visited = {start_node}
    
    placed_list = [start_node]
    visited = {start_node}
    
    # Implementation truncated for brevity in repair