import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    try:
        N = int(input_data[0])
    except (ValueError, IndexError):
        return

    advertisers = []
    idx = 1
    for i in range(N):
        if idx + 2 >= len(input_data):
            break
        try:
            x = float(input_data[idx])
            y = float(input_data[idx+1])
            r = float(input_data[idx+2])
            advertisers.append({
                'id': i,
                'x': x,
                'y': y,
                'r': r
            })
        except ValueError:
            pass
        idx += 3

    # The problem asks for rectangles in a 10000 x 10000 square.
    # The previous code used 1000000.0 which was likely wrong.
    # Also, the output must be integers or formatted such that the scorer can read them.
    # The scorer error 'failed to parse 0.0 to i64' suggests it expects integers.
    
    results = [None] * N

    def partition(points, x_min, y_min, x_max, y_max):
        if not points:
            return
        
        if len(points) == 1:
            p = points[0]
            # Ensure the point is actually inside the rectangle
            # and the rectangle is within [0, 10000]
            rx_min = max(0, min(x_min, p['x']))
            ry_min = max(0, min(y_min, p['y']))
            rx_max = min(10000, max(x_max, p['x']))
            ry_max = min(10000, max(y_max, p['y']))
            # To be safe and non-overlapping, we use the split bounds
            results[p['id']] = (int(x_min), int(y_min), int(x_max), int(y_max))
            return

        width = x_max - x_min
        height = y_max - y_min
        
        if width > height:
            points.sort(key=lambda p: p['x'])
            mid = len(points) // 2
            split_val = points[mid]['x']
            # Clamp split_val to ensure progress and stay in bounds
            split_val = max(x_min + 1e-7, min(x_max - 1e-7, split_val))
            partition(points[:mid], x_min, y_min, split_val, y_max)
            partition(points[mid:], split_val, y_min, x_max, y_max)
        else:
            points.sort(key=lambda p: p['y'])
            mid = len(points) // 2
            split_val = points[mid]['y']
            split_val = max(y_min + 1e-7, min(y_max - 1e-7, split_val))
            partition(points[:mid], x_min, y_min, x_max, split_val)
            partition(points[mid:], x_min, split_val, x_max, y_max)

    # Use the correct bounds 0 to 10000
    partition(advertisers, 0, 0, 10000, 10000)

    for i in range(N):
        res = results[i]
        if res:
            # Print as integers to satisfy the scorer's i64 requirement
            print(f"{int(res[0])} {int(res[1])} {int(res[2])} {int(res[3])}")
        else:
            # Fallback for safety: a tiny rectangle containing the point
            # This shouldn't happen with the partition logic
            p = advertisers[i]
            print(f"{int(p['x'])} {int(p['y'])} {int(p['x'])+1} {int(p['y'])+1}")

if __name__ == '__main__':
    solve()
