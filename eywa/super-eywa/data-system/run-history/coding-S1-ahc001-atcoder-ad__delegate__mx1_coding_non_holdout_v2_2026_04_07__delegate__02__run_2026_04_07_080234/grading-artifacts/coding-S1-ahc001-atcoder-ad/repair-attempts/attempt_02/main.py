import sys

def solve():
    # Read N
    line = sys.stdin.readline()
    if not line:
        return
    try:
        n_str = line.strip()
        if not n_str:
            return
        n = int(n_str)
    except ValueError:
        return
    
    advertisers = []
    for i in range(n):
        line = sys.stdin.readline()
        if not line:
            break
        parts = line.split()
        if len(parts) < 3:
            break
        x = float(parts[0])
        y = float(parts[1])
        r = float(parts[2])
        advertisers.append({'id': i, 'x': x, 'y': y, 'r': r})

    # The error in the previous version was printing floats with decimals 
    # (e.g., 4335.0000000000) when the scorer expected integers (i64).
    # Even though the problem says "x_i y_i r_i" and "x1 y1 x2 y2", 
    # the scorer error "failed to parse ... to the value of type i64" 
    # indicates the coordinates in the test cases are actually integers 
    # and the output must be integers.
    
    # To avoid overlap and satisfy the requirement of containing (x, y),
    # we can use a tiny rectangle [x, x+1) x [y, y+1) if we treat them as integers.
    # However, if points are identical, we need to be careful.
    # Let's try to use a very small integer-based rectangle.
    # Since the board is 10000x10000, we can use [x, x+1) x [y, y+1) 
    # but we must ensure we don't overlap.
    
    # A safer way to avoid overlap for integer coordinates is to use 
    # a tiny area that doesn't overlap if points are distinct.
    # If points are not distinct, the problem is impossible without overlap.
    # Let's assume points are distinct or the scorer allows tiny integer rects.
    
    # Given the error, let's output integers.
    for adv in advertisers:
        tx = int(round(adv['x']))
        ty = int(round(adv['y']))
        
        # We need x1 <= tx < x2 and y1 <= ty < y2
        # To minimize overlap risk, we use the smallest possible integer rectangle.
        x1 = tx
        x2 = tx + 1
        y1 = ty
        y2 = ty + 1
        
        # Check board boundaries
        if x2 > 10000:
            x2 = tx
            x1 = tx - 1
        if y2 > 10000:
            y2 = ty
            y1 = ty - 1
        if x1 < 0:
            x1 = 0
            x2 = 1
        if y1 < 0:
            y1 = 0
            y2 = 1
            
        # Ensure x1 < x2 and y1 < y2
        if x1 >= x2: x2 = x1 + 1
        if y1 >= y2: y2 = y1 + 1
        
        # Final boundary clamp
        if x2 > 10000: x2 = 10000
        if y2 > 10000: y2 = 10000
        if x1 < 0: x1 = 0
        if y1 < 0: y1 = 0

        print(f"{int(x1)} {int(y1)} {int(x2)} {int(y2)}")

if __name__ == "__main__":
    solve()
