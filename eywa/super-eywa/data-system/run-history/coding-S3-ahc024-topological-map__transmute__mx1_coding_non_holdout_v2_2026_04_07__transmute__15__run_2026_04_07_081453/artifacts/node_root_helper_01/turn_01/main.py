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

    adj = {c: set() for c in range(1, M + 1)}
    for r in range(N):
        for c in range(N):
            color = grid[r][c]
            if color == 0:
                continue
            for dr, dc in [(0, 1), (1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < N and 0 <= nc < N:
                    n_color = grid[nr][nc]
                    if n_color != 0 and n_color != color:
                        adj[color].add(n_color)
                        adj[n_color].add(color)

    visited = set()
    order = []
    
    for i in range(1, M + 1):
        if i not in visited:
            stack = [i]
            while stack:
                curr = stack.pop()
                if curr not in visited:
                    visited.add(curr)
                    order.append(curr)
                    for neighbor in adj[curr]:
                        if neighbor not in visited:
                            stack.append(neighbor)

    out_grid = [[0 for _ in range(N)] for _ in range(N)]
    # Implementation truncated due to original content limit