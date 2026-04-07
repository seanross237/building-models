import sys

def solve():
    # The problem asks for a sequence of operations to reach 1000 target beverages.
    # Each operation is (x1, y1) -> (x2, y2) where x2 >= x1 and y2 >= y1.
    # The cost is (x2-x1) + (y2-y1).
    # We start with (0, 0).
    
    try:
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
    except EOFError:
        return
    except Exception:
        return

    # A simple valid baseline: 
    # For each target (tx, ty), we can go (0,0) -> (tx, 0) -> (tx, ty).
    # However, the problem implies we build a tree/sequence of operations.
    # Let's just output a simple path for each target from (0,0) to ensure validity.
    # But the problem says 'a sequence of monotone derivation operations'.
    # This usually means each operation uses an existing beverage to create a new one.
    
    # We start with (0,0) in our set.
    current_beverages = [(0, 0)]
    
    # To ensure we don't violate monotonicity and keep it simple:
    # For each target, we find a beverage (vx, vy) already in the set such that vx <= tx and vy <= ty.
    # If we can't find one, we create intermediate steps.
    
    # Since we need to output the operations:
    # Format: x1 y1 x2 y2
    
    for tx, ty in targets:
        # Try to find a source in current_beverages
        found = False
        for vx, vy in current_beverages:
            if vx <= tx and vy <= ty:
                print(f"{vx} {vy} {tx} {ty}")
                current_beverages.append((tx, ty))
                found = True
                break
        
        if not found:
            # If no direct monotone path, create intermediate nodes
            # (0,0) -> (tx, 0) -> (tx, ty)
            # Check if (tx, 0) is valid (tx >= 0)
            if tx > 0:
                print(f"0 0 {tx} 0")
                print(f"{tx} 0 {tx} {ty}")
            else:
                print(f"0 0 0 {ty}")
                print(f"0 {ty} {tx} {ty}")
            current_beverages.append((tx, ty))

if __name__ == '__main__':
    solve()
