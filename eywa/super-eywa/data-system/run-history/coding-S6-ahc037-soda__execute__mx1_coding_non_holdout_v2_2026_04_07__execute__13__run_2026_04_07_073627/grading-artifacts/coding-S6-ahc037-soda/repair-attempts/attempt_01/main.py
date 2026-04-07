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

    # Sort targets primarily by x, then by y.
    # This ensures that when we process a target, we are moving "forward" in the grid.
    targets.sort()

    # existing_beverages stores (x, y) of beverages already created.
    # We start with (0, 0).
    existing_beverages = [(0, 0)]
    operations = []
    
    # To avoid duplicates and unnecessary operations, we track what we've created.
    # Note: The problem says "Every target beverage must eventually be created".
    # If a target is (0,0), it's already created.
    created_set = {(0, 0)}

    for tx, ty in targets:
        if (tx, ty) in created_set:
            continue
            
        # Find the best existing beverage (fx, fy) such that fx <= tx and fy <= ty
        # and (tx - fx) + (ty - fy) is minimized.
        # This is equivalent to maximizing (fx + fy) subject to fx <= tx and fy <= ty.
        best_f = None
        max_sum = -1

        for fx, fy in existing_beverages:
            if fx <= tx and fy <= ty:
                current_sum = fx + fy
                if current_sum > max_sum:
                    max_sum = current_sum
                    best_f = (fx, fy)
                elif current_sum == max_sum:
                    # Tie-break: prefer larger x to keep options open
                    if best_f is None or fx > best_f[0]:
                        best_f = (fx, fy)

        if best_f is not None:
            fx, fy = best_f
            operations.append((fx, fy, tx, ty))
            existing_beverages.append((tx, ty))
            created_set.add((tx, ty))

    # Output the number of operations
    print(len(operations))
    # Output each operation
    for op in operations:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == "__main__":
    solve()
