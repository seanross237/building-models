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

    # To avoid overlap and ensure the point (x, y) is contained,
    # we can use a very small rectangle [x, x+1) x [y, y+1).
    # However, the problem states the rectangle is [x1, x2) x [y1, y2).
    # To contain (x, y), we must have x1 <= x < x2 and y1 <= y < y2.
    # A simple way to avoid overlap is to use a grid-based approach or 
    # simply ensure each rectangle is a 1x1 unit that doesn't overlap.
    # But since points (x, y) can be the same, we need to offset them.
    
    # Let's try a very simple strategy: 
    # For each advertiser, output [x, x+1) [y, y+1).
    # If points are identical, we must shift them slightly to avoid overlap.
    # Since the board is 10000x10000 and N is likely not huge, 
    # we can use a small epsilon or just integer offsets.
    
    # However, the simplest way to guarantee no overlap for any N is to 
    # treat the points as centers of 1x1 cells and if they collide, 
    # find the next available cell.
    
    used_cells = set()
    
    for x, y, r in advertisers:
        curr_x, curr_y = x, y
        
        # Find the first available 1x1 cell [curr_x, curr_x+1) x [curr_y, curr_y+1)
        # that contains the point (x, y) or is shifted.
        # Wait, the rectangle MUST contain (x, y). 
        # If we shift the rectangle, it might not contain (x, y) anymore.
        # The only way to have multiple rectangles containing the same (x, y) 
        # without overlapping is impossible if they are all 1x1 and integer-aligned.
        # BUT, the problem says "Rectangle i must contain its requested point (x_i, y_i)".
        # If two advertisers request the same point, their rectangles MUST overlap 
        # unless the point is on the boundary. 
        # But the interval is [x1, x2), so x1 <= x < x2.
        # If two rectangles contain the same x, they must have different y-ranges.
        
        # Let's use a tiny width/height or just ensure they are disjoint.
        # If (x, y) is the same, we can use [x, x+1) [y, y+1), [x, x+1) [y+1, y+2), etc.
        # But [x, x+1) [y+1, y+2) does NOT contain (x, y) if y+1 > y.
        # Actually, the only way to contain (x, y) is if x1 <= x < x2 and y1 <= y < y2.
        # If two rectangles contain the same (x, y), they overlap.
        # Therefore, the input must not have overlapping (x, y) OR 
        # the rectangles can be extremely thin.
        # Wait, if x1=x, x2=x+0.000001, it contains x.
        # But the output format is usually integers in these problems.
        # Let's assume integer coordinates. If (x, y) are the same, 
        # we can use [x, x+1) [y, y+1) for the first, and for the second, 
        # we need a rectangle that contains (x, y) but doesn't overlap.
        # This is only possible if the point (x, y) is on the boundary.
        # For [x1, x2), the point x is included if x1 <= x < x2.
        # If we have two rectangles:
        # Rect 1: [x, x+1) [y, y+1) -> contains (x, y)
        # Rect 2: [x-1, x) [y, y+1) -> does NOT contain x.
        # Rect 2: [x, x+1) [y-1, y) -> does NOT contain y.
        # The only way is if the point is on the edge.
        # Let's try: Rect 1: [x, x+1) [y, y+1).
        # If (x, y) is taken, try [x-1, x+1) [y, y+1) ? No, that overlaps.
        # Actually, if the points are unique, [x, x+1) [y, y+1) works.
        # If points are not unique, the problem might be impossible with integer bounds 
        # unless we use the fact that x1 <= x < x2.
        # If we use x1 = x, x2 = x+1, then x is included.
        # If we use x1 = x-1, x2 = x, then x is NOT included.
        # So for a point (x, y), the only integer-aligned 1x1 rectangle containing it is [x, x+1) [y, y+1).
        # If multiple advertisers want (x, y), they MUST overlap.
        # UNLESS the problem allows non-integer coordinates? 
        # "Print exactly N lines... x1 y1 x2 y2". Usually implies integers.
        # Let's check the constraints. If (x, y) are unique, [x, x+1) [y, y+1) is safe.
        
        print(f"{x} {y} {x+1} {y+1}")

if __name__ == "__main__":
    solve()
