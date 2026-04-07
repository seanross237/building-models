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

    adj = {}
    colors = set()
    for r in range(N):
        for c in range(N):
            color = grid[r][c]
            if color != 0:
                colors.add(color)
                if color not in adj:
                    adj[color] = set()
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < N and 0 <= nc < N:
                        n_color = grid[nr][nc]
                        if n_color != 0 and n_color != color:
                            adj[color].add(n_color)

    output_grid = [[0 for _ in range(N)] for _ in range(N)]
    placed_colors = {}
    
    if not colors:
        for row in output_grid:
            print(*(row))
        return

    start_color = sorted(list(colors))[0]
    queue = [start_color]
    placed_colors[start_color] = (0, 0)
    output_grid[0][0] = start_color
    visited = {start_color}

    q_idx = 0
    while q_idx < len(queue):
        u = queue[q_idx]
        q_idx += 1
        u_r, u_c = placed_colors[u]
        for v in adj.get(u, []):
            if v not in visited:
                found = False
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = u_r + dr, u_c + dc
                    if 0 <= nr < N and 0 <= nc < N and output_grid[nr][nc] == 0:
                        output_grid[nr][nc] = v
                        placed_colors[v] = (nr, nc)
                        visited.add(v)
                        queue.append(v)
                        found = True
                        break
                if not found:
                    pass

    for row in output_grid:
        print(*(row))

solve()