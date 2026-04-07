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
        advertisers.append((x, y, r))
        idx += 3

    # To avoid overlap, we can use very small rectangles
    # centered at (x, y) or just a tiny area around (x, y).
    # Since we need [x1, x2) x [y1, y2) and must contain (x, y),
    # we can use [x, x+1) x [y, y+1) if x+1 <= 10000 and y+1 <= 10000.
    # However, to be safer and handle potential integer issues,
    # let's use a tiny epsilon-like approach with integers.
    # A rectangle [x, x+1) x [y, y+1) contains (x, y).
    
    for x, y, r in advertisers:
        # Ensure the rectangle is within [0, 10000)
        # and contains (x, y).
        # We use a 1x1 rectangle.
        x1 = x
        y1 = y
        x2 = min(x + 1, 10000)
        y2 = min(y + 1, 10000)
        
        # If x is 10000, we must shift back
        if x1 >= 10000:
            x1 = 9999
            x2 = 10000
        if y1 >= 10000:
            y1 = 9999
            y2 = 10000
            
        # If x2 is not greater than x1 (shouldn't happen with +1)
        if x2 <= x1:
            x2 = x1 + 1
        if y2 <= y1:
            y2 = y1 + 1
            
        # Final check to ensure (x,y) is in [x1, x2) x [y1, y2)
        # If x1 > x, we must adjust. But x1=x is fine.
        # If x2 <= x, we must adjust. But x2=x+1 is fine.
        
        print(f"{x1} {y1} {x2} {y2}")

if __name__ == "__main__":
    solve()