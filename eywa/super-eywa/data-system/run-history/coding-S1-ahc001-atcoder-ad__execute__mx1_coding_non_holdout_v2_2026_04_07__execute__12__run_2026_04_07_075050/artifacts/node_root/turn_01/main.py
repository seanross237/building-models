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
    # However, we must ensure the point (x, y) is inside the strip.
    # A safer way for a baseline: use tiny 1x1 rectangles at (x, y).
    # Since the problem asks for area close to r, but overlap is fatal,
    # let's try to make very small rectangles that are guaranteed not to overlap.
    # Actually, a 1x1 rectangle [x, x+1) x [y, y+1) might overlap if points are same.
    # Let's use a very small epsilon-like approach or just tiny rectangles.
    # To be absolutely safe from overlap, we can use the fact that points are discrete.
    # But the problem doesn't say points are integers. Let's assume they are.
    
    for x, y, r in advertisers:
        # Output a tiny 1x1 rectangle centered (roughly) at (x, y)
        # To ensure no overlap, we can use a very small size or a grid.
        # Let's try a 0.1 x 0.1 rectangle if possible, but output must be integers?
        # The problem says [x1, x2) x [y1, y2). Usually these are integers in AtCoder.
        # Let's use [x, x+1) x [y, y+1) and hope points are distinct.
        # If points are not distinct, we need a better strategy.
        # Let's use a tiny rectangle [x, x+1) x [y, y+1) but adjust if needed.
        # Actually, the simplest non-overlapping way is to use a grid.
        # But we must contain (x, y).
        # Let's just output [x, x+1) x [y, y+1) for now.
        # If x, y are integers, this is a 1x1 square.
        print(f"{x} {y} {x+1} {y+1}")

if __name__ == '__main__':
    solve()