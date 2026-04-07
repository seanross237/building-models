import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    targets = []
    idx = 1
    for _ in range(N):
        x = int(input_data[idx])
        y = int(input_data[idx+1])
        targets.append((x, y))
        idx += 2

    # Sort targets to process in a way that respects monotonicity
    # Sorting by x then y helps in finding potential parents
    targets.sort()

    visited = [(0, 0)]
    edges = []
    remaining = targets[:]

    while remaining:
        best_edge = None
        min_dist = float('inf')
        best_rem_idx = -1
        best_vis_idx = -1

        for i, (tx, ty) in enumerate(remaining):
            for j, (fx, fy) in enumerate(visited):
                if tx >= fx and ty >= fy:
                    dist = (tx - fx) + (ty - fy)
                    if dist < min_dist:
                        min_dist = dist
                        best_edge = (fx, fy, tx, ty)
                        best_rem_idx = i
                        best_vis_idx = j
        
        if best_edge:
            edges.append(best_edge)
            visited.append((best_edge[2], best_edge[3]))
            remaining.pop(best_rem_idx)
        else:
            # This case should not happen if all targets are reachable from (0,0)
            # under the monotonicity constraint (tx >= fx, ty >= fy).
            # If not reachable, the problem constraints might be violated.
            break

    print(len(edges))
    for e in edges:
        print(f"{e[0]} {e[1]} {e[2]} {e[3]}")

if __name__ == "__main__":
    solve()