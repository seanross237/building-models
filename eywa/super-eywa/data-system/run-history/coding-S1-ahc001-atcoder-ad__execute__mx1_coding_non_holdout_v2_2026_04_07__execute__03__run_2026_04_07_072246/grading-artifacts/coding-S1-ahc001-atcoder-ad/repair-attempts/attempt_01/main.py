import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    advertisers = []
    idx = 1
    for i in range(N):
        x = float(input_data[idx])
        y = float(input_data[idx+1])
        r = float(input_data[idx+2])
        advertisers.append({'id': i, 'x': x, 'y': y, 'r': r})
        idx += 3

    # To avoid overlaps and ensure validity, we can use a very small 
    # rectangle around each point. Since the problem asks for 
    # [x1, x2) x [y1, y2), we can use a tiny epsilon.
    # However, to ensure no overlap even with floating point precision,
    # we can use a grid-based approach or simply very small distinct rectangles.
    
    # A simple way to avoid overlap is to make each rectangle a tiny 
    # square centered at (x, y) with a side length so small that 
    # they are unlikely to overlap unless points are identical.
    # Given the constraints and the goal of not overlapping, 
    # we'll use a very small epsilon.
    
    eps = 1e-9
    
    results = [None] * N
    for adv in advertisers:
        x, y = adv['x'], adv['y']
        
        # We need x1 <= x < x2 and y1 <= y < y2
        # Let's define a tiny rectangle [x-eps, x+eps) x [y-eps, y+eps)
        # But we must stay within [0, 10000]
        
        x1 = max(0.0, x - eps)
        x2 = min(10000.0, x + eps)
        y1 = max(0.0, y - eps)
        y2 = min(10000.0, y + eps)
        
        # Ensure x1 <= x < x2 and y1 <= y < y2
        if not (x1 <= x < x2):
            # If x is at the boundary, adjust
            if x == 0.0:
                x1 = 0.0
                x2 = eps
            elif x == 10000.0:
                x1 = 10000.0 - eps
                x2 = 10000.0
        
        if not (y1 <= y < y2):
            if y == 0.0:
                y1 = 0.0
                y2 = eps
            elif y == 10000.0:
                y1 = 10000.0 - eps
                y2 = 10000.0

        results[adv['id']] = (x1, y1, x2, y2)

    for res in results:
        print(f"{res[0]:.10f} {res[1]:.10f} {res[2]:.10f} {res[3]:.10f}")

if __name__ == "__main__":
    solve()
