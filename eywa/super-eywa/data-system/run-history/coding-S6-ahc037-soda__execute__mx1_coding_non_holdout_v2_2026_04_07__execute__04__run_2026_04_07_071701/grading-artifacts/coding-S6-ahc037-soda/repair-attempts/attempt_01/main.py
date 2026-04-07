import sys

def solve():
    # The problem asks to build 1000 target beverages from (0,0).
    # The input format for AHC problems usually provides N and then N pairs.
    # However, the current code fails because it doesn't output the required format.
    # A valid baseline is to simply output the operations needed to reach each target.
    # Since the problem asks for a sequence of operations, we must output them.
    # A simple valid strategy: for each target (tx, ty), if we can't find a source,
    # we can always use (0,0) if tx >= 0 and ty >= 0, but the problem implies
    # we build a sequence. Let's assume we can always reach (tx, ty) from (0,0)
    # or a previously created beverage.
    
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    try:
        N = int(input_data[0])
    except:
        return

    targets = []
    idx = 1
    for _ in range(N):
        if idx + 1 < len(input_data):
            a = int(input_data[idx])
            b = int(input_data[idx+1])
            targets.append((a, b))
            idx += 2

    # To ensure we can always find a source, we sort targets by sweetness and carbonation.
    # But a simpler way to ensure validity is to just use (0,0) as the source for every target
    # if the problem allows multiple operations from the same source, or build a chain.
    # The problem says 'sequence of monotone derivation operations'.
    # Let's try to build a chain: (0,0) -> target1 -> target2... if possible.
    # If not possible, we can always use (0,0) as the source for any (tx, ty) where tx, ty >= 0.
    
    # Sort targets to try and build a chain
    sorted_targets = sorted(targets, key=lambda p: (p[0], p[1]))
    
    existing = [(0, 0)]
    
    for tx, ty in sorted_targets:
        # Find a source in 'existing' such that fx <= tx and fy <= ty
        best_source = None
        # To minimize cost (tx-fx) + (ty-fy), we want fx, fy to be as large as possible.
        # Since we sorted, the last element in 'existing' is a good candidate.
        for fx, fy in reversed(existing):
            if fx <= tx and fy <= ty:
                best_source = (fx, fy)
                break
        
        if best_source is not None:
            fx, fy = best_source
            # Output format: source_index target_index (or similar)
            # Since the problem doesn't specify the exact output format in the prompt,
            # but the goal is to fix the 'Unexpected EOF', we must output the operations.
            # Standard AHC output for this type of problem is usually:
            # Number of operations
            # op1_source_idx op1_target_idx ...
            # However, without the exact spec, the safest baseline is to output
            # the operations in a way that matches the most common AHC format.
            # Let's assume the output should be: 
            # Number of operations
            # For each operation: source_id target_id
            # where source_id is the index in the 'existing' list (0 is (0,0)).
            pass

    # Given the ambiguity of the output format in the prompt, 
    # and the fact that the previous code failed with EOF, 
    # the most likely issue is that it didn't print anything at all.
    # Let's provide a simple valid output: 
    # 1. Print the number of operations.
    # 2. For each target, print the index of the source and the index of the target.
    
    # Re-calculating with indices
    existing_indices = [0] # index 0 is (0,0)
    existing_coords = [(0, 0)]
    ops = []
    
    for tx, ty in sorted_targets:
        best_idx = -1
        max_val = -1
        for i, (fx, fy) in enumerate(existing_coords):
            if fx <= tx and fy <= ty:
                # Heuristic: pick source that minimizes cost
                dist = (tx - fx) + (ty - fy)
                if best_idx == -1 or dist < max_val:
                    max_val = dist
                    best_idx = i
        
        if best_idx != -1:
            ops.append((best_idx, len(existing_coords)))
            existing_coords.append((tx, ty))
            
    print(len(ops))
    for src, tgt in ops:
        print(f"{src} {tgt}")

if __name__ == '__main__':
    solve()
