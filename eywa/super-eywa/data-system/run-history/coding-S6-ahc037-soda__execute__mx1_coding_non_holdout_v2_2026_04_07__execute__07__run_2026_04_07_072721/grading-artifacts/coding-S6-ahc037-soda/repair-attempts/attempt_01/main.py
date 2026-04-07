import sys

def solve():
    # The problem asks to build 1000 target beverages from (0,0).
    # The input format for AHC problems usually provides N and then N pairs.
    # However, the current code fails because it doesn't follow the required output format.
    # Based on the problem description, we need to output the sequence of operations.
    # Since the exact output format (e.g., '1 beverage', then 'source_x source_y target_x target_y') 
    # is not explicitly detailed in the prompt but the scorer expects a specific format,
    # and the current code prints only the total cost, we will provide a simple valid baseline.
    # A common AHC output format is: 
    # Number of operations
    # For each operation: source_x source_y target_x target_y
    
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    try:
        N = int(input_data[0])
    except (ValueError, IndexError):
        return

    targets = []
    idx = 1
    for _ in range(N):
        if idx + 1 < len(input_data):
            a = int(input_data[idx])
            b = int(input_data[idx+1])
            targets.append((a, b))
            idx += 2

    # Sort targets to ensure monotonicity (fx <= tx and fy <= ty)
    # A simple way to ensure monotonicity is to sort by x then y.
    # However, if a target cannot be reached from any existing beverage, 
    # we must ensure we don't break the rules. 
    # The problem says "build a target set... using a sequence of monotone derivation operations".
    # This implies a path exists. Let's assume we can always reach targets from (0,0) 
    # or a previously created beverage.
    
    existing_beverages = [(0, 0)]
    operations = []

    # To ensure we can always find a source, we sort targets.
    # But simple sorting might not guarantee fx <= tx AND fy <= ty.
    # Let's try to build them one by one from (0,0) if needed, or from the closest.
    # For a baseline, let's just connect every target to (0,0) if possible, 
    # but that's only valid if 0 <= tx and 0 <= ty.
    
    for tx, ty in targets:
        if tx == 0 and ty == 0:
            continue
        
        # Find a source in existing_beverages such that fx <= tx and fy <= ty
        best_source = None
        min_dist = float('inf')
        
        for fx, fy in existing_beverages:
            if fx <= tx and fy <= ty:
                dist = (tx - fx) + (ty - fy)
                if dist < min_dist:
                    min_dist = dist
                    best_source = (fx, fy)
        
        if best_source:
            fx, fy = best_source
            operations.append((fx, fy, tx, ty))
            existing_beverages.append((tx, ty))
        else:
            # If no monotone source found, this target is impossible under current logic.
            # In a real contest, we'd need a better strategy. 
            # For a baseline, we'll just skip it to avoid invalid output.
            pass

    # Output the number of operations
    print(len(operations))
    # Output each operation
    for op in operations:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == "__main__":
    solve()
