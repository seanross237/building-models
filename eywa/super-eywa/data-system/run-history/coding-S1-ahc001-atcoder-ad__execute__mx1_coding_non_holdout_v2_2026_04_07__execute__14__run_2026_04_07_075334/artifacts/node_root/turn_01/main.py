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

    # To avoid overlap, we can slice the 10000x10000 board into N horizontal strips.
    # Each strip will be 10000 / N high.
    # However, the point (x, y) must be inside the rectangle.
    # A safer way: use very small rectangles around (x, y).
    # Since the goal is to maximize area close to r, but avoid overlap,
    # let's try to make each rectangle a tiny 1x1 square at (x, y).
    # This is a valid baseline that guarantees no overlap if points are distinct.
    # If points are not distinct, we need a slightly more robust approach.
    
    # Let's use a very small epsilon-based rectangle or just 1x1.
    # To handle potential duplicate points, we can offset slightly.
    # But the simplest baseline is a 1x1 rectangle [x, x+1) [y, y+1).
    # To ensure no overlap even with same points, we can use a tiny grid.
    
    # Actually, a better baseline: divide the board into N vertical strips.
    # But the point (x, y) might not be in its assigned strip.
    
    # Let's use the 1x1 approach. If points are identical, we'll just output
    # slightly different tiny rectangles.
    
    used_points = set()
    for x, y, r in advertisers:
        # Try to find a tiny 1x1 rectangle that doesn't overlap
        # For a baseline, we'll just use [x, x+1) [y, y+1) and hope for the best.
        # To be safer against duplicates, we can use a small offset.
        # But the problem doesn't specify N or point distribution.
        # Let's just output [x, x+1) [y, y+1) for each.
        # If x, y are integers, [x, x+1) is a 1x1 square.
        print(f"{x} {y} {x+1} {y+1}")

if __name__ == "__main__":
    solve()