import sys

def solve():
    # Read N
    line = sys.stdin.readline()
    if not line:
        return
    try:
        n = int(line.strip())
    except ValueError:
        return

    targets = []
    for _ in range(n):
        line = sys.stdin.readline()
        if not line:
            break
        targets.append(list(map(int, line.split())))

    # To minimize cost C = sum((tx - fx) + (ty - fy)), 
    # we want to connect each target (tx, ty) to an existing point (fx, fy)
    # such that fx <= tx and fy <= ty and (tx-fx) + (ty-fy) is minimized.
    # Note: (tx-fx) + (ty-fy) = tx + ty - (fx + fy).
    # Minimizing this is equivalent to maximizing (fx + fy) subject to fx <= tx and fy <= ty.

    # We must ensure the sequence is valid: 'from' must exist before 'to'.
    # A safe way is to process targets in an order that respects the monotonicity.
    # Sorting by x then y ensures that if (fx, fy) can reach (tx, ty), 
    # (fx, fy) will likely be processed earlier or is (0,0).
    
    # However, a target might be a 'from' point for another target.
    # Let's sort targets such that we always pick a point that is "smaller" first.
    # Sorting by x + y is a good heuristic for the order of creation.
    
    # We also need to handle the case where multiple targets are the same.
    # The problem says "Every target beverage must eventually be created".
    # If two targets are (10, 10) and (10, 10), we still need to "create" it twice?
    # Usually, in these problems, if coordinates are identical, we can just 
    # create one and then "create" the second one from the first with 0 cost.
    # But the cost (tx-fx) + (ty-fy) would be 0.
    
    # Let's sort targets by x then y.
    targets.sort()

    # existing_points stores (x, y)
    existing_points = [(0, 0)]
    operations = []

    # To efficiently find the best (fx, fy), we can just iterate through existing_points.
    # Since N=1000, O(N^2) is perfectly fine.
    
    for tx, ty in targets:
        best_f = None
        max_sum = -1
        
        for fx, fy in existing_points:
            if fx <= tx and fy <= ty:
                current_sum = fx + fy
                if current_sum > max_sum:
                    max_sum = current_sum
                    best_f = (fx, fy)
        
        # It is guaranteed that (0,0) is in existing_points and 0 <= tx, 0 <= ty
        # so best_f will never be None.
        
        fx, fy = best_f
        operations.append((fx, fy, tx, ty))
        existing_points.append((tx, ty))

    # Output
    print(len(operations))
    for op in operations:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == "__main__":
    solve()
