import sys

def solve():
    # The problem asks to build 1000 target beverages starting from (0,0).
    # The input format for AHC problems usually provides N targets.
    # However, the goal is to output a sequence of operations.
    # A valid operation is (x1, y1, x2, y2) where x1 <= x2 and y1 <= y2.
    # Since we need a valid baseline, we will simply output operations
    # that connect (0,0) to each target (tx, ty) sequentially.
    
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

    # To ensure we can always reach a target from an existing beverage,
    # we can just build a chain or connect everything to (0,0).
    # But the problem implies we need to reach the specific targets provided.
    # A simple valid strategy: for each target, if it's not (0,0), 
    # create it from (0,0) or the previous target if possible.
    
    # Let's try to connect each target (tx, ty) from (0,0) if 0 <= tx and 0 <= ty.
    # Since sweetness and carbonation are non-negative, this is always valid.
    
    # The output format for these types of problems is usually:
    # Number of operations
    # op1_x1 op1_y1 op1_x2 op1_y2
    # ...
    
    valid_ops = []
    for tx, ty in targets:
        if tx == 0 and ty == 0:
            continue
        # Check if (0,0) -> (tx, ty) is a valid monotone operation
        if 0 <= tx and 0 <= ty:
            valid_ops.append((0, 0, tx, ty))

    print(len(valid_ops))
    for op in valid_ops:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == "__main__":
    solve()
