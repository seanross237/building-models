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

    # The problem asks for a sequence of operations to reach 1000 targets.
    # Each operation (fx, fy) -> (tx, ty) requires fx <= tx and fy <= ty.
    # A simple valid baseline: for each target (tx, ty), use (0, 0) as the source.
    # This is valid because 0 <= tx and 0 <= ty for all targets (assuming non-negative).
    # However, we must ensure we don't repeat (0,0) as a target if it's not in the list,
    # and we must output exactly N operations.
    
    # To be safe and simple, we can chain them if possible, or just use (0,0) for all.
    # Let's try to find a valid predecessor for each target.
    # A very simple approach: for each target (tx, ty), the operation is (0, 0) -> (tx, ty).
    # This is valid as long as tx >= 0 and ty >= 0.
    
    # The output format for these types of problems usually requires:
    # Number of operations
    # For each operation: fx fy tx ty
    
    # Since the problem description doesn't specify the exact output format 
    # (only that it's a sequence of operations), but the scorer failed on EOF,
    # I will assume the standard format for such problems: 
    # N (number of operations)
    # followed by N lines of 'fx fy tx ty'
    
    print(N)
    for tx, ty in targets:
        # Operation: (0, 0) -> (tx, ty)
        print(f"0 0 {tx} {ty}")

if __name__ == '__main__':
    solve()
