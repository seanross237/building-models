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

    # The problem requires that for every operation (fx, fy) -> (tx, ty),
    # tx >= fx and ty >= fy.
    # We start with (0, 0).
    # To ensure we can reach all points, we can use a strategy where we 
    # always move to a point that is "greater" in both coordinates.
    # However, not all points can be reached in a single chain.
    # But we can always reach any (tx, ty) from (0, 0) by:
    # (0, 0) -> (tx, 0) -> (tx, ty)
    # This is valid because tx >= 0 and ty >= 0.
    # This creates a valid sequence of operations.
    
    # To minimize cost, we want to reuse existing points.
    # A simple greedy approach:
    # Keep a set of "available" points. Initially {(0, 0)}.
    # For each target point, find an existing point (fx, fy) such that
    # fx <= tx and fy <= ty and (tx-fx) + (ty-fy) is minimized.
    
    existing_points = [(0, 0)]
    operations = []

    # Sort targets to process them in a way that might allow reuse
    # Sorting by x then y helps in finding a good (fx, fy)
    targets.sort()

    for tx, ty in targets:
        best_f = None
        min_dist = float('inf')
        
        # Find the best existing point to transition from
        for fx, fy in existing_points:
            if fx <= tx and fy <= ty:
                dist = (tx - fx) + (ty - fy)
                if dist < min_dist:
                    min_dist = dist
                    best_f = (fx, fy)
        
        # If for some reason no point is found (shouldn't happen as (0,0) is there)
        if best_f is None:
            # Fallback to (0,0) via intermediate steps if necessary
            # (0,0) -> (tx, 0) -> (tx, ty)
            if tx > 0:
                operations.append((0, 0, tx, 0))
                existing_points.append((tx, 0))
            if ty > 0:
                # If (tx, 0) was just added, use it. Otherwise use (0,0)
                if tx > 0:
                    operations.append((tx, 0, tx, ty))
                else:
                    operations.append((0, 0, 0, ty))
                    existing_points.append((0, ty))
                existing_points.append((tx, ty))
            else:
                operations.append((0, 0, tx, ty))
                existing_points.append((tx, ty))
        else:
            fx, fy = best_f
            # If the transition is not a single step (e.g., tx > fx and ty > fy),
            # we can do it in two steps to potentially reuse points, 
            # but the cost (tx-fx) + (ty-fy) is the same whether we do 
            # (fx, fy) -> (tx, fy) -> (tx, ty) or (fx, fy) -> (fx, ty) -> (tx, ty)
            # or just (fx, fy) -> (tx, ty).
            # The problem says "Each operation creates a new beverage...".
            # It doesn't forbid (fx, fy) -> (tx, ty) directly.
            
            # Check if (tx, ty) is already in existing_points to avoid duplicates
            # though the problem says "Every target beverage must eventually be created"
            # and doesn't explicitly forbid creating the same point twice.
            # However, we only add it if it's a new coordinate.
            
            if (tx, ty) not in existing_points:
                # To be safe and ensure we don't violate tx >= fx and ty >= fy:
                # If tx > fx and ty > fy, we can do it in one step.
                # If tx == fx or ty == fy, it's one step.
                operations.append((fx, fy, tx, ty))
                existing_points.append((tx, ty))

    # Print results
    print(len(operations))
    for op in operations:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == "__main__":
    solve()
