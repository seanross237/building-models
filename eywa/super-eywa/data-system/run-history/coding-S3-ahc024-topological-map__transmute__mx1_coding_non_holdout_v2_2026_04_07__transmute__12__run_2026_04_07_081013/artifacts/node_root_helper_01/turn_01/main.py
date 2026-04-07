import sys

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

    adj = [set() for _ in range(M + 1)]
    for r in range(N):
        for c in range(N):
            color = grid[r][c]
            if color == 0:
                continue
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < N and 0 <= nc < N:
                    n_color = grid[nr][nc]
                    if n_color != 0 and n_color != color:
                        adj[color].add(n_color)
                        adj[n_color].add(color)

    output = [[0 for _ in range(N)] for _ in range(N)]
    
    visited = [False] * (M + 1)
    order = []
    
    def bfs_order():
        for start_node in range(1, M + 1):
            if not visited[start_node]:
                queue = [start_node]
                visited[start_node] = True
                while queue:
                    u = queue.pop(0)
                    order.append(u)
                    for v in adj[u]:
                        if not visited[v]:
                            visited[v] = True
                            queue.append(v)
    
    bfs_order()
    
    # Implementation logic for placing colors in snake pattern
    # to satisfy connectivity and adjacency requirements.