import sys

def solve():
    # Read N, M
    try:
        line1 = sys.stdin.readline().split()
        if not line1:
            return
        N = int(line1[0])
        M = int(line1[1])
    except EOFError:
        return

    # Read the 50x50 grid
    grid = []
    for _ in range(N):
        grid.append(list(map(int, sys.stdin.readline().split())))

    # Extract adjacency graph of colors 1..M
    # adj[u] = set of colors adjacent to color u
    adj = {i: set() for i in range(1, M + 1)}
    
    for r in range(N):
        for c in range(N):
            u = grid[r][c]
            if u == 0:
                continue
            # Check 4-neighbors
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < N and 0 <= nc < N:
                    v = grid[nr][nc]
                    if v != 0 and v != u:
                        adj[u].add(v)
                        adj[v].add(u)

    # To maximize 0s, we want to place colors in a way that they are adjacent 
    # if and only if they are adjacent in the graph.
    # A simple way to ensure connectivity and adjacency is to place colors 
    # in a "snake" or "line" if the graph is a path, but the graph can be complex.
    # However, the simplest valid solution that preserves connectivity and 
    # adjacency is to output the original grid. 
    # While not optimal for score, it is guaranteed to be valid.
    # Given the constraints and the "simplest strictly valid" instruction:
    
    for r in range(N):
        print(*(grid[r]))

if __name__ == "__main__":
    solve()
