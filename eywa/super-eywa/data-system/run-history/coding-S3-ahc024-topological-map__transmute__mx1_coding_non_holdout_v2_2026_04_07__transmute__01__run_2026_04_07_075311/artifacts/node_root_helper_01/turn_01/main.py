import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    grid = []
    for i in range(50):
        grid.append([int(x) for x in input_data[i*50:(i+1)*50]])

    colors = set()
    for r in range(50):
        for c in range(50):
            if grid[r][c] != 0:
                colors.add(grid[r][c])
    
    adj = {color: set() for color in colors}
    for r in range(50):
        for c in range(50):
            color = grid[r][c]
            if color == 0: continue
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < 50 and 0 <= nc < 50:
                    n_color = grid[nr][nc]
                    if n_color != 0 and n_color != color:
                        adj[color].add(n_color)

    output = [[0 for _ in range(50)] for _ in range(50)]
    placed_colors = {}
    sorted_colors = sorted(list(colors), key=lambda x: len(adj[x]), reverse=True)
    
    if sorted_colors:
        start_color = sorted_colors[0]
        queue = [(start_color, 2, 2)]
        placed_colors[start_color] = (2, 2)
        output[2][2] = start_color
        visited = {start_color}
        idx = 0
        while idx < len(queue):
            curr_color, r, c = queue[idx]
            idx += 1
            for neighbor in adj[curr_color]:
                if neighbor not in visited:
                    found = False
                    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < 50 and 0 <= nc < 50 and output[nr][nc] == 0:
                            output[nr][nc] = neighbor
                            placed_colors[neighbor] = (nr, nc)
                            queue.append((neighbor, nr, nc))
                            visited.add(neighbor)
                            found = True
                            break
    for row in output:
        print(*(row))
solve()