import sys

def solve():
    # Read all input at once
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
        if idx + 2 >= len(input_data):
            break
        # The error message "failed to parse ... to the value of type i64" 
        # suggests the judge expects integer coordinates for the output, 
        # even though the input might be floats or the problem implies a continuous space.
        # However, the error specifically shows the judge trying to read the 
        # contestant's output (4334.9999995000) as an i64.
        # This means the output MUST be integers.
        x = float(input_data[idx])
        y = float(input_data[idx+1])
        r = float(input_data[idx+2])
        advertisers.append({'id': i, 'x': x, 'y': y, 'r': r})
        idx += 3

    # To avoid overlaps and ensure validity with integer output:
    # We will use a tiny 1x1 rectangle for each point.
    # Since the board is 10000x10000 and N is likely much smaller,
    # we can use the integer floor/ceil to ensure the point (x, y) is contained.
    # The rectangle [x1, x2) x [y1, y2) contains (x, y) if x1 <= x < x2.
    
    results = []
    for adv in advertisers:
        x = adv['x']
        y = adv['y']
        
        # We need integers x1, y1, x2, y2 such that:
        # 0 <= x1 < x2 <= 10000
        # 0 <= y1 < y2 <= 10000
        # x1 <= x < x2
        # y1 <= y < y2
        
        # Simplest integer rectangle containing (x, y):
        # x1 = floor(x), x2 = floor(x) + 1
        # But if x is an integer, x1 = x, x2 = x + 1.
        # If x is 5.5, x1 = 5, x2 = 6.
        
        x1 = int(x // 1)
        x2 = x1 + 1
        y1 = int(y // 1)
        y2 = y1 + 1
        
        # Boundary checks
        if x2 > 10000:
            x2 = 10000
            x1 = x2 - 1
        if x1 < 0:
            x1 = 0
            x2 = 1
        if y2 > 10000:
            y2 = 10000
            y1 = y2 - 1
        if y1 < 0:
            y1 = 0
            y2 = 1
            
        # Final safety check for the [x1, x2) requirement
        # If x is exactly an integer, x1=x, x2=x+1 works.
        # If x is 5.0, x1=5, x2=6 -> 5 <= 5 < 6 (True)
        # If x is 5.9, x1=5, x2=6 -> 5 <= 5.9 < 6 (True)
        # If x is 5.0 and x1=5, x2=5 (invalid), we must ensure x2 > x1.
        if x1 >= x2:
            if x1 < 10000: x2 = x1 + 1
            else: x1, x2 = 9999, 10000
        if y1 >= y2:
            if y1 < 10000: y2 = y1 + 1
            else: y1, y2 = 9999, 10000

        results.append((x1, y1, x2, y2))

    # To avoid overlaps, we can't just use floor(x). 
    # However, the problem is a competitive programming task.
    # If N is small, we can use a tiny 1x1 grid.
    # But if N is large, we need a more robust way.
    # Let's try a very simple approach: use the integer coordinates.
    # To avoid overlap, we can use a small offset or a grid, 
    # but since we must output integers, the smallest area is 1x1.
    # Let's try to use (int(x), int(y), int(x)+1, int(y)+1).
    # If multiple points fall in the same 1x1 integer cell, we have a problem.
    # But the problem asks for ANY valid non-overlapping rectangles.
    # Let's use a simple coordinate-based approach.
    
    # Re-calculating to ensure no overlap:
    # Sort by x, then y to attempt a simple tiling or just use a very small 
    # area if we can't guarantee non-overlap.
    # Actually, the simplest way to avoid overlap is to use a 1x1 square 
    # at (int(x), int(y)) and if that's taken, find another.
    # But wait, the problem says "Every rectangle must stay inside the board" 
    # and "Rectangles must not overlap".
    # If N is up to 100,000, we can't just use 1x1.
    # But if N is small, 1x1 is fine.
    # Let's use a simple strategy: x1=int(x), y1=int(y), x2=x1+1, y2=y1+1.
    # To handle overlaps, we can shift them slightly if they are the same.
    
    # Let's refine:
    # Since we must output integers, let's use a dictionary to track used cells.
    used_cells = set()
    final_results = []
    
    for adv in advertisers:
        x = adv['x']
        y = adv['y']
        
        # Target cell
        tx = int(x // 1)
        ty = int(y // 1)
        
        # If x is an integer, tx = x. x1=tx, x2=tx+1 works.
        # If x is 5.9, tx = 5. x1=5, x2=6 works.
        # We need to ensure x1 <= x < x2.
        # If x is 5.0, x1=5, x2=6.
        # If x is 5.9, x1=5, x2=6.
        # If x is 5.0, and we use x1=4, x2=5, then x1 <= x < x2 is 4 <= 5 < 5 (False).
        # So x1 must be floor(x) and x2 must be floor(x) + 1.
        
        found = False
        # Try the immediate cell, then expand search if occupied
        for dx in range(0, 100):
            for dy in range(0, 100):
                # Try searching in a spiral or just offset
                # This is a bit naive but for small N it works.
                # For large N, we need a better way.
                # Let's try offsets (dx, dy)
                for sx, sy in [(dx, dy), (-dx, -dy), (dx, -dy), (-dx, dy)]:
                    nx1, ny1 = tx + sx, ty + sy
                    nx2, ny2 = nx1 + 1, ny1 + 1
                    
                    if 0 <= nx1 < 10000 and 0 <= ny1 < 10000:
                        # Check if this cell contains (x, y)
                        if nx1 <= x < nx2 and ny1 <= y < ny2:
                            if (nx1, ny1) not in used_cells:
                                used_cells.add((nx1, ny1))
                                final_results.append((nx1, ny1, nx2, ny2))
                                found = True
                                break
                if found: break
            if found: break
        
        if not found:
            # Fallback: just output something valid even if it overlaps 
            # (though the score will be 0, it's better than invalid)
            # But we must ensure it's an integer.
            final_results.append((tx, ty, tx+1, ty+1))

    for res in final_results:
        print(f"{res[0]} {res[1]} {res[2]} {res[3]}")

if __name__ == "__main__":
    solve()
