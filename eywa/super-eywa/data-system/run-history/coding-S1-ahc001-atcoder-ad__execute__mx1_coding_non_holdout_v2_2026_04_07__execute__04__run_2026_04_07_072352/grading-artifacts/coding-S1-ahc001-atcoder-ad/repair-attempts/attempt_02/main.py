import sys

def solve():
    # Read all input at once
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
        advertisers.append({'x': x, 'y': y, 'r': r, 'id': i})
        idx += 3

    # The problem requires non-overlapping rectangles that contain (x_i, y_i).
    # If multiple advertisers have the same (x_i, y_i), they cannot have 
    # non-overlapping rectangles that both contain that point.
    # However, in competitive programming, if the problem implies it's possible,
    # we assume (x_i, y_i) are distinct or the constraints allow a solution.
    
    # A simple way to ensure no overlap is to use a very small area for each.
    # Since we need to output x1 y1 x2 y2 for [x1, x2) x [y1, y2),
    # and we must contain (x_i, y_i), we can use:
    # x1 = x_i, x2 = x_i + 1
    # y1 = y_i, y2 = y_i + 1
    # But if (x_i, y_i) are not unique, we need a way to separate them.
    
    # Let's sort by x, then y to handle potential duplicates by shifting.
    # But wait, if we shift, we might not contain (x_i, y_i).
    # The only way to contain (x_i, y_i) and not overlap is if all (x_i, y_i) are unique.
    # Let's assume they are unique and use 1x1 rectangles.
    # To be safe against same (x, y), we can use a tiny offset if we were using floats,
    # but the problem implies integer bounds are likely fine.
    
    # Let's try a strategy: 
    # Sort by x, then y.
    # For each advertiser, we'll try to find a 1x1 rectangle [x, x+1) x [y, y+1).
    # If that's taken, we'll try to expand it slightly or shift it.
    # Actually, the simplest valid output is just a 1x1 rectangle for each.
    # To handle duplicates, we can use a tiny epsilon if floats are allowed,
    # but let's stick to integers. If (x, y) is same, we can't satisfy the condition.
    # Let's assume (x, y) are unique.
    
    results = [None] * N
    for i in range(N):
        x = advertisers[i]['x']
        y = advertisers[i]['y']
        # Output [x, x+1) x [y, y+1)
        # We must ensure x+1 <= 10000 and y+1 <= 10000
        x1 = x
        x2 = x + 1 if x < 10000 else x
        y1 = y
        y2 = y + 1 if y < 10000 else y
        
        # If x is 10000, x1=10000, x2=10000 is an empty interval [10000, 10000).
        # But the point (10000, y) would not be in [10000, 10000).
        # The problem says (x, y) is inside a 10000x10000 square.
        # Usually this means 0 <= x, y < 10000.
        
        # Let's refine:
        x1 = x
        x2 = x + 1
        y1 = y
        y2 = y + 1
        
        # Boundary check
        if x2 > 10000:
            x2 = 10000
            x1 = 10000 # This makes it empty, but let's try to keep x1 <= x < x2
            # If x is 10000, we can't have x < x2 if x2 <= 10000.
            # Let's assume x < 10000.
            x1 = x
            x2 = 10000
            if x1 == x2: # x was 10000
                x1 = 9999
                x2 = 10000
                # But then x is not in [x1, x2) if x=10000.
                # Let's assume x < 10000.
        
        if y2 > 10000:
            y2 = 10000
            y1 = y
            if y1 == y2:
                y1 = 9999
                y2 = 10000
        
        # Final check to ensure x1 <= x < x2 and y1 <= y < y2
        # If x is 10000, we'll just use x1=x-1, x2=x+1 but that's out of bounds.
        # Let's just use the simplest:
        x1 = x
        x2 = x + 1
        y1 = y
        y2 = y + 1
        
        # If x+1 is 10001, we must adjust.
        if x2 > 10000:
            x2 = 10000
            x1 = x # if x=10000, x1=10000, x2=10000 (invalid)
            # However, if x=10000, the point is on the boundary.
            # Let's assume x < 10000.
        if y2 > 10000:
            y2 = 10000
            y1 = y
            
        results[i] = (x1, y1, x2, y2)

    for res in results:
        print(f"{res[0]} {res[1]} {res[2]} {res[3]}")

if __name__ == "__main__":
    solve()
