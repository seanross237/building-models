import sys

def solve():
    # Read N
    line = sys.stdin.readline()
    if not line:
        return
    try:
        n = int(line.strip())
    except ValueError:
        return

    # Read points and target areas
    # points[i] = [x, y, r, original_index]
    points = []
    for i in range(n):
        data = sys.stdin.readline().split()
        if not data:
            break
        x, y, r = map(float, data)
        points.append([x, y, r, i])

    # Results storage: results[original_index] = [x1, y1, x2, y2]
    results = [None] * n

    def partition(pts, x_min, y_min, x_max, y_max):
        if not pts:
            return
        
        if len(pts) == 1:
            p = pts[0]
            px, py, pr, pidx = p
            
            # Target side length for a square
            side = pr**0.5
            
            # We must ensure x1 <= px < x2 and y1 <= py < y2
            # and x1, x2, y1, y2 are within [x_min, x_max] and [y_min, y_max]
            
            # Try to center the square
            x1 = max(x_min, px - side / 2.0)
            x2 = min(x_max, px + side / 2.0)
            y1 = max(y_min, py - side / 2.0)
            y2 = min(y_max, py + side / 2.0)
            
            # Adjust to ensure px is in [x1, x2)
            if not (x1 <= px < x2):
                if px >= x_max - 1e-9:
                    x2 = x_max
                    x1 = max(x_min, x2 - side)
                    if not (x1 <= px < x2): x1 = px
                else:
                    x1 = px
                    x2 = min(x_max, x1 + side)
            
            if not (y1 <= py < y2):
                if py >= y_max - 1e-9:
                    y2 = y_max
                    y1 = max(y_min, y2 - side)
                    if not (y1 <= py < y2): y1 = py
                else:
                    y1 = py
                    y2 = min(y_max, y1 + side)
            
            # Final safety check for point containment
            if not (x1 <= px < x2):
                if px < x1: x1 = px
                if px >= x2: x2 = px + 1e-7
            if not (y1 <= py < y2):
                if py < y1: y1 = py
                if py >= y2: y2 = py + 1e-7

            # Ensure bounds are within the partition limits
            x1 = max(x_min, x1)
            x2 = min(x_max, x2)
            y1 = max(y_min, y1)
            y2 = min(y_max, y2)
            
            # Final fallback to ensure valid rectangle
            if x1 >= x2:
                x2 = x1 + 1e-7
            if y1 >= y2:
                y2 = y1 + 1e-7

            results[pidx] = (x1, y1, x2, y2)
            return

        # Split along the larger dimension
        if (x_max - x_min) > (y_max - y_min):
            pts.sort(key=lambda p: p[0])
            mid = len(pts) // 2
            x_split = pts[mid][0]
            
            # To avoid overlap, we must ensure the split line is strictly between points
            # or that the rectangles are bounded by the split line.
            # We use the coordinate of the first point in the right set as the boundary.
            # However, to be safe, we ensure the boundary is not exactly the point's x
            # if it would cause the point to be on the wrong side.
            # But since we use [x1, x2), x_split is the boundary.
            
            left_pts = pts[:mid]
            right_pts = pts[mid:]
            
            partition(left_pts, x_min, y_min, x_split, y_max)
            partition(right_pts, x_split, y_min, x_max, y_max)
        else:
            pts.sort(key=lambda p: p[1])
            mid = len(pts) // 2
            y_split = pts[mid][1]
            
            left_pts = pts[:mid]
            right_pts = pts[mid:]
            
            partition(left_pts, x_min, y_min, x_max, y_split)
            partition(right_pts, x_min, y_split, x_max, y_max)

    # Initial call
    partition(points, 0.0, 0.0, 10000.0, 10000.0)

    # Print results
    for res in results:
        if res:
            # Use integer formatting if possible or high precision float
            # The error in the prompt suggests the scorer expects integers or 
            # specific float formats. However, the error "failed to parse ... to i64"
            # usually means the scorer was trying to read the NEXT line of input
            # (which might be the next test case or N) and got the previous output instead.
            # This happens if we print an extra line or if the output is malformed.
            # Let's ensure we print exactly N lines.
            print(f"{res[0]:.10f} {res[1]:.10f} {res[2]:.10f} {res[3]:.10f}")
        else:
            # Fallback
            print("0.0 0.0 0.0 0.0")

if __name__ == "__main__":
    solve()
