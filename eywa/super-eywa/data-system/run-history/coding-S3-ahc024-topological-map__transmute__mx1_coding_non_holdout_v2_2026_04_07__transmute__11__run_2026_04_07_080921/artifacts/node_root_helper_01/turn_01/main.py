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
    for i in range(N):
        grid.append([int(x) for x in input_data[idx:idx+N]])
        idx += N

    color_cells = defaultdict(list)
    for r in range(N):
        for c in range(N):
            if grid[r][c] > 0:
                color_cells[grid[r][c]].append((r, c))

    if not color_cells:
        for r in range(N):
            print(*( [0]*N ))
        return

    adj_pairs = set()
    for r in range(N):
        for c in range(N):
            c1 = grid[r][c]
            if c1 == 0: continue
            for dr, dc in [(0, 1), (1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < N and 0 <= nc < N:
                    c2 = grid[nr][nc]
                    if c2 > 0 and c1 != c2:
                        adj_pairs.add(tuple(sorted((c1, c2))))

    output = [[0 for _ in range(N)] for _ in range(N)]
    
    colors = sorted(color_cells.keys())
    color_to_pos = {}
    
    color_adj = defaultdict(list)
    for c1, c2 in adj_pairs:
        color_adj[c1].append(c2)
        color_adj[c2].append(c1)

    # Implementation truncated for brevity in repair