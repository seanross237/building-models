import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    advertisers = []
    idx = 1
    for i in range(N):
        x = float(input_data[idx])
        y = float(input_data[idx+1])
        r = float(input_data[idx+2])
        advertisers.append({
            'id': i,
            'x': x,
            'y': y,
            'r': r
        })
        idx += 3

    # Results storage
    results = [None] * N

    # Recursive function to partition space
    # bounds: (x_min, y_min, x_max, y_max)
    def partition(points, x_min, y_min, x_max, y_max):
        if not points:
            return
        
        if len(points) == 1:
            p = points[0]
            results[p['id']] = (x_min, y_min, x_max, y_max)
            return

        # Choose axis to split: longest dimension
        width = x_max - x_min
        height = y_max - y_min
        
        if width > height:
            # Split on X
            points.sort(key=lambda p: p['x'])
            mid = len(points) // 2
            split_val = points[mid]['x']
            partition(points[:mid], x_min, y_min, split_val, y_max)
            partition(points[mid:], split_val, y_min, x_max, y_max)
        else:
            # Split on Y
            points.sort(key=lambda p: p['y'])
            mid = len(points) // 2
            split_val = points[mid]['y']
            partition(points[:mid], x_min, y_min, x_max, split_val)
            partition(points[mid:], x_min, split_val, x_max, y_max)

    partition(advertisers, 0.0, 0.0, 1000000.0, 1000000.0)
    for res in results:
        if res:
            print(f"{res[0]} {res[1]} {res[2]} {res[3]}")

solve()