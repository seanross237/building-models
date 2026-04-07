import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    targets = []
    idx = 1
    for _ in range(n):
        x = int(input_data[idx])
        y = int(input_data[idx+1])
        targets.append((x, y))
        idx += 2

    targets.sort()
    
    edges = []
    visited = [(0, 0)]
    
    for tx, ty in targets:
        best_node = None
        min_dist = float('inf')
        
        for vx, vy in visited:
            if tx >= vx and ty >= vy:
                dist = (tx - vx) + (ty - vy)
                if dist < min_dist:
                    min_dist = dist
                    best_node = (vx, vy)
        
        if best_node:
            edges.append((best_node[0], best_node[1], tx, ty))
            visited.append((tx, ty))
        else:
            if tx > 0:
                edges.append((0, 0, tx, 0))
                visited.append((tx, 0))
                best_node = (tx, 0)
            else:
                edges.append((0, 0, 0, ty))
                visited.append((0, ty))
                best_node = (0, ty)
            edges.append((best_node[0], best_node[1], tx, ty))
            visited.append((tx, ty))
