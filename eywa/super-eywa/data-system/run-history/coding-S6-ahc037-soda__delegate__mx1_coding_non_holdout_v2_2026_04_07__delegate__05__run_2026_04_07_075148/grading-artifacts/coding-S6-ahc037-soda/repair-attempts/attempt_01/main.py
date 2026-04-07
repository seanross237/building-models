import sys

def solve():
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

    # The problem asks for a sequence of operations to build the target set.
    # A valid sequence must specify which existing beverage (index) is used to create the new one.
    # Beverage 0 is (0,0).
    # Output format: 
    # For each target i (from 1 to N):
    #   source_index target_x target_y
    # where source_index is the index of an existing beverage (0 to i-1).
    
    # A simple baseline: for each target, use beverage 0 (0,0) as the source.
    # This is valid as long as target_x >= 0 and target_y >= 0.
    
    for i in range(n):
        tx, ty = targets[i]
        # We use beverage 0 as the source for every target.
        # The index of the target itself in the sequence will be i+1.
        print(f"0 {tx} {ty}")

if __name__ == '__main__':
    solve()
