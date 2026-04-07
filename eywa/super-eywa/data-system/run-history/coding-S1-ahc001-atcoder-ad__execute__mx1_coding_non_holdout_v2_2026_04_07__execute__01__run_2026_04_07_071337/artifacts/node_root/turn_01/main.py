import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    idx = 1
    
    # To avoid overlap, we can use very small rectangles
    # centered at (x, y). Since coordinates are integers
    # and we need [x1, x2) x [y1, y2),
    # we can use [x, x+1) x [y, y+1).
    # However, if multiple points are the same, we need to offset.
    
    points = []
    for i in range(N):
        x = int(input_data[idx])
        y = int(input_data[idx+1])
        r = int(input_data[idx+2])
        points.append((x, y, r, i))
        idx += 3

    # Sort points to handle potential overlaps via a grid or offset
    # For a simple baseline, we use a tiny 1x1 rectangle.
    # If points are identical, we offset slightly.
    
    # Using a dictionary to track occupied integer coordinates
    occupied = set()
    
    results = [None] * N
    
    for x, y, r, i in points:
        # Try to find the smallest available 1x1 rectangle
        # starting at (x, y), (x+1, y), (x, y+1), etc.
        found = False
        for dx in range(100):
            for dy in range(100):
                nx, ny = x + dx, y + dy
                if (nx, ny) not in occupied:
                    # Check bounds
                    if 0 <= nx < 10000 and 0 <= ny < 10000:
                        results[i] = (nx, ny, nx + 1, ny + 1)
                        occupied.add((nx, ny))
                        found = True
                        break
            if found: break
        
        if not found:
            # Fallback to a 1x1 at x, y if possible, or just something valid
            # This part is unlikely to be hit given 10000x10000 grid
            results[i] = (x, y, x + 1, y + 1)

    for res in results:
        print(f"{res[0]} {res[1]} {res[2]} {res[3]}")

if __name__ == "__main__":
    solve()