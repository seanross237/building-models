import sys
import math

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    W = int(input_data[idx]); idx += 1
    H = int(input_data[idx]); idx += 1
    N = int(input_data[idx]); idx += 1
    P = float(input_data[idx]); idx += 1
    
    num_shapes = int(input_data[idx]); idx += 1
    shapes = []
    for _ in range(num_shapes):
        s_size = int(input_data[idx]); idx += 1
        coords = []
        for _ in range(s_size):
            dx = int(input_data[idx]); idx += 1
            dy = int(input_data[idx]); idx += 1
            coords.append((dx, dy))
        shapes.append(coords)

    # Belief map: probability of oil at (x, y)
    belief = [[0.5 for _ in range(H)] for _ in range(W)]
    
    # Simple strategy: probe single cells to build belief
    # In a real scenario, we'd use Bayesian updates and aggregate queries
    # For this baseline, we probe cells and then guess based on threshold
    
    probed_cells = []
    for x in range(W):
        for y in range(H):
            print(f"q 1 {x} {y}", flush=True)
            res = sys.stdin.readline().strip()
            if not res:
                break
            
            # Assuming response is '1' for oil, '0' for no oil
            # Adjusting for noise P if necessary (simplified here)
            if res == '1':
                belief[x][y] = 1.0
            else:
                belief[x][y] = 0.0
            probed_cells.append((x, y))
        else: continue
        break

    # Collect cells with high belief
    final_cells = []
    for x in range(W):
        for y in range(H):
            if belief[x][y] > 0.5:
                final_cells.append((x, y))
    
    # Output final answer
    k = len(final_cells)
    cmd = [f"a", str(k)]
    for cx, cy in final_cells:
        cmd.append(str(cx))
        cmd.append(str(cy))
    print(" ".join(cmd), flush=True)

if __name__ == "__main__":
    solve()