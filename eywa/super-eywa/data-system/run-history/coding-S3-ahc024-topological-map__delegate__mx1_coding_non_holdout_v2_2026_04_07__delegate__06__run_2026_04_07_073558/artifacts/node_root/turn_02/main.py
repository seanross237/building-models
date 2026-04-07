import sys

def solve():
    # Read N, M
    try:
        line1 = sys.stdin.readline().split()
        if not line1: return
        N = int(line1[0])
        M = int(line1[1])
    except EOFError:
        return

    grid = []
    for _ in range(N):
        grid.append(list(map(int, sys.stdin.readline().split())))

    # 1. Extract Adjacency and Connectivity
    # We need to find which colors are adjacent and ensure each color's cells are connected.
    # To maximize 0s, we represent each color as a single cell or a minimal path.
    # However, the problem requires preserving ALL color-adjacency relations.
    
    adj_colors = set()
    color_cells = {} # color -> list of (r, c)
    
    for r in range(N):
        for c in range(N):
            color = grid[r][c]
            if color == 0: continue
            if color not in color_cells: color_cells[color] = []
            color_cells[color].append((r, c))
            
            # Check neighbors for adjacency
            for dr, dc in [(0, 1), (1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < N and 0 <= nc < N:
                    n_color = grid[nr][nc]
                    if n_color != 0 and n_color != color:
                        # Sort to ensure (1,2) is same as (2,1)
                        pair = tuple(sorted((color, n_color)))
                        adj_colors.add(pair)

    # 2. Build a Spanning Tree of Colors
    # We treat colors as nodes in a graph. We want to place them in the 50x50 grid.
    # A simple way to preserve adjacency and connectivity is to place colors in a sequence
    # if they form a path, or use a BFS/DFS layout.
    
    # To maximize 0s, we can try to place each color in exactly one cell if possible.
    # But colors might have multiple adjacencies. 
    # A safe way: Place colors in a 'snake' or 'grid' pattern if they are connected.
    # Since we must preserve ALL adjacencies, if color A is adjacent to B and C, 
    # A must be placed such that it touches both B and C.
    
    # Let's use a simple approach: 
    # Map each color to a single coordinate (r, c) in a sparse way.
    # To ensure adjacency, we can use a BFS-based placement.
    
    output_grid = []