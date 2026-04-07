import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    try:
        N = int(input_data[0])
    except ValueError:
        return

    advertisers = []
    idx = 1
    for i in range(N):
        # The error log suggests the scorer expects integer coordinates.
        # Even if the input is provided as floats, the output must be integers
        # to avoid the ParseIntError in the Rust-based scorer.
        x = int(float(input_data[idx]))
        y = int(float(input_data[idx+1]))
        r = float(input_data[idx+2])
        advertisers.append({'id': i, 'x': x, 'y': y, 'r': r})
        idx += 3

    # To avoid overlaps and ensure validity, we use a tiny 1x1 rectangle.
    # The problem states [x1, x2) x [y1, y2).
    # For a point (x, y), the smallest valid integer rectangle is [x, x+1) x [y, y+1).
    # However, we must ensure x+1 and y+1 do not exceed the 10000 boundary.
    
    results = []
    for adv in advertisers:
        x, y = adv['x'], adv['y']
        
        # Default 1x1 rectangle
        x1, x2 = x, x + 1
        y1, y2 = y, y + 1
        
        # Boundary checks for 10000x10000 board
        if x2 > 10000:
            x2 = 10000
            x1 = x
            if x1 >= x2: # Handle edge case where x is 10000
                x1 = x - 1
                
        if y2 > 10000:
            y2 = 10000
            y1 = y
            if y1 >= y2: # Handle edge case where y is 10000
                y1 = y - 1
        
        # Final safety check to ensure x1 <= x < x2 and y1 <= y < y2
        # If x is 10000, we must use [9999, 10000)
        if x == 10000:
            x1, x2 = 9999, 10000
        elif x < 0: # Should not happen based on problem but for safety
            x1, x2 = 0, 1
            
        if y == 10000:
            y1, y2 = 9999, 10000
        elif y < 0:
            y1, y2 = 0, 1

        results.append((x1, y1, x2, y2))

    # Print results as integers to satisfy the scorer's i64 requirement
    for res in results:
        print(f"{int(res[0])} {int(res[1])} {int(res[2])} {int(res[3])}")

if __name__ == "__main__":
    solve()
