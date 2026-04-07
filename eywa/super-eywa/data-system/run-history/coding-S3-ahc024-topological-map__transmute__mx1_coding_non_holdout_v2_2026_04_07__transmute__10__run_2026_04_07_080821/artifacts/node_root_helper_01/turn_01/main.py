import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    M = int(input_data[1])
    grid = []
    idx = 2
    for r in range(N):
        grid.append([int(x) for x in input_data[idx:idx+N]])
        idx += N

    # Identify non-zero colors and their adjacency
    colors = set()
    for r in range(N):
        for c in range(N):
            if grid[r][c] > 0:
                colors.add(grid[r][c])
    
    adj_in = set()
    for r in range(N):
        for c in range(N):
            k1 = grid[r][c]
            if k1 == 0: continue
            for dr, dc in [(0, 1), (1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < N and 0 <= nc < N:
                    k2 = grid[nr][nc]
                    if k2 > 0 and k1 != k2:
                        adj_in.add(tuple(sorted((k1, k2))))

    # Find a representative cell for each color to maintain connectivity
    # and a way to place them to satisfy adjacency.
    # Since we want to minimize cells, we try to place one cell per color.
    # However, to satisfy adjacency, we must place them adjacent to each other.
    # We can treat the adjacency graph as a graph problem.
    
    color_list = sorted(list(colors))
    color_to_pos = {}
    
    # Simple strategy: Place colors in a snake-like pattern if they are adjacent.
    # But we must respect the exact adjacency graph.
    # We'll use a BFS/DFS approach to place colors in a connected way.
    
    adj_graph = {k: set() for k in color_list}
    for k1, k2 in adj_in:
        adj_graph[k1].add(k2)
        adj_graph[k2].add(k1)

    out_grid = [[0 for _ in range(N)] for _ in range(N)]
    visited_colors = set()