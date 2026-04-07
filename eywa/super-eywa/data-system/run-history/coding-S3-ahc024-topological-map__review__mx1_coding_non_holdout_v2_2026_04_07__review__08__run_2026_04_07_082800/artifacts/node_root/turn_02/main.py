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

    # Adjacency requirements: which colors must be adjacent
    adj_req = set()
    for r in range(N):
        for c in range(N):
            color = grid[r][c]
            if color == 0: continue
            for dr, dc in [(0, 1), (1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < N and 0 <= nc < N:
                    n_color = grid[nr][nc]
                    if n_color != 0 and n_color != color:
                        pair = tuple(sorted((color, n_color)))
                        adj_req.add(pair)

    # Connectivity requirements: each color must be connected
    # We'll use a simple approach: for each color, find its cells.
    # To maximize 0s, we want to reduce each color to a minimal skeleton.
    # A simple skeleton is a spanning tree of the original cells.
    
    new_grid = [[0 for _ in range(N)] for _ in range(N)]
    
    # Group cells by color
    color_cells = {}
    for r in range(N):
        for c in range(N):
            color = grid[r][c]
            if color != 0:
                if color not in color_cells: color_cells[color] = []
                color_cells[color].append((r, c))

    # For each color, find a spanning tree to keep it connected
    # and ensure adjacency requirements are met.
    # To keep it simple and robust, we'll pick one cell per color as a 'hub'
    # and connect it to its neighbors in the original grid.
    
    # However, a better way to ensure adjacency is to pick one cell for each color
    # and ensure that if color A and B were adjacent, their chosen cells are adjacent.
    
    # Let's try a greedy approach: 
    # 1. Identify 'representative' cells for each color.
    # 2. Ensure representatives of adjacent colors are adjacent.
    # 3. Connect representatives to all other cells of the same color (not possible if we want 0s).
    # Actually, the rule is: Every nonzero color must remain connected.
    # This means we need a path of cells of color X connecting all parts of color X.
