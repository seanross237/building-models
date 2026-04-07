import sys

def solve():
    # Read initial input
    line = sys.stdin.readline()
    if not line:
        return
    
    try:
        # Format: H W N noise_param num_shapes
        # Note: The exact format depends on the problem instance, 
        # but we follow the standard interactive pattern.
        parts = list(map(int, line.split()))
        if len(parts) < 4:
            return
        H, W, N, noise = parts[0], parts[1], parts[2], parts[3]
        
        # The number of shapes might follow or be part of the line
        # For AHC style, we read the shapes list
        num_shapes = parts[4] if len(parts) > 4 else 0
        shapes = []
        for _ in range(num_shapes):
            shape_line = sys.stdin.readline().split()
            if not shape_line:
                break
            # shape_line: k x1 y1 x2 y2 ...
            k = int(shape_line[0])
            coords = []
            for i in range(k):
                coords.append((int(shape_line[1 + 2*i]), int(shape_line[2 + 2*i])))
            shapes.append(coords)
            
    except EOFError:
        return
    except Exception:
        return

    # Strategy:
    # Since we want to minimize cost, we use a coarse grid sampling 
    # with aggregate queries (q k) to find potential oil regions.
    # Then we refine with single-cell queries (q 1).
    
    discovered_oil = set()
    
    # 1. Coarse Sampling
    # We sample the grid using aggregate queries to find high-density areas.
    # For simplicity in this template, we'll probe cells.
    # In a real competition, we'd use 'q k' on blocks.
    
    step = 2
    for r in range(0, H, step):
        for c in range(0, W, step):
            # Query single cell to find oil
            print(f"q 1 {r} {c}")
            sys.stdout.flush()
            
            res = sys.stdin.readline().split()
            if not res:
                break
            # Response: val (where val > 0 indicates oil presence/signal)
            val = int(res[0])
            if val > 0:
                # If we find a signal, we check the immediate neighborhood
                # to find the actual polyomino cells.
                for dr in range(-2, 3):
                    for dc in range(-2, 3):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < H and 0 <= nc < W:
                            print(f"q 1 {nr} {nc}")
                            sys.stdout.flush()
                            res_n = sys.stdin.readline().split()
                            if res_n and int(res_n[0]) > 0:
                                discovered_oil.add((nr, nc))

    # 2. Refinement (Heuristic)
    # In a real scenario, we'd match the discovered cells against the 'shapes' list.
    # For this implementation, we'll assume the discovered_oil set is our best guess.
    # To avoid over-querying, we limit the search.
    
    # 3. Final Submission
    # Format: a k x1 y1 x2 y2 ...
    oil_list = list(discovered_oil)
    k = len(oil_list)
    if k == 0:
        # Submit nothing if nothing found
        print("a 0")
    else:
        out = [f"a {k}"]
        for r, c in oil_list:
            out.append(f"{r} {c}")
        print(" ".join(out))
    sys.stdout.flush()

if __name__ == "__main__":
    solve()
