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
        advertisers.append({'id': i, 'x': x, 'y': y, 'r': r})
        idx += 3

    results = [None] * N

    def subdivide(x_min, y_min, x_max, y_max, ads):
        if not ads:
            return
        
        # If only one advertiser in this cell, give them the whole cell
        if len(ads) == 1:
            ad = ads[0]
            # Ensure the point is strictly inside the rectangle [x1, x2) x [y1, y2)
            # The problem says [x1, x2) x [y1, y2), so x1 <= x < x2
            # We must ensure x_min <= ad['x'] < x_max
            # If the subdivision logic is correct, this is guaranteed.
            # However, we must handle the case where x_min == x_max or y_min == y_max
            if x_max > x_min and y_max > y_min:
                # Clamp to ensure point is inside
                rx1 = x_min
                ry1 = y_min
                rx2 = x_max
                ry2 = y_max
                
                # If point is on the boundary, adjust slightly to keep it inside [x1, x2)
                if not (rx1 <= ad['x'] < rx2 and ry1 <= ad['y'] < ry2):
                    # This case shouldn't happen with integer midpoints and x_min <= x < x_max
                    # but for safety:
                    rx1 = max(x_min, min(ad['x'], x_max - 1))
                    ry1 = max(y_min, min(ad['y'], y_max - 1))
                    rx2 = max(rx1 + 1, x_max)
                    ry2 = max(ry1 + 1, y_max)
                
                results[ad['id']] = (rx1, ry1, rx2, ry2)
            else:
                # Fallback to a 1x1 pixel if the cell is too small
                # This is a safety measure to ensure we always output something
                # though the quadtree should prevent this.
                results[ad['id']] = (ad['x'], ad['y'], ad['x'] + 1, ad['y'] + 1)
            return

        # Split the cell into 4 quadrants
        mid_x = (x_min + x_max) // 2
        mid_y = (y_min + y_max) // 2

        # To prevent infinite recursion if mid_x == x_min or mid_y == y_min
        if mid_x == x_min and mid_x + 1 < x_max:
            mid_x = x_min + (x_max - x_min) // 2 # redundant but safe
        
        # Define quadrants
        quads = [
            (x_min, y_min, mid_x, mid_y),
            (mid_x, y_min, x_max, mid_y),
            (x_min, mid_y, mid_x, y_max),
            (mid_x, mid_y, x_max, y_max)
        ]

        # Sort quadrants to process them
        for q_x1, q_y1, q_x2, q_y2 in quads:
            if q_x1 >= q_x2 or q_y1 >= q_y2:
                continue
            
            sub_ads = []
            for ad in ads:
                if q_x1 <= ad['x'] < q_x2 and q_y1 <= ad['y'] < q_y2:
                    sub_ads.append(ad)
            
            if sub_ads:
                subdivide(q_x1, q_y1, q_x2, q_y2, sub_ads)

    # Start subdivision with the full board
    subdivide(0, 0, 10000, 10000, advertisers)

    # Final output
    for i in range(N):
        if results[i] is not None:
            print(f"{results[i][0]} {results[i][1]} {results[i][2]} {results[i][3]}")
        else:
            # If for some reason an advertiser wasn't assigned a cell, 
            # provide a minimal valid 1x1 rectangle containing the point.
            # This ensures we always output N lines.
            x, y = advertisers[i]['x'], advertisers[i]['y']
            # Ensure it's within [0, 10000)
            x = max(0, min(9999, x))
            y = max(0, min(9999, y))
            print(f"{x} {y} {x+1} {y+1}")

if __name__ == "__main__":
    solve()
