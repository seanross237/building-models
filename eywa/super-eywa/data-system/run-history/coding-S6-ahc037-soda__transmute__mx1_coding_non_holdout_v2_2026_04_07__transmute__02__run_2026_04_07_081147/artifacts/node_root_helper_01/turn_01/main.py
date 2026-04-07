import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    targets = []
    idx = 1
    for _ in range(n):
        x = int(input_data[idx])
        y = int(input_data[idx+1])
        targets.append((x, y))
        idx += 2

    # Sort targets primarily by x, then by y to facilitate monotonic paths
    # This is a heuristic for the Steiner-like problem with monotonicity
    targets.sort()

    # We start with (0,0) in our set of available beverages
    current_beverages = [(0, 0)]
    operations = []

    # For each target, find the best existing beverage to connect from
    # 'Best' here means minimizing (tx-fx) + (ty-fy) subject to tx>=fx, ty>=fy
    for tx, ty in targets:
        best_dist = float('inf')
        best_source = None
        
        for fx, fy in current_beverages:
            if tx >= fx and ty >= fy:
                dist = (tx - fx) + (ty - fy)
                if dist < best_dist:
                    best_dist = dist
                    best_source = (fx, fy)
        
        if best_source:
            operations.append((best_source[0], best_source[1], tx, ty))
            current_beverages.append((tx, ty))
        else:
            # If no monotonic source found, we must connect from (0,0) 
            # or handle it by creating intermediate points. 
            # However, the problem implies a valid path exists.
            # In a grid with (0,0) and positive targets, (0,0) is always a fallback.
            # But we need to ensure monotonicity. If tx < fx or ty < fy, 
            # we can't use that source. Since we sort by x, tx >= fx is likely.
            # If ty < fy, we might need to find a different source.
            # Let's refine: find source with max fx <= tx and max fy <= ty.
            
            # Fallback: find any source that satisfies monotonicity
            # If none, this specific target might be unreachable under strict rules
            # but the problem implies a solution exists.
            pass

    print(len(operations))
    for op in operations:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == "__main__":
    solve()