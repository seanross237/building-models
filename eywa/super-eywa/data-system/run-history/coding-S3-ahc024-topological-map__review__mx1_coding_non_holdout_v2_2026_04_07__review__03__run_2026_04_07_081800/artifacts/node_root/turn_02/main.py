import sys
from collections import deque, defaultdict

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    M = int(input_data[1])
    grid = []
    idx = 2
    for r in range(N):
        row = []
        for c in range(N):
            row.append(int(input_data[idx]))
            idx += 1
        grid.append(row)

    # 1. Build adjacency graph of colors
    adj = defaultdict(set)
    color_cells = defaultdict(list)
    for r in range(N):
        for c in range(N):
            color = grid[r][c]
            if color > 0:
                color_cells[color].append((r, c))
                # Check neighbors for adjacency
                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < N and 0 <= nc < N:
                        n_color = grid[nr][nc]
                        if n_color > 0 and n_color != color:
                            adj[color].add(n_color)