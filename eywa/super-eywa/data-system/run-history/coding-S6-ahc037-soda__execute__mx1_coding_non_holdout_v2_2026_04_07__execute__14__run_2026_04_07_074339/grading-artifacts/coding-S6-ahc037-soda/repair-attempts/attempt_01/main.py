import sys

def solve():
    # The problem asks for a sequence of operations to reach 1000 target beverages.
    # Based on the problem description, we need to output the operations.
    # However, the current main.py only prints a single integer (the cost).
    # The scorer feedback indicates the output is 'Out of range', implying the format is wrong.
    # A standard AHC format for 'sequence of operations' usually requires printing
    # the number of operations followed by the operations themselves, or a specific format.
    # Since the exact output format is not provided in the prompt, but the goal is to
    # produce 'valid contestant output' and 'a simple valid baseline', 
    # and the current code fails by printing a single large number, 
    # we will assume the output should be the sequence of operations.
    # Given the constraints and the nature of the problem, a simple valid baseline
    # is to reach each target from (0,0) directly if possible, or just outputting
    # the targets in a way that satisfies the 'sequence of monotone derivation operations'.
    
    # Re-reading: 'build a target set of 1000 beverages... using a sequence of monotone derivation operations'.
    # Monotone derivation: (x, y) -> (x+dx, y+dy) where dx, dy >= 0.
    # Cost of (x1, y1) -> (x2, y2) is (x2-x1) + (y2-y1).
    
    # Let's assume the output format is:
    # Number of operations
    # op1_x1 op1_y1 op1_x2 op1_y2
    # ...
    
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

    # To ensure monotonicity and valid operations, we sort targets.
    # A simple way is to sort by x then y.
    targets.sort()
    
    # We must ensure that for every target, there is a path from (0,0).
    # We can just treat each target as an operation from (0,0) if we don't care about cost,
    # but we need to make sure we don't duplicate (0,0).
    
    ops = []
    current_beverages = {(0, 0)}
    
    for tx, ty in targets:
        if (tx, ty) == (0, 0):
            continue
        # Find a parent (ex, ey) such that ex <= tx and ey <= ty
        # To keep it simple and valid, we can always use (0,0) as parent.
        # But to be safe, let's try to find the 'closest' existing beverage.
        best_p = (0, 0)
        for ex, ey in current_beverages:
            if ex <= tx and ey <= ty:
                # We don't actually need to minimize cost for a baseline, 
                # just be valid.
                best_p = (ex, ey)
                break
        
        ops.append((best_p[0], best_p[1], tx, ty))
        current_beverages.add((tx, ty))

    # Output the number of operations and then each operation.
    print(len(ops))
    for op in ops:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == '__main__':
    solve()
