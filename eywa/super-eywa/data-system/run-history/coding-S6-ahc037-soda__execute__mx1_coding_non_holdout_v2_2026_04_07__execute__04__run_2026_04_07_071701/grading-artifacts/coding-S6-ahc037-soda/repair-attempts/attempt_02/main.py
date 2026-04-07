import sys

def solve():
    # Read all input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    try:
        # The problem states N=1000 targets. 
        # In AHC, N is usually the first integer.
        N = int(input_data[0])
    except (ValueError, IndexError):
        return

    targets = []
    idx = 1
    for _ in range(N):
        if idx + 1 < len(input_data):
            try:
                a = int(input_data[idx])
                b = int(input_data[idx+1])
                targets.append((a, b))
                idx += 2
            except ValueError:
                idx += 1
                continue
        else:
            break

    # The problem asks to build 1000 target beverages from (0,0).
    # A monotone derivation operation (fx, fy) -> (tx, ty) is valid if fx <= tx and fy <= ty.
    # We need to output a sequence of operations.
    # A safe baseline: for each target, derive it from (0,0).
    # However, the problem implies we build a sequence of beverages. 
    # Let's assume the output format is:
    # Number of operations
    # For each operation: source_index target_index
    # where index 0 is the initial (0,0).
    
    # To ensure we can always find a source, we sort targets by sweetness and carbonation.
    # This allows us to potentially chain them.
    sorted_targets = sorted(targets, key=lambda p: (p[0], p[1]))
    
    # existing_coords[0] is (0,0)
    existing_coords = [(0, 0)]
    ops = []
    
    for tx, ty in sorted_targets:
        # Find a source in 'existing_coords' such that fx <= tx and fy <= ty
        # To minimize cost, we look for the closest one.
        best_idx = -1
        min_dist = float('inf')
        
        for i, (fx, fy) in enumerate(existing_coords):
            if fx <= tx and fy <= ty:
                dist = (tx - fx) + (ty - fy)
                if dist < min_dist:
                    min_dist = dist
                    best_idx = i
        
        if best_idx != -1:
            # The target index in the sequence of beverages created is len(existing_coords)
            target_idx = len(existing_coords)
            ops.append((best_idx, target_idx))
            existing_coords.append((tx, ty))
        else:
            # This case should not happen if (0,0) is always a valid source for tx, ty >= 0
            # But if it does, we skip this target to maintain validity.
            pass

    # Output the number of operations
    print(len(ops))
    # Output each operation: source_index target_index
    for src, tgt in ops:
        print(f"{src} {tgt}")

if __name__ == '__main__':
    solve()
