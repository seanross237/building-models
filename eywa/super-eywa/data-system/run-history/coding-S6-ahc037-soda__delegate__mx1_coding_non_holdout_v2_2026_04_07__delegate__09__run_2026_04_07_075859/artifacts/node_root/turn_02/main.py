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

    # Sort targets to process them in an order that facilitates monotonicity.
    # Sorting by x then y ensures that if we pick a point, we can potentially
    # connect it to a point with smaller x and smaller or equal y.
    # However, the constraint is tx >= fx AND ty >= fy.
    # This means we can only connect (fx, fy) -> (tx, ty) if fx <= tx and fy <= ty.
    
    # Let's sort targets by x + y to process 'closer' points first.
    # We also need to keep track of points we have 'created'.
    # Initially, we have (0, 0).
    
    created_points = [(0, 0)]
    operations = []
    
    # To satisfy the constraint tx >= fx and ty >= fy for all operations,
    # we must ensure that for every target (a, b), there exists a path from (0,0).
    # A simple way: Sort targets by x, then y.
    # For each target, try to find an existing point (fx, fy) such that fx <= tx and fy <= ty.
    # To minimize cost (tx-fx + ty-fy), we want to maximize fx + fy.
    
    # Sort targets primarily by x, then by y.
    sorted_targets = sorted(targets, key=lambda p: (p[0], p[1]))
    