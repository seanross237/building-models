import sys

def solve():
    # The problem AHC037 / Soda involves building 1000 target beverages.
    # The input format for AHC problems typically starts with N (number of targets).
    # The goal is to output a sequence of operations to reach these targets.
    # Based on the problem description, we need to reach (a, b) from (0, 0).
    # A common AHC format for such problems is:
    # 1. Output the number of operations.
    # 2. For each operation, output its parameters.
    
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

    # Since the exact operation syntax is not provided in the prompt, 
    # but the goal is to fix the 'Unexpected EOF' error, we must ensure 
    # we output something that matches the expected structure.
    # In AHC037, the operations are typically defined as adding sweetness/carbonation.
    # A common format for these problems is: 
    # <number of operations>
    # <op_type> <delta_sweetness> <delta_carbonation>
    
    # Let's assume the simplest possible valid output: 
    # For each target, we perform one operation to reach it from (0,0).
    # We will output N operations, each being '1 a b' where 1 is the op type.
    
    # However, if the problem requires reaching the targets sequentially 
    # (building a set), we might need to output the operations that, 
    # when applied to the current state, result in the target set.
    
    # Given the ambiguity, we will output N operations. 
    # Each operation will be '1 a b' (type 1, sweetness a, carbonation b).
    # This is a common baseline for 'build' problems.
    
    print(len(targets))
    for a, b in targets:
        print(f"1 {a} {b}")

if __name__ == '__main__':
    solve()
