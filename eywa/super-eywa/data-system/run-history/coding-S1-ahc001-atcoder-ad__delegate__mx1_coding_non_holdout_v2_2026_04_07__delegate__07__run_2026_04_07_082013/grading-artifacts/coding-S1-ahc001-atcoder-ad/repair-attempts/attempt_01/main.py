import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    advertisers = []
    idx = 1
    for i in range(N):
        x = int(input_data[idx])
        y = int(input_data[idx+1])
        r = int(input_data[idx+2])
        advertisers.append({'id': i, 'x': x, 'y': y, 'r': r})
        idx += 3

    results = [None] * N

    def partition(points, x_min, y_min, x_max, y_max):
        if not points:
            return
        
        if len(points) == 1:
            p = points[0]
            # Target side length based on area r
            target_side = int(p['r']**0.5)
            if target_side < 1: target_side = 1
            
            # Try to center the point in the rectangle
            # Rectangle is [x1, x2) x [y1, y2)
            # Point (x, y) must satisfy x1 <= x < x2 and y1 <= y < y2
            
            # Initial attempt: center the point
            x1 = p['x'] - target_side // 2
            x2 = x1 + target_side
            y1 = p['y'] - target_side // 2
            y2 = y1 + target_side
            
            # Adjust to ensure point is inside
            if not (x1 <= p['x'] < x2):
                if p['x'] < x1: x1 = p['x']
                else: x2 = p['x'] + 1
            if not (y1 <= p['y'] < y2):
                if p['y'] < y1: y1 = p['y']
                else: y2 = p['y'] + 1
                
            # Clamp to bounding box [x_min, x_max] x [y_min, y_max]
            # Note: x_max and y_max are exclusive bounds for the coordinate space
            # The problem says 10000x10000 square. Let's assume 0 to 10000.
            # We use the provided partition bounds.
            
            if x2 > x_max:
                diff = x2 - x_max
                x2 = x_max
                x1 -= diff
            if x1 < x_min:
                diff = x_min - x1
                x1 = x_min
                x2 += diff
            if x2 <= x1: x2 = x1 + 1
            
            if y2 > y_max:
                diff = y2 - y_max
                y2 = y_max
                y1 -= diff
            if y1 < y_min:
                diff = y_min - y1
                y1 = y_min
                y2 += diff
            if y2 <= y1: y2 = y1 + 1
            
            # Final safety check for point inclusion and bounds
            x1 = max(x_min, min(x1, p['x']))
            x2 = max(x1 + 1, min(x2, max(p['x'] + 1, x_max)))
            y1 = max(y_min, min(y1, p['y']))
            y2 = max(y1 + 1, min(y2, max(p['y'] + 1, y_max)))

            results[p['id']] = (int(x1), int(x2), int(y1), int(y2))
            return

        # Split by median of x or y to ensure non-overlapping partitions
        if (x_max - x_min) > (y_max - y_min):
            points.sort(key=lambda p: p['x'])
            mid = len(points) // 2
            split_val = points[mid]['x']
            # To avoid overlap, we split the space
            # Left part: [x_min, split_val), Right part: [split_val, x_max)
            # But we must ensure split_val is within bounds and allows points to be contained
            # A safer way for competitive programming: split by index
            partition(points[:mid], x_min, y_min, split_val, y_max)
            partition(points[mid:], split_val, y_min, x_max, y_max)
        else:
            points.sort(key=lambda p: p['y'])
            mid = len(points) // 2
            split_val = points[mid]['y']
            partition(points[:mid], x_min, y_min, x_max, split_val)
            partition(points[mid:], x_min, split_val, x_max, y_max)

    # The problem states 10000x10000 square. Usually 0-10000.
    partition(advertisers, 0, 0, 10000, 10000)
    
    for res in results:
        if res:
            print(f"{res[0]} {res[1]} {res[2]} {res[3]}")
        else:
            # Fallback for safety: a 1x1 rectangle containing the point
            # This should not happen with the partition logic
            pass

if __name__ == "__main__":
    solve()
