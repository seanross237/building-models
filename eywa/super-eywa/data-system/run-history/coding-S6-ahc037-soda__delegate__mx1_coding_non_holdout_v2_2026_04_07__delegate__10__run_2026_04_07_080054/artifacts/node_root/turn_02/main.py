import sys

def solve():
    # Read all input
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

    # Sort targets to facilitate monotonic construction
    # Sorting by x then y helps in finding a sequence
    targets.sort()

    # existing_points stores (x, y) of beverages we have already created
    # We start with the initial beverage (0, 0)
    existing_points = [(0, 0)]
    
    # operations will store (fx, fy, tx, ty)
    operations = []

    for tx, ty in targets:
        # We need to find an existing point (fx, fy) such that fx <= tx and fy <= ty
        # To minimize cost (tx-fx) + (ty-fy), we want to maximize fx + fy
        best_f = None
        max_sum = -1

        for fx, fy in existing_points:
            if fx <= tx and fy <= ty:
                current_sum = fx + fy
                if current_sum > max_sum:
                    max_sum = current_sum
                    best_f = (fx, fy)
        
        # If we found a valid predecessor
        if best_f is not None:
            fx, fy = best_f
            # If the target is not already (0,0) and not already created
            # (Though targets are usually > 0,0)
            if (tx, ty) != (fx, fy):
                operations.append((fx, fy, tx, ty))
                existing_points.append((tx, ty))
        else:
            # This case