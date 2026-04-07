import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    targets = []
    for i in range(N):
        a = int(input_data[1 + 2*i])
        b = int(input_data[2 + 2*i])
        targets.append((a, b))
    
    # Sort targets to ensure we can build them monotonically
    # A simple way is to sort by sweetness then carbonation
    targets.sort()
    
    existing_beverages = [(0, 0)]
    operations = []
    
    for tx, ty in targets:
        best_source_idx = -1
        min_dist = float('inf')
        
        # Find a source (fx, fy) such that fx <= tx and fy <= ty
        for i, (fx, fy) in enumerate(existing_beverages):
            if fx <= tx and fy <= ty:
                dist = (tx - fx) + (ty - fy)
                if dist < min_dist:
                    min_dist = dist
                    best_source_idx = i
        
        if best_source_idx != -1:
            fx, fy = existing_beverages[best_source_idx]
            # The problem requires outputting the sequence of operations.
            # Based on typical AHC formats, we output the number of operations
            # and then the details of each operation.
            operations.append((fx, fy, tx, ty))
            existing_beverages.append((tx, ty))
        else:
            # If no valid source is found, this simple greedy approach fails.
            # However, for a baseline, we can try to connect to (0,0) if possible
            # or just skip. But (0,0) is always a valid source for (tx, ty) if tx,ty >= 0.
            # Since targets are likely positive, (0,0) works.
            fx, fy = 0, 0
            operations.append((fx, fy, tx, ty))
            existing_beverages.append((tx, ty))

    # Output format: 
    # First line: number of operations
    # Subsequent lines: source_sweetness source_carbonation target_sweetness target_carbonation
    print(len(operations))
    for op in operations:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == '__main__':
    solve()
