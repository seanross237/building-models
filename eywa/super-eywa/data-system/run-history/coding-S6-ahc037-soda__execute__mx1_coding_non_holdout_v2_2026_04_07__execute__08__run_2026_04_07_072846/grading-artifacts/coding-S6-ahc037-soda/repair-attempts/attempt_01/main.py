import sys

def solve():
    # The problem asks to build a target set of 1000 beverages.
    # The input format for this specific problem type usually provides N targets.
    # However, the goal is to output a sequence of operations to reach these targets.
    # A valid baseline is to simply output the target coordinates as operations
    # from (0,0) if they are reachable, or just provide a valid sequence.
    
    # Since the exact input format for the targets isn't fully specified in the prompt
    # but the goal is to produce valid contestant output, we will read N and targets.
    # A simple valid strategy: for each target (tx, ty), if we can reach it from (0,0),
    # we output the operation. To ensure we don't fail on 'Unexpected EOF',
    # we must handle input carefully.
    
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    try:
        N = int(input_data[0])
        targets = []
        idx = 1
        for _ in range(N):
            if idx + 1 < len(input_data):
                a = int(input_data[idx])
                b = int(input_data[idx+1])
                targets.append((a, b))
                idx += 2
    except (ValueError, IndexError):
        return

    # The problem requires a sequence of operations. 
    # Based on the context of AHC (AtCoder Heuristic Contest), 
    # the output format usually requires printing the number of operations 
    # followed by the operations themselves.
    # Since the exact output format is not provided in the prompt, 
    # but the error was 'Unexpected EOF', it implies the scorer expected 
    # more output or a specific structure.
    
    # Let's assume the output format is:
    # Number of operations
    # op1_x op1_y op2_x op2_y ...
    # Or similar. Given the ambiguity, a common AHC format is:
    # Number of operations
    # x1 y1 x2 y2 ...
    
    # However, without the exact spec, the safest 'baseline' is to assume 
    # the targets themselves are the operations from (0,0).
    
    # Let's try to output the targets as operations from (0,0).
    # We'll output the number of targets, then for each target, the source and destination.
    
    print(len(targets))
    for tx, ty in targets:
        # Assuming operation format: source_x source_y dest_x dest_y
        # We use (0,0) as the source for all to ensure monotonicity if targets are increasing.
        # But to be safe and simple, we'll just output the target as a derivation from (0,0).
        # If the problem requires a sequence where each target is derived from a previous one:
        print(f"0 0 {tx} {ty}")

solve()
