import sys

def solve():
    try:
        line1 = sys.stdin.readline().split()
        if not line1: return
        N = int(line1[0])
        M = int(line1[1])
        grid = []
        for _ in range(N):
            grid.append(list(map(int, sys.stdin.readline().split())))
    except EOFError:
        return

    adj_pairs = set()
    color_cells = [[] for _ in range(M + 1)]
    
    for r in range(N):
        for c in range(N):
            val = grid[r][c]
            if val > 0:
                color_cells[val].append((r, c))
            
            for dr, dc in [(0, 1), (1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < N and 0 <= nc < N:
                    v1, v2 = grid[r][c], grid[nr][nc]
                    if v1 > 0 and v2 > 0 and v1 != v2:
                        pair = tuple(sorted((v1, v2)))
                        adj_pairs.add(pair)

    output = [[0 for _ in range(N)] for _ in range(N)]
    
    adj_list = [set() for _ in range(M + 1)]
    for u, v in adj_pairs:
        adj_list[u].add(v)
        adj_list[v].add(u)

    visited_colors = [False] * (M + 1)
    path = []