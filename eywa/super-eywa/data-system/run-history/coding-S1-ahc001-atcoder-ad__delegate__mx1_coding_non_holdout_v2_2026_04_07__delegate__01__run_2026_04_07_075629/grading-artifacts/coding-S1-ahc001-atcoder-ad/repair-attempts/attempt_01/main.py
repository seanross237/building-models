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
            
            # Try to center the square at (px, py)
            # We must ensure x1 <= px < x2 and y1 <= py < y2
            # and x1, x2, y1, y2 are within [x_min, x_max] and [y_min, y_max]
            
            # Initial attempt: centered square
            x1 = max(x_min, px - side / 2.0)
            x2 = min(x_max, px + side / 2.0)
            y1 = max(y_min, py - side / 2.0)
            y2 = min(y_max, py + side / 2.0)
            
            # Adjust to ensure px is in [x1, x2)
            if not (x1 <= px < x2):
                if px >= x_max - 1e-9: # px is at the right edge
                    x2 = x_max
                    x1 = max(x_min, x2 - side)
                    if not (x1 <= px < x2): x1 = px # fallback
                else:
                    x1 = px
                    x2 = min(x_max, x1 + side)
            
            if not (y1 <= py < y2):
                if py >= y_max - 1e-9:
                    y2 = y_max
                    y1 = max(y_min, y2 - side)
                    if not (y1 <= py < y2): y1 = py # fallback
                else:
                    y1 = py
                    y2 = min(y_max, y1 + side)
            
            # Final safety check for point containment
            if not (x1 <= px < x2):
                if px < x1: x1 = px
                if px >= x2: x2 = px + 1e-7 # tiny width
            if not (y1 <= py < y2):
                if py < y1: y1 = py
                if py >= y2: y2 = py + 1e-7

            results[pidx] = (x1, y1, x2, y2)
            return

        # Split along the larger dimension
        if (x_max - x_min) > (y_max - y_min):
            # Split X
            pts.sort(key=lambda p: p[0])
            mid = len(pts) // 2
            split_val = pts[mid][0]
            # Ensure split_val is strictly between the two sets if possible
            # but for BSP, we just split the list.
            # To avoid overlap, we use the split_val as the boundary.
            # However, the point itself might be on the boundary.
            # We must ensure the split_val is not a point's coordinate if it causes issues.
            # For simplicity, we split the list and use the coordinate of the first point in the right set.
            split_x = pts[mid][0]
            
            # To prevent overlap, we must ensure all points in left are < split_x
            # and all points in right are >= split_x.
            # But the rectangles must contain the points.
            # A safer way: split by index and use the coordinate of the split point.
            # But we need a boundary. Let's use the median x.
            
            left_pts = pts[:mid]
            right_pts = pts[mid:]
            
            # We need a boundary x_split such that left_pts are in [x_min, x_split]
            # and right_pts are in [x_split, x_max].
            # To ensure no overlap, we can use the x-coordinate of the first point in right_pts.
            # But we must be careful: the rectangle for the last point in left_pts 
            # could extend past this x_split.
            # A robust way: use the actual x-coordinates to define the split.
            
            # Find a split line that doesn't cut through a point's required area? 
            # No, we just need to ensure the rectangles don't overlap.
            # Let's use the median x as the boundary.
            x_split = pts[mid][0]
            
            # To ensure no overlap, we must ensure all rectangles in left are <= x_split
            # and all in right are >= x_split.
            # This is hard with arbitrary r. 
            # Let's refine: the partition defines the bounding box for the rectangles.
            partition(left_pts, x_min, y_min, x_split, y_max)
            partition(right_pts, x_split, y_min, x_max, y_max)
        else:
            # Split Y
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
            print(f"{res[0]:.10f} {res[1]:.10f} {res[2]:.10f} {res[3]:.10f}")
        else:
            # Fallback for any missed points (should not happen with BSP)
            print("0.0 0.0 0.0 0.0")

if __name__ == "__main__":
    solve()
