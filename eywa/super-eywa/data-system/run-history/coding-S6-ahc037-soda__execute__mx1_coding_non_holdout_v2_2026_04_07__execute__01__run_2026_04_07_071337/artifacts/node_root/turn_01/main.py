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

    # Sort targets to ensure valid sequence (non-decreasing x and y)
    # A simple way to ensure tx >= fx and ty >= fy is to sort by x then y
    # and then check if we can reach it from a previously created beverage.
    # However, the problem says tx >= fx and ty >= fy. 
    # This implies we can only move in positive directions.
    # Let's sort targets by x+y to process closer ones first.
    
    targets.sort(key=lambda p: (p[0] + p[1]))
    
    created = [(0, 0)]
    ops = []
    
    for tx, ty in targets:
        best_dist = float('inf')
        best_source = None
        
        for fx, fy in created:
            if tx >= fx and ty >= fy:
                dist = (tx - fx) + (ty - fy)
                if dist < best_dist:
                    best_dist = dist
                    best_source = (fx, fy)
        
        if best_source is not None:
            ops.append((best_source[0], best_source[1], tx, ty))
            created.append((tx, ty))
        else:
            # If no valid source found, this target cannot be reached 
            # under the strict tx >= fx and ty >= fy constraint 
            # unless we create intermediate steps. 
            # But the problem implies a valid path exists.
            # Let's try to find a path via (tx, 0) or (0, ty) if needed.
            # However, the simplest valid approach is to ensure we can always reach it.
            # Let's refine: if we can't find a source, we must create one.
            # But the problem says 'Every target beverage must eventually be created'.
            # This implies the targets are reachable from (0,0).
            # If a target (tx, ty) is not reachable from any existing (fx, fy),
            # it means for all existing, fx > tx or fy > ty.
            # This shouldn't happen if we process in a specific order.
            pass

    print(len(ops))
    for op in ops:
        print(f"{op[0]} {op[1]} {op[2]} {op[3]}")

if __name__ == "__main__":
    solve()