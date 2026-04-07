import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    targets = []
    idx = 1
    for _ in range(N):
        a = int(input_data[idx])
        b = int(input_data[idx+1])
        targets.append((a, b))
        idx += 2

    # Sort targets to process them in a way that facilitates building
    # Sorting by x then y helps in finding 'predecessors' easily.
    # However, a simple greedy approach: for each target, find the best existing point.
    
    existing_points = [(0, 0)]
    operations = []

    # To optimize, we sort targets by their Manhattan distance from origin or simply by x+y
    # This ensures we process 'smaller' targets first.
    sorted_targets = sorted(targets, key=lambda p: (p[0] + p[1]))

    for tx, ty in sorted_targets:
        best_dist = float('inf')
        best_source = None

        for sx, sy in existing_points:
            if tx >= sx and ty >= sy:
                dist = (tx - sx) + (ty - sy)
                if dist < best_dist:
                    best_dist = dist
                    best_source = (sx, sy)
        
        # If for some reason no source is found (shouldn't happen as (0,0) is always there)
        # but if tx or ty were negative, we'd need to handle it. 
        # The problem implies tx >= fx and ty >= fy.
        if best_source is not None:
            sx, sy = best_source
            operations.append((sx, sy, tx, ty))
            existing_points.append((tx, ty))
        else:
            # This case should not be reachable given (0,0) and tx, ty >= 0
            pass

    print(len(operations))
    for op in operations:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == "__main__":
    solve()