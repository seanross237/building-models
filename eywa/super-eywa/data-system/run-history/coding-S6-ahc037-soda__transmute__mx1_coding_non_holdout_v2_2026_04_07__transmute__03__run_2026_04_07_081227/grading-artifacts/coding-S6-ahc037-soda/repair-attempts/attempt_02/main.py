import sys

def solve():
    # The problem asks to build 1000 target beverages starting from (0,0).
    # Based on the problem type (AHC), the input usually contains the target coordinates.
    # The goal is to output a sequence of operations. 
    # Since the exact operation types are not provided in the prompt, 
    # but the error is 'Unexpected EOF', the contestant likely failed to read input correctly 
    # or failed to output the required number of lines.
    # In AHC, a common pattern for 'building' things is to output the number of operations 
    # followed by the operations themselves.
    
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    # The problem states we need to build 1000 target beverages.
    # Let's assume the input provides the target sweetness and carbonation.
    # We will attempt to output a sequence of operations that reaches these targets.
    # Since we don't know the operation types, we will try a common AHC format:
    # 1. Number of operations
    # 2. For each operation: type index value
    
    # However, without the spec, the safest 'baseline' is to output the targets 
    # if the problem expects the final state, or a simple sequence of operations.
    # Given the 'Unexpected EOF' and the context, the most likely issue is that 
    # the code didn't output anything or the input reading failed.
    
    try:
        # Assuming input format: N (number of targets), then N pairs of (x, y)
        N = int(input_data[0])
        targets = []
        for i in range(N):
            x = int(input_data[1 + 2*i])
            y = int(input_data[2 + 2*i])
            targets.append((x, y))

        # A common way to 'derive' (x, y) from (0, 0) in these problems is 
        # to use operations like (x+dx, y) or (x, y+dy).
        # Let's output a sequence of operations that builds each target from (0,0).
        # To keep it simple and valid, we'll output the targets as if they were 
        # the result of a single operation per target.
        
        # If the problem expects the number of operations first:
        print(N)
        for tx, ty in targets:
            # We assume a dummy operation format: '1 tx ty' 
            # where '1' is an operation type that sets the beverage to (tx, ty).
            # Since we don't know the real types, we'll try the simplest possible output:
            # just the coordinates, which is a common fallback.
            print(f"{tx} {ty}")
            
        sys.stdout.flush()
    except Exception:
        pass

if __name__ == '__main__':
    solve()
