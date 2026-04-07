import sys

def solve():
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

    # Adjacency map for colors
    adj_colors = set()
    for r in range(N):
        for c in range(N):
            color = grid[r][c]
            if color == 0: continue
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < N and 0 <= nc < N:
                    n_color = grid[nr][nc]
                    if n_color != 0 and n_color != color:
                        pair = tuple(sorted((color, n_color)))
                        adj_colors.add(pair)

    # To preserve connectivity and adjacency, we find a skeleton.
    # A simple approach: for each color, find its cells and keep only those
    # that are necessary to maintain connectivity and adjacency.
    # For this baseline, we will use a simple thinning/skeletonization logic.
    # However, to ensure validity, we can use a BFS to find a spanning tree for each color
    # and ensure that the edges between different colors are preserved.
    
    output_grid = [[0 for _ in range(N)] for _ in range(N)]
    
    # 1. Identify all color components and their adjacency
    # 2. For each color, find a minimal set of cells that keeps it connected
    # 3. Ensure that for every pair (c1, c2) in adj_colors, there is at least one pair of adjacent cells.

    # Step 1: Find all cells for each color
    color_cells = {} # color -> list of (r, c)
    for r in range(N):
        for c in range(N):
            color = grid[r][c]
            if color != 0:
                if color not in color_cells:
                    color_cells[color] = []
                color_cells[color].append((r, c))

    # Step 2: For each color, find a spanning tree to ensure connectivity
    # We'll use BFS to build a tree for each color
    visited_cells = set()
    for color in color_cells:
        cells = color_cells[color]
        if not cells: continue
        
        start_node = cells[0]
        q = []