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

    # We need to reach all (a_i, b_i) starting from (0, 0).
    # Constraint: (fx, fy) -> (tx, ty) requires tx >= fx and ty >= fy.
    # Cost: (tx - fx) + (ty - fy).
    # This is equivalent to finding a directed tree rooted at (0,0) 
    # where edges follow the monotonicity constraint.
    
    # To minimize total cost, we want to connect each target to an existing 
    # point (fx, fy) such that fx <= tx and fy <= ty and (tx-fx) + (ty-fy) is minimized.
    # Note that (tx-fx) + (ty-fy) = tx + ty - (fx + fy).
    # To minimize this, we need to maximize (fx + fy) subject to fx <= tx and fy <= ty.

    # Sort targets to process them in an order that ensures parents are likely already processed.
    # Sorting by x then y (or x+y) helps.
    targets.sort()

    # existing_points stores (x, y) of beverages already created.
    # Start with (0, 0).
    existing_points = [(0, 0)]
    operations = []

    # To handle N=1000 efficiently, O(N^2) is fine.
    # For each target, find the best parent from existing_points.
    
    # However, some targets might be "covered" by others. 
    # If target A is (2, 2) and target B is (3, 3), B can be reached from A.
    # If target A is (2, 2) and target B is (1, 3), B cannot be reached from A.
    
    # We must ensure we don't try to add the same coordinate twice if it's in targets.
    # But the problem says "Every target beverage must eventually be created".
    # If multiple targets have the same coordinates, we still need to "create" them?
    # Usually, in these problems, if coordinates are identical, one operation covers both.
    # But to be safe, let's treat each target as a unique requirement.
    
    # Let's refine the target list to unique points to avoid redundant operations,
    # but we must ensure all N are "created". If targets are identical, 
    # we can just skip the redundant ones in terms of operations but they are "created".
    # Actually, the problem says "Every target beverage must eventually be created".
    # If two targets are (5,5), once we create (5,5), both are satisfied.
    
    unique_targets = []
    seen = set()
    for t in targets:
        if t not in seen:
            unique_targets.append(t)
            seen.add(t)
    
    # Sort unique targets by x+y to process closer ones first.
    unique_targets.sort(key=lambda p: (p[0] + p[1]))

    for tx, ty in unique_targets:
        best_parent = None
        max_sum = -1
        
        for fx, fy in existing_points:
            if fx <= tx and fy <= ty:
                current_sum = fx + fy
                if current_sum > max_sum:
                    max_sum = current_sum
                    best_parent = (fx, fy)
        
        if best_parent:
            fx, fy = best_parent
            operations.append((fx, fy, tx, ty))
            existing_points.append((tx, ty))
        else:
            # This case should not happen because (0,0) is always a valid parent
            # for any (tx, ty) where tx >= 0 and ty >= 0.
            pass

    # Output the number of operations and the operations themselves.
    print(len(operations))
    for op in operations:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == "__main__":
    solve()
