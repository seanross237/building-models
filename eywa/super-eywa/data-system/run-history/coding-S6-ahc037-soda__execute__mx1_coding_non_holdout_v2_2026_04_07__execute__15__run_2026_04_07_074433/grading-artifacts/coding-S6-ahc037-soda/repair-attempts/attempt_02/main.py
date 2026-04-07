import sys

def solve():
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

    # The problem requires building a target set of 1000 beverages.
    # We start with (0,0) at index 0.
    # Each operation: source_index target_sweetness target_carbonation
    # Monotone derivation: source_x <= target_x and source_y <= target_y
    
    beverages = [(0, 0)]
    results = []

    for tx, ty in targets:
        # We can always derive any (tx, ty) where tx >= 0 and ty >= 0 from (0,0)
        # because (0,0) is at index 0 and 0 <= tx, 0 <= ty.
        # We check if the target is already (0,0) to avoid redundant operations if needed,
        # but the problem asks to build the target set. 
        # If a target is (0,0), we don't need an operation to 'create' it, 
        # but the problem implies we need to reach the target set.
        # However, the simplest valid approach is to derive every target from index 0.
        
        if tx == 0 and ty == 0:
            # If the target is (0,0), it's already in our 'beverages' list at index 0.
            # But the problem asks for a sequence of operations to build the set.
            # Usually, in these problems, if the target is the starting state, 
            # we might not need an operation, but we must ensure the final set matches.
            # To be safe and simple, we only add operations for non-(0,0) targets.
            # We'll assume the target set includes the (0,0) we start with.
            continue
            
        results.append(f"0 {tx} {ty}")
        beverages.append((tx, ty))

    # Output the number of operations
    print(len(results))
    # Output each operation
    for res in results:
        print(res)

if __name__ == "__main__":
    solve()
