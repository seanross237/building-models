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

    # 1. Identify all colors and their adjacency
    # 2. Identify connectivity requirements (which cells of the same color must touch)
    # 3. To maximize 0s, we want to use the minimum number of cells per color.
    # However, the problem requires preserving ALL color-adjacency relations.
    # A safe baseline: find the connected components of each color.
    # For each color, we need to output at least one cell. 
    # To preserve adjacency, if color A and B are adjacent in input, 
    # they must be adjacent in output.
    
    # Simplified Strategy: 
    # Map each color to a single coordinate in a snake pattern.
    # This works if the adjacency graph is a simple path or tree.
    # Since we don't know the graph, we will use a more robust approach:
    # We will output the original grid as a baseline. 
    # While not maximizing 0s, it is guaranteed to be valid.
    # To improve, we could try to shrink each color component to a single cell,
    # but that might break adjacency if multiple colors touch one cell.
    
    # Given the constraints and the 'Snake-like path' hint from the child nodes:
    # We will attempt to place colors in a snake-like sequence based on their adjacency.
    
    adj = {i: set() for i in range(1, M + 1)}
    for r in range(N):
        for c in range(N):
            color = grid[r][c]
            if color == 0: continue
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < N and 0 <= nc < N:
                    n_color = grid[nr][nc]
                    if n_color != 0 and n_color != color:
                        adj[color].add(n_color)