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

    # The problem asks for a sequence of operations to reach the target set.
    # Based on the error 'Out of range', the contestant was printing a single integer (the score),
    # but the problem requires a specific sequence of operations.
    # A valid operation is (x1, y1, x2, y2) where x1 <= x2 and y1 <= y2.
    # We need to reach all N targets starting from (0,0).
    
    existing = [(0, 0)]
    
    # Sort targets to ensure we can build them monotonically
    # A simple way is to sort by x then y.
    sorted_targets = sorted(targets)
    
    for tx, ty in sorted_targets:
        # Find an existing point (fx, fy) such that fx <= tx and fy <= ty
        best_f = (0, 0)
        found = False
        # To keep it simple and valid, we just find the first one that satisfies the condition
        # or default to (0,0) if we assume (0,0) is always available.
        for fx, fy in existing:
            if fx <= tx and fy <= ty:
                best_f = (fx, fy)
                found = True
                break
        
        # If we found a valid source, output the operation
        # The problem format for AHC usually requires specific lines per operation.
        # Since the exact format isn't in the prompt but the error was 'Out of range' for a single number,
        # we assume the output should be the sequence of operations.
        # Standard AHC format for this type of problem is usually:
        # Number of operations
        # x1 y1 x2 y2
        # ...
        # However, without the exact spec, a safe baseline is to output the operations.
        # Let's assume the format is: 
        # Total operations
        # x1 y1 x2 y2
        
        # Wait, the prompt says 'Return a corrected main.py that produces valid contestant output'.
        # The error 'Out of range' suggests the scorer expected a sequence but got a huge number.
        # Let's try to output the operations in a standard way.
        
        if tx == 0 and ty == 0:
            continue
            
        # We'll collect operations and print them at the end.
        # But we need to be careful about the format. 
        # Let's assume the format is: 
        # K (number of operations)
        # x1 y1 x2 y2 (for each operation)
        
    # Re-evaluating: The simplest valid baseline is to just output the operations.
    # Let's try the most common AHC format for 'sequence of operations'.
    
    ops = []
    current_points = [(0, 0)]
    for tx, ty in sorted_targets:
        if tx == 0 and ty == 0:
            continue
        # Find a point in current_points that can reach (tx, ty)
        source = (0, 0)
        for px, py in current_points:
            if px <= tx and py <= ty:
                source = (px, py)
                break
        ops.append((source[0], source[1], tx, ty))
        current_points.append((tx, ty))

    print(len(ops))
    for op in ops:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

solve()
