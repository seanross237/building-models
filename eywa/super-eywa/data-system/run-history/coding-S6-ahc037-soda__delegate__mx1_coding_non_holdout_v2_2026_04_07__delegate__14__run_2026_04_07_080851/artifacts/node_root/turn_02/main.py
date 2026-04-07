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

    # Sort targets primarily by x, then by y to facilitate a monotonic path
    # This helps in ensuring that for most points, a predecessor exists.
    targets.sort()

    # existing_beverages stores (x, y) coordinates of beverages we have already created
    existing_beverages = [(0, 0)]
    operations = []

    for tx, ty in targets:
        # We need to find an existing beverage (fx, fy) such that fx <= tx and fy <= ty
        # and (tx - fx) + (ty - fy) is minimized.
        best_source = None
        min_dist = float('inf')

        for fx, fy in existing_beverages:
            if fx <= tx and fy <= ty:
                dist = (tx - fx) + (ty - fy)
                if dist < min_dist:
                    min_dist = dist
                    best_source = (fx, fy)
                elif dist == min_dist:
                    # Tie-break: prefer source with larger coordinates to keep options open
                    if best_source is None or (fx + fy > best_source[0] + best_source[1]):
                        best_source = (fx, fy)

        # If for some reason no valid source is found (shouldn't happen with (0,0) and sorted targets)
        # we fallback to (0,0) but the problem constraints imply a valid path exists.
        if best_source is None:
            best_source = (0, 0)
            min_dist = tx + ty

        fx, fy = best_source
        operations.append((fx, fy, tx, ty))
        existing_beverages.append((tx, ty))

    # Output the results
    print(len(operations))
    for op in operations:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == "__main__":
    solve()