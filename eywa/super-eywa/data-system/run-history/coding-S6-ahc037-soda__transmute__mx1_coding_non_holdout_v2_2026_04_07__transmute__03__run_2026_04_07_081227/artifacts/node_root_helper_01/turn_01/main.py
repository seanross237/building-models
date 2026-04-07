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
    
    nodes = [(0, 0)]
    ops = []
    
    for tx, ty in targets:
        best_node = (0, 0)
        min_dist = float('inf')
        found = False
        for fx, fy in nodes:
            if tx >= fx and ty >= fy:
                dist = (tx - fx) + (ty - fy)
                if dist < min_dist:
                    min_dist = dist
                    best_node = (fx, fy)
                    found = True
        
        if found:
            nodes.append((tx, ty))

if __name__ == '__main__':
    solve()