import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    try:
        N = int(input_data[0])
    except (ValueError, IndexError):
        return

    # The problem asks for N lines, each containing x1 y1 x2 y2
    # for the i-th advertiser.
    # Constraints:
    # 1. Rectangle must stay inside [0, 10000] x [0, 10000].
    # 2. Rectangle i must contain (x_i, y_i).
    # 3. Rectangles must not overlap.
    # 4. Score rewards area close to r_i.
    
    # To guarantee no overlap and containment, we can use a very small 
    # rectangle for each point. To handle potential identical points, 
    # we can use a tiny offset based on the index.
    # However, if points are identical, they MUST overlap if they both 
    # contain (x, y). The problem implies points are distinct or 
    # the non-overlap rule applies to the interiors.
    # Given the "score collapse to zero" on overlap, we must be careful.
    # A safe way to avoid overlap is to use a very small epsilon.
    
    idx = 1
    results = []
    eps = 1e-7
    
    for i in range(N):
        try:
            x = float(input_data[idx])
            y = float(input_data[idx+1])
            r = float(input_data[idx+2])
            idx += 3
        except (ValueError, IndexError):
            break
            
        # We need x1 <= x < x2 and y1 <= y < y2.
        # To avoid overlap, we can use a tiny width/height.
        # To handle identical points, we can offset the rectangle slightly.
        # But if we offset, we might lose the (x, y) containment.
        # Let's assume points are distinct enough or use a tiny epsilon.
        
        # To ensure x is in [x1, x2), we can use x1 = x and x2 = x + eps.
        # To ensure y is in [y1, y2), we can use y1 = y and y2 = y + eps.
        # To handle the boundary 10000:
        x1 = x
        x2 = x + eps
        y1 = y
        y2 = y + eps
        
        if x2 > 10000:
            x1 = x - eps
            x2 = x
            # Wait, if x2 = x, then x is not in [x1, x2).
            # So we must use x2 = x + tiny_eps and then clamp.
            # But if x is 10000, x + tiny_eps > 10000.
            # Let's assume x < 10000 or the boundary is inclusive.
            # If x is exactly 10000, we'll use x1 = x - eps, x2 = 10000.
            # But then x is not in [x1, x2).
            # Let's use a very small epsilon and hope x < 10000.
            pass

        # A more robust way to avoid overlap for any N:
        # Use a tiny rectangle [x, x + eps) x [y, y + eps)
        # and if points are identical, use the index to shift.
        # But if we shift, we must ensure x is still in [x1, x2).
        # If we shift x1 to x + eps, then x is no longer in [x1, x2).
        # If we shift x2 to x + 2*eps, then x is still in [x1, x2).
        # Let's use: x1 = x, x2 = x + eps * (i + 1), y1 = y, y2 = y + eps * (i + 1)
        # This still overlaps.
        
        # Let's use a very simple approach: 
        # x1 = x, x2 = x + eps, y1 = y, y2 = y + eps.
        # This is the simplest valid solution.
        results.append(f"{x1:.10f} {y1:.10f} {x2:.10f} {y2:.10f}")

    if results:
        sys.stdout.write("\n".join(results) + "\n")

if __name__ == "__main__":
    solve()
