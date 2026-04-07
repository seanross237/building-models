import sys

def solve():
    # Read N, M
    line1 = sys.stdin.readline().split()
    if not line1:
        return
    n = int(line1[0])
    m = int(line1[1])
    
    grid = []
    for _ in range(n):
        grid.append(list(map(int, sys.stdin.readline().split())))

    # Build adjacency graph for colors 1..M
    adj = [set() for _ in range(m + 1)]
    color_cells = [[] for _ in range(m + 1)]
    
    for r in range(n):
        for c in range(n):
            color = grid[r][c]
            if color > 0:
                color_cells[color].append((r, c))
                # Check neighbors for adjacency
                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n:
                        n_color = grid[nr][nc]
                        if n_color > 0 and n_color != color:
                            adj[color].add(n_color)

    # We need to output a 50x50 grid.
    # A simple valid strategy: 
    # For each color, pick one representative cell from the original grid.
    # To ensure adjacency, if color A and B are adjacent, we need to ensure 
    # their representative cells are adjacent or connected via a path.
    # However, the simplest valid solution is to just output the original grid.
    # The problem asks to maximize 0s, but the priority is correctness.
    # A "skeleton" approach is complex. Let's try to output the original grid 
    # as a baseline, but the problem implies we should try to reduce it.
    # Given the constraints and the "simplest strictly valid" instruction,
    # the original grid is a valid topological map.
    
    # Let's try a slightly more optimized version: 
    # For each color, find its "center" or just use the first cell found.
    # But to maintain adjacency, we must be careful.
    # Actually, the simplest valid solution that is guaranteed to work is the input itself.
    # Let's output the input grid.
    
    for r in range(n):
        print(*(grid[r]))

if __name__ == "__main__":
    solve()
